#!/usr/bin/env python3
"""Add Mermaid step-flow diagrams to deploy/index.md pages.

Extracts H2 headings (the deployment steps) and injects a flowchart
between the SVG hero image and the first step heading. No OpenAI needed.

Diagram placement:
  ![SVG hero]
  ```mermaid
  flowchart LR / TD
    ...
  ```
  ## Prerequisites   ← first step heading

Usage:
  python3 scripts/deploy_flow_diagrams.py --dry-run
  python3 scripts/deploy_flow_diagrams.py --limit 5
  python3 scripts/deploy_flow_diagrams.py --file docs/backup/veeam/deploy/index.md
  python3 scripts/deploy_flow_diagrams.py --section virtualization
  python3 scripts/deploy_flow_diagrams.py          # all 67 deploy pages
"""

import argparse
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"

SKIP_HEADINGS = {
    "see also",
    "see also:",
    "references",
}

VERIFY_PREFIXES = ("verif", "validat")

MAX_LABEL_LEN = 45
LR_THRESHOLD = 6  # use LR for <= this many steps, TD for more


def find_deploy_pages(docs_dir: Path) -> list[Path]:
    return sorted(docs_dir.rglob("deploy/index.md"))


def extract_h2_headings(content: str) -> list[str]:
    """Return all H2 headings except navigation boilerplate."""
    headings = []
    for line in content.splitlines():
        if line.startswith("## "):
            heading = line[3:].strip()
            if heading.lower().rstrip(":") not in SKIP_HEADINGS:
                headings.append(heading)
    return headings


def shorten(label: str) -> str:
    """Truncate long labels and escape chars that break Mermaid."""
    label = label.replace("&", "and").replace('"', "'")
    if len(label) > MAX_LABEL_LEN:
        label = label[: MAX_LABEL_LEN - 3] + "..."
    return label


def is_verify_step(heading: str) -> bool:
    h = heading.lower()
    return any(h.startswith(p) for p in VERIFY_PREFIXES)


def generate_flowchart(headings: list[str]) -> str:
    direction = "LR" if len(headings) <= LR_THRESHOLD else "TD"
    lines = ["```mermaid", f"flowchart {direction}"]

    node_ids = [f"s{i}" for i in range(len(headings))]

    for nid, heading in zip(node_ids, headings):
        label = shorten(heading)
        if is_verify_step(heading):
            lines.append(f'    {nid}["✓ {label}"]')
        else:
            lines.append(f'    {nid}["{label}"]')

    # Edges as a chain
    chain = " --> ".join(node_ids)
    lines.append(f"    {chain}")

    # Style verify nodes
    for nid, heading in zip(node_ids, headings):
        if is_verify_step(heading):
            lines.append(
                f"    style {nid} fill:#2e7d32,color:#fff,stroke:#1b5e20"
            )

    lines.append("```")
    return "\n".join(lines)


def find_injection_point(lines: list[str]) -> int | None:
    """Return index of the first H2 heading that appears after the SVG image."""
    svg_seen = False
    for i, line in enumerate(lines):
        if not svg_seen and "![" in line and ".svg" in line:
            svg_seen = True
            continue
        if svg_seen and line.startswith("## "):
            return i
    return None


def process_file(path: Path, dry_run: bool) -> bool:
    """Return True if the file was (or would be) modified."""
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"  ERROR reading: {e}")
        return False

    if "```mermaid" in content:
        return False

    headings = extract_h2_headings(content)
    if len(headings) < 2:
        print(f"  SKIP — only {len(headings)} heading(s) found")
        return False

    lines = content.splitlines()
    inject_at = find_injection_point(lines)
    if inject_at is None:
        print(f"  SKIP — no SVG + H2 pattern found")
        return False

    flowchart = generate_flowchart(headings)
    direction = "LR" if len(headings) <= LR_THRESHOLD else "TD"

    if dry_run:
        print(
            f"  DRY RUN — {len(headings)} steps, flowchart {direction}"
            f" → inject before line {inject_at + 1}"
        )
        print(f"    {' → '.join(h[:25] for h in headings[:4])}"
              f"{'...' if len(headings) > 4 else ''}")
        return True

    new_lines = lines[:inject_at] + ["", flowchart, ""] + lines[inject_at:]
    try:
        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    except OSError as e:
        print(f"  ERROR writing: {e}")
        return False

    print(f"  ADDED — {len(headings)}-step flowchart ({direction})")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add step-flow Mermaid diagrams to deploy pages"
    )
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    parser.add_argument("--limit", type=int, default=0, help="Stop after N files (file-granular)")
    parser.add_argument("--file", type=str, help="Process a single file by path")
    parser.add_argument(
        "--section", type=str, default="",
        help="Only process files under docs/<section> (e.g. backup)"
    )
    args = parser.parse_args()

    if args.file:
        files = [Path(args.file)]
    else:
        files = find_deploy_pages(DOCS_DIR)
        if args.section:
            section_path = DOCS_DIR / args.section
            files = [f for f in files if f.is_relative_to(section_path)]

    if args.limit:
        files = files[: args.limit]

    modified = 0
    skipped = 0

    for i, path in enumerate(files):
        rel = path.relative_to(DOCS_DIR) if DOCS_DIR in path.parents else path
        print(f"[{i + 1}/{len(files)}] {rel}")
        result = process_file(path, args.dry_run)
        if result:
            modified += 1
        else:
            skipped += 1

    print(f"\n{'=' * 60}")
    if args.dry_run:
        print(f"DRY RUN: {modified} pages would be updated, {skipped} skipped")
    else:
        print(f"COMPLETE: {modified} pages updated, {skipped} skipped")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
