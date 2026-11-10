# Changelog

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
