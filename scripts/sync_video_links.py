#!/usr/bin/env python3
"""
Sync video links from docs/videos.yml into KB pages as tip admonitions.

Placement rules by video type:
  deploy         → after "## Before you begin" section heading
  troubleshooting → before "## See also" section heading
  operations     → after first H2 heading (below main intro)
  architecture   → after first H2 heading (below main intro)

Idempotent: running twice produces the same result.
Run: python3 scripts/sync_video_links.py [--dry-run]
"""

import re
import sys
import yaml
from pathlib import Path

REPO = Path(__file__).parent.parent
REGISTRY = REPO / "docs" / "videos.yml"

ADMONITION_START = "<!-- video-link -->"
ADMONITION_END = "<!-- /video-link -->"

TEMPLATE = """\
<!-- video-link -->
!!! tip "Video Walkthrough"
    [:fontawesome-brands-youtube: {title}]({url}){{ .md-button }}
<!-- /video-link -->"""

DRY_RUN = "--dry-run" in sys.argv


def build_admonition(entry: dict) -> str:
    return TEMPLATE.format(title=entry["title"], url=entry["url"])


def strip_existing(content: str) -> str:
    """Remove any previously injected admonition block."""
    return re.sub(
        rf"{re.escape(ADMONITION_START)}.*?{re.escape(ADMONITION_END)}\n?",
        "",
        content,
        flags=re.DOTALL,
    )


def insert_after_heading(content: str, heading_pattern: str, block: str) -> str:
    """Insert block on the line after the first matching heading."""
    lines = content.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if re.match(heading_pattern, line.strip(), re.IGNORECASE):
            lines.insert(i + 1, "\n" + block + "\n")
            return "".join(lines)
    return None  # heading not found


def insert_before_heading(content: str, heading_pattern: str, block: str) -> str:
    """Insert block on the line before the first matching heading."""
    lines = content.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if re.match(heading_pattern, line.strip(), re.IGNORECASE):
            lines.insert(i, block + "\n\n")
            return "".join(lines)
    return None  # heading not found


def insert_after_first_h2(content: str, block: str) -> str:
    """Insert block after the first H2 section (after its content begins)."""
    lines = content.splitlines(keepends=True)
    h2_count = 0
    for i, line in enumerate(lines):
        if re.match(r"^## ", line):
            h2_count += 1
            if h2_count == 1:
                # insert after a blank line following the heading
                insert_at = i + 1
                while insert_at < len(lines) and lines[insert_at].strip() == "":
                    insert_at += 1
                lines.insert(insert_at, block + "\n\n")
                return "".join(lines)
    return None


def apply_video(page_path: Path, entry: dict) -> bool:
    """Return True if file was (or would be) changed."""
    content = page_path.read_text(encoding="utf-8")
    content = strip_existing(content)
    block = build_admonition(entry)
    video_type = entry.get("type", "deploy")

    updated = None
    if video_type == "deploy":
        updated = insert_after_heading(content, r"^##\s+before you begin", block)
        if updated is None:
            updated = insert_after_first_h2(content, block)
    elif video_type == "troubleshooting":
        updated = insert_before_heading(content, r"^##\s+see also", block)
        if updated is None:
            updated = insert_after_first_h2(content, block)
    else:  # operations, architecture
        updated = insert_after_first_h2(content, block)

    if updated is None or updated == content:
        return False

    if not DRY_RUN:
        page_path.write_text(updated, encoding="utf-8")
    return True


def main():
    with open(REGISTRY, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    changed = 0
    skipped = 0
    for entry in data["videos"]:
        page_path = REPO / entry["page"]
        if not page_path.exists():
            print(f"  SKIP (missing): {entry['page']}")
            skipped += 1
            continue

        was_changed = apply_video(page_path, entry)
        status = ("DRY" if DRY_RUN else "UPDATED") if was_changed else "OK"
        print(f"  {status}: {entry['page']}")
        if was_changed:
            changed += 1

    label = "Would update" if DRY_RUN else "Updated"
    print(f"\n{label} {changed} page(s), skipped {skipped}")


if __name__ == "__main__":
    main()
