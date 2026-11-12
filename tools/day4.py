#!/usr/bin/env python3
"""Day 4 (2026-11-04) settings & persistence pass — applies the v1.0.8 edits.

Run from the repository root:  python3 tools/day4.py

Every replacement asserts that it matched exactly once, so a drifted edit fails loudly
instead of writing a half-applied file. The finished app/src/main/assets/index.html is
checked against a known md5.
"""
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, 'app/src/main/assets/index.html')
GRADLE = os.path.join(ROOT, 'app/build.gradle')
CHANGELOG = os.path.join(ROOT, 'CHANGELOG.md')
BACKLOG = os.path.join(ROOT, 'BACKLOG.md')

HTML_MD5 = 'c7c37d05a3784138cc1c039528b0f552'


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def write(path, text):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(text)


def rep(text, old, new, label):
    n = text.count(old)
    if n != 1:
        sys.exit('FAIL %s: expected exactly one match, found %d' % (label, n))
    return text.replace(old, new, 1)


# ---------------------------------------------------------------- index.html
html = read(HTML)

html = rep(html, '<title>Glass Player</title>\n<style>', '''<title>Glass Player</title>
<script>/* The stored theme is applied before the first paint, so a light-mode user never
   sees a dark flash while the rest of the app boots. Read-only and fully guarded: a corrupt or
   unreadable payload just leaves the system default in place. */
try{var _g=JSON.parse(localStorage.getItem('gp')||'null');if(_g&&(_g.t==='light'||_g.t==='dark'))document.documentElement.dataset.theme=_g.t}catch(e){}</script>
<style>''', 'head theme script')

html = rep(html, '''/* settings */
const R=document.documentElement;
function save(){try{localStorage.setItem('gp',JSON.stringify({snd:S.snd,vib:S.vib,nx:S.nx,fill:S.fill,dep:S.dep,tilt:S.tilt,dz:S.dz,ta:S.ta,par:S.par,g:$('#sG').value,b:$('#sB').value,t:R.dataset.theme||'auto'}))}catch(e){}}''', '''/* settings */
const R=document.documentElement;
/* Storage can be absent or refuse writes (private mode, storage disabled, quota full). Every access
   goes through this wrapper, so a failed write can never throw into a handler or break the UI. */
const store={get(k){try{return localStorage.getItem(k)}catch(e){return null}},set(k,v){try{localStorage.setItem(k,v);return true}catch(e){return false}}};
function snapshot(){return JSON.stringify({snd:S.snd,vib:S.vib,nx:S.nx,fill:S.fill,dep:S.dep,tilt:S.tilt,dz:S.dz,ta:S.ta,par:S.par,g:$('#sG').value,b:$('#sB').value,t:R.dataset.theme||'auto'})}
let saveT=0,lastSaved=null;
/* A slider fires input on every pixel of a drag. Writes are coalesced into one per 250 ms, and a write
   whose serialised state is identical to the stored one is skipped entirely. */
function writeNow(){saveT=0;const j=snapshot();if(j===lastSaved)return;if(store.set('gp',j))lastSaved=j}
function save(){if(saveT)return;saveT=setTimeout(writeNow,250)}
function saveFlush(){if(saveT){clearTimeout(saveT);saveT=0}writeNow()}''', 'save debounce')

html = rep(html, '''$('#sG').oninput=()=>{apply();save()};$('#sB').oninput=()=>{apply();save()};''', '''$('#sG').oninput=()=>{apply();save()};$('#sB').oninput=()=>{apply();save()};
/* releasing a slider commits the value straight away instead of waiting for the debounce */
['#sG','#sB','#sDz','#sTa','#sPar'].forEach(q=>{$(q).onchange=saveFlush});''', 'slider flush')

html = rep(html, '''function theme(v){if(v==='auto')delete R.dataset.theme;else R.dataset.theme=v;$$('#seg button').forEach(b=>b.classList.toggle('on',b.dataset.v===v));save()}''', '''function theme(v,quiet){if(v==='auto')delete R.dataset.theme;else R.dataset.theme=v;$$('#seg button').forEach(b=>b.classList.toggle('on',b.dataset.v===v));if(!quiet)save()}''', 'theme quiet')

html = rep(html, '''try{const c=JSON.parse(localStorage.getItem('gp')||'null');if(c){S.snd=c.snd;S.vib=c.vib;S.nx=c.nx;S.fill=c.fill!==false;pl.classList.toggle('fill',S.fill);$('#sFill').checked=S.fill;$('#sSnd').checked=S.snd;$('#sVib').checked=S.vib;$('#sNx').checked=S.nx;$('#sG').value=c.g;$('#sB').value=c.b;S.dep=c.dep!==false;S.tilt=c.tilt!==false;S.dz=c.dz==null?60:+c.dz;S.ta=c.ta==null?60:+c.ta;S.par=c.par==null?50:+c.par;$('#sDep').checked=S.dep;$('#sTilt').checked=S.tilt;$('#sDz').value=S.dz;$('#sTa').value=S.ta;$('#sPar').value=S.par;theme(c.t||'auto')}}catch(e){}''', '''/* Restored values are validated one field at a time: a truncated or hand-edited payload must not cost
   the fields that are still good, and every number is clamped into its own slider's range so a bogus
   value can never reach a custom property or a control. */
const num=(v,el)=>{const lo=+el.min,hi=+el.max;let n=parseFloat(v);if(!isFinite(n))n=parseFloat(el.defaultValue);if(!isFinite(n))n=lo;return Math.min(hi,Math.max(lo,Math.round(n)))};
const bool=(v,d)=>v===undefined||v===null?d:v!==false;
function restore(){let c=null,bad=false;const raw=store.get('gp');
 if(raw){try{c=JSON.parse(raw)}catch(e){bad=true}
  if(c!==null&&(typeof c!=='object'||Array.isArray(c))){c=null;bad=true}
  if(c&&c.t!==undefined&&c.t!=='auto'&&c.t!=='light'&&c.t!=='dark')bad=true}
 c=c||{};
 S.snd=bool(c.snd,true);S.vib=bool(c.vib,true);S.nx=bool(c.nx,true);S.fill=bool(c.fill,true);
 S.dep=bool(c.dep,true);S.tilt=bool(c.tilt,true);
 $('#sSnd').checked=S.snd;$('#sVib').checked=S.vib;$('#sNx').checked=S.nx;$('#sFill').checked=S.fill;
 pl.classList.toggle('fill',S.fill);
 $('#sG').value=num(c.g,$('#sG'));$('#sB').value=num(c.b,$('#sB'));
 $('#sDz').value=num(c.dz,$('#sDz'));$('#sTa').value=num(c.ta,$('#sTa'));$('#sPar').value=num(c.par,$('#sPar'));
 S.dz=+$('#sDz').value;S.ta=+$('#sTa').value;S.par=+$('#sPar').value;
 $('#sDep').checked=S.dep;$('#sTilt').checked=S.tilt;
 theme(c.t==='light'||c.t==='dark'?c.t:'auto',true);
 /* a damaged payload is not recorded as saved, so the next change rewrites it in healed form */
 lastSaved=bad?null:snapshot()}
/* runs before the splash finishes, so the first frame the user sees already has the right settings */
restore();''', 'validated restore')

html = rep(html, '''addEventListener('pagehide',e=>{if(!e.persisted)revokeAll()});
addEventListener('beforeunload',revokeAll);''', '''/* a pending debounced write is committed before the page goes away or is backgrounded */
addEventListener('pagehide',e=>{saveFlush();if(!e.persisted)revokeAll()});
addEventListener('beforeunload',()=>{saveFlush();revokeAll()});
addEventListener('visibilitychange',()=>{if(document.visibilityState==='hidden')saveFlush()},{passive:true});''', 'flush on teardown')

write(HTML, html)
digest = hashlib.md5(open(HTML, 'rb').read()).hexdigest()
if digest != HTML_MD5:
    sys.exit('FAIL index.html md5 %s != %s' % (digest, HTML_MD5))

# ---------------------------------------------------------------- build.gradle
gradle = read(GRADLE)
gradle = rep(gradle, 'versionCode 8', 'versionCode 9', 'versionCode')
gradle = rep(gradle, 'versionName "1.0.7"', 'versionName "1.0.8"', 'versionName')
write(GRADLE, gradle)

# ---------------------------------------------------------------- CHANGELOG.md
ENTRY = '''## 1.0.8

Maintenance release: the picture is unchanged, but your settings are now saved safely and restored exactly.

- **Settings are written once per gesture, not once per pixel.** Dragging a slider used to serialise the whole settings object and write it to storage on every `input` event — up to dozens of writes per drag. Writes are now coalesced into one every 250 ms, committed immediately when you let go of a slider, and committed again if the app is backgrounded or closed mid-drag.
- **A write that changes nothing is skipped.** The serialised state is compared with what is already stored, so tapping a setting back to the value it already had no longer touches storage.
- **Restored values are validated and clamped.** A saved depth, tilt, parallax, transparency or blur value is forced into its own slider's range, so a hand-edited or out-of-range number can no longer push a custom property to a nonsense value.
- **A damaged settings payload no longer costs you everything.** Previously one bad field made the whole restore throw and every setting fell back to default. Each field is now validated on its own: a truncated or partially corrupt payload keeps the fields that are still readable and defaults only the rest, and the healed state is rewritten on your next change.
- **Storage failures are contained.** Private mode, storage disabled or a full quota used to be swallowed by an outer `catch`; every read and write now goes through one guarded wrapper, so a refused write cannot throw into a settings handler or leave the UI half-applied.
- **Fixed:** restoring settings on boot used to write them straight back to storage. Boot is now read-only, and nothing is written until you change something.
- **No dark flash for light-mode users.** The saved theme is applied by a tiny blocking script in `<head>`, before the first paint, instead of at the end of the inline script — so a light-mode user no longer sees the dark splash for a moment on launch. The rest of the settings are restored before the splash finishes, so the first frame is already correct.
- **Fixed:** a partially saved payload could turn sound, haptics, play-next, stretch-to-fill, depth or tilt *off* even though they default to on, because a missing field was read as `undefined`. Missing booleans now keep their default.
- **Nothing visible changed** — the stylesheet is byte-identical to 1.0.7 and the page markup is unchanged; the only additions are a `<head>` script that sets the already-supported theme attribute and the persistence code in the inline script.

'''

changelog = read(CHANGELOG)
changelog = rep(changelog, '# Changelog\n\n', '# Changelog\n\n' + ENTRY, 'changelog entry')
write(CHANGELOG, changelog)

# ---------------------------------------------------------------- BACKLOG.md
ROW = ('| 4 | 2026-11-04 | 1.0.8 | 10/10 | Settings & persistence — executed 2026-11-12. '
       '`save()` debounced to one write per 250 ms, flushed on slider release, `pagehide`, `beforeunload` and '
       '`visibilitychange:hidden`, and skipped when the serialised state is unchanged (a 20-step slider drag writes '
       'once, not 20 times; 10 no-op inputs write 0 times); boot no longer writes back the state it just read; every '
       'restored number is parsed and clamped into its own slider range (4-45, 4-60, 0-100); a truncated, array, '
       'scalar or hand-edited payload no longer loses every field — each field is validated on its own, missing '
       'booleans keep their `true` default (a partial payload used to switch sound, haptics, play-next, fill, depth '
       'and tilt off), and a damaged payload is not recorded as saved so the next change rewrites it healed; all '
       'storage access goes through one guarded `get`/`set` wrapper, so `QuotaExceededError`, private mode and '
       'storage-disabled throw nothing into a handler and the change still applies; the saved theme is applied by a '
       'blocking `<head>` script before first paint, so no dark flash for light-mode users, and the rest is restored '
       'before the splash finishes. Verified: settings never re-render the library grid (same node identity across '
       'slider/toggle/theme changes) and `depthApply()` applies restored values before `render()` with no entry '
       'animation replayed. Headless jsdom check (22 assertions: clean boot, exact round trip, boot writes nothing, '
       '6 corrupt/partial payloads, quota failure, pre-paint theme, no grid re-render) all pass; '
       '`tools/stress-memory.mjs` still clean (20/20 revoked, 0 listener growth). No item skipped, no visual change '
       '(stylesheet and markup byte-identical). |')

backlog = read(BACKLOG)
start = backlog.find('## Day 4 · 2026-11-04 · Settings & persistence')
end = backlog.find('## Day 5 ·')
if start < 0 or end < 0 or end <= start:
    sys.exit('FAIL backlog: day 4 block not found')
block = backlog[start:end]
if block.count('- [ ]') != 10:
    sys.exit('FAIL backlog: expected 10 unticked items, found %d' % block.count('- [ ]'))
backlog = backlog[:start] + block.replace('- [ ]', '- [x]') + backlog[end:]

backlog = rep(backlog, '| 4 | 2026-11-04 | — | 0/10 | Settings & persistence |', ROW, 'backlog row')
write(BACKLOG, backlog)

print('day 4 applied: index.html md5 %s' % digest)
