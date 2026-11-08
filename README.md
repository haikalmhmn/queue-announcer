# Queue Announcer

A small touch app for the Foodle counter. Staff key in an order code (for example A105), and the app plays the Foodle bell, then a calm voice reads the code letter by letter.

**Live app:** https://haikalmhmn.github.io/queue-announcer/
Open it in Microsoft Edge and choose **⋯ → Apps → Install this site as an app**.

**Staff guide (PDF):** https://haikalmhmn.github.io/queue-announcer/guide/Queue-Announcer-Staff-Guide-v1.4.2.pdf

## How updates reach every PC
GitHub Pages serves this repository. When a new version is pushed here, every PC running the app checks `version.json` every 5 minutes and loads the new version once nothing is being typed or spoken.

## What's in here
| Path | What it is |
|---|---|
| `index.html` | The live page. **Built** from `source/index.html`; don't edit by hand. |
| `source/index.html` | The app itself: layout, styles and code. Edit this one. |
| `version.json` | The current version number. PCs compare against it to update. |
| `CHANGELOG.md` | Version rules, release checklist and full version history. |
| `sounds/` | Bell sounds, plus the SOP for adding a new one (`sounds/README.md`). |
| `icons/` | App icon in every size (Foodle logo). |
| `sw.js` | Lets the app keep working offline. |
| `manifest.webmanifest` | App name and icon for installing on PCs. |
| `guide/` | Staff guide PDF, named with the app version (e.g. `Queue-Announcer-Staff-Guide-v1.4.2.pdf`) and updated with every app release. `guide/source/` holds the HTML and screenshots it is printed from. |
| `tools/` | `check_version.py`, `build.py`, `prepare_sound.py`. |

## Releasing a new version
Follow the checklist in `CHANGELOG.md`. In short: add the version notes, run `python3 tools/check_version.py`, run `python3 tools/build.py`, commit, push.
