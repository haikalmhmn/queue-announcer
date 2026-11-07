"""Set the Settings PIN for every PC.

Usage: python3 tools/set_pin.py <PIN>
The PIN must be digits only. Its length becomes the PIN length the app expects.
Only a salted SHA-256 hash is written into source/index.html; the PIN itself is never stored.
After running this, release a new version so every PC gets the new PIN.
"""
import hashlib
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SRC = os.path.join(ROOT, "source", "index.html")


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"\d{4,8}", sys.argv[1]):
        sys.exit("Give a PIN of 4 to 8 digits, e.g. python3 tools/set_pin.py 482913")
    pin = sys.argv[1]
    s = open(SRC, encoding="utf-8").read()
    salt = re.search(r"var PIN_SALT = '([^']*)';", s).group(1)
    h = hashlib.sha256((salt + pin).encode("utf-8")).hexdigest()
    s, n1 = re.subn(r"var PIN_HASH = '[^']*';", "var PIN_HASH = '%s';" % h, s)
    s, n2 = re.subn(r"var PIN_LENGTH = \d+;", "var PIN_LENGTH = %d;" % len(pin), s)
    if n1 != 1 or n2 != 1:
        sys.exit("Couldn't find PIN_HASH / PIN_LENGTH in source/index.html")
    open(SRC, "w", encoding="utf-8").write(s)
    print("PIN updated (%d digits). Now release a new version." % len(pin))


if __name__ == "__main__":
    main()
