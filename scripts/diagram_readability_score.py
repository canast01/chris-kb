"""
Phase 0 of the Diagram Readability Project: scan every diagram in the KB and
score it on quantifiable proxies for the agreed criteria (see
project_diagram_readability.md in Claude's memory system) -- density, text
overflow, unexplained jargon, and generic/missing alt text. Output is a
ranked report only; this script does not fix anything.

Covers all 3 diagram forms used in this KB:
  - SVG assets referenced via markdown image syntax
  - ```d2 fenced blocks
  - ```plantuml fenced blocks

Usage:
  python3 scripts/diagram_readability_score.py            # full report
  python3 scripts/diagram_readability_score.py --top 50    # worst N only
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_overflow_check import analyze_svg, local_text, walk_absolute, NS

DOCS = Path(__file__).resolve().parent.parent / 'docs'

IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+\.svg)\)')
D2_BLOCK_RE = re.compile(r'```d2\n(.*?)\n```', re.DOTALL)
PLANTUML_BLOCK_RE = re.compile(r'```plantuml\n(.*?)\n```', re.DOTALL)

# Acronyms common enough that even an incoming IT-degree freshman likely
# already knows them (or they're explained in virtually every intro course) --
# excluded from jargon flags so the list surfaces genuine vendor/domain
# friction (VRA, RPO, SRDF) instead of drowning in ubiquitous ones.
COMMON_KNOWLEDGE = {
    'CPU', 'RAM', 'IP', 'URL', 'HTTP', 'HTTPS', 'USB', 'ID', 'OS', 'UI',
    'API', 'CLI', 'GUI', 'PDF', 'FAQ', 'DNS', 'SSD', 'HDD', 'GB', 'MB', 'TB',
    'WIFI', 'LAN', 'WAN', 'VM', 'CI', 'CD',
}
ACRONYM_RE = re.compile(r'\b[A-Z]{2,8}[A-Z0-9]*\b')

GENERIC_ALT_RE = re.compile(r'^[\w\s—-]+ (Diagram|Overview)$', re.IGNORECASE)

# Filter out plain English words used as ALL-CAPS section headers/style
# (e.g. "PLATFORM", "SECURITY", "MANAGEMENT" as a diagram section title) --
# these aren't jargon needing explanation, but a naive "any all-caps token"
# regex flags them the same as real acronyms. A dictionary check ALONE is
# not enough: real jargon like RAID, SAN, FABRIC, ZONING also happen to be
# dictionary words. Length is the deciding factor -- verified 2026-07-09
# against real output: every genuine false-positive word was 7+ characters
# (PLATFORM, SECURITY, MANAGEMENT, CAPABILITIES, TOPOLOGY...) while every
# real short acronym stayed under that (SAN=3, RAID=4, FABRIC=6, ZONING=6).
try:
    with open('/usr/share/dict/words') as _f:
        _DICT_WORDS = {w.strip().lower() for w in _f}
except FileNotFoundError:
    _DICT_WORDS = set()

MIN_JARGON_LEN_FOR_DICT_CHECK = 7


def is_plain_english_header(token: str) -> bool:
    return len(token) >= MIN_JARGON_LEN_FOR_DICT_CHECK and token.lower() in _DICT_WORDS


def find_diagrams_in_page(md_path):
    text = md_path.read_text(errors='replace')
    diagrams = []
    for m in IMG_RE.finditer(text):
        alt, rel_path = m.group(1), m.group(2)
        svg_path = (md_path.parent / rel_path).resolve()
        diagrams.append({'type': 'svg', 'page': md_path, 'alt': alt, 'svg_path': svg_path})
    for m in D2_BLOCK_RE.finditer(text):
        diagrams.append({'type': 'd2', 'page': md_path, 'body': m.group(1)})
    for m in PLANTUML_BLOCK_RE.finditer(text):
        diagrams.append({'type': 'plantuml', 'page': md_path, 'body': m.group(1)})
    return diagrams


def extract_svg_labels(svg_path):
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(svg_path)
    except Exception:
        return None
    root = tree.getroot()
    labels = []
    text_count = 0
    for elem, _, _ in walk_absolute(root):
        if elem.tag == f'{NS}text':
            content = local_text(elem)
            if content:
                labels.append(content)
                text_count += 1
    return labels, text_count


def jargon_hits(labels_text, page_prose):
    """Acronyms appearing in diagram labels with no nearby spelled-out
    expansion (checked against the surrounding page's prose, not just the
    diagram itself -- diagram + adjacent prose together satisfy the
    self-sufficiency bar per the user's chosen option)."""
    found = set()
    for label in labels_text:
        for m in ACRONYM_RE.finditer(label):
            acronym = m.group(0)
            if acronym in COMMON_KNOWLEDGE:
                continue
            if is_plain_english_header(acronym):
                continue
            found.add(acronym)

    unexplained = []
    for acronym in found:
        # crude expansion check: does the prose contain the acronym inside
        # parens (spelled out first) or immediately after a capitalized
        # multi-word phrase, e.g. "Recovery Point Objective (RPO)"?
        expansion_pattern = re.compile(
            r'[A-Z][\w/]+(?:\s+[A-Z][\w/]+){1,5}\s*\(' + re.escape(acronym) + r'\)'
        )
        if not expansion_pattern.search(page_prose) and f'({acronym})' not in page_prose:
            unexplained.append(acronym)
    return sorted(unexplained)


def score_svg_diagram(d):
    svg_path = d['svg_path']
    if not svg_path.exists():
        return None
    result = extract_svg_labels(svg_path)
    if result is None:
        return None
    labels, text_count = result

    findings, err = analyze_svg(svg_path)
    overflow_count = len(findings) if not err else 0

    page_prose = d['page'].read_text(errors='replace')
    jargon = jargon_hits(labels, page_prose)

    alt = d['alt'].strip()
    generic_alt = bool(GENERIC_ALT_RE.match(alt)) or len(alt) < 8

    score = (
        overflow_count * 10
        + len(jargon) * 5
        + (8 if generic_alt else 0)
        + max(0, text_count - 20)  # density penalty above ~20 labels
    )
    return {
        'page': str(d['page'].relative_to(DOCS.parent)),
        'diagram': svg_path.name,
        'type': 'svg',
        'text_count': text_count,
        'overflow_count': overflow_count,
        'jargon': jargon,
        'generic_alt': generic_alt,
        'alt': alt,
        'score': score,
    }


def score_text_diagram(d):
    body = d['body']
    if d['type'] == 'd2':
        node_count = len(re.findall(r'^\s*[\w."\']+\s*:\s*["\']?[^{]*\{?\s*(shape:|$)', body, re.MULTILINE))
        edge_count = body.count('->') + body.count('<-')
    else:  # plantuml
        node_count = len(re.findall(r'^\s*(participant|actor|entity)\s', body, re.MULTILINE))
        edge_count = len(re.findall(r'-->|->|\.\.>', body))

    page_prose = d['page'].read_text(errors='replace')
    label_texts = re.findall(r'"([^"]+)"', body)
    jargon = jargon_hits(label_texts, page_prose)

    score = len(jargon) * 5 + max(0, node_count - 15)
    return {
        'page': str(d['page'].relative_to(DOCS.parent)),
        'diagram': f"{d['type']} block",
        'type': d['type'],
        'node_count': node_count,
        'edge_count': edge_count,
        'jargon': jargon,
        'score': score,
    }


def main():
    top_n = None
    if '--top' in sys.argv:
        top_n = int(sys.argv[sys.argv.index('--top') + 1])

    results = []
    pages = list(DOCS.rglob('*.md'))
    print(f'Scanning {len(pages)} pages...', file=sys.stderr)

    for i, md_path in enumerate(pages):
        for d in find_diagrams_in_page(md_path):
            if d['type'] == 'svg':
                r = score_svg_diagram(d)
            else:
                r = score_text_diagram(d)
            if r:
                results.append(r)
        if i % 500 == 0:
            print(f'  ...{i}/{len(pages)} pages scanned', file=sys.stderr)

    results.sort(key=lambda r: -r['score'])
    if top_n:
        results = results[:top_n]

    print(f'\n{len(results)} diagrams scored (worst first):\n')
    for r in results:
        if r['score'] == 0:
            continue
        extra = f"jargon={r['jargon']}" if r['jargon'] else ''
        if r['type'] == 'svg':
            print(f"[{r['score']:3d}] {r['page']} -- {r['diagram']} "
                  f"(labels={r['text_count']}, overflow={r['overflow_count']}, "
                  f"generic_alt={r['generic_alt']}) {extra}")
        else:
            print(f"[{r['score']:3d}] {r['page']} -- {r['diagram']} "
                  f"(nodes={r['node_count']}, edges={r['edge_count']}) {extra}")


if __name__ == '__main__':
    main()
