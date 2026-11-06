"""Check that the version number matches in source/index.html, version.json and CHANGELOG.md.

Usage: python3 tools/check_version.py
"""
import json
import os
import re
import sys

root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
html = open(os.path.join(root, "source", "index.html"), encoding="utf-8").read()
m = re.search(r"var RELEASES = \[\s*\{\s*version:\s*'([^']+)'", html)
app = m.group(1) if m else None
vj = json.load(open(os.path.join(root, "version.json"), encoding="utf-8")).get("version")
cl = open(os.path.join(root, "CHANGELOG.md"), encoding="utf-8").read()
m2 = re.search(r"^## (\d+\.\d+\.\d+)", cl, re.M)
log = m2.group(1) if m2 else None

print("source/index.html (RELEASES):", app)
print("version.json:                ", vj)
print("CHANGELOG.md:                ", log)
if app and app == vj == log and re.fullmatch(r"\d+\.\d+\.\d+", app):
    print("OK: all match", app)
else:
    print("MISMATCH: fix before releasing")
    sys.exit(1)
