#!/usr/bin/env python3
"""
Convert **From vCenter UI:** + prose + CLI-block patterns to Material Tabs.

Pattern detected (strict):
    **From vCenter UI:**
    [one or more navigation text lines]
    [blank line]
    ```bash / powershell / text
    [commands]
    ```

Output:
    === "vCenter UI"
        [navigation text lines]

    === "CLI" / "PowerCLI"
        ```bash
        [commands]
        ```

Safety: only converts when a code fence IMMEDIATELY follows the blank line after
the UI text. If prose or a heading follows instead, the block is left unchanged.
"""

import re
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent / "docs"

UI_MARKERS = {
    "**From vCenter UI:**",
    "**Via vCenter UI:**",
    "**From the UI:**",
    "**Via the UI:**",
}

CLI_LABEL = {
    "powershell": "PowerCLI",
    "ps1":        "PowerCLI",
    "bash":       "CLI",
    "sh":         "CLI",
    "text":       "CLI",
    "":           "CLI",
}


def cli_label_for(lang: str) -> str:
    return CLI_LABEL.get(lang.strip().lower(), "CLI")


def convert_lines(lines: list[str]) -> tuple[list[str], int]:
    """Return (converted_lines, count_of_conversions)."""
    result = []
    i = 0
    changed = 0

    while i < len(lines):
        stripped = lines[i].rstrip()

        if stripped not in UI_MARKERS:
            result.append(lines[i])
            i += 1
            continue

        # Already inside a tab set? Skip (idempotent).
        if result and result[-1].startswith('=== "'):
            result.append(lines[i])
            i += 1
            continue

        # Collect UI text lines (non-blank lines immediately after marker).
        j = i + 1
        ui_text_lines = []
        while j < len(lines) and lines[j].rstrip():
            ui_text_lines.append(lines[j].rstrip())
            j += 1

        if not ui_text_lines:
            # Nothing after the marker — leave as-is.
            result.append(lines[i])
            i += 1
            continue

        # Skip the blank line(s) between UI text and potential code fence.
        blank_start = j
        while j < len(lines) and not lines[j].rstrip():
            j += 1

        # Is the next non-blank line a code fence?
        if j >= len(lines) or not lines[j].rstrip().startswith("```"):
            # No CLI block — leave unchanged.
            result.append(lines[i])
            i += 1
            continue

        # Extract the fence language.
        fence_open = lines[j].rstrip()
        lang = fence_open[3:].strip()

        # Collect the full code block.
        code_lines = [fence_open]
        j += 1
        while j < len(lines) and not lines[j].rstrip().startswith("```"):
            code_lines.append(lines[j].rstrip())
            j += 1
        if j < len(lines):
            code_lines.append(lines[j].rstrip())  # closing ```
            j += 1

        label = cli_label_for(lang)

        # Emit the two-tab block.
        result.append('=== "vCenter UI"\n')
        for t in ui_text_lines:
            result.append(f"    {t}\n")
        result.append("\n")
        result.append(f'=== "{label}"\n')
        for c in code_lines:
            result.append(f"    {c}\n")
        result.append("\n")

        changed += 1
        i = j  # resume after the closing fence

    return result, changed


def process_file(path: Path, dry_run: bool) -> tuple[int, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    # Quick pre-check — skip if no marker present.
    if not any(line.rstrip() in UI_MARKERS for line in lines):
        return 0, "no-match"

    # Skip if already fully converted (all markers already inside tab blocks).
    new_lines, count = convert_lines(lines)

    if count == 0:
        return 0, "no-match"

    if not dry_run:
        path.write_text("".join(new_lines), encoding="utf-8")

    return count, "dry" if dry_run else "updated"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="Show what would change, don't write")
    ap.add_argument("--file", help="Process a single file")
    ap.add_argument("--section", help="Limit to docs sub-path, e.g. virtualization/vmware/vsan")
    args = ap.parse_args()

    if args.file:
        paths = [Path(args.file)]
    else:
        base = ROOT / args.section if args.section else ROOT
        paths = sorted(base.rglob("*.md"))

    total_files = 0
    total_blocks = 0

    for path in paths:
        n, status = process_file(path, args.dry_run)
        if n:
            rel = path.relative_to(ROOT)
            verb = "WOULD UPDATE" if args.dry_run else "UPDATED"
            print(f"[{verb}] {rel}  ({n} block{'s' if n != 1 else ''} converted)")
            total_files += 1
            total_blocks += n

    print()
    print("=" * 60)
    if args.dry_run:
        print(f"DRY RUN: {total_blocks} blocks across {total_files} files would be converted")
    else:
        print(f"COMPLETE: {total_blocks} blocks converted across {total_files} files")
    print("=" * 60)


if __name__ == "__main__":
    main()
