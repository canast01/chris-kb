#!/usr/bin/env python3
"""Convert FAQ comparison/decision Q&A answers to Markdown tables using OpenAI.

Targets two patterns found across the 90 faq.md pages:
  1. True X vs Y  — "difference between A and B", "when to use each"
  2. Default + decision — "What is the default X and when should it change?"
     (answers that list 2+ modes with distinct conditions)

Usage:
  python3 scripts/faq_comparison_tables.py --dry-run
  python3 scripts/faq_comparison_tables.py --limit 3
  python3 scripts/faq_comparison_tables.py --file docs/backup/veeam/operations/faq.md
  python3 scripts/faq_comparison_tables.py          # full batch (90 files)
"""

import argparse
import os
import re
import sys
import time
from pathlib import Path

from openai import OpenAI, RateLimitError, APIError, APIConnectionError, APITimeoutError

DOCS_DIR = Path(__file__).parent.parent / "docs"
MODEL = "gpt-4o"
BATCH_SIZE = 10
SLEEP_BETWEEN_BATCHES = 4.0
MAX_RETRIES = 3

COMPARISON_Q_PATTERNS = [
    r"difference between",
    r"\bvs\b",
    r"when to use each",
    r"which .*(should|do I use)",
    r"when should it change",
    r"when should it be changed",
    r"protection group types",
    r"features.*included.*vs",
]

SYSTEM_PROMPT = """You are a technical documentation specialist converting FAQ prose answers into
concise Markdown comparison tables.

Rules:
- Only create a table when the answer presents 2 or more DISTINCT options, modes, types, or
  settings, each with a different use case or behaviour.
- Table must have 2–4 columns. Use column names appropriate to the content, e.g.:
    Mode | Behaviour | When to Use
    Type | Description | When to Use
    Option A | Option B | Key Difference    (for two-option comparisons)
- Keep cell content concise (≤15 words per cell). No filler phrases.
- Do NOT create a table for:
    • single-option answers ("always use X")
    • procedural steps (do A, then B, then C)
    • yes/no answers with a simple explanation
    • answers where options aren't meaningfully distinct
- If the answer should not become a table, respond with exactly: SKIP
- Return ONLY the markdown table OR the word SKIP. No preamble, no explanation."""

USER_PROMPT = """Convert this FAQ answer to a Markdown table, or respond SKIP.

Q: {question}
A: {answer}"""


def find_faq_files(docs_dir: Path) -> list[Path]:
    return sorted(docs_dir.rglob("faq.md"))


def parse_qa_pairs(content: str) -> list[tuple[str, str, int]]:
    """Return list of (question, answer, answer_line_index).

    Answer line index is the 0-based index into content.splitlines() of the A: line.
    Only returns pairs where answer is not already a table (no | present).
    """
    lines = content.splitlines()
    pairs = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("**Q:") and line.endswith("**"):
            question = line[4:-2].strip()
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].lstrip().startswith("A:"):
                answer = lines[j].lstrip()[2:].strip()
                if "|" not in answer and answer:
                    pairs.append((question, answer, j))
                i = j + 1  # advance past the A: line
            else:
                i = j  # no A: found — let outer loop process lines[j] (may be next Q)
        else:
            i += 1
    return pairs


def is_candidate(question: str, answer: str) -> bool:
    """Quick heuristic filter before calling OpenAI."""
    q_lower = question.lower()
    for pat in COMPARISON_Q_PATTERNS:
        if re.search(pat, q_lower):
            return True
    # Answer mentions "use" 2+ times with distinct conditions
    use_count = len(re.findall(r"\buse\b", answer.lower()))
    if use_count >= 2:
        return True
    return False


def call_openai(client: OpenAI, question: str, answer: str) -> str | None:
    """Call OpenAI to convert answer to table. Returns table markdown or None (SKIP)."""
    prompt = USER_PROMPT.format(question=question, answer=answer)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=800,
                temperature=0.1,
            )
            if not response.choices:
                print("    OpenAI returned empty choices (content filtered) — skipping")
                return None
            content = response.choices[0].message.content
            if content is None:
                print("    OpenAI returned None content — skipping")
                return None
            result = content.strip()
            if result.upper() == "SKIP" or not result.startswith("|"):
                return None
            # Basic table validation: must have header + separator row
            table_lines = result.splitlines()
            if len(table_lines) < 3:
                print(f"    Table too short ({len(table_lines)} lines) — skipping")
                return None
            if not re.match(r"^\|[\s\-|]+\|$", table_lines[1]):
                print(f"    Table missing separator row — skipping")
                return None
            return result
        except RateLimitError as e:
            # insufficient_quota will never clear — abort immediately
            if "insufficient_quota" in str(e):
                print("ERROR: OpenAI quota exhausted — add credits at platform.openai.com", file=sys.stderr)
                sys.exit(1)
            wait = 15 * attempt
            print(f"    Rate limit — waiting {wait}s (attempt {attempt}/{MAX_RETRIES})")
            time.sleep(wait)
        except (APIConnectionError, APITimeoutError, APIError) as e:
            print(f"    API error: {e} (attempt {attempt}/{MAX_RETRIES})")
            time.sleep(5 * attempt)
    return None


def process_file(
    client: OpenAI, path: Path, dry_run: bool
) -> tuple[int, int]:
    """Returns (candidates_found, tables_written)."""
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"  ERROR reading {path}: {e}")
        return 0, 0

    pairs = parse_qa_pairs(content)
    candidates = [(q, a, idx) for q, a, idx in pairs if is_candidate(q, a)]

    if not candidates:
        return 0, 0

    lines = content.splitlines()
    written = 0

    for question, answer, a_idx in candidates:
        table = call_openai(client, question, answer)
        if table is None:
            print(f"  SKIP  — {question[:70]}")
            continue
        if dry_run:
            print(f"  DRY RUN — would convert: {question[:70]}")
            print(f"    → {table.splitlines()[0][:80]}...")
            written += 1
        else:
            # Replace the A: line with a blank line + table
            lines[a_idx] = "\n" + table
            written += 1
            print(f"  TABLE — {question[:70]}")

    if written > 0 and not dry_run:
        try:
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        except OSError as e:
            print(f"  ERROR writing {path}: {e}")
            return len(candidates), 0

    return len(candidates), written


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert FAQ comparison Q&As to Markdown tables"
    )
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    parser.add_argument("--limit", type=int, default=0, help="Stop after N files (file-granular)")
    parser.add_argument("--file", type=str, help="Process a single file by path")
    parser.add_argument("--section", type=str, default="", help="Only process files under docs/<section>")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    if args.file:
        files = [Path(args.file)]
    else:
        files = find_faq_files(DOCS_DIR)
        if args.section:
            section_path = DOCS_DIR / args.section
            files = [f for f in files if f.is_relative_to(section_path)]

    if args.limit:
        files = files[: args.limit]

    total_candidates = 0
    total_written = 0
    files_changed = 0

    for i, path in enumerate(files):
        rel = path.relative_to(DOCS_DIR) if DOCS_DIR in path.parents else path
        print(f"[{i + 1}/{len(files)}] {rel}")

        candidates, written = process_file(client, path, args.dry_run)
        total_candidates += candidates
        total_written += written
        if written > 0:
            files_changed += 1

        if (i + 1) % BATCH_SIZE == 0 and i + 1 < len(files):
            print(f"  [batch pause {SLEEP_BETWEEN_BATCHES}s]")
            time.sleep(SLEEP_BETWEEN_BATCHES)

    print(f"\n{'=' * 60}")
    if args.dry_run:
        print(f"DRY RUN: {total_written} tables would be written across {files_changed} files")
    else:
        print(f"COMPLETE: {total_written} tables written across {files_changed} files")
    print(f"  Candidates found: {total_candidates} | Skipped by OpenAI: {total_candidates - total_written}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
