#!/usr/bin/env bash
set -e

echo "== Storage audit =="

echo
echo "Storage folders:"
find docs/storage -type d | sort

echo
echo "Storage pages:"
find docs/storage -name "*.md" | sort

echo
echo "Storage page count:"
find docs/storage -name "*.md" | wc -l | tr -d ' '
echo

echo
echo "Empty Storage files:"
empty_files="$(find docs/storage -name "*.md" -size 0)"
if [ -n "$empty_files" ]; then
  echo "$empty_files"
  exit 1
else
  echo "OK: no empty Storage files"
fi

echo
echo "Placeholder links in Storage:"
if grep -R 'href="#"' docs/storage >/dev/null 2>&1; then
  grep -R 'href="#"' docs/storage
  exit 1
else
  echo "OK: no placeholder links"
fi

echo
echo "Storage index links that point to missing files:"
python3 << 'PY'
from pathlib import Path
import re
import sys

root = Path("docs/storage")
missing = []

for md in root.rglob("*.md"):
    text = md.read_text()
    links = re.findall(r'href="([^"]+\.md)"', text)
    links += re.findall(r'\[[^\]]+\]\(([^)]+\.md)\)', text)

    for link in links:
        target = (md.parent / link).resolve()
        if not target.exists():
            missing.append((str(md), link))

if missing:
    for src, link in missing:
        print(f"MISSING LINK: {src} -> {link}")
    sys.exit(1)

print("OK: all Storage .md links resolve")
PY

echo
echo "Storage audit passed."
