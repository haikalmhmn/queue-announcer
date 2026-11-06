"""Prepare a bell sound for Queue Announcer (see sounds/README.md for the SOP).

Usage:  python3 tools/prepare_sound.py <input file> <output name>
Example: python3 tools/prepare_sound.py ~/Downloads/bell_new.wav foodle-bell

Steps it performs:
  1. Decode any audio file (wav, mp3, m4a...) to mono 44.1 kHz 16-bit with ffmpeg.
  2. Cut silence at the start and end (anything quieter than -50 dBFS), keeping 10 ms.
  3. Add a 30 ms fade-out so the cut end doesn't click.
  4. Set the loudest point to -1 dBFS so every bell plays at a similar volume.
  5. Save as sounds/<output name>.wav and print a before/after report.
"""
import array
import math
import os
import subprocess
import sys
import wave

SR = 44100
THRESHOLD_DB = -50.0
KEEP_MS = 10
FADE_MS = 30
TARGET_PEAK_DB = -1.0
MAX_SECONDS = 4.0


def decode(path):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
        check=True, capture_output=True,
    ).stdout
    a = array.array("h")
    a.frombytes(raw)
    return a


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    src, name = sys.argv[1], sys.argv[2]
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "sounds", name + ".wav")

    s = decode(src)
    if not s:
        sys.exit("No audio found in that file.")
    peak = max(abs(x) for x in s) or 1
    thr = 32768 * (10 ** (THRESHOLD_DB / 20))
    # Judge loudness in 10 ms windows (RMS), so single stray samples don't count as sound.
    win = SR // 100
    loud = []
    for w0 in range(0, len(s), win):
        chunk = s[w0:w0 + win]
        rms = math.sqrt(sum(x * x for x in chunk) / len(chunk))
        if rms > thr:
            loud.append(w0)
    if not loud:
        sys.exit("The file is silent.")
    keep = int(SR * KEEP_MS / 1000)
    start = max(0, loud[0] - keep)
    end = min(len(s), loud[-1] + win + keep)
    t = s[start:end]

    gain = (32767 * (10 ** (TARGET_PEAK_DB / 20))) / peak
    fade = int(SR * FADE_MS / 1000)
    outv = array.array("h")
    for i, x in enumerate(t):
        g = gain
        if i >= len(t) - fade:
            g *= (len(t) - i) / fade
        outv.append(max(-32768, min(32767, int(round(x * g)))))

    with wave.open(out, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(outv.tobytes())

    before, after = len(s) / SR, len(outv) / SR
    print("Saved:            sounds/%s.wav" % name)
    print("Length:           %.2fs -> %.2fs" % (before, after))
    print("Silence cut:      %.0f ms at start, %.0f ms at end" % (start / SR * 1000, (len(s) - end) / SR * 1000))
    print("Peak level:       %.1f dBFS -> %.1f dBFS" % (20 * math.log10(peak / 32768), TARGET_PEAK_DB))
    print("File size:        %.0f KB" % (os.path.getsize(out) / 1024))
    if after > MAX_SECONDS:
        print("WARNING: longer than %.0fs. Long bells delay the announcement; consider a shorter clip." % MAX_SECONDS)


if __name__ == "__main__":
    main()
