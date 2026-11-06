# Queue Announcer: version history

## How version numbers work

Versions look like **MAJOR.MINOR.FIX**, for example 1.2.3.

| Change | Example | What goes up |
|---|---|---|
| Small fix or tweak: wording, colours, timing, a bug | Shorter pause, fixed button colour | **FIX**: 1.0.0 → 1.0.1 |
| New feature or new option | New bell sound, new setting, new page | **MINOR**: 1.0.1 → 1.1.0 (FIX resets to 0) |
| Big change to how the app works | Numbers shared between PCs, full redesign | **MAJOR**: 1.4.2 → 2.0.0 (others reset to 0) |

Several changes released together get one version, using the biggest change in the batch.

## Keep the history

Older versions are never removed or rewritten. Each new version is added **on top** of the list, here and in the app's About page, so the full history is always visible.

## Release checklist

Every release, before it goes online:

1. Add the new version at the top of `RELEASES` in `source/index.html` (date + short notes staff can understand). Leave every older entry as it is.
2. Set the same number in `version.json`.
3. Add the same entry at the top of the list below. Leave every older entry as it is.
4. Run `python3 tools/check_version.py`. It confirms all three match.
5. Run `python3 tools/build.py`. It rebuilds the live `index.html`.
6. Commit and push to `main`. GitHub Pages publishes it in about a minute.
7. Every PC picks up the new version within about 10 minutes (or when the app is reopened).

---

## 1.1.0 — 6 Nov 2026
- When the floating window opens, the main window shrinks to a small tab in the bottom-left corner
- Closing the floating window puts the main window back where it was

## 1.0.2 — 6 Nov 2026
- Fixed: "Speaking" could get stuck; it now always clears
- Shows a message if the voice does not play, instead of waiting forever
- Reopening the app now always loads the newest version straight away

## 1.0.1 — 6 Nov 2026
- Fixed: no sound after the app moved into the floating window
- Fixed: the very first tap was ignored when the window popped out

## 1.0.0 — 6 Nov 2026
First release.
- Keypad with letters A–Z and numbers 0–9 on one page
- Bell, then Ava reads the code letter by letter
- One call at a time, with Repeat and Mute
- Recent page with a Recall button for every number
- Settings for volume, speed, repeats and bell sound
- Floating window that stays on top of other apps
- Updates load automatically on every PC
- Foodle logo as the app icon
