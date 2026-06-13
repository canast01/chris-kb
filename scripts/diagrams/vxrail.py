"""
VxRail diagram functions.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)

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
