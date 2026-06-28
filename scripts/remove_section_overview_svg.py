#!/usr/bin/env python3
"""
remove_section_overview_svg.py — Remove inline "Section Overview" pipeline SVG
blocks from all markdown files in docs/.

These 820×200 SVGs were injected at the top of pages by the SVG expansion
scripts and render as a generic Context→Key→Procedures→Reference→Ready
pipeline on every page, regardless of content.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent / "docs"

SVG_BLOCK = re.compile(
    r'<svg[^>]*width="820"[^>]*height="200"[^>]*>.*?</svg>',
    re.DOTALL,
)


def is_section_overview(block: str) -> bool:
    return "Section Overview" in block


def process(text: str) -> tuple[str, int]:
    removed = 0

    def replace(m):
        nonlocal removed
        if is_section_overview(m.group(0)):
            removed += 1
            return ""
        return m.group(0)

    new_text = SVG_BLOCK.sub(replace, text)
    new_text = re.sub(r"^\n+", "", new_text)      # strip leading blank lines
    new_text = re.sub(r"\n{3,}", "\n\n", new_text) # collapse internal blanks
    return new_text, removed


def main():
    paths = sorted(ROOT.rglob("*.md"))
    total_files = total_removed = 0

    for path in paths:
        text = path.read_text(encoding="utf-8")
        if "Section Overview" not in text:
            continue
        new_text, count = process(text)
        if count > 0:
            path.write_text(new_text, encoding="utf-8")
            total_files += 1
            total_removed += count

    print(f"Done: {total_removed} SVG blocks removed from {total_files} files")


if __name__ == "__main__":
    main()
