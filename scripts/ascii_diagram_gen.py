#!/usr/bin/env python3
"""
ASCII box-drawing diagram generator for KB markdown files.

Every diagram is built from a shared position dict (col → char) then rendered
with row().  Because positions are set by index, all │ symbols land at the
exact same column on every line — guaranteed straight verticals.

HOW TO DEFINE A NEW DIAGRAM
────────────────────────────
1. Choose W (inner width, between outer walls).  Outer string width = W + 2.
2. Use layout() to calculate (L, R) column spans for each box.
3. Build each line by merging position dicts from the helpers below.
4. Wrap the list in a ``` code block in the markdown file.

POSITION CALCULATION
─────────────────────
Key formula:  L  R  inner_width  total_width
              L  R  R - L - 1    R - L + 1

Given margin m, gap g between boxes, and a list of desired inner widths:
  L[0]   = m
  R[0]   = L[0] + inner[0] + 1
  L[n+1] = R[n] + g + 1          ← gap chars, then next left wall
  R[n+1] = L[n+1] + inner[n+1] + 1

Worked example (VMware, W=85, m=3, g=2):
  VC  inner=13 → L=3,  R=17   (17-3-1=13 ✓)
  VX  inner=13 → L=20, R=34   (34-20-1=13 ✓, 20=17+2+1 ✓)
  AR  inner=42 → L=37, R=80   (80-37-1=42 ✓, 37=34+2+1 ✓)
  Divider inside AR at col 51: sec1_w=51-37-1=13, sec2 starts at 52
  Divider at col 64:           sec2_w=64-51-1=12, sec3_w=80-64-1=15

Use layout() below to print positions for a new diagram without manual arithmetic.

POSITION DICT CONVENTIONS
──────────────────────────
All column indices are 0-based within the W-wide inner space.
The outer │ walls (at string positions 0 and W+1) are added by row().
Do NOT set index 0 or W-1 unless you want to override the inner content
right next to the outer wall.

HELPER REFERENCE
────────────────
  layout(inner_widths, margin, gap)
                      — print (L, R) positions for a row of boxes; use this first
  row(d)              — render one line; outer │ walls added automatically
  bTop(l, r, tees)    — ┌────┐ with optional ┬ at tees
  bMid(l, r, text)    — │ text │ (text centred, truncated to fit)
  bBot(l, r, tees)    — └────┘ with optional ┴ at tees
  sections(l,r,divs,texts)
                      — │ sec1 │ sec2 │ sec3 │ across one box with dividers
  connector(cols)     — a row of │ stems (use with ┬ tees on the next bTop)
  arrow(cols)         — a row of ▼ arrows (use with plain bTop, no tees)
  title_border(w, title, top)
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

def arrow(cols):
    """A row of ▼ arrows pointing down, alternative to connector() + ┬ tees."""
    return {c: '▼' for c in cols}

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

def layout(inner_widths, margin=3, gap=2):
    """
    Calculate and print (L, R) positions for a row of boxes.

    inner_widths — list of desired inner widths per box (chars between the │ walls)
    margin       — left offset before the first box (default 3)
    gap          — spaces between adjacent box right wall and next box left wall (default 2)

    Returns list of (L, R) tuples.

    Example:
      layout([13, 13, 42], margin=3, gap=2)
      →  Box 1: L=3,  R=17   inner=13
         Box 2: L=20, R=34   inner=13
         Box 3: L=37, R=80   inner=42
    """
    positions = []
    l = margin
    for iw in inner_widths:
        r = l + iw + 1
        positions.append((l, r))
        l = r + gap + 1
    for i, (l, r) in enumerate(positions):
        print(f'  Box {i + 1}: L={l:3d}, R={r:3d}   inner={r - l - 1}   total={r - l + 1}')
    return positions


# ── Worked example: VMware Platform Landscape ────────────────────────────────
# Run this file directly to regenerate the diagram.
#
# Column layout (all 0-indexed in W=85 inner space):
#   VC  : 3–17   VX: 20–34   AR: 37–80  (AR divs at 51, 64)
#   VS  : 3–80   (vSphere cluster outer box)
#   ESXi: (6,19) (22,35) (38,51) (54,67)
#   VM  : eL+3 .. eL+9  inside each ESXi (┴ tees at both ends)
#   COMP: (3,17) (20,34) (37,51) (54,80)  ← COMP[3] and VF extend to VS_R so right edges align
#   TZ  : 3–34   VF: 38–80

def vmware_platform_landscape():
    VC_L, VC_R   = 3, 17
    VX_L, VX_R   = 20, 34
    AR_L, AR_R   = 37, 80
    AR_D1, AR_D2 = 51, 64

    VS_L, VS_R   = 3, 80

    ESXI     = [(6, 19), (22, 35), (38, 51), (54, 67)]
    VM_BOXES = [(eL + 3, eL + 9) for (eL, eR) in ESXI]

    COMP = [(3, 17), (20, 34), (37, 51), (54, 80)]  # COMP[3] extends to VS_R
    TZ_L, TZ_R = 3, 34
    VF_L, VF_R = 38, 80  # extends to VS_R so right edge aligns throughout

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

    # ▼ arrows from vCenter/VxRail down to vSphere
    lines.append(row(arrow([VC_MID, VX_MID])))

    # vSphere cluster box (plain top — arrows are on row above, no ┬ tees needed)
    lines.append(row(bTop(VS_L, VS_R)))
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

    # ▼ arrows from vSphere down to component boxes
    COMP_MIDS = [(cL + cR) // 2 for (cL, cR) in COMP]
    lines.append(row(arrow(COMP_MIDS)))

    # Component boxes (plain tops — arrows are on row above)
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


def vmware_platform_landscape_v2():
    """
    Full VMware Platform Landscape (W=103) — comprehensive learning diagram:
    - VC inner=20: adds SSO · Roles · LDAP and vLCM · Licensing rows
    - VX inner=20: Turnkey HCI / Dell + VMware detail
    - Aria 3×15 sections; last row "↓ monitors & manages all layers below"
    - Arrow row shows VC/VX controlling vSphere AND Aria reaching all layers
    - vSphere: adds Cluster features (HA · DRS · vMotion · FT) header row
    - Integrated tier: vSAN(3-48) + NSX(51-99) — "part of vSphere, not appliances"
    - Add-on tier: Horizon(3-33) + SRM(36-66) + vSphere Replication(69-99)
    - VCF outer box(3-99): SDDC Manager(6-50) + Tanzu(53-97) nested inside
    - Expanded glossary: VM, ESXi, HA, DRS, vMotion, SSO, vLCM, VDI, SRM, vSR, HCI, SDDC
    """
    W2 = 103

    def R(positions):
        r = [' '] * W2
        for col, ch in positions.items():
            if 0 <= col < W2:
                r[col] = ch
        return '│' + ''.join(r) + '│'

    def txt_row(text='', indent=2):
        r = [' '] * W2
        for i, c in enumerate(text):
            pos = indent + i
            if 0 <= pos < W2:
                r[pos] = c
        return '│' + ''.join(r) + '│'

    def T(l, r, tees=()):
        d = {}
        for i in range(l, r + 1): d[i] = '─'
        d[l] = '┌'; d[r] = '┐'
        for t in tees: d[t] = '┬'
        return d

    def M(l, r, text=''):
        iw = r - l - 1
        txt = text.center(iw)[:iw]
        d = {l: '│', r: '│'}
        for i, c in enumerate(txt): d[l + 1 + i] = c
        return d

    def B(l, r, tees=()):
        d = {}
        for i in range(l, r + 1): d[i] = '─'
        d[l] = '└'; d[r] = '┘'
        for t in tees: d[t] = '┴'
        return d

    def S(l, r, divs, texts):
        bounds = [l] + list(divs) + [r]
        d = {}
        for p in bounds: d[p] = '│'
        for i, text in enumerate(texts):
            sl = bounds[i]; sr = bounds[i + 1]
            iw = sr - sl - 1
            txt = text.center(iw)[:iw]
            for j, c in enumerate(txt): d[sl + 1 + j] = c
        return d

    def G(*dicts):
        out = {}
        for d in dicts: out.update(d)
        return out

    # ── Layout ───────────────────────────────────────────────────────────────────
    VC_L, VC_R   =  3, 24   # inner=20
    VX_L, VX_R   = 27, 48   # inner=20
    AR_L, AR_R   = 51, 99   # inner=47; 3 equal sections of 15
    AR_D1, AR_D2 = 67, 83

    VS_L, VS_R   =  3, 99
    ESXI     = [(6, 19), (22, 35), (38, 51), (54, 67)]
    VM_BOXES = [(eL + 3, eL + 9) for (eL, eR) in ESXI]
    FB_L, FB_R   = 70, 97   # fact box inside vSphere, inner=26

    VSAN_L, VSAN_R =  3, 48   # integrated tier: inner=44
    NSX_L,  NSX_R  = 51, 99   # integrated tier: inner=47

    HZ_L,  HZ_R   =  3, 33   # add-on tier: inner=29
    SRM_L, SRM_R  = 36, 66   # add-on tier: inner=29
    REP_L, REP_R  = 69, 99   # add-on tier: inner=29

    VCF_L, VCF_R   =  3, 99  # VCF outer box: inner=95
    SDDC_L, SDDC_R =  6, 50  # SDDC Manager inside VCF: inner=43
    TZ_L,   TZ_R   = 53, 97  # Tanzu inside VCF: inner=43

    VC_MID = (VC_L + VC_R) // 2   # 13
    VX_MID = (VX_L + VX_R) // 2   # 37
    AR_MID = (AR_L + AR_R) // 2   # 75

    lines = []

    # ── Title ────────────────────────────────────────────────────────────────────
    lines.append(title_border(W2, 'VMware Platform Landscape'))
    lines.append(txt_row())

    # ── Management tier ──────────────────────────────────────────────────────────
    # 5 content rows: VC adds SSO + vLCM; Aria adds "↓ monitors all layers" row
    lines.append(R(G(T(VC_L, VC_R), T(VX_L, VX_R), T(AR_L, AR_R))))
    lines.append(R(G(
        M(VC_L, VC_R, 'vCenter'),
        M(VX_L, VX_R, 'VxRail'),
        M(AR_L, AR_R, 'Aria Suite'),
    )))
    lines.append(R(G(
        M(VC_L, VC_R, '(Manage)'),
        M(VX_L, VX_R, '(Appliance)'),
        S(AR_L, AR_R, [AR_D1, AR_D2], ['Ops/Logs', 'Automation', 'Suite Lifecycle']),
    )))
    lines.append(R(G(
        M(VC_L, VC_R, 'Web UI & API'),
        M(VX_L, VX_R, 'Turnkey HCI'),
        S(AR_L, AR_R, [AR_D1, AR_D2], ['Monitor/Alert', 'IaC / Deploy', 'Patch/Upgrade']),
    )))
    lines.append(R(G(
        M(VC_L, VC_R, 'SSO · Roles · LDAP'),
        M(VX_L, VX_R, 'Dell + VMware'),
        S(AR_L, AR_R, [AR_D1, AR_D2], ['Operations', 'Blueprints', 'Certificates']),
    )))
    lines.append(R(G(
        M(VC_L, VC_R, 'vLCM · Licensing'),
        M(VX_L, VX_R, 'All-in-one HCI'),
        M(AR_L, AR_R, '↓ monitors & manages all layers below'),
    )))
    lines.append(R(G(
        B(VC_L, VC_R),
        B(VX_L, VX_R),
        B(AR_L, AR_R, tees=[AR_D1, AR_D2]),
    )))

    # ── Arrow row: VC/VX control vSphere; Aria reaches all tiers ─────────────────
    lines.append(txt_row())
    d = {VC_MID: '▼', VX_MID: '▼', AR_MID: '▼'}
    note = '← Aria monitors all layers'
    for i, c in enumerate(note):
        pos = AR_MID + 2 + i
        if pos < W2: d[pos] = c
    lines.append(R(d))
    lines.append(txt_row('             vCenter/VxRail: control plane for vSphere', indent=0))
    lines.append(txt_row())

    # ── vSphere cluster ───────────────────────────────────────────────────────────
    lines.append(R(T(VS_L, VS_R)))
    lines.append(R(M(VS_L, VS_R, 'vSphere Cluster (ESXi Hosts)')))
    lines.append(R(M(VS_L, VS_R, 'Type-1 hypervisor: runs directly on hardware — no host OS required')))
    lines.append(R(M(VS_L, VS_R, 'Cluster features: HA · DRS · vMotion · Fault Tolerance')))
    lines.append(R({VS_L: '│', VS_R: '│'}))

    # ESXi tops + fact box top
    d = {VS_L: '│', VS_R: '│'}
    for (eL, eR) in ESXI: d.update(T(eL, eR))
    d.update(T(FB_L, FB_R))
    lines.append(R(d))

    # ESXi labels + fact row 1
    d = {VS_L: '│', VS_R: '│'}
    for (eL, eR), lbl in zip(ESXI, ['ESXi-01', 'ESXi-02', 'ESXi-03', 'ESXi-04']):
        d.update(M(eL, eR, lbl))
    d.update(M(FB_L, FB_R, 'Each host: 50-200+ VMs'))
    lines.append(R(d))

    # (Hypervisor) + fact row 2
    d = {VS_L: '│', VS_R: '│'}
    for (eL, eR) in ESXI:
        d[eL] = '│'; d[eR] = '│'
        d.update(M(eL, eR, '(Hypervisor)'))
    d.update(M(FB_L, FB_R, 'Types: web, DB, app, AD'))
    lines.append(R(d))

    # VM tops + fact row 3
    d = {VS_L: '│', VS_R: '│'}
    for (eL, eR), (vmL, vmR) in zip(ESXI, VM_BOXES):
        d[eL] = '│'; d[eR] = '│'
        d.update(T(vmL, vmR))
    d.update(M(FB_L, FB_R, 'vMotion: live migration'))
    lines.append(R(d))

    # VM labels + fact row 4
    d = {VS_L: '│', VS_R: '│'}
    for (eL, eR), (vmL, vmR) in zip(ESXI, VM_BOXES):
        d[eL] = '│'; d[eR] = '│'
        d.update(M(vmL, vmR, 'VMs'))
    d.update(M(FB_L, FB_R, 'HA: restart on failure'))
    lines.append(R(d))

    # ESXi bottoms (VM → ┴ tees) + fact box bottom
    d = {VS_L: '│', VS_R: '│'}
    for (eL, eR), (vmL, vmR) in zip(ESXI, VM_BOXES):
        dd = B(eL, eR); dd[vmL] = '┴'; dd[vmR] = '┴'
        d.update(dd)
    d.update(B(FB_L, FB_R))
    lines.append(R(d))

    lines.append(R({VS_L: '│', VS_R: '│'}))
    lines.append(R(B(VS_L, VS_R)))
    lines.append(txt_row())

    # ── Integrated tier ───────────────────────────────────────────────────────────
    lines.append(txt_row('  Integrated into vSphere — part of the hypervisor, not separate appliances:'))
    lines.append(txt_row())
    d = {(VSAN_L + VSAN_R) // 2: '▼', (NSX_L + NSX_R) // 2: '▼'}
    lines.append(R(d))
    lines.append(txt_row())

    lines.append(R(G(T(VSAN_L, VSAN_R), T(NSX_L, NSX_R))))
    lines.append(R(G(
        M(VSAN_L, VSAN_R, 'vSAN (Software-Defined Storage)'),
        M(NSX_L,  NSX_R,  'NSX (Software-Defined Networking)'),
    )))
    lines.append(R(G(
        M(VSAN_L, VSAN_R, 'Pooled from ESXi local disks'),
        M(NSX_L,  NSX_R,  'Virtual switches + distributed firewall'),
    )))
    lines.append(R(G(
        M(VSAN_L, VSAN_R, 'Policy-based; no external array'),
        M(NSX_L,  NSX_R,  'Micro-segmentation & east-west routing'),
    )))
    lines.append(R(G(B(VSAN_L, VSAN_R), B(NSX_L, NSX_R))))
    lines.append(txt_row())

    # ── Add-on products tier ──────────────────────────────────────────────────────
    lines.append(txt_row('  Add-on products — licensed separately, deployed on top of vSphere:'))
    lines.append(txt_row())
    d = {(HZ_L + HZ_R) // 2: '▼', (SRM_L + SRM_R) // 2: '▼', (REP_L + REP_R) // 2: '▼'}
    lines.append(R(d))
    lines.append(txt_row())

    lines.append(R(G(T(HZ_L, HZ_R), T(SRM_L, SRM_R), T(REP_L, REP_R))))
    lines.append(R(G(
        M(HZ_L,  HZ_R,  'Horizon (VDI)'),
        M(SRM_L, SRM_R, 'Site Recovery Manager'),
        M(REP_L, REP_R, 'vSphere Replication'),
    )))
    lines.append(R(G(
        M(HZ_L,  HZ_R,  '(Desktops)'),
        M(SRM_L, SRM_R, '(DR Orchestration)'),
        M(REP_L, REP_R, '(VM Replication)'),
    )))
    lines.append(R(G(
        M(HZ_L,  HZ_R,  'VDI + app publishing'),
        M(SRM_L, SRM_R, 'Failover + Failback'),
        M(REP_L, REP_R, 'RPO-based replication'),
    )))
    lines.append(R(G(B(HZ_L, HZ_R), B(SRM_L, SRM_R), B(REP_L, REP_R))))
    lines.append(txt_row())

    # ── VCF outer box with SDDC Manager + Tanzu nested inside ────────────────────
    lines.append(R(T(VCF_L, VCF_R)))
    lines.append(R(M(VCF_L, VCF_R, 'VMware Cloud Foundation (VCF/SDDC)')))
    lines.append(R(M(VCF_L, VCF_R, 'Packages & delivers the full SDDC: vSphere + vSAN + NSX + Lifecycle')))
    lines.append(R({VCF_L: '│', VCF_R: '│'}))

    lines.append(R(G({VCF_L: '│', VCF_R: '│'}, T(SDDC_L, SDDC_R), T(TZ_L, TZ_R))))
    lines.append(R(G(
        {VCF_L: '│', VCF_R: '│'},
        M(SDDC_L, SDDC_R, 'SDDC Manager'),
        M(TZ_L,   TZ_R,   'Tanzu (Kubernetes Platform)'),
    )))
    lines.append(R(G(
        {VCF_L: '│', VCF_R: '│'},
        M(SDDC_L, SDDC_R, 'Lifecycle orchestrator for VCF'),
        M(TZ_L,   TZ_R,   'Container Orchestration'),
    )))
    lines.append(R(G(
        {VCF_L: '│', VCF_R: '│'},
        M(SDDC_L, SDDC_R, 'Bringup · Upgrades · Compliance'),
        M(TZ_L,   TZ_R,   'Workload domain within VCF'),
    )))
    lines.append(R(G({VCF_L: '│', VCF_R: '│'}, B(SDDC_L, SDDC_R), B(TZ_L, TZ_R))))
    lines.append(R({VCF_L: '│', VCF_R: '│'}))
    lines.append(R(B(VCF_L, VCF_R)))
    lines.append(txt_row())

    # ── Physical infrastructure ───────────────────────────────────────────────────
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('CPU cores · RAM (GBs to TBs per host) · NIC (10/25/100 GbE) · NVMe/SSD/HDD · Power & Cooling'))
    lines.append(txt_row())

    # ── Glossary ──────────────────────────────────────────────────────────────────
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VM      = a software-emulated computer; runs a full OS + apps inside a physical host'))
    lines.append(txt_row('ESXi    = Type-1 hypervisor; installed directly on bare metal — no host OS needed'))
    lines.append(txt_row('vSAN    = pools local server disks into shared storage — no separate SAN array needed'))
    lines.append(txt_row('NSX     = software-defined networking; virtual switches, routers & distributed firewall'))
    lines.append(txt_row('HA      = High Availability; vSphere auto-restarts VMs on another host if one fails'))
    lines.append(txt_row('DRS     = Distributed Resource Scheduler; auto-balances VM workload across ESXi hosts'))
    lines.append(txt_row('vMotion = live migration of a running VM between ESXi hosts with zero downtime'))
    lines.append(txt_row('SSO     = Single Sign-On; central identity used by all vCenter/vSphere authentication'))
    lines.append(txt_row('vLCM    = vSphere Lifecycle Manager; patches ESXi hosts and manages firmware baselines'))
    lines.append(txt_row('VDI     = your desktop OS runs in the data centre; you stream it to any device remotely'))
    lines.append(txt_row('SRM     = Site Recovery Manager; orchestrates DR failover using pre-defined recovery plans'))
    lines.append(txt_row('vSR     = vSphere Replication; replicates VMs to a remote site; provides recovery point for SRM'))
    lines.append(txt_row('HCI     = Hyper-Converged Infrastructure; compute + storage + networking in one appliance'))
    lines.append(txt_row('SDDC Mgr= VCF lifecycle orchestrator; automates bringup, upgrades & compliance checks'))
    lines.append(txt_row())

    # Bottom border
    lines.append('└' + '─' * W2 + '┘')

    return lines


if __name__ == '__main__':
    import sys
    diagram = vmware_platform_landscape_v2()
    for line in diagram:
        print(line)
    widths = set(len(l) for l in diagram)
    print(f'\n[width={widths}  lines={len(diagram)}]', file=sys.stderr)
