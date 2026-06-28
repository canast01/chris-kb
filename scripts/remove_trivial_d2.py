#!/usr/bin/env python3
"""
remove_trivial_d2.py — Remove auto-generated trivial D2 blocks:
  1. Hub-and-spoke blocks (have a 'center:' node with only outgoing edges)
  2. Disconnected-node blocks (nodes defined but no edges at all)

Keeps all legitimate D2 diagrams (troubleshooting flowcharts, architecture
diagrams, SRDF topology, I/O diagrams, etc.).
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent / "docs"
D2_BLOCK = re.compile(r"```d2\n.*?\n```", re.DOTALL)


def is_trivial(block: str) -> bool:
    # Hub-and-spoke: has a 'center:' node definition
    if re.search(r"^center:", block, re.MULTILINE):
        return True
    # Disconnected list: nodes defined but zero '->' edges
    has_nodes = bool(re.search(r"^\w+:.*\{shape:", block, re.MULTILINE))
    has_edges = "->" in block
    if has_nodes and not has_edges:
        return True
    return False


def process(text: str) -> tuple[str, int]:
    removed = 0

    def replace(m):
        nonlocal removed
        if is_trivial(m.group(0)):
            removed += 1
            return ""
        return m.group(0)

    new_text = D2_BLOCK.sub(replace, text)
    new_text = re.sub(r"\n{3,}", "\n\n", new_text)
    return new_text, removed


def main():
    paths = sorted(ROOT.rglob("*.md"))
    total_files = total_removed = 0

    for path in paths:
        text = path.read_text(encoding="utf-8")
        if "```d2" not in text:
            continue
        new_text, count = process(text)
        if count > 0:
            path.write_text(new_text, encoding="utf-8")
            total_files += 1
            total_removed += count

    print(f"Done: {total_removed} trivial D2 blocks removed from {total_files} files")


if __name__ == "__main__":
    main()
