#!/usr/bin/env python3
"""
Generate per-section health flowchart SVGs for KB health-checks.md pages.

For each ## section in a health-checks page:
  - Generates a compact horizontal health flowchart SVG (820 × 200 px)
  - Writes to docs/assets/
  - Removes the existing page-level ASCII overview block
  - Injects an SVG img reference immediately after each ## heading

Usage:
  python3 scripts/generate_svgs_health.py --dry-run
  python3 scripts/generate_svgs_health.py
  python3 scripts/generate_svgs_health.py --path virtualization/vmware/vsan
"""
import argparse
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

REPO = Path(__file__).parent.parent.resolve()
DOCS = REPO / 'docs'
ASSETS = REPO / 'docs' / 'assets'

# Sections to skip (standard boilerplate, not actual checks)
SKIP_SECTIONS = {
    'before you begin', 'run this routine', 'see also', 'verify',
    'change readiness checklist', 'change readiness', 'when to restore from backup',
    'health summary table', 'pre-change checklist', 'verify checks',
    'escalation', 'escalation path', 'summary',
}

# Colour tokens
NAVY      = '#1a2744'
BLUE      = '#1565c0'
BLUE_L    = '#e3f2fd'
GREEN     = '#2e7d32'
GREEN_L   = '#e8f5e9'
ORANGE    = '#e65100'
ORANGE_L  = '#fff3e0'
TEXT_DARK = '#1a2744'
TEXT_MID  = '#37474f'
TEXT_LIGHT= '#78909c'
FOOTER_FG = '#7a8fbb'

SVG_W  = 820
SVG_H  = 200
HDR_H  = 42
FTR_H  = 26
FTR_Y  = SVG_H - FTR_H
BOX_Y  = HDR_H + 14
BOX_H  = 58
PAD    = 18
ARW_W  = 14


def xe(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _slug(product: str, heading: str) -> str:
    h = re.sub(r'[^a-z0-9]+', '-', heading.lower()).strip('-')
    prefix = f'{product}-hc-'
    max_h = 80 - len(prefix) - len('.svg')
    return prefix + h[:max_h] + '.svg'


def _wrap(text: str, width: int = 13) -> tuple:
    words = text.split()
    line1, line2 = '', ''
    for w in words:
        if len(line1) + len(w) + (1 if line1 else 0) <= width:
            line1 += (' ' if line1 else '') + w
        elif len(line2) + len(w) + (1 if line2 else 0) <= width:
            line2 += (' ' if line2 else '') + w
        else:
            break
    if len(line2) > width:
        line2 = line2[:width - 1] + '…'
    return line1, line2


def _rel_assets(page_abs: Path) -> str:
    depth = len(page_abs.parts) - len(DOCS.parts) - 1
    return '../' * depth + 'assets/'


def make_health_svg(check_title: str, product_label: str) -> str:
    """820×200 health flowchart: Execute → Verify → Pass ✓ / Fail ✗ → Remediate."""
    boxes = [
        ('Execute', 'Check', BLUE_L, BLUE),
        ('Review', 'Output', '#e8eaf6', '#3949ab'),
        ('✓ Pass', '', GREEN_L, GREEN),
        ('Remediate', 'if Fail', ORANGE_L, ORANGE),
    ]
    n = len(boxes)
    total_arrow = (n - 1) * ARW_W
    box_w = (SVG_W - 2 * PAD - total_arrow) // n

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{SVG_H}" '
        f"font-family=\"'Segoe UI',Arial,sans-serif\">",
        f'  <rect width="{SVG_W}" height="{SVG_H}" fill="#f4f6f9"/>',
        f'  <rect x="0" y="0" width="{SVG_W}" height="{HDR_H}" fill="{NAVY}"/>',
        f'  <text x="410" y="25" text-anchor="middle" fill="white" '
        f'font-size="13" font-weight="700">{xe(check_title[:90])}</text>',
        f'  <text x="410" y="37" text-anchor="middle" fill="{FOOTER_FG}" '
        f'font-size="9">{xe(product_label)} — Health Check</text>',
    ]

    x = PAD
    for i, (l1, l2, fill, stroke) in enumerate(boxes):
        cx = x + box_w // 2
        lines.append(
            f'  <rect x="{x}" y="{BOX_Y}" width="{box_w}" height="{BOX_H}" '
            f'fill="{fill}" rx="4" stroke="{stroke}" stroke-width="1.5"/>'
        )
        ty = BOX_Y + (BOX_H // 2 - (5 if l2 else 0))
        lines.append(
            f'  <text x="{cx}" y="{ty}" text-anchor="middle" '
            f'fill="{TEXT_DARK}" font-size="10" font-weight="700">{xe(l1)}</text>'
        )
        if l2:
            lines.append(
                f'  <text x="{cx}" y="{ty + 14}" text-anchor="middle" '
                f'fill="{TEXT_MID}" font-size="9">{xe(l2)}</text>'
            )
        if i < n - 1:
            ax = x + box_w
            ay = BOX_Y + BOX_H // 2
            lines += [
                f'  <line x1="{ax}" y1="{ay}" x2="{ax + ARW_W - 3}" y2="{ay}" '
                f'stroke="{TEXT_LIGHT}" stroke-width="1.5"/>',
                f'  <polygon points="{ax + ARW_W - 3},{ay - 4} '
                f'{ax + ARW_W + 1},{ay} {ax + ARW_W - 3},{ay + 4}" fill="{TEXT_LIGHT}"/>',
            ]
        x += box_w + ARW_W

    lines += [
        f'  <rect x="0" y="{FTR_Y}" width="{SVG_W}" height="{FTR_H}" fill="{NAVY}"/>',
        f'  <text x="410" y="{FTR_Y + 16}" text-anchor="middle" '
        f'fill="{FOOTER_FG}" font-size="9">{xe(product_label)} · Health Checks Reference</text>',
        '</svg>',
    ]

    svg = '\n'.join(lines)
    ET.fromstring(svg)
    return svg


_ASCII_RE  = re.compile(r'```text\n┌[^`]*?┘[ \t]*\n```', re.DOTALL)
_HEADING_RE = re.compile(r'^## (.+)$', re.MULTILINE)


def product_label_from_path(page: Path) -> str:
    """Derive a human-friendly product label from the file path."""
    parts = page.parts
    docs_idx = next(i for i, p in enumerate(parts) if p == 'docs')
    # Take up to 2 path segments after docs/
    segs = parts[docs_idx + 1: docs_idx + 4]
    label = ' / '.join(s.replace('-', ' ').title() for s in segs if s != 'operations')
    return label


def process_page(page: Path, dry_run: bool = False, verbose: bool = True) -> int:
    text = page.read_text(encoding='utf-8')
    label = product_label_from_path(page)
    rel_assets = _rel_assets(page)

    # Find ## check sections (skip boilerplate)
    sections = []
    for m in _HEADING_RE.finditer(text):
        title = m.group(1).strip()
        if title.lower() in SKIP_SECTIONS:
            continue
        sections.append(title)

    if not sections:
        if verbose:
            print(f'  SKIP {page.relative_to(REPO)}: no check sections found')
        return 0

    has_ascii = bool(_ASCII_RE.search(text))
    if verbose:
        mode = 'DRY RUN' if dry_run else 'GENERATE'
        print(f'[{mode}] {page.relative_to(REPO)} — {len(sections)} checks, ASCII: {has_ascii}')

    # Determine slug prefix from path
    parts = page.parts
    docs_idx = next(i for i, p in enumerate(parts) if p == 'docs')
    slug = '-'.join(parts[docs_idx + 1: -2]).replace('/', '-')
    slug = re.sub(r'[^a-z0-9-]', '-', slug.lower()).strip('-')[:40]

    injections = []
    for title in sections:
        svg_fname = _slug(slug, title)
        svg_path  = ASSETS / svg_fname
        if not dry_run:
            svg = make_health_svg(title, label)
            svg_path.write_text(svg, encoding='utf-8')
        injections.append((title, svg_fname))

    if not dry_run:
        new_text = _ASCII_RE.sub('', text)
        for heading, svg_fname in injections:
            pattern = re.compile(r'(^## ' + re.escape(heading) + r'[ \t]*\n)', re.MULTILINE)
            img_ref = f'![{heading}]({rel_assets}{svg_fname})'
            new_text = pattern.sub(r'\1\n' + img_ref + '\n', new_text, count=1)
        page.write_text(new_text, encoding='utf-8')
        if verbose:
            print(f'  → injected {len(injections)} SVGs, removed ASCII')

    return len(injections)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--path', help='Limit to pages under this docs/ subpath')
    args = parser.parse_args()

    pages = sorted(DOCS.rglob('health-checks.md'))
    if args.path:
        pages = [p for p in pages if args.path in str(p)]

    total = 0
    for page in pages:
        total += process_page(page, dry_run=args.dry_run)

    print(f'\nTotal SVGs {"(dry run)" if args.dry_run else "generated"}: {total}')


if __name__ == '__main__':
    main()
