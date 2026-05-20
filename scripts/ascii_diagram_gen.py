#!/usr/bin/env python3
"""
ASCII box-drawing diagram generator for KB markdown files.

Every diagram is built from a shared position dict (col → char) then rendered
with row().  Because positions are set by index, all │ symbols land at the
exact same column on every line — guaranteed straight verticals.

HOW TO ADD A NEW DIAGRAM
─────────────────────────
1. Write a function that returns list[str] — one string per output line.
   Use the vmware_platform_landscape() function below as the template.
   Two lines of setup at the top, then use the module-level helpers directly:

       @kb_diagram('my-key', 'docs/section/index.md', 'Short description')
       def my_diagram():
           W2 = 103
           R, txt_row = make_helpers(W2)
           # layout constants …
           lines = []
           lines.append(title_border(W2, 'My Title'))
           lines.append(txt_row())
           lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
           lines.append(R(merge(bMid(L1, R1, 'Label'), bMid(L2, R2, 'Label'))))
           lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
           lines.append('└' + '─' * W2 + '┘')
           return lines

   Arrow sections between tiers always follow this four-line pattern:
       lines.append(txt_row('  <explanation of what the arrows mean>'))
       lines.append(txt_row())
       lines.append(R(arrow([MID1, MID2, ...])))
       lines.append(txt_row())
   Never put annotations inline on the arrow line — put them in the label above.

2. The @kb_diagram decorator auto-registers the function — no separate DIAGRAMS entry.
3. Run:  python3 scripts/ascii_diagram_gen.py my-key --write

USAGE
─────
  python3 scripts/ascii_diagram_gen.py                         # list all diagrams
  python3 scripts/ascii_diagram_gen.py vmware                  # print to stdout
  python3 scripts/ascii_diagram_gen.py vmware --write          # update markdown file
  python3 scripts/ascii_diagram_gen.py --write-all             # update all files
  python3 scripts/ascii_diagram_gen.py --check                 # verify files are in sync
  python3 scripts/ascii_diagram_gen.py --layout 20 20 47       # calculate box positions
  python3 scripts/ascii_diagram_gen.py --layout 20 20 47 --margin 3 --gap 2

POSITION CALCULATION
─────────────────────
Key formula:  L  R  inner_width  total_width
              L  R  R - L - 1    R - L + 1

Given margin m, gap g between boxes, and a list of desired inner widths:
  L[0]   = m
  R[0]   = L[0] + inner[0] + 1
  L[n+1] = R[n] + g + 1          ← gap chars, then next left wall
  R[n+1] = L[n+1] + inner[n+1] + 1

Use layout() to print positions without manual arithmetic.

HELPER REFERENCE
────────────────
  make_helpers(w)               — returns (R, txt_row) bound to inner width w
  layout(inner_widths, m, gap)  — print (L, R) positions for a box row
  row(d, w)                     — render one line; outer │ walls added
  bTop(l, r, tees)              — ┌────┐ with optional ┴ at tees (stem up, toward incoming)
  bMid(l, r, text)              — │ text │  (text centred, truncated)
  bBot(l, r, tees)              — └────┘ with optional ┴ at tees (stem up, exit downward)
  sections(l, r, divs, texts)   — │ sec1 │ sec2 │ sec3 │ with dividers
  connector(cols)               — row of │ stems
  arrow(cols)                   — row of ▼ arrows
  title_border(w, title, top)   — ┌──── Title ────┐ outer border line
  merge(*dicts)                 — combine position dicts (last write wins)
"""

import os
import re
import sys

# ── Diagram registry ─────────────────────────────────────────────────────────
DIAGRAMS = {}  # populated at import time by @kb_diagram decorators

def kb_diagram(key, file, description):
    """Decorator that auto-registers a diagram function. Usage:

        @kb_diagram('my-key', 'docs/path/index.md', 'Short description')
        def my_diagram():
            ...
    """
    def _register(fn):
        DIAGRAMS[key] = {'fn': fn, 'file': file, 'description': description}
        return fn
    return _register

# ── Core primitives ──────────────────────────────────────────────────────────

def row(positions, w):
    """Render one diagram line. positions: {col: char} (0-indexed in inner space).
    Columns outside [0, w) are silently ignored."""
    r = [' '] * w
    for col, ch in positions.items():
        if 0 <= col < w:
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
    """Top border of a box. tees: column positions to replace ─ with ┴.
    ┴ is correct here: the horizontal bar is the top border, and the stem
    points UP toward the incoming connector above the box."""
    d = {}
    _hspan(d, l, r, '─', '┌', '┐')
    for t in tees:
        d[t] = '┴'
    return d

def bMid(l, r, text=''):
    """One content row of a box. text is centred and truncated to inner width."""
    iw = r - l - 1
    if len(text) > iw:
        print(f'  WARN bMid: truncated ({len(text)} → {iw}): {text!r}', file=sys.stderr)
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
    A single content row spanning box (l..r) split by internal dividers.

    divs  — list of column positions for internal │ dividers (must be sorted)
    texts — list of strings, one per section (len == len(divs) + 1)

    Example: sections(51, 99, [67, 83], ['Ops/Logs', 'Automation', 'Suite Lifecycle'])
    """
    boundaries = [l] + list(divs) + [r]
    d = {}
    for pos in boundaries:
        d[pos] = '│'
    for i, text in enumerate(texts):
        sl = boundaries[i]
        sr = boundaries[i + 1]
        iw = sr - sl - 1
        if len(text) > iw:
            print(f'  WARN sections[{i}]: truncated ({len(text)} → {iw}): {text!r}', file=sys.stderr)
        txt = text.center(iw)[:iw]
        for j, c in enumerate(txt):
            d[sl + 1 + j] = c
    return d

def connector(cols):
    """A row of vertical │ stems between a box bottom and the next box top."""
    return {c: '│' for c in cols}

def arrow(cols):
    """A row of ▼ arrows pointing down."""
    return {c: '▼' for c in cols}

def title_border(w, title, top=True):
    """
    Outer border line with an embedded title, e.g.:
      ┌───────────── My Title ─────────────┐
    w     — inner width (same w passed to make_helpers)
    title — string to embed (centred with ─ padding); pass '' for a plain border
    top   — True for ┌/┐, False for └/┘
    """
    lc, rc = ('┌', '┐') if top else ('└', '┘')
    if title:
        padded = f' {title} '
        if len(padded) > w:
            print(f'  WARN title_border: title too long ({len(padded)} > {w}): {title!r}', file=sys.stderr)
            padded = padded[:w]
        left_dashes = (w - len(padded)) // 2
        right_dashes = w - len(padded) - left_dashes
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

def make_helpers(w):
    """
    Return (R, txt_row) bound to inner width w.

    R(d)                      — render one diagram line (wraps row(d, w))
    txt_row(text='', indent=2) — left-aligned text line inside the outer border

    Use at the top of every diagram function, then call bTop/bMid/bBot/
    sections/merge/arrow/connector directly from module scope:

        W2 = 95
        R, txt_row = make_helpers(W2)
    """
    def R(d):
        return row(d, w)

    def txt_row(text='', indent=2):
        r = [' '] * w
        for i, c in enumerate(text):
            pos = indent + i
            if pos >= w:
                print(f'  WARN txt_row: truncated at col {w} (indent={indent}): {text!r}', file=sys.stderr)
                break
            if 0 <= pos < w:
                r[pos] = c
        return '│' + ''.join(r) + '│'

    return R, txt_row

def layout(inner_widths, margin=3, gap=2):
    """
    Print and return (L, R) positions for a row of boxes.

    inner_widths — desired inner widths per box (chars between the │ walls)
    margin       — left offset before the first box (default 3)
    gap          — spaces between adjacent box walls (default 2)

    Example:
      layout([20, 20, 47], margin=3, gap=2)
      →  Box 1: L=3,  R=24   inner=20
         Box 2: L=27, R=48   inner=20
         Box 3: L=51, R=99   inner=47
    """
    positions = []
    l = margin
    for iw in inner_widths:
        r = l + iw + 1
        positions.append((l, r))
        l = r + gap + 1
    for i, (bl, br) in enumerate(positions):
        print(f'  Box {i + 1}: L={bl:3d}, R={br:3d}   inner={br - bl - 1}   total={br - bl + 1}')
    return positions


# ── Diagrams ─────────────────────────────────────────────────────────────────
# Each function returns list[str].
# Start with:  W2 = <width>;  R, txt_row = make_helpers(W2)
# Then use bTop/bMid/bBot/sections/merge/arrow/connector from module scope.
# Register every new function in DIAGRAMS at the bottom of this file.

@kb_diagram(
    'vmware',
    'docs/virtualization/vmware/index.md',
    'VMware Platform Landscape — full stack: vSphere, vSAN, NSX, VCF, Aria',
)
def vmware_platform_landscape():
    """VMware Platform Landscape — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    # ── Layout ───────────────────────────────────────────────────────────────
    VC_L, VC_R   =  3, 24   # inner=20
    VX_L, VX_R   = 27, 48   # inner=20
    AR_L, AR_R   = 51, 99   # inner=47; 3 equal sections of 15
    AR_D1, AR_D2 = 67, 83

    VS_L, VS_R   =  3, 99
    ESXI         = [(6, 19), (22, 35), (38, 51), (54, 67)]
    VM_BOXES     = [(eL + 3, eL + 9) for (eL, eR) in ESXI]
    FB_L, FB_R   = 70, 97   # fact box inside vSphere cluster, inner=26

    VSAN_L, VSAN_R =  3, 48   # integrated tier: inner=44
    NSX_L,  NSX_R  = 51, 99   # integrated tier: inner=47

    HZ_L,  HZ_R   =  3, 33   # add-on tier: inner=29
    SRM_L, SRM_R  = 36, 66   # add-on tier: inner=29
    REP_L, REP_R  = 69, 99   # add-on tier: inner=29

    VCF_L,  VCF_R  =  3, 99  # VCF outer box: inner=95
    SDDC_L, SDDC_R =  6, 50  # SDDC Manager inside VCF: inner=43
    TZ_L,   TZ_R   = 53, 97  # Tanzu inside VCF: inner=43

    VC_MID = (VC_L + VC_R) // 2   # 13
    VX_MID = (VX_L + VX_R) // 2   # 37
    AR_MID = (AR_L + AR_R) // 2   # 75

    lines = []

    # ── Title ────────────────────────────────────────────────────────────────
    lines.append(title_border(W2, 'VMware Platform Landscape'))
    lines.append(txt_row())

    # ── Management tier ──────────────────────────────────────────────────────
    lines.append(R(merge(bTop(VC_L, VC_R), bTop(VX_L, VX_R), bTop(AR_L, AR_R))))
    lines.append(R(merge(
        bMid(VC_L, VC_R, 'vCenter'),
        bMid(VX_L, VX_R, 'VxRail'),
        bMid(AR_L, AR_R, 'Aria Suite'),
    )))
    lines.append(R(merge(
        bMid(VC_L, VC_R, '(Manage)'),
        bMid(VX_L, VX_R, '(Appliance)'),
        sections(AR_L, AR_R, [AR_D1, AR_D2], ['Ops/Logs', 'Automation', 'Suite Lifecycle']),
    )))
    lines.append(R(merge(
        bMid(VC_L, VC_R, 'Web UI & API'),
        bMid(VX_L, VX_R, 'Turnkey HCI'),
        sections(AR_L, AR_R, [AR_D1, AR_D2], ['Monitor/Alert', 'IaC / Deploy', 'Patch/Upgrade']),
    )))
    lines.append(R(merge(
        bMid(VC_L, VC_R, 'SSO · Roles · LDAP'),
        bMid(VX_L, VX_R, 'Dell + VMware'),
        sections(AR_L, AR_R, [AR_D1, AR_D2], ['Operations', 'Blueprints', 'Certificates']),
    )))
    lines.append(R(merge(
        bMid(VC_L, VC_R, 'vLCM · Licensing'),
        bMid(VX_L, VX_R, 'All-in-one HCI'),
        bMid(AR_L, AR_R, '↓ monitors & manages all layers below'),
    )))
    lines.append(R(merge(
        bBot(VC_L, VC_R),
        bBot(VX_L, VX_R),
        bBot(AR_L, AR_R, tees=[AR_D1, AR_D2]),
    )))

    # ── Arrow row ────────────────────────────────────────────────────────────
    lines.append(txt_row())
    lines.append(txt_row('  vCenter/VxRail: control plane for vSphere  ·  Aria Suite: monitors all layers'))
    lines.append(txt_row())
    lines.append(R(arrow([VC_MID, VX_MID, AR_MID])))
    lines.append(txt_row())

    # ── vSphere cluster ───────────────────────────────────────────────────────
    lines.append(R(bTop(VS_L, VS_R)))
    lines.append(R(bMid(VS_L, VS_R, 'vSphere Cluster (ESXi Hosts)')))
    lines.append(R(bMid(VS_L, VS_R, 'Type-1 hypervisor: runs directly on hardware — no host OS required')))
    lines.append(R(bMid(VS_L, VS_R, 'Cluster features: HA · DRS · vMotion · Fault Tolerance')))
    lines.append(R({VS_L: '│', VS_R: '│'}))

    d = {VS_L: '│', VS_R: '│'}
    for eL, eR in ESXI: d.update(bTop(eL, eR))
    d.update(bTop(FB_L, FB_R))
    lines.append(R(d))

    d = {VS_L: '│', VS_R: '│'}
    for (eL, eR), lbl in zip(ESXI, ['ESXi-01', 'ESXi-02', 'ESXi-03', 'ESXi-04']):
        d.update(bMid(eL, eR, lbl))
    d.update(bMid(FB_L, FB_R, 'Each host: 50-200+ VMs'))
    lines.append(R(d))

    d = {VS_L: '│', VS_R: '│'}
    for eL, eR in ESXI:
        d[eL] = '│'; d[eR] = '│'
        d.update(bMid(eL, eR, '(Hypervisor)'))
    d.update(bMid(FB_L, FB_R, 'Types: web, DB, app, AD'))
    lines.append(R(d))

    d = {VS_L: '│', VS_R: '│'}
    for (eL, eR), (vmL, vmR) in zip(ESXI, VM_BOXES):
        d[eL] = '│'; d[eR] = '│'
        d.update(bTop(vmL, vmR))
    d.update(bMid(FB_L, FB_R, 'vMotion: live migration'))
    lines.append(R(d))

    d = {VS_L: '│', VS_R: '│'}
    for (eL, eR), (vmL, vmR) in zip(ESXI, VM_BOXES):
        d[eL] = '│'; d[eR] = '│'
        d.update(bMid(vmL, vmR, 'VMs'))
    d.update(bMid(FB_L, FB_R, 'HA: restart on failure'))
    lines.append(R(d))

    d = {VS_L: '│', VS_R: '│'}
    for (eL, eR), (vmL, vmR) in zip(ESXI, VM_BOXES):
        dd = bBot(eL, eR); dd[vmL] = '┴'; dd[vmR] = '┴'
        d.update(dd)
    d.update(bBot(FB_L, FB_R))
    lines.append(R(d))

    lines.append(R({VS_L: '│', VS_R: '│'}))
    lines.append(R(bBot(VS_L, VS_R)))
    lines.append(txt_row())

    # ── Integrated tier ───────────────────────────────────────────────────────
    lines.append(txt_row('  Integrated into vSphere — part of the hypervisor, not separate appliances:'))
    lines.append(txt_row())
    lines.append(R(arrow([(VSAN_L + VSAN_R) // 2, (NSX_L + NSX_R) // 2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(VSAN_L, VSAN_R), bTop(NSX_L, NSX_R))))
    lines.append(R(merge(
        bMid(VSAN_L, VSAN_R, 'vSAN (Software-Defined Storage)'),
        bMid(NSX_L,  NSX_R,  'NSX (Software-Defined Networking)'),
    )))
    lines.append(R(merge(
        bMid(VSAN_L, VSAN_R, 'Pooled from ESXi local disks'),
        bMid(NSX_L,  NSX_R,  'Virtual switches + distributed firewall'),
    )))
    lines.append(R(merge(
        bMid(VSAN_L, VSAN_R, 'Policy-based; no external array'),
        bMid(NSX_L,  NSX_R,  'Micro-segmentation & east-west routing'),
    )))
    lines.append(R(merge(bBot(VSAN_L, VSAN_R), bBot(NSX_L, NSX_R))))
    lines.append(txt_row())

    # ── Add-on tier ───────────────────────────────────────────────────────────
    lines.append(txt_row('  Add-on products — licensed separately, deployed on top of vSphere:'))
    lines.append(txt_row())
    lines.append(R(arrow([(HZ_L + HZ_R) // 2, (SRM_L + SRM_R) // 2, (REP_L + REP_R) // 2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(HZ_L, HZ_R), bTop(SRM_L, SRM_R), bTop(REP_L, REP_R))))
    lines.append(R(merge(
        bMid(HZ_L,  HZ_R,  'Horizon (VDI)'),
        bMid(SRM_L, SRM_R, 'Site Recovery Manager'),
        bMid(REP_L, REP_R, 'vSphere Replication'),
    )))
    lines.append(R(merge(
        bMid(HZ_L,  HZ_R,  '(Desktops)'),
        bMid(SRM_L, SRM_R, '(DR Orchestration)'),
        bMid(REP_L, REP_R, '(VM Replication)'),
    )))
    lines.append(R(merge(
        bMid(HZ_L,  HZ_R,  'VDI + app publishing'),
        bMid(SRM_L, SRM_R, 'Failover + Failback'),
        bMid(REP_L, REP_R, 'RPO-based replication'),
    )))
    lines.append(R(merge(bBot(HZ_L, HZ_R), bBot(SRM_L, SRM_R), bBot(REP_L, REP_R))))
    lines.append(txt_row())

    # ── VCF outer box with SDDC Manager + Tanzu nested inside ────────────────
    lines.append(R(bTop(VCF_L, VCF_R)))
    lines.append(R(bMid(VCF_L, VCF_R, 'VMware Cloud Foundation (VCF/SDDC)')))
    lines.append(R(bMid(VCF_L, VCF_R, 'Packages & delivers the full SDDC: vSphere + vSAN + NSX + Lifecycle')))
    lines.append(R({VCF_L: '│', VCF_R: '│'}))

    lines.append(R(merge({VCF_L: '│', VCF_R: '│'}, bTop(SDDC_L, SDDC_R), bTop(TZ_L, TZ_R))))
    lines.append(R(merge(
        {VCF_L: '│', VCF_R: '│'},
        bMid(SDDC_L, SDDC_R, 'SDDC Manager'),
        bMid(TZ_L,   TZ_R,   'Tanzu (Kubernetes Platform)'),
    )))
    lines.append(R(merge(
        {VCF_L: '│', VCF_R: '│'},
        bMid(SDDC_L, SDDC_R, 'Lifecycle orchestrator for VCF'),
        bMid(TZ_L,   TZ_R,   'Container Orchestration'),
    )))
    lines.append(R(merge(
        {VCF_L: '│', VCF_R: '│'},
        bMid(SDDC_L, SDDC_R, 'Bringup · Upgrades · Compliance'),
        bMid(TZ_L,   TZ_R,   'Workload domain within VCF'),
    )))
    lines.append(R(merge({VCF_L: '│', VCF_R: '│'}, bBot(SDDC_L, SDDC_R), bBot(TZ_L, TZ_R))))
    lines.append(R({VCF_L: '│', VCF_R: '│'}))
    lines.append(R(bBot(VCF_L, VCF_R)))
    lines.append(txt_row())

    # ── Physical infrastructure ───────────────────────────────────────────────
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('CPU cores · RAM (GBs to TBs per host) · NIC (10/25/100 GbE) · NVMe/SSD/HDD · Power & Cooling'))
    lines.append(txt_row())

    # ── Glossary ──────────────────────────────────────────────────────────────
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

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virtualization',
    'docs/virtualization/index.md',
    'VMware Platform Stack — VCF → vCenter/NSX-T/VxRail → ESXi → vSAN',
)
def virtualization_platform_stack():
    """VMware Platform Stack — W=103. Full learning diagram: VCF → vCenter/NSX-T/VxRail → ESXi → vSAN.

    Layout: inner=29 boxes with margin=3, gap=2 forces VCF_MID = NSX_MID = ESXI_MID = 51
    so the connector, branch ┼, and arrows all share the same column perfectly.
    """
    W2 = 103
    R, txt_row = make_helpers(W2)

    # ── Layout ───────────────────────────────────────────────────────────────
    # With inner=29, margin=3, gap=2: layout([29, 29, 29]) produces MIDs at 18, 51, 84.
    # VCF spans L=3 to R=99 (= VX_R), so VCF_MID = (3+99)//2 = 51 = NSX_MID. ✓
    # Branch: ┌ at 18, ┼ at 51, ┐ at 84 → left span = right span = 33. Symmetric.
    VCF_L, VCF_R   =  3, 99   # inner=95, MID=51
    VC_L,  VC_R    =  3, 33   # inner=29, MID=18
    NSX_L, NSX_R   = 36, 66   # inner=29, MID=51  (= VCF_MID)
    VX_L,  VX_R    = 69, 99   # inner=29, MID=84  (VX_R = VCF_R — shared wall)
    ESXI_L, ESXI_R =  3, 99   # inner=95, MID=51
    VSAN_L, VSAN_R =  3, 99   # inner=95, MID=51

    VCF_MID  = (VCF_L  + VCF_R)  // 2   # 51
    VC_MID   = (VC_L   + VC_R)   // 2   # 18
    NSX_MID  = (NSX_L  + NSX_R)  // 2   # 51  (= VCF_MID)
    VX_MID   = (VX_L   + VX_R)   // 2   # 84
    ESXI_MID = (ESXI_L + ESXI_R) // 2   # 51

    lines = []

    # ── Title ────────────────────────────────────────────────────────────────
    lines.append(title_border(W2, 'VMware Platform Stack'))
    lines.append(txt_row())

    # ── VCF box ───────────────────────────────────────────────────────────────
    lines.append(R(bTop(VCF_L, VCF_R)))
    lines.append(R(bMid(VCF_L, VCF_R, 'VMware Cloud Foundation (VCF / SDDC)')))
    lines.append(R(bMid(VCF_L, VCF_R, 'Packages and delivers the full SDDC: vSphere + vSAN + NSX + Lifecycle')))
    lines.append(R(bMid(VCF_L, VCF_R, 'SDDC Manager: bringup · upgrades · compliance · certificate rotation')))
    lines.append(R(bMid(VCF_L, VCF_R, 'Tanzu: Kubernetes workload domains hosted within VCF')))
    lines.append(R(bBot(VCF_L, VCF_R, tees=[VCF_MID])))

    # ── VCF → three-box branch ───────────────────────────────────────────────
    lines.append(R(connector([VCF_MID])))
    lines.append(txt_row('orchestrates', indent=VCF_MID - 6))
    lines.append(txt_row())
    d = {i: '─' for i in range(VC_MID, VX_MID + 1)}
    d[VC_MID] = '┌'; d[NSX_MID] = '┼'; d[VX_MID] = '┐'
    lines.append(R(d))
    lines.append(R(arrow([VC_MID, NSX_MID, VX_MID])))

    # ── vCenter · NSX-T · VxRail ──────────────────────────────────────────────
    lines.append(R(merge(bTop(VC_L, VC_R), bTop(NSX_L, NSX_R), bTop(VX_L, VX_R))))
    lines.append(R(merge(
        bMid(VC_L,  VC_R,  'vCenter'),
        bMid(NSX_L, NSX_R, 'NSX-T'),
        bMid(VX_L,  VX_R,  'VxRail'),
    )))
    lines.append(R(merge(
        bMid(VC_L,  VC_R,  'Management & Control Plane'),
        bMid(NSX_L, NSX_R, 'Software-Defined Networking'),
        bMid(VX_L,  VX_R,  'Hyper-Converged Appliance'),
    )))
    lines.append(R(merge(
        bMid(VC_L,  VC_R,  'Inventory · Roles · Alarms'),
        bMid(NSX_L, NSX_R, 'Segments · T0/T1 Gateways'),
        bMid(VX_L,  VX_R,  'Dell hardware + VMware stack'),
    )))
    lines.append(R(merge(
        bMid(VC_L,  VC_R,  'HA · DRS · vMotion · vLCM'),
        bMid(NSX_L, NSX_R, 'Distributed Firewall · LB'),
        bMid(VX_L,  VX_R,  'VxRail Manager · Lifecycle'),
    )))
    lines.append(R(merge(
        bMid(VC_L,  VC_R,  'SSO · LDAP · Permissions'),
        bMid(NSX_L, NSX_R, 'Micro-segmentation · VPN'),
        bMid(VX_L,  VX_R,  'Automated node expansion'),
    )))
    lines.append(R(merge(
        bBot(VC_L,  VC_R,  tees=[VC_MID]),
        bBot(NSX_L, NSX_R, tees=[NSX_MID]),
        bBot(VX_L,  VX_R),                         # VxRail stops here — no stem
    )))

    # ── vCenter + NSX-T → ESXi ────────────────────────────────────────────────
    lines.append(txt_row())
    lines.append(txt_row('  vCenter manages ESXi hosts and cluster resources; NSX-T runs inside the hypervisor'))
    lines.append(txt_row())
    lines.append(R(arrow([VC_MID, NSX_MID])))
    lines.append(txt_row())

    # ── ESXi box ──────────────────────────────────────────────────────────────
    lines.append(R(bTop(ESXI_L, ESXI_R)))
    lines.append(R(bMid(ESXI_L, ESXI_R, 'ESXi Hosts (vSphere Cluster)')))
    lines.append(R(bMid(ESXI_L, ESXI_R, 'Type-1 hypervisor: installed directly on bare metal — no host OS required')))
    lines.append(R(bMid(ESXI_L, ESXI_R, 'Cluster features: HA · DRS · vMotion · Fault Tolerance · EVC')))
    lines.append(R(bMid(ESXI_L, ESXI_R, 'VMkernel adapters: vmk0(mgmt) · vmk1(vMotion) · vmk2(vSAN) · vmk3(other)')))
    lines.append(R(bMid(ESXI_L, ESXI_R, 'Each host runs 50-200+ VMs; types: web · DB · app · AD · infra')))
    lines.append(R(bBot(ESXI_L, ESXI_R, tees=[ESXI_MID])))

    # ── ESXi → vSAN ───────────────────────────────────────────────────────────
    lines.append(txt_row())
    lines.append(txt_row('  ESXi local disks contribute capacity to vSAN — no external storage array required'))
    lines.append(txt_row())
    lines.append(R(arrow([ESXI_MID])))
    lines.append(txt_row())

    # ── vSAN box ──────────────────────────────────────────────────────────────
    lines.append(R(bTop(VSAN_L, VSAN_R)))
    lines.append(R(bMid(VSAN_L, VSAN_R, 'vSAN (Software-Defined Storage)')))
    lines.append(R(bMid(VSAN_L, VSAN_R, 'Pools local NVMe/SSD/HDD disks from all ESXi hosts into a shared datastore')))
    lines.append(R(bMid(VSAN_L, VSAN_R, 'Storage policy assigned per VM: RAID-1 (mirror) · RAID-5/6 (erasure coding)')))
    lines.append(R(bMid(VSAN_L, VSAN_R, 'Features: Deduplication · Compression · Encryption · Stretched Cluster')))
    lines.append(R(bBot(VSAN_L, VSAN_R)))
    lines.append(txt_row())

    # ── Physical infrastructure ───────────────────────────────────────────────
    lines.append(txt_row('Physical Infrastructure (the hardware all layers above run on):'))
    lines.append(txt_row('CPU cores · RAM (GBs to TBs per host) · NIC (10/25/100 GbE) · NVMe/SSD/HDD · Power & Cooling'))
    lines.append(txt_row())

    # ── Key terms ─────────────────────────────────────────────────────────────
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VCF      = VMware Cloud Foundation; packages vSphere + vSAN + NSX with lifecycle mgmt'))
    lines.append(txt_row('SDDC Mgr = VCF lifecycle orchestrator; automates bringup, upgrades, and compliance'))
    lines.append(txt_row('Tanzu    = VMware Kubernetes platform; runs container workloads inside VCF domains'))
    lines.append(txt_row('vCenter  = central management UI/API; manages hosts, VMs, roles, alarms, and lifecycle'))
    lines.append(txt_row('NSX-T    = software-defined networking; segments, gateways, DFW, LB, VPN, and routing'))
    lines.append(txt_row('VxRail   = Dell HCI appliance; compute + storage + networking in one rack unit'))
    lines.append(txt_row('ESXi     = Type-1 hypervisor; installed directly on bare metal — no host OS needed'))
    lines.append(txt_row('vSAN     = software-defined storage; pools local ESXi disks — no external array needed'))
    lines.append(txt_row('HA       = High Availability; vSphere auto-restarts VMs on another host if one fails'))
    lines.append(txt_row('DRS      = Distributed Resource Scheduler; auto-balances VM workload across ESXi hosts'))
    lines.append(txt_row('vMotion  = live migration of a running VM between ESXi hosts with zero downtime'))
    lines.append(txt_row('SSO      = Single Sign-On; central identity used by all vCenter/vSphere authentication'))
    lines.append(txt_row('vLCM     = vSphere Lifecycle Manager; patches ESXi hosts and manages firmware baselines'))
    lines.append(txt_row('DFW      = Distributed Firewall (NSX-T); stateful firewall enforced on every vNIC'))
    lines.append(txt_row('HCI      = Hyper-Converged Infrastructure; compute + storage + networking in one box'))
    lines.append(txt_row('SDDC     = Software-Defined Data Centre; compute, storage, and network all virtualised'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell',
    'docs/storage/dell/index.md',
    'Dell Storage Portfolio — PowerMax, PowerStore, Unity, PowerScale, Data Domain, ECS',
)
def dell_storage_portfolio():
    """Dell Storage Portfolio — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99   # full-width management, inner=95

    # Primary block tier (inner=29)
    PM_L, PM_R =  3, 33   # PowerMax,   MID=18
    PS_L, PS_R = 36, 66   # PowerStore, MID=51
    UT_L, UT_R = 69, 99   # Unity XT,   MID=84

    PM_MID = (PM_L + PM_R) // 2   # 18
    PS_MID = (PS_L + PS_R) // 2   # 51
    UT_MID = (UT_L + UT_R) // 2   # 84

    # Specialty tier (inner=29, same positions)
    SC_L, SC_R =  3, 33   # PowerScale
    DD_L, DD_R = 36, 66   # Data Domain
    EC_L, EC_R = 69, 99   # ECS

    # Protocol layer
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []

    lines.append(title_border(W2, 'Dell Storage Portfolio'))
    lines.append(txt_row())

    # ── Management ───────────────────────────────────────────────────────────
    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Dell Storage Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Unisphere: unified web UI for PowerMax, PowerStore, and Unity management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'CloudIQ: cloud analytics, health scoring, capacity forecasting, and proactive alerts')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'InsightIQ: performance analytics and capacity management for PowerScale/OneFS')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'REST API: programmatic management across all Dell storage platforms')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Dell AIOps: AI-driven recommendations and anomaly detection across the portfolio')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Unisphere and CloudIQ manage arrays via REST APIs — on-prem UI or cloud analytics portal'))
    lines.append(txt_row())
    lines.append(R(arrow([PM_MID, PS_MID, UT_MID])))
    lines.append(txt_row())

    # ── Primary Block Storage ────────────────────────────────────────────────
    lines.append(R(merge(bTop(PM_L, PM_R), bTop(PS_L, PS_R), bTop(UT_L, UT_R))))
    lines.append(R(merge(
        bMid(PM_L, PM_R, 'Dell PowerMax'),
        bMid(PS_L, PS_R, 'Dell PowerStore'),
        bMid(UT_L, UT_R, 'Dell Unity XT'),
    )))
    lines.append(R(merge(
        bMid(PM_L, PM_R, 'Enterprise all-flash block'),
        bMid(PS_L, PS_R, 'Mid-range all-flash unified'),
        bMid(UT_L, UT_R, 'Mid-range unified storage'),
    )))
    lines.append(R(merge(
        bMid(PM_L, PM_R, 'FC · iSCSI · NVMe/FC'),
        bMid(PS_L, PS_R, 'Block + file in one platform'),
        bMid(UT_L, UT_R, 'Block · file · VMware ready'),
    )))
    lines.append(R(merge(
        bMid(PM_L, PM_R, 'SRDF: sync + async repl'),
        bMid(PS_L, PS_R, 'AppsON: containers on-array'),
        bMid(UT_L, UT_R, 'FC · iSCSI · NFS · SMB'),
    )))
    lines.append(R(merge(
        bMid(PM_L, PM_R, 'TimeFinder: local snapshots'),
        bMid(PS_L, PS_R, 'Intelligent automation + ML'),
        bMid(UT_L, UT_R, 'Async replication + snaps'),
    )))
    lines.append(R(merge(
        bMid(PM_L, PM_R, 'NVMe end-to-end, up to 4PB'),
        bMid(PS_L, PS_R, 'NVMe-based storage nodes'),
        bMid(UT_L, UT_R, 'VAAI/VASA VMware support'),
    )))
    lines.append(R(merge(bBot(PM_L, PM_R), bBot(PS_L, PS_R), bBot(UT_L, UT_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Block arrays expose LUNs to hosts via FC, iSCSI, or NVMe; file via NFS and SMB'))
    lines.append(txt_row())
    lines.append(R(arrow([PM_MID, PS_MID, UT_MID])))
    lines.append(txt_row())

    # ── Specialty Storage ────────────────────────────────────────────────────
    lines.append(R(merge(bTop(SC_L, SC_R), bTop(DD_L, DD_R), bTop(EC_L, EC_R))))
    lines.append(R(merge(
        bMid(SC_L, SC_R, 'Dell PowerScale'),
        bMid(DD_L, DD_R, 'Dell Data Domain'),
        bMid(EC_L, EC_R, 'Dell ECS'),
    )))
    lines.append(R(merge(
        bMid(SC_L, SC_R, 'Scale-out NAS, OneFS OS'),
        bMid(DD_L, DD_R, 'Purpose-built backup dedup'),
        bMid(EC_L, EC_R, 'Enterprise object storage'),
    )))
    lines.append(R(merge(
        bMid(SC_L, SC_R, 'NFS · SMB · HDFS · S3'),
        bMid(DD_L, DD_R, 'DD Boost: client-side dedup'),
        bMid(EC_L, EC_R, 'S3 · Swift · Atmos APIs'),
    )))
    lines.append(R(merge(
        bMid(SC_L, SC_R, 'SmartQuotas: quota mgmt'),
        bMid(DD_L, DD_R, 'DD Replicator: remote copy'),
        bMid(EC_L, EC_R, 'Geo-distribution + WORM'),
    )))
    lines.append(R(merge(
        bMid(SC_L, SC_R, 'SyncIQ: async replication'),
        bMid(DD_L, DD_R, 'WORM: compliance retention'),
        bMid(EC_L, EC_R, 'Erasure coding for durability'),
    )))
    lines.append(R(merge(
        bMid(SC_L, SC_R, 'Up to 100PB per cluster'),
        bMid(DD_L, DD_R, 'Cloud Tier: long-term archive'),
        bMid(EC_L, EC_R, 'Petabyte-scale capacity'),
    )))
    lines.append(R(merge(bBot(SC_L, SC_R), bBot(DD_L, DD_R), bBot(EC_L, EC_R))))

    lines.append(txt_row())
    lines.append(txt_row('  VPLEX: storage federation and active-active data mobility across arrays and sites'))
    lines.append(txt_row('  PowerPath: host multipathing software; automatic path failover and load balancing'))
    lines.append(txt_row())
    lines.append(R(arrow([PM_MID, PS_MID, UT_MID])))
    lines.append(txt_row())

    # ── Protocol layer ───────────────────────────────────────────────────────
    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Fibre Channel', 'iSCSI', 'NFS', 'SMB / CIFS', 'S3 / Object'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['SAN block access', 'IP block access', 'Unix file mounts', 'Windows shares', 'REST object store'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['16G · 32G · 64G', 'TCP/IP · iSNS', 'NFS v3 · v4.1', 'CIFS · DFS-N', 'HTTP · REST · SDK'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['HBA → SAN switch', 'iSCSI initiator', 'Mount via IP', 'SMB sessions', 'Buckets + prefixes'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Zoning + masking', 'CHAP auth · iSNS', 'Export policies', 'Share perms+ACL', 'Policies + IAM'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    # ── Physical Infrastructure ──────────────────────────────────────────────
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NVMe/SSD/NL-SAS drives · FC HBAs · 10/25/100 GbE NICs · SAN switches · Power & Cooling'))
    lines.append(txt_row())

    # ── Glossary ─────────────────────────────────────────────────────────────
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('PowerMax     = Dell high-end all-flash block array; NVMe end-to-end, up to 4PB usable capacity'))
    lines.append(txt_row('PowerStore   = Dell mid-range unified array; block + file, AppsON containers, intelligent automation'))
    lines.append(txt_row('Unity XT     = Dell mid-range unified array; block, file, and deep VMware integration'))
    lines.append(txt_row('PowerScale   = Dell scale-out NAS running OneFS; supports NFS, SMB, HDFS, S3; scales to 100PB'))
    lines.append(txt_row('Data Domain  = Dell purpose-built backup appliance; DD Boost dedup, replication, cloud tier'))
    lines.append(txt_row('ECS          = Dell Enterprise Content Storage; S3-compatible object with geo-distribution and WORM'))
    lines.append(txt_row('VPLEX        = Dell storage federation; active-active data mobility across arrays and sites'))
    lines.append(txt_row('PowerPath    = Dell host multipathing software; automatic path failover and load balancing'))
    lines.append(txt_row('SRDF         = Symmetrix Remote Data Facility; sync or async replication between PowerMax arrays'))
    lines.append(txt_row('TimeFinder   = Dell local snapshot technology for PowerMax; point-in-time copies of volumes'))
    lines.append(txt_row('DD Boost     = Data Domain client-side dedup library; reduces data sent to the backup target'))
    lines.append(txt_row('OneFS        = PowerScale distributed file system OS; spans all nodes as a single namespace'))
    lines.append(txt_row('SyncIQ       = PowerScale async replication engine; policy-based replication to DR site'))
    lines.append(txt_row('SmartQuotas  = PowerScale quota management; enforces hard/soft limits per directory or user'))
    lines.append(txt_row('AppsON       = PowerStore capability to run VMs and containers directly on the storage array'))
    lines.append(txt_row('CloudIQ      = Dell cloud analytics SaaS; health scoring, capacity forecasting, proactive alerts'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'pure',
    'docs/storage/pure/index.md',
    'Pure Storage Stack — Pure1, FlashArray, FlashBlade, Evergreen, replication',
)
def pure_storage_stack():
    """Pure Storage Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    # Management — full width
    MGMT_L, MGMT_R = 3, 99   # inner=95

    # Product tier — three equal boxes (inner=29)
    FA_L, FA_R =  3, 33   # FlashArray, MID=18
    FB_L, FB_R = 36, 66   # FlashBlade, MID=51
    EG_L, EG_R = 69, 99   # Evergreen/One, MID=84

    FA_MID = (FA_L + FA_R) // 2   # 18
    FB_MID = (FB_L + FB_R) // 2   # 51
    EG_MID = (EG_L + EG_R) // 2   # 84

    # Services tier — three equal boxes (inner=29)
    AC_L, AC_R =  3, 33   # ActiveCluster
    AD_L, AD_R = 36, 66   # ActiveDR
    PO_L, PO_R = 69, 99   # Purity OS + SafeMode

    # Protocol layer — full width with 5 sections
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []

    # ── Title ────────────────────────────────────────────────────────────────
    lines.append(title_border(W2, 'Pure Storage Stack'))
    lines.append(txt_row())

    # ── Management tier ──────────────────────────────────────────────────────
    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Pure1')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'SaaS cloud management portal — no on-prem management appliance required')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Fleet health monitoring · capacity analytics · AI-driven anomaly detection')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Upgrade orchestration: non-disruptive controller and software refreshes')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Auto-opens support cases; integrates with Pure Technical Services team')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'REST API · Purity CLI · Pure Service Orchestrator (PSO) for Kubernetes')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Pure1 manages all arrays via HTTPS — no on-prem management server required'))
    lines.append(txt_row())
    lines.append(R(arrow([FA_MID, FB_MID, EG_MID])))
    lines.append(txt_row())

    # ── Product tier ─────────────────────────────────────────────────────────
    lines.append(R(merge(bTop(FA_L, FA_R), bTop(FB_L, FB_R), bTop(EG_L, EG_R))))
    lines.append(R(merge(
        bMid(FA_L, FA_R, 'Pure FlashArray'),
        bMid(FB_L, FB_R, 'Pure FlashBlade'),
        bMid(EG_L, EG_R, 'Evergreen / Evergreen//One'),
    )))
    lines.append(R(merge(
        bMid(FA_L, FA_R, '//X · //C · //E models'),
        bMid(FB_L, FB_R, '//S: perf · //E: capacity'),
        bMid(EG_L, EG_R, 'Non-disruptive refreshes'),
    )))
    lines.append(R(merge(
        bMid(FA_L, FA_R, 'All-flash block storage'),
        bMid(FB_L, FB_R, 'Scale-out file + object'),
        bMid(EG_L, EG_R, 'Controller swap, no downtime'),
    )))
    lines.append(R(merge(
        bMid(FA_L, FA_R, 'FC · iSCSI · NVMe-oF'),
        bMid(FB_L, FB_R, 'NFS · SMB · S3 · HDFS'),
        bMid(EG_L, EG_R, 'Evergreen//One: STaaS'),
    )))
    lines.append(R(merge(
        bMid(FA_L, FA_R, 'Always-on dedup + compress'),
        bMid(FB_L, FB_R, 'DirectFlash blade modules'),
        bMid(EG_L, EG_R, 'Pure-owned HW on-premises'),
    )))
    lines.append(R(merge(
        bMid(FA_L, FA_R, 'SafeMode: immutable snaps'),
        bMid(FB_L, FB_R, 'Rapid Restore: backup target'),
        bMid(EG_L, EG_R, 'SLA-guaranteed performance'),
    )))
    lines.append(R(merge(bBot(FA_L, FA_R), bBot(FB_L, FB_R), bBot(EG_L, EG_R))))

    lines.append(txt_row())
    lines.append(txt_row('  FlashArray serves block workloads · FlashBlade serves file and object workloads'))
    lines.append(txt_row())
    lines.append(R(arrow([FA_MID, FB_MID, EG_MID])))
    lines.append(txt_row())

    # ── Services tier ────────────────────────────────────────────────────────
    lines.append(R(merge(bTop(AC_L, AC_R), bTop(AD_L, AD_R), bTop(PO_L, PO_R))))
    lines.append(R(merge(
        bMid(AC_L, AC_R, 'ActiveCluster (Sync)'),
        bMid(AD_L, AD_R, 'ActiveDR (Async)'),
        bMid(PO_L, PO_R, 'Purity OS · SafeMode'),
    )))
    lines.append(R(merge(
        bMid(AC_L, AC_R, 'Active-active stretch cluster'),
        bMid(AD_L, AD_R, 'Asynchronous replication'),
        bMid(PO_L, PO_R, 'Purity//FA: FlashArray OS'),
    )))
    lines.append(R(merge(
        bMid(AC_L, AC_R, 'Sync replication, RPO=0'),
        bMid(AD_L, AD_R, 'RPO configurable (seconds)'),
        bMid(PO_L, PO_R, 'Purity//FB: FlashBlade OS'),
    )))
    lines.append(R(merge(
        bMid(AC_L, AC_R, 'Mediator: tie-breaker node'),
        bMid(AD_L, AD_R, 'Cross-array and cross-site DR'),
        bMid(PO_L, PO_R, 'SafeMode: retention-locked'),
    )))
    lines.append(R(merge(
        bMid(AC_L, AC_R, 'Transparent host failover'),
        bMid(AD_L, AD_R, 'Non-disruptive failover test'),
        bMid(PO_L, PO_R, 'Policy-based snap scheduling'),
    )))
    lines.append(R(merge(bBot(AC_L, AC_R), bBot(AD_L, AD_R), bBot(PO_L, PO_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Replication and data services protect workloads across sites and against ransomware'))
    lines.append(txt_row())
    lines.append(R(arrow([FA_MID, FB_MID, EG_MID])))
    lines.append(txt_row())

    # ── Protocol layer ───────────────────────────────────────────────────────
    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Fibre Channel', 'iSCSI', 'NVMe-oF', 'NFS / SMB', 'S3 / HDFS'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['SAN block access', 'IP block access', 'NVMe over Fabrics', 'File protocols', 'Object / analytics'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['16G · 32G · 64G', 'TCP/IP network', 'Ethernet / RoCE', 'NFS v3/v4.1 · SMB', 'REST · SDK · POSIX'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['HBA → SAN switch', 'iSCSI initiator', 'NVMe host adapter', 'Exports + shares', 'Buckets + keys'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Zoning + masking', 'CHAP auth · iSNS', 'RDMA low latency', 'Perms + quotas', 'IAM + policies'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    # ── Physical Infrastructure ──────────────────────────────────────────────
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('DirectFlash NVMe modules · Dual controllers · 10/25/100 GbE · FC 16G/32G · Power & Cooling'))
    lines.append(txt_row())

    # ── Glossary ─────────────────────────────────────────────────────────────
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('FlashArray    = Pure all-flash block array; //X (performance), //C (capacity), //E (entry)'))
    lines.append(txt_row('FlashBlade    = Pure scale-out file + object platform built on DirectFlash blade modules'))
    lines.append(txt_row('Pure1         = Pure SaaS cloud management; health, analytics, and upgrade orchestration'))
    lines.append(txt_row('Purity//FA    = FlashArray operating system; manages volumes, snapshots, and replication'))
    lines.append(txt_row('Purity//FB    = FlashBlade operating system; manages NFS, SMB, S3 buckets, and expansion'))
    lines.append(txt_row('ActiveCluster = Sync active-active stretch cluster; RPO=0, transparent host failover'))
    lines.append(txt_row('ActiveDR      = Async replication with configurable RPO (seconds); used for cross-site DR'))
    lines.append(txt_row('SafeMode      = Immutable retention-locked snapshots; immune to admin or ransomware deletion'))
    lines.append(txt_row('Evergreen     = Pure upgrade programme; controller refresh without downtime or data migration'))
    lines.append(txt_row('Evergreen//One= STaaS model; Pure owns and maintains hardware on-premises, billed by use'))
    lines.append(txt_row('DirectFlash   = Pure proprietary NVMe modules; bypasses SSD firmware for lower latency'))
    lines.append(txt_row('PSO           = Pure Service Orchestrator; Kubernetes operator for dynamic volume provisioning'))
    lines.append(txt_row('Mediator      = Lightweight VM that arbitrates ActiveCluster split-brain scenarios'))
    lines.append(txt_row('RPO           = Recovery Point Objective; max acceptable data loss (ActiveCluster=0, ActiveDR=secs)'))
    lines.append(txt_row('STaaS         = Storage-as-a-Service; hardware owned by Pure, customer pays by consumption'))
    lines.append(txt_row('NVMe-oF       = NVMe over Fabrics; extends NVMe protocol across Ethernet (RoCE) or FC'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'storage',
    'docs/storage/index.md',
    'Enterprise Storage Landscape — Pure, Dell, NetApp arrays + protocol layer',
)
def enterprise_storage_landscape():
    """Enterprise Storage Landscape — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    # Three equal-width boxes (inner=29, margin=3, gap=2)
    PURE_L, PURE_R =  3, 33   # inner=29, MID=18
    DELL_L, DELL_R = 36, 66   # inner=29, MID=51
    NTAP_L, NTAP_R = 69, 99   # inner=29, MID=84

    PURE_MID = (PURE_L + PURE_R) // 2   # 18
    DELL_MID = (DELL_L + DELL_R) // 2   # 51
    NTAP_MID = (NTAP_L + NTAP_R) // 2   # 84

    # Full-width protocol layer
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []

    # ── Title ────────────────────────────────────────────────────────────────
    lines.append(title_border(W2, 'Enterprise Storage Landscape'))
    lines.append(txt_row())

    # ── Management tier ──────────────────────────────────────────────────────
    lines.append(R(merge(bTop(PURE_L, PURE_R), bTop(DELL_L, DELL_R), bTop(NTAP_L, NTAP_R))))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Pure1'),
        bMid(DELL_L, DELL_R, 'Unisphere / CloudIQ'),
        bMid(NTAP_L, NTAP_R, 'ONTAP System Manager'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Cloud mgmt portal'),
        bMid(DELL_L, DELL_R, 'Unisphere: array admin UI'),
        bMid(NTAP_L, NTAP_R, 'Browser-based admin UI'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'FlashArray & FlashBlade'),
        bMid(DELL_L, DELL_R, 'CloudIQ: cloud analytics'),
        bMid(NTAP_L, NTAP_R, 'Volume, LUN & quota mgmt'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Capacity & performance'),
        bMid(DELL_L, DELL_R, 'Health scoring & forecast'),
        bMid(NTAP_L, NTAP_R, 'ActiveIQ: cloud analytics'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Proactive support alerts'),
        bMid(DELL_L, DELL_R, 'REST API & automation'),
        bMid(NTAP_L, NTAP_R, 'Proactive health alerting'),
    )))
    lines.append(R(merge(bBot(PURE_L, PURE_R), bBot(DELL_L, DELL_R), bBot(NTAP_L, NTAP_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Management planes connect to arrays via HTTPS / REST APIs'))
    lines.append(txt_row())
    lines.append(R(arrow([PURE_MID, DELL_MID, NTAP_MID])))
    lines.append(txt_row())

    # ── Primary Storage Arrays ───────────────────────────────────────────────
    lines.append(R(merge(bTop(PURE_L, PURE_R), bTop(DELL_L, DELL_R), bTop(NTAP_L, NTAP_R))))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Pure FlashArray'),
        bMid(DELL_L, DELL_R, 'Dell PowerMax / VMAX'),
        bMid(NTAP_L, NTAP_R, 'NetApp ONTAP'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'All-flash block storage'),
        bMid(DELL_L, DELL_R, 'Mission-critical block'),
        bMid(NTAP_L, NTAP_R, 'Unified block + file'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'FC · iSCSI · NVMe-oF'),
        bMid(DELL_L, DELL_R, 'FC · iSCSI · NVMe/FC'),
        bMid(NTAP_L, NTAP_R, 'FC · iSCSI · NFS · SMB'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Always-on dedup + comp'),
        bMid(DELL_L, DELL_R, 'SRDF: sync replication'),
        bMid(NTAP_L, NTAP_R, 'SnapMirror: replication'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'ActiveCluster: active-active'),
        bMid(DELL_L, DELL_R, 'Dynamic tiering + cache'),
        bMid(NTAP_L, NTAP_R, 'SnapCenter: backup mgmt'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'SafeMode: immutable snaps'),
        bMid(DELL_L, DELL_R, 'PowerPath: multipathing'),
        bMid(NTAP_L, NTAP_R, 'FabricPool: cloud tiering'),
    )))
    lines.append(R(merge(bBot(PURE_L, PURE_R), bBot(DELL_L, DELL_R), bBot(NTAP_L, NTAP_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Arrays expose LUNs (block) or volumes (file) to hosts and VMs via storage protocols'))
    lines.append(txt_row())
    lines.append(R(arrow([PURE_MID, DELL_MID, NTAP_MID])))
    lines.append(txt_row())

    # ── Specialty / Extended Storage ─────────────────────────────────────────
    lines.append(R(merge(bTop(PURE_L, PURE_R), bTop(DELL_L, DELL_R), bTop(NTAP_L, NTAP_R))))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Pure FlashBlade'),
        bMid(DELL_L, DELL_R, 'PowerScale / Data Domain'),
        bMid(NTAP_L, NTAP_R, 'Keystone / StorageGRID'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Scale-out file + object'),
        bMid(DELL_L, DELL_R, 'PowerScale: scale-out NAS'),
        bMid(NTAP_L, NTAP_R, 'Keystone: STaaS model'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'NFS · SMB · S3 protocols'),
        bMid(DELL_L, DELL_R, 'Data Domain: dedup backup'),
        bMid(NTAP_L, NTAP_R, 'StorageGRID: object store'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Unstructured data at scale'),
        bMid(DELL_L, DELL_R, 'NFS · SMB · DD Boost'),
        bMid(NTAP_L, NTAP_R, 'Cloud Volumes ONTAP'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Rapid Restore: backup'),
        bMid(DELL_L, DELL_R, 'Multi-PB capacity scaling'),
        bMid(NTAP_L, NTAP_R, 'Snap replication + backup'),
    )))
    lines.append(R(merge(bBot(PURE_L, PURE_R), bBot(DELL_L, DELL_R), bBot(NTAP_L, NTAP_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Specialty platforms handle unstructured data, backup, and cloud-connected workloads'))
    lines.append(txt_row())
    lines.append(R(arrow([PURE_MID, DELL_MID, NTAP_MID])))
    lines.append(txt_row())

    # ── Protocol Layer ───────────────────────────────────────────────────────
    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Fibre Channel', 'iSCSI', 'NFS', 'SMB / CIFS', 'S3 / Object'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['SAN block access', 'IP block access', 'Unix file mounts', 'Windows shares', 'REST object store'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['16G · 32G · 64G', 'TCP/IP · iSNS', 'NFS v3 · v4.1', 'CIFS · DFS-N', 'HTTP · REST · SDK'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['HBA → SAN switch', 'iSCSI initiator', 'Mount via IP', 'SMB sessions', 'Buckets + prefixes'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Zoning + masking', 'CHAP auth + iSNS', 'Export policies', 'Share perms+ACL', 'Policies + IAM'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    # ── Physical Infrastructure ──────────────────────────────────────────────
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NVMe/SSD drives · FC HBAs (16G/32G) · 10/25/100 GbE NICs · SAN switches · Power & Cooling'))
    lines.append(txt_row())

    # ── Glossary ─────────────────────────────────────────────────────────────
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('LUN          = Logical Unit Number; a block device exposed by a storage array via FC or iSCSI'))
    lines.append(txt_row('SAN          = Storage Area Network; dedicated high-speed network carrying block storage traffic'))
    lines.append(txt_row('NAS          = Network Attached Storage; file-level storage served over IP via NFS or SMB'))
    lines.append(txt_row('FC           = Fibre Channel; high-speed block protocol using HBAs, SAN switches, and WWPN zoning'))
    lines.append(txt_row('iSCSI        = Internet SCSI; block storage over standard TCP/IP — no specialised hardware required'))
    lines.append(txt_row('NFS          = Network File System; Unix/Linux file protocol; mounts remote directories over IP'))
    lines.append(txt_row('SMB          = Server Message Block; Windows file-sharing protocol, also known as CIFS'))
    lines.append(txt_row('SRDF         = Symmetrix Remote Data Facility; Dell EMC sync replication between PowerMax arrays'))
    lines.append(txt_row('SnapMirror   = NetApp replication engine; copies volumes between ONTAP systems or to cloud'))
    lines.append(txt_row('SafeMode     = Pure Storage immutable snapshot feature; protects data against ransomware deletion'))
    lines.append(txt_row('ActiveCluster= Pure active-active stretch cluster; I/O served from both sites simultaneously'))
    lines.append(txt_row('Dedup        = Deduplication; eliminates duplicate data blocks to reduce raw capacity consumption'))
    lines.append(txt_row('FabricPool   = NetApp tiering; auto-moves cold blocks to S3-compatible object storage'))
    lines.append(txt_row('ONTAP        = NetApp unified storage OS running on FAS, AFF, Cloud Volumes, and StorageGRID'))
    lines.append(txt_row('DD Boost     = Data Domain client-side dedup; reduces backup data transferred over the network'))
    lines.append(txt_row('Keystone     = NetApp STaaS subscription; on-prem arrays billed like cloud consumption'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cloud',
    'docs/cloud/index.md',
    'Cloud Infrastructure — AWS and Azure: IAM, compute, storage, networking, connectivity',
)
def cloud_infrastructure_overview():
    """Cloud Infrastructure Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99   # full-width, inner=95

    # Two-cloud layout
    AWS_L, AWS_R = 3, 50    # inner=46, MID=26
    AZ_L,  AZ_R  = 53, 99  # inner=45, MID=76

    AWS_MID = (AWS_L + AWS_R) // 2   # 26
    AZ_MID  = (AZ_L  + AZ_R)  // 2   # 76

    CONN_L, CONN_R = 3, 99

    lines = []

    # ── Title ────────────────────────────────────────────────────────────────
    lines.append(title_border(W2, 'Cloud Infrastructure'))
    lines.append(txt_row())

    # ── Management tier ──────────────────────────────────────────────────────
    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Cloud Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'AWS: Console · CloudWatch · CloudTrail · Organizations · Control Tower · Cost Explorer')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Azure: Portal · Monitor · Log Analytics · Entra ID · Management Groups · Cost Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'AWS Config + Service Control Policies enforce governance across accounts')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Azure Policy + Blueprints enforce governance across subscriptions')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Both platforms expose REST APIs and CLIs (aws-cli / az-cli) for automation')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Governance, monitoring, and automation span all resources across both platforms'))
    lines.append(txt_row())
    lines.append(R(arrow([AWS_MID, AZ_MID])))
    lines.append(txt_row())

    # ── Identity & Access tier ────────────────────────────────────────────────
    lines.append(R(merge(bTop(AWS_L, AWS_R), bTop(AZ_L, AZ_R))))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'AWS IAM'),
        bMid(AZ_L,  AZ_R,  'Azure Entra ID (AAD)'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'Users · groups · roles · policies'),
        bMid(AZ_L,  AZ_R,  'Users · groups · service principals'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'Policy: allow/deny on AWS resources'),
        bMid(AZ_L,  AZ_R,  'RBAC: role assignments on resources'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'STS: temporary credentials + AssumeRole'),
        bMid(AZ_L,  AZ_R,  'PIM: just-in-time privileged access'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'Federation: SAML 2.0 · OIDC · SSO'),
        bMid(AZ_L,  AZ_R,  'Conditional Access: MFA + location'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'Managed policies · SCPs · permissions'),
        bMid(AZ_L,  AZ_R,  'Service principals · managed identities'),
    )))
    lines.append(R(merge(bBot(AWS_L, AWS_R), bBot(AZ_L, AZ_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Identity controls who can access what — least-privilege IAM is the security foundation'))
    lines.append(txt_row())
    lines.append(R(arrow([AWS_MID, AZ_MID])))
    lines.append(txt_row())

    # ── Compute tier ──────────────────────────────────────────────────────────
    lines.append(R(merge(bTop(AWS_L, AWS_R), bTop(AZ_L, AZ_R))))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'AWS Compute'),
        bMid(AZ_L,  AZ_R,  'Azure Compute'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'EC2: VMs — on-demand/reserved/spot'),
        bMid(AZ_L,  AZ_R,  'VMs: sizes — pay-as-you-go/reserved'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'Auto Scaling + ALB/NLB load balancers'),
        bMid(AZ_L,  AZ_R,  'VMSS + Azure Load Balancer / App GW'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'ECS/EKS: container and Kubernetes'),
        bMid(AZ_L,  AZ_R,  'AKS: managed Kubernetes clusters'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'Lambda: serverless function execution'),
        bMid(AZ_L,  AZ_R,  'Azure Functions: serverless execution'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'AMI: VM image; instance store/EBS root'),
        bMid(AZ_L,  AZ_R,  'Compute Gallery: VM image versioning'),
    )))
    lines.append(R(merge(bBot(AWS_L, AWS_R), bBot(AZ_L, AZ_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Compute resources run inside VPCs (AWS) or VNets (Azure) for network isolation'))
    lines.append(txt_row())
    lines.append(R(arrow([AWS_MID, AZ_MID])))
    lines.append(txt_row())

    # ── Storage & Networking tier ─────────────────────────────────────────────
    lines.append(R(merge(bTop(AWS_L, AWS_R), bTop(AZ_L, AZ_R))))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'AWS Storage & Networking'),
        bMid(AZ_L,  AZ_R,  'Azure Storage & Networking'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'S3: object storage, lifecycle, versioning'),
        bMid(AZ_L,  AZ_R,  'Blob Storage: hot/cool/archive tiers'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'EBS: block volumes attached to EC2'),
        bMid(AZ_L,  AZ_R,  'Managed Disks: block volumes for VMs'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'EFS/FSx: managed NFS and SMB services'),
        bMid(AZ_L,  AZ_R,  'Azure Files + NetApp Files (NFS/SMB)'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'VPC: subnets · SGs · NACLs · routes'),
        bMid(AZ_L,  AZ_R,  'VNet: subnets · NSGs · UDRs · peering'),
    )))
    lines.append(R(merge(
        bMid(AWS_L, AWS_R, 'Route53 · CloudFront · WAF · Shield'),
        bMid(AZ_L,  AZ_R,  'Azure DNS · Front Door · WAF · DDoS'),
    )))
    lines.append(R(merge(bBot(AWS_L, AWS_R), bBot(AZ_L, AZ_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Hybrid connectivity links on-premises data centres to cloud resources'))
    lines.append(txt_row())
    lines.append(R(arrow([AWS_MID, AZ_MID])))
    lines.append(txt_row())

    # ── Connectivity tier ─────────────────────────────────────────────────────
    lines.append(R(bTop(CONN_L, CONN_R)))
    lines.append(R(bMid(CONN_L, CONN_R, 'Hybrid Connectivity')))
    lines.append(R(bMid(CONN_L, CONN_R, 'AWS Direct Connect · Azure ExpressRoute: dedicated private circuits to cloud (1/10 Gbps)')))
    lines.append(R(bMid(CONN_L, CONN_R, 'AWS Site-to-Site VPN · Azure VPN Gateway: IPsec tunnels over the public internet')))
    lines.append(R(bMid(CONN_L, CONN_R, 'VPC Peering · VNet Peering: private routing between cloud network segments')))
    lines.append(R(bMid(CONN_L, CONN_R, 'AWS Transit Gateway · Azure Virtual WAN: hub-and-spoke WAN topology at scale')))
    lines.append(R(bBot(CONN_L, CONN_R)))

    # ── Physical Infrastructure ──────────────────────────────────────────────
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Cloud regions and availability zones; data centres owned and operated by AWS and Microsoft'))
    lines.append(txt_row())

    # ── Glossary ─────────────────────────────────────────────────────────────
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Region       = geographic area containing multiple isolated data centre clusters (AZs)'))
    lines.append(txt_row('AZ           = Availability Zone; isolated data centre within a region for fault tolerance'))
    lines.append(txt_row('IAM          = Identity and Access Management; controls who can call which AWS API actions'))
    lines.append(txt_row('Entra ID     = Azure Active Directory; cloud identity for users and service principals'))
    lines.append(txt_row('RBAC         = Role-Based Access Control; Azure permission model built on role assignments'))
    lines.append(txt_row('STS          = AWS Security Token Service; issues temporary credentials for AssumeRole calls'))
    lines.append(txt_row('EC2          = Elastic Compute Cloud; AWS virtual machines with many instance type families'))
    lines.append(txt_row('VMSS         = Azure Virtual Machine Scale Set; auto-scaling pool of identical VMs'))
    lines.append(txt_row('VPC          = Virtual Private Cloud; isolated AWS network with subnets and route tables'))
    lines.append(txt_row('VNet         = Azure Virtual Network; isolated Azure network with subnets and NSG rules'))
    lines.append(txt_row('S3           = Simple Storage Service; AWS object store with 11 nines durability guarantee'))
    lines.append(txt_row('NSG          = Network Security Group; Azure stateful firewall applied to subnets or NICs'))
    lines.append(txt_row('SG           = Security Group; AWS stateful firewall applied to EC2 instances and ENIs'))
    lines.append(txt_row('EKS          = Elastic Kubernetes Service; AWS managed Kubernetes control plane'))
    lines.append(txt_row('AKS          = Azure Kubernetes Service; Azure managed Kubernetes control plane'))
    lines.append(txt_row('Direct Connect= Dedicated private circuit from on-prem to AWS — bypasses public internet'))
    lines.append(txt_row('ExpressRoute = Dedicated private circuit from on-prem to Azure — bypasses public internet'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'netapp',
    'docs/storage/netapp/index.md',
    'NetApp Storage Stack — ONTAP, StorageGRID, Keystone, SnapMirror, SnapCenter, FabricPool',
)
def netapp_storage_stack():
    """NetApp Storage Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    # Management — full width
    MGMT_L, MGMT_R = 3, 99   # inner=95

    # Product tier — three equal boxes (inner=29)
    OT_L, OT_R =  3, 33   # ONTAP (AFF/FAS), MID=18
    SG_L, SG_R = 36, 66   # StorageGRID, MID=51
    KS_L, KS_R = 69, 99   # Keystone, MID=84

    OT_MID = (OT_L + OT_R) // 2   # 18
    SG_MID = (SG_L + SG_R) // 2   # 51
    KS_MID = (KS_L + KS_R) // 2   # 84

    # Data services tier (inner=29, same positions)
    SM_L, SM_R =  3, 33   # SnapMirror
    SC_L, SC_R = 36, 66   # SnapCenter
    FP_L, FP_R = 69, 99   # FabricPool

    # Protocol layer
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []

    # ── Title ────────────────────────────────────────────────────────────────
    lines.append(title_border(W2, 'NetApp Storage Stack'))
    lines.append(txt_row())

    # ── Management tier ──────────────────────────────────────────────────────
    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'NetApp Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'ONTAP System Manager: browser-based admin UI for volumes, LUNs, and quotas')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'ActiveIQ: cloud analytics — health scoring, capacity forecasting, proactive alerts')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'REST API: programmatic management across AFF, FAS, Cloud Volumes, StorageGRID')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'ONTAP CLI: SSH-based command-line management for volumes, aggregates, and SVMs')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'BlueXP: unified multi-cloud management — on-prem and cloud ONTAP from one console')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  ONTAP System Manager and BlueXP manage arrays via REST APIs'))
    lines.append(txt_row())
    lines.append(R(arrow([OT_MID, SG_MID, KS_MID])))
    lines.append(txt_row())

    # ── Product tier ─────────────────────────────────────────────────────────
    lines.append(R(merge(bTop(OT_L, OT_R), bTop(SG_L, SG_R), bTop(KS_L, KS_R))))
    lines.append(R(merge(
        bMid(OT_L, OT_R, 'NetApp ONTAP'),
        bMid(SG_L, SG_R, 'NetApp StorageGRID'),
        bMid(KS_L, KS_R, 'NetApp Keystone'),
    )))
    lines.append(R(merge(
        bMid(OT_L, OT_R, 'AFF · FAS · ONTAP Select'),
        bMid(SG_L, SG_R, 'Enterprise object storage'),
        bMid(KS_L, KS_R, 'Storage-as-a-service'),
    )))
    lines.append(R(merge(
        bMid(OT_L, OT_R, 'Unified block + file + S3'),
        bMid(SG_L, SG_R, 'S3 · Swift · NFS · HDFS'),
        bMid(KS_L, KS_R, 'NetApp-owned HW on-premises'),
    )))
    lines.append(R(merge(
        bMid(OT_L, OT_R, 'FC · iSCSI · NFS · SMB'),
        bMid(SG_L, SG_R, 'WORM: compliance retention'),
        bMid(KS_L, KS_R, 'Billed by consumption (TiB)'),
    )))
    lines.append(R(merge(
        bMid(OT_L, OT_R, 'MetroCluster: sync stretch'),
        bMid(SG_L, SG_R, 'Erasure coding for durability'),
        bMid(KS_L, KS_R, 'SLA-guaranteed performance'),
    )))
    lines.append(R(merge(
        bMid(OT_L, OT_R, 'Cloud Volumes ONTAP: AWS/GCP'),
        bMid(SG_L, SG_R, 'Petabyte-scale capacity'),
        bMid(KS_L, KS_R, 'Flex burst above committed'),
    )))
    lines.append(R(merge(bBot(OT_L, OT_R), bBot(SG_L, SG_R), bBot(KS_L, KS_R))))

    lines.append(txt_row())
    lines.append(txt_row('  ONTAP serves block and file workloads · StorageGRID serves object workloads at scale'))
    lines.append(txt_row())
    lines.append(R(arrow([OT_MID, SG_MID, KS_MID])))
    lines.append(txt_row())

    # ── Data services tier ───────────────────────────────────────────────────
    lines.append(R(merge(bTop(SM_L, SM_R), bTop(SC_L, SC_R), bTop(FP_L, FP_R))))
    lines.append(R(merge(
        bMid(SM_L, SM_R, 'SnapMirror'),
        bMid(SC_L, SC_R, 'SnapCenter'),
        bMid(FP_L, FP_R, 'FabricPool'),
    )))
    lines.append(R(merge(
        bMid(SM_L, SM_R, 'Async + sync replication'),
        bMid(SC_L, SC_R, 'Application-aware backup'),
        bMid(FP_L, FP_R, 'Auto cold-data tiering'),
    )))
    lines.append(R(merge(
        bMid(SM_L, SM_R, 'DR + data distribution'),
        bMid(SC_L, SC_R, 'SQL · Oracle · SAP · VMware'),
        bMid(FP_L, FP_R, 'Tier to S3 or cloud object'),
    )))
    lines.append(R(merge(
        bMid(SM_L, SM_R, 'ONTAP to ONTAP or cloud'),
        bMid(SC_L, SC_R, 'Consistent snapshot + clone'),
        bMid(FP_L, FP_R, 'Reduce on-prem footprint'),
    )))
    lines.append(R(merge(
        bMid(SM_L, SM_R, 'Active Sync: RPO=0'),
        bMid(SC_L, SC_R, 'Restore to alt. location'),
        bMid(FP_L, FP_R, 'Policy-based temp scan'),
    )))
    lines.append(R(merge(bBot(SM_L, SM_R), bBot(SC_L, SC_R), bBot(FP_L, FP_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Data services protect, replicate, and optimise capacity across all ONTAP platforms'))
    lines.append(txt_row())
    lines.append(R(arrow([OT_MID, SG_MID, KS_MID])))
    lines.append(txt_row())

    # ── Protocol layer ───────────────────────────────────────────────────────
    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Fibre Channel', 'iSCSI', 'NFS', 'SMB / CIFS', 'S3 / Object'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['SAN block access', 'IP block access', 'Unix file mounts', 'Windows shares', 'REST object store'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['16G · 32G · 64G', 'TCP/IP · iSNS', 'NFS v3 · v4.1', 'CIFS · DFS-N', 'HTTP · REST · SDK'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['HBA → SAN switch', 'iSCSI initiator', 'Mount via IP', 'SMB sessions', 'Buckets + prefixes'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Zoning + masking', 'CHAP auth · iSNS', 'Export policies', 'Share perms+ACL', 'Policies + IAM'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    # ── Physical Infrastructure ──────────────────────────────────────────────
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NVMe/SSD/HDD drives · FC HBAs · 10/25/100 GbE NICs · SAN switches · Power & Cooling'))
    lines.append(txt_row())

    # ── Glossary ─────────────────────────────────────────────────────────────
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ONTAP        = NetApp unified storage OS; runs on AFF, FAS, Cloud Volumes, and ONTAP Select'))
    lines.append(txt_row('AFF          = All-Flash FAS; NetApp all-NVMe/SSD arrays optimised for performance workloads'))
    lines.append(txt_row('FAS          = Fabric-Attached Storage; NetApp hybrid arrays with HDD and SSD capacity tiers'))
    lines.append(txt_row('SVM          = Storage Virtual Machine; logical ONTAP partition with its own namespace and protocols'))
    lines.append(txt_row('SnapMirror   = NetApp replication engine; async or sync volume copies between ONTAP systems'))
    lines.append(txt_row('SnapCenter   = Application-consistent backup tool; integrates with SQL, Oracle, SAP, and VMware'))
    lines.append(txt_row('FabricPool   = ONTAP auto-tiering; moves cold data blocks to S3-compatible object storage'))
    lines.append(txt_row('StorageGRID  = NetApp object store; S3/Swift APIs, WORM compliance, petabyte geo-distribution'))
    lines.append(txt_row('Keystone     = NetApp STaaS; NetApp-owned hardware on-prem, billed by consumption per TiB'))
    lines.append(txt_row('ActiveIQ     = NetApp SaaS analytics; predictive health, capacity forecasting, proactive support'))
    lines.append(txt_row('MetroCluster = ONTAP sync stretch cluster; RPO=0 across two sites with transparent failover'))
    lines.append(txt_row('Active Sync  = SnapMirror Active Sync; granular sync replication for persistent LUN access'))
    lines.append(txt_row('FlexVol      = ONTAP flexible volume; dynamically grows or shrinks within a storage aggregate'))
    lines.append(txt_row('FlexGroup    = ONTAP distributed volume; scales to petabytes across multiple cluster nodes'))
    lines.append(txt_row('BlueXP       = NetApp unified console; manages on-prem and cloud ONTAP from one SaaS portal'))
    lines.append(txt_row('SnapVault    = Policy-based snapshot replication to a secondary system for backup retention'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aws',
    'docs/cloud/aws/index.md',
    'AWS Platform Stack — IAM, Compute, Networking, Storage, DB, Security, Connectivity',
)
def aws_platform_stack():
    """AWS Platform Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    IA_L, IA_R =  3, 33;  IA_MID = (IA_L + IA_R) // 2
    CP_L, CP_R = 36, 66;  CP_MID = (CP_L + CP_R) // 2
    NW_L, NW_R = 69, 99;  NW_MID = (NW_L + NW_R) // 2
    ST_L, ST_R =  3, 33
    DB_L, DB_R = 36, 66
    SC_L, SC_R = 69, 99
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'AWS Platform Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'AWS Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Console · CloudWatch · CloudTrail · Organizations · Control Tower · Cost Explorer')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'AWS Config: resource compliance rules · SCPs: account-level permission guardrails')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Trusted Advisor: cost, security, and performance best-practice checks')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'AWS CLI · SDK (boto3) · CloudFormation · CDK: infrastructure as code')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Governance and automation span all AWS services and accounts'))
    lines.append(txt_row())
    lines.append(R(arrow([IA_MID, CP_MID, NW_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(IA_L, IA_R), bTop(CP_L, CP_R), bTop(NW_L, NW_R))))
    lines.append(R(merge(
        bMid(IA_L, IA_R, 'AWS IAM'),
        bMid(CP_L, CP_R, 'Compute'),
        bMid(NW_L, NW_R, 'Networking'),
    )))
    lines.append(R(merge(
        bMid(IA_L, IA_R, 'Users · groups · roles'),
        bMid(CP_L, CP_R, 'EC2: on-demand/reserved'),
        bMid(NW_L, NW_R, 'VPC: subnets · routing'),
    )))
    lines.append(R(merge(
        bMid(IA_L, IA_R, 'Policies: allow/deny'),
        bMid(CP_L, CP_R, 'Auto Scaling · ALB/NLB'),
        bMid(NW_L, NW_R, 'SG · NACL: stateful FW'),
    )))
    lines.append(R(merge(
        bMid(IA_L, IA_R, 'STS: temp credentials'),
        bMid(CP_L, CP_R, 'ECS · EKS: containers'),
        bMid(NW_L, NW_R, 'Route53: DNS service'),
    )))
    lines.append(R(merge(
        bMid(IA_L, IA_R, 'AssumeRole: delegation'),
        bMid(CP_L, CP_R, 'Lambda: serverless FaaS'),
        bMid(NW_L, NW_R, 'CloudFront: global CDN'),
    )))
    lines.append(R(merge(
        bMid(IA_L, IA_R, 'SAML 2.0 · OIDC · SSO'),
        bMid(CP_L, CP_R, 'Spot: spare capacity'),
        bMid(NW_L, NW_R, 'WAF · Shield: DDoS'),
    )))
    lines.append(R(merge(bBot(IA_L, IA_R), bBot(CP_L, CP_R), bBot(NW_L, NW_R))))

    lines.append(txt_row())
    lines.append(txt_row('  IAM controls access · EC2 runs inside VPCs · networking isolates workloads'))
    lines.append(txt_row())
    lines.append(R(arrow([IA_MID, CP_MID, NW_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(ST_L, ST_R), bTop(DB_L, DB_R), bTop(SC_L, SC_R))))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'Storage'),
        bMid(DB_L, DB_R, 'Database'),
        bMid(SC_L, SC_R, 'Security & Monitoring'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'S3: object + versioning'),
        bMid(DB_L, DB_R, 'RDS: managed relational'),
        bMid(SC_L, SC_R, 'GuardDuty: threat detect'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'EBS: block volumes (EC2)'),
        bMid(DB_L, DB_R, 'Aurora: MySQL/PostgreSQL'),
        bMid(SC_L, SC_R, 'Security Hub: findings'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'EFS: managed NFS share'),
        bMid(DB_L, DB_R, 'DynamoDB: serverless KV'),
        bMid(SC_L, SC_R, 'CloudTrail: API audit log'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'FSx: Windows/Lustre/ONTAP'),
        bMid(DB_L, DB_R, 'ElastiCache: Redis/Memcd'),
        bMid(SC_L, SC_R, 'Config: compliance rules'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'Glacier: archive storage'),
        bMid(DB_L, DB_R, 'Redshift: data warehouse'),
        bMid(SC_L, SC_R, 'KMS: key management'),
    )))
    lines.append(R(merge(bBot(ST_L, ST_R), bBot(DB_L, DB_R), bBot(SC_L, SC_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Storage, databases, and security services consumed as fully managed APIs'))
    lines.append(txt_row())
    lines.append(R(arrow([IA_MID, CP_MID, NW_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Hybrid & Multi-Account Connectivity')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Direct Connect: dedicated private circuit from on-premises to AWS (1/10 Gbps)')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Site-to-Site VPN: IPsec tunnel over the public internet to a VPC endpoint')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Transit Gateway: hub-and-spoke router connecting VPCs and on-prem networks')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'VPC Peering: private routing between two VPCs within or across regions')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS global regions and availability zones; data centres owned and operated by Amazon'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('IAM           = Identity and Access Management; controls which API actions a principal can call'))
    lines.append(txt_row('STS           = Security Token Service; issues temporary credentials via AssumeRole'))
    lines.append(txt_row('EC2           = Elastic Compute Cloud; virtual machines with hundreds of instance type families'))
    lines.append(txt_row('ECS           = Elastic Container Service; managed container orchestration on EC2 or Fargate'))
    lines.append(txt_row('EKS           = Elastic Kubernetes Service; AWS managed Kubernetes control plane'))
    lines.append(txt_row('Lambda        = Serverless function execution; event-driven, no server provisioning required'))
    lines.append(txt_row('VPC           = Virtual Private Cloud; isolated network with subnets, route tables, and gateways'))
    lines.append(txt_row('SG            = Security Group; stateful firewall applied to EC2 instances and ENIs'))
    lines.append(txt_row('S3            = Simple Storage Service; object store with 11 nines durability guarantee'))
    lines.append(txt_row('EBS           = Elastic Block Store; persistent block volumes for EC2; gp3 and io2 Block Express'))
    lines.append(txt_row('RDS           = Relational Database Service; managed MySQL, PostgreSQL, SQL Server, Oracle'))
    lines.append(txt_row('Route53       = AWS managed DNS; latency routing, geo-routing, and health-check failover'))
    lines.append(txt_row('CloudFront    = AWS CDN; caches content at 400+ global edge locations; integrates with WAF'))
    lines.append(txt_row('GuardDuty     = ML threat detection; analyses VPC Flow Logs, CloudTrail, and DNS logs'))
    lines.append(txt_row('Direct Connect= Dedicated private circuit from on-premises to AWS — bypasses public internet'))
    lines.append(txt_row('Transit Gateway= Hub-and-spoke router connecting multiple VPCs and Direct Connect/VPN links'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'azure',
    'docs/cloud/azure/index.md',
    'Azure Platform Stack — Entra ID, Compute, Networking, Storage, DB, Security',
)
def azure_platform_stack():
    """Azure Platform Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    ID_L, ID_R =  3, 33;  ID_MID = (ID_L + ID_R) // 2
    CP_L, CP_R = 36, 66;  CP_MID = (CP_L + CP_R) // 2
    NW_L, NW_R = 69, 99;  NW_MID = (NW_L + NW_R) // 2
    ST_L, ST_R =  3, 33
    DB_L, DB_R = 36, 66
    SC_L, SC_R = 69, 99
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'Azure Platform Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Azure Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Portal · Azure Monitor · Log Analytics · Cost Management · Resource Manager · Policy')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Management Groups → Subscriptions → Resource Groups: hierarchical governance model')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Entra ID: cloud identity for users, apps, and workloads across the tenant')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'az CLI · Azure PowerShell · ARM templates · Bicep: infrastructure as code')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Governance and policy enforcement span all subscriptions and resource groups'))
    lines.append(txt_row())
    lines.append(R(arrow([ID_MID, CP_MID, NW_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(ID_L, ID_R), bTop(CP_L, CP_R), bTop(NW_L, NW_R))))
    lines.append(R(merge(
        bMid(ID_L, ID_R, 'Entra ID (Azure AD)'),
        bMid(CP_L, CP_R, 'Compute'),
        bMid(NW_L, NW_R, 'Networking'),
    )))
    lines.append(R(merge(
        bMid(ID_L, ID_R, 'Users · groups · app regs'),
        bMid(CP_L, CP_R, 'VMs: PAYG/reserved sizes'),
        bMid(NW_L, NW_R, 'VNet: subnets · peering'),
    )))
    lines.append(R(merge(
        bMid(ID_L, ID_R, 'RBAC: role assignments'),
        bMid(CP_L, CP_R, 'VMSS: auto-scaling pool'),
        bMid(NW_L, NW_R, 'NSG: stateful FW on NICs'),
    )))
    lines.append(R(merge(
        bMid(ID_L, ID_R, 'PIM: just-in-time access'),
        bMid(CP_L, CP_R, 'AKS: managed Kubernetes'),
        bMid(NW_L, NW_R, 'Azure DNS: managed DNS'),
    )))
    lines.append(R(merge(
        bMid(ID_L, ID_R, 'Conditional Access · MFA'),
        bMid(CP_L, CP_R, 'Functions: serverless FaaS'),
        bMid(NW_L, NW_R, 'Front Door: global CDN'),
    )))
    lines.append(R(merge(
        bMid(ID_L, ID_R, 'Service principals · MI'),
        bMid(CP_L, CP_R, 'App Service: PaaS host'),
        bMid(NW_L, NW_R, 'WAF · DDoS Protection'),
    )))
    lines.append(R(merge(bBot(ID_L, ID_R), bBot(CP_L, CP_R), bBot(NW_L, NW_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Entra ID controls access · VMs run inside VNets · NSGs enforce network policy'))
    lines.append(txt_row())
    lines.append(R(arrow([ID_MID, CP_MID, NW_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(ST_L, ST_R), bTop(DB_L, DB_R), bTop(SC_L, SC_R))))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'Storage'),
        bMid(DB_L, DB_R, 'Database'),
        bMid(SC_L, SC_R, 'Security & Monitoring'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'Blob: hot/cool/archive'),
        bMid(DB_L, DB_R, 'Azure SQL: managed MSSQL'),
        bMid(SC_L, SC_R, 'Defender for Cloud: CSPM'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'Managed Disks: block VMs'),
        bMid(DB_L, DB_R, 'Cosmos DB: multi-model'),
        bMid(SC_L, SC_R, 'Sentinel: SIEM + SOAR'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'Azure Files: NFS/SMB'),
        bMid(DB_L, DB_R, 'PostgreSQL: managed PG'),
        bMid(SC_L, SC_R, 'Key Vault: secrets+certs'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'NetApp Files: enterprise'),
        bMid(DB_L, DB_R, 'Redis Cache: in-memory'),
        bMid(SC_L, SC_R, 'Policy: compliance scan'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'ADLS Gen2: analytics'),
        bMid(DB_L, DB_R, 'Synapse: data warehouse'),
        bMid(SC_L, SC_R, 'Monitor: metrics + logs'),
    )))
    lines.append(R(merge(bBot(ST_L, ST_R), bBot(DB_L, DB_R), bBot(SC_L, SC_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Storage, databases, and security services consumed as fully managed platform APIs'))
    lines.append(txt_row())
    lines.append(R(arrow([ID_MID, CP_MID, NW_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Hybrid & Multi-Subscription Connectivity')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'ExpressRoute: dedicated private circuit from on-premises to Azure (1/10 Gbps)')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'VPN Gateway: IPsec tunnels over the public internet to Azure VNets')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'VNet Peering: private routing between VNets within or across regions')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Virtual WAN: hub-and-spoke WAN topology for global connectivity at scale')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure global regions and availability zones; data centres owned and operated by Microsoft'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Entra ID      = Azure Active Directory; cloud identity for users, devices, and service principals'))
    lines.append(txt_row('RBAC          = Role-Based Access Control; Azure permission model using role assignments on scopes'))
    lines.append(txt_row('PIM           = Privileged Identity Management; just-in-time privileged role activation'))
    lines.append(txt_row('VNet          = Azure Virtual Network; isolated network with subnets, NSGs, and route tables'))
    lines.append(txt_row('NSG           = Network Security Group; stateful firewall applied to subnets or individual NICs'))
    lines.append(txt_row('VMSS          = Virtual Machine Scale Set; auto-scaling pool of identical VMs'))
    lines.append(txt_row('AKS           = Azure Kubernetes Service; managed Kubernetes control plane and node pools'))
    lines.append(txt_row('Blob          = Azure Blob Storage; object store with hot, cool, and archive access tiers'))
    lines.append(txt_row('Managed Disks = Azure block volumes for VMs; Premium SSD, Standard SSD, and Ultra Disk'))
    lines.append(txt_row('ExpressRoute  = Dedicated private circuit from on-prem to Azure — bypasses public internet'))
    lines.append(txt_row('Virtual WAN   = Azure hub-and-spoke WAN; connects VNets, branches, and on-premises at scale'))
    lines.append(txt_row('Defender      = Microsoft Defender for Cloud; CSPM and workload protection for Azure resources'))
    lines.append(txt_row('Sentinel      = Azure cloud-native SIEM; ingests logs, correlates alerts, automates response'))
    lines.append(txt_row('Key Vault     = Azure managed secret store; stores keys, certificates, and connection strings'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'compute',
    'docs/compute/index.md',
    'Compute Platform Overview — Linux and Windows Server side by side',
)
def compute_platform_overview():
    """Compute Platform Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    LX_L, LX_R =  3, 50;  LX_MID = (LX_L + LX_R) // 2   # inner=46
    WS_L, WS_R = 53, 99;  WS_MID = (WS_L + WS_R) // 2   # inner=45
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'Compute Platform Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Compute Infrastructure')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Physical and virtual x86-64 servers running Linux and Windows Server workloads')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Remote access: SSH port 22 (Linux) · RDP port 3389 / WinRM 5985 (Windows)')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Out-of-band: Dell iDRAC · HP iLO · IPMI — independent of the host OS')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Automation: Bash/Python (Linux) · PowerShell/DSC (Windows) · Ansible across both')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Both platforms run on the same physical hardware — differentiated by OS and tooling'))
    lines.append(txt_row())
    lines.append(R(arrow([LX_MID, WS_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LX_L, LX_R), bTop(WS_L, WS_R))))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'Linux Server'),
        bMid(WS_L, WS_R, 'Windows Server'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'RHEL · Ubuntu · Debian · Rocky · Alpine'),
        bMid(WS_L, WS_R, 'Server 2019 · Server 2022 · Core mode'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'Kernel: modules, parameters, namespaces'),
        bMid(WS_L, WS_R, 'Hyper-V: built-in Type 1 hypervisor'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'systemd: service management and boot'),
        bMid(WS_L, WS_R, 'Active Directory Domain Services (AD DS)'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'LVM: flexible logical volume management'),
        bMid(WS_L, WS_R, 'NTFS · ReFS: file systems with ACLs'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'Package mgmt: dnf / apt / rpm / dpkg'),
        bMid(WS_L, WS_R, 'Group Policy (GPO): central config'),
    )))
    lines.append(R(merge(bBot(LX_L, LX_R), bBot(WS_L, WS_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Linux and Windows share hardware but differ in tooling, auth, and management patterns'))
    lines.append(txt_row())
    lines.append(R(arrow([LX_MID, WS_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LX_L, LX_R), bTop(WS_L, WS_R))))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'Linux Operations'),
        bMid(WS_L, WS_R, 'Windows Operations'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'SSH remote access and key management'),
        bMid(WS_L, WS_R, 'RDP and WinRM remote management'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'Performance: perf/sar/iostat/vmstat'),
        bMid(WS_L, WS_R, 'Performance Monitor · Get-Counter'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'Security: SELinux/AppArmor · auditd'),
        bMid(WS_L, WS_R, 'Defender AV · Audit Policies · LAPS'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'Logs: journalctl · rsyslog · logrotate'),
        bMid(WS_L, WS_R, 'Event Viewer: logs and diagnostics'),
    )))
    lines.append(R(merge(
        bMid(LX_L, LX_R, 'Automation: Bash/Python · cron jobs'),
        bMid(WS_L, WS_R, 'PowerShell automation · Task Scheduler'),
    )))
    lines.append(R(merge(bBot(LX_L, LX_R), bBot(WS_L, WS_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Day-to-day operations use platform-native tools and automation frameworks'))
    lines.append(txt_row())
    lines.append(R(arrow([LX_MID, WS_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['SSH', 'RDP', 'WinRM', 'iDRAC / BMC', 'SNMP / Syslog'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Linux remote', 'Windows remote', 'PS remoting', 'Out-of-band', 'Monitoring'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['TCP port 22', 'TCP port 3389', 'TCP 5985/86', 'IPMI / REST', 'UDP 161/162'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Key + cert auth', 'NLA + Kerberos', 'HTTP/S WS-Mgmt', 'DRAC web+CLI', 'MIB + traps'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['SCP · SFTP · rsync', 'mstsc.exe client', 'Invoke-Command', 'Lifecycle Ctrl', 'Nagios/OpenNMS'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 rack servers · NIC teaming · FC HBAs · iDRAC / iLO BMC · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('systemd      = Linux PID 1; manages service units, timers, mounts, and boot targets'))
    lines.append(txt_row('LVM          = Logical Volume Manager; PV → VG → LV abstraction for flexible disk layout'))
    lines.append(txt_row('SELinux      = Security-Enhanced Linux; mandatory access control via kernel labels'))
    lines.append(txt_row('AD DS        = Active Directory Domain Services; LDAP directory + Kerberos KDC for auth'))
    lines.append(txt_row('GPO          = Group Policy Object; settings pushed to computers and users via LDAP'))
    lines.append(txt_row('Hyper-V      = Windows built-in Type 1 hypervisor; supports checkpoints and live migration'))
    lines.append(txt_row('NTFS         = New Technology File System; ACLs, compression, encryption, and quotas'))
    lines.append(txt_row('WinRM        = Windows Remote Management; WS-Management for PowerShell PSRemoting'))
    lines.append(txt_row('iDRAC        = Dell Integrated Remote Access Controller; out-of-band BMC for server mgmt'))
    lines.append(txt_row('LAPS         = Local Admin Password Solution; rotates local admin passwords stored in AD'))
    lines.append(txt_row('auditd       = Linux audit daemon; logs syscall events for security compliance/forensics'))
    lines.append(txt_row('SNMP         = Simple Network Management Protocol; polls device metrics and receives traps'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'linux',
    'docs/compute/linux/index.md',
    'Linux Server Stack — architecture, networking, storage, ops, security, troubleshooting',
)
def linux_server_stack():
    """Linux Server Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    AR_L, AR_R =  3, 33;  AR_MID = (AR_L + AR_R) // 2
    NW_L, NW_R = 36, 66;  NW_MID = (NW_L + NW_R) // 2
    ST_L, ST_R = 69, 99;  ST_MID = (ST_L + ST_R) // 2
    OP_L, OP_R =  3, 33
    SC_L, SC_R = 36, 66
    TR_L, TR_R = 69, 99
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'Linux Server Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Linux Administration')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'SSH: remote access · systemctl: service management · journalctl: log inspection')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Package management: dnf (RHEL/Rocky) · apt (Ubuntu/Debian) · rpm / dpkg')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Performance: perf/sar/iostat/vmstat/top · tracing: strace / ltrace / eBPF')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Automation: Bash scripting · Python · Ansible: idempotent configuration management')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Administration tools span all subsystems from the kernel to application processes'))
    lines.append(txt_row())
    lines.append(R(arrow([AR_MID, NW_MID, ST_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(AR_L, AR_R), bTop(NW_L, NW_R), bTop(ST_L, ST_R))))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'Architecture'),
        bMid(NW_L, NW_R, 'Networking'),
        bMid(ST_L, ST_R, 'Storage'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'Linux kernel: monolithic'),
        bMid(NW_L, NW_R, 'ip/ss: iproute2 toolkit'),
        bMid(ST_L, ST_R, 'LVM: PV → VG → LV chain'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'Namespaces: isolation'),
        bMid(NW_L, NW_R, 'iptables/nftables: FW'),
        bMid(ST_L, ST_R, 'XFS · ext4 · Btrfs: FS'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'cgroups: resource limits'),
        bMid(NW_L, NW_R, 'NetworkManager/netplan'),
        bMid(ST_L, ST_R, 'NFS/CIFS: network mounts'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'systemd: PID 1, init'),
        bMid(NW_L, NW_R, 'NIC bonding: 802.3ad'),
        bMid(ST_L, ST_R, 'multipath: I/O failover'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'VFS: unified file layer'),
        bMid(NW_L, NW_R, 'DNS: resolv.conf+systemd'),
        bMid(ST_L, ST_R, 'RAID: md software RAID'),
    )))
    lines.append(R(merge(bBot(AR_L, AR_R), bBot(NW_L, NW_R), bBot(ST_L, ST_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Kernel subsystems provide isolation, networking, and storage to all processes'))
    lines.append(txt_row())
    lines.append(R(arrow([AR_MID, NW_MID, ST_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(OP_L, OP_R), bTop(SC_L, SC_R), bTop(TR_L, TR_R))))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'Operations'),
        bMid(SC_L, SC_R, 'Security'),
        bMid(TR_L, TR_R, 'Troubleshooting'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'cron/anacron: scheduling'),
        bMid(SC_L, SC_R, 'SELinux: MAC enforcement'),
        bMid(TR_L, TR_R, 'strace: syscall tracing'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'systemd timers: modern'),
        bMid(SC_L, SC_R, 'AppArmor: profile confinement'),
        bMid(TR_L, TR_R, 'tcpdump: packet capture'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'logrotate: log lifecycle'),
        bMid(SC_L, SC_R, 'sudo/PAM: privilege ctrl'),
        bMid(TR_L, TR_R, 'dmesg: kernel ring buffer'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'tuned: performance tuning'),
        bMid(SC_L, SC_R, 'auditd: syscall auditing'),
        bMid(TR_L, TR_R, 'lsof: open file/port map'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'ulimits: resource caps'),
        bMid(SC_L, SC_R, 'SSH: key auth + MFA'),
        bMid(TR_L, TR_R, 'perf: CPU profiling'),
    )))
    lines.append(R(merge(bBot(OP_L, OP_R), bBot(SC_L, SC_R), bBot(TR_L, TR_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Operations, security, and troubleshooting tools work at the OS and kernel level'))
    lines.append(txt_row())
    lines.append(R(arrow([AR_MID, NW_MID, ST_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['SSH', 'SFTP / SCP', 'NFS', 'SMB / CIFS', 'rsync'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Secure shell', 'File transfer', 'Unix FS mounts', 'Windows shares', 'Sync + backup'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['TCP port 22', 'SSH subsystem', 'TCP/UDP 2049', 'TCP 445', 'TCP 873'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['PubKey + TOTP', 'sftp/scp cmds', 'exports+fstab', 'smb.conf+fstab', 'rsync daemon'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['sshd_config', 'SFTP server', 'mount.nfs', 'mount.cifs', 'Incremental'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 servers · NIC teaming · FC/iSCSI HBAs · iDRAC/iLO BMC · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('systemd  = PID 1 init system; manages service units, timers, mounts, and boot targets'))
    lines.append(txt_row('SELinux  = Security-Enhanced Linux; mandatory access control using kernel labels'))
    lines.append(txt_row('LVM      = Logical Volume Manager; abstracts physical disks into flexible logical volumes'))
    lines.append(txt_row('iproute2 = Modern Linux networking toolkit; ip, ss, tc replace ifconfig and route'))
    lines.append(txt_row('iptables = Linux kernel packet-filter firewall; replaced by nftables in newer kernels'))
    lines.append(txt_row('NFS      = Network File System; mounts remote directories over IP using exports/fstab'))
    lines.append(txt_row('cgroups  = Control Groups; kernel feature that limits CPU, memory, and I/O per process'))
    lines.append(txt_row('strace   = System call tracer; shows every kernel call a process makes in real time'))
    lines.append(txt_row('auditd   = Linux audit daemon; logs syscall events for compliance and forensic analysis'))
    lines.append(txt_row('PAM      = Pluggable Authentication Modules; controls how logins and sudo authenticate'))
    lines.append(txt_row('tuned    = Linux performance daemon; applies OS profiles for different workload types'))
    lines.append(txt_row('multipath= Device mapper feature; aggregates HBA paths to a single block device'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'windows',
    'docs/compute/windows-server/index.md',
    'Windows Server Stack — architecture, networking, AD, ops, security, troubleshooting',
)
def windows_server_stack():
    """Windows Server Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    AR_L, AR_R =  3, 33;  AR_MID = (AR_L + AR_R) // 2
    NW_L, NW_R = 36, 66;  NW_MID = (NW_L + NW_R) // 2
    AD_L, AD_R = 69, 99;  AD_MID = (AD_L + AD_R) // 2
    OP_L, OP_R =  3, 33
    SC_L, SC_R = 36, 66
    TR_L, TR_R = 69, 99
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'Windows Server Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Windows Server Administration')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Server Manager · PowerShell · Windows Admin Center · Event Viewer · Task Scheduler')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Remote management: RDP (3389) · WinRM (5985/5986) · PowerShell PSRemoting')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Monitoring: Performance Monitor · Get-Counter · Resource Monitor · Defender')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Automation: PowerShell DSC · Scheduled Tasks · Group Policy · Ansible WinRM')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Administration tools span OS architecture, networking, and Active Directory'))
    lines.append(txt_row())
    lines.append(R(arrow([AR_MID, NW_MID, AD_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(AR_L, AR_R), bTop(NW_L, NW_R), bTop(AD_L, AD_R))))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'Architecture'),
        bMid(NW_L, NW_R, 'Networking'),
        bMid(AD_L, AD_R, 'Active Directory'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'Server 2019 / 2022'),
        bMid(NW_L, NW_R, 'DNS Server: zone mgmt'),
        bMid(AD_L, AD_R, 'AD DS: domain services'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'NTFS · ReFS filesystems'),
        bMid(NW_L, NW_R, 'DHCP Server: IP leasing'),
        bMid(AD_L, AD_R, 'Group Policy (GPO)'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'Registry: config database'),
        bMid(NW_L, NW_R, 'NIC Teaming: LACP bonds'),
        bMid(AD_L, AD_R, 'Kerberos: auth tickets'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'Services: Win32 daemons'),
        bMid(NW_L, NW_R, 'Windows Firewall + WDF'),
        bMid(AD_L, AD_R, 'LDAP: directory queries'),
    )))
    lines.append(R(merge(
        bMid(AR_L, AR_R, 'Hyper-V: Type 1 hypervisor'),
        bMid(NW_L, NW_R, 'DFS-N: namespace sharing'),
        bMid(AD_L, AD_R, 'Trusts: cross-domain auth'),
    )))
    lines.append(R(merge(bBot(AR_L, AR_R), bBot(NW_L, NW_R), bBot(AD_L, AD_R))))

    lines.append(txt_row())
    lines.append(txt_row('  OS architecture, networking, and Active Directory form the Windows platform foundation'))
    lines.append(txt_row())
    lines.append(R(arrow([AR_MID, NW_MID, AD_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(OP_L, OP_R), bTop(SC_L, SC_R), bTop(TR_L, TR_R))))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'Operations'),
        bMid(SC_L, SC_R, 'Security'),
        bMid(TR_L, TR_R, 'Troubleshooting'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'WSUS: patch management'),
        bMid(SC_L, SC_R, 'BitLocker: drive encrypt'),
        bMid(TR_L, TR_R, 'Event Viewer: logs+alerts'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'WinRM: remote execution'),
        bMid(SC_L, SC_R, 'Defender AV + EDR'),
        bMid(TR_L, TR_R, 'SFC / DISM: system repair'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'IIS: web server mgmt'),
        bMid(SC_L, SC_R, 'JEA: Just Enough Admin'),
        bMid(TR_L, TR_R, 'WinPE: recovery env.'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'Volume Shadow Copies'),
        bMid(SC_L, SC_R, 'Audit Policy: event log'),
        bMid(TR_L, TR_R, 'Process Monitor/Explorer'),
    )))
    lines.append(R(merge(
        bMid(OP_L, OP_R, 'FSRM: quota+screening'),
        bMid(SC_L, SC_R, 'LAPS: local admin pwds'),
        bMid(TR_L, TR_R, 'WMI/CIM: system queries'),
    )))
    lines.append(R(merge(bBot(OP_L, OP_R), bBot(SC_L, SC_R), bBot(TR_L, TR_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Operations, security hardening, and diagnostic tools work across all Windows roles'))
    lines.append(txt_row())
    lines.append(R(arrow([AR_MID, NW_MID, AD_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['RDP', 'SMB', 'WinRM', 'Kerberos', 'LDAP / LDAPS'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Remote desktop', 'File sharing', 'PS remoting', 'Authentication', 'Directory'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['TCP 3389', 'TCP 445', 'TCP 5985/86', 'TCP 88/UDP', 'TCP 389/636'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['NLA · TLS 1.2', 'NTLM/Kerberos', 'HTTP · HTTPS', 'KDC ticket srv', 'SSL+SASL bind'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['mstsc.exe', 'net use / UNC', 'Invoke-Command', 'Ticket + PAC', 'ADSI/RSAT tools'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86-64 rack servers · NIC teaming · iDRAC/iLO BMC · Windows licensing · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('AD DS    = Active Directory Domain Services; LDAP directory + Kerberos KDC for Windows auth'))
    lines.append(txt_row('GPO      = Group Policy Object; settings pushed to computers and users via LDAP queries'))
    lines.append(txt_row('WinRM    = Windows Remote Management; WS-Management for PowerShell PSRemoting'))
    lines.append(txt_row('Kerberos = Ticket-based authentication protocol; default for all AD domain accounts'))
    lines.append(txt_row('NTFS     = New Technology File System; supports ACLs, compression, and EFS encryption'))
    lines.append(txt_row('Hyper-V  = Windows Type 1 hypervisor; VM checkpoints and live migration built in'))
    lines.append(txt_row('BitLocker= Full-volume encryption using AES; TPM-backed key storage for boot protection'))
    lines.append(txt_row('LAPS     = Local Admin Password Solution; rotates local admin passwords stored in AD'))
    lines.append(txt_row('JEA      = Just Enough Administration; limits PS remoting to specific command sets'))
    lines.append(txt_row('WSUS     = Windows Server Update Services; internal patch distribution server'))
    lines.append(txt_row('SFC      = System File Checker; scans and repairs corrupt Windows system files'))
    lines.append(txt_row('DISM     = Deployment Image Servicing; manages Windows images and component packages'))
    lines.append(txt_row('DFS-N    = Distributed File System Namespace; virtual UNC namespace across share paths'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'san',
    'docs/san/index.md',
    'SAN Fabric Overview — Cisco MDS and Brocade FC fabric side by side',
)
def san_fabric_overview():
    """SAN Fabric Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    CI_L, CI_R =  3, 50;  CI_MID = (CI_L + CI_R) // 2   # inner=46
    BR_L, BR_R = 53, 99;  BR_MID = (BR_L + BR_R) // 2   # inner=45
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'SAN Fabric Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'SAN Fabric Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Cisco: DCNM / Nexus Dashboard · CLI · NX-OS REST API · SNMP · Syslog')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Brocade: SANnav Portal · Fabric OS CLI · REST API · SNMP trap forwarding')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Both vendors: fabric-wide zoning, ISL monitoring, and performance dashboards')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'REST APIs enable programmable fabric automation and health integration')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Management platforms provide fabric-wide visibility, zoning, and lifecycle control'))
    lines.append(txt_row())
    lines.append(R(arrow([CI_MID, BR_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(CI_L, CI_R), bTop(BR_L, BR_R))))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'Cisco MDS (SAN-OS / NX-OS)'),
        bMid(BR_L, BR_R, 'Brocade (Fabric OS)'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'MDS 9000: 16/32/64G FC switches'),
        bMid(BR_L, BR_R, 'Gen 7: 64G FC switching'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'VSANs: virtual fabric isolation'),
        bMid(BR_L, BR_R, 'Zone aliases + zone configs'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'Smart Zoning + device aliases'),
        bMid(BR_L, BR_R, 'ISL trunking + Port Channels'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'IVR: inter-VSAN routing'),
        bMid(BR_L, BR_R, 'QoS: priority FC traffic'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'DCNM / Nexus Dashboard mgmt'),
        bMid(BR_L, BR_R, 'SANnav: fabric management'),
    )))
    lines.append(R(merge(bBot(CI_L, CI_R), bBot(BR_L, BR_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Both vendors deliver 16/32/64G Fibre Channel with zoning and trunked ISLs'))
    lines.append(txt_row())
    lines.append(R(arrow([CI_MID, BR_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(CI_L, CI_R), bTop(BR_L, BR_R))))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'Cisco Fabric Services'),
        bMid(BR_L, BR_R, 'Brocade Fabric Services'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'FLOGI: host login to fabric'),
        bMid(BR_L, BR_R, 'FLOGI DB: registered ports'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'FSPF: fabric shortest path'),
        bMid(BR_L, BR_R, 'D-Port: diagnostics port'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'CFS: config fabric sync'),
        bMid(BR_L, BR_R, 'MAPS: monitoring alerts'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'FCNS: fabric name service'),
        bMid(BR_L, BR_R, 'Buffer Credits: flow ctrl'),
    )))
    lines.append(R(merge(
        bMid(CI_L, CI_R, 'Port modes: F · E · TE · NP'),
        bMid(BR_L, BR_R, 'E-Port: ISL · F-Port: host'),
    )))
    lines.append(R(merge(bBot(CI_L, CI_R), bBot(BR_L, BR_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Fabric protocol services register initiators and targets for SCSI data exchange'))
    lines.append(txt_row())
    lines.append(R(arrow([CI_MID, BR_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['FLOGI', 'FDISC', 'Zoning', 'FSPF', 'ISL / Trunk'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['N_Port login', 'NPIV port', 'Access control', 'Link routing', 'E-port links'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['WWPN register', 'Virtual WWPN', 'pWWN / alias', 'Shortest path', 'TE/trunk port'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['FC-ID assign', 'HBA multiplex', 'Hard or soft', 'ECMP spread', 'Load balance'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['FCNS register', 'VF_Port serve', 'Zone database', 'Path failover', 'BB credits'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('FC switches · 16G/32G/64G SFPs · OM4 fibre · FC HBAs in hosts · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('FC       = Fibre Channel; dedicated high-speed block network using optical or copper links'))
    lines.append(txt_row('WWPN     = World Wide Port Name; globally unique 64-bit identifier for each FC HBA port'))
    lines.append(txt_row('WWNN     = World Wide Node Name; 64-bit identifier for the HBA device (node) itself'))
    lines.append(txt_row('FLOGI    = Fabric Login; N-Port registers its WWPN with the fabric to get an FC-ID'))
    lines.append(txt_row('FSPF     = Fabric Shortest Path First; link-state routing protocol for FC fabric paths'))
    lines.append(txt_row('Zoning   = Fabric access control; limits which initiators can communicate with targets'))
    lines.append(txt_row('VSAN     = Virtual SAN (Cisco); logical fabric partition within a shared physical switch'))
    lines.append(txt_row('ISL      = Inter-Switch Link; E-Port or TE-Port carrying aggregated fabric traffic'))
    lines.append(txt_row('NPIV     = N-Port ID Virtualisation; one HBA presents multiple virtual WWPNs'))
    lines.append(txt_row('D-Port   = Diagnostic Port; Brocade link mode for BER and latency testing'))
    lines.append(txt_row('MAPS     = Monitoring and Alerting Policy Suite; Brocade threshold-based SAN alerts'))
    lines.append(txt_row('IVR      = Inter-VSAN Routing; Cisco controlled traffic flow between VSANs'))
    lines.append(txt_row('SANnav   = Brocade SAN management portal; replaced BSNA with modern REST-based UI'))
    lines.append(txt_row('DCNM     = Data Center Network Manager; Cisco fabric management (now Nexus Dashboard)'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'cisco-san',
    'docs/san/cisco/index.md',
    'Cisco SAN Stack — MDS 9000, DCNM, Nexus Dashboard, VSAN, Zoning, ISL',
)
def cisco_san_stack():
    """Cisco SAN Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    MD_L, MD_R =  3, 33;  MD_MID = (MD_L + MD_R) // 2
    DC_L, DC_R = 36, 66;  DC_MID = (DC_L + DC_R) // 2
    ND_L, ND_R = 69, 99;  ND_MID = (ND_L + ND_R) // 2
    VS_L, VS_R =  3, 33
    ZN_L, ZN_R = 36, 66
    IS_L, IS_R = 69, 99
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'Cisco SAN Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Cisco SAN Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'DCNM / Nexus Dashboard: GUI fabric management, zoning workflows, and telemetry')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'NX-OS / SAN-OS CLI: config t · show flogi database · show zone status')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'SNMP v3 · Syslog: event collection and forwarding to monitoring platforms')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'REST API: programmable fabric config, metrics, and zoning via HTTPS/JSON')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Management tools span hardware switches, legacy DCNM, and modern Nexus Dashboard'))
    lines.append(txt_row())
    lines.append(R(arrow([MD_MID, DC_MID, ND_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(MD_L, MD_R), bTop(DC_L, DC_R), bTop(ND_L, ND_R))))
    lines.append(R(merge(
        bMid(MD_L, MD_R, 'Cisco MDS 9000'),
        bMid(DC_L, DC_R, 'DCNM'),
        bMid(ND_L, ND_R, 'Nexus Dashboard (ND)'),
    )))
    lines.append(R(merge(
        bMid(MD_L, MD_R, '9132T: 32-port 32G FC'),
        bMid(DC_L, DC_R, 'Data Center Ntwk Mgr'),
        bMid(ND_L, ND_R, 'Successor to DCNM'),
    )))
    lines.append(R(merge(
        bMid(MD_L, MD_R, '9396T: 96-port 32G FC'),
        bMid(DC_L, DC_R, 'Fabric discovery+sync'),
        bMid(ND_L, ND_R, 'Fabric Controller (NDF)'),
    )))
    lines.append(R(merge(
        bMid(MD_L, MD_R, '9700: modular director'),
        bMid(DC_L, DC_R, 'Zoning: templates+push'),
        bMid(ND_L, ND_R, 'Fabric Insights (NDI)'),
    )))
    lines.append(R(merge(
        bMid(MD_L, MD_R, 'Line cards: 16/32/64G'),
        bMid(DC_L, DC_R, 'Performance monitoring'),
        bMid(ND_L, ND_R, 'Multi-site management'),
    )))
    lines.append(R(merge(
        bMid(MD_L, MD_R, 'SAN-OS → NX-OS upgrade'),
        bMid(DC_L, DC_R, 'Health: port + fabric'),
        bMid(ND_L, ND_R, 'Flow telemetry + VXLAN'),
    )))
    lines.append(R(merge(bBot(MD_L, MD_R), bBot(DC_L, DC_R), bBot(ND_L, ND_R))))

    lines.append(txt_row())
    lines.append(txt_row('  MDS hardware, DCNM (legacy), and Nexus Dashboard (current) form the Cisco SAN stack'))
    lines.append(txt_row())
    lines.append(R(arrow([MD_MID, DC_MID, ND_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(VS_L, VS_R), bTop(ZN_L, ZN_R), bTop(IS_L, IS_R))))
    lines.append(R(merge(
        bMid(VS_L, VS_R, 'VSANs'),
        bMid(ZN_L, ZN_R, 'Zoning'),
        bMid(IS_L, IS_R, 'ISL & Trunking'),
    )))
    lines.append(R(merge(
        bMid(VS_L, VS_R, 'Virtual fabric partition'),
        bMid(ZN_L, ZN_R, 'Device aliases: names'),
        bMid(IS_L, IS_R, 'E-Port: standard ISL'),
    )))
    lines.append(R(merge(
        bMid(VS_L, VS_R, 'VSAN membership: port'),
        bMid(ZN_L, ZN_R, 'pWWN or FC ID members'),
        bMid(IS_L, IS_R, 'TE-Port: trunked ISL'),
    )))
    lines.append(R(merge(
        bMid(VS_L, VS_R, 'Domain IDs: 1–239'),
        bMid(ZN_L, ZN_R, 'Smart Zoning: auto-bind'),
        bMid(IS_L, IS_R, 'Port channels: LACP'),
    )))
    lines.append(R(merge(
        bMid(VS_L, VS_R, 'IVR: inter-VSAN route'),
        bMid(ZN_L, ZN_R, 'Enhanced zoning: atomic'),
        bMid(IS_L, IS_R, 'FSPF: load balancing'),
    )))
    lines.append(R(merge(
        bMid(VS_L, VS_R, 'VSAN DB sync via CFS'),
        bMid(ZN_L, ZN_R, 'Zone sets: named policy'),
        bMid(IS_L, IS_R, 'F-Port channels: NPV'),
    )))
    lines.append(R(merge(bBot(VS_L, VS_R), bBot(ZN_L, ZN_R), bBot(IS_L, IS_R))))

    lines.append(txt_row())
    lines.append(txt_row('  VSANs isolate traffic · Zoning controls access · ISL trunks carry aggregated load'))
    lines.append(txt_row())
    lines.append(R(arrow([MD_MID, DC_MID, ND_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['FLOGI', 'FDISC', 'FC-NS', 'RSCN', 'CFS'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['N_Port login', 'NPIV port', 'Name service', 'Change notice', 'Fabric sync'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['WWPN + WWNN', 'Virtual ports', 'FCid database', 'Topology chg', 'Atomic apply'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['FC-ID: 24-bit', 'HBA multiplex', 'PLOGI follows', 'Zone trigger', 'CFS lock'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['FCNS register', 'VF_Port serve', 'show flogi db', 'RSCN payload', 'Full fabric'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('MDS 9000 switches · 16G/32G/64G FC SFPs · OM4 fibre · FC HBAs · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('MDS     = Cisco Multilayer Director Switch; purpose-built FC SAN switches'))
    lines.append(txt_row('NX-OS   = Network OS used on Cisco MDS after SAN-OS; shared CLI with Nexus'))
    lines.append(txt_row('SAN-OS  = Original Cisco MDS OS; succeeded by NX-OS for unified CLI'))
    lines.append(txt_row('VSAN    = Virtual SAN; Cisco method of partitioning one fabric into isolated SANs'))
    lines.append(txt_row('IVR     = Inter-VSAN Routing; allows controlled traffic exchange between VSANs'))
    lines.append(txt_row('DCNM    = Data Center Network Manager; Cisco GUI for MDS zoning and monitoring'))
    lines.append(txt_row('ND      = Nexus Dashboard; successor to DCNM; unified multi-fabric management'))
    lines.append(txt_row('Smart Zoning= Inserts exact FC IDs into zone members; reduces unnecessary RSCN storms'))
    lines.append(txt_row('Device Alias= Fabric-wide friendly name for a WWN; simplifies zone configuration'))
    lines.append(txt_row('CFS     = Cisco Fabric Services; distributes and synchronises config across MDS peers'))
    lines.append(txt_row('RSCN    = Registered State Change Notification; alerts hosts of topology changes'))
    lines.append(txt_row('TE-Port = Trunked E-Port; carries multiple VSANs over one physical ISL link'))
    lines.append(txt_row('NPV     = N-Port Virtualiser; MDS edge mode that proxies logins to a core switch'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'brocade',
    'docs/san/brocade/index.md',
    'Brocade SAN Stack — Fabric OS, SANnav, Zoning, ISL, MAPS, D-Port',
)
def brocade_san_stack():
    """Brocade SAN Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    FO_L, FO_R =  3, 50;  FO_MID = (FO_L + FO_R) // 2   # inner=46
    SN_L, SN_R = 53, 99;  SN_MID = (SN_L + SN_R) // 2   # inner=45
    ZN_L, ZN_R =  3, 50
    IL_L, IL_R = 53, 99
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'Brocade SAN Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Brocade SAN Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'SANnav Management Portal: web UI for fabric discovery, zoning, and performance')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Fabric OS CLI: switchshow · cfgshow · zoneshow · supportshow · portcfgshow')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'REST API: HTTPS-based access to FOS config and monitoring data')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'SNMP v3 · Syslog: polling and trap forwarding to SIEM and monitoring tools')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  SANnav and the FOS CLI are the two primary management surfaces for Brocade fabrics'))
    lines.append(txt_row())
    lines.append(R(arrow([FO_MID, SN_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(FO_L, FO_R), bTop(SN_L, SN_R))))
    lines.append(R(merge(
        bMid(FO_L, FO_R, 'Fabric OS (FOS)'),
        bMid(SN_L, SN_R, 'SANnav Management Portal'),
    )))
    lines.append(R(merge(
        bMid(FO_L, FO_R, 'Distributed OS across all ports'),
        bMid(SN_L, SN_R, 'Fabric discovery + inventory'),
    )))
    lines.append(R(merge(
        bMid(FO_L, FO_R, 'Zone management: cfgshow/cfgsave'),
        bMid(SN_L, SN_R, 'Health dashboard + alerts'),
    )))
    lines.append(R(merge(
        bMid(FO_L, FO_R, 'ISL trunking: trunk groups'),
        bMid(SN_L, SN_R, 'Zoning: drag-and-drop UI'),
    )))
    lines.append(R(merge(
        bMid(FO_L, FO_R, 'Port types: E / F / G / D / L'),
        bMid(SN_L, SN_R, 'Performance analytics: IOPS'),
    )))
    lines.append(R(merge(
        bMid(FO_L, FO_R, 'MAPS: threshold-based alerts'),
        bMid(SN_L, SN_R, 'Replaces older BSNA / DCFM'),
    )))
    lines.append(R(merge(bBot(FO_L, FO_R), bBot(SN_L, SN_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Fabric OS runs on the switch; SANnav is the management application layer'))
    lines.append(txt_row())
    lines.append(R(arrow([FO_MID, SN_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(ZN_L, ZN_R), bTop(IL_L, IL_R))))
    lines.append(R(merge(
        bMid(ZN_L, ZN_R, 'Zoning & Security'),
        bMid(IL_L, IL_R, 'ISL & Performance'),
    )))
    lines.append(R(merge(
        bMid(ZN_L, ZN_R, 'Zone aliases: pWWN names'),
        bMid(IL_L, IL_R, 'Trunk groups: 8 ports max'),
    )))
    lines.append(R(merge(
        bMid(ZN_L, ZN_R, 'Zone configs: named sets'),
        bMid(IL_L, IL_R, 'Buffer credits: flow ctrl'),
    )))
    lines.append(R(merge(
        bMid(ZN_L, ZN_R, 'Open / enforce / strict modes'),
        bMid(IL_L, IL_R, 'QoS: high/medium/low lanes'),
    )))
    lines.append(R(merge(
        bMid(ZN_L, ZN_R, 'DCC: device connection ctrl'),
        bMid(IL_L, IL_R, 'D-Port: link diagnostics'),
    )))
    lines.append(R(merge(
        bMid(ZN_L, ZN_R, 'SCC: switch connection ctrl'),
        bMid(IL_L, IL_R, 'Access Gateway: edge mode'),
    )))
    lines.append(R(merge(bBot(ZN_L, ZN_R), bBot(IL_L, IL_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Zoning enforces access control · ISL trunks aggregate bandwidth between switches'))
    lines.append(txt_row())
    lines.append(R(arrow([FO_MID, SN_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['FLOGI DB', 'Zoning', 'ISL Trunk', 'MAPS', 'D-Port'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Login register', 'Zone alias', 'Trunk groups', 'Alert policy', 'Link test'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['WWN + FC-ID', 'cfgshow/save', 'trunkshow', 'mapsshow', 'portdiag'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['nsshow cmd', 'cfgenable', 'Port Channel', 'Threshold rules', 'BER testing'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['fabricshow', 'zonecreate', 'Load balance', 'Health scoring', 'Eye margins'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Brocade FC switches · 16G/32G/64G SFPs · OM4 fibre · FC HBAs · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('FOS       = Fabric OS; Brocade switch OS distributed across all ports in the switch'))
    lines.append(txt_row('SANnav    = Brocade SAN management portal; replaced BSNA/DCFM with modern REST UI'))
    lines.append(txt_row('MAPS      = Monitoring and Alerting Policy Suite; threshold engine for SAN health'))
    lines.append(txt_row('D-Port    = Diagnostic Port; Brocade link mode for BER and optical latency testing'))
    lines.append(txt_row('Trunk Group= Bundle of ISL ports acting as one logical link for load balancing'))
    lines.append(txt_row('Buffer Credits= FC flow control; limits in-flight frames per port to prevent overflow'))
    lines.append(txt_row('Zone Alias= Named reference to a pWWN; simplifies zone member configuration'))
    lines.append(txt_row('Zone Config= Named collection of zones saved and activated as a policy on the fabric'))
    lines.append(txt_row('cfgshow   = FOS command to display zone config; cfgsave persists to flash'))
    lines.append(txt_row('DCC       = Device Connection Control; restricts ports a WWN may connect to'))
    lines.append(txt_row('SCC       = Switch Connection Control; restricts which switches may join via ISL'))
    lines.append(txt_row('Access Gateway= Brocade edge mode; connects to core switch as an N-Port proxy'))
    lines.append(txt_row('supportshow= FOS diagnostic command; captures full switch state for support cases'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vxrail',
    'docs/virtualization/vxrail/index.md',
    'VxRail Platform Stack — compute, networking, vSAN, LCM, ops, integration',
)
def vxrail_platform_stack():
    """VxRail Platform Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    CO_L, CO_R =  3, 33;  CO_MID = (CO_L + CO_R) // 2
    NW_L, NW_R = 36, 66;  NW_MID = (NW_L + NW_R) // 2
    ST_L, ST_R = 69, 99;  ST_MID = (ST_L + ST_R) // 2
    LC_L, LC_R =  3, 33
    OP_L, OP_R = 36, 66
    IN_L, IN_R = 69, 99
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'VxRail Platform Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'VxRail Platform Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'VxRail Manager: node health, cluster expansion, and LCM upgrade orchestration')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'vCenter: VM and cluster management; integrated with VxRail for lifecycle events')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Dell SupportAssist: automated diagnostics and proactive support case creation')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'CloudIQ: cloud analytics for capacity forecasting and health scoring')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  VxRail Manager coordinates all cluster operations alongside vCenter'))
    lines.append(txt_row())
    lines.append(R(arrow([CO_MID, NW_MID, ST_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(CO_L, CO_R), bTop(NW_L, NW_R), bTop(ST_L, ST_R))))
    lines.append(R(merge(
        bMid(CO_L, CO_R, 'Compute (Nodes)'),
        bMid(NW_L, NW_R, 'Networking'),
        bMid(ST_L, ST_R, 'Storage (vSAN)'),
    )))
    lines.append(R(merge(
        bMid(CO_L, CO_R, 'P/E/S/V node families'),
        bMid(NW_L, NW_R, 'vSAN: dedicated VMkernel'),
        bMid(ST_L, ST_R, 'vSAN HCI datastore'),
    )))
    lines.append(R(merge(
        bMid(CO_L, CO_R, 'Intel Xeon CPUs'),
        bMid(NW_L, NW_R, 'Management VMkernel'),
        bMid(ST_L, ST_R, 'Disk groups: cache+cap'),
    )))
    lines.append(R(merge(
        bMid(CO_L, CO_R, 'iDRAC: BMC management'),
        bMid(NW_L, NW_R, 'vMotion: live migration'),
        bMid(ST_L, ST_R, 'Erasure coding: FTT=1/2'),
    )))
    lines.append(R(merge(
        bMid(CO_L, CO_R, 'BIOS + firmware lifecycle'),
        bMid(NW_L, NW_R, 'NSX-T: overlay network'),
        bMid(ST_L, ST_R, 'Dedup + compression'),
    )))
    lines.append(R(merge(
        bMid(CO_L, CO_R, 'NVMe/SSD/HDD tiers'),
        bMid(NW_L, NW_R, '10/25/100 GbE uplinks'),
        bMid(ST_L, ST_R, 'Stretched cluster opt.'),
    )))
    lines.append(R(merge(bBot(CO_L, CO_R), bBot(NW_L, NW_R), bBot(ST_L, ST_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Compute, networking, and storage are pre-validated on Dell HCI node hardware'))
    lines.append(txt_row())
    lines.append(R(arrow([CO_MID, NW_MID, ST_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LC_L, LC_R), bTop(OP_L, OP_R), bTop(IN_L, IN_R))))
    lines.append(R(merge(
        bMid(LC_L, LC_R, 'Lifecycle (LCM)'),
        bMid(OP_L, OP_R, 'Operations'),
        bMid(IN_L, IN_R, 'Integration'),
    )))
    lines.append(R(merge(
        bMid(LC_L, LC_R, 'VxRail-specific bundles'),
        bMid(OP_L, OP_R, 'Health: VxRail Manager'),
        bMid(IN_L, IN_R, 'VCF: SDDC Manager mgd'),
    )))
    lines.append(R(merge(
        bMid(LC_L, LC_R, 'HCL: compat. validation'),
        bMid(OP_L, OP_R, 'vSAN health service UI'),
        bMid(IN_L, IN_R, 'NSX-T: overlay+micro-seg'),
    )))
    lines.append(R(merge(
        bMid(LC_L, LC_R, 'Non-disruptive upgrades'),
        bMid(OP_L, OP_R, 'SupportAssist: log bundle'),
        bMid(IN_L, IN_R, 'Tanzu: K8s on VxRail'),
    )))
    lines.append(R(merge(
        bMid(LC_L, LC_R, 'Rolling: node by node'),
        bMid(OP_L, OP_R, 'Syslog + SNMP alerting'),
        bMid(IN_L, IN_R, 'Dell APEX: as-a-service'),
    )))
    lines.append(R(merge(
        bMid(LC_L, LC_R, 'VC + VxRail compat. lock'),
        bMid(OP_L, OP_R, 'Performance: vCenter UI'),
        bMid(IN_L, IN_R, 'SRM: DR for VxRail'),
    )))
    lines.append(R(merge(bBot(LC_L, LC_R), bBot(OP_L, OP_R), bBot(IN_L, IN_R))))

    lines.append(txt_row())
    lines.append(txt_row('  LCM, operational tooling, and integrations complete the VxRail platform picture'))
    lines.append(txt_row())
    lines.append(R(arrow([CO_MID, NW_MID, ST_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['vSAN', 'vMotion', 'Management', 'iDRAC / BMC', 'NSX-T'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['HCI datastore', 'VM live migrate', 'Host/VM admin', 'Out-of-band', 'Overlay nets'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['iSCSI / RDMA', 'TCP dedicated', 'HTTPS / SOAP', 'IPMI + REST', 'Geneve/VXLAN'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Witness VM', 'Encryption opt.', 'vCenter API', 'iDRAC web UI', 'Micro-seg FW'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['FTT policy', 'DRS-managed', 'Syslog fwd.', 'Lifecycle Ctrl', 'T-bit tagging'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('VxRail nodes · 10/25/100 GbE ToR switches · iDRAC BMC · Optional FC HBAs · Power'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VxRail  = Dell HCI appliance; vSphere + vSAN pre-validated on Dell hardware nodes'))
    lines.append(txt_row('LCM     = Lifecycle Manager; VMware/VxRail upgrade engine for rolling cluster upgrades'))
    lines.append(txt_row('HCL     = Hardware Compatibility List; VMware list of validated vSAN hardware'))
    lines.append(txt_row('iDRAC   = Integrated Dell Remote Access Controller; out-of-band BMC for servers'))
    lines.append(txt_row('vSAN    = VMware hyperconverged storage; NVMe/SSD pools shared across cluster nodes'))
    lines.append(txt_row('FTT     = Failures to Tolerate; vSAN policy for data redundancy (FTT=1: 1 failure)'))
    lines.append(txt_row('Disk Group= vSAN unit: one NVMe/SSD cache device with 1-7 capacity devices per node'))
    lines.append(txt_row('Erasure Coding= RAID-5/6 over vSAN; more efficient than mirroring for FTT=1/2'))
    lines.append(txt_row('VCF     = VMware Cloud Foundation; full SDDC stack managed by SDDC Manager'))
    lines.append(txt_row('NSX-T   = VMware NSX; software-defined networking with distributed FW and LB'))
    lines.append(txt_row('SupportAssist= Dell automated diagnostics; sends logs to support on trigger'))
    lines.append(txt_row('CloudIQ = Dell cloud analytics SaaS; VxRail health, capacity, and performance'))
    lines.append(txt_row('SRM     = Site Recovery Manager; orchestrated DR failover for vSphere workloads'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vmware-ops',
    'docs/virtualization/operations/index.md',
    'VMware Operations Overview — health checks, troubleshooting, runbooks, automation',
)
def vmware_operations_overview():
    """VMware Operations Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    HC_L, HC_R =  3, 33;  HC_MID = (HC_L + HC_R) // 2
    TS_L, TS_R = 36, 66;  TS_MID = (TS_L + TS_R) // 2
    RB_L, RB_R = 69, 99;  RB_MID = (RB_L + RB_R) // 2
    MO_L, MO_R =  3, 33
    MA_L, MA_R = 36, 66
    AU_L, AU_R = 69, 99
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'VMware Operations Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'VMware Platform Operations')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'vCenter: cluster, host, and VM management · Aria Operations: performance dashboards')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Log Insight / Aria Log Intelligence: log aggregation, search, and correlation')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'CLI: esxcli (host ops) · govc (scripted vCenter tasks) · PowerCLI (automation)')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'vROps capacity analytics: right-sizing, trend forecasting, workload placement')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Management tools cover health monitoring, troubleshooting, and runbook execution'))
    lines.append(txt_row())
    lines.append(R(arrow([HC_MID, TS_MID, RB_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(HC_L, HC_R), bTop(TS_L, TS_R), bTop(RB_L, RB_R))))
    lines.append(R(merge(
        bMid(HC_L, HC_R, 'Health Checks'),
        bMid(TS_L, TS_R, 'Troubleshooting'),
        bMid(RB_L, RB_R, 'Runbooks'),
    )))
    lines.append(R(merge(
        bMid(HC_L, HC_R, 'Cluster capacity headroom'),
        bMid(TS_L, TS_R, 'VM boot failures: logs'),
        bMid(RB_L, RB_R, 'Host maintenance mode'),
    )))
    lines.append(R(merge(
        bMid(HC_L, HC_R, 'vSAN health service check'),
        bMid(TS_L, TS_R, 'Network: vmkping/traffic'),
        bMid(RB_L, RB_R, 'Rolling patch procedure'),
    )))
    lines.append(R(merge(
        bMid(HC_L, HC_R, 'Host connectivity: vCenter'),
        bMid(TS_L, TS_R, 'Storage latency: esxtop'),
        bMid(RB_L, RB_R, 'VM snapshot management'),
    )))
    lines.append(R(merge(
        bMid(HC_L, HC_R, 'Alarm: red/yellow review'),
        bMid(TS_L, TS_R, 'ESXi PSOD: vmkernel dump'),
        bMid(RB_L, RB_R, 'Cert renewal workflow'),
    )))
    lines.append(R(merge(
        bMid(HC_L, HC_R, 'Cert expiry + NTP drift'),
        bMid(TS_L, TS_R, 'HA/DRS: config + events'),
        bMid(RB_L, RB_R, 'VDS port group changes'),
    )))
    lines.append(R(merge(bBot(HC_L, HC_R), bBot(TS_L, TS_R), bBot(RB_L, RB_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Health checks prevent outages · troubleshooting resolves them · runbooks standardise ops'))
    lines.append(txt_row())
    lines.append(R(arrow([HC_MID, TS_MID, RB_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(MO_L, MO_R), bTop(MA_L, MA_R), bTop(AU_L, AU_R))))
    lines.append(R(merge(
        bMid(MO_L, MO_R, 'Monitoring'),
        bMid(MA_L, MA_R, 'Maintenance'),
        bMid(AU_L, AU_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(MO_L, MO_R, 'vCenter performance charts'),
        bMid(MA_L, MA_R, 'Maintenance mode evac'),
        bMid(AU_L, AU_R, 'PowerCLI: Connect-VIServer'),
    )))
    lines.append(R(merge(
        bMid(MO_L, MO_R, 'Aria dashboards: vROps'),
        bMid(MA_L, MA_R, 'VUM/LCM: upgrade baseline'),
        bMid(AU_L, AU_R, 'govc: fast CLI operations'),
    )))
    lines.append(R(merge(
        bMid(MO_L, MO_R, 'SNMP traps → monitoring'),
        bMid(MA_L, MA_R, 'Cluster remediation order'),
        bMid(AU_L, AU_R, 'vCenter REST API: HTTPS'),
    )))
    lines.append(R(merge(
        bMid(MO_L, MO_R, 'Log alerts: query+notify'),
        bMid(MA_L, MA_R, 'HA admission control adj'),
        bMid(AU_L, AU_R, 'Event triggers: DRS/HA'),
    )))
    lines.append(R(merge(
        bMid(MO_L, MO_R, 'Capacity: forecast/resize'),
        bMid(MA_L, MA_R, 'DRS migration threshold'),
        bMid(AU_L, AU_R, 'Scheduled tasks: recur'),
    )))
    lines.append(R(merge(bBot(MO_L, MO_R), bBot(MA_L, MA_R), bBot(AU_L, AU_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Monitoring feeds maintenance decisions · automation scales operational repeatability'))
    lines.append(txt_row())
    lines.append(R(arrow([HC_MID, TS_MID, RB_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['esxcli', 'govc', 'PowerCLI', 'REST API', 'SSH'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['ESXi host ops', 'vCenter tasks', 'vSphere module', 'HTTPS JSON', 'Direct host'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Namespace cmds', 'VMOMI client', 'Cmdlet syntax', 'OAuth2 bearer', 'Port 22'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['esxcli --help', 'env GOVC_URL', 'Import-Module', 'Postman / curl', 'Auth key'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['sw/network/vm', 'vm.info / ls', 'Get-VM | ...', 'GET/POST/PUT', 'known_hosts'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ESXi hosts · vSAN datastores · vCenter appliance · NSX Managers · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vCenter  = VMware vCenter Server; central management platform for hosts and VMs'))
    lines.append(txt_row('esxcli   = ESXi command-line utility; manages network, storage, and VM kernel modules'))
    lines.append(txt_row('govc     = Go-based open-source vCenter CLI; wraps vSphere API for fast operations'))
    lines.append(txt_row('PowerCLI = VMware PowerShell module; 700+ cmdlets for full vSphere automation'))
    lines.append(txt_row('Aria Operations= VMware vROps; ML-based performance analytics and capacity management'))
    lines.append(txt_row('PSOD     = Purple Screen of Death; ESXi kernel panic with vmkernel dump for analysis'))
    lines.append(txt_row('vSAN     = VMware hyperconverged storage; NVMe/SSD pools forming a cluster datastore'))
    lines.append(txt_row('DRS      = Distributed Resource Scheduler; auto-migrates VMs to balance CPU/memory'))
    lines.append(txt_row('HA       = High Availability; restarts VMs on surviving hosts after a host failure'))
    lines.append(txt_row('VUM      = vSphere Update Manager; baseline-based patching for ESXi hosts'))
    lines.append(txt_row('LCM      = Lifecycle Manager; successor to VUM; manages vSphere add-on lifecycle'))
    lines.append(txt_row('vROps    = VMware vRealize Operations; analytics engine in Aria Operations platform'))
    lines.append(txt_row('VDS      = vSphere Distributed Switch; cluster-level virtual switch managed by vCenter'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vmware-ref',
    'docs/virtualization/reference/index.md',
    'VMware Reference Hub — standards, inventory, upgrade readiness, quick reference',
)
def vmware_reference_hub():
    """VMware Reference Hub — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99
    ST_L, ST_R =  3, 33;  ST_MID = (ST_L + ST_R) // 2
    IV_L, IV_R = 36, 66;  IV_MID = (IV_L + IV_R) // 2
    UP_L, UP_R = 69, 99;  UP_MID = (UP_L + UP_R) // 2
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'VMware Reference Hub'))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'VMware Reference Hub')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Central reference for platform standards, inventory, upgrade readiness, and quick lookup')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Standards define how the environment is built · Inventory tracks what exists')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Upgrade Readiness validates compatibility · Quick Reference gives commands on demand')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Maintained alongside change records to stay current with deployed platform versions')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Standards, inventory, and readiness work together to keep the platform well-managed'))
    lines.append(txt_row())
    lines.append(R(arrow([ST_MID, IV_MID, UP_MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(ST_L, ST_R), bTop(IV_L, IV_R), bTop(UP_L, UP_R))))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'Standards'),
        bMid(IV_L, IV_R, 'Inventory'),
        bMid(UP_L, UP_R, 'Upgrade Readiness'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'Naming: VM, host, cluster'),
        bMid(IV_L, IV_R, 'Host register: cluster map'),
        bMid(UP_L, UP_R, 'HCL: hardware compat.'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'Host build: BIOS/ESXi std'),
        bMid(IV_L, IV_R, 'VM catalog: owner + tier'),
        bMid(UP_L, UP_R, 'Interop matrix: VC+ESXi'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'Port groups: VLAN design'),
        bMid(IV_L, IV_R, 'Datastore: usage+policy'),
        bMid(UP_L, UP_R, 'Pre-checks: health+certs'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'vSAN policy: FTT+stripe'),
        bMid(IV_L, IV_R, 'Network: VDS + VLAN map'),
        bMid(UP_L, UP_R, 'Rollback: snapshot+plan'),
    )))
    lines.append(R(merge(
        bMid(ST_L, ST_R, 'Change control: process'),
        bMid(IV_L, IV_R, 'Certs + SVC accounts'),
        bMid(UP_L, UP_R, 'Post-val: VM + vSAN'),
    )))
    lines.append(R(merge(bBot(ST_L, ST_R), bBot(IV_L, IV_R), bBot(UP_L, UP_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Reference content drives consistency across builds, changes, and upgrade events'))
    lines.append(txt_row())
    lines.append(R(arrow([ST_MID, IV_MID, UP_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Quick Reference')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Port reference: vCenter 443/8443 · ESXi 443/902 · NFC 2049 · vMotion 8000')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Common CLI: esxcli network nic list · vim-cmd vmsvc/getallvms · govc vm.info')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'vSphere versions: vCenter must be ≥ ESXi; 2-hop version hop limit for upgrades')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'License SKUs: Essentials+ · Standard · Enterprise Plus · vSAN Standard/Enterprise')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Quick Reference covers commands, ports, versioning, and license SKU details'))
    lines.append(txt_row())
    lines.append(R(arrow([ST_MID, IV_MID, UP_MID])))
    lines.append(txt_row())

    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Standards', 'Inventory', 'Upgrades', 'Quick Ref', 'Ports'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Naming std.', 'Host register', 'HCL lookup', 'esxcli cmds', 'HTTPS 443'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Build std.', 'VM catalog', 'Pre-checks', 'govc cmds', 'vMotion 8000'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['VLAN design', 'Cert tracking', 'Rollback plan', 'PowerCLI ref.', 'NFC 2049'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Change ctrl', 'SVC accounts', 'Post-val', 'API reference', 'ESXi 902'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ESXi hosts · vCenter appliance · vSAN datastores · NSX Managers · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('HCL     = VMware Hardware Compatibility List; certified hardware for vSphere and vSAN'))
    lines.append(txt_row('FTT     = Failures to Tolerate; vSAN SPBM policy setting for data redundancy'))
    lines.append(txt_row('VDS     = vSphere Distributed Switch; cluster-level virtual switch in vCenter'))
    lines.append(txt_row('SPBM    = Storage Policy-Based Management; assigns vSAN rules per VM or virtual disk'))
    lines.append(txt_row('vMotion  = Live VM migration between ESXi hosts; traffic on VMkernel port 8000'))
    lines.append(txt_row('NFC     = Network File Copy; protocol for vCenter cold migrations and deployments'))
    lines.append(txt_row('Port 902 = ESXi hostd/vpxa heartbeat and management traffic from vCenter to host'))
    lines.append(txt_row('Interop  = VMware interoperability matrix; validates vCenter + ESXi version combinations'))
    lines.append(txt_row('SVC Account= Service account for vCenter, backup, and monitoring tool authentication'))
    lines.append(txt_row('Enterprise Plus= vSphere top-tier licence; includes DRS, HA, vSAN, and all features'))
    lines.append(txt_row('Change Control= Documented process for approved infra changes; tracks risk and rollback'))
    lines.append(txt_row('Essentials+= vSphere entry licence; limited to 3 hosts; HA but no DRS or vSAN'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines



# ── Pure Storage sub-section diagrams ─────────────────────────────────────────

@kb_diagram(
    'pure-flasharray',
    'docs/storage/pure/flasharray/index.md',
    'Pure FlashArray Stack — CT0/CT1 HA, Purity//FA, NVMe/FC, ActiveDR, ActiveCluster, SafeMode',
)
def pure_flasharray_stack():
    """Pure FlashArray Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Pure FlashArray Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Pure FlashArray — All-Flash Block Storage (Purity//FA)')))
    lines.append(R(bMid(IV_L, IV_R, 'Dual-controller HA pair: CT0 + CT1 active/active with NVRAM mirroring for < 1 ms write ACK')))
    lines.append(R(bMid(IV_L, IV_R, 'Protocols: Fibre Channel (16/32G) · iSCSI (10/25 GbE) · NVMe/FC · NVMe/RoCE · NVMe/TCP')))
    lines.append(R(bMid(IV_L, IV_R, 'Pure1: cloud management portal — telemetry, AI support alerts, capacity forecasting, proactive')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication: ActiveDR (async, RPO minutes) · ActiveCluster (sync, zero RPO, stretch cluster)')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  FlashArray management layer feeds architecture, operations, security, and troubleshooting'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CT0/CT1 HA pair design'),
        bMid(B2_L, B2_R, 'purearray CLI + REST API'),
        bMid(B3_L, B3_R, 'SafeMode: immutable snaps'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NVRAM: write buffer+mirror'),
        bMid(B2_L, B2_R, 'Volume: create, expand, map'),
        bMid(B3_L, B3_R, 'RBAC: roles + API tokens'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Flash shelves: NVMe SSD'),
        bMid(B2_L, B2_R, 'Snapshots + clones + PGs'),
        bMid(B3_L, B3_R, 'Data-at-rest: AES-256'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Inline dedup+compression'),
        bMid(B2_L, B2_R, 'Health: drives, ports, cache'),
        bMid(B3_L, B3_R, 'Audit log + syslog export'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ActiveCluster: stretch vols'),
        bMid(B2_L, B2_R, 'ActiveDR: async replication'),
        bMid(B3_L, B3_R, 'Directory services: AD/LDAP'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines HA and data path · Operations manage volumes'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Volume offline', 'purearray list', 'Drive health OK', 'Case: array ID', 'purearray get'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Repl lag/BW check', 'purelog download', 'Port: link state', 'Log bundle req', 'purevolume list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['HA failover path', 'puresupport bundle', 'Capacity: >80%?', 'Remote assist', 'purehgroup list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Snap space growth', 'netconfig verify', 'Repl state: Active', 'P1/P2 severity', 'pureport list'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Dual controllers (CT0/CT1) · NVMe flash shelves · FC/iSCSI/NVMe HBAs · SAN switches · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Purity//FA    = FlashArray operating system; manages data services, dedup, compression, and protocols'))
    lines.append(txt_row('NVRAM         = Non-volatile RAM; write buffer mirrored CT0↔CT1 before ACK — guarantees < 1 ms writes'))
    lines.append(txt_row('ActiveCluster = Synchronous stretch cluster; zero RPO across two sites or arrays on same fabric'))
    lines.append(txt_row('ActiveDR      = Asynchronous replication; RPO in minutes; automated failover and failback workflow'))
    lines.append(txt_row('SafeMode      = Pure immutable snapshot protection; delete requires PIN from Pure Storage support'))
    lines.append(txt_row('Protection Group= PG; set of volumes replicated together on a schedule to a target array or cloud'))
    lines.append(txt_row('Inline dedup  = Deduplication applied before data hits flash; no post-process latency penalty'))
    lines.append(txt_row('CT0 / CT1     = Controller 0 and Controller 1; both actively serve I/O simultaneously'))
    lines.append(txt_row('NVMe/RoCE     = NVMe over RDMA over Converged Ethernet; ultra-low latency block access over IP fabric'))
    lines.append(txt_row('NVMe/FC       = NVMe over Fibre Channel; block protocol for NVMe SSDs transported over FC fabric'))
    lines.append(txt_row('Pure1         = Cloud management portal; remote telemetry, AI-driven alerts, capacity forecasting'))
    lines.append(txt_row('RBAC          = Role-Based Access Control; Storage Admin, Array Admin, Read-Only built-in roles'))
    lines.append(txt_row('purearray     = CLI entry point on FlashArray; purearray get/list/set for array-level config'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'pure-flashblade',
    'docs/storage/pure/flashblade/index.md',
    'Pure FlashBlade Stack — scale-out blades, NFS/SMB/S3/HDFS, Purity//FB, replication',
)
def pure_flashblade_stack():
    """Pure FlashBlade Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Pure FlashBlade Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Pure FlashBlade — Unified Fast File and Object Storage (Purity//FB)')))
    lines.append(R(bMid(IV_L, IV_R, 'Scale-out blade architecture: blade modules add capacity + performance; no hot spots')))
    lines.append(R(bMid(IV_L, IV_R, 'Protocols: NFS v3/v4.1 · SMB 2/3 · S3 API · HDFS — unified from single platform')))
    lines.append(R(bMid(IV_L, IV_R, 'Use cases: AI/ML training data, analytics, backup targets, unstructured data at scale')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication: asynchronous object and file replication to another FlashBlade or cloud')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  FlashBlade management spans blade hardware, protocol services, operations, and security'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Blade modules: F-series'),
        bMid(B2_L, B2_R, 'purefb CLI + REST API'),
        bMid(B3_L, B3_R, 'RBAC: roles + tokens'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Chassis: 4–15 blades'),
        bMid(B2_L, B2_R, 'File system + bucket ops'),
        bMid(B3_L, B3_R, 'Data-at-rest: AES-256'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NFS exports + SMB shares'),
        bMid(B2_L, B2_R, 'Snapshots: dir + object'),
        bMid(B3_L, B3_R, 'Network: subnet policies'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'S3 buckets + IAM policies'),
        bMid(B2_L, B2_R, 'Capacity: blades + forecast'),
        bMid(B3_L, B3_R, 'Audit log + syslog'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Replication: async FB→FB'),
        bMid(B2_L, B2_R, 'Health: blade, network'),
        bMid(B3_L, B3_R, 'Directory services: AD/LDAP'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines scale-out layout · Operations manage shares and buckets'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['NFS mount fail', 'purefb list', 'Blade health OK', 'Case: array SN', 'purefb get'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['S3 auth failure', 'purelog download', 'Network: ports', 'Log bundle req', 'purefb fs list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Repl lag: BW', 'purebuddy check', 'Capacity: >80%?', 'Remote assist', 'purefb bucket ls'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SMB slow writes', 'netconfig verify', 'Repl state: OK', 'P1/P2 severity', 'purefb snap list'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('FlashBlade chassis · F-series blade modules · 10/25/100 GbE NICs · Ethernet switches'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Purity//FB   = FlashBlade operating system; manages file, object, and HDFS data services'))
    lines.append(txt_row('F-series     = FlashBlade blade module type; NVMe-based, each adds capacity and throughput'))
    lines.append(txt_row('NFS          = Network File System; file protocol used by Linux/Unix clients; v3 and v4.1 supported'))
    lines.append(txt_row('SMB          = Server Message Block; Windows file sharing protocol; SMB 2.0 and 3.0 on FlashBlade'))
    lines.append(txt_row('S3           = AWS-compatible object storage API; FlashBlade implements S3 bucket/object model'))
    lines.append(txt_row('HDFS         = Hadoop Distributed File System API; FlashBlade serves as HDFS-compatible target'))
    lines.append(txt_row('purefb       = FlashBlade CLI entry point; purefb fs/bucket/snap/hw commands for management'))
    lines.append(txt_row('Scale-out    = Adding blades increases both capacity and performance simultaneously (no hot spots)'))
    lines.append(txt_row('Replication  = Async file/object replication to another FlashBlade or object store; RPO-based'))
    lines.append(txt_row('Subnet policy= Network access rules bound to FlashBlade interfaces for NFS, SMB, S3, replication'))
    lines.append(txt_row('RBAC         = Role-Based Access Control; Array Admin, Storage Admin, Read-Only roles on FlashBlade'))
    lines.append(txt_row('Pure1        = Cloud management portal; monitors all FlashBlade arrays; capacity and health analytics'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'pure-evergreen',
    'docs/storage/pure/evergreen/index.md',
    'Pure Evergreen Program — NDU controller refresh, Purity upgrades, Ever Modern lifecycle',
)
def pure_evergreen_program():
    """Pure Evergreen Program — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Pure Evergreen Program'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Pure Evergreen — Hardware Subscription + Non-Disruptive Lifecycle')))
    lines.append(R(bMid(IV_L, IV_R, 'Ever Modern: periodic controller refresh with zero downtime — no forklift upgrades, ever')))
    lines.append(R(bMid(IV_L, IV_R, 'Purity upgrades: OS updates delivered non-disruptively on same hardware via Pure1 scheduling')))
    lines.append(R(bMid(IV_L, IV_R, 'Subscription tiers: Evergreen//Forever (purchased) · Evergreen//One (STaaS) · Evergreen//Flex')))
    lines.append(R(bMid(IV_L, IV_R, 'Controller refresh: new CT shipped, slide-in swap; no data migration, no reformat required')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Evergreen covers the full lifecycle: architecture, operations, refresh, security, and'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Lifecycle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Subscription model: NDU'),
        bMid(B2_L, B2_R, 'Purity upgrade: schedule'),
        bMid(B3_L, B3_R, 'Version matrix: FA/FB'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Controller: slide-in swap'),
        bMid(B2_L, B2_R, 'Controller refresh prep'),
        bMid(B3_L, B3_R, 'EOL tracking: model dates'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Flash: add shelf/blade NDU'),
        bMid(B2_L, B2_R, 'Pre-check: health + alerts'),
        bMid(B3_L, B3_R, 'Refresh planning: timeline'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Evergreen//Forever model'),
        bMid(B2_L, B2_R, 'Post-val: array + hosts'),
        bMid(B3_L, B3_R, 'Upgrade path: hop rules'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pure1: lifecycle visibility'),
        bMid(B2_L, B2_R, 'Security: baseline check'),
        bMid(B3_L, B3_R, 'Compatibility matrix check'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines the subscription model · Operations execute upgrades'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Upgrade fails', 'purearray get', 'SW version OK?', 'Case: upgrade', 'purearray get'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CT swap issues', 'purelog download', 'Drive health OK', 'TAM escalation', 'purearray list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Host I/O during ND', 'puresupport bundle', 'Pre-check: pass?', 'Remote assist', 'purevolume list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Repl: pause+resume', 'netconfig verify', 'Post-val: vols', 'P1/P2 severity', 'pureport list'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('FlashArray controllers (CT0/CT1) · NVMe flash shelves · FC/iSCSI/NVMe HBAs · SAN switches · Power'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Evergreen      = Pure hardware + software subscription model; replaces forklift upgrade cycle'))
    lines.append(txt_row('NDU            = Non-Disruptive Upgrade; Purity OS updates applied with zero downtime to hosts'))
    lines.append(txt_row('Ever Modern    = Controller refresh entitlement; new CT0/CT1 shipped and swapped non-disruptively'))
    lines.append(txt_row('Purity upgrade = Operating system upgrade applied to FlashArray or FlashBlade via Pure1 schedule'))
    lines.append(txt_row('Evergreen//Forever = Purchased subscription; hardware refresh rights included; perpetual entitlement'))
    lines.append(txt_row('Evergreen//One = STaaS tier; Pure-owned hardware, consumption billing, 99.9999% SLA guaranteed'))
    lines.append(txt_row('Evergreen//Flex= Flex subscription; capacity can scale up or down; usage-based billing model'))
    lines.append(txt_row('Controller swap= Physical CT replacement; slides in while array stays online serving I/O'))
    lines.append(txt_row('EOL            = End of Life; model or Purity version reaching end of support/maintenance'))
    lines.append(txt_row('Hop limit      = Maximum Purity version jump in one upgrade step; check compatibility matrix'))
    lines.append(txt_row('Pre-check      = Automated or manual health validation before starting controller or Purity upgrade'))
    lines.append(txt_row('Pure1          = Cloud portal that schedules and monitors Evergreen upgrades and refresh events'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'pure-evergreen-one',
    'docs/storage/pure/evergreen-one/index.md',
    'Pure Evergreen//One — STaaS, Pure-owned hardware, 99.9999% SLA, consumption billing',
)
def pure_evergreen_one():
    """Pure Evergreen//One STaaS — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Pure Evergreen//One'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Evergreen//One — Storage-as-a-Service (Pure-Owned, Customer-Operated)')))
    lines.append(R(bMid(IV_L, IV_R, 'Pure-owned and managed hardware installed on-premises or in colocation — customer pays per TiB')))
    lines.append(R(bMid(IV_L, IV_R, 'SLA: 99.9999% availability · performance guarantees · consumption-based billing per TiB used')))
    lines.append(R(bMid(IV_L, IV_R, 'Pure manages: hardware refresh, Purity upgrades, capacity additions — all non-disruptive')))
    lines.append(R(bMid(IV_L, IV_R, 'Customer operates: volume provisioning, host zoning, snapshots, replication policies')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Evergreen//One combines STaaS economics with on-premises control and guaranteed SLAs'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Vendor Support'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pure-owned hardware on-prem'),
        bMid(B2_L, B2_R, 'Pure1: health + telemetry'),
        bMid(B3_L, B3_R, 'Vendor: hw refresh + Purity'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Consumption billing: TiB'),
        bMid(B2_L, B2_R, 'Volume + host mapping ops'),
        bMid(B3_L, B3_R, 'SLA: 99.9999% + perf SLO'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '99.9999% availability SLA'),
        bMid(B2_L, B2_R, 'Snapshots + replication'),
        bMid(B3_L, B3_R, 'Support portal: case open'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Min committed capacity'),
        bMid(B2_L, B2_R, 'Capacity: usage reporting'),
        bMid(B3_L, B3_R, 'On-site engineer if needed'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Integration: colo/on-prem'),
        bMid(B2_L, B2_R, 'Alerts: Pure1 proactive'),
        bMid(B3_L, B3_R, 'Data to collect: log bundle'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines STaaS model · Operations run daily tasks · Vendor Support covers incidents'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Volume offline', 'purearray list', 'SLA: green OK?', 'Case: SLA breach', 'purearray get'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Billing dispute', 'Pure1 telemetry', 'Capacity headroom', 'TAM escalation', 'purevolume list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Perf below SLO', 'purelog download', 'Perf SLO: met?', 'Remote assist', 'pureport list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Connectivity loss', 'netconfig verify', 'Repl state: OK', 'P1/P2 severity', 'purehgroup list'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Pure-owned FlashArray/FlashBlade · customer data centre or colo rack · Power, Cooling, and Network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Evergreen//One  = Pure Storage-as-a-Service; Pure owns hardware, customer gets consumption pricing'))
    lines.append(txt_row('STaaS           = Storage as a Service; pay-per-TiB model with no CapEx hardware purchase'))
    lines.append(txt_row('99.9999% SLA    = Six nines availability guarantee; ~31 seconds downtime per year maximum'))
    lines.append(txt_row('Perf SLO        = Performance Service Level Objective; latency and IOPS thresholds guaranteed'))
    lines.append(txt_row('Consumption billing = Billed on actual TiB consumed above committed base; metered monthly'))
    lines.append(txt_row('Committed capacity= Minimum TiB reserved in contract; pay for this floor regardless of actual use'))
    lines.append(txt_row('Pure1           = Cloud portal; Pure team monitors SLA health and proactively resolves issues'))
    lines.append(txt_row('Vendor refresh  = Pure ships replacement controllers or blades when hardware reaches EOL'))
    lines.append(txt_row('Colo deployment = Pure-owned array installed in a customer-selected colocation facility'))
    lines.append(txt_row('Log bundle      = Diagnostic data package pulled from array for Pure support case analysis'))
    lines.append(txt_row('TAM             = Technical Account Manager; Pure escalation point for strategic and critical issues'))
    lines.append(txt_row('Remote assist   = Pure engineer connects via secure tunnel for live troubleshooting on the array'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'pure-operations',
    'docs/storage/pure/operations/index.md',
    'Pure Storage Operations Hub — Pure1 portal, alerts severity, support cases P1-P4',
)
def pure_operations_hub():
    """Pure Storage Operations Hub — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Pure Storage Operations Hub'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Pure Storage Operations — Pure1, Alerts, and Support Case Management')))
    lines.append(R(bMid(IV_L, IV_R, 'Pure1 cloud portal: central management for all FlashArray and FlashBlade arrays globally')))
    lines.append(R(bMid(IV_L, IV_R, 'Alerts: hardware, software, and capacity events; severity levels Info, Warning, Error, Critical')))
    lines.append(R(bMid(IV_L, IV_R, 'Support cases: opened via Pure1 or phone; include log bundle, serial number, and impact')))
    lines.append(R(bMid(IV_L, IV_R, 'Proactive support: Pure1 AI detects anomalies and opens cases automatically before failure')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Pure1 feeds alerts and support workflows — day-to-day ops span portal, CLI, and case management'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pure1 Portal'),
        bMid(B2_L, B2_R, 'Alerts'),
        bMid(B3_L, B3_R, 'Support Cases'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Array fleet dashboard'),
        bMid(B2_L, B2_R, 'Severity: Info → Critical'),
        bMid(B3_L, B3_R, 'Open via Pure1 or phone'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Capacity + perf analytics'),
        bMid(B2_L, B2_R, 'Hardware alerts: drive, CT'),
        bMid(B3_L, B3_R, 'Collect: log bundle + SN'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AI-driven health insights'),
        bMid(B2_L, B2_R, 'SW alerts: Purity version'),
        bMid(B3_L, B3_R, 'Severity: P1-P4 tiers'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Upgrade scheduler: NDU'),
        bMid(B2_L, B2_R, 'Capacity alerts: >80%'),
        bMid(B3_L, B3_R, 'Remote assist session'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Proactive case auto-open'),
        bMid(B2_L, B2_R, 'Repl alerts: lag + state'),
        bMid(B3_L, B3_R, 'TAM for strategic issues'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Pure1 provides fleet visibility · Alerts drive action'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Pure1 Features', 'Alert Types', 'Case Workflow', 'Escalation', 'CLI Commands'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Fleet dashboard', 'Drive failure', 'Collect log bundle', 'TAM engagement', 'purearray list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Capacity forecast', 'CT warning', 'Describe impact', 'Remote assist', 'purealert list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Perf analytics', 'Purity upgrade', 'Submit via portal', 'Exec escalation', 'purearray get'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Upgrade schedule', 'Capacity >80%', 'P1: 24/7 response', 'VP escalation', 'purelog download'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('FlashArray / FlashBlade arrays · customer data centre · Pure1 cloud (SaaS portal) · Internet uplink'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Pure1         = Cloud management portal for all Pure arrays; telemetry, AI health, and upgrade'))
    lines.append(txt_row('Alert severity= Info (FYI) · Warning (monitor) · Error (investigate) · Critical (act immediately)'))
    lines.append(txt_row('Log bundle    = puresupport bundle command output; full diagnostic archive for support case'))
    lines.append(txt_row('Proactive case= Pure1 AI opens a support case automatically when anomaly detected before failure'))
    lines.append(txt_row('P1 case       = Severity 1; production down or data loss; 24/7 response SLA, engineer on phone'))
    lines.append(txt_row('P2 case       = Severity 2; degraded performance or risk; business-hours response with engineer'))
    lines.append(txt_row('Remote assist = Pure engineer connects via secure tunnel to live array for real-time troubleshooting'))
    lines.append(txt_row('TAM           = Technical Account Manager; Pure named escalation contact for strategic accounts'))
    lines.append(txt_row('NDU scheduler = Non-Disruptive Upgrade scheduler in Pure1; picks maintenance window for Purity update'))
    lines.append(txt_row('purealert     = CLI command to list, acknowledge, and filter alerts on FlashArray or FlashBlade'))
    lines.append(txt_row('Capacity alert= Fires when array used capacity exceeds configured threshold (default 80%)'))
    lines.append(txt_row('SN            = Serial number; required in every Pure support case for array identification'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── AWS sub-section diagrams ───────────────────────────────────────────────────

@kb_diagram(
    'aws-architecture',
    'docs/cloud/aws/architecture/index.md',
    'AWS Architecture Overview — multi-account, Organizations, SCPs, TGW, IAM Identity Center',
)
def aws_architecture_overview():
    """AWS Architecture Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Platform Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Platform Architecture — Multi-Account Organisation with Hub-and-Spoke Networking')))
    lines.append(R(bMid(IV_L, IV_R, 'Management Account: AWS Organizations root · SCPs · IAM Identity Center SSO · billing')))
    lines.append(R(bMid(IV_L, IV_R, 'Networking: Transit Gateway hub connects spoke VPCs across accounts and on-premises via')))
    lines.append(R(bMid(IV_L, IV_R, 'Workload accounts: dedicated member accounts per environment (dev/staging/prod) or per team')))
    lines.append(R(bMid(IV_L, IV_R, 'Guardrails: SCPs (preventive) + AWS Config (detective) + Security Hub (aggregated compliance)')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Management account controls governance · networking hub connects spokes'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Organizations: root + OUs'),
        bMid(B2_L, B2_R, 'On-prem: DirectConnect'),
        bMid(B3_L, B3_R, 'Account structure: OU layout'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'IAM Identity Center: SSO'),
        bMid(B2_L, B2_R, 'IdP: Azure AD / Okta SAML'),
        bMid(B3_L, B3_R, 'Tagging: env+owner+team'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Transit Gateway: hub-spoke'),
        bMid(B2_L, B2_R, 'Monitoring: CloudWatch/SIEM'),
        bMid(B3_L, B3_R, 'Naming: account + resource'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SCPs: OU-level guardrails'),
        bMid(B2_L, B2_R, 'Security: GuardDuty+Hub'),
        bMid(B3_L, B3_R, 'Security baselines: CIS AWS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Config: resource inventory'),
        bMid(B2_L, B2_R, 'Billing: CUR + Cost Expl.'),
        bMid(B3_L, B3_R, 'No workloads in mgmt acct'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines OU layout and networking · Integrations connect IdP and on-prem'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Account Layer', 'Networking', 'Identity', 'Guardrails', 'Observability'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Mgmt account', 'Transit Gateway', 'IAM Identity Ctr', 'SCPs on OUs', 'CloudTrail org'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Audit account', 'VPC per account', 'SSO groups', 'AWS Config', 'CloudWatch logs'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Log archive acct', 'DirectConnect', 'Permission sets', 'Security Hub', 'Cost Explorer'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Workload accounts', 'VPC Endpoints', 'MFA enforced', 'GuardDuty org', 'Budgets+alerts'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Regions · Availability Zones · Data Centres · Global backbone · DirectConnect physical ports'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Organizations = AWS service for multi-account management; root contains management account and OUs'))
    lines.append(txt_row('OU            = Organisational Unit; logical grouping of accounts; SCPs applied at OU level'))
    lines.append(txt_row('SCP           = Service Control Policy; preventive guardrail; restricts what actions accounts can'))
    lines.append(txt_row('IAM Identity Center= AWS SSO service; assigns permission sets to users/groups in member accounts'))
    lines.append(txt_row('Transit Gateway= Regional hub router; connects VPCs across accounts and to on-premises via DX/VPN'))
    lines.append(txt_row('DirectConnect = Dedicated private network connection from on-premises to AWS; bypasses internet'))
    lines.append(txt_row('AWS Config    = Tracks resource configuration history; evaluates rules; records compliance state'))
    lines.append(txt_row('Security Hub  = Aggregates findings from GuardDuty, Inspector, Config; scores security posture'))
    lines.append(txt_row('GuardDuty     = Threat detection service; analyses CloudTrail, VPC Flow Logs, DNS logs for threats'))
    lines.append(txt_row('CUR           = Cost and Usage Report; detailed billing data for chargeback and FinOps analysis'))
    lines.append(txt_row('Permission set= IAM Identity Center policy assigned to a user/group for a specific member account'))
    lines.append(txt_row('Management account= Root of the AWS Organization; no workloads; used for billing and org-level policy'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aws-backup',
    'docs/cloud/aws/backup/index.md',
    'AWS Backup Overview — Backup Plans, Vaults, Vault Lock, jobs, restore testing, compliance',
)
def aws_backup_overview():
    """AWS Backup Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Backup Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Backup — Centralised Backup Management Across AWS Services')))
    lines.append(R(bMid(IV_L, IV_R, 'Backup Plans: define schedules, lifecycle, copy rules, and resource assignments per service')))
    lines.append(R(bMid(IV_L, IV_R, 'Supported resources: EC2 · EBS · RDS · Aurora · DynamoDB · EFS · FSx · S3 · Storage Gateway')))
    lines.append(R(bMid(IV_L, IV_R, 'Backup Vaults: encrypted storage for recovery points; Vault Lock enforces immutable retention')))
    lines.append(R(bMid(IV_L, IV_R, 'Compliance: backup reports via Audit Manager; cross-region and cross-account copy supported')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Backup Plans trigger jobs · Jobs produce recovery points in Vaults · compliance validates coverage'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Backup Plans'),
        bMid(B2_L, B2_R, 'Backup Vaults'),
        bMid(B3_L, B3_R, 'Backup Jobs'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Rules: schedule + window'),
        bMid(B2_L, B2_R, 'KMS-encrypted storage'),
        bMid(B3_L, B3_R, 'Status: Completed/Failed'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Lifecycle: warm → cold'),
        bMid(B2_L, B2_R, 'Vault Lock: WORM policy'),
        bMid(B3_L, B3_R, 'Monitor: EventBridge events'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Resource assignment: tag'),
        bMid(B2_L, B2_R, 'Cross-region copy vault'),
        bMid(B3_L, B3_R, 'Alerts: CloudWatch alarms'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Copy rules: X-region/acct'),
        bMid(B2_L, B2_R, 'Access policy: IAM+vault'),
        bMid(B3_L, B3_R, 'Restore testing: monthly'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Retention: daily/wk/mo/yr'),
        bMid(B2_L, B2_R, 'Recovery point: RPO time'),
        bMid(B3_L, B3_R, 'Compliance: Audit Manager'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Plans define schedules · Vaults store recovery points securely'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Backup Plans', 'Backup Vaults', 'Backup Jobs', 'Restore Testing', 'Compliance'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Daily + weekly', 'KMS key assign', 'Monitor status', 'Restore by RPO', 'Audit reports'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cold lifecycle', 'Vault Lock WORM', 'Failed: retry?', 'Test validation', 'Coverage gaps'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Tag-based assign', 'X-region vault', 'EventBridge hook', 'RTO verify', 'Backup report'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Org-level plan', 'Access policy', 'Alert on failure', 'Compliance test', 'Org framework'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Regions · S3-backed Backup Vaults · EC2/EBS/RDS source resources · KMS key infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Plan    = Policy that defines backup rules: schedule, lifecycle, copy destinations, retention'))
    lines.append(txt_row('Backup Vault   = Encrypted container for recovery points; access controlled by vault policy + IAM'))
    lines.append(txt_row('Vault Lock     = WORM protection on a vault; prevents deletion even by account root; compliance mode'))
    lines.append(txt_row('Recovery Point = Snapshot/backup of a resource at a point in time; stored in vault; restorable'))
    lines.append(txt_row('Backup Job     = Single backup execution; status tracked as Pending/Running/Completed/Failed/Aborted'))
    lines.append(txt_row('Restore Job    = Recovery of a resource from a recovery point; creates a new resource copy'))
    lines.append(txt_row('RPO            = Recovery Point Objective; maximum age of backup acceptable for restore after failure'))
    lines.append(txt_row('RTO            = Recovery Time Objective; maximum acceptable time to restore service after failure'))
    lines.append(txt_row('Lifecycle rule = Moves recovery points from warm (standard) to cold (cheaper) storage after N days'))
    lines.append(txt_row('X-region copy  = Cross-region replication of recovery points for DR; configured in backup plan rule'))
    lines.append(txt_row('Audit Manager  = AWS service generating backup compliance reports against defined frameworks'))
    lines.append(txt_row('Backup Compliance Report= scheduled report showing backup coverage, job success rates, and gaps'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aws-cli',
    'docs/cloud/aws/cli-reference/index.md',
    'AWS CLI Reference — CLI v2, profiles, assume-role, ec2/s3/iam/rds/eks commands',
)
def aws_cli_reference():
    """AWS CLI Reference — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS CLI Reference'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS CLI — Command-Line Interface for AWS Service Management')))
    lines.append(R(bMid(IV_L, IV_R, 'Structured as: aws <service> <command> [--options] — e.g. aws ec2 describe-instances')))
    lines.append(R(bMid(IV_L, IV_R, 'Auth: profiles in ~/.aws/credentials; assume-role; IAM Identity Center SSO login')))
    lines.append(R(bMid(IV_L, IV_R, 'Output formats: --output json (default) | table | text | yaml | yaml-stream')))
    lines.append(R(bMid(IV_L, IV_R, 'Pagination: --max-items / --starting-token; or --no-paginate for full result sets')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  AWS CLI organises commands by service — EC2, S3, IAM, RDS, EKS, SSM, CloudFormation, CloudWatch'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Compute (EC2/Lambda)'),
        bMid(B2_L, B2_R, 'Storage (S3/EBS/EFS)'),
        bMid(B3_L, B3_R, 'Identity (IAM/SSO)'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ec2 describe-instances'),
        bMid(B2_L, B2_R, 's3 ls / cp / sync / rm'),
        bMid(B3_L, B3_R, 'iam list-users/roles'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ec2 start/stop-instances'),
        bMid(B2_L, B2_R, 'ec2 describe-volumes'),
        bMid(B3_L, B3_R, 'iam get-policy/document'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ec2 create-snapshot'),
        bMid(B2_L, B2_R, 'ec2 create-volume/attach'),
        bMid(B3_L, B3_R, 'sts assume-role'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'lambda invoke/list'),
        bMid(B2_L, B2_R, 'efs describe-filesystems'),
        bMid(B3_L, B3_R, 'sso login / logout'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ssm start-session'),
        bMid(B2_L, B2_R, 's3api head-bucket'),
        bMid(B3_L, B3_R, 'iam simulate-principal'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Compute CLI manages instances · Storage CLI handles S3/EBS/EFS'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['EC2 / SSM', 'S3', 'IAM', 'RDS / EKS', 'CloudWatch'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['describe-instances', 's3 sync src dst', 'list-roles', 'rds describe-db', 'get-metric-data'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['ssm start-session', 's3api list-obj', 'assume-role', 'eks get-token', 'put-metric-alarm'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['run-instances', 'cp --recursive', 'create-policy', 'eks list-clusters', 'describe-alarms'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['send-command', 'rb --force', 'delete-role', 'rds failover-db', 'logs filter-log'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS Regions · API endpoints (HTTPS) · IAM authentication layer · CloudShell or local workstation'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('AWS CLI v2     = Current CLI version; install via pip or official pkg; aws --version to verify'))
    lines.append(txt_row('Named profile  = ~/.aws/credentials named section; use --profile name or AWS_PROFILE env var'))
    lines.append(txt_row('assume-role    = sts assume-role --role-arn ... --role-session-name; exports temp credentials'))
    lines.append(txt_row('--query        = JMESPath filter on JSON output; e.g. --query "Instances[*].InstanceId"'))
    lines.append(txt_row('--filter       = Server-side filter; e.g. --filters "Name=tag:Env,Values=prod" on describe calls'))
    lines.append(txt_row('--output table = Formats JSON output as ASCII table for human-readable inspection in terminal'))
    lines.append(txt_row('aws configure  = Interactive setup; writes region, key ID, secret, and output format to ~/.aws'))
    lines.append(txt_row('sso login      = Initiates browser-based IAM Identity Center login; caches SSO token locally'))
    lines.append(txt_row('--dry-run      = Validates permissions without executing; useful for IAM policy troubleshooting'))
    lines.append(txt_row('CloudShell     = Browser-based shell in AWS console; pre-authenticated, no local install needed'))
    lines.append(txt_row('--no-paginate  = Retrieves all pages of a paginated result in a single command call'))
    lines.append(txt_row('--region       = Overrides default region for a single command; or set AWS_DEFAULT_REGION env var'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aws-compute',
    'docs/cloud/aws/compute/index.md',
    'AWS Compute Overview — EC2, AMI, instance types, Auto Scaling, Lambda, SSM',
)
def aws_compute_overview():
    """AWS Compute Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Compute Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Compute — EC2, Auto Scaling, Lambda, and Systems Manager Fleet Management')))
    lines.append(R(bMid(IV_L, IV_R, 'EC2: virtual machines in 400+ instance types across general, compute, memory, storage families')))
    lines.append(R(bMid(IV_L, IV_R, 'Auto Scaling: launch templates + scaling policies maintain desired capacity across AZs')))
    lines.append(R(bMid(IV_L, IV_R, 'Systems Manager: fleet management without SSH — session manager, patch manager, run command')))
    lines.append(R(bMid(IV_L, IV_R, 'Lambda: serverless functions; event-driven; up to 15 min timeout; 10 GB RAM; no servers to')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Compute spans persistent VMs (EC2), elastic fleets (ASG), and serverless (Lambda) managed by SSM'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'EC2'),
        bMid(B2_L, B2_R, 'Auto Scaling'),
        bMid(B3_L, B3_R, 'Systems Manager'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Instance types: t/m/c/r/x'),
        bMid(B2_L, B2_R, 'Launch template: AMI+type'),
        bMid(B3_L, B3_R, 'Session Manager: no SSH'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AMI: OS + config snapshot'),
        bMid(B2_L, B2_R, 'Min / desired / max count'),
        bMid(B3_L, B3_R, 'Patch Manager: baselines'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'EBS: root + data volumes'),
        bMid(B2_L, B2_R, 'Scaling policies: CPU/SQS'),
        bMid(B3_L, B3_R, 'Run Command: remote exec'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Instance profile: IAM role'),
        bMid(B2_L, B2_R, 'Health check: EC2 or ELB'),
        bMid(B3_L, B3_R, 'Inventory: installed SW'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Metadata: IMDSv2 only'),
        bMid(B2_L, B2_R, 'Instance refresh: rolling'),
        bMid(B3_L, B3_R, 'Parameter Store: config'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  EC2 provides persistent VMs · Auto Scaling elastically manages fleets'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['EC2', 'Auto Scaling', 'Lambda', 'Systems Manager', 'Patch Manager'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Start / stop', 'Desired capacity', 'Runtime: py/js/go', 'Session: connect', 'Baseline: rules'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AMI: launch cfg', 'Scale in/out', 'Trigger: events', 'Run command', 'Patch: schedule'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Snapshot: EBS', 'Launch template', 'CW Logs output', 'Inventory: list', 'Compliance: view'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Resize: change typ', 'Instance refresh', 'X-acct trigger', 'Param Store: get', 'Reboot: post'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS bare-metal hosts · Nitro hypervisor · Availability Zones · VPC network · EBS storage fabric'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('EC2            = Elastic Compute Cloud; virtual machines running on AWS Nitro hypervisor'))
    lines.append(txt_row('AMI            = Amazon Machine Image; snapshot of OS + config used to launch new EC2 instances'))
    lines.append(txt_row('Instance type  = Defines vCPU, RAM, network, and storage; families: t (burstable), m (general), c'))
    lines.append(txt_row('Launch template= Versioned EC2 config (AMI, type, SG, IAM, user-data) used by ASG and manual launches'))
    lines.append(txt_row('Auto Scaling Group= Maintains desired instance count; replaces unhealthy; scales on policies or'))
    lines.append(txt_row('Instance profile= IAM role attached to EC2; grants AWS API permissions to the instance itself'))
    lines.append(txt_row('IMDSv2         = Instance Metadata Service v2; token-based; required; prevents SSRF metadata theft'))
    lines.append(txt_row('Session Manager= SSM feature replacing SSH; browser or CLI access; no inbound ports needed on SG'))
    lines.append(txt_row('Patch Manager  = SSM feature applying OS patches on schedule; records compliance per instance'))
    lines.append(txt_row('Run Command    = SSM feature executing scripts/commands on fleets without SSH; output to CloudWatch'))
    lines.append(txt_row('Lambda         = Serverless compute; no servers to manage; billed per invocation and duration (ms)'))
    lines.append(txt_row('EBS            = Elastic Block Store; persistent block volumes attached to EC2; survives instance'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aws-cost',
    'docs/cloud/aws/cost/index.md',
    'AWS Cost Management — Cost Explorer, Budgets, Reserved Instances, Savings Plans',
)
def aws_cost_management():
    """AWS Cost Management — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Cost Management'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Cost Management — Visibility, Optimisation, and Governance')))
    lines.append(R(bMid(IV_L, IV_R, 'Cost Explorer: historical and forecasted spend by service, account, region, and tag')))
    lines.append(R(bMid(IV_L, IV_R, 'Budgets: threshold alerts via email or SNS; action budgets can auto-apply IAM policies')))
    lines.append(R(bMid(IV_L, IV_R, 'Reserved Instances + Savings Plans: commit to 1 or 3 years for up to 72% discount on EC2/RDS')))
    lines.append(R(bMid(IV_L, IV_R, 'Cost Anomaly Detection: ML-based; detects unexpected spend spikes and notifies immediately')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Visibility (Explorer/CUR) feeds optimisation (RI/SP) and governance (Budgets/Anomaly/Tags)'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cost Explorer'),
        bMid(B2_L, B2_R, 'Budgets'),
        bMid(B3_L, B3_R, 'Optimisation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Service breakdowns: daily'),
        bMid(B2_L, B2_R, 'Cost threshold: $+alert'),
        bMid(B3_L, B3_R, 'Reserved Instances: 1/3yr'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Account + region filters'),
        bMid(B2_L, B2_R, 'Usage budget: unit+alert'),
        bMid(B3_L, B3_R, 'Savings Plans: compute'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Tag-based chargeback'),
        bMid(B2_L, B2_R, 'Action budget: IAM deny'),
        bMid(B3_L, B3_R, 'Spot Instances: -90% cost'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Rightsizing: recommendations'),
        bMid(B2_L, B2_R, 'Forecast: alert at 80%'),
        bMid(B3_L, B3_R, 'Anomaly Detection: ML'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CUR: hourly cost detail'),
        bMid(B2_L, B2_R, 'SNS: alert notification'),
        bMid(B3_L, B3_R, 'Cost alloc tags: billing'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Cost Explorer provides visibility · Budgets alert on thresholds · Optimisation reduces total spend'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cost Explorer', 'Budgets', 'RI / Savings', 'Anomaly', 'Tags'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['By service: EC2', 'Monthly limit', 'RI coverage %', 'ML alert: spike', 'Activate tags'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['By account: all', 'Forecast alert', 'SP utilisation', 'Investigate: who', 'Cost alloc tag'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Rightsizing recs', 'Action budget', 'RI renewal: when', 'Anomaly report', 'Chargeback: team'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Forecast: 3mo', 'SNS notify', 'Spot: savings', 'Suppress: known', 'Tagging policy'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS billing infrastructure · CUR data in S3 · Cost Explorer API · Budget notifications via SNS/email'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Cost Explorer   = AWS console and API tool for analysing spend trends by service, account, tag,'))
    lines.append(txt_row('CUR             = Cost and Usage Report; detailed hourly billing data exported to S3 for FinOps tools'))
    lines.append(txt_row('Budget          = Spend threshold with alert and optional action; types: cost, usage, RI, Savings'))
    lines.append(txt_row('Action budget   = Budget that auto-applies SCPs or IAM policies when spend threshold is crossed'))
    lines.append(txt_row('Reserved Instance= 1 or 3-year commitment to EC2/RDS capacity; up to 72% discount vs on-demand'))
    lines.append(txt_row('Savings Plan    = Flexible commitment to $/hr compute spend; applies to EC2, Fargate, Lambda'))
    lines.append(txt_row('Spot Instance   = Unused EC2 capacity at up to 90% discount; can be reclaimed with 2-min notice'))
    lines.append(txt_row('RI Coverage     = Percentage of eligible usage hours covered by Reserved Instances; target >80%'))
    lines.append(txt_row('Cost alloc tag  = Resource tag activated in billing console; appears as column in Cost Explorer/CUR'))
    lines.append(txt_row('Chargeback      = Attributing AWS costs to business units or teams using cost allocation tags'))
    lines.append(txt_row('Anomaly Detection= ML model that learns normal spend patterns and alerts on statistically unexpected'))
    lines.append(txt_row('Rightsizing     = Cost Explorer recommendation to downsize underutilised EC2 or RDS instances'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aws-governance',
    'docs/cloud/aws/governance/index.md',
    'AWS Governance — Organizations, OUs, SCPs, AWS Config, tag policies, compliance',
)
def aws_governance_overview():
    """AWS Governance Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Governance Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Governance — Organizations, SCPs, Config, and Compliance')))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Organizations: root account > OUs > member accounts; SCPs enforced at each OU level')))
    lines.append(R(bMid(IV_L, IV_R, 'Service Control Policies: preventive guardrails; deny actions before IAM even evaluates them')))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Config: detective compliance; records every resource config change; evaluates rules')))
    lines.append(R(bMid(IV_L, IV_R, 'Tagging standards: mandatory tags enforced by Config rules; used for cost and compliance')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Organizations provides structure · SCPs prevent violations · Config detects drift'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AWS Organizations'),
        bMid(B2_L, B2_R, 'Service Control Policies'),
        bMid(B3_L, B3_R, 'AWS Config'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Root: management acct'),
        bMid(B2_L, B2_R, 'JSON policy: allow/deny'),
        bMid(B3_L, B3_R, 'Config recorder: all types'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'OUs: env / team / app'),
        bMid(B2_L, B2_R, 'OU-level attachment'),
        bMid(B3_L, B3_R, 'Rules: managed + custom'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Member accounts: isolated'),
        bMid(B2_L, B2_R, 'Deny: regions, services'),
        bMid(B3_L, B3_R, 'Compliance: pass/fail/N/A'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Consolidated billing'),
        bMid(B2_L, B2_R, 'Allow-list pattern: safe'),
        bMid(B3_L, B3_R, 'Remediation: auto/manual'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Account structure std.'),
        bMid(B2_L, B2_R, 'Guardrail: no root key'),
        bMid(B3_L, B3_R, 'Config: S3 delivery dest'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Organizations structures accounts · SCPs prevent bad actions'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Organizations', 'SCPs', 'AWS Config', 'Tagging', 'Compliance'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Create account', 'Attach to OU', 'Enable recorder', 'Mandatory tags', 'Audit reports'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Move to OU', 'Deny: eu-west', 'Add managed rule', 'Tag policy: org', 'Non-compliant?'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Invite accounts', 'Test: SCP sim', 'Remediation auto', 'Tagging standard', 'Security Hub'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Consolidated bill', 'Exception: allow', 'Delivery: S3+SNS', 'Cost alloc tags', 'Frameworks: CIS'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS global infrastructure · Organizations API · Config delivery to S3 · CloudTrail audit trail'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Organizations   = AWS multi-account management service; enforces billing and governance hierarchy'))
    lines.append(txt_row('OU              = Organisational Unit; logical account grouping; SCPs attach at this level'))
    lines.append(txt_row('SCP             = Service Control Policy; max permission boundary for all IAM in attached accounts'))
    lines.append(txt_row('Preventive guardrail= SCP that blocks actions before IAM policy is evaluated; hard boundary'))
    lines.append(txt_row('Detective guardrail = Config rule that detects non-compliant resources after they exist'))
    lines.append(txt_row('Config recorder = Tracks configuration snapshots and changes for all or selected resource types'))
    lines.append(txt_row('Config rule     = Evaluates resource configs against defined conditions; managed or custom Lambda'))
    lines.append(txt_row('Remediation action= Auto-fix triggered by Config rule non-compliance; e.g. delete public S3 bucket'))
    lines.append(txt_row('Tag policy      = Organizations policy enforcing consistent tag keys/values across accounts'))
    lines.append(txt_row('Consolidated billing= Single bill for all accounts in org; volume discounts and RI sharing applies'))
    lines.append(txt_row('Account structure = Pattern of management/audit/log-archive/workload accounts following landing zone'))
    lines.append(txt_row('SCP allow-list   = Deny-all-except pattern; safer than deny-list; only permits explicitly listed'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aws-identity',
    'docs/cloud/aws/identity/index.md',
    'AWS Identity — IAM, roles, policies, IAM Identity Center SSO, Access Analyzer',
)
def aws_identity_overview():
    """AWS Identity Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Identity Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Identity — IAM, IAM Identity Center, and Permission Management')))
    lines.append(R(bMid(IV_L, IV_R, 'IAM: every AWS API call is authenticated via IAM; roles preferred over long-lived user keys')))
    lines.append(R(bMid(IV_L, IV_R, 'IAM Identity Center: SSO for AWS console and CLI; groups mapped to permission sets in accounts')))
    lines.append(R(bMid(IV_L, IV_R, 'Least privilege: customer-managed policies + Permission Boundaries limit blast radius')))
    lines.append(R(bMid(IV_L, IV_R, 'Review cycle: Access Analyzer, Access Advisor, Credential Report — quarterly permission review')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  IAM authenticates every API call · Identity Center enables SSO'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'IAM'),
        bMid(B2_L, B2_R, 'IAM Identity Center'),
        bMid(B3_L, B3_R, 'Access Control'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Roles: EC2, Lambda, X-acct'),
        bMid(B2_L, B2_R, 'SSO: browser + CLI login'),
        bMid(B3_L, B3_R, 'Permission Boundary'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Policies: managed+inline'),
        bMid(B2_L, B2_R, 'Groups → permission sets'),
        bMid(B3_L, B3_R, 'Resource policies: S3/KMS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Trust policy: who assumes'),
        bMid(B2_L, B2_R, 'IdP: Azure AD / Okta'),
        bMid(B3_L, B3_R, 'Access Analyzer: external'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Access keys: rotate/delete'),
        bMid(B2_L, B2_R, 'Permission sets: scoped'),
        bMid(B3_L, B3_R, 'Access Advisor: last used'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cross-acct: sts assume'),
        bMid(B2_L, B2_R, 'Assignment: user+acct+set'),
        bMid(B3_L, B3_R, 'Credential Report: audit'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  IAM manages roles and policies · Identity Center enables SSO'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['IAM', 'IAM Roles', 'IAM Policies', 'Access Keys', 'Cross-Account'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['List users', 'Trust policy', 'Managed: AWS', 'Rotate 90d', 'Trust: sts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Password policy', 'EC2 profile', 'Managed: custom', 'Delete unused', 'assume-role'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['MFA: enforce', 'X-acct assume', 'Inline: tight', 'Inventory: all', 'External ID'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Credential report', 'Lambda role', 'Boundary: max', 'Cred report', 'Session tags'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS IAM global service · IAM Identity Center in management account · STS regional endpoints'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('IAM Role       = Identity with trust policy; assumed by services, users, or other accounts for temp'))
    lines.append(txt_row('Trust policy   = JSON document on a role defining who can call sts:AssumeRole on it'))
    lines.append(txt_row('Permission Boundary= IAM policy limiting maximum permissions a role or user can have; reduces blast'))
    lines.append(txt_row('IAM Identity Center= AWS SSO; centralises human access to accounts via groups and permission sets'))
    lines.append(txt_row('Permission set = Collection of IAM policies assigned to a user/group for one or more accounts via SSO'))
    lines.append(txt_row('Access Analyzer= Identifies resources shared outside the account or org; detects unintended external'))
    lines.append(txt_row('Access Advisor  = Shows last service access dates per role; helps prune unused permissions'))
    lines.append(txt_row('Credential Report= CSV listing all IAM users, key age, MFA status, and last login per account'))
    lines.append(txt_row('Instance profile= IAM role wrapper for EC2; metadata endpoint exposes temporary credentials to the OS'))
    lines.append(txt_row('Cross-account role= Role in account B trusted by account A; enables resource sharing without key'))
    lines.append(txt_row('STS            = Security Token Service; issues temporary credentials for assume-role and federation'))
    lines.append(txt_row('External ID    = Secret added to cross-account trust policy; prevents confused deputy attacks'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aws-monitoring',
    'docs/cloud/aws/monitoring/index.md',
    'AWS Monitoring — CloudWatch metrics/logs/alarms, CloudTrail, EventBridge, AWS Health',
)
def aws_monitoring_overview():
    """AWS Monitoring Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Monitoring Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Monitoring — CloudWatch, CloudTrail, and EventBridge')))
    lines.append(R(bMid(IV_L, IV_R, 'CloudWatch: metrics, logs, alarms, dashboards — native to every AWS service; no agent for')))
    lines.append(R(bMid(IV_L, IV_R, 'CloudWatch Agent: installs on EC2 for OS-level metrics (memory, disk) and custom log forwarding')))
    lines.append(R(bMid(IV_L, IV_R, 'CloudTrail: API audit log; every AWS API call recorded; multi-region trail ships to S3 +')))
    lines.append(R(bMid(IV_L, IV_R, 'EventBridge: event bus routing rules to targets (Lambda, SNS, SQS, Step Functions,')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  CloudWatch collects metrics/logs · CloudTrail audits API calls'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CloudWatch'),
        bMid(B2_L, B2_R, 'CloudTrail'),
        bMid(B3_L, B3_R, 'EventBridge'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Metrics: service built-in'),
        bMid(B2_L, B2_R, 'API calls: all services'),
        bMid(B3_L, B3_R, 'Event bus: default + custom'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Logs: groups + retention'),
        bMid(B2_L, B2_R, 'Multi-region trail: org'),
        bMid(B3_L, B3_R, 'Rules: event pattern match'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alarms: threshold → SNS'),
        bMid(B2_L, B2_R, 'S3: log delivery + lock'),
        bMid(B3_L, B3_R, 'Targets: Lambda/SQS/SNS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Dashboards: metric tiles'),
        bMid(B2_L, B2_R, 'Log integrity validation'),
        bMid(B3_L, B3_R, 'Schedule: cron-like rules'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Metric filters: log→metric'),
        bMid(B2_L, B2_R, 'Athena: query trail logs'),
        bMid(B3_L, B3_R, 'X-acct event bus pipe'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  CloudWatch collects and alerts · CloudTrail records who did what · EventBridge automates responses'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CloudWatch', 'CW Logs', 'CW Alarms', 'CloudTrail', 'EventBridge'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Metric: CPUUtil', 'Log group: 30d', 'Alarm: CPU>80%', 'Org trail: all', 'Rule: EC2 stop'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Dashboard: ops', 'Metric filter', 'Action: SNS', 'S3 delivery', 'Target: Lambda'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Agent: mem/disk', 'Insights: query', 'Composite alarm', 'Athena query', 'Schedule rule'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AWS Health: svc', 'Subscription flt', 'OK → ALARM', 'Integrity check', 'X-acct pipe'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS CloudWatch backend · S3 for CloudTrail · EventBridge event bus infrastructure · SNS topics'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CloudWatch metrics = Time-series data from AWS services; 1-min granularity; stored 15 months'))
    lines.append(txt_row('Log group         = CloudWatch Logs container for streams; retention 1 day–10 years or indefinite'))
    lines.append(txt_row('Metric filter     = Extracts numeric values from log events and publishes them as CloudWatch metrics'))
    lines.append(txt_row('CW Alarm          = Watches a metric or expression; transitions OK/ALARM/INSUFFICIENT; triggers'))
    lines.append(txt_row('Composite alarm   = AND/OR combination of alarms; reduces alert noise from correlated conditions'))
    lines.append(txt_row('CloudTrail        = Records management events (API calls) and optionally data events (S3/Lambda)'))
    lines.append(txt_row('Org trail         = Single CloudTrail covering all accounts in the AWS Organization; recommended'))
    lines.append(txt_row('Log file integrity= CloudTrail SHA-256 hash validation; detects tampered or deleted log files'))
    lines.append(txt_row('EventBridge rule  = Pattern-matches incoming events and routes them to one or more targets'))
    lines.append(txt_row('AWS Health        = Service health and scheduled events for your specific AWS account and resources'))
    lines.append(txt_row('CloudWatch Agent  = Daemon on EC2/on-prem; collects OS metrics (memory, disk) and custom log files'))
    lines.append(txt_row('Logs Insights     = Interactive CloudWatch Logs query engine; KQL-like syntax; serverless execution'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aws-networking',
    'docs/cloud/aws/networking/index.md',
    'AWS Networking — VPC, subnets, SGs, NACLs, TGW, DirectConnect, VPC Endpoints, ALB',
)
def aws_networking_overview():
    """AWS Networking Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Networking Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Networking — VPC, Transit Gateway, Security, and Connectivity')))
    lines.append(R(bMid(IV_L, IV_R, 'VPC: isolated virtual network per account+region; CIDR block /16–/28; multi-AZ subnet design')))
    lines.append(R(bMid(IV_L, IV_R, 'Transit Gateway: regional hub connecting VPCs + DirectConnect + VPN; route tables per TGW')))
    lines.append(R(bMid(IV_L, IV_R, 'Security: Security Groups (stateful, per-resource) + NACLs (stateless, per-subnet)')))
    lines.append(R(bMid(IV_L, IV_R, 'VPC Endpoints: private access to S3, DynamoDB, and 150+ services without internet gateway')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  VPC is the foundation · TGW connects VPCs and on-prem · SGs+NACLs protect resources'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VPC & Subnets'),
        bMid(B2_L, B2_R, 'Security Controls'),
        bMid(B3_L, B3_R, 'Connectivity'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VPC: CIDR /16-/28'),
        bMid(B2_L, B2_R, 'Security Groups: stateful'),
        bMid(B3_L, B3_R, 'Internet Gateway: public'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Public subnet: IGW route'),
        bMid(B2_L, B2_R, 'NACLs: stateless + order'),
        bMid(B3_L, B3_R, 'NAT Gateway: private out'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Private subnet: no IGW'),
        bMid(B2_L, B2_R, 'Flow Logs: VPC traffic'),
        bMid(B3_L, B3_R, 'Transit Gateway: hub'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Route tables: subnet assoc'),
        bMid(B2_L, B2_R, 'Network Firewall: L7'),
        bMid(B3_L, B3_R, 'DirectConnect: private'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VPC Endpoints: private SVC'),
        bMid(B2_L, B2_R, 'WAF: ALB / CloudFront'),
        bMid(B3_L, B3_R, 'VPN: site-to-site IPsec'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  VPC/subnets define the network · Security controls filter traffic'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VPC', 'Subnets', 'Security Groups', 'Routing', 'Load Balancer'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CIDR: plan /16', 'Public: AZ-a/b/c', 'Inbound rules', 'IGW route: 0/0', 'ALB: L7 HTTP/S'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Flow Logs: S3', 'Private: no IGW', 'Outbound rules', 'NAT: 0/0 priv', 'NLB: L4 TCP'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['DNS: enableDNS', 'Multi-AZ design', 'Ref by SG ID', 'TGW attachment', 'Route 53: DNS'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Endpoint: S3/SVC', 'NACL: stateless', 'All-outbound: no', 'VPN: DX backup', 'Health checks'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS network fabric · Availability Zones · DirectConnect physical ports · Transit Gateway routers'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VPC            = Virtual Private Cloud; logically isolated network within a region; one CIDR block'))
    lines.append(txt_row('Subnet         = CIDR subdivision of a VPC; lives in one AZ; public if route to IGW exists'))
    lines.append(txt_row('Security Group = Stateful firewall attached to ENI; return traffic automatically allowed'))
    lines.append(txt_row('NACL           = Network Access Control List; stateless; rules evaluated in order; both in and out'))
    lines.append(txt_row('Internet Gateway= Allows resources in public subnets to reach the internet; 1:1 to a VPC'))
    lines.append(txt_row('NAT Gateway    = Allows private subnet resources to initiate outbound internet; blocks inbound'))
    lines.append(txt_row('Transit Gateway= Regional router connecting VPCs and on-premises networks; route tables per TGW'))
    lines.append(txt_row('VPC Endpoint   = Private connection to AWS services (S3, DynamoDB, etc.) without leaving AWS network'))
    lines.append(txt_row('VPC Flow Logs  = Captures network flow metadata for VPC, subnet, or ENI; written to S3 or CW Logs'))
    lines.append(txt_row('DirectConnect  = Dedicated 1/10/100 Gbps private link from on-premises to AWS; lower latency than VPN'))
    lines.append(txt_row('ALB            = Application Load Balancer; Layer 7; supports path/host routing, WAF integration'))
    lines.append(txt_row('Route 53       = AWS managed DNS; supports public/private zones, health checks, failover routing'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aws-operations',
    'docs/cloud/aws/operations/index.md',
    'AWS Operations — health checks, procedures, Patch Manager, backup/restore, automation',
)
def aws_operations_overview():
    """AWS Operations Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Operations Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Operations — Health Checks, Procedures, Patching, and Automation')))
    lines.append(R(bMid(IV_L, IV_R, 'Health Checks: EC2 status checks · RDS availability · CloudWatch alarm state · AWS Health')))
    lines.append(R(bMid(IV_L, IV_R, 'Procedures: instance lifecycle, AMI management, EBS expansion, ASG scaling, RDS failover')))
    lines.append(R(bMid(IV_L, IV_R, 'Patching: Systems Manager Patch Manager applies OS patches on schedule; compliance reporting')))
    lines.append(R(bMid(IV_L, IV_R, 'Backup/Restore: AWS Backup jobs · EBS snapshot restore · RDS point-in-time recovery')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Health checks prevent failures · Procedures execute changes safely'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Health Checks'),
        bMid(B2_L, B2_R, 'Procedures'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'EC2 status: 2/2 checks'),
        bMid(B2_L, B2_R, 'Start/stop/reboot EC2'),
        bMid(B3_L, B3_R, 'SSM Run Command: fleet'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RDS: available + IOPS'),
        bMid(B2_L, B2_R, 'Resize: instance type'),
        bMid(B3_L, B3_R, 'EventBridge: auto-trigger'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CW Alarms: OK vs ALARM'),
        bMid(B2_L, B2_R, 'EBS: extend + resize fs'),
        bMid(B3_L, B3_R, 'Lambda: remediation fn'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AWS Health: svc events'),
        bMid(B2_L, B2_R, 'ASG: refresh instances'),
        bMid(B3_L, B3_R, 'CloudFormation: IaC drift'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'TGW + VPN: BGP sessions'),
        bMid(B2_L, B2_R, 'RDS failover: promote'),
        bMid(B3_L, B3_R, 'Step Functions: workflow'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Health checks detect issues · Procedures resolve them'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Health Checks', 'Procedures', 'Patching', 'Backup/Restore', 'Scripts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['EC2 2/2 OK?', 'AMI: create', 'Patch baseline', 'Backup job: run', 'CLI: describe'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CW alarms: OK', 'EBS: extend', 'Patch window', 'EBS snap restore', 'Boto3: boto3'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['RDS: available', 'ASG: refresh', 'Compliance: view', 'RDS PITR', 'SSM scripts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AWS Health: evts', 'RDS failover', 'Reboot if needed', 'Cross-region: cp', 'CDK / TF'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('EC2 hosts on Nitro · EBS storage fabric · RDS managed infrastructure · AZs for HA · VPC networking'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('EC2 status checks = System check (AWS infra) + instance check (OS/app); both must pass (2/2)'))
    lines.append(txt_row('AWS Health        = Personalised service health and maintenance events for your account and resources'))
    lines.append(txt_row('Patch Manager     = SSM feature; applies OS patches per baseline; records compliance per instance'))
    lines.append(txt_row('Patch baseline    = Defines which patches to install; AWS-managed or custom per OS and severity'))
    lines.append(txt_row('AMI               = Amazon Machine Image; golden image snapshot; used for ASG instance refresh'))
    lines.append(txt_row('ASG instance refresh= Rolling replacement of instances in an ASG with a new launch template version'))
    lines.append(txt_row('EBS expansion     = Increase volume size; then extend filesystem (growpart + resize2fs or diskpart)'))
    lines.append(txt_row('RDS PITR          = Point-in-time recovery; restore RDS to any second within the retention window'))
    lines.append(txt_row('CloudFormation drift= Detects manual changes to stack resources not captured in the template'))
    lines.append(txt_row('Step Functions    = AWS serverless workflow orchestrator; chains Lambda, SSM, ECS tasks with retries'))
    lines.append(txt_row('Run Command       = SSM feature executing commands/scripts on EC2 fleet; no SSH or VPN needed'))
    lines.append(txt_row('EventBridge rule  = Triggers Lambda/SSM/SQS on schedule or event pattern; enables auto-remediation'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aws-security',
    'docs/cloud/aws/security/index.md',
    'AWS Security — IAM IC SSO, MFA, KMS, Secrets Manager, ACM, GuardDuty, Security Hub',
)
def aws_security_overview():
    """AWS Security Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Security Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Security — Authentication, Encryption, and Threat Detection')))
    lines.append(R(bMid(IV_L, IV_R, 'Authentication: IAM Identity Center SSO · MFA enforcement · no shared credentials; roles only')))
    lines.append(R(bMid(IV_L, IV_R, 'Encryption: KMS for data-at-rest · ACM for TLS certificates · Secrets Manager for credentials')))
    lines.append(R(bMid(IV_L, IV_R, 'Threat detection: GuardDuty (ML-based) · Security Hub (posture) · Inspector (vulnerability')))
    lines.append(R(bMid(IV_L, IV_R, 'Preventive guardrails: SCPs limit service/region access · Config rules detect drift · WAF')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication controls access · Encryption protects data'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Encryption'),
        bMid(B3_L, B3_R, 'Threat Detection'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'IAM Identity Center SSO'),
        bMid(B2_L, B2_R, 'KMS: CMK + AWS managed'),
        bMid(B3_L, B3_R, 'GuardDuty: ML threat'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'MFA: virtual or hardware'),
        bMid(B2_L, B2_R, 'Secrets Manager: rotate'),
        bMid(B3_L, B3_R, 'Security Hub: score'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Roles: no long-lived keys'),
        bMid(B2_L, B2_R, 'ACM: TLS certs managed'),
        bMid(B3_L, B3_R, 'Inspector: CVE scanning'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SCP: deny root actions'),
        bMid(B2_L, B2_R, 'S3: SSE-S3 / SSE-KMS'),
        bMid(B3_L, B3_R, 'Config: drift detection'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Access Analyzer: review'),
        bMid(B2_L, B2_R, 'EBS/RDS: encrypt at rest'),
        bMid(B3_L, B3_R, 'WAF: ALB + CloudFront'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication + SCPs prevent access · Encryption protects data'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Authentication', 'Access Control', 'Encryption', 'Hardening', 'Certificate Mgr'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SSO: IAM IC', 'Roles: least priv', 'KMS: CMK create', 'GuardDuty: org', 'ACM: request'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['MFA: enforce all', 'SCP: deny risky', 'Secrets: rotate', 'Security Hub', 'Auto-renew: yes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['No shared keys', 'Boundary: set', 'S3 SSE-KMS', 'Inspector: scan', 'ALB: TLS 1.2+'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['IdP: SAML 2.0', 'Access Analyzer', 'EBS: encrypted', 'Config: rules', 'DNS valid: txt'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AWS security regions · KMS hardware security modules · CloudFront edge for WAF'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('KMS             = Key Management Service; create and manage CMKs for encryption across AWS services'))
    lines.append(txt_row('CMK             = Customer Managed Key; KMS key you control; used for S3, EBS, RDS, Secrets Manager'))
    lines.append(txt_row('Secrets Manager = Manages credentials, API keys, and passwords; auto-rotates via Lambda integration'))
    lines.append(txt_row('ACM             = AWS Certificate Manager; provisions and auto-renews TLS certificates for ALB/CF'))
    lines.append(txt_row('GuardDuty       = ML-based threat detection; analyses CloudTrail, VPC Flow Logs, and DNS logs'))
    lines.append(txt_row('Security Hub    = Aggregates findings; computes security score against CIS, PCI-DSS, AWS Foundational'))
    lines.append(txt_row('Inspector       = Automated vulnerability scanner for EC2 OS CVEs and container image vulnerabilities'))
    lines.append(txt_row('WAF             = Web Application Firewall; Layer 7 rules for ALB, API Gateway, and CloudFront'))
    lines.append(txt_row('SSE-KMS         = Server-side encryption with KMS CMK; allows key policy + CloudTrail audit of usage'))
    lines.append(txt_row('Permission Boundary= IAM policy capping maximum permissions; limits blast radius of over-provisioned'))
    lines.append(txt_row('Access Analyzer = IAM service that finds externally-accessible resources; generates least-priv'))
    lines.append(txt_row('IAM Identity Center= SSO for human access; enforces MFA; integrates with Okta/Azure AD via SAML/SCIM'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aws-storage',
    'docs/cloud/aws/storage/index.md',
    'AWS Storage — EBS (gp3/io2), S3 (classes/lifecycle/replication), EFS, FSx',
)
def aws_storage_overview():
    """AWS Storage Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Storage Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Storage — EBS, S3, EFS, and FSx')))
    lines.append(R(bMid(IV_L, IV_R, 'EBS: persistent block volumes attached to EC2; types gp3/io2/sc1/st1; AZ-locked; snapshots to')))
    lines.append(R(bMid(IV_L, IV_R, 'S3: unlimited object storage; 11 nines durability; lifecycle, versioning, replication, and')))
    lines.append(R(bMid(IV_L, IV_R, 'EFS: managed NFS for Linux; multi-AZ shared filesystem; provisioned or bursting throughput')))
    lines.append(R(bMid(IV_L, IV_R, 'FSx: managed Windows SMB (FSx for Windows) and HPC Lustre (FSx for Lustre) file systems')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  EBS serves block I/O for EC2 · S3 stores objects durably · EFS/FSx serve shared file workloads'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'EBS'),
        bMid(B2_L, B2_R, 'S3'),
        bMid(B3_L, B3_R, 'EFS / FSx'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Types: gp3/io2/st1/sc1'),
        bMid(B2_L, B2_R, 'Buckets: region-scoped'),
        bMid(B3_L, B3_R, 'EFS: NFS v4.1 + 4.2'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'IOPS: gp3=3K, io2=64K'),
        bMid(B2_L, B2_R, 'Storage classes: S/IA/GDA'),
        bMid(B3_L, B3_R, 'FSx Windows: SMB AD'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Encrypt: CMK default'),
        bMid(B2_L, B2_R, 'Versioning: protect objs'),
        bMid(B3_L, B3_R, 'FSx Lustre: HPC Gbps'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Snapshots: S3-backed copy'),
        bMid(B2_L, B2_R, 'Lifecycle: tier+expire'),
        bMid(B3_L, B3_R, 'EFS: bursting throughput'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Resize: online (no reboot)'),
        bMid(B2_L, B2_R, 'Replication: X-region'),
        bMid(B3_L, B3_R, 'Mount: NFS or DFS-N'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  EBS for EC2 block I/O · S3 for durable objects and lifecycle'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['EBS', 'EBS Snapshots', 'S3', 'S3 Lifecycle', 'EFS / FSx'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['gp3: baseline', 'Create snap', 'Bucket: create', 'Transition rule', 'Mount target'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['io2: 64K IOPS', 'AMI from snap', 'Block public', 'Expire: delete', 'EFS SG rules'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Resize: no stop', 'Cross-region cp', 'Object lock', 'IA: 30d+ infreq', 'FSx: AD join'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Encrypt at rest', 'Retention: policy', 'Replication: CRR', 'GDA: 90d+ cold', 'FSx backup'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('EBS storage fabric (AZ-local) · S3 distributed storage (region) · EFS/FSx managed NAS infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('EBS            = Elastic Block Store; persistent block volumes; AZ-locked; attach to one EC2 at a'))
    lines.append(txt_row('gp3            = General Purpose SSD v3; 3,000 IOPS and 125 MiB/s baseline; independently'))
    lines.append(txt_row('io2            = Provisioned IOPS SSD; up to 64,000 IOPS; 99.999% durability; multi-attach supported'))
    lines.append(txt_row('EBS Snapshot   = Incremental S3-backed copy of a volume; used for backup, AMI creation, region copy'))
    lines.append(txt_row('S3             = Simple Storage Service; object storage; buckets in a region; 11 nines durability'))
    lines.append(txt_row('S3 Storage Class= Tiers: Standard / Standard-IA / Glacier Instant / Glacier DA / Glacier Deep Archive'))
    lines.append(txt_row('S3 Lifecycle   = Rules transitioning objects between classes or expiring them after N days'))
    lines.append(txt_row('S3 Replication = CRR (cross-region) or SRR (same-region); requires versioning on source bucket'))
    lines.append(txt_row('EFS            = Elastic File System; serverless NFS; multi-AZ; auto-scales; mount via EFS mount'))
    lines.append(txt_row('FSx for Windows= Managed SMB file share with Active Directory integration; DFS namespace support'))
    lines.append(txt_row('FSx for Lustre = High-performance parallel file system; used for ML training and HPC workloads'))
    lines.append(txt_row('Object Lock    = S3 WORM; Governance or Compliance mode; prevents delete/overwrite for retention'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aws-troubleshooting',
    'docs/cloud/aws/troubleshooting/index.md',
    'AWS Troubleshooting — common issues, Policy Simulator, Reachability Analyzer, CloudTrail',
)
def aws_troubleshooting_overview():
    """AWS Troubleshooting Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'AWS Troubleshooting Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AWS Troubleshooting — Common Issues, Diagnostics, and Escalation')))
    lines.append(R(bMid(IV_L, IV_R, 'Common issues: IAM permission denied · SG/NACL blocking traffic · EC2 instance unreachable')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnostics: CloudWatch Logs · CloudTrail event history · VPC Flow Logs · EC2 serial console')))
    lines.append(R(bMid(IV_L, IV_R, 'Tools: AWS CLI describe commands · Policy Simulator · Reachability Analyzer · CloudShell')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: AWS Support cases; collect account ID, region, resource ARN, error message + time')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide investigation · Diagnostics locate root cause · Escalation engages AWS support'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'EC2: 2/2 status fail'),
        bMid(B2_L, B2_R, 'CW Logs: app errors'),
        bMid(B3_L, B3_R, 'Account ID + region'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SG: port not open'),
        bMid(B2_L, B2_R, 'CloudTrail: API history'),
        bMid(B3_L, B3_R, 'Resource ARN: include'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'IAM: Access Denied'),
        bMid(B2_L, B2_R, 'VPC Flow Logs: traffic'),
        bMid(B3_L, B3_R, 'Error message + time'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RDS: conn refused'),
        bMid(B2_L, B2_R, 'Policy Simulator: test'),
        bMid(B3_L, B3_R, 'Severity: P1-P4'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'S3: 403 on object'),
        bMid(B2_L, B2_R, 'Reachability Analyzer'),
        bMid(B3_L, B3_R, 'TAM: strategic issues'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Identify issue category → gather diagnostics (logs + trail + flow) → resolve or escalate with data'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Escalation', 'CLI Tools', 'Console Tools'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['EC2 unreachable', 'CW Logs: filter', 'P1: 24/7 phone', 'describe-sgs', 'Policy Simulator'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SG: missing rule', 'CloudTrail: who?', 'Case: open now', 'flow-logs: get', 'Reach Analyzer'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['IAM: denied', 'VPC Flow Logs', 'ARN + error msg', 'sts get-caller', 'EC2 serial con'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['S3: bucket ACL', 'Serial console', 'Trusted Advisor', 'ec2 describe', 'AWS Health evt'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('EC2 Nitro hosts · VPC network fabric · AWS Support infrastructure · CloudTrail S3 log delivery'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('EC2 status check = System check (infra) + instance check (OS); failure triggers alarm or'))
    lines.append(txt_row('Policy Simulator = IAM console tool; tests IAM policies to check if an action would be allowed/denied'))
    lines.append(txt_row('Reachability Analyzer= VPC tool; traces packet path between source and destination; finds blocking'))
    lines.append(txt_row('VPC Flow Logs   = Captures accepted/rejected traffic metadata for subnets, VPCs, or ENIs'))
    lines.append(txt_row('CloudTrail      = Records every AWS API call; start with event history for the last 90 days in'))
    lines.append(txt_row('EC2 Serial Console= Out-of-band console access; useful when SSH/SSM unreachable; OS-level triage'))
    lines.append(txt_row('Trusted Advisor  = AWS checks across cost, security, performance, fault tolerance, and service limits'))
    lines.append(txt_row('P1 case          = Production down; 24/7 response; call +1-800-xxx alongside opening console case'))
    lines.append(txt_row('TAM              = Technical Account Manager; named AWS contact for strategic and critical escalation'))
    lines.append(txt_row('sts get-caller-identity= CLI command returning current identity; first step when debugging IAM issues'))
    lines.append(txt_row('Session Manager  = SSM feature; connect to EC2 without SSH when networking is broken but SSM agent'))
    lines.append(txt_row('Access Denied    = IAM error; check CloudTrail for the denied call; use Policy Simulator to trace'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Azure sub-section diagrams ─────────────────────────────────────────────────

@kb_diagram(
    'azure-architecture',
    'docs/cloud/azure/architecture/index.md',
    'Azure Architecture Overview — tenant hierarchy, hub-spoke VNet, Entra ID, Availability Zones',
)
def azure_architecture_overview():
    """Azure Architecture Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Platform Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Platform Architecture — Management Hierarchy, Networking, and Identity')))
    lines.append(R(bMid(IV_L, IV_R, 'Hierarchy: Tenant > Management Groups > Subscriptions > Resource Groups > Resources')))
    lines.append(R(bMid(IV_L, IV_R, 'Networking: hub-and-spoke VNet peering; hub holds shared services (firewall, DNS, VPN gateway)')))
    lines.append(R(bMid(IV_L, IV_R, 'Identity: Entra ID (formerly Azure AD); SSO, MFA, Conditional Access, PIM for privileged roles')))
    lines.append(R(bMid(IV_L, IV_R, 'Guardrails: Azure Policy (detective + preventive) · RBAC · Management Group scope policies')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Hierarchy provides scope · Hub-spoke networking connects workloads · Entra ID governs all identity'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Mgmt Groups: org scope'),
        bMid(B2_L, B2_R, 'ExpressRoute: on-prem'),
        bMid(B3_L, B3_R, 'Naming: RG + resource std'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Subscriptions: isolation'),
        bMid(B2_L, B2_R, 'IdP: on-prem AD + Entra'),
        bMid(B3_L, B3_R, 'Tagging: env+owner+team'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Hub VNet: shared services'),
        bMid(B2_L, B2_R, 'Monitoring: Azure Monitor'),
        bMid(B3_L, B3_R, 'Subscription design: prod'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Spoke VNets: workloads'),
        bMid(B2_L, B2_R, 'Security: Defender + SIEM'),
        bMid(B3_L, B3_R, 'Security baseline: CIS Az'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Availability Zones: 3 per'),
        bMid(B2_L, B2_R, 'Billing: Cost Management'),
        bMid(B3_L, B3_R, 'HA: zone + region pattern'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines hierarchy and networking · Integrations connect on-prem'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Hierarchy', 'Networking', 'Identity', 'Guardrails', 'Availability'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Tenant: root', 'Hub VNet: fw', 'Entra ID: IdP', 'Policy: deny', 'Zones: 3 AZ'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Mgmt Groups', 'Spoke: app', 'RBAC: scope', 'Initiative', 'Regions: pair'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Subscriptions', 'Peering: hub', 'PIM: JIT', 'Compliance', 'ASR: failover'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Resource Groups', 'ExpressRoute', 'Cond. Access', 'RBAC assign', 'LB + AG: HA'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure Regions · Availability Zones · Data Centres · Global WAN backbone · ExpressRoute physical ports'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Management Group  = Scope above subscriptions; policies and RBAC applied here cascade to all children'))
    lines.append(txt_row('Subscription      = Billing unit and access boundary; resources live inside subscriptions'))
    lines.append(txt_row('Resource Group    = Logical container for resources; lifecycle boundary; RBAC and policy scope'))
    lines.append(txt_row('Entra ID          = Microsoft cloud identity (formerly Azure AD); directory for users, groups, apps'))
    lines.append(txt_row('Hub-spoke VNet    = Hub has shared services (firewall, DNS); spokes peer to hub for connectivity'))
    lines.append(txt_row('VNet peering      = Private connectivity between VNets; traffic stays on Microsoft backbone'))
    lines.append(txt_row('ExpressRoute      = Dedicated private circuit from on-premises to Azure; Layer 2/3; bypasses internet'))
    lines.append(txt_row('Azure Policy      = Governance service; defines and enforces compliance rules across resource configs'))
    lines.append(txt_row('RBAC              = Role-Based Access Control; Owner/Contributor/Reader built-in + custom roles'))
    lines.append(txt_row('PIM               = Privileged Identity Management; just-in-time role activation; approval + audit'))
    lines.append(txt_row('Availability Zone = Physically separate DC within a region; independent power/cooling/networking'))
    lines.append(txt_row('Conditional Access = Entra ID policy engine; evaluates sign-in context to enforce MFA, block, or'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'azure-backup-dr',
    'docs/cloud/azure/backup-dr/index.md',
    'Azure Backup & DR — Azure Backup, RSV, ASR replication, failover/failback, test failover',
)
def azure_backup_dr_overview():
    """Azure Backup and DR Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Backup and DR Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Backup and DR — Recovery Services Vault, Azure Backup, and Azure Site Recovery')))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Backup: VM, SQL, SAP, files, blobs — all via Recovery Services Vault; policy-driven')))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Site Recovery (ASR): continuous replication; orchestrated failover + failback for VMs')))
    lines.append(R(bMid(IV_L, IV_R, 'Recovery Services Vault: central container for backup items and ASR replication configs')))
    lines.append(R(bMid(IV_L, IV_R, 'Restore testing: mandatory for RTO/RPO validation; test failover in isolated network (ASR)')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Backup policies protect data · ASR replicates VMs for DR'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Azure Backup'),
        bMid(B2_L, B2_R, 'Recovery Svc Vault'),
        bMid(B3_L, B3_R, 'Azure Site Recovery'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VM: daily + weekly'),
        bMid(B2_L, B2_R, 'GRS: geo-redundant'),
        bMid(B3_L, B3_R, 'Replication: Azure→Az'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SQL/SAP: log backup'),
        bMid(B2_L, B2_R, 'Soft delete: 14d'),
        bMid(B3_L, B3_R, 'RPO: ~30 seconds'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Files/blobs: policy'),
        bMid(B2_L, B2_R, 'Immutability: WORM'),
        bMid(B3_L, B3_R, 'Failover: 1-click plan'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Backup jobs: monitor'),
        bMid(B2_L, B2_R, 'Access policy: RBAC'),
        bMid(B3_L, B3_R, 'Test failover: isolated'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Restore: disk or full VM'),
        bMid(B2_L, B2_R, 'Reports: backup health'),
        bMid(B3_L, B3_R, 'Failback: re-protect'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Backup protects point-in-time data · Vault stores recovery points · ASR enables DR orchestration'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Azure Backup', 'RSV', 'ASR', 'Restore Test', 'Compliance'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VM: enable', 'GRS setting', 'Enable repltn', 'Test failover', 'Backup report'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Policy: daily', 'Soft delete', 'RPO: monitor', 'Validate: app', 'Policy coverage'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Job: monitor', 'Immutability', 'Failover plan', 'RTO measured', 'Gaps: alert'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Restore: VM', 'RBAC: ops', 'Re-protect', 'Cleanup test', 'Audit: vault'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure Storage (GRS vaults) · ASR replication infrastructure · paired regions · VM host fabric'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Recovery Services Vault= Azure container for backup items and ASR replication configs; scoped per'))
    lines.append(txt_row('Azure Backup    = Managed backup for VMs, SQL, SAP, files, blobs; policy-driven; encrypted at rest'))
    lines.append(txt_row('Backup Policy   = Defines schedule (daily/weekly) and retention (daily/weekly/monthly/yearly)'))
    lines.append(txt_row('Soft delete     = 14-day recovery window after accidental backup item deletion; default enabled'))
    lines.append(txt_row('Immutability    = WORM policy on vault; prevents deletion of recovery points; compliance requirement'))
    lines.append(txt_row('GRS             = Geo-Redundant Storage; vault data replicated to paired region; 6 copies total'))
    lines.append(txt_row('Azure Site Recovery= Continuous replication of VMs to another region; orchestrated failover/failback'))
    lines.append(txt_row('RPO             = Recovery Point Objective; ASR achieves ~30s RPO for Azure-to-Azure VM replication'))
    lines.append(txt_row('Test failover   = ASR feature; spins up replica VM in isolated VNet; validates app without affecting'))
    lines.append(txt_row('Failback        = Re-protecting and reversing replication direction after a failover test or real'))
    lines.append(txt_row('Recovery plan   = ASR orchestration of failover order, scripts, and timing for multi-VM workloads'))
    lines.append(txt_row('Replication health= ASR metric; monitors churn rate, RPO breach, and agent connectivity on source VM'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'azure-cli',
    'docs/cloud/azure/cli-reference/index.md',
    'Azure CLI Reference — az login, az vm/storage/network/backup/identity commands',
)
def azure_cli_reference():
    """Azure CLI Reference — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure CLI Reference'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure CLI — az command-line tool for managing Azure resources')))
    lines.append(R(bMid(IV_L, IV_R, 'Structured as: az <group> <command> [--options] — e.g. az vm list --resource-group myRG')))
    lines.append(R(bMid(IV_L, IV_R, 'Auth: az login (browser) · az login --service-principal · az account set --subscription <id>')))
    lines.append(R(bMid(IV_L, IV_R, 'Output formats: --output json (default) | table | tsv | yaml | none')))
    lines.append(R(bMid(IV_L, IV_R, 'Query: --query uses JMESPath; e.g. --query "[?powerState==`VM running`].name" -o tsv')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  az CLI organises by resource type — vm, network, storage, account, backup, monitor, identity, aks'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Compute (VM/AKS)'),
        bMid(B2_L, B2_R, 'Storage / Disks'),
        bMid(B3_L, B3_R, 'Identity / Network'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'az vm list/show/start'),
        bMid(B2_L, B2_R, 'az storage account ls'),
        bMid(B3_L, B3_R, 'az ad user/group list'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'az vm stop/deallocate'),
        bMid(B2_L, B2_R, 'az disk list/create'),
        bMid(B3_L, B3_R, 'az role assignment list'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'az vm resize/create'),
        bMid(B2_L, B2_R, 'az snapshot create'),
        bMid(B3_L, B3_R, 'az network vnet list'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'az aks get-credentials'),
        bMid(B2_L, B2_R, 'az storage blob up/down'),
        bMid(B3_L, B3_R, 'az network nsg rule list'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'az vm run-command'),
        bMid(B2_L, B2_R, 'az keyvault secret get'),
        bMid(B3_L, B3_R, 'az monitor alert list'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Compute CLI manages VMs/AKS · Storage CLI handles blobs and disks'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Account', 'Virtual Machines', 'Storage', 'Networking', 'Backup / KV'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['az login', 'vm list --rg', 'blob upload', 'vnet list', 'backup item ls'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['account set', 'vm start/stop', 'blob download', 'nsg rule add', 'kv secret get'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['account list', 'vm resize', 'disk create', 'lb list', 'backup protect'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['sp create', 'vm run-cmd', 'snapshot cp', 'vnet peering', 'kv key list'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure Resource Manager API · Azure AD token endpoint · Azure CloudShell or local workstation'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Azure CLI v2     = Current az CLI; install via Homebrew/apt/pip; az --version to verify'))
    lines.append(txt_row('az login         = Browser-based interactive login; stores token in ~/.azure/; expires after 1 hour'))
    lines.append(txt_row('Service principal= Non-human identity; use az login --service-principal for automation'))
    lines.append(txt_row('az account set   = Switch active subscription; use with --subscription <name or id>'))
    lines.append(txt_row('--resource-group = Required for most resource commands; shorthand --g; targets RG scope'))
    lines.append(txt_row('--query          = JMESPath filter on JSON output; e.g. [].name for list of resource names'))
    lines.append(txt_row('--output table   = Renders JSON as a formatted table; useful for terminal readability'))
    lines.append(txt_row('az vm run-command= Execute a script inside a VM via VM agent; works without SSH or port access'))
    lines.append(txt_row('az configure     = Set default resource group, output format, and location for the CLI session'))
    lines.append(txt_row('CloudShell       = Browser-based shell in Azure portal; pre-authenticated; az available by default'))
    lines.append(txt_row('--no-wait        = Submits a long-running operation without blocking the terminal; async execution'))
    lines.append(txt_row('az find          = AI-powered CLI helper; suggests relevant commands for a given scenario'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'azure-compute',
    'docs/cloud/azure/compute/index.md',
    'Azure Compute Overview — VMs, Availability Sets/Zones, VMSS, Update Manager, extensions',
)
def azure_compute_overview():
    """Azure Compute Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Compute Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Compute — Virtual Machines, Scale Sets, Availability, and Fleet Management')))
    lines.append(R(bMid(IV_L, IV_R, 'Virtual Machines: Windows and Linux VMs; 800+ sizes; Availability Zones for HA deployment')))
    lines.append(R(bMid(IV_L, IV_R, 'VM Scale Sets: auto-scaling fleet; uniform or flexible orchestration; custom or platform images')))
    lines.append(R(bMid(IV_L, IV_R, 'Availability: Zones (physically isolated) and Sets (fault/update domains) for redundancy')))
    lines.append(R(bMid(IV_L, IV_R, 'Fleet ops: Azure Update Manager (patching) · Extensions (monitoring, DSC) · Boot diagnostics')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  VMs provide compute · Scale Sets enable elasticity · Availability features ensure HA deployments'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Virtual Machines'),
        bMid(B2_L, B2_R, 'Availability'),
        bMid(B3_L, B3_R, 'Fleet Management'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Sizes: B/D/E/F families'),
        bMid(B2_L, B2_R, 'Availability Zones: 3'),
        bMid(B3_L, B3_R, 'Update Manager: patch'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'OS disk: managed Premium'),
        bMid(B2_L, B2_R, 'Availability Sets: FD/UD'),
        bMid(B3_L, B3_R, 'Extensions: agent+script'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Image: custom gallery'),
        bMid(B2_L, B2_R, 'VM Scale Sets: VMSS'),
        bMid(B3_L, B3_R, 'Boot diagnostics: serial'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Identity: managed identity'),
        bMid(B2_L, B2_R, 'Zone: PPG for low lat'),
        bMid(B3_L, B3_R, 'Serial console: OOB'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Resize: without data loss'),
        bMid(B2_L, B2_R, 'VMSS: instance refresh'),
        bMid(B3_L, B3_R, 'Inventory: ASC + Defender'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  VMs provide individual compute · Availability features distribute load'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Virtual Machines', 'Avail. Sets', 'Avail. Zones', 'Scale Sets', 'Patching'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Start/stop VM', 'FD: 2-3 racks', 'Zone 1/2/3', 'Min/max count', 'Update Manager'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Resize: portal', 'UD: rolling', 'Zone balance', 'Scale rule: CPU', 'Patch schedule'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Image: capture', 'Use: SAP/SQL', 'Use: web tier', 'Rolling upgrade', 'Compliance'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Boot diag: log', 'SLA: 99.95%', 'SLA: 99.99%', 'Instance refresh', 'Reboot: sched'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure host servers · Availability Zones (physical DCs) · Managed Disk storage fabric'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Availability Set  = Groups VMs across fault domains (rack) and update domains (patch group)'))
    lines.append(txt_row('Availability Zone = Physically separate DC in a region; each with independent power, cooling, network'))
    lines.append(txt_row('VM Scale Set      = VMSS; fleet of identical VMs with auto-scaling; uniform or flexible orchestration'))
    lines.append(txt_row('Managed Identity  = Auto-managed service principal for a VM; used to authenticate to Azure services'))
    lines.append(txt_row('Proximity Placement Group= PPG; co-locates VMs in same data centre for lowest latency between VMs'))
    lines.append(txt_row('Fault Domain      = Rack-level isolation in an Availability Set; typically 2 or 3 per set'))
    lines.append(txt_row('Update Domain     = Rolling maintenance group; Azure updates one UD at a time during planned'))
    lines.append(txt_row('Boot Diagnostics  = Captures VM serial console log and screenshot; diagnoses non-booting VMs'))
    lines.append(txt_row('Serial Console    = Out-of-band console access to VM; works when SSH/RDP unreachable'))
    lines.append(txt_row('Azure Update Manager= Replaces Azure Automation Update Management; patches VMs on schedule at scale'))
    lines.append(txt_row('VM Extension      = Agent-based add-ons; installs monitoring agents, DSC, custom scripts on VMs'))
    lines.append(txt_row('Shared Image Gallery= Azure Compute Gallery; stores versioned custom VM images shared across'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'azure-cost',
    'docs/cloud/azure/cost/index.md',
    'Azure Cost Management — Cost Management, budgets, Reservations, Savings Plans, Advisor',
)
def azure_cost_management():
    """Azure Cost Management — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Cost Management'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Cost Management — Visibility, Budgets, Reservations, and Optimisation')))
    lines.append(R(bMid(IV_L, IV_R, 'Cost Management + Billing: analyse spend by subscription, RG, service, tag, and location')))
    lines.append(R(bMid(IV_L, IV_R, 'Budgets: cost or usage threshold alerts; linked to action groups for email or automation')))
    lines.append(R(bMid(IV_L, IV_R, 'Reservations: 1 or 3-year committed use for VMs, SQL, Storage; up to 72% discount')))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Advisor: right-sizing, RI recommendations, idle resources, and cost savings estimates')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Cost visibility feeds budget alerts · Advisor finds savings · Reservations commit for discounts'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cost Analysis'),
        bMid(B2_L, B2_R, 'Budgets'),
        bMid(B3_L, B3_R, 'Optimisation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'By service: monthly'),
        bMid(B2_L, B2_R, 'Threshold: $ alert'),
        bMid(B3_L, B3_R, 'Reservations: 1/3yr'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'By tag: team/env'),
        bMid(B2_L, B2_R, 'Forecast: 80% alert'),
        bMid(B3_L, B3_R, 'Savings Plans: flex'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'By subscription: trend'),
        bMid(B2_L, B2_R, 'Action group: email'),
        bMid(B3_L, B3_R, 'Advisor: rightsizing'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Export: storage account'),
        bMid(B2_L, B2_R, 'Anomaly alerts: ML'),
        bMid(B3_L, B3_R, 'Spot VMs: -90% cost'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cost alloc: tags billing'),
        bMid(B2_L, B2_R, 'Budget: scope mgmt grp'),
        bMid(B3_L, B3_R, 'Idle: deallocate + del'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Cost analysis provides visibility · Budgets alert on thresholds'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cost Analysis', 'Budgets', 'Reservations', 'Savings Plans', 'Azure Advisor'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['By service view', 'Monthly limit', 'VM: 1yr save%', 'Compute flex', 'Resize: -30%'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Tag: chargeback', 'Forecast alert', 'SQL: 3yr 72%', 'DB flexible', 'Idle: terminate'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Export: daily', 'Action grp', 'Coverage: view', 'Storage flex', 'RI: recommend'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Anomaly: detect', 'Scope: sub/RG', 'Utilise: >80%', 'Spend commit', 'Cost: estimate'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure billing infrastructure · Cost Management API · Export storage account · Action Group SNS/email'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Cost Management + Billing= Azure portal blade for analysing and controlling Azure spend'))
    lines.append(txt_row('Budget          = Spending threshold; types: cost (£/$) or usage; alerts at % of limit'))
    lines.append(txt_row('Action Group    = Named set of actions (email, SMS, webhook, Logic App) triggered by alerts'))
    lines.append(txt_row('Reservation     = 1 or 3-year committed use purchase; applies to specific VM size or service'))
    lines.append(txt_row('Savings Plan    = Flexible spend commitment ($/hr); applies across regions and eligible services'))
    lines.append(txt_row('Spot VM         = Low-priority VM using spare Azure capacity; up to 90% cheaper; can be evicted'))
    lines.append(txt_row('Azure Advisor   = Personalised recommendations for cost, security, performance, and reliability'))
    lines.append(txt_row('Cost allocation = Attributing Azure costs to teams/apps via resource tags; chargeback enablement'))
    lines.append(txt_row('Cost export     = Scheduled export of usage data to Azure Blob Storage; feeds BI tools / Power BI'))
    lines.append(txt_row('Anomaly alert   = AI-detected unexpected spend spike on subscription, resource group, or service'))
    lines.append(txt_row('Reserved capacity= Azure Reservation; pre-purchase a discount for predictable workloads'))
    lines.append(txt_row('Rightsizing     = Advisor recommendation to reduce VM SKU when CPU/memory consistently underused'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'azure-governance',
    'docs/cloud/azure/governance/index.md',
    'Azure Governance — Management Groups, Azure Policy (Audit/Deny/DINE), initiatives, compliance',
)
def azure_governance_overview():
    """Azure Governance Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Governance Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Governance — Policy, Initiatives, Compliance, and Management Groups')))
    lines.append(R(bMid(IV_L, IV_R, 'Management Groups: policy and RBAC applied at MG scope cascade to all subscriptions below')))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Policy: define rules for resource configs; effects: Audit, Deny, DeployIfNotExists')))
    lines.append(R(bMid(IV_L, IV_R, 'Initiatives: group multiple policy definitions; assign as one unit (e.g. CIS Azure Benchmark)')))
    lines.append(R(bMid(IV_L, IV_R, 'Compliance review: policy state dashboard; non-compliant resources; remediation tasks')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Management Groups scope policies · Policy defines rules · Initiatives bundle them'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Management Groups'),
        bMid(B2_L, B2_R, 'Azure Policy'),
        bMid(B3_L, B3_R, 'Compliance'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Root: tenant root MG'),
        bMid(B2_L, B2_R, 'Effect: Audit/Deny/DINE'),
        bMid(B3_L, B3_R, 'Dashboard: compliant %'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Custom MG hierarchy'),
        bMid(B2_L, B2_R, 'Scope: MG/sub/RG/res'),
        bMid(B3_L, B3_R, 'Non-compliant: list/fix'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Inheritance: sub → RG'),
        bMid(B2_L, B2_R, 'Initiatives: CIS/NIST'),
        bMid(B3_L, B3_R, 'Remediation: auto task'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Policy scope: inherited'),
        bMid(B2_L, B2_R, 'Parameters: reuse policy'),
        bMid(B3_L, B3_R, 'Exemption: time-bound'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Tag policy: org-wide'),
        bMid(B2_L, B2_R, 'Assignment: + params'),
        bMid(B3_L, B3_R, 'Audit log: activity log'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Management Groups establish hierarchy · Policy defines rules · Compliance validates and remediates'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Mgmt Groups', 'Azure Policy', 'Initiatives', 'Compliance', 'Exemptions'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Create MG', 'New definition', 'Assign init', 'View %: pass', 'Create exemp'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Move sub to MG', 'Assign policy', 'CIS Az 1.4', 'Non-compliant', 'Waiver: reason'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Policy: inherit', 'Effect: Deny', 'NIST SP800-53', 'Remediation', 'Expiry: date'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['RBAC at MG', 'DeployIfNotEx', 'Custom bundled', 'Mitigate task', 'Scope: RG/res'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure Resource Manager · Policy engine · Management Group hierarchy · Activity Log infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Management Group   = Container above subscriptions; scoping boundary for policy and RBAC'))
    lines.append(txt_row('Azure Policy       = Service for defining, assigning, and evaluating compliance rules on resources'))
    lines.append(txt_row('Policy definition  = JSON rule with conditions and effects; built-in or custom; parameterised'))
    lines.append(txt_row('Policy assignment  = Applies a definition or initiative to a scope with specific parameter values'))
    lines.append(txt_row('Effect: Audit      = Logs non-compliant resources without blocking; compliance reporting only'))
    lines.append(txt_row('Effect: Deny       = Blocks creation or update of non-compliant resources; hard enforcement'))
    lines.append(txt_row('Effect: DINE       = DeployIfNotExists; deploys remediation resource when policy condition is met'))
    lines.append(txt_row('Initiative         = Collection of policy definitions assigned together; simplifies compliance sets'))
    lines.append(txt_row('Remediation task   = Auto-runs the DINE effect on existing non-compliant resources in scope'))
    lines.append(txt_row('Exemption          = Excludes a resource or scope from a policy assignment; time-bound or permanent'))
    lines.append(txt_row('Compliance state   = Per-resource evaluation result: Compliant / Non-compliant / Not started / Exempt'))
    lines.append(txt_row('Tagging policy     = Policy enforcing required tags (e.g. Owner, Environment) on all resource'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'azure-identity',
    'docs/cloud/azure/identity/index.md',
    'Azure Identity — Entra ID, RBAC, managed identities, PIM, conditional access',
)
def azure_identity_overview():
    """Azure Identity Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Identity Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Identity — Entra ID, RBAC, Managed Identities, and PIM')))
    lines.append(R(bMid(IV_L, IV_R, 'Entra ID: cloud identity directory; users, groups, B2B guests, and app registrations')))
    lines.append(R(bMid(IV_L, IV_R, 'RBAC: Owner / Contributor / Reader built-in roles + custom; scope: MG, sub, RG, resource')))
    lines.append(R(bMid(IV_L, IV_R, 'Managed Identities: system or user-assigned; auto-managed SP for Azure services to authenticate')))
    lines.append(R(bMid(IV_L, IV_R, 'PIM: just-in-time role activation; approval workflow; time-limited privileged access')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Entra ID is the identity source · RBAC grants access · Managed Identities remove secrets'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Entra ID'),
        bMid(B2_L, B2_R, 'RBAC'),
        bMid(B3_L, B3_R, 'Privileged Access'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Users: UPN + MFA'),
        bMid(B2_L, B2_R, 'Owner: full control'),
        bMid(B3_L, B3_R, 'PIM: JIT activate'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Groups: security+M365'),
        bMid(B2_L, B2_R, 'Contributor: no RBAC'),
        bMid(B3_L, B3_R, 'Approval: manager'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'App registrations: SPN'),
        bMid(B2_L, B2_R, 'Reader: read-only'),
        bMid(B3_L, B3_R, 'Time-limit: 8 hours'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Conditional Access: MFA'),
        bMid(B2_L, B2_R, 'Custom roles: JSON def'),
        bMid(B3_L, B3_R, 'Audit: PIM history'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Managed identities: MI'),
        bMid(B2_L, B2_R, 'Scope: sub/RG/resource'),
        bMid(B3_L, B3_R, 'Access review: quarterly'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Entra ID manages identities · RBAC controls access at scope'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Entra ID', 'App Reg.', 'RBAC', 'Managed ID', 'PIM'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['User: create', 'Register app', 'Assign: sub', 'System-assign', 'Activate: JIT'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Group: add mem', 'Client secret', 'Assign: RG', 'User-assign', 'Approve: MFA'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['MFA: enforce', 'API permission', 'Custom role', 'RBAC to MI', 'Expiry: 8h'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cond. Access', 'Enterprise app', 'Review: list', 'No secrets', 'Access review'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Entra ID global service · Azure RBAC control plane · PIM service · ARM token endpoint'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Entra ID         = Microsoft cloud identity directory (formerly Azure AD); users, groups, apps,'))
    lines.append(txt_row('App registration = Entra ID object representing an application; has client ID, secret or certificate'))
    lines.append(txt_row('Service principal= Instance of an app registration in a tenant; has identity and can be assigned'))
    lines.append(txt_row('Managed Identity = Azure-managed service principal; no secrets; system (tied to resource) or'))
    lines.append(txt_row('System-assigned MI= Identity tied to one resource; deleted when resource is deleted; most common'))
    lines.append(txt_row('User-assigned MI = Standalone identity; assigned to multiple resources; survives resource deletion'))
    lines.append(txt_row('RBAC             = Role-Based Access Control; assigns built-in or custom roles at a defined scope'))
    lines.append(txt_row('RBAC scope       = Hierarchy: Management Group > Subscription > Resource Group > Resource'))
    lines.append(txt_row('PIM              = Privileged Identity Management; manages just-in-time access to sensitive roles'))
    lines.append(txt_row('Conditional Access= Policy evaluating sign-in signals (location, device, risk) to grant, block, or'))
    lines.append(txt_row('Access review    = Periodic review of group membership or role assignments; remove stale access'))
    lines.append(txt_row('B2B              = Business-to-business; inviting external users (guests) to your Entra ID tenant'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'azure-monitoring',
    'docs/cloud/azure/monitoring/index.md',
    'Azure Monitoring — Azure Monitor, Log Analytics (KQL), alerts, action groups',
)
def azure_monitoring_overview():
    """Azure Monitoring Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Monitoring Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Monitor — Metrics, Logs, Alerts, and Observability')))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Monitor: platform for all metrics, logs, alerts, and dashboards across Azure services')))
    lines.append(R(bMid(IV_L, IV_R, 'Log Analytics: workspace stores logs; KQL query language; used for dashboards and alert rules')))
    lines.append(R(bMid(IV_L, IV_R, 'Alerts: metric, log, and activity log alert rules; action groups for notification and')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnostic settings: route resource logs and metrics to Log Analytics, Storage, or Event Hub')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Metrics and logs feed alert rules · Alerts trigger action groups · Dashboards provide visibility'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Azure Monitor'),
        bMid(B2_L, B2_R, 'Log Analytics'),
        bMid(B3_L, B3_R, 'Alerts'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Metrics: platform native'),
        bMid(B2_L, B2_R, 'Workspace: per region'),
        bMid(B3_L, B3_R, 'Metric alert: threshold'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Activity log: ctrl-plane'),
        bMid(B2_L, B2_R, 'KQL: query + transform'),
        bMid(B3_L, B3_R, 'Log alert: KQL query'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Diagnostic settings'),
        bMid(B2_L, B2_R, 'Retention: 30-730d'),
        bMid(B3_L, B3_R, 'Activity alert: ops'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Service Health: events'),
        bMid(B2_L, B2_R, 'Workbooks: dashboards'),
        bMid(B3_L, B3_R, 'Action group: email/web'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Dashboards: pin metrics'),
        bMid(B2_L, B2_R, 'Saved queries: reuse'),
        bMid(B3_L, B3_R, 'Alert rule: severity 0-4'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Azure Monitor collects metrics/logs · Log Analytics stores and queries · Alerts notify and automate'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Azure Monitor', 'Log Analytics', 'Alerts', 'Activity Log', 'Service Health'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Metrics: CPU', 'KQL: query', 'Metric: CPU>80', 'Who changed?', 'Planned maint'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Diag settings', 'Workspace: RG', 'Log: KQL rule', 'Activity alert', 'Incidents: svc'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Dashboard: pin', 'Retention: 90d', 'Action: email', 'Export: LA', 'Health alerts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Workbooks', 'Saved query', 'Severity 0-4', 'ARM events', 'Subscr events'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure Monitor backend · Log Analytics workspace storage · Action Group notification services'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Azure Monitor     = Platform service aggregating all metrics, logs, alerts, and traces from Azure'))
    lines.append(txt_row('Log Analytics workspace= Storage and query engine for Azure Monitor logs; uses KQL; one or more per'))
    lines.append(txt_row('KQL               = Kusto Query Language; used in Log Analytics, Application Insights, and Data'))
    lines.append(txt_row('Diagnostic settings= Resource-level config routing logs/metrics to Log Analytics, Storage, or Event'))
    lines.append(txt_row('Activity Log      = Subscription-level control-plane audit log; who did what, when; 90 days retention'))
    lines.append(txt_row('Metric alert      = Fires when a metric (CPU, memory, latency) crosses a threshold for N minutes'))
    lines.append(txt_row('Log alert         = Fires when a KQL query returns rows; evaluated on a schedule (5 min – 1 day)'))
    lines.append(txt_row('Activity alert    = Fires on specific control-plane events (e.g. VM deleted, RBAC assigned)'))
    lines.append(txt_row('Action group      = Reusable set of notification actions (email, SMS, webhook, Logic App, ITSM)'))
    lines.append(txt_row('Alert severity    = Sev 0 (Critical) to Sev 4 (Verbose); used to route and prioritise alerts'))
    lines.append(txt_row('Service Health    = Azure-side health events and planned maintenance for your subscriptions/services'))
    lines.append(txt_row('Workbook          = Azure Monitor interactive report combining metrics, logs, and parameters in one'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'azure-networking',
    'docs/cloud/azure/networking/index.md',
    'Azure Networking — VNet, subnets, NSGs, Azure Firewall, Private Endpoints, ExpressRoute',
)
def azure_networking_overview():
    """Azure Networking Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Networking Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Networking — VNet, NSG, Load Balancer, DNS, and Hybrid Connectivity')))
    lines.append(R(bMid(IV_L, IV_R, 'VNet: isolated network; CIDR /8–/29; subnets per AZ; hub-and-spoke via VNet peering')))
    lines.append(R(bMid(IV_L, IV_R, 'Security: NSG (stateful L4 rules per subnet/NIC) · Azure Firewall (stateful L4/L7 in hub)')))
    lines.append(R(bMid(IV_L, IV_R, 'Load balancing: Load Balancer (L4) · Application Gateway (L7 + WAF) · Traffic Manager (DNS)')))
    lines.append(R(bMid(IV_L, IV_R, 'Hybrid: ExpressRoute (private circuit) · VPN Gateway (IPsec) · Private Endpoints (PaaS)')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  VNet defines the network · NSG/Firewall secure it · Load Balancer distributes traffic'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VNet & Subnets'),
        bMid(B2_L, B2_R, 'Security Controls'),
        bMid(B3_L, B3_R, 'Connectivity'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VNet: CIDR /16 plan'),
        bMid(B2_L, B2_R, 'NSG: allow/deny rules'),
        bMid(B3_L, B3_R, 'ExpressRoute: private'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Subnets: per AZ/tier'),
        bMid(B2_L, B2_R, 'Firewall: hub central'),
        bMid(B3_L, B3_R, 'VPN Gateway: IPsec'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Peering: hub ↔ spoke'),
        bMid(B2_L, B2_R, 'Network Watcher: diag'),
        bMid(B3_L, B3_R, 'Private Endpoint: PaaS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Route tables: UDR'),
        bMid(B2_L, B2_R, 'DDoS: Basic or std'),
        bMid(B3_L, B3_R, 'Azure DNS: pub + priv'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Service endpoints'),
        bMid(B2_L, B2_R, 'Flow logs: NSG → LA'),
        bMid(B3_L, B3_R, 'LB: internal+public'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  VNet/subnets form the base · NSG/Firewall protect traffic'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VNet', 'Subnets', 'NSG', 'Load Balancer', 'App Gateway'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CIDR: plan', 'App subnet', 'Inbound rules', 'Backend pool', 'L7: path route'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Peering: hub', 'DB subnet', 'Outbound rules', 'Health probe', 'WAF: OWASP'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Flow logs: LA', 'GW subnet: /27', 'Priority: 100', 'LB rule: port', 'SSL termination'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['DNS: custom', 'Service endpt', 'NSG flow logs', 'Internal LB', 'Autoscale: min'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure SDN fabric · Availability Zones · ExpressRoute physical circuits · VPN Gateway hardware'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VNet           = Virtual Network; isolated private network in a region; one or more CIDR address'))
    lines.append(txt_row('Subnet         = Address range within a VNet; services and NSGs attached per subnet'))
    lines.append(txt_row('NSG            = Network Security Group; stateful L4 ACL; priority-ordered allow/deny rules on'))
    lines.append(txt_row('VNet peering   = Private connectivity between VNets in same or different regions; low latency'))
    lines.append(txt_row('UDR            = User Defined Route; custom route table overriding Azure defaults; force to firewall'))
    lines.append(txt_row('Azure Firewall = Managed stateful L4/L7 firewall in hub VNet; centralises egress and spoke traffic'))
    lines.append(txt_row('Private Endpoint= Private IP in a VNet for accessing PaaS (Storage, SQL, Key Vault) without internet'))
    lines.append(txt_row('Service Endpoint= Optimised route from VNet to PaaS service; not a private IP; firewall-accessible'))
    lines.append(txt_row('Application Gateway= L7 load balancer with URL routing, SSL offload, and optional WAF integration'))
    lines.append(txt_row('Network Watcher = Diagnostics for connectivity, packet capture, NSG flow logs, and topology view'))
    lines.append(txt_row('ExpressRoute   = Dedicated private 50 Mbps–10 Gbps circuit between on-premises and Azure'))
    lines.append(txt_row('Azure DNS      = Managed DNS for public zones (internet) and private zones (VNet resolution)'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'azure-operations',
    'docs/cloud/azure/operations/index.md',
    'Azure Operations — health checks, VM procedures, Update Manager, backup/restore, automation',
)
def azure_operations_overview():
    """Azure Operations Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Operations Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Operations — Health Checks, Procedures, Patching, and Automation')))
    lines.append(R(bMid(IV_L, IV_R, 'Health Checks: VM status · Load Balancer health probes · Monitor alert state · Service Health')))
    lines.append(R(bMid(IV_L, IV_R, 'Procedures: VM lifecycle, disk expansion, scale set refresh, RG cleanup, ASR failover tests')))
    lines.append(R(bMid(IV_L, IV_R, 'Patching: Azure Update Manager; scheduled patch runs; compliance reporting per VM fleet')))
    lines.append(R(bMid(IV_L, IV_R, 'Backup/Restore: Azure Backup jobs · RSV restore · disk snapshot restore · ASR test failover')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Health checks detect issues · Procedures resolve them · Automation prevents recurrence'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Health Checks'),
        bMid(B2_L, B2_R, 'Procedures'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VM: running + health'),
        bMid(B2_L, B2_R, 'Start/stop/restart VM'),
        bMid(B3_L, B3_R, 'az CLI: scripted ops'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LB health probe: pass'),
        bMid(B2_L, B2_R, 'Resize VM SKU'),
        bMid(B3_L, B3_R, 'Logic App: workflow'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Monitor alerts: OK?'),
        bMid(B2_L, B2_R, 'Disk: expand + extend'),
        bMid(B3_L, B3_R, 'ARM / Bicep: IaC'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Service Health: events'),
        bMid(B2_L, B2_R, 'VMSS: instance refresh'),
        bMid(B3_L, B3_R, 'Event Grid: auto-trigger'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Backup jobs: success?'),
        bMid(B2_L, B2_R, 'ASR: test failover'),
        bMid(B3_L, B3_R, 'Azure Automation: run'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Health checks prevent failures · Procedures execute changes'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Health Checks', 'Procedures', 'Patching', 'Backup/Restore', 'Scripts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VM: running?', 'Start/stop VM', 'Update Manager', 'Backup: enable', 'az vm list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LB probe: pass', 'Resize: dealoc', 'Patch schedule', 'RSV: restore', 'az disk create'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Alerts: OK', 'Disk: expand', 'Compliance', 'Snap: restore', 'Bicep: deploy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Svc Health: evt', 'VMSS refresh', 'Reboot: sched', 'ASR: test fail', 'Automation RB'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure VM host fabric · Managed Disk storage · Load Balancer health infrastructure · VNet networking'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Azure Update Manager = Replaces Automation Update Management; patches OS at scale per schedule'))
    lines.append(txt_row('Service Health      = Azure health dashboard for your subscriptions; planned and unplanned events'))
    lines.append(txt_row('LB health probe     = TCP or HTTP check sent to backend pool members; failure removes VM from'))
    lines.append(txt_row('VM resize           = Change VM SKU; requires deallocation first (downtime); no data loss'))
    lines.append(txt_row('Disk expansion      = Increase managed disk size in portal/CLI; then extend partition inside OS'))
    lines.append(txt_row('VMSS instance refresh= Rolling replacement of scale set instances with updated image or config'))
    lines.append(txt_row('ASR test failover   = Spins up replica VM in isolated VNet; validates recovery without affecting prod'))
    lines.append(txt_row('Azure Automation    = Runbooks (PowerShell/Python) executed on schedule or on demand at scale'))
    lines.append(txt_row('Logic App           = Low-code workflow automation; triggered by events, HTTP, or schedule'))
    lines.append(txt_row('Event Grid          = Event routing service; triggers Logic Apps, Functions, or webhooks on resource'))
    lines.append(txt_row('Bicep              = ARM template DSL; cleaner syntax for deploying Azure resources as IaC'))
    lines.append(txt_row('az vm run-command   = Execute script inside VM via agent; works when RDP/SSH is blocked'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'azure-security',
    'docs/cloud/azure/security/index.md',
    'Azure Security — Entra ID SSO/MFA, Key Vault, CMK, Defender for Cloud, Secure Score, Sentinel',
)
def azure_security_overview():
    """Azure Security Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Security Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Security — Authentication, Encryption, and Threat Detection')))
    lines.append(R(bMid(IV_L, IV_R, 'Authentication: Entra ID SSO · MFA · Conditional Access · PIM for just-in-time admin access')))
    lines.append(R(bMid(IV_L, IV_R, 'Encryption: Key Vault (keys+secrets+certs) · Customer-Managed Keys · Private Link for PaaS')))
    lines.append(R(bMid(IV_L, IV_R, 'Threat detection: Defender for Cloud (posture + CSPM) · Secure Score · Defender plans per svc')))
    lines.append(R(bMid(IV_L, IV_R, 'Network security: NSGs · Azure Firewall in hub · WAF on App Gateway · DDoS Protection')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication controls access · Encryption protects data · Defender detects and remediates threats'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Encryption'),
        bMid(B3_L, B3_R, 'Threat Detection'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Entra ID: SSO+MFA'),
        bMid(B2_L, B2_R, 'Key Vault: keys/certs'),
        bMid(B3_L, B3_R, 'Defender for Cloud'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Conditional Access'),
        bMid(B2_L, B2_R, 'CMK: storage+SQL+disk'),
        bMid(B3_L, B3_R, 'Secure Score: target'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'PIM: JIT privileged'),
        bMid(B2_L, B2_R, 'TLS: App GW + APIM'),
        bMid(B3_L, B3_R, 'Defender plans: VMs'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RBAC: least privilege'),
        bMid(B2_L, B2_R, 'Private Link: no pub IP'),
        bMid(B3_L, B3_R, 'Microsoft Sentinel: SIEM'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Access reviews: quarterly'),
        bMid(B2_L, B2_R, 'Disk: SSE + CMK'),
        bMid(B3_L, B3_R, 'NSG + Firewall: network'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication + RBAC prevent access · Encryption protects data'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Authentication', 'Access Control', 'Encryption', 'Hardening', 'Key Vault'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Entra ID: SSO', 'RBAC: Contrib', 'KV: key create', 'Defender plans', 'Key: rotate'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['MFA: all users', 'PIM: JIT role', 'CMK: storage', 'Secure Score', 'Secret: get'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cond. Access', 'MI: no secret', 'TLS: 1.2+ only', 'Policy: audit', 'Cert: import'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Access review', 'Custom role', 'Disk: SSE-CMK', 'NSG + FW', 'RBAC: Key Vault'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure HSM for Key Vault · Defender for Cloud backend · Entra ID global service'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Key Vault        = Managed secrets, keys, and certificates; RBAC + access policy; HSM-backed option'))
    lines.append(txt_row('CMK              = Customer-Managed Key; encryption key you control in Key Vault; used for Azure'))
    lines.append(txt_row('SSE              = Server-Side Encryption; Azure encrypts managed disks at rest using PME or CMK'))
    lines.append(txt_row('Private Link     = Private Endpoint mapping PaaS service to VNet IP; eliminates public internet'))
    lines.append(txt_row('Defender for Cloud= CSPM + CWPP; security posture management and workload protection across Azure'))
    lines.append(txt_row('Secure Score     = Numeric score (0-100) of security posture; improvements mapped to recommendations'))
    lines.append(txt_row('Defender plans   = Per-resource workload protection: VMs, SQL, Storage, Containers, Key Vault, DNS'))
    lines.append(txt_row('Microsoft Sentinel= Cloud-native SIEM + SOAR; ingests logs, detects threats, automates response'))
    lines.append(txt_row('Conditional Access= Entra ID engine; blocks, MFAs, or allows sign-in based on device, location, risk'))
    lines.append(txt_row('PIM              = Privileged Identity Management; JIT admin access with approval and time limits'))
    lines.append(txt_row('TLS validation   = Enforce minimum TLS 1.2 on Storage accounts, App Gateway, and API Management'))
    lines.append(txt_row('Access review    = Periodic audit of who has what access; approvers confirm or remove assignments'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'azure-storage',
    'docs/cloud/azure/storage/index.md',
    'Azure Storage — Blob tiers, lifecycle, Managed Disks (Premium/Ultra/ZRS), Azure Files',
)
def azure_storage_overview():
    """Azure Storage Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Storage Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Storage — Blob, Managed Disks, Files, and Storage Accounts')))
    lines.append(R(bMid(IV_L, IV_R, 'Blob Storage: Hot / Cool / Cold / Archive access tiers; lifecycle management; immutable WORM')))
    lines.append(R(bMid(IV_L, IV_R, 'Managed Disks: Premium SSD / Standard SSD / Ultra; ZRS for zone redundancy; snapshots')))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Files: managed SMB and NFS shares; AD integration for Windows shares; Azure File Sync')))
    lines.append(R(bMid(IV_L, IV_R, 'Storage accounts: replication LRS/ZRS/GRS/GZRS; encryption at rest by default; private')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Blob serves objects · Managed Disks serve VM block I/O · Files serve shared mounts'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Blob Storage'),
        bMid(B2_L, B2_R, 'Managed Disks'),
        bMid(B3_L, B3_R, 'Azure Files'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Hot: frequent access'),
        bMid(B2_L, B2_R, 'Premium SSD: low lat'),
        bMid(B3_L, B3_R, 'SMB 2.1/3.0 shares'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cool/Cold: infreq'),
        bMid(B2_L, B2_R, 'Standard SSD: gen use'),
        bMid(B3_L, B3_R, 'NFS 4.1: Linux'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Archive: offline store'),
        bMid(B2_L, B2_R, 'Ultra: 160K IOPS'),
        bMid(B3_L, B3_R, 'AD auth: Windows'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Lifecycle: tier rules'),
        bMid(B2_L, B2_R, 'ZRS: zone redundant'),
        bMid(B3_L, B3_R, 'File Sync: on-prem'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Immutability: WORM'),
        bMid(B2_L, B2_R, 'Snapshots: incremental'),
        bMid(B3_L, B3_R, 'Backup: RSV policy'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Blob for unstructured objects · Managed Disks for VM boot/data · Files for shared SMB/NFS workloads'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Blob Storage', 'Managed Disks', 'Azure Files', 'Storage Accts', 'Snapshots'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Upload: AzCopy', 'Create: P10/P30', 'Create share', 'LRS/ZRS/GRS', 'Disk snap: incr'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Lifecycle: rule', 'Attach to VM', 'Mount: Windows', 'Private endpt', 'Blob snap'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Immutability', 'Expand: no stop', 'Mount: Linux', 'SAS token', 'Restore: snap'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Tier: archive', 'ZRS: 3-zone', 'File Sync', 'CMK encrypt', 'Copy to region'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure Storage clusters (LRS/ZRS/GRS) · Managed Disk fabric per AZ · Storage account endpoints'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Storage account  = Top-level namespace for Blob, Files, Queue, Table; controls replication and access'))
    lines.append(txt_row('LRS              = Locally Redundant Storage; 3 copies in one data centre; cheapest option'))
    lines.append(txt_row('ZRS              = Zone-Redundant Storage; 3 copies across 3 AZs; survives zone failure'))
    lines.append(txt_row('GRS              = Geo-Redundant Storage; 6 copies across 2 regions; async replication to secondary'))
    lines.append(txt_row('GZRS             = Geo-Zone-Redundant Storage; ZRS in primary + LRS in secondary region'))
    lines.append(txt_row('Blob access tier  = Hot (frequent), Cool (infrequent), Cold (rare), Archive (offline); cost tiers'))
    lines.append(txt_row('Lifecycle policy = Automatically transitions or deletes blobs based on age and last-modified date'))
    lines.append(txt_row('Immutable storage= WORM policy on container; Legal hold or time-based; prevents delete/overwrite'))
    lines.append(txt_row('Managed Disk     = Azure-managed block storage for VMs; types: Premium SSD, Standard SSD, Ultra'))
    lines.append(txt_row('ZRS disk         = Zone-Redundant disk; synchronously replicates across 3 AZs; no AZ downtime impact'))
    lines.append(txt_row('Azure File Sync  = Syncs Azure Files share to on-premises Windows Server; cloud tiering option'))
    lines.append(txt_row('SAS token        = Shared Access Signature; time-limited URL token for scoped blob/container access'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'azure-troubleshooting',
    'docs/cloud/azure/troubleshooting/index.md',
    'Azure Troubleshooting — common issues, Boot Diagnostics, Serial Console, Network Watcher',
)
def azure_troubleshooting_overview():
    """Azure Troubleshooting Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Azure Troubleshooting Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Azure Troubleshooting — Common Issues, Diagnostics, and Escalation')))
    lines.append(R(bMid(IV_L, IV_R, 'Common issues: VM unreachable · NSG blocking · RBAC access denied · Storage auth error')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnostics: Boot diagnostics · Serial Console · Network Watcher · Activity Log · Monitor')))
    lines.append(R(bMid(IV_L, IV_R, 'Tools: az CLI describe · Azure portal diagnostics · Connection Troubleshoot · Resource Health')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: Azure Support cases; collect sub ID, region, resource ID, error, and timeframe')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide investigation · Diagnostics locate root cause'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VM: RDP/SSH fails'),
        bMid(B2_L, B2_R, 'Boot diagnostics: log'),
        bMid(B3_L, B3_R, 'Sub ID + resource ID'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NSG: port blocked'),
        bMid(B2_L, B2_R, 'Serial Console: OOB'),
        bMid(B3_L, B3_R, 'Error + timestamp'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RBAC: access denied'),
        bMid(B2_L, B2_R, 'Network Watcher: path'),
        bMid(B3_L, B3_R, 'Severity: Crit/High'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Storage: 403 auth'),
        bMid(B2_L, B2_R, 'Activity Log: who/when'),
        bMid(B3_L, B3_R, 'Sev A: production down'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'DNS: resolution fail'),
        bMid(B2_L, B2_R, 'Resource Health: state'),
        bMid(B3_L, B3_R, 'Premium support: TAM'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Identify symptom → collect diagnostics (logs, Network Watcher, health) → resolve or escalate'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Escalation', 'CLI Tools', 'Portal Tools'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VM: no RDP', 'Boot diag log', 'Sev A: call', 'az vm list', 'Resource Health'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['NSG: miss rule', 'Serial console', 'Sub ID + error', 'az network nsg', 'Net Watcher'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['RBAC: denied', 'Activity Log', 'Premium: TAM', 'az role assign', 'Boot Diag'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Storage: 403', 'Net Watcher', 'Collect: all', 'az storage ls', 'Diagn settings'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Azure VM host fabric · Azure networking SDN · Microsoft Support infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Boot Diagnostics  = Captures VM serial console log and screenshot; diagnoses non-starting VMs'))
    lines.append(txt_row('Serial Console    = Out-of-band terminal access to VM; works when RDP/SSH unreachable'))
    lines.append(txt_row('Network Watcher   = Diagnoses connectivity; Connection Troubleshoot traces hop-by-hop path'))
    lines.append(txt_row('Connection Troubleshoot= Network Watcher tool; tests TCP reachability from source VM to destination'))
    lines.append(txt_row('Resource Health   = Per-resource health history; shows Azure platform events affecting the resource'))
    lines.append(txt_row('Activity Log      = Control-plane audit; search for who made a change and when in the last 90 days'))
    lines.append(txt_row('NSG flow logs     = Accepted/denied traffic metadata; route to Log Analytics for KQL queries'))
    lines.append(txt_row('Severity A case   = Production down; 24/7 response; phone callback + online case together'))
    lines.append(txt_row('Severity B case   = Degraded function; business-hours response; online case sufficient'))
    lines.append(txt_row('TAM               = Technical Account Manager; named Microsoft contact for Premier/Unified support'))
    lines.append(txt_row('RBAC denied       = Check Activity Log for the 403; look for missing role or wrong scope'))
    lines.append(txt_row('Storage 403       = Check access key vs SAS vs RBAC; check firewall rules and private endpoint config'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── VMware product diagrams — batch 1 of 2 ────────────────────────────────────

@kb_diagram(
    'esxi',
    'docs/virtualization/vmware/esxi/index.md',
    'ESXi Host Stack — VMkernel, VMkernel ports, patching, host profiles, lockdown mode',
)
def esxi_stack():
    """ESXi Host Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'ESXi Host Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware ESXi — Type-1 Bare-Metal Hypervisor (VMkernel OS)')))
    lines.append(R(bMid(IV_L, IV_R, 'VMkernel: micro-kernel manages CPU/memory/storage/network for all VMs on the host')))
    lines.append(R(bMid(IV_L, IV_R, 'VMkernel ports: Management · vMotion · vSAN · NFC · Replication — each on separate VLAN')))
    lines.append(R(bMid(IV_L, IV_R, 'Storage: local VMFS, SAN (FC/iSCSI/NVMe), NFS — all via storage adapters and PSPs')))
    lines.append(R(bMid(IV_L, IV_R, 'Networking: vSS or vDS; uplink teaming; port groups per workload or function')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  VMkernel is the host foundation · networking and storage connect VMs'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VMkernel: CPU+RAM sched'),
        bMid(B2_L, B2_R, 'DCUI: local console mgmt'),
        bMid(B3_L, B3_R, 'Lockdown mode: strict/norm'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSwitch/vDS: port groups'),
        bMid(B2_L, B2_R, 'Patching: VUM / LCM'),
        bMid(B3_L, B3_R, 'Firewall: service rules'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'HBAs: FC/iSCSI/NVMe'),
        bMid(B2_L, B2_R, 'Host profiles: enforce std'),
        bMid(B3_L, B3_R, 'Secure boot: TPM verify'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NIC teaming: active/standby'),
        bMid(B2_L, B2_R, 'esxcli: config + diagnose'),
        bMid(B3_L, B3_R, 'SSH/Shell: disabled by std'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VMkernel ports: VMk0-VMkN'),
        bMid(B2_L, B2_R, 'esxtop: real-time perf'),
        bMid(B3_L, B3_R, 'Syslog: to vRLI or syslog'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines the host stack · Operations maintain health · Security hardens the hypervisor'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['PSOD: check vmkern', 'vm-support bundle', 'Host conn: green?', 'GSS: support bundl', 'esxcli system'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['NFS unmount: check', 'esxcli storage lis', 'HBA: link state OK', 'TAM escalation', 'esxcli network'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vMotion fail: VMk ', 'esxtop -b -n 5', 'vSAN health: green', 'Log bundle + vmx', 'vmkfstools -i'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['HA agent restart', '/var/log/vmkernel', 'Uptime + tasks', 'P1: production dow', 'vim-cmd vmsvc'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 server · CPUs (Intel/AMD) · RAM DIMMs · PCIe HBAs and NICs · SAS/NVMe disks · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VMkernel      = ESXi micro-kernel OS; manages CPU scheduling, memory balloon, and device I/O'))
    lines.append(txt_row('DCUI          = Direct Console User Interface; local text console on ESXi host physical screen'))
    lines.append(txt_row('VMkernel port = VMk NIC; carries management, vMotion, vSAN, NFC, or replication traffic'))
    lines.append(txt_row('Lockdown mode = Host setting that prevents direct access; all management via vCenter only'))
    lines.append(txt_row('Host Profile  = Saved configuration template applied to hosts for consistency enforcement'))
    lines.append(txt_row('PSP           = Path Selection Policy; controls multipath selection: MRU, Fixed, or RR'))
    lines.append(txt_row('vDS           = vSphere Distributed Switch; cluster-level virtual switch managed by vCenter'))
    lines.append(txt_row('esxcli        = ESXi CLI framework; namespaces: system, network, storage, vm, software'))
    lines.append(txt_row('esxtop        = ESXi real-time performance monitor; CPU/memory/disk/network counters per VM'))
    lines.append(txt_row('vmkfstools    = CLI for VMDK operations: clone, resize, inflate, import/export'))
    lines.append(txt_row('PSOD          = Purple Screen of Death; ESXi kernel panic; check vmkernel log for cause'))
    lines.append(txt_row('LCM           = Lifecycle Manager; patching engine in vCenter for ESXi host baselines'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'nsx',
    'docs/virtualization/vmware/nsx/index.md',
    'NSX SDN Stack — Geneve overlay, T0/T1 gateways, DFW microsegmentation, Edge nodes',
)
def nsx_stack():
    """NSX Software-Defined Networking Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NSX Software-Defined Networking Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware NSX — Software-Defined Networking and Security')))
    lines.append(R(bMid(IV_L, IV_R, 'Overlay networking: Geneve encapsulation over physical underlay; TEPs on each host')))
    lines.append(R(bMid(IV_L, IV_R, 'Routing: T0 Gateway (north-south, BGP to physical) · T1 Gateway (east-west, per tenant)')))
    lines.append(R(bMid(IV_L, IV_R, 'Security: Distributed Firewall (DFW) on every hypervisor kernel — zero-trust microsegmentation')))
    lines.append(R(bMid(IV_L, IV_R, 'Edge: Edge Nodes run T0/T1 services; deployed as VM or bare-metal for high throughput')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  NSX Manager controls all SDN config · overlay transports workloads · DFW secures every VM'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NSX Manager: 3-node cluster'),
        bMid(B2_L, B2_R, 'Segment: create + attach'),
        bMid(B3_L, B3_R, 'DFW: kernel-level rules'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'T0: BGP to physical fabric'),
        bMid(B2_L, B2_R, 'T0/T1: routing config'),
        bMid(B3_L, B3_R, 'Gateway Firewall: N/S'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'T1: per-tenant routing'),
        bMid(B2_L, B2_R, 'Edge node: health + BFD'),
        bMid(B3_L, B3_R, 'IDS/IPS: signature-based'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'TEP: Geneve on VMk port'),
        bMid(B2_L, B2_R, 'DFW: policy + group mgmt'),
        bMid(B3_L, B3_R, 'Endpoint Protection'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Transport zone: overlay'),
        bMid(B2_L, B2_R, 'Alarms: BGP down, TEP'),
        bMid(B3_L, B3_R, 'NSX Intelligence: flow'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines overlay and routing · Operations manage segments and DFW'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['BGP session down', 'get logical-router', 'Manager: 3 nodes up', 'GSS: collect logs', 'nsxcli get route'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['TEP connectivity', 'ping ++netstack=vx', 'Edge: HA state UP?', 'TAM escalation', 'nsxcli get edge'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['DFW rule blocking', 'get firewall stats', 'TEP MTU: 1600 min', 'Collect tech-suppo', 'nsxcli get fw'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Segment not visibl', 'get transport-node', 'BGP neighbour up?', 'P1: network down', 'nsxcli get mgr'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ESXi hosts with TEP VMkernel NICs · physical ToR switches · BGP-capable fabric'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Geneve        = Generic Network Virtualisation Encapsulation; NSX overlay protocol (UDP 6081)'))
    lines.append(txt_row('TEP           = Tunnel End Point; VMkernel port on each host used for Geneve overlay traffic'))
    lines.append(txt_row('T0 Gateway    = Tier-0; connects NSX overlay to physical network via BGP or static routing'))
    lines.append(txt_row('T1 Gateway    = Tier-1; per-tenant router; provides east-west routing between segments'))
    lines.append(txt_row('DFW           = Distributed Firewall; stateful L4 firewall running in each ESXi kernel vNIC'))
    lines.append(txt_row('Segment       = NSX logical network (replaces port group); backed by Geneve overlay or VLAN'))
    lines.append(txt_row('Edge Node     = VM or bare-metal running T0/T1 data-plane services and gateway firewall'))
    lines.append(txt_row('Transport Zone= Scope boundary for overlay or VLAN segments; spans hosts and edge nodes'))
    lines.append(txt_row('BFD           = Bidirectional Forwarding Detection; fast failure detection for BGP peers'))
    lines.append(txt_row('NSX Manager   = Control and management plane; 3-node cluster for HA; single pane of glass'))
    lines.append(txt_row('IDS/IPS       = Intrusion Detection/Prevention System; signature-based; east-west traffic'))
    lines.append(txt_row('Microsegment  = Zero-trust network policy per workload; DFW rules by VM tag or group'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan',
    'docs/virtualization/vmware/vsan/index.md',
    'vSAN Stack — disk groups, SPBM policies, FTT, resync, D@RE, vSAN ESA',
)
def vsan_stack():
    """vSAN Software-Defined Storage Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSAN Software-Defined Storage Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware vSAN — Hyper-Converged Software-Defined Storage')))
    lines.append(R(bMid(IV_L, IV_R, 'Object-based storage: VMs stored as objects distributed across hosts in the cluster')))
    lines.append(R(bMid(IV_L, IV_R, 'Disk groups (OSA): 1 cache device + 1-7 capacity devices per host; or vSAN ESA (all-NVMe)')))
    lines.append(R(bMid(IV_L, IV_R, 'SPBM policies: FTT (failures to tolerate), stripe width, dedup/compression, encryption')))
    lines.append(R(bMid(IV_L, IV_R, 'Resync: data rebuilds after host/disk failure; controlled by I/O scheduler')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Disk groups form the storage layer · SPBM policies govern data protection'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Disk group: cache+capacity'),
        bMid(B2_L, B2_R, 'SPBM: policy per VM'),
        bMid(B3_L, B3_R, 'D@RE: AES-256 at rest'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'FTT: RAID-1/5/6 tolerance'),
        bMid(B2_L, B2_R, 'Capacity: usage + forecast'),
        bMid(B3_L, B3_R, 'In-transit: encryption on'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Witness host: stretched'),
        bMid(B2_L, B2_R, 'Health: proactive checks'),
        bMid(B3_L, B3_R, 'KMS: external key server'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSAN ESA: NVMe-only tier'),
        bMid(B2_L, B2_R, 'Resync: monitor + throttle'),
        bMid(B3_L, B3_R, 'RBAC: vSAN roles'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Dedup+compression: cluster'),
        bMid(B2_L, B2_R, 'Disk group: add/remove'),
        bMid(B3_L, B3_R, 'Audit log: config changes'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines the disk groups · Operations manage policies and capacity'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Non-compliant objs', 'vsan.health.health', 'Health: all green?', 'GSS: collect logs', 'esxcli vsan'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Disk group failure', 'vsan.disks_stats', 'Capacity <70%?', 'TAM escalation', 'rvc vsan.check'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Resync: high delay', 'vsan.resync_dashbo', 'Resync: <1%?', 'Log bundle req', 'rvc vsan.summary'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Performance: high ', 'vsan.perf.stats', 'FTT: compliant?', 'P1: data at risk', 'cmmds-tool find'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ESXi hosts with NVMe/SSD disks · vSAN VMkernel NICs (25 GbE min) · ToR switches · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SPBM          = Storage Policy-Based Management; assigns FTT, stripe, dedup rules per VM disk'))
    lines.append(txt_row('FTT           = Failures to Tolerate; RAID-1=1 host, RAID-5=1 host (4 needed), RAID-6=2 hosts'))
    lines.append(txt_row('Disk group    = Per-host grouping of 1 cache device + 1-7 capacity NVMe/SSD devices'))
    lines.append(txt_row('vSAN ESA      = Express Storage Architecture; single-tier all-NVMe; replaces OSA disk groups'))
    lines.append(txt_row('Resync        = Data rebuild after device or host failure; monitored via health dashboard'))
    lines.append(txt_row('D@RE          = Data at Rest Encryption; AES-256 per disk group; requires external KMS'))
    lines.append(txt_row('Witness host  = Tie-breaking third site in stretched cluster; holds metadata only, no data'))
    lines.append(txt_row('Dedup         = Deduplication applied at block level across disk group; cluster-wide or host-local'))
    lines.append(txt_row('CMMDS         = Cluster Monitoring, Membership, and Directory Services; vSAN metadata plane'))
    lines.append(txt_row('Stripe width  = Number of capacity devices a single object is striped across for performance'))
    lines.append(txt_row('RVC           = Ruby vSphere Console; CLI for vSAN health and capacity diagnostic commands'))
    lines.append(txt_row('Non-compliant = Object does not meet its assigned SPBM policy; usually after host/disk failure'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter',
    'docs/virtualization/vmware/vcenter/index.md',
    'vCenter Server Management Plane — VCSA, DRS, HA, SSO, ELM, LCM',
)
def vcenter_stack():
    """vCenter Server Management Plane — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vCenter Server Management Plane'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware vCenter Server (VCSA) — vSphere Management Control Plane')))
    lines.append(R(bMid(IV_L, IV_R, 'VCSA: Linux appliance running vCenter, PSC (embedded), and vPostgres database')))
    lines.append(R(bMid(IV_L, IV_R, 'Cluster services: DRS (workload balancing) · HA (host failure restart) · DPM (power mgmt)')))
    lines.append(R(bMid(IV_L, IV_R, 'SSO: identity source (AD/LDAP); vCenter single sign-on for all Aria and vSphere tools')))
    lines.append(R(bMid(IV_L, IV_R, 'Linked mode: multiple vCenters share inventory via Enhanced Linked Mode (ELM)')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  VCSA is the management hub · DRS/HA automate cluster operations · SSO unifies authentication'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VCSA: embedded PSC+DB'),
        bMid(B2_L, B2_R, 'Cluster: DRS + HA rules'),
        bMid(B3_L, B3_R, 'SSO: AD identity source'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'DRS: VM workload balance'),
        bMid(B2_L, B2_R, 'Snapshot: create+manage'),
        bMid(B3_L, B3_R, 'RBAC: roles + global perms'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'HA: heartbeat + restart'),
        bMid(B2_L, B2_R, 'LCM: host patching'),
        bMid(B3_L, B3_R, 'TLS: cert replace + renew'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ELM: multi-vCenter view'),
        bMid(B2_L, B2_R, 'vMotion: live migration'),
        bMid(B3_L, B3_R, '2FA: RSA/RADIUS/Duo'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vDS: distributed switching'),
        bMid(B2_L, B2_R, 'Alarms: configure + ack'),
        bMid(B3_L, B3_R, 'Audit: tasks + events log'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines the management plane · Operations run day-to-day tasks'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SSO login failure', 'vc-support bundle', 'VCSA health: OK?', 'GSS: collect logs', 'govc ls /dc'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['DRS not migrating', 'vpxd.log review', 'DB disk <80%?', 'TAM escalation', 'govc vm.info'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['HA agent restart', 'service-control --', 'Services: running?', 'Collect vpxd.log', 'govc cluster.usage'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cert expired alert', 'python /usr/lib/vm', 'Certs: expiry OK?', 'P1: mgmt plane dow', 'govc events'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('VCSA VM on ESXi host · vSphere cluster hosts · shared datastore for VCSA · network for port 443/8443'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VCSA          = vCenter Server Appliance; Photon OS Linux VM running vCenter and embedded PSC'))
    lines.append(txt_row('DRS           = Distributed Resource Scheduler; migrates VMs via vMotion to balance cluster load'))
    lines.append(txt_row('HA            = vSphere High Availability; restarts VMs on surviving hosts after host failure'))
    lines.append(txt_row('SSO           = Single Sign-On; vCenter identity service; integrates AD/LDAP identity sources'))
    lines.append(txt_row('ELM           = Enhanced Linked Mode; joins multiple vCenter instances to share inventory view'))
    lines.append(txt_row('DPM           = Distributed Power Management; consolidates workloads and powers off idle hosts'))
    lines.append(txt_row('vDS           = vSphere Distributed Switch; centrally managed virtual switch across all cluster hosts'))
    lines.append(txt_row('PSC           = Platform Services Controller; handles SSO, certs, licensing; now embedded in VCSA'))
    lines.append(txt_row('LCM           = Lifecycle Manager; manages ESXi patching baselines and cluster remediation'))
    lines.append(txt_row('govc          = Go-based vSphere CLI; faster than PowerCLI for scripting; uses GOVC_URL env var'))
    lines.append(txt_row('vpxd.log      = Main vCenter service log; first place to check for management plane errors'))
    lines.append(txt_row('HA heartbeat  = vCenter and datastore heartbeat; determines host isolation vs failure'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf',
    'docs/virtualization/vmware/vmware-cloud-foundation/index.md',
    'VCF Full Stack — SDDC Manager, management domain, workload domains, LCM, CloudBuilder',
)
def vcf_stack():
    """VMware Cloud Foundation Full-Stack Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VMware Cloud Foundation (VCF) Full Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Cloud Foundation — Integrated Private Cloud Platform')))
    lines.append(R(bMid(IV_L, IV_R, 'SDDC Manager: lifecycle orchestration for vCenter, NSX, vSAN, and workload domains')))
    lines.append(R(bMid(IV_L, IV_R, 'Management Domain: first domain; runs SDDC Manager, vCenter, NSX Manager, vSAN')))
    lines.append(R(bMid(IV_L, IV_R, 'Workload Domains: VI (vSphere+vSAN+NSX) or VVF (VI+Tanzu); up to 15 per SDDC')))
    lines.append(R(bMid(IV_L, IV_R, 'Bring-up: CloudBuilder deploys VCF from Day 0; creates management domain automatically')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  SDDC Manager orchestrates · management domain runs platform services · workload domains host apps'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SDDC Manager: LCM core'),
        bMid(B2_L, B2_R, 'SOS: health diagnostics'),
        bMid(B3_L, B3_R, 'SDDC Mgr RBAC: roles'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Mgmt domain: 4+ hosts'),
        bMid(B2_L, B2_R, 'LCM: bundle + upgrade'),
        bMid(B3_L, B3_R, 'Cert rotation: all comps'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Workload domain: VI/VVF'),
        bMid(B2_L, B2_R, 'Password rotation: SDDC'),
        bMid(B3_L, B3_R, 'Security baseline: DISA'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NSX: overlay per domain'),
        bMid(B2_L, B2_R, 'Host commissioning'),
        bMid(B3_L, B3_R, 'KMS: key mgmt for vSAN'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CloudBuilder: day-0 deploy'),
        bMid(B2_L, B2_R, 'Network pools: IP blocks'),
        bMid(B3_L, B3_R, 'Compliance: audit + log'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines domain layout · Operations execute LCM and commissioning'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LCM upgrade fail', 'SOS health-check', 'SDDC Mgr: running?', 'GSS: SOS bundle', 'sddc-manager api'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Domain add fail', 'vcf-support bundle', 'Domain state: UP?', 'TAM escalation', 'sddc-manager hosts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['NSX cert rotation', 'SDDC Mgr UI logs', 'LCM state: OK?', 'Collect all logs', 'sddc-manager domai'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Password out-of-sy', 'SOS password-check', 'Certs valid +30d?', 'P1: mgmt domain', 'sddc-manager certs'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Rack servers (HCL certified) · 25 GbE ToR switches · management network · vSAN-ready NVMe/SSD drives'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SDDC Manager  = VCF orchestration appliance; manages lifecycle, inventory, passwords, and'))
    lines.append(txt_row('Workload Domain= Isolated vSphere+vSAN+NSX instance for a workload type; VI or VVF flavour'))
    lines.append(txt_row('VI Domain     = vSphere Infrastructure domain; vCenter + NSX + vSAN for VM workloads'))
    lines.append(txt_row('VVF Domain    = vSphere with Tanzu; VI domain plus Supervisor Cluster for Kubernetes'))
    lines.append(txt_row('CloudBuilder  = Day-0 VCF deployment appliance; validates HW and deploys management domain'))
    lines.append(txt_row('LCM           = Lifecycle Management; SDDC Manager downloads bundles and upgrades all components'))
    lines.append(txt_row('SOS           = SDDC Operations Support; health-check and log bundle tool in VCF'))
    lines.append(txt_row('Network Pool  = IP address range assigned in SDDC Manager for VMkernel port allocation'))
    lines.append(txt_row('Management Domain= First VCF domain; runs SDDC Manager, vCenter, NSX Manager, vSAN'))
    lines.append(txt_row('Host commissioning= Adding a bare-metal host to SDDC Manager inventory before domain assignment'))
    lines.append(txt_row('Bundle        = LCM upgrade package downloaded from VMware depot containing product updates'))
    lines.append(txt_row('DISA STIG     = US government security baseline; VCF includes DISA STIG compliance profile'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-automation',
    'docs/virtualization/vmware/aria-automation/index.md',
    'Aria Automation Stack — blueprints, CAS, ABX, service catalogue, approval policies',
)
def aria_automation_stack():
    """Aria Automation (vRealize Automation) Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Automation Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Aria Automation — Infrastructure Automation and Service Catalogue')))
    lines.append(R(bMid(IV_L, IV_R, 'Blueprints (templates): IaC definitions for VMs, networks, storage, and cloud resources')))
    lines.append(R(bMid(IV_L, IV_R, 'Service Catalogue: self-service portal for end-users to request approved deployments')))
    lines.append(R(bMid(IV_L, IV_R, 'CAS: Cloud Assembly; where blueprints are designed and cloud accounts connected')))
    lines.append(R(bMid(IV_L, IV_R, 'ABX: Action-Based eXtensibility; serverless functions triggered on deployment events')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Blueprints define desired state · Service Catalogue delivers self-service · ABX extends automation'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CAS: cloud accounts'),
        bMid(B2_L, B2_R, 'Blueprint: design+version'),
        bMid(B3_L, B3_R, 'RBAC: org + project roles'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ABX: serverless actions'),
        bMid(B2_L, B2_R, 'Deployment: manage+delete'),
        bMid(B3_L, B3_R, 'Approval policies: gated'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Service Broker: catalogue'),
        bMid(B2_L, B2_R, 'Cloud account: sync'),
        bMid(B3_L, B3_R, 'Secrets: integrated vault'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pipelines: CI/CD IaC'),
        bMid(B2_L, B2_R, 'Content source: Git/vRO'),
        bMid(B3_L, B3_R, 'Content trust: signed'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Terraform: IaC provider'),
        bMid(B2_L, B2_R, 'Approval: request+grant'),
        bMid(B3_L, B3_R, 'Audit: deployment log'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines the platform · Operations manage deployments'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Deployment fails', 'vra-support bundle', 'Services: running?', 'GSS + bundle', 'vra-cli login'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Approval not firin', 'cloud-account sync', 'Cloud acct: sync OK', 'TAM escalation', 'vra-cli get deploy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Blueprint error', 'ABX action logs', 'ABX: runtime OK?', 'Collect service lo', 'vra-cli get bluepr'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Catalogue empty', 'content-source syn', 'Catalogue: publish?', 'P1: automation dow', 'vra-cli get reques'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Aria Automation VMs on vSphere cluster · vPostgres DB · NSX network segments · Aria Suite LCM'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Blueprint     = YAML IaC template defining VMs, networks, storage, and cloud resources'))
    lines.append(txt_row('CAS           = Cloud Assembly; blueprint designer and cloud account manager in Aria Automation'))
    lines.append(txt_row('ABX           = Action-Based eXtensibility; serverless functions (Python/JS/PS) on deploy events'))
    lines.append(txt_row('Service Broker= Catalogue front-end; users request approved items from published content sources'))
    lines.append(txt_row('Deployment    = Running instance of a blueprint; tracks provisioned resources and lifecycle'))
    lines.append(txt_row('Cloud Account = vSphere, AWS, Azure, or GCP connection supplying infrastructure endpoints'))
    lines.append(txt_row('Project       = RBAC boundary; groups users and cloud zones; controls blueprint deployment targets'))
    lines.append(txt_row('Content Source= Git repo or vRO connection feeding blueprint content into Service Catalogue'))
    lines.append(txt_row('Approval Policy= Workflow gate before deployment; requires named approver or group sign-off'))
    lines.append(txt_row('vRO           = vRealize Orchestrator; workflow engine integrated with Aria Automation'))
    lines.append(txt_row('Pipeline      = CI/CD pipeline in Aria Automation Pipelines; integrates Git, test, and deploy'))
    lines.append(txt_row('Terraform provider= Aria Automation Terraform service; manages Terraform state and runs plans'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-operations',
    'docs/virtualization/vmware/aria-operations/index.md',
    'Aria Operations Stack — analytics cluster, adapters, management packs, rightsizing',
)
def aria_operations_stack():
    """Aria Operations (vRealize Operations) Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Operations (vROps) Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Aria Operations — Performance, Capacity, and Compliance Management')))
    lines.append(R(bMid(IV_L, IV_R, 'Analytics cluster: master + replica + data nodes collect and correlate all metrics')))
    lines.append(R(bMid(IV_L, IV_R, 'Adapters: vSphere, vSAN, NSX, AWS, Azure, storage — each adds metric collection')))
    lines.append(R(bMid(IV_L, IV_R, 'Policies: alert thresholds, capacity model, workload placement, compliance benchmark')))
    lines.append(R(bMid(IV_L, IV_R, 'Rightsizing: reclaim wasted CPU/RAM; workload heatmaps; capacity forecasting')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Adapters collect metrics · analytics engine correlates · policies alert and guide optimisation'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Analytics: master+data'),
        bMid(B2_L, B2_R, 'Alert: configure+action'),
        bMid(B3_L, B3_R, 'RBAC: user + role mgmt'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Adapters: vSphere/NSX/S3'),
        bMid(B2_L, B2_R, 'Rightsizing: reclaim'),
        bMid(B3_L, B3_R, 'SSO: AD/vCenter login'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Management packs: extend'),
        bMid(B2_L, B2_R, 'Capacity: forecast+what-if'),
        bMid(B3_L, B3_R, 'Compliance: benchmark'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Policies: alert + capacity'),
        bMid(B2_L, B2_R, 'Dashboard: build+share'),
        bMid(B3_L, B3_R, 'TLS: cert management'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Remote collector: scale'),
        bMid(B2_L, B2_R, 'Report: schedule+export'),
        bMid(B3_L, B3_R, 'Audit log: user actions'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture scales collection · Operations optimise the environment · Security controls access'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Adapter not coll.', 'vrops-support bund', 'Analytics: online?', 'GSS + bundle', 'vrops-cli cluster'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Alert storm: noise', 'adapter-log review', 'Adapter: green?', 'TAM escalation', 'vrops-cli alerts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Disk filling up', 'vsan/disk usage', 'Disk: >70%?', 'Collect app logs', 'vrops-cli capacity'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['No capacity data', 'Analytics node log', 'Data age: <15 min?', 'P1: analytics fail', 'vrops-cli objects'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Aria Operations VMs (master/replica/data/RC) · vSphere cluster · shared datastore'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Analytics node= Aria Operations cluster member that stores and processes collected metric data'))
    lines.append(txt_row('Adapter       = Plugin collecting metrics from a source (vSphere, NSX, vSAN, AWS, storage)'))
    lines.append(txt_row('Management Pack= Bundle of adapters, dashboards, alerts, and policies for a specific product'))
    lines.append(txt_row('Policy        = Configuration for alert thresholds, capacity model, and compliance benchmark'))
    lines.append(txt_row('Rightsizing   = Recommendations to reclaim oversized vCPU/vRAM allocations from idle VMs'))
    lines.append(txt_row('Remote Collector= Aria Operations node deployed close to data source; forwards to analytics cluster'))
    lines.append(txt_row('Compliance    = Benchmark checks (CIS, DISA STIG, PCI-DSS) against collected configuration data'))
    lines.append(txt_row('Heatmap       = Visual grid showing resource utilisation across VMs, hosts, or clusters'))
    lines.append(txt_row('What-if       = Capacity scenario modelling; simulates adding VMs or hosts to forecast headroom'))
    lines.append(txt_row('Alert         = Symptom-driven notification when metric breaches threshold defined in policy'))
    lines.append(txt_row('Workload      = Aria Operations concept; resource utilisation relative to demand and capacity'))
    lines.append(txt_row('Report        = Scheduled or on-demand export of capacity, alerts, or compliance data as PDF/CSV'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── VMware product diagrams — batch 2 of 2 ────────────────────────────────────

@kb_diagram(
    'aria-logs',
    'docs/virtualization/vmware/aria-operations-for-logs/index.md',
    'Aria Operations for Logs Stack — log ingestion, content packs, alerts, webhooks',
)
def aria_logs_stack():
    """Aria Operations for Logs Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Operations for Logs Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Aria Operations for Logs — Centralised Log Management and Analysis')))
    lines.append(R(bMid(IV_L, IV_R, 'Log ingestion: syslog (UDP/TCP 514), CFAPI agents on VMs, Fluentd forwarding')))
    lines.append(R(bMid(IV_L, IV_R, 'Content packs: pre-built dashboards and queries for vSphere, NSX, ESXi, Linux, Windows')))
    lines.append(R(bMid(IV_L, IV_R, 'Interactive analytics: live-tail, field extraction, regex filters, time-window search')))
    lines.append(R(bMid(IV_L, IV_R, 'Alerts: query-based triggers; webhooks to PagerDuty, Slack, ServiceNow, or email')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Ingestion receives logs · analytics queries them · alerts and dashboards surface insights'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Master+worker nodes'),
        bMid(B2_L, B2_R, 'Log search: query+filter'),
        bMid(B3_L, B3_R, 'RBAC: AD + local users'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'syslog: UDP/TCP 514'),
        bMid(B2_L, B2_R, 'Content pack: install'),
        bMid(B3_L, B3_R, 'TLS: syslog encrypted'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CFAPI agent: per-VM'),
        bMid(B2_L, B2_R, 'Alert: query + webhook'),
        bMid(B3_L, B3_R, 'SSO: vCenter login'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Forwarder: to SIEM'),
        bMid(B2_L, B2_R, 'Dashboard: build+share'),
        bMid(B3_L, B3_R, 'Retention: policy set'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Disk: retention sizing'),
        bMid(B2_L, B2_R, 'Agent group: bulk mgmt'),
        bMid(B3_L, B3_R, 'Audit: admin actions'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture ingests logs · Operations search and alert · Security controls access and retention'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Logs not arriving', 'System diagnostics', 'Ingest rate: OK?', 'GSS + bundle', 'li-admin status'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Disk full: purging', 'Disk usage check', 'Disk: >70% used?', 'TAM escalation', 'li-admin cluster'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Alert not firing', 'Alert query debug', 'Alert: enabled?', 'Collect app logs', 'li-admin alerts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Content pack error', 'content-pack.log', 'Packs: installed?', 'P1: log loss event', 'li-admin packs'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Aria Logs VMs (master+worker) · large /storage/core disk · syslog network paths · Aria Suite LCM'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CFAPI agent   = Log agent installed on VMs; forwards structured logs via CFAPI protocol on port 9543'))
    lines.append(txt_row('Content pack  = Pre-built bundle of log queries, dashboards, and alerts for a specific product'))
    lines.append(txt_row('Field extract = Named regex capture group applied to log messages to create queryable fields'))
    lines.append(txt_row('Agent group   = Logical grouping of CFAPI agents sharing the same configuration and filters'))
    lines.append(txt_row('Webhook       = HTTP callback for alerts; sends payload to Slack, PagerDuty, or custom URL'))
    lines.append(txt_row('Forwarder     = Sends matching log events to a remote syslog target or SIEM for correlation'))
    lines.append(txt_row('Interactive analytics= Live log search with regex, field filters, and time window; no pre-indexing'))
    lines.append(txt_row('Retention     = Policy setting number of days logs are kept before purging; constrained by disk'))
    lines.append(txt_row('Master node   = Primary Aria Logs node; holds index and coordinates worker nodes in cluster'))
    lines.append(txt_row('Worker node   = Additional Aria Logs node adding ingestion capacity and search throughput'))
    lines.append(txt_row('syslog        = UDP/TCP port 514 protocol; most infrastructure devices send logs via syslog'))
    lines.append(txt_row('li-admin      = Aria Logs admin CLI; cluster status, disk usage, configuration management'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-networks',
    'docs/virtualization/vmware/aria-operations-for-networks/index.md',
    'Aria Operations for Networks Stack — path analysis, IPFIX flows, physical topology',
)
def aria_networks_stack():
    """Aria Operations for Networks Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Operations for Networks Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Aria Operations for Networks — Network Visibility and Troubleshooting')))
    lines.append(R(bMid(IV_L, IV_R, 'Path analysis: end-to-end network path between source and destination VMs or IPs')))
    lines.append(R(bMid(IV_L, IV_R, 'Flow analytics: IPFIX/NetFlow collection; application traffic maps; top talkers')))
    lines.append(R(bMid(IV_L, IV_R, 'Physical topology: autodiscovered switch/router map integrated with NSX overlay view')))
    lines.append(R(bMid(IV_L, IV_R, 'Security: network exposure analysis; identifies unintended external reachability')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Collectors gather flows · path analysis traces packets · topology maps the full network'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Platform + collectors'),
        bMid(B2_L, B2_R, 'Path analysis: src→dst'),
        bMid(B3_L, B3_R, 'Exposure: internet reach'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NSX: overlay + DFW data'),
        bMid(B2_L, B2_R, 'Flow: top talker + app'),
        bMid(B3_L, B3_R, 'Security groups: view'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'IPFIX/NetFlow: from hosts'),
        bMid(B2_L, B2_R, 'Physical topology: map'),
        bMid(B3_L, B3_R, 'Alert: exposure + drift'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Physical: SNMP discover'),
        bMid(B2_L, B2_R, 'Alert: path change'),
        bMid(B3_L, B3_R, 'RBAC: user + role'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vCenter: VM + NIC data'),
        bMid(B2_L, B2_R, 'Network intent: plan'),
        bMid(B3_L, B3_R, 'Compliance: check rules'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture collects network data · Operations trace paths and flows · Security surfaces exposure'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['No flow data', 'Collector logs', 'Collector: online?', 'GSS + bundle', 'vrni-cli cluster'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Path shows blocked', 'path analysis log', 'Data source: sync?', 'TAM escalation', 'vrni-cli sources'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Topology missing', 'SNMP poll debug', 'Phys topo: OK?', 'Collect app logs', 'vrni-cli flows'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['NSX not integrated', 'NSX credential che', 'NSX data: current?', 'P1: net blind spot', 'vrni-cli alerts'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Aria Networks VMs (platform+collectors) · SNMP access to switches · IPFIX from ESXi hosts'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Path analysis = Traces every hop from source to destination; shows NSX DFW rules that allow/block'))
    lines.append(txt_row('IPFIX         = IP Flow Information Export; flow telemetry from ESXi/NSX to collectors'))
    lines.append(txt_row('Collector     = Aria Networks remote node that receives IPFIX/NetFlow and forwards to platform'))
    lines.append(txt_row('Physical topology= Auto-discovered map of switches, routers, and links via SNMP and LLDP/CDP'))
    lines.append(txt_row('Flow          = Recorded network conversation: src/dst IP, port, protocol, byte count, duration'))
    lines.append(txt_row('Network intent= Policy that describes desired connectivity; Aria Networks validates compliance'))
    lines.append(txt_row('Exposure      = VM or service reachable from internet/untrusted network; flagged as security risk'))
    lines.append(txt_row('Application   = Auto-discovered group of VMs that communicate; basis for microsegmentation planning'))
    lines.append(txt_row('Top talker    = VM or IP generating the highest volume of network flows in a time window'))
    lines.append(txt_row('NSX integration= Aria Networks pulls DFW rule, segment, and group data directly from NSX Manager'))
    lines.append(txt_row('SNMP          = Simple Network Management Protocol; used to poll physical switch for topology data'))
    lines.append(txt_row('Data source   = vCenter, NSX, or physical device added to Aria Networks for data collection'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-lcm',
    'docs/virtualization/vmware/aria-suite-lifecycle/index.md',
    'Aria Suite Lifecycle Manager — deploy/upgrade Aria products, cert manager, Locker',
)
def aria_lcm_stack():
    """Aria Suite Lifecycle Manager Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Suite Lifecycle Manager Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Aria Suite Lifecycle Manager (Aria SuiteLC) — Aria Product LCM')))
    lines.append(R(bMid(IV_L, IV_R, 'Deploys and upgrades: Aria Operations, Logs, Networks, Automation, and Workspace ONE')))
    lines.append(R(bMid(IV_L, IV_R, 'Environment: logical grouping of Aria products sharing vSphere infra and certificates')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate manager: Aria SuiteLC manages TLS certs for all Aria products centrally')))
    lines.append(R(bMid(IV_L, IV_R, 'Locker: secure credential store for passwords, certificates, and licence keys')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Aria SuiteLC deploys products · manages their certs and passwords · executes upgrades'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Global env: infra acct'),
        bMid(B2_L, B2_R, 'Deploy: product wizard'),
        bMid(B3_L, B3_R, 'Locker: creds + certs'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Product env: Aria suite'),
        bMid(B2_L, B2_R, 'Upgrade: binary + apply'),
        bMid(B3_L, B3_R, 'Cert replace: all prods'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Binary mapping: depot'),
        bMid(B2_L, B2_R, 'Cert: rotate on demand'),
        bMid(B3_L, B3_R, 'RBAC: admin + viewer'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSphere: infra account'),
        bMid(B2_L, B2_R, 'Health: env health check'),
        bMid(B3_L, B3_R, 'Password: scheduled rot'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Upgrade checker: pre-val'),
        bMid(B2_L, B2_R, 'Scale: node add/remove'),
        bMid(B3_L, B3_R, 'Audit: change log'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines environments · Operations deploy and upgrade'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Upgrade precheck f', 'lcm-support bundle', 'Env health: green?', 'GSS + bundle', 'lcm-cli status'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cert rotation fail', 'certificate.log', 'Certs: valid +30d?', 'TAM escalation', 'lcm-cli certs'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Product deploy stu', 'product-install.lo', 'Binary: available?', 'Collect install lo', 'lcm-cli products'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Locker credential ', 'locker-service.log', 'Locker: reachable?', 'P1: LCM failure', 'lcm-cli locker'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Aria SuiteLC VM on vSphere · vSphere infrastructure account · NFS/VMFS datastore · port 443'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Global environment= Aria SuiteLC top-level container; links to vSphere infra account and NTP/DNS'))
    lines.append(txt_row('Product environment= Named grouping of Aria products sharing an infra account and cert authority'))
    lines.append(txt_row('Infrastructure account= vCenter service account used by Aria SuiteLC to deploy product VMs'))
    lines.append(txt_row('Locker        = Secure vault inside Aria SuiteLC; stores passwords, certs, and licence keys'))
    lines.append(txt_row('Binary mapping = Links downloaded product installer to a product version for deployment/upgrade'))
    lines.append(txt_row('Upgrade checker= Pre-upgrade compatibility validation; checks versions and health before proceeding'))
    lines.append(txt_row('Certificate manager= Aria SuiteLC module that generates, replaces, and renews TLS certs for products'))
    lines.append(txt_row('Content management= Feature to import/export Aria product config (blueprints, dashboards) via LCM'))
    lines.append(txt_row('Password rotation= Scheduled or manual rotation of product service account passwords via Locker'))
    lines.append(txt_row('Scale out     = Adding nodes to a product (e.g. vROps data node) managed through Aria SuiteLC'))
    lines.append(txt_row('Health check  = Aria SuiteLC environment health scan; validates products, certs, and credentials'))
    lines.append(txt_row('Depot         = VMware Customer Connect binary source; Aria SuiteLC downloads product binaries'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon',
    'docs/virtualization/vmware/horizon/index.md',
    'Horizon VDI Stack — Connection Server, UAG, desktop pools, App Volumes, DEM',
)
def horizon_stack():
    """VMware Horizon VDI Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VMware Horizon VDI Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Horizon — Virtual Desktop and App Delivery Platform')))
    lines.append(R(bMid(IV_L, IV_R, 'Connection Server: broker authenticating users and directing them to desktop pools')))
    lines.append(R(bMid(IV_L, IV_R, 'UAG: Unified Access Gateway; external proxy terminating Blast/PCoIP from internet')))
    lines.append(R(bMid(IV_L, IV_R, 'Desktop pools: instant clone (fast provision), linked clone, or full-clone pools')))
    lines.append(R(bMid(IV_L, IV_R, 'App Volumes: application layering; real-time delivery via AppStacks and WritableVolumes')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Connection Server brokers sessions · UAG secures external access · pools deliver desktops'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Connection Server HA'),
        bMid(B2_L, B2_R, 'Pool: provision+resize'),
        bMid(B3_L, B3_R, 'Smart card + MFA auth'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'UAG: Blast/PCoIP proxy'),
        bMid(B2_L, B2_R, 'Session: monitor+reset'),
        bMid(B3_L, B3_R, 'UAG: cert + TLS config'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Instant clone: parent VM'),
        bMid(B2_L, B2_R, 'App Volumes: AppStack'),
        bMid(B3_L, B3_R, 'DEM: user env policy'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ADAM: CS config DB'),
        bMid(B2_L, B2_R, 'Certificate: renew CS'),
        bMid(B3_L, B3_R, 'Blast: protocol lockdown'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'DEM: user profile mgmt'),
        bMid(B2_L, B2_R, 'Events DB: query logs'),
        bMid(B3_L, B3_R, 'Entitlement: AD group'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines the brokering stack · Operations manage pools and sessions'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Login loop: CS che', 'Horizon events DB', 'CS: services up?', 'GSS + CS log bundl', 'vdmadmin -l'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Black screen: blas', 'UAG edge log', 'UAG: reachable?', 'TAM escalation', 'vdmadmin -A'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Pool not provision', 'instant-clone.log', 'Pool: available VMs', 'Collect debug log', 'vdmadmin -n'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['App Volumes not mo', 'AppVolumes.log', 'AppStack: attached?', 'P1: VDI outage', 'vdmadmin -c'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vSphere cluster for VDI VMs · Connection Server Windows VMs · UAG VMs in DMZ · GPU hosts if needed'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Connection Server= Windows service brokering user sessions to desktop pools; requires AD membership'))
    lines.append(txt_row('UAG           = Unified Access Gateway; DMZ appliance proxying Blast/PCoIP without VPN'))
    lines.append(txt_row('Desktop pool  = Collection of VMs or RDS hosts assigned to users; persistent or floating'))
    lines.append(txt_row('Instant clone = Fast desktop provision using vmFork; creates linked child from running parent VM'))
    lines.append(txt_row('Linked clone  = Template-based pool sharing a parent snapshot; saves storage vs full clone'))
    lines.append(txt_row('App Volumes   = Application layering; AppStack VMDK attached at login; WritableVolume for user data'))
    lines.append(txt_row('DEM           = Dynamic Environment Manager; user profile and policy management for VDI sessions'))
    lines.append(txt_row('Blast         = VMware display protocol; H.264/H.265; works over HTTPS 443; preferred for WAN'))
    lines.append(txt_row('PCoIP         = PC-over-IP; Teradici display protocol; UDP 4172; good for LAN/graphics'))
    lines.append(txt_row('ADAM          = Active Directory Application Mode; Connection Server internal config database'))
    lines.append(txt_row('Entitlement   = AD user or group granted access to a pool or application in Horizon'))
    lines.append(txt_row('vdmadmin      = Horizon CLI; manage users, entitlements, machines, and Connection Server config'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'tanzu',
    'docs/virtualization/vmware/tanzu/index.md',
    'Tanzu Kubernetes Stack — Supervisor Cluster, TKG, vSphere namespaces, Harbor, TMC',
)
def tanzu_stack():
    """VMware Tanzu Kubernetes Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VMware Tanzu Kubernetes Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Tanzu — Enterprise Kubernetes on vSphere')))
    lines.append(R(bMid(IV_L, IV_R, 'Supervisor Cluster: vSphere-integrated Kubernetes control plane on ESXi hosts')))
    lines.append(R(bMid(IV_L, IV_R, 'TKG Workload Clusters: tenant Kubernetes clusters provisioned in vSphere namespaces')))
    lines.append(R(bMid(IV_L, IV_R, 'vSphere Namespace: resource boundary per team with CPU/RAM/storage quotas and RBAC')))
    lines.append(R(bMid(IV_L, IV_R, 'Harbor: private OCI-compliant registry; image scanning, replication, content trust')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Supervisor hosts the control plane · namespaces isolate tenants · TKG runs workload clusters'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Supervisor: Kubernetes CP'),
        bMid(B2_L, B2_R, 'Cluster: create+upgrade'),
        bMid(B3_L, B3_R, 'RBAC: namespace + cluster'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSphere namespace: quota'),
        bMid(B2_L, B2_R, 'Harbor: image push/pull'),
        bMid(B3_L, B3_R, 'Network policy: pod L4'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NSX-T CNI: pod networking'),
        bMid(B2_L, B2_R, 'kubectl + tanzu CLI'),
        bMid(B3_L, B3_R, 'PSA: pod security admit'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Harbor: OCI registry'),
        bMid(B2_L, B2_R, 'Carvel: package mgmt'),
        bMid(B3_L, B3_R, 'Image scan: Trivy/Clair'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'TMC: multi-cluster mgmt'),
        bMid(B2_L, B2_R, 'TMC: policy + lifecycle'),
        bMid(B3_L, B3_R, 'Audit: API server logs'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines the Kubernetes layers · Operations manage clusters'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cluster stuck: che', 'kubectl describe', 'Supervisor: healthy', 'GSS + bundle', 'tanzu cluster ls'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Pod pending: no no', 'kubectl get events', 'Nodes: Ready?', 'TAM escalation', 'kubectl get pods -'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Image pull: Harbor', 'Harbor harbor.log', 'Harbor: running?', 'Collect API logs', 'tanzu package ls'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['NSX CNI not ready', 'NSX node agent log', 'CNI: pods running?', 'P1: cluster down', 'kubectl get ns'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vSphere + vSAN cluster · NSX-T for pod networking · Harbor VM · management network + workload network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Supervisor Cluster= vSphere-integrated Kubernetes control plane running as ESXi kernel components'))
    lines.append(txt_row('TKG           = Tanzu Kubernetes Grid; tenant Kubernetes clusters deployed from Supervisor'))
    lines.append(txt_row('vSphere Namespace= Resource boundary with CPU/RAM/storage quotas; maps to Kubernetes namespace'))
    lines.append(txt_row('Harbor        = VMware open-source OCI registry; image scanning, replication, and content trust'))
    lines.append(txt_row('TMC           = Tanzu Mission Control; SaaS multi-cluster management, policy, and observability'))
    lines.append(txt_row('Carvel        = Tool suite (kapp, ytt, kbld, imgpkg) for Kubernetes packaging and deployment'))
    lines.append(txt_row('PSA           = Pod Security Admission; Kubernetes enforcer for restricted/baseline/privileged modes'))
    lines.append(txt_row('NSX CNI       = NSX-T container network interface; provides pod networking and policy for TKG'))
    lines.append(txt_row('Content trust = Harbor feature ensuring only signed images can be pulled; uses Notary/cosign'))
    lines.append(txt_row('RBAC          = Kubernetes Role-Based Access Control; ClusterRole, Role, RoleBinding,'))
    lines.append(txt_row('Network policy= Kubernetes L4 firewall rules between pods; enforced by NSX CNI in Tanzu'))
    lines.append(txt_row('tanzu CLI     = kubectl plugin for TKG; cluster create, upgrade, kubeconfig management'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'srm',
    'docs/virtualization/vmware/srm/index.md',
    'Site Recovery Manager Stack — site pair, protection groups, recovery plans, test failover',
)
def srm_stack():
    """VMware Site Recovery Manager Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VMware Site Recovery Manager Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Site Recovery Manager (SRM) — DR Orchestration Platform')))
    lines.append(R(bMid(IV_L, IV_R, 'Site pair: SRM Server at protected site paired with recovery site SRM Server')))
    lines.append(R(bMid(IV_L, IV_R, 'Protection groups: VMs grouped by replication method (vSphere Replication or array-based)')))
    lines.append(R(bMid(IV_L, IV_R, 'Recovery plans: ordered failover runbook — VM priority, IP mapping, startup scripts')))
    lines.append(R(bMid(IV_L, IV_R, 'Test failover: creates isolated test network bubble; no production impact during DR test')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Site pairing enables recovery · protection groups define scope'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SRM Server: per site'),
        bMid(B2_L, B2_R, 'Protection group: create'),
        bMid(B3_L, B3_R, 'RBAC: SRM roles'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Site pair: tunnel + cert'),
        bMid(B2_L, B2_R, 'Recovery plan: design'),
        bMid(B3_L, B3_R, 'Network isolation: test'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSphere Replication: RPO'),
        bMid(B2_L, B2_R, 'Test failover: validate'),
        bMid(B3_L, B3_R, 'TLS: site pair cert'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Array replication: SRA'),
        bMid(B2_L, B2_R, 'Planned migration: exec'),
        bMid(B3_L, B3_R, 'IP customisation: rules'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'IP mapping: prod→DR net'),
        bMid(B2_L, B2_R, 'Reprotect: reverse repl'),
        bMid(B3_L, B3_R, 'Audit: plan exec log'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture pairs sites · Operations execute and test recovery plans · Security governs DR access'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Plan fails: step e', 'SRM support bundle', 'Site pair: connecte', 'GSS + bundle', 'srm-util srmcli'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VR repl lag high', 'VR appliance log', 'VMs protected: yes?', 'TAM escalation', 'srm-util showvms'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Test cleanup stuck', 'recovery-plan.log', 'Test: cleanup OK?', 'Collect SRM log', 'srm-util plans'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['IP remap not appli', 'IP customisation c', 'IP map: configured?', 'P1: DR event', 'srm-util history'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SRM VM at protected site · SRM VM at recovery site · replication network · vCenter at each site'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRM Server    = Windows service (or VA) managing protection groups and recovery plans'))
    lines.append(txt_row('Site pair     = Trusted connection between two SRM Servers; established via certificate exchange'))
    lines.append(txt_row('Protection group= Set of VMs replicated together; associated with one or more recovery plans'))
    lines.append(txt_row('Recovery plan = Ordered failover script: VM priority groups, startup delays, IP mappings, scripts'))
    lines.append(txt_row('Test failover = Validates recovery plan; VMs start in isolated network; no production impact'))
    lines.append(txt_row('Planned migration= Controlled move of workloads to recovery site; apps shut down cleanly at source'))
    lines.append(txt_row('Reprotect     = Reverses replication direction after failover; makes DR site the new protected site'))
    lines.append(txt_row('vSphere Replication= Built-in VM replication engine; RPO 5 minutes or more; host-based delta sync'))
    lines.append(txt_row('SRA           = Storage Replication Adapter; plugin allowing SRM to use array-based replication'))
    lines.append(txt_row('IP customisation= Rules mapping VM IP addresses from production subnet to recovery site subnet'))
    lines.append(txt_row('Test bubble   = Isolated network created during test failover; VMs boot but cannot reach production'))
    lines.append(txt_row('RPO           = Recovery Point Objective; maximum acceptable data loss; drives replication frequency'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsphere-replication',
    'docs/virtualization/vmware/vsphere-replication/index.md',
    'vSphere Replication Stack — VRMS, HBRSVC, delta sync, RPO, MPIT, failover/failback',
)
def vsphere_replication_stack():
    """vSphere Replication Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere Replication Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware vSphere Replication — VM-Level Asynchronous Replication')))
    lines.append(R(bMid(IV_L, IV_R, 'VR Server (VRMS): appliance per site managing replication config and site pairing')))
    lines.append(R(bMid(IV_L, IV_R, 'Delta sync: only changed disk blocks transmitted; compressed over replication network')))
    lines.append(R(bMid(IV_L, IV_R, 'RPO: configurable 5 min to 24 hours per VM; drives how often delta syncs occur')))
    lines.append(R(bMid(IV_L, IV_R, 'MPIT: Multiple Point-In-Time snapshots at target; retain recovery points for rollback')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  VR Server pairs sites · HBRSVC on ESXi sends deltas · RPO and MPIT control recovery options'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VRMS: site pair + config'),
        bMid(B2_L, B2_R, 'Configure: VM + RPO'),
        bMid(B3_L, B3_R, 'RBAC: VR roles in vCenter'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'HBRSVC: ESXi repl agent'),
        bMid(B2_L, B2_R, 'Monitor: lag + bandwidth'),
        bMid(B3_L, B3_R, 'TLS: site pair cert'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Delta sync: block-level'),
        bMid(B2_L, B2_R, 'MPIT: snapshot at target'),
        bMid(B3_L, B3_R, 'Encryption: in-transit'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RPO: 5 min to 24 hrs'),
        bMid(B2_L, B2_R, 'Failover: planned / forced'),
        bMid(B3_L, B3_R, 'Quiescing: app-consistent'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Seed: initial full copy'),
        bMid(B2_L, B2_R, 'Failback: reprotect VM'),
        bMid(B3_L, B3_R, 'Audit: vCenter events'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines replication data path · Operations monitor and execute failover'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Repl lag exceeds R', 'VRMS appliance log', 'RPO: met for all VM', 'GSS + bundle', 'vicfg-module VR'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Sync stuck at 0%', 'HBRSVC log on host', 'Site pair: connecte', 'TAM escalation', 'hbr-manager stat'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Full sync triggere', 'vr-transfer.log', 'Bandwidth: adequate', 'Collect VR logs', 'esxcli vr config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['MPIT: snapshot err', 'target-datastore l', 'MPIT: captured OK?', 'P1: repl loss', 'vr-manager status'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('VRMS appliance at each site · ESXi hosts running HBRSVC · replication network (dedicated or shared)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VRMS          = vSphere Replication Management Server; per-site VA; manages config and site pair'))
    lines.append(txt_row('HBRSVC        = Host-Based Replication Service; ESXi kernel module transmitting VM disk deltas'))
    lines.append(txt_row('Delta sync    = Incremental block-level replication; only changed disk regions are transmitted'))
    lines.append(txt_row('RPO           = Recovery Point Objective; minimum sync frequency; 5 min, 1 hr, or up to 24 hrs'))
    lines.append(txt_row('MPIT          = Multiple Point-In-Time; snapshots of replicated VM at target site for rollback'))
    lines.append(txt_row('Seed          = Initial full-copy replication; can be seeded from backup media to reduce WAN transfer'))
    lines.append(txt_row('Quiescing     = VSS/sync quiesce of VM guest before snapshot for application-consistent recovery'))
    lines.append(txt_row('Failover      = Powered-on recovery of replicated VM at target site; planned (clean) or forced'))
    lines.append(txt_row('Failback      = After failover: reprotect from recovery site back to original protected site'))
    lines.append(txt_row('Replication lag= Time between a change at source and its arrival at target; must stay under RPO'))
    lines.append(txt_row('Site pair     = VRMS-to-VRMS trust established via certificate exchange; required for replication'))
    lines.append(txt_row('Compression   = vSphere Replication compresses delta blocks in transit; reduces WAN bandwidth'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'esxi-architecture',
    'docs/virtualization/vmware/esxi/architecture/index.md',
    'ESXi Architecture — VMkernel, vmknic, storage stack, HA/DRS integration',
)
def esxi_architecture():
    """ESXi Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'ESXi — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware ESXi — Type-1 bare-metal hypervisor; VMkernel OS runs directly on server hardware')))
    lines.append(R(bMid(IV_L, IV_R, 'Deployed standalone, in vSphere cluster, vSAN cluster (HCI), or stretched cluster across sites')))
    lines.append(R(bMid(IV_L, IV_R, 'VMkernel ports isolate traffic: management, vMotion, vSAN, NFC, replication — one VMk per role')))
    lines.append(R(bMid(IV_L, IV_R, 'Storage: VMFS on SAN (FC/iSCSI/NVMe-oF), NFS datastores, or vSAN — accessed via HBAs + PSPs')))
    lines.append(R(bMid(IV_L, IV_R, 'Networking: vSS per host or vDS cluster-wide; port groups per workload; NIC teaming for HA')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines VMkernel internals · integrations connect vCenter and storage'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VMkernel: CPU/RAM sched'),
        bMid(B2_L, B2_R, 'vCenter: mgmt + HA/DRS'),
        bMid(B3_L, B3_R, 'Host naming std'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSwitch/vDS port groups'),
        bMid(B2_L, B2_R, 'SAN/NAS/vSAN storage'),
        bMid(B3_L, B3_R, 'BIOS/UEFI baseline'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'HBAs: FC/iSCSI/NVMe'),
        bMid(B2_L, B2_R, 'Backup: VADP via NBD'),
        bMid(B3_L, B3_R, 'VMkernel IP layout'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NIC teaming: active/stby'),
        bMid(B2_L, B2_R, 'Monitoring: Aria Ops'),
        bMid(B3_L, B3_R, 'NTP: 2 sources required'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cluster: HA/DRS/vSAN'),
        bMid(B2_L, B2_R, 'Identity: vCenter SSO'),
        bMid(B3_L, B3_R, 'VIB acceptance policy'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers VMkernel · integrations connect storage and monitoring'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VMkernel sched', 'vCenter plugin', 'Standalone host', 'Single ESXi', 'Naming std'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vSwitch/vDS', 'SAN/NAS/vSAN', 'vSphere cluster', '3+ hosts HA', 'BIOS baseline'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['HBA multipath', 'VADP backup', 'vSAN cluster', '3+ HCI hosts', 'VMk IP plan'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['HA/DRS model', 'Aria Ops intg', 'Stretched clstr', '4+ 2-per-site', 'VIB policy'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 server · CPUs (Intel/AMD) · RAM DIMMs · PCIe HBAs/NICs · SAS/NVMe disks · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VMkernel      = ESXi micro-kernel OS; schedules CPU/memory and handles I/O for all VMs on the host'))
    lines.append(txt_row('vSS           = vSphere Standard Switch; per-host virtual switch; port groups define VM networks'))
    lines.append(txt_row('vDS           = vSphere Distributed Switch; cluster-wide switch managed centrally by vCenter'))
    lines.append(txt_row('VMkernel port = VMk NIC for host services: management, vMotion, vSAN, NFC, or replication'))
    lines.append(txt_row('VMFS          = VM File System; cluster-aware filesystem on shared block storage for VMDK files'))
    lines.append(txt_row('HBA           = Host Bus Adapter; PCIe card connecting ESXi to FC SAN or iSCSI/NVMe storage'))
    lines.append(txt_row('PSP           = Path Selection Policy; multipathing algorithm: MRU, Fixed, or Round Robin per LUN'))
    lines.append(txt_row('HA            = vSphere High Availability; restarts VMs on surviving hosts after a host failure'))
    lines.append(txt_row('DRS           = Distributed Resource Scheduler; load-balances VMs across cluster hosts via vMotion'))
    lines.append(txt_row('vSAN          = Virtual SAN; pools local flash/HDD from ESXi hosts into a shared HCI datastore'))
    lines.append(txt_row('VADP          = vStorage APIs for Data Protection; backup vendor interface for consistent VM backup'))
    lines.append(txt_row('VIB           = vSphere Installation Bundle; ESXi software package; acceptance level governs install'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'esxi-operations',
    'docs/virtualization/vmware/esxi/operations/index.md',
    'ESXi Operations — patching, host profiles, maintenance mode, lifecycle',
)
def esxi_operations():
    """ESXi Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'ESXi — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'ESXi day-to-day operations: CLI commands, health checks, procedures, and lifecycle management')))
    lines.append(R(bMid(IV_L, IV_R, 'Daily: review host alarms in vCenter, check storage paths, confirm NTP sync and hardware health')))
    lines.append(R(bMid(IV_L, IV_R, 'Lifecycle: patch via VUM/LCM baselines; apply host profiles; update ESXi image in cluster')))
    lines.append(R(bMid(IV_L, IV_R, 'Backup: no built-in VM backup; use VADP-based solutions; host config backed up via host')))
    lines.append(R(bMid(IV_L, IV_R, 'Automation: esxcli scripting, PowerCLI, REST API, Ansible VMware modules for at-scale changes')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  CLI gives direct host access · lifecycle keeps hosts patched · automation scales daily operations'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Host alarms: vCenter'),
        bMid(B2_L, B2_R, 'VUM/LCM: baseline'),
        bMid(B3_L, B3_R, 'esxcli: namespaces'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Storage paths: esxcli'),
        bMid(B2_L, B2_R, 'Host profile: apply'),
        bMid(B3_L, B3_R, 'PowerCLI: host cmds'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NTP drift: check sync'),
        bMid(B2_L, B2_R, 'Patch: remediate task'),
        bMid(B3_L, B3_R, 'Ansible: VMware mods'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Hardware: iDRAC/iLO'),
        bMid(B2_L, B2_R, 'Update planner tool'),
        bMid(B3_L, B3_R, 'REST API: host ops'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'esxtop: perf monitor'),
        bMid(B2_L, B2_R, 'Boot bank: validate'),
        bMid(B3_L, B3_R, 'vSphere SDK scripts'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch drift early · lifecycle keeps hosts secure and current · automation reduces toil'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['esxcli system', 'Host: green?', 'Maint mode', 'VUM baseline', 'No native bkp'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['esxcli network', 'vSAN: resync', 'DRS evacuate', 'Image profile', 'VADP-based sol'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['esxcli storage', 'NTP: in sync', 'Host profile', 'Pre/post check', 'Host profile bk'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vim-cmd vmsvc', 'HW: iDRAC ok', 'Patch remediate', 'Boot bank ok', 'Restore: redep'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 server · CPUs · RAM DIMMs · PCIe HBAs/NICs · SAS/NVMe disks · iDRAC/iLO OOB management'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('esxcli        = ESXi CLI framework; namespaces: system, network, storage, vm, software, hardware'))
    lines.append(txt_row('esxtop        = ESXi real-time performance monitor; displays CPU/memory/disk/network per VM'))
    lines.append(txt_row('VUM           = vSphere Update Manager; baseline-based patching; scans, stages, and remediates'))
    lines.append(txt_row('LCM           = Lifecycle Manager; image-based ESXi patching integrated into vCenter 7+'))
    lines.append(txt_row('Host Profile  = Saved configuration template; applied to hosts to enforce configuration consistency'))
    lines.append(txt_row('Maintenance mode = Host state that migrates VMs away before patching or hardware maintenance'))
    lines.append(txt_row('Boot bank     = ESXi dual-bank boot; active and standby banks; rollback to standby if needed'))
    lines.append(txt_row('VADP          = vStorage APIs for Data Protection; backup vendor interface for quiesced VM snapshots'))
    lines.append(txt_row('vim-cmd       = ESXi CLI for VM operations: power on/off, snapshot, register, unregister'))
    lines.append(txt_row('vmkfstools    = ESXi CLI for VMDK operations: clone, resize, inflate, import/export'))
    lines.append(txt_row('iDRAC/iLO     = Out-of-band management; provides console access and hardware health independent of OS'))
    lines.append(txt_row('PowerCLI      = VMware PowerShell module for at-scale vSphere automation and reporting'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'esxi-security',
    'docs/virtualization/vmware/esxi/security/index.md',
    'ESXi Security — lockdown mode, RBAC, TLS, vSphere Trust Authority',
)
def esxi_security():
    """ESXi Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'ESXi — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'ESXi security layers: authentication, access control, encryption, and host hardening')))
    lines.append(R(bMid(IV_L, IV_R, 'Authentication: all management via vCenter SSO; direct host login via DCUI for break-glass only')))
    lines.append(R(bMid(IV_L, IV_R, 'Access: lockdown mode (normal/strict) restricts direct access; RBAC inherited from vCenter')))
    lines.append(R(bMid(IV_L, IV_R, 'Encryption: VM encryption via vSAN/storage policy; vMotion encrypted; vTPM per VM supported')))
    lines.append(R(bMid(IV_L, IV_R, 'Hardening: DISA STIG / VMware Security Guide baseline; SSH disabled; secure boot enabled')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication gates access · lockdown mode enforces vCenter-only management'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vCenter SSO: primary'),
        bMid(B2_L, B2_R, 'Lockdown: normal/strict'),
        bMid(B3_L, B3_R, 'VM encrypt: KMS/KMIP'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'DCUI: break-glass only'),
        bMid(B2_L, B2_R, 'RBAC from vCenter'),
        bMid(B3_L, B3_R, 'vMotion: encrypted'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Local root: min 1 acct'),
        bMid(B2_L, B2_R, 'Firewall: service rules'),
        bMid(B3_L, B3_R, 'vTPM: per-VM chip'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SSH: disabled by std'),
        bMid(B2_L, B2_R, 'Shell: time-limited'),
        bMid(B3_L, B3_R, 'Secure boot: UEFI'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'MFA: via vCenter SSO'),
        bMid(B2_L, B2_R, 'Syslog: to vRLI/SIEM'),
        bMid(B3_L, B3_R, 'vSAN encrypt: at rest'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication controls who logs in · access control limits what they can do'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vCenter SSO', 'Lockdown mode', 'VM encryption', 'SSH disabled', 'Syslog to SIEM'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['DCUI breakglass', 'RBAC inherit', 'vMotion encr', 'Secure boot on', 'vCenter events'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Local root: 1', 'Host FW rules', 'vTPM per VM', 'Shell: timed', 'Firewall audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SSH key auth', 'Shell access log', 'KMS/KMIP keys', 'DISA STIG align', 'Host log review'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 server · TPM 2.0 chip · UEFI firmware · iDRAC/iLO OOB management · Physical access controls'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Lockdown mode  = Host setting preventing direct access; all management must go through vCenter'))
    lines.append(txt_row('DCUI           = Direct Console User Interface; physical/IPMI console on ESXi host; break-glass'))
    lines.append(txt_row('vTPM           = Virtual Trusted Platform Module; per-VM emulated TPM 2.0 for BitLocker and'))
    lines.append(txt_row('KMS            = Key Management Server; external KMIP-compatible server for VM encryption keys'))
    lines.append(txt_row('KMIP           = Key Management Interoperability Protocol; standard API for KMS integration'))
    lines.append(txt_row('Secure Boot    = UEFI feature verifying ESXi VIB signatures; prevents loading unsigned modules'))
    lines.append(txt_row('vMotion encrypt = AES-256 encryption of vMotion traffic between ESXi hosts in vCenter 6.5+'))
    lines.append(txt_row('SSH            = Secure Shell; direct host CLI access; should be disabled per security baseline'))
    lines.append(txt_row('ESXi firewall  = Host-based firewall; rules control which services/IPs can reach VMkernel ports'))
    lines.append(txt_row('DISA STIG      = Defense Information Systems Agency Security Technical Implementation Guide for ESXi'))
    lines.append(txt_row('Host profile   = Configuration template that enforces security settings consistently across all hosts'))
    lines.append(txt_row('Syslog         = ESXi log forwarding to vRLI or external SIEM; configured via esxcli or host profile'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'esxi-troubleshooting',
    'docs/virtualization/vmware/esxi/troubleshooting/index.md',
    'ESXi Troubleshooting — PSOD, APD/PDL, DCUI, esxcli diagnostics',
)
def esxi_troubleshooting():
    """ESXi Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'ESXi — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'ESXi troubleshooting: common failure patterns, diagnostic commands, and escalation process')))
    lines.append(R(bMid(IV_L, IV_R, 'Common issues: PSOD (purple screen), host disconnect from vCenter, storage path loss, vMotion')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnostics: esxcli for live state, esxtop for real-time perf, vmkernel.log for kernel events')))
    lines.append(R(bMid(IV_L, IV_R, 'Log collection: vm-support bundle collects all host logs; attach to GSS support case')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: P1 for production VMs down; TAM escalation for critical/sustained incidents')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues define the triage path · diagnostics isolate root cause'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'PSOD: kernel panic'),
        bMid(B2_L, B2_R, 'esxtop: live perf'),
        bMid(B3_L, B3_R, 'vm-support bundle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Host disconnect vCtr'),
        bMid(B2_L, B2_R, 'vmkernel.log events'),
        bMid(B3_L, B3_R, 'GSS: P1/P2 case'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Storage path failure'),
        bMid(B2_L, B2_R, 'esxcli storage list'),
        bMid(B3_L, B3_R, 'TAM escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vMotion fail: VMk IP'),
        bMid(B2_L, B2_R, 'esxcli network cmd'),
        bMid(B3_L, B3_R, 'vmx + log bundle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'HA agent restart'),
        bMid(B2_L, B2_R, '/var/log/vmkernel'),
        bMid(B3_L, B3_R, 'HCL / BOM match'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics pinpoint root cause'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['PSOD / panic', 'esxtop -b -n5', '/var/log/vmk', 'vm-support.tgz', 'reboot host'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Host disconnect', 'esxcli storage', '/var/log/hostd', 'GSS P1 case', 'restart hostd'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Path APD/PDL', 'esxcli network', '/var/log/vpxa', 'TAM escalate', 'rescan HBAs'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vMotion fail', '/var/log/vmkw', '/var/log/syslog', 'HCL validate', 'HA restart VM'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 server · CPUs · RAM DIMMs · PCIe HBAs/NICs · SAS/NVMe disks · iDRAC/iLO OOB console'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('PSOD          = Purple Screen of Death; ESXi kernel panic; check /var/log/vmkernel for root cause'))
    lines.append(txt_row('APD           = All Paths Down; storage device unreachable; all paths to LUN failed simultaneously'))
    lines.append(txt_row('PDL           = Permanent Device Loss; storage reports device gone; triggers VM failover if HA'))
    lines.append(txt_row('vm-support    = ESXi log bundle collector; generates .tgz with all host logs for GSS cases'))
    lines.append(txt_row('hostd         = ESXi host agent; handles vCenter communication; restart if host shows disconnected'))
    lines.append(txt_row('vpxa          = vCenter agent on ESXi; proxies vCenter management; restart to fix vCenter disconnect'))
    lines.append(txt_row('esxtop        = ESXi real-time monitor; -b batch mode; -n iteration count; CSV output for analysis'))
    lines.append(txt_row('GSS           = Global Support Services; VMware/Broadcom support; P1=production down, P2=degraded'))
    lines.append(txt_row('TAM           = Technical Account Manager; named support resource; escalation for critical incidents'))
    lines.append(txt_row('HCL           = Hardware Compatibility List; validates server/driver/firmware combinations for ESXi'))
    lines.append(txt_row('BOM           = Bill of Materials; version matrix for ESXi, FW, and driver compatibility'))
    lines.append(txt_row('vmkfstools    = ESXi VMDK utility: clone, inflate, check, convert disk formats'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'nsx-architecture',
    'docs/virtualization/vmware/nsx/architecture/index.md',
    'NSX Architecture — manager cluster, control plane, transport nodes, DFW',
)
def nsx_architecture():
    """NSX Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NSX — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware NSX — software-defined networking; overlay fabric via GENEVE encapsulation on ESXi hosts')))
    lines.append(R(bMid(IV_L, IV_R, 'Manager cluster (3 nodes active/active) controls the control plane and policy API')))
    lines.append(R(bMid(IV_L, IV_R, 'Transport nodes: ESXi/KVM hosts and Edge nodes form the GENEVE overlay data plane')))
    lines.append(R(bMid(IV_L, IV_R, 'Tier-0 provides BGP/static routing to the physical network; Tier-1 connects tenant segments')))
    lines.append(R(bMid(IV_L, IV_R, 'Distributed Firewall (DFW) enforces microsegmentation at the vNIC level on every host')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines overlay mechanics · integrations connect physical network'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Manager: 3-node AAA'),
        bMid(B2_L, B2_R, 'vCenter: plugin'),
        bMid(B3_L, B3_R, 'Manager: L sizing'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Transport: ESXi/KVM'),
        bMid(B2_L, B2_R, 'BGP: ToR peers'),
        bMid(B3_L, B3_R, 'Edge: L/XL sizing'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Edge: routing + FW'),
        bMid(B2_L, B2_R, 'AD/LDAP for auth'),
        bMid(B3_L, B3_R, 'MTU: ≥1600 overlay'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'T0: physical BGP'),
        bMid(B2_L, B2_R, 'vSAN: storage intg'),
        bMid(B3_L, B3_R, 'BFD: keepalives'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'DFW: per-vNIC rules'),
        bMid(B2_L, B2_R, 'SIEM: syslog API'),
        bMid(B3_L, B3_R, 'IP plan: overlay/T0'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines overlay and routing · integrations connect physical fabric'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['GENEVE overlay', 'vCenter plugin', 'Manager 3-node', 'Greenfield', 'MTU ≥1600'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['T0/T1 routing', 'BGP ToR peers', 'Edge cluster HA', 'Brownfield', 'BFD timers'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['DFW vNIC rules', 'AD/LDAP auth', 'ECMP uplinks', 'Multi-site', 'IP addr plan'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Edge cluster', 'SIEM syslog', 'Overlay TZ', 'Federation', 'VLAN trunk std'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 servers (ESXi hosts) · ToR switches (BGP peers) · Physical NICs (uplinks) · Network fabric'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('GENEVE        = Generic Network Virtualization Encapsulation; NSX overlay protocol; encapsulates L2'))
    lines.append(txt_row('Transport node = ESXi host or Edge VM prepared for NSX; carries overlay traffic via GENEVE'))
    lines.append(txt_row('Manager cluster = 3-node NSX Manager in active/active/active; hosts control plane and Policy API'))
    lines.append(txt_row('Tier-0 (T0)   = NSX logical router with physical connectivity; BGP/static to ToR switches'))
    lines.append(txt_row('Tier-1 (T1)   = NSX logical router for tenant segments; connected to T0 for north-south routing'))
    lines.append(txt_row('DFW           = Distributed Firewall; stateful L4 firewall enforced at vNIC on every ESXi host'))
    lines.append(txt_row('Edge cluster  = Pool of NSX Edge nodes providing services: routing, NAT, load balancing, VPN'))
    lines.append(txt_row('TEP           = Tunnel End Point; VMkernel port on each transport node used for GENEVE encapsulation'))
    lines.append(txt_row('BFD           = Bidirectional Forwarding Detection; fast failure detection for BGP keepalives'))
    lines.append(txt_row('ECMP          = Equal-Cost Multi-Path; load-balances T0 uplinks across multiple ToR switch paths'))
    lines.append(txt_row('Microsegmentation = DFW policies that restrict lateral VM-to-VM traffic within the same VLAN/segment'))
    lines.append(txt_row('Transport Zone = NSX scope definition for overlay or VLAN segments; limits which hosts can connect'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'nsx-operations',
    'docs/virtualization/vmware/nsx/operations/index.md',
    'NSX Operations — manager cluster health, transport node prep, upgrade coordinator',
)
def nsx_operations():
    """NSX Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NSX — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'NSX operations: CLI commands, health checks, upgrade procedures, and automation')))
    lines.append(R(bMid(IV_L, IV_R, 'Daily: check Manager cluster health, Edge cluster state, transport node status, BGP peer state')))
    lines.append(R(bMid(IV_L, IV_R, 'Health: verify DFW rule sync on all hosts; confirm MPA connectivity; review alarm dashboard')))
    lines.append(R(bMid(IV_L, IV_R, 'Lifecycle: upgrade via NSX coordinator (Manager → Edge → host transport nodes in sequence)')))
    lines.append(R(bMid(IV_L, IV_R, 'Automation: NSX Policy REST API, Terraform NSX provider, PowerCLI NSX, Ansible modules')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily checks catch control plane drift · lifecycle upgrades in sequence'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Manager: cluster ok'),
        bMid(B2_L, B2_R, 'NSX coordinator'),
        bMid(B3_L, B3_R, 'Policy REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Edge: cluster state'),
        bMid(B2_L, B2_R, 'Manager upgrade 1st'),
        bMid(B3_L, B3_R, 'Terraform NSX'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Transport: node state'),
        bMid(B2_L, B2_R, 'Edge upgrade 2nd'),
        bMid(B3_L, B3_R, 'PowerCLI NSX mod'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'BGP: peer up/active'),
        bMid(B2_L, B2_R, 'Host TN upgrade 3rd'),
        bMid(B3_L, B3_R, 'Ansible: NSX role'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'DFW: rule count sync'),
        bMid(B2_L, B2_R, 'Version compat check'),
        bMid(B3_L, B3_R, 'nsxcli on edge'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch issues early · upgrade sequence prevents mismatch'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['nsxcli on edge', 'Manager: green', 'Add TN: prep', 'Coordinator', 'Config export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['get routes', 'Edge: cluster ok', 'BGP peer add', 'Mgr upgrade 1st', 'Policy API bkp'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['get logical-router', 'TN: state ok', 'Segment create', 'Edge upg 2nd', 'Restore: redep'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['set debug-level', 'BGP: peer up', 'DFW rule add', 'Host TN upg 3rd', 'Config backup'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 ESXi hosts · Edge VM nodes · ToR switches (BGP peers) · Physical NICs (TEP uplinks)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('nsxcli        = NSX Edge CLI; access via SSH or console; commands: get, set, debug namespaces'))
    lines.append(txt_row('NSX coordinator = Upgrade orchestrator built into NSX Manager; manages upgrade sequence and'))
    lines.append(txt_row('MPA           = Management Plane Agent; runs on each transport node; communicates with Manager'))
    lines.append(txt_row('Transport node = ESXi host or Edge VM enrolled in NSX; carries GENEVE overlay traffic'))
    lines.append(txt_row('BGP peer      = ToR switch NSX peers with for T0 uplink routing; BFD tracks peer state'))
    lines.append(txt_row('DFW rule sync = Verification that all hosts have the same distributed firewall rule count and policy'))
    lines.append(txt_row('Policy API    = NSX primary REST API (preferred over deprecated Manager API); intent-based config'))
    lines.append(txt_row('Terraform NSX = HashiCorp Terraform provider for NSX-T; automates segment, DFW, and routing config'))
    lines.append(txt_row('Edge cluster  = Group of Edge nodes providing routing/NAT/LB; HA active/standby or ECMP'))
    lines.append(txt_row('Config backup = NSX Manager periodic backup to SFTP; restores Manager config not data plane state'))
    lines.append(txt_row('Version compat = NSX and vSphere/vCenter version compatibility matrix; check before upgrade'))
    lines.append(txt_row('Ansible NSX   = VMware Ansible collection modules for NSX policy, segments, DFW, and routing'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'nsx-security',
    'docs/virtualization/vmware/nsx/security/index.md',
    'NSX Security — DFW microsegmentation, IDPS, RBAC, TLS, audit logging',
)
def nsx_security():
    """NSX Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NSX — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'NSX security: distributed firewall, microsegmentation, IDPS, URL filtering, and TLS inspection')))
    lines.append(R(bMid(IV_L, IV_R, 'Authentication: AD/LDAP integration; NSX admin roles; API token auth; vIDM/Workspace ONE SSO')))
    lines.append(R(bMid(IV_L, IV_R, 'Access control: RBAC roles (Enterprise Admin, Security Admin, Auditor); object-level')))
    lines.append(R(bMid(IV_L, IV_R, 'DFW microsegmentation: stateful L4 rules enforced at vNIC; east-west traffic control per VM')))
    lines.append(R(bMid(IV_L, IV_R, 'Advanced security: IDPS signatures, Gateway FW, URL filtering, TLS inspection on Edge')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication controls who manages NSX · RBAC limits scope'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AD/LDAP: roles'),
        bMid(B2_L, B2_R, 'Enterprise Admin'),
        bMid(B3_L, B3_R, 'IDPS: L7 sigs'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vIDM SSO: optional'),
        bMid(B2_L, B2_R, 'Security Admin'),
        bMid(B3_L, B3_R, 'Gateway FW: edge'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'API token: bearer'),
        bMid(B2_L, B2_R, 'Auditor: read-only'),
        bMid(B3_L, B3_R, 'URL filtering'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert-based API auth'),
        bMid(B2_L, B2_R, 'Object-level perms'),
        bMid(B3_L, B3_R, 'TLS inspection'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Audit log: all events'),
        bMid(B2_L, B2_R, 'Least privilege std'),
        bMid(B3_L, B3_R, 'DFW microseg rules'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth gates NSX access · RBAC scopes permissions · DFW and IDPS enforce east-west security policy'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'DFW/Security', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AD/LDAP roles', 'Enterprise Adm', 'DFW: L4 rules', 'TLS on API', 'Syslog export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vIDM SSO', 'Security Admin', 'IDPS: L7 sigs', 'Cert rotation', 'Event audit log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['API tokens', 'Auditor role', 'URL filtering', 'Default deny DFW', 'Role reviews'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cert-based auth', 'Object-level', 'TLS inspection', 'Min-perm API', 'SIEM forward'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 ESXi hosts · Edge VM nodes · ToR switches · Physical NICs · Out-of-band network management'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('DFW           = Distributed Firewall; stateful L4 rules enforced at VM vNIC on every ESXi host'))
    lines.append(txt_row('IDPS          = Intrusion Detection and Prevention System; L7 signature-based; runs on Edge nodes'))
    lines.append(txt_row('Gateway FW    = Stateful firewall on T0/T1 Edge; enforces north-south and inter-segment policy'))
    lines.append(txt_row('TLS inspection = NSX Edge decrypts and inspects HTTPS traffic; re-encrypts after inspection'))
    lines.append(txt_row('URL filtering  = Edge service blocking or categorizing HTTP/HTTPS URLs via category lookup'))
    lines.append(txt_row('Enterprise Admin = Full NSX RBAC role; manage all objects and system config'))
    lines.append(txt_row('Security Admin  = NSX role for managing DFW and security policy; no system config access'))
    lines.append(txt_row('Auditor        = Read-only NSX role; view all objects and logs; no write access'))
    lines.append(txt_row('vIDM           = VMware Identity Manager (Workspace ONE Access); provides SSO for NSX Manager UI'))
    lines.append(txt_row('Microsegmentation = Zero-trust approach using DFW to restrict lateral VM-to-VM communication'))
    lines.append(txt_row('API token      = Bearer token for REST API auth; generated per user/service; scoped to role'))
    lines.append(txt_row('Default deny   = DFW policy posture where all traffic is denied unless explicitly allowed by a rule'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'nsx-troubleshooting',
    'docs/virtualization/vmware/nsx/troubleshooting/index.md',
    'NSX Troubleshooting — transport node issues, BGP peering, DFW, support bundle',
)
def nsx_troubleshooting():
    """NSX Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NSX — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'NSX troubleshooting: transport node failures, routing issues, DFW drops, and escalation process')))
    lines.append(R(bMid(IV_L, IV_R, 'Common issues: TN prep failure, BGP peer down, DFW asymmetric drop, Manager unreachable')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnostics: nsxcli on Edge for routing state; connectivity checker; flow analysis API')))
    lines.append(R(bMid(IV_L, IV_R, 'Log collection: get-tech-support on Manager and Edge; attach bundle to GSS case')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: NSX support bundle; TAM for P1; verify vSphere and NSX version compatibility')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues define the triage path · diagnostics isolate the layer'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'TN prep failure'),
        bMid(B2_L, B2_R, 'nsxcli get routes'),
        bMid(B3_L, B3_R, 'get-tech-support'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'BGP peer down'),
        bMid(B2_L, B2_R, 'Connectivity chkr'),
        bMid(B3_L, B3_R, 'GSS P1/P2 case'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'DFW asymm drop'),
        bMid(B2_L, B2_R, 'Flow analysis API'),
        bMid(B3_L, B3_R, 'TAM escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Manager unreachable'),
        bMid(B2_L, B2_R, 'Packet capture edge'),
        bMid(B3_L, B3_R, 'Version compat chk'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'MTU mismatch drop'),
        bMid(B2_L, B2_R, '/var/log/syslog'),
        bMid(B3_L, B3_R, 'Core dump collect'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics use nsxcli and flow analysis'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['TN prep fail', 'nsxcli routes', '/var/log/syslog', 'get-tech-supp', 'Re-prep TN'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['BGP peer down', 'Conn. checker', '/image/logs/', 'GSS P1 case', 'BGP re-peer'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['DFW drop asym', 'Flow analysis', 'Manager syslog', 'TAM escalate', 'Rule reorder'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['MTU black hole', 'Pkt capture', 'Edge var/log', 'Compat matrix', 'MTU fix ToR'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 ESXi hosts · Edge VM nodes · ToR switches (BGP) · Physical NICs (TEP uplinks) · OOB mgmt'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('TN prep failure = Transport node preparation failed; check ESXi version compat and network config'))
    lines.append(txt_row('BGP peer down  = T0 BGP session to ToR dropped; check BFD timers, interface IP, and AS numbers'))
    lines.append(txt_row('DFW asymmetric = Stateful DFW receives return traffic on different host with no state; causes drops'))
    lines.append(txt_row('MTU mismatch   = GENEVE requires MTU ≥1600; lower ToR MTU causes silent packet drops in overlay'))
    lines.append(txt_row('Connectivity checker = NSX built-in tool; tests L2/L3 connectivity between two endpoints in overlay'))
    lines.append(txt_row('Flow analysis  = NSX API that queries per-VM traffic flows; identifies which DFW rule applied'))
    lines.append(txt_row('get-tech-support = NSX CLI command on Manager/Edge; collects full support bundle for GSS'))
    lines.append(txt_row('nsxcli         = NSX Edge CLI; namespaces: get (read), set (write), debug (packet capture)'))
    lines.append(txt_row('TEP            = Tunnel End Point; VMkernel port on ESXi/Edge; source/dest of GENEVE packets'))
    lines.append(txt_row('MPA            = Management Plane Agent on transport nodes; if offline, node appears disconnected'))
    lines.append(txt_row('Core dump      = NSX Manager/Edge crash dump; required for P1 escalation analysis by support'))
    lines.append(txt_row('Version compat = NSX to vSphere version compatibility; mismatch can cause TN prep or upgrade failures'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-architecture',
    'docs/virtualization/vmware/vsan/architecture/index.md',
    'vSAN Architecture — disk groups, SPBM, FTT, ESA, stretched cluster',
)
def vsan_architecture():
    """vSAN Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSAN — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware vSAN — HCI storage pooling local NVMe/SSD/HDD from ESXi hosts into a shared datastore')))
    lines.append(R(bMid(IV_L, IV_R, 'FTT policies (RAID-1 mirroring, RAID-5/6 erasure coding) protect objects across hosts/domains')))
    lines.append(R(bMid(IV_L, IV_R, 'Dedup and compression available in all-flash OSA; OSA (original) vs ESA (express) architecture')))
    lines.append(R(bMid(IV_L, IV_R, 'vSAN ESA uses single-tier NVMe with compression-first; no separate cache/capacity disk groups')))
    lines.append(R(bMid(IV_L, IV_R, 'Stretched cluster spans two sites with a witness host; SPBM storage policies enforce per-VM')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines HCI storage pooling · integrations connect vSphere and management'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Disk groups (OSA)'),
        bMid(B2_L, B2_R, 'vCenter: native UI'),
        bMid(B3_L, B3_R, 'Min 3 nodes OSA'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'FTT/RAID policies'),
        bMid(B2_L, B2_R, 'vSphere HA/DRS'),
        bMid(B3_L, B3_R, 'Min 4 nodes ESA'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Witness: stretch HA'),
        bMid(B2_L, B2_R, 'NSX: microseg'),
        bMid(B3_L, B3_R, 'FTT=1 default'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Dedup+compress'),
        bMid(B2_L, B2_R, 'File services: NFS'),
        bMid(B3_L, B3_R, 'Cache ≥10% OSA'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSAN ESA: NVMe'),
        bMid(B2_L, B2_R, 'HCL: hw compat'),
        bMid(B3_L, B3_R, 'Witness: tiny VM'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SPBM per-VM policy'),
        bMid(B2_L, B2_R, 'Aria Ops adapter'),
        bMid(B3_L, B3_R, '25% headroom'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers pooling and policies · integrations connect vCenter and NSX'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Disk groups', 'vCenter native', 'Min 3 nodes', 'All-flash', 'FTT policy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['FTT/RAID tiers', 'HA/DRS intg', 'Min 4 (ESA)', 'Hybrid OSA', 'Cache 10%'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Dedup/compress', 'NSX microseg', 'Witness host', 'Stretched', 'HCL required'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SPBM policies', 'Aria Ops intg', '25% headroom', 'HCI design', 'SPBM std'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 servers with NVMe/SSD/HDD · RAM DIMMs · 25GbE NICs · Witness host VM · ToR switches'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('OSA           = Original Storage Architecture; vSAN disk groups with separate cache and capacity'))
    lines.append(txt_row('ESA           = Express Storage Architecture; single-tier NVMe; compression-first; vSAN 8.0+'))
    lines.append(txt_row('FTT           = Failures To Tolerate; number of host/disk failures a vSAN object can survive'))
    lines.append(txt_row('RAID-5/6      = Erasure coding in vSAN; RAID-5 requires 4 hosts (1 FTT); RAID-6 needs 6 hosts (2 FTT)'))
    lines.append(txt_row('Disk group    = OSA unit of storage; one cache disk + 1-7 capacity disks per ESXi host'))
    lines.append(txt_row('SPBM          = Storage Policy-Based Management; per-VM policy defines FTT, RAID, IOPs limits'))
    lines.append(txt_row('Witness       = Lightweight VM in stretched cluster; holds metadata tie-breaker; no VM data stored'))
    lines.append(txt_row('Dedup+compress = All-flash OSA feature reducing capacity footprint; applied per disk group'))
    lines.append(txt_row('vSAN health   = Built-in health service in vCenter; checks HCL, network, disk, and capacity'))
    lines.append(txt_row('HCL           = Hardware Compatibility List; vSAN requires HCL-certified disks, NICs, and servers'))
    lines.append(txt_row('Stretched cluster = vSAN spanning two fault domains with a witness; tolerates full site failure'))
    lines.append(txt_row('PFTT          = Primary Failures To Tolerate; site-level FTT setting in stretched cluster policy'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-operations',
    'docs/virtualization/vmware/vsan/operations/index.md',
    'vSAN Operations — health service, resyncing, capacity, upgrade sequencing',
)
def vsan_operations():
    """vSAN Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSAN — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'vSAN health service provides proactive monitoring of disk, network, HCL, and capacity status')))
    lines.append(R(bMid(IV_L, IV_R, 'Daily: review disk group state, resync operations (target zero), capacity headroom (<70% used)')))
    lines.append(R(bMid(IV_L, IV_R, 'Lifecycle: LCM upgrades ESXi and vSAN together; pre-check health before node-by-node upgrade')))
    lines.append(R(bMid(IV_L, IV_R, 'Post-expansion: rebalance cluster after adding nodes; validate HCL compliance for new hardware')))
    lines.append(R(bMid(IV_L, IV_R, 'Automation: vSAN REST API, RVC commands, PowerCLI vSAN module, esxcli vsan namespace')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch drift · lifecycle keeps vSAN current · automation scales vSAN management tasks'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSAN health svc'),
        bMid(B2_L, B2_R, 'LCM + ESXi together'),
        bMid(B3_L, B3_R, 'vSAN REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Disk group: state'),
        bMid(B2_L, B2_R, 'Pre-check health'),
        bMid(B3_L, B3_R, 'RVC commands'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Resync: 0 ideal'),
        bMid(B2_L, B2_R, 'Node-by-node upg'),
        bMid(B3_L, B3_R, 'PowerCLI vSAN'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Capacity: <70%'),
        bMid(B2_L, B2_R, 'Rebalance post-add'),
        bMid(B3_L, B3_R, 'esxcli vsan'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Policy compliance'),
        bMid(B2_L, B2_R, 'HCL validate'),
        bMid(B3_L, B3_R, 'Capacity report'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alarms review'),
        bMid(B2_L, B2_R, 'Post-check'),
        bMid(B3_L, B3_R, 'SPBM API'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch resync and capacity issues · lifecycle upgrades node-by-node'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['esxcli vsan', 'Health UI green', 'Maint mode', 'LCM bundle', 'vSAN no native'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['RVC vsan.*', 'Resync = 0', 'Add disk grp', 'Pre-check run', 'VM backup VADP'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vSAN API', 'Capacity <70%', 'Expand cluster', 'Node upg order', 'Rep policy chk'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['PowerCLI vSAN', 'HCL compliant', 'Rebalance run', 'Post-upg chk', 'Witness backup'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 servers with NVMe/SSD/HDD · RAM DIMMs · 25GbE NICs (vSAN network) · Witness host · ToR switches'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vSAN health   = Built-in vCenter health service; checks HCL, network, disk, and capacity proactively'))
    lines.append(txt_row('Disk group    = OSA unit: one cache disk + up to 7 capacity disks; state must be healthy'))
    lines.append(txt_row('FTT           = Failures To Tolerate; objects rebuild when a host enters maintenance mode'))
    lines.append(txt_row('Resync        = Rebuild or rebalance of vSAN objects; high resync indicates degraded protection'))
    lines.append(txt_row('Rebalance     = vSAN redistributes data across nodes after adding capacity to equalize usage'))
    lines.append(txt_row('RVC           = Ruby vSphere Console; CLI tool with vSAN-specific commands for diagnostics'))
    lines.append(txt_row('SPBM          = Storage Policy-Based Management; policy compliance check ensures FTT is satisfied'))
    lines.append(txt_row('LCM           = Lifecycle Manager; image-based ESXi + vSAN upgrade integrated in vCenter 7+'))
    lines.append(txt_row('HCL           = Hardware Compatibility List; vSAN requires certified disks and NICs at all times'))
    lines.append(txt_row('Witness       = Tie-breaker node in stretched cluster; must be reachable from both data sites'))
    lines.append(txt_row('OSA           = Original Storage Architecture; disk-group-based; cache+capacity tier design'))
    lines.append(txt_row('ESA           = Express Storage Architecture; NVMe-only single-tier; vSAN 8.0+ required'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-security',
    'docs/virtualization/vmware/vsan/security/index.md',
    'vSAN Security — D@RE, RBAC, data-in-transit encryption, KMS, vSphere Trust',
)
def vsan_security():
    """vSAN Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSAN — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'vSAN data-at-rest encryption via external KMS (KMIP); key rotation without data re-encryption')))
    lines.append(R(bMid(IV_L, IV_R, 'Host Trust Authority provides TPM-based attestation; ensures only trusted hosts join the')))
    lines.append(R(bMid(IV_L, IV_R, 'vSAN stretched cluster requires authentication between sites; network isolation per segment')))
    lines.append(R(bMid(IV_L, IV_R, 'SPBM security policies enforce encryption and FTT compliance; audit via vCenter events')))
    lines.append(R(bMid(IV_L, IV_R, 'RBAC inherited from vCenter SSO; AD groups map to roles; in-transit encryption on vSAN ESA')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication controls cluster access · access control enforces RBAC'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vCenter SSO auth'),
        bMid(B2_L, B2_R, 'vCenter RBAC'),
        bMid(B3_L, B3_R, 'Data-at-rest enc'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'KMS/KMIP intg'),
        bMid(B2_L, B2_R, 'Datastore perms'),
        bMid(B3_L, B3_R, 'KMS provider cfg'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Host trust auth'),
        bMid(B2_L, B2_R, 'Cluster-level acc'),
        bMid(B3_L, B3_R, 'Key rotation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AD group RBAC'),
        bMid(B2_L, B2_R, 'Admin role: vCenter'),
        bMid(B3_L, B3_R, 'In-transit encr'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert management'),
        bMid(B2_L, B2_R, 'Policy RBAC'),
        bMid(B3_L, B3_R, 'vSAN ESA native'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSAN stretch auth'),
        bMid(B2_L, B2_R, 'Audit events'),
        bMid(B3_L, B3_R, 'TPM attestation'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth gates cluster membership · RBAC scopes access'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vCenter SSO', 'RBAC inherit', 'Data-at-rest', 'KMIP KMS', 'vCenter events'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['KMS/KMIP', 'Datastore perm', 'KMS key rotate', 'TLS vSAN net', 'Policy audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Host trust auth', 'Admin role', 'In-transit enc', 'TPM attest', 'HCL audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AD group RBAC', 'Least privilege', 'ESA native enc', 'Cert rotation', 'SIEM forward'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 servers with NVMe/SSD/HDD · TPM 2.0 chip · RAM DIMMs · 25GbE NICs · Key Management Server'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('KMS           = Key Management Server; external KMIP-compatible server holding vSAN encryption keys'))
    lines.append(txt_row('KMIP          = Key Management Interoperability Protocol; standard API for integrating external KMS'))
    lines.append(txt_row('Data-at-rest  = vSAN encryption of disk data; enabled cluster-wide; keys held by external KMS'))
    lines.append(txt_row('Host Trust Authority = vSphere service using TPM attestation to verify host integrity before joining'))
    lines.append(txt_row('TPM           = Trusted Platform Module; chip providing hardware root of trust for host attestation'))
    lines.append(txt_row('vSAN stretched = Two-site cluster; auth and network isolation between sites required for security'))
    lines.append(txt_row('SPBM          = Storage Policy-Based Management; policies can enforce encryption compliance per VM'))
    lines.append(txt_row('FTT           = Failures To Tolerate; security-relevant as it controls data redundancy level'))
    lines.append(txt_row('Erasure coding = RAID-5/6 in vSAN; distributes parity across hosts; efficient redundancy method'))
    lines.append(txt_row('Key rotation  = Replacing encryption keys without re-encrypting data; shallow vs deep rekey options'))
    lines.append(txt_row('In-transit    = vSAN ESA encrypts data in flight between hosts on the vSAN network layer'))
    lines.append(txt_row('vCenter RBAC  = Role-based access control inherited by vSAN; all datastore access managed via vCenter'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-troubleshooting',
    'docs/virtualization/vmware/vsan/troubleshooting/index.md',
    'vSAN Troubleshooting — disk faults, resync stalls, network partition, proactive tests',
)
def vsan_troubleshooting():
    """vSAN Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSAN — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'vSAN object health issues: degraded, absent, or non-compliant components cause VM risk')))
    lines.append(R(bMid(IV_L, IV_R, 'Resync stalls indicate disk group failures, network issues, or hosts in maintenance mode')))
    lines.append(R(bMid(IV_L, IV_R, 'Disk group failures remove capacity; witness connectivity loss affects stretched cluster HA')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity alarms at 70%/80% thresholds; address before hitting the 100% hard limit')))
    lines.append(R(bMid(IV_L, IV_R, 'RVC and esxcli vsan provide CLI diagnostics; vm-support bundle for GSS escalation')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues define the triage path · diagnostics isolate root cause'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Object degraded'),
        bMid(B2_L, B2_R, 'RVC vsan.check'),
        bMid(B3_L, B3_R, 'vSAN Skyline'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Resync stuck'),
        bMid(B2_L, B2_R, 'vSAN health UI'),
        bMid(B3_L, B3_R, 'GSS log bundle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Disk group fail'),
        bMid(B2_L, B2_R, 'esxcli vsan list'),
        bMid(B3_L, B3_R, 'HCL validate'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Witness offline'),
        bMid(B2_L, B2_R, 'vsantop perf'),
        bMid(B3_L, B3_R, 'Stretched log'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Capacity alarm'),
        bMid(B2_L, B2_R, 'Support bundle'),
        bMid(B3_L, B3_R, 'ESXi host log'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Component absent'),
        bMid(B2_L, B2_R, 'Policy violations'),
        bMid(B3_L, B3_R, 'Core analysis'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics pinpoint root cause'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Object degraded', 'RVC vsan.chk', '/var/log/vmk', 'vm-support.tgz', 'Re-add disk'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Resync stuck', 'esxcli vsan', 'vCenter tasks', 'GSS P1 case', 'Maint + remove'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Disk group fail', 'vSAN health UI', '/var/log/hostd', 'HCL validate', 'Disk replace'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Witness offline', 'vsantop cmd', 'Witness /logs', 'TAM escalate', 'Re-sync wait'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 servers with NVMe/SSD/HDD · RAM DIMMs · 25GbE NICs · Witness host · ToR switches'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Object health = vSAN object state: healthy, degraded, absent, or non-compliant per SPBM policy'))
    lines.append(txt_row('Resync        = Rebuild or sync of vSAN object components; stalls indicate disk or network issues'))
    lines.append(txt_row('Disk group    = OSA storage unit; single disk group failure removes all its capacity from the pool'))
    lines.append(txt_row('Witness       = Stretched cluster tie-breaker; if offline, vSAN cannot vote on site partition'))
    lines.append(txt_row('Component     = Individual piece of a vSAN object; absent components reduce FTT protection'))
    lines.append(txt_row('APD           = All Paths Down; storage network path loss; triggers vSAN network partition'))
    lines.append(txt_row('PDL           = Permanent Device Loss; disk reports fatal error; data on that disk is inaccessible'))
    lines.append(txt_row('RVC           = Ruby vSphere Console; vsan.check_state and vsan.vm_object_info are key commands'))
    lines.append(txt_row('esxcli vsan   = vSAN CLI namespace; storage list, cluster info, and network diagnostics'))
    lines.append(txt_row('Proactive rebalance = Manual or automatic redistribution of data to equalize disk usage'))
    lines.append(txt_row('Capacity alarm = vSAN threshold alert at 70% (warning) and 80% (critical) utilization'))
    lines.append(txt_row('vSAN Skyline  = Proactive health analytics service; identifies issues before they cause outages'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-architecture',
    'docs/virtualization/vmware/vcenter/architecture/index.md',
    'vCenter Architecture — VCSA, PSC, SSO, ELM topology, HA, LCM',
)
def vcenter_architecture():
    """vCenter Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vCenter — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VCSA — virtual appliance (Linux-based); PSC embedded since vCenter 7.0; no external PSC needed')))
    lines.append(R(bMid(IV_L, IV_R, 'SSO domain provides identity federation; AD/LDAP identity sources for enterprise authentication')))
    lines.append(R(bMid(IV_L, IV_R, 'Inventory hierarchy: Datacenter > Cluster > Host > VM; permissions inherited down the tree')))
    lines.append(R(bMid(IV_L, IV_R, 'vCenter HA: 3-node active/passive/witness; protects VCSA from host failure; same-site only')))
    lines.append(R(bMid(IV_L, IV_R, 'VAMI (port 5480) manages appliance: network, time, backup, update, and service control')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines VCSA internals · integrations connect identity and tools'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VCSA appliance VM'),
        bMid(B2_L, B2_R, 'AD/LDAP identity'),
        bMid(B3_L, B3_R, 'VCSA sizing L/XL'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SSO domain: IdP'),
        bMid(B2_L, B2_R, 'NSX-T: plugin'),
        bMid(B3_L, B3_R, 'HA 3-node prod'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Inventory: DC>Clst'),
        bMid(B2_L, B2_R, 'Aria Ops: adapter'),
        bMid(B3_L, B3_R, 'Backup: daily'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vCenter HA: 3-node'),
        bMid(B2_L, B2_R, 'LCM: built-in'),
        bMid(B3_L, B3_R, 'NTP: 2 sources'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'PSC embedded'),
        bMid(B2_L, B2_R, 'Backup: SFTP/NFS'),
        bMid(B3_L, B3_R, 'Cert: VMCA/custom'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VAMI: web mgmt'),
        bMid(B2_L, B2_R, 'Aria Auto: cloud'),
        bMid(B3_L, B3_R, 'SSO single domain'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines VCSA and SSO · integrations connect identity and tools'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VCSA appliance', 'AD/LDAP IdP', 'VCSA L sizing', 'Single vCenter', 'NTP 2 sources'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SSO domain', 'NSX-T plugin', 'HA 3-node', 'Linked mode', 'Cert policy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Inventory hier', 'Aria Ops adapter', 'Daily backup', 'Multi-site', 'RBAC std'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vCenter HA', 'Backup SFTP', 'VMCA/custom', 'Multi-vCenter', 'SSO domain std'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 server (VCSA VM target) · RAM DIMMs · Network NICs · Shared datastore · OOB management'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VCSA          = vCenter Server Appliance; Linux-based OVA deployed as a VM; single management plane'))
    lines.append(txt_row('SSO domain    = Single Sign-On domain (vsphere.local by default); identity hub for vSphere auth'))
    lines.append(txt_row('PSC           = Platform Services Controller; embedded in VCSA 7.0+; manages SSO, certs, licensing'))
    lines.append(txt_row('VMCA          = VMware Certificate Authority; built-in CA signing VCSA and host certificates'))
    lines.append(txt_row('vCenter HA    = 3-node VCSA cluster: active, passive, witness; automatic failover on host failure'))
    lines.append(txt_row('VAMI          = vCenter Appliance Management Interface; web UI on port 5480 for appliance operations'))
    lines.append(txt_row('Linked Mode   = Multiple vCenters sharing SSO domain; unified inventory view across instances'))
    lines.append(txt_row('RBAC          = Role-Based Access Control; permissions set at inventory objects and inherited down'))
    lines.append(txt_row('Inventory hierarchy = DC > Cluster > Host > VM; permissions and policies propagate downward'))
    lines.append(txt_row('AD/LDAP       = Active Directory or LDAP identity source added to SSO for enterprise user auth'))
    lines.append(txt_row('File-based backup = VCSA periodic backup to SFTP or NFS; restores full appliance configuration'))
    lines.append(txt_row('Update Planner = vCenter tool that checks interoperability and schedules upgrade order'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-operations',
    'docs/virtualization/vmware/vcenter/operations/index.md',
    'vCenter Operations — VAMI, backup, upgrade, certificate management',
)
def vcenter_operations():
    """vCenter Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vCenter — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VCSA service health monitoring via VAMI; check all services green on start of each day')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate lifecycle management: monitor expiry in VAMI; renew via VMCA or custom CA')))
    lines.append(R(bMid(IV_L, IV_R, 'File-based backup to SFTP or NFS: schedule daily; retention of 3-7 restore points minimum')))
    lines.append(R(bMid(IV_L, IV_R, 'Update Planner checks compatibility and schedules upgrade; snapshot VCSA before upgrade')))
    lines.append(R(bMid(IV_L, IV_R, 'Automation: PowerCLI for vCenter management, REST API explorer, tag and attribute API')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops monitor VCSA health · lifecycle keeps vCenter current'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VCSA services ok'),
        bMid(B2_L, B2_R, 'Update appliance'),
        bMid(B3_L, B3_R, 'REST API explorer'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert expiry chk'),
        bMid(B2_L, B2_R, 'Pre-check health'),
        bMid(B3_L, B3_R, 'PowerCLI vCenter'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alarm review'),
        bMid(B2_L, B2_R, 'Snapshot pre-upg'),
        bMid(B3_L, B3_R, 'Tag/attr API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Storage tasks'),
        bMid(B2_L, B2_R, 'Cert renewal'),
        bMid(B3_L, B3_R, 'Automation scripts'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'HA cluster state'),
        bMid(B2_L, B2_R, 'LCM integration'),
        bMid(B3_L, B3_R, 'vCenter CLI'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'DB size check'),
        bMid(B2_L, B2_R, 'PSC sync chk'),
        bMid(B3_L, B3_R, 'API token auth'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch service drift · lifecycle upgrades vCenter safely'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['REST API', 'Services green', 'Cert renewal', 'Update Planner', 'File-based bkp'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['PowerCLI conn', 'HA state ok', 'RBAC review', 'Pre-check run', 'SFTP/NFS target'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Tag API calls', 'Backup: success', 'Add host', 'Snapshot pre', 'Restore: VCSA'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Event API', 'Cert: 60d+', 'Add cluster', 'Post-upg chk', 'Config backup'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 server (VCSA VM) · RAM DIMMs · Network NICs · Shared datastore (vSAN or SAN) · OOB management'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VCSA          = vCenter Server Appliance; Linux-based VM; all vSphere management runs here'))
    lines.append(txt_row('VAMI          = vCenter Appliance Management Interface; port 5480; monitors services and backup'))
    lines.append(txt_row('File-based backup = Scheduled VCSA backup to SFTP or NFS; restores full appliance config and'))
    lines.append(txt_row('Update Planner = vCenter tool checking compatibility matrix before scheduling an upgrade'))
    lines.append(txt_row('PowerCLI      = VMware PowerShell module; connects to vCenter REST API for at-scale automation'))
    lines.append(txt_row('REST API      = vCenter REST API (api/); supports hosts, VMs, tags, policies, and content library'))
    lines.append(txt_row('Certificate lifecycle = VCSA certificate expiry monitored in VAMI; renew via VMCA or custom CA'))
    lines.append(txt_row('VMCA          = VMware Certificate Authority; built-in CA for VCSA and ESXi host certificates'))
    lines.append(txt_row('LCM           = Lifecycle Manager; integrated in vCenter for ESXi image-based upgrade management'))
    lines.append(txt_row('vCenter HA    = Active/passive/witness VCSA cluster; failover automatic on host or network failure'))
    lines.append(txt_row('SSO           = Single Sign-On; vSphere identity service; local and AD/LDAP sources'))
    lines.append(txt_row('PSC           = Platform Services Controller; embedded 7.0+; handles SSO tokens and certificates'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-security',
    'docs/virtualization/vmware/vcenter/security/index.md',
    'vCenter Security — SSO hardening, RBAC, TLS, audit, Workspace ONE',
)
def vcenter_security():
    """vCenter Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vCenter — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'SSO domain with AD/LDAP identity provider; enterprise users map to vCenter RBAC roles')))
    lines.append(R(bMid(IV_L, IV_R, 'RBAC: built-in roles (Admin, Read-only, No-access) and custom roles with granular privileges')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate management: VMCA issues machine certs; custom CA for enterprise PKI integration')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit event export to SIEM via syslog; vCenter events capture all inventory and auth actions')))
    lines.append(R(bMid(IV_L, IV_R, '2FA via SSO plugin (RSA SecurID or RADIUS); API over TLS; VCSA disk encryption optional')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication gates vCenter access · RBAC scopes permissions'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SSO domain config'),
        bMid(B2_L, B2_R, 'RBAC: built-in'),
        bMid(B3_L, B3_R, 'API over TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AD/LDAP provider'),
        bMid(B2_L, B2_R, 'Custom roles'),
        bMid(B3_L, B3_R, 'VMCA cert mgmt'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '2FA via SSO'),
        bMid(B2_L, B2_R, 'Object-level perm'),
        bMid(B3_L, B3_R, 'Custom CA intg'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Admin acct policy'),
        bMid(B2_L, B2_R, 'Tag-based access'),
        bMid(B3_L, B3_R, 'Cert lifecycle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Service accounts'),
        bMid(B2_L, B2_R, 'Least privilege'),
        bMid(B3_L, B3_R, 'Audit syslog TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'IdP federation'),
        bMid(B2_L, B2_R, 'Audit export'),
        bMid(B3_L, B3_R, 'VCSA disk encr'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth gates vCenter login · RBAC scopes object access · TLS and certs protect management traffic'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SSO domain', 'RBAC roles', 'TLS API', 'Cert rotation', 'vCenter events'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AD/LDAP IdP', 'Custom roles', 'VMCA/custom', '2FA enforce', 'Syslog export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['2FA via SSO', 'Object perms', 'TLS syslog', 'Min password', 'Audit log review'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Service accts', 'Least privilege', 'Cert auto-renew', 'STIG align', 'Role review'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 server (VCSA VM) · RAM DIMMs · Network NICs · Shared datastore · Trusted CA infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SSO domain    = vSphere identity hub; authenticates all UI and API logins to vCenter'))
    lines.append(txt_row('VMCA          = VMware Certificate Authority; built-in CA; issues certs to VCSA and ESXi hosts'))
    lines.append(txt_row('Custom CA     = Enterprise PKI CA replacing VMCA; certs signed by corporate root for compliance'))
    lines.append(txt_row('RBAC          = Role-Based Access Control; grants privileges on inventory objects; inherited down'))
    lines.append(txt_row('Object-level permission = Permission set at specific VM, cluster, or folder; overrides parent'))
    lines.append(txt_row('2FA           = Two-Factor Authentication via SSO plugin: RSA SecurID or RADIUS integration'))
    lines.append(txt_row('vCenter audit = All inventory and auth events logged in vCenter; export via syslog to SIEM'))
    lines.append(txt_row('Service account = Non-interactive account for automation; scope to minimum required privileges'))
    lines.append(txt_row('Identity source = AD, LDAP, or OpenLDAP added to SSO; maps enterprise users to vCenter roles'))
    lines.append(txt_row('Certificate lifecycle = Monitor cert expiry in VAMI; renew before 60-day warning threshold'))
    lines.append(txt_row('Least privilege = RBAC principle: grant only the permissions needed for a specific role or task'))
    lines.append(txt_row('Tag-based access = vCenter tags used to scope RBAC; assign roles on tag categories for flexibility'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-troubleshooting',
    'docs/virtualization/vmware/vcenter/troubleshooting/index.md',
    'vCenter Troubleshooting — SSO issues, DB connection, service restarts, VAMI',
)
def vcenter_troubleshooting():
    """vCenter Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vCenter — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'SSO login failures: expired certs, clock skew, or identity source misconfiguration most common')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate expiry cascade: expired VMCA root causes all host and service cert failures at once')))
    lines.append(R(bMid(IV_L, IV_R, 'VCSA service failures: vpxd process restart for vCenter main service; check VAMI health tab')))
    lines.append(R(bMid(IV_L, IV_R, 'vCenter HA split-brain: both active and passive claim active role; check witness connectivity')))
    lines.append(R(bMid(IV_L, IV_R, 'VCSA shell and vcsa-check script for diagnostics; PSC sync issues resolved by SSO repair tool')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics isolate the service layer'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SSO login fail'),
        bMid(B2_L, B2_R, 'VCSA shell cmds'),
        bMid(B3_L, B3_R, 'VCSA support bndl'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert expired'),
        bMid(B2_L, B2_R, '/var/log/vmware'),
        bMid(B3_L, B3_R, 'GSS P1/P2 case'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VCSA svc down'),
        bMid(B2_L, B2_R, 'VAMI health'),
        bMid(B3_L, B3_R, 'Cert reset steps'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'HA split-brain'),
        bMid(B2_L, B2_R, 'API debug mode'),
        bMid(B3_L, B3_R, 'RCA template'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LCM task stuck'),
        bMid(B2_L, B2_R, 'SSO health chk'),
        bMid(B3_L, B3_R, 'TAM escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NSX plugin error'),
        bMid(B2_L, B2_R, 'vcsa-check script'),
        bMid(B3_L, B3_R, 'Log archive'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics use VCSA shell and logs · escalation bundles logs for GSS'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SSO login fail', 'VCSA shell', '/var/log/sso', 'VCSA bndl.tgz', 'Restart SSO'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cert expired', 'VAMI health', '/var/log/vmware', 'GSS P1 case', 'Cert re-issue'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VCSA svc down', 'API debug', '/var/log/vpxd', 'TAM escalate', 'Restart service'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['HA split-brain', 'vcsa-check', '/var/log/vmsvc', 'RCA template', 'HA re-init'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 server (VCSA VM) · RAM DIMMs · Network NICs · Shared datastore · OOB management'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SSO           = Single Sign-On; vSphere identity service; login failures from cert or clock issues'))
    lines.append(txt_row('VCSA shell    = Bash shell on VCSA; enabled via VAMI or SSH; run service-control and log review'))
    lines.append(txt_row('VAMI          = vCenter Appliance Management Interface; port 5480; shows service and health status'))
    lines.append(txt_row('vpxd          = Main vCenter process (VMware vCenter Server daemon); restart to recover vCenter UI'))
    lines.append(txt_row('/var/log/vmware = VCSA log directory; vpxd.log, sso/vmware-sts*.log, vapi-endpoint.log'))
    lines.append(txt_row('vcsa-check    = VMware script validating VCSA service and configuration health pre/post upgrade'))
    lines.append(txt_row('vCenter HA split-brain = Both active and passive nodes active; isolate passive and re-init HA'))
    lines.append(txt_row('VCSA support bundle = Full log archive generated via VAMI or CLI; attach to GSS support case'))
    lines.append(txt_row('PSC           = Platform Services Controller; embedded 7.0+; SSO token and certificate management'))
    lines.append(txt_row('LCM task      = Lifecycle Manager upgrade task; if stuck, check vpxd.log and LCM log for errors'))
    lines.append(txt_row('Certificate cascade = Expired VMCA root invalidates all child certs simultaneously across cluster'))
    lines.append(txt_row('RCA           = Root Cause Analysis; post-incident document capturing timeline, cause, and fix'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-architecture',
    'docs/virtualization/vmware/vmware-cloud-foundation/architecture/index.md',
    'VCF Architecture — SDDC Manager, management/workload domains, CloudBuilder',
)
def vcf_architecture():
    """VCF Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VCF — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Cloud Foundation = SDDC Manager + Cloud Builder + vSphere + vSAN + NSX bundled together')))
    lines.append(R(bMid(IV_L, IV_R, 'Workload domains isolate workloads; BOM ensures component compatibility across the full stack')))
    lines.append(R(bMid(IV_L, IV_R, 'Automated bring-up via Cloud Builder; Management domain deployed first, VI domains added after')))
    lines.append(R(bMid(IV_L, IV_R, 'SDDC Manager orchestrates lifecycle: patching, password rotation, certificate management')))
    lines.append(R(bMid(IV_L, IV_R, 'NSX per domain provides overlay networking; vCenter per domain for workload management')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines domain architecture · integrations connect stack components'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SDDC Manager UI'),
        bMid(B2_L, B2_R, 'vSphere+vSAN+NSX'),
        bMid(B3_L, B3_R, 'Mgmt domain first'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cloud Builder: deploy'),
        bMid(B2_L, B2_R, 'Aria Suite intg'),
        bMid(B3_L, B3_R, 'VI domains: isolated'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Workload domains'),
        bMid(B2_L, B2_R, 'vCenter per domain'),
        bMid(B3_L, B3_R, 'NSX per domain'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'BOM: version set'),
        bMid(B2_L, B2_R, 'NSX per domain'),
        bMid(B3_L, B3_R, 'SDDC user roles'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VI domain: workload'),
        bMid(B2_L, B2_R, 'Identity Manager'),
        bMid(B3_L, B3_R, 'BOM compat matrix'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Mgmt domain: core'),
        bMid(B2_L, B2_R, 'SIEM syslog'),
        bMid(B3_L, B3_R, 'Subscription model'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers domain model · integrations connect stack and identity'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SDDC Manager', 'vSphere+vSAN', 'Mgmt domain 1st', 'Cloud Builder', 'BOM matrix'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Workload domains', 'NSX per domain', 'VI domains', 'Automated deploy', 'Domain naming'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['BOM lifecycle', 'Aria Suite intg', 'SDDC RBAC', 'Pre-check reqs', 'SDDC roles'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cloud Builder', 'Identity Mgr', 'NSX overlay', 'Post-deploy val', 'Password std'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 servers · PCIe NICs · ToR switches · SAN/vSAN storage · OOB management network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SDDC Manager  = VCF control plane; orchestrates domain lifecycle, LCM upgrades, password rotation'))
    lines.append(txt_row('Cloud Builder = Automated bring-up appliance; validates prerequisites and deploys Management domain'))
    lines.append(txt_row('Workload domain = Isolated vSphere+vSAN+NSX unit; separate vCenter, NSX Manager, and cluster'))
    lines.append(txt_row('Management domain = First VCF domain; hosts SDDC Manager, vCenter, and shared infrastructure'))
    lines.append(txt_row('VI domain     = Virtual Infrastructure workload domain; runs production VMs separate from management'))
    lines.append(txt_row('BOM (Bill of Materials) = Validated version matrix for all VCF components; ensures stack'))
    lines.append(txt_row('SDDC bring-up = Cloud Builder automated deployment of Management domain from JSON spec'))
    lines.append(txt_row('NSX per domain = Each VCF workload domain gets its own NSX Manager cluster for isolation'))
    lines.append(txt_row('vCenter per domain = Each VCF domain has a dedicated vCenter for workload management and HA/DRS'))
    lines.append(txt_row('LCM (Lifecycle Manager) = SDDC Manager component for orchestrating upgrades across VCF stack'))
    lines.append(txt_row('SoS tool      = Support and Serviceability tool; runs health checks across all VCF components'))
    lines.append(txt_row('VCF subscription = Licensing model for VCF; covers all included components under one SKU'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-operations',
    'docs/virtualization/vmware/vmware-cloud-foundation/operations/index.md',
    'VCF Operations — LCM bundle upgrades, domain lifecycle, SDDC Manager tasks',
)
def vcf_operations():
    """VCF Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VCF — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'SDDC Manager dashboard for domain health; LCM upgrade orchestration across all components')))
    lines.append(R(bMid(IV_L, IV_R, 'SoS health check tool validates VCF component state; reports failures per domain and service')))
    lines.append(R(bMid(IV_L, IV_R, 'Password rotation for all components via SDDC Manager; certificate status monitoring across')))
    lines.append(R(bMid(IV_L, IV_R, 'LCM upgrade sequence: Management domain first; VI domains staged after; pre-checks mandatory')))
    lines.append(R(bMid(IV_L, IV_R, 'Automation: SDDC REST API, LCM API, PowerCLI VCF, Terraform VCF provider')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch drift · lifecycle orchestrates upgrades safely · automation scales VCF management'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SDDC dashboard'),
        bMid(B2_L, B2_R, 'SDDC LCM upgrade'),
        bMid(B3_L, B3_R, 'SDDC REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Domain health chk'),
        bMid(B2_L, B2_R, 'Bundle download'),
        bMid(B3_L, B3_R, 'LCM API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LCM status'),
        bMid(B2_L, B2_R, 'Pre-check run'),
        bMid(B3_L, B3_R, 'PowerCLI VCF'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Password rotation'),
        bMid(B2_L, B2_R, 'Upg: mgmt first'),
        bMid(B3_L, B3_R, 'Terraform VCF'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert status'),
        bMid(B2_L, B2_R, 'Aria upgrades'),
        bMid(B3_L, B3_R, 'Cloud Builder API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SoS tool run'),
        bMid(B2_L, B2_R, 'BOM update'),
        bMid(B3_L, B3_R, 'Tag-based policy'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops keep domains healthy · lifecycle upgrades safely in sequence'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SDDC REST API', 'Domain: healthy', 'Add VI domain', 'LCM bundle dl', 'Config backup'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SoS tool cmds', 'LCM: current', 'Add host', 'Pre-check run', 'SFTP target'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['PowerCLI VCF', 'Certs: valid', 'Add cluster', 'Mgmt upg 1st', 'SDDC restore'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LCM API', 'Passwords: ok', 'Expand domain', 'Post-upg val', 'Domain backup'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 servers (mgmt + workload) · PCIe NICs · ToR switches · vSAN/SAN · OOB management'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SDDC Manager  = VCF control plane; dashboard shows domain health, alerts, and LCM upgrade status'))
    lines.append(txt_row('LCM           = Lifecycle Manager; orchestrates upgrades for vSphere, vSAN, NSX, and SDDC Manager'))
    lines.append(txt_row('SoS (Support and Service Guidance tool) = Health check CLI; validates all VCF component states'))
    lines.append(txt_row('Workload domain = Isolated VCF unit; add hosts, clusters, or expand via SDDC Manager workflow'))
    lines.append(txt_row('BOM           = Bill of Materials; defines validated component versions for each VCF release'))
    lines.append(txt_row('Cloud Builder = Bring-up appliance used for initial Management domain deployment; retired post-deploy'))
    lines.append(txt_row('SDDC REST API = VCF programmatic interface; manage domains, hosts, clusters, and lifecycle tasks'))
    lines.append(txt_row('Password rotation = SDDC Manager rotates credentials for vCenter, NSX, ESXi, and SDDC components'))
    lines.append(txt_row('vCenter per domain = Dedicated vCenter in each domain; upgraded as part of LCM domain upgrade'))
    lines.append(txt_row('NSX per domain = NSX Manager cluster per VCF domain; upgraded after vCenter in LCM sequence'))
    lines.append(txt_row('Certificate rotation = SDDC Manager renews certificates for all VCF components on schedule'))
    lines.append(txt_row('VCF upgrade sequence = Mgmt domain first; VI domains after; never upgrade VI before Management'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-security',
    'docs/virtualization/vmware/vmware-cloud-foundation/security/index.md',
    'VCF Security — SDDC Manager RBAC, cert management, vIDM, STIG compliance',
)
def vcf_security():
    """VCF Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VCF — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'SDDC Manager RBAC with admin/viewer roles; Identity Manager SSO across all domains')))
    lines.append(R(bMid(IV_L, IV_R, 'Component password policy via SoS; audit events logged in SDDC Manager activity log')))
    lines.append(R(bMid(IV_L, IV_R, 'vSAN encryption per domain with KMS; NSX TLS fabric for all inter-component traffic')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate management: SDDC Manager rotates certs for vCenter, NSX, and SDDC components')))
    lines.append(R(bMid(IV_L, IV_R, 'Break-glass admin account for emergency access; credential vault for service account storage')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication gates VCF access · RBAC scopes management · encryption protects domain data at rest'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Identity Mgr SSO'),
        bMid(B2_L, B2_R, 'SDDC roles: admin'),
        bMid(B3_L, B3_R, 'vSAN encr/domain'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AD/LDAP intg'),
        bMid(B2_L, B2_R, 'SDDC roles: viewer'),
        bMid(B3_L, B3_R, 'NSX TLS fabric'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'API token auth'),
        bMid(B2_L, B2_R, 'NSX+vCtr RBAC'),
        bMid(B3_L, B3_R, 'vCtr cert mgmt'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Break-glass admin'),
        bMid(B2_L, B2_R, 'Domain-level acc'),
        bMid(B3_L, B3_R, 'SDDC cert rotate'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'User management'),
        bMid(B2_L, B2_R, 'Audit events'),
        bMid(B3_L, B3_R, 'Credential vault'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SDDC Manager auth'),
        bMid(B2_L, B2_R, 'Password policy'),
        bMid(B3_L, B3_R, 'KMS config'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth controls who accesses VCF · RBAC limits domain scope'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Identity Mgr', 'SDDC admin', 'vSAN encrypt', 'Cert rotation', 'SDDC events'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AD/LDAP', 'SDDC viewer', 'NSX TLS', 'Password policy', 'NSX audit log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['API tokens', 'Domain access', 'vCenter cert', 'KMS config', 'vCenter events'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Break-glass', 'Least privilege', 'SDDC cert', 'SoS scan', 'SIEM forward'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 servers · TPM 2.0 · NVMe/SSD (vSAN) · PCIe NICs · Key Management Server · OOB network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SDDC Manager RBAC = Admin and Viewer roles in SDDC Manager; controls domain and lifecycle access'))
    lines.append(txt_row('Identity Manager  = VMware vIDM provides SSO across VCF vCenter, NSX, and SDDC Manager UIs'))
    lines.append(txt_row('Workload domain isolation = Each domain has independent vCenter, NSX, and access control boundaries'))
    lines.append(txt_row('SoS password rotation = SDDC Manager rotates all component passwords via SoS on schedule'))
    lines.append(txt_row('vSAN encryption   = Per-domain data-at-rest encryption using KMS-managed keys; enabled per policy'))
    lines.append(txt_row('NSX TLS           = All NSX management plane traffic encrypted with TLS; cert managed by SDDC Mgr'))
    lines.append(txt_row('Certificate rotation = SDDC Manager renews certificates for all VCF components automatically'))
    lines.append(txt_row('API token         = SDDC Manager REST API bearer token; scoped to user role and domain'))
    lines.append(txt_row('Break-glass account = Emergency local admin in SDDC Manager; used when SSO is unavailable'))
    lines.append(txt_row('KMS/KMIP          = External Key Management Server; manages vSAN and VM encryption keys via KMIP'))
    lines.append(txt_row('Audit events      = SDDC Manager logs all user and system actions for compliance review'))
    lines.append(txt_row('Credential vault  = SDDC Manager stores all component service account passwords securely'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-troubleshooting',
    'docs/virtualization/vmware/vmware-cloud-foundation/troubleshooting/index.md',
    'VCF Troubleshooting — LCM failures, NSX prep, SDDC Manager, support bundles',
)
def vcf_troubleshooting():
    """VCF Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VCF — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'SoS health check failures; workload domain deployment errors; LCM upgrade stalls')))
    lines.append(R(bMid(IV_L, IV_R, 'NSX host prep failures in VCF; SDDC Manager service issues; password rotation errors')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnostics: SoS tool output, SDDC Manager logs, SDDC REST API debug, NSX prep log')))
    lines.append(R(bMid(IV_L, IV_R, 'Log collection: VCF support bundle via SDDC Manager; attach to GSS case for analysis')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: TAM/GSS for P1; BOM mismatch validation; Skyline proactive diagnostics')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues define the triage path · diagnostics isolate root cause'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SoS health fail'),
        bMid(B2_L, B2_R, 'SoS tool output'),
        bMid(B3_L, B3_R, 'VCF support bndl'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Workload dom err'),
        bMid(B2_L, B2_R, 'SDDC Mgr logs'),
        bMid(B3_L, B3_R, 'GSS/TAM escalate'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LCM stall'),
        bMid(B2_L, B2_R, 'API debug'),
        bMid(B3_L, B3_R, 'BOM mismatch'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NSX prep fail'),
        bMid(B2_L, B2_R, 'Domain health'),
        bMid(B3_L, B3_R, 'Core analysis'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SDDC svc down'),
        bMid(B2_L, B2_R, 'NSX prep log'),
        bMid(B3_L, B3_R, 'Skyline'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Password rot err'),
        bMid(B2_L, B2_R, 'vSAN health'),
        bMid(B3_L, B3_R, 'P1 process'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics pinpoint root cause'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SoS fail', 'SoS tool run', '/var/log/vmware', 'VCF bndl.tgz', 'Re-run SoS'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Domain err', 'SDDC API debug', 'SDDC Mgr logs', 'GSS P1 case', 'Redeploy dom'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LCM stall', 'NSX prep log', '/var/log/nsx', 'TAM escalate', 'LCM retry'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['NSX prep fail', 'vSAN health UI', '/var/log/vsan', 'BOM validate', 'Re-prep NSX'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 servers · PCIe NICs · ToR switches · vSAN/SAN · OOB management network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SoS tool      = Support and Serviceability; CLI tool that validates all VCF component health states'))
    lines.append(txt_row('LCM stall     = Lifecycle Manager upgrade task stuck; check SDDC Manager logs and retry via API'))
    lines.append(txt_row('NSX host prep = VCF NSX transport node preparation; fails if ESXi version or network config mismatch'))
    lines.append(txt_row('SDDC Manager service = Core VCF service; restart via systemctl if dashboard is unresponsive'))
    lines.append(txt_row('Workload domain error = Domain add/expand task failure; review SDDC Manager task log for detail'))
    lines.append(txt_row('BOM mismatch  = Component versions outside validated BOM; must resolve before LCM can proceed'))
    lines.append(txt_row('VCF support bundle = Downloaded from SDDC Manager; contains logs for all VCF components'))
    lines.append(txt_row('Password rotation failure = SoS rotation error; check component connectivity and account lockout'))
    lines.append(txt_row('Skyline Health = VMware proactive diagnostics; collects and analyzes VCF telemetry for known issues'))
    lines.append(txt_row('TAM escalation = Technical Account Manager engagement for critical VCF production incidents'))
    lines.append(txt_row('GSS P1/P2     = Global Support Services priority; P1=production down, P2=significant degradation'))
    lines.append(txt_row('Cloud Builder deployment = Initial bring-up failures; review JSON spec and network pre-check output'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-automation-architecture',
    'docs/virtualization/vmware/aria-automation/architecture/index.md',
    'Aria Automation Architecture — Prelude cluster, CAS, ABX, service broker, extensibility',
)
def aria_automation_architecture():
    """Aria Automation Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Automation — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Automation = Automation appliance + Service Broker + Assembler + Extensibility (ABX +')))
    lines.append(R(bMid(IV_L, IV_R, 'Service Broker provides self-service catalog with entitlements and approval policies')))
    lines.append(R(bMid(IV_L, IV_R, 'Assembler manages blueprints, cloud accounts, and cloud zones for multi-cloud provisioning')))
    lines.append(R(bMid(IV_L, IV_R, 'ABX actions and embedded Orchestrator extend automation with custom functions and workflows')))
    lines.append(R(bMid(IV_L, IV_R, 'Connects to cloud accounts: vCenter, AWS, Azure, GCP; cloud proxy for on-premises connectivity')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines platform components · integrations connect cloud accounts'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Automation appliance'),
        bMid(B2_L, B2_R, 'vCenter cloud acct'),
        bMid(B3_L, B3_R, 'Org/project RBAC'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Service Broker: catalog'),
        bMid(B2_L, B2_R, 'GitHub/GitLab: IaC'),
        bMid(B3_L, B3_R, 'Blueprint versioning'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Assembler: blueprints'),
        bMid(B2_L, B2_R, 'ServiceNow ITSM'),
        bMid(B3_L, B3_R, 'Naming standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ABX: extensibility'),
        bMid(B2_L, B2_R, 'AD/LDAP auth'),
        bMid(B3_L, B3_R, 'ABX action limits'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Orchestrator: embed'),
        bMid(B2_L, B2_R, 'Terraform plugin'),
        bMid(B3_L, B3_R, 'Approval policies'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cloud accounts'),
        bMid(B2_L, B2_R, 'Slack/Teams notify'),
        bMid(B3_L, B3_R, 'Cloud zones'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers platform components · integrations connect cloud and ITSM'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Service Broker', 'vCenter acct', 'Org/proj RBAC', 'Single-node', 'Blueprint std'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Assembler', 'GitHub IaC', 'Blueprint ver', 'HA cluster', 'Naming conv'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['ABX actions', 'ServiceNow', 'Approval policy', 'Cloud proxy', 'ABX limits'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Orchestrator', 'Terraform', 'Cloud zones', 'Multi-cloud', 'Secret policy'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VM (Automation appliance) · RAM DIMMs · Network NICs · vCenter/cloud provider targets'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Service Broker = Aria Automation self-service catalog; manages entitlements and approval workflows'))
    lines.append(txt_row('Assembler     = Aria Automation design surface; creates blueprints and manages cloud accounts/zones'))
    lines.append(txt_row('ABX (Action Based Extensibility) = FaaS runtime for Python/Node/PowerShell custom actions'))
    lines.append(txt_row('Orchestrator  = vRO embedded in Aria Automation; runs complex multi-step workflows'))
    lines.append(txt_row('Blueprint     = IaC template in Aria YAML; defines cloud-agnostic infrastructure topology'))
    lines.append(txt_row('Cloud account = Aria connection to a cloud endpoint: vCenter, AWS, Azure, or GCP'))
    lines.append(txt_row('Cloud zone    = Subset of a cloud account resources (clusters, regions) available for provisioning'))
    lines.append(txt_row('Catalog item  = Published blueprint or Orchestrator workflow available in Service Broker'))
    lines.append(txt_row('Entitlement   = Policy granting a project/user access to specific catalog items in Service Broker'))
    lines.append(txt_row('Approval policy = Workflow requiring approver sign-off before catalog item request is fulfilled'))
    lines.append(txt_row('Cloud proxy   = Lightweight VM deployed on-premises; routes Aria SaaS traffic to vCenter'))
    lines.append(txt_row('Organization/Project = Org is top-level tenant; Project scopes users, cloud zones, and policies'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-automation-operations',
    'docs/virtualization/vmware/aria-automation/operations/index.md',
    'Aria Automation Operations — blueprint publishing, upgrade, cert management, API',
)
def aria_automation_operations():
    """Aria Automation Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Automation — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Blueprint lifecycle management; request monitoring for failed deployments; catalog item health')))
    lines.append(R(bMid(IV_L, IV_R, 'Subscription and event broker management; pipeline status monitoring; ABX function execution')))
    lines.append(R(bMid(IV_L, IV_R, 'Daily: review failed requests, check cloud account connectivity, verify ABX timeout thresholds')))
    lines.append(R(bMid(IV_L, IV_R, 'Lifecycle: Automation upgrade with pre-upgrade snapshot; embedded vRO and plugin updates')))
    lines.append(R(bMid(IV_L, IV_R, 'Automation: vRA REST API, ABX Python/Node, Terraform integration, vRO workflows')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch request failures · lifecycle keeps Automation current · automation scales delivery'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Request monitoring'),
        bMid(B2_L, B2_R, 'Automation upgrade'),
        bMid(B3_L, B3_R, 'vRA REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Failed deploys'),
        bMid(B2_L, B2_R, 'Pre-upg snapshot'),
        bMid(B3_L, B3_R, 'ABX: Python/Node'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Catalog health'),
        bMid(B2_L, B2_R, 'Embedded vRO'),
        bMid(B3_L, B3_R, 'Terraform intg'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Sub. events'),
        bMid(B2_L, B2_R, 'ABX FaaS update'),
        bMid(B3_L, B3_R, 'vRO workflows'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pipeline status'),
        bMid(B2_L, B2_R, 'Plugin updates'),
        bMid(B3_L, B3_R, 'PowerShell ABX'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ABX timeout chk'),
        bMid(B2_L, B2_R, 'API compat chk'),
        bMid(B3_L, B3_R, 'API Explorer'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops monitor request health · lifecycle upgrades safely with snapshot'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vRA REST API', 'Requests: ok', 'Blueprint ver', 'Pre-upg snap', 'Config export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['ABX function', 'Catalog: items', 'Deploy test', 'Automation upg', 'Policy backup'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Terraform CLI', 'Cloud accts ok', 'ABX test', 'API compat', 'Blueprint bkp'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['API Explorer', 'Pipelines: ok', 'Entitlement', 'Post-upg val', 'Restore redep'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VM (Automation appliance) · RAM DIMMs · Network NICs · Cloud provider connectivity'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Blueprint     = IaC template; versioned in Aria Automation; deploy, update, and destroy lifecycle'))
    lines.append(txt_row('Request       = User-initiated catalog item deployment; tracked in Service Broker with status and'))
    lines.append(txt_row('Catalog item  = Published blueprint or workflow in Service Broker; versioned and'))
    lines.append(txt_row('ABX action    = FaaS function (Python/Node/PowerShell) triggered by events or directly from blueprint'))
    lines.append(txt_row('Subscription  = Event broker rule mapping a lifecycle event to an ABX action or Orchestrator workflow'))
    lines.append(txt_row('Event broker  = Aria Automation event bus; publishes compute/network/storage events to subscriptions'))
    lines.append(txt_row('Cloud account = Aria connection to vCenter/AWS/Azure/GCP; health check ensures connectivity'))
    lines.append(txt_row('Approval policy = Required sign-off before request fulfillment; configurable per catalog item'))
    lines.append(txt_row('Orchestrator workflow = vRO workflow embedded in Aria Automation; runs complex multi-step tasks'))
    lines.append(txt_row('vRA REST API  = Primary Aria Automation programmatic interface; used for requests, blueprints,'))
    lines.append(txt_row('Terraform provider = Aria Automation Terraform provider for IaC-driven provisioning workflows'))
    lines.append(txt_row('Entitlement   = Service Broker policy granting project members access to specific catalog items'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-automation-security',
    'docs/virtualization/vmware/aria-automation/security/index.md',
    'Aria Automation Security — vIDM SSO, RBAC org/project, TLS, audit events',
)
def aria_automation_security():
    """Aria Automation Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Automation — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Workspace ONE/vIDM for SSO; org/project RBAC for catalog and blueprint access control')))
    lines.append(R(bMid(IV_L, IV_R, 'API token management with TTL; approval policies for deployment governance and compliance')))
    lines.append(R(bMid(IV_L, IV_R, 'Secret references for credential storage; Password Locker replaces plaintext in blueprints')))
    lines.append(R(bMid(IV_L, IV_R, 'TLS enforced on all endpoints; cloud account credentials stored encrypted; HTTPS API only')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit log captures all request, catalog, and ABX events for compliance review')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication gates Aria access · RBAC scopes catalog and blueprints · secrets protect credentials'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'WS1/vIDM SSO'),
        bMid(B2_L, B2_R, 'Org/proj roles'),
        bMid(B3_L, B3_R, 'TLS all endpoints'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AD/LDAP intg'),
        bMid(B2_L, B2_R, 'Custom roles'),
        bMid(B3_L, B3_R, 'Secrets at rest'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'API token auth'),
        bMid(B2_L, B2_R, 'Resource-level'),
        bMid(B3_L, B3_R, 'Password Locker'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'OAuth 2.0'),
        bMid(B2_L, B2_R, 'Approval policy'),
        bMid(B3_L, B3_R, 'Cert management'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Project member'),
        bMid(B2_L, B2_R, 'Catalog entitle'),
        bMid(B3_L, B3_R, 'HTTPS API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Break-glass admin'),
        bMid(B2_L, B2_R, 'Cloud zone acc'),
        bMid(B3_L, B3_R, 'Secret refs'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth controls who uses Aria · RBAC limits catalog and blueprint scope'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vIDM/WS1 SSO', 'Org admin', 'TLS enforced', 'API token TTL', 'Request audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AD/LDAP', 'Project roles', 'Secrets encr', 'Min permissions', 'Catalog events'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['API tokens', 'Custom roles', 'Password Locker', 'Cert rotation', 'ABX log audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['OAuth 2.0', 'Approval policy', 'HTTPS only', 'Secret refs', 'Org event log'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VM (Automation appliance) · RAM DIMMs · Network NICs · Identity provider infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vIDM (Identity Manager) = VMware Identity Manager; provides SSO for Aria Automation via SAML/OAuth'))
    lines.append(txt_row('Workspace ONE = Broadcom unified endpoint and identity platform; SSO source for Aria Automation'))
    lines.append(txt_row('Organization  = Top-level Aria Automation tenant; all projects and users belong to an organization'))
    lines.append(txt_row('Project       = Aria Automation grouping; scopes cloud zones, members, and catalog entitlements'))
    lines.append(txt_row('RBAC          = Role-based access control; org/project roles control blueprint and catalog access'))
    lines.append(txt_row('API token     = Bearer token for Aria REST API; has configurable TTL; scoped to user role'))
    lines.append(txt_row('Approval policy = Deployment governance requiring approver action before request proceeds'))
    lines.append(txt_row('Entitlement   = Service Broker policy controlling which projects can consume which catalog items'))
    lines.append(txt_row('Password Locker = Aria Automation encrypted credential store; replaces plaintext blueprint passwords'))
    lines.append(txt_row('Secret reference = Blueprint reference to Password Locker entry; keeps credentials out of IaC code'))
    lines.append(txt_row('Cloud account credentials = Encrypted vCenter/cloud API keys stored in Aria Automation'))
    lines.append(txt_row('OAuth 2.0     = Token-based authorization protocol; used for Aria API and third-party integrations'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-automation-troubleshooting',
    'docs/virtualization/vmware/aria-automation/troubleshooting/index.md',
    'Aria Automation Troubleshooting — deployment failures, vRO errors, ABX, support bundle',
)
def aria_automation_troubleshooting():
    """Aria Automation Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Automation — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Blueprint deploy failures; ABX action errors; cloud account connectivity issues')))
    lines.append(R(bMid(IV_L, IV_R, 'Catalog item errors; pipeline failures; API debug for root cause analysis')))
    lines.append(R(bMid(IV_L, IV_R, 'Event broker subscription troubleshooting; lease expiry and approval stuck scenarios')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnostics: vRA API debug, ABX function logs, vRO log files, request detail view')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: vRA log bundle export; GSS case; TAM for P1; support compatibility matrix')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues define the triage path · diagnostics isolate root cause'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Blueprint fail'),
        bMid(B2_L, B2_R, 'vRA API debug'),
        bMid(B3_L, B3_R, 'vRA log bundle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ABX action err'),
        bMid(B2_L, B2_R, 'ABX function log'),
        bMid(B3_L, B3_R, 'GSS case open'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cloud acct conn'),
        bMid(B2_L, B2_R, 'vRO log files'),
        bMid(B3_L, B3_R, 'ABX debug mode'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Catalog item err'),
        bMid(B2_L, B2_R, 'Request details'),
        bMid(B3_L, B3_R, 'API trace'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Lease expiry'),
        bMid(B2_L, B2_R, 'Event broker log'),
        bMid(B3_L, B3_R, 'Support matrix'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Approval stuck'),
        bMid(B2_L, B2_R, 'ABX FaaS console'),
        bMid(B3_L, B3_R, 'Log export'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics use API and logs · escalation bundles evidence for GSS'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Blueprint fail', 'vRA API debug', '/var/log/vra', 'vRA log bundle', 'Re-deploy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['ABX error', 'ABX func logs', '/var/log/abx', 'GSS P1 case', 'Fix + retry'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cloud acct err', 'vRO logs', '/var/log/vro', 'TAM escalate', 'Re-auth acct'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Approval stuck', 'Event broker', '/var/log/event', 'Support matrix', 'Clear + retry'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VM (Automation appliance) · RAM DIMMs · Network NICs · Cloud provider APIs'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Blueprint deployment = End-to-end request from Service Broker through Assembler to cloud provider'))
    lines.append(txt_row('ABX action    = FaaS function failure; check ABX console logs and timeout configuration'))
    lines.append(txt_row('Cloud account = vCenter/AWS/Azure connection; re-validate credentials and proxy connectivity'))
    lines.append(txt_row('Catalog item  = Service Broker published item; errors traced via request detail and event log'))
    lines.append(txt_row('Approval policy = Stuck approval due to missing approver; check policy config and user assignment'))
    lines.append(txt_row('Event broker  = Aria Automation event bus; subscription failures visible in event broker log'))
    lines.append(txt_row('Subscription  = Event-to-action mapping; failed subscriptions appear in event broker error log'))
    lines.append(txt_row('Lease expiry  = Deployment TTL reached; check reclaim notification config and project lease policy'))
    lines.append(txt_row('vRO (Orchestrator) = Embedded workflow engine; logs at /var/log/vro for workflow execution debug'))
    lines.append(txt_row('API debug     = Aria REST API with ?debug=true parameter; returns detailed provisioning trace'))
    lines.append(txt_row('Request lifecycle = Created → Pending Approval → In Progress → Successful/Failed states'))
    lines.append(txt_row('Pipeline stage = Aria Automation Pipelines stage failure; review stage log for task error detail'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-operations-architecture',
    'docs/virtualization/vmware/aria-operations/architecture/index.md',
    'Aria Operations Architecture — analytics cluster, remote collectors, adapters, capacity',
)
def aria_operations_architecture():
    """Aria Operations Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Operations — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Operations (formerly vROps) — analytics cluster: primary + replica + data nodes per site')))
    lines.append(R(bMid(IV_L, IV_R, 'Remote collectors deployed per site collect metrics without exposing firewall paths to the')))
    lines.append(R(bMid(IV_L, IV_R, 'Adapter instances per integration: vSphere, NSX-T, storage, ServiceNow, SIEM, email/SNMP')))
    lines.append(R(bMid(IV_L, IV_R, 'Dashboards and alerts surface health, risk, efficiency badges across vSphere, NSX, storage,')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity management and optimization actions right-size VMs and forecast resource exhaustion')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines the cluster internals · integrations connect adapters'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Analytics cluster'),
        bMid(B2_L, B2_R, 'vSphere adapter'),
        bMid(B3_L, B3_R, 'Cluster L/XL sizing'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Remote collectors'),
        bMid(B2_L, B2_R, 'NSX-T adapter'),
        bMid(B3_L, B3_R, 'Remote coll/site'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Adapter instances'),
        bMid(B2_L, B2_R, 'Storage adapters'),
        bMid(B3_L, B3_R, 'Adapter config std'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Collector groups'),
        bMid(B2_L, B2_R, 'ServiceNow ITSM'),
        bMid(B3_L, B3_R, 'Data retain 6 mo'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Dashboards+alerts'),
        bMid(B2_L, B2_R, 'SIEM/Kafka'),
        bMid(B3_L, B3_R, 'Alert policy'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Capacity mgmt'),
        bMid(B2_L, B2_R, 'Email/SNMP alert'),
        bMid(B3_L, B3_R, 'Custom dash std'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers cluster nodes · integrations connect adapters and ITSM'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Analytics cluster', 'vSphere adapter', 'Cluster sizing', 'Single node', 'Alert policy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Remote collectors', 'NSX-T adapter', 'Remote coll', 'Small cluster', 'Dashboard std'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Adapter instances', 'Storage adapters', 'Data retention', 'HA cluster', 'Naming conv'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Collector groups', 'ServiceNow intg', 'Custom policies', 'Multi-cloud', 'RBAC std'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (cluster nodes + remote collectors) · RAM DIMMs · Network NICs · vCenter/cloud targets'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Analytics cluster  = Primary + replica + data nodes forming the Aria Ops processing engine'))
    lines.append(txt_row('Primary node       = Cluster leader; hosts the UI, API, and coordinates analytics workload'))
    lines.append(txt_row('Replica node       = Standby for primary; takes over if primary fails; participates in analytics'))
    lines.append(txt_row('Data node          = Additional analytics capacity node; scales metric ingestion and retention'))
    lines.append(txt_row('Remote collector   = Lightweight VM per site; collects adapter data and forwards to cluster'))
    lines.append(txt_row('Adapter instance   = Configured connection to a monitored product: vSphere, NSX, storage, cloud'))
    lines.append(txt_row('Collector group    = Named group of remote collectors assigned to adapter instances for load sharing'))
    lines.append(txt_row('Dashboard          = Customizable view of metrics, badges, and alerts for a resource group'))
    lines.append(txt_row('Alert definition   = Rule triggering notification when a metric crosses a threshold or symptom fires'))
    lines.append(txt_row('Capacity analytics = Forecasting engine projecting resource exhaustion based on trend analysis'))
    lines.append(txt_row('Optimization action = Recommended change (right-size, power off, migrate) to improve efficiency'))
    lines.append(txt_row('Badge              = Health/risk/efficiency score (0-100) summarising object state at a glance'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-operations-operations',
    'docs/virtualization/vmware/aria-operations/operations/index.md',
    'Aria Operations Operations — alert management, right-sizing, lifecycle, REST API',
)
def aria_operations_operations():
    """Aria Operations Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Operations — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Alert management and noise reduction: tune thresholds, suppress flapping, cancel false')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity optimization: review right-sizing recommendations; act on workload placement advice')))
    lines.append(R(bMid(IV_L, IV_R, 'Report scheduling: cost management integration; automated PDF/CSV delivery to stakeholders')))
    lines.append(R(bMid(IV_L, IV_R, 'Cluster node health monitoring: verify all nodes stable; check adapter collection intervals')))
    lines.append(R(bMid(IV_L, IV_R, 'Lifecycle: upgrade wizard sequences node upgrades; pre-upgrade health check mandatory')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops review alerts and capacity · lifecycle keeps cluster current'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert management'),
        bMid(B2_L, B2_R, 'Upgrade planner'),
        bMid(B3_L, B3_R, 'REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Capacity overview'),
        bMid(B2_L, B2_R, 'Pre-upg health'),
        bMid(B3_L, B3_R, 'PowerCLI vROps'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Optim. actions'),
        bMid(B2_L, B2_R, 'Node upg order'),
        bMid(B3_L, B3_R, 'Alert API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Workload place'),
        bMid(B2_L, B2_R, 'Adapter compat'),
        bMid(B3_L, B3_R, 'Capacity API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Badge status'),
        bMid(B2_L, B2_R, 'CMDB sync'),
        bMid(B3_L, B3_R, 'Dashboard API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Report schedule'),
        bMid(B2_L, B2_R, 'Cert renew'),
        bMid(B3_L, B3_R, 'Report API'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch alert noise · lifecycle upgrades nodes in sequence · automation reduces manual toil'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['REST API calls', 'Cluster: green', 'Alert triage', 'Upgrade wizard', 'Config export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['PowerCLI vROps', 'Nodes: healthy', 'Capacity rpt', 'Pre-chk health', 'Support.zip'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Alert API', 'Adapters: ok', 'Add remote coll', 'Node upg order', 'Restore config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Capacity API', 'Collectors: up', 'Dashboard add', 'Post-upg val', 'Metric data bk'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (primary/replica/data/collector) · RAM DIMMs · Network NICs · vCenter/cloud connectivity'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Analytics cluster  = Primary + replica + data nodes; all must be healthy for full functionality'))
    lines.append(txt_row('Remote collector   = Lightweight VM per site forwarding adapter metrics to the analytics cluster'))
    lines.append(txt_row('Adapter instance   = Configured integration to a monitored product; collection interval configurable'))
    lines.append(txt_row('Alert definition   = Symptom-based rule firing notifications on threshold breach or anomaly'))
    lines.append(txt_row('Capacity engine    = Forecasting subsystem projecting time-to-exhaustion for CPU, RAM, storage'))
    lines.append(txt_row('Optimization action = Right-size, power-off, or migrate recommendation generated by analytics'))
    lines.append(txt_row('Workload placement = DRS-aligned recommendation for optimal VM-to-host assignment'))
    lines.append(txt_row('Badge score        = 0-100 health/risk/efficiency score assigned to every monitored object'))
    lines.append(txt_row('Right-sizing       = Reducing oversized vCPU/RAM allocations based on observed peak utilisation'))
    lines.append(txt_row('Cost driver        = Resource consumer identified as a top contributor to capacity or cost usage'))
    lines.append(txt_row('Upgrade planner    = Built-in wizard validating compatibility and sequencing node upgrade steps'))
    lines.append(txt_row('support.zip bundle = Diagnostic package collected from Aria Ops for GSS case submission'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-operations-security',
    'docs/virtualization/vmware/aria-operations/security/index.md',
    'Aria Operations Security — vIDM SSO, RBAC roles, TLS, API tokens, audit log',
)
def aria_operations_security():
    """Aria Operations Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Operations — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'vIDM/Active Directory integration for SSO; RBAC roles (admin/user/viewer) for object-level')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate management: cluster and adapter TLS certificates rotated on schedule')))
    lines.append(R(bMid(IV_L, IV_R, 'API token authentication: scoped bearer tokens for REST API integrations and automation')))
    lines.append(R(bMid(IV_L, IV_R, 'All REST API communication over TLS; encrypted passwords stored in credential vault')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit event log captures all admin actions; syslog forwarding to SIEM over TLS')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication gates access · RBAC scopes permissions · encryption and audit enforce compliance'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vIDM/AD auth'),
        bMid(B2_L, B2_R, 'Admin: full access'),
        bMid(B3_L, B3_R, 'REST over TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LDAP/AD groups'),
        bMid(B2_L, B2_R, 'User: dashboards'),
        bMid(B3_L, B3_R, 'Cert management'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Local admin'),
        bMid(B2_L, B2_R, 'Viewer: read-only'),
        bMid(B3_L, B3_R, 'Encrypted passwords'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert-based auth'),
        bMid(B2_L, B2_R, 'Object-level acc'),
        bMid(B3_L, B3_R, 'Syslog over TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'API token'),
        bMid(B2_L, B2_R, 'Custom roles'),
        bMid(B3_L, B3_R, 'Data encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Audit log'),
        bMid(B2_L, B2_R, 'Content share'),
        bMid(B3_L, B3_R, 'FIPS mode'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth controls who logs in · access control limits scope · encryption and audit enforce compliance'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vIDM/AD SSO', 'Admin role', 'TLS enforced', 'Cert rotation', 'Event audit log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LDAP groups', 'User role', 'Pwd encrypted', 'API token TTL', 'Adapter log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['API tokens', 'Viewer role', 'Syslog TLS', 'RBAC review', 'Alert log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cert-based', 'Object access', 'FIPS mode', 'Min-perm API', 'Config changes'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (cluster) · RAM DIMMs · Network NICs · Identity provider (AD/LDAP) · CA infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vIDM               = VMware Identity Manager; provides SSO and group-based role assignment to Aria'))
    lines.append(txt_row('Active Directory    = LDAP-compatible directory; groups mapped to Aria Ops roles for user access'))
    lines.append(txt_row('RBAC               = Role-Based Access Control; admin/user/viewer roles scoped to object groups'))
    lines.append(txt_row('Admin role         = Full access: manage adapters, alerts, dashboards, users, and system config'))
    lines.append(txt_row('User role          = Dashboard and alert access; can create content but not manage system config'))
    lines.append(txt_row('Viewer role        = Read-only access to dashboards and alerts; cannot create or modify content'))
    lines.append(txt_row('Object-level access = Permissions scoped to specific resource groups or monitored object sets'))
    lines.append(txt_row('API token          = Bearer token for REST API auth; scoped to user role; configurable TTL'))
    lines.append(txt_row('TLS                = Transport Layer Security; all API and UI communication encrypted in transit'))
    lines.append(txt_row('FIPS mode          = Federal Information Processing Standard 140-2 compliant cryptography mode'))
    lines.append(txt_row('Certificate management = Rotate cluster TLS and adapter certs via admin UI or REST API'))
    lines.append(txt_row('Audit event log    = Immutable record of all admin actions: login, config change, user management'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-operations-troubleshooting',
    'docs/virtualization/vmware/aria-operations/troubleshooting/index.md',
    'Aria Operations Troubleshooting — adapter failures, alert noise, missing data, support.zip',
)
def aria_operations_troubleshooting():
    """Aria Operations Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Operations — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Adapter collection failures: verify credentials, firewall paths, and adapter version')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert noise and false positives: tune symptom thresholds; check adapter collection gaps')))
    lines.append(R(bMid(IV_L, IV_R, 'Missing metric data: confirm remote collector reachability; check collector group assignment')))
    lines.append(R(bMid(IV_L, IV_R, 'Dashboard errors: verify data source adapter health; check widget metric mappings')))
    lines.append(R(bMid(IV_L, IV_R, 'support.zip bundle collects all cluster logs; attach to GSS case for escalation')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics isolate adapter or cluster root cause'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Adapter coll fail'),
        bMid(B2_L, B2_R, 'Cluster diagnostics'),
        bMid(B3_L, B3_R, 'Support.zip'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert noise'),
        bMid(B2_L, B2_R, 'Adapter log'),
        bMid(B3_L, B3_R, 'GSS case open'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Missing data'),
        bMid(B2_L, B2_R, 'Support.zip'),
        bMid(B3_L, B3_R, 'Skyline health'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Dashboard error'),
        bMid(B2_L, B2_R, 'REST API debug'),
        bMid(B3_L, B3_R, 'TAM escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Remote coll down'),
        bMid(B2_L, B2_R, 'Log Insight intg'),
        bMid(B3_L, B3_R, 'Log bundle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Capacity wrong'),
        bMid(B2_L, B2_R, 'Metric explorer'),
        bMid(B3_L, B3_R, 'Version compat'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues triage adapter and cluster faults · diagnostics use logs and metric explorer'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Adapter fail', 'Adapter log', '/var/log/vrops', 'support.zip', 'Re-auth adapter'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Alert noise', 'Metric explorer', 'Cluster diag', 'GSS P1 case', 'Tune alert'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Missing data', 'REST API debug', '/var/log/casa', 'TAM escalate', 'Re-collect'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Collector down', 'Support.zip', '/var/log/coll', 'Skyline health', 'Restart coll'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (cluster nodes + collectors) · RAM DIMMs · Network NICs · vCenter/cloud connectivity'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Adapter collection = Periodic metric pull by an adapter instance; fails on auth or network errors'))
    lines.append(txt_row('Remote collector   = Site-local VM forwarding metrics; offline if unreachable or out of resources'))
    lines.append(txt_row('Alert noise        = Excessive or false-positive alerts caused by overly sensitive symptom thresholds'))
    lines.append(txt_row('Metric gap         = Missing data points in a metric time series; caused by collection or node'))
    lines.append(txt_row('Support.zip bundle = Full diagnostic archive from Aria Ops cluster; submitted to GSS for analysis'))
    lines.append(txt_row('Cluster diagnostics = Built-in health tool validating node connectivity, services, and disk usage'))
    lines.append(txt_row('Metric explorer    = UI tool for querying raw metric time series to identify gaps or anomalies'))
    lines.append(txt_row('Capacity calculation = Engine consuming metric history to project resource exhaustion dates'))
    lines.append(txt_row('Skyline Health     = VMware proactive support tool that validates cluster health against best'))
    lines.append(txt_row('REST API           = Aria Ops API for querying metrics, alerts, recommendations programmatically'))
    lines.append(txt_row('Log Insight intg   = Aria Logs integration forwarding Aria Ops cluster logs for structured search'))
    lines.append(txt_row('False positive alert = Alert firing when no real problem exists; tuned via symptom threshold change'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-logs-architecture',
    'docs/virtualization/vmware/aria-operations-for-logs/architecture/index.md',
    'Aria Logs Architecture — master/worker HA cluster, vRLI agents, VLQL, content packs',
)
def aria_logs_architecture():
    """Aria Logs Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Logs — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Operations for Logs (formerly vRealize Log Insight) — master node + worker nodes HA')))
    lines.append(R(bMid(IV_L, IV_R, 'vRLI agents on Windows/Linux hosts; syslog TCP/UDP ingestion from network devices and ESXi')))
    lines.append(R(bMid(IV_L, IV_R, 'VLQL structured queries for interactive analytics; alert pipelines to vROps/email/webhook')))
    lines.append(R(bMid(IV_L, IV_R, 'Content packs provide structured field extraction and dashboards for known log sources')))
    lines.append(R(bMid(IV_L, IV_R, 'Log forwarder exports filtered streams to SIEM; retention enforced by disk policy per node')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines cluster mechanics · integrations connect log sources'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Master + workers HA'),
        bMid(B2_L, B2_R, 'vROps integration'),
        bMid(B3_L, B3_R, '3-node HA cluster'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vRLI agents'),
        bMid(B2_L, B2_R, 'NSX syslog'),
        bMid(B3_L, B3_R, 'Log retention pol'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Syslog TCP/UDP'),
        bMid(B2_L, B2_R, 'ESXi syslog'),
        bMid(B3_L, B3_R, 'Agent deployment'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VLQL queries'),
        bMid(B2_L, B2_R, 'Windows agent'),
        bMid(B3_L, B3_R, 'Alert thresholds'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert pipelines'),
        bMid(B2_L, B2_R, 'Syslog sources'),
        bMid(B3_L, B3_R, 'Content pack org'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Content packs'),
        bMid(B2_L, B2_R, 'SIEM forwarding'),
        bMid(B3_L, B3_R, 'Disk sizing'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers cluster and ingestion · integrations connect sources'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Master+workers', 'vROps intg', '3-node cluster', 'Single node', 'Retention pol'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vRLI agents', 'NSX syslog', 'Log retention', 'HA cluster', 'Alert thresh'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Syslog TCP/UDP', 'ESXi syslog', 'Agent deploy', 'Forwarder', 'Disk sizing'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VLQL queries', 'SIEM forward', 'Alert config', 'Multi-site', 'Content packs'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (master + workers) · RAM DIMMs · Network NICs · High-capacity storage (log disk)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master node        = Aria Logs cluster leader; hosts UI, API, and coordinates ingestion across'))
    lines.append(txt_row('Worker node        = Additional cluster member; shares ingestion load and stores log partitions'))
    lines.append(txt_row('vRLI agent         = Lightweight agent on Windows/Linux; forwards structured log events to cluster'))
    lines.append(txt_row('Syslog ingestion   = UDP/TCP syslog receiver on port 514/6514; accepts RFC3164/5424 formatted logs'))
    lines.append(txt_row('VLQL               = vRLI Query Language; structured query syntax for filtering and aggregating logs'))
    lines.append(txt_row('Content pack       = Pre-built dashboards and field extractors for a specific log source (NSX,'))
    lines.append(txt_row('Alert pipeline     = Rule triggering notifications or forwarding to vROps/email/webhook on log match'))
    lines.append(txt_row('Log forwarder      = Cluster feature streaming filtered log events to an external SIEM destination'))
    lines.append(txt_row('Structured parsing = Field extraction from raw log text using content pack or custom regex rules'))
    lines.append(txt_row('Log retention      = Disk-based policy deleting oldest log partitions when capacity threshold reached'))
    lines.append(txt_row('HA cluster         = Master + 2+ worker nodes with integrated load balancer virtual IP for ingestion'))
    lines.append(txt_row('Interactive analytics = UI-based VLQL query workspace for ad-hoc log investigation and charting'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-logs-operations',
    'docs/virtualization/vmware/aria-operations-for-logs/operations/index.md',
    'Aria Logs Operations — alert management, disk retention, content packs, upgrade',
)
def aria_logs_operations():
    """Aria Logs Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Logs — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Alert management and dashboard queries; agent health monitoring across all forwarding hosts')))
    lines.append(R(bMid(IV_L, IV_R, 'Disk usage and retention enforcement: monitor partition fill rate; expand disks proactively')))
    lines.append(R(bMid(IV_L, IV_R, 'Content pack management: import, update, and validate packs for new log source onboarding')))
    lines.append(R(bMid(IV_L, IV_R, 'Forwarder configuration for SIEM integration: filter, tag, and stream log events externally')))
    lines.append(R(bMid(IV_L, IV_R, 'vRLI upgrade sequence: backup config, upgrade nodes in order, validate post-upgrade health')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops review alerts and agents · lifecycle upgrades nodes safely'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert review'),
        bMid(B2_L, B2_R, 'vRLI upgrades'),
        bMid(B3_L, B3_R, 'vRLI REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Dashboard query'),
        bMid(B2_L, B2_R, 'Pre-chk backup'),
        bMid(B3_L, B3_R, 'Content pk import'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Agent health'),
        bMid(B2_L, B2_R, 'Node upg order'),
        bMid(B3_L, B3_R, 'Agent config API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Disk usage'),
        bMid(B2_L, B2_R, 'Agent upgrade'),
        bMid(B3_L, B3_R, 'Alert API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Source health'),
        bMid(B2_L, B2_R, 'Content pk update'),
        bMid(B3_L, B3_R, 'Query API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Content pk status'),
        bMid(B2_L, B2_R, 'Cert renew'),
        bMid(B3_L, B3_R, 'VLQL scripted'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops monitor agents and disk · lifecycle upgrades safely'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['REST API calls', 'Cluster: green', 'Alert tune', 'Upgrade node', 'Config export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VLQL queries', 'Agents: sending', 'Add log source', 'Agent update', 'Content bkp'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Alert API', 'Disk: <80%', 'Forwarder cfg', 'Content pk upg', 'Restore config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Content pk API', 'Sources: active', 'Retention chk', 'Post-upg val', 'Log archive'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (master + workers) · RAM DIMMs · Network NICs · High-capacity log storage · Syslog network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Content pack       = Pre-built field extractors and dashboards; imported via UI or REST API'))
    lines.append(txt_row('vRLI agent         = Host-based log forwarder; reports sending state visible in admin sources page'))
    lines.append(txt_row('Alert pipeline     = Log-match rule triggering email, webhook, or vROps notification on condition'))
    lines.append(txt_row('VLQL query         = vRLI Query Language statement for filtering, grouping, and charting log events'))
    lines.append(txt_row('Log forwarder      = Cluster feature streaming matched events to SIEM via syslog or REST endpoint'))
    lines.append(txt_row('Disk retention     = Automatic deletion of oldest log partitions when disk reaches configured'))
    lines.append(txt_row('HA cluster upgrade = Sequenced upgrade: master node last; workers upgraded first to preserve'))
    lines.append(txt_row('Source health      = Admin UI view showing per-source event rate and last-received timestamp'))
    lines.append(txt_row('REST API           = vRLI API for querying events, managing alerts, sources, and content packs'))
    lines.append(txt_row('Interactive analytics = VLQL query workspace for ad-hoc investigation with chart and table views'))
    lines.append(txt_row('Log ingestion rate = Events-per-second metric; baseline for disk capacity planning and alerting'))
    lines.append(txt_row('Content pack version = Versioned pack release; update to get new dashboards and field extractors'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-logs-security',
    'docs/virtualization/vmware/aria-operations-for-logs/security/index.md',
    'Aria Logs Security — AD/LDAP SSO, RBAC, TLS agent/syslog, FIPS, audit trail',
)
def aria_logs_security():
    """Aria Logs Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Logs — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Active Directory/LDAP for SSO; role-based access for dashboards and alerts per user group')))
    lines.append(R(bMid(IV_L, IV_R, 'TLS for agent connections and syslog TCP/TLS; REST API served over HTTPS only')))
    lines.append(R(bMid(IV_L, IV_R, 'FIPS 140-2 mode available; encrypted passwords at rest in credential store')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit trail captures all admin actions: login events, config changes, source additions')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate rotation for agent TLS, cluster UI cert, and syslog TLS endpoints')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication gates access · role-based access scopes dashboards'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AD/LDAP auth'),
        bMid(B2_L, B2_R, 'Admin: full'),
        bMid(B3_L, B3_R, 'Agent TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LDAP integration'),
        bMid(B2_L, B2_R, 'User: dashboards'),
        bMid(B3_L, B3_R, 'Syslog TCP/TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Local admin'),
        bMid(B2_L, B2_R, 'Dashboard roles'),
        bMid(B3_L, B3_R, 'REST over HTTPS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Role-based'),
        bMid(B2_L, B2_R, 'Source access'),
        bMid(B3_L, B3_R, 'Cert management'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'API token'),
        bMid(B2_L, B2_R, 'Alert mgmt'),
        bMid(B3_L, B3_R, 'FIPS mode'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SAML support'),
        bMid(B2_L, B2_R, 'Content pk admin'),
        bMid(B3_L, B3_R, 'Pwd encrypted'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth controls who logs in · access control scopes dashboards · encryption secures all log paths'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AD/LDAP SSO', 'Admin role', 'Agent TLS', 'Cert rotation', 'Admin events'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['API tokens', 'User role', 'Syslog TLS', 'FIPS mode', 'Query log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SAML support', 'Dashboard role', 'HTTPS REST', 'Pwd policy', 'Alert audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Local admin', 'Source access', 'Cert mgmt', 'Min-perm API', 'Config changes'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (cluster) · RAM DIMMs · Network NICs · AD/LDAP server · CA infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('AD/LDAP            = Active Directory/LDAP; group membership mapped to Aria Logs roles'))
    lines.append(txt_row('SAML               = Security Assertion Markup Language; federated SSO for Aria Logs UI login'))
    lines.append(txt_row('Role-based access   = Admin/user/viewer roles; scoped to dashboard sets and log source access'))
    lines.append(txt_row('Admin role         = Full Aria Logs access: manage sources, alerts, content packs, and users'))
    lines.append(txt_row('User role          = Dashboard view and query access; cannot manage sources or system config'))
    lines.append(txt_row('TLS agent connection = Encrypted channel between vRLI agent and cluster ingestion endpoint'))
    lines.append(txt_row('Syslog over TLS    = RFC5425 TLS-wrapped syslog on port 6514; encrypts log transit from sources'))
    lines.append(txt_row('FIPS 140-2         = Federal cryptographic standard; enabled at cluster level for compliance'))
    lines.append(txt_row('Certificate management = Rotate UI, agent, and syslog TLS certificates via admin settings'))
    lines.append(txt_row('API token          = Bearer token for REST API calls; scoped to authenticated user role'))
    lines.append(txt_row('Audit trail        = Immutable log of admin actions: logins, config changes, source management'))
    lines.append(txt_row('Encrypted credentials = Passwords and secrets stored encrypted in cluster credential vault'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-logs-troubleshooting',
    'docs/virtualization/vmware/aria-operations-for-logs/troubleshooting/index.md',
    'Aria Logs Troubleshooting — agents silent, disk full, alert not firing, vRLI bundle',
)
def aria_logs_troubleshooting():
    """Aria Logs Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Logs — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Agents not sending logs: check agent connectivity, firewall rules, and agent configuration')))
    lines.append(R(bMid(IV_L, IV_R, 'Missing log sources: verify syslog UDP/TCP port reachability and source IP configuration')))
    lines.append(R(bMid(IV_L, IV_R, 'Disk full blocking ingestion: expand disk or reduce retention; clear oldest partitions')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert not firing: validate field extraction in content pack; check query match logic')))
    lines.append(R(bMid(IV_L, IV_R, 'vRLI support bundle collects cluster and agent logs; attach to GSS case for escalation')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues triage agent and source faults · diagnostics use logs and API'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Agent not sending'),
        bMid(B2_L, B2_R, 'Admin UI sources'),
        bMid(B3_L, B3_R, 'vRLI support bndl'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Source missing'),
        bMid(B2_L, B2_R, 'Agent log files'),
        bMid(B3_L, B3_R, 'GSS case open'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Disk full'),
        bMid(B2_L, B2_R, '/var/log/loginsight'),
        bMid(B3_L, B3_R, 'Agent config exp'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert not fire'),
        bMid(B2_L, B2_R, 'REST API debug'),
        bMid(B3_L, B3_R, 'Log sample coll'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Query empty'),
        bMid(B2_L, B2_R, 'Source status'),
        bMid(B3_L, B3_R, 'TAM escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Forwarder err'),
        bMid(B2_L, B2_R, 'Content pk test'),
        bMid(B3_L, B3_R, 'Version matrix'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics use source admin and log paths'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Agent silent', 'Agent log file', '/var/log/loginsight', 'vRLI bundle', 'Restart agent'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Disk full', 'Source status', '/var/log/li-server', 'GSS P1 case', 'Expand disk'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Alert not fire', 'REST API dbg', '/var/log/agent', 'TAM escalate', 'Retune alert'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Query empty', 'Content pk test', '/var/log/server', 'Version matrix', 'Fix time range'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (cluster) · RAM DIMMs · Network NICs · Log storage · Syslog source hosts'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vRLI agent         = Host-based log forwarder; check agent service status and firewall on port 9000'))
    lines.append(txt_row('Syslog source      = Network device or host sending UDP/TCP syslog; verify source IP is allowed'))
    lines.append(txt_row('Disk retention     = Policy deleting oldest partitions at threshold; full disk blocks all ingestion'))
    lines.append(txt_row('Alert pipeline     = Log-match rule; fails silently if field extraction is incorrect in content pack'))
    lines.append(txt_row('VLQL query         = Query returning empty if time range, field name, or syntax is incorrect'))
    lines.append(txt_row('Content pack       = Field extractor and dashboard bundle; test via UI to validate regex patterns'))
    lines.append(txt_row('Log forwarder      = SIEM stream; errors if destination unreachable or certificate mismatch'))
    lines.append(txt_row('Ingestion rate     = Events-per-second; drop to zero indicates cluster issue or source problem'))
    lines.append(txt_row('Cluster node health = Admin dashboard showing master and worker node status and disk usage'))
    lines.append(txt_row('REST API debug     = Query the vRLI API directly to bypass UI and validate field extraction'))
    lines.append(txt_row('Support bundle     = Full diagnostic archive: cluster logs, config, and event data for GSS review'))
    lines.append(txt_row('Agent configuration = JSON config file on host specifying cluster address, port, and log paths'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-networks-architecture',
    'docs/virtualization/vmware/aria-operations-for-networks/architecture/index.md',
    'Aria Networks Architecture — platform/collector VMs, IPFIX flows, path analysis, NSX',
)
def aria_networks_architecture():
    """Aria Networks Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Networks — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Operations for Networks (formerly vRealize Network Insight) = Platform VM + Collector VMs')))
    lines.append(R(bMid(IV_L, IV_R, 'Ingests VMware (NSX/vCenter) and physical switch data (SNMP) for full-stack network visibility')))
    lines.append(R(bMid(IV_L, IV_R, 'Provides network topology, path tracing, flow analysis, and security group auditing')))
    lines.append(R(bMid(IV_L, IV_R, 'Collector VMs deployed per site forward data to the central Platform VM for correlation')))
    lines.append(R(bMid(IV_L, IV_R, 'Data sources: NSX-T/V, vCenter, physical switches (SNMP v3), AWS/Azure VPC flow logs, IPAM')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines data collection mechanics · integrations connect all data sources'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Platform VM: central'),
        bMid(B2_L, B2_R, 'NSX-T/V source'),
        bMid(B3_L, B3_R, 'Collector per site'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Collector VMs: sites'),
        bMid(B2_L, B2_R, 'vCenter source'),
        bMid(B3_L, B3_R, 'Platform sizing'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NSX data source'),
        bMid(B2_L, B2_R, 'Physical switch'),
        bMid(B3_L, B3_R, 'Data src creds'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Physical SNMP'),
        bMid(B2_L, B2_R, 'AWS/Azure VPC'),
        bMid(B3_L, B3_R, 'SNMP v3 config'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Path trace engine'),
        bMid(B2_L, B2_R, 'IPAM integration'),
        bMid(B3_L, B3_R, 'Collection interval'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Flow analysis'),
        bMid(B2_L, B2_R, 'Log Insight fwd'),
        bMid(B3_L, B3_R, 'Retention policy'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers data ingestion · integrations bring in all network sources'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Platform VM', 'NSX-T source', 'Collector sizing', 'Single platform', 'SNMP v3'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Collector VMs', 'vCenter source', 'Platform size', 'Multi-site', 'Cred rotation'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Path trace', 'Physical SNMP', 'Retention pol', 'AWS/Azure', 'Collection intv'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Flow analysis', 'IPAM intg', 'Cred mgmt', 'Enterprise', 'Alert thresh'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (Platform + Collector) · RAM DIMMs · Network NICs · Physical switches (SNMP) · NSX/vCenter'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Platform VM       = Central Aria Networks appliance; receives data from all Collectors; hosts the UI'))
    lines.append(txt_row('Collector VM      = Per-site VM that collects data from local data sources and forwards to Platform'))
    lines.append(txt_row('Data source       = Configured connection to NSX, vCenter, physical switch, or cloud for data'))
    lines.append(txt_row('Path tracing      = End-to-end network path visualization from source VM to destination across'))
    lines.append(txt_row('Flow analysis     = Query interface for historical and real-time network flow data from all data'))
    lines.append(txt_row('SNMP v3           = SNMPv3 protocol for physical switch collection; provides auth and encryption'))
    lines.append(txt_row('NSX-T data source = Aria Networks integration that ingests NSX topology, DFW rules, and flow data'))
    lines.append(txt_row('Physical topology = Network map that includes physical switches alongside virtual overlay components'))
    lines.append(txt_row('VPC flow logs     = AWS/Azure network flow records ingested by Aria Networks for hybrid visibility'))
    lines.append(txt_row('Network intent check = Policy verification that compares actual traffic flows against defined'))
    lines.append(txt_row('Security group audit = Review of NSX/cloud security group membership and rule coverage for compliance'))
    lines.append(txt_row('Collection interval = Frequency at which Collector VMs poll each data source; configurable per'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-networks-operations',
    'docs/virtualization/vmware/aria-operations-for-networks/operations/index.md',
    'Aria Networks Operations — flow queries, path analysis, alert management, upgrade',
)
def aria_networks_operations():
    """Aria Networks Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Networks — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Network intent checks for policy compliance; flow analysis queries for traffic patterns per')))
    lines.append(R(bMid(IV_L, IV_R, 'Path trace for troubleshooting connectivity issues between any two endpoints in the environment')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert review for topology changes; security group auditing for microsegmentation drift')))
    lines.append(R(bMid(IV_L, IV_R, 'Lifecycle: vRNI upgrades via Platform UI; upgrade Platform first then Collector VMs at each')))
    lines.append(R(bMid(IV_L, IV_R, 'Automation: REST API for path trace, flow query, alert management, and scheduled report')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops verify network intent · lifecycle keeps platform current'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Intent checks'),
        bMid(B2_L, B2_R, 'vRNI upgrades'),
        bMid(B3_L, B3_R, 'vRNI REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert review'),
        bMid(B2_L, B2_R, 'Platform+coll upg'),
        bMid(B3_L, B3_R, 'Path trace API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Flow analysis'),
        bMid(B2_L, B2_R, 'Data src re-auth'),
        bMid(B3_L, B3_R, 'Flow query API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Sec grp audit'),
        bMid(B2_L, B2_R, 'SNMP compat'),
        bMid(B3_L, B3_R, 'Alert API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Path trace'),
        bMid(B2_L, B2_R, 'Cert renew'),
        bMid(B3_L, B3_R, 'Report API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Dashboard review'),
        bMid(B2_L, B2_R, 'Config backup'),
        bMid(B3_L, B3_R, 'Python SDK'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch policy drift · lifecycle upgrades Platform before Collectors'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['REST API calls', 'Platform: ok', 'Intent check', 'Upgrade plat', 'Config export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Flow query API', 'Collectors: up', 'Path trace', 'Coll upgrade', 'API config bk'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Alert API', 'Data srcs: ok', 'Sec grp audit', 'Data src auth', 'Restore config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Python SDK', 'Alerts: none', 'Flow report', 'Post-upg val', 'Log archive'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (Platform + Collectors) · RAM DIMMs · Network NICs · NSX/vCenter/Physical switches'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Network intent    = Defined policy for how traffic should flow between workloads; verified against'))
    lines.append(txt_row('Path trace        = On-demand trace of the actual network path between two endpoints in the'))
    lines.append(txt_row('Flow analysis     = Query of historical flow data to identify communication patterns and anomalies'))
    lines.append(txt_row('Security group audit = Comparison of current security group membership against expected baseline'))
    lines.append(txt_row('Data source       = Configured NSX/vCenter/switch/cloud connection; requires re-auth after cred'))
    lines.append(txt_row('Collector health  = Status of each site Collector VM; must show connected and collecting for valid'))
    lines.append(txt_row('REST API          = Aria Networks REST API; supports path trace, flow query, alert, and report'))
    lines.append(txt_row('Platform upgrade  = Upgrade Platform VM first using built-in UI wizard before upgrading any'))
    lines.append(txt_row('Collector upgrade = Per-site upgrade of Collector VMs after Platform VM upgrade is validated'))
    lines.append(txt_row('SNMP v3           = SNMPv3 credentials for physical switch collection; compat check needed at upgrade'))
    lines.append(txt_row('VPC flow logs     = Cloud provider flow logs from AWS/Azure ingested for hybrid network visibility'))
    lines.append(txt_row('Alert threshold   = Configurable metric limit that triggers an Aria Networks alert for topology'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-networks-security',
    'docs/virtualization/vmware/aria-operations-for-networks/security/index.md',
    'Aria Networks Security — vIDM SSO, RBAC, TLS, API tokens, audit log',
)
def aria_networks_security():
    """Aria Networks Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Networks — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'AD/LDAP auth for user access; data source service accounts for NSX/vCenter/switch collection')))
    lines.append(R(bMid(IV_L, IV_R, 'API key management for REST API access; SNMP v3 credentials for physical switch collection')))
    lines.append(R(bMid(IV_L, IV_R, 'REST API over TLS; role-based access for data visibility; SAML support for SSO integration')))
    lines.append(R(bMid(IV_L, IV_R, 'Roles: Admin (full), Member (view), Auditor (read-only); scoped to data source visibility')))
    lines.append(R(bMid(IV_L, IV_R, 'Credential rotation policy for data source service accounts; API key TTL enforcement')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication gates platform access · RBAC limits data visibility'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AD/LDAP auth'),
        bMid(B2_L, B2_R, 'Admin: full'),
        bMid(B3_L, B3_R, 'REST API TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Local admin'),
        bMid(B2_L, B2_R, 'Member: view'),
        bMid(B3_L, B3_R, 'Collector TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Data src svc acct'),
        bMid(B2_L, B2_R, 'Auditor: read'),
        bMid(B3_L, B3_R, 'Data at rest'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'API key mgmt'),
        bMid(B2_L, B2_R, 'Data src access'),
        bMid(B3_L, B3_R, 'Cert mgmt'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SAML support'),
        bMid(B2_L, B2_R, 'Report share'),
        bMid(B3_L, B3_R, 'SNMP v3 auth'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Role-based'),
        bMid(B2_L, B2_R, 'Alert mgmt'),
        bMid(B3_L, B3_R, 'Pwd storage'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth controls user access · RBAC scopes data visibility · TLS and SNMP v3 protect data in transit'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AD/LDAP auth', 'Admin role', 'REST TLS', 'Cred rotation', 'Event log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['API keys', 'Member role', 'Collector TLS', 'SNMP v3', 'Data src log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Data src accts', 'Auditor role', 'Data encr', 'Cert rotation', 'Alert audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SAML support', 'Report share', 'Pwd storage', 'API key TTL', 'Config changes'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (Platform + Collectors) · RAM DIMMs · Network NICs · AD/LDAP · CA infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('AD/LDAP           = Active Directory or LDAP integration for user authentication to Aria Networks'))
    lines.append(txt_row('API key           = Authentication token for REST API access; scoped to user role; subject to TTL'))
    lines.append(txt_row('Data source credential = Service account used by Aria Networks to connect to NSX, vCenter, or'))
    lines.append(txt_row('SNMP v3           = SNMPv3 credentials for physical switch collection; provides authentication and'))
    lines.append(txt_row('Service account   = Dedicated non-interactive account used for data source authentication and'))
    lines.append(txt_row('Admin role        = Full access role in Aria Networks; can configure data sources, users, and all'))
    lines.append(txt_row('Member role       = Standard access role; can view topology, run queries, and use path trace features'))
    lines.append(txt_row('Auditor role      = Read-only role; can view all data and reports but cannot make configuration'))
    lines.append(txt_row('TLS encryption    = Transport Layer Security enforced on all REST API and Collector-to-Platform'))
    lines.append(txt_row('Certificate management = Platform and Collector TLS cert lifecycle including rotation and CA trust'))
    lines.append(txt_row('Credential rotation = Periodic renewal of data source service account passwords and API keys per'))
    lines.append(txt_row('Role-based access = RBAC model limiting which data sources and features each user role can access'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-networks-troubleshooting',
    'docs/virtualization/vmware/aria-operations-for-networks/troubleshooting/index.md',
    'Aria Networks Troubleshooting — flow gaps, path analysis errors, collector offline',
)
def aria_networks_troubleshooting():
    """Aria Networks Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria Networks — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Collector offline and not collecting data; missing flow data gaps in platform analytics')))
    lines.append(R(bMid(IV_L, IV_R, 'Path trace errors for connectivity troubleshooting; NSX data source stale after credential')))
    lines.append(R(bMid(IV_L, IV_R, 'Physical switch collection gaps due to SNMP misconfiguration or firewall blocking SNMP')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert not firing for topology changes; platform UI unresponsive or API returning errors')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: support bundle export from Platform UI; GSS case with logs and API debug output')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues define the triage path · diagnostics isolate data source or platform layer'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Collector offline'),
        bMid(B2_L, B2_R, 'Support bundle'),
        bMid(B3_L, B3_R, 'Bundle export'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Flow data gap'),
        bMid(B2_L, B2_R, 'Collector logs'),
        bMid(B3_L, B3_R, 'GSS case open'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Path trace err'),
        bMid(B2_L, B2_R, 'Data src status'),
        bMid(B3_L, B3_R, 'Cred reset'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NSX src stale'),
        bMid(B2_L, B2_R, 'API debug mode'),
        bMid(B3_L, B3_R, 'TAM escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Phys sw gap'),
        bMid(B2_L, B2_R, 'Flow query dbg'),
        bMid(B3_L, B3_R, 'Version matrix'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert not fire'),
        bMid(B2_L, B2_R, 'SNMP test'),
        bMid(B3_L, B3_R, 'Log collect'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics isolate data source or network layer'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Collector down', 'Coll log file', '/var/log/coll', 'Bundle export', 'Restart coll'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Flow data gap', 'Data src status', '/var/log/platform', 'GSS P1 case', 'Re-auth src'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Path trace err', 'API debug', '/var/log/api', 'TAM escalate', 'Fix routing'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['NSX src stale', 'SNMP test', '/var/log/nsx-ds', 'Cred rotation', 'Re-sync src'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (Platform + Collectors) · RAM DIMMs · Network NICs · NSX/vCenter/switches'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Collector offline      = Collector VM not reachable or service stopped; no data flows to Platform VM'))
    lines.append(txt_row('Flow data gap         = Missing time range in flow analytics; caused by Collector outage or data'))
    lines.append(txt_row('Path trace engine     = Aria Networks component that computes end-to-end path using topology and'))
    lines.append(txt_row('NSX data source       = Configured NSX connection; becomes stale if credentials change without'))
    lines.append(txt_row('SNMP collection       = Physical switch polling via SNMP; gaps caused by cred mismatch or firewall'))
    lines.append(txt_row('Support bundle        = Diagnostic archive generated from Platform UI; contains logs and'))
    lines.append(txt_row('API debug mode        = Verbose logging mode for REST API requests; helps diagnose query and auth'))
    lines.append(txt_row('Data source re-authentication = Process of re-entering credentials for a stale NSX/vCenter data'))
    lines.append(txt_row('Platform restart      = Service or VM restart of the Platform appliance to recover from unresponsive'))
    lines.append(txt_row('Credential rotation   = Update of service account passwords requiring re-auth of all affected data'))
    lines.append(txt_row('Version compatibility  = Aria Networks to NSX/vCenter version matrix; mismatch can cause collection'))
    lines.append(txt_row('Stale topology        = Outdated network map caused by data source not syncing; resolve by'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-lcm-architecture',
    'docs/virtualization/vmware/aria-suite-lifecycle/architecture/index.md',
    'Aria LCM Architecture — LCM appliance, Locker, cert manager, product registry',
)
def aria_lcm_architecture():
    """Aria LCM Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria LCM — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Suite Lifecycle (formerly vRealize Suite LCM) = LCM appliance with embedded vIDM identity')))
    lines.append(R(bMid(IV_L, IV_R, 'Manages lifecycle of Aria products (vRA/vROps/vRLI/vRNI) grouped into named Environments')))
    lines.append(R(bMid(IV_L, IV_R, 'Password Locker stores and encrypts credentials at rest; Certificate Locker manages product')))
    lines.append(R(bMid(IV_L, IV_R, 'Install/upgrade wizard orchestrates product deployment order and pre-check validation')))
    lines.append(R(bMid(IV_L, IV_R, 'DR replication between LCM instances; My VMware integration for product binary downloads')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines LCM appliance role · integrations connect identity and deployment targets'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LCM appliance'),
        bMid(B2_L, B2_R, 'WS1/vIDM SSO'),
        bMid(B3_L, B3_R, 'LCM sizing 4vCPU'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Environments'),
        bMid(B2_L, B2_R, 'vCenter deploy tgt'),
        bMid(B3_L, B3_R, 'Env naming std'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Password Locker'),
        bMid(B2_L, B2_R, 'My VMware DL'),
        bMid(B3_L, B3_R, 'Pwd Locker policy'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert Locker'),
        bMid(B2_L, B2_R, 'LDAP directory'),
        bMid(B3_L, B3_R, 'Cert Locker std'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Install/upgrade'),
        bMid(B2_L, B2_R, 'NSX placement'),
        bMid(B3_L, B3_R, 'Product compat'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'DR replication'),
        bMid(B2_L, B2_R, 'NTP/DNS config'),
        bMid(B3_L, B3_R, 'DR replication'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers LCM appliance and Lockers · integrations connect identity and vCenter'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LCM appliance', 'vIDM/WS1 SSO', 'LCM sizing', 'Single LCM', 'Env naming'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Environments', 'vCenter deploy', 'Env naming', 'DR pair', 'Pwd policy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Password Locker', 'My VMware DL', 'Cert policy', 'Multi-env', 'Compat matrix'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cert Locker', 'LDAP directory', 'DR replica', 'Enterprise', 'Locker std'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VM (LCM appliance) · RAM DIMMs · Network NICs · vCenter (deployment target) · Identity provider'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('LCM appliance     = Aria Suite Lifecycle virtual appliance; central orchestrator for all Aria'))
    lines.append(txt_row('Environment       = Logical grouping in LCM containing related Aria products sharing the same vIDM'))
    lines.append(txt_row('Password Locker   = Encrypted credential store in LCM; holds passwords for all products and'))
    lines.append(txt_row('Certificate Locker = LCM certificate store; manages TLS certs for Aria products; supports CA-signed'))
    lines.append(txt_row('vIDM (Identity Manager) = Embedded identity provider in LCM; provides SSO across all managed Aria'))
    lines.append(txt_row('Product BOM       = Bill of Materials; version matrix listing compatible Aria product versions per'))
    lines.append(txt_row('Install wizard    = LCM UI workflow for deploying a new Aria product into an existing Environment'))
    lines.append(txt_row('Upgrade wizard    = LCM UI workflow for upgrading Aria products in dependency order with pre-check'))
    lines.append(txt_row('Day-2 operations  = Post-install operations in LCM: cert rotation, password rotation, content'))
    lines.append(txt_row('DR replication    = LCM appliance replication to a secondary site for disaster recovery failover'))
    lines.append(txt_row('My VMware         = Broadcom/VMware portal integration; LCM downloads product binaries directly from'))
    lines.append(txt_row('Workspace ONE     = VMware identity and access management platform; can replace embedded vIDM in LCM'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-lcm-operations',
    'docs/virtualization/vmware/aria-suite-lifecycle/operations/index.md',
    'Aria LCM Operations — product deploy/upgrade, binary sync, cert rotation, Locker',
)
def aria_lcm_operations():
    """Aria LCM Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria LCM — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Environment health dashboard for all Aria products; upgrade wizard for orchestrated upgrades')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate rotation via Certificate Locker; password rotation via Password Locker workflows')))
    lines.append(R(bMid(IV_L, IV_R, 'Content management for environments; request monitoring for all LCM background jobs')))
    lines.append(R(bMid(IV_L, IV_R, 'Upgrade wizard validates BOM compatibility and runs pre-checks before any product upgrade')))
    lines.append(R(bMid(IV_L, IV_R, 'LCM REST API for day-2 automation; vIDM integration API for identity and SSO management')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops monitor all Aria products · lifecycle wizard orchestrates upgrades'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Env health dash'),
        bMid(B2_L, B2_R, 'Upgrade wizard'),
        bMid(B3_L, B3_R, 'LCM REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Product versions'),
        bMid(B2_L, B2_R, 'Pre-chk validate'),
        bMid(B3_L, B3_R, 'Day-2 actions'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert expiry'),
        bMid(B2_L, B2_R, 'BOM compat chk'),
        bMid(B3_L, B3_R, 'Cert API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Request status'),
        bMid(B2_L, B2_R, 'Product upg order'),
        bMid(B3_L, B3_R, 'Pwd Locker API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Locker inventory'),
        bMid(B2_L, B2_R, 'Post-upg val'),
        bMid(B3_L, B3_R, 'Content mgmt'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Download catalog'),
        bMid(B2_L, B2_R, 'Cert rotation'),
        bMid(B3_L, B3_R, 'vIDM intg API'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch cert expiry and version drift · upgrade wizard enforces order'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LCM REST API', 'Env: healthy', 'Cert rotation', 'Upgrade wizard', 'Config export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Day-2 API', 'Products: ok', 'Pwd rotation', 'Pre-chk run', 'Locker backup'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cert API', 'Certs: valid', 'Add product', 'BOM compat', 'Restore LCM'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Pwd Locker API', 'Downloads ok', 'Env snapshot', 'Post-upg val', 'DR failover'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VM (LCM appliance) · RAM DIMMs · Network NICs · vCenter (deploy target) · Internet (My VMware)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Upgrade wizard    = LCM UI workflow that orchestrates Aria product upgrades in correct dependency'))
    lines.append(txt_row('Pre-check validation = Automated checks run before upgrade; verifies disk space, connectivity, and'))
    lines.append(txt_row('Certificate Locker = LCM component for managing TLS certificates; used for cert rotation workflows'))
    lines.append(txt_row('Password Locker   = LCM encrypted credential store; used for password rotation day-2 operations'))
    lines.append(txt_row('BOM compatibility = Verification that all Aria products in an Environment are on a supported version'))
    lines.append(txt_row('Day-2 operations  = Post-install LCM tasks: cert rotation, password rotation, environment snapshots'))
    lines.append(txt_row('Environment health = Dashboard view showing status of all Aria products in each LCM Environment'))
    lines.append(txt_row('Product version   = Currently installed Aria product version tracked by LCM in each Environment'))
    lines.append(txt_row('Request monitoring = LCM job tracker for all background operations; shows progress and error details'))
    lines.append(txt_row('DR replication    = LCM configuration backup replicated to DR site for failover capability'))
    lines.append(txt_row('Content management = LCM workflow for managing Aria Automation content packs and blueprints'))
    lines.append(txt_row('LCM REST API      = REST API for automating LCM day-2 operations: cert rotation, upgrades, locker'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-lcm-security',
    'docs/virtualization/vmware/aria-suite-lifecycle/security/index.md',
    'Aria LCM Security — vIDM SSO, RBAC, Locker vault, TLS, audit log',
)
def aria_lcm_security():
    """Aria LCM Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria LCM — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'vIDM/Workspace ONE for SSO; environment-level RBAC (admin/operator/viewer) for LCM access')))
    lines.append(R(bMid(IV_L, IV_R, 'Password Locker encrypts credentials at rest; Certificate Locker manages product TLS certs')))
    lines.append(R(bMid(IV_L, IV_R, 'All API over HTTPS; audit log for all LCM operations including Locker access and upgrades')))
    lines.append(R(bMid(IV_L, IV_R, 'Break-glass local admin account; session timeout enforcement; API key with TTL policy')))
    lines.append(R(bMid(IV_L, IV_R, 'Least privilege: operator role limited to day-2 tasks; viewer role read-only for dashboards')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication gates LCM access · RBAC scopes environment permissions'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vIDM/WS1 SSO'),
        bMid(B2_L, B2_R, 'LCM admin role'),
        bMid(B3_L, B3_R, 'LCM TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LDAP/AD auth'),
        bMid(B2_L, B2_R, 'Operator role'),
        bMid(B3_L, B3_R, 'Locker encr at rest'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Local admin'),
        bMid(B2_L, B2_R, 'Viewer role'),
        bMid(B3_L, B3_R, 'vIDM TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LCM API key'),
        bMid(B2_L, B2_R, 'Env-level acc'),
        bMid(B3_L, B3_R, 'Cert management'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Break-glass'),
        bMid(B2_L, B2_R, 'Locker read/write'),
        bMid(B3_L, B3_R, 'HTTPS only API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Session timeout'),
        bMid(B2_L, B2_R, 'Request approve'),
        bMid(B3_L, B3_R, 'Log encryption'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth gates LCM access · RBAC scopes per-environment permissions'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vIDM/WS1', 'Admin role', 'TLS enforced', 'Cert rotation', 'LCM event log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LDAP/AD', 'Operator role', 'Locker encr', 'API key TTL', 'Request log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['API keys', 'Viewer role', 'vIDM TLS', 'Session timeout', 'Cert changes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Break-glass', 'Env access', 'HTTPS only', 'Min permissions', 'Role audit'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VM (LCM appliance) · RAM DIMMs · Network NICs · Identity provider (vIDM/AD) · CA infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vIDM              = VMware Identity Manager embedded in LCM; provides SSO across all managed Aria'))
    lines.append(txt_row('Workspace ONE     = VMware identity platform; alternative to embedded vIDM for enterprise SSO'))
    lines.append(txt_row('LCM RBAC          = Role-based access control in LCM; scoped per Environment; admin/operator/viewer'))
    lines.append(txt_row('Admin role        = Full LCM access; can install/upgrade products, manage Lockers, and configure'))
    lines.append(txt_row('Operator role     = Day-2 access in LCM; can run cert/password rotation and monitoring; no install'))
    lines.append(txt_row('Viewer role       = Read-only LCM access; can view Environment health and Locker inventory; no write'))
    lines.append(txt_row('Password Locker encryption = AES encryption of all credentials stored in LCM Password Locker at rest'))
    lines.append(txt_row('Certificate Locker = LCM store for TLS certificates; supports rotation workflows and CA-signed cert'))
    lines.append(txt_row('API key           = Bearer token for LCM REST API access; subject to TTL and minimum privilege policy'))
    lines.append(txt_row('HTTPS enforcement = All LCM API and UI traffic requires TLS; HTTP redirected or blocked by policy'))
    lines.append(txt_row('Session timeout   = LCM UI session automatically expires after idle period; configurable per'))
    lines.append(txt_row('Audit event log   = LCM audit trail recording all user actions: logins, upgrades, Locker access,'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'aria-lcm-troubleshooting',
    'docs/virtualization/vmware/aria-suite-lifecycle/troubleshooting/index.md',
    'Aria LCM Troubleshooting — deploy failures, binary sync, cert issues, support bundle',
)
def aria_lcm_troubleshooting():
    """Aria LCM Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Aria LCM — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Environment install failures; upgrade stall mid-way through product deployment sequence')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate mismatch between LCM and managed products; vIDM connectivity issues for SSO')))
    lines.append(R(bMid(IV_L, IV_R, 'Disk space on LCM appliance blocking upgrades; API errors for day-2 operations')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnostics: LCM UI request logs, /var/log/vlcm, vIDM diagnostics, REST API debug mode')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: LCM support bundle export from UI; pre-check report; TAM escalation for P1')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues define the triage path · diagnostics isolate LCM or product layer'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Env install fail'),
        bMid(B2_L, B2_R, 'LCM UI req logs'),
        bMid(B3_L, B3_R, 'LCM support bndl'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Upgrade stall'),
        bMid(B2_L, B2_R, '/var/log/vlcm'),
        bMid(B3_L, B3_R, 'GSS case open'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert mismatch'),
        bMid(B2_L, B2_R, 'vIDM diagnostics'),
        bMid(B3_L, B3_R, 'Pre-chk report'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vIDM offline'),
        bMid(B2_L, B2_R, 'REST API debug'),
        bMid(B3_L, B3_R, 'TAM escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Disk space'),
        bMid(B2_L, B2_R, 'Pre-chk output'),
        bMid(B3_L, B3_R, 'Version matrix'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'API errors'),
        bMid(B2_L, B2_R, 'Product logs'),
        bMid(B3_L, B3_R, 'Log export'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics use LCM logs and pre-check output'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Install fail', 'LCM UI logs', '/var/log/vlcm', 'LCM bundle', 'Retry install'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Upgrade stall', 'REST API debug', '/var/log/vra', 'GSS P1 case', 'Resume upg'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cert mismatch', 'Pre-chk output', '/var/log/vro', 'TAM escalate', 'Re-issue cert'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vIDM offline', 'vIDM diag', '/var/log/vidm', 'Version matrix', 'Restart vIDM'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VM (LCM appliance) · RAM DIMMs · Network NICs · vCenter · vIDM/Workspace ONE'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Environment installation = LCM workflow deploying Aria products into a new or existing named'))
    lines.append(txt_row('Upgrade orchestration = LCM upgrade wizard that sequences product upgrades to maintain compatibility'))
    lines.append(txt_row('Certificate mismatch  = TLS cert on LCM or product does not match expected CA or SAN; causes auth'))
    lines.append(txt_row('vIDM connectivity     = LCM requires vIDM to be reachable for SSO; vIDM failure breaks all product'))
    lines.append(txt_row('Disk space threshold  = LCM appliance disk usage limit; upgrade aborts if insufficient space detected'))
    lines.append(txt_row('Pre-check validation  = Automated checks before install/upgrade; catches misconfig before deployment'))
    lines.append(txt_row('LCM support bundle    = Diagnostic archive from LCM UI; contains vlcm logs and request history for'))
    lines.append(txt_row('Day-2 operation       = Post-install LCM task such as cert rotation, password rotation, or content'))
    lines.append(txt_row('API debug             = Verbose REST API logging mode in LCM; shows detailed request and response'))
    lines.append(txt_row('BOM version mismatch  = Aria products in an Environment on incompatible versions; blocks LCM upgrade'))
    lines.append(txt_row('TAM escalation        = Escalation to Technical Account Manager for critical LCM P1 upgrade or'))
    lines.append(txt_row('Product log collection = Gathering logs from individual Aria products (vRA/vROps/vRLI) to diagnose'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-architecture',
    'docs/virtualization/vmware/horizon/architecture/index.md',
    'Horizon Architecture — Connection Server, UAG, Blast/PCoIP, App Volumes, DEM, pools',
)
def horizon_architecture():
    """Horizon Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Horizon — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Horizon = Connection Servers (HA pair+) + Unified Access Gateway (UAG) in DMZ')))
    lines.append(R(bMid(IV_L, IV_R, 'Desktop pools: instant clone (fast refresh) or full clone; RDS for published applications')))
    lines.append(R(bMid(IV_L, IV_R, 'App Volumes delivers applications on-demand; Dynamic Environment Manager controls user settings')))
    lines.append(R(bMid(IV_L, IV_R, 'UAG in DMZ proxies Blast Extreme and PCoIP protocols; Connection Server authenticates users')))
    lines.append(R(bMid(IV_L, IV_R, 'vGPU (NVIDIA) profiles attached to pools for 3D/graphics workloads; vCenter manages ESXi pools')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines broker and pool mechanics · integrations connect directory and vCenter'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Connection Server HA'),
        bMid(B2_L, B2_R, 'vCenter/ESXi pools'),
        bMid(B3_L, B3_R, '≥2 CS per pod'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'UAG: DMZ proxy'),
        bMid(B2_L, B2_R, 'Active Directory'),
        bMid(B3_L, B3_R, 'UAG in DMZ'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Desktop pools'),
        bMid(B2_L, B2_R, 'WS1 Access SSO'),
        bMid(B3_L, B3_R, 'vGPU profile size'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RDS: pub apps'),
        bMid(B2_L, B2_R, 'NSX microseg'),
        bMid(B3_L, B3_R, 'Pool quota'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'App Volumes'),
        bMid(B2_L, B2_R, 'vGPU (NVIDIA)'),
        bMid(B3_L, B3_R, 'Image mgmt std'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Dyn Env Mgr'),
        bMid(B2_L, B2_R, 'Horizon Cloud'),
        bMid(B3_L, B3_R, 'RDS session lim'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers broker and pools · integrations connect vCenter and directory'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Connection Svr', 'vCenter pools', '≥2 CS per pod', 'Single pod', 'CS sizing'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['UAG reverse proxy', 'Active Directory', 'UAG in DMZ', 'Multi-pod', 'Pool quota'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Instant clone', 'WS1 Access', 'vGPU profiles', 'Cloud pod', 'Image std'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['App Volumes', 'NSX microseg', 'RDS limits', 'Enterprise', 'Session limit'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 ESXi hosts · GPU cards (NVIDIA) · RAM DIMMs · Network NICs · UAG appliance VMs · vCenter'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Connection Server  = Horizon broker VM; authenticates users, entitles desktops, manages sessions'))
    lines.append(txt_row('UAG (Unified Access Gateway) = DMZ reverse proxy for Blast/PCoIP; replaces Security Server'))
    lines.append(txt_row('Instant clone      = Desktop provisioning method; child VMs forked from parent snapshot at login'))
    lines.append(txt_row('Full clone         = Independent desktop VM cloned from template; persists independently'))
    lines.append(txt_row('RDS (Remote Desktop Services) = Windows Server role publishing apps or desktops via Horizon'))
    lines.append(txt_row('App Volumes        = On-demand application delivery using AppStacks mounted at login'))
    lines.append(txt_row('Dynamic Environment Manager = Per-user Windows settings and policy management for Horizon desktops'))
    lines.append(txt_row('Blast Extreme      = VMware display protocol; optimized for LAN and WAN; supports H.264/H.265'))
    lines.append(txt_row('PCoIP              = PC-over-IP protocol; Teradici-based display protocol supported by Horizon'))
    lines.append(txt_row('vGPU               = NVIDIA virtual GPU; shared GPU profile assigned to desktop pool VMs'))
    lines.append(txt_row('Cloud Pod Architecture = Horizon feature linking multiple pods for global entitlements across sites'))
    lines.append(txt_row('Entitlement        = Assignment of a user or group to a Horizon desktop or application pool'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-operations',
    'docs/virtualization/vmware/horizon/operations/index.md',
    'Horizon Operations — pod health, pool management, composer recompose, upgrade',
)
def horizon_operations():
    """Horizon Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Horizon — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Connection Server health monitoring; active session count and session management daily')))
    lines.append(R(bMid(IV_L, IV_R, 'Desktop pool provisioning and recompose; image management and push to instant clone pools')))
    lines.append(R(bMid(IV_L, IV_R, 'App Volumes assignment per user or group; log review and event DB monitoring for errors')))
    lines.append(R(bMid(IV_L, IV_R, 'Lifecycle: upgrade Connection Server first, then UAG, then push agent via pool recompose')))
    lines.append(R(bMid(IV_L, IV_R, 'Automation: PowerCLI Horizon module, REST API, Provisioning API for at-scale pool management')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops track sessions and pool health · lifecycle upgrades CS first'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CS health check'),
        bMid(B2_L, B2_R, 'Horizon upgrades'),
        bMid(B3_L, B3_R, 'PowerCLI Horizon'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Active sessions'),
        bMid(B2_L, B2_R, 'CS upgrade 1st'),
        bMid(B3_L, B3_R, 'REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pool provision'),
        bMid(B2_L, B2_R, 'UAG upgrade'),
        bMid(B3_L, B3_R, 'Provisioning API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Composer status'),
        bMid(B2_L, B2_R, 'Agent via recomp'),
        bMid(B3_L, B3_R, 'Connection API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Image push'),
        bMid(B2_L, B2_R, 'App Vol upgrade'),
        bMid(B3_L, B3_R, 'LDAP query'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Log review'),
        bMid(B2_L, B2_R, 'Add new CS'),
        bMid(B3_L, B3_R, 'Dashboard API'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch session and pool issues · lifecycle upgrades in order'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['REST API', 'CS: running', 'Pool recompose', 'CS upgrade 1st', 'Event DB bkp'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['PowerCLI Hor', 'Sessions: ok', 'Image push', 'UAG upgrade', 'Config export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LDAP query', 'UAG: healthy', 'App Vol assign', 'Agent recomp', 'CS config bk'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Event DB query', 'Pool: ready', 'User reset', 'Post-upg val', 'Restore config'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 ESXi hosts · GPU cards · RAM DIMMs · Network NICs · UAG VMs · vCenter · AD domain'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Connection Server  = Horizon broker; health monitored via vCenter plugin and Horizon Admin console'))
    lines.append(txt_row('UAG                = Unified Access Gateway; DMZ proxy; upgrade after Connection Server upgrade'))
    lines.append(txt_row('Desktop pool       = Group of Horizon desktops provisioned from a parent image or template'))
    lines.append(txt_row('Recompose          = Horizon operation pushing a new parent image to all instant clone pool desktops'))
    lines.append(txt_row('Instant clone      = Pool type where desktops are forked from a live parent VM snapshot'))
    lines.append(txt_row('App Volumes        = Application delivery layer; AppStacks assigned per user, group, or OU'))
    lines.append(txt_row('Dynamic Environment Manager = User environment and settings roaming for Horizon virtual desktops'))
    lines.append(txt_row('vGPU profile       = NVIDIA vGPU slice assigned to a VM; profile determines VRAM allocation'))
    lines.append(txt_row('Event database     = Horizon SQL database logging all session, admin, and provisioning events'))
    lines.append(txt_row('REST API           = Horizon REST API for pool, session, and entitlement management at scale'))
    lines.append(txt_row('Horizon agent      = Software installed in guest OS; communicates with Connection Server'))
    lines.append(txt_row('Image management   = Process of updating parent VM, taking snapshot, and recomposing pool'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-security',
    'docs/virtualization/vmware/horizon/security/index.md',
    'Horizon Security — UAG smart card, AD auth, TLS, RBAC, Blast encryption',
)
def horizon_security():
    """Horizon Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Horizon — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Active Directory authentication; MFA via RSA SecurID/RADIUS or SAML with Workspace ONE')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate management for Connection Servers and UAG; Horizon RBAC for entitlements')))
    lines.append(R(bMid(IV_L, IV_R, 'Blast Extreme and PCoIP traffic encrypted with TLS 1.2+; smart card auth supported')))
    lines.append(R(bMid(IV_L, IV_R, 'UAG performs certificate passthrough; Connection Server validates AD credentials and MFA')))
    lines.append(R(bMid(IV_L, IV_R, 'App Volumes and DEM file encryption; USB policy enforces device restriction per pool')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication gates user access · RBAC controls entitlements'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AD auth primary'),
        bMid(B2_L, B2_R, 'Horizon RBAC'),
        bMid(B3_L, B3_R, 'Blast TLS 1.2+'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RSA/RADIUS MFA'),
        bMid(B2_L, B2_R, 'AD group entitle'),
        bMid(B3_L, B3_R, 'PCoIP TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SAML/WS1 SSO'),
        bMid(B2_L, B2_R, 'Pool permissions'),
        bMid(B3_L, B3_R, 'Cert CS/UAG'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Smart card auth'),
        bMid(B2_L, B2_R, 'Global admin role'),
        bMid(B3_L, B3_R, 'App Vol cert'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert-based auth'),
        bMid(B2_L, B2_R, 'Help desk role'),
        bMid(B3_L, B3_R, 'DEM file encr'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'UAG passthrough'),
        bMid(B2_L, B2_R, 'Audit events'),
        bMid(B3_L, B3_R, 'USB policy'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth controls who connects · access control limits entitlements'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AD auth', 'RBAC entitle', 'Blast TLS', 'Cert rotation', 'CS event log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['RSA MFA', 'Pool access', 'PCoIP TLS', 'MFA enforce', 'Session audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SAML/WS1', 'Admin role', 'CS/UAG cert', 'Smart card', 'UAG access log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Smart card', 'Help desk role', 'App Vol cert', 'Lockout policy', 'Entitle audit'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 ESXi hosts · GPU cards · RAM DIMMs · Network NICs · UAG VMs · RSA/MFA server · AD domain'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Blast Extreme      = VMware display protocol; encrypted with TLS 1.2+; supports H.264 and H.265'))
    lines.append(txt_row('PCoIP              = PC-over-IP display protocol; TLS-encrypted tunnel between client and UAG'))
    lines.append(txt_row('UAG (Unified Access Gateway) = DMZ proxy performing cert passthrough and MFA pre-authentication'))
    lines.append(txt_row('RSA SecurID        = RADIUS-based MFA token server integrated with Connection Server'))
    lines.append(txt_row('SAML               = Security Assertion Markup Language; enables WS1 Access SSO for Horizon'))
    lines.append(txt_row('Smart card auth    = PIV/CAC card authentication via Connection Server or UAG'))
    lines.append(txt_row('Connection Server certificate = TLS cert on CS for Blast/PCoIP and admin UI; must be CA-signed'))
    lines.append(txt_row('Entitlement        = Assignment of AD user or group to a Horizon desktop or application pool'))
    lines.append(txt_row('RBAC               = Role-Based Access Control in Horizon Admin console; admin, helpdesk, auditor'))
    lines.append(txt_row('Help desk role     = Horizon RBAC role allowing session management without pool administration'))
    lines.append(txt_row('DEM (Dynamic Environment Manager) = User settings manager; supports file encryption for profiles'))
    lines.append(txt_row('Session audit      = Horizon event DB records all session start, disconnect, and logoff events'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-troubleshooting',
    'docs/virtualization/vmware/horizon/troubleshooting/index.md',
    'Horizon Troubleshooting — black screen, provisioning errors, UAG, log bundle',
)
def horizon_troubleshooting():
    """Horizon Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Horizon — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Connection Server failures; desktop not starting or stuck in provisioning state')))
    lines.append(R(bMid(IV_L, IV_R, 'Blast/PCoIP protocol latency; session disconnects; pool provisioning errors')))
    lines.append(R(bMid(IV_L, IV_R, 'UAG certificate issues; vGPU driver issues; App Volumes mount failures')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnostics: Horizon events DB, /opt/vmware/hzn logs, UAG admin UI, esxtop for vGPU')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: collect Horizon log bundle and UAG support bundle; open GSS case with TAM')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues define the triage path · diagnostics isolate the layer'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CS fail/down'),
        bMid(B2_L, B2_R, 'Horizon events DB'),
        bMid(B3_L, B3_R, 'Horizon log bndl'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Desktop stuck'),
        bMid(B2_L, B2_R, '/opt/vmware/hzn'),
        bMid(B3_L, B3_R, 'UAG support bndl'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Blast/PCoIP lag'),
        bMid(B2_L, B2_R, 'UAG admin UI'),
        bMid(B3_L, B3_R, 'GSS case open'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Session disconn'),
        bMid(B2_L, B2_R, 'esxtop vGPU'),
        bMid(B3_L, B3_R, 'TAM escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pool prov err'),
        bMid(B2_L, B2_R, 'App Vol log'),
        bMid(B3_L, B3_R, 'Event DB query'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'UAG cert err'),
        bMid(B2_L, B2_R, 'DCT tool'),
        bMid(B3_L, B3_R, 'RCA template'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics pinpoint root cause'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CS down', 'Events DB', '/opt/vmware/hzn', 'Horizon bundle', 'Restart CS'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Desktop stuck', 'UAG admin UI', '/var/log/vmware', 'GSS P1 case', 'Recompose pool'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Blast/PCoIP lag', 'esxtop vGPU', 'UAG /var/log', 'TAM escalate', 'Check MTU/QoS'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Pool prov err', 'DCT tool', 'App Vol logs', 'Event DB query', 'Re-prov pool'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 ESXi hosts · GPU cards · RAM DIMMs · Network NICs · UAG VMs · vCenter · AD domain'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Connection Server  = Horizon broker; if down no new sessions; check Windows service and event log'))
    lines.append(txt_row('UAG                = Unified Access Gateway; cert issues cause client connection failures'))
    lines.append(txt_row('Desktop pool       = Group of desktops; stuck provisioning may indicate snapshot or vCenter error'))
    lines.append(txt_row('Instant clone provisioning = Fork operation from parent VM; fails if parent snapshot is stale'))
    lines.append(txt_row('Blast Extreme      = Display protocol; lag indicates MTU, QoS, or bandwidth constraint'))
    lines.append(txt_row('PCoIP              = Display protocol; session drops often tied to UDP port blockage or MTU'))
    lines.append(txt_row('vGPU               = NVIDIA virtual GPU; driver mismatch causes display or performance failures'))
    lines.append(txt_row('DCT (Desktop Connectivity Tool) = Horizon diagnostic tool for end-to-end session connectivity'))
    lines.append(txt_row('Horizon events database = SQL DB logging all session and admin events; query for error codes'))
    lines.append(txt_row('Recompose          = Operation to push new image to pool desktops; resolves stuck provisioning'))
    lines.append(txt_row('Log bundle         = Horizon diagnostic package collected from Connection Server for GSS'))
    lines.append(txt_row('TAM escalation     = Technical Account Manager escalation for critical production incidents'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'srm-architecture',
    'docs/virtualization/vmware/srm/architecture/index.md',
    'SRM Architecture — site pair, SRA, protection groups, recovery plans, IP customisation',
)
def srm_architecture():
    """SRM Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'SRM — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Site Recovery Manager = SRM server pair (one per site) + protection groups (VM sets)')))
    lines.append(R(bMid(IV_L, IV_R, 'Recovery plans are ordered runbooks: test / planned migration / failover workflows')))
    lines.append(R(bMid(IV_L, IV_R, 'Uses vSphere Replication or array-based replication for data movement between sites')))
    lines.append(R(bMid(IV_L, IV_R, 'Inventory mappings connect protected site resources to recovery site equivalents')))
    lines.append(R(bMid(IV_L, IV_R, 'NSX network remapping automates IP customization during failover or planned migration')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines replication and runbooks · integrations connect vCenter and storage'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SRM server pair'),
        bMid(B2_L, B2_R, 'vCenter pair sites'),
        bMid(B3_L, B3_R, 'RTO/RPO per VM'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Protection groups'),
        bMid(B2_L, B2_R, 'NSX: net remap'),
        bMid(B3_L, B3_R, 'PG granularity'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Recovery plans'),
        bMid(B2_L, B2_R, 'vSAN+SAN replic'),
        bMid(B3_L, B3_R, 'Net mapping'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Test failover'),
        bMid(B2_L, B2_R, 'AD auth'),
        bMid(B3_L, B3_R, 'DS mapping'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Planned migration'),
        bMid(B2_L, B2_R, 'Aria Ops monitor'),
        bMid(B3_L, B3_R, 'IP customization'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Inventory maps'),
        bMid(B2_L, B2_R, 'Array API'),
        bMid(B3_L, B3_R, 'Test schedule'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers replication and recovery plans · integrations connect sites'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SRM server pair', 'vCenter pair', 'RTO/RPO tiers', '2-site setup', 'PG naming'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Protection grps', 'NSX net remap', 'PG granularity', 'Bi-directional', 'RPO policy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Recovery plans', 'vSAN/SAN replic', 'Net mapping', 'Active-passive', 'IP custom std'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Test failover', 'Array API', 'IP customization', 'Active-active', 'Test schedule'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 servers (SRM VMs both sites) · Shared storage or vSAN · Network uplinks · WAN/DCI link'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRM server         = Site Recovery Manager appliance; one per site; paired across protected and'))
    lines.append(txt_row('Protection group   = Logical set of VMs grouped for replication and recovery together'))
    lines.append(txt_row('Recovery plan      = Ordered runbook of steps executed during test, migration, or failover'))
    lines.append(txt_row('Test failover      = Non-disruptive recovery validation in an isolated network; production unaffected'))
    lines.append(txt_row('Planned migration  = Controlled workload move from protected to recovery site; no data loss'))
    lines.append(txt_row('Failover           = Emergency activation of recovery site after protected site failure'))
    lines.append(txt_row('Reprotect          = Reverses replication direction after failover to enable failback'))
    lines.append(txt_row('Inventory mapping  = Maps protected site resource (network, folder, pool) to recovery site equivalent'))
    lines.append(txt_row('Network mapping    = SRM mapping of protected site port group to recovery site port group'))
    lines.append(txt_row('Datastore mapping  = Maps protected datastore to recovery site datastore for VM registration'))
    lines.append(txt_row('IP customization   = SRM rules that change VM IP/gateway/DNS during failover to recovery network'))
    lines.append(txt_row('RPO (Recovery Point Objective) = Maximum acceptable data loss; drives replication frequency'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'srm-operations',
    'docs/virtualization/vmware/srm/operations/index.md',
    'SRM Operations — test failover, planned migration, reprotect, failback, upgrade',
)
def srm_operations():
    """SRM Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'SRM — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Replication status and RPO compliance monitoring; protection group health checks daily')))
    lines.append(R(bMid(IV_L, IV_R, 'Test failover on schedule; recovery plan validation; planned migration for maintenance')))
    lines.append(R(bMid(IV_L, IV_R, 'Reprotect after failover to restore replication in reverse direction for failback')))
    lines.append(R(bMid(IV_L, IV_R, 'Lifecycle: upgrade SRM on both sites; run pre-checks; validate partner compatibility')))
    lines.append(R(bMid(IV_L, IV_R, 'Automation: SRM REST API, PowerCLI SRM, PG API, Recovery plan API for at-scale ops')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops monitor RPO and PG health · lifecycle upgrades both sites'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Replication status'),
        bMid(B2_L, B2_R, 'SRM upgrades both'),
        bMid(B3_L, B3_R, 'SRM REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RPO compliance'),
        bMid(B2_L, B2_R, 'Appliance mode'),
        bMid(B3_L, B3_R, 'PowerCLI SRM'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'PG health'),
        bMid(B2_L, B2_R, 'Pre-check run'),
        bMid(B3_L, B3_R, 'PG API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Recovery plan'),
        bMid(B2_L, B2_R, 'Partner compat'),
        bMid(B3_L, B3_R, 'Recovery plan API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Test schedule'),
        bMid(B2_L, B2_R, 'Test post-upg'),
        bMid(B3_L, B3_R, 'Test API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert review'),
        bMid(B2_L, B2_R, 'HBCR agent upg'),
        bMid(B3_L, B3_R, 'Inventory map API'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch RPO breaches early · lifecycle upgrades both sites together'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SRM REST API', 'Replic: ok', 'Test failover', 'SRM upg both', 'SRM config bk'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['PowerCLI SRM', 'RPO: compliant', 'Planned migr', 'HBCR upg', 'Recovery plan'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['PG API', 'PG: healthy', 'Reprotect', 'Pre-check run', 'Mapping backup'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Recovery API', 'Test: passed', 'IP custom', 'Post-upg val', 'Restore config'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 servers (SRM VMs both sites) · vSAN/SAN storage · WAN/DCI link · Network connectivity'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Protection group   = Set of VMs replicated and recovered together; health monitored daily'))
    lines.append(txt_row('Recovery plan      = Ordered runbook; validated by test failover before a real event'))
    lines.append(txt_row('Test failover      = Isolated recovery validation; confirms plan works without impacting production'))
    lines.append(txt_row('Planned migration  = Zero-RPO controlled site move for scheduled maintenance or evacuation'))
    lines.append(txt_row('Failover           = Emergency activation of recovery site; may have data loss up to RPO'))
    lines.append(txt_row('Reprotect          = Post-failover operation that reverses replication to enable failback'))
    lines.append(txt_row('RPO compliance     = Monitoring that replication lag stays within the configured RPO threshold'))
    lines.append(txt_row('HBCR (Host-Based Changed Block Replication) = vSphere Replication agent on ESXi hosts'))
    lines.append(txt_row('SRM REST API       = REST interface for automating protection group and recovery plan operations'))
    lines.append(txt_row('PowerCLI SRM       = PowerShell cmdlets for SRM automation: plan execution, PG management'))
    lines.append(txt_row('Inventory mapping  = Config object linking protected site resources to recovery site equivalents'))
    lines.append(txt_row('Partner site       = The paired remote site in an SRM configuration; protected or recovery role'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'srm-security',
    'docs/virtualization/vmware/srm/security/index.md',
    'SRM Security — vCenter SSO, RBAC, TLS site pair, SRA authentication, audit',
)
def srm_security():
    """SRM Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'SRM — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'vCenter SSO for SRM authentication; site pair credentials for cross-site trust')))
    lines.append(R(bMid(IV_L, IV_R, 'RBAC roles: admin / recovery execute / test operator / read-only for least privilege')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate management for SRM servers; array replication auth; audit log for all ops')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication traffic encrypted with TLS; vSAN encryption at rest for DR datastores')))
    lines.append(R(bMid(IV_L, IV_R, 'Test isolation network prevents recovery test VMs from reaching production systems')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication controls SRM access · RBAC scopes recovery roles'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vCenter SSO auth'),
        bMid(B2_L, B2_R, 'SRM admin: full'),
        bMid(B3_L, B3_R, 'Replic TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AD integration'),
        bMid(B2_L, B2_R, 'Recovery exec'),
        bMid(B3_L, B3_R, 'Array replic auth'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SRM admin role'),
        bMid(B2_L, B2_R, 'Test exec only'),
        bMid(B3_L, B3_R, 'SRM cert mgmt'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Site pair creds'),
        bMid(B2_L, B2_R, 'Read-only audit'),
        bMid(B3_L, B3_R, 'Test isolation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Array creds'),
        bMid(B2_L, B2_R, 'Custom roles'),
        bMid(B3_L, B3_R, 'vSAN encr DR'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert management'),
        bMid(B2_L, B2_R, 'vCenter RBAC'),
        bMid(B3_L, B3_R, 'Audit log TLS'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth controls who uses SRM · RBAC limits recovery execution'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vCenter SSO', 'SRM admin', 'Replic TLS', 'Cert rotation', 'Recovery audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AD integration', 'Recovery exec', 'Array auth', 'Site pair cert', 'Test log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Site pair creds', 'Test exec', 'SRM cert', 'Least privilege', 'Plan changes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Array creds', 'Read-only', 'vSAN encr', 'Isolation net', 'GSS audit trail'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 servers (SRM VMs both sites) · vSAN/SAN · WAN link · AD domain · CA infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vCenter SSO        = Single Sign-On; SRM authenticates all users via vCenter SSO domain'))
    lines.append(txt_row('Site pair          = Trusted connection between two SRM servers across protected and recovery sites'))
    lines.append(txt_row('Array-based replication = Storage array replicates LUNs/volumes; SRM integrates via SRA adapter'))
    lines.append(txt_row('vSphere Replication = Host-based replication using HBCR agent; RPO minimum 5 minutes'))
    lines.append(txt_row('SRM RBAC           = Role-Based Access Control in SRM; roles: admin, recovery exec, test, read-only'))
    lines.append(txt_row('Recovery admin     = SRM role with full recovery plan and protection group management'))
    lines.append(txt_row('Recovery user      = SRM role that can execute recovery plans but not modify them'))
    lines.append(txt_row('Test operator      = SRM role that can run test failovers only; cannot run real failover'))
    lines.append(txt_row('Certificate management = SRM server TLS cert lifecycle; must be CA-signed for site pair trust'))
    lines.append(txt_row('Audit log          = SRM records all recovery, test, reprotect, and admin operations'))
    lines.append(txt_row('Test isolation network = Isolated port group used during test failover; blocks production access'))
    lines.append(txt_row('Least privilege    = Principle of assigning minimum SRM role needed for each operator function'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'srm-troubleshooting',
    'docs/virtualization/vmware/srm/troubleshooting/index.md',
    'SRM Troubleshooting — site pair failure, plan errors, replication issues, log bundle',
)
def srm_troubleshooting():
    """SRM Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'SRM — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Site pair connectivity failures; replication lag and RPO breaches; PG config errors')))
    lines.append(R(bMid(IV_L, IV_R, 'Recovery plan execution failures; array API connectivity issues; HBCR agent failures')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnostics: SRM log files, VR appliance log, array API test, RPO dashboard review')))
    lines.append(R(bMid(IV_L, IV_R, 'Recovery plan test identifies misconfigurations before a real failover event occurs')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: collect SRM bundles from both sites; engage array vendor; contact TAM for P1')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues define triage path · diagnostics isolate replication or plan layer'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Site pair conn'),
        bMid(B2_L, B2_R, 'SRM log files'),
        bMid(B3_L, B3_R, 'SRM bndl both'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Replic lag/RPO'),
        bMid(B2_L, B2_R, 'VR appliance log'),
        bMid(B3_L, B3_R, 'GSS P1 case'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'PG config err'),
        bMid(B2_L, B2_R, 'Array API test'),
        bMid(B3_L, B3_R, 'Both site logs'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Recovery plan fail'),
        bMid(B2_L, B2_R, 'Recovery plan test'),
        bMid(B3_L, B3_R, 'Array vendor esc'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Array API err'),
        bMid(B2_L, B2_R, 'RPO dashboard'),
        bMid(B3_L, B3_R, 'TAM contact'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'HBCR agent fail'),
        bMid(B2_L, B2_R, 'Support bundle'),
        bMid(B3_L, B3_R, 'P1 process'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics use logs and RPO dashboard'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Site pair fail', 'SRM log files', '/var/log/vmware/srm', 'SRM bundle', 'Re-pair sites'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Replic lag', 'RPO dashboard', 'VR app /logs', 'GSS P1 case', 'Resync data'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['PG config err', 'Recovery test', '/var/log/hms', 'Array vendor', 'Fix PG config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Recovery fail', 'Array API test', '/var/log/vr', 'TAM contact', 'Plan dry run'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 servers (both sites) · vSAN/SAN · WAN/DCI link · Array storage · AD domain'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Site pair          = Trusted link between SRM servers; failure blocks all SRM operations cross-site'))
    lines.append(txt_row('RPO breach         = Replication lag exceeds configured RPO threshold; alerts in SRM dashboard'))
    lines.append(txt_row('Protection group   = VM set in SRM; config error prevents inclusion in recovery plans'))
    lines.append(txt_row('Recovery plan      = Ordered failover runbook; execution failures logged with step-level detail'))
    lines.append(txt_row('HBCR agent         = Host-Based Changed Block Replication agent; failure stops vSphere Replication'))
    lines.append(txt_row('Array-based replication = Array LUN replication via SRA; API errors block SRM inventory sync'))
    lines.append(txt_row('SRM support bundle = Log package from SRM appliance; collected from both sites for GSS cases'))
    lines.append(txt_row('VR appliance log   = vSphere Replication appliance logs; diagnose HBCR and replication failures'))
    lines.append(txt_row('TAM escalation     = Technical Account Manager escalation for P1 DR incidents'))
    lines.append(txt_row('Test failover      = Non-disruptive test; use to validate plan config before real event'))
    lines.append(txt_row('Reprotect          = Post-failover step; reverses replication; required before failback'))
    lines.append(txt_row('Recovery time      = Actual elapsed time of recovery plan execution; compare against RTO target'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'tanzu-architecture',
    'docs/virtualization/vmware/tanzu/architecture/index.md',
    'Tanzu Architecture — Supervisor Cluster, TKGs/TKGm, Cluster API, NSX-T, Harbor, TMC',
)
def tanzu_architecture():
    """Tanzu Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VMware Tanzu — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Tanzu portfolio: TKGs (Supervisor Cluster on vSphere) + TKGm (standalone management cluster)')))
    lines.append(R(bMid(IV_L, IV_R, 'Supervisor Cluster: vSphere control plane enabling Kubernetes namespaces on ESXi hosts')))
    lines.append(R(bMid(IV_L, IV_R, 'Workload clusters: Tanzu Kubernetes clusters provisioned via Cluster API on vSphere')))
    lines.append(R(bMid(IV_L, IV_R, 'NSX-T or VDS networking: pod networking, load balancing via NSX Advanced LB (Avi)')))
    lines.append(R(bMid(IV_L, IV_R, 'Tanzu Mission Control: multi-cluster governance, policy, and lifecycle management plane')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines supervisor and workload clusters · integrations connect NSX and storage'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Supervisor cluster'),
        bMid(B2_L, B2_R, 'NSX-T networking'),
        bMid(B3_L, B3_R, 'Namespace sizing'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Workload clusters'),
        bMid(B2_L, B2_R, 'Avi load balancer'),
        bMid(B3_L, B3_R, 'Cluster profiles'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSphere namespaces'),
        bMid(B2_L, B2_R, 'vSAN storage'),
        bMid(B3_L, B3_R, 'Image policy'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cluster API'),
        bMid(B2_L, B2_R, 'Harbor registry'),
        bMid(B3_L, B3_R, 'Network config'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'TKG node pools'),
        bMid(B2_L, B2_R, 'TMC governance'),
        bMid(B3_L, B3_R, 'RBAC namespaces'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Control plane HA'),
        bMid(B2_L, B2_R, 'vCenter auth'),
        bMid(B3_L, B3_R, 'Resource quota'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers supervisor + workload clusters · integrations connect NSX and Harbor'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Supervisor cluster', 'NSX-T network', 'Namespace sizing', 'Single cluster', 'Namespace policy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Workload clusters', 'Avi LB', 'Cluster profile', 'HA control plane', 'Image policy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vSphere namespace', 'vSAN storage', 'RBAC namespaces', 'Multi-cluster', 'Quota policy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cluster API', 'Harbor registry', 'Resource quota', 'TMC governed', 'Network config'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ESXi hosts · RAM DIMMs · Network NICs · vSAN or NFS storage · NSX-T or VDS virtual switch fabric'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Supervisor Cluster  = vSphere control plane running Kubernetes API server on ESXi host kernel'))
    lines.append(txt_row('TKGs               = Tanzu Kubernetes Grid Service; provisions workload clusters via Supervisor'))
    lines.append(txt_row('TKGm               = Tanzu Kubernetes Grid multicloud; standalone management cluster on any infra'))
    lines.append(txt_row('vSphere namespace   = Kubernetes namespace mapped to vSphere resource pool, storage policy, and'))
    lines.append(txt_row('Workload cluster   = Tanzu Kubernetes cluster provisioned in a namespace via Cluster API'))
    lines.append(txt_row('Cluster API        = Kubernetes-native API for declarative lifecycle management of workload clusters'))
    lines.append(txt_row('Node pool          = Group of identically sized worker nodes within a Tanzu Kubernetes cluster'))
    lines.append(txt_row('Control plane HA   = 3 control plane nodes per cluster across ESXi hosts for Kubernetes API HA'))
    lines.append(txt_row('Avi Load Balancer  = NSX Advanced LB (Avi); provides L4/L7 load balancing for Tanzu services'))
    lines.append(txt_row('Harbor             = VMware container registry; private image registry integrated with Tanzu'))
    lines.append(txt_row('Tanzu Mission Ctrl = SaaS management plane for multi-cluster policy, RBAC, and lifecycle governance'))
    lines.append(txt_row('Resource quota     = vSphere namespace CPU, memory, storage limits enforced across all cluster'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'tanzu-operations',
    'docs/virtualization/vmware/tanzu/operations/index.md',
    'Tanzu Operations — cluster lifecycle, node pool scaling, upgrade, Harbor, Tanzu CLI',
)
def tanzu_operations():
    """Tanzu Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VMware Tanzu — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Cluster lifecycle: provision, scale, and upgrade workload clusters via kubectl or Tanzu CLI')))
    lines.append(R(bMid(IV_L, IV_R, 'Node pool management: add/remove workers; drain nodes before maintenance operations')))
    lines.append(R(bMid(IV_L, IV_R, 'Supervisor health: check vCenter Workload Management status; validate namespace quotas')))
    lines.append(R(bMid(IV_L, IV_R, 'Image management: scan and promote images in Harbor; enforce OPA/admission policies')))
    lines.append(R(bMid(IV_L, IV_R, 'Tanzu CLI: tanzu cluster create/delete/upgrade/scale; kubeconfig context management')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops manage cluster state · lifecycle upgrades Kubernetes versions'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cluster status'),
        bMid(B2_L, B2_R, 'Cluster upgrade'),
        bMid(B3_L, B3_R, 'Tanzu CLI'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Node pool scale'),
        bMid(B2_L, B2_R, 'K8s version bump'),
        bMid(B3_L, B3_R, 'kubectl apply'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Namespace quotas'),
        bMid(B2_L, B2_R, 'Node drain/cordon'),
        bMid(B3_L, B3_R, 'GitOps pipelines'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Image scanning'),
        bMid(B2_L, B2_R, 'Supervisor upg'),
        bMid(B3_L, B3_R, 'TMC automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Harbor registry'),
        bMid(B2_L, B2_R, 'OVA bundle upg'),
        bMid(B3_L, B3_R, 'Cluster API CR'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'kubeconfig mgmt'),
        bMid(B2_L, B2_R, 'Cert rotation'),
        bMid(B3_L, B3_R, 'Helm deploys'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops check cluster and node health · lifecycle upgrades Kubernetes safely'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['tanzu cluster', 'Cluster: Running', 'Scale workers', 'Cluster upgrade', 'kubeconfig bkp'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['kubectl apply', 'Nodes: Ready', 'Add namespace', 'Supervisor upg', 'ETCD snapshot'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['kubectl drain', 'Quotas: ok', 'Update quota', 'OVA bundle', 'Cluster config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['tanzu login', 'Harbor: healthy', 'Image promote', 'Post-upg val', 'Namespace bkp'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ESXi hosts · RAM DIMMs · Network NICs · vSAN/NFS storage · NSX-T fabric · vCenter appliance'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Tanzu CLI          = kubectl plug-in and tanzu binary for cluster lifecycle and context management'))
    lines.append(txt_row('tanzu cluster      = CLI sub-command for create, scale, upgrade, delete of workload clusters'))
    lines.append(txt_row('Node drain         = kubectl drain removes pods from a node before maintenance or upgrade'))
    lines.append(txt_row('Node pool scaling  = Adding or removing worker VMs in a pool via Cluster API update'))
    lines.append(txt_row('Supervisor upgrade = vCenter-driven update of the Workload Management control plane version'))
    lines.append(txt_row('OVA bundle         = Tanzu node OS image OVA; uploaded to vCenter content library for upgrades'))
    lines.append(txt_row('kubeconfig         = Kubernetes configuration file with cluster endpoint and credentials for kubectl'))
    lines.append(txt_row('Namespace quota    = CPU/memory/storage limits applied to a vSphere namespace; enforced by Supervisor'))
    lines.append(txt_row('Cluster API CR     = Custom Resource defining desired cluster state; reconciled by Cluster API'))
    lines.append(txt_row('GitOps pipeline    = Declarative deployment pipeline applying manifests from git to Kubernetes'))
    lines.append(txt_row('Harbor             = VMware OCI-compatible registry; image scanning and replication built-in'))
    lines.append(txt_row('ETCD snapshot      = Backup of Kubernetes cluster state; taken before any major upgrade operation'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'tanzu-security',
    'docs/virtualization/vmware/tanzu/security/index.md',
    'Tanzu Security — vSphere SSO, RBAC, Pod Security Admission, NSX-T policies, mTLS',
)
def tanzu_security():
    """Tanzu Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VMware Tanzu — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'vSphere SSO and LDAP/AD integration for Kubernetes RBAC; namespace-scoped role bindings')))
    lines.append(R(bMid(IV_L, IV_R, 'Pod Security Admission: enforce Restricted/Baseline/Privileged policies per namespace')))
    lines.append(R(bMid(IV_L, IV_R, 'Network policies via NSX-T: micro-segmentation between pods and namespaces')))
    lines.append(R(bMid(IV_L, IV_R, 'Harbor image scanning: Trivy/Clair CVE scanning; admission webhook rejects vulnerable images')))
    lines.append(R(bMid(IV_L, IV_R, 'mTLS between services via Tanzu Service Mesh (TSM); certificate rotation automated')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication gates cluster access · RBAC scopes namespace permissions'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Workload Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSphere SSO'),
        bMid(B2_L, B2_R, 'RBAC bindings'),
        bMid(B3_L, B3_R, 'Pod Security Adm'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LDAP/AD groups'),
        bMid(B2_L, B2_R, 'Namespace RBAC'),
        bMid(B3_L, B3_R, 'Network policy'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'OIDC provider'),
        bMid(B2_L, B2_R, 'Service accounts'),
        bMid(B3_L, B3_R, 'Image scanning'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'kubeconfig auth'),
        bMid(B2_L, B2_R, 'Cluster roles'),
        bMid(B3_L, B3_R, 'mTLS (TSM)'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert rotation'),
        bMid(B2_L, B2_R, 'OPA/Gatekeeper'),
        bMid(B3_L, B3_R, 'Admission webhook'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Audit logging'),
        bMid(B2_L, B2_R, 'TMC policies'),
        bMid(B3_L, B3_R, 'vSAN encryption'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth controls cluster access · RBAC scopes roles'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Workload Sec', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vSphere SSO', 'RBAC roles', 'Pod Sec Adm', 'CIS k8s bench', 'API audit log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LDAP groups', 'Namespace RBAC', 'Network policy', 'PSA Restricted', 'RBAC changes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['OIDC provider', 'Cluster roles', 'Image scanning', 'Cert rotation', 'Harbor scan log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Service accounts', 'OPA policies', 'mTLS TSM', 'Min-priv SA', 'Admission log'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ESXi hosts · RAM DIMMs · Network NICs · NSX-T fabric · vSAN encryption · CA infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vSphere SSO        = vCenter Single Sign-On; identity source for Kubernetes RBAC in Tanzu'))
    lines.append(txt_row('RBAC               = Kubernetes Role-Based Access Control; ClusterRole/Role bound to users or groups'))
    lines.append(txt_row('Pod Security Adm   = Kubernetes built-in policy enforcing Restricted/Baseline/Privileged per'))
    lines.append(txt_row('Network policy     = Kubernetes resource restricting pod-to-pod traffic; enforced by NSX-T CNI'))
    lines.append(txt_row('OPA/Gatekeeper     = Open Policy Agent admission controller; enforces custom policy constraints'))
    lines.append(txt_row('Admission webhook  = Kubernetes API hook that validates or mutates resources before admission'))
    lines.append(txt_row('Image scanning     = Harbor Trivy/Clair CVE scan; blocks deployment of images above severity'))
    lines.append(txt_row('mTLS               = Mutual TLS between services; provided by Tanzu Service Mesh (Istio-based)'))
    lines.append(txt_row('OIDC               = OpenID Connect; used by Pinniped to federate identity to Kubernetes API server'))
    lines.append(txt_row('Service account    = Kubernetes identity for pods; scoped to namespace; used for API server auth'))
    lines.append(txt_row('vSAN encryption    = Data-at-rest encryption for node disks; uses vCenter Key Provider (KMS)'))
    lines.append(txt_row('Kubernetes audit   = API server audit log capturing all API calls; forwarded to Aria Logs for SIEM'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'tanzu-troubleshooting',
    'docs/virtualization/vmware/tanzu/troubleshooting/index.md',
    'Tanzu Troubleshooting — cluster stuck, node NotReady, WCP degraded, tanzu diagnostics',
)
def tanzu_troubleshooting():
    """Tanzu Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VMware Tanzu — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Cluster creation stuck: check Supervisor status in vCenter; validate NSX-T and storage config')))
    lines.append(R(bMid(IV_L, IV_R, 'Nodes NotReady: check kubelet status on node; verify vSAN/network connectivity from node VM')))
    lines.append(R(bMid(IV_L, IV_R, 'Workload Management degraded: validate vCenter health, vSphere namespace quota, and NTP sync')))
    lines.append(R(bMid(IV_L, IV_R, 'Image pull failures: check Harbor availability; verify imagePullSecret and network policy')))
    lines.append(R(bMid(IV_L, IV_R, 'kubectl logs and describe events are first diagnostic step; tanzu diagnostics collects bundles')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics use kubectl and events · escalation bundles for VMware GSS'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cluster stuck'),
        bMid(B2_L, B2_R, 'kubectl describe'),
        bMid(B3_L, B3_R, 'tanzu diagnostics'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Node NotReady'),
        bMid(B2_L, B2_R, 'kubectl logs'),
        bMid(B3_L, B3_R, 'GSS case'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'WCP degraded'),
        bMid(B2_L, B2_R, 'kubectl events'),
        bMid(B3_L, B3_R, 'Skyline Health'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Image pull fail'),
        bMid(B2_L, B2_R, 'vCenter events'),
        bMid(B3_L, B3_R, 'TAM escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pod pending'),
        bMid(B2_L, B2_R, 'NSX-T logs'),
        bMid(B3_L, B3_R, 'Log bundle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Quota exceeded'),
        bMid(B2_L, B2_R, 'Harbor health'),
        bMid(B3_L, B3_R, 'Version compat'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues triage cluster and node faults · diagnostics use kubectl and vCenter'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cluster stuck', 'kubectl descr', 'vCenter tasks', 'tanzu diagnos', 'Re-provision'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Node NotReady', 'kubectl logs', 'kubelet journal', 'GSS P1 case', 'Drain+replace'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['WCP degraded', 'kubectl events', 'NSX-T manager', 'TAM escalate', 'Restart WCP'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Image pull fail', 'Harbor health', 'Harbor logs', 'Skyline health', 'Update secret'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ESXi hosts · RAM DIMMs · Network NICs · vSAN/NFS storage · NSX-T fabric · vCenter appliance'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Supervisor status  = Workload Management health shown in vCenter UI; Running/Degraded/Error states'))
    lines.append(txt_row('Node NotReady      = Kubernetes node condition when kubelet cannot communicate with API server'))
    lines.append(txt_row('kubelet            = Node agent managing pod lifecycle; check journalctl -u kubelet for errors'))
    lines.append(txt_row('WCP                = Workload Control Plane; VMware internal name for the Supervisor Cluster'))
    lines.append(txt_row('kubectl describe   = Shows detailed state and events for any Kubernetes resource'))
    lines.append(txt_row('kubectl events     = Lists recent events in a namespace; critical for cluster and pod triage'))
    lines.append(txt_row('imagePullSecret    = Kubernetes secret holding registry credentials for pulling private images'))
    lines.append(txt_row('tanzu diagnostics  = CLI command collecting cluster diagnostic bundle for GSS escalation'))
    lines.append(txt_row('Pod Pending        = Pod scheduled but not running; check events for resource or image pull errors'))
    lines.append(txt_row('Quota exceeded     = vSphere namespace CPU/memory/storage limit reached; expand or reclaim resources'))
    lines.append(txt_row('Skyline Health     = VMware proactive support tool validating Tanzu configuration against best'))
    lines.append(txt_row('Cluster API events = Events on TanzuKubernetesCluster CR showing provisioning error details'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsphere-replication-architecture',
    'docs/virtualization/vmware/vsphere-replication/architecture/index.md',
    'vSphere Replication Architecture — VRMS/VRS per site, per-VMDK RPO, SRM integration',
)
def vsphere_replication_architecture():
    """vSphere Replication Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere Replication — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'vSphere Replication (VR): per-VM async replication from source vCenter to target vCenter')))
    lines.append(R(bMid(IV_L, IV_R, 'VR appliance (VRMS) per site; VR server (VRS) handles bulk of replication traffic per site')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication granularity: per-VMDK; RPO configurable from 5 minutes to 24 hours per VM')))
    lines.append(R(bMid(IV_L, IV_R, 'Network compression and encryption of replication traffic; FQDN-resolved endpoints')))
    lines.append(R(bMid(IV_L, IV_R, 'Site Recovery Manager integration: VR seeds VM copies used for SRM orchestrated failover')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines VR appliances · integrations connect SRM · standards govern RPO and sizing'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VRMS per site'),
        bMid(B2_L, B2_R, 'SRM integration'),
        bMid(B3_L, B3_R, 'RPO per VM class'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VRS per site'),
        bMid(B2_L, B2_R, 'vCenter plugin'),
        bMid(B3_L, B3_R, 'Bandwidth sizing'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Per-VMDK rep'),
        bMid(B2_L, B2_R, 'Storage compat'),
        bMid(B3_L, B3_R, 'Encryption on'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RPO 5 min-24 hr'),
        bMid(B2_L, B2_R, 'vSAN as target'),
        bMid(B3_L, B3_R, 'Compression on'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Traffic encrypt'),
        bMid(B2_L, B2_R, 'NFS/VMFS target'),
        bMid(B3_L, B3_R, 'Max VMs per VRS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Delta sync'),
        bMid(B2_L, B2_R, 'Aria Ops intg'),
        bMid(B3_L, B3_R, 'FQDN config'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers VR appliances and RPO · integrations connect SRM and storage'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VRMS per site', 'SRM pairing', 'RPO tiers', 'VRMS deploy', 'RPO per class'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VRS per site', 'vCenter plugin', 'BW planning', 'VRS deploy', 'Encrypt traffic'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Per-VMDK rep', 'vSAN target', 'Compress on', 'Site pairing', 'Max VM/VRS'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Delta sync', 'NFS/VMFS tgt', 'FQDN config', 'Multi-VRS', 'Storage policy'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (VRMS + VRS) · RAM DIMMs · WAN link for replication traffic · Target storage (vSAN/NFS/VMFS)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VRMS               = vSphere Replication Management Server; registers with vCenter; manages'))
    lines.append(txt_row('VRS                = vSphere Replication Server; handles the bulk replication data transfer per site'))
    lines.append(txt_row('Per-VMDK replication = Each virtual disk replicated independently; exclude swap VMDKs to save'))
    lines.append(txt_row('RPO                = Recovery Point Objective; minimum 5 minutes in VR; defines max data loss window'))
    lines.append(txt_row('Delta sync         = Changed block tracking (CBT) used to send only modified blocks each replication'))
    lines.append(txt_row('Site pairing       = vCenter-level trust relationship between source and target VR sites'))
    lines.append(txt_row('Replication target = Datastore on target site where replica VMDK files are stored'))
    lines.append(txt_row('Traffic encryption = TLS-encrypted replication stream between source VRS and target VRS'))
    lines.append(txt_row('Compression        = Network compression of replication data; reduces bandwidth at cost of CPU'))
    lines.append(txt_row('SRM integration    = Site Recovery Manager uses VR as the replication provider for orchestrated'))
    lines.append(txt_row('vSAN target        = vSAN datastore on target site used as replication destination; policy-based'))
    lines.append(txt_row('Changed block track = CBT bitmap tracking written blocks in a VMDK; enables efficient delta'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsphere-replication-operations',
    'docs/virtualization/vmware/vsphere-replication/operations/index.md',
    'vSphere Replication Operations — RPO monitoring, pause/resume, test recovery, upgrade',
)
def vsphere_replication_operations():
    """vSphere Replication Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere Replication — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Monitor replication status for all protected VMs; check RPO compliance and missed sync counts')))
    lines.append(R(bMid(IV_L, IV_R, 'Configure replication: select VM, set RPO, choose target datastore and network compression')))
    lines.append(R(bMid(IV_L, IV_R, 'Pause and resume replication: maintenance window operations; resume to trigger full delta sync')))
    lines.append(R(bMid(IV_L, IV_R, 'Test recovery: recover to isolated test network; validate VM boots at target; revert test')))
    lines.append(R(bMid(IV_L, IV_R, 'Appliance upgrades: upgrade VRMS and VRS before upgrading protected VMs and vCenter hosts')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops monitor RPO compliance · lifecycle upgrades appliances before hosts · automation via SRM'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RPO compliance'),
        bMid(B2_L, B2_R, 'VRMS upgrade'),
        bMid(B3_L, B3_R, 'SRM plans'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Missed sync'),
        bMid(B2_L, B2_R, 'VRS upgrade'),
        bMid(B3_L, B3_R, 'REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Rep health'),
        bMid(B2_L, B2_R, 'Cert rotation'),
        bMid(B3_L, B3_R, 'Aria Ops alerts'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pause/resume'),
        bMid(B2_L, B2_R, 'vCenter upg'),
        bMid(B3_L, B3_R, 'Scheduled test'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Test recovery'),
        bMid(B2_L, B2_R, 'Config backup'),
        bMid(B3_L, B3_R, 'VR API calls'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'BW utilisation'),
        bMid(B2_L, B2_R, 'Post-upg val'),
        bMid(B3_L, B3_R, 'Monitoring API'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops track RPO and sync health · lifecycle upgrades appliances · automation tests and alerts'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VR REST API', 'RPO: met', 'Configure VM', 'VRMS upgrade', 'Config export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vSphere API', 'Sync: ok', 'Pause rep', 'VRS upgrade', 'Rep metadata'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SRM API', 'BW: normal', 'Resume rep', 'Cert rotation', 'Restore config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Aria Ops API', 'Appliance: up', 'Test recovery', 'Post-upg val', 'Site re-pair'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (VRMS + VRS) · RAM DIMMs · WAN link · Target storage array or vSAN · vCenter appliance'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPO compliance     = All replicated VMs meeting their configured RPO within the monitoring window'))
    lines.append(txt_row('Missed sync        = Replication cycle that failed to complete within the RPO window; alerts in'))
    lines.append(txt_row('Pause replication  = Temporarily halting delta sync; all changes accumulate until resumed'))
    lines.append(txt_row('Resume replication = Restarting replication after pause; triggers full delta resync of changed blocks'))
    lines.append(txt_row('Test recovery      = Recovering replica to isolated test network; validates DR readiness without'))
    lines.append(txt_row('Bandwidth usage    = Network throughput consumed by replication; monitored to prevent link saturation'))
    lines.append(txt_row('VRMS upgrade       = OVF/VAMI-based upgrade of the management appliance; must precede VRS upgrade'))
    lines.append(txt_row('VRS upgrade        = Upgrade of the replication server appliance; precedes vCenter and host upgrades'))
    lines.append(txt_row('Configuration backup = Export of VR replication config; used for recovery if appliance rebuild needed'))
    lines.append(txt_row('Site pairing health = vCenter-to-vCenter VR trust relationship; must be green for replication to'))
    lines.append(txt_row('SRM recovery plan  = Orchestrated failover workflow that uses VR replicas as recovery source'))
    lines.append(txt_row('VR REST API        = HTTP API for querying and managing replication config programmatically'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsphere-replication-security',
    'docs/virtualization/vmware/vsphere-replication/security/index.md',
    'vSphere Replication Security — vCenter SSO, RBAC, TLS traffic, cert management, FIPS',
)
def vsphere_replication_security():
    """vSphere Replication Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere Replication — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'vCenter SSO authentication for VR appliance management; RBAC via vCenter roles')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication traffic encrypted over TLS between source VRS and target VRS')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate management: VRMS and VRS certs signed by CA or vCenter CA; rotated on schedule')))
    lines.append(R(bMid(IV_L, IV_R, 'Firewall rules: VRMS port 8043/443, VRS port 31031, vCenter port 443 between sites')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit: all replication config changes logged in vCenter Tasks and Events; syslog forward')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  vCenter SSO gates management · TLS encrypts replication traffic'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vCenter SSO'),
        bMid(B2_L, B2_R, 'vCenter RBAC'),
        bMid(B3_L, B3_R, 'Traffic TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LDAP via vCenter'),
        bMid(B2_L, B2_R, 'Admin role'),
        bMid(B3_L, B3_R, 'Cert management'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VRMS local admin'),
        bMid(B2_L, B2_R, 'Read-only role'),
        bMid(B3_L, B3_R, 'CA-signed certs'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Plugin auth'),
        bMid(B2_L, B2_R, 'Datastore perm'),
        bMid(B3_L, B3_R, 'FIPS mode'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Site trust cert'),
        bMid(B2_L, B2_R, 'Site admin roles'),
        bMid(B3_L, B3_R, 'Compress+encrypt'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VAMI local auth'),
        bMid(B2_L, B2_R, 'Firewall rules'),
        bMid(B3_L, B3_R, 'Audit logging'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  SSO controls management access · RBAC scopes permissions'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vCenter SSO', 'vCenter RBAC', 'Traffic TLS', 'Cert rotation', 'vCenter tasks'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LDAP groups', 'Admin role', 'CA-signed cert', 'Firewall rules', 'Config events'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VRMS local', 'Read-only role', 'FIPS mode', 'Min-perm RBAC', 'Syslog forward'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Site trust cert', 'Firewall scope', 'Compress+enc', 'VAMI hardening', 'Site pair log'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (VRMS + VRS) · RAM DIMMs · WAN firewall · CA infrastructure · vCenter appliance'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vCenter SSO        = Single Sign-On; authenticates admin access to VR plugin within vCenter UI'))
    lines.append(txt_row('RBAC               = Role-Based Access Control; VR uses vCenter roles for permissions scoping'))
    lines.append(txt_row('Admin role         = Full VR management: configure, pause, resume, reconfigure replication'))
    lines.append(txt_row('Read-only role     = View replication status only; cannot configure or modify replication'))
    lines.append(txt_row('Traffic encryption = TLS between source and target VRS; enabled by default; FIPS mode optional'))
    lines.append(txt_row('VRMS certificate   = TLS cert for the VRMS management UI; signed by vCenter CA or external CA'))
    lines.append(txt_row('VRS certificate    = TLS cert for the VRS data path; must be trusted at both source and target sites'))
    lines.append(txt_row('Site trust         = Certificate-based trust between source vCenter and target vCenter for VR pairing'))
    lines.append(txt_row('VAMI               = Virtual Appliance Management Interface; admin UI for VRMS/VRS; secured with'))
    lines.append(txt_row('Firewall rules     = Required: 8043/443 for VRMS, 31031 for VRS data, 443 for vCenter communication'))
    lines.append(txt_row('Audit log          = All VR config changes logged in vCenter Tasks/Events; forwarded via syslog to'))
    lines.append(txt_row('FIPS 140-2         = Federal cryptographic standard; enabled for VR traffic encryption at cluster'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsphere-replication-troubleshooting',
    'docs/virtualization/vmware/vsphere-replication/troubleshooting/index.md',
    'vSphere Replication Troubleshooting — rep failures, RPO violations, CBT, VAMI bundle',
)
def vsphere_replication_troubleshooting():
    """vSphere Replication Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere Replication — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Replication failing: verify firewall rules on ports 443, 8043, 31031; check site pairing cert')))
    lines.append(R(bMid(IV_L, IV_R, 'RPO violations: check available WAN bandwidth; review missed sync count in VR monitor')))
    lines.append(R(bMid(IV_L, IV_R, 'VR appliance unreachable: verify VRMS/VRS VM is powered on; check VAMI service status')))
    lines.append(R(bMid(IV_L, IV_R, 'CBT issues: reset CBT on VM via snapshot cycle; required after hardware change events')))
    lines.append(R(bMid(IV_L, IV_R, 'Collect support bundle from VRMS VAMI; attach to VMware GSS case with vCenter logs')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues triage network and appliance faults · diagnostics use logs and VAMI'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Replication fail'),
        bMid(B2_L, B2_R, 'vCenter events'),
        bMid(B3_L, B3_R, 'VRMS bundle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RPO violation'),
        bMid(B2_L, B2_R, 'VAMI health'),
        bMid(B3_L, B3_R, 'GSS case open'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VRMS unreachable'),
        bMid(B2_L, B2_R, 'VR monitor UI'),
        bMid(B3_L, B3_R, 'vCenter log bndl'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CBT corruption'),
        bMid(B2_L, B2_R, '/var/log/vmware/vr'),
        bMid(B3_L, B3_R, 'TAM escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Site pair fail'),
        bMid(B2_L, B2_R, 'Firewall test'),
        bMid(B3_L, B3_R, 'Skyline health'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Disk space target'),
        bMid(B2_L, B2_R, 'Cert validity'),
        bMid(B3_L, B3_R, 'Version compat'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues triage replication faults · diagnostics use VAMI and VR monitor'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Rep failing', 'vCenter events', '/var/log/vmware/vr', 'VRMS bundle', 'Re-configure'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['RPO violated', 'VAMI health pg', '/var/log/hms', 'GSS P1 case', 'Reduce RPO'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VRMS down', 'VR monitor UI', '/var/log/vmware', 'TAM escalate', 'Restart VRMS'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CBT issue', 'Firewall test', 'VRMS syslog', 'Skyline health', 'Reset CBT'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (VRMS + VRS) · RAM DIMMs · WAN link · Firewall between sites · Target datastore'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Replication failure = VR sync cycle did not complete; check vCenter events for error code and source'))
    lines.append(txt_row('RPO violation      = Missed sync count > 0 in VR monitor; investigate bandwidth or appliance health'))
    lines.append(txt_row('CBT               = Changed Block Tracking; bitmap tracking VMDK changes; corruption causes resync'))
    lines.append(txt_row('CBT reset          = Snapshot + delete cycle on a VM to force CBT bitmap rebuild; triggers full'))
    lines.append(txt_row('VAMI               = Virtual Appliance Management Interface; check service status and disk usage here'))
    lines.append(txt_row('VR Monitor UI      = vCenter plugin tab showing per-VM replication status, RPO, and last sync time'))
    lines.append(txt_row('Site pairing failure = Lost trust between source/target vCenter; re-pair after certificate change'))
    lines.append(txt_row('Firewall ports     = 443 (vCenter), 8043 (VRMS mgmt), 31031 (VRS data); all required between sites'))
    lines.append(txt_row('VRMS support bundle = Diagnostic archive from VAMI including VR logs; attach to GSS case'))
    lines.append(txt_row('Disk space target  = Insufficient space on target datastore; VR pauses replication until resolved'))
    lines.append(txt_row('Skyline Health     = VMware proactive tool validating VR configuration against known best practices'))
    lines.append(txt_row('Log path           = Primary VR logs at /var/log/vmware/vr/; HMS service logs at /var/log/hms'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vmware-vxrail-architecture',
    'docs/virtualization/vmware/vxrail/architecture/index.md',
    'VMware VxRail Architecture — node families, vSAN HCI stack, LCM, VCF integration',
)
def vmware_vxrail_architecture():
    """VxRail Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VxRail — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VxRail = Dell EMC HCI appliance running VMware ESXi + vSAN + vCenter (embedded)')))
    lines.append(R(bMid(IV_L, IV_R, 'VxRail Manager provides unified lifecycle management via REST API and plugin in vCenter')))
    lines.append(R(bMid(IV_L, IV_R, 'Node families: P-series (general), E-series (entry), V-series (vSAN ESA), G-series (GPU)')))
    lines.append(R(bMid(IV_L, IV_R, 'Supports stretched clusters and VCF integration for full software-defined data centre')))
    lines.append(R(bMid(IV_L, IV_R, 'LCM bundles upgrade FW + ESXi + vSAN together per node; VxRail Manager orchestrates sequence')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines HCI mechanics · integrations connect vCenter and Dell tools'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'HCI: ESXi+vSAN+vCtr'),
        bMid(B2_L, B2_R, 'vCenter plugin'),
        bMid(B3_L, B3_R, 'Cluster 3-64 nodes'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VxRail Mgr API'),
        bMid(B2_L, B2_R, 'Dell OMIVV'),
        bMid(B3_L, B3_R, 'VMk VLAN plan'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LCM unified upg'),
        bMid(B2_L, B2_R, 'iDRAC hardware'),
        bMid(B3_L, B3_R, 'iDRAC OOB VLAN'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Node families P/E/V/G'),
        bMid(B2_L, B2_R, 'Aria Ops adapter'),
        bMid(B3_L, B3_R, 'LCM bundle match'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSAN stretched'),
        bMid(B2_L, B2_R, 'SupportAssist'),
        bMid(B3_L, B3_R, 'FTT policy'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VxRail on VCF'),
        bMid(B2_L, B2_R, 'CloudIQ monitoring'),
        bMid(B3_L, B3_R, 'Witness sizing'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers HCI stack · integrations connect Dell and VMware tools'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VxRail Mgr API', 'vCenter plugin', '3-64 nodes', '3-node starter', 'VLAN plan'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LCM lifecycle', 'Dell OMIVV', 'VMk VLANs', '4+ stretched', 'FTT policy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Node families', 'iDRAC HW', 'iDRAC OOB', 'VCF ready', 'Witness sizing'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vSAN stretched', 'Aria Ops', 'LCM bundle', 'Scale-out', 'BOM match'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Dell PowerEdge servers · NVMe/SSD/HDD drives · 25GbE NICs · iDRAC OOB · ToR switches'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VxRail Manager    = Embedded VM on the cluster; provides REST API and vCenter plugin for HCI'))
    lines.append(txt_row('OMIVV             = OpenManage Integration for VMware vCenter; surfaces Dell hardware alerts in'))
    lines.append(txt_row('LCM               = Lifecycle Manager; orchestrates FW + ESXi + vSAN upgrade as a single bundle'))
    lines.append(txt_row('HCI               = Hyperconverged Infrastructure; compute, storage, and networking in a single'))
    lines.append(txt_row('iDRAC             = Integrated Dell Remote Access Controller; OOB management for hardware health and'))
    lines.append(txt_row('SupportAssist     = Dell proactive support service; auto-creates cases on hardware alert detection'))
    lines.append(txt_row('CloudIQ           = Dell SaaS monitoring platform; capacity, performance, and health tracking for'))
    lines.append(txt_row('VxRail bundle     = Signed LCM package containing matched FW, ESXi, and vSAN component versions'))
    lines.append(txt_row('FTT               = Failures to Tolerate; vSAN policy defining how many host/disk failures data can'))
    lines.append(txt_row('P/E/V/G-series    = VxRail node families: P=general, E=entry, V=vSAN ESA NVMe, G=GPU-accelerated'))
    lines.append(txt_row('Stretched cluster = VxRail cluster spanning two sites with a witness VM for quorum and zero RPO'))
    lines.append(txt_row('VCF on VxRail     = VMware Cloud Foundation deployed on VxRail hardware using Dell-managed LCM'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vmware-vxrail-operations',
    'docs/virtualization/vmware/vxrail/operations/index.md',
    'VMware VxRail Operations — daily health, LCM upgrades, cluster expansion, automation',
)
def vmware_vxrail_operations():
    """VxRail Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VxRail — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VxRail plugin daily health checks in vCenter; iDRAC hardware alarms monitoring')))
    lines.append(R(bMid(IV_L, IV_R, 'LCM bundle download and pre-check before upgrade; node-by-node upgrade sequence')))
    lines.append(R(bMid(IV_L, IV_R, 'FW + ESXi upgraded together per node in a single LCM operation per node')))
    lines.append(R(bMid(IV_L, IV_R, 'SupportAssist for proactive case creation on hardware alerts from iDRAC or OMIVV')))
    lines.append(R(bMid(IV_L, IV_R, 'Post-upgrade validation: vSAN health, ESXi version, iDRAC FW, and cluster stability checks')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch drift early · lifecycle upgrades per node · automation scales VxRail management'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VxRail plugin UI'),
        bMid(B2_L, B2_R, 'LCM bundle DL'),
        bMid(B3_L, B3_R, 'VxRail Mgr API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'iDRAC alarms'),
        bMid(B2_L, B2_R, 'Pre-check health'),
        bMid(B3_L, B3_R, 'LCM REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ESXi connected'),
        bMid(B2_L, B2_R, 'Node-by-node upg'),
        bMid(B3_L, B3_R, 'PowerCLI vSAN'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSAN resync chk'),
        bMid(B2_L, B2_R, 'FW+ESXi together'),
        bMid(B3_L, B3_R, 'Dell automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LCM status'),
        bMid(B2_L, B2_R, 'Rebalance post-add'),
        bMid(B3_L, B3_R, 'Ansible VxRail'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SupportAssist'),
        bMid(B2_L, B2_R, 'Post-check'),
        bMid(B3_L, B3_R, 'SupportAssist API'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch issues early · lifecycle upgrades in sequence · automation handles at-scale changes'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VxRail API', 'Plugin: green', 'Daily checks', 'LCM bundle DL', 'Config export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LCM REST API', 'iDRAC: ok', 'Maint window', 'Pre-check run', 'vSAN config bk'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['PowerCLI vSAN', 'vSAN: resync=0', 'Node maint', 'Node-by-node', 'iDRAC config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Ansible VxRail', 'ESXi: connected', 'Expand cluster', 'Post-upg val', 'Restore redep'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Dell PowerEdge servers · NVMe/SSD/HDD · 25GbE NICs · iDRAC OOB · ToR switches'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VxRail Manager API  = REST API on VxRail Manager VM; used for LCM jobs, health queries, and config'))
    lines.append(txt_row('LCM bundle          = Signed Dell upgrade package; FW + ESXi + vSAN versions tested and bundled'))
    lines.append(txt_row('Pre-check           = Health validation run before LCM upgrade; blocks if vSAN or network issues'))
    lines.append(txt_row('Node-by-node upgrade = LCM puts one node in maintenance, upgrades FW+ESXi, then moves to next node'))
    lines.append(txt_row('SupportAssist       = Dell proactive support; auto-opens cases on hardware alert from iDRAC or OMIVV'))
    lines.append(txt_row('iDRAC               = Integrated Dell Remote Access Controller; hardware health, console, and OOB'))
    lines.append(txt_row('OMIVV               = OpenManage Integration for VMware vCenter; shows Dell hardware alarms in'))
    lines.append(txt_row('vSAN rebalance      = Redistributes vSAN objects evenly after a node is added to the cluster'))
    lines.append(txt_row('Maintenance mode    = ESXi state that evacuates VMs via DRS before hardware or upgrade operations'))
    lines.append(txt_row('FW update           = Firmware update applied to iDRAC, BIOS, NICs, and drives as part of LCM bundle'))
    lines.append(txt_row('PowerCLI            = VMware PowerShell module; used for vSAN health checks and cluster automation'))
    lines.append(txt_row('Post-upgrade validation = Checks ESXi version, iDRAC FW, vSAN health, and cluster stability after LCM'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vmware-vxrail-security',
    'docs/virtualization/vmware/vxrail/security/index.md',
    'VMware VxRail Security — iDRAC LDAP, lockdown mode, vSAN encryption, Secure Boot',
)
def vmware_vxrail_security():
    """VxRail Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VxRail — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'iDRAC LDAP/AD authentication with OOB-only VLAN access for hardware management')))
    lines.append(R(bMid(IV_L, IV_R, 'ESXi lockdown mode (normal) with host profiles enforcement across all cluster nodes')))
    lines.append(R(bMid(IV_L, IV_R, 'vCenter SSO for all management plane access; VxRail Manager TLS certificates enforced')))
    lines.append(R(bMid(IV_L, IV_R, 'vSAN data-at-rest encryption with KMIP-compatible KMS integration for key management')))
    lines.append(R(bMid(IV_L, IV_R, 'Secure Boot on all nodes; STIG alignment via host profiles; syslog forwarded to SIEM')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication gates hardware access · access control limits management scope'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'iDRAC LDAP/AD'),
        bMid(B2_L, B2_R, 'RBAC via vCenter'),
        bMid(B3_L, B3_R, 'vSAN data-at-rest'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ESXi lockdown mode'),
        bMid(B2_L, B2_R, 'iDRAC user roles'),
        bMid(B3_L, B3_R, 'iDRAC HTTPS only'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vCenter SSO'),
        bMid(B2_L, B2_R, 'VxRail Mgr roles'),
        bMid(B3_L, B3_R, 'Secure Boot ESXi'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VxRail Mgr local'),
        bMid(B2_L, B2_R, 'LCM op roles'),
        bMid(B3_L, B3_R, 'VxRail Mgr TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'iDRAC 2FA'),
        bMid(B2_L, B2_R, 'Least privilege'),
        bMid(B3_L, B3_R, 'iDRAC SSL cert'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Svc acct policy'),
        bMid(B2_L, B2_R, 'Audit events'),
        bMid(B3_L, B3_R, 'Syslog TLS'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth controls who accesses hardware · RBAC scopes management'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['iDRAC LDAP', 'vCenter RBAC', 'vSAN encrypt', 'Secure Boot', 'vCenter events'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['ESXi lockdown', 'iDRAC roles', 'iDRAC HTTPS', 'SSH disabled', 'iDRAC audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vCenter SSO', 'VxRail roles', 'VxRail TLS', 'Host profiles', 'Syslog to SIEM'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['iDRAC 2FA', 'Least privilege', 'Cert rotation', 'STIG align', 'LCM log audit'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Dell PowerEdge servers · TPM 2.0 · NVMe/SSD/HDD · iDRAC OOB network · CA infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('iDRAC             = Integrated Dell Remote Access Controller; LDAP/AD auth; OOB-only VLAN access'))
    lines.append(txt_row('Lockdown mode     = ESXi host setting preventing direct SSH/DCUI; all management via vCenter only'))
    lines.append(txt_row('vSAN encryption   = Data-at-rest encryption on vSAN datastore; keys managed by external KMIP KMS'))
    lines.append(txt_row('KMS/KMIP          = Key Management Server / protocol; external key store for vSAN and VM encryption'))
    lines.append(txt_row('Secure Boot       = UEFI feature verifying ESXi VIB signatures on all VxRail nodes at boot time'))
    lines.append(txt_row('Host Profile      = vCenter config template enforcing lockdown, NTP, syslog, and security settings'))
    lines.append(txt_row('VxRail Manager TLS = TLS certificate on VxRail Manager VM; used for API and plugin communications'))
    lines.append(txt_row('STIG alignment    = Defense Information Systems Agency hardening guide applied via host profiles'))
    lines.append(txt_row('OOB VLAN          = Out-of-band management VLAN restricted to iDRAC access only; no VM traffic'))
    lines.append(txt_row('LDAP/AD integration = iDRAC and vCenter authenticate against Active Directory for role mapping'))
    lines.append(txt_row('RBAC              = Role-Based Access Control; vCenter roles applied to VxRail management operations'))
    lines.append(txt_row('2FA on iDRAC      = Two-factor authentication on iDRAC console; reduces OOB access risk'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vmware-vxrail-troubleshooting',
    'docs/virtualization/vmware/vxrail/troubleshooting/index.md',
    'VMware VxRail Troubleshooting — plugin unavailable, LCM pre-check, vSAN degraded',
)
def vmware_vxrail_troubleshooting():
    """VxRail Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VxRail — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VxRail plugin unavailable in vCenter; LCM pre-check failure blocking upgrade')))
    lines.append(R(bMid(IV_L, IV_R, 'vSAN object degraded or resync stuck; iDRAC hardware alert on a node')))
    lines.append(R(bMid(IV_L, IV_R, 'Node not rejoining cluster after maintenance; network mismatch causing VxRail Manager issues')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnostics: VxRail API debug, LCM logs, vSAN health UI, iDRAC system event log')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: support bundle export, Dell GSS P1, TAM contact, log archive for ProSupport')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues define triage path · diagnostics isolate root cause · escalation engages Dell support'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Plugin unavail'),
        bMid(B2_L, B2_R, 'VxRail API debug'),
        bMid(B3_L, B3_R, 'VxRail bndl'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LCM pre-chk fail'),
        bMid(B2_L, B2_R, 'LCM log files'),
        bMid(B3_L, B3_R, 'Dell support case'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSAN degraded'),
        bMid(B2_L, B2_R, 'vSAN health UI'),
        bMid(B3_L, B3_R, 'GSS escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'iDRAC alert'),
        bMid(B2_L, B2_R, 'iDRAC sys event'),
        bMid(B3_L, B3_R, 'TAM contact'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Node not rejoin'),
        bMid(B2_L, B2_R, 'get-tech-support'),
        bMid(B3_L, B3_R, 'P1 Dell ProSupp'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Net mismatch'),
        bMid(B2_L, B2_R, 'vm-support bndl'),
        bMid(B3_L, B3_R, 'Log archive'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics pinpoint root cause · escalation gets Dell support engaged'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Plugin unavail', 'VxRail API dbg', 'VxRail Mgr logs', 'Bundle export', 'Restart VxRail'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LCM pre-chk fail', 'LCM log files', '/var/log/vmware', 'Dell support', 'Fix + retry'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vSAN degraded', 'vSAN health UI', '/var/log/vsan', 'GSS P1 case', 'Replace disk'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Node not rejoin', 'iDRAC sys evt', 'iDRAC /log', 'TAM contact', 'Re-add node'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Dell PowerEdge servers · NVMe/SSD/HDD · iDRAC OOB · 25GbE NICs · ToR switches'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VxRail plugin     = vCenter plugin provided by VxRail Manager; shows cluster health and LCM status'))
    lines.append(txt_row('LCM pre-check     = Validation run before upgrade; fails if vSAN resync, network, or health issues'))
    lines.append(txt_row('vSAN object health = vSAN tracks each VM object; degraded = FTT violated; resync = rebuilding copies'))
    lines.append(txt_row('iDRAC SEL         = System Event Log on iDRAC; hardware faults (disk, PSU, fan, NIC) recorded here'))
    lines.append(txt_row('get-tech-support  = VxRail CLI command collecting full diagnostic bundle for Dell GSS cases'))
    lines.append(txt_row('Support bundle    = Compressed log archive from VxRail Manager, ESXi hosts, and iDRAC for escalation'))
    lines.append(txt_row('TAM               = Technical Account Manager; Dell named support contact for critical escalations'))
    lines.append(txt_row('Dell ProSupport   = Dell premium support tier; P1 = production down, response in under 4 hours'))
    lines.append(txt_row('Node rejoin       = Process of ESXi host re-entering vSAN cluster after maintenance or failure'))
    lines.append(txt_row('Network mismatch  = VLAN or MTU misconfiguration preventing VxRail Manager from reaching ESXi hosts'))
    lines.append(txt_row('VxRail Mgr restart = Restarting Mystic service on VxRail Manager VM to recover plugin or API issues'))
    lines.append(txt_row('GSS escalation    = Global Support Services; Dell/VMware support organisation for P1/P2 incidents'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vmware-topics',
    'docs/virtualization/vmware/topics/index.md',
    'VMware Topics — HA, DRS, APD/PDL, resource contention, NTP/DNS deep-dive topics',
)
def vmware_topics():
    """VMware Topics sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VMware — Topics'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware technical deep-dive topics: cluster failure domains, cluster state validation')))
    lines.append(R(bMid(IV_L, IV_R, 'DRS/vMotion behavior, HA admission control, host isolation response, maintenance risk')))
    lines.append(R(bMid(IV_L, IV_R, 'Network packet loss, recovery behavior, resource contention, snapshot impact on storage')))
    lines.append(R(bMid(IV_L, IV_R, 'Storage latency troubleshooting: APD/PDL response, VMFS locking, datastore I/O queues')))
    lines.append(R(bMid(IV_L, IV_R, 'Time/DNS validation: NTP sync required for HA, vSAN, and certificate operations')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Cluster topics cover HA design · performance topics isolate bottlenecks'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cluster Topics'),
        bMid(B2_L, B2_R, 'Performance Topics'),
        bMid(B3_L, B3_R, 'Resilience Topics'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Failure domains'),
        bMid(B2_L, B2_R, 'Resource conten'),
        bMid(B3_L, B3_R, 'Recovery behav'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cluster state'),
        bMid(B2_L, B2_R, 'Snapshot impact'),
        bMid(B3_L, B3_R, 'HA restart ord'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'DRS/vMotion'),
        bMid(B2_L, B2_R, 'Storage latency'),
        bMid(B3_L, B3_R, 'APD/PDL resp'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'HA admission'),
        bMid(B2_L, B2_R, 'Network pkt loss'),
        bMid(B3_L, B3_R, 'Host isolation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Isolation resp'),
        bMid(B2_L, B2_R, 'vMotion timing'),
        bMid(B3_L, B3_R, 'Time/DNS val'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Maint risk val'),
        bMid(B2_L, B2_R, 'Balloon/swap'),
        bMid(B3_L, B3_R, 'Upgrade seq'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Cluster topics cover HA/DRS · performance topics isolate contention'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['HA/Cluster', 'DRS/vMotion', 'Resources', 'Storage', 'Network/Time'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Failure domains', 'DRS behavior', 'Resource cont', 'Storage latency', 'Network pkt loss'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cluster state', 'vMotion timing', 'Snapshot impact', 'APD/PDL resp', 'Time/DNS val'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['HA admission', 'Maint risk', 'Memory balloon', 'Datastore I/O', 'DNS resolution'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Isolation resp', 'Migration thres', 'CPU ready %', 'VMFS lock', 'NTP sync check'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 cluster · ESXi hosts · Shared storage (SAN/vSAN) · ToR switches · Physical NICs'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Failure domain      = Host group in a cluster; HA distributes VM restarts across domains to limit'))
    lines.append(txt_row('Cluster state val.  = Verification of vCenter, HA agent, DRS, and vSAN state across all cluster hosts'))
    lines.append(txt_row('HA admission control = Policy reserving cluster capacity for VM restarts; slot-based or % resource'))
    lines.append(txt_row('Host isolation resp = HA action when host loses heartbeat: power off, shutdown, or leave VMs running'))
    lines.append(txt_row('DRS migration thres = Aggressiveness setting (1-5) controlling how often DRS initiates vMotion'))
    lines.append(txt_row('vMotion             = Live migration of a running VM between ESXi hosts with zero downtime'))
    lines.append(txt_row('Resource contention = CPU ready, memory balloon/swap, or storage latency caused by overcommitment'))
    lines.append(txt_row('Snapshot delta      = VMDK delta disk created at snapshot time; grows with writes; impacts'))
    lines.append(txt_row('APD                 = All Paths Down; storage device unreachable; all paths to datastore failed'))
    lines.append(txt_row('PDL                 = Permanent Device Loss; storage device reports itself gone; triggers HA restart'))
    lines.append(txt_row('NTP synchronization = Required for HA elections, vSAN, SSO certificates, and replication timestamps'))
    lines.append(txt_row('Balloon driver      = VMware memory reclaim driver; inflates inside guest to force OS to free memory'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vxrail-hardware',
    'docs/virtualization/vxrail/hardware/index.md',
    'VxRail Hardware — node health, disk replacement, NIC health, power/cooling, FW inventory',
)
def vxrail_hardware():
    """VxRail Hardware sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VxRail — Hardware'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VxRail hardware operations: node health monitoring via iDRAC and VxRail Manager')))
    lines.append(R(bMid(IV_L, IV_R, 'Disk replacement procedures using guided workflow; NIC health and link state checks')))
    lines.append(R(bMid(IV_L, IV_R, 'Power and cooling alarm management; iDRAC out-of-band access configuration')))
    lines.append(R(bMid(IV_L, IV_R, 'Firmware inventory and compliance tracking via OMIVV and LCM bundle validation')))
    lines.append(R(bMid(IV_L, IV_R, 'SupportAssist and CloudIQ for proactive hardware monitoring and capacity planning')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Node health monitors hardware state · hardware ops cover disk and NIC'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Node Health'),
        bMid(B2_L, B2_R, 'Hardware Ops'),
        bMid(B3_L, B3_R, 'HW Monitoring'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VxRail plugin'),
        bMid(B2_L, B2_R, 'Disk replacement'),
        bMid(B3_L, B3_R, 'OMIVV alerts'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'iDRAC health'),
        bMid(B2_L, B2_R, 'NIC link check'),
        bMid(B3_L, B3_R, 'SupportAssist'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ESXi connected'),
        bMid(B2_L, B2_R, 'Power/cooling'),
        bMid(B3_L, B3_R, 'CloudIQ view'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSAN node ok'),
        bMid(B2_L, B2_R, 'iDRAC config'),
        bMid(B3_L, B3_R, 'iDRAC SEL log'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Hardware alarm'),
        bMid(B2_L, B2_R, 'FW inventory'),
        bMid(B3_L, B3_R, 'Temp/fan/PSU'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Disk state'),
        bMid(B2_L, B2_R, 'Guided removal'),
        bMid(B3_L, B3_R, 'Drive SMART'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Node health surfaces hardware faults · ops guide replacement procedures'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Node Health', 'Disk Replace', 'NIC Health', 'Power/Cooling', 'iDRAC/FW'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VxRail plugin', 'Guided workflow', 'Link state', 'PSU status', 'iDRAC config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['iDRAC health', 'Pre-removal chk', 'NIC teaming', 'Temp alarms', 'FW inventory'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['ESXi connected', 'vSAN rebuild', 'Driver compat', 'Fan speed', 'iDRAC LDAP'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vSAN node ok', 'Post-replace val', 'OMIVV NIC chk', 'Cooling zones', 'FW compliance'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Dell PowerEdge servers · NVMe/SSD/HDD drives · iDRAC OOB chip · PSUs · Cooling fans · NICs'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('iDRAC             = Integrated Dell Remote Access Controller; hardware health, OOB console, LDAP auth'))
    lines.append(txt_row('VxRail Manager    = Embedded management VM; aggregates node health from iDRAC and ESXi into plugin'))
    lines.append(txt_row('OMIVV             = OpenManage Integration for VMware vCenter; surfaces Dell HW alarms in vCenter UI'))
    lines.append(txt_row('SupportAssist     = Dell proactive support service; auto-creates cases on hardware fault detection'))
    lines.append(txt_row('CloudIQ           = Dell SaaS monitoring platform; capacity, health, and performance tracking'))
    lines.append(txt_row('SEL               = System Event Log on iDRAC; records all hardware events (disk, PSU, fan, NIC)'))
    lines.append(txt_row('SMART             = Self-Monitoring Analysis and Reporting Technology; drive health predictor'))
    lines.append(txt_row('PSU               = Power Supply Unit; dual PSU in each VxRail node for redundancy'))
    lines.append(txt_row('NIC teaming       = Active/standby or LACP NIC bonding on VxRail nodes for network redundancy'))
    lines.append(txt_row('Firmware inventory = LCM bundle tracks required FW versions for BIOS, iDRAC, NICs, and drives'))
    lines.append(txt_row('vSAN disk group   = Cache + capacity disk grouping per node; disk failure triggers vSAN rebuild'))
    lines.append(txt_row('Guided disk replacement = VxRail Manager workflow that puts node in maint mode before disk removal'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vxrail-lifecycle',
    'docs/virtualization/vxrail/lifecycle/index.md',
    'VxRail Lifecycle — BOM validation, LCM planning, node upgrade, rollback, post-validation',
)
def vxrail_lifecycle():
    """VxRail Lifecycle sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VxRail — Lifecycle'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VxRail upgrade lifecycle: planning with compatibility matrix and BOM validation')))
    lines.append(R(bMid(IV_L, IV_R, 'Pre-check health assessment before LCM run; bundle download from Dell support portal')))
    lines.append(R(bMid(IV_L, IV_R, 'Firmware update alongside ESXi in single LCM operation per node (node-by-node)')))
    lines.append(R(bMid(IV_L, IV_R, 'Rollback planning if upgrade fails; post-upgrade validation of all cluster components')))
    lines.append(R(bMid(IV_L, IV_R, 'vSAN rebalance after cluster expansion; staged upgrade planning for large environments')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Planning validates BOM · execution runs LCM node-by-node'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Planning'),
        bMid(B2_L, B2_R, 'Execution'),
        bMid(B3_L, B3_R, 'Validation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'BOM compat check'),
        bMid(B2_L, B2_R, 'Bundle download'),
        bMid(B3_L, B3_R, 'Post-upg health'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Upgrade planning'),
        bMid(B2_L, B2_R, 'Pre-check run'),
        bMid(B3_L, B3_R, 'vSAN check'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pre-req review'),
        bMid(B2_L, B2_R, 'Node-by-node'),
        bMid(B3_L, B3_R, 'ESXi version ok'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Bundle select'),
        bMid(B2_L, B2_R, 'FW+ESXi together'),
        bMid(B3_L, B3_R, 'iDRAC FW ver'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Rollback plan'),
        bMid(B2_L, B2_R, 'vSAN rebalance'),
        bMid(B3_L, B3_R, 'LCM status'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Risk assessment'),
        bMid(B2_L, B2_R, 'Progress monitor'),
        bMid(B3_L, B3_R, 'Cluster stable'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Planning catches BOM gaps · execution upgrades node-by-node safely'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Upg Planning', 'Pre-Checks', 'Bundle Mgmt', 'Firmware', 'Rollback/Post'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['BOM compat', 'Health pre-chk', 'Bundle download', 'FW with ESXi', 'Rollback plan'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Upgrade plan', 'vSAN resync=0', 'Bundle validate', 'FW inventory', 'Post-upg val'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Risk assess', 'ESXi compat', 'Staging area', 'iDRAC FW', 'vSAN check'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['BOM select', 'Network check', 'Bundle history', 'BIOS version', 'Cluster stable'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Dell PowerEdge servers · NVMe/SSD/HDD · iDRAC · 25GbE NICs · ToR switches'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('LCM               = Lifecycle Manager; VxRail orchestration engine for node-by-node upgrade'))
    lines.append(txt_row('BOM               = Bill of Materials; version matrix of ESXi, FW, and driver combinations from Dell'))
    lines.append(txt_row('Pre-check         = LCM health validation before upgrade; blocks if vSAN or connectivity issues found'))
    lines.append(txt_row('Bundle            = Signed Dell LCM package with all matched component versions for the upgrade'))
    lines.append(txt_row('Firmware update   = BIOS, iDRAC, NIC, and drive FW updated per node as part of the LCM bundle'))
    lines.append(txt_row('ESXi upgrade      = ESXi version bump included in LCM bundle; applied node-by-node with maintenance'))
    lines.append(txt_row('vSAN rebalance    = Object redistribution after cluster expansion; triggered automatically or'))
    lines.append(txt_row('Rollback          = Returning a node to previous ESXi boot bank if LCM upgrade fails mid-sequence'))
    lines.append(txt_row('Post-upgrade val  = Checks ESXi version, iDRAC FW, vSAN health, and cluster alarms after LCM run'))
    lines.append(txt_row('Compatibility matrix = Dell matrix defining which ESXi, vCenter, and FW versions are supported'))
    lines.append(txt_row('Staged upgrade    = Upgrading a subset of nodes first to validate before proceeding to full cluster'))
    lines.append(txt_row('Node-by-node      = LCM upgrade sequence: one node at a time into maintenance, upgrade, then exit'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vxrail-operations',
    'docs/virtualization/vxrail/operations/index.md',
    'VxRail Operations — daily ops, maintenance windows, cluster expansion, support bundles',
)
def vxrail_operations():
    """VxRail Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VxRail — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Daily VxRail cluster operations: health checks via VxRail plugin and iDRAC')))
    lines.append(R(bMid(IV_L, IV_R, 'Maintenance window procedures; node maintenance mode workflow and DRS evacuation')))
    lines.append(R(bMid(IV_L, IV_R, 'Cluster expansion node addition; support case preparation with bundle generation')))
    lines.append(R(bMid(IV_L, IV_R, 'Post-change validation; LCM failure triage; pre-upgrade readiness checks')))
    lines.append(R(bMid(IV_L, IV_R, 'Change management log; alert review from OMIVV, SupportAssist, and vCenter alarms')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch cluster issues · maintenance keeps nodes updated · cluster mgmt handles expansion'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Maintenance'),
        bMid(B3_L, B3_R, 'Cluster Mgmt'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily checks'),
        bMid(B2_L, B2_R, 'Maint window'),
        bMid(B3_L, B3_R, 'Cluster expand'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VxRail plugin'),
        bMid(B2_L, B2_R, 'Node maint mode'),
        bMid(B3_L, B3_R, 'Node add guide'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'iDRAC alarms'),
        bMid(B2_L, B2_R, 'Pre-maint chk'),
        bMid(B3_L, B3_R, 'Rebalance'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSAN resync'),
        bMid(B2_L, B2_R, 'Change window'),
        bMid(B3_L, B3_R, 'Support case'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Node health'),
        bMid(B2_L, B2_R, 'Post-change val'),
        bMid(B3_L, B3_R, 'LCM fail triage'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert review'),
        bMid(B2_L, B2_R, 'Change log'),
        bMid(B3_L, B3_R, 'Pre-upg checks'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops surface issues early · maintenance follows change process'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Daily Chks', 'Maint Window', 'Node Maint', 'Cluster Expnd', 'Support Case'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VxRail plugin', 'Pre-maint chk', 'Maint mode', 'Add node guide', 'Bundle gen'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['iDRAC alarms', 'Change window', 'DRS evacuate', 'Rebalance', 'Log collect'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vSAN resync=0', 'Work perform', 'FW+ESXi upg', 'vSAN expand', 'SupportAssist'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['ESXi connected', 'Post-chng val', 'Exit maint', 'Cluster health', 'GSS portal'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Dell PowerEdge servers · NVMe/SSD/HDD · iDRAC OOB · 25GbE NICs · ToR switches'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VxRail plugin     = vCenter plugin aggregating cluster health from VxRail Manager into a single view'))
    lines.append(txt_row('Maintenance mode  = ESXi state evacuating VMs via DRS before node-level maintenance or upgrade'))
    lines.append(txt_row('DRS evacuation    = DRS migrates all VMs off a host via vMotion before maintenance mode is entered'))
    lines.append(txt_row('Cluster expansion = Adding new VxRail nodes to an existing cluster via guided VxRail Manager workflow'))
    lines.append(txt_row('Post-change val   = Checks vSAN health, ESXi connectivity, iDRAC status, and alarms after any change'))
    lines.append(txt_row('Support bundle    = Log archive generated by VxRail Manager for Dell GSS case submission'))
    lines.append(txt_row('SupportAssist     = Dell proactive support service; opens cases automatically on hardware fault'))
    lines.append(txt_row('LCM failure triage = Investigating why an LCM upgrade stalled; review LCM logs and pre-check output'))
    lines.append(txt_row('Pre-upgrade check = Health and readiness validation run before initiating an LCM upgrade job'))
    lines.append(txt_row('Change management = Formal process for scheduling, approving, and documenting cluster changes'))
    lines.append(txt_row('iDRAC             = Integrated Dell Remote Access Controller; hardware health and OOB access'))
    lines.append(txt_row('Node-by-node      = LCM upgrade pattern: maintenance → upgrade → validate → next node in sequence'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vxrail-troubleshooting',
    'docs/virtualization/vxrail/troubleshooting/index.md',
    'VxRail Troubleshooting — LCM failures, Mystic unavailable, vSAN alerts, network alerts',
)
def vxrail_troubleshooting():
    """VxRail Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VxRail — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'LCM upgrade failures and rollback; VxRail Manager VM (Mystic service) unavailable')))
    lines.append(R(bMid(IV_L, IV_R, 'Host alerts from ESXi or hardware; vSAN alerts for degraded objects or capacity')))
    lines.append(R(bMid(IV_L, IV_R, 'Support bundle generation failures; network alerts for VLAN or link issues')))
    lines.append(R(bMid(IV_L, IV_R, 'iDRAC system event review; OMIVV alarm triage; VxRail API debug for service issues')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: Dell GSS P1, TAM contact, ProSupport log archive for critical incidents')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  LCM/VxRail issues block upgrades · diagnostics isolate service failures'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LCM/VxRail Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LCM fail triage'),
        bMid(B2_L, B2_R, 'VxRail API debug'),
        bMid(B3_L, B3_R, 'VxRail bundle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Mgr unavailable'),
        bMid(B2_L, B2_R, 'LCM log files'),
        bMid(B3_L, B3_R, 'Dell support'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Host alerts'),
        bMid(B2_L, B2_R, 'iDRAC SEL'),
        bMid(B3_L, B3_R, 'GSS escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSAN alerts'),
        bMid(B2_L, B2_R, 'vSAN health UI'),
        bMid(B3_L, B3_R, 'TAM contact'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Bundle fail'),
        bMid(B2_L, B2_R, 'Bundle gen log'),
        bMid(B3_L, B3_R, 'P1 ProSupport'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Net alerts'),
        bMid(B2_L, B2_R, 'OMIVV alerts'),
        bMid(B3_L, B3_R, 'Log archive'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  LCM issues block upgrades · diagnostics pinpoint service faults'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LCM Failures', 'Mgr Unavail', 'Host/vSAN', 'Bundle Fail', 'Network Alerts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LCM pre-chk', 'VxRail svc', 'Host alerts', 'Bundle gen err', 'VLAN mismatch'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LCM stall', 'Mystic server', 'vSAN degrade', 'Log collection', 'Link down NIC'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LCM rollback', 'VxRail API', 'vSAN capacity', 'API timeout', 'MTU issue'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Post-fail chk', 'Mgr restart', 'iDRAC alerts', 'Manual bundle', 'ToR config'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Dell PowerEdge servers · NVMe/SSD/HDD · iDRAC · 25GbE NICs · ToR switches'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('LCM failure       = Upgrade job failed mid-sequence; check LCM logs and pre-check output for root'))
    lines.append(txt_row('VxRail Manager    = Embedded management VM running Mystic service; provides REST API and vCenter'))
    lines.append(txt_row('Host alert        = ESXi or iDRAC hardware alarm (disk, NIC, PSU, CPU) surfaced in VxRail plugin'))
    lines.append(txt_row('vSAN degraded     = vSAN object FTT violated; component on failed disk or host; rebuild in progress'))
    lines.append(txt_row('Support bundle    = Compressed log archive from VxRail Manager and ESXi hosts for Dell GSS submission'))
    lines.append(txt_row('SupportAssist     = Dell proactive support; auto-opens cases on hardware fault; submits initial logs'))
    lines.append(txt_row('iDRAC SEL         = System Event Log; hardware events (disk, PSU, fan, NIC); first stop for HW triage'))
    lines.append(txt_row('OMIVV             = OpenManage Integration for VMware vCenter; surfaces Dell HW alarms in vCenter'))
    lines.append(txt_row('TAM escalation    = Engaging named Dell Technical Account Manager for critical production incidents'))
    lines.append(txt_row('Dell ProSupport P1 = Highest Dell support priority; production down; response in under 4 hours'))
    lines.append(txt_row('LCM rollback      = Reverting a node to previous ESXi boot bank after a failed LCM upgrade attempt'))
    lines.append(txt_row('Network alert     = VLAN mismatch, link down, or MTU issue detected by OMIVV or VxRail Manager'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vxrail-manager',
    'docs/virtualization/vxrail/vxrail-manager/index.md',
    'VxRail Manager — Mystic service health, LCM jobs, bundle generation, connectivity, certs',
)
def vxrail_manager():
    """VxRail Manager Overview sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VxRail Manager — Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VxRail Manager is the VM running the "Mystic" service: REST API and vCenter plugin')))
    lines.append(R(bMid(IV_L, IV_R, 'Manages LCM lifecycle jobs; generates support bundles; manages cluster connectivity config')))
    lines.append(R(bMid(IV_L, IV_R, 'Handles certificate management for the appliance; aggregates log files for diagnostics')))
    lines.append(R(bMid(IV_L, IV_R, 'API token authentication for REST access; job queue for LCM and pre-check operations')))
    lines.append(R(bMid(IV_L, IV_R, 'DNS/NTP configuration and proxy config managed through VxRail Manager connectivity page')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Service health monitors Mystic · lifecycle jobs run upgrades'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Service Health'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Connectivity'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Mystic service'),
        bMid(B2_L, B2_R, 'Lifecycle jobs'),
        bMid(B3_L, B3_R, 'vCenter plugin'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'API endpoint'),
        bMid(B2_L, B2_R, 'Support bundle'),
        bMid(B3_L, B3_R, 'VxRail API TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Plugin status'),
        bMid(B2_L, B2_R, 'Cert management'),
        bMid(B3_L, B3_R, 'iDRAC access'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Job queue'),
        bMid(B2_L, B2_R, 'Log collection'),
        bMid(B3_L, B3_R, 'ESXi mgmt net'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Log service'),
        bMid(B2_L, B2_R, 'API token'),
        bMid(B3_L, B3_R, 'DNS/NTP config'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Health endpoint'),
        bMid(B2_L, B2_R, 'Upgrade trigger'),
        bMid(B3_L, B3_R, 'Proxy config'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Service health confirms Mystic is running · operations cover LCM and certs'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Svc Health', 'Lifecycle Jobs', 'Support Bndl', 'Connectivity', 'Certs/Logs'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Mystic status', 'LCM job status', 'Bundle gen', 'Plugin connect', 'Cert expiry'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['API endpoint', 'Job history', 'Log collect', 'vCenter auth', 'Cert rotation'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Plugin loaded', 'Pre-check jobs', 'SupportAssist', 'DNS/NTP cfg', '/var/log/mystic'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Health check', 'Upgrade jobs', 'Manual bundle', 'Proxy config', 'API access log'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Dell PowerEdge servers · VxRail Manager VM · iDRAC OOB · 25GbE NICs · vCenter cluster'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VxRail Manager    = Embedded VM on VxRail cluster; runs Mystic service for all cluster management'))
    lines.append(txt_row('Mystic service    = Core Java service inside VxRail Manager VM; handles API, LCM, and plugin'))
    lines.append(txt_row('LCM job           = Lifecycle Manager upgrade task managed by VxRail Manager; tracked in job queue'))
    lines.append(txt_row('Support bundle    = Compressed diagnostic archive generated by VxRail Manager for Dell GSS cases'))
    lines.append(txt_row('vCenter plugin    = VxRail UI extension in vCenter; shows cluster health, LCM status, and node'))
    lines.append(txt_row('REST API          = VxRail Manager API on port 443; used for LCM, health queries, and cluster config'))
    lines.append(txt_row('API token         = Bearer token for VxRail Manager REST API authentication; scoped per session'))
    lines.append(txt_row('Certificate mgmt  = VxRail Manager manages TLS certs for API and plugin; rotation handled via UI/API'))
    lines.append(txt_row('DNS/NTP config    = Cluster DNS servers and NTP sources configured in VxRail Manager connectivity'))
    lines.append(txt_row('Proxy config      = HTTP proxy settings for VxRail Manager to reach SupportAssist and CloudIQ'))
    lines.append(txt_row('/var/log/mystic   = Primary VxRail Manager log directory; contains service, API, and LCM job logs'))
    lines.append(txt_row('SupportAssist intg = VxRail Manager sends hardware alerts to Dell for proactive case creation'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines



# ── Write / check helpers ─────────────────────────────────────────────────────

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Matches the first bare ``` block (no language tag on the opening line).
_BLOCK_RE = re.compile(r'^```\n.*?^```$', re.MULTILINE | re.DOTALL)
# Matches the first ```mermaid block (fallback for pages that have mermaid diagrams).
_MERMAID_RE = re.compile(r'^```mermaid\n.*?^```$', re.MULTILINE | re.DOTALL)


def _width_str(lines):
    widths = {len(l) for l in lines}
    if len(widths) == 1:
        return str(next(iter(widths)))
    return f'{min(widths)}-{max(widths)}'


def _write(name):
    """Replace the first bare ``` block (or ```mermaid fallback) with fresh output.

    When a mermaid block is found, it is removed from its current position and
    the diagram is inserted immediately after the kb-summary </div> instead —
    enforcing the MkDocs superfences rule that the code fence must precede
    any <div class="kb-grid"> block.
    """
    entry = DIAGRAMS[name]
    lines = entry['fn']()
    target = os.path.join(REPO_ROOT, entry['file'])
    try:
        with open(target, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f'  ERROR: file not found: {entry["file"]}', file=sys.stderr)
        return False
    replacement = '```\n' + '\n'.join(lines) + '\n```'
    new_content, n = _BLOCK_RE.subn(replacement, content, count=1)
    if n == 0:
        # Mermaid fallback: remove the block in-place, then re-insert after kb-summary.
        stripped, n = _MERMAID_RE.subn('', content, count=1)
        if n == 0:
            print(f'  ERROR: no ``` or ```mermaid block found in {entry["file"]}', file=sys.stderr)
            return False
        # Insert after the kb-summary closing </div>
        summary_end = re.search(r'</div>\n', stripped)
        if summary_end:
            pos = summary_end.end()
            new_content = stripped[:pos] + '\n' + replacement + '\n' + stripped[pos:].lstrip('\n')
        else:
            # No kb-summary — insert after the title line
            title_end = re.search(r'^# .+\n', stripped, re.MULTILINE)
            pos = title_end.end() if title_end else 0
            new_content = stripped[:pos] + '\n' + replacement + '\n' + stripped[pos:].lstrip('\n')
    if n == 0:
        print(f'  ERROR: no ``` or ```mermaid block found in {entry["file"]}', file=sys.stderr)
        return False
    if new_content == content:
        print(f'  OK (unchanged)  {entry["file"]}')
        return True
    with open(target, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'  Updated  {entry["file"]}  [{len(lines)} lines, w={_width_str(lines)}]')
    return True


def _check(name):
    """Return True if the file's ``` block matches current output, False if out of sync, None if not found."""
    entry = DIAGRAMS[name]
    lines = entry['fn']()
    target = os.path.join(REPO_ROOT, entry['file'])
    try:
        with open(target, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return None
    m = _BLOCK_RE.search(content)
    if not m:
        return None
    # Strip the opening ``` line and the closing ``` line to get the diagram body.
    body = m.group(0).split('\n', 1)[1].rsplit('\n', 1)[0]
    return body.split('\n') == lines


# ── CLI ───────────────────────────────────────────────────────────────────────

def _list():
    col = max(len(n) for n in DIAGRAMS) + 2
    print('Registered diagrams:\n')
    for name, entry in sorted(DIAGRAMS.items()):
        print(f'  {name:<{col}}  {entry["description"]}')
        print(f'  {"":<{col}}  → {entry["file"]}')
        print()


def _audit_placement():
    """Return list of (name, file, issue) for placement violations."""
    issues = []
    for name, entry in DIAGRAMS.items():
        path = os.path.join(REPO_ROOT, entry['file'])
        if not os.path.exists(path):
            continue
        with open(path) as f:
            lines = f.read().split('\n')
        fence = next((i + 1 for i, l in enumerate(lines) if l == '```'), None)
        grid  = next((i + 1 for i, l in enumerate(lines) if 'kb-grid' in l), None)
        if fence is None:
            issues.append((name, entry['file'], 'NO FENCE'))
        elif grid and fence >= grid:
            issues.append((name, entry['file'], f'fence={fence} after grid={grid}'))
    return issues


def _audit_widths():
    """Run all diagram functions and collect WARNs, grouped by diagram name.
    Returns dict of name -> list of warn strings (empty means clean)."""
    import io, contextlib
    results = {}
    for name, entry in sorted(DIAGRAMS.items()):
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            entry['fn']()
        warns = [l.strip() for l in buf.getvalue().splitlines() if 'WARN' in l]
        if warns:
            results[name] = warns
    return results


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        prog='ascii_diagram_gen.py',
        description='ASCII diagram generator for KB markdown files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            'Examples:\n'
            '  python3 scripts/ascii_diagram_gen.py                      # list diagrams\n'
            '  python3 scripts/ascii_diagram_gen.py vmware               # print to stdout\n'
            '  python3 scripts/ascii_diagram_gen.py vmware --write       # update file\n'
            '  python3 scripts/ascii_diagram_gen.py --write-all          # update all\n'
            '  python3 scripts/ascii_diagram_gen.py --check              # sync + widths + placement\n'
            '  python3 scripts/ascii_diagram_gen.py --validate           # width WARNs grouped by name\n'
            '  python3 scripts/ascii_diagram_gen.py --layout 20 20 47    # box positions\n'
        ),
    )
    parser.add_argument('name', nargs='?', help='diagram name (omit to list all)')
    parser.add_argument('--write', action='store_true',
                        help='write diagram to its registered markdown file')
    parser.add_argument('--write-all', action='store_true',
                        help='update all registered markdown files')
    parser.add_argument('--check', action='store_true',
                        help='verify sync, width limits, and fence placement for all files')
    parser.add_argument('--validate', action='store_true',
                        help='run all functions and report width WARNs grouped by diagram name')
    parser.add_argument('--layout', nargs='+', type=int, metavar='W',
                        help='calculate box (L, R) positions for given inner widths')
    parser.add_argument('--margin', type=int, default=3,
                        help='left margin for --layout (default 3)')
    parser.add_argument('--gap', type=int, default=2,
                        help='gap between boxes for --layout (default 2)')

    args = parser.parse_args()

    if args.layout:
        layout(args.layout, margin=args.margin, gap=args.gap)

    elif args.write_all:
        for name in sorted(DIAGRAMS):
            _write(name)

    elif args.validate:
        width_issues = _audit_widths()
        if not width_issues:
            print('All diagrams clean — no width WARNs.')
        else:
            print(f'{len(width_issues)} diagram(s) have width WARNs:\n')
            for name, warns in width_issues.items():
                print(f'  {name}:')
                for w in warns:
                    print(f'    {w}')
        sys.exit(1 if width_issues else 0)

    elif args.check:
        all_ok = True
        col = max(len(n) for n in DIAGRAMS) + 2

        # 1. Sync check
        print('── Sync ──')
        for name, entry in sorted(DIAGRAMS.items()):
            result = _check(name)
            if result is None:
                status = 'NO BLOCK   '
                all_ok = False
            elif result:
                status = 'OK         '
            else:
                status = 'OUT OF SYNC'
                all_ok = False
            if result is None or not result:
                print(f'  {name:<{col}}  {status}  {entry["file"]}')
        if all_ok:
            print(f'  All {len(DIAGRAMS)} diagrams in sync.\n')

        # 2. Width check
        print('── Widths ──')
        width_issues = _audit_widths()
        if not width_issues:
            print(f'  All {len(DIAGRAMS)} diagrams within width limits.\n')
        else:
            all_ok = False
            for name, warns in width_issues.items():
                print(f'  {name}: {len(warns)} WARN(s)')
                for w in warns[:3]:
                    print(f'    {w}')

        # 3. Placement check
        print('── Placement ──')
        placement_issues = _audit_placement()
        if not placement_issues:
            print(f'  All {len(DIAGRAMS)} diagrams correctly placed before kb-grid.\n')
        else:
            all_ok = False
            for name, filepath, issue in placement_issues:
                print(f'  {name:<{col}}  {issue}  {filepath}')

        if not all_ok:
            sys.exit(1)

    elif args.name:
        if args.name not in DIAGRAMS:
            known = ', '.join(sorted(DIAGRAMS))
            print(f'ERROR: unknown diagram "{args.name}". Known: {known}', file=sys.stderr)
            sys.exit(1)
        if args.write:
            _write(args.name)
        else:
            lines = DIAGRAMS[args.name]['fn']()
            for line in lines:
                print(line)
            print(f'\n[w={_width_str(lines)}  lines={len(lines)}]', file=sys.stderr)

    else:
        _list()
