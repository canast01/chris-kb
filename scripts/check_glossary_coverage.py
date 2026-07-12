"""
Track B (criterion #1) mechanical pass for the Diagram Readability Project:
checks whether jargon/acronyms used in a page's diagrams are covered by
that page's own explanation -- either inline "Term (ACRONYM)" prose (Phase
0's original check) or a "## Key Terms" glossary table (the pattern already
used on 37+ pages, which Phase 0's original regex did not recognize at all).

This is a fast, cheap first pass for ONE of the 11 readability criteria.
It is NOT a substitute for the naive-reader test, which remains the real
gate for the other 10 criteria (internal consistency, wrong facts, garbled
text, density, flow, etc.) -- see project_diagram_readability.md.

Usage:
  python3 scripts/check_glossary_coverage.py             # full report
  python3 scripts/check_glossary_coverage.py --no-glossary-only
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from diagram_readability_score import (
    DOCS, find_diagrams_in_page, extract_svg_labels, ACRONYM_RE,
    COMMON_KNOWLEDGE, EMPHASIS_WORDS, is_plain_english_header,
    strip_hex_addresses,
)

KEY_TERMS_HEADING_RE = re.compile(r'^##\s+Key Terms.*$', re.MULTILINE)
TABLE_ROW_RE = re.compile(r'^\|\s*([^|]+?)\s*\|', re.MULTILINE)
INLINE_EXPANSION_TMPL = r'[A-Z][\w/]+(?:\s+[A-Z][\w/]+){{1,5}}\s*\({}\)'


def extract_glossary_terms(page_prose: str) -> set:
    """Terms covered by a '## Key Terms' table on this page, if one exists."""
    m = KEY_TERMS_HEADING_RE.search(page_prose)
    if not m:
        return set()
    # table lives between this heading and the next '##' heading (or EOF)
    rest = page_prose[m.end():]
    next_heading = re.search(r'\n##\s', rest)
    table_text = rest[:next_heading.start()] if next_heading else rest
    terms = set()
    for row in TABLE_ROW_RE.finditer(table_text):
        cell = row.group(1).strip()
        if cell.lower() in ('term', '---', ''):
            continue
        # a term cell may itself contain an acronym plus prose, e.g. "SRDF/STAR"
        terms.add(cell.upper())
    return terms


def find_jargon_in_diagram(d) -> set:
    if d['type'] == 'svg':
        result = extract_svg_labels(d['svg_path'])
        if result is None:
            return set()
        labels, _ = result
    elif d['type'] == 'd2':
        labels = re.findall(r'"([^"]+)"', d['body'])
    else:  # plantuml
        labels = re.findall(r'"([^"]+)"', d['body'])

    found = set()
    for label in labels:
        for m in ACRONYM_RE.finditer(strip_hex_addresses(label)):
            acronym = m.group(0)
            if acronym in COMMON_KNOWLEDGE or acronym in EMPHASIS_WORDS or is_plain_english_header(acronym):
                continue
            found.add(acronym)
    return found


def is_covered(acronym: str, page_prose: str, glossary_terms: set) -> bool:
    if acronym in glossary_terms:
        return True
    # glossary term cells sometimes contain the acronym as a substring
    # (e.g. cell "SRDF/STAR" covers jargon hit "STAR")
    if any(acronym in gt for gt in glossary_terms):
        return True
    pattern = re.compile(INLINE_EXPANSION_TMPL.format(re.escape(acronym)))
    if pattern.search(page_prose) or f'({acronym})' in page_prose or f'({acronym}s)' in page_prose:
        return True
    return False


def main():
    no_glossary_only = '--no-glossary-only' in sys.argv

    pages = list(DOCS.rglob('*.md'))
    print(f'Scanning {len(pages)} pages...', file=sys.stderr)

    has_glossary_gap = []   # page has a Key Terms table but missing some rows
    no_glossary_gap = []    # page has jargon-bearing diagrams, no Key Terms table at all

    for md_path in pages:
        diagrams = find_diagrams_in_page(md_path)
        if not diagrams:
            continue
        page_prose = md_path.read_text(errors='replace')
        glossary_terms = extract_glossary_terms(page_prose)

        all_jargon = set()
        for d in diagrams:
            all_jargon |= find_jargon_in_diagram(d)
        if not all_jargon:
            continue

        uncovered = {a for a in all_jargon if not is_covered(a, page_prose, glossary_terms)}
        if not uncovered:
            continue

        rel = str(md_path.relative_to(DOCS.parent))
        if glossary_terms:
            has_glossary_gap.append((rel, sorted(uncovered)))
        else:
            no_glossary_gap.append((rel, sorted(uncovered)))

    print(f"\n=== Pages WITH a Key Terms table, missing some rows ({len(has_glossary_gap)}) ===")
    for rel, terms in has_glossary_gap:
        print(f"  {rel}: {terms}")

    if not no_glossary_only:
        print(f"\n=== Pages with jargon-bearing diagrams, NO Key Terms table at all ({len(no_glossary_gap)}) ===")
        for rel, terms in no_glossary_gap:
            print(f"  {rel}: {terms}")

    print(f"\nSummary: {len(has_glossary_gap)} glossary-gap pages (fast fix), "
          f"{len(no_glossary_gap)} no-glossary pages (need a new section)")


if __name__ == '__main__':
    main()
