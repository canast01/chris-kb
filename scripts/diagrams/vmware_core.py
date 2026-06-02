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


@kb_diagram(
    'virt-ref-cluster-inventory',
    'docs/virtualization/reference/inventory/cluster-inventory/index.md',
    'vSphere Cluster Inventory — fields, HA/DRS config, vSAN/NSX flags, capacity tracking',
)
def virt_ref_cluster_inventory():
    """vSphere Cluster Inventory reference — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere — Cluster Inventory'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Per-cluster record capturing identity, feature enablement, and capacity state')))
    lines.append(R(bMid(IV_L, IV_R, 'One row per cluster; reviewed during capacity planning, audits, and change control')))
    lines.append(R(bMid(IV_L, IV_R, 'Fields: name, vCenter, environment, host count, HA, DRS, vSAN, NSX, resource pools')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity fields: overcommit ratio, datastore count, free memory headroom, notes')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Identity fields anchor the record · Feature flags drive operational decisions'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Identity'), bMid(B2_L, B2_R, 'Feature Flags'), bMid(B3_L, B3_R, 'Capacity'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cluster name'), bMid(B2_L, B2_R, 'HA enabled (Y/N)'), bMid(B3_L, B3_R, 'Host count'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vCenter FQDN'), bMid(B2_L, B2_R, 'DRS automation'), bMid(B3_L, B3_R, 'Datastore count'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Environment tag'), bMid(B2_L, B2_R, 'vSAN enabled'), bMid(B3_L, B3_R, 'vCPU overcommit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Datacenter / site'), bMid(B2_L, B2_R, 'NSX enabled'), bMid(B3_L, B3_R, 'RAM headroom %'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Owner / team'), bMid(B2_L, B2_R, 'EVC baseline'), bMid(B3_L, B3_R, 'Free datastore GB'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Identity + flags determine operational posture and expansion eligibility'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Name', 'vCenter', 'HA/DRS', 'vSAN/NSX', 'Capacity'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['cl-prod-compute', 'vcsa-prod-01', 'Y / Auto', 'Y / Y', '>25% free'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['cl-prod-edge', 'vcsa-prod-01', 'Y / Partial', 'N / Y', 'NFS backed'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['cl-dev-compute', 'vcsa-dev-01', 'Y / Auto', 'Y / N', 'Dev only'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: Dell PowerEdge nodes · vCenter appliance · vSAN disk groups · NSX transport nodes'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Cluster       = vSphere grouping of ESXi hosts sharing HA, DRS, and vSAN resources'))
    lines.append(txt_row('  HA            = High Availability; restarts VMs on surviving hosts after a host failure'))
    lines.append(txt_row('  DRS           = Distributed Resource Scheduler; balances VM workloads across cluster hosts'))
    lines.append(txt_row('  vSAN          = Virtual SAN; pooled storage from host-local NVMe/SSD disks per cluster'))
    lines.append(txt_row('  NSX           = Network virtualisation; software-defined networking overlay for the cluster'))
    lines.append(txt_row('  EVC           = Enhanced vMotion Compatibility; CPU baseline for cross-host live migration'))
    lines.append(txt_row('  DRS Auto      = DRS migrates VMs automatically to balance load without operator approval'))
    lines.append(txt_row('  Overcommit    = vCPU or vRAM assigned to VMs vs physical cores/RAM on the cluster'))
    lines.append(txt_row('  HA headroom   = Free memory reserved by admission control for VM restart on host failure'))
    lines.append(txt_row('  Resource pool = vSphere object limiting and reserving CPU/memory for a group of VMs'))
    lines.append(txt_row('  Environment   = Production / Non-Production / DR tag applied for policy and access scoping'))
    lines.append(txt_row('  Datacenter    = vSphere logical container grouping clusters, hosts, and datastores'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virt-ref-datastore-inventory',
    'docs/virtualization/reference/inventory/datastore-inventory/index.md',
    'vSphere Datastore Inventory — capacity, free space, type, connected hosts, VM count',
)
def virt_ref_datastore_inventory():
    """vSphere Datastore Inventory reference — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere — Datastore Inventory'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Per-datastore record for capacity management, storage policy audits, and VM placement')))
    lines.append(R(bMid(IV_L, IV_R, 'Fields: name, type (VMFS/vSAN/NFS/vVol), capacity, free space, hosts, VM count')))
    lines.append(R(bMid(IV_L, IV_R, 'Policy: default SPBM policy applied, datastore cluster membership, replication state')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert thresholds: 80% used = capacity warning; 90% used = critical; action required')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Datastore type determines protocol, redundancy model, and SPBM policy options'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Identity'), bMid(B2_L, B2_R, 'Capacity'), bMid(B3_L, B3_R, 'Connectivity'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Datastore name'), bMid(B2_L, B2_R, 'Total capacity (GB)'), bMid(B3_L, B3_R, 'Hosts connected'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Type (VMFS/NFS)'), bMid(B2_L, B2_R, 'Free space (GB)'), bMid(B3_L, B3_R, 'VM count'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Version/block sz'), bMid(B2_L, B2_R, 'Used %'), bMid(B3_L, B3_R, 'Storage policy'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Datastore cluster'), bMid(B2_L, B2_R, 'Thin provisioned'), bMid(B3_L, B3_R, 'Replication state'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NFS server/path'), bMid(B2_L, B2_R, 'Overcommit ratio'), bMid(B3_L, B3_R, 'Backup target tag'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Capacity and connectivity fields drive VM placement and storage DRS decisions'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Name', 'Type', 'Cap / Free', 'Hosts/VMs', 'Policy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['ds-vsan-prod-01', 'vSAN', '40TB / 12TB', '8 / 220', 'vSAN Default'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['ds-nfs-prod-01', 'NFS v3', '20TB / 6TB', '8 / 80', 'NetApp NFS'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['ds-vmfs-mgmt', 'VMFS 6', '4TB / 1.2TB', '4 / 15', 'Management'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: vSAN NVMe/SSD disk groups · NFS NAS heads · VMFS on FC/iSCSI LUNs'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  VMFS          = vSphere VMFS filesystem on block LUN (FC/iSCSI); cluster-aware locking'))
    lines.append(txt_row('  vSAN          = Pooled datastore from host-local NVMe/SSD managed by vSAN kernel module'))
    lines.append(txt_row('  NFS datastore = NAS share mounted over NFS v3/v4.1; managed at the NAS head level'))
    lines.append(txt_row('  vVol          = Virtual Volumes; per-VM objects on VASA-capable arrays (no VMFS needed)'))
    lines.append(txt_row('  SPBM          = Storage Policy Based Management; assigns storage capabilities to VMs'))
    lines.append(txt_row('  SDRS          = Storage DRS; balances space/IO across datastores in a datastore cluster'))
    lines.append(txt_row('  Thin prov.    = VM disk uses only written space; capacity grows on demand up to disk limit'))
    lines.append(txt_row('  Overcommit    = Total thin-provisioned capacity vs actual datastore physical capacity'))
    lines.append(txt_row('  Replication   = SnapMirror / vSAN Stretched / SRM protection state of the datastore'))
    lines.append(txt_row('  Backup target = Tag marking datastore as backup destination rather than primary workload'))
    lines.append(txt_row('  80% threshold = Standard alert point; capacity action required before hitting 90% usage'))
    lines.append(txt_row('  Datastore cluster = SDRS-managed group; VMs placed and migrated across member datastores'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virt-ref-host-inventory',
    'docs/virtualization/reference/inventory/host-inventory/index.md',
    'vSphere Host Inventory — hardware model, CPU/RAM, ESXi version, cluster, NIC/HBA config',
)
def virt_ref_host_inventory():
    """vSphere Host Inventory reference — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere — Host Inventory'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Per-ESXi-host record for lifecycle, capacity, and support — updated after each LCM cycle')))
    lines.append(R(bMid(IV_L, IV_R, 'Fields: hostname, cluster, hardware model, CPU (sockets/cores), RAM, ESXi build')))
    lines.append(R(bMid(IV_L, IV_R, 'Network: NIC count, VDS uplinks, NIC model; Storage: HBA count, HBA model, iDRAC IP')))
    lines.append(R(bMid(IV_L, IV_R, 'State: lockdown mode, maintenance mode, vSAN participation, host profile compliance')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Hardware identity drives upgrade eligibility · ESXi build drives HCL compliance state'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Identity'), bMid(B2_L, B2_R, 'Hardware'), bMid(B3_L, B3_R, 'State'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Hostname (FQDN)'), bMid(B2_L, B2_R, 'Model (PowerEdge)'), bMid(B3_L, B3_R, 'ESXi build'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cluster member'), bMid(B2_L, B2_R, 'CPU sockets/cores'), bMid(B3_L, B3_R, 'Lockdown mode'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vCenter managed'), bMid(B2_L, B2_R, 'RAM (GB total)'), bMid(B3_L, B3_R, 'Maint. mode'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'iDRAC IP addr'), bMid(B2_L, B2_R, 'NIC count/model'), bMid(B3_L, B3_R, 'vSAN member'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Site/rack'), bMid(B2_L, B2_R, 'HBA count/model'), bMid(B3_L, B3_R, 'Profile OK'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Hardware + state fields determine maintenance eligibility and capacity contribution'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Host', 'Model', 'CPU / RAM', 'ESXi build', 'State'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['esx-prod-01', 'R750xa', '2x18c/1.5TB', '8.0 U3', 'Active'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['esx-prod-02', 'R750xa', '2x18c/1.5TB', '8.0 U3', 'Active'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['esx-prod-03', 'R750xa', '2x18c/1.5TB', '8.0 U2', 'Needs patch'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: Dell PowerEdge servers · iDRAC OOB · NIC/HBA PCIe cards · vSAN NVMe disks'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  ESXi build    = Specific patch level (e.g. 8.0 U3 build 24022510); matches HCL entry'))
    lines.append(txt_row('  Lockdown mode = ESXi blocks direct SSH/shell; all management via vCenter API only'))
    lines.append(txt_row('  Host profile  = vCenter config template enforcing NTP, syslog, lockdown, NIC teaming'))
    lines.append(txt_row('  HBA           = Host Bus Adapter; FC card connecting ESXi host to SAN fabric'))
    lines.append(txt_row('  iDRAC         = Dell out-of-band management; independent of ESXi state for hardware ops'))
    lines.append(txt_row('  vSAN member   = Host contributing local NVMe/SSD disks to the vSAN datastore pool'))
    lines.append(txt_row('  Maint. mode   = ESXi state where VMs are evacuated prior to host maintenance work'))
    lines.append(txt_row('  HCL           = Hardware Compatibility List; ESXi build + model + driver must be listed'))
    lines.append(txt_row('  NIC teaming   = Multiple physical NICs bonded for redundancy and throughput on VDS'))
    lines.append(txt_row('  Profile OK    = Host configuration matches host profile; non-compliant hosts flagged'))
    lines.append(txt_row('  Site/rack     = Physical location tag used for anti-affinity and failure domain config'))
    lines.append(txt_row('  CPU sockets   = Physical CPU count; drives vCPU overcommit capacity for the cluster'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virt-ref-mgmt-tools',
    'docs/virtualization/reference/inventory/management-tools/index.md',
    'VMware Management Tools — vCenter, VxRail Manager, Aria Suite, NSX Manager, SDDC Manager',
)
def virt_ref_mgmt_tools():
    """VMware Management Tools inventory — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VMware — Management Tools'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Layered management toolstack for the VMware platform: compute, network, storage, lifecycle')))
    lines.append(R(bMid(IV_L, IV_R, 'Each tool manages a distinct layer; SDDC Manager orchestrates VCF lifecycle across all')))
    lines.append(R(bMid(IV_L, IV_R, 'Track: FQDN, version, admin URL, primary admin account, last upgrade date per tool')))
    lines.append(R(bMid(IV_L, IV_R, 'Access: all tools require LDAP/SSO + MFA; direct root is break-glass only, vault stored')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Compute/storage mgmt → network mgmt → operations and lifecycle management'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Compute & Storage'), bMid(B2_L, B2_R, 'Network & Security'), bMid(B3_L, B3_R, 'Ops & Lifecycle'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vCenter Server'), bMid(B2_L, B2_R, 'NSX Manager'), bMid(B3_L, B3_R, 'Aria Operations'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vSphere Client'), bMid(B2_L, B2_R, 'NSX UI / API'), bMid(B3_L, B3_R, 'Aria Logs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VxRail Manager'), bMid(B2_L, B2_R, 'Aria Networks'), bMid(B3_L, B3_R, 'Aria Automation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vSAN Skyline'), bMid(B2_L, B2_R, 'NSX Intelligence'), bMid(B3_L, B3_R, 'Aria Suite LCM'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SDDC Manager'), bMid(B2_L, B2_R, 'Load Balancer UI'), bMid(B3_L, B3_R, 'Skyline Advisor'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Hardware access: iDRAC / RACADM — independent of ESXi and vCenter for OOB management'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Tool', 'FQDN', 'Version', 'Admin URL', 'Last upgrade'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['vCenter', 'vcsa-prod-01', '8.0 U3', 'https://vcsa', '2025-03'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['NSX Manager', 'nsx-mgr-01', '4.1.2', 'https://nsx', '2025-03'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['VxRail Mgr', 'vxrail-mgr', '8.0.300', 'https://vxrm', '2025-04'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: management VMs on dedicated cluster · iDRAC on dedicated OOB network'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  vCenter Server  = Central management for ESXi clusters, VMs, storage, and networking'))
    lines.append(txt_row('  NSX Manager     = Control plane for NSX-T; manages segments, gateways, DFW policy'))
    lines.append(txt_row('  VxRail Manager  = Dell VxRail appliance manager; Mystic service orchestrates LCM'))
    lines.append(txt_row('  SDDC Manager    = VCF lifecycle orchestrator; manages domains, clusters, upgrades'))
    lines.append(txt_row('  Aria Operations = vROps; monitors vSphere/vSAN/NSX with ML anomaly detection'))
    lines.append(txt_row('  Aria Logs       = vRLI; log analytics for ESXi, vCenter, NSX, and infrastructure'))
    lines.append(txt_row('  Aria Automation = vRA; IaC and self-service cloud automation; Terraform backed'))
    lines.append(txt_row('  Aria Suite LCM  = Lifecycle Manager for Aria products; upgrades and cert rotation'))
    lines.append(txt_row('  Skyline Advisor = Proactive support; flags known issues before they cause outages'))
    lines.append(txt_row('  iDRAC           = Dell OOB management; hardware-level access independent of OS'))
    lines.append(txt_row('  Aria Networks   = vRNI; network flow visibility and micro-segmentation planning'))
    lines.append(txt_row('  Break-glass     = Emergency admin account in vault; used only when SSO/LDAP fails'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virt-ref-network-inventory',
    'docs/virtualization/reference/inventory/network-inventory/index.md',
    'vSphere Network Inventory — VDS switches, port groups, VLANs, uplinks, NSX segments',
)
def virt_ref_network_inventory():
    """vSphere Network Inventory reference — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere — Network Inventory'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Per-VDS record tracking port groups, VLAN assignments, uplinks, and NSX overlay config')))
    lines.append(R(bMid(IV_L, IV_R, 'VDS is the standard for production clusters; one VDS per cluster with defined uplinks')))
    lines.append(R(bMid(IV_L, IV_R, 'Port groups: Management, vMotion, vSAN, iSCSI/NFS, NSX TEP — each on distinct VLAN')))
    lines.append(R(bMid(IV_L, IV_R, 'NSX overlay: GENEVE-encapsulated traffic over TEP VLAN; logical segments over physical')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical NIC uplinks → VDS → port groups → VMs and VMkernel adapters'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VDS Identity'), bMid(B2_L, B2_R, 'Port Groups'), bMid(B3_L, B3_R, 'NSX Overlay'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VDS name'), bMid(B2_L, B2_R, 'PG-Mgmt VLAN 10'), bMid(B3_L, B3_R, 'TEP VLAN ID'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VDS version'), bMid(B2_L, B2_R, 'PG-vMotion VLAN 20'), bMid(B3_L, B3_R, 'Segment count'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MTU setting'), bMid(B2_L, B2_R, 'PG-vSAN VLAN 30'), bMid(B3_L, B3_R, 'Gateway IP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Uplink count'), bMid(B2_L, B2_R, 'PG-iSCSI VLAN 40'), bMid(B3_L, B3_R, 'Tier-0 name'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LB policy'), bMid(B2_L, B2_R, 'PG-VM trunk'), bMid(B3_L, B3_R, 'Edge cluster'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  VDS config + NSX overlay define all VM and VMkernel reachability across the cluster'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['VDS name', 'Version', 'MTU', 'Uplinks', 'LB policy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['vds-prod-01', '8.0', '9000', '2x 25GbE', 'Route by port'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['vds-mgmt-01', '8.0', '1500', '2x 10GbE', 'Active/standby'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['vds-edge-01', '8.0', '9000', '2x 25GbE', 'Route by port'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: 25/100GbE NICs · top-of-rack switches · physical VLAN trunks to hosts'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  VDS           = vSphere Distributed Switch; centrally managed in vCenter across hosts'))
    lines.append(txt_row('  Port group    = Named VLAN policy container on VDS; VMkernel or VM adapters attach here'))
    lines.append(txt_row('  VMkernel      = ESXi virtual NIC for Management, vMotion, vSAN, iSCSI, NFS traffic'))
    lines.append(txt_row('  VLAN          = 802.1Q tag isolating traffic at Layer 2 across the physical switch fabric'))
    lines.append(txt_row('  MTU 9000      = Jumbo frames required for vSAN and NSX TEP traffic (GENEVE overhead)'))
    lines.append(txt_row('  TEP           = Tunnel Endpoint; NSX GENEVE encapsulation source/dest per ESXi host'))
    lines.append(txt_row('  GENEVE        = NSX overlay protocol; carries logical segment traffic over underlay IP'))
    lines.append(txt_row('  Tier-0 GW     = NSX logical router peering with physical switches; handles N/S routing'))
    lines.append(txt_row('  Tier-1 GW     = NSX tenant router for workload E/W routing; connected to Tier-0'))
    lines.append(txt_row('  LB policy     = VDS uplink selection: route by port ID, IP hash, active/standby, LACP'))
    lines.append(txt_row('  Edge cluster  = NSX Edge transport nodes hosting Tier-0/1 gateways and load balancers'))
    lines.append(txt_row('  Segment       = NSX logical network; GENEVE-backed overlay equivalent of a VLAN port group'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virt-ref-version-inventory',
    'docs/virtualization/reference/inventory/version-inventory/index.md',
    'VMware Platform Version Inventory — vCenter, ESXi, vSAN, NSX, VxRail, Aria Suite versions',
)
def virt_ref_version_inventory():
    """VMware Platform Version Inventory reference — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VMware — Version Inventory'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Track product versions for all VMware components — required for LCM planning and support')))
    lines.append(R(bMid(IV_L, IV_R, 'Versions must be validated against the VMware Product Interoperability Matrix before upgrades')))
    lines.append(R(bMid(IV_L, IV_R, 'HCL status: ESXi build + server model + driver version must appear on VMware HCL')))
    lines.append(R(bMid(IV_L, IV_R, 'Support dates: track EoGS and EoTGS per product for lifecycle and budget planning')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Core platform versions → Aria Suite versions → support and compliance status'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Core Platform'), bMid(B2_L, B2_R, 'Aria Suite'), bMid(B3_L, B3_R, 'Compliance'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vCenter version'), bMid(B2_L, B2_R, 'Aria Automation'), bMid(B3_L, B3_R, 'HCL status'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ESXi build'), bMid(B2_L, B2_R, 'Aria Operations'), bMid(B3_L, B3_R, 'EoGS date'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vSAN version'), bMid(B2_L, B2_R, 'Aria Logs'), bMid(B3_L, B3_R, 'EoTGS date'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NSX-T version'), bMid(B2_L, B2_R, 'Aria LCM'), bMid(B3_L, B3_R, 'Interop matrix'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VxRail version'), bMid(B2_L, B2_R, 'SDDC Manager'), bMid(B3_L, B3_R, 'Patch level'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  EoGS components require immediate lifecycle action — unpatched = unsupported risk'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Product', 'Version', 'Build', 'EoGS', 'HCL/Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['vCenter', '8.0 U3', '24022515', '2027-10', 'Compliant'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['ESXi', '8.0 U3', '24022510', '2027-10', 'HCL OK'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['NSX-T', '4.1.2', '23287883', '2026-06', 'Check matrix'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: iDRAC firmware also tracked — updated via VxRail LCM bundle automatically'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  EoGS          = End of General Support; product still supported but no new features added'))
    lines.append(txt_row('  EoTGS         = End of Technical Guidance Support; only critical CVE patches provided'))
    lines.append(txt_row('  Interop matrix = VMware Product Interoperability Matrix; validates cross-product versions'))
    lines.append(txt_row('  HCL           = Hardware Compatibility List; ESXi build + model + driver must be listed'))
    lines.append(txt_row('  Build number  = Exact patch build identifier; used for support cases and HCL lookup'))
    lines.append(txt_row('  VxRail ver.   = Compound version: bundle includes ESXi + vCenter + iDRAC + VxRail Mgr'))
    lines.append(txt_row('  Patch level   = Latest applied patch; may differ from GA release version number'))
    lines.append(txt_row('  SDDC Manager  = VCF LCM; must match supported version for workload domain upgrades'))
    lines.append(txt_row('  LCM bundle    = VxRail single package covering all node components in one upgrade'))
    lines.append(txt_row('  Interop check = Required before any upgrade; prevents incompatible version combinations'))
    lines.append(txt_row('  Critical CVE  = High-severity security flaw; drives emergency patching outside LCM cycle'))
    lines.append(txt_row('  Upgrade path  = Validated intermediate version sequence needed to reach target version'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virt-std-access',
    'docs/virtualization/reference/standards/access-standard/index.md',
    'vSphere Access Standard — RBAC roles, SSO, lockdown mode, service accounts, audit logging',
)
def virt_std_access():
    """vSphere Access Standard — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere — Access Standard'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Access standard governing authentication, authorisation, and audit for the vSphere platform')))
    lines.append(R(bMid(IV_L, IV_R, 'All management access via vCenter SSO backed by Active Directory; direct host access blocked')))
    lines.append(R(bMid(IV_L, IV_R, 'Three-tier RBAC: Administrator / Operator (custom role) / Read-only; no built-in admin sharing')))
    lines.append(R(bMid(IV_L, IV_R, 'Service accounts: one per integration, least-privilege, vault-stored, rotated 90 days')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Authentication gate → authorisation scope → audit trail for all management actions'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Authentication'), bMid(B2_L, B2_R, 'Authorisation'), bMid(B3_L, B3_R, 'Audit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vCenter SSO + AD'), bMid(B2_L, B2_R, 'Administrator role'), bMid(B3_L, B3_R, 'vCenter events'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MFA enforcement'), bMid(B2_L, B2_R, 'Operator (custom)'), bMid(B3_L, B3_R, 'iDRAC audit log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Lockdown mode'), bMid(B2_L, B2_R, 'Read-only role'), bMid(B3_L, B3_R, 'Syslog to SIEM'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Service accounts'), bMid(B2_L, B2_R, 'Scope: DC/cluster'), bMid(B3_L, B3_R, 'Login attempts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Break-glass acct'), bMid(B2_L, B2_R, 'Least privilege'), bMid(B3_L, B3_R, 'Role changes'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  All three pillars required: no auth without logging, no access without defined role'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Access tier', 'Auth method', 'vCenter role', 'Scope', 'Review freq'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Administrator', 'SSO + AD + MFA', 'Administrator', 'Datacenter', 'Quarterly'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Operator', 'SSO + AD + MFA', 'Custom ops role', 'Cluster', 'Quarterly'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Read-only', 'SSO + AD', 'Read-only', 'Datacenter', 'Annual'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: ESXi hosts in lockdown mode; iDRAC on OOB VLAN; vCenter on management cluster'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  vCenter SSO   = Single Sign-On; authentication broker for vCenter and connected services'))
    lines.append(txt_row('  Lockdown mode = ESXi blocks direct SSH/shell; all access via vCenter API path only'))
    lines.append(txt_row('  RBAC          = Role-Based Access Control; vCenter permissions assigned via role+scope'))
    lines.append(txt_row('  Administrator = Full vCenter access; restricted to named infra team members only'))
    lines.append(txt_row('  Operator role = Custom role with write permissions scoped to specific operations'))
    lines.append(txt_row('  Read-only     = No changes; appropriate for monitoring and helpdesk triage access'))
    lines.append(txt_row('  Service acct  = Non-human account for tool integration; one per tool, least-privilege'))
    lines.append(txt_row('  Break-glass   = Emergency admin stored in vault; retrieved on MFA failure or lockout'))
    lines.append(txt_row('  Least priv.   = Grant only the minimum permissions required for the role to function'))
    lines.append(txt_row('  Propagate     = vCenter permission flag that applies a role to all child objects too'))
    lines.append(txt_row('  Scope         = vCenter object level where permission is assigned: DC, cluster, folder'))
    lines.append(txt_row('  SIEM          = Security Information and Event Management; receives vSphere syslog events'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virt-std-cluster',
    'docs/virtualization/reference/standards/cluster-standard/index.md',
    'vSphere Cluster Standard — HA admission control, DRS settings, EVC mode, capacity rules',
)
def virt_std_cluster():
    """vSphere Cluster Standard — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere — Cluster Standard'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Standard configuration for all vSphere clusters — HA, DRS, EVC, and naming enforcement')))
    lines.append(R(bMid(IV_L, IV_R, 'HA admission control: percentage-based; reserve capacity for N host failures (default N=1)')))
    lines.append(R(bMid(IV_L, IV_R, 'DRS: Fully Automated for compute clusters; Partially Automated for edge/management clusters')))
    lines.append(R(bMid(IV_L, IV_R, 'Naming: cl-{env}-{function}-{nn}; consistent naming enables automated policy application')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  HA protects availability · DRS optimises performance · EVC enables live migration'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'HA Settings'), bMid(B2_L, B2_R, 'DRS Settings'), bMid(B3_L, B3_R, 'EVC & Sizing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Enabled: always'), bMid(B2_L, B2_R, 'Fully Automated'), bMid(B3_L, B3_R, 'EVC: enabled'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Admission: % based'), bMid(B2_L, B2_R, 'Threshold: 65%'), bMid(B3_L, B3_R, 'CPU baseline set'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Heartbeat: 5 min'), bMid(B2_L, B2_R, 'Predictive DRS'), bMid(B3_L, B3_R, 'Min 3 hosts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Restart priority'), bMid(B2_L, B2_R, 'Affinity rules'), bMid(B3_L, B3_R, 'Max 64 hosts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Failure condition'), bMid(B2_L, B2_R, 'Resource pools'), bMid(B3_L, B3_R, 'Homogeneous HW'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Settings applied via host profiles and cluster configuration; reviewed quarterly'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Setting', 'Production', 'Dev/Test', 'Edge', 'Management'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['HA', 'Enabled', 'Enabled', 'Enabled', 'Enabled'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['DRS', 'Fully Auto', 'Fully Auto', 'Partial', 'Partial'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['EVC', 'Required', 'Required', 'Optional', 'Required'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: consistent hardware generation per cluster required for EVC baseline stability'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  HA            = High Availability; monitors hosts and restarts VMs on failure detection'))
    lines.append(txt_row('  Admission ctrl = HA reserves CPU/RAM capacity for N host failure scenarios'))
    lines.append(txt_row('  DRS           = Distributed Resource Scheduler; migrates VMs to balance cluster load'))
    lines.append(txt_row('  Fully Auto    = DRS applies vMotion migrations without operator approval'))
    lines.append(txt_row('  Partial Auto  = DRS recommends but operator must approve each migration'))
    lines.append(txt_row('  EVC           = Enhanced vMotion Compatibility; masks newer CPU features for migration'))
    lines.append(txt_row('  Affinity rule = DRS rule keeping or separating specific VMs across hosts'))
    lines.append(txt_row('  Resource pool = vSphere container applying CPU/RAM shares and limits to VM groups'))
    lines.append(txt_row('  Predictive DRS = DRS integration with Aria Operations for workload-aware pre-migration'))
    lines.append(txt_row('  Heartbeat     = HA heartbeat network; secondary check when management network lost'))
    lines.append(txt_row('  Homogeneous   = Same CPU generation across cluster hosts; required for stable EVC'))
    lines.append(txt_row('  Restart prio  = HA restart order for VMs; high priority VMs restarted before medium'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virt-std-datastore',
    'docs/virtualization/reference/standards/datastore-standard/index.md',
    'vSphere Datastore Standard — storage policies, naming, sizing thresholds, vSAN rules',
)
def virt_std_datastore():
    """vSphere Datastore Standard — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere — Datastore Standard'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Standards governing datastore naming, sizing, storage policy assignment, and vSAN config')))
    lines.append(R(bMid(IV_L, IV_R, 'Naming: ds-{type}-{site}-{nn}; type = vsan / nfs / vmfs; site = datacenter code')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity: 80% used triggers warning; 90% used triggers critical and blocks new VMs')))
    lines.append(R(bMid(IV_L, IV_R, 'SPBM: all VMs must have an explicit storage policy; no VMs on default policy in prod')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Naming standard + SPBM policy + capacity thresholds define the datastore compliance state'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Naming Rules'), bMid(B2_L, B2_R, 'Capacity Rules'), bMid(B3_L, B3_R, 'Policy Rules'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ds-{type}-{site}'), bMid(B2_L, B2_R, '80% = warn'), bMid(B3_L, B3_R, 'SPBM required'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Lowercase only'), bMid(B2_L, B2_R, '90% = critical'), bMid(B3_L, B3_R, 'vSAN FTT=1 min'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No spaces/dots'), bMid(B2_L, B2_R, 'Max 64TB VMFS'), bMid(B3_L, B3_R, 'Dedup/compress'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Site code suffix'), bMid(B2_L, B2_R, 'SDRS at 85%'), bMid(B3_L, B3_R, 'Backup tag reqd'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Sequential nn'), bMid(B2_L, B2_R, 'Thin < 150%'), bMid(B3_L, B3_R, 'Tiering policy'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Non-compliant datastores flagged in vCenter; reviewed in weekly capacity meeting'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Type', 'Naming example', 'Max size', 'SPBM policy', 'Threshold'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['vSAN', 'ds-vsan-lon-01', 'Cluster-bound', 'vSAN FTT=1', '80% warn'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['NFS', 'ds-nfs-lon-01', 'NAS-bound', 'NetApp Gold', '80% warn'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['VMFS', 'ds-vmfs-lon-01', '64TB', 'SAN Standard', '80% warn'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: NVMe/SSD disk groups (vSAN) · NFS NAS arrays · FC/iSCSI LUNs (VMFS)'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SPBM          = Storage Policy Based Management; VM-level storage capability assignment'))
    lines.append(txt_row('  FTT           = Failures To Tolerate; vSAN redundancy level (FTT=1 means 1 host failure ok)'))
    lines.append(txt_row('  SDRS          = Storage DRS; migrates VMs when datastore exceeds utilisation threshold'))
    lines.append(txt_row('  Datastore cluster = SDRS-managed group; enables automated space and IO balancing'))
    lines.append(txt_row('  Thin overcommit = Provisioned thin capacity as ratio of physical; max 150% recommended'))
    lines.append(txt_row('  Dedup/compress = vSAN space efficiency; reduces effective capacity needed per VM'))
    lines.append(txt_row('  Backup tag    = Custom vCenter tag marking backup target datastores vs workload stores'))
    lines.append(txt_row('  Tiering policy = FabricPool / vSAN policy for cold data migration to capacity tier'))
    lines.append(txt_row('  Sequential nn = Two-digit suffix (-01, -02) for ordered datastore identification'))
    lines.append(txt_row('  Site code     = Two-to-four letter datacenter code embedded in datastore name'))
    lines.append(txt_row('  64TB VMFS     = Maximum VMFS 6 datastore size on a single LUN'))
    lines.append(txt_row('  Capacity warn = 80% threshold triggers capacity planning; 90% blocks new provisioning'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virt-std-host-build',
    'docs/virtualization/reference/standards/host-build-standard/index.md',
    'ESXi Host Build Standard — NTP, DNS, syslog, lockdown, NIC teaming, host profile',
)
def virt_std_host_build():
    """ESXi Host Build Standard — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'ESXi — Host Build Standard'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Baseline configuration applied to every ESXi host via host profile — enforced in vCenter')))
    lines.append(R(bMid(IV_L, IV_R, 'NTP: 2+ NTP servers; drift < 250ms; required for vSAN, vMotion, and Kerberos auth')))
    lines.append(R(bMid(IV_L, IV_R, 'Syslog: forwarded to centralised SIEM; retention 90 days minimum at SIEM level')))
    lines.append(R(bMid(IV_L, IV_R, 'Lockdown: Normal mode on all production hosts; exception list for LCM service accounts')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Build standard items enforced via host profile; non-compliant hosts flagged in vCenter'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Time & DNS'), bMid(B2_L, B2_R, 'Security'), bMid(B3_L, B3_R, 'Networking'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NTP servers x2'), bMid(B2_L, B2_R, 'Lockdown: Normal'), bMid(B3_L, B3_R, 'VDS uplinks x2'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DNS primary/sec'), bMid(B2_L, B2_R, 'SSH: disabled'), bMid(B3_L, B3_R, 'MTU: 9000'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DNS suffix list'), bMid(B2_L, B2_R, 'ESXi Shell: off'), bMid(B3_L, B3_R, 'LACP / failover'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Syslog target'), bMid(B2_L, B2_R, 'VIB: PartnerSupp'), bMid(B3_L, B3_R, 'VMkernel IPs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Drift < 250ms'), bMid(B2_L, B2_R, 'Host profile'), bMid(B3_L, B3_R, 'iDRAC VLAN'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Host profile compliance checked after every LCM patch; non-compliant hosts remediated'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Item', 'Required value', 'Enforced by', 'Check', 'Remediation'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Lockdown mode', 'Normal', 'Host profile', 'vCenter UI', 'Profile apply'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['SSH service', 'Stopped/off', 'Host profile', 'esxcli check', 'Profile apply'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['NTP drift', '< 250ms', 'NTP daemon', 'ntpq -p', 'Sync NTP servers'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: management NIC on VLAN 10; iDRAC on OOB VLAN; vSAN NIC on VLAN 30'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Host profile  = vCenter template enforcing consistent config across all cluster hosts'))
    lines.append(txt_row('  Lockdown mode = ESXi state blocking direct SSH; all management routed through vCenter'))
    lines.append(txt_row('  Exception list = Accounts permitted direct host access in lockdown (VxRail Mgr SVC acct)'))
    lines.append(txt_row('  VIB acceptance = Host policy for VIB package signing: VMwareCertified > PartnerSupported'))
    lines.append(txt_row('  NTP drift     = Clock offset tolerance; >250ms breaks vSAN resync and Kerberos tickets'))
    lines.append(txt_row('  ESXi Shell    = TSM service; disabled in production to reduce attack surface'))
    lines.append(txt_row('  SSH service   = TSM-SSH service; disabled in production; enabled only for troubleshooting'))
    lines.append(txt_row('  Syslog target = Remote syslog server (SIEM) receiving all ESXi log events'))
    lines.append(txt_row('  LACP          = Link Aggregation Control Protocol; bonds uplinks for bandwidth and failover'))
    lines.append(txt_row('  PartnerSupp   = VIB acceptance level allowing Dell, NetApp, and VMware-signed VIBs'))
    lines.append(txt_row('  VMkernel IP   = Per-VLAN ESXi virtual NIC IP: management, vMotion, vSAN, iSCSI/NFS'))
    lines.append(txt_row('  iDRAC VLAN    = OOB management VLAN for iDRAC; isolated from ESXi and VM traffic'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virt-std-naming',
    'docs/virtualization/reference/standards/naming-standard/index.md',
    'vSphere Naming Standard — conventions for clusters, hosts, VMs, datastores, port groups',
)
def virt_std_naming():
    """vSphere Naming Standard — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere — Naming Standard'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Consistent naming conventions for all vSphere objects — enables automation and auditing')))
    lines.append(R(bMid(IV_L, IV_R, 'Pattern: {prefix}-{env}-{function}-{site}-{nn} — lowercase, hyphens, no spaces or dots')))
    lines.append(R(bMid(IV_L, IV_R, 'Environment codes: prod / nprod / dev / dr; site codes: 3-letter DC identifier')))
    lines.append(R(bMid(IV_L, IV_R, 'Enforced via vCenter tags and automated naming check in CI/CD provisioning pipelines')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Consistent names drive automation, CMDB population, and audit traceability'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Infrastructure'), bMid(B2_L, B2_R, 'Networking'), bMid(B3_L, B3_R, 'Storage'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cluster: cl-*'), bMid(B2_L, B2_R, 'VDS: vds-{env}'), bMid(B3_L, B3_R, 'DS: ds-{type}'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Host: esx-{site}'), bMid(B2_L, B2_R, 'PG-{vlan}-{func}'), bMid(B3_L, B3_R, 'ds-vsan-{site}'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VM: {app}-{env}'), bMid(B2_L, B2_R, 'NSX seg: seg-*'), bMid(B3_L, B3_R, 'ds-nfs-{site}'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Template: tmpl-*'), bMid(B2_L, B2_R, 'Tier-0: t0-{site}'), bMid(B3_L, B3_R, 'ds-vmfs-{site}'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vCenter: vcsa-*'), bMid(B2_L, B2_R, 'Tier-1: t1-{func}'), bMid(B3_L, B3_R, 'Policy: pol-{tier}'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Non-compliant names flagged by naming lint script in provisioning pipeline'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Object', 'Pattern', 'Example', 'Max len', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Cluster', 'cl-{env}-{fn}-{nn}', 'cl-prod-compute-01', '32', 'Lowercase'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['ESXi host', 'esx-{site}-{nn}', 'esx-lon-01', '15', 'FQDN used'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['VM', '{app}-{env}-{nn}', 'app1-prod-01', '15', 'FQDN match'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: server naming aligned with iDRAC hostname and rack label for traceability'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Prefix        = Object type identifier: cl (cluster), esx (host), ds (datastore), pg (portgroup)'))
    lines.append(txt_row('  Environment   = prod / nprod / dev / dr — applied to clusters, VMs, and datastores'))
    lines.append(txt_row('  Site code     = 3-letter datacenter ID (lon, ams, nyc); embedded in host and DS names'))
    lines.append(txt_row('  Function      = Role identifier in cluster/VDS name: compute, edge, mgmt, vdi, db'))
    lines.append(txt_row('  Sequential nn = Zero-padded two-digit counter per site/env: -01, -02, -03'))
    lines.append(txt_row('  FQDN          = Fully Qualified Domain Name; VM hostname must match FQDN in DNS'))
    lines.append(txt_row('  NSX segment   = seg-{function}-{vlan}: seg-web-100, seg-db-200, seg-app-300'))
    lines.append(txt_row('  Port group    = PG-{VLAN ID}-{purpose}: PG-10-Mgmt, PG-20-vMotion, PG-30-vSAN'))
    lines.append(txt_row('  Template      = tmpl-{os}-{version}: tmpl-rhel9-2024q4, tmpl-win2022-2024q4'))
    lines.append(txt_row('  Policy name   = pol-{tier}: pol-gold, pol-silver, pol-bronze for storage SPBM'))
    lines.append(txt_row('  Lint script   = CI/CD pre-provisioning check that validates names against naming regex'))
    lines.append(txt_row('  CMDB populate = Automated CMDB entry creation triggered by consistent naming pattern'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'virt-std-vm',
    'docs/virtualization/reference/standards/vm-standard/index.md',
    'vSphere VM Standard — vHW version, CPU/RAM sizing tiers, snapshot policy, VMware Tools',
)
def virt_std_vm():
    """vSphere VM Standard — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere — VM Standard'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Baseline VM configuration standard — hardware version, sizing, snapshot, and tools policy')))
    lines.append(R(bMid(IV_L, IV_R, 'Hardware version: vHW 21 minimum (ESXi 8.0); upgrade at OS patching cycle if feasible')))
    lines.append(R(bMid(IV_L, IV_R, 'Sizing tiers: XS/S/M/L/XL — defined by vCPU and RAM; over-sized VMs flagged by DRS')))
    lines.append(R(bMid(IV_L, IV_R, 'Snapshots: max 3 per VM, max 14 days age; monitored and alerted via Aria Operations')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Hardware version → OS template → sizing tier → storage policy → snapshot compliance'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Hardware Config'), bMid(B2_L, B2_R, 'Sizing Policy'), bMid(B3_L, B3_R, 'Lifecycle'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vHW 21 minimum'), bMid(B2_L, B2_R, 'XS: 1vCPU/2GB'), bMid(B3_L, B3_R, 'VMware Tools'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CPU hot-add: off'), bMid(B2_L, B2_R, 'S: 2vCPU/4GB'), bMid(B3_L, B3_R, 'Auto-update on'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RAM hot-add: off'), bMid(B2_L, B2_R, 'M: 4vCPU/8GB'), bMid(B3_L, B3_R, 'Snapshot: max 3'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCSI: PVSCSI'), bMid(B2_L, B2_R, 'L: 8vCPU/16GB'), bMid(B3_L, B3_R, 'Max age 14 days'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NIC: VMXNET3'), bMid(B2_L, B2_R, 'XL: 16vCPU/32+'), bMid(B3_L, B3_R, 'Thin disks'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Templates enforce vHW version and NIC/SCSI controller types at provisioning time'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Setting', 'Standard value', 'Exception path', 'Enforced by', 'Alert'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['vHW version', '21+', 'Change ticket', 'Template', 'Aria Ops'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Snapshot age', '≤ 14 days', 'CAB approval', 'Aria monitor', 'Alert email'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['VMware Tools', 'Current', 'Frozen OS', 'Tools check', 'Aria Ops'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: VMs on vSAN datastores with SPBM policy; PVSCSI for all non-legacy workloads'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  vHW version   = VMware Virtual Hardware version; controls available VM features and devices'))
    lines.append(txt_row('  CPU hot-add   = Add vCPUs without reboot; disabled — causes NUMA imbalance in most OSes'))
    lines.append(txt_row('  RAM hot-add   = Add vRAM without reboot; disabled — OS fragmentation risk, keep off'))
    lines.append(txt_row('  PVSCSI        = Paravirtual SCSI controller; higher throughput and lower CPU than LSI Logic'))
    lines.append(txt_row('  VMXNET3       = Paravirtual NIC; much higher performance than E1000; required standard'))
    lines.append(txt_row('  VMware Tools  = Guest agent enabling quiesced snapshots, heartbeat, IP reporting'))
    lines.append(txt_row('  Thin disk     = VM disk uses only written bytes; grows to allocated maximum on demand'))
    lines.append(txt_row('  Snapshot      = Point-in-time VM state; delta disk accumulates writes; delete after use'))
    lines.append(txt_row('  Sizing tier   = Predefined vCPU/RAM combination; prevents arbitrary VM sizing'))
    lines.append(txt_row('  SPBM policy   = Storage policy assigned at provisioning; defines redundancy and tiering'))
    lines.append(txt_row('  Template      = Golden image VM converted to template; enforces vHW and controller type'))
    lines.append(txt_row('  DRS oversized = DRS flag when VM has more vCPUs than it uses; triggers right-size alert'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'nsx-architecture-how-it-works',
    'docs/virtualization/vmware/nsx/architecture/how-it-works/index.md',
    'NSX Architecture — how data flows through control plane, overlay, DFW, and Edge Nodes',
)
def nsx_architecture_how_it_works():
    """NSX How It Works — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NSX Architecture — How It Works'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'NSX separates control, management, and data planes; overlay runs on each ESXi host')))
    lines.append(R(bMid(IV_L, IV_R, 'Control plane: NSX Manager (3-node cluster) pushes config to Transport Nodes via RPC')))
    lines.append(R(bMid(IV_L, IV_R, 'Data plane: DLR runs on each host; Geneve encapsulates E-W traffic between TEPs')))
    lines.append(R(bMid(IV_L, IV_R, 'North-South: SR on Edge Node routes to physical; BGP peers with ToR switches')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  NSX Manager config → Transport Node kernel modules → Geneve overlay → Edge SR → physical'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Control Plane'), bMid(B2_L, B2_R, 'Data Plane (E-W)'), bMid(B3_L, B3_R, 'Edge (N-S)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NSX Manager × 3'), bMid(B2_L, B2_R, 'DLR on each host'), bMid(B3_L, B3_R, 'Service Router'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Config RPC push'), bMid(B2_L, B2_R, 'Geneve VNI tag'), bMid(B3_L, B3_R, 'BGP to ToR'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TEP pool assign'), bMid(B2_L, B2_R, 'TEP src/dst'), bMid(B3_L, B3_R, 'SNAT / DNAT'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DFW rule push'), bMid(B2_L, B2_R, 'DFW at vNIC'), bMid(B3_L, B3_R, 'LB service'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Segment create'), bMid(B2_L, B2_R, 'BUM replication'), bMid(B3_L, B3_R, 'GRE/IPsec VPN'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  VM-to-VM same host: no Geneve; DFW filters and DLR forwards in-kernel directly'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Traffic type', 'Entry point', 'Path', 'Exit point', 'Protocol'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['E-W same host', 'VM vNIC', 'DFW → DLR', 'Target VM', 'None/in-kernel'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['E-W diff host', 'VM vNIC', 'DFW→TEP', 'TEP→DFW→VM', 'Geneve/UDP 6081'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['N-S outbound', 'VM → T1 DR', 'T1 SR → T0 SR', 'ToR→upstream', 'BGP ECMP'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['N-S inbound', 'ToR → T0 SR', 'T0 → T1 SR', 'DNAT → VM', 'BGP + SNAT'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: ESXi hosts · N-VDS/VDS with TEP vmknic · Edge VMs on bare-metal or VM form'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  DLR           = Distributed Logical Router; runs as kernel module on every ESXi host'))
    lines.append(txt_row('  SR            = Service Router; runs on Edge Node; handles stateful N-S services'))
    lines.append(txt_row('  TEP           = Tunnel End Point; vmknic IP used as Geneve encap src/dst per host'))
    lines.append(txt_row('  Geneve        = Generic Network Virtualization Encapsulation; NSX overlay protocol'))
    lines.append(txt_row('  VNI           = Virtual Network Identifier; 24-bit segment ID in Geneve header'))
    lines.append(txt_row('  DFW           = Distributed Firewall; stateful L4-L7 kernel-level filter at each vNIC'))
    lines.append(txt_row('  BUM           = Broadcast/Unknown-unicast/Multicast; replicated via head-end or multicast'))
    lines.append(txt_row('  T0 gateway    = Tier-0 Logical Router; provider-level; BGP peers with physical fabric'))
    lines.append(txt_row('  T1 gateway    = Tier-1 Logical Router; tenant-level; connects segments to T0'))
    lines.append(txt_row('  BGP ECMP      = T0 uses ECMP over multiple Edge uplinks for active-active North-South'))
    lines.append(txt_row('  N-VDS         = NSX-managed vSwitch; hosts TEP vmknic and overlay traffic'))
    lines.append(txt_row('  ToR           = Top-of-Rack physical switch; BGP peer for T0 gateway uplinks'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'nsx-architecture-design-standards',
    'docs/virtualization/vmware/nsx/architecture/design-standards/index.md',
    'NSX Architecture Design Standards — transport zones, Edge sizing, T0/T1 design, IP pools',
)
def nsx_architecture_design_standards():
    """NSX Architecture Design Standards — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NSX Architecture — Design Standards'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'NSX design standards: transport zones, T0/T1 gateway tiers, Edge sizing, IP pools')))
    lines.append(R(bMid(IV_L, IV_R, 'Two transport zones: VLAN TZ (N-S Edge uplinks) + Overlay TZ (E-W tenant segments)')))
    lines.append(R(bMid(IV_L, IV_R, 'T0 per environment (provider); T1 per tenant or application group (consumer)')))
    lines.append(R(bMid(IV_L, IV_R, 'Edge clusters: min 2 Edge Nodes for HA; bare-metal for high-throughput workloads')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Transport Zone design → Gateway tier → Edge cluster → IP pool → segment naming'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Transport Zones'), bMid(B2_L, B2_R, 'Gateway Design'), bMid(B3_L, B3_R, 'Edge Sizing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Overlay TZ'), bMid(B2_L, B2_R, 'T0: provider'), bMid(B3_L, B3_R, 'Small: 2vCPU'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VLAN TZ'), bMid(B2_L, B2_R, 'T1: per tenant'), bMid(B3_L, B3_R, 'Medium: 4vCPU'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No cross-TZ'), bMid(B2_L, B2_R, 'T0 BGP ECMP'), bMid(B3_L, B3_R, 'Large: 8vCPU'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Host TZ attach'), bMid(B2_L, B2_R, 'T1 static/OSPF'), bMid(B3_L, B3_R, 'Bare-metal max'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Multi-TZ Edge'), bMid(B2_L, B2_R, 'NAT on T1 SR'), bMid(B3_L, B3_R, 'Min 2 per site'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  TEP pool: /24 minimum; no overlap with VM or management networks; MTU 1600+ on pNIC'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Design area', 'Standard', 'Why', 'Verify', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['TEP pool', '/24 non-overlap', 'No routing', 'Ping TEPs', 'MTU 1600'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Edge HA', '2 nodes min', 'SR failover', 'BFD state', 'A/S or A/A'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['T0 uplinks', '2 per Edge', 'ECMP / HA', 'BGP peers', 'VLAN TZ'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Seg naming', '<env>-<app>', 'Readability', 'Audit', 'No spaces'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: pNIC MTU ≥ 1600 for Geneve · dedicated TEP VLAN · ToR BGP peer config'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Overlay TZ    = Transport Zone spanning all hosts; carries Geneve-encapsulated E-W traffic'))
    lines.append(txt_row('  VLAN TZ       = Transport Zone for Edge uplinks; carries native VLAN traffic to physical'))
    lines.append(txt_row('  TEP pool      = IP pool assigned to hosts for Geneve src/dst; one IP per host TEP vmknic'))
    lines.append(txt_row('  T0 gateway    = Provider Logical Router; BGP to physical; ECMP over multiple Edge uplinks'))
    lines.append(txt_row('  T1 gateway    = Tenant Logical Router; connects segments upstream to T0'))
    lines.append(txt_row('  Edge cluster  = Group of Edge Nodes hosting Service Routers; provides N-S HA'))
    lines.append(txt_row('  BFD           = Bidirectional Forwarding Detection; fast failover between Edge uplinks'))
    lines.append(txt_row('  ECMP          = Equal-Cost Multi-Path; distributes N-S traffic across multiple Edge uplinks'))
    lines.append(txt_row('  Active/Standby = SR runs on one Edge; fails to standby if primary fails'))
    lines.append(txt_row('  Active/Active  = Two SRs active; stateless traffic only; requires external LB for SPI'))
    lines.append(txt_row('  MTU 1600      = Minimum pNIC MTU for Geneve (50-byte overhead) + standard 1500 payload'))
    lines.append(txt_row('  Seg naming    = Consistent segment naming prevents confusion in large environments'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'nsx-architecture-integrations',
    'docs/virtualization/vmware/nsx/architecture/integrations/index.md',
    'NSX Integrations — vCenter, Aria suite, Active Directory IDFW, third-party tools',
)
def nsx_architecture_integrations():
    """NSX Architecture Integrations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NSX Architecture — Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'NSX integrations: vCenter, Aria suite, Active Directory IDFW, and third-party tools')))
    lines.append(R(bMid(IV_L, IV_R, 'vCenter: registers NSX Manager as plugin; VM tag sync via Compute Manager')))
    lines.append(R(bMid(IV_L, IV_R, 'IDFW: AD group membership drives DFW rules per user; key for VDI environments')))
    lines.append(R(bMid(IV_L, IV_R, 'Aria Network Insight: flow-level visibility; Aria Operations: health and alert')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  vCenter sync → VM tagging → dynamic groups → DFW auto-update → policy enforcement'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VMware Stack'), bMid(B2_L, B2_R, 'Identity / AD'), bMid(B3_L, B3_R, 'Third-Party'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vCenter plug-in'), bMid(B2_L, B2_R, 'LDAP/AD join'), bMid(B3_L, B3_R, 'Partner LB'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VM tag sync'), bMid(B2_L, B2_R, 'IDFW rules'), bMid(B3_L, B3_R, 'IDS/IPS feed'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Aria Operations'), bMid(B2_L, B2_R, 'User → VM map'), bMid(B3_L, B3_R, 'ServiceNow'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Aria Net.Insight'), bMid(B2_L, B2_R, 'Group member'), bMid(B3_L, B3_R, 'Ansible/Terraform'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Tanzu / TKG'), bMid(B2_L, B2_R, 'Policy auto'), bMid(B3_L, B3_R, 'Panorama/FMC'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Compute Manager (vCenter) registration is prerequisite for VM-tag dynamic group policy'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Integration', 'Protocol', 'NSX feature', 'Benefit', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['vCenter', 'REST API', 'Tag sync', 'Dyn. groups', 'Comp. Mgr'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['AD / LDAP', 'LDAPS', 'IDFW rules', 'User-based FW', 'VDI use'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Aria NI', 'Flow export', 'Visibility', 'Flow map', 'IPFIX parse'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Terraform', 'NSX provider', 'IaC deploy', 'Repeatability', 'VCS pipeline'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: vCenter API access from NSX Manager · AD reachable via management network'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Compute Manager = vCenter registered in NSX Manager; source of VM inventory and tags'))
    lines.append(txt_row('  VM tag          = vSphere tag applied to VM; synced to NSX for dynamic group membership'))
    lines.append(txt_row('  Dynamic group   = NSX group whose membership auto-updates based on tag, OS, or name'))
    lines.append(txt_row('  IDFW            = Identity Firewall; maps AD user to VM for user-based DFW policy'))
    lines.append(txt_row('  LDAP            = AD integration; NSX reads group membership to build IDFW mappings'))
    lines.append(txt_row('  Aria Net.Insight = VMware flow analytics; parses NSX IPFIX/sFlow; builds flow map'))
    lines.append(txt_row('  Aria Operations = VMware monitoring; NSX plugin shows gateway health and DFW stats'))
    lines.append(txt_row('  Tanzu / TKG     = Kubernetes integration; NSX provides pod networking via NCP plugin'))
    lines.append(txt_row('  NCP             = NSX Container Plugin; syncs K8s namespace/pod state to NSX segments'))
    lines.append(txt_row('  Terraform NSX   = VMware NSX Terraform provider; declare segments, rules, gateways as HCL'))
    lines.append(txt_row('  Partner LB      = Third-party LB (F5, Citrix) inserted into NSX via service chain'))
    lines.append(txt_row('  Panorama/FMC    = Palo Alto/Cisco FMC; integrates with NSX for micro-seg enforcement'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── ESXi sub-page diagrams ────────────────────────────────────────────────────

@kb_diagram('esxi-arch-how', 'docs/virtualization/vmware/esxi/architecture/how-it-works/index.md', 'ESXi How It Works — vmkernel, I/O stack, VM execution model')
def _esxi_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'ESXi — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('Type-1 hypervisor running directly on hardware; vmkernel mediates all I/O.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'vmkernel (Kernel Layer)'), bMid(L2, R2, 'VM Execution Engine'))))
    lines.append(R(merge(bMid(L1, R1, 'Schedules CPUs across all VMs'), bMid(L2, R2, 'VMX process per running VM'))))
    lines.append(R(merge(bMid(L1, R1, 'Memory balloon / swap / TPS'), bMid(L2, R2, 'vCPU mapped to pCPU threads'))))
    lines.append(R(merge(bMid(L1, R1, 'VMkernel NIC (vmknic) mgmt'), bMid(L2, R2, 'Guest OS in HW virt ring 0'))))
    lines.append(R(merge(bMid(L1, R1, 'Storage I/O via PSA stack'), bMid(L2, R2, 'VMDK on VMFS/NFS/vSAN'))))
    lines.append(R(merge(bMid(L1, R1, 'Networking via vSwitch/dvSwitch'), bMid(L2, R2, 'VMM, VMX, VCPU threads'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('vmkernel sends scheduled VM I/O to PSA (storage) and vSwitch (network).'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Storage I/O Stack (PSA)'), bMid(L2, R2, 'Network I/O Stack'))))
    lines.append(R(merge(bMid(L1, R1, 'NMP → SATP → PSP path'), bMid(L2, R2, 'vSwitch / dvSwitch ports'))))
    lines.append(R(merge(bMid(L1, R1, 'iSCSI/FC/FCoE/NFS/NVMe-oF'), bMid(L2, R2, 'Uplinks to physical switches'))))
    lines.append(R(merge(bMid(L1, R1, 'VMFS datastores on LUNs'), bMid(L2, R2, 'vmk0 mgmt / vmk1 vMotion'))))
    lines.append(R(merge(bMid(L1, R1, 'vSAN uses local disk groups'), bMid(L2, R2, 'vmk2 vSAN / vmk3 other'))))
    lines.append(R(merge(bMid(L1, R1, 'APD/PDL handling per policy'), bMid(L2, R2, 'NIOC bandwidth reservations'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 servers, NVMe/SSD/HDD, 10/25/100 GbE NICs, FC/iSCSI HBAs, ToR switches'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vmkernel  = ESXi micro-kernel; schedules CPU/mem/I/O for all VMs on host'))
    lines.append(txt_row('VMX       = user-space process managing one running VM; I/O emulation'))
    lines.append(txt_row('PSA       = Pluggable Storage Architecture; ESXi storage I/O framework'))
    lines.append(txt_row('NMP       = Native Multipathing Plugin; default path selector in PSA'))
    lines.append(txt_row('SATP      = Storage Array Type Plugin; array-specific PSA plugin'))
    lines.append(txt_row('PSP       = Path Selection Policy; round-robin, fixed, or MRU per LUN'))
    lines.append(txt_row('vmknic    = VMkernel NIC; carries mgmt/vMotion/vSAN/overlay traffic'))
    lines.append(txt_row('dvSwitch  = Distributed vSwitch; managed centrally by vCenter'))
    lines.append(txt_row('VMFS      = VMware File System; clustered FS shared across ESXi hosts'))
    lines.append(txt_row('TPS       = Transparent Page Sharing; deduplicates identical guest mem pages'))
    lines.append(txt_row('APD       = All Paths Down; storage path loss without PDL declared'))
    lines.append(txt_row('PDL       = Permanent Device Loss; device signals storage is gone permanently'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('esxi-arch-int', 'docs/virtualization/vmware/esxi/architecture/integrations/index.md', 'ESXi Integrations — vCenter, storage arrays, AD, backup, monitoring')
def _esxi_arch_int():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'ESXi — Integrations'))
    lines.append(txt_row())
    lines.append(txt_row('ESXi integrates with vCenter, storage arrays, AD, backup agents, monitoring.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'vCenter Integration'), bMid(L2, R2, 'Storage Integration'))))
    lines.append(R(merge(bMid(L1, R1, 'vCenter manages host lifecycle'), bMid(L2, R2, 'VMFS on iSCSI/FC/FCoE'))))
    lines.append(R(merge(bMid(L1, R1, 'vLCM patches ESXi firmware'), bMid(L2, R2, 'NFS v3/v4.1 datastores'))))
    lines.append(R(merge(bMid(L1, R1, 'HA/DRS cluster membership'), bMid(L2, R2, 'vSAN local disk pools'))))
    lines.append(R(merge(bMid(L1, R1, 'vMotion/svMotion operations'), bMid(L2, R2, 'NVMe-oF fabric support'))))
    lines.append(R(merge(bMid(L1, R1, 'dvSwitch port group mgmt'), bMid(L2, R2, 'VAAI offload to array'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('vCenter API → ESXi agent; backup uses VADP/CBT snapshot transport.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Identity / AD Integration'), bMid(L2, R2, 'Backup / Monitoring'))))
    lines.append(R(merge(bMid(L1, R1, 'AD join for host auth'), bMid(L2, R2, 'Veeam VADP proxy on ESXi'))))
    lines.append(R(merge(bMid(L1, R1, 'Smart card / CAC login'), bMid(L2, R2, 'Commvault / Avamar CBT'))))
    lines.append(R(merge(bMid(L1, R1, 'LDAP for SSO identity src'), bMid(L2, R2, 'Aria Ops agent per host'))))
    lines.append(R(merge(bMid(L1, R1, 'Local host users fallback'), bMid(L2, R2, 'SNMP traps to NMS'))))
    lines.append(R(merge(bMid(L1, R1, 'vSphere Roles on AD groups'), bMid(L2, R2, 'Syslog to Log Insight'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 hosts, SAN/NAS arrays, 10/25 GbE NICs, mgmt network for vCenter reach'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VADP     = vStorage APIs for Data Protection; snapshot-based backup API'))
    lines.append(txt_row('CBT      = Changed Block Tracking; tracks dirty disk blocks since backup'))
    lines.append(txt_row('VAAI     = vStorage APIs for Array Integration; offloads clone/zero to array'))
    lines.append(txt_row('vLCM     = vSphere Lifecycle Mgr; manages ESXi image + firmware baseline'))
    lines.append(txt_row('dvSwitch = Distributed vSwitch; centrally managed by vCenter across hosts'))
    lines.append(txt_row('VMFS     = VMware File System; clustered FS shared across ESXi hosts'))
    lines.append(txt_row('NFS      = Network File System; supported as ESXi datastore v3 and v4.1'))
    lines.append(txt_row('NVMe-oF  = NVMe over Fabrics; high-perf block storage protocol on ESXi'))
    lines.append(txt_row('Aria Ops = VMware monitoring; collects ESXi metrics via agent/API'))
    lines.append(txt_row('SNMP     = Simple Network Mgmt Protocol; ESXi sends traps on events'))
    lines.append(txt_row('SSO      = Single Sign-On; vCenter auth; integrates AD for ESXi login'))
    lines.append(txt_row('svMotion = Storage vMotion; migrates VMDK between datastores live'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('esxi-arch-design', 'docs/virtualization/vmware/esxi/architecture/design-standards/index.md', 'ESXi Design Standards — sizing, HA design, hardware requirements')
def _esxi_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'ESXi — Design Standards'))
    lines.append(txt_row())
    lines.append(txt_row('Hardware sizing, HA cluster design, and build standards for ESXi deployments.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Hardware Requirements'), bMid(L2, R2, 'Cluster Design'))))
    lines.append(R(merge(bMid(L1, R1, 'Min 2 sockets / 16 cores'), bMid(L2, R2, 'Min 3 hosts for HA N+1'))))
    lines.append(R(merge(bMid(L1, R1, '256 GB RAM per prod host'), bMid(L2, R2, 'Max 96 hosts per cluster'))))
    lines.append(R(merge(bMid(L1, R1, '2x 10/25 GbE NICs mgmt+VM'), bMid(L2, R2, 'EVC mode per CPU family'))))
    lines.append(R(merge(bMid(L1, R1, '2x 10/25 GbE vMotion/vSAN'), bMid(L2, R2, 'DRS threshold: moderate'))))
    lines.append(R(merge(bMid(L1, R1, 'Boot: SD/USB/M.2 or disk'), bMid(L2, R2, 'HA admission ctrl: slots'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical sizing → cluster policy → HA/DRS tuning → network teaming standard.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Networking Standards'), bMid(L2, R2, 'Storage Standards'))))
    lines.append(R(merge(bMid(L1, R1, 'dvSwitch for all prod hosts'), bMid(L2, R2, 'VMFS-6 on shared LUNs'))))
    lines.append(R(merge(bMid(L1, R1, 'vmk0 mgmt VLAN tagged'), bMid(L2, R2, 'vSAN disk group: 1 cache'))))
    lines.append(R(merge(bMid(L1, R1, 'vMotion on dedicated vmk'), bMid(L2, R2, 'Datastore naming standard'))))
    lines.append(R(merge(bMid(L1, R1, 'NIC teaming: LACP/failover'), bMid(L2, R2, 'Multipathing: RR for SAN'))))
    lines.append(R(merge(bMid(L1, R1, 'MTU 9000 vSAN/vMotion'), bMid(L2, R2, 'VAAI enabled on arrays'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Rack servers (2U), ToR switches (25 GbE), SAN fabric, power redundancy (2N)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('EVC     = Enhanced vMotion Compat; masks CPU features for live migration'))
    lines.append(txt_row('HA      = High Availability; vSphere restarts VMs after host failure'))
    lines.append(txt_row('DRS     = Distributed Resource Scheduler; balances CPU/mem load via vMotion'))
    lines.append(txt_row('LACP    = Link Aggregation Control Protocol; bonds NICs for bandwidth'))
    lines.append(txt_row('MTU     = Maximum Transmission Unit; jumbo frames (9000) for vSAN/vMotion'))
    lines.append(txt_row('RR      = Round Robin; PSA path policy across all active storage paths'))
    lines.append(txt_row('vmk     = VMkernel adapter; carries system traffic (mgmt/vMotion/vSAN)'))
    lines.append(txt_row('dvSwitch= Distributed vSwitch; enforces consistent port config across hosts'))
    lines.append(txt_row('VAAI    = vStorage API Array Integration; array offload for clone/zeroing'))
    lines.append(txt_row('Admission ctrl = HA policy reserving capacity to restart VMs on failure'))
    lines.append(txt_row('N+1     = cluster design with capacity to lose 1 host without VM impact'))
    lines.append(txt_row('Slot    = HA resource unit = worst-case VM CPU+mem in cluster'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('esxi-ops-backup', 'docs/virtualization/vmware/esxi/operations/backup-restore/index.md', 'ESXi Backup and Restore — config backup, host profile, restore steps')
def _esxi_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'ESXi — Backup and Restore'))
    lines.append(txt_row())
    lines.append(txt_row('configBundle backup, Host Profiles, and full reinstall restore procedure.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Config Backup (configBundle)'), bMid(L2, R2, 'Host Profile Backup'))))
    lines.append(R(merge(bMid(L1, R1, 'vim-cmd hostsvc/firmware/'), bMid(L2, R2, 'Export profile from vCenter'))))
    lines.append(R(merge(bMid(L1, R1, 'sync_config → backup_config'), bMid(L2, R2, 'Includes NIC/storage/dns'))))
    lines.append(R(merge(bMid(L1, R1, 'Exports .tgz configBundle'), bMid(L2, R2, 'Attach to host compliance'))))
    lines.append(R(merge(bMid(L1, R1, 'Schedule via cron/script'), bMid(L2, R2, 'vLCM image backup included'))))
    lines.append(R(merge(bMid(L1, R1, 'Store off-host (NFS/NAS)'), bMid(L2, R2, 'Compare with desired state'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Backup configBundle → store safely → restore via firmware/restore_config.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Restore Procedure'), bMid(L2, R2, 'Verification Steps'))))
    lines.append(R(merge(bMid(L1, R1, 'Reinstall ESXi same version'), bMid(L2, R2, 'Check vmk0 IP restored'))))
    lines.append(R(merge(bMid(L1, R1, 'Upload configBundle to host'), bMid(L2, R2, 'Verify vCenter reconnects'))))
    lines.append(R(merge(bMid(L1, R1, 'firmware/restore_config'), bMid(L2, R2, 'Check datastore mounts'))))
    lines.append(R(merge(bMid(L1, R1, 'Reboot → rejoin cluster'), bMid(L2, R2, 'Validate VM power-on'))))
    lines.append(R(merge(bMid(L1, R1, 'Apply Host Profile if used'), bMid(L2, R2, 'Confirm HA agent running'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 host, local boot media (SD/M.2), management network, NAS backup store'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('configBundle = .tgz ESXi host config archive; firmware/backup_config cmd'))
    lines.append(txt_row('vim-cmd     = ESXi CLI tool for host service and management tasks'))
    lines.append(txt_row('Host Profile = vCenter policy capturing desired ESXi configuration state'))
    lines.append(txt_row('vLCM        = vSphere Lifecycle Mgr; manages ESXi image and firmware'))
    lines.append(txt_row('restore_config = vim-cmd call to apply a previously saved configBundle'))
    lines.append(txt_row('HA agent    = fdm process on ESXi; communicates with vCenter HA master'))
    lines.append(txt_row('sync_config = vim-cmd call to flush pending config before backup'))
    lines.append(txt_row('NAS         = Network Attached Storage; stores configBundle files'))
    lines.append(txt_row('Desired state = Host Profile compliance target; re-applied after restore'))
    lines.append(txt_row('DCUI        = Direct Console UI; local console for host configuration'))
    lines.append(txt_row('fdm         = Fault Domain Manager; ESXi HA agent process'))
    lines.append(txt_row('Cluster     = group of ESXi hosts sharing HA, DRS, and vSAN resources'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('esxi-ops-cli', 'docs/virtualization/vmware/esxi/operations/cli-reference/index.md', 'ESXi CLI Reference — esxcli, vim-cmd, govc, PowerCLI commands')
def _esxi_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'ESXi — CLI Reference'))
    lines.append(txt_row())
    lines.append(txt_row('esxcli on-host, vim-cmd, govc (remote), and PowerCLI automation commands.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'esxcli (on-host)'), bMid(L2, R2, 'vim-cmd (on-host)'))))
    lines.append(R(merge(bMid(L1, R1, 'esxcli system version get'), bMid(L2, R2, 'vim-cmd vmsvc/getallvms'))))
    lines.append(R(merge(bMid(L1, R1, 'esxcli network ip interface'), bMid(L2, R2, 'vim-cmd vmsvc/power.on ID'))))
    lines.append(R(merge(bMid(L1, R1, 'esxcli storage core path'), bMid(L2, R2, 'vim-cmd hostsvc/maintenance'))))
    lines.append(R(merge(bMid(L1, R1, 'esxcli vm process list'), bMid(L2, R2, 'vim-cmd hostsvc/firmware/'))))
    lines.append(R(merge(bMid(L1, R1, 'esxcli software vib list'), bMid(L2, R2, 'vim-cmd solo/registervm'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('govc (remote vCenter API) and PowerCLI for scripted multi-host operations.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'govc (remote CLI)'), bMid(L2, R2, 'PowerCLI (remote)'))))
    lines.append(R(merge(bMid(L1, R1, 'govc host.info'), bMid(L2, R2, 'Get-VMHost | select Name'))))
    lines.append(R(merge(bMid(L1, R1, 'govc datastore.ls'), bMid(L2, R2, 'Get-Datastore | sort Name'))))
    lines.append(R(merge(bMid(L1, R1, 'govc vm.migrate -host'), bMid(L2, R2, 'Move-VM -Destination $h'))))
    lines.append(R(merge(bMid(L1, R1, 'govc host.maintenance.enter'), bMid(L2, R2, 'Set-VMHost -State Maint'))))
    lines.append(R(merge(bMid(L1, R1, 'govc events -type HostEvent'), bMid(L2, R2, 'Get-VIEvent -Entity $h'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ESXi hosts on x86; management network for SSH/API access to host/vCenter'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('esxcli    = on-host CLI; namespaces: system, network, storage, vm, software'))
    lines.append(txt_row('vim-cmd   = on-host; wraps vSphere API calls (hostsvc/vmsvc namespaces)'))
    lines.append(txt_row('govc      = open-source Go CLI for vCenter API; runs from any workstation'))
    lines.append(txt_row('PowerCLI  = VMware PowerShell module for scripted vSphere management'))
    lines.append(txt_row('VIB       = vSphere Installation Bundle; ESXi extension/driver package'))
    lines.append(txt_row('GOVC_URL  = env var pointing govc at vCenter: https://user:pass@vc/sdk'))
    lines.append(txt_row('maintenance = host state; vCenter migrates VMs before maintenance tasks'))
    lines.append(txt_row('hostsvc   = vim-cmd namespace for host-level service operations'))
    lines.append(txt_row('vmsvc     = vim-cmd namespace for VM lifecycle operations'))
    lines.append(txt_row('PSC       = Platform Services Controller; SSO/certs (pre-7.0)'))
    lines.append(txt_row('fdm       = Fault Domain Manager; HA agent queried via vim-cmd'))
    lines.append(txt_row('vCenter API = REST + SOAP endpoint; govc/PowerCLI both use it'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('esxi-ops-health', 'docs/virtualization/vmware/esxi/operations/health-checks/index.md', 'ESXi Health Checks — runbook, alarms, capacity review')
def _esxi_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'ESXi — Health Checks'))
    lines.append(txt_row())
    lines.append(txt_row('Daily/weekly health runbook: hardware sensors, alarms, capacity, and storage.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Hardware Health'), bMid(L2, R2, 'vSphere Cluster Health'))))
    lines.append(R(merge(bMid(L1, R1, 'IPMI/iDRAC sensor status'), bMid(L2, R2, 'HA master elected & green'))))
    lines.append(R(merge(bMid(L1, R1, 'CPU/mem/fan/PSU alarms'), bMid(L2, R2, 'DRS balance score < 2'))))
    lines.append(R(merge(bMid(L1, R1, 'esxcli hardware ipmi sdr'), bMid(L2, R2, 'vMotion network reachable'))))
    lines.append(R(merge(bMid(L1, R1, 'HBA/NIC link state up'), bMid(L2, R2, 'No disconnected hosts'))))
    lines.append(R(merge(bMid(L1, R1, 'Boot media health S.M.A.R.T.'), bMid(L2, R2, 'EVC mode consistent'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Hardware sensors → vSphere alarms → storage health → capacity review.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Storage Health'), bMid(L2, R2, 'Capacity Review'))))
    lines.append(R(merge(bMid(L1, R1, 'All paths active per LUN'), bMid(L2, R2, 'Host CPU util < 70% avg'))))
    lines.append(R(merge(bMid(L1, R1, 'No APD/PDL events today'), bMid(L2, R2, 'Host mem util < 80% avg'))))
    lines.append(R(merge(bMid(L1, R1, 'Datastore free > 20%'), bMid(L2, R2, 'VM balloon/swap = 0'))))
    lines.append(R(merge(bMid(L1, R1, 'VMFS no ATS heartbeat err'), bMid(L2, R2, 'vSAN disk capacity < 70%'))))
    lines.append(R(merge(bMid(L1, R1, 'vSAN health: all green'), bMid(L2, R2, 'Trend forecast 30/60 days'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 hosts with IPMI/iDRAC BMC, SAN/NAS/vSAN storage, 10/25 GbE NICs'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('IPMI     = Intelligent Platform Mgmt Interface; OOB hardware sensor access'))
    lines.append(txt_row('iDRAC    = Dell Remote Access Controller; OOB management BMC'))
    lines.append(txt_row('S.M.A.R.T = Self-Monitoring Analysis; disk health from boot media'))
    lines.append(txt_row('APD      = All Paths Down; storage unreachable but PDL not declared'))
    lines.append(txt_row('PDL      = Permanent Device Loss; device signals loss is permanent'))
    lines.append(txt_row('ATS      = Atomic Test & Set; VMFS locking primitive; heartbeat mechanism'))
    lines.append(txt_row('DRS score= 1-5 imbalance rating; 1=balanced, 5=critical imbalance'))
    lines.append(txt_row('Balloon  = VMware memory mgmt; guest driver returns idle pages to host'))
    lines.append(txt_row('EVC      = Enhanced vMotion Compat; consistent CPU flags across cluster'))
    lines.append(txt_row('fdm      = Fault Domain Manager; HA agent; must run on all hosts'))
    lines.append(txt_row('vSAN health = Skyline Health dashboard in vCenter; 60+ automated checks'))
    lines.append(txt_row('BMC      = Baseboard Management Controller; embedded OOB management chip'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('esxi-ops-install', 'docs/virtualization/vmware/esxi/operations/install-upgrade/index.md', 'ESXi Install and Upgrade — fresh install, vLCM upgrade, version matrix')
def _esxi_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'ESXi — Install and Upgrade'))
    lines.append(txt_row())
    lines.append(txt_row('Fresh install via ISO/PXE and in-place upgrade via vLCM baseline or image.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Fresh Install'), bMid(L2, R2, 'vLCM Upgrade'))))
    lines.append(R(merge(bMid(L1, R1, 'Boot from ISO/USB/PXE'), bMid(L2, R2, 'Create cluster image in vLCM'))))
    lines.append(R(merge(bMid(L1, R1, 'Accept EULA, select disk'), bMid(L2, R2, 'Attach baseline to cluster'))))
    lines.append(R(merge(bMid(L1, R1, 'Set root password + mgmt IP'), bMid(L2, R2, 'Remediate in rolling order'))))
    lines.append(R(merge(bMid(L1, R1, 'Reboot → add to vCenter'), bMid(L2, R2, 'Maintenance → upgrade → reboot'))))
    lines.append(R(merge(bMid(L1, R1, 'Apply Host Profile config'), bMid(L2, R2, 'Verify version post-upgrade'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Prerequisites → install/upgrade → add to cluster → verify health state.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Prerequisites'), bMid(L2, R2, 'Version Matrix'))))
    lines.append(R(merge(bMid(L1, R1, 'HCL check for hardware'), bMid(L2, R2, 'ESXi 8.0 U3 — current GA'))))
    lines.append(R(merge(bMid(L1, R1, 'vCenter >= ESXi version'), bMid(L2, R2, 'ESXi 7.0 U3 — supported'))))
    lines.append(R(merge(bMid(L1, R1, 'Storage/NIC drivers on HCL'), bMid(L2, R2, 'vCenter must lead ESXi ver'))))
    lines.append(R(merge(bMid(L1, R1, 'Boot disk >= 8 GB (>= 32 GB)'), bMid(L2, R2, 'N-2 upgrade path maximum'))))
    lines.append(R(merge(bMid(L1, R1, 'Mgmt network planned ahead'), bMid(L2, R2, 'Check VMware interop matrix'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 server on HCL, IPMI/iDRAC for PXE, 10 GbE mgmt NIC, boot disk (M.2/SD)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vLCM     = vSphere Lifecycle Mgr; image-based ESXi patch and upgrade mgmt'))
    lines.append(txt_row('HCL      = VMware Hardware Compatibility List; validated hardware for ESXi'))
    lines.append(txt_row('PXE      = Preboot Execution Env; network boot for ESXi install via TFTP'))
    lines.append(txt_row('Baseline = vLCM patch set; defines target ESXi build for remediation'))
    lines.append(txt_row('Remediate= vLCM process: puts host in maintenance + upgrades ESXi'))
    lines.append(txt_row('EULA     = End User License Agreement; accepted during ESXi installer'))
    lines.append(txt_row('N-2 path = VMware supports skipping up to 2 major versions in upgrade'))
    lines.append(txt_row('Host Profile = desired state config applied after fresh ESXi install'))
    lines.append(txt_row('Interop  = VMware Product Interoperability Matrix; validates version combos'))
    lines.append(txt_row('GA       = General Availability; production-ready official release'))
    lines.append(txt_row('Rolling  = upgrade one host at a time; VMs migrated before each upgrade'))
    lines.append(txt_row('Boot disk = ESXi install target; SD/USB (legacy), M.2 NVMe (recommended)'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('esxi-ops-proc', 'docs/virtualization/vmware/esxi/operations/procedures/index.md', 'ESXi Standard Procedures — maintenance mode, change management')
def _esxi_ops_proc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'ESXi — Standard Procedures'))
    lines.append(txt_row())
    lines.append(txt_row('Maintenance mode, change control, and host decommission standard procedures.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Maintenance Mode Procedure'), bMid(L2, R2, 'Change Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Drain VMs via vMotion/DRS'), bMid(L2, R2, 'Raise change request (CR)'))))
    lines.append(R(merge(bMid(L1, R1, 'Enter maintenance: vCenter UI'), bMid(L2, R2, 'Pre-change health snapshot'))))
    lines.append(R(merge(bMid(L1, R1, 'esxcli system maintenanceMode'), bMid(L2, R2, 'Maintenance window agreed'))))
    lines.append(R(merge(bMid(L1, R1, 'Verify no VMs remain on host'), bMid(L2, R2, 'Post-change validation'))))
    lines.append(R(merge(bMid(L1, R1, 'Perform task, exit maintenance'), bMid(L2, R2, 'Close CR with evidence'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Maintenance mode drains VMs; change control wraps every host-level change.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Host Decommission'), bMid(L2, R2, 'Emergency Procedures'))))
    lines.append(R(merge(bMid(L1, R1, 'Migrate all VMs off host'), bMid(L2, R2, 'Force maintenance if HA'))))
    lines.append(R(merge(bMid(L1, R1, 'Remove from vSAN disk group'), bMid(L2, R2, 'PSOD: capture vmkernel log'))))
    lines.append(R(merge(bMid(L1, R1, 'Disconnect from vCenter'), bMid(L2, R2, 'Isolate host from network'))))
    lines.append(R(merge(bMid(L1, R1, 'Remove from cluster'), bMid(L2, R2, 'Power off affected VMs'))))
    lines.append(R(merge(bMid(L1, R1, 'Deregister from vCenter'), bMid(L2, R2, 'Escalate to VMware GSS'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 host, iDRAC/IPMI for OOB control, management network, vCenter appliance'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Maintenance mode = host state; vCenter stops VM placement; drains existing'))
    lines.append(txt_row('vMotion     = live VM migration; used to drain host before maintenance'))
    lines.append(txt_row('PSOD        = Purple Screen Of Death; ESXi kernel panic / crash dump'))
    lines.append(txt_row('CR          = Change Request; ITSM ticket authorising planned changes'))
    lines.append(txt_row('DRS         = Distributed Resource Scheduler; auto-migrates VMs'))
    lines.append(txt_row('HA          = High Availability; restarts VMs on remaining hosts'))
    lines.append(txt_row('Decommission= formal process to remove host from inventory and cluster'))
    lines.append(txt_row('iDRAC       = Dell OOB management; power control when host unresponsive'))
    lines.append(txt_row('vmkernel log= /var/log/vmkernel.log; primary diagnostic log on ESXi'))
    lines.append(txt_row('vSAN evac   = removes host disks from vSAN before decommission'))
    lines.append(txt_row('Force maint = maintenance without VM evacuation; HA failure scenario only'))
    lines.append(txt_row('Health snap = pre/post change comparison of alarms/metrics/log tail'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('esxi-ops-scripts', 'docs/virtualization/vmware/esxi/operations/scripts/index.md', 'ESXi Scripts — PowerCLI, Python, shell scripts for common tasks')
def _esxi_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'ESXi — Scripts'))
    lines.append(txt_row())
    lines.append(txt_row('PowerCLI, shell, and Python scripts automating ESXi host operations at scale.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'PowerCLI Scripts'), bMid(L2, R2, 'Shell / esxcli Scripts'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-VMHost health report'), bMid(L2, R2, 'esxcli system version get'))))
    lines.append(R(merge(bMid(L1, R1, 'Set-VMHostNTP / DNS bulk'), bMid(L2, R2, 'for host in list; ssh cmd'))))
    lines.append(R(merge(bMid(L1, R1, 'Move-VM bulk vMotion'), bMid(L2, R2, 'esxcli storage core path'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-Datastore free space rpt'), bMid(L2, R2, 'esxcli vm process kill'))))
    lines.append(R(merge(bMid(L1, R1, 'Invoke-VMScript in guest'), bMid(L2, R2, 'cron + configBundle backup'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('PowerCLI for vCenter-scope tasks; esxcli over SSH for per-host automation.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Python / pyVmomi Scripts'), bMid(L2, R2, 'Automation Patterns'))))
    lines.append(R(merge(bMid(L1, R1, 'ServiceInstance connect'), bMid(L2, R2, 'Idempotent design'))))
    lines.append(R(merge(bMid(L1, R1, 'Traverse container view'), bMid(L2, R2, 'Error handling + retry'))))
    lines.append(R(merge(bMid(L1, R1, 'Get host config objects'), bMid(L2, R2, 'Dry-run mode flag'))))
    lines.append(R(merge(bMid(L1, R1, 'Reconfigure host via API'), bMid(L2, R2, 'Log output to file'))))
    lines.append(R(merge(bMid(L1, R1, 'Task monitoring wait loop'), bMid(L2, R2, 'Pipeline integration'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ESXi hosts on x86, management network, jump host for script execution'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('PowerCLI    = VMware PowerShell SDK; Connect-VIServer for vCenter/ESXi'))
    lines.append(txt_row('pyVmomi     = Python SDK for vSphere API; official VMware library'))
    lines.append(txt_row('esxcli      = on-host CLI; run via SSH or Ansible for bulk host ops'))
    lines.append(txt_row('govc        = Go CLI for vCenter API; lightweight alternative to PowerCLI'))
    lines.append(txt_row('Invoke-VMScript = PowerCLI cmd to run script in guest via VMtools'))
    lines.append(txt_row('Container view = pyVmomi API for traversing vCenter inventory objects'))
    lines.append(txt_row('Task object = vSphere async task; polled until complete or error'))
    lines.append(txt_row('Idempotent  = script produces same result if run multiple times safely'))
    lines.append(txt_row('Dry-run     = logic executes but no changes applied; safe testing'))
    lines.append(txt_row('cron        = Linux scheduler on jump host; triggers backup/health scripts'))
    lines.append(txt_row('SSH         = Secure Shell; disabled by default on ESXi; enable per-host'))
    lines.append(txt_row('VMtools     = VMware Tools; guest agent enabling Invoke-VMScript'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('esxi-sec-access', 'docs/virtualization/vmware/esxi/security/access-control/index.md', 'ESXi Access Control — RBAC, roles, permission sets, lockdown mode')
def _esxi_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'ESXi — Access Control'))
    lines.append(txt_row())
    lines.append(txt_row('RBAC via vCenter roles, lockdown mode, and direct host permission management.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'vCenter RBAC'), bMid(L2, R2, 'Direct Host Permissions'))))
    lines.append(R(merge(bMid(L1, R1, 'Roles: Admin, ReadOnly, VM'), bMid(L2, R2, 'Local root: SSH only'))))
    lines.append(R(merge(bMid(L1, R1, 'Assign role to user+object'), bMid(L2, R2, 'DCUI access: locked down'))))
    lines.append(R(merge(bMid(L1, R1, 'Propagate to child objects'), bMid(L2, R2, 'Exception users: emergency'))))
    lines.append(R(merge(bMid(L1, R1, 'AD group → vSphere role'), bMid(L2, R2, 'Lockdown mode: normal/strict'))))
    lines.append(R(merge(bMid(L1, R1, 'Audit permission changes'), bMid(L2, R2, 'DCUI exception list config'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('vCenter roles govern all access; lockdown mode blocks direct ESXi SSH login.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Privilege Management'), bMid(L2, R2, 'Audit and Review'))))
    lines.append(R(merge(bMid(L1, R1, 'No-priv users read-only'), bMid(L2, R2, 'Review permissions monthly'))))
    lines.append(R(merge(bMid(L1, R1, 'Custom roles: least priv'), bMid(L2, R2, 'Remove stale AD accounts'))))
    lines.append(R(merge(bMid(L1, R1, 'No global admin for ops'), bMid(L2, R2, 'Log access events in Aria'))))
    lines.append(R(merge(bMid(L1, R1, 'PowerCLI: Get-VIPermission'), bMid(L2, R2, 'Alert on root SSH login'))))
    lines.append(R(merge(bMid(L1, R1, 'Service accounts: named'), bMid(L2, R2, 'Export permission report'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 hosts, management network, AD/LDAP, vCenter SSO, syslog target'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RBAC        = Role-Based Access Control; user+role+object permission model'))
    lines.append(txt_row('Lockdown mode = ESXi state; blocks direct host login; normal or strict'))
    lines.append(txt_row('DCUI        = Direct Console UI; local keyboard/screen access to host'))
    lines.append(txt_row('Exception users = accounts allowed DCUI in lockdown; emergency access'))
    lines.append(txt_row('SSO         = Single Sign-On; vCenter identity service integrating AD'))
    lines.append(txt_row('Propagate   = permission inherited by child inventory objects'))
    lines.append(txt_row('Least priv  = principle: grant minimum permissions needed for role'))
    lines.append(txt_row('Custom role = vSphere role built from individual privilege checkboxes'))
    lines.append(txt_row('Get-VIPermission = PowerCLI cmdlet; lists all permissions on object'))
    lines.append(txt_row('Service acct= named account used by automation; not shared personal creds'))
    lines.append(txt_row('Strict lockdown = no DCUI; only vCenter API access allowed to host'))
    lines.append(txt_row('Audit log   = record of permission changes; stored in vCenter events'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('esxi-sec-auth', 'docs/virtualization/vmware/esxi/security/authentication/index.md', 'ESXi Authentication — SSO, AD/LDAP, smart card, MFA configuration')
def _esxi_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'ESXi — Authentication'))
    lines.append(txt_row())
    lines.append(txt_row('SSO, AD/LDAP join, smart card (CAC), and MFA configuration for ESXi access.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'vCenter SSO'), bMid(L2, R2, 'Host AD Integration'))))
    lines.append(R(merge(bMid(L1, R1, 'vsphere.local default domain'), bMid(L2, R2, 'Join host to AD domain'))))
    lines.append(R(merge(bMid(L1, R1, 'Add AD as identity source'), bMid(L2, R2, 'AD users log in to DCUI'))))
    lines.append(R(merge(bMid(L1, R1, 'Password policy in SSO'), bMid(L2, R2, 'ESXi Shell AD auth'))))
    lines.append(R(merge(bMid(L1, R1, 'Token policy: timeout/count'), bMid(L2, R2, 'AD group to DCUI access'))))
    lines.append(R(merge(bMid(L1, R1, 'MFA: RSA SecurID / Radius'), bMid(L2, R2, 'Leave domain on decomm'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SSO identity source → vCenter auth → RBAC mapping → ESXi host access.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Smart Card / CAC Auth'), bMid(L2, R2, 'MFA Configuration'))))
    lines.append(R(merge(bMid(L1, R1, 'vCenter: enable cert auth'), bMid(L2, R2, 'RSA SecurID integration'))))
    lines.append(R(merge(bMid(L1, R1, 'Map cert UPN to AD user'), bMid(L2, R2, 'Radius server configured'))))
    lines.append(R(merge(bMid(L1, R1, 'CAC card + PIN required'), bMid(L2, R2, 'SSO MFA policy enabled'))))
    lines.append(R(merge(bMid(L1, R1, 'OCSP/CRL revocation check'), bMid(L2, R2, 'Fallback: local admin only'))))
    lines.append(R(merge(bMid(L1, R1, 'DOD/STIG CAC requirement'), bMid(L2, R2, 'MFA for vCenter UI/API'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 hosts, management network, AD/LDAP servers, RSA/Radius MFA servers'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SSO         = Single Sign-On; vCenter embedded auth service'))
    lines.append(txt_row('vsphere.local = built-in SSO domain; local admin accounts live here'))
    lines.append(txt_row('Identity source = AD/LDAP added to SSO; users can log in with domain'))
    lines.append(txt_row('CAC         = Common Access Card; US Gov smart card for auth'))
    lines.append(txt_row('OCSP        = Online Certificate Status Protocol; checks cert revocation'))
    lines.append(txt_row('CRL         = Certificate Revocation List; offline revocation list'))
    lines.append(txt_row('RSA SecurID = MFA token; OTP used as second factor for vCenter'))
    lines.append(txt_row('Radius      = Remote Auth Dial-In User Service; MFA protocol'))
    lines.append(txt_row('UPN         = User Principal Name; cert field mapped to AD user'))
    lines.append(txt_row('DCUI        = Direct Console UI; local access; can use AD auth'))
    lines.append(txt_row('Token policy = SSO setting: session lifetime and concurrent count'))
    lines.append(txt_row('STIG        = Security Technical Implementation Guide; DOD hardening'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('esxi-sec-enc', 'docs/virtualization/vmware/esxi/security/encryption/index.md', 'ESXi Encryption — VM encryption, vMotion encryption, KMS integration')
def _esxi_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'ESXi — Encryption'))
    lines.append(txt_row())
    lines.append(txt_row('VM encryption, vMotion encryption, and KMS key management for ESXi workloads.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'VM Encryption'), bMid(L2, R2, 'KMS Integration'))))
    lines.append(R(merge(bMid(L1, R1, 'Enabled via Storage Policy'), bMid(L2, R2, 'vCenter Key Provider'))))
    lines.append(R(merge(bMid(L1, R1, 'Encrypts VMDK + config'), bMid(L2, R2, 'KMIP-compatible KMS'))))
    lines.append(R(merge(bMid(L1, R1, 'DEK wrapped by KEK from KMS'), bMid(L2, R2, 'Native Key Provider (vCenter)'))))
    lines.append(R(merge(bMid(L1, R1, 'Requires Crypto-Enabled host'), bMid(L2, R2, 'HyTrust / Thales / Vormetric'))))
    lines.append(R(merge(bMid(L1, R1, 'Snapshots encrypted too'), bMid(L2, R2, 'Key rotation procedure'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('KMS provides KEKs; vCenter wraps VM DEKs; host decrypts at power-on.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'vMotion Encryption'), bMid(L2, R2, 'vSAN Encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'Required/Opportunistic modes'), bMid(L2, R2, 'Data-at-rest encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'AES-256 in-flight traffic'), bMid(L2, R2, 'Enabled per cluster policy'))))
    lines.append(R(merge(bMid(L1, R1, 'Requires vSphere 6.5+'), bMid(L2, R2, 'KMS provides cluster keys'))))
    lines.append(R(merge(bMid(L1, R1, 'Config in cluster settings'), bMid(L2, R2, 'Dedup disabled if enc on'))))
    lines.append(R(merge(bMid(L1, R1, 'Enabled by default (8.0+)'), bMid(L2, R2, 'Key re-key on node failure'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 hosts with AES-NI CPU, management network, external KMS appliance'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VM Encryption = VMDK encrypted at rest using DEK/KEK model'))
    lines.append(txt_row('DEK          = Data Encryption Key; encrypts actual VM data on disk'))
    lines.append(txt_row('KEK          = Key Encryption Key; wraps the DEK; stored in KMS'))
    lines.append(txt_row('KMS          = Key Management Server; KMIP server storing KEKs'))
    lines.append(txt_row('KMIP         = Key Mgmt Interoperability Protocol; standard KMS API'))
    lines.append(txt_row('Native KP    = vCenter built-in key provider; no external KMS needed'))
    lines.append(txt_row('Crypto host  = ESXi host in crypto-enabled state; required for enc VMs'))
    lines.append(txt_row('vMotion enc  = encrypts live migration traffic; required or opportunistic'))
    lines.append(txt_row('vSAN enc     = encrypts all data written to vSAN datastore'))
    lines.append(txt_row('AES-NI       = CPU instruction set accelerating AES encryption'))
    lines.append(txt_row('Key rotation = replacing KEK; re-wraps DEKs without re-encrypting data'))
    lines.append(txt_row('Dedup        = deduplication; disabled when vSAN encryption is active'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('esxi-sec-hard', 'docs/virtualization/vmware/esxi/security/hardening/index.md', 'ESXi Hardening — CIS benchmark, lockdown mode, host firewall')
def _esxi_sec_hard():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'ESXi — Hardening'))
    lines.append(txt_row())
    lines.append(txt_row('CIS VMware benchmark, lockdown mode, host firewall, and hardening profile.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'CIS / STIG Benchmarks'), bMid(L2, R2, 'Lockdown Mode'))))
    lines.append(R(merge(bMid(L1, R1, 'CIS VMware ESXi benchmark'), bMid(L2, R2, 'Normal: DCUI restricted'))))
    lines.append(R(merge(bMid(L1, R1, 'DISA STIG for vSphere'), bMid(L2, R2, 'Strict: no DCUI at all'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable SSH in production'), bMid(L2, R2, 'Exception users config'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable MOB browser'), bMid(L2, R2, 'All access via vCenter'))))
    lines.append(R(merge(bMid(L1, R1, 'vSphere Assessment Tool'), bMid(L2, R2, 'Enter/exit lockdown API'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('CIS/STIG baseline → lockdown mode → firewall rules → Host Profile enforce.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Host Firewall'), bMid(L2, R2, 'Hardening Controls'))))
    lines.append(R(merge(bMid(L1, R1, 'Default: deny all inbound'), bMid(L2, R2, 'NTP configured (ntpd)'))))
    lines.append(R(merge(bMid(L1, R1, 'Allow: vCenter/vMotion IPs'), bMid(L2, R2, 'Syslog to remote host'))))
    lines.append(R(merge(bMid(L1, R1, 'esxcli network firewall rule'), bMid(L2, R2, 'Banner / MOTD set'))))
    lines.append(R(merge(bMid(L1, R1, 'Limit SSH to mgmt VLAN'), bMid(L2, R2, 'Disable SNMP v1/v2'))))
    lines.append(R(merge(bMid(L1, R1, 'Close unnecessary services'), bMid(L2, R2, 'Host Profile enforced'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 hosts, management VLAN, dedicated OOB network, syslog collector'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CIS         = Center for Internet Security; produces hardening benchmarks'))
    lines.append(txt_row('STIG        = Security Technical Implementation Guide; DOD hardening'))
    lines.append(txt_row('DISA        = Defense Information Systems Agency; publishes STIGs'))
    lines.append(txt_row('MOB         = Managed Object Browser; web debug UI; disable in prod'))
    lines.append(txt_row('Lockdown    = ESXi mode blocking direct host admin; enforces vCenter'))
    lines.append(txt_row('Exception users = accounts exempt from lockdown for break-glass access'))
    lines.append(txt_row('MOTD        = Message of the Day; banner displayed at ESXi login'))
    lines.append(txt_row('ntpd        = NTP daemon on ESXi; keeps host clock in sync'))
    lines.append(txt_row('Host Profile= vCenter desired-state enforcement; applied after reconfig'))
    lines.append(txt_row('VAT         = vSphere Assessment Tool; checks ESXi against benchmark'))
    lines.append(txt_row('Firewall rule= ESXi kernel-level packet filter; allow/deny per service'))
    lines.append(txt_row('SNMP v3     = secure SNMP version with auth+enc; v1/v2 must be disabled'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('esxi-ts-common', 'docs/virtualization/vmware/esxi/troubleshooting/common-issues/index.md', 'ESXi Common Issues — host disconnect, PSOD, storage latency, VM issues')
def _esxi_ts_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'ESXi — Common Issues'))
    lines.append(txt_row())
    lines.append(txt_row('Host disconnect, PSOD, storage APD/PDL, VM power-on failures, and fixes.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Host Connectivity Issues'), bMid(L2, R2, 'PSOD / Kernel Crash'))))
    lines.append(R(merge(bMid(L1, R1, 'vCenter shows disconnected'), bMid(L2, R2, 'Purple screen on console'))))
    lines.append(R(merge(bMid(L1, R1, 'Check mgmt vmk0 IP/VLAN'), bMid(L2, R2, 'Note error code + offset'))))
    lines.append(R(merge(bMid(L1, R1, 'Restart hostd / vpxa'), bMid(L2, R2, 'Collect vm-support bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'Check DNS resolution'), bMid(L2, R2, 'Review /var/log/vmkernel'))))
    lines.append(R(merge(bMid(L1, R1, 'Reconnect from vCenter UI'), bMid(L2, R2, 'Engage VMware GSS'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Diagnose host/network issues first; storage APD/PDL separate path below.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Storage Issues'), bMid(L2, R2, 'VM Power-On Failures'))))
    lines.append(R(merge(bMid(L1, R1, 'APD: check path state'), bMid(L2, R2, 'Insufficient resources'))))
    lines.append(R(merge(bMid(L1, R1, 'PDL: array controller check'), bMid(L2, R2, 'Lock file from prior crash'))))
    lines.append(R(merge(bMid(L1, R1, 'esxcli storage core path'), bMid(L2, R2, 'Remove stale .lck file'))))
    lines.append(R(merge(bMid(L1, R1, 'Latency: check DAVG/KAVG'), bMid(L2, R2, 'Disk space exhausted'))))
    lines.append(R(merge(bMid(L1, R1, 'Rescan storage adapters'), bMid(L2, R2, 'VMtools version mismatch'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 hosts, SAN/NAS/vSAN storage, ToR switches, management network, vCenter'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('PSOD     = Purple Screen Of Death; ESXi kernel panic; host reboots'))
    lines.append(txt_row('APD      = All Paths Down; storage paths lost; VM I/O paused'))
    lines.append(txt_row('PDL      = Permanent Device Loss; device signals permanent failure'))
    lines.append(txt_row('hostd    = ESXi host agent; manages host locally; restart to recover'))
    lines.append(txt_row('vpxa     = vCenter agent on ESXi; communicates with vCenter'))
    lines.append(txt_row('DAVG     = Device Average latency; measured at storage adapter layer'))
    lines.append(txt_row('KAVG     = Kernel Average latency; delay in VMkernel queue'))
    lines.append(txt_row('.lck     = VM lock file; stale lock prevents VM power-on'))
    lines.append(txt_row('vm-support = bundle command to collect ESXi diagnostic data'))
    lines.append(txt_row('vmkernel.log = main ESXi system log; first check for any issue'))
    lines.append(txt_row('Reconnect = vCenter action to re-establish agent connection to host'))
    lines.append(txt_row('vmk0     = management VMkernel adapter; ping test first step'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('esxi-ts-diag', 'docs/virtualization/vmware/esxi/troubleshooting/diagnostics/index.md', 'ESXi Diagnostics — log locations, esxcli diagnostics, support bundle')
def _esxi_ts_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'ESXi — Diagnostics'))
    lines.append(txt_row())
    lines.append(txt_row('Log file locations, esxcli diagnostic commands, and support bundle collection.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Key Log Files'), bMid(L2, R2, 'esxcli Diagnostic Commands'))))
    lines.append(R(merge(bMid(L1, R1, '/var/log/vmkernel.log'), bMid(L2, R2, 'esxcli system stats'))))
    lines.append(R(merge(bMid(L1, R1, '/var/log/hostd.log'), bMid(L2, R2, 'esxcli network stat get'))))
    lines.append(R(merge(bMid(L1, R1, '/var/log/vpxa.log'), bMid(L2, R2, 'esxcli storage core path'))))
    lines.append(R(merge(bMid(L1, R1, '/var/log/fdm.log (HA)'), bMid(L2, R2, 'esxcli vm process list'))))
    lines.append(R(merge(bMid(L1, R1, '/scratch/log (SD/USB)'), bMid(L2, R2, 'esxcli system process'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Logs → esxcli live state → esxtop performance → support bundle for GSS.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'esxtop Performance'), bMid(L2, R2, 'Support Bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'esxtop interactive TUI'), bMid(L2, R2, 'vm-support -w /tmp/bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'c=CPU, m=mem, d=disk'), bMid(L2, R2, 'vCenter: Export Support'))))
    lines.append(R(merge(bMid(L1, R1, 'n=network, i=interrupt'), bMid(L2, R2, 'Includes logs + configs'))))
    lines.append(R(merge(bMid(L1, R1, 'batch mode: -b -n 5'), bMid(L2, R2, 'Upload to VMware SR'))))
    lines.append(R(merge(bMid(L1, R1, 'DAVG > 25ms = issue'), bMid(L2, R2, 'Keep for 30 days min'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 hosts, SAN/NAS storage, management network, syslog server for logs'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vmkernel.log = main ESXi kernel log; storage/network/crash events'))
    lines.append(txt_row('hostd.log   = host daemon log; VM operations, config changes'))
    lines.append(txt_row('vpxa.log    = vCenter agent log; connection issues to vCenter'))
    lines.append(txt_row('fdm.log     = HA agent log; cluster membership and failover events'))
    lines.append(txt_row('esxtop      = real-time performance tool; CPU/mem/disk/net metrics'))
    lines.append(txt_row('DAVG        = device average latency; > 25ms indicates storage issue'))
    lines.append(txt_row('KAVG        = kernel average latency; VMkernel queue delay'))
    lines.append(txt_row('vm-support  = CLI tool to create ESXi diagnostic bundle'))
    lines.append(txt_row('SR          = Service Request; VMware GSS support ticket'))
    lines.append(txt_row('/scratch    = persistent log path; on SD/USB hosts may be volatile'))
    lines.append(txt_row('batch mode  = esxtop -b -n N; captures N iterations non-interactively'))
    lines.append(txt_row('Support bundle = zip of logs, configs, hardware state for GSS analysis'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('esxi-ts-esc', 'docs/virtualization/vmware/esxi/troubleshooting/escalation/index.md', 'ESXi Escalation — VMware GSS, support bundle, severity levels')
def _esxi_ts_esc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'ESXi — Escalation'))
    lines.append(txt_row())
    lines.append(txt_row('VMware GSS escalation, support bundle collection, and severity level matrix.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Escalation Decision'), bMid(L2, R2, 'Pre-Escalation Steps'))))
    lines.append(R(merge(bMid(L1, R1, 'PSOD / data loss risk'), bMid(L2, R2, 'Collect support bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'Unexplained host failure'), bMid(L2, R2, 'Document symptoms + time'))))
    lines.append(R(merge(bMid(L1, R1, 'Storage APD not resolving'), bMid(L2, R2, 'Capture esxtop batch'))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster HA not recovering'), bMid(L2, R2, 'Note ESXi/vCenter version'))))
    lines.append(R(merge(bMid(L1, R1, 'Suspected driver/firmware'), bMid(L2, R2, 'Verify HCL status first'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Internal diagnosis → pre-escalation bundle → VMware SR → severity match.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Severity Levels'), bMid(L2, R2, 'Support Bundle Contents'))))
    lines.append(R(merge(bMid(L1, R1, 'S1: prod down, data loss'), bMid(L2, R2, '/var/log/* all logs'))))
    lines.append(R(merge(bMid(L1, R1, 'S2: major feature broken'), bMid(L2, R2, 'vmkernel PSOD dump'))))
    lines.append(R(merge(bMid(L1, R1, 'S3: degraded, workaround'), bMid(L2, R2, 'Hardware config + HCL'))))
    lines.append(R(merge(bMid(L1, R1, 'S4: info/question'), bMid(L2, R2, 'Network config (vmknic)'))))
    lines.append(R(merge(bMid(L1, R1, 'S1 = 24x7 phone support'), bMid(L2, R2, 'Storage path state output'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 hosts, SAN/NAS/vSAN, vCenter appliance, management network, OOB access'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('GSS         = Global Support Services; VMware support organisation'))
    lines.append(txt_row('SR          = Service Request; support ticket raised via my.vmware.com'))
    lines.append(txt_row('S1          = Severity 1; production system down; 24x7 phone response'))
    lines.append(txt_row('S2          = Severity 2; major impact but workaround possible'))
    lines.append(txt_row('Support bundle = vm-support archive; upload to SR for GSS analysis'))
    lines.append(txt_row('PSOD dump   = memory dump from kernel crash; captured at panic time'))
    lines.append(txt_row('HCL         = Hardware Compatibility List; confirm before escalating'))
    lines.append(txt_row('vmkernel.log= primary ESXi system log; first item GSS will review'))
    lines.append(txt_row('esxtop batch= esxtop -b output; shows performance at time of issue'))
    lines.append(txt_row('my.vmware.com= VMware customer portal; SR creation and file upload'))
    lines.append(txt_row('Workaround  = temporary fix; allows S2 to remain S2 not S1'))
    lines.append(txt_row('Phone bridge= S1 SR triggers phone call from VMware engineer'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── NSX operations, security, and troubleshooting sub-page diagrams ───────────

@kb_diagram('nsx-ops-backup', 'docs/virtualization/vmware/nsx/operations/backup-restore/index.md', 'NSX Backup and Restore — Manager backup, restore procedure')
def _nsx_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NSX — Backup and Restore'))
    lines.append(txt_row())
    lines.append(txt_row('NSX Manager cluster backup via SFTP, scheduling, and full restore procedure.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'NSX Manager Backup'), bMid(L2, R2, 'Backup Configuration'))))
    lines.append(R(merge(bMid(L1, R1, 'Full cluster state backup'), bMid(L2, R2, 'SFTP server required'))))
    lines.append(R(merge(bMid(L1, R1, 'API: POST /api/v1/cluster/'), bMid(L2, R2, 'Passphrase for encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'UI: System > Backup'), bMid(L2, R2, 'Schedule: daily minimum'))))
    lines.append(R(merge(bMid(L1, R1, 'Includes all config + certs'), bMid(L2, R2, 'Retention: 30+ backups'))))
    lines.append(R(merge(bMid(L1, R1, 'Inventory + policy backup'), bMid(L2, R2, 'Test restore quarterly'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Schedule backup → verify SFTP receipt → test restore in non-prod quarterly.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Restore Procedure'), bMid(L2, R2, 'Verification Steps'))))
    lines.append(R(merge(bMid(L1, R1, 'Deploy fresh NSX Manager'), bMid(L2, R2, 'All nodes show green'))))
    lines.append(R(merge(bMid(L1, R1, 'Point to SFTP backup'), bMid(L2, R2, 'Segments/T0/T1 intact'))))
    lines.append(R(merge(bMid(L1, R1, 'Provide passphrase'), bMid(L2, R2, 'DFW rules restored'))))
    lines.append(R(merge(bMid(L1, R1, 'Restore initiates cluster'), bMid(L2, R2, 'Transport nodes synced'))))
    lines.append(R(merge(bMid(L1, R1, 'Reconnect compute manager'), bMid(L2, R2, 'vCenter integration OK'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NSX Manager VMs on ESXi, vCenter, SFTP backup server, management network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('NSX Manager = 3-node cluster VM; central control/mgmt plane for NSX'))
    lines.append(txt_row('SFTP        = SSH File Transfer Protocol; NSX backup destination'))
    lines.append(txt_row('Passphrase  = encryption key for NSX backup file; store securely'))
    lines.append(txt_row('Compute Mgr = vCenter registered in NSX; must reconnect after restore'))
    lines.append(txt_row('Transport node = ESXi/Edge with NSX dataplane (N-VDS) installed'))
    lines.append(txt_row('DFW         = Distributed Firewall; policy object restored from backup'))
    lines.append(txt_row('T0 gateway  = Tier-0; north-south routing; restored from backup state'))
    lines.append(txt_row('T1 gateway  = Tier-1; service gateway; connected to T0 and segments'))
    lines.append(txt_row('Cluster restore = NSX API call re-deploying config from SFTP backup'))
    lines.append(txt_row('N-VDS       = NSX virtual distributed switch on transport nodes'))
    lines.append(txt_row('Inventory   = groups, tags, VMs known to NSX; backed up with config'))
    lines.append(txt_row('Policy API  = NSX policy REST API; primary management interface'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('nsx-ops-cli', 'docs/virtualization/vmware/nsx/operations/cli-reference/index.md', 'NSX CLI Reference — NSX Manager CLI, Edge CLI, API commands')
def _nsx_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NSX — CLI Reference'))
    lines.append(txt_row())
    lines.append(txt_row('NSX Manager CLI, Edge Node CLI, and REST API commands for operations.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'NSX Manager CLI'), bMid(L2, R2, 'Edge Node CLI'))))
    lines.append(R(merge(bMid(L1, R1, 'get cluster status'), bMid(L2, R2, 'get logical-routers'))))
    lines.append(R(merge(bMid(L1, R1, 'get management-plane'), bMid(L2, R2, 'get bgp neighbor summary'))))
    lines.append(R(merge(bMid(L1, R1, 'get certificate'), bMid(L2, R2, 'get route table'))))
    lines.append(R(merge(bMid(L1, R1, 'start service <svc>'), bMid(L2, R2, 'ping <IP> vrf <n>'))))
    lines.append(R(merge(bMid(L1, R1, 'get node-uuid'), bMid(L2, R2, 'traceroute <IP>'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Manager CLI for cluster health; Edge CLI for routing/BGP/path checks.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'NSX Policy REST API'), bMid(L2, R2, 'Useful curl Examples'))))
    lines.append(R(merge(bMid(L1, R1, 'GET /policy/api/v1/infra'), bMid(L2, R2, 'curl -k -u admin:pass \\'))))
    lines.append(R(merge(bMid(L1, R1, 'GET /api/v1/cluster/status'), bMid(L2, R2, '-X GET https://mgr/...'))))
    lines.append(R(merge(bMid(L1, R1, 'POST /policy/api/v1/infra/'), bMid(L2, R2, 'jq .results[].status'))))
    lines.append(R(merge(bMid(L1, R1, 'GET /api/v1/transport-nodes'), bMid(L2, R2, 'Token auth: Bearer token'))))
    lines.append(R(merge(bMid(L1, R1, 'DELETE /policy/api/v1/...'), bMid(L2, R2, 'Postman collection NSX'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NSX Manager cluster VMs, Edge VMs on ESXi, management network, vCenter'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('NSX Manager CLI = SSH to manager appliance; admin account access'))
    lines.append(txt_row('Edge CLI      = SSH to edge node; routing, BGP, NAT diagnostics'))
    lines.append(txt_row('Policy API    = NSX REST API /policy/api/v1; primary config interface'))
    lines.append(txt_row('Management API= NSX REST API /api/v1; legacy + infra ops endpoints'))
    lines.append(txt_row('Transport node= ESXi or Edge with N-VDS installed; dataplane element'))
    lines.append(txt_row('BGP neighbor  = Edge peers; get bgp shows session state + prefixes'))
    lines.append(txt_row('VRF           = Virtual Routing and Forwarding; per-router context'))
    lines.append(txt_row('cluster status= manager API; shows CCP/MP health of all 3 nodes'))
    lines.append(txt_row('Bearer token  = JWT token for NSX API auth; alternative to Basic auth'))
    lines.append(txt_row('jq            = JSON query tool; parses NSX API responses in shell'))
    lines.append(txt_row('logical-router= Edge data structure; mapped to T0/T1 gateway object'))
    lines.append(txt_row('node-uuid     = unique ID of NSX appliance; used in API paths'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('nsx-ops-health', 'docs/virtualization/vmware/nsx/operations/health-checks/index.md', 'NSX Health Checks — runbook, cluster health, transport node status')
def _nsx_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NSX — Health Checks'))
    lines.append(txt_row())
    lines.append(txt_row('Daily/weekly health runbook: cluster, transport nodes, edges, and DFW state.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Manager Cluster Health'), bMid(L2, R2, 'Transport Node Health'))))
    lines.append(R(merge(bMid(L1, R1, 'All 3 nodes STABLE'), bMid(L2, R2, 'All ESXi nodes: Success'))))
    lines.append(R(merge(bMid(L1, R1, 'CCP cluster: leader elected'), bMid(L2, R2, 'Edge nodes: Up'))))
    lines.append(R(merge(bMid(L1, R1, 'MP: policy sync active'), bMid(L2, R2, 'N-VDS status green'))))
    lines.append(R(merge(bMid(L1, R1, 'Certificate expiry check'), bMid(L2, R2, 'Tunnel endpoint up'))))
    lines.append(R(merge(bMid(L1, R1, 'Backup age < 24 hours'), bMid(L2, R2, 'BGP sessions established'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Manager health → transport nodes → edge BGP → DFW rule count check.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Edge Gateway Health'), bMid(L2, R2, 'DFW and Policy Health'))))
    lines.append(R(merge(bMid(L1, R1, 'T0 gateway active standby'), bMid(L2, R2, 'DFW rule sync green'))))
    lines.append(R(merge(bMid(L1, R1, 'BGP sessions up/prefixes'), bMid(L2, R2, 'No policy realise errors'))))
    lines.append(R(merge(bMid(L1, R1, 'ECMP paths balanced'), bMid(L2, R2, 'Groups resolved correctly'))))
    lines.append(R(merge(bMid(L1, R1, 'NAT rules active'), bMid(L2, R2, 'Segment VNI table sync'))))
    lines.append(R(merge(bMid(L1, R1, 'Edge CPU < 70%, mem < 80%'), bMid(L2, R2, 'Alarm queue empty'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NSX Manager VMs, Edge VMs, ESXi transport nodes, physical ToR switches'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CCP         = Central Control Plane; distributes config to dataplane'))
    lines.append(txt_row('MP          = Management Plane; NSX policy API and UI backend'))
    lines.append(txt_row('N-VDS       = NSX virtual distributed switch; dataplane on ESXi/Edge'))
    lines.append(txt_row('TEP         = Tunnel Endpoint; VTEP for GENEVE overlay encapsulation'))
    lines.append(txt_row('GENEVE      = tunnel protocol; carries overlay traffic between TEPs'))
    lines.append(txt_row('T0 gateway  = Tier-0; north-south routing; BGP to physical fabric'))
    lines.append(txt_row('DFW         = Distributed Firewall; stateful kernel-level L4 firewall'))
    lines.append(txt_row('ECMP        = Equal Cost Multi-Path; load-balances traffic across paths'))
    lines.append(txt_row('Policy realise = NSX applying config changes to dataplane'))
    lines.append(txt_row('VNI         = VXLAN Network Identifier; unique ID per overlay segment'))
    lines.append(txt_row('STABLE      = NSX Manager cluster status meaning all nodes healthy'))
    lines.append(txt_row('BGP session = Edge peering with physical router; must be Established'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('nsx-ops-install', 'docs/virtualization/vmware/nsx/operations/install-upgrade/index.md', 'NSX Install and Upgrade — deployment, transport nodes, upgrade steps')
def _nsx_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NSX — Install and Upgrade'))
    lines.append(txt_row())
    lines.append(txt_row('NSX Manager OVA deployment, transport node prep, and in-place upgrade flow.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Fresh Deployment'), bMid(L2, R2, 'Upgrade Procedure'))))
    lines.append(R(merge(bMid(L1, R1, 'Deploy Manager OVA x3'), bMid(L2, R2, 'Download upgrade bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'Form cluster (join nodes)'), bMid(L2, R2, 'Upload to NSX Manager'))))
    lines.append(R(merge(bMid(L1, R1, 'Register compute manager'), bMid(L2, R2, 'Run pre-check validation'))))
    lines.append(R(merge(bMid(L1, R1, 'Deploy edge transport nodes'), bMid(L2, R2, 'Upgrade MP → CCP → hosts'))))
    lines.append(R(merge(bMid(L1, R1, 'Prepare ESXi hosts (N-VDS)'), bMid(L2, R2, 'Verify each tier before next'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Deploy manager cluster → compute manager → edges → ESXi transport nodes.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Prerequisites'), bMid(L2, R2, 'Version Compatibility'))))
    lines.append(R(merge(bMid(L1, R1, 'vCenter registered first'), bMid(L2, R2, 'NSX 4.x — current GA'))))
    lines.append(R(merge(bMid(L1, R1, 'IP pool for TEP addresses'), bMid(L2, R2, 'vCenter 7.0+ required'))))
    lines.append(R(merge(bMid(L1, R1, 'Uplink/overlay profiles set'), bMid(L2, R2, 'ESXi 7.0+ for N-VDS 2'))))
    lines.append(R(merge(bMid(L1, R1, 'MTU 1600+ on fabric NICs'), bMid(L2, R2, 'Interop matrix check'))))
    lines.append(R(merge(bMid(L1, R1, 'BGP ASN planned with NetEng'), bMid(L2, R2, 'VCF: use SDDC Mgr LCM'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ESXi hosts, vCenter, physical ToR with BGP, SFTP server, management network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('OVA         = Open Virtualisation Appliance; NSX Manager deploy format'))
    lines.append(txt_row('Compute Mgr = vCenter registered in NSX; source of host inventory'))
    lines.append(txt_row('Transport node = ESXi or Edge with N-VDS installed for overlay'))
    lines.append(txt_row('N-VDS       = NSX managed vSwitch replacing dvSwitch on host'))
    lines.append(txt_row('TEP         = Tunnel Endpoint; source IP for GENEVE overlay traffic'))
    lines.append(txt_row('Uplink profile= defines LAG, teaming, VLAN for TEP traffic'))
    lines.append(txt_row('IP pool     = range of IPs assigned to TEPs during host prep'))
    lines.append(txt_row('MP          = Management Plane; upgraded first in NSX upgrade sequence'))
    lines.append(txt_row('CCP         = Central Control Plane; upgraded second after MP'))
    lines.append(txt_row('SDDC Mgr    = VCF lifecycle mgr; handles NSX upgrades in VCF context'))
    lines.append(txt_row('Pre-check   = NSX upgrade validator; runs before bundle apply'))
    lines.append(txt_row('Interop     = VMware Product Interoperability Matrix for version support'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('nsx-ops-proc', 'docs/virtualization/vmware/nsx/operations/procedures/index.md', 'NSX Standard Procedures — segment add, gateway config, change control')
def _nsx_ops_proc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NSX — Standard Procedures'))
    lines.append(txt_row())
    lines.append(txt_row('Segment creation, T0/T1 gateway config, DFW rule changes, and change control.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Add New Segment'), bMid(L2, R2, 'T1 Gateway Config'))))
    lines.append(R(merge(bMid(L1, R1, 'Policy > Networking > Segments'), bMid(L2, R2, 'Add T1 gateway'))))
    lines.append(R(merge(bMid(L1, R1, 'Set VNI / transport zone'), bMid(L2, R2, 'Link to T0 gateway'))))
    lines.append(R(merge(bMid(L1, R1, 'Set VLAN or overlay mode'), bMid(L2, R2, 'Advertise connected'))))
    lines.append(R(merge(bMid(L1, R1, 'Connect to T1 gateway'), bMid(L2, R2, 'Set edge cluster'))))
    lines.append(R(merge(bMid(L1, R1, 'Attach segment to VM vNIC'), bMid(L2, R2, 'Apply DNS/DHCP profile'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Network change → DFW policy update → change control record → verify.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'DFW Rule Changes'), bMid(L2, R2, 'Change Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Add to security policy'), bMid(L2, R2, 'Raise CR before change'))))
    lines.append(R(merge(bMid(L1, R1, 'Define source/dest groups'), bMid(L2, R2, 'Pre-change packet trace'))))
    lines.append(R(merge(bMid(L1, R1, 'Set service (port/proto)'), bMid(L2, R2, 'Change window agreed'))))
    lines.append(R(merge(bMid(L1, R1, 'Publish policy changes'), bMid(L2, R2, 'Post-change connectivity'))))
    lines.append(R(merge(bMid(L1, R1, 'Verify in traceflow'), bMid(L2, R2, 'Close CR with evidence'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NSX Manager VMs, Edge VMs, ESXi hosts, ToR switches, vCenter, management net'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Segment     = logical L2 overlay network; mapped to a transport zone'))
    lines.append(txt_row('VNI         = VXLAN Network ID; unique per segment in overlay'))
    lines.append(txt_row('Transport zone = scope of overlay or VLAN segment reachability'))
    lines.append(txt_row('T1 gateway  = distributed L3 gateway; service router on edge cluster'))
    lines.append(txt_row('T0 gateway  = north-south routing gateway; BGP peers with fabric'))
    lines.append(txt_row('DFW         = Distributed Firewall; L4 stateful firewall per vNIC'))
    lines.append(txt_row('Security policy = DFW container grouping rules by purpose'))
    lines.append(txt_row('Groups      = NSX dynamic member sets (tag, OS, name, IP criteria)'))
    lines.append(txt_row('Traceflow   = NSX UI tool; injects synthetic packet to trace path/drops'))
    lines.append(txt_row('Publish     = NSX action; commits policy changes to dataplane'))
    lines.append(txt_row('Packet trace= captures before change; confirms expected traffic flow'))
    lines.append(txt_row('CR          = Change Request; ITSM record authorising change'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('nsx-ops-scripts', 'docs/virtualization/vmware/nsx/operations/scripts/index.md', 'NSX Scripts — PowerCLI, Python, Terraform, NSX API automation')
def _nsx_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NSX — Scripts'))
    lines.append(txt_row())
    lines.append(txt_row('NSX REST API, Python, PowerShell, and Terraform scripts for NSX automation.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Python / REST Scripts'), bMid(L2, R2, 'PowerShell Scripts'))))
    lines.append(R(merge(bMid(L1, R1, 'requests.get policy/api/v1'), bMid(L2, R2, 'Invoke-RestMethod NSX'))))
    lines.append(R(merge(bMid(L1, R1, 'List all segments + VNIs'), bMid(L2, R2, 'Get-NsxLogicalSwitch'))))
    lines.append(R(merge(bMid(L1, R1, 'Export DFW rules to CSV'), bMid(L2, R2, 'New-NsxLogicalRouter'))))
    lines.append(R(merge(bMid(L1, R1, 'Bulk group member audit'), bMid(L2, R2, 'Export security policy'))))
    lines.append(R(merge(bMid(L1, R1, 'Health check API poll'), bMid(L2, R2, 'Connect-NSXServer'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('REST API for ops scripts; Terraform for IaC segment and policy deployment.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Terraform IaC'), bMid(L2, R2, 'Automation Patterns'))))
    lines.append(R(merge(bMid(L1, R1, 'provider "nsxt" config'), bMid(L2, R2, 'Idempotent API calls'))))
    lines.append(R(merge(bMid(L1, R1, 'nsxt_policy_segment'), bMid(L2, R2, 'Pagination: cursor param'))))
    lines.append(R(merge(bMid(L1, R1, 'nsxt_policy_security_policy'), bMid(L2, R2, 'Error retry on 429'))))
    lines.append(R(merge(bMid(L1, R1, 'nsxt_policy_tier1_gateway'), bMid(L2, R2, 'Realise status polling'))))
    lines.append(R(merge(bMid(L1, R1, 'terraform plan/apply/destroy'), bMid(L2, R2, 'Token refresh logic'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NSX Manager VMs, management network, jump host, CI/CD runner for Terraform'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('NSX Policy API = /policy/api/v1; primary REST API for all NSX config'))
    lines.append(txt_row('Bearer token  = JWT auth token for NSX API; refresh via /api/session'))
    lines.append(txt_row('Cursor        = NSX API pagination param; use to page large result sets'))
    lines.append(txt_row('429           = HTTP Too Many Requests; NSX rate limit; retry with backoff'))
    lines.append(txt_row('Realise       = NSX applying changes to dataplane; poll status after'))
    lines.append(txt_row('Terraform NSX = HashiCorp provider for NSX; declare infra as HCL'))
    lines.append(txt_row('nsxt_policy_segment = Terraform resource for NSX overlay segment'))
    lines.append(txt_row('PowerNSX      = PowerShell module for NSX; older but widely used'))
    lines.append(txt_row('IaC           = Infrastructure as Code; version-controlled infra config'))
    lines.append(txt_row('Idempotent    = API call safe to repeat; same result every time'))
    lines.append(txt_row('CSV export    = common audit output; DFW rules exported for review'))
    lines.append(txt_row('policy/api/v1 = NSX Policy API base path; preferred over MP API'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('nsx-sec-access', 'docs/virtualization/vmware/nsx/security/access-control/index.md', 'NSX Access Control — RBAC, roles, permission sets, audit')
def _nsx_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NSX — Access Control'))
    lines.append(txt_row())
    lines.append(txt_row('NSX RBAC roles, vCenter-linked permissions, project isolation, and auditing.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'NSX Built-in Roles'), bMid(L2, R2, 'vCenter-Linked Auth'))))
    lines.append(R(merge(bMid(L1, R1, 'Enterprise Admin: full NSX'), bMid(L2, R2, 'SSO integration via vCenter'))))
    lines.append(R(merge(bMid(L1, R1, 'Ops: read + basic changes'), bMid(L2, R2, 'AD groups map to roles'))))
    lines.append(R(merge(bMid(L1, R1, 'Auditor: read only'), bMid(L2, R2, 'LDAP identity source'))))
    lines.append(R(merge(bMid(L1, R1, 'Security Admin: DFW only'), bMid(L2, R2, 'Named service accounts'))))
    lines.append(R(merge(bMid(L1, R1, 'Network Admin: segments/GW'), bMid(L2, R2, 'No shared admin accounts'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Assign least-privilege NSX roles; audit quarterly; remove stale accounts.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Projects (Multi-Tenancy)'), bMid(L2, R2, 'Audit and Review'))))
    lines.append(R(merge(bMid(L1, R1, 'NSX Projects isolate tenants'), bMid(L2, R2, 'NSX Manager audit log'))))
    lines.append(R(merge(bMid(L1, R1, 'Project admin role scoped'), bMid(L2, R2, 'API access recorded'))))
    lines.append(R(merge(bMid(L1, R1, 'Shared T0 / per-project T1'), bMid(L2, R2, 'Export to syslog/SIEM'))))
    lines.append(R(merge(bMid(L1, R1, 'VRF-Lite or full tenant T0'), bMid(L2, R2, 'Role review quarterly'))))
    lines.append(R(merge(bMid(L1, R1, 'Segment scoped per project'), bMid(L2, R2, 'Remove leavers promptly'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NSX Manager VMs, vCenter SSO, AD/LDAP, syslog/SIEM, management network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RBAC       = Role-Based Access Control; role+user+scope model in NSX'))
    lines.append(txt_row('Enterprise Admin = full NSX admin; maps to vSphere Administrator'))
    lines.append(txt_row('Security Admin = DFW and security policy management role only'))
    lines.append(txt_row('Network Admin = segments, gateways, routing; no security policy'))
    lines.append(txt_row('Auditor    = read-only role; can view all config and logs'))
    lines.append(txt_row('Project    = NSX multi-tenancy scope; isolates config per tenant'))
    lines.append(txt_row('VRF-Lite   = T0 virtualisation; multiple routing tables on one T0'))
    lines.append(txt_row('Audit log  = NSX system event log; records all API + UI changes'))
    lines.append(txt_row('SSO        = Single Sign-On; vCenter identity used for NSX login'))
    lines.append(txt_row('SIEM       = Security Information and Event Mgmt; syslog consumer'))
    lines.append(txt_row('Least priv = minimum role needed; avoids over-privileged accounts'))
    lines.append(txt_row('Service acct = named automation account; not shared personal login'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('nsx-sec-auth', 'docs/virtualization/vmware/nsx/security/authentication/index.md', 'NSX Authentication — SSO, AD/LDAP, smart card, local accounts')
def _nsx_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NSX — Authentication'))
    lines.append(txt_row())
    lines.append(txt_row('NSX SSO via vCenter, local admin, LDAP identity source, and API token auth.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'vCenter SSO Integration'), bMid(L2, R2, 'Local Admin Account'))))
    lines.append(R(merge(bMid(L1, R1, 'NSX uses vCenter SSO'), bMid(L2, R2, 'admin user local to NSX'))))
    lines.append(R(merge(bMid(L1, R1, 'AD identity source in SSO'), bMid(L2, R2, 'audit user: read-only'))))
    lines.append(R(merge(bMid(L1, R1, 'Users log into NSX UI via SSO'), bMid(L2, R2, 'guestuser1/2: limited'))))
    lines.append(R(merge(bMid(L1, R1, 'vSphere role → NSX role map'), bMid(L2, R2, 'Change admin password'))))
    lines.append(R(merge(bMid(L1, R1, 'MFA via SSO Radius/RSA'), bMid(L2, R2, 'Disable root if possible'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SSO for UI access; API token or basic auth for automation; AD for ops.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'API Authentication'), bMid(L2, R2, 'Security Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'Basic auth (admin:pass)'), bMid(L2, R2, 'Password complexity policy'))))
    lines.append(R(merge(bMid(L1, R1, 'Bearer token via /api/session'), bMid(L2, R2, 'Account lockout after 5'))))
    lines.append(R(merge(bMid(L1, R1, 'Principal Identity for ops'), bMid(L2, R2, 'Session idle timeout'))))
    lines.append(R(merge(bMid(L1, R1, 'Client certificates option'), bMid(L2, R2, 'Log all auth attempts'))))
    lines.append(R(merge(bMid(L1, R1, 'vIDM integration optional'), bMid(L2, R2, 'Alert on failed logins'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NSX Manager VMs, vCenter SSO, AD/LDAP, Radius/RSA, management network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SSO         = Single Sign-On; vCenter embedded auth used by NSX'))
    lines.append(txt_row('Principal Identity = long-lived API credential for automation services'))
    lines.append(txt_row('Bearer token= JWT session token from /api/session/create; short-lived'))
    lines.append(txt_row('vIDM        = VMware Identity Manager; optional ext auth for NSX'))
    lines.append(txt_row('Local admin = NSX-local admin account; break-glass if SSO fails'))
    lines.append(txt_row('audit user  = read-only local NSX account for compliance review'))
    lines.append(txt_row('MFA         = Multi-Factor Auth; configured in vCenter SSO policy'))
    lines.append(txt_row('Radius      = remote auth server for MFA OTP tokens'))
    lines.append(txt_row('Client cert = X.509 cert used as API client auth credential'))
    lines.append(txt_row('Password policy = NSX local: min length, complexity, rotation'))
    lines.append(txt_row('Lockout     = account disabled after N failed login attempts'))
    lines.append(txt_row('Session timeout = idle session expiry; configurable in NSX'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('nsx-sec-enc', 'docs/virtualization/vmware/nsx/security/encryption/index.md', 'NSX Encryption — overlay encryption, IPSec VPN, TLS, key management')
def _nsx_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NSX — Encryption'))
    lines.append(txt_row())
    lines.append(txt_row('IPSec VPN, L2 VPN, TLS API, GENEVE overlay, and NSX certificate management.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'IPSec VPN'), bMid(L2, R2, 'L2 VPN'))))
    lines.append(R(merge(bMid(L1, R1, 'Route-based or policy-based'), bMid(L2, R2, 'Extends L2 over IPSec'))))
    lines.append(R(merge(bMid(L1, R1, 'IKEv2 recommended'), bMid(L2, R2, 'Client: NSX Edge standalone'))))
    lines.append(R(merge(bMid(L1, R1, 'AES-256-GCM encryption'), bMid(L2, R2, 'Server: NSX Edge in site'))))
    lines.append(R(merge(bMid(L1, R1, 'DH group 20 (ECDH)'), bMid(L2, R2, 'Stretches segment across DC'))))
    lines.append(R(merge(bMid(L1, R1, 'Per-T0 or per-T1 VPN'), bMid(L2, R2, 'Use case: DC migration'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('IPSec encrypts north-south; TLS secures manager API; certs managed in NSX.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'TLS and Certificate Mgmt'), bMid(L2, R2, 'Overlay Encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'NSX API: TLS 1.2/1.3 only'), bMid(L2, R2, 'GENEVE tunnel: no default'))))
    lines.append(R(merge(bMid(L1, R1, 'Replace self-signed with CA'), bMid(L2, R2, 'vMotion enc: on overlay'))))
    lines.append(R(merge(bMid(L1, R1, 'CSR workflow in NSX UI'), bMid(L2, R2, 'IPSec ESP encrypts flow'))))
    lines.append(R(merge(bMid(L1, R1, 'Cert expiry alarm: 60 days'), bMid(L2, R2, 'TLS between manager nodes'))))
    lines.append(R(merge(bMid(L1, R1, 'Auto-renew via ACME/CA'), bMid(L2, R2, 'Mgmt plane: mTLS nodes'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NSX Manager VMs, Edge VMs, physical ToR, CA server, management network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('IPSec       = IP Security; encrypts site-to-site or remote access VPN'))
    lines.append(txt_row('IKEv2       = Internet Key Exchange v2; tunnel setup protocol for IPSec'))
    lines.append(txt_row('AES-256-GCM = AES cipher in Galois/Counter Mode; authenticated encryption'))
    lines.append(txt_row('DH group 20 = ECDH P-384; key exchange group for IPSec'))
    lines.append(txt_row('L2 VPN      = stretches L2 segment across sites over encrypted tunnel'))
    lines.append(txt_row('GENEVE      = overlay protocol for NSX segments; tunnels between TEPs'))
    lines.append(txt_row('mTLS        = mutual TLS; both sides authenticate with certs'))
    lines.append(txt_row('CSR         = Certificate Signing Request; sent to CA for signing'))
    lines.append(txt_row('ACME        = auto cert renewal protocol; used with Let\'s Encrypt type CA'))
    lines.append(txt_row('ESP         = Encapsulating Security Payload; IPSec encryption header'))
    lines.append(txt_row('Route-based = IPSec with VTI; preferred; supports dynamic routing'))
    lines.append(txt_row('Policy-based= IPSec with selectors; legacy; no dynamic routing'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('nsx-sec-hard', 'docs/virtualization/vmware/nsx/security/hardening/index.md', 'NSX Hardening — CIS benchmark, API security, DFW default policy')
def _nsx_sec_hard():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NSX — Hardening'))
    lines.append(txt_row())
    lines.append(txt_row('CIS NSX benchmark, API security, DFW default-deny, and lockdown posture.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'CIS / STIG Controls'), bMid(L2, R2, 'API Security'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable root SSH on manager'), bMid(L2, R2, 'TLS 1.2+ only'))))
    lines.append(R(merge(bMid(L1, R1, 'Change default admin pass'), bMid(L2, R2, 'Disable TLS 1.0/1.1'))))
    lines.append(R(merge(bMid(L1, R1, 'NTP configured on all nodes'), bMid(L2, R2, 'Replace self-signed certs'))))
    lines.append(R(merge(bMid(L1, R1, 'Syslog to SIEM/syslog host'), bMid(L2, R2, 'Rate limit API calls'))))
    lines.append(R(merge(bMid(L1, R1, 'FIPS mode if required'), bMid(L2, R2, 'Named service accounts only'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Baseline hardening → DFW default-deny policy → regular audit reviews.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'DFW Default Policy'), bMid(L2, R2, 'Hardening Review'))))
    lines.append(R(merge(bMid(L1, R1, 'Default layer: deny + log'), bMid(L2, R2, 'Review DFW rules monthly'))))
    lines.append(R(merge(bMid(L1, R1, 'Emergency allow above default'), bMid(L2, R2, 'Alert on new allow-all'))))
    lines.append(R(merge(bMid(L1, R1, 'Micro-seg by app / zone'), bMid(L2, R2, 'Check cert expiry < 60d'))))
    lines.append(R(merge(bMid(L1, R1, 'Log all blocked traffic'), bMid(L2, R2, 'Verify FIPS if mandated'))))
    lines.append(R(merge(bMid(L1, R1, 'Gateway firewall as perimeter'), bMid(L2, R2, 'Audit role assignments'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NSX Manager VMs, Edge VMs, ESXi hosts, syslog/SIEM, management network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CIS         = Center for Internet Security; NSX hardening benchmark'))
    lines.append(txt_row('STIG        = Security Technical Implementation Guide; DOD hardening'))
    lines.append(txt_row('FIPS 140-2  = US crypto standard; NSX FIPS mode enforces compliant algos'))
    lines.append(txt_row('DFW default = last DFW rule; set to deny+log to block unmatched traffic'))
    lines.append(txt_row('Micro-seg   = per-VM/app firewall rules; east-west security enforcement'))
    lines.append(txt_row('Gateway FW  = NSX Edge firewall; north-south perimeter rule enforcement'))
    lines.append(txt_row('TLS 1.2     = minimum TLS for NSX API; 1.3 preferred'))
    lines.append(txt_row('SIEM        = Security Info & Event Mgmt; receives NSX syslog'))
    lines.append(txt_row('Rate limit  = API throttle; prevents brute force or runaway scripts'))
    lines.append(txt_row('Root SSH    = disabled on NSX Manager appliance in hardened config'))
    lines.append(txt_row('Named accts = automation uses dedicated named service accounts'))
    lines.append(txt_row('NTP         = time sync; required for cert validity and log correlation'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('nsx-ts-common', 'docs/virtualization/vmware/nsx/troubleshooting/common-issues/index.md', 'NSX Common Issues — BGP down, DFW drops, transport node failures')
def _nsx_ts_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NSX — Common Issues'))
    lines.append(txt_row())
    lines.append(txt_row('BGP session down, DFW unexpected drops, transport node failures, and fixes.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'BGP / Routing Issues'), bMid(L2, R2, 'DFW Drop Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'Session Idle or Connect'), bMid(L2, R2, 'Traffic unexpectedly dropped'))))
    lines.append(R(merge(bMid(L1, R1, 'Check Edge uplink VLAN'), bMid(L2, R2, 'Check DFW rule order'))))
    lines.append(R(merge(bMid(L1, R1, 'Verify BGP timers match'), bMid(L2, R2, 'Enable DFW flow logs'))))
    lines.append(R(merge(bMid(L1, R1, 'Check ASN/neighbor IP'), bMid(L2, R2, 'Use Traceflow tool'))))
    lines.append(R(merge(bMid(L1, R1, 'get bgp neighbor summary'), bMid(L2, R2, 'Check group membership'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('BGP/routing diagnosis first; DFW Traceflow for east-west drop issues.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Transport Node Issues'), bMid(L2, R2, 'Manager Cluster Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'Node shows degraded'), bMid(L2, R2, 'Node shows DEGRADED'))))
    lines.append(R(merge(bMid(L1, R1, 'Check NSX agent on ESXi'), bMid(L2, R2, 'Check disk space on mgr'))))
    lines.append(R(merge(bMid(L1, R1, 'Resync transport node'), bMid(L2, R2, 'Restart proton service'))))
    lines.append(R(merge(bMid(L1, R1, 'Check TEP connectivity'), bMid(L2, R2, 'Verify NTP in sync'))))
    lines.append(R(merge(bMid(L1, R1, 'N-VDS mtu / uplink check'), bMid(L2, R2, 'Check /var/log/proton'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NSX Manager VMs, Edge VMs, ESXi transport nodes, ToR switches, vCenter'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('BGP session = routing peer; Idle/Connect = not established'))
    lines.append(txt_row('Traceflow   = NSX tool; sends test packet to debug path/drops'))
    lines.append(txt_row('DFW flow log= per-rule hit log; enabled in rule settings'))
    lines.append(txt_row('Transport node = ESXi/Edge with N-VDS; resync forces config refresh'))
    lines.append(txt_row('TEP         = Tunnel Endpoint; GENEVE source; ping to verify'))
    lines.append(txt_row('N-VDS       = NSX distributed switch; check uplink binding'))
    lines.append(txt_row('proton      = NSX Manager core service; restart to recover stuck state'))
    lines.append(txt_row('DEGRADED    = NSX cluster status; one or more nodes unhealthy'))
    lines.append(txt_row('Group memb  = DFW group members; wrong group = wrong firewall policy'))
    lines.append(txt_row('ASN         = Autonomous System Number; must match on BGP peers'))
    lines.append(txt_row('Edge uplink = VLAN uplink on Edge to physical switch; check tagging'))
    lines.append(txt_row('Resync      = NSX Manager pushes config to transport node again'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('nsx-ts-diag', 'docs/virtualization/vmware/nsx/troubleshooting/diagnostics/index.md', 'NSX Diagnostics — log locations, Traceflow, support bundle')
def _nsx_ts_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NSX — Diagnostics'))
    lines.append(txt_row())
    lines.append(txt_row('NSX log locations, Traceflow tool, IPFIX flow export, and support bundles.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Key Log Files'), bMid(L2, R2, 'Traceflow Tool'))))
    lines.append(R(merge(bMid(L1, R1, '/var/log/proton (manager)'), bMid(L2, R2, 'NSX UI: Plan > Traceflow'))))
    lines.append(R(merge(bMid(L1, R1, '/var/log/nsx-syslog'), bMid(L2, R2, 'Inject L2/L3/L4 packet'))))
    lines.append(R(merge(bMid(L1, R1, '/var/log/bfd.log (routing)'), bMid(L2, R2, 'See path hop by hop'))))
    lines.append(R(merge(bMid(L1, R1, 'ESXi: /var/log/nsx-*.log'), bMid(L2, R2, 'Identify drop + rule hit'))))
    lines.append(R(merge(bMid(L1, R1, 'Edge: /var/log/nsx-*.log'), bMid(L2, R2, 'Bidirectional trace'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Logs → Traceflow for path/DFW → IPFIX for flows → bundle for GSS.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'IPFIX / Flow Export'), bMid(L2, R2, 'Support Bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'DFW IPFIX per-rule export'), bMid(L2, R2, 'UI: System > Support Bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'Collector: Aria NI / sflow'), bMid(L2, R2, 'API: POST /api/v1/suppbndl'))))
    lines.append(R(merge(bMid(L1, R1, 'Flow visibility map build'), bMid(L2, R2, 'Includes all node logs'))))
    lines.append(R(merge(bMid(L1, R1, 'Used for micro-seg planning'), bMid(L2, R2, 'Select: manager + edges'))))
    lines.append(R(merge(bMid(L1, R1, 'Identify undocumented flows'), bMid(L2, R2, 'Upload to VMware SR'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NSX Manager VMs, Edge VMs, ESXi nodes, IPFIX collector, management network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('proton log  = NSX Manager core process log; cluster/config events'))
    lines.append(txt_row('Traceflow   = NSX packet path simulation; shows rule hits and drops'))
    lines.append(txt_row('IPFIX       = IP Flow Info Export; protocol for DFW flow telemetry'))
    lines.append(txt_row('Aria NI     = Aria Network Insight; NSX flow analytics platform'))
    lines.append(txt_row('sFlow       = sampling protocol; alternative to IPFIX for flows'))
    lines.append(txt_row('BFD         = Bidirectional Forwarding Detection; fast link failure detect'))
    lines.append(txt_row('nsx-syslog  = aggregated NSX system log; forwarded to SIEM'))
    lines.append(txt_row('Support bundle = NSX zip; all nodes logs + configs for GSS'))
    lines.append(txt_row('SR          = Service Request; VMware GSS support ticket'))
    lines.append(txt_row('Drop observation = Traceflow result showing which rule blocked packet'))
    lines.append(txt_row('Flow visibility = map of who talks to whom; built from IPFIX data'))
    lines.append(txt_row('Bidirectional= Traceflow sends packets in both directions simultaneously'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('nsx-ts-esc', 'docs/virtualization/vmware/nsx/troubleshooting/escalation/index.md', 'NSX Escalation — VMware GSS, support bundle, severity levels')
def _nsx_ts_esc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NSX — Escalation'))
    lines.append(txt_row())
    lines.append(txt_row('VMware GSS escalation, pre-escalation steps, severity matrix, bundle contents.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Escalation Triggers'), bMid(L2, R2, 'Pre-Escalation Steps'))))
    lines.append(R(merge(bMid(L1, R1, 'Manager cluster DEGRADED'), bMid(L2, R2, 'Collect support bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'BGP flapping unexplained'), bMid(L2, R2, 'Document symptoms + time'))))
    lines.append(R(merge(bMid(L1, R1, 'DFW drops all traffic'), bMid(L2, R2, 'Run Traceflow and capture'))))
    lines.append(R(merge(bMid(L1, R1, 'Upgrade failed mid-way'), bMid(L2, R2, 'Note NSX + vCenter version'))))
    lines.append(R(merge(bMid(L1, R1, 'Data plane unreachable'), bMid(L2, R2, 'Verify HCL and interop'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Internal triage → bundle → VMware SR → severity assignment → bridge.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Severity Matrix'), bMid(L2, R2, 'Support Bundle Contents'))))
    lines.append(R(merge(bMid(L1, R1, 'S1: network down / data loss'), bMid(L2, R2, 'Manager + edge + host logs'))))
    lines.append(R(merge(bMid(L1, R1, 'S2: major feature broken'), bMid(L2, R2, 'Traceflow trace export'))))
    lines.append(R(merge(bMid(L1, R1, 'S3: degraded with workaround'), bMid(L2, R2, 'IPFIX collector data'))))
    lines.append(R(merge(bMid(L1, R1, 'S4: question or how-to'), bMid(L2, R2, 'Config export (API/UI)'))))
    lines.append(R(merge(bMid(L1, R1, 'S1 = 24x7 phone support'), bMid(L2, R2, 'Timeline of events'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NSX Manager VMs, Edge VMs, ESXi nodes, ToR switches, vCenter, OOB access'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('GSS         = Global Support Services; VMware support organisation'))
    lines.append(txt_row('SR          = Service Request; VMware ticket raised on my.vmware.com'))
    lines.append(txt_row('S1          = Severity 1; network down/data loss; 24x7 phone response'))
    lines.append(txt_row('S2          = Severity 2; major degradation but workaround exists'))
    lines.append(txt_row('Support bundle = NSX diagnostic archive; manager + edge + hosts'))
    lines.append(txt_row('DEGRADED    = NSX Manager cluster health status indicating node failure'))
    lines.append(txt_row('BGP flapping= BGP session cycling between up and down rapidly'))
    lines.append(txt_row('Traceflow   = NSX path debug tool; export results for GSS'))
    lines.append(txt_row('Interop     = VMware Interoperability Matrix; check version support'))
    lines.append(txt_row('HCL         = VMware Hardware Compatibility List; verify NICs/HBAs'))
    lines.append(txt_row('Phone bridge= S1 SR triggers live call with VMware engineer'))
    lines.append(txt_row('Config export = API GET of all NSX config; provides GSS full picture'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines



@kb_diagram(
    'vcenter-arch-how',
    'docs/virtualization/vmware/vcenter/architecture/how-it-works/index.md',
    'vCenter Server — How It Works',
)
def vcenter_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vCenter Server — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('vCenter Server is the centralised management platform for vSphere; all'))
    lines.append(txt_row('ESXi hosts, VMs, clusters, and policies are controlled through its APIs.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Client Layer'), bMid(L2, R2, 'API / Service Layer'))))
    lines.append(R(merge(bMid(L1, R1, 'vSphere Client (HTML5 UI)'), bMid(L2, R2, 'REST API + SOAP API'))))
    lines.append(R(merge(bMid(L1, R1, 'CLI: govc, PowerCLI'), bMid(L2, R2, 'SSO token auth for calls'))))
    lines.append(R(merge(bMid(L1, R1, 'SDKs: Python, Go, Java'), bMid(L2, R2, 'vCenter API gateway'))))
    lines.append(R(merge(bMid(L1, R1, 'vCenter Mob browser'), bMid(L2, R2, 'Task / event bus'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Client requests hit the API gateway; SSO validates the token before any operation.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Core Services'), bMid(L2, R2, 'Host Agent (vpxa)'))))
    lines.append(R(merge(bMid(L1, R1, 'Inventory: hosts/VMs/nets'), bMid(L2, R2, 'Runs on each ESXi host'))))
    lines.append(R(merge(bMid(L1, R1, 'Scheduler: DRS/HA/DPM'), bMid(L2, R2, 'Relays tasks to hostd'))))
    lines.append(R(merge(bMid(L1, R1, 'Storage: SDRS/profiles'), bMid(L2, R2, 'Reports events up to VC'))))
    lines.append(R(merge(bMid(L1, R1, 'Postgres DB: full state'), bMid(L2, R2, 'Reconnects on VC restart'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vCenter Server Appliance (VCSA) runs as a Linux VM on an ESXi host; requires'))
    lines.append(txt_row('shared storage and management network reachability from all managed hosts.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VCSA          = vCenter Server Appliance; OVA-deployed Photon OS VM'))
    lines.append(txt_row('vpxd          = vCenter Server daemon; core process; crash restarts service'))
    lines.append(txt_row('vpxa          = vCenter agent on each ESXi host; bridges host and vCenter'))
    lines.append(txt_row('hostd         = host daemon on ESXi; handles VM power ops, storage, network'))
    lines.append(txt_row('PSC           = Platform Services Controller; merged into VCSA 7.0+'))
    lines.append(txt_row('SSO           = Single Sign-On; identity store; issues SAML tokens for API'))
    lines.append(txt_row('DRS           = Distributed Resource Scheduler; automates VM placement'))
    lines.append(txt_row('HA            = High Availability; restarts VMs on host failure automatically'))
    lines.append(txt_row('DPM           = Distributed Power Management; powers off idle hosts'))
    lines.append(txt_row('SDRS          = Storage DRS; balances datastore utilisation automatically'))
    lines.append(txt_row('vDS           = vSphere Distributed Switch; managed centrally from vCenter'))
    lines.append(txt_row('Inventory     = hierarchical object tree: DC → cluster → host → VM'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-arch-int',
    'docs/virtualization/vmware/vcenter/architecture/integrations/index.md',
    'vCenter Server — Integrations',
)
def vcenter_arch_int():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vCenter Server — Integrations'))
    lines.append(txt_row())
    lines.append(txt_row('vCenter integrates with identity, storage, network, backup, and monitoring'))
    lines.append(txt_row('systems via standardised APIs and plugin frameworks.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Identity Integrations'), bMid(L2, R2, 'Storage Integrations'))))
    lines.append(R(merge(bMid(L1, R1, 'Active Directory via LDAP'), bMid(L2, R2, 'VASA: storage policies'))))
    lines.append(R(merge(bMid(L1, R1, 'SAML IdP federation'), bMid(L2, R2, 'vVols: per-VM volumes'))))
    lines.append(R(merge(bMid(L1, R1, 'SSO local domain'), bMid(L2, R2, 'NFS / iSCSI / FC mounts'))))
    lines.append(R(merge(bMid(L1, R1, 'MFA via smart card/RADIUS'), bMid(L2, R2, 'HCI: vSAN integrated'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Identity gates all logins; storage providers register via VASA for policy management.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Network & Security'), bMid(L2, R2, 'Backup & Monitoring'))))
    lines.append(R(merge(bMid(L1, R1, 'NSX: SDN via vCenter'), bMid(L2, R2, 'VADP: backup API'))))
    lines.append(R(merge(bMid(L1, R1, 'vDS: distributed switching'), bMid(L2, R2, 'CBT: changed block track'))))
    lines.append(R(merge(bMid(L1, R1, 'Firewall rules via NSX'), bMid(L2, R2, 'vROps: perf monitoring'))))
    lines.append(R(merge(bMid(L1, R1, 'Microsegmentation policy'), bMid(L2, R2, 'SNMP / syslog export'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Integration traffic crosses the management network; VADP uses NBD or SAN transport.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VADP    = vStorage APIs for Data Protection; backup quiescing and CBT'))
    lines.append(txt_row('CBT     = Changed Block Tracking; incremental backup efficiency mechanism'))
    lines.append(txt_row('VASA    = vSphere APIs for Storage Awareness; policy-based storage mgmt'))
    lines.append(txt_row('vVols   = Virtual Volumes; per-VM storage objects on VASA-capable arrays'))
    lines.append(txt_row('vDS     = vSphere Distributed Switch; centralised network config in VC'))
    lines.append(txt_row('NSX     = Network & Security virtualisation; integrates with vCenter'))
    lines.append(txt_row('vROps   = VMware Aria Operations; pulls metrics via vCenter APIs'))
    lines.append(txt_row('SAML    = Security Assertion Markup Language; federated SSO token format'))
    lines.append(txt_row('LDAP    = Lightweight Directory Access Protocol; AD identity source'))
    lines.append(txt_row('NBD     = Network Block Device; backup transport over TCP (slower)'))
    lines.append(txt_row('SAN     = Storage Area Network; fast backup transport via FC/iSCSI'))
    lines.append(txt_row('HCI     = Hyper-Converged Infrastructure; vSAN = primary HCI integration'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-arch-design',
    'docs/virtualization/vmware/vcenter/architecture/design-standards/index.md',
    'vCenter Server — Design Standards',
)
def vcenter_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vCenter Server — Design Standards'))
    lines.append(txt_row())
    lines.append(txt_row('Design standards define sizing, HA topology, network placement, and upgrade'))
    lines.append(txt_row('sequencing to ensure a stable and supportable vCenter deployment.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Sizing Standards'), bMid(L2, R2, 'HA & Resilience'))))
    lines.append(R(merge(bMid(L1, R1, 'Tiny: ≤10 hosts, 100 VMs'), bMid(L2, R2, 'vCenter HA: active-passive'))))
    lines.append(R(merge(bMid(L1, R1, 'Small: ≤100 hosts, 1k VMs'), bMid(L2, R2, 'Witness node: tiebreaker'))))
    lines.append(R(merge(bMid(L1, R1, 'Medium: ≤400 hosts, 4k VMs'), bMid(L2, R2, 'Backup: file-based daily'))))
    lines.append(R(merge(bMid(L1, R1, 'Large: ≤1k hosts, 10k VMs'), bMid(L2, R2, 'RPO: 24h; RTO: <1h'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Size to the largest projected inventory; HA mode requires 3 VCSA nodes.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Network Placement'), bMid(L2, R2, 'Upgrade Sequencing'))))
    lines.append(R(merge(bMid(L1, R1, 'Mgmt network: dedicated NIC'), bMid(L2, R2, 'Always upgrade VC first'))))
    lines.append(R(merge(bMid(L1, R1, 'DNS: A + PTR required'), bMid(L2, R2, 'Then upgrade ESXi hosts'))))
    lines.append(R(merge(bMid(L1, R1, 'NTP: same source as hosts'), bMid(L2, R2, 'Then NSX, then tools'))))
    lines.append(R(merge(bMid(L1, R1, 'Static IP: no DHCP for VC'), bMid(L2, R2, 'Snapshot VC before patch'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('VCSA runs on an ESXi host with local/shared storage; management network is separate'))
    lines.append(txt_row('from VM network; dedicated NIC or VLAN on management vDS.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vCenter HA   = active/passive VCSA pair + witness; auto-failover in ~60s'))
    lines.append(txt_row('Witness      = third VCSA node providing quorum vote; no data replica'))
    lines.append(txt_row('File-based   = VCSA built-in backup; schedule via VAMI; excludes stats DB'))
    lines.append(txt_row('VAMI         = vCenter Appliance Management Interface; port 5480'))
    lines.append(txt_row('RPO          = Recovery Point Objective; max data loss window'))
    lines.append(txt_row('RTO          = Recovery Time Objective; max acceptable downtime'))
    lines.append(txt_row('NTP          = time sync; clock skew >5min breaks SSO certificates'))
    lines.append(txt_row('DNS PTR      = reverse lookup record; required for FQDN-based trust'))
    lines.append(txt_row('Upgrade seq  = vCenter first; NSX/tools after; prevents API mismatch'))
    lines.append(txt_row('Snapshot     = pre-upgrade rollback point; remove within 24–72h'))
    lines.append(txt_row('Management vDS= dedicated distributed switch for management traffic'))
    lines.append(txt_row('Static IP    = required; DHCP lease expiry causes cert/DNS mismatch'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-ops-backup',
    'docs/virtualization/vmware/vcenter/operations/backup-restore/index.md',
    'vCenter Server — Backup & Restore',
)
def vcenter_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vCenter Server — Backup & Restore'))
    lines.append(txt_row())
    lines.append(txt_row('vCenter provides built-in file-based backup via VAMI; image-level backup via'))
    lines.append(txt_row('third-party tools using VADP; restore rebuilds the appliance from backup files.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Backup Methods'), bMid(L2, R2, 'Backup Scope'))))
    lines.append(R(merge(bMid(L1, R1, 'File-based: VAMI schedule'), bMid(L2, R2, 'Config: inventory + policy'))))
    lines.append(R(merge(bMid(L1, R1, 'Protocols: FTP/FTPS/HTTP/SCP'), bMid(L2, R2, 'Events & tasks DB'))))
    lines.append(R(merge(bMid(L1, R1, 'Image-based: 3rd party tools'), bMid(L2, R2, 'Stats DB excluded by default'))))
    lines.append(R(merge(bMid(L1, R1, 'Schedule: daily minimum'), bMid(L2, R2, 'Certs included in backup'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('File-based backup exports VCSA config; restore deploys a new VCSA then imports.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Restore Procedure'), bMid(L2, R2, 'Validation Steps'))))
    lines.append(R(merge(bMid(L1, R1, 'Deploy new VCSA OVA'), bMid(L2, R2, 'Verify host connectivity'))))
    lines.append(R(merge(bMid(L1, R1, 'Point to backup location'), bMid(L2, R2, 'Check SSO login works'))))
    lines.append(R(merge(bMid(L1, R1, 'Stage 1: appliance setup'), bMid(L2, R2, 'Confirm inventory intact'))))
    lines.append(R(merge(bMid(L1, R1, 'Stage 2: data restore'), bMid(L2, R2, 'Validate alarms/policies'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Backup target must be reachable from VCSA management network; backup files are'))
    lines.append(txt_row('compressed tarballs; restore needs network access to backup server.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VAMI         = vCenter Appliance Management Interface; port 5480'))
    lines.append(txt_row('File-based   = VCSA native backup; transfers config + DB to remote server'))
    lines.append(txt_row('Image-based  = full VMDK snapshot backup; requires quiescing or powered-off'))
    lines.append(txt_row('VADP         = vStorage APIs for Data Protection; 3rd-party backup API'))
    lines.append(txt_row('SCP          = Secure Copy; encrypted file transfer for backup destination'))
    lines.append(txt_row('Stage 1/2    = two-phase restore: deploy appliance, then restore config'))
    lines.append(txt_row('Stats DB     = performance metrics DB; excluded from default backup scope'))
    lines.append(txt_row('Retention    = number of backup copies to keep; set in VAMI scheduler'))
    lines.append(txt_row('Encryption   = backup password encrypts the tarball at rest'))
    lines.append(txt_row('RTO          = target restore time; typically <1h for file-based restore'))
    lines.append(txt_row('Quiescing    = VADP flush; ensures consistent VM disk state during backup'))
    lines.append(txt_row('Tarball      = compressed archive format used by VCSA file-based backup'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-ops-cli',
    'docs/virtualization/vmware/vcenter/operations/cli-reference/index.md',
    'vCenter Server — CLI Reference',
)
def vcenter_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vCenter Server — CLI Reference'))
    lines.append(txt_row())
    lines.append(txt_row('vCenter is primarily managed via the HTML5 UI, but PowerCLI, govc, and the'))
    lines.append(txt_row('VCSA appliance shell provide CLI automation and troubleshooting capabilities.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'PowerCLI Commands'), bMid(L2, R2, 'govc Commands'))))
    lines.append(R(merge(bMid(L1, R1, 'Connect-VIServer -Server vc'), bMid(L2, R2, 'govc about (VC version)'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-VM | Sort Name'), bMid(L2, R2, 'govc ls / (inventory tree)'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-VMHost | Sort State'), bMid(L2, R2, 'govc vm.info <vm>'))))
    lines.append(R(merge(bMid(L1, R1, 'Move-VM -Destination $host'), bMid(L2, R2, 'govc host.info <host>'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('PowerCLI connects via REST/SOAP; govc uses vSphere REST API natively.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'VCSA Appliance Shell'), bMid(L2, R2, 'vCenter API (REST)'))))
    lines.append(R(merge(bMid(L1, R1, 'service-control --status'), bMid(L2, R2, 'GET /api/vcenter/vm'))))
    lines.append(R(merge(bMid(L1, R1, 'service-control --restart'), bMid(L2, R2, 'POST /api/vcenter/vm'))))
    lines.append(R(merge(bMid(L1, R1, 'vmon-cli -l (list svcs)'), bMid(L2, R2, 'GET /api/vcenter/host'))))
    lines.append(R(merge(bMid(L1, R1, 'vcsa-util backup (CLI bkp)'), bMid(L2, R2, 'Bearer token auth'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('All CLI tools connect over TCP to vCenter management IP; shell access is via SSH'))
    lines.append(txt_row('on port 22 (must be enabled in VAMI or appliance console).'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('PowerCLI       = VMware PowerShell module; wraps vSphere SOAP/REST APIs'))
    lines.append(txt_row('govc           = open-source Go CLI for vSphere REST API automation'))
    lines.append(txt_row('vmon-cli       = vCenter service control; lists and manages VCSA services'))
    lines.append(txt_row('service-control= wrapper for vmon-cli; used in support bundles'))
    lines.append(txt_row('vcsa-util      = appliance utility; backup, restore, certificate ops'))
    lines.append(txt_row('VCSA shell     = Bash shell accessed via SSH; restricted by default'))
    lines.append(txt_row('REST API       = modern vSphere API; JSON; bearer token auth'))
    lines.append(txt_row('SOAP API       = legacy vSphere API; XML; session ticket auth'))
    lines.append(txt_row('Bearer token   = short-lived JWT obtained from POST /api/session'))
    lines.append(txt_row('GOVC_URL       = env var: https://user:pass@vc-fqdn for govc'))
    lines.append(txt_row('Inventory path = /dc/vm/folder/name; used in govc ls and vm.info'))
    lines.append(txt_row('SSH enable     = VAMI > Access > SSH login; off by default'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-ops-health',
    'docs/virtualization/vmware/vcenter/operations/health-checks/index.md',
    'vCenter Server — Health Checks',
)
def vcenter_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vCenter Server — Health Checks'))
    lines.append(txt_row())
    lines.append(txt_row('Regular vCenter health checks verify service state, certificate validity, database'))
    lines.append(txt_row('health, and host connectivity to prevent silent failures.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Service Health'), bMid(L2, R2, 'Certificate Health'))))
    lines.append(R(merge(bMid(L1, R1, 'VAMI: Summary panel green'), bMid(L2, R2, 'Cert expiry >30 days'))))
    lines.append(R(merge(bMid(L1, R1, 'vmon-cli -l: all RUNNING'), bMid(L2, R2, 'STS cert: renew yearly'))))
    lines.append(R(merge(bMid(L1, R1, 'SSO: login works normally'), bMid(L2, R2, 'Machine cert: auto-renew'))))
    lines.append(R(merge(bMid(L1, R1, 'Events: no critical alarms'), bMid(L2, R2, 'certmgr: check via CLI'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Check services first; certificate expiry is the most common silent failure mode.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Database & Disk'), bMid(L2, R2, 'Host Connectivity'))))
    lines.append(R(merge(bMid(L1, R1, 'Postgres: no vacuums stuck'), bMid(L2, R2, 'All hosts: Connected'))))
    lines.append(R(merge(bMid(L1, R1, 'Disk usage <80% on /storage'), bMid(L2, R2, 'vpxa heartbeat: <60s ago'))))
    lines.append(R(merge(bMid(L1, R1, 'Stats DB: no overflow'), bMid(L2, R2, 'DRS: no red clusters'))))
    lines.append(R(merge(bMid(L1, R1, 'Backup: last run <24h ago'), bMid(L2, R2, 'HA: no admission failures'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('VCSA health depends on underlying ESXi host resource availability and shared'))
    lines.append(txt_row('storage connectivity; network latency to hosts must be <10ms.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VAMI         = vCenter Appliance Management Interface; port 5480'))
    lines.append(txt_row('vmon-cli     = service monitor; RUNNING state = healthy'))
    lines.append(txt_row('STS cert     = Security Token Service cert; 2-year expiry; breaks SSO if expired'))
    lines.append(txt_row('Machine cert = VCSA machine SSL cert; auto-renewed by default'))
    lines.append(txt_row('certmgr      = certificate manager utility on VCSA appliance shell'))
    lines.append(txt_row('vpxa         = host agent; heartbeat to vCenter; disconnect = host error'))
    lines.append(txt_row('Postgres     = VCSA embedded DB; vacuum stuck = performance degradation'))
    lines.append(txt_row('/storage     = VCSA data partition; events, stats, logs stored here'))
    lines.append(txt_row('HA admission = cluster reserves capacity for one host failure; red if short'))
    lines.append(txt_row('DRS red      = DRS migration imbalance or constraint violation'))
    lines.append(txt_row('Stats DB     = performance metrics; rollup jobs run on schedule'))
    lines.append(txt_row('certmgr      = /usr/lib/vmware-vmca/bin/certool for cert inspection'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-ops-install',
    'docs/virtualization/vmware/vcenter/operations/install-upgrade/index.md',
    'vCenter Server — Install & Upgrade',
)
def vcenter_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vCenter Server — Install & Upgrade'))
    lines.append(txt_row())
    lines.append(txt_row('vCenter is deployed as an OVA; upgrades use the built-in VCSA installer ISO'))
    lines.append(txt_row('which migrates config from the old appliance in two stages.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Pre-Install Checklist'), bMid(L2, R2, 'Deployment Steps'))))
    lines.append(R(merge(bMid(L1, R1, 'DNS A + PTR records ready'), bMid(L2, R2, 'Mount ISO on jump host'))))
    lines.append(R(merge(bMid(L1, R1, 'NTP configured on hosts'), bMid(L2, R2, 'Run vcsa-ui-installer'))))
    lines.append(R(merge(bMid(L1, R1, 'Port 443/80/9443 open'), bMid(L2, R2, 'Stage 1: OVA deploy'))))
    lines.append(R(merge(bMid(L1, R1, 'SSO password complexity met'), bMid(L2, R2, 'Stage 2: configure SSO'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Pre-install DNS and NTP are critical; failures here block SSO certificate issuance.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Upgrade Pre-Checks'), bMid(L2, R2, 'Upgrade Procedure'))))
    lines.append(R(merge(bMid(L1, R1, 'Snapshot old VCSA'), bMid(L2, R2, 'ISO: vcsa-deploy upgrade'))))
    lines.append(R(merge(bMid(L1, R1, 'Run Pre-Upgrade Checker'), bMid(L2, R2, 'Stage 1: new VCSA boots'))))
    lines.append(R(merge(bMid(L1, R1, 'Check cert expiry first'), bMid(L2, R2, 'Stage 2: config migrated'))))
    lines.append(R(merge(bMid(L1, R1, 'Drain old VC of snapshots'), bMid(L2, R2, 'Old VC powered off after'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Target ESXi host needs sufficient RAM/CPU/storage for VCSA size tier;'))
    lines.append(txt_row('upgrade deploys a second appliance temporarily (needs 2x storage).'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VCSA installer = GUI/CLI ISO tool; runs on Windows/Linux/Mac jump host'))
    lines.append(txt_row('vcsa-deploy    = CLI installer included in the VCSA ISO'))
    lines.append(txt_row('Stage 1        = OVA deployment; network and storage config'))
    lines.append(txt_row('Stage 2        = SSO setup; inventory and config import'))
    lines.append(txt_row('Pre-check      = built-in checker; validates certs, DNS, ports, DB'))
    lines.append(txt_row('Snapshot (pre) = rollback point before upgrade; remove after success'))
    lines.append(txt_row('Jump host      = Windows/Linux machine that mounts and runs ISO installer'))
    lines.append(txt_row('DNS PTR        = reverse lookup; required for VCSA identity establishment'))
    lines.append(txt_row('SSO complexity = min 8 chars, upper, lower, digit, special'))
    lines.append(txt_row('Drain snapshots= remove all VM snapshots before upgrading to avoid bloat'))
    lines.append(txt_row('Port 9443      = VCSA appliance management HTTPS (VAMI)'))
    lines.append(txt_row('2x storage     = upgrade deploys new VCSA alongside old; same datastore OK'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-ops-proc',
    'docs/virtualization/vmware/vcenter/operations/procedures/index.md',
    'vCenter Server — Common Procedures',
)
def vcenter_ops_proc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vCenter Server — Common Procedures'))
    lines.append(txt_row())
    lines.append(txt_row('Routine vCenter procedures: certificate renewal, host add/remove, cluster'))
    lines.append(txt_row('configuration, permissions management, and licence assignment.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Certificate Procedures'), bMid(L2, R2, 'Host Procedures'))))
    lines.append(R(merge(bMid(L1, R1, 'Renew machine cert: VAMI'), bMid(L2, R2, 'Add host: Hosts & Clusters'))))
    lines.append(R(merge(bMid(L1, R1, 'Replace cert: certmgr CLI'), bMid(L2, R2, 'Enter maintenance mode'))))
    lines.append(R(merge(bMid(L1, R1, 'STS cert: scripted renewal'), bMid(L2, R2, 'Remove host: disconnect'))))
    lines.append(R(merge(bMid(L1, R1, 'Renew all: certificate-manager'), bMid(L2, R2, 'Reconnect: fix vpxa creds'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Certificate procedures require SSO admin; host procedures require host permissions.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Permissions & Licences'), bMid(L2, R2, 'Cluster Procedures'))))
    lines.append(R(merge(bMid(L1, R1, 'Assign role at object level'), bMid(L2, R2, 'Enable DRS: auto/manual'))))
    lines.append(R(merge(bMid(L1, R1, 'SSO groups: AD mapped'), bMid(L2, R2, 'Enable HA: configure slots'))))
    lines.append(R(merge(bMid(L1, R1, 'Licence: Administration tab'), bMid(L2, R2, 'vSAN: create diskgroups'))))
    lines.append(R(merge(bMid(L1, R1, 'Global perm: cross-DC roles'), bMid(L2, R2, 'EVC: set CPU baseline'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('All procedures run over vCenter management network; certificate operations'))
    lines.append(txt_row('cause brief service interruption (~2 min) during VCSA service restart.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('certificate-manager = VCSA interactive script; renews/replaces all certs'))
    lines.append(txt_row('certmgr       = low-level cert tool; used for individual cert replacement'))
    lines.append(txt_row('STS cert      = Security Token Service cert; 2-year validity; manual renew'))
    lines.append(txt_row('VAMI          = Appliance Management; port 5480; auto-renew machine cert'))
    lines.append(txt_row('Maintenance mode= drain host of VMs before patching or removal'))
    lines.append(txt_row('vpxa creds    = host agent credentials; reconnect if changed via VC UI'))
    lines.append(txt_row('EVC           = Enhanced vMotion Compatibility; CPU instruction masking'))
    lines.append(txt_row('DRS slots     = admission control slots; HA reserves resources per policy'))
    lines.append(txt_row('Global perm   = permission applies to all objects in all datacentres'))
    lines.append(txt_row('Role          = named permission set; e.g., Administrator, ReadOnly'))
    lines.append(txt_row('Licence key   = applied per product; vSAN, DRS, HA all need VC licence'))
    lines.append(txt_row('Diskgroup     = vSAN storage unit; one cache tier + capacity tier per host'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-ops-scripts',
    'docs/virtualization/vmware/vcenter/operations/scripts/index.md',
    'vCenter Server — Operational Scripts',
)
def vcenter_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vCenter Server — Operational Scripts'))
    lines.append(txt_row())
    lines.append(txt_row('PowerCLI and govc scripts automate routine vCenter operations: VM reporting,'))
    lines.append(txt_row('bulk host operations, snapshot cleanup, and permission auditing.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'VM & Host Reporting'), bMid(L2, R2, 'Maintenance Scripts'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-VM | Export-Csv'), bMid(L2, R2, 'Get snapshots >7 days old'))))
    lines.append(R(merge(bMid(L1, R1, 'VM tools version report'), bMid(L2, R2, 'Remove-Snapshot bulk'))))
    lines.append(R(merge(bMid(L1, R1, 'Host NTP config audit'), bMid(L2, R2, 'Set-VMHostNtpServer bulk'))))
    lines.append(R(merge(bMid(L1, R1, 'Datastore usage report'), bMid(L2, R2, 'Move-VM for DRS balance'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Reporting scripts run read-only; maintenance scripts require administrator role.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Permission & Cert Scripts'), bMid(L2, R2, 'Alarms & Events'))))
    lines.append(R(merge(bMid(L1, R1, 'Audit all role assignments'), bMid(L2, R2, 'Get-VIEvent last 24h'))))
    lines.append(R(merge(bMid(L1, R1, 'List SSO users/groups'), bMid(L2, R2, 'Export alarm definitions'))))
    lines.append(R(merge(bMid(L1, R1, 'Certificate expiry checker'), bMid(L2, R2, 'Alert on critical events'))))
    lines.append(R(merge(bMid(L1, R1, 'Token expiry script'), bMid(L2, R2, 'Bulk alarm acknowledge'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Scripts run from a management jump host with PowerCLI/govc installed;'))
    lines.append(txt_row('service account with minimum required permissions is recommended.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Export-Csv    = PowerCLI cmdlet output to CSV for reporting'))
    lines.append(txt_row('Get-Snapshot  = PowerCLI; returns all VM snapshots across inventory'))
    lines.append(txt_row('Remove-Snapshot= PowerCLI; deletes snapshot; runs consolidation'))
    lines.append(txt_row('Get-VIEvent   = PowerCLI; retrieves vCenter event log entries'))
    lines.append(txt_row('Set-VMHostNtpServer= configures NTP on ESXi hosts in bulk'))
    lines.append(txt_row('govc ls       = list inventory objects; similar to PowerCLI Get-*'))
    lines.append(txt_row('Service account= dedicated low-privilege account for automation'))
    lines.append(txt_row('Jump host     = management server running PowerCLI/govc scripts'))
    lines.append(txt_row('DRS balance   = Move-VM vMotions to equalize host utilisation'))
    lines.append(txt_row('Cert checker  = script: check cert.Subject.NotAfter vs today'))
    lines.append(txt_row('Token expiry  = SSO session token TTL; default 8h; renew on expiry'))
    lines.append(txt_row('Alarm ack     = acknowledges triggered alarm; stops repeat notifications'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-sec-access',
    'docs/virtualization/vmware/vcenter/security/access-control/index.md',
    'vCenter Server — Access Control',
)
def vcenter_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vCenter Server — Access Control'))
    lines.append(txt_row())
    lines.append(txt_row('vCenter access control uses SSO for authentication and a role-based permission'))
    lines.append(txt_row('system applied at inventory object level for authorisation.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Role-Based Access'), bMid(L2, R2, 'Permission Inheritance'))))
    lines.append(R(merge(bMid(L1, R1, 'Roles: built-in + custom'), bMid(L2, R2, 'Propagate to children'))))
    lines.append(R(merge(bMid(L1, R1, 'Admin / ReadOnly / NoAccess'), bMid(L2, R2, 'Override at child object'))))
    lines.append(R(merge(bMid(L1, R1, 'Privilege sets per role'), bMid(L2, R2, 'Global perm: all DCs'))))
    lines.append(R(merge(bMid(L1, R1, 'Apply role to user/group'), bMid(L2, R2, 'No propagate: exact obj only'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Assign minimum roles at highest useful object; propagate down the hierarchy.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Identity Sources'), bMid(L2, R2, 'Admin Lockout Prevention'))))
    lines.append(R(merge(bMid(L1, R1, 'SSO local domain'), bMid(L2, R2, 'Always keep administrator@vsphere'))))
    lines.append(R(merge(bMid(L1, R1, 'Active Directory joined'), bMid(L2, R2, 'Break-glass: local SSO user'))))
    lines.append(R(merge(bMid(L1, R1, 'LDAP: OpenLDAP support'), bMid(L2, R2, 'Audit: review perms quarterly'))))
    lines.append(R(merge(bMid(L1, R1, 'AD groups mapped to roles'), bMid(L2, R2, 'Log: all permission changes'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SSO identity store traffic goes over LDAP/LDAPS to AD DCs on management network.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SSO           = Single Sign-On; vCenter identity service; issues SAML tokens'))
    lines.append(txt_row('Role          = named collection of privileges; applied to user+object pair'))
    lines.append(txt_row('Privilege     = atomic permission; e.g., VirtualMachine.Power.On'))
    lines.append(txt_row('Propagate     = permission flows to all child objects in hierarchy'))
    lines.append(txt_row('Global perm   = permission applied at root level across all datacentres'))
    lines.append(txt_row('administrator@vsphere.local= built-in SSO admin; never remove'))
    lines.append(txt_row('Break-glass   = local SSO account for use when AD/LDAP is down'))
    lines.append(txt_row('Identity source= AD, LDAP, or local domain; multiple sources allowed'))
    lines.append(txt_row('AD group      = Active Directory security group mapped to vCenter role'))
    lines.append(txt_row('NoAccess role = explicitly blocks access at that object level'))
    lines.append(txt_row('Audit         = review all admin-role assignments at least quarterly'))
    lines.append(txt_row('Hierarchy     = DC → cluster → host → VM; permissions flow downward'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-sec-auth',
    'docs/virtualization/vmware/vcenter/security/authentication/index.md',
    'vCenter Server — Authentication',
)
def vcenter_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vCenter Server — Authentication'))
    lines.append(txt_row())
    lines.append(txt_row('vCenter authentication is handled by the embedded SSO service; it validates'))
    lines.append(txt_row('credentials against identity sources and issues SAML tokens for session access.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Authentication Flow'), bMid(L2, R2, 'MFA Options'))))
    lines.append(R(merge(bMid(L1, R1, 'User → vSphere Client login'), bMid(L2, R2, 'Smart card / CAC'))))
    lines.append(R(merge(bMid(L1, R1, 'SSO validates credentials'), bMid(L2, R2, 'RSA SecurID token'))))
    lines.append(R(merge(bMid(L1, R1, 'SAML token issued (8h TTL)'), bMid(L2, R2, 'RADIUS integration'))))
    lines.append(R(merge(bMid(L1, R1, 'Token used for API calls'), bMid(L2, R2, 'Duo via RADIUS proxy'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SSO token TTL is 8h; re-login required; API calls use bearer token from POST /api/session.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Session Management'), bMid(L2, R2, 'Lockout Policies'))))
    lines.append(R(merge(bMid(L1, R1, 'Max concurrent sessions'), bMid(L2, R2, '5 failed → lockout'))))
    lines.append(R(merge(bMid(L1, R1, 'Idle timeout: configurable'), bMid(L2, R2, 'Lockout duration: 5 min'))))
    lines.append(R(merge(bMid(L1, R1, 'Force re-auth on privilege op'), bMid(L2, R2, 'Unlock: SSO admin'))))
    lines.append(R(merge(bMid(L1, R1, 'API session token: short-lived'), bMid(L2, R2, 'Alert on failed logins'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SSO service runs on VCSA; AD/LDAP identity source must be reachable from'))
    lines.append(txt_row('management network on port 389 (LDAP) or 636 (LDAPS).'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SSO          = Single Sign-On; built into VCSA; core auth service'))
    lines.append(txt_row('SAML token   = XML security assertion; vCenter uses this internally'))
    lines.append(txt_row('SAML TTL     = 8 hours default; configurable in SSO configuration'))
    lines.append(txt_row('Smart card   = PIV/CAC certificate-based login; requires vCenter config'))
    lines.append(txt_row('RSA SecurID  = one-time password hardware token; RADIUS integration'))
    lines.append(txt_row('RADIUS       = Remote Authentication Dial-In User Service; MFA backend'))
    lines.append(txt_row('Duo          = MFA provider; integrates via RADIUS proxy to vCenter'))
    lines.append(txt_row('Lockout      = SSO account temporarily blocked after failed attempts'))
    lines.append(txt_row('Idle timeout = browser session closes after inactivity period'))
    lines.append(txt_row('POST /api/session= REST API login; returns bearer token in response'))
    lines.append(txt_row('LDAPS        = LDAP over TLS/SSL; port 636; required for AD in vcenter 8+'))
    lines.append(txt_row('AD identity  = Active Directory added as SSO identity source'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-sec-enc',
    'docs/virtualization/vmware/vcenter/security/encryption/index.md',
    'vCenter Server — Encryption',
)
def vcenter_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vCenter Server — Encryption'))
    lines.append(txt_row())
    lines.append(txt_row('vCenter encrypts management traffic via TLS and integrates with external KMS'))
    lines.append(txt_row('for VM encryption and vSAN encryption key management.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Transport Encryption'), bMid(L2, R2, 'VM Encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'All API traffic: TLS 1.2+'), bMid(L2, R2, 'Encrypt VM via policy'))))
    lines.append(R(merge(bMid(L1, R1, 'VCSA ↔ ESXi: TLS on 443'), bMid(L2, R2, 'KMS: external key server'))))
    lines.append(R(merge(bMid(L1, R1, 'DB: Postgres on loopback'), bMid(L2, R2, 'DEK per VM: AES-256'))))
    lines.append(R(merge(bMid(L1, R1, 'Backup: encrypted tarball'), bMid(L2, R2, 'KEK from KMS wraps DEK'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Transport encryption protects management plane; VM encryption protects data at rest.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Certificate Management'), bMid(L2, R2, 'vSAN Encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'VMCA: internal CA'), bMid(L2, R2, 'vSAN: cluster-level AES'))))
    lines.append(R(merge(bMid(L1, R1, 'Custom CA: enterprise PKI'), bMid(L2, R2, 'KMS required for vSAN'))))
    lines.append(R(merge(bMid(L1, R1, 'Cert expiry: monitor 30d+'), bMid(L2, R2, 'Re-key: rolling no downtime'))))
    lines.append(R(merge(bMid(L1, R1, 'STS cert: 2yr manual renew'), bMid(L2, R2, 'Shred key: destroys data'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('KMS server must be reachable from vCenter management network on KMIP port 5696;'))
    lines.append(txt_row('KMS unavailability prevents encrypted VM power-on.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('TLS 1.2+     = minimum transport security for all vCenter API traffic'))
    lines.append(txt_row('VMCA         = vSphere Certificate Authority; embedded in VCSA'))
    lines.append(txt_row('STS cert     = Security Token Service cert; 2-year expiry; breaks SSO'))
    lines.append(txt_row('KMS          = Key Management Server; KMIP protocol; stores KEKs'))
    lines.append(txt_row('KMIP         = Key Management Interoperability Protocol; port 5696'))
    lines.append(txt_row('DEK          = Data Encryption Key; unique per VM; encrypts VMDK'))
    lines.append(txt_row('KEK          = Key Encryption Key; stored in KMS; wraps DEKs'))
    lines.append(txt_row('AES-256      = Advanced Encryption Standard; key size used by VM/vSAN enc'))
    lines.append(txt_row('Re-key       = rotate DEKs without powering off VM; KMS generates new KEK'))
    lines.append(txt_row('Shred key    = destroy KEK in KMS; renders encrypted data unrecoverable'))
    lines.append(txt_row('Custom CA    = replace VMCA-signed certs with enterprise PKI certs'))
    lines.append(txt_row('vSAN enc     = cluster-wide encryption; hosts encrypt writes to disk'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-sec-hard',
    'docs/virtualization/vmware/vcenter/security/hardening/index.md',
    'vCenter Server — Hardening',
)
def vcenter_sec_hard():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vCenter Server — Hardening'))
    lines.append(txt_row())
    lines.append(txt_row('vCenter hardening follows the VMware Security Hardening Guide and CIS benchmark;'))
    lines.append(txt_row('key controls: network isolation, MFA, minimal admin, FIPS mode, audit logging.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Network Hardening'), bMid(L2, R2, 'Access Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'Mgmt network: dedicated VLAN'), bMid(L2, R2, 'MFA: smart card/RADIUS'))))
    lines.append(R(merge(bMid(L1, R1, 'Firewall: only needed ports'), bMid(L2, R2, 'SSO lockout: 5 attempts'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable SSH when not needed'), bMid(L2, R2, 'Admin group: 2 accounts max'))))
    lines.append(R(merge(bMid(L1, R1, 'TLS 1.2 minimum enforced'), bMid(L2, R2, 'Log: all admin actions'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Network isolation and MFA are the highest-value controls for vCenter hardening.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Patch & Config Hardening'), bMid(L2, R2, 'Audit & Compliance'))))
    lines.append(R(merge(bMid(L1, R1, 'Apply patches within 30 days'), bMid(L2, R2, 'vCenter Chargeback audit'))))
    lines.append(R(merge(bMid(L1, R1, 'FIPS mode: enable in VAMI'), bMid(L2, R2, 'Syslog: forward to SIEM'))))
    lines.append(R(merge(bMid(L1, R1, 'Disable banner-less login'), bMid(L2, R2, 'CIS benchmark scans'))))
    lines.append(R(merge(bMid(L1, R1, 'Shell access: time-limited'), bMid(L2, R2, 'Review perms quarterly'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('VCSA runs on ESXi host; ESXi itself must be hardened; management VLAN must'))
    lines.append(txt_row('be unreachable from guest VM networks.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VMware Hardening Guide= published per vSphere version; CIS baseline'))
    lines.append(txt_row('CIS benchmark= Center for Internet Security; independent hardening standard'))
    lines.append(txt_row('FIPS 140-2   = US federal cryptography standard; enable in VAMI > Security'))
    lines.append(txt_row('MFA          = Multi-Factor Authentication; prevents credential-only login'))
    lines.append(txt_row('SIEM         = Security Info and Event Mgmt; receives syslog from vCenter'))
    lines.append(txt_row('Shell timeout= SSH session auto-closes after idle period (set to 900s)'))
    lines.append(txt_row('Lockout      = SSO disables account after N failed login attempts'))
    lines.append(txt_row('Banner       = login warning message; required by some compliance frameworks'))
    lines.append(txt_row('Dedicated VLAN= separate network segment for vCenter management traffic'))
    lines.append(txt_row('Patch SLA    = agree cadence: critical <7d, high <30d, medium <90d'))
    lines.append(txt_row('Quarterly review= revoke stale/unnecessary role assignments'))
    lines.append(txt_row('Admin count  = fewer admin accounts = smaller blast radius on compromise'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-ts-common',
    'docs/virtualization/vmware/vcenter/troubleshooting/common-issues/index.md',
    'vCenter Server — Common Issues',
)
def vcenter_ts_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vCenter Server — Common Issues'))
    lines.append(txt_row())
    lines.append(txt_row('Common vCenter issues: hosts disconnecting, certificate errors, SSO login failure,'))
    lines.append(txt_row('service crashes, disk space exhaustion, and database performance degradation.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Connectivity Issues'), bMid(L2, R2, 'Certificate Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'Host disconnected: check vpxa'), bMid(L2, R2, 'Login fails: cert expired'))))
    lines.append(R(merge(bMid(L1, R1, 'Reconnect: right-click host'), bMid(L2, R2, 'Error: SEC_E_UNTRUSTED'), )))
    lines.append(R(merge(bMid(L1, R1, 'vpxa restart: esxcli on host'), bMid(L2, R2, 'Fix: renew cert via VAMI'))))
    lines.append(R(merge(bMid(L1, R1, 'Network check: ping VC FQDN'), bMid(L2, R2, 'STS cert: scripted renewal'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Cert expiry is the most common cause of login/connectivity failures; check first.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Service & Disk Issues'), bMid(L2, R2, 'SSO & Login Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'Service down: vmon-cli -l'), bMid(L2, R2, 'SSO: password lock out'))))
    lines.append(R(merge(bMid(L1, R1, 'Restart: service-control'), bMid(L2, R2, 'Unlock: dir-cli unlock'))))
    lines.append(R(merge(bMid(L1, R1, 'Disk /storage >80%: purge logs'), bMid(L2, R2, 'AD: domain unreachable'))))
    lines.append(R(merge(bMid(L1, R1, 'DB vacuum stuck: kill + restart'), bMid(L2, R2, 'Use local SSO for access'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Most issues trace back to: network (FQDN/DNS), storage (disk full), time (NTP),'))
    lines.append(txt_row('or certificates (expired); check all four before deep investigation.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vpxa          = vCenter host agent; handles VC→host communication'))
    lines.append(txt_row('vmon-cli -l   = list all VCSA services and their current state'))
    lines.append(txt_row('service-control= restart VCSA services; --restart --all (use carefully)'))
    lines.append(txt_row('dir-cli       = SSO CLI; list users, unlock accounts, set passwords'))
    lines.append(txt_row('SEC_E_UNTRUSTED= Windows error: cert chain not trusted; replace cert'))
    lines.append(txt_row('STS cert      = Security Token Service cert; 2yr expiry; most common failure'))
    lines.append(txt_row('/storage      = VCSA data partition; full = service crashes'))
    lines.append(txt_row('DB vacuum     = Postgres autovacuum job; kill if stuck; restart postgres'))
    lines.append(txt_row('NTP skew      = clock drift >5min breaks SSO certificate validation'))
    lines.append(txt_row('Reconnect     = right-click disconnected host; re-establishes vpxa link'))
    lines.append(txt_row('Local SSO     = vsphere.local admin; always works if AD is unreachable'))
    lines.append(txt_row('Log purge     = /var/log compression/rotation; also rotate stats DB'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-ts-diag',
    'docs/virtualization/vmware/vcenter/troubleshooting/diagnostics/index.md',
    'vCenter Server — Diagnostics',
)
def vcenter_ts_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vCenter Server — Diagnostics'))
    lines.append(txt_row())
    lines.append(txt_row('vCenter diagnostics use log bundles, service status checks, and database queries'))
    lines.append(txt_row('to identify root causes of connectivity, performance, and auth failures.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Log Collection'), bMid(L2, R2, 'Service Diagnostics'))))
    lines.append(R(merge(bMid(L1, R1, 'Support bundle: VC UI'), bMid(L2, R2, 'vmon-cli -l (status)'))))
    lines.append(R(merge(bMid(L1, R1, 'vc-support.sh on appliance'), bMid(L2, R2, 'journalctl -u vmware-*'))))
    lines.append(R(merge(bMid(L1, R1, 'Key logs: vpxd.log'), bMid(L2, R2, 'service-control --status'))))
    lines.append(R(merge(bMid(L1, R1, 'SSO: ssoAdminServer.log'), bMid(L2, R2, 'Check port 443/9443 open'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Collect support bundle first; vpxd.log and SSO logs cover 90% of issues.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'DB & Performance Diag'), bMid(L2, R2, 'Network Diagnostics'))))
    lines.append(R(merge(bMid(L1, R1, 'Postgres: select pg_stat_activity'), bMid(L2, R2, 'Ping VC from ESXi host'))))
    lines.append(R(merge(bMid(L1, R1, 'DB size: /storage/db usage'), bMid(L2, R2, 'nslookup: VC FQDN + PTR'))))
    lines.append(R(merge(bMid(L1, R1, 'Slow UI: vpxd CPU usage'), bMid(L2, R2, 'traceroute: management path'))))
    lines.append(R(merge(bMid(L1, R1, 'Stats rollup: latency logs'), bMid(L2, R2, 'Port test: nc -zv vc 443'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('All diagnostic access is via SSH to VCSA appliance or via browser to vSphere Client;'))
    lines.append(txt_row('support bundles are downloaded via browser UI.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vc-support.sh = generates support bundle on VCSA; exports to /tmp'))
    lines.append(txt_row('vpxd.log      = main vCenter Server log; task, event, error messages'))
    lines.append(txt_row('ssoAdminServer= SSO authentication service log; login failures here'))
    lines.append(txt_row('pg_stat_activity= Postgres view; shows active DB queries'))
    lines.append(txt_row('vmon-cli      = service monitor; RUNNING/STOPPED states'))
    lines.append(txt_row('journalctl    = systemd log; vmware-* services write here'))
    lines.append(txt_row('/storage      = VCSA data partition; contains DB, logs, stats'))
    lines.append(txt_row('nc -zv        = netcat; test TCP port reachability'))
    lines.append(txt_row('nslookup PTR  = reverse DNS check; must match forward A record'))
    lines.append(txt_row('Support bundle= ZIP of all VCSA logs + config; send to GSS'))
    lines.append(txt_row('Stats rollup  = scheduled job; aggregates perf metrics; latency = problem'))
    lines.append(txt_row('vpxd CPU      = high vCenter process CPU = query storm or stuck tasks'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcenter-ts-esc',
    'docs/virtualization/vmware/vcenter/troubleshooting/escalation/index.md',
    'vCenter Server — Escalation',
)
def vcenter_ts_esc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vCenter Server — Escalation'))
    lines.append(txt_row())
    lines.append(txt_row('Escalate vCenter issues to VMware GSS when self-service troubleshooting exhausts'))
    lines.append(txt_row('available options; attach support bundle and document timeline.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Escalation Triggers'), bMid(L2, R2, 'Pre-Escalation Steps'))))
    lines.append(R(merge(bMid(L1, R1, 'VCSA crashes repeatedly'), bMid(L2, R2, 'Collect support bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'Data loss suspected'), bMid(L2, R2, 'Snapshot VCSA if stable'))))
    lines.append(R(merge(bMid(L1, R1, 'All self-steps exhausted'), bMid(L2, R2, 'Document exact error text'))))
    lines.append(R(merge(bMid(L1, R1, 'P1 outage: VC inaccessible'), bMid(L2, R2, 'Timeline: when started'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('GSS requires SR number, support bundle, and change timeline to start root-cause.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'GSS Engagement'), bMid(L2, R2, 'Escalation Path'))))
    lines.append(R(merge(bMid(L1, R1, 'Open SR at support.broadcom'), bMid(L2, R2, 'T1: SR triage + bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'Severity: P1 for full outage'), bMid(L2, R2, 'T2: Senior SE assigned'))))
    lines.append(R(merge(bMid(L1, R1, 'Include vCenter version'), bMid(L2, R2, 'T3: Engineering review'))))
    lines.append(R(merge(bMid(L1, R1, 'Attach support bundle ZIP'), bMid(L2, R2, 'CritSit: 24/7 coverage'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('GSS may request live session access via Bomgar/WebEx; prepare VCSA SSH access'))
    lines.append(txt_row('and vSphere Client access for remote support engineers.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('GSS          = Global Support Services; VMware (Broadcom) official support'))
    lines.append(txt_row('SR           = Service Request; support ticket number; reference in all calls'))
    lines.append(txt_row('Support bundle= ZIP of all VCSA logs; generated via UI or vc-support.sh'))
    lines.append(txt_row('Severity P1  = critical; production outage; fastest SLA response'))
    lines.append(txt_row('CritSit      = Critical Situation; escalation for P1 with exec involvement'))
    lines.append(txt_row('T1/T2/T3     = support tiers; T3 has access to engineering teams'))
    lines.append(txt_row('Bomgar       = VMware remote access tool; screen share for live debug'))
    lines.append(txt_row('Timeline     = chronological list of changes/events before the issue'))
    lines.append(txt_row('Snapshot     = pre-work safety net; capture VCSA state before GSS changes'))
    lines.append(txt_row('KB article   = VMware knowledge base; check before raising SR'))
    lines.append(txt_row('vCenter version= full build number from Administration > About'))
    lines.append(txt_row('Broadcom portal= support.broadcom.com replaced my.vmware.com for SRs'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-arch-how',
    'docs/virtualization/vmware/vsan/architecture/how-it-works/index.md',
    'vSAN — How It Works',
)
def vsan_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vSAN — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('vSAN pools local disks from ESXi hosts into a shared datastore; data is'))
    lines.append(txt_row('distributed across hosts using a policy-driven object-based storage model.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Data Path'), bMid(L2, R2, 'Disk Groups'))))
    lines.append(R(merge(bMid(L1, R1, 'VM write → vSAN object'), bMid(L2, R2, '1 cache NVMe/SSD per group'))))
    lines.append(R(merge(bMid(L1, R1, 'Policy: FTT + RAID type'), bMid(L2, R2, '1-7 capacity disks per group'))))
    lines.append(R(merge(bMid(L1, R1, 'Components placed on hosts'), bMid(L2, R2, 'Express Storage Arch (ESA)'))))
    lines.append(R(merge(bMid(L1, R1, 'Witness: metadata quorum'), bMid(L2, R2, 'All-NVMe: ESA only'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Each object (VMDK) is split into components placed across hosts per the storage policy.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster Requirements'), bMid(L2, R2, 'Fault Domains'))))
    lines.append(R(merge(bMid(L1, R1, 'Min 3 hosts (FTT=1)'), bMid(L2, R2, 'Rack awareness: per-rack FD'))))
    lines.append(R(merge(bMid(L1, R1, '10GbE+ vSAN VMkernel'), bMid(L2, R2, 'Stretched: 2 sites + witness'))))
    lines.append(R(merge(bMid(L1, R1, 'Unicast: no multicast needed'), bMid(L2, R2, 'FD isolates host failures'))))
    lines.append(R(merge(bMid(L1, R1, 'Health: periodic resync'), bMid(L2, R2, 'Min 3 FDs for FTT=1'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vSAN requires dedicated SSDs/NVMe for cache and HDDs/SSDs for capacity on each host;'))
    lines.append(txt_row('10GbE+ network with dedicated vSAN VMkernel adapter.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Object        = vSAN storage unit; one VMDK = one or more objects'))
    lines.append(txt_row('Component     = slice of an object placed on a single host'))
    lines.append(txt_row('Witness       = metadata-only component; tie-breaker for quorum'))
    lines.append(txt_row('FTT           = Failures To Tolerate; policy setting; FTT=1 needs 3 hosts'))
    lines.append(txt_row('RAID-1        = mirroring; FTT=1: 2 data + 1 witness'))
    lines.append(txt_row('RAID-5        = erasure coding; FTT=1: 4 hosts; more space-efficient'))
    lines.append(txt_row('Disk group    = cache + capacity disks on one host; O(SA: per host)'))
    lines.append(txt_row('ESA           = Express Storage Architecture; vSAN 8+; all-NVMe only'))
    lines.append(txt_row('Fault domain  = logical grouping of hosts; failure unit for placement'))
    lines.append(txt_row('Stretched cluster= 2 active sites + 1 witness site; RPO=0 across sites'))
    lines.append(txt_row('Resync        = after host failure/return, components rebalanced'))
    lines.append(txt_row('VMkernel      = special NIC adapter; vSAN uses vmk for cluster traffic'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-arch-int',
    'docs/virtualization/vmware/vsan/architecture/integrations/index.md',
    'vSAN — Integrations',
)
def vsan_arch_int():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vSAN — Integrations'))
    lines.append(txt_row())
    lines.append(txt_row('vSAN integrates with vCenter for management, NSX for micro-segmentation,'))
    lines.append(txt_row('external KMS for encryption, and backup tools via VADP.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'vCenter Integration'), bMid(L2, R2, 'Backup Integration'))))
    lines.append(R(merge(bMid(L1, R1, 'Managed via Hosts & Clusters'), bMid(L2, R2, 'VADP: CBT snapshots'))))
    lines.append(R(merge(bMid(L1, R1, 'Storage policies from VC'), bMid(L2, R2, 'Veeam / Commvault / Avamar'))))
    lines.append(R(merge(bMid(L1, R1, 'Health in vCenter UI'), bMid(L2, R2, 'NFS target: not needed'))))
    lines.append(R(merge(bMid(L1, R1, 'Alarms: disk/host failures'), bMid(L2, R2, 'SRM: vSAN datastores OK'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('vCenter is the single management plane; policies defined here flow to all vSAN hosts.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Security Integrations'), bMid(L2, R2, 'Monitoring Integrations'))))
    lines.append(R(merge(bMid(L1, R1, 'KMS: external KMIP server'), bMid(L2, R2, 'vROps: vSAN capacity'))))
    lines.append(R(merge(bMid(L1, R1, 'Data-at-rest encryption'), bMid(L2, R2, 'vSAN Skyline health'))))
    lines.append(R(merge(bMid(L1, R1, 'NSX: microsegment VM traffic'), bMid(L2, R2, 'SNMP: disk failure alerts'))))
    lines.append(R(merge(bMid(L1, R1, 'vSAN ESA: inline encryption'), bMid(L2, R2, 'Syslog: host events'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('KMS must be reachable from each ESXi host on KMIP port 5696; monitoring tools'))
    lines.append(txt_row('use vCenter APIs to pull vSAN health and capacity data.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VADP     = vStorage APIs for Data Protection; backup quiescing'))
    lines.append(txt_row('CBT      = Changed Block Tracking; incremental backup efficiency'))
    lines.append(txt_row('KMIP     = Key Management Interoperability Protocol; port 5696'))
    lines.append(txt_row('KMS      = Key Management Server; holds KEKs for vSAN encryption'))
    lines.append(txt_row('SRM      = Site Recovery Manager; supports vSAN datastores directly'))
    lines.append(txt_row('vROps    = Aria Operations; capacity planning for vSAN'))
    lines.append(txt_row('Skyline  = VMware proactive support; vSAN health telemetry'))
    lines.append(txt_row('NSX      = network virtualisation; micro-segments guest VMs'))
    lines.append(txt_row('Storage policy= VC-defined rules: FTT, RAID, IOPs limit per VM'))
    lines.append(txt_row('Avamar   = Dell backup tool; VADP integration for vSAN VMs'))
    lines.append(txt_row('Commvault = backup tool; VADP snapshot integration'))
    lines.append(txt_row('Inline enc= ESA encrypts data as it enters the storage layer'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-arch-design',
    'docs/virtualization/vmware/vsan/architecture/design-standards/index.md',
    'vSAN — Design Standards',
)
def vsan_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vSAN — Design Standards'))
    lines.append(txt_row())
    lines.append(txt_row('vSAN design standards cover host sizing, disk group ratios, network requirements,'))
    lines.append(txt_row('fault tolerance policy selection, and cluster expansion rules.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Host & Disk Standards'), bMid(L2, R2, 'Network Standards'))))
    lines.append(R(merge(bMid(L1, R1, 'Min 3 hosts (FTT=1)'), bMid(L2, R2, '10GbE minimum; 25GbE preferred'))))
    lines.append(R(merge(bMid(L1, R1, 'Homogeneous hosts preferred'), bMid(L2, R2, 'Dedicated VMkernel NIC'))))
    lines.append(R(merge(bMid(L1, R1, 'Cache:capacity 1:10 ratio'), bMid(L2, R2, 'Jumbo frames: MTU 9000'))))
    lines.append(R(merge(bMid(L1, R1, 'vSAN HCL: all disks listed'), bMid(L2, R2, 'Latency <1ms host to host'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('All hardware must appear on the vSAN HCL; off-HCL disks cause unsupported state.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Policy Standards'), bMid(L2, R2, 'Capacity Planning'))))
    lines.append(R(merge(bMid(L1, R1, 'Prod VMs: FTT=1 RAID-1'), bMid(L2, R2, 'Slack: 30% free always'))))
    lines.append(R(merge(bMid(L1, R1, 'Critical: FTT=2 RAID-6'), bMid(L2, R2, 'Resync headroom: 1 host'))))
    lines.append(R(merge(bMid(L1, R1, 'Test/dev: FTT=0 (no HA)'), bMid(L2, R2, 'Expand by 3 hosts (FD rule)'))))
    lines.append(R(merge(bMid(L1, R1, 'Encryption: policy-based'), bMid(L2, R2, 'Dedup/compress: OSA only'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('All ESXi hosts contribute their local NVMe/SSD/HDD to the shared vSAN datastore;'))
    lines.append(txt_row('TOR switches must support jumbo frames and LLDP for vSAN network health.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('HCL          = Hardware Compatibility List; VMware approved disk list'))
    lines.append(txt_row('FTT          = Failures To Tolerate; defines redundancy level'))
    lines.append(txt_row('RAID-1       = mirroring; FTT=1 needs 3 hosts; simple, higher cost'))
    lines.append(txt_row('RAID-5/6     = erasure coding; space-efficient; FTT=1 needs 4, FTT=2 needs 6'))
    lines.append(txt_row('Cache ratio  = 1:10 cache to capacity; e.g., 400GB cache → 4TB capacity'))
    lines.append(txt_row('30% slack    = required for resync operations after disk/host failure'))
    lines.append(txt_row('Resync headroom= capacity to rebuild one failed host worth of data'))
    lines.append(txt_row('OSA          = Original Storage Architecture; HDD+SSD; supports dedup'))
    lines.append(txt_row('ESA          = Express Storage Architecture; all-NVMe; no dedup needed'))
    lines.append(txt_row('Homogeneous  = same CPU/RAM/disk model per host; simplifies policy math'))
    lines.append(txt_row('MTU 9000     = jumbo frames; reduces CPU overhead for large I/O'))
    lines.append(txt_row('LLDP         = Link Layer Discovery Protocol; used for vSAN net health'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-ops-backup',
    'docs/virtualization/vmware/vsan/operations/backup-restore/index.md',
    'vSAN — Backup & Restore',
)
def vsan_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vSAN — Backup & Restore'))
    lines.append(txt_row())
    lines.append(txt_row('vSAN itself is not a backup solution; VMs on vSAN are backed up via VADP;'))
    lines.append(txt_row('restore targets can be the same or a different datastore.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Backup Methods'), bMid(L2, R2, 'vSAN Config Backup'))))
    lines.append(R(merge(bMid(L1, R1, 'VADP: Veeam/Commvault/Avamar'), bMid(L2, R2, 'vCenter backup includes vSAN'))))
    lines.append(R(merge(bMid(L1, R1, 'CBT: incremental efficiency'), bMid(L2, R2, 'Disk group config: in DB'))))
    lines.append(R(merge(bMid(L1, R1, 'HotAdd: proxy on same host'), bMid(L2, R2, 'Storage policies: VC DB'))))
    lines.append(R(merge(bMid(L1, R1, 'NBD fallback if no HotAdd'), bMid(L2, R2, 'Re-create diskgroup on restore'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('HotAdd provides fastest backup throughput; NBD over 10GbE is fallback.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Restore Procedure'), bMid(L2, R2, 'DR with vSAN'))))
    lines.append(R(merge(bMid(L1, R1, 'Restore from backup to vSAN DS'), bMid(L2, R2, 'vSAN stretched: RPO=0'))))
    lines.append(R(merge(bMid(L1, R1, 'Apply correct storage policy'), bMid(L2, R2, 'SRM: vSAN replication'))))
    lines.append(R(merge(bMid(L1, R1, 'Wait for resync if FTT>0'), bMid(L2, R2, 'vSAN HCI Mesh: xsite DS'))))
    lines.append(R(merge(bMid(L1, R1, 'Validate policy compliance'), bMid(L2, R2, 'vSphere Rep: per-VM RPO'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Backup proxy VMs need access to vSAN datastore; HotAdd requires proxy on same cluster.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VADP       = vStorage APIs for Data Protection; backup quiescing API'))
    lines.append(txt_row('CBT        = Changed Block Tracking; tracks changed sectors since last backup'))
    lines.append(txt_row('HotAdd     = proxy VM on same host; attaches VMDK directly; fastest'))
    lines.append(txt_row('NBD        = Network Block Device; backup over TCP; slower fallback'))
    lines.append(txt_row('Proxy      = backup VM; intermediary between vSAN VM and backup target'))
    lines.append(txt_row('Resync     = after restore, vSAN rebuilds missing replicas per policy'))
    lines.append(txt_row('Policy compliance= UI shows red/yellow if restored VM policy not met'))
    lines.append(txt_row('SRM        = Site Recovery Manager; orchestrates vSAN failover'))
    lines.append(txt_row('vSphere Rep= vSphere Replication; per-VM async replication to DR site'))
    lines.append(txt_row('HCI Mesh   = cross-cluster vSAN datastore sharing (vSAN 7.0+)'))
    lines.append(txt_row('Stretched  = 2-site active-active; RPO=0; needs >10ms RTT <5ms preferred'))
    lines.append(txt_row('Diskgroup  = cache + capacity units; re-created after disk replacement'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-ops-cli',
    'docs/virtualization/vmware/vsan/operations/cli-reference/index.md',
    'vSAN — CLI Reference',
)
def vsan_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vSAN — CLI Reference'))
    lines.append(txt_row())
    lines.append(txt_row('vSAN CLI operations use esxcli on hosts, RVC (Ruby vSphere Console), PowerCLI,'))
    lines.append(txt_row('and the vSphere Client UI for health, disk, and object management.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'esxcli Commands'), bMid(L2, R2, 'RVC Commands'))))
    lines.append(R(merge(bMid(L1, R1, 'esxcli vsan cluster get'), bMid(L2, R2, 'vsan.health.health_test'))))
    lines.append(R(merge(bMid(L1, R1, 'esxcli vsan storage list'), bMid(L2, R2, 'vsan.disks_info <host>'))))
    lines.append(R(merge(bMid(L1, R1, 'esxcli vsan network list'), bMid(L2, R2, 'vsan.obj_status_report'))))
    lines.append(R(merge(bMid(L1, R1, 'esxcli vsan debug object'), bMid(L2, R2, 'vsan.resync_dashboard'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('esxcli runs on the ESXi host shell; RVC runs from the vCenter or jump host.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'PowerCLI Commands'), bMid(L2, R2, 'Object & Disk Commands'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-VsanClusterConfiguration'), bMid(L2, R2, 'esxcli vsan debug object'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-VsanDisk | Ft Status'), bMid(L2, R2, 'cmmds-tool find (metadata)'))))
    lines.append(R(merge(bMid(L1, R1, 'Test-VsanClusterHealth'), bMid(L2, R2, 'vsanObserver (perf data)'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-VsanView (advanced)'), bMid(L2, R2, 'esxcli vsan trace cat'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('All commands execute against host or vCenter management plane; cmmds-tool'))
    lines.append(txt_row('is host-local only and reads cluster metadata database.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('esxcli vsan   = vSAN management namespace in ESXi CLI'))
    lines.append(txt_row('RVC           = Ruby vSphere Console; legacy; still used for vSAN diag'))
    lines.append(txt_row('cmmds-tool    = Cluster Monitoring, Membership, Directory Service tool'))
    lines.append(txt_row('CMMDS         = cluster metadata store; tracks object component locations'))
    lines.append(txt_row('vsanObserver  = performance observability tool; requires RVC'))
    lines.append(txt_row('obj_status    = per-object health report; shows degraded/absent'))
    lines.append(txt_row('resync_dash   = RVC command showing active resync bytes/throughput'))
    lines.append(txt_row('debug object  = detailed per-object component and placement info'))
    lines.append(txt_row('vsan trace    = per-host vSAN trace log; crash and I/O analysis'))
    lines.append(txt_row('health_test   = runs all vSAN health checks programmatically'))
    lines.append(txt_row('Get-VsanDisk  = PowerCLI; lists disk status across cluster'))
    lines.append(txt_row('Test-VsanCluster= PowerCLI; triggers health check run'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-ops-health',
    'docs/virtualization/vmware/vsan/operations/health-checks/index.md',
    'vSAN — Health Checks',
)
def vsan_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vSAN — Health Checks'))
    lines.append(txt_row())
    lines.append(txt_row('vSAN health checks verify cluster, network, disk, and object health; run daily'))
    lines.append(txt_row('via the vSAN Health UI or Test-VsanClusterHealth PowerCLI cmdlet.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster Health'), bMid(L2, R2, 'Network Health'))))
    lines.append(R(merge(bMid(L1, R1, 'All hosts: member of cluster'), bMid(L2, R2, 'vSAN MTU test: 9000'))))
    lines.append(R(merge(bMid(L1, R1, 'No host disconnected'), bMid(L2, R2, 'Latency <1ms host to host'))))
    lines.append(R(merge(bMid(L1, R1, 'Witness reachable (stretched)'), bMid(L2, R2, 'No multicast required'))))
    lines.append(R(merge(bMid(L1, R1, 'No decommission in progress'), bMid(L2, R2, 'Unicast agent running'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Cluster and network health are prerequisites; disk and object health depend on them.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Disk & Object Health'), bMid(L2, R2, 'Capacity Health'))))
    lines.append(R(merge(bMid(L1, R1, 'All disks: healthy/OK'), bMid(L2, R2, 'Free space >30% total'))))
    lines.append(R(merge(bMid(L1, R1, 'No degraded components'), bMid(L2, R2, 'Resync ETA <24h'))))
    lines.append(R(merge(bMid(L1, R1, 'Policy compliance: 100%'), bMid(L2, R2, 'No dedup overhead alarm'))))
    lines.append(R(merge(bMid(L1, R1, 'Resync: 0 bytes pending'), bMid(L2, R2, 'Capacity per host balanced'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical disk health reported via SMART; failed disk shows degraded component;'))
    lines.append(txt_row('replace disk within 60 minutes to avoid data loss window.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Degraded      = component lost; vSAN has no redundancy until rebuilt'))
    lines.append(txt_row('Absent        = component temporarily missing; wait 60min before rebuild'))
    lines.append(txt_row('Resync        = rebuilding missing components after host/disk failure'))
    lines.append(txt_row('Policy compliance= all VMs must meet FTT policy; red = risk'))
    lines.append(txt_row('MTU test      = vSAN sends 8972-byte pings to test jumbo frames end-to-end'))
    lines.append(txt_row('Unicast agent = replaced multicast in vSAN 6.6+; always check running'))
    lines.append(txt_row('SMART         = disk self-monitoring; pre-failure indicator'))
    lines.append(txt_row('Decommission  = remove host from vSAN while migrating data; slow'))
    lines.append(txt_row('60-min timer  = vSAN waits 60 min before marking absent as degraded'))
    lines.append(txt_row('Witness (stretched)= third-site VM; heartbeat must be <200ms RTT'))
    lines.append(txt_row('Free 30%      = vSAN needs headroom for resync; alert at <25%'))
    lines.append(txt_row('Resync ETA    = estimate shown in vSAN performance health panel'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-ops-install',
    'docs/virtualization/vmware/vsan/operations/install-upgrade/index.md',
    'vSAN — Install & Upgrade',
)
def vsan_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vSAN — Install & Upgrade'))
    lines.append(txt_row())
    lines.append(txt_row('vSAN is enabled per cluster in vCenter; hardware must be on the HCL; upgrades'))
    lines.append(txt_row('use vSphere Lifecycle Manager (vLCM) with host remediation.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Enable vSAN Checklist'), bMid(L2, R2, 'Disk Group Creation'))))
    lines.append(R(merge(bMid(L1, R1, 'HCL: verify all disks'), bMid(L2, R2, 'Claim disks in UI'))))
    lines.append(R(merge(bMid(L1, R1, '10GbE+ VMkernel per host'), bMid(L2, R2, 'Cache: 1 disk per group'))))
    lines.append(R(merge(bMid(L1, R1, 'Jumbo frames on switches'), bMid(L2, R2, 'Capacity: 1–7 per group'))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster > Configure > vSAN', ), bMid(L2, R2, 'ESA: all NVMe auto-claim'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('HCL compliance is mandatory; non-HCL disks cause unsupported configuration warning.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Upgrade with vLCM'), bMid(L2, R2, 'Post-Upgrade Steps'))))
    lines.append(R(merge(bMid(L1, R1, 'Create baseline image'), bMid(L2, R2, 'Run health checks'))))
    lines.append(R(merge(bMid(L1, R1, 'Attach to cluster'), bMid(L2, R2, 'Verify disk format version'))))
    lines.append(R(merge(bMid(L1, R1, 'Remediate: rolling hosts'), bMid(L2, R2, 'Upgrade disk format (OSA)'))))
    lines.append(R(merge(bMid(L1, R1, 'Hosts: maintenance → patch'), bMid(L2, R2, 'Monitor resync complete'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Each host must enter maintenance mode before remediation; vSAN evacuates data'))
    lines.append(txt_row('during maintenance; requires 30% free space for safe data migration.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vLCM          = vSphere Lifecycle Manager; baseline images + remediation'))
    lines.append(txt_row('Remediate     = apply baseline to host; put in maintenance, patch, reboot'))
    lines.append(txt_row('HCL           = Hardware Compatibility List; required for support'))
    lines.append(txt_row('Disk format   = vSAN on-disk format version; upgrade after host upgrade'))
    lines.append(txt_row('OSA           = Original Storage Architecture; needs explicit format upgrade'))
    lines.append(txt_row('ESA           = Express Storage Architecture; vSAN 8+; all-NVMe'))
    lines.append(txt_row('VMkernel      = vSAN network adapter; must be enabled with vSAN tag'))
    lines.append(txt_row('Maintenance mode= evacuates VMs; ensures FTT=1 redundancy before host offline'))
    lines.append(txt_row('Jumbo frames  = MTU 9000; configure on TOR switches and VMkernel'))
    lines.append(txt_row('Resync        = post-upgrade, data rebalances across now-updated hosts'))
    lines.append(txt_row('Claim disks   = select disks in VC UI for cache/capacity role'))
    lines.append(txt_row('Disk group    = logical container of cache + capacity disks per host'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-ops-proc',
    'docs/virtualization/vmware/vsan/operations/procedures/index.md',
    'vSAN — Common Procedures',
)
def vsan_ops_proc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vSAN — Common Procedures'))
    lines.append(txt_row())
    lines.append(txt_row('vSAN operational procedures: disk replacement, host removal, policy update,'))
    lines.append(txt_row('rebalancing, decommission, and storage policy compliance remediation.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Disk Replacement'), bMid(L2, R2, 'Host Decommission'))))
    lines.append(R(merge(bMid(L1, R1, 'Mark disk failed in UI'), bMid(L2, R2, 'Full data evacuation mode'))))
    lines.append(R(merge(bMid(L1, R1, 'Remove disk group'), bMid(L2, R2, 'Wait for resync complete'))))
    lines.append(R(merge(bMid(L1, R1, 'Physically replace disk'), bMid(L2, R2, 'Remove from cluster'))))
    lines.append(R(merge(bMid(L1, R1, 'Claim new disk in UI'), bMid(L2, R2, 'Verify no degraded objects'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Always mark disk as failed before physical removal to trigger safe data migration.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Policy & Rebalancing'), bMid(L2, R2, 'Capacity Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Edit policy: Policies & Profiles'), bMid(L2, R2, 'Check usage in Health UI'))))
    lines.append(R(merge(bMid(L1, R1, 'Apply policy to VM storage'), bMid(L2, R2, 'Rebalance if imbalanced'))))
    lines.append(R(merge(bMid(L1, R1, 'Compliance: fix non-compliant'), bMid(L2, R2, 'Add host: expand cluster'))))
    lines.append(R(merge(bMid(L1, R1, 'Re-apply: right-click VM'), bMid(L2, R2, 'Decommission disk: gradual'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('All vSAN disk operations trigger resync; ensure >30% free space before starting;'))
    lines.append(txt_row('replacements must use HCL-approved disk models.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Mark failed    = UI action; moves data off disk before physical removal'))
    lines.append(txt_row('Full evacuation= moves all data off host before decommission'))
    lines.append(txt_row('Resync         = rebuild missing components after disk/host change'))
    lines.append(txt_row('Policy compliance= VM storage matches defined FTT/RAID policy'))
    lines.append(txt_row('Non-compliant  = policy not met; often after host failure or disk loss'))
    lines.append(txt_row('Rebalance      = redistribute objects across hosts for even utilisation'))
    lines.append(txt_row('Policies & Profiles= VC area for defining storage policies'))
    lines.append(txt_row('Re-apply policy= recalculate placement to restore compliance'))
    lines.append(txt_row('Decommission disk= graceful removal with data migration'))
    lines.append(txt_row('Claim disk     = assign new physical disk to vSAN cache/capacity role'))
    lines.append(txt_row('Disk group     = one cache + up to 7 capacity disks per ESXi host'))
    lines.append(txt_row('30% free       = minimum headroom for resync operations'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-ops-scripts',
    'docs/virtualization/vmware/vsan/operations/scripts/index.md',
    'vSAN — Operational Scripts',
)
def vsan_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vSAN — Operational Scripts'))
    lines.append(txt_row())
    lines.append(txt_row('PowerCLI and esxcli scripts automate vSAN health checks, capacity reporting,'))
    lines.append(txt_row('disk status audits, object compliance scans, and resync monitoring.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Health & Capacity Scripts'), bMid(L2, R2, 'Disk & Object Scripts'))))
    lines.append(R(merge(bMid(L1, R1, 'Test-VsanClusterHealth'), bMid(L2, R2, 'Get-VsanDisk | Ft Status'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-VsanClusterConfiguration'), bMid(L2, R2, 'esxcli vsan debug object'))))
    lines.append(R(merge(bMid(L1, R1, 'Capacity: Get-VsanDatastore'), bMid(L2, R2, 'cmmds-tool find -t DOM_NAME'))))
    lines.append(R(merge(bMid(L1, R1, 'Export CSV for capacity report'), bMid(L2, R2, 'vsan.resync_dashboard'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Health scripts run read-only; object debug scripts may need host shell access.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Policy Compliance Scripts'), bMid(L2, R2, 'Resync Monitoring'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-SpbmEntityConfiguration'), bMid(L2, R2, 'Watch-VsanResync loop'))))
    lines.append(R(merge(bMid(L1, R1, 'Find non-compliant VMs'), bMid(L2, R2, 'esxcli vsan debug object'))))
    lines.append(R(merge(bMid(L1, R1, 'Set-SpbmEntityConfiguration'), bMid(L2, R2, 'RVC: vsan.resync_dashboard'))))
    lines.append(R(merge(bMid(L1, R1, 'Bulk policy re-apply script'), bMid(L2, R2, 'Alert if resync >4h old'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Scripts connect via PowerCLI to vCenter; esxcli/cmmds-tool run on ESXi host shell.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Test-VsanClusterHealth= PowerCLI health check trigger'))
    lines.append(txt_row('Get-VsanDisk  = list disk state across all vSAN hosts'))
    lines.append(txt_row('Get-SpbmEntityConfiguration= policy compliance per VM'))
    lines.append(txt_row('Set-SpbmEntityConfiguration= apply storage policy to VM'))
    lines.append(txt_row('cmmds-tool    = Cluster Membership and Metadata Directory Service tool'))
    lines.append(txt_row('DOM_NAME      = Distributed Object Manager; each object has a UUID'))
    lines.append(txt_row('vsan.resync_dashboard= RVC command; shows resync progress'))
    lines.append(txt_row('SPBM          = Storage Policy Based Management; VC policy engine'))
    lines.append(txt_row('Non-compliant = VM FTT not met; data at risk'))
    lines.append(txt_row('Watch loop    = PowerShell while loop; poll resync every 60s'))
    lines.append(txt_row('Alert >4h     = resync older than 4h suggests stuck operation'))
    lines.append(txt_row('Capacity report= UsedCapacity/TotalCapacity per datastore per host'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-arch-comp-states',
    'docs/virtualization/vmware/vsan/architecture/component-states/index.md',
    'vSAN — Component State Lifecycle',
)
def vsan_arch_comp_states():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vSAN — Component State Lifecycle'))
    lines.append(txt_row())
    lines.append(txt_row('Every vSAN object is made of components distributed across hosts. Each component has a state'))
    lines.append(txt_row('that determines whether the object\'s protection policy is currently being met.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'ABSENT (transient)'), bMid(L2, R2, 'DEGRADED (at risk)'))))
    lines.append(R(merge(bMid(L1, R1, 'Host rebooted or lost temporarily'), bMid(L2, R2, 'Component confirmed lost'))))
    lines.append(R(merge(bMid(L1, R1, 'vSAN waits clomRepairDelay (default 60m)'), bMid(L2, R2, 'VM at risk: one more failure = loss'))))
    lines.append(R(merge(bMid(L1, R1, 'No rebuild triggered during wait'), bMid(L2, R2, 'CLOM schedules rebuild immediately'))))
    lines.append(R(merge(bMid(L1, R1, 'If host returns: component goes Healthy'), bMid(L2, R2, 'Rebuild needs capacity + healthy hosts'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('ABSENT → wait → host returns = Healthy. ABSENT → timer expires = DEGRADED → REBUILDING'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'STALE (outdated)'), bMid(L2, R2, 'REBUILDING (recovering)'))))
    lines.append(R(merge(bMid(L1, R1, 'Component exists but data is behind'), bMid(L2, R2, 'New component being written'))))
    lines.append(R(merge(bMid(L1, R1, 'Host was offline while writes occurred'), bMid(L2, R2, 'Bytes remaining shown in resync queue'))))
    lines.append(R(merge(bMid(L1, R1, 'Must sync before becoming healthy again'), bMid(L2, R2, 'I/O continues during rebuild'))))
    lines.append(R(merge(bMid(L1, R1, 'Can become healthy without full rebuild'), bMid(L2, R2, 'Completes to HEALTHY when done'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Component placement is managed by CLOM (Cluster Level Object Manager); each component'))
    lines.append(txt_row('lives on a specific disk group on a specific ESXi host; hardware health drives state changes.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Component      = one piece of a vSAN object stored on a specific disk group'))
    lines.append(txt_row('CLOM           = Cluster Level Object Manager; decides placement and rebuild'))
    lines.append(txt_row('clomRepairDelay= minutes vSAN waits before treating ABSENT as DEGRADED (default: 60)'))
    lines.append(txt_row('Resync         = the rebuild process — copies data from healthy to new component'))
    lines.append(txt_row('Object         = full logical unit (e.g. a VMDK); made of multiple components'))
    lines.append(txt_row('FTT            = Failures to Tolerate; determines how many components exist per object'))
    lines.append(txt_row('Witness        = metadata-only component; used for quorum, holds no data'))
    lines.append(txt_row('INACCESSIBLE   = all copies of a component are unavailable; VM stops I/O'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-arch-resync',
    'docs/virtualization/vmware/vsan/architecture/resync-mechanics/index.md',
    'vSAN — Resync Mechanics',
)
def vsan_arch_resync():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vSAN — Resync Mechanics'))
    lines.append(txt_row())
    lines.append(txt_row('Resync is vSAN rebuilding or rebalancing component data. Every disk replacement, host failure,'))
    lines.append(txt_row('policy change, or rebalance triggers it. Understanding resync mechanics prevents surprises.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Why Resync Triggers'), bMid(L2, R2, 'How CLOM Decides'))))
    lines.append(R(merge(bMid(L1, R1, 'Component goes DEGRADED'), bMid(L2, R2, 'Scan all degraded objects'))))
    lines.append(R(merge(bMid(L1, R1, 'Storage policy changes'), bMid(L2, R2, 'Find host + disk with free capacity'))))
    lines.append(R(merge(bMid(L1, R1, 'Host added (rebalance)'), bMid(L2, R2, 'Check FTT policy requirements'))))
    lines.append(R(merge(bMid(L1, R1, 'Dedup/encryption enabled'), bMid(L2, R2, 'Schedule rebuild operations'))))
    lines.append(R(merge(bMid(L1, R1, 'On-disk format upgrade'), bMid(L2, R2, 'Prioritise by object criticality'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Resync competes with VM I/O for disk and network bandwidth on all participating hosts.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Bandwidth and Duration'), bMid(L2, R2, 'Capacity Headroom Rule'))))
    lines.append(R(merge(bMid(L1, R1, 'Throughput limited by slowest disk'), bMid(L2, R2, '30% free required to rebuild'))))
    lines.append(R(merge(bMid(L1, R1, 'Network bottleneck on small clusters'), bMid(L2, R2, 'Without headroom: resync queued'))))
    lines.append(R(merge(bMid(L1, R1, 'Throttle: 0 = unlimited (fast)'), bMid(L2, R2, 'Over-commit blocks all future rebuilds'))))
    lines.append(R(merge(bMid(L1, R1, 'Throttle: 500 IOPS = business-safe'), bMid(L2, R2, 'Alert at 70%; hard stop near 80%'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Resync I/O travels over the vSAN VMkernel network (25 GbE recommended); disk throughput'))
    lines.append(txt_row('on destination host limits rebuild speed; CLOM runs on the cluster master host.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CLOM           = Cluster Level Object Manager; schedules and tracks all rebuild operations'))
    lines.append(txt_row('DOM            = Distributed Object Manager; handles per-object I/O and component writes'))
    lines.append(txt_row('Resync         = the actual data copy operation from source to destination component'))
    lines.append(txt_row('Delta-sync     = partial resync for STALE components — only changed blocks, not full copy'))
    lines.append(txt_row('Throttle       = IOPS limit applied to resync I/O; 0 = unlimited; 500 = production-safe'))
    lines.append(txt_row('Headroom       = free capacity needed to place the new component before old is removed'))
    lines.append(txt_row('Rebalance      = proactive move of components to equalise utilisation across hosts'))
    lines.append(txt_row('Policy resync  = triggered by FTT change, stripe width change, or dedup/encrypt toggle'))
    lines.append(txt_row('clomRepairDelay= minutes between component going ABSENT and CLOM starting rebuild'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-deploy',
    'docs/virtualization/vmware/vsan/deploy/index.md',
    'vSAN — Deployment Phases',
)
def vsan_deploy():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1 = 3, 29
    L2, R2 = 32, 59
    L3, R3 = 62, 97
    L7, R7 = 35, 70
    lines = []
    lines.append(title_border(W2, 'vSAN — Deployment Phases'))
    lines.append(txt_row())
    lines.append(txt_row('Seven phases from bare metal to operational vSAN cluster. Each phase has a clear exit criterion.'))
    lines.append(txt_row('Do not proceed to the next phase until the current phase validates clean.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2), bTop(L3, R3))))
    lines.append(R(merge(bMid(L1, R1, 'Phase 1: Physical'), bMid(L2, R2, 'Phase 2: ESXi'), bMid(L3, R3, 'Phase 3: vCenter'))))
    lines.append(R(merge(bMid(L1, R1, 'BIOS/UEFI settings'), bMid(L2, R2, 'Boot from ISO/PXE'), bMid(L3, R3, 'Deploy VCSA OVA'))))
    lines.append(R(merge(bMid(L1, R1, 'Network cabling'), bMid(L2, R2, 'First-boot config'), bMid(L3, R3, 'Configure SSO + inventory'))))
    lines.append(R(merge(bMid(L1, R1, 'iDRAC/iLO config'), bMid(L2, R2, 'vmk0 management IP'), bMid(L3, R3, 'Add hosts to datacenter'))))
    lines.append(R(merge(bMid(L1, R1, 'HCL verification'), bMid(L2, R2, 'NTP + DNS'), bMid(L3, R3, 'Create cluster object'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2), bBot(L3, R3))))
    lines.append(txt_row())
    lines.append(R(arrow([16, 45, 79])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2), bTop(L3, R3))))
    lines.append(R(merge(bMid(L1, R1, 'Phase 4: Networking'), bMid(L2, R2, 'Phase 5: vSAN Enable'), bMid(L3, R3, 'Phase 6: Aria Suite (optional)'))))
    lines.append(R(merge(bMid(L1, R1, 'dvSwitch creation'), bMid(L2, R2, 'Enable vSAN on cluster'), bMid(L3, R3, 'Aria Suite Lifecycle deploy'))))
    lines.append(R(merge(bMid(L1, R1, 'vSAN VMkernel + tag'), bMid(L2, R2, 'Disk group claim'), bMid(L3, R3, 'Aria Operations config'))))
    lines.append(R(merge(bMid(L1, R1, 'MTU 9000 end-to-end'), bMid(L2, R2, 'Storage policies'), bMid(L3, R3, 'vSAN adapter + dashboards'))))
    lines.append(R(merge(bMid(L1, R1, 'NIOC if shared NICs'), bMid(L2, R2, 'Health validation'), bMid(L3, R3, 'Alert thresholds'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2), bBot(L3, R3))))
    lines.append(txt_row())
    lines.append(R(arrow([52])))
    lines.append(txt_row())
    lines.append(R(bTop(L7, R7)))
    lines.append(R(bMid(L7, R7, 'Phase 7: Validation')))
    lines.append(R(bMid(L7, R7, 'Skyline Health all green')))
    lines.append(R(bMid(L7, R7, 'Storage policy compliance')))
    lines.append(R(bMid(L7, R7, 'Failover simulation')))
    lines.append(R(bMid(L7, R7, 'Performance baseline')))
    lines.append(R(bBot(L7, R7)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure: All phases run on physical ESXi hosts with NVMe/SSD disks,'))
    lines.append(txt_row('ToR switches (MTU 9000), OOB management (iDRAC/iLO), and DNS/NTP infrastructure.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('dvSwitch       = Distributed Virtual Switch; managed from vCenter across all hosts'))
    lines.append(txt_row('vmk            = VMkernel adapter; IP interface for vSAN, vMotion, management traffic'))
    lines.append(txt_row('VCSA           = vCenter Server Appliance; the VM running vCenter'))
    lines.append(txt_row('HCL            = Hardware Compatibility List; required for vSAN support'))
    lines.append(txt_row('NIOC           = Network I/O Control; traffic shaping on shared NICs'))
    lines.append(txt_row('Disk group     = one cache device + 1-7 capacity devices per ESXi host (OSA)'))
    lines.append(txt_row('SPBM           = Storage Policy-Based Management; policies applied per VM'))
    lines.append(txt_row('Skyline Health = built-in vSAN health dashboard in vCenter'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-sec-access',
    'docs/virtualization/vmware/vsan/security/access-control/index.md',
    'vSAN — Access Control',
)
def vsan_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vSAN — Access Control'))
    lines.append(txt_row())
    lines.append(txt_row('vSAN access control is managed through vCenter RBAC; dedicated vSAN admin'))
    lines.append(txt_row('roles and storage policy permissions control cluster configuration changes.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'vCenter RBAC for vSAN'), bMid(L2, R2, 'vSAN-Specific Privileges'))))
    lines.append(R(merge(bMid(L1, R1, 'Host.Config.Storage priv'), bMid(L2, R2, 'Datastore.Config: required'))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster-level Admin role'), bMid(L2, R2, 'StorageProfile.Update'))))
    lines.append(R(merge(bMid(L1, R1, 'No direct disk access for VMs'), bMid(L2, R2, 'VsanHealth: read-only role'))))
    lines.append(R(merge(bMid(L1, R1, 'Least privilege: read-only ops'), bMid(L2, R2, 'Disk.Configure: only admin'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Restrict disk configuration to cluster admins; storage policy changes to vSAN admins.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'ESXi Host Access'), bMid(L2, R2, 'Audit & Compliance'))))
    lines.append(R(merge(bMid(L1, R1, 'SSH: disable when not needed'), bMid(L2, R2, 'Log: all disk config ops'))))
    lines.append(R(merge(bMid(L1, R1, 'ESXi shell: time-limited'), bMid(L2, R2, 'Review: admin accounts qtrly'))))
    lines.append(R(merge(bMid(L1, R1, 'Lockdown mode: enforce'), bMid(L2, R2, 'Alert: unexpected disk claim'))))
    lines.append(R(merge(bMid(L1, R1, 'Access via vCenter only'), bMid(L2, R2, 'SIEM: forward vCenter events'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical disk access is restricted by ESXi; vSAN manages all disk I/O;'))
    lines.append(txt_row('no direct block device access from guest VMs.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RBAC          = Role-Based Access Control; vCenter permission model'))
    lines.append(txt_row('Privilege     = atomic permission; e.g., Datastore.Config'))
    lines.append(txt_row('Lockdown mode = ESXi blocks direct access; all ops via vCenter only'))
    lines.append(txt_row('StorageProfile= vCenter storage policy permission set'))
    lines.append(txt_row('VsanHealth    = read-only vSAN health monitoring privilege'))
    lines.append(txt_row('Disk.Configure= permission to add/remove disks from vSAN'))
    lines.append(txt_row('SIEM          = Security Info and Event Mgmt; receives vCenter events'))
    lines.append(txt_row('SSH disable   = reduce attack surface; enable only for troubleshooting'))
    lines.append(txt_row('Shell timeout = ESXi shell auto-closes after idle; set to 600s'))
    lines.append(txt_row('Cluster admin = role with full vSAN management privileges'))
    lines.append(txt_row('Audit log     = vCenter event log; captures all disk/policy changes'))
    lines.append(txt_row('Qtrly review  = check admin accounts; remove stale assignments'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-sec-auth',
    'docs/virtualization/vmware/vsan/security/authentication/index.md',
    'vSAN — Authentication',
)
def vsan_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vSAN — Authentication'))
    lines.append(txt_row())
    lines.append(txt_row('vSAN cluster nodes authenticate each other using the ESXi host SSL certificates;'))
    lines.append(txt_row('management authentication uses vCenter SSO.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster Node Auth'), bMid(L2, R2, 'Management Auth'))))
    lines.append(R(merge(bMid(L1, R1, 'ESXi SSL cert: node ID'), bMid(L2, R2, 'vCenter SSO: all logins'))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster UUID: shared secret'), bMid(L2, R2, 'SAML token for API calls'))))
    lines.append(R(merge(bMid(L1, R1, 'Host join: vCenter issues UUID'), bMid(L2, R2, 'AD groups: role-mapped'))))
    lines.append(R(merge(bMid(L1, R1, 'RDT: Reliable Datagram Transport'), bMid(L2, R2, 'MFA: per vCenter policy'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Cluster node trust uses ESXi certs; management trust uses vCenter SSO tokens.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'KMS Authentication'), bMid(L2, R2, 'Certificate Requirements'))))
    lines.append(R(merge(bMid(L1, R1, 'KMS: client cert per ESXi'), bMid(L2, R2, 'Host cert: auto-renewed'))))
    lines.append(R(merge(bMid(L1, R1, 'KMIP mutual TLS auth'), bMid(L2, R2, 'VMCA: signs host certs'))))
    lines.append(R(merge(bMid(L1, R1, 'KMS cluster: redundant pair'), bMid(L2, R2, 'Custom CA: replace VMCA'))))
    lines.append(R(merge(bMid(L1, R1, 'Key retrieval: power-on path'), bMid(L2, R2, 'Expiry: monitor >30 days'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('KMS server must be reachable from each ESXi host on management network port 5696;'))
    lines.append(txt_row('KMS cluster ensures HA key retrieval for encrypted vSAN.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Cluster UUID  = unique identifier shared across all vSAN cluster nodes'))
    lines.append(txt_row('RDT           = Reliable Datagram Transport; vSAN inter-host protocol'))
    lines.append(txt_row('KMIP          = Key Management Interoperability Protocol; port 5696'))
    lines.append(txt_row('KMS           = Key Management Server; holds encryption keys'))
    lines.append(txt_row('Mutual TLS    = both client and server present certs; bidirectional auth'))
    lines.append(txt_row('VMCA          = vSphere Certificate Authority; signs host machine certs'))
    lines.append(txt_row('Host cert     = SSL cert on each ESXi host; auto-renewed by VMCA'))
    lines.append(txt_row('Custom CA     = replace VMCA with enterprise PKI for compliance'))
    lines.append(txt_row('SAML token    = SSO assertion; used for vCenter API auth'))
    lines.append(txt_row('KMS cluster   = HA pair of KMS nodes; both must be reachable'))
    lines.append(txt_row('Key retrieval = power-on of encrypted VM triggers KMS request'))
    lines.append(txt_row('AD groups     = Active Directory groups mapped to vCenter RBAC roles'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-sec-enc',
    'docs/virtualization/vmware/vsan/security/encryption/index.md',
    'vSAN — Encryption',
)
def vsan_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vSAN — Encryption'))
    lines.append(txt_row())
    lines.append(txt_row('vSAN offers cluster-level data-at-rest encryption (OSA) and inline encryption'))
    lines.append(txt_row('(ESA); both require an external KMS and use AES-256 with KEK/DEK hierarchy.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'OSA Encryption (at-rest)'), bMid(L2, R2, 'ESA Inline Encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'Enabled per cluster'), bMid(L2, R2, 'vSAN 8+ / all-NVMe only'))))
    lines.append(R(merge(bMid(L1, R1, 'AES-256 XTS mode'), bMid(L2, R2, 'Encrypts before disk write'))))
    lines.append(R(merge(bMid(L1, R1, 'KEK from KMS wraps DEK'), bMid(L2, R2, 'Lower overhead than OSA'))))
    lines.append(R(merge(bMid(L1, R1, 'Re-key: rolling no outage'), bMid(L2, R2, 'Same KMS integration'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('OSA encrypts data at the disk layer; ESA encrypts inline before storage commit.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'KMS Configuration'), bMid(L2, R2, 'Key Management Ops'))))
    lines.append(R(merge(bMid(L1, R1, 'Add KMS cluster in vCenter'), bMid(L2, R2, 'Re-key: new KEK, same DEKs'))))
    lines.append(R(merge(bMid(L1, R1, 'Trust KMS cert in vCenter'), bMid(L2, R2, 'Shred key: wipe cluster'))))
    lines.append(R(merge(bMid(L1, R1, 'Enable enc: Cluster > Configure'), bMid(L2, R2, 'Backup KMS: critical!'))))
    lines.append(R(merge(bMid(L1, R1, 'Erase disks when removed'), bMid(L2, R2, 'KMS HA: cluster pair'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('KMS must be highly available and reachable from all ESXi hosts; losing KMS'))
    lines.append(txt_row('access prevents encrypted VM power-on.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('OSA enc       = Original Storage Architecture encryption; data at rest'))
    lines.append(txt_row('ESA inline    = Express Storage Architecture; encrypts before NVMe write'))
    lines.append(txt_row('AES-256 XTS   = encryption algorithm; XTS mode for block storage'))
    lines.append(txt_row('DEK           = Data Encryption Key; per disk group; AES-256'))
    lines.append(txt_row('KEK           = Key Encryption Key; stored in KMS; wraps DEKs'))
    lines.append(txt_row('Re-key        = rotate KEK from KMS; no downtime; existing DEKs unchanged'))
    lines.append(txt_row('Shred key     = destroy KEK in KMS; all data becomes unreadable'))
    lines.append(txt_row('Erase disks   = secure wipe when decommissioning encrypted disks'))
    lines.append(txt_row('KMS backup    = critical; if KMS lost with no backup, data is gone'))
    lines.append(txt_row('KMS cluster   = HA pair; both nodes hold key copies'))
    lines.append(txt_row('KMIP          = Key Management Interoperability Protocol; port 5696'))
    lines.append(txt_row('Trust KMS cert= vCenter must trust KMS server TLS cert for KMIP'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-sec-hard',
    'docs/virtualization/vmware/vsan/security/hardening/index.md',
    'vSAN — Hardening',
)
def vsan_sec_hard():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vSAN — Hardening'))
    lines.append(txt_row())
    lines.append(txt_row('vSAN hardening includes ESXi host hardening, vSAN network isolation, data-at-rest'))
    lines.append(txt_row('encryption, disk-level secure erase, and lockdown mode on all hosts.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Network Hardening'), bMid(L2, R2, 'Host Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'Dedicated vSAN VLAN'), bMid(L2, R2, 'Lockdown mode: enabled'))))
    lines.append(R(merge(bMid(L1, R1, 'Isolate from guest VM nets'), bMid(L2, R2, 'SSH: off when not in use'))))
    lines.append(R(merge(bMid(L1, R1, 'Jumbo frames vSAN net only'), bMid(L2, R2, 'ESXi shell: time-limited'))))
    lines.append(R(merge(bMid(L1, R1, 'Firewall: block mgmt from VMs'), bMid(L2, R2, 'Patch: 30-day SLA'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Network isolation prevents VM-level attacks on vSAN management traffic.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Data Hardening'), bMid(L2, R2, 'Compliance & Audit'))))
    lines.append(R(merge(bMid(L1, R1, 'Enable at-rest encryption'), bMid(L2, R2, 'CIS vSphere benchmark'))))
    lines.append(R(merge(bMid(L1, R1, 'Secure erase on disk removal'), bMid(L2, R2, 'Syslog: vSAN events to SIEM'))))
    lines.append(R(merge(bMid(L1, R1, 'KMS HA: 2+ nodes'), bMid(L2, R2, 'Policy: enforce FTT>0 always'))))
    lines.append(R(merge(bMid(L1, R1, 'Re-key schedule: 90 days'), bMid(L2, R2, 'Alert: disk removed event'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical disk security: tag decommissioned drives, apply secure erase, log disposal;'))
    lines.append(txt_row('KMS appliances must be physically secured.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Lockdown mode  = blocks direct ESXi access; requires vCenter for all ops'))
    lines.append(txt_row('At-rest enc    = AES-256 encryption of all vSAN disk data'))
    lines.append(txt_row('Secure erase   = SCSI sanitize command; wipe disk before decommission'))
    lines.append(txt_row('KMS HA         = 2+ KMS nodes; survives single KMS failure'))
    lines.append(txt_row('Re-key         = rotate KEK on schedule; 90 days is common policy'))
    lines.append(txt_row('vSAN VLAN      = dedicated L2 segment for inter-host vSAN traffic'))
    lines.append(txt_row('SIEM           = Security Info and Event Mgmt; vSAN alerts forwarded'))
    lines.append(txt_row('CIS benchmark  = Centre for Internet Security; vSphere hardening checklist'))
    lines.append(txt_row('FTT>0 policy   = ensure all VMs have ≥1 failure tolerance'))
    lines.append(txt_row('Disk disposal  = document and secure-erase all removed vSAN disks'))
    lines.append(txt_row('Patch SLA      = critical patches within 7d; high within 30d'))
    lines.append(txt_row('SSH off        = SSH disabled on ESXi; enable only for active troubleshoot'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-ts-common',
    'docs/virtualization/vmware/vsan/troubleshooting/common-issues/index.md',
    'vSAN — Common Issues',
)
def vsan_ts_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vSAN — Common Issues'))
    lines.append(txt_row())
    lines.append(txt_row('Common vSAN issues: degraded components, resync stalls, disk failures, network'))
    lines.append(txt_row('latency causing I/O aborts, capacity alarms, and policy non-compliance.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Degraded Components'), bMid(L2, R2, 'Resync Stalls'))))
    lines.append(R(merge(bMid(L1, R1, 'Symptom: health UI red'), bMid(L2, R2, 'Resync bytes not decreasing'))))
    lines.append(R(merge(bMid(L1, R1, 'Check: disk SMART errors'), bMid(L2, R2, 'Check: host in maint mode'))))
    lines.append(R(merge(bMid(L1, R1, 'Fix: replace failed disk'), bMid(L2, R2, 'Fix: exit maint mode'))))
    lines.append(R(merge(bMid(L1, R1, '60-min timer before rebuild'), bMid(L2, R2, 'Bandwidth limit: raise'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Degraded = policy at risk; check health UI immediately; resync removes the risk.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Network & I/O Issues'), bMid(L2, R2, 'Capacity & Policy Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'I/O abort: check MTU mismatch'), bMid(L2, R2, 'Capacity >70%: alert'))))
    lines.append(R(merge(bMid(L1, R1, 'Latency spike: resync traffic'), bMid(L2, R2, 'Non-compliant: re-apply'))))
    lines.append(R(merge(bMid(L1, R1, 'MTU test: vSAN health UI'), bMid(L2, R2, 'Dedup savings gone: expand'))))
    lines.append(R(merge(bMid(L1, R1, 'NIC team fail: check uplinks'), bMid(L2, R2, 'Stretched: witness down'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Most issues trace to: disk SMART failure, network MTU mismatch, host in maintenance,'))
    lines.append(txt_row('or capacity >70%; check all four before deep investigation.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Degraded      = replica lost; policy not met; data at risk'))
    lines.append(txt_row('Absent        = component missing <60min; vSAN waits before rebuilding'))
    lines.append(txt_row('60-min timer  = vSAN delay before treating absent as degraded'))
    lines.append(txt_row('SMART error   = disk pre-failure indicator; replace proactively'))
    lines.append(txt_row('MTU mismatch  = jumbo frames not configured end-to-end; causes I/O errors'))
    lines.append(txt_row('Resync BW     = configurable limit; default 128Mbps; raise for faster rebuild'))
    lines.append(txt_row('Policy non-compliant= VM does not meet FTT policy; fix = re-apply policy'))
    lines.append(txt_row('Witness down  = stretched cluster loses quorum; VMs may stall'))
    lines.append(txt_row('NIC team fail = check uplink status on vDS; failover should be automatic'))
    lines.append(txt_row('Dedup savings = dedup ratio drops when data is incompressible'))
    lines.append(txt_row('I/O abort     = VM I/O fails; check vSAN health for root cause'))
    lines.append(txt_row('Capacity 70%  = alert threshold; keep 30% free for resync headroom'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-ts-diag',
    'docs/virtualization/vmware/vsan/troubleshooting/diagnostics/index.md',
    'vSAN — Diagnostics',
)
def vsan_ts_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vSAN — Diagnostics'))
    lines.append(txt_row())
    lines.append(txt_row('vSAN diagnostics use the health UI, esxcli, RVC, cmmds-tool, and support bundle'))
    lines.append(txt_row('to identify root causes of component, network, and performance issues.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Health UI Checks'), bMid(L2, R2, 'CLI Diagnostics'))))
    lines.append(R(merge(bMid(L1, R1, 'vSAN Health: all green?'), bMid(L2, R2, 'esxcli vsan debug object'))))
    lines.append(R(merge(bMid(L1, R1, 'Object health: policy met?'), bMid(L2, R2, 'cmmds-tool find -t DOM_NAME'))))
    lines.append(R(merge(bMid(L1, R1, 'Network: MTU test pass?'), bMid(L2, R2, 'esxcli vsan storage list'))))
    lines.append(R(merge(bMid(L1, R1, 'Disk: all SMART healthy?'), bMid(L2, R2, 'vsan.resync_dashboard (RVC)'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Start in health UI; drill to object level with esxcli for per-component detail.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Performance Diagnostics'), bMid(L2, R2, 'Log Collection'))))
    lines.append(R(merge(bMid(L1, R1, 'vSAN Perf: latency graphs'), bMid(L2, R2, 'VC support bundle: host logs'))))
    lines.append(R(merge(bMid(L1, R1, 'vsanObserver: per-host stats'), bMid(L2, R2, 'vm-support on host shell'))))
    lines.append(R(merge(bMid(L1, R1, 'IOPS/throughput per datastore'), bMid(L2, R2, 'vsan_health*.log'))))
    lines.append(R(merge(bMid(L1, R1, 'NIC utilisation: esxtop net'), bMid(L2, R2, 'vsantraces: I/O path'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('All diagnostics run from ESXi host shell or vCenter; vsanObserver requires Java;'))
    lines.append(txt_row('support bundle is generated from vSphere Client > vCenter.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('cmmds-tool    = Cluster Membership and Directory Service CLI'))
    lines.append(txt_row('DOM_NAME      = Distributed Object Manager; per-object UUID'))
    lines.append(txt_row('RVC           = Ruby vSphere Console; vsan.resync_dashboard'))
    lines.append(txt_row('vsanObserver  = performance data collection tool; needs RVC'))
    lines.append(txt_row('vsan trace    = detailed I/O path log; written per host'))
    lines.append(txt_row('vm-support    = ESXi support bundle generator; per host'))
    lines.append(txt_row('esxtop net    = real-time ESXi NIC stats; throughput + drops'))
    lines.append(txt_row('MTU test      = pings vSAN VMkernel with 8972-byte payload'))
    lines.append(txt_row('IOPS graph    = vSAN Performance Service; must be enabled'))
    lines.append(txt_row('vsan_health   = health service log; check for ERROR lines'))
    lines.append(txt_row('Object health = per-VM health; shows absent/degraded components'))
    lines.append(txt_row('SMART         = disk self-test; pre-failure indicator'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vsan-ts-esc',
    'docs/virtualization/vmware/vsan/troubleshooting/escalation/index.md',
    'vSAN — Escalation',
)
def vsan_ts_esc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'vSAN — Escalation'))
    lines.append(txt_row())
    lines.append(txt_row('Escalate vSAN issues to VMware GSS when data is at risk, resync is stalled,'))
    lines.append(txt_row('or cluster is degraded below FTT policy with no recovery path.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Escalation Triggers'), bMid(L2, R2, 'Pre-Escalation Steps'))))
    lines.append(R(merge(bMid(L1, R1, 'Multiple disk failures'), bMid(L2, R2, 'Collect support bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'All objects degraded'), bMid(L2, R2, 'Run vm-support on hosts'))))
    lines.append(R(merge(bMid(L1, R1, 'Resync stalled >4 hours'), bMid(L2, R2, 'Note exact error messages'))))
    lines.append(R(merge(bMid(L1, R1, 'Data inaccessible / I/O hang'), bMid(L2, R2, 'Capture cmmds-tool output'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Multiple simultaneous disk failures require urgent GSS engagement; data may be at risk.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'GSS Engagement'), bMid(L2, R2, 'Escalation Path'))))
    lines.append(R(merge(bMid(L1, R1, 'Open P1 SR immediately'), bMid(L2, R2, 'T1: triage + bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'Include vSAN build number'), bMid(L2, R2, 'T2: vSAN SE assigned'))))
    lines.append(R(merge(bMid(L1, R1, 'Attach support bundle ZIP'), bMid(L2, R2, 'T3: engineering review'))))
    lines.append(R(merge(bMid(L1, R1, 'Do NOT power off hosts'), bMid(L2, R2, 'CritSit if data lost'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Do not touch physical disks or power cycle hosts without GSS guidance when data'))
    lines.append(txt_row('is degraded; further failures may push below quorum threshold.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Degraded      = FTT policy not met; one more failure = data loss'))
    lines.append(txt_row('Quorum        = majority of object components must be accessible'))
    lines.append(txt_row('I/O hang      = VMs stalled waiting for storage; immediate P1'))
    lines.append(txt_row('Support bundle= includes all vSAN host logs + CMMDS metadata'))
    lines.append(txt_row('vm-support    = per-host diagnostic bundle; run on all affected hosts'))
    lines.append(txt_row('cmmds-tool    = shows component placement; critical for GSS triage'))
    lines.append(txt_row('P1 SR         = highest priority SR; triggers 24/7 oncall response'))
    lines.append(txt_row('CritSit       = Critical Situation; executive escalation; 24/7 war room'))
    lines.append(txt_row('T2/T3         = senior SE or engineering involvement'))
    lines.append(txt_row('Do not power off= hosts hold component data; powering off worsens state'))
    lines.append(txt_row('Build number  = vSAN version from: esxcli vsan cluster get'))
    lines.append(txt_row('GSS           = Global Support Services (VMware/Broadcom)'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-arch-how',
    'docs/virtualization/vmware/vmware-cloud-foundation/architecture/how-it-works/index.md',
    'VMware Cloud Foundation — How It Works',
)
def vcf_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Cloud Foundation — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('VCF bundles vSphere, vSAN, NSX, and Aria into a single SDDC stack; SDDC Manager'))
    lines.append(txt_row('automates lifecycle, domain creation, and cluster expansion.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'SDDC Manager'), bMid(L2, R2, 'Domain Model'))))
    lines.append(R(merge(bMid(L1, R1, 'Lifecycle management hub'), bMid(L2, R2, 'Management domain: ops stack'))))
    lines.append(R(merge(bMid(L1, R1, 'Deploys vCenter + NSX + vSAN'), bMid(L2, R2, 'Workload domains: tenant'))))
    lines.append(R(merge(bMid(L1, R1, 'Certificate management'), bMid(L2, R2, 'VI domain: vSphere+vSAN'))))
    lines.append(R(merge(bMid(L1, R1, 'Password rotation: all stacks'), bMid(L2, R2, 'NSX: shared or per-domain'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SDDC Manager orchestrates all operations; management domain deploys first.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Bring-Up Process'), bMid(L2, R2, 'Cluster Expansion'))))
    lines.append(R(merge(bMid(L1, R1, 'Cloud Builder: initial deploy'), bMid(L2, R2, 'Add host to pool'))))
    lines.append(R(merge(bMid(L1, R1, 'Validates HW readiness'), bMid(L2, R2, 'SDDC Mgr: expand cluster'))))
    lines.append(R(merge(bMid(L1, R1, 'Deploys mgmt domain stack'), bMid(L2, R2, 'Create workload domain'))))
    lines.append(R(merge(bMid(L1, R1, 'JSON spec: all config values'), bMid(L2, R2, 'Hosts: from free pool'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('VCF requires VMware-compatible servers on the VCF HCL; minimum 4 hosts for'))
    lines.append(txt_row('management domain; 25GbE+ network with defined VLAN layout.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SDDC Manager  = VCF automation and lifecycle engine; manages all components'))
    lines.append(txt_row('Cloud Builder = initial deployment tool; validates and bootstraps VCF'))
    lines.append(txt_row('Management domain= first domain; runs SDDC Mgr, vCenter, NSX, vSAN'))
    lines.append(txt_row('Workload domain= tenant cluster; separate vCenter + NSX per domain'))
    lines.append(txt_row('VI domain     = vSphere+vSAN workload domain; most common type'))
    lines.append(txt_row('NSX shared    = single NSX manager serves multiple workload domains'))
    lines.append(txt_row('Free pool     = unallocated hosts available for domain creation'))
    lines.append(txt_row('JSON spec     = configuration file passed to Cloud Builder for bringup'))
    lines.append(txt_row('Bring-up      = process to deploy management domain from scratch'))
    lines.append(txt_row('HCL           = Hardware Compatibility List; VCF-specific list'))
    lines.append(txt_row('vLCM          = vSphere Lifecycle Manager; manages ESXi patching in VCF'))
    lines.append(txt_row('SDDC          = Software-Defined Data Center; the overall VCF platform'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-arch-int',
    'docs/virtualization/vmware/vmware-cloud-foundation/architecture/integrations/index.md',
    'VMware Cloud Foundation — Integrations',
)
def vcf_arch_int():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Cloud Foundation — Integrations'))
    lines.append(txt_row())
    lines.append(txt_row('VCF integrates with external identity (AD/LDAP), backup tools, external KMS,'))
    lines.append(txt_row('monitoring (Aria Operations), and cloud connectivity (VMware Cloud Gateway).'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Identity Integrations'), bMid(L2, R2, 'Backup Integrations'))))
    lines.append(R(merge(bMid(L1, R1, 'AD/LDAP: per vCenter domain'), bMid(L2, R2, 'VADP: Veeam/Commvault'))))
    lines.append(R(merge(bMid(L1, R1, 'SSO: per workload domain'), bMid(L2, R2, 'vSAN: CBT snapshots'))))
    lines.append(R(merge(bMid(L1, R1, 'vIDM: unified identity'), bMid(L2, R2, 'SDDC Mgr: config backup'))))
    lines.append(R(merge(bMid(L1, R1, 'SAML federation: Aria suite'), bMid(L2, R2, 'NSX: config export'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Identity integrates per domain; vIDM provides unified SSO across all VCF components.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Monitoring & Security'), bMid(L2, R2, 'Cloud Integrations'))))
    lines.append(R(merge(bMid(L1, R1, 'Aria Operations: all domains'), bMid(L2, R2, 'VMware Cloud Gateway'))))
    lines.append(R(merge(bMid(L1, R1, 'Aria Logs: syslog ingestion'), bMid(L2, R2, 'HCX: VM migration'))))
    lines.append(R(merge(bMid(L1, R1, 'KMS: per vSAN encryption'), bMid(L2, R2, 'VMC on AWS integration'))))
    lines.append(R(merge(bMid(L1, R1, 'SIEM: forward syslog'), bMid(L2, R2, 'Tanzu: Kubernetes on VCF'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Integration traffic crosses management network; KMS must be reachable from all hosts;'))
    lines.append(txt_row('HCX uses dedicated uplink network for VM migrations.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vIDM       = VMware Identity Manager; unified SSO across VCF products'))
    lines.append(txt_row('SAML       = Security Assertion Markup Language; federation token format'))
    lines.append(txt_row('HCX        = Hybrid Cloud Extension; WAN-optimised VM migration'))
    lines.append(txt_row('VMC        = VMware Cloud on AWS; extend VCF to public cloud'))
    lines.append(txt_row('Cloud GW   = on-prem appliance connecting VCF to VMware cloud services'))
    lines.append(txt_row('Tanzu      = Kubernetes runtime integrated into VCF workload domains'))
    lines.append(txt_row('Aria Ops   = operations management; multi-domain visibility'))
    lines.append(txt_row('Aria Logs  = centralised log management for all VCF components'))
    lines.append(txt_row('KMS        = external key server for vSAN at-rest encryption'))
    lines.append(txt_row('VADP       = vStorage APIs for Data Protection; backup integration'))
    lines.append(txt_row('SDDC Mgr backup= exports SDDC Manager config; restore to rebuild'))
    lines.append(txt_row('SIEM       = Security Information and Event Management; log receiver'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-arch-design',
    'docs/virtualization/vmware/vmware-cloud-foundation/architecture/design-standards/index.md',
    'VMware Cloud Foundation — Design Standards',
)
def vcf_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Cloud Foundation — Design Standards'))
    lines.append(txt_row())
    lines.append(txt_row('VCF design standards define domain layout, host sizing, VLAN scheme, NSX topology,'))
    lines.append(txt_row('and upgrade sequencing following VMware VCF design guidance.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Domain Design'), bMid(L2, R2, 'Network Design'))))
    lines.append(R(merge(bMid(L1, R1, '1 mgmt domain: min 4 hosts'), bMid(L2, R2, 'VLANs: mgmt/vSAN/vMotion'))))
    lines.append(R(merge(bMid(L1, R1, '1+ workload domains'), bMid(L2, R2, 'NSX overlay: VXLAN/GENEVE'))))
    lines.append(R(merge(bMid(L1, R1, 'Separate VC per domain'), bMid(L2, R2, '25GbE minimum uplinks'))))
    lines.append(R(merge(bMid(L1, R1, 'NSX: shared or dedicated'), bMid(L2, R2, 'MTU 9000: all VLANs'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Mgmt domain hosts VCF tooling; workload domains host applications.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Upgrade Standards'), bMid(L2, R2, 'Sizing Standards'))))
    lines.append(R(merge(bMid(L1, R1, 'SDDC Mgr: upgrade via UI'), bMid(L2, R2, 'Mgmt hosts: 512GB RAM+'))))
    lines.append(R(merge(bMid(L1, R1, 'Bundle: download from depot'), bMid(L2, R2, 'Workload: right-size for app'))))
    lines.append(R(merge(bMid(L1, R1, 'Upgrade order: VCF defined'), bMid(L2, R2, 'vSAN: HCL disks only'))))
    lines.append(R(merge(bMid(L1, R1, 'Pre-check: run before apply'), bMid(L2, R2, 'NVMe/SSD: ESA or OSA'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Servers must be on VCF HCL; 25GbE TOR switches; dedicated management network;'))
    lines.append(txt_row('separate OOB management (iDRAC/iLO) for host lifecycle.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Management domain= first VCF domain; hosts SDDC Manager + shared infra'))
    lines.append(txt_row('Workload domain = application cluster; separate lifecycle from mgmt'))
    lines.append(txt_row('SDDC Manager  = automation hub; upgrade bundles applied here'))
    lines.append(txt_row('Bundle        = VCF update package; downloaded from VMware depot'))
    lines.append(txt_row('Pre-check     = automated readiness validation before applying bundle'))
    lines.append(txt_row('NSX shared    = one NSX manager serving multiple domains'))
    lines.append(txt_row('NSX dedicated = per-domain NSX manager for isolation'))
    lines.append(txt_row('GENEVE        = NSX-T overlay protocol; replaced VXLAN'))
    lines.append(txt_row('MTU 9000      = jumbo frames; required for all VCF network segments'))
    lines.append(txt_row('OOB           = Out-of-Band management; iDRAC/iLO for host power/BIOS'))
    lines.append(txt_row('HCL           = Hardware Compatibility List; VCF-specific requirements'))
    lines.append(txt_row('Upgrade order = VCF prescribes sequence; SDDC Mgr → vCenter → ESXi → NSX'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-ops-backup',
    'docs/virtualization/vmware/vmware-cloud-foundation/operations/backup-restore/index.md',
    'VMware Cloud Foundation — Backup & Restore',
)
def vcf_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Cloud Foundation — Backup & Restore'))
    lines.append(txt_row())
    lines.append(txt_row('VCF backup covers SDDC Manager, all vCenters, and NSX managers; each component'))
    lines.append(txt_row('has its own backup mechanism; orchestrated via SDDC Manager.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'SDDC Manager Backup'), bMid(L2, R2, 'vCenter Backup'))))
    lines.append(R(merge(bMid(L1, R1, 'SFTP-based external backup'), bMid(L2, R2, 'File-based via VAMI'))))
    lines.append(R(merge(bMid(L1, R1, 'Schedule: daily minimum'), bMid(L2, R2, 'SFTP or SCP target'))))
    lines.append(R(merge(bMid(L1, R1, 'Config: domains + credentials'), bMid(L2, R2, 'Schedule: daily'))))
    lines.append(R(merge(bMid(L1, R1, 'Encryption: optional passphrase'), bMid(L2, R2, 'All domains backed up'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SDDC Manager backup is critical; without it domain topology cannot be recovered.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'NSX Manager Backup'), bMid(L2, R2, 'Restore Procedure'))))
    lines.append(R(merge(bMid(L1, R1, 'NSX UI: Operations > Backup'), bMid(L2, R2, 'Restore SDDC Mgr first'))))
    lines.append(R(merge(bMid(L1, R1, 'SFTP target: external server'), bMid(L2, R2, 'Then restore vCenters'))))
    lines.append(R(merge(bMid(L1, R1, 'Per-domain NSX backed up'), bMid(L2, R2, 'Then restore NSX managers'))))
    lines.append(R(merge(bMid(L1, R1, 'Encryption passphrase: store!'), bMid(L2, R2, 'Validate: all services up'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Backup target SFTP server must be on management network; store passphrase in'))
    lines.append(txt_row('separate secure location from backup files.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SDDC Manager backup= JSON export of all domain topology and credentials'))
    lines.append(txt_row('SFTP          = Secure File Transfer Protocol; backup transport'))
    lines.append(txt_row('Passphrase    = encrypts NSX backup; must be stored separately'))
    lines.append(txt_row('File-based    = VCSA native backup; config + DB; not full image'))
    lines.append(txt_row('Restore order = SDDC Mgr → vCenter → NSX; sequence is critical'))
    lines.append(txt_row('Domain topology= SDDC Mgr stores which hosts/clusters/domains exist'))
    lines.append(txt_row('NSX backup    = includes all routing, firewall, segment config'))
    lines.append(txt_row('vCenter backup= inventory, policies, permissions, alarms'))
    lines.append(txt_row('vSAN VMs      = backed up separately via VADP tools'))
    lines.append(txt_row('Encryption    = backup passphrase; AES encryption of backup files'))
    lines.append(txt_row('VAMI          = vCenter Appliance Management; port 5480; backup UI'))
    lines.append(txt_row('RPO           = daily backup = 24h RPO for config; VMs = per backup tool'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-ops-cli',
    'docs/virtualization/vmware/vmware-cloud-foundation/operations/cli-reference/index.md',
    'VMware Cloud Foundation — CLI Reference',
)
def vcf_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Cloud Foundation — CLI Reference'))
    lines.append(txt_row())
    lines.append(txt_row('VCF is primarily managed via SDDC Manager UI and REST API; PowerVCF and lcm-cli'))
    lines.append(txt_row('provide CLI automation for lifecycle, password, and certificate operations.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'PowerVCF Commands'), bMid(L2, R2, 'SDDC Manager REST API'))))
    lines.append(R(merge(bMid(L1, R1, 'Connect-VCFManager -fqdn'), bMid(L2, R2, 'GET /v1/sddcs (list)'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-VCFDomain (list domains)'), bMid(L2, R2, 'GET /v1/domains'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-VCFHost (host inventory)'), bMid(L2, R2, 'GET /v1/hosts'))))
    lines.append(R(merge(bMid(L1, R1, 'Start-VCFUpgrade (trigger)'), bMid(L2, R2, 'POST /v1/upgrades'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('PowerVCF wraps SDDC Manager REST API; all ops require SDDC Manager admin credentials.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Password & Cert CLI'), bMid(L2, R2, 'LCM CLI (on appliance)'))))
    lines.append(R(merge(bMid(L1, R1, 'Request-VCFToken (auth)'), bMid(L2, R2, 'lcm status'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-VCFCredential (list)'), bMid(L2, R2, 'lcm bundle-download'))))
    lines.append(R(merge(bMid(L1, R1, 'Set-VCFCredential (rotate)'), bMid(L2, R2, 'lcm upgrade-status'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-VCFCertificate (status)'), bMid(L2, R2, 'lcm remediate'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('PowerVCF connects over HTTPS to SDDC Manager; lcm-cli runs on SDDC Manager appliance'))
    lines.append(txt_row('shell accessed via SSH on port 22.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('PowerVCF     = PowerShell module for SDDC Manager REST API automation'))
    lines.append(txt_row('SDDC Manager = VCF control plane; REST API on port 443'))
    lines.append(txt_row('Request-VCFToken= obtain bearer token for API auth'))
    lines.append(txt_row('lcm-cli      = Lifecycle Manager CLI on SDDC Manager appliance'))
    lines.append(txt_row('lcm bundle   = upgrade package downloaded from VMware depot'))
    lines.append(txt_row('Get-VCFCredential= list all managed passwords (rotated by SDDC Mgr)'))
    lines.append(txt_row('Set-VCFCredential= trigger password rotation for a component'))
    lines.append(txt_row('Get-VCFDomain = list all workload and management domains'))
    lines.append(txt_row('Get-VCFHost  = list all hosts; free pool or assigned to domain'))
    lines.append(txt_row('Bearer token = JWT token; obtained via API; expires after 24h'))
    lines.append(txt_row('lcm remediate= fix failed upgrade tasks; retry individual steps'))
    lines.append(txt_row('upgrade-status= show current upgrade state across all components'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-ops-health',
    'docs/virtualization/vmware/vmware-cloud-foundation/operations/health-checks/index.md',
    'VMware Cloud Foundation — Health Checks',
)
def vcf_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Cloud Foundation — Health Checks'))
    lines.append(txt_row())
    lines.append(txt_row('VCF health checks span SDDC Manager, all vCenters, NSX managers, vSAN clusters,'))
    lines.append(txt_row('and certificate validity across all workload and management domains.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'SDDC Manager Health'), bMid(L2, R2, 'Component Health'))))
    lines.append(R(merge(bMid(L1, R1, 'Dashboard: all green status'), bMid(L2, R2, 'All vCenters: connected'))))
    lines.append(R(merge(bMid(L1, R1, 'Free pool: hosts available'), bMid(L2, R2, 'NSX: all nodes UP'))))
    lines.append(R(merge(bMid(L1, R1, 'Backup: last run <24h'), bMid(L2, R2, 'vSAN: health green'))))
    lines.append(R(merge(bMid(L1, R1, 'LCM: no upgrade in progress'), bMid(L2, R2, 'Credentials: not expired'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SDDC Manager dashboard gives holistic view; drill into each domain for detail.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Certificate Health'), bMid(L2, R2, 'Network & Storage Health'))))
    lines.append(R(merge(bMid(L1, R1, 'SDDC Mgr cert expiry >30d'), bMid(L2, R2, 'vSAN: resync = 0 bytes'))))
    lines.append(R(merge(bMid(L1, R1, 'vCenter STS cert check'), bMid(L2, R2, 'NSX: BGP/routes OK'))))
    lines.append(R(merge(bMid(L1, R1, 'NSX cert expiry >30d'), bMid(L2, R2, 'MTU: vSAN test pass'))))
    lines.append(R(merge(bMid(L1, R1, 'Rotate before expiry!'), bMid(L2, R2, 'Hosts: all connected'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('All VCF components run as VMs on the management domain; SDDC Manager health'))
    lines.append(txt_row('depends on underlying ESXi hosts and vSAN datastore availability.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SDDC Manager  = checks aggregated health of all VCF components'))
    lines.append(txt_row('LCM           = Lifecycle Manager; controls upgrade pipelines'))
    lines.append(txt_row('Free pool     = unassigned hosts; availability affects domain growth'))
    lines.append(txt_row('STS cert      = SSO Security Token Service cert; 2yr expiry'))
    lines.append(txt_row('NSX cert      = NSX Manager and edge certs; auto-renew in 8.0+'))
    lines.append(txt_row('Credentials   = SDDC Mgr manages passwords for all components'))
    lines.append(txt_row('vSAN resync   = 0 bytes = no data movement in progress'))
    lines.append(txt_row('BGP           = NSX routing protocol to physical network'))
    lines.append(txt_row('MTU test      = vSAN jumbo frame validation across all hosts'))
    lines.append(txt_row('Backup health = SDDC Mgr tracks last backup success timestamp'))
    lines.append(txt_row('Rotate cert   = use SDDC Mgr to rotate certs >30d before expiry'))
    lines.append(txt_row('Domain view   = per-domain health in SDDC Mgr Workload Domains tab'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-ops-install',
    'docs/virtualization/vmware/vmware-cloud-foundation/operations/install-upgrade/index.md',
    'VMware Cloud Foundation — Install & Upgrade',
)
def vcf_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Cloud Foundation — Install & Upgrade'))
    lines.append(txt_row())
    lines.append(txt_row('VCF installation uses Cloud Builder to deploy the management domain; upgrades'))
    lines.append(txt_row('are orchestrated by SDDC Manager LCM using versioned upgrade bundles.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Installation Steps'), bMid(L2, R2, 'Pre-Install Requirements'))))
    lines.append(R(merge(bMid(L1, R1, 'Deploy Cloud Builder OVA'), bMid(L2, R2, 'HCL: all hardware listed'))))
    lines.append(R(merge(bMid(L1, R1, 'Complete bringup JSON spec'), bMid(L2, R2, 'DNS: all FQDNs resolve'))))
    lines.append(R(merge(bMid(L1, R1, 'Cloud Builder validates input'), bMid(L2, R2, 'NTP: all hosts synced'))))
    lines.append(R(merge(bMid(L1, R1, 'Deploy mgmt domain (~2h)'), bMid(L2, R2, 'VLANs: created on switches'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('DNS and NTP must be correct before bringup; validation failures abort deployment.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Upgrade Process'), bMid(L2, R2, 'Post-Upgrade Steps'))))
    lines.append(R(merge(bMid(L1, R1, 'Download bundle in SDDC Mgr'), bMid(L2, R2, 'Run VCF health check'))))
    lines.append(R(merge(bMid(L1, R1, 'Run pre-check validation'), bMid(L2, R2, 'Verify all certs valid'))))
    lines.append(R(merge(bMid(L1, R1, 'Apply: mgmt domain first'), bMid(L2, R2, 'Check vSAN health'))))
    lines.append(R(merge(bMid(L1, R1, 'Then apply to workload domains'), bMid(L2, R2, 'Validate NSX routing'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Bringup needs 4+ identical bare-metal servers; upgrade temporarily increases'))
    lines.append(txt_row('host resource usage during patching; maintain 30% vSAN free space.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Cloud Builder = OVA appliance; validates spec and deploys management domain'))
    lines.append(txt_row('Bringup       = initial VCF deployment process; ~2h for management domain'))
    lines.append(txt_row('JSON spec     = configuration file for Cloud Builder; all IP/FQDN values'))
    lines.append(txt_row('SDDC Manager  = takes over from Cloud Builder post-bringup'))
    lines.append(txt_row('LCM           = Lifecycle Manager in SDDC Mgr; manages all upgrades'))
    lines.append(txt_row('Bundle        = versioned upgrade package; downloaded from VMware depot'))
    lines.append(txt_row('Pre-check     = automated readiness validation; must pass before upgrade'))
    lines.append(txt_row('Mgmt domain first= always upgrade management domain before workload domains'))
    lines.append(txt_row('VCF version   = e.g., VCF 5.2; all components versioned together'))
    lines.append(txt_row('HCL           = Hardware Compatibility List; VCF-specific server/NIC list'))
    lines.append(txt_row('VLAN scheme   = mgmt/vSAN/vMotion/uplink VLANs defined in spec'))
    lines.append(txt_row('Depot         = VMware online update repository; SDDC Mgr downloads from'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-ops-proc',
    'docs/virtualization/vmware/vmware-cloud-foundation/operations/procedures/index.md',
    'VMware Cloud Foundation — Common Procedures',
)
def vcf_ops_proc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Cloud Foundation — Common Procedures'))
    lines.append(txt_row())
    lines.append(txt_row('Routine VCF procedures: add host to free pool, create workload domain, rotate'))
    lines.append(txt_row('passwords, renew certificates, and commission/decommission domains.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Host Management'), bMid(L2, R2, 'Domain Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Commission host to free pool'), bMid(L2, R2, 'Create workload domain'))))
    lines.append(R(merge(bMid(L1, R1, 'Validate: HCL + connectivity'), bMid(L2, R2, 'Select hosts from pool'))))
    lines.append(R(merge(bMid(L1, R1, 'Assign to workload domain'), bMid(L2, R2, 'SDDC Mgr deploys VC+NSX'))))
    lines.append(R(merge(bMid(L1, R1, 'Remove: decommission first'), bMid(L2, R2, 'Decommission: drain VMs'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Commission adds hardware capacity; workload domain creation consumes free pool hosts.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Credential & Cert Rotation'), bMid(L2, R2, 'Cluster Scaling'))))
    lines.append(R(merge(bMid(L1, R1, 'Rotate: SDDC Mgr > Security'), bMid(L2, R2, 'Expand: add hosts to domain'))))
    lines.append(R(merge(bMid(L1, R1, 'Remediate: fix stuck rotation'), bMid(L2, R2, 'Contract: drain + remove'))))
    lines.append(R(merge(bMid(L1, R1, 'Certs: Certificates tab'), bMid(L2, R2, 'Add cluster to domain'))))
    lines.append(R(merge(bMid(L1, R1, 'CSR: generate + import'), bMid(L2, R2, 'Delete cluster: drain first'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Adding hosts requires physical cabling, BIOS config, and SDDC Mgr commissioning;'))
    lines.append(txt_row('password rotation may cause brief component restarts.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Commission    = add physical host to SDDC Mgr free pool'))
    lines.append(txt_row('Decommission  = remove host from VCF; must drain first'))
    lines.append(txt_row('Free pool     = hosts available for domain assignment'))
    lines.append(txt_row('Workload domain= isolated cluster with its own vCenter + NSX'))
    lines.append(txt_row('Credential rotation= SDDC Mgr rotates passwords for all managed components'))
    lines.append(txt_row('CSR           = Certificate Signing Request; generated by SDDC Mgr'))
    lines.append(txt_row('Remediate     = fix stuck lifecycle task; retry failed step'))
    lines.append(txt_row('Expand cluster= add hosts to existing cluster in a domain'))
    lines.append(txt_row('Contract      = reduce cluster size; hosts return to free pool'))
    lines.append(txt_row('Drain         = migrate VMs off host before decommission'))
    lines.append(txt_row('Security tab  = SDDC Mgr area for credential rotation and cert management'))
    lines.append(txt_row('Certificate tab= SDDC Mgr UI for cert status, CSR, and import'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-ops-scripts',
    'docs/virtualization/vmware/vmware-cloud-foundation/operations/scripts/index.md',
    'VMware Cloud Foundation — Operational Scripts',
)
def vcf_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Cloud Foundation — Operational Scripts'))
    lines.append(txt_row())
    lines.append(txt_row('PowerVCF scripts automate VCF operations: domain inventory, upgrade status,'))
    lines.append(txt_row('credential audit, certificate expiry check, and health report generation.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Inventory Scripts'), bMid(L2, R2, 'Health & Cert Scripts'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-VCFDomain | Export-Csv'), bMid(L2, R2, 'Request-VCFToken (auth)'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-VCFHost (all hosts)'), bMid(L2, R2, 'Get-VCFCertificate (expiry)'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-VCFCluster (all clusters)'), bMid(L2, R2, 'VMware.CloudFoundation.Reporting'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-VCFCredential (audit)'), bMid(L2, R2, 'Invoke-VcfHealthReport'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('PowerVCF scripts connect to SDDC Manager REST API; read-only ops need no approval.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Upgrade Scripts'), bMid(L2, R2, 'Automation Examples'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-VCFBundle (list bundles)'), bMid(L2, R2, 'New-VCFDomain (create)'))))
    lines.append(R(merge(bMid(L1, R1, 'Start-VCFBundleUpload'), bMid(L2, R2, 'Add-VCFHost (commission)'))))
    lines.append(R(merge(bMid(L1, R1, 'Start-VCFUpgrade (trigger)'), bMid(L2, R2, 'Set-VCFCredential (rotate)'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-VCFTask (status poll)'), bMid(L2, R2, 'Watch upgrade via task ID'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Scripts run from management jump host; connect to SDDC Manager on port 443;'))
    lines.append(txt_row('VMware.CloudFoundation.Reporting module needs PowerCLI + PowerVCF.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('PowerVCF       = PowerShell module for SDDC Manager automation'))
    lines.append(txt_row('Request-VCFToken= authenticate and store bearer token for session'))
    lines.append(txt_row('Get-VCFBundle  = list available upgrade bundles in depot/local'))
    lines.append(txt_row('Start-VCFUpgrade= trigger upgrade for a domain or component'))
    lines.append(txt_row('Get-VCFTask   = poll async task status by task ID'))
    lines.append(txt_row('Invoke-VcfHealthReport= generates HTML health report for all domains'))
    lines.append(txt_row('Get-VCFCertificate= certificate expiry report for all components'))
    lines.append(txt_row('New-VCFDomain = automate workload domain creation via API'))
    lines.append(txt_row('Add-VCFHost   = commission new host to SDDC Manager'))
    lines.append(txt_row('Set-VCFCredential= trigger credential rotation for component'))
    lines.append(txt_row('Reporting module= VMware.CloudFoundation.Reporting on PowerShell Gallery'))
    lines.append(txt_row('Task ID       = async operation ID; poll with Get-VCFTask until complete'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-sec-access',
    'docs/virtualization/vmware/vmware-cloud-foundation/security/access-control/index.md',
    'VMware Cloud Foundation — Access Control',
)
def vcf_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Cloud Foundation — Access Control'))
    lines.append(txt_row())
    lines.append(txt_row('VCF access control spans SDDC Manager (admin/operator/viewer roles), vCenter RBAC'))
    lines.append(txt_row('per domain, NSX RBAC, and credential management for all service accounts.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'SDDC Manager Roles'), bMid(L2, R2, 'Per-Domain RBAC'))))
    lines.append(R(merge(bMid(L1, R1, 'Admin: full control'), bMid(L2, R2, 'Each domain: own vCenter'))))
    lines.append(R(merge(bMid(L1, R1, 'Operator: manage but not config'), bMid(L2, R2, 'AD groups per domain'))))
    lines.append(R(merge(bMid(L1, R1, 'Viewer: read-only dashboard'), bMid(L2, R2, 'NSX: per-domain roles'))))
    lines.append(R(merge(bMid(L1, R1, 'SSO: AD-integrated login'), bMid(L2, R2, 'No cross-domain access'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SDDC Manager roles control VCF platform ops; domain RBAC controls workload access.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Credential Management'), bMid(L2, R2, 'Audit & Compliance'))))
    lines.append(R(merge(bMid(L1, R1, 'SDDC Mgr: rotate passwords'), bMid(L2, R2, 'Log: all SDDC Mgr events'))))
    lines.append(R(merge(bMid(L1, R1, 'Service accounts: managed'), bMid(L2, R2, 'Review admin list qtrly'))))
    lines.append(R(merge(bMid(L1, R1, 'Break-glass: local SSO admin'), bMid(L2, R2, 'Alert: failed login SIEM'))))
    lines.append(R(merge(bMid(L1, R1, 'Vault integration: optional'), bMid(L2, R2, 'SDDC Mgr audit log: API'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SDDC Manager runs on management domain; AD must be reachable on management network'))
    lines.append(txt_row('for identity-based login; all SDDC Mgr operations are logged.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SDDC Manager Admin= full platform control; assign to minimal staff'))
    lines.append(txt_row('Operator role= manage domains/clusters; cannot change VCF config'))
    lines.append(txt_row('Viewer role   = read-only; safe for monitoring teams'))
    lines.append(txt_row('AD integration= SDDC Mgr authenticates against AD via LDAP'))
    lines.append(txt_row('Break-glass   = local admin account; used when AD is unreachable'))
    lines.append(txt_row('Credential rotation= SDDC Mgr rotates service account passwords automatically'))
    lines.append(txt_row('Vault integration= optional HashiCorp Vault for credential storage'))
    lines.append(txt_row('SIEM          = receives SDDC Mgr syslog and vCenter events'))
    lines.append(txt_row('Audit API     = SDDC Mgr REST API /v1/audit-events endpoint'))
    lines.append(txt_row('Quarterly review= verify admin role assignments across all domains'))
    lines.append(txt_row('No cross-domain= workload domain RBAC is isolated per domain'))
    lines.append(txt_row('Service accounts= SDDC Mgr manages all component service credentials'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-sec-auth',
    'docs/virtualization/vmware/vmware-cloud-foundation/security/authentication/index.md',
    'VMware Cloud Foundation — Authentication',
)
def vcf_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Cloud Foundation — Authentication'))
    lines.append(txt_row())
    lines.append(txt_row('VCF authentication flows through SDDC Manager (API token), vCenter SSO (per domain),'))
    lines.append(txt_row('and NSX; vIDM provides unified identity across all VCF components.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'SDDC Manager Auth'), bMid(L2, R2, 'Per-Domain Auth'))))
    lines.append(R(merge(bMid(L1, R1, 'Local users + AD groups'), bMid(L2, R2, 'Each domain: own vCenter SSO'))))
    lines.append(R(merge(bMid(L1, R1, 'API: POST /v1/tokens'), bMid(L2, R2, 'AD joined per domain'))))
    lines.append(R(merge(bMid(L1, R1, 'Bearer token: 24h TTL'), bMid(L2, R2, 'SSO: local + AD identity'))))
    lines.append(R(merge(bMid(L1, R1, 'MFA: via RADIUS proxy'), bMid(L2, R2, 'vIDM: optional unified SSO'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SDDC Manager token auth is separate from each domain SSO; both may need AD.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'vIDM Integration'), bMid(L2, R2, 'NSX Authentication'))))
    lines.append(R(merge(bMid(L1, R1, 'Unified identity across VCF'), bMid(L2, R2, 'NSX: local + vIDM/LDAP'))))
    lines.append(R(merge(bMid(L1, R1, 'SAML federation to Aria'), bMid(L2, R2, 'NSX token: 24h expiry'))))
    lines.append(R(merge(bMid(L1, R1, 'AD: one source per vIDM'), bMid(L2, R2, 'NSX API: Bearer token'))))
    lines.append(R(merge(bMid(L1, R1, 'MFA: per vIDM policy'), bMid(L2, R2, 'NSX UI: SSO via vCenter'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AD DCs must be reachable on management network; vIDM requires TCP 443 to AD and'))
    lines.append(txt_row('all VCF components; RADIUS server required for MFA.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vIDM         = VMware Identity Manager; unified SSO across VCF'))
    lines.append(txt_row('SDDC Mgr token= bearer JWT; 24h TTL; POST /v1/tokens'))
    lines.append(txt_row('SAML         = Security Assertion Markup Language; federation format'))
    lines.append(txt_row('vCenter SSO  = per-domain identity service; issues SAML tokens'))
    lines.append(txt_row('RADIUS       = Remote Authentication Dial-In User Service; MFA backend'))
    lines.append(txt_row('Bearer token = JWT presented in Authorization header for API calls'))
    lines.append(txt_row('AD joined    = vCenter SSO configured with AD as identity source'))
    lines.append(txt_row('NSX token    = separate API token; 24h TTL; POST to NSX manager'))
    lines.append(txt_row('MFA          = Multi-Factor Auth; enforced via vIDM or RADIUS policy'))
    lines.append(txt_row('TTL          = Token Time-to-Live; renew before expiry for automation'))
    lines.append(txt_row('NSX SSO      = NSX UI login via vCenter SSO delegation'))
    lines.append(txt_row('SAML to Aria = vIDM provides SAML assertions to Aria Operations/Logs'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-sec-enc',
    'docs/virtualization/vmware/vmware-cloud-foundation/security/encryption/index.md',
    'VMware Cloud Foundation — Encryption',
)
def vcf_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Cloud Foundation — Encryption'))
    lines.append(txt_row())
    lines.append(txt_row('VCF encryption covers transport (TLS 1.2+), vSAN at-rest encryption, VM encryption,'))
    lines.append(txt_row('and SDDC Manager credential vault; all keys via external KMS.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Transport Encryption'), bMid(L2, R2, 'vSAN Encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'All APIs: TLS 1.2+ enforced'), bMid(L2, R2, 'Cluster-level AES-256'))))
    lines.append(R(merge(bMid(L1, R1, 'NSX: TLS between components'), bMid(L2, R2, 'KMS: KMIP protocol'))))
    lines.append(R(merge(bMid(L1, R1, 'SDDC Mgr: TLS to all VCF'), bMid(L2, R2, 'DEK/KEK hierarchy'))))
    lines.append(R(merge(bMid(L1, R1, 'Backup: encrypted SFTP'), bMid(L2, R2, 'Re-key: rolling no outage'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Transport protects management plane; vSAN encryption protects data at rest.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Certificate Management'), bMid(L2, R2, 'SDDC Manager Vault'))))
    lines.append(R(merge(bMid(L1, R1, 'SDDC Mgr: rotate all certs'), bMid(L2, R2, 'Service passwords: encrypted'))))
    lines.append(R(merge(bMid(L1, R1, 'Custom CA: enterprise PKI'), bMid(L2, R2, 'SDDC DB: AES encrypted'))))
    lines.append(R(merge(bMid(L1, R1, 'VMCA: default per domain'), bMid(L2, R2, 'Optional: HashiCorp Vault'))))
    lines.append(R(merge(bMid(L1, R1, 'Expiry: 30d alert in SDDC Mgr'), bMid(L2, R2, 'Master key: admin password'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('KMS must be highly available on management network; SDDC Manager DB encryption'))
    lines.append(txt_row('key is derived from the admin password — protect and rotate it.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('TLS 1.2+     = minimum transport security for all VCF APIs'))
    lines.append(txt_row('vSAN enc     = cluster-level AES-256 encryption of all disk data'))
    lines.append(txt_row('KMS          = Key Management Server; KMIP protocol; holds KEKs'))
    lines.append(txt_row('KMIP         = Key Management Interoperability Protocol; port 5696'))
    lines.append(txt_row('DEK          = Data Encryption Key; per disk group'))
    lines.append(txt_row('KEK          = Key Encryption Key; from KMS; wraps DEKs'))
    lines.append(txt_row('Re-key       = rotate KEK without downtime; new KEK wraps existing DEKs'))
    lines.append(txt_row('SDDC vault   = encrypted store for all component service passwords'))
    lines.append(txt_row('VMCA         = vSphere Certificate Authority; per-domain default CA'))
    lines.append(txt_row('Custom CA    = replace VMCA with enterprise PKI via SDDC Mgr'))
    lines.append(txt_row('HashiCorp Vault= optional external credential store for SDDC Mgr'))
    lines.append(txt_row('Master key   = SDDC Mgr DB encryption; derived from admin password'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-sec-hard',
    'docs/virtualization/vmware/vmware-cloud-foundation/security/hardening/index.md',
    'VMware Cloud Foundation — Hardening',
)
def vcf_sec_hard():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Cloud Foundation — Hardening'))
    lines.append(txt_row())
    lines.append(txt_row('VCF hardening follows the VMware Security Hardening Guide and VCF Security Config;'))
    lines.append(txt_row('applies to all layers: SDDC Manager, vCenter, NSX, vSAN, and ESXi hosts.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Platform Hardening'), bMid(L2, R2, 'Network Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'FIPS 140-2: enable all layers'), bMid(L2, R2, 'Mgmt VLAN: isolated'))))
    lines.append(R(merge(bMid(L1, R1, 'MFA: all admin accounts'), bMid(L2, R2, 'NSX firewall: default deny'))))
    lines.append(R(merge(bMid(L1, R1, 'TLS 1.2+: all components'), bMid(L2, R2, 'vSAN VLAN: dedicated'))))
    lines.append(R(merge(bMid(L1, R1, 'Patch: 30-day SLA'), bMid(L2, R2, 'No direct VM to mgmt'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('FIPS mode and MFA are the highest-value controls across the VCF stack.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'ESXi Host Hardening'), bMid(L2, R2, 'Audit & Compliance'))))
    lines.append(R(merge(bMid(L1, R1, 'Lockdown mode: all hosts'), bMid(L2, R2, 'CIS vSphere benchmark'))))
    lines.append(R(merge(bMid(L1, R1, 'SSH: off by default'), bMid(L2, R2, 'SIEM: all events forwarded'))))
    lines.append(R(merge(bMid(L1, R1, 'Shell: time-limited access'), bMid(L2, R2, 'Quarterly: role review'))))
    lines.append(R(merge(bMid(L1, R1, 'vLCM: enforce baseline images'), bMid(L2, R2, 'SDDC Mgr: audit API'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Physical rack access controls, OOB (iDRAC/iLO) credential rotation, and BIOS'))
    lines.append(txt_row('Secure Boot are essential complements to VCF software hardening.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('FIPS 140-2   = federal crypto standard; enable across all VCF layers'))
    lines.append(txt_row('MFA          = Multi-Factor Authentication; required for all admin logins'))
    lines.append(txt_row('Lockdown mode= ESXi blocks direct access; all ops via vCenter'))
    lines.append(txt_row('vLCM         = vSphere Lifecycle Manager; baseline images for ESXi'))
    lines.append(txt_row('Default deny = NSX distributed firewall default posture'))
    lines.append(txt_row('CIS benchmark= Center for Internet Security vSphere hardening guide'))
    lines.append(txt_row('SIEM         = Security Information and Event Mgmt; log aggregation'))
    lines.append(txt_row('OOB          = Out-of-Band management (iDRAC/iLO); physical host control'))
    lines.append(txt_row('Secure Boot  = BIOS/UEFI feature; validates ESXi bootloader integrity'))
    lines.append(txt_row('Audit API    = SDDC Mgr /v1/audit-events; all platform changes logged'))
    lines.append(txt_row('Patch SLA    = critical <7d, high <30d, medium <90d across all layers'))
    lines.append(txt_row('Baseline image= vLCM image that all ESXi hosts must match'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-ts-common',
    'docs/virtualization/vmware/vmware-cloud-foundation/troubleshooting/common-issues/index.md',
    'VMware Cloud Foundation — Common Issues',
)
def vcf_ts_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Cloud Foundation — Common Issues'))
    lines.append(txt_row())
    lines.append(txt_row('Common VCF issues: upgrade task failures, credential rotation stuck, domain'))
    lines.append(txt_row('commission failures, certificate expiry, and SDDC Manager service outages.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Upgrade Task Failures'), bMid(L2, R2, 'Credential Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'Pre-check fails: fix first'), bMid(L2, R2, 'Rotation stuck: check logs'))))
    lines.append(R(merge(bMid(L1, R1, 'Upgrade paused: check task'), bMid(L2, R2, 'Service account locked out'))))
    lines.append(R(merge(bMid(L1, R1, 'Remediate: retry failed step'), bMid(L2, R2, 'Fix: unlock in AD + retry'))))
    lines.append(R(merge(bMid(L1, R1, 'Rollback: snapshot (if taken)'), bMid(L2, R2, 'Manual rotation: PowerVCF'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Pre-check failures must be resolved before applying any upgrade bundle.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Commission & Domain Issues'), bMid(L2, R2, 'SDDC Manager Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'Host commission fails: DNS'), bMid(L2, R2, 'UI unreachable: check svc'))))
    lines.append(R(merge(bMid(L1, R1, 'Domain create stuck: check tasks'), bMid(L2, R2, 'Restart: service-control'))))
    lines.append(R(merge(bMid(L1, R1, 'Cert error: renew via SDDC Mgr'), bMid(L2, R2, 'DB issue: check Postgres'))))
    lines.append(R(merge(bMid(L1, R1, 'VCF HCL: hardware not listed'), bMid(L2, R2, 'Disk full: purge old logs'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Most VCF failures trace to DNS, NTP, network connectivity, or certificate expiry;'))
    lines.append(txt_row('check all four before raising a GSS SR.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Pre-check     = automated validation; fixes required before upgrade'))
    lines.append(txt_row('Remediate     = retry a failed upgrade task step in SDDC Mgr'))
    lines.append(txt_row('Rollback      = restore snapshot taken before upgrade attempt'))
    lines.append(txt_row('Credential rotation= SDDC Mgr updates service passwords; may time out'))
    lines.append(txt_row('Commission    = add host to free pool; requires DNS + HCL validation'))
    lines.append(txt_row('VCF HCL       = VCF-specific HCL; server + NIC + disk must all be listed'))
    lines.append(txt_row('service-control= restart SDDC Manager services on appliance shell'))
    lines.append(txt_row('Postgres      = SDDC Manager embedded DB; full = service crash'))
    lines.append(txt_row('Log purge     = delete old SDDC Mgr logs when disk >80%'))
    lines.append(txt_row('DNS failure   = most common commission failure; check A + PTR'))
    lines.append(txt_row('Task view     = SDDC Mgr Inventory > Tasks; shows stuck operations'))
    lines.append(txt_row('Cert expiry   = check SDDC Mgr Certificates tab; renew >30d ahead'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-ts-diag',
    'docs/virtualization/vmware/vmware-cloud-foundation/troubleshooting/diagnostics/index.md',
    'VMware Cloud Foundation — Diagnostics',
)
def vcf_ts_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Cloud Foundation — Diagnostics'))
    lines.append(txt_row())
    lines.append(txt_row('VCF diagnostics use SDDC Manager task logs, SOS utility, component logs, and'))
    lines.append(txt_row('health reports to identify root causes across all VCF layers.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'SDDC Manager Logs'), bMid(L2, R2, 'SOS Utility'))))
    lines.append(R(merge(bMid(L1, R1, '/var/log/vmware/vcf/'), bMid(L2, R2, 'python3 sos.py --version'))))
    lines.append(R(merge(bMid(L1, R1, 'operationsmanager.log'), bMid(L2, R2, 'sos.py --collect-dc-logs'))))
    lines.append(R(merge(bMid(L1, R1, 'upgrades.log: LCM detail'), bMid(L2, R2, 'SOS: all component bundles'))))
    lines.append(R(merge(bMid(L1, R1, 'Tasks API: get failed tasks'), bMid(L2, R2, 'Send ZIP to GSS'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SOS utility generates a comprehensive bundle across all VCF components.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Component Diagnostics'), bMid(L2, R2, 'Health Reports'))))
    lines.append(R(merge(bMid(L1, R1, 'vCenter: vc-support.sh'), bMid(L2, R2, 'Invoke-VcfHealthReport'))))
    lines.append(R(merge(bMid(L1, R1, 'NSX: /api/v1/node/logs'), bMid(L2, R2, 'SDDC Mgr: health dashboard'))))
    lines.append(R(merge(bMid(L1, R1, 'ESXi: vm-support bundle'), bMid(L2, R2, 'PowerVCF: Get-VCFTask'))))
    lines.append(R(merge(bMid(L1, R1, 'vSAN: esxcli vsan debug'), bMid(L2, R2, 'HTML report: all domains'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Diagnostic access requires SSH to SDDC Manager appliance and each component;'))
    lines.append(txt_row('SOS utility must be run as root on SDDC Manager.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SOS utility   = VCF diagnostic bundle collector; /opt/vmware/sddc-support'))
    lines.append(txt_row('operationsmanager= SDDC Mgr main service log; task and API operations'))
    lines.append(txt_row('upgrades.log  = LCM upgrade details; step-by-step progress'))
    lines.append(txt_row('Tasks API     = GET /v1/tasks; list failed/running tasks with errors'))
    lines.append(txt_row('vc-support.sh = vCenter support bundle; run on VCSA appliance'))
    lines.append(txt_row('NSX node logs = REST API to retrieve NSX manager diagnostic logs'))
    lines.append(txt_row('vm-support    = ESXi diagnostic bundle; run on host shell'))
    lines.append(txt_row('esxcli vsan   = vSAN diagnostic commands on ESXi host'))
    lines.append(txt_row('Health report = HTML; generated by VMware.CloudFoundation.Reporting'))
    lines.append(txt_row('Get-VCFTask   = PowerVCF; poll task status and retrieve error details'))
    lines.append(txt_row('/var/log/vmware= SDDC Mgr log root; multiple component subdirectories'))
    lines.append(txt_row('Root access   = SOS requires root; access via sudo after SSH'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'vcf-ts-esc',
    'docs/virtualization/vmware/vmware-cloud-foundation/troubleshooting/escalation/index.md',
    'VMware Cloud Foundation — Escalation',
)
def vcf_ts_esc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Cloud Foundation — Escalation'))
    lines.append(txt_row())
    lines.append(txt_row('Escalate VCF issues to VMware GSS when upgrade is stuck, data is at risk,'))
    lines.append(txt_row('or SDDC Manager is inaccessible; attach SOS bundle and timeline.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Escalation Triggers'), bMid(L2, R2, 'Pre-Escalation Steps'))))
    lines.append(R(merge(bMid(L1, R1, 'SDDC Mgr inaccessible'), bMid(L2, R2, 'Run SOS utility'))))
    lines.append(R(merge(bMid(L1, R1, 'Upgrade stuck >4h'), bMid(L2, R2, 'Collect component bundles'))))
    lines.append(R(merge(bMid(L1, R1, 'Data at risk: vSAN degraded'), bMid(L2, R2, 'Document failed task ID'))))
    lines.append(R(merge(bMid(L1, R1, 'All self-steps exhausted'), bMid(L2, R2, 'Timeline of changes'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SOS bundle and task IDs allow GSS to quickly triage the failure point.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'GSS Engagement'), bMid(L2, R2, 'Escalation Path'))))
    lines.append(R(merge(bMid(L1, R1, 'Open SR at support.broadcom'), bMid(L2, R2, 'T1: triage + SOS'))))
    lines.append(R(merge(bMid(L1, R1, 'Severity P1: full outage'), bMid(L2, R2, 'T2: VCF SE assigned'))))
    lines.append(R(merge(bMid(L1, R1, 'Include VCF version + build'), bMid(L2, R2, 'T3: engineering review'))))
    lines.append(R(merge(bMid(L1, R1, 'Attach SOS ZIP'), bMid(L2, R2, 'CritSit: 24/7 if data at risk'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('GSS may request live SSH session to SDDC Manager and component appliances;'))
    lines.append(txt_row('prepare access for remote engineers before the call.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SOS utility   = VCF support bundle; /opt/vmware/sddc-support/sos'))
    lines.append(txt_row('SR            = Service Request; raise at support.broadcom.com'))
    lines.append(txt_row('Task ID       = SDDC Mgr async operation ID; include in SR'))
    lines.append(txt_row('P1 severity   = highest priority; production outage; 24/7 SLA'))
    lines.append(txt_row('CritSit       = Critical Situation; exec escalation + war room'))
    lines.append(txt_row('VCF version   = e.g., VCF 5.2.0.0 build 12345678'))
    lines.append(txt_row('T2 VCF SE     = VMware senior engineer specialising in VCF'))
    lines.append(txt_row('Timeline      = chronological list of changes before issue'))
    lines.append(txt_row('Broadcom      = VMware support portal post-acquisition'))
    lines.append(txt_row('Live SSH      = GSS remote debug via Bomgar or WebEx'))
    lines.append(txt_row('Do not remediate= stop retrying stuck upgrades; wait for GSS guidance'))
    lines.append(txt_row('Component bundle= per-product logs (VC/NSX/ESXi) for targeted debug'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines
