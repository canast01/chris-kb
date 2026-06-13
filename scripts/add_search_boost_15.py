#!/usr/bin/env python3
"""Add search.boost: 1.5 to troubleshooting and deploy pages.

Skips pages that already have a search: block (the top-20 with boost: 2).
"""

import re
from pathlib import Path

DOCS = Path("docs")
FRONT_MATTER_RE = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)


def main():
    targets = [
        p for p in DOCS.rglob("index.md")
        if "/troubleshooting/" in str(p) or "/deploy/" in str(p)
    ]

    updated = skipped_existing = skipped_no_fm = 0
    for path in sorted(targets):
        content = path.read_text(encoding="utf-8")
        m = FRONT_MATTER_RE.match(content)
        if not m:
            skipped_no_fm += 1
            continue
        fm = m.group(1)
        if "search:" in fm:
            skipped_existing += 1
            continue
        new_fm = fm + "\nsearch:\n  boost: 1.5"
        path.write_text(f"---\n{new_fm}\n---\n" + content[m.end():], encoding="utf-8")
        updated += 1

    print(f"Boosted:          {updated}")
    print(f"Skipped (already): {skipped_existing}")
    print(f"Skipped (no FM):   {skipped_no_fm}")
    print(f"Total scanned:     {len(targets)}")


if __name__ == "__main__":
    main()
