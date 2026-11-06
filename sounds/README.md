# SOP: adding a bell sound

Follow every step before a new sound goes into the Bell sound list.

## 1. Check the file
- Any common audio format is fine (WAV, MP3, M4A).
- Listen to it once. It should be a single bell or chime, ideally under 2 seconds.

## 2. Clean it with the prepare script
Run from the top of the repository:

```
python3 tools/prepare_sound.py <path to file> <short-name>
```

The script:
- cuts silence at the start and end (quieter than -50 dBFS),
- adds a 30 ms fade-out so the end doesn't click,
- sets the peak to -1 dBFS so all bells play at a similar volume,
- saves `sounds/<short-name>.wav` (mono, 44.1 kHz, 16-bit).

## 3. Check the report
- **Silence cut**: confirms what was removed.
- **Length**: should be under 4 seconds. The script warns if it's longer.
- Optional double check: `ffmpeg -i sounds/<short-name>.wav -af silencedetect=noise=-50dB:d=0.05 -f null -` should report no silence.

## 4. Add it to the list
In `source/index.html`, find `var SOUNDS = [` and add one line:

```
{ id: '<short-name>', name: '<Name shown in the dropdown>', file: 'sounds/<short-name>.wav' },
```

## 5. Test, then release
- Open Settings, pick the new sound and press **Test**.
- Release it as a new version (a new sound is a MINOR change, e.g. 1.0.0 → 1.1.0) by following the release checklist in `CHANGELOG.md`.

## Sounds in the app
| Name | File | Source | Cut |
|---|---|---|---|
| Foodle bell (default) | foodle-bell.wav | bell_new.wav, supplied 6 Nov 2026 | 10 ms start, 306 ms end; peak set to -1 dBFS |
| Classic chime | built into the code | n/a | n/a |
