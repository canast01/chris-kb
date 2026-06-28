#!/usr/bin/env python3
"""
add_threshold_charts.py — Inject Vega-Lite threshold charts into pages that
have a Markdown table with an "Alert threshold" / "Threshold" column.

For each qualifying page:
  1. Find the threshold table and parse metric + numeric % values
  2. Build a Vega-Lite stacked bar showing Safe (green) vs Alert (red) zones
  3. Inject the fence before the first ## heading
  4. Skip if page already has a vega-lite fence

CLI:
  --dry-run     Show what would change, don't write
  --file PATH   Process a single file
  --limit N     Cap number of files processed
"""

import re
import json
import argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent / "docs"

# ─── Threshold table parser ────────────────────────────────────────────────

_THRESHOLD_HEADER = re.compile(
    r"threshold|alert.*level|warning.*threshold|check.*threshold",
    re.IGNORECASE,
)
_PCT = re.compile(r"([><≥≤])\s*(\d{1,3})\s*%")
_CLEAN_METRIC = re.compile(r"\*+|\`+|\[.*?\]\(.*?\)")


def _col_index(header_cols: list, patterns: list) -> int:
    """Return index of first column whose header matches any pattern."""
    for pattern in patterns:
        for i, col in enumerate(header_cols):
            if re.search(pattern, col, re.IGNORECASE):
                return i
    return -1


def parse_thresholds(text: str) -> list:
    """Return list of {metric, threshold, direction} dicts from the page text."""
    lines = text.splitlines()
    results = []
    in_table = False
    metric_idx = threshold_idx = -1

    for line in lines:
        stripped = line.strip()

        # --- enter a potential threshold table ---
        if stripped.startswith("|") and not in_table:
            cols = [c.strip() for c in stripped.split("|")[1:-1]]
            if any(_THRESHOLD_HEADER.search(c) for c in cols):
                metric_idx = _col_index(
                    cols,
                    [r"metric|check|component|resource|sensor|category|item"],
                )
                threshold_idx = _col_index(
                    cols,
                    [r"alert.*threshold|threshold|warning.*level|alert.*level"],
                )
                if threshold_idx >= 0:
                    metric_idx = max(metric_idx, 0)
                    in_table = True
            continue

        # --- inside table ---
        if in_table:
            if not stripped.startswith("|"):
                in_table = False
                continue
            if re.match(r"^\|[\s\-\|]+\|$", stripped):  # separator row
                continue

            parts = [c.strip() for c in stripped.split("|")[1:-1]]
            if len(parts) <= max(metric_idx, threshold_idx):
                continue

            raw_metric = _CLEAN_METRIC.sub("", parts[metric_idx]).strip()
            raw_thresh = parts[threshold_idx] if threshold_idx < len(parts) else ""

            m = _PCT.search(raw_thresh)
            if not m or not raw_metric or raw_metric.startswith("-"):
                continue

            direction = "above" if m.group(1) in (">", "≥") else "below"
            value = int(m.group(2))
            metric_clean = re.sub(r"\s+", " ", raw_metric)[:50]

            results.append(
                {"metric": metric_clean, "threshold": value, "direction": direction}
            )

    # Deduplicate by metric name (keep first occurrence)
    seen = set()
    unique = []
    for r in results:
        key = r["metric"].lower()
        if key not in seen:
            seen.add(key)
            unique.append(r)

    return unique[:12]  # cap at 12 metrics per chart


# ─── Vega-Lite spec builder ────────────────────────────────────────────────

def build_vegalite_spec(thresholds: list, title: str = "Alert Thresholds") -> dict:
    values = []
    for t in thresholds:
        tval = t["threshold"]
        if t["direction"] == "above":
            safe_val, alert_val = tval, 100 - tval
        else:
            safe_val, alert_val = 100 - tval, tval

        values.append({"metric": t["metric"], "zone": "Safe",  "val": safe_val})
        values.append({"metric": t["metric"], "zone": "Alert", "val": alert_val})

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": {
            "text": title,
            "fontSize": 13,
            "fontWeight": "normal",
        },
        "width": 480,
        "height": {"step": 26},
        "data": {"values": values},
        "mark": {"type": "bar", "cornerRadiusEnd": 3},
        "encoding": {
            "y": {
                "field": "metric",
                "type": "nominal",
                "axis": {"title": None, "labelLimit": 200},
                "sort": None,
            },
            "x": {
                "field": "val",
                "type": "quantitative",
                "stack": "normalize",
                "axis": {"title": "Threshold boundary", "format": ".0%"},
            },
            "color": {
                "field": "zone",
                "type": "nominal",
                "scale": {
                    "domain": ["Safe", "Alert"],
                    "range": ["#15803d", "#dc2626"],
                },
                "legend": {"title": "Zone"},
            },
            "order": {"field": "zone", "sort": ["Safe", "Alert"]},
            "tooltip": [
                {"field": "metric", "type": "nominal", "title": "Metric"},
                {"field": "zone",   "type": "nominal", "title": "Zone"},
                {
                    "field": "val",
                    "type": "quantitative",
                    "title": "Segment %",
                    "format": ".0f",
                },
            ],
        },
    }


def format_fence(spec: dict) -> str:
    return "```vega-lite\n" + json.dumps(spec, indent=2) + "\n```\n"


# ─── Injection helpers ─────────────────────────────────────────────────────

def already_has_vegalite(lines: list) -> bool:
    return any(line.rstrip() == "```vega-lite" for line in lines)


def find_inject_pos(lines: list):
    for i, line in enumerate(lines):
        if line.startswith("## "):
            return i
    return None


def inject_block(lines: list, pos: int, content: str) -> list:
    block = []
    if pos > 0 and lines[pos - 1].strip():
        block.append("\n")
    block.append(content if content.endswith("\n") else content + "\n")
    if pos < len(lines) and lines[pos].strip():
        block.append("\n")
    return lines[:pos] + block + lines[pos:]


# ─── Per-file processor ────────────────────────────────────────────────────

def page_title(lines: list) -> str:
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip().split("—")[-1].strip()[:40]
    return "Alert Thresholds"


def process_file(path: Path, dry_run: bool) -> str:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    if already_has_vegalite(lines):
        return "SKIP"

    thresholds = parse_thresholds(text)
    if not thresholds:
        return "NO_DATA"

    pos = find_inject_pos(lines)
    if pos is None:
        return "NO_H2"

    title = page_title(lines)
    spec = build_vegalite_spec(thresholds, title=f"{title} — Thresholds")
    fence = format_fence(spec)

    if not dry_run:
        new_lines = inject_block(lines, pos, fence)
        path.write_text("".join(new_lines), encoding="utf-8")

    return "DRY" if dry_run else "OK"


# ─── CLI ──────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--file",    help="Process a single file")
    ap.add_argument("--limit",   type=int, default=0)
    args = ap.parse_args()

    if args.file:
        paths = [Path(args.file)]
    else:
        paths = sorted(ROOT.rglob("*.md"))

    counts = {"OK": 0, "DRY": 0, "SKIP": 0, "NO_DATA": 0, "NO_H2": 0, "ERR": 0}
    processed = 0

    for path in paths:
        if args.limit and processed >= args.limit:
            break
        try:
            result = process_file(path, args.dry_run)
        except Exception as exc:
            print(f"[ERR    ] {path.relative_to(ROOT)} — {exc}")
            counts["ERR"] += 1
            processed += 1
            continue

        counts[result] += 1
        processed += 1

        if result in ("OK", "DRY"):
            verb = "DRY RUN" if result == "DRY" else "UPDATED"
            print(f"[{verb:7}] {path.relative_to(ROOT)}")

    print()
    print("=" * 68)
    n = counts["DRY"] if args.dry_run else counts["OK"]
    action = "Would update" if args.dry_run else "Updated"
    print(
        f"{action}: {n}  |  Has Vega-Lite: {counts['SKIP']}  |  "
        f"No threshold data: {counts['NO_DATA']}  |  "
        f"No H2: {counts['NO_H2']}  |  Errors: {counts['ERR']}"
    )
    print("=" * 68)


if __name__ == "__main__":
    main()
