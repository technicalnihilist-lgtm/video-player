# Optimization backlog — 1 to 20 November

Standing rules live in [AUTOMATION.md](AUTOMATION.md). Ten items per day, one release per day,
and **no visible change to the app** — fixes, performance, memory, robustness and accessibility only.

Tick items as they are done and append to the progress log at the bottom.

## Day 1 · 2026-11-01 · Memory & leaks

- [ ] Revoke object URLs (`URL.revokeObjectURL`) for a video's blob when it is deleted, and when the app tears down.
- [ ] Free the temporary `<video>` element used for thumbnail generation: clear `src`, drop listeners, `load()` to release the decoder.
- [ ] Register `navigator.mediaSession` metadata/action handlers once, not on every player open (duplicate listeners accumulate today).
- [ ] Clear the player's `src` and `load()` on close so the decoder and buffers are released between videos.
- [ ] Guard `openP()` against a missing/undefined item url instead of throwing.
- [ ] Make sure the undo-delete path cannot reinsert a stale item after the toast expires.
- [ ] Remove ripple `<span>` nodes reliably even if the player closes mid-animation.
- [ ] Stop the toast action button from lingering in the DOM after the toast hides.
- [ ] Release the wake lock on any player error path, not only on a clean close.
- [ ] Stress check: add and delete 20 videos, then confirm no detached nodes / listeners keep growing.

## Day 2 · 2026-11-02 · Playback correctness

- [ ] Seek bar resolution: `max=1000` quantises to ~7 s per step on a 2-hour video — raise the step resolution.
- [ ] Handle the video `error` event (unsupported codec / unreadable file) with a clear message instead of a black screen.
- [ ] Wrap the `currentTime = 1e101` duration probe in try/catch for engines that throw.
- [ ] Guard against NaN/Infinity duration everywhere duration is formatted or compared.
- [ ] Fix `onended` when auto-next is on but the next item has no usable url.
- [ ] Check loop + ended interaction: a looping video must not trigger auto-next.
- [ ] Clamp `playbackRate` back to 1 (or the last valid value) when opening a new video.
- [ ] Do not restore a saved position when the duration is still unknown or the saved value is past the end.
- [ ] Bound `skip()` when duration is unknown or 0.
- [ ] After playback ends, controls must stay visible and the play button must show the right icon.

## Day 3 · 2026-11-03 · Input responsiveness

- [ ] Throttle `timeupdate` DOM writes to one rAF per frame instead of every event (4–10 Hz today).
- [ ] Batch tilt CSS-variable writes into a single rAF per pointer move.
- [ ] Cache the card's bounding rect on pointer-enter / resize instead of calling `getBoundingClientRect()` on every move.
- [ ] Clear tilt state on `pointercancel` and when the pointer leaves the window.
- [ ] Remove layout thrash from the pointer path (no reads after writes in the same frame).
- [ ] Debounce or rAF-throttle the `resize` / orientation handler.
- [ ] Audit every listener for `{passive:true}` where the handler never calls `preventDefault`.
- [ ] Review single-tap vs double-tap timing so a slow double tap still seeks.
- [ ] Hold-to-2× must restore the previous rate if the player closes mid-hold.
- [ ] Scrubbing while paused must not auto-resume playback.

## Day 4 · 2026-11-04 · Settings & persistence

- [ ] Debounce `save()` — it currently stringifies and writes localStorage on every slider `input` event.
- [ ] Skip the write when the serialised state has not changed.
- [ ] Clamp restored values (depth, tilt, parallax, transparency, blur) to the slider's min/max on load.
- [ ] Handle corrupted or partial saved JSON without losing the rest of the settings.
- [ ] Swallow `QuotaExceededError` / private-mode storage failures without breaking the UI.
- [ ] Apply the saved theme before first paint so a light-mode user never sees a dark flash.
- [ ] Restore settings before the splash finishes so the first frame is already correct.
- [ ] Verify toggles and sliders reflect restored values exactly after a reload.
- [ ] Make sure a settings change never triggers a full re-render of the library.
- [ ] Confirm the depth/tilt engine applies restored values on boot without replaying the entry animation.

## Day 5 · 2026-11-05 · Rendering & DOM

- [ ] Render incrementally: append/remove single cards instead of rebuilding the whole grid on every add or delete.
- [ ] Reuse existing card nodes so unrelated cards do not re-run their entry animation.
- [ ] Keep tilt/parallax state across a re-render.
- [ ] Toggle the empty state without touching the grid when only visibility changes.
- [ ] Batch class changes to avoid repeated style recalculation.
- [ ] Profile a 100-item library and remove the biggest per-frame cost.
- [ ] Keep scroll smooth with the glass blur on screen (measure, then cut work if needed).
- [ ] Ensure the delete animation cannot leave a half-removed node in the grid.
- [ ] Avoid re-creating the duration/size text nodes on every render.
- [ ] Check that adding 20 files at once does not block the main thread for long.

## Day 6 · 2026-11-06 · Player teardown & power

- [ ] Release decoder resources on close and on app pause (visibilitychange).
- [ ] Suspend the AudioContext after a short idle so tap sounds stop draining battery.
- [ ] Release the wake lock on pause and re-acquire on play.
- [ ] Stop the orientation listener work while the player is closed.
- [ ] Stop the gyro listener while the page is hidden.
- [ ] Avoid backdrop-filter work for hidden player controls.
- [ ] Resume cleanly after returning from background without a stuck paused state.
- [ ] Handle audio focus loss / another app taking over (best effort, no crash).
- [ ] Verify 10 open/close cycles do not grow memory or listener count.
- [ ] Make sure closing the player always leaves the library in a consistent state.

## Day 7 · 2026-11-07 · Accessibility

- [ ] Give every range input an accessible name (aria-label) — depth, tilt, parallax, transparency, blur, seek.
- [ ] Add `aria-pressed` to the appearance segment buttons and the loop/mute toggles.
- [ ] Make toasts announce politely (`aria-live`) without stealing focus.
- [ ] Ensure keyboard focus is visible on all buttons and sliders.
- [ ] Fix tab order through the player controls.
- [ ] Keyboard shortcuts must not fire while the settings page is open.
- [ ] Expose current slider values as text for screen readers (aria-valuetext).
- [ ] Give every icon-only button a distinct accessible name.
- [ ] Measure contrast of secondary text and fix only if it fails without changing the palette.
- [ ] Honour `prefers-reduced-motion` in the JS tilt/parallax engine, not just in CSS.

## Day 8 · 2026-11-08 · Back button & history

- [ ] Audit every `pushState` and `history.back()` pair for balance.
- [ ] Guard `popstate` so a fast double-back cannot desync the player/sheet state.
- [ ] Closing the player with the in-app button and with the hardware back must behave identically.
- [ ] Opening the speed sheet from the player and backing out must return to the player, not the library.
- [ ] Back after an undo-delete must not reopen the deleted video.
- [ ] Back while native fullscreen is active must exit fullscreen only.
- [ ] Prevent history spam when the same video is opened repeatedly.
- [ ] Restore the correct screen after a `popstate` triggered from outside the app.
- [ ] Define and verify what back does on the settings tab.
- [ ] Write down the expected back-navigation matrix and check it case by case.

## Day 9 · 2026-11-09 · Stability & error handling

- [ ] Add a global `error` / `unhandledrejection` guard that surfaces a non-blocking message instead of dying silently.
- [ ] Wrap WebView-only APIs (wake lock, PiP, fullscreen, orientation lock) so failures are always caught.
- [ ] Guard every `querySelector` that could be null at that moment.
- [ ] Make thumbnail generation defensive: cancel it if the item was deleted mid-generation.
- [ ] Clean up all timers (meta timeout, hide timer, toast timer, hold timer) on teardown.
- [ ] Handle adding the same file twice without corrupting the list.
- [ ] Handle very long file names and non-ASCII names without layout breakage.
- [ ] Handle a zero-byte or non-video file dropped on the app.
- [ ] Make sure a failure in one video never blocks the rest of the library.
- [ ] Re-test the whole add → play → seek → delete path with a deliberately broken file.

## Day 10 · 2026-11-10 · CI & delivery

- [ ] Add a verify step to the workflow: extract the inline script and run `node --check` before Gradle.
- [ ] Add an APK sanity check: unzip and confirm `assets/index.html`, manifest and icons are present.
- [ ] Skip the build for docs-only pushes (`paths-ignore`) to stop wasting CI minutes.
- [ ] Cache Gradle between runs to shorten build time.
- [ ] Automate the release: on a version tag, publish a release and attach the APK from CI.
- [ ] Fail the build if the JS does not parse.
- [ ] Keep exactly one APK in each release so store auto-pick keeps working.
- [ ] Generate release notes from the CHANGELOG section for the tag.
- [ ] Document the versioning scheme in the README.
- [ ] Verify the whole chain once end to end with a throwaway tag.

## Day 11 · 2026-11-11 · CSS performance

- [ ] Audit for animated properties that force paint (box-shadow, backdrop-filter) instead of compositing.
- [ ] Scope `will-change` to interaction time only.
- [ ] Consolidate duplicated rules and drop anything unused.
- [ ] Add paint containment where it is safe and provably invisible.
- [ ] Reduce the number of stacked blur layers on low-memory devices (deviceMemory / hardwareConcurrency).
- [ ] Check the cost of the three animated background blobs and cut it if it is measurable.
- [ ] Make sure no selector does more work than it needs (deep descendant chains).
- [ ] Measure style recalc and paint counts before/after.
- [ ] Keep the light and dark palettes byte-identical in outcome.
- [ ] Confirm nothing in this pass changes a single computed visual property.

## Day 12 · 2026-11-12 · Video pipeline

- [ ] Set a sensible preload strategy for the player element.
- [ ] Never decode two videos at once (thumbnail pass while playback is running).
- [ ] Limit concurrent thumbnail generation to one at a time.
- [ ] Cap thumbnail dimensions and quality to keep memory flat.
- [ ] Handle rotation metadata: a portrait clip flagged landscape must still be framed correctly.
- [ ] Handle 10-bit/HDR or unsupported codecs with a clear message rather than a black frame.
- [ ] Test mp4, webm and mkv inputs and record what actually plays.
- [ ] Make duration probing cheaper for large files.
- [ ] Free the probe element immediately after the thumbnail is taken.
- [ ] Confirm the library still shows correct thumbnails and durations after all of the above.

## Day 13 · 2026-11-13 · Gesture polish

- [ ] Clamp ripple position so it never renders outside the viewport.
- [ ] Make double-tap seek zones sane on very narrow screens.
- [ ] Use pointer capture while scrubbing so a finger sliding off the bar keeps control.
- [ ] Ensure hold-to-2× never fights a vertical scroll on the library.
- [ ] Prevent text selection / callout on long press without breaking buttons.
- [ ] Make sure gestures do not double-fire on touch devices that also emit mouse events.
- [ ] Verify tap-to-toggle-controls still works while the video is paused.
- [ ] Check that tilt does not trigger on scroll-only gestures.
- [ ] Confirm the seek thumb does not jump when touched.
- [ ] Re-test every gesture on a 320 px wide viewport.

## Day 14 · 2026-11-14 · State robustness

- [ ] Establish one source of truth for player state and remove duplicated flags.
- [ ] Make `S.cur` impossible to leave stale after a delete.
- [ ] Restore position on reopen, clear it when playback ends.
- [ ] Auto-next must respect loop and must not fire twice.
- [ ] Speed must reset on open and never carry over silently.
- [ ] Validate the items array on restore paths.
- [ ] Guard index maths in delete/undo against off-by-one errors.
- [ ] Make closing the player idempotent.
- [ ] Ensure the player never shows a title from a previous video.
- [ ] Run a scripted sequence of 30 mixed actions and assert the final state.

## Day 15 · 2026-11-15 · Layout & safe areas

- [ ] Verify safe-area insets on a notched/rounded device profile.
- [ ] Check landscape safe areas around the player controls.
- [ ] Ensure the tab bar never covers content at short viewport heights.
- [ ] Check the player controls in landscape on a small screen.
- [ ] Check settings scrolling with the on-screen keyboard open.
- [ ] Verify a 320 px wide viewport does not clip labels.
- [ ] Check tablet and foldable widths.
- [ ] Confirm long titles ellipsise instead of wrapping.
- [ ] Sanity check RTL: no broken layout, no mirrored icons where it matters.
- [ ] Fix only breakage — no cosmetic adjustments.

## Day 16 · 2026-11-16 · Code quality

- [ ] Split the inline script into clearly commented sections (no behaviour change).
- [ ] Remove dead code and unused helpers.
- [ ] Deduplicate repeated DOM lookups into cached references.
- [ ] Give the helpers consistent names and arguments.
- [ ] Document the non-obvious parts (tilt maths, history contract, thumbnail probe).
- [ ] Ensure no console noise is left in production paths.
- [ ] Run a lightweight lint pass and fix real issues only.
- [ ] Keep the single-file structure and its size reasonable.
- [ ] Prove behaviour is unchanged by diffing computed styles and smoke-test output before/after.
- [ ] Record the before/after numbers in the day's notes.

## Day 17 · 2026-11-17 · Regression harness

- [ ] Add `tools/smoke.mjs`: a headless script that loads the page, adds a video, plays, seeks, changes settings, deletes, and asserts invariants.
- [ ] Assert no console errors and no unhandled rejections during the run.
- [ ] Assert the DOM node count returns to baseline after delete.
- [ ] Wire the smoke check into CI as a required step.
- [ ] Keep the check under a minute.
- [ ] Print timings so day-over-day regressions are visible.
- [ ] Cover the tilt/parallax engine toggles in the check.
- [ ] Cover the seek precision assertion.
- [ ] Cover the back-navigation matrix.
- [ ] Document how to run it locally.

## Day 18 · 2026-11-18 · Android shell hardening

- [ ] Handle a cancelled file picker without leaving the callback dangling.
- [ ] Handle `onActivityResult` with null data.
- [ ] Pause/resume the WebView video on app pause/resume.
- [ ] Keep the screen on while a video is playing.
- [ ] Destroy the WebView cleanly and free its data on exit.
- [ ] Verify fullscreen entry/exit from the hardware back button.
- [ ] Check the status bar / cutout behaviour is unchanged visually.
- [ ] Review the manifest for anything unnecessary.
- [ ] Confirm no new permissions were added (must stay without INTERNET).
- [ ] Static-review the shell and note anything that needs a real device to confirm.

## Day 19 · 2026-11-19 · Final sweep

- [ ] Re-read the whole HTML file end to end for leftovers.
- [ ] Verify every earlier backlog item still holds after later changes.
- [ ] Re-run the full smoke check and the 100-item performance check.
- [ ] Confirm the screenshots still match the app exactly.
- [ ] Confirm the store listing text is still accurate.
- [ ] Check the APK size has not crept up.
- [ ] Remove any temporary debugging aids.
- [ ] Do a final performance profile and record it.
- [ ] Confirm no release has more than one APK.
- [ ] List anything still open for the user's decision.

## Day 20 · 2026-11-20 · Release & handover

- [ ] Ship the final version with a consolidated changelog of the 20 days.
- [ ] Add a short quality/performance section to the README.
- [ ] Verify the final APK from a clean CI run.
- [ ] Double-check versionCode/versionName monotonicity.
- [ ] Confirm the release page and assets are correct.
- [ ] Confirm the store-facing metadata still matches the app.
- [ ] Write the handover summary: what improved, what is left.
- [ ] Recommend pausing or deleting this daily schedule.
- [ ] Archive the completed backlog with dates.
- [ ] Final report to the user.

## Progress log

| Day | Date | Version | Items done | Notes |
| --- | --- | --- | --- | --- |
| 1 | 2026-11-01 | — | 0/10 | Memory & leaks |
| 2 | 2026-11-02 | — | 0/10 | Playback correctness |
| 3 | 2026-11-03 | — | 0/10 | Input responsiveness |
| 4 | 2026-11-04 | — | 0/10 | Settings & persistence |
| 5 | 2026-11-05 | — | 0/10 | Rendering & DOM |
| 6 | 2026-11-06 | — | 0/10 | Player teardown & power |
| 7 | 2026-11-07 | — | 0/10 | Accessibility |
| 8 | 2026-11-08 | — | 0/10 | Back button & history |
| 9 | 2026-11-09 | — | 0/10 | Stability & error handling |
| 10 | 2026-11-10 | — | 0/10 | CI & delivery |
| 11 | 2026-11-11 | — | 0/10 | CSS performance |
| 12 | 2026-11-12 | — | 0/10 | Video pipeline |
| 13 | 2026-11-13 | — | 0/10 | Gesture polish |
| 14 | 2026-11-14 | — | 0/10 | State robustness |
| 15 | 2026-11-15 | — | 0/10 | Layout & safe areas |
| 16 | 2026-11-16 | — | 0/10 | Code quality |
| 17 | 2026-11-17 | — | 0/10 | Regression harness |
| 18 | 2026-11-18 | — | 0/10 | Android shell hardening |
| 19 | 2026-11-19 | — | 0/10 | Final sweep |
| 20 | 2026-11-20 | — | 0/10 | Release & handover |
