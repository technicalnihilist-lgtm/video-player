# Store submission details

Copy-paste values for the Orion Store "Submit an app" form (or any GitHub-based store).

## 1. Source — Repo URL

```
https://github.com/technicalnihilist-lgtm/video-player
```

## 2. Details

| Field | Value |
| --- | --- |
| Name | `Video Player` |
| Category | `Utility` (also fits `Multimedia` / `Video` if offered) |
| Author | `technicalnihilist-lgtm` |
| App ID | leave blank to let the store derive it, or use `video-player` |

## 3. Store listing

**Icon URL** (512 × 512 PNG):

```
https://raw.githubusercontent.com/technicalnihilist-lgtm/video-player/main/docs/icon.png
```

**Description:**

```
A glassmorphism video player for Android. Everything runs on-device and fully offline — the app declares no INTERNET permission at all, so your videos never leave your phone.

Pick videos straight from storage and they appear as cards with an auto-generated thumbnail and duration. Playback is gesture-first: tap to toggle the controls, double-tap the left or right side to jump 10 seconds, hold anywhere to speed up to 2x with a ripple. There is also a scrubber, ±10 s buttons, loop, mute, playback speed from 0.5x to 2x, picture-in-picture and native fullscreen.

Framing is handled properly. A landscape video fills the screen with no black bars while your phone is sideways, and is letterboxed at its true shape when you hold it upright — never stretched. Portrait videos are never stretched either, and a rotate hint appears if one is played in landscape. Playback position is remembered per video and the next video plays automatically.

The interface is real glass: an animated gradient backdrop behind live blur, with transparency and blur strength you can tune yourself. Tap sounds, haptics, autoplay-next and Auto/Light/Dark theme all persist between sessions, and deleting a video gives you an Undo toast. The Android back button closes the player, then the speed sheet, then the app.

No ads, no trackers, no network access, no account. 111 KB.
```

## 4. Release

| Field | Value |
| --- | --- |
| Package name | `com.glassplayer.app` |
| Release keyword | leave **Auto** on — every release contains exactly one APK, `Video-Player.apk` |

The latest release ([v1.0.1](https://github.com/technicalnihilist-lgtm/video-player/releases/latest)) attaches `Video-Player.apk`, so auto-pick works as-is. If you ever prefer an explicit keyword, use `Video-Player`.

## 5. Screenshots — direct image links

At least three are required; these six are live and return `image/png`:

```
https://raw.githubusercontent.com/technicalnihilist-lgtm/video-player/main/docs/screenshots/02-library.png
https://raw.githubusercontent.com/technicalnihilist-lgtm/video-player/main/docs/screenshots/03-player.png
https://raw.githubusercontent.com/technicalnihilist-lgtm/video-player/main/docs/screenshots/04-settings.png
https://raw.githubusercontent.com/technicalnihilist-lgtm/video-player/main/docs/screenshots/05-light.png
https://raw.githubusercontent.com/technicalnihilist-lgtm/video-player/main/docs/screenshots/01-empty.png
https://raw.githubusercontent.com/technicalnihilist-lgtm/video-player/main/docs/screenshots/06-landscape.png
```

Order above is the suggested store order: library, player, settings, light theme, empty state, landscape playback.

## Notes before you submit

- The APK is **debug-signed**. It installs fine and updates over itself, but some stores reject debug signatures and Google Play will not accept it. For a proper release signature, add a keystore to the repo as Actions secrets and switch `app/build.gradle` to a `signingConfigs.release` block.
- `minSdk 23` (Android 6.0+), `targetSdk 34`, `versionCode 2`, `versionName 1.0.1`.
- No `INTERNET` permission is requested, so the store's privacy section can state "no data collected, no network access".
