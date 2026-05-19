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
  bTop(l, r, tees)              — ┌────┐ with optional ┬ at tees
  bMid(l, r, text)              — │ text │  (text centred, truncated)
  bBot(l, r, tees)              — └────┘ with optional ┴ at tees
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


# ── Diagram registry ──────────────────────────────────────────────────────────
# 'file' is relative to the repo root (the directory containing mkdocs.yml).
# Add an entry here whenever you add a new diagram function above.

DIAGRAMS = {
    'vmware': {
        'fn': vmware_platform_landscape,
        'file': 'docs/virtualization/vmware/index.md',
        'description': 'VMware Platform Landscape — full stack: vSphere, vSAN, NSX, VCF, Aria',
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
