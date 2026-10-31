# Changelog

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
