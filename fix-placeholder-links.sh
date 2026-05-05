#!/usr/bin/env bash
set -euo pipefail

echo
echo "=== FIXING PLACEHOLDER LINKS ==="

python3 - << 'PY'
from pathlib import Path
import re

changed = []

for path in Path("docs").rglob("*.md"):
    text = path.read_text()
    new_text = re.sub(r'href="#"', 'href="./"', text)

    if new_text != text:
        path.write_text(new_text)
        changed.append(str(path))

if changed:
    print("Updated files:")
    for item in changed:
        print(f"- {item}")
else:
    print("No placeholder links found.")
PY

echo
echo "Running validation and health check..."
./validate-site.sh

echo
echo "Running audit..."
if [ -f "./audit-site.sh" ]; then
  ./audit-site.sh
fi

echo
echo "Placeholder link cleanup complete."
