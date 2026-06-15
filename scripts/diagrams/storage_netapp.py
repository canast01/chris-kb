"""
NetApp storage sub-product diagram functions (Keystone, ONTAP, Operations, SnapCenter, SnapMirror).
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)


@kb_diagram(
    'netapp-keystone',
    'docs/storage/netapp/keystone/index.md',
    'NetApp Keystone — STaaS subscription model, service levels, consumption billing',
)
def netapp_keystone():
    """NetApp Keystone — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NetApp Keystone'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'NetApp Keystone: Storage-as-a-Service; on-prem hardware; subscription billing')))
    lines.append(R(bMid(IV_L, IV_R, 'Service tiers: Extreme, Premium, Standard, Value — mapped to performance SLOs')))
    lines.append(R(bMid(IV_L, IV_R, 'Managed by NetApp Keystone Success Manager; hardware installed at customer site')))
    lines.append(R(bMid(IV_L, IV_R, 'Billing: committed capacity + burst; monthly invoicing via Active IQ Digital Advisor')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Customer orders -> NetApp installs ONTAP hardware -> consume file/block/object storage'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Service Levels'), bMid(B2_L, B2_R, 'Management'), bMid(B3_L, B3_R, 'Protocols'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Extreme (NVMe)'), bMid(B2_L, B2_R, 'Active IQ DA'), bMid(B3_L, B3_R, 'NFS v3/v4'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Premium (SSD)'), bMid(B2_L, B2_R, 'Keystone Portal'), bMid(B3_L, B3_R, 'SMB 2/3'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Standard (SSD)'), bMid(B2_L, B2_R, 'Success Mgr'), bMid(B3_L, B3_R, 'iSCSI'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Value (HDD)'), bMid(B2_L, B2_R, 'REST API'), bMid(B3_L, B3_R, 'FC'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Burst headroom'), bMid(B2_L, B2_R, 'AutoSupport'), bMid(B3_L, B3_R, 'S3 object'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  NetApp owns hardware; customer owns data and workloads'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Layer', 'Function', 'Owner', 'Tool', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Hardware', 'ONTAP arrays', 'NetApp', 'Field svc.', 'On-prem'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Management', 'Portal/API', 'Customer', 'Active IQ DA', 'Cloud SaaS'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Monitoring', 'Health/perf', 'Shared', 'AutoSupport', 'Via KSM'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Billing', 'Usage report', 'NetApp', 'Keystone UI', 'Monthly'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: NetApp AFF/FAS nodes on-premises · customer network switches · 10/25 GbE or FC'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Keystone STaaS    = Storage as a Service from NetApp; on-prem hardware, cloud billing'))
    lines.append(txt_row('  Active IQ DA      = Digital Advisor; portal for capacity, usage, billing, and health'))
    lines.append(txt_row('  KSM               = Keystone Success Manager; NetApp point of contact for the service'))
    lines.append(txt_row('  Service level     = Predefined performance tier: Extreme/Premium/Standard/Value'))
    lines.append(txt_row('  Committed cap.    = Minimum capacity contracted; billed monthly regardless of use'))
    lines.append(txt_row('  Burst capacity    = Excess above committed; billed at burst rate per TB per month'))
    lines.append(txt_row('  AFF               = All Flash FAS; NetApp all-NVMe or all-SSD ONTAP storage arrays'))
    lines.append(txt_row('  FAS               = Fabric-Attached Storage; hybrid HDD/SSD ONTAP arrays'))
    lines.append(txt_row('  AutoSupport       = Telemetry agent; sends diagnostics from ONTAP to NetApp support'))
    lines.append(txt_row('  SVM               = Storage Virtual Machine; ONTAP multi-tenancy namespace unit'))
    lines.append(txt_row('  Aggregate         = RAID group of disks in ONTAP; FlexVols and FlexGroups reside here'))
    lines.append(txt_row('  FlexVol           = Traditional ONTAP volume; thin-provisioned within an aggregate'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


def netapp_keystone_arch():
    """NetApp Keystone Architecture — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NetApp Keystone — Architecture'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Architecture: ONTAP cluster + Keystone Collector VM + Active IQ management plane')))
    lines.append(R(bMid(IV_L, IV_R, 'Keystone Collector: Linux VM; gathers usage metrics; uploads to Active IQ portal')))
    lines.append(R(bMid(IV_L, IV_R, 'ONTAP cluster: AFF/FAS nodes in HA pair; manages SVMs, aggregates, volumes')))
    lines.append(R(bMid(IV_L, IV_R, 'Network: in-band data NFS/SMB/iSCSI/FC + out-of-band mgmt HTTPS/AutoSupport')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  ONTAP cluster -> Keystone Collector -> Active IQ portal -> billing engine -> invoice'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Storage Layer'), bMid(B2_L, B2_R, 'Collection Layer'), bMid(B3_L, B3_R, 'Management Layer'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'AFF/FAS nodes'), bMid(B2_L, B2_R, 'Keystone Coll.'), bMid(B3_L, B3_R, 'Active IQ DA'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'HA pair (2 ctrl)'), bMid(B2_L, B2_R, 'Linux VM'), bMid(B3_L, B3_R, 'Keystone Portal'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ONTAP OS'), bMid(B2_L, B2_R, 'HTTPS upload'), bMid(B3_L, B3_R, 'Billing engine'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SVMs/volumes'), bMid(B2_L, B2_R, 'Capacity metrics'), bMid(B3_L, B3_R, 'AutoSupport'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NFS/SMB/iSCSI'), bMid(B2_L, B2_R, 'Perf counters'), bMid(B3_L, B3_R, 'REST API'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Data path: host <-> ONTAP data LIFs; mgmt: ONTAP mgmt LIF -> Keystone Collector VM'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Component', 'Role', 'Protocol', 'Placement', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['AFF node', 'Storage', 'NFS/FC/iSCSI', 'On-prem rack', 'HA pair'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['KS Collector', 'Metrics', 'HTTPS/REST', 'Customer VM', 'Sends to cloud'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Active IQ', 'Portal/bill', 'HTTPS', 'NetApp cloud', 'SaaS'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['AutoSupport', 'Diagnostics', 'HTTPS/SMTP', 'ONTAP built-in', 'To NetApp'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: AFF/FAS 2U/4U shelves in rack · 10/25/100 GbE data NICs · FC 16/32Gb HBAs'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Keystone Collector = Linux VM on-prem; polls ONTAP REST API; uploads usage to cloud'))
    lines.append(txt_row('  Active IQ DA       = Digital Advisor; cloud portal for capacity, billing, health'))
    lines.append(txt_row('  HA pair            = Two ONTAP nodes sharing disk shelves; automatic failover'))
    lines.append(txt_row('  SVM                = Storage VM; isolated namespace with LIFs, volumes, protocols'))
    lines.append(txt_row('  Data LIF           = Logical Interface for data traffic; bound to port/VLAN'))
    lines.append(txt_row('  Mgmt LIF           = Management Logical Interface; SSH/REST/ONTAP API access'))
    lines.append(txt_row('  Aggregate          = RAID group container; FlexVols and FlexGroups provisioned here'))
    lines.append(txt_row('  AutoSupport        = Built-in ONTAP telemetry; sends support bundles to NetApp'))
    lines.append(txt_row('  REST API           = ONTAP 9.6+ native REST API; used by Keystone Collector'))
    lines.append(txt_row('  ZAPI               = Legacy ONTAP API (pre-REST); still used by older tools'))
    lines.append(txt_row('  ONTAP Mediator     = VM providing quorum for MetroCluster/SnapMirror SM-BC'))
    lines.append(txt_row('  NVMe/FC            = Non-Volatile Memory Express over Fibre Channel; <100 us latency'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'netapp-keystone-arch-standards',
    'docs/storage/netapp/keystone/architecture/design-standards/index.md',
    'Keystone Architecture Design Standards — service level mapping, network, HA, sizing',
)
def netapp_keystone_arch_standards():
    """NetApp Keystone Architecture Design Standards — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NetApp Keystone — Architecture Design Standards'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Design standards: service level -> hardware, network redundancy, sizing, burst')))
    lines.append(R(bMid(IV_L, IV_R, 'Extreme: AFF A-series NVMe; <1ms latency; 10k+ IOPS/TB committed throughput')))
    lines.append(R(bMid(IV_L, IV_R, 'Network: dedicated NFS/iSCSI VLAN MTU 9000; dual FC; separate mgmt VLAN')))
    lines.append(R(bMid(IV_L, IV_R, 'HA: dual-node ONTAP cluster; storage failover within 60 s; SFO/CFO policy')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Workload SLO -> tier -> NW design -> multipath -> committed sizing -> burst budget'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Tier Standards'), bMid(B2_L, B2_R, 'Network Design'), bMid(B3_L, B3_R, 'HA & Sizing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Extreme: NVMe'), bMid(B2_L, B2_R, 'Dedicated VLAN'), bMid(B3_L, B3_R, 'Dual node HA'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Premium: AFF SSD'), bMid(B2_L, B2_R, 'MTU 9000 NFS'), bMid(B3_L, B3_R, 'SFO 60 s RTO'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Standard: SSD'), bMid(B2_L, B2_R, 'Dual FC fabric'), bMid(B3_L, B3_R, 'MPIO 4+ paths'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Value: HDD'), bMid(B2_L, B2_R, 'OOB mgmt VLAN'), bMid(B3_L, B3_R, 'Commit 70-80%'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Burst 20% extra'), bMid(B2_L, B2_R, 'IPMI/BMC OOB'), bMid(B3_L, B3_R, 'Burst alert 90%'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Commit 70-80% of expected peak; burst rate covers spikes; review quarterly with KSM'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Area', 'Standard', 'Why', 'Verify', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['NFS MTU', '9000 jumbo', 'Throughput', 'ping -s 8972', 'End-to-end'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Multipath', 'ALUA/MPIO', '4 paths', 'sanlun show', 'FC/iSCSI'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Committed', '70-80% peak', 'Cost ctl', 'Active IQ', 'Quarterly'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Burst alert', '90% of burst', 'Avoid fees', 'Alert rule', 'Auto notify'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: AFF/FAS nodes in rack · dual 10/25 GbE per node · 16/32Gb HBAs for FC'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SFO      = Storage Failover; ONTAP HA takeover of partner node storage in <60 s'))
    lines.append(txt_row('  CFO      = Controller Failover; faster variant; non-disruptive LIF failover'))
    lines.append(txt_row('  MPIO     = Multipath I/O; OS driver balancing I/O across multiple HBA/NIC paths'))
    lines.append(txt_row('  ALUA     = Asymmetric Logical Unit Access; preferred vs non-preferred path hints'))
    lines.append(txt_row('  MTU 9000 = Jumbo frames for NFS/iSCSI; requires end-to-end switch config'))
    lines.append(txt_row('  Burst    = Capacity above committed level; billed at premium burst rate'))
    lines.append(txt_row('  KSM      = Keystone Success Manager; NetApp advisor for capacity planning'))
    lines.append(txt_row('  BMC      = Baseboard Management Controller; OOB access for remote power/console'))
    lines.append(txt_row('  IPMI     = Intelligent Platform Management Interface; OOB management standard'))
    lines.append(txt_row('  NVMe-oF  = NVMe over Fabrics (FC or TCP); <100 us block latency'))
    lines.append(txt_row('  AFF A    = AFF A-series; all-NVMe flash; highest performance tier'))
    lines.append(txt_row('  AFF C    = AFF C-series; capacity-optimised all-flash; QLC NAND'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'netapp-keystone-arch-how',
    'docs/storage/netapp/keystone/architecture/how-it-works/index.md',
    'Keystone How It Works — collector polling, metric upload, billing computation',
)
def netapp_keystone_arch_how():
    """NetApp Keystone Architecture How It Works — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NetApp Keystone — How It Works'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Keystone Collector VM polls ONTAP REST API every 5 min; aggregates capacity')))
    lines.append(R(bMid(IV_L, IV_R, 'Metrics compressed and uploaded to Active IQ via HTTPS/TLS to cloud endpoint')))
    lines.append(R(bMid(IV_L, IV_R, 'Billing engine computes committed + burst consumed; monthly invoice generated')))
    lines.append(R(bMid(IV_L, IV_R, 'Customer views usage in Active IQ Digital Advisor; exports CSV for finance')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  ONTAP REST poll -> Collector aggregates -> HTTPS upload -> IQ billing -> invoice'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Collection'), bMid(B2_L, B2_R, 'Upload'), bMid(B3_L, B3_R, 'Billing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'REST API poll'), bMid(B2_L, B2_R, 'HTTPS/TLS'), bMid(B3_L, B3_R, 'Committed calc'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Every 5 min'), bMid(B2_L, B2_R, 'Compressed JSON'), bMid(B3_L, B3_R, 'Burst calc'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Volume capacity'), bMid(B2_L, B2_R, 'IQ endpoint'), bMid(B3_L, B3_R, 'Monthly invoice'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Perf counters'), bMid(B2_L, B2_R, 'Retry on fail'), bMid(B3_L, B3_R, 'CSV export'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SVM metadata'), bMid(B2_L, B2_R, 'Proxy support'), bMid(B3_L, B3_R, 'Usage charts'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Collector must reach ONTAP mgmt LIF on 443 and Active IQ cloud endpoint on 443'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Step', 'Action', 'Frequency', 'Outcome', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Poll', 'REST API call', '5 min', 'Raw metrics', 'Per SVM'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Aggregate', 'Summarise', 'Per poll', 'JSON bundle', 'Compressed'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Upload', 'HTTPS to IQ', 'Per cycle', 'Cloud stored', 'TLS 1.2+'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Bill', 'Compute cost', 'Monthly', 'Invoice PDF', 'Burst extra'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: Collector VM 2 vCPU 8 GB RAM needs outbound TCP 443 to cloud'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Keystone Collector = Linux VM; polls ONTAP and ships metrics to Active IQ'))
    lines.append(txt_row('  ONTAP REST API     = Native JSON/HTTPS API (v9.6+); replaces legacy ZAPI'))
    lines.append(txt_row('  Active IQ          = NetApp cloud analytics; stores metrics; computes billing'))
    lines.append(txt_row('  Committed cap.     = Baseline TB contracted; billed at flat rate monthly'))
    lines.append(txt_row('  Burst cap.         = TB used above committed; billed at higher per-TB rate'))
    lines.append(txt_row('  Service level SLO  = Max latency + min IOPS/TB guaranteed per tier'))
    lines.append(txt_row('  SVM                = Storage VM; ONTAP tenancy unit; polled individually'))
    lines.append(txt_row('  JSON bundle        = Compressed payload Collector uploads: volumes, capacity, perf'))
    lines.append(txt_row('  Proxy support      = Collector can route HTTPS uploads via HTTP/SOCKS proxy'))
    lines.append(txt_row('  Retry              = Collector queues failed uploads; retries up to 24 h'))
    lines.append(txt_row('  CSV export         = Active IQ provides usage CSV for chargeback/finance'))
    lines.append(txt_row('  TLS 1.2+           = Minimum encryption standard for all Collector communications'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'netapp-keystone-arch-int',
    'docs/storage/netapp/keystone/architecture/integrations/index.md',
    'Keystone Integrations — Active IQ, ServiceNow, Ansible, BlueXP, monitoring hooks',
)
def netapp_keystone_arch_int():
    """NetApp Keystone Architecture Integrations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NetApp Keystone — Architecture Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Keystone integrations: Active IQ, BlueXP, Ansible ONTAP, ServiceNow, Prometheus')))
    lines.append(R(bMid(IV_L, IV_R, 'BlueXP: unified cloud manager; controls Keystone ordering and capacity changes')))
    lines.append(R(bMid(IV_L, IV_R, 'Ansible NetApp collection: automates SVM, volume, LUN provisioning on ONTAP')))
    lines.append(R(bMid(IV_L, IV_R, 'Prometheus exporter: exposes ONTAP perf metrics; Grafana dashboards for ops')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  ONTAP REST API <- Ansible/Terraform/BlueXP; ONTAP -> Prometheus -> Grafana -> alerts'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cloud Integrations'), bMid(B2_L, B2_R, 'Automation'), bMid(B3_L, B3_R, 'Monitoring'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Active IQ DA'), bMid(B2_L, B2_R, 'Ansible netapp'), bMid(B3_L, B3_R, 'Prometheus'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'BlueXP portal'), bMid(B2_L, B2_R, 'Terraform ONTAP'), bMid(B3_L, B3_R, 'Grafana boards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Keystone UI'), bMid(B2_L, B2_R, 'REST API calls'), bMid(B3_L, B3_R, 'SNMP traps'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'AutoSupport'), bMid(B2_L, B2_R, 'ServiceNow'), bMid(B3_L, B3_R, 'EMS alerts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SR portal'), bMid(B2_L, B2_R, 'Python SDK'), bMid(B3_L, B3_R, 'Syslog export'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  ONTAP REST API is the integration backbone; all modern tools use JSON/HTTPS'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Tool', 'Use Case', 'Protocol', 'Auth', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['BlueXP', 'Capacity order', 'HTTPS', 'OAuth2', 'NetApp cloud'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Ansible', 'Provisioning', 'REST/ZAPI', 'Basic/cert', 'na_ontap_*'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Prometheus', 'Perf metrics', 'HTTP scrape', 'None/token', 'ONTAP exporter'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['ServiceNow', 'ITSM tickets', 'REST webhook', 'OAuth', 'EMS -> SNOW'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: Ansible controller VM · Prometheus server · Grafana in mgmt network'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  BlueXP           = NetApp cloud manager; unified UI for on-prem and cloud storage'))
    lines.append(txt_row('  Ansible na_ontap = NetApp Ansible collection; 200+ modules for ONTAP automation'))
    lines.append(txt_row('  Terraform ONTAP  = NetApp provider for Terraform; declarative ONTAP provisioning'))
    lines.append(txt_row('  Prometheus       = Time-series metrics DB; scrapes ONTAP exporter endpoint'))
    lines.append(txt_row('  EMS              = Event Management System; ONTAP event log and alert engine'))
    lines.append(txt_row('  SNMP trap        = UDP event notification; ONTAP -> monitoring system'))
    lines.append(txt_row('  AutoSupport      = ONTAP built-in support telemetry; HTTPS to support.netapp.com'))
    lines.append(txt_row('  ServiceNow       = ITSM platform; EMS webhooks create incident tickets'))
    lines.append(txt_row('  Python SDK       = netapp-lib / ontap-rest-python; scripting ONTAP REST API'))
    lines.append(txt_row('  Syslog           = ONTAP EMS forwarded to syslog server (Splunk, Graylog, etc.)'))
    lines.append(txt_row('  OAuth2           = Token-based auth for BlueXP and modern REST API clients'))
    lines.append(txt_row('  ZAPI             = Legacy XML-based ONTAP API; deprecated from ONTAP 9.13 onward'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'netapp-keystone-cli',
    'docs/storage/netapp/keystone/cli-reference/index.md',
    'Keystone CLI Reference — ONTAP CLI, Keystone Collector CLI, ActiveIQ commands',
)
def netapp_keystone_cli():
    """NetApp Keystone CLI Reference — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NetApp Keystone — CLI Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CLI interfaces: ONTAP CLI (SSH), Keystone Collector CLI (Linux), Active IQ REST')))
    lines.append(R(bMid(IV_L, IV_R, 'ONTAP CLI: volume show, vserver show, storage aggregate show, net interface show')))
    lines.append(R(bMid(IV_L, IV_R, 'Collector CLI: keystone-collector status, collect, upload, logs, config-check')))
    lines.append(R(bMid(IV_L, IV_R, 'Active IQ REST: GET /v1/keystone/capacity, GET /v1/keystone/billing/invoices')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  SSH to cluster mgmt LIF -> ONTAP CLI; SSH to Collector VM -> collector-manager CLI'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ONTAP CLI'), bMid(B2_L, B2_R, 'Collector CLI'), bMid(B3_L, B3_R, 'Active IQ API'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'volume show'), bMid(B2_L, B2_R, 'ks status'), bMid(B3_L, B3_R, 'GET /capacity'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vserver show'), bMid(B2_L, B2_R, 'ks collect'), bMid(B3_L, B3_R, 'GET /invoices'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'aggr show'), bMid(B2_L, B2_R, 'ks upload'), bMid(B3_L, B3_R, 'GET /billing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'net int show'), bMid(B2_L, B2_R, 'ks logs'), bMid(B3_L, B3_R, 'Auth: Bearer'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'storage disk show'), bMid(B2_L, B2_R, 'ks config-check'), bMid(B3_L, B3_R, 'TLS required'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  ONTAP CLI privilege levels: admin (default), advanced (diag-level commands)'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Command', 'Description', 'Interface', 'Level', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['volume show', 'List volumes', 'ONTAP CLI', 'admin', 'Per SVM'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['aggr show', 'List aggrs', 'ONTAP CLI', 'admin', 'Disk usage'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['ks status', 'Coll. health', 'Collector', 'Linux root', 'Svc status'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['ks upload', 'Force upload', 'Collector', 'Linux root', 'Debug use'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SSH from jump host to cluster mgmt LIF (22/TCP); HTTPS to Active IQ (443)'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  ONTAP CLI          = SSH-based command shell on cluster mgmt LIF; fsm-driven'))
    lines.append(txt_row('  Privilege level    = admin (normal) vs advanced (set -priv advanced); diag for support'))
    lines.append(txt_row('  vserver show       = Lists all SVMs; use -vserver <name> to filter'))
    lines.append(txt_row('  volume show -space = Adds used/available columns; key for Keystone sizing'))
    lines.append(txt_row('  aggr show -space   = Aggregate capacity; Keystone committed is at aggr level'))
    lines.append(txt_row('  ks status          = Keystone Collector service status; checks upload backlog'))
    lines.append(txt_row('  ks collect         = Manually trigger ONTAP REST poll; useful after fix'))
    lines.append(txt_row('  ks upload          = Force metric upload to Active IQ; bypasses schedule'))
    lines.append(txt_row('  ks config-check    = Validates Collector config (API creds, endpoints, proxy)'))
    lines.append(txt_row('  Bearer token       = Active IQ REST auth; retrieved via NetApp SSO login'))
    lines.append(txt_row('  net int show       = Lists all LIFs; confirms data/mgmt LIF status and IP'))
    lines.append(txt_row('  storage disk show  = Physical disk info; checks spares, broken, and RAID groups'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'netapp-keystone-design',
    'docs/storage/netapp/keystone/design-standards/index.md',
    'Keystone Design Standards — capacity planning, QoS policy, tiering, access patterns',
)
def netapp_keystone_design():
    """NetApp Keystone Design Standards — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NetApp Keystone — Design Standards'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Design standards: capacity planning, QoS adaptive policies, FabricPool tiering')))
    lines.append(R(bMid(IV_L, IV_R, 'QoS adaptive: auto-assign IOPS/TB ceiling per service level per volume')))
    lines.append(R(bMid(IV_L, IV_R, 'FabricPool: automatic cold-data tiering to S3/StorageGRID object store')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity: size committed at 70-80% peak; monitor via Active IQ alerts')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Workload profile -> service level -> QoS adaptive policy -> volume + tiering policy'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity Design'), bMid(B2_L, B2_R, 'QoS Design'), bMid(B3_L, B3_R, 'Tiering Design'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Committed 70-80%'), bMid(B2_L, B2_R, 'Adaptive QoS'), bMid(B3_L, B3_R, 'FabricPool'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Burst headroom 20%'), bMid(B2_L, B2_R, 'Min IOPS/TB'), bMid(B3_L, B3_R, 'S3 cloud tier'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Thin provision'), bMid(B2_L, B2_R, 'Max IOPS/TB'), bMid(B3_L, B3_R, 'StorageGRID'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dedup+compress'), bMid(B2_L, B2_R, 'Burst allowance'), bMid(B3_L, B3_R, 'Cold threshold'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Quota policies'), bMid(B2_L, B2_R, 'QoS group'), bMid(B3_L, B3_R, 'Retrieve policy'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Enable dedup+compression on all volumes; typical 2-3x reduction on structured data'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Standard', 'Value', 'Apply When', 'Check', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Dedup', 'Enable all', 'All volumes', 'sis show', '2-3x saving'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Compress', 'Inline+post', 'Block data', 'sis show', 'CPU cost'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Tiering', 'Cold >31 days', 'Capacity vol', 'FP show', 'To S3'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['QoS adaptive', 'Per SL tier', 'All vols', 'qos show', 'Auto-apply'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: AFF local tier + object store bucket (S3/StorageGRID) for FabricPool'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Adaptive QoS     = ONTAP policy that auto-scales IOPS ceiling with volume size'))
    lines.append(txt_row('  FabricPool       = ONTAP feature; automatically moves cold blocks to object tier'))
    lines.append(txt_row('  Tiering policy   = Per-volume: none / snapshot-only / auto / all'))
    lines.append(txt_row('  StorageGRID      = NetApp on-prem S3 object storage; common FabricPool target'))
    lines.append(txt_row('  Dedup            = Inline deduplication; removes duplicate 4KB blocks on write'))
    lines.append(txt_row('  Compression      = Inline or post-process; reduces physical block footprint'))
    lines.append(txt_row('  Thin provisioning= Volume logical size > physical allocation; grows on write'))
    lines.append(txt_row('  Quota policy     = User/group/qtree disk and file count limits in ONTAP'))
    lines.append(txt_row('  sis show         = Storage Inline Storage cmd; shows dedup/compress status'))
    lines.append(txt_row('  qos show         = ONTAP command; lists QoS policies and current IOPS utilisation'))
    lines.append(txt_row('  Cold threshold   = Days of inactivity before FabricPool moves block to object'))
    lines.append(txt_row('  Retrieve policy  = Controls if tiered data read back to SSD (on-demand vs never)'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'netapp-keystone-integration',
    'docs/storage/netapp/keystone/integration/index.md',
    'Keystone Integration — ONTAP with vCenter, VMware, Kubernetes, AWS/Azure',
)
def netapp_keystone_integration():
    """NetApp Keystone Integration — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NetApp Keystone — Integration'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Integrations: VMware (VAAI/VASA), Kubernetes (Trident), AWS/Azure blending')))
    lines.append(R(bMid(IV_L, IV_R, 'VAAI: hardware offload for clone, zero, lock operations from ESXi to ONTAP')))
    lines.append(R(bMid(IV_L, IV_R, 'VASA: Storage Policy-Based Management; maps service levels to VM policies')))
    lines.append(R(bMid(IV_L, IV_R, 'Trident: CSI driver for Kubernetes; dynamic PVC provisioning on ONTAP')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  App -> vSphere/K8s -> VAAI/VASA/Trident -> ONTAP SVM -> aggregate -> physical'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VMware'), bMid(B2_L, B2_R, 'Kubernetes'), bMid(B3_L, B3_R, 'Cloud'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VAAI NAS/SAN'), bMid(B2_L, B2_R, 'Trident CSI'), bMid(B3_L, B3_R, 'Cloud Volumes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VASA provider'), bMid(B2_L, B2_R, 'StorageClass'), bMid(B3_L, B3_R, 'BlueXP hybrid'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SPBM policies'), bMid(B2_L, B2_R, 'PVC dynamic'), bMid(B3_L, B3_R, 'SnapMirror S3'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VVOL datastores'), bMid(B2_L, B2_R, 'NFS/iSCSI PV'), bMid(B3_L, B3_R, 'Backup cloud'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vCenter plugin'), bMid(B2_L, B2_R, 'Astra Control'), bMid(B3_L, B3_R, 'Cloud Sync'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Trident needs ONTAP SVM admin credentials; deploys as DaemonSet in k8s cluster'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Integration', 'Mechanism', 'Protocol', 'Auth', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['VAAI', 'ESXi HW offload', 'NFS/SCSI', 'n/a', 'Vendor plugin'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['VASA', 'Storage policy', 'HTTPS', 'SSL cert', 'vVols capable'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Trident', 'CSI driver', 'REST API', 'SVM creds', 'K8s operator'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['BlueXP', 'Hybrid cloud', 'HTTPS', 'OAuth2', 'Cloud mgmt'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: ESXi hosts connect to ONTAP data LIFs via NFS VLAN or FC fabric'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  VAAI          = vStorage APIs for Array Integration; offloads clone/lock to array'))
    lines.append(txt_row('  VASA          = vSphere APIs for Storage Awareness; storage capability profiles'))
    lines.append(txt_row('  SPBM          = Storage Policy-Based Management; VM tier via vCenter policy'))
    lines.append(txt_row('  vVol          = Virtual Volume; per-VM ONTAP object; VM-level QoS and snapshot'))
    lines.append(txt_row('  Trident       = NetApp CSI driver; creates NFS/iSCSI PVs from ONTAP'))
    lines.append(txt_row('  StorageClass  = Kubernetes resource; maps to Trident backend (SVM + protocol)'))
    lines.append(txt_row('  PVC           = PersistentVolumeClaim; K8s request for storage; Trident fulfils'))
    lines.append(txt_row('  Astra Control = NetApp app-aware backup/DR for Kubernetes workloads'))
    lines.append(txt_row('  Cloud Volumes = ONTAP as managed service on AWS/Azure/GCP (CVO/CVS)'))
    lines.append(txt_row('  BlueXP        = Unified NetApp cloud manager; controls on-prem and cloud ONTAP'))
    lines.append(txt_row('  SnapMirror S3 = Replication to/from S3-compatible targets for data mobility'))
    lines.append(txt_row('  Cloud Sync    = NetApp SaaS data migration/sync; NFS, SMB, S3, HDFS'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'netapp-keystone-lifecycle',
    'docs/storage/netapp/keystone/lifecycle/index.md',
    'Keystone Lifecycle — contract, provisioning, capacity changes, renewal, exit',
)
def netapp_keystone_lifecycle():
    """NetApp Keystone Lifecycle — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NetApp Keystone — Lifecycle'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Keystone lifecycle: contract -> install -> operate -> capacity change -> renew')))
    lines.append(R(bMid(IV_L, IV_R, 'Contract: 1-5 year term; committed TB per service level; burst allowance set')))
    lines.append(R(bMid(IV_L, IV_R, 'Install: NetApp ships AFF/FAS; rack + cable + ONTAP config by NetApp engineer')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity change: add TB via KSM; contract amendment; hardware added if needed')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Contract sign -> install -> operate -> capacity change -> renew or exit'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Pre-Deploy'), bMid(B2_L, B2_R, 'In-Life'), bMid(B3_L, B3_R, 'End of Term'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Contract sign'), bMid(B2_L, B2_R, 'Operations'), bMid(B3_L, B3_R, 'Renewal option'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'HW sizing'), bMid(B2_L, B2_R, 'Capacity review'), bMid(B3_L, B3_R, 'Upgrade term'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Site survey'), bMid(B2_L, B2_R, 'Burst monitoring'), bMid(B3_L, B3_R, 'Exit: data move'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Rack install'), bMid(B2_L, B2_R, 'Capacity add'), bMid(B3_L, B3_R, 'HW return'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ONTAP config'), bMid(B2_L, B2_R, 'ONTAP upgrade'), bMid(B3_L, B3_R, 'Contract close'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Quarterly review with KSM: usage vs committed; plan capacity change before burst'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Phase', 'Action', 'Owner', 'SLA', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Deploy', 'Rack/install', 'NetApp', '30-60 days', 'Site ready req'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Cap add', 'Contract amend', 'KSM', '30 days', 'HW lead time'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['ONTAP upg', 'Patch/upgrade', 'NetApp/cust', 'Scheduled', 'Non-disruptive'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Exit', 'Data migration', 'Customer', 'EOL date', 'HW returned'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: NetApp ships AFF/FAS + disk shelves; customer provides rack/power/cooling'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  KSM                = Keystone Success Manager; lifecycle advisor; quarterly reviews'))
    lines.append(txt_row('  Contract term      = 1, 3, or 5 years; defines committed TB and burst allowance'))
    lines.append(txt_row('  Capacity amendment = Formal change to contract committed TB; requires KSM sign-off'))
    lines.append(txt_row('  Site survey        = Pre-install assessment: rack space, power, cooling, network'))
    lines.append(txt_row('  Non-disruptive upg = ONTAP upgrade without host I/O interruption via rolling'))
    lines.append(txt_row('  Exit plan          = 90-day notice; customer migrates data; NetApp reclaims HW'))
    lines.append(txt_row('  Burst monitoring   = Active IQ alerts at 80%, 90% of burst ceiling'))
    lines.append(txt_row('  ONTAP upgrade      = Cluster rolling upgrade; one node at a time; HA takes over'))
    lines.append(txt_row('  HW return          = Hardware is NetApp property; decommission on contract end'))
    lines.append(txt_row('  SFO                = Storage Failover; HA takeover during ONTAP upgrade cycles'))
    lines.append(txt_row('  Quarterly review   = KSM meets customer; reviews usage, forecasts, adjusts plan'))
    lines.append(txt_row('  HW lead time       = 30-60 days for new AFF/FAS nodes post-amendment'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'netapp-keystone-ops',
    'docs/storage/netapp/keystone/operations/index.md',
    'Keystone Operations — daily ops, capacity review, ONTAP admin, Collector health',
)
def netapp_keystone_ops():
    """NetApp Keystone Operations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NetApp Keystone — Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Operations: daily ONTAP health checks, Collector upload status, capacity review')))
    lines.append(R(bMid(IV_L, IV_R, 'Daily: verify Collector upload, check EMS errors, confirm HA state, node health')))
    lines.append(R(bMid(IV_L, IV_R, 'Weekly: review Active IQ dashboard, burst usage trend, aggregate utilisation')))
    lines.append(R(bMid(IV_L, IV_R, 'Monthly: usage report export, billing reconciliation, ONTAP patch planning')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Daily checks -> weekly trend -> monthly billing -> quarterly KSM -> capacity plan'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Daily Checks'), bMid(B2_L, B2_R, 'Weekly Tasks'), bMid(B3_L, B3_R, 'Monthly Tasks'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Collector upload'), bMid(B2_L, B2_R, 'Active IQ dash'), bMid(B3_L, B3_R, 'Usage report'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'EMS error review'), bMid(B2_L, B2_R, 'Burst trend'), bMid(B3_L, B3_R, 'Billing check'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Node health'), bMid(B2_L, B2_R, 'Aggr utilisation'), bMid(B3_L, B3_R, 'Patch review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'HA state'), bMid(B2_L, B2_R, 'Volume growth'), bMid(B3_L, B3_R, 'QoS review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Disk spares'), bMid(B2_L, B2_R, 'Perf baselines'), bMid(B3_L, B3_R, 'Capacity plan'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Alert thresholds: Collector offline >30 min = P2; aggr >85% = P1; HA fault = P1'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Task', 'Command / Tool', 'Frequency', 'Owner', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['HA check', 'storage failover', 'Daily', 'StorageOps', 'Connected'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Collector', 'ks status', 'Daily', 'StorageOps', 'Upload OK'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Aggr util', 'aggr show', 'Weekly', 'StorageOps', '<85% used'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Billing', 'Active IQ UI', 'Monthly', 'FinanceOps', 'Match invoice'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: ONTAP cluster mgmt LIF accessible from ops jump host; Collector VM same net'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  EMS             = Event Management System; ONTAP internal event/alert log'))
    lines.append(txt_row('  HA state        = storage failover show; nodes must be Connected not Takeover'))
    lines.append(txt_row('  Disk spare      = Unassigned disk; ONTAP uses to replace failed drives auto'))
    lines.append(txt_row('  Aggregate util  = Physical used/total; above 85% risks out-of-space errors'))
    lines.append(txt_row('  Burst trend     = Rate of committed + burst consumption; projected overage'))
    lines.append(txt_row('  Collector status= ks status; connected, last upload <30 min ago'))
    lines.append(txt_row('  QoS review      = Check qos show for IOPS throttling events; adjust if needed'))
    lines.append(txt_row('  Billing recon.  = Compare Active IQ invoice vs internal cost allocation'))
    lines.append(txt_row('  Patch review    = Check NetApp PSIRT advisories; plan ONTAP NDU upgrade window'))
    lines.append(txt_row('  NDU             = Non-Disruptive Upgrade; rolling upgrade without I/O interruption'))
    lines.append(txt_row('  Volume growth   = Track FlexVol/FlexGroup growth rate; predict aggregate fill'))
    lines.append(txt_row('  Perf baseline   = Weekly latency/IOPS averages; compare to service level SLO'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'netapp-keystone-ops-backup',
    'docs/storage/netapp/keystone/operations/backup-restore/index.md',
    'Keystone Backup/Restore — SnapVault, SnapCenter, object backup, restore runbook',
)
def netapp_keystone_ops_backup():
    """NetApp Keystone Operations Backup-Restore — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NetApp Keystone — Operations: Backup & Restore'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Backup: ONTAP Snapshots, SnapVault disk-to-disk, SnapCenter app-consistent')))
    lines.append(R(bMid(IV_L, IV_R, 'Snapshot: instantaneous, space-efficient; RPO minutes; stored in same SVM')))
    lines.append(R(bMid(IV_L, IV_R, 'SnapVault: replicates snapshots to secondary ONTAP; RPO hours; diff cluster')))
    lines.append(R(bMid(IV_L, IV_R, 'Restore: snap restore (volume), snap restore -item (file), SnapCenter clone')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Schedule snapshots -> SnapVault to secondary -> SnapCenter for DB -> restore on demand'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Snapshot'), bMid(B2_L, B2_R, 'SnapVault'), bMid(B3_L, B3_R, 'SnapCenter'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Instant capture'), bMid(B2_L, B2_R, 'Vault policy'), bMid(B3_L, B3_R, 'App plugin'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Space-efficient'), bMid(B2_L, B2_R, 'Secondary vol'), bMid(B3_L, B3_R, 'SQL/Oracle/SAP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Per-volume'), bMid(B2_L, B2_R, 'RPO hours'), bMid(B3_L, B3_R, 'App-consistent'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RPO <5 min'), bMid(B2_L, B2_R, 'Long retention'), bMid(B3_L, B3_R, 'Clone workflow'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Max 255/vol'), bMid(B2_L, B2_R, 'Throttle xfer'), bMid(B3_L, B3_R, 'Report audit'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Test restores quarterly; document RTO targets; validate clone integrity before prod'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Method', 'RPO', 'RTO', 'Retention', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Snapshot', '<5 min', '<1 min', '30-90 days', 'Local only'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['SnapVault', 'Hours', '15-30 min', '1-7 years', 'Secondary'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['SnapCenter', '<1 min', '<5 min', 'Policy-based', 'App consist.'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Object', 'Hours', '30-60 min', 'Years', 'S3/Grid'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: primary AFF cluster + secondary FAS/AFF cluster different rack or site'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  ONTAP Snapshot  = Read-only point-in-time copy; shares blocks with active volume'))
    lines.append(txt_row('  SnapVault       = Disk-to-disk backup replication; vault policy retains snapshots'))
    lines.append(txt_row('  SnapCenter      = NetApp backup server; quiesces apps before snapshot'))
    lines.append(txt_row('  Vault policy    = SnapVault label schedule: hourly/daily/weekly/monthly retention'))
    lines.append(txt_row('  snap restore    = ONTAP CLI: volume snapshot restore; overwrites active volume'))
    lines.append(txt_row('  snap restore -item = Single-file restore from snapshot without rollback'))
    lines.append(txt_row('  Clone           = Writable FlexClone of snapshot; instant; space-efficient'))
    lines.append(txt_row('  RPO             = Recovery Point Objective; max acceptable data loss in time'))
    lines.append(txt_row('  RTO             = Recovery Time Objective; max acceptable downtime for restore'))
    lines.append(txt_row('  App-consistent  = Backup taken with app quiesced (SQL VSS/Oracle RMAN)'))
    lines.append(txt_row('  StorageGRID     = NetApp on-prem S3 object store; long-term vault target'))
    lines.append(txt_row('  FlexClone       = Instant writable clone of volume/snapshot; shares blocks'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'netapp-keystone-ops-cli',
    'docs/storage/netapp/keystone/operations/cli-reference/index.md',
    'Keystone Operations CLI Reference — ONTAP admin commands, Collector, Active IQ API',
)
def netapp_keystone_ops_cli():
    """NetApp Keystone Operations CLI Reference — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'NetApp Keystone — Operations: CLI Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CLI reference: ONTAP admin commands for daily Keystone storage operations')))
    lines.append(R(bMid(IV_L, IV_R, 'Health: storage failover show, system health alert show, disk show -broken')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity: volume show -space, aggr show -space, df -h (NFS from host)')))
    lines.append(R(bMid(IV_L, IV_R, 'Performance: statistics show, qos statistics show, network interface show')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  SSH cluster LIF -> ONTAP CLI; set -priv advanced for extended commands'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Health Commands'), bMid(B2_L, B2_R, 'Capacity Commands'), bMid(B3_L, B3_R, 'Perf Commands'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'storage fail show'), bMid(B2_L, B2_R, 'volume show -sp'), bMid(B3_L, B3_R, 'statistics show'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'system health show'), bMid(B2_L, B2_R, 'aggr show -space'), bMid(B3_L, B3_R, 'qos stat show'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'disk show -broken'), bMid(B2_L, B2_R, 'snap list'), bMid(B3_L, B3_R, 'nfsstat -l'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'event log show'), bMid(B2_L, B2_R, 'vol efficiency'), bMid(B3_L, B3_R, 'net stat show'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'system node show'), bMid(B2_L, B2_R, 'quota report'), bMid(B3_L, B3_R, 'lun stats show'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Collector CLI Linux: sudo keystone-collector status | logs | collect | upload'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Command', 'Output', 'Use When', 'Level', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['storage fail show', 'HA state', 'Daily', 'admin', 'Both Connected'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['aggr show -space', 'Aggr capacity', 'Weekly', 'admin', '<85% used'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['qos stat show', 'IOPS throttle', 'On alert', 'admin', 'Throttled?'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['event log show', 'EMS events', 'On alert', 'admin', 'Last 24 h'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SSH from jump host port 22 to cluster management LIF IP'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  storage failover show    = Lists HA pair state; both nodes must be Connected'))
    lines.append(txt_row('  system health alert show = Active system health alarms; review daily'))
    lines.append(txt_row('  disk show -broken        = Lists failed/predictive-fail disks; action: replace'))
    lines.append(txt_row('  event log show -sev err  = EMS errors; filter last 24 h'))
    lines.append(txt_row('  volume show -space       = Per-volume used/avail; check thin overcommit'))
    lines.append(txt_row('  aggr show -space         = Aggregate physical capacity; key Keystone metric'))
    lines.append(txt_row('  statistics show          = Live performance counters: latency, IOPS, throughput'))
    lines.append(txt_row('  qos statistics show      = QoS policy hit rate; check if volumes are throttled'))
    lines.append(txt_row('  volume efficiency show   = Dedup/compress savings; verify efficiency enabled'))
    lines.append(txt_row('  quota report             = Displays qtree and user quotas; check for overages'))
    lines.append(txt_row('  ks status                = Collector service; last upload time; upload backlog'))
    lines.append(txt_row('  set -priv advanced       = Enable advanced CLI; required for diag-level cmds'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'netapp-insightiq-arch-index',
    'docs/storage/netapp/insightiq/architecture/index.md',
    'NetApp InsightIQ Architecture — performance analytics, capacity reporting, cluster health',
)
def netapp_insightiq_arch_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NetApp InsightIQ — Performance Analytics Architecture'))
    lines.append(txt_row())
    lines.append(txt_row('Performance reporting and analytics application for NetApp clusters; collects'))
    lines.append(txt_row('metrics via PAPI/REST; generates capacity forecasts and performance trend reports.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Collection Architecture'), bMid(L2, R2, 'Analytics Capabilities'))))
    lines.append(R(merge(bMid(L1, R1, 'Linux VM (separate appliance)'), bMid(L2, R2, 'Capacity forecasting'))))
    lines.append(R(merge(bMid(L1, R1, 'PAPI/REST: cluster metrics'), bMid(L2, R2, 'Performance trending'))))
    lines.append(R(merge(bMid(L1, R1, 'Poll interval: configurable'), bMid(L2, R2, 'Workload analysis'))))
    lines.append(R(merge(bMid(L1, R1, 'Stores: local PostgreSQL DB'), bMid(L2, R2, 'Usage reports: exportable'))))
    lines.append(R(merge(bMid(L1, R1, 'Multi-cluster: one instance'), bMid(L2, R2, 'Chargebacks: by client IP'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('InsightIQ complements ActiveIQ; InsightIQ for on-prem deep-dive, ActiveIQ for health.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Report Types'), bMid(L2, R2, 'Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Capacity: per volume/qtree'), bMid(L2, R2, 'Web UI: browser-based'))))
    lines.append(R(merge(bMid(L1, R1, 'Throughput: MB/s over time'), bMid(L2, R2, 'REST API: report export'))))
    lines.append(R(merge(bMid(L1, R1, 'Latency: ops response time'), bMid(L2, R2, 'Email: scheduled PDF/CSV'))))
    lines.append(R(merge(bMid(L1, R1, 'Protocol: NFS/CIFS breakdown'), bMid(L2, R2, 'Alerts: threshold-based'))))
    lines.append(R(merge(bMid(L1, R1, 'Client: per-IP breakdown'), bMid(L2, R2, 'AD integration: user auth'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Linux VM (4 vCPU, 8 GB RAM, 200+ GB disk); management network access to all'))
    lines.append(txt_row('monitored clusters on HTTPS; outbound SMTP for email reports.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('InsightIQ      = NetApp/Isilon performance and capacity analytics application'))
    lines.append(txt_row('PAPI           = Platform API; cluster REST interface used for metric collection'))
    lines.append(txt_row('Capacity forecast= projects date when volume or cluster will reach threshold'))
    lines.append(txt_row('Performance trending= graphs throughput/latency/IOPS over days, weeks, months'))
    lines.append(txt_row('Workload analysis= identifies top clients and protocols consuming capacity'))
    lines.append(txt_row('Chargeback     = report showing per-client or per-group storage consumption'))
    lines.append(txt_row('PostgreSQL     = local DB inside InsightIQ VM; stores collected metrics'))
    lines.append(txt_row('ActiveIQ       = NetApp cloud health monitoring; complementary to InsightIQ'))
    lines.append(txt_row('Poll interval  = how often InsightIQ queries cluster (default: 5 minutes)'))
    lines.append(txt_row('Protocol breakdown= IOPS split between NFS, CIFS, iSCSI, FCP'))
    lines.append(txt_row('Qtree          = ONTAP subdirectory with quota enforcement; InsightIQ tracks per-qtree'))
    lines.append(txt_row('Scheduled report= PDF/CSV delivered by email on daily/weekly/monthly schedule'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'netapp-keystone-arch-index',
    'docs/storage/netapp/keystone/architecture/index.md',
    'NetApp Keystone Architecture — STaaS subscription, service levels, Keystone Collector',
)
def netapp_keystone_arch_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NetApp Keystone — Storage as a Service Architecture'))
    lines.append(txt_row())
    lines.append(txt_row('Pay-per-use STaaS for NetApp AFF, FAS, and Cloud Volumes; Keystone Collector'))
    lines.append(txt_row('deployed on-prem to track consumption; subscription managed via Keystone Manager.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Service Model'), bMid(L2, R2, 'Service Levels'))))
    lines.append(R(merge(bMid(L1, R1, 'OpEx: monthly consumption bill'), bMid(L2, R2, 'Extreme: 1ms latency SLA'))))
    lines.append(R(merge(bMid(L1, R1, 'Hardware on-prem or cloud'), bMid(L2, R2, 'Premium: <2ms latency'))))
    lines.append(R(merge(bMid(L1, R1, 'NetApp manages HW lifecycle'), bMid(L2, R2, 'Standard: 4ms latency'))))
    lines.append(R(merge(bMid(L1, R1, 'Burst: auto approved up to X%'), bMid(L2, R2, 'CVO: Cloud Volumes ONTAP'))))
    lines.append(R(merge(bMid(L1, R1, 'Committed + burst billing'), bMid(L2, R2, 'Data protection: add-on tier'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Keystone Collector is a lightweight VM deployed on customer premises to report usage.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Keystone Collector'), bMid(L2, R2, 'Keystone Manager Portal'))))
    lines.append(R(merge(bMid(L1, R1, 'On-prem VM (or container)'), bMid(L2, R2, 'Subscription overview'))))
    lines.append(R(merge(bMid(L1, R1, 'Polls ONTAP for usage data'), bMid(L2, R2, 'Consumption dashboard'))))
    lines.append(R(merge(bMid(L1, R1, 'Reports to Keystone cloud'), bMid(L2, R2, 'Burst usage tracking'))))
    lines.append(R(merge(bMid(L1, R1, 'REST API: cluster metrics'), bMid(L2, R2, 'Invoice reconciliation'))))
    lines.append(R(merge(bMid(L1, R1, 'HTTPS 443: outbound only'), bMid(L2, R2, 'Service request portal'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NetApp AFF/FAS arrays or Cloud Volumes ONTAP; Keystone Collector VM on vSphere;'))
    lines.append(txt_row('internet access for Collector to reach Keystone cloud on TCP 443.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Keystone       = NetApp STaaS subscription offering; hardware + management included'))
    lines.append(txt_row('STaaS          = Storage as a Service; pay-per-use like cloud, but on-prem hardware'))
    lines.append(txt_row('Service level  = latency SLA tier (Extreme/Premium/Standard); billed separately'))
    lines.append(txt_row('Committed capacity= minimum subscribed amount; always billed regardless of use'))
    lines.append(txt_row('Burst capacity = usage above committed; auto-approved up to 20% over'))
    lines.append(txt_row('Keystone Collector= on-prem VM that tracks and reports consumption to NetApp'))
    lines.append(txt_row('Keystone Manager= NetApp portal for subscription, usage, and invoice management'))
    lines.append(txt_row('AFF            = All Flash FAS; NetApp NVMe-ready all-flash array'))
    lines.append(txt_row('CVO            = Cloud Volumes ONTAP; ONTAP on AWS/Azure/GCP as Keystone option'))
    lines.append(txt_row('OpEx model     = operational expense; monthly billing replaces CapEx purchase'))
    lines.append(txt_row('Data protection tier= add-on: SnapVault/SnapMirror included in the STaaS bill'))
    lines.append(txt_row('ONTAP API      = Collector queries cluster-mgmt LIF for capacity metrics'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'netapp-ontap-arch-index',
    'docs/storage/netapp/ontap/architecture/index.md',
    'NetApp ONTAP Architecture — unified storage OS, SVM, SnapShot, SnapMirror, NVMe-oF',
)
def netapp_ontap_arch_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NetApp ONTAP — Unified Storage OS Architecture'))
    lines.append(txt_row())
    lines.append(txt_row('ONTAP is the OS for AFF and FAS arrays; unified SAN + NAS from the same system;'))
    lines.append(txt_row('SVM for multi-tenancy; Snapshot for instant copies; SnapMirror for replication.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Architecture'), bMid(L2, R2, 'Protocols'))))
    lines.append(R(merge(bMid(L1, R1, 'HA pair: two nodes active-active'), bMid(L2, R2, 'NFS v3/v4.1: file'))))
    lines.append(R(merge(bMid(L1, R1, 'Cluster: 2-24 nodes'), bMid(L2, R2, 'SMB/CIFS: Windows file'))))
    lines.append(R(merge(bMid(L1, R1, 'SVM: storage virtual machine'), bMid(L2, R2, 'FC: block SAN (FCP)'))))
    lines.append(R(merge(bMid(L1, R1, 'Aggregate: RAID group of disks'), bMid(L2, R2, 'iSCSI: block over IP'))))
    lines.append(R(merge(bMid(L1, R1, 'Volume: logical data container'), bMid(L2, R2, 'NVMe-oF: FC or RDMA'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SVM is the tenant unit; each has own protocols, LIFs, volumes, and network config.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Data Services'), bMid(L2, R2, 'Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Snapshot: instant, no-cost copy'), bMid(L2, R2, 'System Manager: web UI'))))
    lines.append(R(merge(bMid(L1, R1, 'SnapMirror: async replication'), bMid(L2, R2, 'ONTAP CLI: SSH session'))))
    lines.append(R(merge(bMid(L1, R1, 'SnapVault: backup-to-disk'), bMid(L2, R2, 'REST API: 9.6+'))))
    lines.append(R(merge(bMid(L1, R1, 'SMBC: sync active-active'), bMid(L2, R2, 'ZAPI: legacy automation'))))
    lines.append(R(merge(bMid(L1, R1, 'FabricPool: cloud tiering'), bMid(L2, R2, 'ActiveIQ: cloud health'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AFF (all-flash) or FAS (hybrid) HA pair in rack; cluster interconnect (100GbE);'))
    lines.append(txt_row('FC or Ethernet host connectivity; dedicated e0M management port per node.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ONTAP          = NetApp unified storage OS; runs on AFF and FAS hardware'))
    lines.append(txt_row('SVM            = Storage Virtual Machine; multi-tenant partition; own protocols'))
    lines.append(txt_row('HA pair        = two ONTAP nodes in active-active cluster; failover in seconds'))
    lines.append(txt_row('Aggregate      = physical RAID group; contains one or more volumes'))
    lines.append(txt_row('Volume         = logical data container; flexible size; thin or thick'))
    lines.append(txt_row('LIF            = Logical Interface; floating IP that moves on failover'))
    lines.append(txt_row('Snapshot       = space-efficient point-in-time copy; no IO impact'))
    lines.append(txt_row('SnapMirror     = async replication between ONTAP systems; DR foundation'))
    lines.append(txt_row('SnapVault      = vault-mode SnapMirror; retains long-term backup snapshots'))
    lines.append(txt_row('SMBC           = SnapMirror Business Continuity; synchronous active-active'))
    lines.append(txt_row('FabricPool     = auto-tier cold data to S3 object store (AWS, GCP, Azure, ECS)'))
    lines.append(txt_row('RAID-DP        = ONTAP RAID level; double parity; default for FAS'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'netapp-snapcenter-arch-index',
    'docs/storage/netapp/snapcenter/architecture/index.md',
    'NetApp SnapCenter Architecture — centralized backup, app-aware, ONTAP Snapshot + SnapVault',
)
def netapp_snapcenter_arch_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NetApp SnapCenter — Centralized Backup Architecture'))
    lines.append(txt_row())
    lines.append(txt_row('Windows-based backup orchestration for app-aware ONTAP Snapshots; plugins for SQL,'))
    lines.append(txt_row('Oracle, SAP HANA, VMware, Exchange; SnapVault for DR copies; REST API for automation.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Architecture'), bMid(L2, R2, 'Supported Applications'))))
    lines.append(R(merge(bMid(L1, R1, 'SnapCenter Server: Windows'), bMid(L2, R2, 'SQL Server: VSS quiesce'))))
    lines.append(R(merge(bMid(L1, R1, 'Plugins: per-app agents'), bMid(L2, R2, 'Oracle: RMAN integration'))))
    lines.append(R(merge(bMid(L1, R1, 'MySQL: internal metadata DB'), bMid(L2, R2, 'SAP HANA: Backint API'))))
    lines.append(R(merge(bMid(L1, R1, 'Web UI: browser-based'), bMid(L2, R2, 'VMware: VADP snapshots'))))
    lines.append(R(merge(bMid(L1, R1, 'REST API: 4.6+'), bMid(L2, R2, 'Exchange: VSS-aware'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Snapshots are instant and zero-impact; SnapVault fans out to secondary ONTAP for DR.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Backup Flow'), bMid(L2, R2, 'Cloning and DR'))))
    lines.append(R(merge(bMid(L1, R1, 'Plugin quiesces app'), bMid(L2, R2, 'Clone from Snapshot: instant'))))
    lines.append(R(merge(bMid(L1, R1, 'ONTAP Snapshot created'), bMid(L2, R2, 'Dev/test: thin clone'))))
    lines.append(R(merge(bMid(L1, R1, 'SnapVault: vault to secondary'), bMid(L2, R2, 'SnapMirror: DR failover'))))
    lines.append(R(merge(bMid(L1, R1, 'Catalog: metadata stored'), bMid(L2, R2, 'Restore: volume or file'))))
    lines.append(R(merge(bMid(L1, R1, 'Retention: policy-based'), bMid(L2, R2, 'SMSQL: SQL-aware failover'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Windows Server VM for SnapCenter; ONTAP primary + secondary HA pairs; management'))
    lines.append(txt_row('network access from SnapCenter to ONTAP cluster-mgmt LIF on HTTPS.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SnapCenter     = NetApp centralized backup and clone management server'))
    lines.append(txt_row('Plugin         = per-application agent; installed on app server; quiesces app'))
    lines.append(txt_row('VSS            = Windows Volume Shadow Service; quiescence for SQL and Exchange'))
    lines.append(txt_row('Snapshot       = instant ONTAP point-in-time copy; no IO impact; basis for backup'))
    lines.append(txt_row('SnapVault      = vault-mode replication; keeps long-term backup copies on secondary'))
    lines.append(txt_row('SnapMirror     = DR replication; failover brings secondary ONTAP to primary role'))
    lines.append(txt_row('Clone          = writable thin copy from Snapshot; used for dev/test instantly'))
    lines.append(txt_row('Backint API    = SAP HANA backup interface; SnapCenter speaks Backint natively'))
    lines.append(txt_row('RMAN           = Oracle recovery manager; SnapCenter plugin coordinates with it'))
    lines.append(txt_row('Retention policy= defines how many Snapshot copies to keep and for how long'))
    lines.append(txt_row('Catalog        = SnapCenter database of all backups; needed for restore operations'))
    lines.append(txt_row('SMSQL          = SnapManager for SQL; legacy tool; replaced by SnapCenter plugin'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'netapp-snapmirror-arch-index',
    'docs/storage/netapp/snapmirror/architecture/index.md',
    'NetApp SnapMirror Architecture — async and sync replication, SMBC, cloud SnapMirror',
)
def netapp_snapmirror_arch_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'NetApp SnapMirror — Replication Architecture'))
    lines.append(txt_row())
    lines.append(txt_row('ONTAP replication technology: async for DR, sync for Metro zero-RPO, SMBC for'))
    lines.append(txt_row('active-active; Cloud SnapMirror tiers to CVO on AWS/Azure/GCP.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Replication Modes'), bMid(L2, R2, 'Use Cases'))))
    lines.append(R(merge(bMid(L1, R1, 'Async: low RPO, remote DR'), bMid(L2, R2, 'DR: failover to secondary'))))
    lines.append(R(merge(bMid(L1, R1, 'Sync: 0 RPO; metro stretch'), bMid(L2, R2, 'Metro: cross-site HA'))))
    lines.append(R(merge(bMid(L1, R1, 'SMBC: active-active; 0 RPO'), bMid(L2, R2, 'Cloud: tier or migrate'))))
    lines.append(R(merge(bMid(L1, R1, 'Vault: long-term retention'), bMid(L2, R2, 'Backup: SnapVault copies'))))
    lines.append(R(merge(bMid(L1, R1, 'Unified: data + protection'), bMid(L2, R2, 'Dev/test: clone from mirror'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('SMBC requires ONTAP Mediator for automated failover without manual intervention.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Async Architecture'), bMid(L2, R2, 'Sync / SMBC Architecture'))))
    lines.append(R(merge(bMid(L1, R1, 'Snapshots transferred as deltas'), bMid(L2, R2, 'Write completes both sites'))))
    lines.append(R(merge(bMid(L1, R1, 'Schedule: hourly/daily/etc'), bMid(L2, R2, 'RPO: zero (synchronous)'))))
    lines.append(R(merge(bMid(L1, R1, 'Mirror: secondary read-only'), bMid(L2, R2, 'SMBC: both sides serve IO'))))
    lines.append(R(merge(bMid(L1, R1, 'Failover: manual break-mirror'), bMid(L2, R2, 'Mediator: auto failover'))))
    lines.append(R(merge(bMid(L1, R1, 'Lag: RPO = transfer interval'), bMid(L2, R2, 'Max distance: 10ms RTT'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Primary ONTAP cluster and secondary ONTAP cluster (or CVO in cloud); intercluster'))
    lines.append(txt_row('LIFs on dedicated ports; WAN or DCI link between sites for replication traffic.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SnapMirror     = ONTAP replication technology; async, sync, or vault modes'))
    lines.append(txt_row('Async          = delta Snapshot transfers on schedule; best for remote DR sites'))
    lines.append(txt_row('Sync SnapMirror= write confirmed on both nodes before ACK; 0 RPO; requires low RTT'))
    lines.append(txt_row('SMBC           = SnapMirror Business Continuity; active-active; both serve reads/writes'))
    lines.append(txt_row('SnapVault      = vault mode; secondary keeps more snapshots than primary'))
    lines.append(txt_row('RPO            = Recovery Point Objective; how much data you can afford to lose'))
    lines.append(txt_row('Break mirror   = convert secondary from read-only to writable; DR activation step'))
    lines.append(txt_row('Mediator       = ONTAP Mediator VM; tiebreaker for SMBC automated failover'))
    lines.append(txt_row('Intercluster LIF= dedicated IP address for cluster-to-cluster replication traffic'))
    lines.append(txt_row('Cloud SnapMirror= replicate ONTAP volumes to Cloud Volumes ONTAP (CVO) on cloud'))
    lines.append(txt_row('Lag time       = how far behind the secondary is; = RPO in async mode'))
    lines.append(txt_row('CVO            = Cloud Volumes ONTAP; ONTAP on public cloud; SnapMirror target'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'netapp-superna-arch-index',
    'docs/storage/netapp/superna-eyeglass/architecture/index.md',
    'Superna Eyeglass Architecture — SVM DR orchestration, config replication, DNS failover',
)
def netapp_superna_arch_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — ONTAP DR Orchestration Architecture'))
    lines.append(txt_row())
    lines.append(txt_row('Third-party DR automation for NetApp ONTAP SVM DR; replicates configuration changes,'))
    lines.append(txt_row('automates failover, and updates DNS — replacing manual SVM DR failover steps.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Architecture'), bMid(L2, R2, 'Key Functions'))))
    lines.append(R(merge(bMid(L1, R1, 'Linux VM (Eyeglass appliance)'), bMid(L2, R2, 'SVM DR config replication'))))
    lines.append(R(merge(bMid(L1, R1, 'Connects to both ONTAP sites'), bMid(L2, R2, 'Export policy sync'))))
    lines.append(R(merge(bMid(L1, R1, 'REST + ZAPI for ONTAP access'), bMid(L2, R2, 'Share + ACL replication'))))
    lines.append(R(merge(bMid(L1, R1, 'HA: active-passive pair'), bMid(L2, R2, 'DNS failover automation'))))
    lines.append(R(merge(bMid(L1, R1, 'Monitor: config drift alerts'), bMid(L2, R2, 'Failover in minutes, not h'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Without Eyeglass, SVM DR failover requires 20+ manual steps; Eyeglass reduces to 1.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Failover Process'), bMid(L2, R2, 'Monitoring'))))
    lines.append(R(merge(bMid(L1, R1, 'Detect: SnapMirror lag alert'), bMid(L2, R2, 'Config drift detection'))))
    lines.append(R(merge(bMid(L1, R1, 'Decide: manual or auto'), bMid(L2, R2, 'Replication lag tracking'))))
    lines.append(R(merge(bMid(L1, R1, 'Break SnapMirror mirrors'), bMid(L2, R2, 'DR readiness score'))))
    lines.append(R(merge(bMid(L1, R1, 'Activate SVM at DR site'), bMid(L2, R2, 'Compliance report: config'))))
    lines.append(R(merge(bMid(L1, R1, 'Update DNS: new IPs live'), bMid(L2, R2, 'Alerts: email + SNMP'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Eyeglass VM (4 vCPU, 16 GB RAM) on vSphere; management network access to both'))
    lines.append(txt_row('ONTAP cluster-mgmt LIFs; DNS server access for automatic record updates.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass       = Superna product; automates ONTAP SVM DR failover and config sync'))
    lines.append(txt_row('SVM DR         = Storage Virtual Machine Disaster Recovery; ONTAP native feature'))
    lines.append(txt_row('Config replication= Eyeglass copies export policies, shares, ACLs to DR site SVM'))
    lines.append(txt_row('Config drift   = production SVM config changed but DR SVM not updated; Eyeglass alerts'))
    lines.append(txt_row('Export policy  = NFS access rule; Eyeglass replicates so NFS works after failover'))
    lines.append(txt_row('SnapMirror lag = time between last successful transfer; Eyeglass monitors and alerts'))
    lines.append(txt_row('DNS failover   = Eyeglass updates DNS records to point to DR SVM IPs post-failover'))
    lines.append(txt_row('DR readiness score= Eyeglass composite score; 0-100; low score = failover risk'))
    lines.append(txt_row('Break mirror   = convert SnapMirror secondary to read-write; Eyeglass automates'))
    lines.append(txt_row('Failback       = reverse replication back to primary after DR event is resolved'))
    lines.append(txt_row('ZAPI           = legacy NetApp ONTAP management API; Eyeglass uses alongside REST'))
    lines.append(txt_row('ACL            = Access Control List; file share permissions replicated to DR'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'pure-evergreen-one-arch-index',
    'docs/storage/pure/evergreen-one/architecture/index.md',
    'Pure Evergreen//One Architecture — STaaS, managed service, non-disruptive upgrades',
)
def pure_evergreen_one_arch_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Pure Evergreen//One — Storage as a Service Architecture'))
    lines.append(txt_row())
    lines.append(txt_row('Pure Storage STaaS: all-NVMe FlashArray delivered to customer DC; Pure manages HW;'))
    lines.append(txt_row('non-disruptive controller upgrades; consumption billing via Pure1 portal.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Service Model'), bMid(L2, R2, 'Underlying Platform'))))
    lines.append(R(merge(bMid(L1, R1, 'FlashArray in customer rack'), bMid(L2, R2, 'FlashArray //X: block NVMe'))))
    lines.append(R(merge(bMid(L1, R1, 'Pure manages HW + Purity OS'), bMid(L2, R2, 'FlashBlade //S: file + obj'))))
    lines.append(R(merge(bMid(L1, R1, 'Non-disruptive controller swap'), bMid(L2, R2, 'All-NVMe: no spinning disk'))))
    lines.append(R(merge(bMid(L1, R1, 'Customer manages data + VMs'), bMid(L2, R2, 'SafeMode: immutable snaps'))))
    lines.append(R(merge(bMid(L1, R1, 'Subscription: per TB/month'), bMid(L2, R2, 'Pure1: management portal'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Pure guarantees controller upgrades are included; no forklift needed ever.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'SLA and Guarantees'), bMid(L2, R2, 'Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Availability: 99.9999% SLA'), bMid(L2, R2, 'Pure1: SaaS portal'))))
    lines.append(R(merge(bMid(L1, R1, 'Performance: guaranteed IOPS'), bMid(L2, R2, 'REST API: automation'))))
    lines.append(R(merge(bMid(L1, R1, 'Non-disruptive upgrade: always'), bMid(L2, R2, 'Pure Support: proactive'))))
    lines.append(R(merge(bMid(L1, R1, 'Capacity burst: elastic'), bMid(L2, R2, 'Pure1 AI: predictive alerts'))))
    lines.append(R(merge(bMid(L1, R1, 'Energy efficiency included'), bMid(L2, R2, 'MSP option: partner managed'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Pure FlashArray //X or //C in customer rack; FC or iSCSI or NVMe-oF host connections;'))
    lines.append(txt_row('Pure1 cloud portal management; phone-home telemetry over TCP 443 to Pure cloud.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Evergreen//One = Pure STaaS; hardware in your DC, Pure manages it, you consume it'))
    lines.append(txt_row('STaaS          = Storage as a Service; pay per TB used, not upfront CapEx'))
    lines.append(txt_row('Non-disruptive = controller upgrade without IO downtime; Pure guarantee'))
    lines.append(txt_row('SafeMode       = immutable Snapshot; cannot be deleted even by admin; ransomware'))
    lines.append(txt_row('Pure1          = Pure SaaS management and analytics portal; all arrays in one view'))
    lines.append(txt_row('FlashArray //X = Pure block storage array; NVMe; target for Evergreen//One block'))
    lines.append(txt_row('FlashBlade //S = Pure scale-out file+object; target for Evergreen//One unstructured'))
    lines.append(txt_row('Purity OS      = Pure storage OS; runs on FlashArray; managed by Pure under contract'))
    lines.append(txt_row('99.9999% SLA   = six nines; ~32 seconds total downtime per year'))
    lines.append(txt_row('Capacity burst = use more than committed; billed at overage rate automatically'))
    lines.append(txt_row('Proactive support= Pure1 AI detects issues and opens support cases before you do'))
    lines.append(txt_row('Phone-home     = telemetry from array to Pure cloud; required for managed service'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'pure-evergreen-arch-index',
    'docs/storage/pure/evergreen/architecture/index.md',
    'Pure Evergreen Architecture — subscription model, controller upgrade path, no forklift',
)
def pure_evergreen_arch_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Pure Evergreen — Subscription Upgrade Architecture'))
    lines.append(txt_row())
    lines.append(txt_row('Evergreen subscription ensures non-disruptive controller upgrades for life of contract;'))
    lines.append(txt_row('customer owns/leases hardware; Pure delivers new controllers without downtime.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Subscription Model'), bMid(L2, R2, 'Upgrade Model'))))
    lines.append(R(merge(bMid(L1, R1, 'Customer purchases array'), bMid(L2, R2, 'New controllers delivered'))))
    lines.append(R(merge(bMid(L1, R1, 'Evergreen: software + support'), bMid(L2, R2, 'Shelf + drives stay in place'))))
    lines.append(R(merge(bMid(L1, R1, 'Annual: Purity upgrades included'), bMid(L2, R2, 'Controller swap: < 30 min'))))
    lines.append(R(merge(bMid(L1, R1, 'Term: 3 or 5 year options'), bMid(L2, R2, 'No migration of data needed'))))
    lines.append(R(merge(bMid(L1, R1, 'No forklift: ever promised'), bMid(L2, R2, 'IO: continues during swap'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Evergreen is the foundation; Evergreen//One adds Pure managing the hardware for you.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Upgrade Generations'), bMid(L2, R2, 'Evergreen vs Evergreen//One'))))
    lines.append(R(merge(bMid(L1, R1, '//X: NVMe director upgrade'), bMid(L2, R2, 'Evergreen: you own HW'))))
    lines.append(R(merge(bMid(L1, R1, '//C: capacity NVMe upgrade'), bMid(L2, R2, 'Evergreen//One: Pure owns HW'))))
    lines.append(R(merge(bMid(L1, R1, '//XL: extreme performance'), bMid(L2, R2, 'Both: no forklift guarantee'))))
    lines.append(R(merge(bMid(L1, R1, 'Director modules: hot-swap'), bMid(L2, R2, 'Both: Pure does controller'))))
    lines.append(R(merge(bMid(L1, R1, 'Same shelf across generations'), bMid(L2, R2, '//One: STaaS billing model'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('FlashArray chassis with drive shelves; new controllers arrive in 2U modules;'))
    lines.append(txt_row('Pure engineer does the swap on-site; drives and shelves are re-used.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Evergreen      = Pure subscription model; controller upgrades included in contract'))
    lines.append(txt_row('Forklift       = replacing entire storage array; Evergreen specifically avoids this'))
    lines.append(txt_row('Controller     = FlashArray compute module; upgrades move to new generation'))
    lines.append(txt_row('Director module= FlashArray controller; single or dual per chassis; hot-swap'))
    lines.append(txt_row('Purity//FA     = FlashArray OS; upgrades included in Evergreen subscription'))
    lines.append(txt_row('Non-disruptive = IO continues during controller swap; no maintenance window'))
    lines.append(txt_row('//X series     = NVMe-optimized FlashArray generation (current)'))
    lines.append(txt_row('//C series     = capacity-optimized; QLC NVMe for colder workloads'))
    lines.append(txt_row('//XL series    = extreme performance; enterprise-scale block storage'))
    lines.append(txt_row('Evergreen//One = STaaS variant; Pure manages hardware; customer just consumes'))
    lines.append(txt_row('Shelf reuse    = drive enclosures remain across controller generations'))
    lines.append(txt_row('3/5-year term  = common contract length; upgrade entitlement during term'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'pure-flasharray-arch-index',
    'docs/storage/pure/flasharray/architecture/index.md',
    'Pure FlashArray Architecture — NVMe AFA, Purity//FA, ActiveCluster, SafeMode, Pure1',
)
def pure_flasharray_arch_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Pure FlashArray — All-NVMe Block Storage Architecture'))
    lines.append(txt_row())
    lines.append(txt_row('All-NVMe all-flash array for block workloads; Purity//FA OS; ActiveCluster for'))
    lines.append(txt_row('active-active stretch; SafeMode immutable snapshots; Pure1 SaaS management.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Platform'), bMid(L2, R2, 'Data Services'))))
    lines.append(R(merge(bMid(L1, R1, '//X: NVMe enterprise block'), bMid(L2, R2, 'Snapshots: instant, space-eff'))))
    lines.append(R(merge(bMid(L1, R1, '//C: QLC capacity block'), bMid(L2, R2, 'Clones: writable snap copy'))))
    lines.append(R(merge(bMid(L1, R1, '//XL: extreme enterprise'), bMid(L2, R2, 'Async replication: remote DR'))))
    lines.append(R(merge(bMid(L1, R1, 'Dual controller: active-active'), bMid(L2, R2, 'ActiveCluster: sync AA'))))
    lines.append(R(merge(bMid(L1, R1, 'FC, iSCSI, NVMe-oF: host'), bMid(L2, R2, 'SafeMode: immutable snaps'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Inline dedup and compression are always on; no performance impact on NVMe.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'ActiveCluster (Sync Repl)'), bMid(L2, R2, 'Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Synchronous: 0 RPO, 0 RTO'), bMid(L2, R2, 'Pure1: SaaS portal'))))
    lines.append(R(merge(bMid(L1, R1, 'Both arrays serve host IO'), bMid(L2, R2, 'Purity UI: per-array web'))))
    lines.append(R(merge(bMid(L1, R1, 'Mediator: Pure cloud tiebreak'), bMid(L2, R2, 'REST API: v2; automation'))))
    lines.append(R(merge(bMid(L1, R1, 'Max RTT: 10ms between sites'), bMid(L2, R2, 'PowerShell/Ansible modules'))))
    lines.append(R(merge(bMid(L1, R1, 'VMware vMSC: certified'), bMid(L2, R2, 'Pure1 AI: predictive alerts'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('FlashArray chassis (3U); dual controllers active-active internally; NVMe drive modules;'))
    lines.append(txt_row('FC or 25GbE iSCSI or NVMe-oF to host; management on dedicated port.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('FlashArray     = Pure all-NVMe block storage array; //X //C //XL variants'))
    lines.append(txt_row('Purity//FA     = FlashArray OS; manages dedup, compression, replication'))
    lines.append(txt_row('ActiveCluster  = Pure synchronous replication; active-active; 0 RPO and 0 RTO'))
    lines.append(txt_row('SafeMode       = immutable Snapshot; protected from deletion even by admin'))
    lines.append(txt_row('Pure1          = SaaS management portal; all FlashArrays in one view'))
    lines.append(txt_row('Snapshot       = instant point-in-time copy; no performance impact'))
    lines.append(txt_row('Clone          = writable copy from Snapshot; dev/test use case'))
    lines.append(txt_row('Mediator       = Pure cloud service; tiebreaker for ActiveCluster failover'))
    lines.append(txt_row('NVMe-oF        = NVMe over Fabrics; FC-NVMe or iSER; lowest latency path'))
    lines.append(txt_row('//X series     = mainstream enterprise; NVMe with DirectFlash modules'))
    lines.append(txt_row('//C series     = capacity-optimized; QLC NAND; lower cost per GB'))
    lines.append(txt_row('vMSC           = vSphere Metro Storage Cluster; ActiveCluster is certified'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'pure-flashblade-arch-index',
    'docs/storage/pure/flashblade/architecture/index.md',
    'Pure FlashBlade Architecture — scale-out AFA, NFS/SMB/S3, AI/ML workloads',
)
def pure_flashblade_arch_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Pure FlashBlade — Scale-Out Unstructured Storage Architecture'))
    lines.append(txt_row())
    lines.append(txt_row('Scale-out all-flash for unstructured data; blade-based architecture; NFS, SMB, S3;'))
    lines.append(txt_row('target: AI/ML datasets, genomics, media workflows, backup targets.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Architecture'), bMid(L2, R2, 'Protocols'))))
    lines.append(R(merge(bMid(L1, R1, 'FlashBlade chassis (4U)'), bMid(L2, R2, 'NFS v3/v4.1: Linux/AI'))))
    lines.append(R(merge(bMid(L1, R1, 'Blades: capacity + compute'), bMid(L2, R2, 'SMB 2/3: Windows shares'))))
    lines.append(R(merge(bMid(L1, R1, 'Scale: add blades for perf'), bMid(L2, R2, 'S3: object; AI data lakes'))))
    lines.append(R(merge(bMid(L1, R1, '//S: storage blade (current)'), bMid(L2, R2, 'HDFS: Hadoop connector'))))
    lines.append(R(merge(bMid(L1, R1, 'Fabric: 40GbE or 100GbE'), bMid(L2, R2, 'Multi-protocol: same data'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Performance scales linearly: each blade adds both capacity and throughput.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Data Services'), bMid(L2, R2, 'Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Snapshots: instant, no-cost'), bMid(L2, R2, 'Purity//FB UI: web browser'))))
    lines.append(R(merge(bMid(L1, R1, 'Replication: async to remote'), bMid(L2, R2, 'REST API v2: automation'))))
    lines.append(R(merge(bMid(L1, R1, 'Pure Object Store: S3 compat'), bMid(L2, R2, 'Pure1: multi-site SaaS'))))
    lines.append(R(merge(bMid(L1, R1, 'SafeMode: immutable snaps'), bMid(L2, R2, 'CLI: purectl commands'))))
    lines.append(R(merge(bMid(L1, R1, 'File system: directory-based'), bMid(L2, R2, 'NFS exports: per-FS share'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('FlashBlade chassis in rack; 40GbE or 100GbE data ports per blade; management'))
    lines.append(txt_row('port (Eth); blades share chassis backplane for internal communication.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('FlashBlade     = Pure scale-out all-flash for file and object workloads'))
    lines.append(txt_row('//S blade      = current FlashBlade generation; each blade = storage + compute'))
    lines.append(txt_row('Scale-out      = add blades to grow capacity and performance simultaneously'))
    lines.append(txt_row('Purity//FB     = FlashBlade OS; manages filesystem, S3, snapshots'))
    lines.append(txt_row('NFS export     = directory shared over NFS; each filesystem can have one export'))
    lines.append(txt_row('Pure Object Store= S3-compatible object store built into FlashBlade //S'))
    lines.append(txt_row('SafeMode       = immutable Snapshot; admin cannot delete; ransomware protection'))
    lines.append(txt_row('HDFS           = Hadoop filesystem; FlashBlade presents as HDFS target'))
    lines.append(txt_row('AI/ML workload = high-throughput random read; FlashBlade optimized for this'))
    lines.append(txt_row('Replication    = async policy-based; replicates filesystems to remote FlashBlade'))
    lines.append(txt_row('Multi-protocol = same data accessible via NFS, SMB, and S3 simultaneously'))
    lines.append(txt_row('Blade          = hot-plug module; each adds storage capacity + bandwidth + IOPS'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'pure-pure1-arch-index',
    'docs/storage/pure/pure1/architecture/index.md',
    'Pure1 Architecture — SaaS management portal, AIOps analytics, cross-site fleet view',
)
def pure_pure1_arch_index():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'Pure1 — SaaS Management and AIOps Platform'))
    lines.append(txt_row())
    lines.append(txt_row('Pure1 is Pure Storage cloud-hosted SaaS for managing all FlashArrays and FlashBlades;'))
    lines.append(txt_row('AIOps: predictive analytics, capacity forecasting, anomaly detection via Pure1 AI.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Platform Architecture'), bMid(L2, R2, 'Analytics Capabilities'))))
    lines.append(R(merge(bMid(L1, R1, 'SaaS: Pure-hosted cloud'), bMid(L2, R2, 'Pure1 AI: ML models'))))
    lines.append(R(merge(bMid(L1, R1, 'All arrays: single pane'), bMid(L2, R2, 'Capacity forecast: 90 days'))))
    lines.append(R(merge(bMid(L1, R1, 'Phone-home: telemetry feed'), bMid(L2, R2, 'Anomaly: vs peer fleet'))))
    lines.append(R(merge(bMid(L1, R1, 'REST API v2: management'), bMid(L2, R2, 'Workload planning advisor'))))
    lines.append(R(merge(bMid(L1, R1, 'Multi-site: cross-DC view'), bMid(L2, R2, 'Proactive: auto support case'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Pure1 is the only management plane; there is no on-prem equivalent management server.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Telemetry Collection'), bMid(L2, R2, 'Support Integration'))))
    lines.append(R(merge(bMid(L1, R1, 'Array: phone-home over 443'), bMid(L2, R2, 'SR: auto-open by Pure1 AI'))))
    lines.append(R(merge(bMid(L1, R1, 'No on-prem collector needed'), bMid(L2, R2, 'Case: status in Pure1 UI'))))
    lines.append(R(merge(bMid(L1, R1, 'Logs + metrics + events'), bMid(L2, R2, 'Remote assist: TAM view'))))
    lines.append(R(merge(bMid(L1, R1, 'Historical: 1 year+ retention'), bMid(L2, R2, 'My Pure1: customer login'))))
    lines.append(R(merge(bMid(L1, R1, 'Real-time: 30s granularity'), bMid(L2, R2, 'Role-based: view or manage'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Pure1 is fully SaaS; arrays need TCP 443 outbound to pure1.purestorage.com;'))
    lines.append(txt_row('no on-prem servers or agents required.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Pure1          = Pure Storage SaaS management and analytics portal'))
    lines.append(txt_row('SaaS           = Software as a Service; Pure hosts it; no on-prem infra needed'))
    lines.append(txt_row('Phone-home     = array telemetry sent to Pure cloud; enables Pure1 AI analytics'))
    lines.append(txt_row('Pure1 AI       = ML-based analytics; trained on Pure fleet; detects anomalies'))
    lines.append(txt_row('Capacity forecast= predicts when arrays will hit threshold; 90-day horizon'))
    lines.append(txt_row('Anomaly        = Pure1 AI flags unusual performance vs fleet peer comparison'))
    lines.append(txt_row('Proactive SR   = Pure1 AI opens support case before you notice a problem'))
    lines.append(txt_row('REST API v2    = Pure1 northbound API; pull metrics, manage arrays programmatically'))
    lines.append(txt_row('Multi-site     = all arrays across all sites visible in one Pure1 login'))
    lines.append(txt_row('TAM            = Technical Account Manager; has read-only view of your Pure1'))
    lines.append(txt_row('My Pure1       = customer-facing login at pure1.purestorage.com'))
    lines.append(txt_row('Historical retention= Pure1 keeps 1 year+ of telemetry for trend analysis'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines
