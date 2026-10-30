# Changelog

## 1.0.2

- **Fixed:** the launcher icon rendered as a plain white circle instead of the glass disc with a play glyph. Regenerated all launcher icon sizes (and the round variant), plus the store icon at `docs/icon.png`.

## 1.0.1

- **Fixed:** a landscape video played in portrait was stretched to fill the tall screen, squashing the picture. `Stretch to fill screen` now only applies while the device is actually in landscape; in portrait the video is letterboxed at its correct aspect ratio. Landscape playback is unchanged — still edge to edge, no black bars.
- Updated the helper text under `Stretch to fill screen` so it says when it applies.
- Refreshed the player screenshot and added a landscape screenshot.

## 1.0.0

- First release: Glass Player UI packaged as an Android APK (WebView shell, fully offline, no `INTERNET` permission).
