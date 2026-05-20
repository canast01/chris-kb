"""
Dell storage sub-product diagram functions (Apex, CloudIQ, CoD, Data Domain, ECS, FoD,
PowerMax, PowerPath, PowerScale, PowerStore, SCG, Unity, VPlex).
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)


@kb_diagram(
    'dell-apex-saas',
    'docs/storage/dell/apex-storage-as-a-service/index.md',
    'Dell Apex Storage as a Service — on-prem STaaS, block and file, cloud-managed portal',
)
def dell_apex_saas():
    """Dell Apex Storage as a Service — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Apex Storage as a Service'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Apex STaaS: Dell-owned hardware on customer premises; consumed as a cloud service')))
    lines.append(R(bMid(IV_L, IV_R, 'Block: NVMe-based tiers (Performance/Capacity); File: NFS/SMB via PowerScale nodes')))
    lines.append(R(bMid(IV_L, IV_R, 'Managed via Apex Console (cloud portal); Dell handles hardware lifecycle')))
    lines.append(R(bMid(IV_L, IV_R, 'Billing: committed base + consumed burst; monthly subscription model')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Apex Console order → Dell installs hardware → customer connects hosts → consume storage'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Storage Tiers'), bMid(B2_L, B2_R, 'Management'), bMid(B3_L, B3_R, 'Connectivity'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Perf (NVMe)'), bMid(B2_L, B2_R, 'Apex Console'), bMid(B3_L, B3_R, 'iSCSI'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity (SAS)'), bMid(B2_L, B2_R, 'CloudIQ monitor'), bMid(B3_L, B3_R, 'FC'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'File (NFS/SMB)'), bMid(B2_L, B2_R, 'SCG telemetry'), bMid(B3_L, B3_R, 'NFS/SMB'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Committed base'), bMid(B2_L, B2_R, 'REST API'), bMid(B3_L, B3_R, 'iSCSI CHAP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Burst capacity'), bMid(B2_L, B2_R, 'Billing portal'), bMid(B3_L, B3_R, 'FC port sec.'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Dell retains ownership of hardware; customer manages workloads and data'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Layer', 'Function', 'Owner', 'Tool', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Hardware', 'Arrays/nodes', 'Dell', 'Field svc.', 'On-prem'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Management', 'Portal/API', 'Customer', 'Apex Console', 'Cloud SaaS'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Monitoring', 'Health/perf', 'Shared', 'CloudIQ', 'Via SCG'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Data', 'Workloads', 'Customer', 'Host tools', 'Customer owns'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: Dell array hardware on-premises · customer network (iSCSI VLAN / FC fabric)'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Apex STaaS     = Storage as a Service; consumption-based billing for on-prem Dell storage'))
    lines.append(txt_row('  Apex Console   = Cloud portal at apex.dell.com; provision volumes, view usage, raise SRs'))
    lines.append(txt_row('  Committed base = Minimum contracted storage tier; always billed regardless of use'))
    lines.append(txt_row('  Burst capacity = Pre-installed but unbilled storage; consumed when above committed level'))
    lines.append(txt_row('  SCG            = Secure Connect Gateway; transmits telemetry from arrays to CloudIQ'))
    lines.append(txt_row('  CloudIQ        = Dell cloud-based analytics; health scores, predictive alerts, capacity'))
    lines.append(txt_row('  NVMe tier      = Performance storage tier; all-flash NVMe drives; lowest latency'))
    lines.append(txt_row('  Capacity tier  = Lower-cost SAS/NL-SAS tier; higher latency; suited to cold workloads'))
    lines.append(txt_row('  iSCSI CHAP     = Challenge Handshake Auth Protocol; authenticates iSCSI initiators'))
    lines.append(txt_row('  FC port sec.   = FC fabric binding + port security; restricts which HBAs can login'))
    lines.append(txt_row('  vVols          = Virtual Volumes; per-VM storage objects; VASA provider exposes to vCenter'))
    lines.append(txt_row('  REST API       = Apex Console REST API; automate volume creation, mapping, and reporting'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-apex-saas-arch-standards',
    'docs/storage/dell/apex-storage-as-a-service/architecture/design-standards/index.md',
    'Apex STaaS Architecture Standards — tier selection, network design, redundancy, sizing',
)
def dell_apex_saas_arch_standards():
    """Dell Apex STaaS Architecture Design Standards — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Apex STaaS — Architecture Design Standards'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Apex design standards: tier selection, network isolation, redundancy, and sizing')))
    lines.append(R(bMid(IV_L, IV_R, 'Tier: Performance (NVMe) for latency-sensitive; Capacity (SAS) for bulk/backup')))
    lines.append(R(bMid(IV_L, IV_R, 'Network: dedicated iSCSI VLAN (jumbo MTU 9000) or FC fabric (dual-fabric HA)')))
    lines.append(R(bMid(IV_L, IV_R, 'Redundancy: dual-controller array; multipath on hosts (PowerPath or native MPIO)')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Workload profile → tier selection → network design → host multipath → committed sizing'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Tier Design'), bMid(B2_L, B2_R, 'Network Design'), bMid(B3_L, B3_R, 'Redundancy'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Perf: <1ms lat'), bMid(B2_L, B2_R, 'Dedicated VLAN'), bMid(B3_L, B3_R, 'Dual controller'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cap: bulk/backup'), bMid(B2_L, B2_R, 'MTU 9000 iSCSI'), bMid(B3_L, B3_R, 'Dual fabric FC'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'File: NFS/SMB'), bMid(B2_L, B2_R, 'Dual FC fabric'), bMid(B3_L, B3_R, 'PowerPath MPIO'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Mix tiers'), bMid(B2_L, B2_R, 'NFS storage VLAN'), bMid(B3_L, B3_R, 'No SPOF design'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Size committed'), bMid(B2_L, B2_R, 'OOB management'), bMid(B3_L, B3_R, 'Alert thresholds'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Commit 70–80% of expected peak usage; burst covers spikes without capacity delays'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Area', 'Standard', 'Why', 'Verify', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['iSCSI MTU', '9000 jumbo', 'Perf', 'ping -s 8972', 'End-to-end'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Multipath', 'MPIO/PowerPath', 'HA paths', 'Paths active', '≥2 paths'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Committed', '70–80% peak', 'Cost control', 'Usage report', 'Burst covers'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Monitoring', 'CloudIQ alert', 'Proactive', 'Alert config', '80% threshold'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: Dell array (dual controller) · 10/25/100 GbE NICs · FC 16/32Gb HBAs'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Performance tier = NVMe all-flash; sub-millisecond latency; suited to databases/VMs'))
    lines.append(txt_row('  Capacity tier    = SAS/NL-SAS; lower cost per TB; suited to backup, archive, file'))
    lines.append(txt_row('  iSCSI VLAN       = Isolated VLAN for storage traffic; prevents broadcast interference'))
    lines.append(txt_row('  Jumbo MTU        = 9000-byte frames on iSCSI path; reduces CPU overhead'))
    lines.append(txt_row('  Dual fabric      = Two independent FC fabrics; each HBA port on different fabric'))
    lines.append(txt_row('  PowerPath        = Dell multipath software; active-active path policy for arrays'))
    lines.append(txt_row('  MPIO             = Native OS multipath I/O; Windows/Linux alternative to PowerPath'))
    lines.append(txt_row('  Committed size   = Contracted Apex STaaS capacity; billed monthly regardless of use'))
    lines.append(txt_row('  Burst threshold  = Capacity level triggering burst billing; configure alert at 80%'))
    lines.append(txt_row('  OOB management   = Out-of-band management network for array controller access'))
    lines.append(txt_row('  No SPOF          = No Single Point of Failure; dual fabric + dual controller + MPIO'))
    lines.append(txt_row('  Tier mix         = Mix Performance and Capacity tiers in same Apex subscription'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-apex-saas-arch-how-it-works',
    'docs/storage/dell/apex-storage-as-a-service/architecture/how-it-works/index.md',
    'Apex STaaS How It Works — ordering, provisioning, telemetry, billing, and lifecycle',
)
def dell_apex_saas_arch_how_it_works():
    """Dell Apex STaaS How It Works — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Apex STaaS — How It Works'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Apex STaaS workflow: order → Dell installs → customer connects → consume and pay')))
    lines.append(R(bMid(IV_L, IV_R, 'SCG gateway transmits array telemetry to CloudIQ for health and capacity analytics')))
    lines.append(R(bMid(IV_L, IV_R, 'Billing: monthly invoice for committed tier + any burst above committed threshold')))
    lines.append(R(bMid(IV_L, IV_R, 'Lifecycle: Dell manages firmware, hardware replacement, and capacity expansion')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Apex Console order → Dell field install → customer network config → host connect → use'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Ordering'), bMid(B2_L, B2_R, 'Monitoring'), bMid(B3_L, B3_R, 'Billing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Apex Console'), bMid(B2_L, B2_R, 'SCG telemetry'), bMid(B3_L, B3_R, 'Committed fee'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Tier/size select'), bMid(B2_L, B2_R, 'CloudIQ health'), bMid(B3_L, B3_R, 'Burst overage'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dell field svc.'), bMid(B2_L, B2_R, 'Health score'), bMid(B3_L, B3_R, 'Monthly invoice'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Rack/cable/init'), bMid(B2_L, B2_R, 'Alert thresholds'), bMid(B3_L, B3_R, 'Usage dashboard'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Customer network'), bMid(B2_L, B2_R, 'Capacity forecast'), bMid(B3_L, B3_R, 'Contract renew'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Dell SupportAssist remotely monitors controller health; dispatches parts proactively'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Phase', 'Actor', 'Action', 'Duration', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Order', 'Customer', 'Apex Console', '1–5 days', 'Contract first'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Install', 'Dell FSE', 'Rack/cable', '1–2 days', 'Site prep req.'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Connect', 'Customer', 'Network/host', '1 day', 'SAN/iSCSI'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Consume', 'Customer', 'Provision vols', 'Ongoing', 'Monitor burst'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: Dell array shipped to site · SCG virtual appliance on customer management VM'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  FSE            = Field Service Engineer; Dell technician who installs and maintains hardware'))
    lines.append(txt_row('  SCG            = Secure Connect Gateway; virtual appliance sending telemetry to Dell cloud'))
    lines.append(txt_row('  SupportAssist  = Dell remote support; uses SCG to proactively detect and resolve faults'))
    lines.append(txt_row('  Health score   = CloudIQ 0–100 score per system; below 80 triggers investigation'))
    lines.append(txt_row('  Burst billing  = Monthly charge for capacity consumed above the committed baseline'))
    lines.append(txt_row('  Site prep      = Customer responsibility: power (kVA), cooling, rack space, network drops'))
    lines.append(txt_row('  Capacity forecast = CloudIQ predictive model showing when committed tier will run out'))
    lines.append(txt_row('  Contract renew = Annual or multi-year renewal; adjust committed tier at renewal'))
    lines.append(txt_row('  Proactive part = Dell dispatches replacement before failure based on predictive analytics'))
    lines.append(txt_row('  Apex Console   = Web portal for ordering, provisioning, billing, and support requests'))
    lines.append(txt_row('  Monthly invoice = Bill showing committed fee + burst overage + data services usage'))
    lines.append(txt_row('  Host connect   = Customer installs multipath, registers initiators, mounts volumes'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-apex-saas-arch-integrations',
    'docs/storage/dell/apex-storage-as-a-service/architecture/integrations/index.md',
    'Apex STaaS Integrations — VMware vVols, Kubernetes CSI, data protection, cloud portal',
)
def dell_apex_saas_arch_integrations():
    """Dell Apex STaaS Integrations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Apex STaaS — Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Apex integrations: VMware (vVols/VMFS), Kubernetes CSI, data protection, REST API')))
    lines.append(R(bMid(IV_L, IV_R, 'VMware: VASA provider for vVols; VMFS datastore via iSCSI or FC; SRM support')))
    lines.append(R(bMid(IV_L, IV_R, 'Kubernetes: Dell CSI driver; dynamic persistent volume provisioning for pods')))
    lines.append(R(bMid(IV_L, IV_R, 'Data protection: PowerProtect DD target, Avamar, or third-party via NFS/iSCSI')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  vCenter VASA → vVols per-VM policy · CSI driver → PVC provisioning · DD target → backup'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VMware'), bMid(B2_L, B2_R, 'Kubernetes'), bMid(B3_L, B3_R, 'Data Protection'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vVols / VASA'), bMid(B2_L, B2_R, 'Dell CSI driver'), bMid(B3_L, B3_R, 'PowerProtect DD'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VMFS datastore'), bMid(B2_L, B2_R, 'PVC dynamic'), bMid(B3_L, B3_R, 'Avamar NDMP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SRM for DR'), bMid(B2_L, B2_R, 'StorageClass'), bMid(B3_L, B3_R, 'NetWorker'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SPBM policy'), bMid(B2_L, B2_R, 'Snapshot CSI'), bMid(B3_L, B3_R, 'Cloud DR copy'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vCenter plugin'), bMid(B2_L, B2_R, 'Helm charts'), bMid(B3_L, B3_R, 'REST API'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  VASA provider and CSI driver installed once; all subsequent provisioning is self-service'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Integration', 'Protocol', 'Key feature', 'Provision', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['VMware vVols', 'VASA 3.0', 'Per-VM policy', 'vCenter UI', 'SPBM driven'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Kubernetes', 'CSI 1.x', 'Dynamic PVC', 'StorageClass', 'Dell CSI helm'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['PowerProt. DD', 'NFS/DD Boost', 'Dedup target', 'PPDM policy', 'DD Boost req.'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['REST API', 'HTTPS/JSON', 'Automation', 'Scripts/IaC', 'Apex portal'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: VASA provider VM on vCenter · CSI controller pod in K8s · DD appliance on-prem'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  vVols          = Virtual Volumes; per-VM storage objects; managed by VASA provider'))
    lines.append(txt_row('  VASA           = vSphere APIs for Storage Awareness; enables per-VM storage policies'))
    lines.append(txt_row('  SPBM           = Storage Policy Based Management; assigns storage policy to each VM'))
    lines.append(txt_row('  VMFS           = vSphere File System; block-based datastore for VMware workloads'))
    lines.append(txt_row('  SRM            = Site Recovery Manager; VMware DR orchestration using storage replication'))
    lines.append(txt_row('  CSI driver     = Container Storage Interface; Dell CSI plugin provisions K8s PVCs'))
    lines.append(txt_row('  StorageClass   = Kubernetes resource defining storage tier and parameters for PVCs'))
    lines.append(txt_row('  PVC            = PersistentVolumeClaim; K8s request for storage; CSI provisions it'))
    lines.append(txt_row('  DD Boost       = Dell Data Domain protocol; deduplicated backup streams to DD target'))
    lines.append(txt_row('  PPDM           = PowerProtect Data Manager; Dell backup orchestration for DD targets'))
    lines.append(txt_row('  NDMP           = Network Data Management Protocol; Avamar backup of NAS file systems'))
    lines.append(txt_row('  Helm chart     = Kubernetes package manager chart; deploys Dell CSI driver components'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-apex-saas-operations',
    'docs/storage/dell/apex-storage-as-a-service/operations/index.md',
    'Apex STaaS Operations — volume provisioning, capacity management, snapshots, monitoring',
)
def dell_apex_saas_operations():
    """Dell Apex STaaS Operations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Apex STaaS — Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Apex day-2 operations: volume provisioning, capacity management, snapshots, alerts')))
    lines.append(R(bMid(IV_L, IV_R, 'Provisioning: Apex Console or REST API; create volumes, exports, map to hosts')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity: monitor committed vs used in CloudIQ; raise SR to expand committed tier')))
    lines.append(R(bMid(IV_L, IV_R, 'Snapshots: schedule via Apex Console; crash-consistent; clone for dev/test')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Provision → map to host → monitor CloudIQ → snapshot → capacity review → expand'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Provisioning'), bMid(B2_L, B2_R, 'Monitoring'), bMid(B3_L, B3_R, 'Data Services'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Create volume'), bMid(B2_L, B2_R, 'CloudIQ health'), bMid(B3_L, B3_R, 'Snapshot sched.'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Map to host'), bMid(B2_L, B2_R, 'Capacity usage'), bMid(B3_L, B3_R, 'Clone volume'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Create NFS exp.'), bMid(B2_L, B2_R, 'Performance IO'), bMid(B3_L, B3_R, 'Replication'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Expand volume'), bMid(B2_L, B2_R, 'Alert review'), bMid(B3_L, B3_R, 'Thin reclaim'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Delete/unmap'), bMid(B2_L, B2_R, 'Billing report'), bMid(B3_L, B3_R, 'Compression'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  All hardware ops (firmware, replacement) are Dell responsibility; open SR via Apex Console'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Task', 'Apex Console', 'Key field', 'Verify', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Create vol', 'Storage>Volumes', 'Size/tier', 'Host sees vol', 'Thin prov.'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Map host', 'Storage>Hosts', 'IQN/WWN', 'Host LUN', 'Multipath on'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Snapshot', 'Data Svc>Snap', 'Schedule', 'Snap count', 'Retention set'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Capacity SR', 'Support>SR', 'Current/target', 'SR created', 'Dell responds'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: array controllers · host HBA/NIC · multipath driver on each host'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Thin provisioning = Volume allocated to host at requested size; storage used only on write'))
    lines.append(txt_row('  Host mapping     = Associate host IQN (iSCSI) or WWN (FC) to a volume or export'))
    lines.append(txt_row('  NFS export       = File storage share; mount on Linux/VMware via NFS protocol'))
    lines.append(txt_row('  Snapshot sched.  = Automated recurring snapshot policy; retain N snapshots'))
    lines.append(txt_row('  Clone            = Writable copy of a volume or snapshot; used for dev/test'))
    lines.append(txt_row('  Thin reclaim     = Return unused thin-provisioned blocks to pool (UNMAP/TRIM)'))
    lines.append(txt_row('  CloudIQ health   = AI-driven health score; monitors controller, drives, fans, thermals'))
    lines.append(txt_row('  Performance IO   = IOPS and throughput graphs per volume in CloudIQ'))
    lines.append(txt_row('  Billing report   = Apex Console monthly view of committed + burst usage by tier'))
    lines.append(txt_row('  SR (Service Req) = Support request to Dell; used for hardware issues and capacity expands'))
    lines.append(txt_row('  Compression      = Inline data compression reducing physical footprint on array'))
    lines.append(txt_row('  Replication      = Async or sync copy of volumes to secondary Apex or PowerStore'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-apex-saas-ops-backup',
    'docs/storage/dell/apex-storage-as-a-service/operations/backup-restore/index.md',
    'Apex STaaS Backup and Restore — snapshots, replication, DD integration, restore procedures',
)
def dell_apex_saas_ops_backup():
    """Dell Apex STaaS Backup and Restore — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Apex STaaS — Backup and Restore'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Apex backup: native snapshots, replication, and external backup target integration')))
    lines.append(R(bMid(IV_L, IV_R, 'Native snapshots: crash-consistent, scheduled; retained on the same array')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication: async volume replication to secondary Apex or PowerStore site')))
    lines.append(R(bMid(IV_L, IV_R, 'External backup: PowerProtect DD, Avamar, or third-party via NFS/iSCSI backup')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Snapshot (local) → replication (remote) → backup target → test restore quarterly'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Snapshots'), bMid(B2_L, B2_R, 'Replication'), bMid(B3_L, B3_R, 'External Backup'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Crash-consistent'), bMid(B2_L, B2_R, 'Async remote'), bMid(B3_L, B3_R, 'PowerProt. DD'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'App-consistent'), bMid(B2_L, B2_R, 'RPO minutes'), bMid(B3_L, B3_R, 'Avamar'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Scheduled policy'), bMid(B2_L, B2_R, 'Failover test'), bMid(B3_L, B3_R, 'Third-party'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Retention rules'), bMid(B2_L, B2_R, 'Reverse sync'), bMid(B3_L, B3_R, 'NFS mount'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Clone restore'), bMid(B2_L, B2_R, 'Site failback'), bMid(B3_L, B3_R, 'iSCSI target'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Test restores quarterly; document RTO/RPO; keep one restore tested per critical volume'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Method', 'RPO', 'RTO', 'Where', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Snapshot', 'Sched (hours)', 'Minutes', 'Same array', 'No off-site'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Replication', 'Minutes', 'Minutes/hrs', 'Remote site', 'Async lag'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['DD backup', 'Hours', 'Hours', 'DD appliance', 'Dedup ratio'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['App-consist.', 'Transaction', 'Minutes', 'VSS/quiesce', 'Agent needed'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: secondary Apex or PowerStore at DR site · DD appliance on-premises or hosted'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Crash-consistent = Snapshot taken without quiescing I/O; suitable for block volumes'))
    lines.append(txt_row('  App-consistent   = Snapshot taken with application quiesce (VSS/freeze); DB-safe'))
    lines.append(txt_row('  Async replication = Volume data replicated after write commit; lag = RPO in minutes'))
    lines.append(txt_row('  RPO              = Recovery Point Objective; maximum acceptable data loss time'))
    lines.append(txt_row('  RTO              = Recovery Time Objective; maximum acceptable restore duration'))
    lines.append(txt_row('  Reverse sync     = After failover, sync changes back to primary to prepare failback'))
    lines.append(txt_row('  DD Boost         = Dell Data Domain protocol; deduplication-aware backup streams'))
    lines.append(txt_row('  Retention policy = How many snapshots to keep; older ones auto-deleted when count met'))
    lines.append(txt_row('  Clone restore    = Create writable clone of snapshot; use as restored volume'))
    lines.append(txt_row('  VSS              = Volume Shadow Copy Service; Windows app-consistent snapshot mechanism'))
    lines.append(txt_row('  Dedup ratio      = DD data reduction ratio; typically 20:1 to 55:1 for backup data'))
    lines.append(txt_row('  Failback         = Return primary workload to original site after DR failover resolves'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-apex-saas-ops-install',
    'docs/storage/dell/apex-storage-as-a-service/operations/install-upgrade/index.md',
    'Apex STaaS Onboarding — site prep, Dell install, network config, host connect, go-live',
)
def dell_apex_saas_ops_install():
    """Dell Apex STaaS Install/Onboarding — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Apex STaaS — Onboarding'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Apex onboarding: site preparation, Dell hardware install, host connection, go-live')))
    lines.append(R(bMid(IV_L, IV_R, 'Site prep (customer): rack space, power (kVA), cooling, network drops, OOB access')))
    lines.append(R(bMid(IV_L, IV_R, 'Dell FSE installs hardware, initialises array, deploys SCG; customer does NOT touch HW')))
    lines.append(R(bMid(IV_L, IV_R, 'Customer: configure iSCSI VLANs or FC zoning, install multipath, connect hosts')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Contract → site prep → Dell install → network config → host connect → validate → go-live'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Site Prep'), bMid(B2_L, B2_R, 'Dell Install'), bMid(B3_L, B3_R, 'Host Connect'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Rack space'), bMid(B2_L, B2_R, 'Rack and cable'), bMid(B3_L, B3_R, 'iSCSI VLAN'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Power (kVA)'), bMid(B2_L, B2_R, 'Array init'), bMid(B3_L, B3_R, 'FC zoning'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cooling'), bMid(B2_L, B2_R, 'SCG deploy'), bMid(B3_L, B3_R, 'Multipath'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Network drops'), bMid(B2_L, B2_R, 'CloudIQ link'), bMid(B3_L, B3_R, 'Initiator reg.'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'OOB management'), bMid(B2_L, B2_R, 'Apex Console'), bMid(B3_L, B3_R, 'Test I/O'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Apex expands (scale-out) are also Dell-managed; customer opens SR; Dell adds capacity'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Phase', 'Owner', 'Task', 'Milestone', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Site prep', 'Customer', 'Rack/power', 'Ready cert.', 'Before ship'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Install', 'Dell FSE', 'HW + init', 'SCG green', '1–2 days'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Network', 'Customer', 'VLAN/zone', 'Ping passes', 'iSCSI or FC'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Host', 'Customer', 'MPIO + test', 'I/O verified', 'All paths'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: 2U or 4U rack space · dedicated 20–30A circuits · 10/25/100GbE or 16/32Gb FC'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Site prep       = Customer prerequisites: power, cooling, rack, network before Dell ships'))
    lines.append(txt_row('  Ready cert.     = Customer signs off that site meets Dell physical requirements'))
    lines.append(txt_row('  FSE             = Field Service Engineer; Dell technician performing on-site work'))
    lines.append(txt_row('  Array init      = Dell initialises OS, pools, networking on hardware; customer not involved'))
    lines.append(txt_row('  SCG deploy      = Dell installs Secure Connect Gateway VM; enables CloudIQ and SupportAssist'))
    lines.append(txt_row('  CloudIQ link    = SCG establishes outbound HTTPS to Dell cloud; confirmed by FSE'))
    lines.append(txt_row('  iSCSI VLAN      = Customer creates dedicated VLAN; configures IP addresses for array ports'))
    lines.append(txt_row('  FC zoning       = Customer creates zones in FC fabric: HBA WWN + array port WWN per zone'))
    lines.append(txt_row('  Initiator reg.  = Register host IQN/WWN in Apex Console; required before volume mapping'))
    lines.append(txt_row('  Multipath test  = Verify active paths; pull one cable; I/O must continue on remaining path'))
    lines.append(txt_row('  Scale-out       = Adding capacity to existing Apex subscription via Dell SR; not self-service'))
    lines.append(txt_row('  OOB management  = Out-of-band access to array iDRAC/iDRAC9; Dell-managed; not customer access'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-apex-saas-ops-procedures',
    'docs/storage/dell/apex-storage-as-a-service/operations/procedures/index.md',
    'Apex STaaS Procedures — create/map volumes, NFS exports, snapshots, capacity expansion',
)
def dell_apex_saas_ops_procedures():
    """Dell Apex STaaS Operational Procedures — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Apex STaaS — Operational Procedures'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Apex procedures: create and map volumes, NFS exports, snapshots, capacity expansion')))
    lines.append(R(bMid(IV_L, IV_R, 'Volume create: Apex Console > Storage > Volumes > Create; set size and tier')))
    lines.append(R(bMid(IV_L, IV_R, 'NFS export: Apex Console > Storage > File > Create Share; set client access list')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity expand: raise SR in Apex Console; Dell processes and provisions within SLA')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Create volume → map host → host rescan → format/mount → monitor → snapshot schedule'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Block Volumes'), bMid(B2_L, B2_R, 'File (NFS/SMB)'), bMid(B3_L, B3_R, 'Data Services'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Create volume'), bMid(B2_L, B2_R, 'Create share'), bMid(B3_L, B3_R, 'Create snap'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Set size/tier'), bMid(B2_L, B2_R, 'Set client ACL'), bMid(B3_L, B3_R, 'Set schedule'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Map to host'), bMid(B2_L, B2_R, 'Mount on host'), bMid(B3_L, B3_R, 'Clone snap'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Host rescan'), bMid(B2_L, B2_R, 'Test write'), bMid(B3_L, B3_R, 'Restore clone'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Format/mount'), bMid(B2_L, B2_R, 'Expand share'), bMid(B3_L, B3_R, 'Delete snap'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  All capacity expansion requires a Dell SR; planned changes need lead time (days)'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Procedure', 'Portal path', 'Key step', 'Verify', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Create vol', 'Storage>Vols', 'Size + tier', 'LUN visible', 'Thin default'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Map host', 'Storage>Hosts', 'IQN/WWN', 'Host LUN', 'Rescan bus'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['NFS share', 'Storage>File', 'Client CIDR', 'Mount test', 'NFS v3/v4'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Snap policy', 'Data Svc>Snap', 'Freq+retain', 'Snap listed', 'No quota'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: host HBA/NIC and OS multipath · NFS client on Linux/VMware · iSCSI initiator'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Host rescan      = OS command to detect new LUNs: iscsiadm rescan / hbacmd; or vCenter rescan'))
    lines.append(txt_row('  Client ACL       = NFS share access list; specify host IP or CIDR; rw or ro'))
    lines.append(txt_row('  Thin default     = Apex volumes are thin-provisioned by default; physical use grows on write'))
    lines.append(txt_row('  LUN visible      = After mapping, host must see LUN via multipath; check multipathd/mpio'))
    lines.append(txt_row('  Snap policy      = Defines frequency (hourly/daily/weekly) and retention count'))
    lines.append(txt_row('  Clone from snap  = Create writable volume from snapshot; mount as separate device'))
    lines.append(txt_row('  Capacity expand  = Open SR specifying current committed + desired new committed size'))
    lines.append(txt_row('  NFS v4           = NFSv4 recommended for Kerberos security and improved locking'))
    lines.append(txt_row('  IQN              = iSCSI Qualified Name; unique identifier for iSCSI initiator (host HBA)'))
    lines.append(txt_row('  WWN              = World Wide Name; unique FC port identifier; used in FC zoning and maps'))
    lines.append(txt_row('  Expand share     = Increase NFS share quota; non-disruptive in most cases'))
    lines.append(txt_row('  iscsiadm         = Linux iSCSI management tool; discover, login, and rescan iSCSI targets'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-apex-saas-security',
    'docs/storage/dell/apex-storage-as-a-service/security/index.md',
    'Apex STaaS Security — RBAC, encryption at rest/transit, access control, audit logging',
)
def dell_apex_saas_security():
    """Dell Apex STaaS Security — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Apex STaaS — Security'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Apex security: RBAC roles, AES-256 encryption at rest, CHAP/TLS in transit, audit')))
    lines.append(R(bMid(IV_L, IV_R, 'RBAC: Account Admin (billing/users), Storage Admin (volumes), Reader (view only)')))
    lines.append(R(bMid(IV_L, IV_R, 'Encryption at rest: AES-256 enabled by default on all arrays; no performance cost')))
    lines.append(R(bMid(IV_L, IV_R, 'In-transit: iSCSI CHAP, NFS Kerberos, HTTPS for Apex Console and REST API')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Auth (SSO/SAML) → RBAC role → portal access → storage ops → audit log export'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Access Control'), bMid(B2_L, B2_R, 'Encryption'), bMid(B3_L, B3_R, 'Audit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RBAC roles'), bMid(B2_L, B2_R, 'AES-256 rest'), bMid(B3_L, B3_R, 'Apex audit log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SSO / SAML'), bMid(B2_L, B2_R, 'iSCSI CHAP'), bMid(B3_L, B3_R, 'CloudIQ events'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MFA required'), bMid(B2_L, B2_R, 'NFS Kerberos'), bMid(B3_L, B3_R, 'User actions'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'API OAuth 2.0'), bMid(B2_L, B2_R, 'TLS 1.2+ API'), bMid(B3_L, B3_R, 'Retention 90d'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'IP allowlist'), bMid(B2_L, B2_R, 'FC port sec.'), bMid(B3_L, B3_R, 'SIEM export'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Dell support access is break-glass; customer must explicitly grant; logged in audit'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Control', 'Mechanism', 'Scope', 'Verify', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Auth', 'SSO/SAML+MFA', 'Console', 'Login test', 'Local fallback'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['AuthZ', 'RBAC role', 'Per resource', 'Func. test', 'Least priv.'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Encrypt rest', 'AES-256', 'All data', 'Always on', 'No config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Encrypt tx', 'CHAP/TLS', 'iSCSI/API', 'CHAP active', 'Kerberos NFS'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: array self-encrypting drives (SED) · FC fabric binding · iSCSI CHAP per host'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  RBAC           = Role-Based Access Control; Apex Console roles control portal operations'))
    lines.append(txt_row('  Account Admin  = Manages Apex subscription, billing, and user accounts; no storage ops'))
    lines.append(txt_row('  Storage Admin  = Creates/deletes volumes, maps hosts, manages snapshots; no billing'))
    lines.append(txt_row('  Reader         = Read-only access to capacity, performance, and configuration data'))
    lines.append(txt_row('  SSO/SAML       = Corporate identity provider integration; single sign-on to Apex Console'))
    lines.append(txt_row('  MFA            = Multi-Factor Authentication; required for all Apex Console users'))
    lines.append(txt_row('  OAuth 2.0      = Token-based API authentication; used for automation and integrations'))
    lines.append(txt_row('  AES-256        = Advanced Encryption Standard 256-bit; used for self-encrypting drives'))
    lines.append(txt_row('  iSCSI CHAP     = Challenge Handshake Auth Protocol; authenticates iSCSI host sessions'))
    lines.append(txt_row('  NFS Kerberos   = Kerberos-based authentication for NFS mounts; sec=krb5 mount option'))
    lines.append(txt_row('  Break-glass    = Dell emergency support access; requires customer approval; fully audited'))
    lines.append(txt_row('  SIEM export    = Audit log forwarding to customer SIEM (Splunk, QRadar) for retention'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-apex-saas-security-access',
    'docs/storage/dell/apex-storage-as-a-service/security/access-control/index.md',
    'Apex STaaS Access Control — RBAC roles, API tokens, IP allowlists, Dell support access',
)
def dell_apex_saas_security_access():
    """Dell Apex STaaS Access Control — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Apex STaaS — Access Control'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Apex access control: RBAC roles, SSO, API tokens, IP allowlists, Dell support')))
    lines.append(R(bMid(IV_L, IV_R, 'Three portal roles: Account Admin, Storage Admin, Reader; assign via Apex Console')))
    lines.append(R(bMid(IV_L, IV_R, 'API access: OAuth 2.0 tokens scoped to read or read-write; rotate quarterly')))
    lines.append(R(bMid(IV_L, IV_R, 'IP allowlist: restrict Apex Console access to corporate IP ranges or VPN egress')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  SSO login → RBAC role check → console or API access → action logged → audit reviewed'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Portal Roles'), bMid(B2_L, B2_R, 'API Access'), bMid(B3_L, B3_R, 'Restrictions'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Account Admin'), bMid(B2_L, B2_R, 'OAuth 2.0 token'), bMid(B3_L, B3_R, 'IP allowlist'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Storage Admin'), bMid(B2_L, B2_R, 'Scoped r/rw'), bMid(B3_L, B3_R, 'MFA enforce'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Reader'), bMid(B2_L, B2_R, 'Token rotation'), bMid(B3_L, B3_R, 'SSO required'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Least privilege'), bMid(B2_L, B2_R, 'API audit log'), bMid(B3_L, B3_R, 'Dell break-glass'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Review quarterly'), bMid(B2_L, B2_R, 'Revoke stale'), bMid(B3_L, B3_R, 'Customer approves'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Review user list quarterly; revoke inactive accounts and rotate API tokens'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Role', 'Can do', 'Cannot do', 'Assign via', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Acct Admin', 'Users/billing', 'Storage ops', 'Apex Console', 'Separate duty'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Storage Admin', 'Vols/snaps', 'Billing/users', 'Apex Console', 'Day-2 ops'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Reader', 'View metrics', 'Any change', 'Apex Console', 'Audit/reports'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['API token', 'Automation', 'Portal login', 'Apex API', 'Rotate 90 days'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: corporate IdP reachable by Apex Console · VPN for IP allowlist enforcement'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Account Admin  = Top-level Apex Console role; manages subscriptions, billing, and users'))
    lines.append(txt_row('  Storage Admin  = Day-to-day storage ops; cannot modify billing or create users'))
    lines.append(txt_row('  Reader         = View-only; suitable for monitoring, auditing, and management review'))
    lines.append(txt_row('  Least privilege = Assign minimum role required for job function; review access regularly'))
    lines.append(txt_row('  OAuth 2.0      = Token issued by Apex for API clients; set shortest practical expiry'))
    lines.append(txt_row('  Token rotation = Replace API tokens quarterly; revoke old token immediately after'))
    lines.append(txt_row('  IP allowlist   = Apex Console setting to permit logins from specified IP ranges only'))
    lines.append(txt_row('  MFA enforce    = Require second factor for all console logins; hardware or TOTP'))
    lines.append(txt_row('  Break-glass    = Dell emergency access; customer must grant in Apex Console; audited'))
    lines.append(txt_row('  Separation     = Account Admin and Storage Admin roles should be different people'))
    lines.append(txt_row('  Stale tokens   = API tokens from departed staff or unused integrations; revoke promptly'))
    lines.append(txt_row('  Quarterly review = Check all active users and API tokens; remove unneeded access'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-apex-saas-security-auth',
    'docs/storage/dell/apex-storage-as-a-service/security/authentication/index.md',
    'Apex STaaS Authentication — SSO/SAML, MFA, iSCSI CHAP, NFS Kerberos, API OAuth',
)
def dell_apex_saas_security_auth():
    """Dell Apex STaaS Authentication — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Apex STaaS — Authentication'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Apex authentication: SSO/SAML for portal, CHAP for iSCSI, Kerberos for NFS')))
    lines.append(R(bMid(IV_L, IV_R, 'Portal: SSO via SAML 2.0 (Okta, Azure AD, AD FS); MFA required for all users')))
    lines.append(R(bMid(IV_L, IV_R, 'iSCSI: CHAP mutual authentication per initiator; secret stored in Apex Console')))
    lines.append(R(bMid(IV_L, IV_R, 'NFS: Kerberos (sec=krb5) recommended; AUTH_SYS (IP-based) as minimum baseline')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  User → SSO IdP → SAML assertion → Apex Console → RBAC role → storage operation'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Portal Auth'), bMid(B2_L, B2_R, 'Storage Auth'), bMid(B3_L, B3_R, 'API Auth'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SAML 2.0 SSO'), bMid(B2_L, B2_R, 'iSCSI CHAP'), bMid(B3_L, B3_R, 'OAuth 2.0'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MFA (TOTP/HW)'), bMid(B2_L, B2_R, 'NFS Kerberos'), bMid(B3_L, B3_R, 'Bearer token'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Local admin'), bMid(B2_L, B2_R, 'FC port sec.'), bMid(B3_L, B3_R, 'HTTPS only'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Session timeout'), bMid(B2_L, B2_R, 'Auth_SYS (min)'), bMid(B3_L, B3_R, 'Token expiry'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Audit login'), bMid(B2_L, B2_R, 'Initiator IQN'), bMid(B3_L, B3_R, 'Rotate 90d'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Always enable CHAP for iSCSI; avoid AUTH_SYS for sensitive NFS shares'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Method', 'Protocol', 'Scope', 'Config path', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['SAML SSO', 'SAML 2.0', 'Portal users', 'Apex>SSO', 'IdP metadata'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['MFA', 'TOTP/FIDO2', 'All users', 'Apex>Security', 'Mandatory'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['CHAP', 'iSCSI CHAP', 'Each host', 'Apex>Hosts', 'Bidirectional'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['OAuth 2.0', 'Bearer token', 'API clients', 'Apex>API keys', '90-day rotate'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: corporate IdP (Okta/AD FS) · KDC for Kerberos NFS · NTP sync required'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SAML 2.0       = Security Assertion Markup Language; IdP issues signed assertions to Apex'))
    lines.append(txt_row('  SSO            = Single Sign-On; user logs in once via IdP; Apex accepts SAML token'))
    lines.append(txt_row('  MFA            = Multi-Factor Authentication; TOTP app or hardware key (FIDO2)'))
    lines.append(txt_row('  Local admin    = Fallback Apex account; used only if SSO is unavailable'))
    lines.append(txt_row('  CHAP           = Challenge Handshake; iSCSI host sends hashed secret to authenticate'))
    lines.append(txt_row('  Bidirectional CHAP = Both host and array authenticate each other; strongest iSCSI auth'))
    lines.append(txt_row('  NFS Kerberos   = sec=krb5 mount option; requires KDC, keytab on NFS client host'))
    lines.append(txt_row('  AUTH_SYS       = NFS trust by UID/GID; no real auth; avoid for sensitive data'))
    lines.append(txt_row('  FC port sec.   = FC switch restricts which pWWNs can login; configured on switch'))
    lines.append(txt_row('  OAuth 2.0      = REST API authentication; scoped bearer token; HTTPS transport only'))
    lines.append(txt_row('  Session timeout = Apex Console auto-logs out idle sessions; configure ≤15 min'))
    lines.append(txt_row('  KDC            = Kerberos Key Distribution Centre; required for NFS Kerberos auth'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-apex-saas-security-encryption',
    'docs/storage/dell/apex-storage-as-a-service/security/encryption/index.md',
    'Apex STaaS Encryption — AES-256 at rest (SED), iSCSI CHAP, NFS Kerberos, TLS in transit',
)
def dell_apex_saas_security_encryption():
    """Dell Apex STaaS Encryption — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Apex STaaS — Encryption'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Apex encryption: AES-256 at rest on all arrays; TLS 1.2+ for portal and API')))
    lines.append(R(bMid(IV_L, IV_R, 'At rest: self-encrypting drives (SED); AES-256-XTS; always on, no user config')))
    lines.append(R(bMid(IV_L, IV_R, 'In transit: iSCSI CHAP session auth; NFS sec=krb5; HTTPS/TLS for management')))
    lines.append(R(bMid(IV_L, IV_R, 'Key management: Dell-managed by default; customer KMIP server optional')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Write → SED encrypts inline → AES-256 stored → read → SED decrypts → host receives'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'At Rest'), bMid(B2_L, B2_R, 'In Transit'), bMid(B3_L, B3_R, 'Key Mgmt'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'AES-256-XTS'), bMid(B2_L, B2_R, 'TLS 1.2+'), bMid(B3_L, B3_R, 'Dell managed'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SED drives'), bMid(B2_L, B2_R, 'iSCSI CHAP'), bMid(B3_L, B3_R, 'KMIP optional'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Always on'), bMid(B2_L, B2_R, 'NFS Kerberos'), bMid(B3_L, B3_R, 'Key rotation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No perf impact'), bMid(B2_L, B2_R, 'HTTPS portal'), bMid(B3_L, B3_R, 'FIPS 140-2'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Drive destruct'), bMid(B2_L, B2_R, 'Cipher TLS 1.3'), bMid(B3_L, B3_R, 'Audit keys'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  SED: cryptographic erase on drive decommission; no data recovery risk when drive replaced'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Layer', 'Algorithm', 'Enabled by', 'Verify', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['At rest', 'AES-256-XTS', 'Default', 'Console view', 'SED hardware'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['iSCSI tx', 'CHAP auth', 'Per host', 'CHAP secret', 'Not payload'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['NFS tx', 'Kerberos', 'Mount option', 'sec=krb5', 'KDC needed'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Mgmt tx', 'TLS 1.2+', 'Always on', 'TLS cert', 'Portal/API'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SED drives in array · iSCSI network switch (not inspecting payload) · KDC server'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SED            = Self-Encrypting Drive; AES-256 hardware encryption on-chip; no CPU overhead'))
    lines.append(txt_row('  AES-256-XTS    = XEX-based tweaked codebook mode; NIST-approved for storage encryption'))
    lines.append(txt_row('  Always on      = Apex SED encryption cannot be disabled; all data encrypted at write'))
    lines.append(txt_row('  Crypto erase   = Reset SED encryption key; instantly renders all data unreadable'))
    lines.append(txt_row('  KMIP           = Key Management Interoperability Protocol; customer-managed key server'))
    lines.append(txt_row('  FIPS 140-2     = US encryption standard; Apex optionally runs FIPS-validated mode'))
    lines.append(txt_row('  CHAP           = iSCSI host authentication only; does NOT encrypt I/O payload'))
    lines.append(txt_row('  Kerberos       = NFS data integrity/confidentiality; sec=krb5i adds integrity signing'))
    lines.append(txt_row('  TLS 1.2+       = Minimum TLS version for Apex Console and REST API endpoints'))
    lines.append(txt_row('  Key rotation   = Periodic re-encryption of SED keys; Dell-managed on schedule'))
    lines.append(txt_row('  FIPS 140-2 L2  = Validated cryptographic modules in Apex arrays; regulatory compliance'))
    lines.append(txt_row('  Drive destruct = Physical destruction of retired SEDs; crypto erase is equivalent'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-apex-saas-security-hardening',
    'docs/storage/dell/apex-storage-as-a-service/security/hardening/index.md',
    'Apex STaaS Hardening — disable unused protocols, network segmentation, firmware, audit',
)
def dell_apex_saas_security_hardening():
    """Dell Apex STaaS Hardening — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Apex STaaS — Security Hardening'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Apex hardening: disable unused protocols, isolate storage VLAN, enforce TLS, audit')))
    lines.append(R(bMid(IV_L, IV_R, 'Network: storage traffic on dedicated VLAN; no routing between storage and user VLANs')))
    lines.append(R(bMid(IV_L, IV_R, 'Protocols: disable Telnet, NFS AUTH_SYS for sensitive data, unused iSCSI ports')))
    lines.append(R(bMid(IV_L, IV_R, 'Firmware: Dell manages array firmware; customer must not block SupportAssist access')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Baseline → disable unused protocols → network isolation → audit config → review quarterly'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Protocol'), bMid(B2_L, B2_R, 'Network'), bMid(B3_L, B3_R, 'Firmware'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Disable Telnet'), bMid(B2_L, B2_R, 'Storage VLAN'), bMid(B3_L, B3_R, 'Dell managed'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Enforce TLS 1.2+'), bMid(B2_L, B2_R, 'No user VLAN'), bMid(B3_L, B3_R, 'SCG allows'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CHAP on iSCSI'), bMid(B2_L, B2_R, 'iSCSI VLAN ACL'), bMid(B3_L, B3_R, 'Auto patches'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Limit NFS ver.'), bMid(B2_L, B2_R, 'FC zone tight'), bMid(B3_L, B3_R, 'CVE tracking'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Disable HTTP'), bMid(B2_L, B2_R, 'OOB separate'), bMid(B3_L, B3_R, 'Audit firmware'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Dell firmware updates are automatic via SupportAssist; never block SCG egress to Dell'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Hardening', 'Action', 'Verify', 'Risk if skip', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['VLAN isolate', 'Dedicated VLAN', 'No cross-ping', 'Lateral move', 'ACL on switch'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['CHAP', 'Enable per host', 'CHAP active', 'Unauth iSCSI', 'Bidirectional'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['TLS enforce', 'Disable TLS<1.2', 'sslyze test', 'Weak cipher', 'Portal/API'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['FC zoning', 'Single init/tgt', 'show zone', 'Broad access', 'One zone/pair'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: switch VLAN ACLs · FC fabric binding + port security · iSCSI ACL on switches'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Storage VLAN   = Dedicated VLAN carrying only iSCSI or NFS; ACL blocks all other hosts'))
    lines.append(txt_row('  OOB separate   = Array management (iDRAC) on separate management VLAN; not in storage VLAN'))
    lines.append(txt_row('  FC zone tight  = One zone per initiator-target pair; not broad zones spanning all targets'))
    lines.append(txt_row('  TLS 1.2+       = Apex Console only accepts TLS 1.2 and 1.3; disable older cipher suites'))
    lines.append(txt_row('  Telnet         = Cleartext protocol; ensure disabled on all Apex Console endpoints'))
    lines.append(txt_row('  HTTP disable   = Force HTTPS redirect on Apex Console; HTTP should return 301'))
    lines.append(txt_row('  CVE tracking   = Dell publishes DSA (Dell Security Advisories); subscribe and track'))
    lines.append(txt_row('  SCG egress     = Allow outbound HTTPS from SCG VM to Dell cloud for SupportAssist'))
    lines.append(txt_row('  Lateral move   = If storage VLAN is flat, compromise of one host risks all volumes'))
    lines.append(txt_row('  iSCSI VLAN ACL = Switch ACL permitting only registered host IPs to reach array iSCSI ports'))
    lines.append(txt_row('  DSA            = Dell Security Advisory; CVE notifications for Dell product vulnerabilities'))
    lines.append(txt_row('  Audit config   = Monthly review of VLAN, zone, and CHAP settings for drift'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-apex-saas-troubleshooting',
    'docs/storage/dell/apex-storage-as-a-service/troubleshooting/index.md',
    'Apex STaaS Troubleshooting — host path, performance, capacity alerts, CloudIQ errors',
)
def dell_apex_saas_troubleshooting():
    """Dell Apex STaaS Troubleshooting — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Apex STaaS — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Apex troubleshooting: host path failures, performance issues, capacity alerts')))
    lines.append(R(bMid(IV_L, IV_R, 'Host path: check multipath status, iSCSI sessions, FC logins, VLAN reachability')))
    lines.append(R(bMid(IV_L, IV_R, 'Performance: check CloudIQ IOPS/latency graphs; identify noisy-neighbour volumes')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity: CloudIQ alert at 80% committed; open SR to expand before hitting burst')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Symptom → CloudIQ health → host path check → array alert → SR to Dell → resolve'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Connectivity'), bMid(B2_L, B2_R, 'Performance'), bMid(B3_L, B3_R, 'Capacity'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Host path down'), bMid(B2_L, B2_R, 'High latency'), bMid(B3_L, B3_R, 'Near-full alert'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'iSCSI session'), bMid(B2_L, B2_R, 'IOPS throttle'), bMid(B3_L, B3_R, 'Burst billing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FC login fail'), bMid(B2_L, B2_R, 'Queue depth'), bMid(B3_L, B3_R, 'Expand SR'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VLAN mismatch'), bMid(B2_L, B2_R, 'Noisy volume'), bMid(B3_L, B3_R, 'Thin reclaim'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCG offline'), bMid(B2_L, B2_R, 'Slow rebuild'), bMid(B3_L, B3_R, 'Forecast review'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Hardware faults are Dell responsibility; open P1 SR immediately for controller alarms'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Symptom', 'First check', 'Tool', 'Resolution', 'Escalation'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Path down', 'multipath -ll', 'Host OS', 'Fix VLAN/zone', 'Dell SR P2'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['High latency', 'CloudIQ graph', 'CloudIQ', 'Throttle/move', 'Dell SR P2'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Capacity 80%', 'Usage report', 'Apex Console', 'Open expand SR', 'P3 SR'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['SCG offline', 'SCG VM status', 'SCG console', 'Restart SCG VM', 'Dell SR P3'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: multipath paths (cable, SFP, switch) · iSCSI VLAN tagging · FC zone check'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  multipath -ll   = Linux command; shows all paths to each storage device with status'))
    lines.append(txt_row('  Path down       = Multipath shows one path in "failed" state; I/O continues on other path'))
    lines.append(txt_row('  iSCSI session   = Active TCP connection between host initiator and array iSCSI target'))
    lines.append(txt_row('  FC login fail   = Host HBA cannot FLOGI to fabric; check zoning and WWN registration'))
    lines.append(txt_row('  IOPS throttle   = Array QoS limiting IOPS on a volume; shown as max-rate in CloudIQ'))
    lines.append(txt_row('  Noisy volume    = High-I/O volume consuming array resources impacting other volumes'))
    lines.append(txt_row('  Queue depth     = Outstanding I/O requests per path; excessive depth causes latency'))
    lines.append(txt_row('  SCG offline     = Secure Connect Gateway VM stopped; CloudIQ data gap; no SupportAssist'))
    lines.append(txt_row('  Thin reclaim    = UNMAP/TRIM commands return unused thin-provisioned blocks to pool'))
    lines.append(txt_row('  Capacity SR     = Service Request to expand Apex committed tier; include usage data'))
    lines.append(txt_row('  P1/P2 severity  = P1=production down; P2=degraded; drives Dell response SLA'))
    lines.append(txt_row('  Controller alarm = CloudIQ or SupportAssist alert on controller hardware; P1 SR now'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-apex-saas-troubleshooting-issues',
    'docs/storage/dell/apex-storage-as-a-service/troubleshooting/common-issues/index.md',
    'Apex STaaS Common Issues — path failures, CHAP errors, NFS mount, capacity, SCG offline',
)
def dell_apex_saas_troubleshooting_issues():
    """Dell Apex STaaS Common Issues — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Apex STaaS — Common Issues'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Common Apex issues: path offline, CHAP mismatch, NFS mount error, SCG gap')))
    lines.append(R(bMid(IV_L, IV_R, 'Path offline: cable/SFP fault → check multipath -ll; fix physical then rescan')))
    lines.append(R(bMid(IV_L, IV_R, 'CHAP mismatch: secret differs between host and array; re-enter in both places')))
    lines.append(R(bMid(IV_L, IV_R, 'NFS stale mount: server restarted; umount -l and remount; check /etc/fstab')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Issue identified → collect logs → isolate layer (physical/network/config) → resolve'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Block Issues'), bMid(B2_L, B2_R, 'File Issues'), bMid(B3_L, B3_R, 'Portal Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Path offline'), bMid(B2_L, B2_R, 'NFS mount fail'), bMid(B3_L, B3_R, 'SCG offline'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CHAP reject'), bMid(B2_L, B2_R, 'Stale handle'), bMid(B3_L, B3_R, 'CloudIQ gap'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LUN not seen'), bMid(B2_L, B2_R, 'Permission deny'), bMid(B3_L, B3_R, 'Console slow'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MPIO asymm.'), bMid(B2_L, B2_R, 'NFS timeout'), bMid(B3_L, B3_R, 'SR not created'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Snap failure'), bMid(B2_L, B2_R, 'Quota exceed'), bMid(B3_L, B3_R, 'Billing error'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  For any unresolved issue after 30 mins: open Apex SR with logs before escalating'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Issue', 'First check', 'Command', 'Fix', 'Escalate'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Path offline', 'Cable/SFP', 'multipath -ll', 'Fix physical', 'Dell SR P2'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['CHAP reject', 'Secret match', 'iscsiadm log', 'Re-enter CHAP', 'Apex Console'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['NFS fail', 'showmount -e', 'mount output', 'Re-mount', 'Check export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['SCG offline', 'SCG VM state', 'SCG UI', 'Restart VM', 'Dell SR P3'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SFP Tx/Rx power · Ethernet cable · FC cable · switch port state'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  multipath -ll   = Shows all device paths with status (active/failed/ready)'))
    lines.append(txt_row('  CHAP reject     = Array refuses iSCSI login because CHAP secrets do not match'))
    lines.append(txt_row('  LUN not seen    = Host does not see volume after mapping; run iscsiadm rescan'))
    lines.append(txt_row('  MPIO asymm.     = All I/O on one path; other paths not load-balanced; check policy'))
    lines.append(txt_row('  NFS stale handle = Cached file handle invalid after server restart; unmount and remount'))
    lines.append(txt_row('  NFS permission  = Host IP not in export access list; add CIDR to share config'))
    lines.append(txt_row('  Quota exceed    = NFS share quota reached; expand in Apex Console or clean data'))
    lines.append(txt_row('  SCG offline     = VM stopped or network issue; restart VM; verify outbound HTTPS works'))
    lines.append(txt_row('  CloudIQ gap     = Historical data missing due to SCG outage; non-impacting but fix SCG'))
    lines.append(txt_row('  Snap failure    = Snapshot policy fails; check available pool space (burst capacity)'))
    lines.append(txt_row('  showmount -e    = Show NFS exports available from server; verify export exists and ACL'))
    lines.append(txt_row('  iscsiadm log    = iSCSI daemon log showing login attempts and auth failures'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-apex-saas-troubleshooting-escalation',
    'docs/storage/dell/apex-storage-as-a-service/troubleshooting/escalation/index.md',
    'Apex STaaS Escalation — severity levels, what to collect, SR workflow, TAC escalation',
)
def dell_apex_saas_troubleshooting_escalation():
    """Dell Apex STaaS Escalation — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Apex STaaS — Escalation'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Apex escalation: severity triage, SR creation, log collection, TAC engagement')))
    lines.append(R(bMid(IV_L, IV_R, 'P1 (production down): call Dell immediately + open SR; 4-hour response SLA')))
    lines.append(R(bMid(IV_L, IV_R, 'P2 (degraded): open SR online; 8-hour response; attach multipath and CloudIQ logs')))
    lines.append(R(bMid(IV_L, IV_R, 'Collect before calling: host OS logs, CloudIQ bundle, SCG diagnostics')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Triage severity → collect logs → open SR → Dell responds → RCA → preventive action'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Severity'), bMid(B2_L, B2_R, 'What to Collect'), bMid(B3_L, B3_R, 'SR Process'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'P1: prod down'), bMid(B2_L, B2_R, 'multipath -ll'), bMid(B3_L, B3_R, 'Apex Console SR'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'P2: degraded'), bMid(B2_L, B2_R, 'CloudIQ bundle'), bMid(B3_L, B3_R, 'Phone + online'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'P3: limited'), bMid(B2_L, B2_R, 'dmesg / syslog'), bMid(B3_L, B3_R, 'Online SR only'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'P4: question'), bMid(B2_L, B2_R, 'SCG diagnostic'), bMid(B3_L, B3_R, 'Community/chat'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Escalate P1'), bMid(B2_L, B2_R, 'CloudIQ events'), bMid(B3_L, B3_R, 'Manager escalate'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Always note time of issue, affected volumes, and host count when opening SR'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Severity', 'Criteria', 'SLA respond', 'Contact', 'Escalation'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['P1', 'Prod down', '4 hours', 'Phone + SR', 'Exec if >4h'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['P2', 'Degraded', '8 hours', 'SR + phone', 'Mgr if >8h'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['P3', 'Limited imp.', 'Next bus. day', 'SR online', 'SR comment'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['P4', 'Question', 'Best effort', 'Portal/chat', 'None needed'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: collect cable/SFP photos for P1 hardware failures · note rack location'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  P1 severity    = Production storage completely unavailable; call Dell 24x7 phone line'))
    lines.append(txt_row('  P2 severity    = Production degraded (slow, one path lost); open SR + follow up by phone'))
    lines.append(txt_row('  P3 severity    = Non-production or isolated issue; online SR; next business day response'))
    lines.append(txt_row('  P4 severity    = General question or feature request; community or chat; no SLA'))
    lines.append(txt_row('  CloudIQ bundle = Downloadable diagnostic package from CloudIQ; attach to SR'))
    lines.append(txt_row('  SCG diagnostic = SCG built-in log collection; download from SCG web UI'))
    lines.append(txt_row('  dmesg          = Linux kernel ring buffer; shows SCSI errors, path events, I/O failures'))
    lines.append(txt_row('  syslog         = System log; contains iSCSI daemon, multipath, and storage driver events'))
    lines.append(txt_row('  Manager escalate = Requesting Dell TAC manager involvement if SLA is not being met'))
    lines.append(txt_row('  RCA            = Root Cause Analysis; Dell provides written cause and prevention plan'))
    lines.append(txt_row('  Exec escalation = For P1 unresolved >4h; request to Dell account team for exec attention'))
    lines.append(txt_row('  SR number      = Service Request ticket; record and share with all team members involved'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cloudiq', 'docs/storage/dell/cloudiq/index.md',
            'Dell CloudIQ — AI-powered cloud storage management platform')
def dell_cloudiq():
    """Dell CloudIQ — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ: Dell SaaS platform delivering AIOps-based storage health and performance analytics')))
    lines.append(R(bMid(IV_L, IV_R, 'Collects telemetry via Secure Connect Gateway (SCG); health scores, alerts, forecasts')))
    lines.append(R(bMid(IV_L, IV_R, 'Supports PowerStore, PowerMax, Unity XT, PowerScale, Data Domain, and legacy VMAX arrays')))
    lines.append(R(bMid(IV_L, IV_R, 'Proactive recommendations, capacity forecasting, and firmware advisory automation')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Array telemetry → SCG relay → CloudIQ SaaS → health scores, alerts, recommendations'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Analytics Engine'), bMid(B2_L, B2_R, 'Array Support'), bMid(B3_L, B3_R, 'Cloud Services'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Health scoring'), bMid(B2_L, B2_R, 'PowerStore'), bMid(B3_L, B3_R, 'SaaS delivery'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Anomaly detection'), bMid(B2_L, B2_R, 'PowerMax / VMAX'), bMid(B3_L, B3_R, 'SCG relay'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity forecast'), bMid(B2_L, B2_R, 'Unity XT'), bMid(B3_L, B3_R, 'REST API'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Perf analytics'), bMid(B2_L, B2_R, 'PowerScale'), bMid(B3_L, B3_R, 'Webhook alerts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Firmware advisory'), bMid(B2_L, B2_R, 'Data Domain'), bMid(B3_L, B3_R, 'Partner portal'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Dell hosts CloudIQ cloud-side; SCG appliance or VM per site relays array telemetry outbound'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Component', 'Role', 'Location', 'Protocol', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Arrays', 'Data source', 'On-premises', 'REST/SCSI', 'Any Dell model'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['SCG', 'Relay agent', 'On-premises', 'HTTPS 443', 'VM or appliance'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['CloudIQ', 'Analytics SaaS', 'Dell cloud', 'HTTPS/REST', 'Multi-tenant'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Consumers', 'Dashboard/API', 'Browser/app', 'HTTPS/OAuth', 'Ops teams'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SCG VM or appliance on management LAN per site · outbound 443 to cloudiq.dell.com'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  CloudIQ        = Dell SaaS analytics platform; cloud-hosted; no on-prem server required'))
    lines.append(txt_row('  SCG            = Secure Connect Gateway; relay agent collecting and forwarding telemetry'))
    lines.append(txt_row('  Health score   = 0-100 integer computed per-array by CloudIQ ML models; 80+ is healthy'))
    lines.append(txt_row('  AIOps          = AI for IT operations; ML detects anomalies and predicts failures early'))
    lines.append(txt_row('  Telemetry      = Performance counters, capacity stats, event logs sent from array via SCG'))
    lines.append(txt_row('  Recommendation = Actionable CloudIQ suggestion to improve health or capacity posture'))
    lines.append(txt_row('  Firmware advisory = CloudIQ alert listing available firmware updates per array model'))
    lines.append(txt_row('  Capacity forecast = CloudIQ projection of when a pool or volume will run out of space'))
    lines.append(txt_row('  Anomaly        = Deviation from learned baseline; triggers alert if condition is sustained'))
    lines.append(txt_row('  Tenant         = CloudIQ org unit; maps to one Dell customer account; multi-site supported'))
    lines.append(txt_row('  REST API       = CloudIQ public API for querying health data, metrics, and alert management'))
    lines.append(txt_row('  SupportAssist  = Integration with Dell support for automatic SR creation on P1 events'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cloudiq-arch-design-standards',
            'docs/storage/dell/cloudiq/architecture/design-standards/index.md',
            'Dell CloudIQ — Architecture design standards')
def dell_cloudiq_arch_design_standards():
    """Dell CloudIQ architecture design standards — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ — Architecture Design Standards'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Design standards: SCG sizing, connectivity, naming, and integration for CloudIQ deployments')))
    lines.append(R(bMid(IV_L, IV_R, 'One SCG per physical site; isolated management VLAN; outbound-only 443 to cloudiq.dell.com')))
    lines.append(R(bMid(IV_L, IV_R, 'SCG VM spec: minimum 4 vCPU, 8 GB RAM, 100 GB thin disk on supported VMware version')))
    lines.append(R(bMid(IV_L, IV_R, 'All integrations use REST API with OAuth2; webhook URLs must be HTTPS with valid cert')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Site design → SCG sizing → connectivity rules → integration standards → naming convention'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCG Standards'), bMid(B2_L, B2_R, 'Connectivity'), bMid(B3_L, B3_R, 'Integration'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'One SCG per site'), bMid(B2_L, B2_R, 'Outbound 443 only'), bMid(B3_L, B3_R, 'REST API v2+'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '4 vCPU / 8 GB RAM'), bMid(B2_L, B2_R, 'No inbound ports'), bMid(B3_L, B3_R, 'OAuth2 tokens'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '100 GB thin disk'), bMid(B2_L, B2_R, 'Proxy if needed'), bMid(B3_L, B3_R, 'Webhook HTTPS'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Mgmt VLAN only'), bMid(B2_L, B2_R, 'DNS resolution'), bMid(B3_L, B3_R, 'SNMP bridge'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VMware OVA deploy'), bMid(B2_L, B2_R, 'NTP time sync'), bMid(B3_L, B3_R, 'ITSM tokens'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Naming: SCG-<SITE>-<NUMBER>; alert policies use <SITE>-<SEVERITY>-<ARRAY> naming scheme'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Standard', 'Requirement', 'Reason', 'Reference', 'Owner'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['SCG per site', 'One per DC', 'Latency/isolation', 'Deploy guide', 'Infra team'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Outbound only', '443 to cloud', 'Security posture', 'Sec policy', 'Network team'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['REST API v2', 'Minimum version', 'Stability/support', 'CloudIQ docs', 'Dev team'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Token rotation', '90-day cycle', 'Credential hygiene', 'Sec standard', 'Ops team'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SCG OVA on VMware management cluster · management VLAN · no storage-facing VLAN'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  OVA            = Open Virtualization Archive; SCG VM image downloaded from Dell support site'))
    lines.append(txt_row('  Management VLAN = Dedicated VLAN for array management IPs; SCG must reach all array mgmt IPs'))
    lines.append(txt_row('  Outbound-only  = SCG initiates all connections to cloud; no inbound firewall rules needed'))
    lines.append(txt_row('  REST API v2    = CloudIQ stable API version; avoid v1 (deprecated); use v2 for all tooling'))
    lines.append(txt_row('  OAuth2 token   = Bearer token for CloudIQ API; generated in portal; store in vault not scripts'))
    lines.append(txt_row('  Webhook        = HTTP POST callback CloudIQ sends to external system when alert fires'))
    lines.append(txt_row('  SNMP bridge    = SCG feature translating CloudIQ alerts to SNMP traps for legacy NMS'))
    lines.append(txt_row('  ITSM token     = Service token for ServiceNow / Jira integration; scoped to alert write only'))
    lines.append(txt_row('  NTP sync       = Required on SCG; clock skew > 5min causes telemetry rejection at cloud'))
    lines.append(txt_row('  Proxy config   = HTTP/HTTPS proxy on SCG if direct 443 to cloud is blocked by firewall'))
    lines.append(txt_row('  Naming scheme  = Consistent SCG and policy names; aids multi-site management and audit'))
    lines.append(txt_row('  Thin disk      = SCG disk is thin-provisioned; grows to 100 GB as telemetry cache fills'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cloudiq-operations', 'docs/storage/dell/cloudiq/operations/index.md',
            'Dell CloudIQ — Day-to-day operations')
def dell_cloudiq_operations():
    """Dell CloudIQ operations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ — Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ operations: daily health review, alert triage, capacity planning, and platform upkeep')))
    lines.append(R(bMid(IV_L, IV_R, 'Health Ops: review scores, acknowledge alerts, apply recommendations, tune alert policies')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity Ops: review forecasts, expand pools, rebalance tiers, update quotas, export reports')))
    lines.append(R(bMid(IV_L, IV_R, 'Platform Ops: update SCG firmware, rotate API tokens, audit users, review audit log')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Daily health → weekly capacity → monthly platform review → on-demand incident response'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Health Ops'), bMid(B2_L, B2_R, 'Capacity Ops'), bMid(B3_L, B3_R, 'Platform Ops'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Review scores'), bMid(B2_L, B2_R, 'Review forecasts'), bMid(B3_L, B3_R, 'Update SCG'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Acknowledge alerts'), bMid(B2_L, B2_R, 'Expand pools'), bMid(B3_L, B3_R, 'Rotate API tokens'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Apply recs'), bMid(B2_L, B2_R, 'Rebalance tiers'), bMid(B3_L, B3_R, 'Audit users'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Tune policies'), bMid(B2_L, B2_R, 'Update quotas'), bMid(B3_L, B3_R, 'Review audit log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Schedule reports'), bMid(B2_L, B2_R, 'Export reports'), bMid(B3_L, B3_R, 'Update alerts'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  CloudIQ web portal for all tasks; SCG management UI for relay health and array registration'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Frequency', 'Task', 'Owner', 'Tool', 'Output'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Daily', 'Health review', 'Storage ops', 'CloudIQ portal', 'Alert log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Weekly', 'Capacity review', 'Storage ops', 'Forecast view', 'Expansion plan'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Monthly', 'Platform review', 'Storage lead', 'Audit log', 'Review report'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['On-demand', 'Incident triage', 'On-call eng.', 'Diagnostics', 'SR / RCA'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: all operations via CloudIQ web portal and SCG management UI; no CLI required'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Health Ops     = Daily task of reviewing array health scores and acting on alerts or recs'))
    lines.append(txt_row('  Capacity Ops   = Weekly review of space forecasts; triggers pool expansion or data migration'))
    lines.append(txt_row('  Platform Ops   = Monthly review of SCG firmware, API tokens, user access, and audit log'))
    lines.append(txt_row('  Recommendation = CloudIQ actionable suggestion; ops team reviews and applies or dismisses'))
    lines.append(txt_row('  Alert policy   = Rule set defining which conditions generate CloudIQ alerts and at what threshold'))
    lines.append(txt_row('  Acknowledgment = Marking an alert as seen; does not resolve; audit trail records who and when'))
    lines.append(txt_row('  Pool expansion = Adding drives or nodes to a storage pool to extend capacity'))
    lines.append(txt_row('  Tier rebalance = Moving data between performance tiers (NVMe/SAS/NL-SAS) based on activity'))
    lines.append(txt_row('  Audit log      = CloudIQ record of all user actions in portal; exported for compliance review'))
    lines.append(txt_row('  SCG update     = Applying new SCG firmware/software via CloudIQ-initiated remote update'))
    lines.append(txt_row('  Token rotation = Generating new API tokens and invalidating old ones on a scheduled cycle'))
    lines.append(txt_row('  Forecast view  = CloudIQ capacity trend graph showing projected full date per pool/volume'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cloudiq-ops-install',
            'docs/storage/dell/cloudiq/operations/install-upgrade/index.md',
            'Dell CloudIQ — Install and onboarding')
def dell_cloudiq_ops_install():
    """Dell CloudIQ install and onboarding — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ — Install and Onboarding'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ onboarding: deploy SCG, register to CloudIQ tenant, add arrays, configure alerts')))
    lines.append(R(bMid(IV_L, IV_R, 'Prerequisites: Dell support account with CloudIQ entitlement, array management credentials')))
    lines.append(R(bMid(IV_L, IV_R, 'SCG deployed as VMware OVA (or physical appliance) on management network per datacenter')))
    lines.append(R(bMid(IV_L, IV_R, 'After registration CloudIQ pulls telemetry within 15 minutes; health scores appear in 1 h')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Prerequisites → SCG deploy → portal setup → array registration → alert config → validation'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Prerequisites'), bMid(B2_L, B2_R, 'SCG Deployment'), bMid(B3_L, B3_R, 'Portal Setup'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dell support acct'), bMid(B2_L, B2_R, 'Download OVA'), bMid(B3_L, B3_R, 'Create org'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CloudIQ license'), bMid(B2_L, B2_R, 'Deploy on VMware'), bMid(B3_L, B3_R, 'Invite users'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Array mgmt creds'), bMid(B2_L, B2_R, 'Configure network'), bMid(B3_L, B3_R, 'Configure alerts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Outbound 443 open'), bMid(B2_L, B2_R, 'Register to cloud'), bMid(B3_L, B3_R, 'Add arrays'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DNS resolution'), bMid(B2_L, B2_R, 'Verify telemetry'), bMid(B3_L, B3_R, 'Verify scores'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Upgrade SCG via CloudIQ portal: Settings > SCG > Update; zero-downtime rolling update'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Phase', 'Step', 'Tool', 'Owner', 'Success Criteria'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Planning', 'Size SCG VM', 'Spec sheet', 'Infra team', 'VM created'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Deployment', 'Deploy OVA', 'vSphere', 'Storage eng.', 'SCG online'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Registration', 'Add arrays', 'SCG UI', 'Storage eng.', 'Telemetry flowing'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Validation', 'Check scores', 'CloudIQ portal', 'Storage lead', 'Score >= 80'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SCG OVA on vSphere management cluster · mgmt VLAN · NTP synced · 443 outbound'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  OVA            = Open Virtualization Archive; SCG VM image downloaded from Dell support portal'))
    lines.append(txt_row('  Entitlement    = CloudIQ license tied to support contract; required before portal access'))
    lines.append(txt_row('  Tenant / org   = CloudIQ logical container for all sites and arrays under one customer account'))
    lines.append(txt_row('  Array registration = Providing array management IP and credentials to SCG so it can collect data'))
    lines.append(txt_row('  Telemetry      = Performance counters, capacity stats, events collected from arrays via SCG'))
    lines.append(txt_row('  Health score   = Appears within ~1 hour of first telemetry; reflects array-wide health 0-100'))
    lines.append(txt_row('  Proxy config   = Configure on SCG if direct outbound 443 is blocked; HTTP/HTTPS proxy supported'))
    lines.append(txt_row('  Upgrade path   = CloudIQ initiates SCG update remotely; no manual download required'))
    lines.append(txt_row('  Management IP  = Dedicated array management interface IP; used by SCG not data-path IPs'))
    lines.append(txt_row('  Alert policy   = Set after arrays appear; defines thresholds for email or webhook notifications'))
    lines.append(txt_row('  NTP sync       = Required on SCG VM; clock skew over 5 minutes causes telemetry rejection'))
    lines.append(txt_row('  Rolling update = SCG update completes without interrupting telemetry collection pipeline'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cloudiq-ops-procedures',
            'docs/storage/dell/cloudiq/operations/procedures/index.md',
            'Dell CloudIQ — Operational procedures')
def dell_cloudiq_ops_procedures():
    """Dell CloudIQ operational procedures — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ — Operational Procedures'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ procedures: alert handling, report generation, and array lifecycle management')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert procedures: acknowledge, suppress, bulk-resolve, escalate to SR, export history')))
    lines.append(R(bMid(IV_L, IV_R, 'Report procedures: generate capacity and perf reports, schedule email delivery, export CSV')))
    lines.append(R(bMid(IV_L, IV_R, 'Array procedures: add new array to SCG, update credentials, remove decommissioned arrays')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Trigger → acknowledge/suppress → action → validate resolution → document in ITSM ticket'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Alert Procedures'), bMid(B2_L, B2_R, 'Report Procedures'), bMid(B3_L, B3_R, 'Array Procedures'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Acknowledge alert'), bMid(B2_L, B2_R, 'Capacity report'), bMid(B3_L, B3_R, 'Add array'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Create suppression'), bMid(B2_L, B2_R, 'Perf report'), bMid(B3_L, B3_R, 'Update creds'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Bulk resolve'), bMid(B2_L, B2_R, 'Email schedule'), bMid(B3_L, B3_R, 'Remove array'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Escalate to SR'), bMid(B2_L, B2_R, 'Custom dashboard'), bMid(B3_L, B3_R, 'Recheck telemetry'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Export history'), bMid(B2_L, B2_R, 'Export CSV/PDF'), bMid(B3_L, B3_R, 'Site removal'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  All procedures executed in CloudIQ portal or SCG management UI; no CLI access needed'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Category', 'Procedure', 'Steps', 'Tool', 'Frequency'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Alerts', 'Acknowledge', '2 steps', 'Portal', 'As needed'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Reports', 'Capacity report', '3 steps', 'Portal', 'Weekly'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Arrays', 'Add to SCG', '4 steps', 'SCG UI', 'Per onboard'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Users', 'Add user', '3 steps', 'Portal', 'Per hire'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: procedures touch only CloudIQ portal and SCG UI — no direct array CLI required'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Acknowledge    = Marking alert as reviewed; does not resolve; creates audit trail entry'))
    lines.append(txt_row('  Suppression    = Rule that silences repeated alerts for a known condition; has expiry date'))
    lines.append(txt_row('  Bulk resolve   = Closing multiple alerts at once; useful after maintenance window completes'))
    lines.append(txt_row('  Escalate to SR = Opening a Dell Service Request from within CloudIQ alert detail view'))
    lines.append(txt_row('  Capacity report = Pre-built CloudIQ report showing pool usage, forecast, and top consumers'))
    lines.append(txt_row('  Custom dashboard = User-defined widget layout in CloudIQ showing selected arrays/metrics'))
    lines.append(txt_row('  Export CSV     = Downloading CloudIQ data as spreadsheet; used for external reporting tools'))
    lines.append(txt_row('  Add array      = Entering array mgmt IP and credentials in SCG so CloudIQ can collect telemetry'))
    lines.append(txt_row('  Update creds   = Refreshing array admin password in SCG when array password is changed'))
    lines.append(txt_row('  Remove array   = Deleting array from SCG and CloudIQ; telemetry history retained for 90 days'))
    lines.append(txt_row('  Site removal   = Decommissioning an SCG site; requires all arrays removed first'))
    lines.append(txt_row('  Email schedule = CloudIQ automated report delivery to specified addresses on a set cadence'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cloudiq-security', 'docs/storage/dell/cloudiq/security/index.md',
            'Dell CloudIQ — Security model overview')
def dell_cloudiq_security():
    """Dell CloudIQ security overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ — Security'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ security: identity access management, data encryption, compliance, and audit logging')))
    lines.append(R(bMid(IV_L, IV_R, 'Identity: SSO via SAML 2.0 / OIDC, local accounts, MFA enforcement, RBAC least privilege')))
    lines.append(R(bMid(IV_L, IV_R, 'Data: TLS 1.2+ in transit, AES-256 at rest, tenant isolation, data residency controls')))
    lines.append(R(bMid(IV_L, IV_R, 'Compliance: SOC 2 Type II certified, GDPR controls, audit log export, right-to-delete')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Auth → RBAC check → encrypted data access → action logged → compliance report'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Identity & Access'), bMid(B2_L, B2_R, 'Data Security'), bMid(B3_L, B3_R, 'Compliance'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SSO / SAML 2.0'), bMid(B2_L, B2_R, 'TLS 1.2+ transit'), bMid(B3_L, B3_R, 'SOC 2 Type II'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Local accounts'), bMid(B2_L, B2_R, 'AES-256 at rest'), bMid(B3_L, B3_R, 'GDPR controls'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MFA enforcement'), bMid(B2_L, B2_R, 'Tenant isolation'), bMid(B3_L, B3_R, 'Audit log export'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RBAC roles'), bMid(B2_L, B2_R, 'Data residency'), bMid(B3_L, B3_R, 'Right-to-delete'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Session management'), bMid(B2_L, B2_R, 'SCG cert auth'), bMid(B3_L, B3_R, 'Retention policy'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Dell manages cloud infrastructure security; customer manages tenant RBAC and SCG network'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Layer', 'Control', 'Standard', 'Tool', 'Owner'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Identity', 'MFA + RBAC', 'NIST 800-63', 'CloudIQ IAM', 'Customer'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Transit', 'TLS 1.2+', 'PCI DSS 4.0', 'SCG/portal', 'Dell + Cust.'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Storage', 'AES-256', 'FIPS 140-2', 'Cloud KMS', 'Dell'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Audit', 'Log all actions', 'SOC 2 CC7', 'Audit log', 'Customer'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: Dell cloud infra (AWS/Azure); customer controls SCG placement and RBAC assignments'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SAML 2.0       = Federated SSO protocol; links corporate IdP to CloudIQ for seamless login'))
    lines.append(txt_row('  OIDC           = OpenID Connect; OAuth2-based identity layer for modern SSO integrations'))
    lines.append(txt_row('  MFA            = Multi-Factor Authentication; TOTP app or email OTP; enforced at org level'))
    lines.append(txt_row('  RBAC           = Role-Based Access Control; Admin, Operator, Viewer roles with scoped perms'))
    lines.append(txt_row('  Tenant isolation = Each customer org is fully isolated; no cross-tenant data access possible'))
    lines.append(txt_row('  Data residency = Customer selects regional CloudIQ endpoint; data stored in chosen geography'))
    lines.append(txt_row('  SOC 2 Type II  = Annual third-party audit of Dell cloud security controls; report on request'))
    lines.append(txt_row('  GDPR controls  = Dell provides data processing agreement; audit log and deletion tools included'))
    lines.append(txt_row('  Right-to-delete = Customer can request deletion of all telemetry data; completed within 30 days'))
    lines.append(txt_row('  Audit log      = Immutable record of every portal action; user, timestamp, resource, outcome'))
    lines.append(txt_row('  SCG cert auth  = SCG authenticates to CloudIQ using mutual TLS certificate (not password)'))
    lines.append(txt_row('  Session mgmt   = Portal sessions expire after 30 min idle; re-auth required; no remember-me'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cloudiq-security-access',
            'docs/storage/dell/cloudiq/security/access-control/index.md',
            'Dell CloudIQ — Access control and RBAC')
def dell_cloudiq_security_access():
    """Dell CloudIQ access control — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ — Access Control'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ RBAC: Admin, Operator, Viewer roles scoped to org, site, or individual array')))
    lines.append(R(bMid(IV_L, IV_R, 'Admin: full config, user management, alert policy, SCG management, and data export')))
    lines.append(R(bMid(IV_L, IV_R, 'Operator: acknowledge/resolve alerts, apply recommendations, view all metrics and reports')))
    lines.append(R(bMid(IV_L, IV_R, 'Viewer: read-only access to health scores, dashboards, and reports; no config changes')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Identity verified → role resolved → scope checked → action permitted or denied → logged'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Roles'), bMid(B2_L, B2_R, 'Policies'), bMid(B3_L, B3_R, 'Governance'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Admin'), bMid(B2_L, B2_R, 'Least privilege'), bMid(B3_L, B3_R, 'Quarterly review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Operator'), bMid(B2_L, B2_R, 'Monitor = Viewer'), bMid(B3_L, B3_R, 'Auto-deactivate'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Viewer'), bMid(B2_L, B2_R, 'Ops = Operator'), bMid(B3_L, B3_R, 'Named admins'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Org scope'), bMid(B2_L, B2_R, 'Admin = named users'), bMid(B3_L, B3_R, 'Access log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Site scope'), bMid(B2_L, B2_R, 'No shared accounts'), bMid(B3_L, B3_R, 'Offboard SOP'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Identity managed in CloudIQ portal or federated via SAML IdP (Okta, Azure AD, Ping)'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Role', 'Permissions', 'Scope', 'Assignment', 'Review Freq'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Admin', 'Full config', 'Org-wide', 'Named only', 'Quarterly'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Operator', 'Alert + recs', 'Site/array', 'Ops team', 'Quarterly'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Viewer', 'Read-only', 'Any scope', 'Monitoring', 'Annual'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['API token', 'Scoped perms', 'Org-wide', 'Automation', '90-day rotate'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: identity in CloudIQ cloud or federated SAML IdP; no on-prem identity server needed'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  RBAC           = Role-Based Access Control; assigns permissions based on role not individual'))
    lines.append(txt_row('  Admin role     = Full access: users, alerts, SCG, config, export; limit to 2-3 named people'))
    lines.append(txt_row('  Operator role  = Can acknowledge alerts, apply recommendations, and run reports; no user mgmt'))
    lines.append(txt_row('  Viewer role    = Read-only; appropriate for monitoring teams and executive dashboards'))
    lines.append(txt_row('  Scope          = RBAC can be limited to specific site or array; not just org-wide'))
    lines.append(txt_row('  Least privilege = Assign minimum role needed; default to Viewer, elevate only when justified'))
    lines.append(txt_row('  No shared accts = Each engineer has individual login; shared accounts defeat audit trail'))
    lines.append(txt_row('  Auto-deactivate = Accounts idle 90 days auto-disabled; re-activation requires admin approval'))
    lines.append(txt_row('  Quarterly review = Access list reviewed by storage lead; remove leavers and role mismatches'))
    lines.append(txt_row('  Offboard SOP   = Immediate account disable when engineer leaves; token revocation checklist'))
    lines.append(txt_row('  Federation     = SAML links corporate IdP; user roles assigned via group attribute mapping'))
    lines.append(txt_row('  API token scope = Tokens created with minimum required permissions; not org-admin by default'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cloudiq-security-auth',
            'docs/storage/dell/cloudiq/security/authentication/index.md',
            'Dell CloudIQ — Authentication methods')
def dell_cloudiq_security_auth():
    """Dell CloudIQ authentication — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ — Authentication'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ supports local accounts with MFA, federated SSO via SAML/OIDC, and API token auth')))
    lines.append(R(bMid(IV_L, IV_R, 'Local auth: username+password with MFA (TOTP or email OTP); password complexity enforced')))
    lines.append(R(bMid(IV_L, IV_R, 'Federated SSO: SAML 2.0 or OIDC links corporate IdP; JIT provisioning and group mapping')))
    lines.append(R(bMid(IV_L, IV_R, 'API auth: OAuth2 Bearer tokens; scoped to required permissions; 90-day rotation required')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  User login → MFA challenge → token issued → RBAC checked → session established → logged'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Local Auth'), bMid(B2_L, B2_R, 'Federated SSO'), bMid(B3_L, B3_R, 'API Auth'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Username+password'), bMid(B2_L, B2_R, 'SAML 2.0'), bMid(B3_L, B3_R, 'Bearer tokens'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TOTP MFA'), bMid(B2_L, B2_R, 'OIDC / OAuth2'), bMid(B3_L, B3_R, 'Client credentials'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Email OTP'), bMid(B2_L, B2_R, 'Corporate IdP'), bMid(B3_L, B3_R, 'Scoped perms'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Password policy'), bMid(B2_L, B2_R, 'JIT provisioning'), bMid(B3_L, B3_R, '90-day rotation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Account lockout'), bMid(B2_L, B2_R, 'Group mapping'), bMid(B3_L, B3_R, 'IP allowlist'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  SCG uses mutual TLS certificate authentication to CloudIQ — not username/password'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Method', 'Protocol', 'MFA', 'Token Lifetime', 'Use Case'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Local', 'HTTPS/form', 'TOTP/email', '30 min session', 'Human users'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['SAML SSO', 'SAML 2.0', 'IdP-side MFA', '30 min session', 'Corp identity'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['API token', 'OAuth2', 'N/A', '90-day max', 'Automation'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['SCG cert', 'mTLS', 'N/A', '1-year cert', 'SCG relay'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: auth flows through CloudIQ identity service in Dell cloud; SCG cert stored locally'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  TOTP           = Time-based One-Time Password; generated by authenticator app (Google/MS Auth)'))
    lines.append(txt_row('  Email OTP      = One-time code sent to registered email; fallback when TOTP not available'))
    lines.append(txt_row('  SAML 2.0       = XML-based SSO protocol; IdP (Okta/AAD) asserts identity to CloudIQ SP'))
    lines.append(txt_row('  OIDC           = OpenID Connect; OAuth2 + identity layer; modern alternative to SAML'))
    lines.append(txt_row('  JIT provisioning = CloudIQ auto-creates user account on first SSO login using assertion attrs'))
    lines.append(txt_row('  Group mapping  = SAML group attribute maps to CloudIQ role; avoids manual role assignment'))
    lines.append(txt_row('  Client credentials = OAuth2 flow for non-interactive API auth; app ID + secret → access token'))
    lines.append(txt_row('  Account lockout = After 5 failed logins account locked; admin or self-service reset required'))
    lines.append(txt_row('  IP allowlist   = Restrict API token or portal access to specific source IP ranges'))
    lines.append(txt_row('  mTLS           = Mutual TLS; both sides present certificates; SCG authenticates to cloud'))
    lines.append(txt_row('  Password policy = Minimum 12 chars, complexity required; no reuse of last 10 passwords'))
    lines.append(txt_row('  Session timeout = Portal session invalidated after 30 min idle; full re-auth required'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cloudiq-security-encryption',
            'docs/storage/dell/cloudiq/security/encryption/index.md',
            'Dell CloudIQ — Encryption at rest and in transit')
def dell_cloudiq_security_encryption():
    """Dell CloudIQ encryption — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ — Encryption'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ encrypts all data in transit (TLS 1.2+) and at rest (AES-256) in Dell cloud stores')))
    lines.append(R(bMid(IV_L, IV_R, 'In transit: SCG to cloud and portal to cloud use TLS 1.2+; mutual TLS for SCG, HSTS portal')))
    lines.append(R(bMid(IV_L, IV_R, 'At rest: telemetry datastore, audit logs, and report exports encrypted with AES-256')))
    lines.append(R(bMid(IV_L, IV_R, 'Key management: Dell-managed KMS by default; BYOK (Bring Your Own Key) option available')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  SCG collects plaintext telemetry on LAN → TLS tunnel to cloud → AES-256 stored at rest'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'In Transit'), bMid(B2_L, B2_R, 'At Rest'), bMid(B3_L, B3_R, 'Key Management'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TLS 1.2+'), bMid(B2_L, B2_R, 'AES-256'), bMid(B3_L, B3_R, 'Dell-managed KMS'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'mTLS for SCG'), bMid(B2_L, B2_R, 'Telemetry store'), bMid(B3_L, B3_R, 'BYOK option'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'HSTS portal'), bMid(B2_L, B2_R, 'Audit log encrypt'), bMid(B3_L, B3_R, '90-day rotation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'AES-256 cipher'), bMid(B2_L, B2_R, 'Report exports'), bMid(B3_L, B3_R, 'Key audit log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cert pinning'), bMid(B2_L, B2_R, 'Backup encrypt'), bMid(B3_L, B3_R, 'FIPS 140-2'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  SCG local disk optionally encrypted via host-level encryption; not managed by CloudIQ'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Layer', 'Algorithm', 'Key Source', 'Rotation', 'Compliance'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Transit', 'TLS 1.2+', 'PKI / cert', 'Annual cert', 'PCI DSS 4.0'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Storage', 'AES-256', 'Dell KMS', '90-day', 'FIPS 140-2'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['BYOK', 'AES-256', 'Customer HSM', 'Customer set', 'Customer req.'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Audit logs', 'AES-256', 'Dell KMS', '90-day', 'SOC 2 CC6'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: Dell cloud stores (AWS/Azure) enforce encryption; customer encrypts SCG host disk'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  TLS 1.2+       = Transport Layer Security; encrypts all SCG to cloud and portal to cloud traffic'))
    lines.append(txt_row('  mTLS           = Mutual TLS; SCG presents client certificate to cloud for bidirectional auth'))
    lines.append(txt_row('  AES-256        = Advanced Encryption Standard, 256-bit key; used for all at-rest data'))
    lines.append(txt_row('  HSTS           = HTTP Strict Transport Security; forces browser to use HTTPS for portal'))
    lines.append(txt_row('  Cert pinning   = SCG validates cloud cert fingerprint; prevents MITM via rogue certificate'))
    lines.append(txt_row('  Dell KMS       = Dell-managed key management service in cloud; keys never leave cloud boundary'))
    lines.append(txt_row('  BYOK           = Bring Your Own Key; customer provides encryption key from their own HSM'))
    lines.append(txt_row('  HSM            = Hardware Security Module; tamper-resistant device for key storage and crypto'))
    lines.append(txt_row('  FIPS 140-2     = US federal standard for cryptographic modules; Level 2 for cloud KMS'))
    lines.append(txt_row('  90-day rotation = Encryption keys rotated every 90 days; old key used to decrypt existing data'))
    lines.append(txt_row('  Telemetry store = Cloud database holding array performance and capacity time-series data'))
    lines.append(txt_row('  Backup encrypt = CloudIQ backup snapshots of telemetry encrypted with same AES-256 scheme'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cloudiq-security-hardening',
            'docs/storage/dell/cloudiq/security/hardening/index.md',
            'Dell CloudIQ — Hardening the SCG and portal')
def dell_cloudiq_security_hardening():
    """Dell CloudIQ hardening — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ — Hardening'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ hardening: harden the SCG VM, portal configuration, and network architecture')))
    lines.append(R(bMid(IV_L, IV_R, 'SCG hardening: disable SSH after initial config, update firmware, restrict management VLAN')))
    lines.append(R(bMid(IV_L, IV_R, 'Portal hardening: enforce MFA, set session timeout 30 min, IP allowlist, disable stale accts')))
    lines.append(R(bMid(IV_L, IV_R, 'Network hardening: outbound-only from SCG, IDS on management segment, proxy logging')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Deploy SCG → harden VM → harden portal config → enforce network controls → monitor'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCG Hardening'), bMid(B2_L, B2_R, 'Portal Hardening'), bMid(B3_L, B3_R, 'Network Hardening'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Disable SSH'), bMid(B2_L, B2_R, 'Enforce MFA'), bMid(B3_L, B3_R, 'Outbound-only'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Mgmt VLAN only'), bMid(B2_L, B2_R, 'Session 30 min'), bMid(B3_L, B3_R, 'No inbound ports'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Update firmware'), bMid(B2_L, B2_R, 'IP allowlist'), bMid(B3_L, B3_R, 'Proxy logging'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TLS only'), bMid(B2_L, B2_R, 'Disable stale accts'), bMid(B3_L, B3_R, 'IDS on segment'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Snapshot SCG VM'), bMid(B2_L, B2_R, 'Audit log review'), bMid(B3_L, B3_R, 'Alert on SCG down'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  SCG on isolated management VLAN; allow only TCP 443 outbound to cloudiq.dell.com'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Layer', 'Control', 'Setting', 'Standard', 'Owner'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['SCG VM', 'Disable SSH', 'After initial setup', 'CIS L1', 'Infra team'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Portal', 'Enforce MFA', 'Org-wide policy', 'NIST 800-63', 'Storage lead'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Network', 'Outbound-only', '443 egress only', 'Sec policy', 'Network team'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Monitoring', 'Alert SCG down', 'CloudIQ + SIEM', 'SOC 2', 'Ops team'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SCG management VLAN isolated from production data VLANs and user workstations'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SSH disable    = After initial SCG configuration, disable SSH; use SCG web UI for management'))
    lines.append(txt_row('  Mgmt VLAN      = Dedicated VLAN for storage management IPs; SCG only on this VLAN'))
    lines.append(txt_row('  Outbound-only  = SCG firewall rule: allow TCP 443 egress to cloudiq.dell.com; deny all inbound'))
    lines.append(txt_row('  Firmware update = Apply SCG firmware updates within 30 days of release via CloudIQ portal'))
    lines.append(txt_row('  IP allowlist   = Restrict CloudIQ portal login to corporate egress IPs; blocks home/VPN bypass'))
    lines.append(txt_row('  Session timeout = Portal auto-logout after 30 min idle; recommended for all environments'))
    lines.append(txt_row('  Stale account  = Accounts inactive 90 days auto-disabled; reviewed quarterly by storage lead'))
    lines.append(txt_row('  IDS on segment = Intrusion Detection System monitoring management VLAN for anomalous traffic'))
    lines.append(txt_row('  Proxy logging  = Log all SCG proxy traffic to detect data exfiltration or C2 activity'))
    lines.append(txt_row('  Snapshot SCG   = VM snapshot before SCG firmware updates; rollback if update fails'))
    lines.append(txt_row('  CIS L1         = Center for Internet Security Level 1 baseline; applied to SCG VM OS'))
    lines.append(txt_row('  Alert SCG down = CloudIQ and SIEM alert when SCG telemetry stops; indicates connectivity loss'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cloudiq-troubleshooting',
            'docs/storage/dell/cloudiq/troubleshooting/index.md',
            'Dell CloudIQ — Troubleshooting overview')
def dell_cloudiq_troubleshooting():
    """Dell CloudIQ troubleshooting — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ troubleshooting: connectivity issues, missing telemetry, alert and report failures')))
    lines.append(R(bMid(IV_L, IV_R, 'Connectivity: SCG not connecting to cloud — check proxy, DNS, firewall, cert validity')))
    lines.append(R(bMid(IV_L, IV_R, 'Data issues: missing health scores, stale metrics — verify array credentials and SCG logs')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert/report issues: false positives, email failures — check policy thresholds and SMTP')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Identify symptom → check SCG Diagnostics → verify array creds → escalate to Dell SR'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Connectivity'), bMid(B2_L, B2_R, 'Data Issues'), bMid(B3_L, B3_R, 'Alert / Report'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCG not connecting'), bMid(B2_L, B2_R, 'Missing telemetry'), bMid(B3_L, B3_R, 'False positives'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Proxy errors'), bMid(B2_L, B2_R, 'Stale scores'), bMid(B3_L, B3_R, 'Alert storms'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DNS failures'), bMid(B2_L, B2_R, 'Array not visible'), bMid(B3_L, B3_R, 'Email not sent'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Firewall block'), bMid(B2_L, B2_R, 'Cred failures'), bMid(B3_L, B3_R, 'Export fails'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cert validation'), bMid(B2_L, B2_R, 'Telemetry lag'), bMid(B3_L, B3_R, 'Dashboard stale'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Check SCG web UI > Diagnostics for connection status; check CloudIQ portal System Status page'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Symptom', 'Cause', 'Check', 'Fix', 'Escalate If'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['SCG offline', 'Firewall/proxy', 'SCG Diagnostics', 'Open 443 egress', '>30 min down'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['No telemetry', 'Bad creds', 'Array cred test', 'Re-enter creds', '>1 h missing'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['False alert', 'Low threshold', 'Policy settings', 'Raise threshold', 'Storm > 50/h'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Email missing', 'SMTP config', 'Test email', 'Fix SMTP relay', 'After 2 retries'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SCG Diagnostics page shows green/red per array · CloudIQ portal shows last telemetry time'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SCG Diagnostics = SCG web UI page showing cloud connectivity status and per-array collection state'))
    lines.append(txt_row('  System Status   = CloudIQ portal banner showing cloud-side outages or maintenance windows'))
    lines.append(txt_row('  Stale scores    = Health score not refreshed in >2 h; usually indicates SCG connectivity loss'))
    lines.append(txt_row('  Cred failure    = SCG cannot log into array; verify array admin password has not been rotated'))
    lines.append(txt_row('  Telemetry lag   = Data arriving late; check SCG clock skew (NTP), proxy latency, load'))
    lines.append(txt_row('  False positive  = Alert firing on a healthy condition; tune threshold or add suppression rule'))
    lines.append(txt_row('  Alert storm     = Burst of alerts from a single event; suppress root alert; dismiss children'))
    lines.append(txt_row('  SMTP relay      = Email server used by CloudIQ to send report and alert notifications'))
    lines.append(txt_row('  Export fails    = Large export times out; reduce date range; try CSV instead of PDF'))
    lines.append(txt_row('  Dashboard stale = Cached view; force refresh or log out and back in to clear cache'))
    lines.append(txt_row('  Cert validation = SCG verifies Dell cloud cert chain; fails if clock skew or proxy MITM'))
    lines.append(txt_row('  SR escalation   = Open Dell Service Request if issue not resolved by standard troubleshooting'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cod', 'docs/storage/dell/cod/index.md',
            'Dell Capacity on Demand — Pay-as-you-grow storage licensing')
def dell_cod():
    """Dell Capacity on Demand — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Capacity on Demand (CoD)'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CoD: pre-installed dark capacity on Dell arrays activated via license key when needed')))
    lines.append(R(bMid(IV_L, IV_R, 'Hardware ships fully populated; drives/nodes locked; capacity unlocked by purchasing CoD key')))
    lines.append(R(bMid(IV_L, IV_R, 'Supported on PowerMax, VMAX, Unity XT, PowerStore, PowerScale, Data Domain platforms')))
    lines.append(R(bMid(IV_L, IV_R, 'Managed via Dell Licensing Portal; keys applied through array management UI or CLI')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Array ships with dark capacity → purchase CoD key → apply key → capacity unlocked instantly'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CoD Model'), bMid(B2_L, B2_R, 'Array Support'), bMid(B3_L, B3_R, 'Management'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Pre-installed hw'), bMid(B2_L, B2_R, 'PowerMax / VMAX'), bMid(B3_L, B3_R, 'Licensing portal'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dark capacity'), bMid(B2_L, B2_R, 'Unity XT'), bMid(B3_L, B3_R, 'Array UI / CLI'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'License key unlock'), bMid(B2_L, B2_R, 'PowerStore'), bMid(B3_L, B3_R, 'CloudIQ monitor'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Pay when used'), bMid(B2_L, B2_R, 'PowerScale'), bMid(B3_L, B3_R, 'Support portal'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Instant expansion'), bMid(B2_L, B2_R, 'Data Domain'), bMid(B3_L, B3_R, 'Dell account team'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  No truck roll needed for expansion; drives or nodes already installed; zero downtime unlock'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Component', 'Role', 'Owner', 'Tool', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Array hw', 'Pre-installed', 'Dell', 'Factory', 'Dark at ship'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['CoD key', 'Unlocks capacity', 'Customer buys', 'License portal', 'Per pool/frame'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Array mgr', 'Applies key', 'Storage eng.', 'GUI or CLI', 'Instant effect'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['CloudIQ', 'Monitors usage', 'Storage team', 'SaaS portal', 'Triggers alerts'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: drives/nodes pre-installed in array chassis; locked by firmware until key applied'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  CoD            = Capacity on Demand; Dell licensing model for pre-installed dark capacity'))
    lines.append(txt_row('  Dark capacity  = Physically installed but software-locked storage; visible in management as locked'))
    lines.append(txt_row('  CoD key        = License file purchased from Dell; applied to array to unlock specific capacity'))
    lines.append(txt_row('  Licensing portal = Dell portal at licensing.dell.com for purchasing and downloading CoD keys'))
    lines.append(txt_row('  Instant expansion = Capacity available within seconds of key application; no reboot required'))
    lines.append(txt_row('  Pay-as-you-grow = Only pay for capacity license when business need justifies expansion'))
    lines.append(txt_row('  Frame license  = CoD key scoped to a specific array serial number; not transferable'))
    lines.append(txt_row('  Pool unlock    = Specific storage pool capacity unlocked by key; other pools remain locked'))
    lines.append(txt_row('  CloudIQ alert  = CloudIQ notifies when used capacity approaches CoD threshold requiring next key'))
    lines.append(txt_row('  No truck roll  = Pre-installed hw means no engineer site visit needed for expansion'))
    lines.append(txt_row('  VMAX CoD       = VMAX All Flash uses CoD for engine and bay additions; applied via Unisphere'))
    lines.append(txt_row('  PowerMax CoD   = PowerMax uses Hypermax OS feature licensing model alongside CoD drives'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cod-arch-integrations',
            'docs/storage/dell/cod/architecture/integrations/index.md',
            'Dell CoD — Architecture integrations')
def dell_cod_arch_integrations():
    """Dell CoD architecture integrations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CoD — Architecture Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CoD integrates with Dell Licensing Portal, array management, CloudIQ, and ITSM workflows')))
    lines.append(R(bMid(IV_L, IV_R, 'Licensing Portal: purchase and download CoD keys; linked to Dell support account and array SN')))
    lines.append(R(bMid(IV_L, IV_R, 'Array management: Unisphere, PMAX GUI, or CLI applies key and activates dark capacity')))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ integration: monitors used vs CoD capacity; alerts when threshold triggers next key')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Purchase key → download from portal → apply via array GUI or CLI → CloudIQ confirms unlock'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Licensing Portal'), bMid(B2_L, B2_R, 'Array Management'), bMid(B3_L, B3_R, 'Monitoring'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Buy CoD key'), bMid(B2_L, B2_R, 'Unisphere for PMax'), bMid(B3_L, B3_R, 'CloudIQ alerts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Download key file'), bMid(B2_L, B2_R, 'VMAX Mgr'), bMid(B3_L, B3_R, 'Capacity forecast'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Serial number tie'), bMid(B2_L, B2_R, 'Unity Unisphere'), bMid(B3_L, B3_R, 'SCG telemetry'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'License history'), bMid(B2_L, B2_R, 'Array CLI apply'), bMid(B3_L, B3_R, 'ITSM ticket'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Account link'), bMid(B2_L, B2_R, 'Instant effect'), bMid(B3_L, B3_R, 'Email alert'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  ITSM integration: CoD key purchase triggers change request; applied in approved change window'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['System', 'Function', 'Protocol', 'Auth', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Licensing portal', 'Key purchase', 'HTTPS', 'Dell SSO', 'licensing.dell.com'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Unisphere', 'Key apply', 'HTTPS REST', 'Local/LDAP', 'Per array model'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['CloudIQ', 'Usage monitor', 'HTTPS/SCG', 'OAuth2', 'Alerts ops team'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['ITSM', 'Change control', 'API/webhook', 'Service token', 'Pre-approved CR'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: CoD key is a signed file applied to array controller; hardware enforced at firmware'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Licensing portal = Dell online portal for purchasing, downloading, and tracking CoD license keys'))
    lines.append(txt_row('  SN tie         = Each CoD key is cryptographically bound to a specific array serial number'))
    lines.append(txt_row('  Unisphere      = Dell web-based management UI for PowerMax, VMAX, and Unity arrays'))
    lines.append(txt_row('  Key apply      = Importing the CoD license file into array management software to unlock capacity'))
    lines.append(txt_row('  Instant effect = Capacity visible and usable within seconds; no array reboot required'))
    lines.append(txt_row('  CloudIQ alert  = Triggered at configurable threshold (e.g. 80%) of current CoD capacity'))
    lines.append(txt_row('  ITSM ticket    = Change request created before key purchase and application for audit trail'))
    lines.append(txt_row('  License history = Dell portal retains all purchased keys per serial; re-download if needed'))
    lines.append(txt_row('  SCG telemetry  = Used capacity metrics flow via SCG to CloudIQ for monitoring'))
    lines.append(txt_row('  Pre-approved CR = Standing change request for CoD activation to avoid delay at capacity trigger'))
    lines.append(txt_row('  Account link   = Dell support account linked to licensing portal; required for key purchase'))
    lines.append(txt_row('  Webhook        = CloudIQ posts alert to ITSM webhook on threshold breach for auto-ticket creation'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cod-operations', 'docs/storage/dell/cod/operations/index.md',
            'Dell CoD — Day-to-day operations')
def dell_cod_operations():
    """Dell CoD operations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CoD — Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CoD operations: monitor dark capacity levels, plan key purchases, apply keys, audit usage')))
    lines.append(R(bMid(IV_L, IV_R, 'Monitoring: CloudIQ tracks used vs locked capacity; alerts at configurable threshold')))
    lines.append(R(bMid(IV_L, IV_R, 'Planning: forecast capacity needs 3-6 months ahead; pre-purchase keys to avoid delays')))
    lines.append(R(bMid(IV_L, IV_R, 'Key application: import key file via array management UI or CLI; instant capacity unlock')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Monitor usage → hit threshold → raise change request → purchase key → apply → verify'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Monitoring'), bMid(B2_L, B2_R, 'Planning'), bMid(B3_L, B3_R, 'Key Operations'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CloudIQ dashboard'), bMid(B2_L, B2_R, 'Forecast review'), bMid(B3_L, B3_R, 'Purchase key'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity alerts'), bMid(B2_L, B2_R, 'Pre-buy keys'), bMid(B3_L, B3_R, 'Download key'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Threshold config'), bMid(B2_L, B2_R, 'Raise CR'), bMid(B3_L, B3_R, 'Apply to array'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dark cap view'), bMid(B2_L, B2_R, 'Lead time plan'), bMid(B3_L, B3_R, 'Verify unlock'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Monthly audit'), bMid(B2_L, B2_R, 'Budget approval'), bMid(B3_L, B3_R, 'Update CMDB'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Monthly review: check dark capacity remaining, update forecast, ensure pre-purchased keys ready'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Frequency', 'Task', 'Owner', 'Tool', 'Output'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Daily', 'Alert triage', 'Storage ops', 'CloudIQ', 'Alert log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Monthly', 'Capacity audit', 'Storage lead', 'CloudIQ + portal', 'Forecast report'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Quarterly', 'Key pre-purchase', 'Storage lead', 'Licensing portal', 'Keys on hand'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['On-demand', 'Key application', 'Storage eng.', 'Array GUI/CLI', 'Capacity live'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: dark drives/nodes on array already installed; key activates firmware to expose them'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Dark capacity  = Installed but locked drives or nodes; appear as locked in array management'))
    lines.append(txt_row('  Threshold alert = CloudIQ fires when used capacity / total CoD capacity exceeds set percentage'))
    lines.append(txt_row('  Pre-buy key    = Purchasing CoD keys before threshold is hit; avoids procurement delay'))
    lines.append(txt_row('  Lead time      = Procurement approval plus Dell order processing; typically 1-5 business days'))
    lines.append(txt_row('  Change request = ITSM CR raised before CoD key application; documents capacity change reason'))
    lines.append(txt_row('  Capacity audit = Monthly review of all arrays: dark remaining, used, forecast, keys on hand'))
    lines.append(txt_row('  CMDB update    = After key applied, update CMDB with new licensed capacity per array'))
    lines.append(txt_row('  Verify unlock  = After key application, confirm in array GUI that new capacity is visible'))
    lines.append(txt_row('  Budget approval = Finance sign-off required for CoD key purchase; include in capacity plan'))
    lines.append(txt_row('  Keys on hand   = Purchased but unapplied CoD keys stored in licensing portal for quick use'))
    lines.append(txt_row('  Monthly audit  = Formal review; compare used vs dark vs keys on hand across all CoD arrays'))
    lines.append(txt_row('  Forecast review = Projecting when next CoD key will be needed based on growth trend'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cod-ops-backup',
            'docs/storage/dell/cod/operations/backup-restore/index.md',
            'Dell CoD — Backup and restore operations')
def dell_cod_ops_backup():
    """Dell CoD backup/restore — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CoD — Backup and Restore'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CoD backup/restore: protect CoD key files and array configuration for recovery scenarios')))
    lines.append(R(bMid(IV_L, IV_R, 'Key backup: store CoD key files in secure vault and Dell licensing portal (re-download avail)')))
    lines.append(R(bMid(IV_L, IV_R, 'Array config backup: export array config before and after each CoD key application')))
    lines.append(R(bMid(IV_L, IV_R, 'Restore: re-apply key from licensing portal if array is replaced or controller swapped')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Apply key → export array config → store key in vault → re-download from portal if lost'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key Backup'), bMid(B2_L, B2_R, 'Config Backup'), bMid(B3_L, B3_R, 'Restore'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Vault storage'), bMid(B2_L, B2_R, 'Pre-apply export'), bMid(B3_L, B3_R, 'Re-download key'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Portal re-download'), bMid(B2_L, B2_R, 'Post-apply export'), bMid(B3_L, B3_R, 'Re-apply to array'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Secure file share'), bMid(B2_L, B2_R, 'SRE diff check'), bMid(B3_L, B3_R, 'Controller swap'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key inventory doc'), bMid(B2_L, B2_R, 'Change record'), bMid(B3_L, B3_R, 'Array replace'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Version tracking'), bMid(B2_L, B2_R, 'CMDB entry'), bMid(B3_L, B3_R, 'Verify capacity'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  CoD keys are tied to array serial number; key must be re-downloaded and re-applied on replacement'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Task', 'Trigger', 'Tool', 'Owner', 'Retention'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Key backup', 'After purchase', 'Vault + portal', 'Storage eng.', 'Permanent'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Config export', 'Before/after key', 'Array GUI', 'Storage eng.', '1 year min'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Key re-download', 'Array replace', 'Licensing portal', 'Storage eng.', 'On-demand'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Verify unlock', 'After restore', 'Array GUI', 'Storage eng.', 'Per restore'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: CoD key is a signed license file; store in HashiCorp Vault or equivalent secure store'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Key vault      = Secure secret store (HashiCorp Vault, CyberArk) holding CoD license files'))
    lines.append(txt_row('  Portal re-download = CoD keys always re-downloadable from Dell Licensing Portal by serial number'))
    lines.append(txt_row('  Pre-apply export = Array config backup taken before key application; baseline for comparison'))
    lines.append(txt_row('  Post-apply export = Array config after key applied; diff confirms expected capacity change'))
    lines.append(txt_row('  Controller swap = Replacing failed array controller; key must be re-applied after new controller'))
    lines.append(txt_row('  Array replace  = Entire array chassis swap (rare); new SN issued; new CoD key required'))
    lines.append(txt_row('  Key inventory  = Document tracking all purchased CoD keys per array: SN, capacity, applied date'))
    lines.append(txt_row('  SRE diff check = Comparing pre/post config exports to confirm only expected changes were made'))
    lines.append(txt_row('  CMDB entry     = Configuration Management Database updated with new licensed capacity post-apply'))
    lines.append(txt_row('  Version tracking = Key inventory tracks each key version as capacity is unlocked over time'))
    lines.append(txt_row('  Secure file share = Encrypted file store as secondary backup for key files alongside vault'))
    lines.append(txt_row('  Verify capacity = Post-restore check in array management that all expected pools are visible'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cod-ops-procedures',
            'docs/storage/dell/cod/operations/procedures/index.md',
            'Dell CoD — Operational procedures')
def dell_cod_ops_procedures():
    """Dell CoD operational procedures — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CoD — Operational Procedures'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CoD procedures: capacity review, key purchase, key application, and post-expansion validation')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity review: monthly CloudIQ review of used vs dark capacity; update growth forecast')))
    lines.append(R(bMid(IV_L, IV_R, 'Key purchase: raise CR, get approval, purchase from licensing portal, store key securely')))
    lines.append(R(bMid(IV_L, IV_R, 'Key application: apply key in array GUI or CLI within approved change window; verify result')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Capacity alert → CR raised → key purchased → key applied in window → verified → CMDB updated'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity Review'), bMid(B2_L, B2_R, 'Key Purchase'), bMid(B3_L, B3_R, 'Key Application'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CloudIQ review'), bMid(B2_L, B2_R, 'Raise CR'), bMid(B3_L, B3_R, 'Log into array'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dark cap remaining'), bMid(B2_L, B2_R, 'Get approval'), bMid(B3_L, B3_R, 'Import key file'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Growth trend'), bMid(B2_L, B2_R, 'Order from portal'), bMid(B3_L, B3_R, 'Confirm unlock'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Forecast trigger'), bMid(B2_L, B2_R, 'Download key'), bMid(B3_L, B3_R, 'Update CMDB'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Update plan'), bMid(B2_L, B2_R, 'Store in vault'), bMid(B3_L, B3_R, 'Close CR'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key application is zero-downtime; hosts see expanded capacity within seconds of key apply'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Phase', 'Procedure', 'Tool', 'Owner', 'Duration'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Review', 'Capacity report', 'CloudIQ', 'Storage ops', '30 min'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Purchase', 'Buy + download', 'Licensing portal', 'Storage lead', '1-5 days'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Apply', 'Import key file', 'Array GUI/CLI', 'Storage eng.', '< 5 min'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Validate', 'Verify capacity', 'Array GUI', 'Storage eng.', '10 min'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: apply key during business hours; downtime not required but have rollback plan ready'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  CR             = Change Request in ITSM; required before any CoD key purchase or application'))
    lines.append(txt_row('  Approval       = Finance and storage lead sign-off on CoD key cost before purchase'))
    lines.append(txt_row('  Import key file = Array management UI: Settings > License > Import; paste or upload key file'))
    lines.append(txt_row('  Confirm unlock = Check array pool view: dark capacity should now show as available'))
    lines.append(txt_row('  CMDB update    = Record new licensed capacity per pool in the Configuration Management Database'))
    lines.append(txt_row('  Close CR       = Mark Change Request resolved after CMDB updated and capacity verified'))
    lines.append(txt_row('  Vault store    = Save key file to HashiCorp Vault or secure share immediately after download'))
    lines.append(txt_row('  Zero-downtime  = CoD key apply does not interrupt I/O; hosts continue without interruption'))
    lines.append(txt_row('  Growth trend   = Monthly CloudIQ capacity chart showing rate of consumption vs projection'))
    lines.append(txt_row('  Forecast trigger = Projected date when dark capacity exhausted; triggers pre-purchase action'))
    lines.append(txt_row('  Dark cap remaining = Current unactivated CoD capacity still available before next key needed'))
    lines.append(txt_row('  Lead time plan = Ensuring key is purchased and ready before capacity threshold is actually hit'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cod-troubleshooting', 'docs/storage/dell/cod/troubleshooting/index.md',
            'Dell CoD — Troubleshooting overview')
def dell_cod_troubleshooting():
    """Dell CoD troubleshooting — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CoD — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CoD troubleshooting: key application failures, capacity not appearing, licensing portal issues')))
    lines.append(R(bMid(IV_L, IV_R, 'Key failure: invalid key, wrong serial, expired — verify SN and re-download from portal')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity not visible: key applied but pool not expanded — check firmware compatibility')))
    lines.append(R(bMid(IV_L, IV_R, 'Portal issues: login failures, key not found — verify support account and entitlements')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Symptom identified → verify key SN match → re-download if needed → escalate to Dell if stuck'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key Issues'), bMid(B2_L, B2_R, 'Capacity Issues'), bMid(B3_L, B3_R, 'Portal Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Invalid key error'), bMid(B2_L, B2_R, 'Pool not expanded'), bMid(B3_L, B3_R, 'Login failure'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Wrong serial'), bMid(B2_L, B2_R, 'Firmware compat'), bMid(B3_L, B3_R, 'Key not found'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Expired key'), bMid(B2_L, B2_R, 'Partial unlock'), bMid(B3_L, B3_R, 'No entitlement'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'File corruption'), bMid(B2_L, B2_R, 'Capacity mismatch'), bMid(B3_L, B3_R, 'Account link'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Duplicate key'), bMid(B2_L, B2_R, 'License conflict'), bMid(B3_L, B3_R, 'Browser issue'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  First step: verify array serial number matches the SN in the CoD key file exactly'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Symptom', 'Cause', 'Check', 'Fix', 'Escalate If'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Invalid key', 'Wrong SN', 'SN in key file', 'Re-download', 'After 2 tries'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['No expansion', 'Firmware old', 'Firmware ver.', 'Upgrade array', 'Dell TAC SR'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Portal login', 'Account issue', 'Support acct.', 'Account reset', 'Dell support'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Key not found', 'Wrong account', 'Order history', 'Link accts', 'Dell licensing'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: verify array SN on chassis label or via array GUI before contacting Dell support'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Invalid key error = Array rejects key file; usually SN mismatch or corrupted download'))
    lines.append(txt_row('  SN mismatch    = CoD key file is bound to a different array serial number than the target'))
    lines.append(txt_row('  Expired key    = Rare; CoD keys typically do not expire but check key file metadata'))
    lines.append(txt_row('  File corruption = Download interrupted; re-download from portal; verify checksum if provided'))
    lines.append(txt_row('  Firmware compat = CoD key requires minimum array firmware version; check release notes'))
    lines.append(txt_row('  Partial unlock = Only some pools unlocked; check key scope matches intended pools'))
    lines.append(txt_row('  Capacity mismatch = Unlocked capacity differs from purchased amount; raise SR with Dell'))
    lines.append(txt_row('  License conflict = Two keys for same pool applied; array shows conflict; contact Dell licensing'))
    lines.append(txt_row('  No entitlement = Dell support account not linked to the service tag; contact Dell licensing team'))
    lines.append(txt_row('  Account link   = Link service tag to Dell support account via support.dell.com portal'))
    lines.append(txt_row('  Order history  = Check purchase history in licensing portal to locate previously bought keys'))
    lines.append(txt_row('  Dell licensing = Dell licensing team reachable via support portal or account team for key issues'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cod-troubleshooting-issues',
            'docs/storage/dell/cod/troubleshooting/common-issues/index.md',
            'Dell CoD — Common troubleshooting issues')
def dell_cod_troubleshooting_issues():
    """Dell CoD common issues — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CoD — Common Issues'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Common CoD issues: key rejection, capacity not visible after apply, alert misconfiguration')))
    lines.append(R(bMid(IV_L, IV_R, 'Key rejection: most common cause is SN mismatch; verify via array GUI or chassis label')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity not visible: check firmware version compatibility; may require array upgrade first')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert issues: CloudIQ threshold misconfigured; ops team not notified until capacity critical')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key rejected → verify SN → re-download key → apply corrected key → confirm capacity shown'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key Problems'), bMid(B2_L, B2_R, 'Capacity Problems'), bMid(B3_L, B3_R, 'Alert Problems'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SN mismatch'), bMid(B2_L, B2_R, 'Not visible'), bMid(B3_L, B3_R, 'Wrong threshold'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Corrupt download'), bMid(B2_L, B2_R, 'Old firmware'), bMid(B3_L, B3_R, 'Alert to wrong team'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Wrong key scope'), bMid(B2_L, B2_R, 'Partial unlock'), bMid(B3_L, B3_R, 'No email config'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Already applied'), bMid(B2_L, B2_R, 'Wrong pool'), bMid(B3_L, B3_R, 'Webhook missing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Account mismatch'), bMid(B2_L, B2_R, 'License conflict'), bMid(B3_L, B3_R, 'Stale alert'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Check array event log and CloudIQ alert history for timestamps and error message detail'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Issue', 'Root Cause', 'Diagnostic', 'Resolution', 'Prevention'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Key rejected', 'SN mismatch', 'Array GUI SN', 'Re-download', 'Confirm SN pre-buy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['No capacity', 'Old firmware', 'FW version', 'Upgrade array', 'Check compat first'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['No alert', 'Bad threshold', 'CloudIQ policy', 'Fix threshold', 'Review monthly'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Key duplicate', 'Already applied', 'License history', 'Contact Dell', 'Track in CMDB'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: always confirm array SN from chassis label, not documentation which may be outdated'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SN mismatch    = Key file SN vs array SN differ; most common CoD failure; re-download correct key'))
    lines.append(txt_row('  Corrupt download = Key file incomplete; browser or network issue; always re-download over HTTPS'))
    lines.append(txt_row('  Wrong key scope = Key unlocks different pool or capacity tier than intended; verify before purchase'))
    lines.append(txt_row('  Already applied = Key was previously used; array shows duplicate; contact Dell licensing team'))
    lines.append(txt_row('  Account mismatch = Key purchased under different Dell account than managing the array'))
    lines.append(txt_row('  Old firmware   = Array firmware below minimum required for CoD key; upgrade before applying key'))
    lines.append(txt_row('  Partial unlock = Key scope smaller than expected; array unlocks only a subset of purchased capacity'))
    lines.append(txt_row('  Wrong pool     = Key targets a different pool; check key details in licensing portal before import'))
    lines.append(txt_row('  License conflict = Two keys active for same pool; contact Dell TAC; do not apply additional keys'))
    lines.append(txt_row('  Wrong threshold = CloudIQ alert threshold set too high; team not alerted until critically low'))
    lines.append(txt_row('  Stale alert    = Alert fires for old condition already resolved; acknowledge and review policy'))
    lines.append(txt_row('  Webhook missing = CloudIQ webhook to ITSM not configured; alerts go to email only or nowhere'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-cod-troubleshooting-escalation',
            'docs/storage/dell/cod/troubleshooting/escalation/index.md',
            'Dell CoD — Escalation procedures')
def dell_cod_troubleshooting_escalation():
    """Dell CoD escalation — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CoD — Escalation'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CoD escalation: when self-service resolution fails, escalate to Dell licensing or TAC')))
    lines.append(R(bMid(IV_L, IV_R, 'Dell Licensing team: for key purchase issues, duplicate keys, SN re-binding, wrong account')))
    lines.append(R(bMid(IV_L, IV_R, 'Dell TAC: for capacity not appearing after valid key applied; firmware or hardware faults')))
    lines.append(R(bMid(IV_L, IV_R, 'Account team: for budget or contract issues affecting CoD entitlements or key availability')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Self-service fails → open SR with error detail → licensing or TAC → account team if contract'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Licensing Team'), bMid(B2_L, B2_R, 'Dell TAC'), bMid(B3_L, B3_R, 'Account Team'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key re-issue'), bMid(B2_L, B2_R, 'Firmware issue'), bMid(B3_L, B3_R, 'Contract dispute'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SN re-binding'), bMid(B2_L, B2_R, 'Hardware fault'), bMid(B3_L, B3_R, 'Entitlement query'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Account merge'), bMid(B2_L, B2_R, 'Capacity conflict'), bMid(B3_L, B3_R, 'Pricing review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Duplicate key'), bMid(B2_L, B2_R, 'License conflict'), bMid(B3_L, B3_R, 'Key pre-purchase'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Order history'), bMid(B2_L, B2_R, 'Event log review'), bMid(B3_L, B3_R, 'Exec escalation'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Collect: array SN, key file, event log, firmware version, and licensing portal screenshots'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Issue Type', 'Escalate To', 'Info Needed', 'SLA', 'Contact'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Key rejected', 'Dell Licensing', 'SN + key file', '1 biz day', 'Licensing portal'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['No capacity', 'Dell TAC', 'FW ver + log', '4h P2 SLA', 'support.dell.com'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Contract issue', 'Account team', 'Contract ID', '1 biz day', 'Dell rep'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Exec escalate', 'Account exec', 'SR number', 'Same day', 'Account team'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: gather chassis label SN photo; compare to key file and portal record before calling'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Licensing team = Dell internal team managing CoD keys, SN binding, and licensing portal accounts'))
    lines.append(txt_row('  SN re-binding  = Dell process to re-issue a key for a replacement array serial number'))
    lines.append(txt_row('  Account merge  = Consolidating two Dell support accounts that each hold CoD keys for same site'))
    lines.append(txt_row('  Duplicate key  = Same key applied twice or purchased twice; licensing team resolves'))
    lines.append(txt_row('  Dell TAC       = Technical Assistance Center; handles firmware, hardware, and capacity issues'))
    lines.append(txt_row('  License conflict = Two active keys for same pool; TAC can resolve with Dell backend licensing'))
    lines.append(txt_row('  Event log      = Array management event log showing exact error text from key rejection'))
    lines.append(txt_row('  Contract ID    = Dell contract reference number; needed for entitlement and pricing disputes'))
    lines.append(txt_row('  P2 SLA         = Dell TAC 4-hour response for degraded production; CoD failure may qualify'))
    lines.append(txt_row('  Account exec   = Dell account executive; involved for contract disputes or exec escalations'))
    lines.append(txt_row('  Entitlement    = Right to activate CoD based on support contract; account team verifies'))
    lines.append(txt_row('  SR number      = Service Request number; track and share when calling Dell escalation contacts'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-data-domain', 'docs/storage/dell/data-domain/index.md',
            'Dell Data Domain (PowerProtect DD) — Backup deduplication platform')
def dell_data_domain():
    """Dell Data Domain — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Data Domain (PowerProtect DD)'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Data Domain: purpose-built backup deduplication appliance; up to 65:1 dedup ratio')))
    lines.append(R(bMid(IV_L, IV_R, 'DD Boost protocol: backup software integrates directly with DD; distributes dedup work')))
    lines.append(R(bMid(IV_L, IV_R, 'Protocols: DD Boost, NFS, CIFS/SMB, VTL (virtual tape), iSCSI; OST for media servers')))
    lines.append(R(bMid(IV_L, IV_R, 'Cloud tier: replicate MTree data to AWS S3, Azure Blob, or DD Virtual Edition for DR')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Backup app writes via DD Boost → deduplication engine → local MTree → cloud tier replication'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dedup Engine'), bMid(B2_L, B2_R, 'Data Services'), bMid(B3_L, B3_R, 'Protection'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Inline dedup'), bMid(B2_L, B2_R, 'DD Boost'), bMid(B3_L, B3_R, 'Replication'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Compression'), bMid(B2_L, B2_R, 'NFS / CIFS'), bMid(B3_L, B3_R, 'Cloud tier'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Segment store'), bMid(B2_L, B2_R, 'VTL'), bMid(B3_L, B3_R, 'WORM lock'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '65:1 ratio'), bMid(B2_L, B2_R, 'iSCSI'), bMid(B3_L, B3_R, 'Retention lock'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Garbage collect'), bMid(B2_L, B2_R, 'OST protocol'), bMid(B3_L, B3_R, 'Encryption'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Integrates with NetBackup, Commvault, Veeam, Avamar, and other backup software via DD Boost'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Layer', 'Component', 'Protocol', 'Location', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Backup app', 'NetBackup/Veeam', 'DD Boost/OST', 'Media server', 'Distributes dedup'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['DD appliance', 'PowerProtect DD', 'All protocols', 'On-premises', 'MTree storage'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Cloud tier', 'DD cloud ext.', 'HTTPS/S3', 'AWS/Azure', 'Long-term ret.'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Management', 'DDMC / DD OS', 'HTTPS', 'On-premises', 'CloudIQ optional'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: 1U-6U appliance with NL-SAS/SSD tiers; cloud tier extends via WAN to S3 or Azure'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  DD Boost       = Dell protocol enabling backup app to participate in dedup; reduces network load'))
    lines.append(txt_row('  MTree          = Logical namespace on DD; each backup job or app typically maps to an MTree'))
    lines.append(txt_row('  Deduplication  = Identifying and storing only unique data segments; eliminates repeated patterns'))
    lines.append(txt_row('  Dedup ratio    = Logical data stored divided by physical space used; 65:1 is theoretical maximum'))
    lines.append(txt_row('  Segment store  = DD internal on-disk format; each unique data segment stored once, indexed'))
    lines.append(txt_row('  Garbage collect = DD process reclaiming space from deleted or expired backup data'))
    lines.append(txt_row('  VTL            = Virtual Tape Library; DD emulates tape drives for legacy backup software'))
    lines.append(txt_row('  OST            = OpenStorage Technology; Veritas API for deep DD Boost integration in NetBackup'))
    lines.append(txt_row('  Cloud tier     = DD feature extending MTree data to object storage (S3/Azure) for cold backup'))
    lines.append(txt_row('  WORM           = Write Once Read Many; DD Retention Lock Compliance for immutable backup copies'))
    lines.append(txt_row('  Replication    = DD-to-DD data replication for DR; directory-based or MTree-based scheduling'))
    lines.append(txt_row('  DDMC           = Data Domain Management Center; centralized management for multiple DD appliances'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-data-domain-operations', 'docs/storage/dell/data-domain/operations/index.md',
            'Dell Data Domain — Day-to-day operations')
def dell_data_domain_operations():
    """Dell Data Domain operations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Data Domain — Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Data Domain operations: monitor capacity, dedup ratio, replication health, and alerts')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity management: track MTree usage, dedup savings, and project retention expiry')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication: verify daily jobs complete on schedule; check lag and error counts in DDMC')))
    lines.append(R(bMid(IV_L, IV_R, 'Maintenance: weekly garbage collect, DDOS updates, disk health, and cloud tier sync')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Daily backup runs → check status and dedup ratio → monitor replication lag → capacity review'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity Ops'), bMid(B2_L, B2_R, 'Replication Ops'), bMid(B3_L, B3_R, 'Maintenance'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MTree usage'), bMid(B2_L, B2_R, 'Check job status'), bMid(B3_L, B3_R, 'Garbage collect'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dedup savings'), bMid(B2_L, B2_R, 'Lag monitoring'), bMid(B3_L, B3_R, 'DDOS updates'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cloud tier sync'), bMid(B2_L, B2_R, 'Error review'), bMid(B3_L, B3_R, 'Disk health'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Expiry review'), bMid(B2_L, B2_R, 'Bandwidth util'), bMid(B3_L, B3_R, 'Fan/PSU check'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Quota enforce'), bMid(B2_L, B2_R, 'Throttle config'), bMid(B3_L, B3_R, 'Log rotation'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  DDMC provides centralized dashboard for all DD appliances; CLI available for scripted checks'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Frequency', 'Task', 'Owner', 'Tool', 'Output'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Daily', 'Backup job check', 'Backup ops', 'DDMC / app', 'Job report'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Weekly', 'Garbage collect', 'Storage ops', 'CLI / GUI', 'Space reclaimed'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Monthly', 'Capacity review', 'Storage lead', 'DDMC report', 'Forecast plan'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Quarterly', 'DDOS update', 'Storage eng.', 'Support bundle', 'Patch applied'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: dedicated backup network for DD Boost traffic; separate replication link or WAN'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  MTree usage    = Per-MTree logical and physical space; track for each backup app or job type'))
    lines.append(txt_row('  Dedup savings  = Reported as percentage; 95% means 20:1 ratio; tracked per-MTree and global'))
    lines.append(txt_row('  Garbage collect = Reclaims physical space from deleted/expired data; run weekly during off-peak'))
    lines.append(txt_row('  Replication lag = Time between source write and target sync; monitor daily; alert if > 24h'))
    lines.append(txt_row('  Expiry review  = Check that retention policies are expiring old backups; prevents space bloat'))
    lines.append(txt_row('  Cloud tier sync = Verifying data tiered to S3/Azure cloud matches expected transfer schedule'))
    lines.append(txt_row('  Quota enforce  = MTree space quotas prevent one app consuming entire DD capacity'))
    lines.append(txt_row('  DDOS update    = Data Domain Operating System firmware update; test in non-production first'))
    lines.append(txt_row('  Disk health    = Monitor S.M.A.R.T. and DD disk status; replace pre-failure disks proactively'))
    lines.append(txt_row('  Throttle config = Replication bandwidth throttle schedule; reduce during business hours'))
    lines.append(txt_row('  DDMC           = Data Domain Management Center; web UI for multi-DD monitoring and management'))
    lines.append(txt_row('  Support bundle = DD diagnostic package; collect before contacting Dell TAC for any issue'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-data-domain-ops-install',
            'docs/storage/dell/data-domain/operations/install-upgrade/index.md',
            'Dell Data Domain — Install and upgrade')
def dell_data_domain_ops_install():
    """Dell Data Domain install and upgrade — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Data Domain — Install and Upgrade'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Data Domain install: rack and power, initial config via CLI or GUI, license activation')))
    lines.append(R(bMid(IV_L, IV_R, 'Initial setup: set hostname, IPs, NTP, DNS, admin password via serial console or GUI')))
    lines.append(R(bMid(IV_L, IV_R, 'DDOS upgrade: upload upgrade bundle to DD, pre-check, upgrade, verify via sysstat')))
    lines.append(R(bMid(IV_L, IV_R, 'Post-install: register with DDMC, configure DD Boost, enable replication, enroll in CloudIQ')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Rack → power → serial console config → license → network → DD Boost → backup app config'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Initial Install'), bMid(B2_L, B2_R, 'Configuration'), bMid(B3_L, B3_R, 'DDOS Upgrade'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Rack and cable'), bMid(B2_L, B2_R, 'Hostname / DNS'), bMid(B3_L, B3_R, 'Upload bundle'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Serial console'), bMid(B2_L, B2_R, 'NTP config'), bMid(B3_L, B3_R, 'Run pre-check'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'License activation'), bMid(B2_L, B2_R, 'DD Boost enable'), bMid(B3_L, B3_R, 'Execute upgrade'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Network IPs'), bMid(B2_L, B2_R, 'Replication setup'), bMid(B3_L, B3_R, 'Verify sysstat'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Register DDMC'), bMid(B2_L, B2_R, 'CloudIQ enroll'), bMid(B3_L, B3_R, 'Test backup job'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  DDOS upgrade is non-disruptive for most versions; schedule during maintenance window anyway'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Phase', 'Task', 'Tool', 'Owner', 'Duration'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Hardware', 'Rack and cable', 'Physical', 'DC team', '2-4 hours'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Initial config', 'Console setup', 'Serial / GUI', 'Storage eng.', '1-2 hours'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Integration', 'Backup app config', 'DD GUI + app', 'Storage eng.', '2-4 hours'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['DDOS upgrade', 'Upload + apply', 'DD GUI / CLI', 'Storage eng.', '30-60 min'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: dedicated backup LAN for DD Boost; management LAN for GUI/SSH; replication WAN link'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Serial console = First access method; configure via DB-9 RS-232 or USB serial at 9600 baud'))
    lines.append(txt_row('  License activation = Apply DD capacity and feature license keys via GUI; tied to chassis SN'))
    lines.append(txt_row('  DD Boost enable = Activate DD Boost protocol in GUI; configure backup app with DD Boost user'))
    lines.append(txt_row('  Replication setup = Configure source→target replication context; IP, path, schedule, throttle'))
    lines.append(txt_row('  DDMC registration = Add new DD to Data Domain Management Center for centralized management'))
    lines.append(txt_row('  CloudIQ enroll = Install SCG and register DD to CloudIQ via SCG for health monitoring'))
    lines.append(txt_row('  DDOS upgrade   = Data Domain OS upgrade; uploaded as .rpm bundle; upgrade wizard in GUI'))
    lines.append(txt_row('  Pre-check      = DDOS upgrade pre-check verifies readiness; abort if any critical warning'))
    lines.append(txt_row('  sysstat        = DD CLI command showing system health post-upgrade; verify all services green'))
    lines.append(txt_row('  NTP config     = Required for replication timestamp accuracy; use same NTP source as backup app'))
    lines.append(txt_row('  Backup LAN     = Dedicated VLAN or network for DD Boost traffic; isolate from production LAN'))
    lines.append(txt_row('  Test backup job = Run full backup cycle after install; verify dedup ratio and job completion'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-data-domain-security', 'docs/storage/dell/data-domain/security/index.md',
            'Dell Data Domain — Security overview')
def dell_data_domain_security():
    """Dell Data Domain security — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Data Domain — Security'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Data Domain security: encryption at rest, in transit, Retention Lock, RBAC, and compliance')))
    lines.append(R(bMid(IV_L, IV_R, 'Encryption at rest: AES-256 for stored segments; software or hardware encryption key mgmt')))
    lines.append(R(bMid(IV_L, IV_R, 'Retention Lock: WORM compliance mode; data immutable until retention period expires')))
    lines.append(R(bMid(IV_L, IV_R, 'RBAC: local users, LDAP/AD integration; sysadmin, backup-admin, restricted-admin roles')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Backup data written → encrypted inline → stored in segments → locked with retention policy'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Encryption'), bMid(B2_L, B2_R, 'Retention Lock'), bMid(B3_L, B3_R, 'Access Control'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'AES-256 at rest'), bMid(B2_L, B2_R, 'WORM compliance'), bMid(B3_L, B3_R, 'LDAP/AD'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TLS in transit'), bMid(B2_L, B2_R, 'Governance mode'), bMid(B3_L, B3_R, 'Local users'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SW key mgmt'), bMid(B2_L, B2_R, 'Period lock'), bMid(B3_L, B3_R, 'Role-based'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Ext KMS (KMIP)'), bMid(B2_L, B2_R, 'Legal hold'), bMid(B3_L, B3_R, 'SSH key auth'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key rotation'), bMid(B2_L, B2_R, 'Audit log'), bMid(B3_L, B3_R, 'IP allowlist'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Compliance mode Retention Lock cannot be disabled by any admin; requires physical replacement'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Control', 'Standard', 'Scope', 'Config', 'Owner'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['AES-256', 'FIPS 140-2', 'All segments', 'Enable in GUI', 'Storage eng.'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Retention Lock', 'SEC 17a-4', 'MTree level', 'Compliance mode', 'Legal + storage'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['LDAP/AD', 'NIST 800-63', 'All users', 'Group mapping', 'Infra team'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Audit log', 'SOC 2', 'All actions', 'Syslog export', 'Security team'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: DD appliance in locked rack; access card required; no KVM; iDRAC for remote mgmt'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Retention Lock = WORM feature that prevents deletion/modification until retention period expires'))
    lines.append(txt_row('  Compliance mode = Strongest Retention Lock; even sysadmin cannot shorten period; SEC 17a-4 ready'))
    lines.append(txt_row('  Governance mode = Retention Lock where admin can adjust period; for internal policy enforcement'))
    lines.append(txt_row('  Legal hold     = Indefinite retention applied per-file; overrides retention period for litigation'))
    lines.append(txt_row('  AES-256        = DD encrypts all stored segments with AES-256; no performance penalty on modern HW'))
    lines.append(txt_row('  SW key mgmt    = DD manages encryption keys internally; keys stored encrypted on the appliance'))
    lines.append(txt_row('  Ext KMS / KMIP = External Key Management Server via KMIP protocol (e.g. Thales, HashiCorp)'))
    lines.append(txt_row('  LDAP/AD        = Bind DD to corporate LDAP or Active Directory for centralized user management'))
    lines.append(txt_row('  SSH key auth   = Disable password SSH; use only public-key authentication for CLI access'))
    lines.append(txt_row('  IP allowlist   = Restrict GUI and SSH access to specific management host IP addresses'))
    lines.append(txt_row('  KMIP           = Key Management Interoperability Protocol; standard for external KMS integration'))
    lines.append(txt_row('  Audit log      = DD event log exported to syslog; records all admin and access events'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-data-domain-troubleshooting',
            'docs/storage/dell/data-domain/troubleshooting/index.md',
            'Dell Data Domain — Troubleshooting overview')
def dell_data_domain_troubleshooting():
    """Dell Data Domain troubleshooting — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Data Domain — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Data Domain troubleshooting: backup failures, replication issues, capacity problems')))
    lines.append(R(bMid(IV_L, IV_R, 'Backup failures: DD Boost errors, authentication, network, or capacity full conditions')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication: lag growing, context errors, bandwidth saturation, or firewall blocking')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity: low space alerts, garbage collect not reclaiming, dedup ratio degraded')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Identify failure source → check DD alerts and event log → collect support bundle → open SR'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Backup Issues'), bMid(B2_L, B2_R, 'Replication'), bMid(B3_L, B3_R, 'Capacity'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DD Boost errors'), bMid(B2_L, B2_R, 'Lag growing'), bMid(B3_L, B3_R, 'Low space alert'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Auth failure'), bMid(B2_L, B2_R, 'Context error'), bMid(B3_L, B3_R, 'GC not helping'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Network timeout'), bMid(B2_L, B2_R, 'BW saturated'), bMid(B3_L, B3_R, 'Ratio degraded'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity full'), bMid(B2_L, B2_R, 'Firewall block'), bMid(B3_L, B3_R, 'Cloud tier stall'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'License expired'), bMid(B2_L, B2_R, 'Schedule missed'), bMid(B3_L, B3_R, 'Disk failure'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  First check: DD GUI Alerts panel and event log; then sysstat and support bundle for TAC'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Symptom', 'Cause', 'Check', 'Fix', 'Escalate If'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Backup fail', 'Auth/network', 'DD Boost log', 'Reset creds', 'Recurring'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Repl lag', 'BW or firewall', 'Repl context', 'Raise throttle', '> 24h lag'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Low space', 'GC needed', 'Space report', 'Run GC', 'After 2 GC runs'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Disk failure', 'Hardware', 'Disk health', 'Replace disk', 'Immediately'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: DD GUI > Maintenance > Disks for disk health; replace failed disks before rebuild needed'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  DD Boost log   = Backup application log combined with DD event log; cross-reference timestamps'))
    lines.append(txt_row('  Auth failure   = DD Boost username or password mismatch between backup app and DD user config'))
    lines.append(txt_row('  Context error  = Replication context broken; usually firewall port 2051 blocked or IP changed'))
    lines.append(txt_row('  Replication lag = Source write rate exceeds replication bandwidth; increase throttle or bandwidth'))
    lines.append(txt_row('  BW saturation  = Replication link at 100%; throttle to reduce backup app impact during peak hours'))
    lines.append(txt_row('  Garbage collect = Run via CLI: filesys clean start; takes hours; do not abort once started'))
    lines.append(txt_row('  GC not helping = GC ran but space not recovered; data may still have valid references; check policy'))
    lines.append(txt_row('  Ratio degraded = Dedup ratio dropped; check if new data type introduced (compressed, encrypted)'))
    lines.append(txt_row('  Cloud tier stall = Cloud tier transfer paused; check internet/proxy connectivity and credentials'))
    lines.append(txt_row('  Support bundle = Collect via GUI: Diagnostics > Support Bundle; attach to Dell TAC SR'))
    lines.append(txt_row('  sysstat        = DD CLI command; shows filesystem status, service health, and hardware summary'))
    lines.append(txt_row('  License expired = DD capacity or feature license expired; check via GUI: Administration > Licenses'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines
