#!/usr/bin/env python3
"""
Generate troubleshooting overview SVGs for KB troubleshooting pages.

One SVG per page; diagram type determined by filename:
  common-issues  → Symptom → Root Cause → Fix flow
  diagnostics    → Diagnostic decision flow
  escalation     → Escalation path
  known-issues   → Bug lifecycle flow

Usage:
  python3 scripts/generate_svgs_troubleshooting.py --dry-run
  python3 scripts/generate_svgs_troubleshooting.py
  python3 scripts/generate_svgs_troubleshooting.py --path virtualization/vmware
"""
import argparse
import re
from pathlib import Path
from xml.etree import ElementTree as ET

REPO  = Path(__file__).parent.parent.resolve()
DOCS  = REPO / 'docs'
ASSETS= REPO / 'docs' / 'assets'

NAVY      = '#1a2744'
GREEN     = '#2e7d32'
GREEN_L   = '#e8f5e9'
TEXT_DARK = '#1a2744'
TEXT_MID  = '#37474f'
TEXT_LIGHT= '#78909c'
FOOTER_FG = '#7a8fbb'

SVG_W = 820
SVG_H = 200
HDR_H = 42
FTR_H = 26
FTR_Y = SVG_H - FTR_H
BOX_Y = HDR_H + 14
BOX_H = 58
PAD   = 18
ARW_W = 14

PAGE_TYPES = {
    'common-issues': {
        'subtitle': 'Symptom → Root Cause → Fix Flow',
        'boxes': [
            ('Symptom', 'Observed', '#fce4ec', '#c62828'),
            ('Triage', 'Logs & Events', '#fff8e1', '#f57f17'),
            ('Root', 'Cause', '#e3f2fd', '#1565c0'),
            ('Apply', 'Fix', '#e8eaf6', '#3949ab'),
            ('✓ Verify', 'Resolved', GREEN_L, GREEN),
        ],
    },
    'diagnostics': {
        'subtitle': 'Diagnostic Decision Flow',
        'boxes': [
            ('Collect', 'Logs', '#e3f2fd', '#1565c0'),
            ('Check', 'Services', '#e8eaf6', '#3949ab'),
            ('Test', 'Connectivity', '#fff8e1', '#f57f17'),
            ('Review', 'Events', '#fce4ec', '#c62828'),
            ('✓ Document', 'Findings', GREEN_L, GREEN),
        ],
    },
    'escalation': {
        'subtitle': 'Escalation Path',
        'boxes': [
            ('L1', 'Triage', '#e3f2fd', '#1565c0'),
            ('L2', 'Engineer', '#e8eaf6', '#3949ab'),
            ('L3', 'Architect', '#fff8e1', '#f57f17'),
            ('Vendor', 'TAC / SR', '#fce4ec', '#c62828'),
            ('✓ RCA', 'Documented', GREEN_L, GREEN),
        ],
    },
    'known-issues': {
        'subtitle': 'Known Issue Lifecycle',
        'boxes': [
            ('Issue', 'Identified', '#fce4ec', '#c62828'),
            ('Severity', 'Assessed', '#fff8e1', '#f57f17'),
            ('Workaround', 'Applied', '#e3f2fd', '#1565c0'),
            ('Patch /\nFix', 'Released', '#e8eaf6', '#3949ab'),
            ('✓ Verified', 'Resolved', GREEN_L, GREEN),
        ],
    },
}

_ASCII_RE   = re.compile(r'```text\n┌[^`]*?┘[ \t]*\n```', re.DOTALL)
_H1_RE      = re.compile(r'^# .+$', re.MULTILINE)
_SUMMARY_RE = re.compile(r'<div class="kb-summary">.*?</div>', re.DOTALL)


def xe(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _rel_assets(page: Path) -> str:
    depth = len(page.parts) - len(DOCS.parts) - 1
    return '../' * depth + 'assets/'


def _product_label(page: Path) -> str:
    parts = page.parts
    docs_idx = next(i for i, p in enumerate(parts) if p == 'docs')
    segs = [s for s in parts[docs_idx + 1: -2] if s not in ('troubleshooting',)]
    return ' / '.join(s.replace('-', ' ').title() for s in segs[:3])


def make_troubleshooting_svg(page_type: str, product_label: str, page_title: str) -> str:
    cfg = PAGE_TYPES[page_type]
    boxes = cfg['boxes']
    n = len(boxes)
    total_arrow = (n - 1) * ARW_W
    box_w = (SVG_W - 2 * PAD - total_arrow) // n

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{SVG_H}" '
        f"font-family=\"'Segoe UI',Arial,sans-serif\">",
        f'  <rect width="{SVG_W}" height="{SVG_H}" fill="#f4f6f9"/>',
        f'  <rect x="0" y="0" width="{SVG_W}" height="{HDR_H}" fill="{NAVY}"/>',
        f'  <text x="410" y="25" text-anchor="middle" fill="white" '
        f'font-size="13" font-weight="700">{xe(page_title[:80])}</text>',
        f'  <text x="410" y="37" text-anchor="middle" fill="{FOOTER_FG}" '
        f'font-size="9">{xe(product_label)} — {xe(cfg["subtitle"])}</text>',
    ]

    x = PAD
    for i, (l1, l2, fill, stroke) in enumerate(boxes):
        # Handle multiline label (using \n in the source)
        l1_clean = l1.replace('\n', ' ').strip()
        cx = x + box_w // 2
        lines.append(
            f'  <rect x="{x}" y="{BOX_Y}" width="{box_w}" height="{BOX_H}" '
            f'fill="{fill}" rx="4" stroke="{stroke}" stroke-width="1.5"/>'
        )
        ty = BOX_Y + (BOX_H // 2 - (5 if l2 else 0))
        lines.append(
            f'  <text x="{cx}" y="{ty}" text-anchor="middle" '
            f'fill="{TEXT_DARK}" font-size="10" font-weight="700">{xe(l1_clean)}</text>'
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
        f'fill="{FOOTER_FG}" font-size="9">{xe(product_label)} · Troubleshooting Reference</text>',
        '</svg>',
    ]

    svg = '\n'.join(lines)
    ET.fromstring(svg)
    return svg


def _slug_from_path(page: Path) -> str:
    parts = page.parts
    docs_idx = next(i for i, p in enumerate(parts) if p == 'docs')
    slug = '-'.join(parts[docs_idx + 1:]).replace('/', '-').replace('.md', '')
    return re.sub(r'[^a-z0-9-]', '-', slug.lower()).strip('-')[:60]


def _page_title(text: str, page: Path) -> str:
    m = _H1_RE.search(text)
    if m:
        return m.group(0).lstrip('# ').strip()
    return page.stem.replace('-', ' ').title()


def process_page(page: Path, dry_run: bool = False, verbose: bool = True) -> int:
    page_type = page.stem
    if page_type not in PAGE_TYPES:
        return 0

    text = page.read_text(encoding='utf-8')
    product_label = _product_label(page)
    title = _page_title(text, page)
    rel_assets = _rel_assets(page)
    svg_fname = _slug_from_path(page) + '.svg'
    svg_path  = ASSETS / svg_fname

    if verbose:
        mode = 'DRY RUN' if dry_run else 'GENERATE'
        print(f'[{mode}] {page.relative_to(REPO)} [{page_type}]')

    if not dry_run:
        svg = make_troubleshooting_svg(page_type, product_label, title)
        svg_path.write_text(svg, encoding='utf-8')

        new_text = _ASCII_RE.sub('', text)
        img_ref = f'\n![{title}]({rel_assets}{svg_fname})\n'
        if _SUMMARY_RE.search(new_text):
            new_text = _SUMMARY_RE.sub(lambda m: m.group(0) + img_ref, new_text, count=1)
        else:
            new_text = _H1_RE.sub(lambda m: m.group(0) + img_ref, new_text, count=1)
        page.write_text(new_text, encoding='utf-8')

    return 1


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--path', help='Limit to pages under this docs/ subpath')
    args = parser.parse_args()

    pages = [
        p for p in sorted(DOCS.rglob('*.md'))
        if p.stem in PAGE_TYPES and '/troubleshooting/' in str(p)
    ]
    if args.path:
        pages = [p for p in pages if args.path in str(p)]

    total = 0
    for page in pages:
        total += process_page(page, dry_run=args.dry_run, verbose=True)

    print(f'\nTotal SVGs {"(dry run)" if args.dry_run else "generated"}: {total}')


if __name__ == '__main__':
    main()
