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

       def my_diagram():
           W2 = 95
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

2. Register it in DIAGRAMS at the bottom of this file.
3. Run:  python3 scripts/ascii_diagram_gen.py my_name --write

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


# ── Diagram registry ──────────────────────────────────────────────────────────
# 'file' is relative to the repo root (the directory containing mkdocs.yml).
# Add an entry here whenever you add a new diagram function above.

DIAGRAMS = {
    'vmware': {
        'fn': vmware_platform_landscape,
        'file': 'docs/virtualization/vmware/index.md',
        'description': 'VMware Platform Landscape — full stack: vSphere, vSAN, NSX, VCF, Aria',
    },
    'virtualization': {
        'fn': virtualization_platform_stack,
        'file': 'docs/virtualization/index.md',
        'description': 'VMware Platform Stack — VCF → vCenter/NSX-T/VxRail → ESXi → vSAN',
    },
    'storage': {
        'fn': enterprise_storage_landscape,
        'file': 'docs/storage/index.md',
        'description': 'Enterprise Storage Landscape — Pure, Dell, NetApp arrays + protocol layer',
    },
    'pure': {
        'fn': pure_storage_stack,
        'file': 'docs/storage/pure/index.md',
        'description': 'Pure Storage Stack — Pure1, FlashArray, FlashBlade, Evergreen, replication',
    },
    'dell': {
        'fn': dell_storage_portfolio,
        'file': 'docs/storage/dell/index.md',
        'description': 'Dell Storage Portfolio — PowerMax, PowerStore, Unity, PowerScale, Data Domain, ECS',
    },
    'netapp': {
        'fn': netapp_storage_stack,
        'file': 'docs/storage/netapp/index.md',
        'description': 'NetApp Storage Stack — ONTAP, StorageGRID, Keystone, SnapMirror, SnapCenter, FabricPool',
    },
    'cloud': {
        'fn': cloud_infrastructure_overview,
        'file': 'docs/cloud/index.md',
        'description': 'Cloud Infrastructure — AWS and Azure: IAM, compute, storage, networking, connectivity',
    },
    'aws': {
        'fn': aws_platform_stack,
        'file': 'docs/cloud/aws/index.md',
        'description': 'AWS Platform Stack — IAM, Compute, Networking, Storage, DB, Security, Connectivity',
    },
    'azure': {
        'fn': azure_platform_stack,
        'file': 'docs/cloud/azure/index.md',
        'description': 'Azure Platform Stack — Entra ID, Compute, Networking, Storage, DB, Security',
    },
    'compute': {
        'fn': compute_platform_overview,
        'file': 'docs/compute/index.md',
        'description': 'Compute Platform Overview — Linux and Windows Server side by side',
    },
    'linux': {
        'fn': linux_server_stack,
        'file': 'docs/compute/linux/index.md',
        'description': 'Linux Server Stack — architecture, networking, storage, ops, security, troubleshooting',
    },
    'windows': {
        'fn': windows_server_stack,
        'file': 'docs/compute/windows-server/index.md',
        'description': 'Windows Server Stack — architecture, networking, AD, ops, security, troubleshooting',
    },
    'san': {
        'fn': san_fabric_overview,
        'file': 'docs/san/index.md',
        'description': 'SAN Fabric Overview — Cisco MDS and Brocade FC fabric side by side',
    },
    'cisco-san': {
        'fn': cisco_san_stack,
        'file': 'docs/san/cisco/index.md',
        'description': 'Cisco SAN Stack — MDS 9000, DCNM, Nexus Dashboard, VSAN, Zoning, ISL',
    },
    'brocade': {
        'fn': brocade_san_stack,
        'file': 'docs/san/brocade/index.md',
        'description': 'Brocade SAN Stack — Fabric OS, SANnav, Zoning, ISL, MAPS, D-Port',
    },
    'vxrail': {
        'fn': vxrail_platform_stack,
        'file': 'docs/virtualization/vxrail/index.md',
        'description': 'VxRail Platform Stack — compute, networking, vSAN, LCM, ops, integration',
    },
    'vmware-ops': {
        'fn': vmware_operations_overview,
        'file': 'docs/virtualization/operations/index.md',
        'description': 'VMware Operations Overview — health checks, troubleshooting, runbooks, automation',
    },
    'vmware-ref': {
        'fn': vmware_reference_hub,
        'file': 'docs/virtualization/reference/index.md',
        'description': 'VMware Reference Hub — standards, inventory, upgrade readiness, quick reference',
    },
}


# ── Write / check helpers ─────────────────────────────────────────────────────

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Matches the first bare ``` block (no language tag on the opening line).
_BLOCK_RE = re.compile(r'^```\n.*?^```$', re.MULTILINE | re.DOTALL)


def _width_str(lines):
    widths = {len(l) for l in lines}
    if len(widths) == 1:
        return str(next(iter(widths)))
    return f'{min(widths)}-{max(widths)}'


def _write(name):
    """Replace the first bare ``` block in the registered file with fresh output."""
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
        print(f'  ERROR: no bare ``` block found in {entry["file"]}', file=sys.stderr)
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
            '  python3 scripts/ascii_diagram_gen.py --check              # verify sync\n'
            '  python3 scripts/ascii_diagram_gen.py --layout 20 20 47    # box positions\n'
        ),
    )
    parser.add_argument('name', nargs='?', help='diagram name (omit to list all)')
    parser.add_argument('--write', action='store_true',
                        help='write diagram to its registered markdown file')
    parser.add_argument('--write-all', action='store_true',
                        help='update all registered markdown files')
    parser.add_argument('--check', action='store_true',
                        help='verify all files match current diagram output')
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

    elif args.check:
        all_ok = True
        col = max(len(n) for n in DIAGRAMS) + 2
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
            print(f'  {name:<{col}}  {status}  {entry["file"]}')
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
