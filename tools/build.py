"""Build the live page from the editable source.

Usage: python3 tools/build.py

Reads source/index.html (the editable app) and writes index.html at the top of the
repository as a complete web page. GitHub Pages serves the top of the repository.
Run tools/check_version.py first; build.py refuses to run if the versions don't match.
"""
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

HEAD = """<!doctype html>
<!-- Built by tools/build.py from source/index.html. Edit the source, not this file. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>[hidden]{display:none!important}body{margin:0}</style>
"""


def main():
    src = open(os.path.join(ROOT, "source", "index.html"), encoding="utf-8").read()
    version = re.search(r"var RELEASES = \[\s*\{\s*version:\s*'([^']+)'", src).group(1)
    vj = json.load(open(os.path.join(ROOT, "version.json"), encoding="utf-8"))["version"]
    if vj != version:
        sys.exit("version.json (%s) does not match source/index.html (%s). Run tools/check_version.py." % (vj, version))

    cut = src.index("</style>") + len("</style>")
    page = HEAD + src[:cut] + "\n</head>\n<body>\n" + src[cut:].lstrip("\n") + "\n</body>\n</html>\n"
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page)
    print("Built index.html for version", version)


if __name__ == "__main__":
    main()
