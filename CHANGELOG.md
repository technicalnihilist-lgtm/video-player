# Changelog

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
