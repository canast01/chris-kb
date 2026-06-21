#!/usr/bin/env python3
"""
Generate per-procedure workflow SVG diagrams for KB procedures.md pages.

For each ### section in a procedures page:
  - Extracts step names from **Step N — description** patterns
  - Generates a compact horizontal workflow SVG (820 × 240 px)
  - Writes to docs/assets/
  - Removes the existing page-level ASCII overview block
  - Injects an SVG img reference immediately after each ### heading

Usage:
  python3 scripts/generate_svgs_procedures.py --dry-run --product vsan
  python3 scripts/generate_svgs_procedures.py --product vsan
  python3 scripts/generate_svgs_procedures.py --product vsan vcenter nsx
  python3 scripts/generate_svgs_procedures.py --all
"""
import argparse
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

REPO = Path(__file__).parent.parent.resolve()
DOCS = REPO / 'docs'
ASSETS = REPO / 'docs' / 'assets'

# ── Colour tokens ─────────────────────────────────────────────────────────────
NAVY       = '#1a2744'
BLUE       = '#1565c0'
BLUE_L     = '#e3f2fd'
GREEN      = '#2e7d32'
GREEN_L    = '#e8f5e9'
GREY       = '#546e7a'
GREY_L     = '#eceff1'
TEXT_DARK  = '#1a2744'
TEXT_MID   = '#37474f'
TEXT_LIGHT = '#78909c'
FOOTER_FG  = '#7a8fbb'

# ── Canvas ────────────────────────────────────────────────────────────────────
SVG_W    = 820
SVG_H    = 240
HDR_H    = 46
FTR_H    = 28
FTR_Y    = SVG_H - FTR_H
BOX_Y    = HDR_H + 16
BOX_H    = 62
PAD      = 22
ARROW_W  = 16
MAX_DISP = 5   # max step boxes before truncating

# ── Product registry ──────────────────────────────────────────────────────────
# Maps product slug → relative path from DOCS to procedures.md
PRODUCTS = {
    # VMware
    'vsan':                   'virtualization/vmware/vsan/operations/procedures.md',
    'vcenter':                'virtualization/vmware/vcenter/operations/procedures.md',
    'esxi':                   'virtualization/vmware/esxi/operations/procedures.md',
    'nsx':                    'virtualization/vmware/nsx/operations/procedures.md',
    'vmware-cloud-foundation': 'virtualization/vmware/vmware-cloud-foundation/operations/procedures.md',
    'vxrail':                 'virtualization/vmware/vxrail/operations/procedures.md',
    'srm':                    'virtualization/vmware/srm/operations/procedures.md',
    'vsphere-replication':    'virtualization/vmware/vsphere-replication/operations/procedures.md',
    'tanzu':                  'virtualization/vmware/tanzu/operations/procedures.md',
    'horizon':                'virtualization/vmware/horizon/operations/procedures.md',
    'aria-automation':        'virtualization/vmware/aria-automation/operations/procedures.md',
    'aria-suite-lifecycle':   'virtualization/vmware/aria-suite-lifecycle/operations/procedures.md',
    'aria-operations':        'virtualization/vmware/aria-operations/operations/procedures.md',
    'aria-operations-for-logs': 'virtualization/vmware/aria-operations-for-logs/operations/procedures.md',
    'aria-operations-for-networks': 'virtualization/vmware/aria-operations-for-networks/operations/procedures.md',
    'powercli':               'virtualization/vmware/powercli/operations/procedures.md',
    # Pure Storage
    'flasharray':             'storage/pure/flasharray/operations/procedures.md',
    'flashblade':             'storage/pure/flashblade/operations/procedures.md',
    'evergreen':              'storage/pure/evergreen/operations/procedures.md',
    # NetApp
    'ontap':                  'storage/netapp/ontap/operations/procedures.md',
    'snapmirror':             'storage/netapp/snapmirror/operations/procedures.md',
    'snapcenter':             'storage/netapp/snapcenter/operations/procedures.md',
    'superna-eyeglass':       'storage/netapp/superna-eyeglass/operations/procedures.md',
    'keystone':               'storage/netapp/keystone/operations/procedures.md',
    # Dell Storage
    'unity':                  'storage/dell/unity/operations/procedures.md',
    'powermax':               'storage/dell/powermax/operations/procedures.md',
    'vplex':                  'storage/dell/vplex/operations/procedures.md',
    'powerstore':             'storage/dell/powerstore/operations/procedures.md',
    'recoverpoint':           'storage/dell/recoverpoint/operations/procedures.md',
    'srdf-a':                 'storage/dell/srdf-a/operations/procedures.md',
    'powerscale':             'storage/dell/powerscale/operations/procedures.md',
    'data-domain':            'storage/dell/data-domain/operations/procedures.md',
    'ecs':                    'storage/dell/ecs/operations/procedures.md',
    # SAN / Compute
    'nexus-dashboard':        'san/cisco/nexus-dashboard/operations/procedures.md',
    'cisco-mds':              'san/cisco/mds/operations/procedures.md',
    'fabric-os':              'san/brocade/fabric-os/operations/procedures.md',
    'active-directory':       'compute/windows-server/active-directory/operations/procedures.md',
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def xe(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _slug(product: str, heading: str) -> str:
    """Generate a safe SVG filename."""
    h = re.sub(r'[^a-z0-9]+', '-', heading.lower()).strip('-')
    # Keep total filename ≤ 80 chars
    prefix = f'{product}-proc-'
    max_h = 80 - len(prefix) - len('.svg')
    return prefix + h[:max_h] + '.svg'


def _wrap(text: str, width: int = 15) -> tuple:
    """Split text into (line1, line2) fitting within width chars each."""
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
    """Return relative path from page to docs/assets/."""
    depth = len(page_abs.parts) - len(DOCS.parts) - 1
    return '../' * depth + 'assets/'


# ── SVG builder ───────────────────────────────────────────────────────────────

def make_procedure_svg(proc_title: str, product_label: str,
                       steps: list, n_total: int) -> str:
    """
    Compact 820×240 workflow SVG showing steps → Verify.
    steps: list of step name strings to display.
    n_total: actual total step count (for subtitle).
    """
    # Truncate display to MAX_DISP + 1 verify box
    if len(steps) > MAX_DISP:
        shown = steps[:MAX_DISP - 1] + [f'+{n_total - (MAX_DISP - 1)} more']
    else:
        shown = steps[:]

    n_boxes = len(shown) + 1   # +1 for Verify
    total_arrow = (n_boxes - 1) * ARROW_W
    box_w = max(80, (SVG_W - 2 * PAD - total_arrow) // n_boxes)

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{SVG_H}" '
        f"font-family=\"'Segoe UI',Arial,sans-serif\">",
        f'  <rect width="{SVG_W}" height="{SVG_H}" fill="#f4f6f9"/>',
        # Header
        f'  <rect x="0" y="0" width="{SVG_W}" height="{HDR_H}" fill="{NAVY}"/>',
        f'  <text x="410" y="28" text-anchor="middle" fill="white" '
        f'font-size="14" font-weight="700">{xe(proc_title[:90])}</text>',
        f'  <text x="410" y="41" text-anchor="middle" fill="{FOOTER_FG}" '
        f'font-size="10">{xe(product_label)} — {n_total} step{"s" if n_total != 1 else ""}</text>',
    ]

    x = PAD
    for i, step in enumerate(shown):
        cx = x + box_w // 2
        is_more = step.startswith('+')
        fill   = GREY_L if is_more else BLUE_L
        stroke = GREY   if is_more else BLUE
        num_c  = GREY   if is_more else BLUE

        lines.append(
            f'  <rect x="{x}" y="{BOX_Y}" width="{box_w}" height="{BOX_H}" '
            f'fill="{fill}" rx="4" stroke="{stroke}" stroke-width="1.5"/>'
        )
        if not is_more:
            # Number circle
            lines += [
                f'  <circle cx="{cx}" cy="{BOX_Y + 13}" r="11" fill="{num_c}"/>',
                f'  <text x="{cx}" y="{BOX_Y + 18}" text-anchor="middle" '
                f'fill="white" font-size="10" font-weight="700">{i + 1}</text>',
            ]
            l1, l2 = _wrap(step, 15)
            ty = BOX_Y + (35 if not l2 else 30)
            lines.append(
                f'  <text x="{cx}" y="{ty}" text-anchor="middle" '
                f'fill="{TEXT_DARK}" font-size="9" font-weight="600">{xe(l1)}</text>'
            )
            if l2:
                lines.append(
                    f'  <text x="{cx}" y="{ty + 12}" text-anchor="middle" '
                    f'fill="{TEXT_MID}" font-size="8">{xe(l2)}</text>'
                )
        else:
            # "…more" pill
            lines.append(
                f'  <text x="{cx}" y="{BOX_Y + 35}" text-anchor="middle" '
                f'fill="{TEXT_LIGHT}" font-size="9">{xe(step)}</text>'
            )

        # Arrow →
        ax = x + box_w
        ay = BOX_Y + BOX_H // 2
        lines += [
            f'  <line x1="{ax}" y1="{ay}" x2="{ax + ARROW_W - 4}" y2="{ay}" '
            f'stroke="{TEXT_LIGHT}" stroke-width="1.5"/>',
            f'  <polygon points="{ax + ARROW_W - 4},{ay - 4} '
            f'{ax + ARROW_W + 1},{ay} {ax + ARROW_W - 4},{ay + 4}" fill="{TEXT_LIGHT}"/>',
        ]
        x += box_w + ARROW_W

    # Verify box
    cx = x + box_w // 2
    lines += [
        f'  <rect x="{x}" y="{BOX_Y}" width="{box_w}" height="{BOX_H}" '
        f'fill="{GREEN_L}" rx="4" stroke="{GREEN}" stroke-width="1.5"/>',
        f'  <circle cx="{cx}" cy="{BOX_Y + 13}" r="11" fill="{GREEN}"/>',
        f'  <text x="{cx}" y="{BOX_Y + 18}" text-anchor="middle" '
        f'fill="white" font-size="13" font-weight="700">✓</text>',
        f'  <text x="{cx}" y="{BOX_Y + 36}" text-anchor="middle" '
        f'fill="#1b5e20" font-size="9" font-weight="600">Verify</text>',
        f'  <text x="{cx}" y="{BOX_Y + 49}" text-anchor="middle" '
        f'fill="#2e7d32" font-size="8">&amp; Complete</text>',
    ]

    # Footer
    lines += [
        f'  <rect x="0" y="{FTR_Y}" width="{SVG_W}" height="{FTR_H}" fill="{NAVY}"/>',
        f'  <text x="410" y="{FTR_Y + 18}" text-anchor="middle" '
        f'fill="{FOOTER_FG}" font-size="9">{xe(product_label)} · Procedures Reference</text>',
        '</svg>',
    ]

    svg = '\n'.join(lines)

    # Validate XML
    try:
        ET.fromstring(svg)
    except ET.ParseError as e:
        raise ValueError(f'SVG XML invalid for "{proc_title}": {e}') from e

    return svg


# ── Page parser ───────────────────────────────────────────────────────────────

_STEP_RE   = re.compile(r'\*\*Step \d+\s*[—–-]\s*([^\*\n]+)\*\*')
_HEADING_RE = re.compile(r'^### (.+)$', re.MULTILINE)
_ASCII_RE   = re.compile(r'```text\n┌[^`]*?┘[ \t]*\n```', re.DOTALL)


def parse_procedures(text: str) -> list:
    """
    Return list of (heading: str, steps: list[str]) for each ### section.
    steps are extracted from **Step N — description** patterns.
    """
    results = []
    # Split into chunks at each ### boundary
    chunks = re.split(r'\n(?=### )', text)
    for chunk in chunks:
        m = re.match(r'^### ([^\n]+)', chunk)
        if not m:
            continue
        heading = m.group(1).strip()
        body = chunk[m.end():]
        steps = _STEP_RE.findall(body)
        # Fallback: numbered list **bold items**
        if not steps:
            steps = re.findall(r'^\d+\.\s+\*\*([^\*\n]+)\*\*', body, re.MULTILINE)
        # Fallback: count bare "Step N" occurrences
        if not steps:
            count = len(re.findall(r'\*\*Step \d+', body))
            if count:
                steps = [f'Step {i + 1}' for i in range(count)]
        results.append((heading, steps))
    return results


# ── Per-product processor ─────────────────────────────────────────────────────

def process_product(slug: str, rel_path: str,
                    dry_run: bool = False, verbose: bool = True) -> int:
    """
    Process one product's procedures.md.
    Returns number of SVGs generated (or that would be generated).
    """
    page = DOCS / rel_path
    if not page.exists():
        print(f'  SKIP {slug}: file not found ({rel_path})')
        return 0

    text = page.read_text(encoding='utf-8')
    procedures = parse_procedures(text)
    if not procedures:
        print(f'  SKIP {slug}: no ### sections found')
        return 0

    # Derive display label from product slug
    product_label = slug.replace('-', ' ').title()
    rel_assets = _rel_assets(page)

    if verbose:
        mode = 'DRY RUN' if dry_run else 'GENERATE'
        print(f'\n[{mode}] {slug} — {page.relative_to(REPO)}')
        print(f'  Found {len(procedures)} procedures')

    has_ascii = bool(_ASCII_RE.search(text))
    if verbose:
        print(f'  ASCII overview block: {"found — will remove" if has_ascii else "not found"}')

    injections = []   # (heading, svg_filename) for page injection
    count = 0

    for i, (heading, steps) in enumerate(procedures):
        svg_fname = _slug(slug, heading)
        svg_path  = ASSETS / svg_fname
        n_total   = len(steps)

        if verbose:
            step_preview = ', '.join(steps[:3])
            if len(steps) > 3:
                step_preview += f', … ({n_total} total)'
            print(f'  [{i + 1}/{len(procedures)}] {heading}')
            if steps:
                print(f'    Steps ({n_total}): {step_preview}')
            else:
                print(f'    Steps: (none detected — no Step N pattern)')
            print(f'    SVG: {svg_path.relative_to(REPO)}')

        if not dry_run:
            svg_content = make_procedure_svg(heading, product_label, steps, n_total)
            svg_path.write_text(svg_content, encoding='utf-8')

        injections.append((heading, svg_fname))
        count += 1

    if not dry_run:
        # Modify the page: remove ASCII block + inject SVG refs
        new_text = _ASCII_RE.sub('', text)
        # Track occurrence index per heading for duplicate-safe injection
        heading_seen: dict = {}
        for heading, svg_fname in injections:
            idx = heading_seen.get(heading, 0)
            heading_seen[heading] = idx + 1
            pat = re.compile(r'(^### ' + re.escape(heading) + r'[ \t]*\n)', re.MULTILINE)
            img_ref = f'![{heading}]({rel_assets}{svg_fname})'
            # Find the (idx+1)-th occurrence and inject only there
            matches = list(pat.finditer(new_text))
            if idx < len(matches):
                m = matches[idx]
                # Only inject if not already present
                after = new_text[m.end():m.end() + 60]
                if not re.match(r'\n?!\[', after):
                    insert = m.end()
                    new_text = new_text[:insert] + '\n' + img_ref + '\n' + new_text[insert:]
        page.write_text(new_text, encoding='utf-8')
        print(f'  Updated {page.relative_to(REPO)}: removed ASCII, injected {count} SVG refs')
    else:
        if verbose:
            print(f'\n  Summary: would generate {count} SVGs, remove ASCII block, inject {count} refs')

    return count


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--dry-run', action='store_true',
                        help='Print what would be done without writing files')
    parser.add_argument('--product', nargs='+', metavar='SLUG',
                        help='One or more product slugs to process (see PRODUCTS dict)')
    parser.add_argument('--all', action='store_true',
                        help='Process all registered products')
    parser.add_argument('--list', action='store_true',
                        help='List registered product slugs and exit')
    args = parser.parse_args()

    if args.list:
        for slug, path in sorted(PRODUCTS.items()):
            exists = '✓' if (DOCS / path).exists() else '✗'
            print(f'  {exists} {slug:40s} {path}')
        return

    if args.all:
        targets = list(PRODUCTS.items())
    elif args.product:
        missing = [p for p in args.product if p not in PRODUCTS]
        if missing:
            print(f'Unknown product(s): {", ".join(missing)}')
            print(f'Run with --list to see available slugs.')
            sys.exit(1)
        targets = [(p, PRODUCTS[p]) for p in args.product]
    else:
        parser.print_help()
        sys.exit(0)

    total = 0
    for slug, rel_path in targets:
        total += process_product(slug, rel_path, dry_run=args.dry_run)

    print(f'\nTotal SVGs {"(dry run)" if args.dry_run else "generated"}: {total}')


if __name__ == '__main__':
    main()
