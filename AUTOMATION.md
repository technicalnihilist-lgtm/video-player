# Daily optimization contract (1–20 November)

This file is the standing brief for the scheduled daily pass. Every scheduled run must follow it exactly.

## The one hard rule

**Improve the app without changing the app's appearance.**

Allowed: bug fixes, crash/glitch fixes, performance, memory, battery, robustness, error handling,
accessibility, code quality, CI/build improvements, Android shell hardening.

Not allowed: any change a user could *see*. No colour, spacing, layout, radius, blur, shadow,
animation-timing, wording or icon changes. No new features. No removed features. No new screens or
settings. Screenshots in `docs/screenshots/` must still be an accurate picture of the app — if a change
would make them stale, the change is out of scope and must be skipped and logged.

If a fix cannot be made without a visible change, skip it and write it in the day's notes as
"needs visual sign-off" instead of doing it.

## Repo facts

- Repo: `technicalnihilist-lgtm/video-player`, default branch `main`, public.
- The whole UI is one file: `app/src/main/assets/index.html` (HTML + CSS + JS in one page).
- Native shell: `app/src/main/java/com/glassplayer/app/MainActivity.java`, `AndroidManifest.xml`.
- CI: `.github/workflows/build-apk.yml` builds `Video-Player-debug.apk` on every push to `main`.
- Package `com.glassplayer.app`, minSdk 23, targetSdk 34, no `INTERNET` permission — keep it that way.
- Releases carry exactly one APK asset named `Video-Player.apk` (a store auto-picks the first APK).

## Each run, in order

1. Read this file and `BACKLOG.md`. Pick the next day-block that is not fully ticked.
2. Implement that block's items. Read the real code before editing; never edit from memory.
3. Fix any glitch or bug you notice on the way, even outside the block — record it.
4. Verify:
   - extract the inline script and run `node --check` (syntax),
   - run the headless smoke check described in `tools/` if present,
   - confirm the CSS/JS diff contains no visual properties (colour, size, spacing, blur, radius,
     shadow, animation duration/easing) unless the block explicitly says otherwise.
5. Bump `versionCode` (+1) and `versionName` (patch, e.g. `1.0.5` → `1.0.6`) in `app/build.gradle`.
6. Update `CHANGELOG.md` (new version section, plain language, honest about anything skipped).
7. Tick the day's items in `BACKLOG.md` and append a line to its progress log.
8. Commit to `main` in one commit with a clear message.
9. Wait for the **Build APK** workflow to succeed, download the `Video-Player-apk` artifact, unzip it,
   verify `assets/index.html` inside the APK matches the committed file (md5), then publish a release
   `v<versionName>` with that APK attached, labelled `Installable APK (<versionName>)`.
10. Report: version, what was fixed, what was verified, what was skipped and why.

## Quality gates — never ship if

- the JS does not parse,
- the APK's bundled `index.html` differs from the committed one,
- the workflow failed,
- a visual change slipped in,
- the release would end up with more than one APK asset.

## Notes

- Ten items per day is the target. If an item turns out to be invalid or already done, say so and pick
  the next one from the same block rather than inventing filler.
- Never publish more than one release per day; the day's ten changes ship together.
- Keep the debug signing config; a real keystore is the user's decision.
- After 20 November the schedule should be paused or deleted.
