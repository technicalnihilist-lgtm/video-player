// Memory / leak stress check for app/src/main/assets/index.html
//
// Loads the real page in jsdom, adds 20 videos, deletes them one by one, and asserts that
// blob URLs are revoked, no detached nodes are left behind, and listener registrations do
// not grow across player open/close cycles.
//
//   node tools/stress-memory.mjs [path-to-index.html]
//
// Exits non-zero on the first failed invariant.

import fs from 'node:fs';
import path from 'node:path';
import { JSDOM, VirtualConsole } from 'jsdom';

const file = process.argv[2] || path.resolve('app/src/main/assets/index.html');
const html = fs.readFileSync(file, 'utf8');
const t0 = Date.now();

const created = new Set();
const revoked = new Set();
let seq = 0;

const vc = new VirtualConsole();
const consoleErrors = [];
vc.on('jsdomError', (e) => consoleErrors.push(String(e && e.message)));
vc.on('error', (...a) => consoleErrors.push(a.join(' ')));

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  url: 'file:///android_asset/index.html',
  virtualConsole: vc,
});
const win = dom.window;

// ---- media stubs: jsdom has no decoder, so fake just enough of one ----
const proto = win.HTMLMediaElement.prototype;
Object.defineProperty(proto, 'duration', { configurable: true, get: () => 120 });
Object.defineProperty(proto, 'videoWidth', { configurable: true, get: () => 1920 });
Object.defineProperty(proto, 'videoHeight', { configurable: true, get: () => 1080 });
Object.defineProperty(proto, 'paused', { configurable: true, get: () => true });
proto.play = function () { return Promise.resolve(); };
proto.pause = function () {};
proto.load = function () { this._src = ''; };
Object.defineProperty(proto, 'src', {
  configurable: true,
  get() { return this._src || ''; },
  set(v) {
    this._src = v;
    if (!v) return;
    setTimeout(() => {
      this.dispatchEvent(new win.Event('loadedmetadata'));
      this.dispatchEvent(new win.Event('seeked'));
    }, 0);
  },
});

// jsdom ships no canvas backend; give the thumbnail path a no-op surface so it does not spam errors
win.HTMLCanvasElement.prototype.getContext = function () {
  return { drawImage() {}, clearRect() {}, fillRect() {} };
};
win.HTMLCanvasElement.prototype.toDataURL = function () { return 'data:image/jpeg;base64,AA'; };

win.URL.createObjectURL = () => { const u = 'blob:fake-' + (++seq); created.add(u); return u; };
win.URL.revokeObjectURL = (u) => { revoked.add(u); };

// ---- count window-level listener registrations ----
let listenerCalls = 0;
const origAdd = win.addEventListener.bind(win);
win.addEventListener = (...a) => { listenerCalls++; return origAdd(...a); };

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
// top-level `const` bindings are not properties of window; reach them through global eval
const ev = (code) => win.eval(code);
const fail = [];
const ok = (cond, msg) => { if (!cond) fail.push(msg); };

function makeFile(name) {
  return { name, type: 'video/mp4', size: 2 * 1024 * 1024 };
}

const baselineNodes = win.document.getElementsByTagName('*').length;

const run = async () => {
  // ---------- add 20 ----------
  const addedAt = Date.now();
  for (let i = 0; i < 20; i++) await win.addFile(makeFile('clip-' + i + '.mp4'));
  const addMs = Date.now() - addedAt;

  const cards = () => win.document.querySelectorAll('#grid .card');
  ok(cards().length === 20, 'expected 20 cards after add, got ' + cards().length);
  ok(ev('S.items.length') === 20, 'expected 20 items after add, got ' + ev('S.items.length'));
  ok(win.document.querySelector('#empty').hidden === true, 'empty state should be hidden with items');

  const nodesWithItems = win.document.getElementsByTagName('*').length;

  // ---------- player open/close cycles ----------
  const listenersBefore = listenerCalls;
  for (let i = 0; i < 5; i++) {
    win.openP(0);
    await sleep(10);
    win.closeP();
  }
  const listenersAfter = listenerCalls;
  ok(listenersAfter === listenersBefore,
    'window listeners grew across 5 open/close cycles: +' + (listenersAfter - listenersBefore));
  ok(ev("typeof initMS === 'function'"), 'media session init helper missing');
  ok(win.document.querySelector('#rip').children.length === 0, 'ripple nodes left in #rip after close');
  ok(win.document.querySelector('#v').getAttribute('src') === null,
    'player <video> still holds a src after close (decoder not released)');

  // ---------- delete all 20, with the undo toast left to expire ----------
  const delAt = Date.now();
  const detached = [];
  for (let i = 0; i < 20; i++) {
    const card = cards()[0];
    if (!card) break;
    card.querySelector('.del').dispatchEvent(new win.MouseEvent('click', { bubbles: true }));
    await sleep(560);
    detached.push(card);
  }
  const delMs = Date.now() - delAt;

  ok(cards().length === 0, 'expected 0 cards after delete, got ' + cards().length);
  ok(ev('S.items.length') === 0, 'expected 0 items after delete, got ' + ev('S.items.length'));
  ok(win.document.querySelector('#empty').hidden === false, 'empty state should be visible with no items');
  ok(detached.every((n) => !n.isConnected), 'a deleted card is still attached to the document');

  // let the undo window (4.5 s toast + 0.4 s fade) close
  await sleep(5200);
  ok(win.document.querySelector('#toast').textContent === '', 'toast action button still in the DOM after it hid');
  ok(revoked.size === 20, 'expected 20 revoked blob URLs, got ' + revoked.size);
  ok([...created].every((u) => revoked.has(u)), 'a created blob URL was never revoked');

  const finalNodes = win.document.getElementsByTagName('*').length;
  ok(finalNodes <= baselineNodes + 4, 'node count did not return to baseline: ' + baselineNodes + ' -> ' + finalNodes);
  ok(consoleErrors.length === 0, 'console/jsdom errors during the run: ' + consoleErrors.slice(0, 3).join(' | '));

  console.log('add 20 videos      ' + addMs + ' ms');
  console.log('delete 20 videos   ' + delMs + ' ms');
  console.log('nodes   baseline ' + baselineNodes + ' -> with items ' + nodesWithItems + ' -> final ' + finalNodes);
  console.log('blob URLs created ' + created.size + ', revoked ' + revoked.size);
  console.log('window listeners added by 5 open/close cycles ' + (listenersAfter - listenersBefore));
  console.log('console errors ' + consoleErrors.length);
  console.log('total ' + (Date.now() - t0) + ' ms');

  if (fail.length) {
    console.error('\nFAILED:');
    for (const f of fail) console.error(' - ' + f);
    process.exit(1);
  }
  console.log('\nOK: all memory invariants held');
};

run().catch((e) => { console.error(e); process.exit(1); });
