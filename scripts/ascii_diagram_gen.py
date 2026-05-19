#!/usr/bin/env python3
"""
ASCII box-drawing diagram generator for KB markdown files.

Every diagram is built from a shared position dict (col → char) then rendered
with row().  Because positions are set by index, all │ symbols land at the
exact same column on every line — guaranteed straight verticals.

HOW TO DEFINE A NEW DIAGRAM
────────────────────────────
1. Choose W (inner width, between outer walls).  Outer string width = W + 2.
2. Decide the column spans for each box: (L, R) in 0-indexed inner space.
   Rule of thumb for a 3-box row with equal widths and 2-space gaps:
     gap=2, box_w=(W - 2*gap) // 3
     B1: (0, box_w-1), B2: (box_w+gap, 2*box_w+gap-1), B3: (2*(box_w+gap), W-1)
3. Build each line by merging position dicts from the helpers below.
4. Wrap the list in a ``` code block in the markdown file.

POSITION DICT CONVENTIONS
──────────────────────────
All column indices are 0-based within the W-wide inner space.
The outer │ walls (at string positions 0 and W+1) are added by row().
Do NOT set index 0 or W-1 unless you want to override the inner content
right next to the outer wall.

HELPER REFERENCE
────────────────
  row(d)              — render one line; outer │ walls added automatically
  bTop(l, r, tees)    — ┌────┐ with optional ┬ at tees
  bMid(l, r, text)    — │ text │ (text centred, truncated to fit)
  bBot(l, r, tees)    — └────┘ with optional ┴ at tees
  sections(l,r,divs,texts)
                      — │ sec1 │ sec2 │ sec3 │ across one box with dividers
  connector(cols)     — a row of │ stems at given column positions
  title_border(W, title, corner='┌')
                      — ┌──── Title ────┐ outer border line
  merge(*dicts)       — combine position dicts (last write wins)
"""

W = 85  # default inner width; override per diagram

# ── Core primitives ──────────────────────────────────────────────────────────

def row(positions, w=None):
    """Render one diagram line. positions: {col: char} (0-indexed in inner space)."""
    if w is None:
        w = W
    r = [' '] * w
    for col, ch in positions.items():
        r[col] = ch
    return '│' + ''.join(r) + '│'

def _hspan(d, l, r, fill='─', lc=None, rc=None):
    for i in range(l, r + 1):
        d[i] = fill
    if lc:
        d[l] = lc
    if rc:
        d[r] = rc

def bTop(l, r, tees=()):
    """Top border of a box. tees: column positions to replace ─ with ┬."""
    d = {}
    _hspan(d, l, r, '─', '┌', '┐')
    for t in tees:
        d[t] = '┬'
    return d

def bMid(l, r, text=''):
    """One content row of a box. text is centred and truncated to inner width."""
    iw = r - l - 1
    txt = text.center(iw)[:iw]
    d = {l: '│', r: '│'}
    for i, c in enumerate(txt):
        d[l + 1 + i] = c
    return d

def bBot(l, r, tees=()):
    """Bottom border of a box. tees: column positions to replace ─ with ┴."""
    d = {}
    _hspan(d, l, r, '─', '└', '┘')
    for t in tees:
        d[t] = '┴'
    return d

def sections(l, r, divs, texts):
    """
    A single content row spanning box (l..r) split by dividers.

    divs  — list of column positions for internal │ dividers (must be sorted)
    texts — list of strings, one per section (len == len(divs) + 1)

    Example: sections(37, 80, [51, 64], ['Ops/Logs', 'Automation', 'Suite Lifecycle'])
    """
    boundaries = [l] + list(divs) + [r]
    d = {}
    for pos in boundaries:
        d[pos] = '│'
    for i, text in enumerate(texts):
        sl = boundaries[i]
        sr = boundaries[i + 1]
        iw = sr - sl - 1
        txt = text.center(iw)[:iw]
        for j, c in enumerate(txt):
            d[sl + 1 + j] = c
    return d

def connector(cols):
    """A row of vertical │ stems, e.g. between a box bottom and the next box top."""
    return {c: '│' for c in cols}

def title_border(w, title, top=True):
    """
    Outer border line with an embedded title, e.g.:
      ┌───────────── My Title ─────────────┐
    w     — inner width (same W used in row())
    title — string to embed (centred with ─ padding)
    top   — True for ┌/┐, False for └/┘
    """
    lc, rc = ('┌', '┐') if top else ('└', '┘')
    if title:
        padded = f' {title} '
        total = w
        left_dashes = (total - len(padded)) // 2
        right_dashes = total - len(padded) - left_dashes
        inner = '─' * left_dashes + padded + '─' * right_dashes
    else:
        inner = '─' * w
    return lc + inner + rc

def merge(*dicts):
    """Merge position dicts left to right (later dicts override earlier)."""
    out = {}
    for d in dicts:
        out.update(d)
    return out


# ── Worked example: VMware Platform Landscape ────────────────────────────────
# Run this file directly to regenerate the diagram.
#
# Column layout (all 0-indexed in W=85 inner space):
#   VC  : 3–17   VX: 20–34   AR: 37–80  (AR divs at 51, 64)
#   VS  : 3–80   (vSphere cluster outer box)
#   ESXi: (6,19) (22,35) (38,51) (54,67)
#   VM  : eL+3 .. eL+9  inside each ESXi (┴ tees at both ends)
#   COMP: (3,17) (20,34) (37,51) (54,68)
#   TZ  : 3–34   VF: 38–79

def vmware_platform_landscape():
    VC_L, VC_R   = 3, 17
    VX_L, VX_R   = 20, 34
    AR_L, AR_R   = 37, 80
    AR_D1, AR_D2 = 51, 64

    VS_L, VS_R   = 3, 80

    ESXI     = [(6, 19), (22, 35), (38, 51), (54, 67)]
    VM_BOXES = [(eL + 3, eL + 9) for (eL, eR) in ESXI]

    COMP = [(3, 17), (20, 34), (37, 51), (54, 68)]
    TZ_L, TZ_R = 3, 34
    VF_L, VF_R = 38, 79

    VC_MID = (VC_L + VC_R) // 2   # 10
    VX_MID = (VX_L + VX_R) // 2   # 27

    lines = []

    # Outer top border (plain — no title text)
    lines.append('┌' + '─' * 85 + '┐')

    # Top boxes — top borders
    lines.append(row(merge(bTop(VC_L, VC_R), bTop(VX_L, VX_R), bTop(AR_L, AR_R))))

    # Top boxes — main labels
    lines.append(row(merge(
        bMid(VC_L, VC_R, 'vCenter'),
        bMid(VX_L, VX_R, 'VxRail'),
        bMid(AR_L, AR_R, 'Aria Suite'),
    )))

    # Top boxes — sub-labels; Aria split into 3 sections
    lines.append(row(merge(
        bMid(VC_L, VC_R, '(Manage)'),
        bMid(VX_L, VX_R, '(Appliance)'),
        sections(AR_L, AR_R, [AR_D1, AR_D2], ['Ops/Logs', 'Automation', 'Suite Lifecycle']),
    )))
    lines.append(row(merge(
        bMid(VC_L, VC_R, ''),
        bMid(VX_L, VX_R, ''),
        sections(AR_L, AR_R, [AR_D1, AR_D2], ['Operations', '', '']),
    )))

    # Top boxes — bottom borders (Aria has ┴ at dividers)
    lines.append(row(merge(
        bBot(VC_L, VC_R),
        bBot(VX_L, VX_R),
        bBot(AR_L, AR_R, tees=[AR_D1, AR_D2]),
    )))

    # Connector stems → vSphere
    lines.append(row(connector([VC_MID, VX_MID])))

    # vSphere cluster box
    lines.append(row(bTop(VS_L, VS_R, tees=[VC_MID, VX_MID])))
    lines.append(row(bMid(VS_L, VS_R, 'vSphere Cluster (ESXi Hosts)')))

    # ESXi top borders (vSphere side walls must be present on every inner row)
    d = {VS_L: '│', VS_R: '│'}
    for (eL, eR) in ESXI:
        d.update(bTop(eL, eR))
    lines.append(row(d))

    # ESXi label row
    d = {VS_L: '│', VS_R: '│'}
    for (eL, eR), lbl in zip(ESXI, ['ESXi-01', 'ESXi-02', 'ESXi-03', 'ESXi-04']):
        d.update(bMid(eL, eR, lbl))
    lines.append(row(d))

    # VM box tops inside each ESXi
    d = {VS_L: '│', VS_R: '│'}
    for (eL, eR), (vmL, vmR) in zip(ESXI, VM_BOXES):
        d[eL] = '│'; d[eR] = '│'
        d.update(bTop(vmL, vmR))
    lines.append(row(d))

    # VM labels
    d = {VS_L: '│', VS_R: '│'}
    for (eL, eR), (vmL, vmR) in zip(ESXI, VM_BOXES):
        d[eL] = '│'; d[eR] = '│'
        d.update(bMid(vmL, vmR, 'VMs'))
    lines.append(row(d))

    # ESXi bottom borders — VM walls become ┴ tees (not ┘) so the bottom reads └──┴─────┴───┘
    d = {VS_L: '│', VS_R: '│'}
    for (eL, eR), (vmL, vmR) in zip(ESXI, VM_BOXES):
        dd = bBot(eL, eR)
        dd[vmL] = '┴'
        dd[vmR] = '┴'
        d.update(dd)
    lines.append(row(d))

    # vSphere cluster bottom border
    lines.append(row(bBot(VS_L, VS_R)))

    # Connector stems → component boxes
    COMP_MIDS = [(cL + cR) // 2 for (cL, cR) in COMP]
    lines.append(row(connector(COMP_MIDS)))

    # Component boxes
    lines.append(row(merge(*[bTop(cL, cR) for cL, cR in COMP])))
    lines.append(row(merge(*[bMid(cL, cR, lbl) for (cL, cR), lbl in zip(COMP, [
        'vSAN', 'NSX', 'Horizon', 'Site Recovery',
    ])])))
    lines.append(row(merge(*[bMid(cL, cR, lbl) for (cL, cR), lbl in zip(COMP, [
        '(Storage)', '(Networking)', '(Desktops)', '(DR Platform)',
    ])])))
    lines.append(row(merge(*[bBot(cL, cR) for cL, cR in COMP])))

    # Blank row
    lines.append(row({}))

    # Tanzu and VCF
    lines.append(row(merge(bTop(TZ_L, TZ_R), bTop(VF_L, VF_R))))
    lines.append(row(merge(
        bMid(TZ_L, TZ_R, 'Tanzu (Kubernetes Platform)'),
        bMid(VF_L, VF_R, 'VMware Cloud Foundation (VCF/SDDC)'),
    )))
    lines.append(row(merge(bBot(TZ_L, TZ_R), bBot(VF_L, VF_R))))

    # Outer bottom border
    lines.append('└' + '─' * 85 + '┘')

    return lines


if __name__ == '__main__':
    import sys
    diagram = vmware_platform_landscape()
    for line in diagram:
        print(line)
    widths = set(len(l) for l in diagram)
    print(f'\n[width={widths}  lines={len(diagram)}]', file=sys.stderr)
