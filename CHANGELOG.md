# Changelog

## 1.0.9

Maintenance release: the picture is unchanged, but the library no longer rebuilds itself from scratch every time you add or delete a video.

- **Adding or deleting one video no longer rebuilds the whole library.** The grid used to be emptied and every card recreated on every change, so a library of 100 videos paid 100 cards of work for one file. Each card is now tied to its video and reused: only the card that actually changed is created, patched or removed. On a 100-video library a re-render went from **96 ms to 0.1 ms**, and adding one video now creates **2 elements instead of 102**; the other 100 cards are left untouched.
- **Cards that are already on screen no longer re-play their entrance animation** when another video is added or removed. A newly added card still enters with exactly the same delay it had before.
- **Fixed:** a card that was mid-way through its delete animation used to be dropped instantly if the library re-rendered underneath it, so the card vanished without its animation. It now finishes its animation and then leaves.
- **Fixed:** a delete whose video had already left the list could leave a half-removed card sitting in the grid, and a second tap on a card that was already being deleted could queue a second removal. Both cases are guarded now: the card always leaves the grid, once.
- **The tilt/parallax state survives a change.** Because cards are reused, a card that is being tilted keeps its tilt when you add or delete a different video; only references to cards that really left the grid are dropped.
- **The playback clock does less work per frame.** The two time labels were looked up by selector on every animation frame; they are cached now, so a playing video costs one style write and at most one text write per frame.
- **The empty state is toggled without touching the grid**, and a render where nothing changed now does literally nothing instead of rebuilding 100 cards.
- **Bulk adds go in as one insertion.** Twenty files chosen at once are placed in the grid in a single DOM insertion rather than one per file, so the main thread yields between files instead of reflowing the grid twenty times.
- **Nothing visible changed** — the stylesheet and the page markup are byte-identical to 1.0.8; only the inline script differs. The one thing you could notice is deliberate and is what this pass was for: cards already on screen stay put instead of animating again.
- Not measurable here: the paint and compositor cost of the glass blur cannot be timed in a headless run. The JavaScript-side cost that used to force every blurred layer to be re-rasterised on each change is gone (one card repainted instead of all of them), but the on-device blur cost itself was left alone — trimming blur layers by device memory is scheduled for the CSS performance pass.

## 1.0.8

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

## 1.0.7

Maintenance release: the picture is unchanged, but taps, drags and scrubbing are handled far more cheaply.

- **The player clock costs one frame instead of ten writes.** The playback clock and the time labels were rewritten on every `timeupdate` event (4–10 a second); they are now painted once per animation frame, and a label is only touched when its text actually changed.
- **4D tilt no longer measures a card on every finger move.** The card's box was read with `getBoundingClientRect()` on every `pointermove`, which forces the page to re-lay out for each event. The box is now measured once when the pointer enters a card, and refreshed when the page scrolls, the window resizes or the library re-renders. Twelve moves over one card cost one layout read instead of twelve.
- **Tilt writes are batched** into a single animation frame per pointer move, and layout is read before anything is written, so no frame mixes the two.
- **Fixed:** the tilt effect could stay stuck on a card after the finger was cancelled or dragged off the window, and after the app lost focus. It now clears on `pointercancel`, when the pointer leaves the window and on window blur.
- **Resize and rotation are throttled** to one orientation check per frame instead of one per event.
- **Fixed:** a slightly slow double tap toggled the controls before it seeked, because the single-tap action fired at 300 ms while a double tap was still accepted up to 320 ms. The single-tap delay is now longer than the double-tap window, so a double tap always seeks cleanly and a single tap still toggles the controls.
- **Fixed:** a 2× hold whose timer was still pending when the player closed could set the next video to double speed and show the 2× badge on a closed player.
- **Fixed:** a scrub can no longer leave a paused video playing, and a drag that is cancelled no longer leaves the seek bar stuck in its dragging state — which used to freeze the clock for the rest of the video.
- **Scrolling and window events are declared passive** where the app never cancels the gesture (tap sound, tilt, gyro, resize, orientation, scroll), so they cannot hold up the scroll or the compositor.
- **Nothing visible changed** — the stylesheet and the page markup are byte-identical to 1.0.6; only the inline script differs. The one timing value that moved is the internal single-tap delay, which is imperceptible and only affects when the controls toggle after a tap.

## 1.0.6

Maintenance release: the picture is unchanged, but playback is now correct at the edges.

- **Seeking is precise.** The seek bar used to move in steps of about 7 seconds on a two-hour video; it now resolves to under a second, so a tap lands where you aimed.
- **A video that cannot be played says so.** An unsupported codec or a file that is no longer readable used to leave a black screen with no explanation; it now shows a short message and puts the controls back on screen.
- **A looping video no longer jumps to the next one** when it reaches the end.
- **Play next skips items whose file is gone** instead of opening a player with nothing in it, and when the queue is finished the controls stay up with the play button showing correctly.
- **Fixed:** the duration probe (the trick some engines need before they report a real length) could throw on engines that clamp the seek, and its listener was never removed. It is guarded now, settles exactly once, and gives up after two seconds.
- **Fixed:** an unknown or infinite duration could show `NaN` on the clock or make the seek bar and the 10-second skip buttons misbehave. Every duration read is now validated.
- **Fixed:** a saved position is only restored once the length is known and the position is inside the file, so a video can no longer open near its end or before its first frame.
- **Fixed:** the clock and the seek bar no longer show the previous video's time for a moment when you open a new one.
- **Fixed:** a 2× hold that was still running when the player closed could leave the next video playing at double speed.
- **Fixed:** the thumbnail step no longer tries to draw a frame from a video that never decoded.
- **Nothing visible changed** — the stylesheet is byte-identical to 1.0.5; the only markup change is the seek bar's internal step resolution, which does not alter how it looks.

## 1.0.5

Maintenance release: nothing looks any different, but the app now lets go of memory properly.

- **Deleted videos are released.** Removing a video from the library frees the memory it was holding instead of keeping it until the app closes. Undo still works — the file is only freed once the undo toast has gone, and everything is freed when the app shuts down.
- **The player frees its decoder when you close a video**, so opening one video after another no longer piles up decoders and buffers in the background.
- **The thumbnail step cleans up after itself.** It no longer leaves a hidden video element (and its decoder) alive once the duration and thumbnail are in — or after its 4-second timeout.
- **Fixed:** the system media controls were being registered again for every video you opened. They are now registered once.
- **Fixed:** the undo button and the tap-ripple markers no longer stay behind in the page after the toast has faded, or when the player is closed mid-animation.
- **Fixed:** the screen wake lock is handed back if a video fails to load, not only when you close the player normally.
- **Fixed:** opening a video whose file is no longer available no longer throws an error; it simply does nothing.
- **Fixed:** deleting a second video no longer keeps the first deleted one's memory alive, and undo can no longer bring back a video whose file has already been released.
- **Nothing visible changed** — colours, spacing, layout, blur, shadows, animation timing, wording and icons are untouched; the stylesheet and markup are byte-identical to 1.0.4.
- Added `tools/stress-memory.mjs`: a headless check that adds and deletes 20 videos and asserts that no nodes, listeners or blob URLs are left behind.

## 1.0.4

- **Depth, tilt and parallax are now adjustable separately.** Settings has three independent sliders instead of one:
  - **Depth strength** — shadow depth under every panel
  - **Tilt angle** — how far a card leans toward your finger and the phone
  - **Parallax** — how much the thumbnail, title and highlight separate from each other
- All three save between sessions, so a look you dial in stays.
- Slider rows no longer squeeze when the label runs to two lines.

## 1.0.3

- **Added: depth effect.** Panels now sit on layered depth — a contact shadow, a wide ambient shadow and a lit glass edge — so they read as solid glass slabs instead of flat sheets. Cards lift off the page and swing up out of the screen as they appear.
- **Added: 4D tilt.** Cards lean toward your finger and follow the way you hold the phone, with real parallax between the thumbnail, the title and the specular highlight that tracks the light across the glass. The backdrop shifts against the content as the phone moves.
- Both are switchable in Settings, with a **Depth strength** slider (0–100) that controls shadow depth and tilt amount.
- Small icon buttons keep a tighter, crisper shadow so controls stay readable over video.
- Refreshed all screenshots.

## 1.0.2

- **Fixed:** the launcher icon rendered as a plain white circle instead of the glass disc with a play glyph. Regenerated all launcher icon sizes (and the round variant), plus the store icon at `docs/icon.png`.

## 1.0.1

- **Fixed:** a landscape video played in portrait was stretched to fill the tall screen, squashing the picture. `Stretch to fill screen` now only applies while the device is actually in landscape; in portrait the video is letterboxed at its correct aspect ratio. Landscape playback is unchanged — still edge to edge, no black bars.
- Updated the helper text under `Stretch to fill screen` so it says when it applies.
- Refreshed the player screenshot and added a landscape screenshot.

## 1.0.0

- First release: Glass Player UI packaged as an Android APK (WebView shell, fully offline, no `INTERNET` permission).
