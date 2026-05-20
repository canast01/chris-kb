"""
VMware Core (ESXi, vSAN, NSX, vCenter, VCF) diagram functions.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)

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
