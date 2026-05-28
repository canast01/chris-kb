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


@kb_diagram('dell-ecs', 'docs/storage/dell/ecs/index.md',
            'Dell ECS — Elastic Cloud Storage object storage platform')
def dell_ecs():
    """Dell ECS — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell ECS — Elastic Cloud Storage'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'ECS: Dell scale-out object storage; S3-compatible; designed for unstructured data at scale')))
    lines.append(R(bMid(IV_L, IV_R, 'Protocols: S3, Swift, Atmos, HDFS, NFS (via gateway); RESTful API for all operations')))
    lines.append(R(bMid(IV_L, IV_R, 'Architecture: commodity nodes in geo-distributed sites; cross-site replication for durability')))
    lines.append(R(bMid(IV_L, IV_R, 'Use cases: backup landing zone, media archive, IoT data lake, cloud-native app storage')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  App writes via S3 → ECS nodes distribute across site → replicate to geo sites → 99.9999% durable'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Storage Engine'), bMid(B2_L, B2_R, 'Data Services'), bMid(B3_L, B3_R, 'Management'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Object store'), bMid(B2_L, B2_R, 'S3 compatible'), bMid(B3_L, B3_R, 'ECS Portal'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Scale-out nodes'), bMid(B2_L, B2_R, 'Swift API'), bMid(B3_L, B3_R, 'ECS REST API'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Erasure coding'), bMid(B2_L, B2_R, 'HDFS support'), bMid(B3_L, B3_R, 'Namespace mgmt'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Geo replication'), bMid(B2_L, B2_R, 'Metadata search'), bMid(B3_L, B3_R, 'CloudIQ'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '99.9999% durable'), bMid(B2_L, B2_R, 'ILM policies'), bMid(B3_L, B3_R, 'Alerting'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  ECS nodes are commodity x86 servers with NL-SAS or NVMe drives; no external storage required'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Layer', 'Component', 'Protocol', 'Location', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Clients', 'Apps/tools', 'S3 REST', 'Any network', 'AWS SDK compat.'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['ECS nodes', 'Object store', 'Internal mesh', 'On-premises', '4+ nodes per site'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Geo sites', 'DR / archive', 'WAN repl.', 'Remote DC', 'Up to 3 sites'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['ECS Portal', 'Management UI', 'HTTPS', 'On-premises', 'Central mgmt'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: commodity nodes in rack; 10/25 GbE data network; 1 GbE management network per node'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  ECS            = Elastic Cloud Storage; Dell object storage platform for unstructured data'))
    lines.append(txt_row('  S3 compatible  = ECS supports Amazon S3 API; AWS SDK and tools work without modification'))
    lines.append(txt_row('  Object         = Immutable data unit with metadata; accessed via bucket/key path'))
    lines.append(txt_row('  Bucket         = Namespace container for objects; analogous to S3 bucket'))
    lines.append(txt_row('  Namespace      = Logical tenant container; groups buckets and users; multitenancy unit'))
    lines.append(txt_row('  Erasure coding = EC (12+4 or 10+2 by default) provides durability without full replication'))
    lines.append(txt_row('  Geo replication = Cross-site object replication; active-active or active-passive configuration'))
    lines.append(txt_row('  ILM policy     = Information Lifecycle Management; auto-move or expire objects by age or tag'))
    lines.append(txt_row('  Metadata search = ECS system metadata and custom user metadata are indexed and searchable'))
    lines.append(txt_row('  HDFS support   = ECS exports as HDFS; Hadoop/Spark workloads read directly from ECS'))
    lines.append(txt_row('  99.9999% durability = Six nines; achieved via erasure coding and geo replication combined'))
    lines.append(txt_row('  ECS Portal     = Web-based management UI for ECS; namespace, user, bucket, and policy mgmt'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-ecs-operations', 'docs/storage/dell/ecs/operations/index.md',
            'Dell ECS — Day-to-day operations')
def dell_ecs_operations():
    """Dell ECS operations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell ECS — Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'ECS operations: capacity monitoring, replication health, node maintenance, and alerts')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity: monitor per-VDC usage, erasure coding overhead, and project growth trends')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication: check geo replication lag, RPO status, and recovery point across sites')))
    lines.append(R(bMid(IV_L, IV_R, 'Maintenance: rolling node updates, drive replacement, disk rebuild monitoring, log review')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Daily health check → capacity review → replication status → node health → alert triage'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity Ops'), bMid(B2_L, B2_R, 'Replication Ops'), bMid(B3_L, B3_R, 'Node Ops'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VDC usage'), bMid(B2_L, B2_R, 'Repl lag check'), bMid(B3_L, B3_R, 'Rolling update'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'EC overhead'), bMid(B2_L, B2_R, 'RPO status'), bMid(B3_L, B3_R, 'Drive replace'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Growth forecast'), bMid(B2_L, B2_R, 'Bandwidth util'), bMid(B3_L, B3_R, 'Rebuild monitor'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Bucket quotas'), bMid(B2_L, B2_R, 'Site failover'), bMid(B3_L, B3_R, 'Log review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ILM review'), bMid(B2_L, B2_R, 'Policy check'), bMid(B3_L, B3_R, 'PSU / fan'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  ECS Portal provides cluster-wide metrics; CLI (ecscli) available for scripted health checks'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Frequency', 'Task', 'Owner', 'Tool', 'Output'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Daily', 'Health check', 'Storage ops', 'ECS Portal', 'Alert log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Weekly', 'Replication check', 'Storage ops', 'ECS Portal', 'RPO report'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Monthly', 'Capacity review', 'Storage lead', 'ECS reports', 'Forecast plan'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['On-demand', 'Drive replace', 'Storage eng.', 'ECS Portal', 'Rebuild done'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: ECS nodes on 10/25 GbE switch; separate management network; nodes same rack or spread'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  VDC            = Virtual Data Center; ECS logical group of nodes within one physical site'))
    lines.append(txt_row('  EC overhead    = Erasure coding adds ~33-50% storage overhead (12+4 EC = 1.33x raw data)'))
    lines.append(txt_row('  Bucket quota   = Per-bucket capacity limit; enforces fair use in multi-tenant environments'))
    lines.append(txt_row('  ILM review     = Check that Information Lifecycle Management policies expire data as expected'))
    lines.append(txt_row('  Repl lag       = Delay between object write and geo replication completion; monitor per-pair'))
    lines.append(txt_row('  RPO            = Recovery Point Objective; maximum data loss if site fails; tied to repl lag'))
    lines.append(txt_row('  Site failover  = Redirect client access to secondary site when primary is unreachable'))
    lines.append(txt_row('  Rolling update = ECS firmware/software update applied node by node; no cluster downtime'))
    lines.append(txt_row('  Drive replace  = Hot-swap failed drive; ECS auto-starts rebuild; monitor rebuild % in Portal'))
    lines.append(txt_row('  Rebuild monitor = Track erasure coding rebuild progress after drive failure; avoid adding load'))
    lines.append(txt_row('  ecscli         = ECS command-line tool for scripted health checks, bucket queries, and exports'))
    lines.append(txt_row('  Growth forecast = ECS capacity trend used to plan node addition before capacity is exhausted'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-ecs-security', 'docs/storage/dell/ecs/security/index.md',
            'Dell ECS — Security overview')
def dell_ecs_security():
    """Dell ECS security — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell ECS — Security'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'ECS security: multitenancy isolation, IAM, encryption, bucket policies, and compliance')))
    lines.append(R(bMid(IV_L, IV_R, 'IAM: namespace-level users, IAM roles, S3 bucket policies, ACLs, resource-based policies')))
    lines.append(R(bMid(IV_L, IV_R, 'Encryption: SSE-S3 and SSE-C (customer-managed keys) for object encryption at rest')))
    lines.append(R(bMid(IV_L, IV_R, 'Network: TLS 1.2+ for all data and management; VLANs separate data from management')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Client auth → IAM/policy check → namespace isolation → encrypted write → audit logged'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Identity & Access'), bMid(B2_L, B2_R, 'Data Security'), bMid(B3_L, B3_R, 'Compliance'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'IAM users'), bMid(B2_L, B2_R, 'SSE-S3 encrypt'), bMid(B3_L, B3_R, 'Audit log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'S3 bucket policy'), bMid(B2_L, B2_R, 'SSE-C key'), bMid(B3_L, B3_R, 'WORM / lock'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ACLs'), bMid(B2_L, B2_R, 'TLS 1.2+'), bMid(B3_L, B3_R, 'Retention lock'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Namespace isolate'), bMid(B2_L, B2_R, 'VLAN separation'), bMid(B3_L, B3_R, 'WORM bucket'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'LDAP/AD'), bMid(B2_L, B2_R, 'Data-at-rest enc.'), bMid(B3_L, B3_R, 'SOC 2 ready'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Namespaces are fully isolated; tenants cannot access other namespace buckets or objects'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Control', 'Standard', 'Scope', 'Config', 'Owner'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['IAM policy', 'AWS IAM compat', 'Per bucket', 'JSON policy', 'App team'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['SSE-S3', 'AES-256', 'All objects', 'Bucket default', 'Storage eng.'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['TLS 1.2+', 'PCI DSS 4.0', 'All endpoints', 'TLS config', 'Infra team'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['WORM bucket', 'SEC 17a-4', 'Bucket level', 'Immutable flag', 'Legal + ops'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: ECS data VLAN and management VLAN separate; TLS on both; nodes not internet-facing'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  IAM            = Identity and Access Management; ECS supports S3-compatible IAM policies'))
    lines.append(txt_row('  Bucket policy  = JSON policy attached to S3 bucket defining who can read, write, or list'))
    lines.append(txt_row('  ACL            = Access Control List; per-object or per-bucket access; simpler than policies'))
    lines.append(txt_row('  SSE-S3         = Server-Side Encryption with S3-managed keys; AES-256; transparent to client'))
    lines.append(txt_row('  SSE-C          = Server-Side Encryption with Customer-provided key; client sends key per request'))
    lines.append(txt_row('  Namespace isolate = ECS tenant boundary; buckets and users in one NS cannot see another NS'))
    lines.append(txt_row('  WORM bucket    = Bucket with object lock enabled; objects cannot be deleted before retention date'))
    lines.append(txt_row('  Retention lock = Object-level retention; object immutable until specified expiry timestamp'))
    lines.append(txt_row('  LDAP/AD        = ECS can authenticate management users via LDAP or Active Directory'))
    lines.append(txt_row('  SOC 2 ready    = ECS audit logging and WORM features support SOC 2 compliance requirements'))
    lines.append(txt_row('  VLAN separation = Data VLAN for S3 traffic; management VLAN for ECS Portal and SSH access'))
    lines.append(txt_row('  SEC 17a-4      = US regulation requiring WORM storage for financial records; ECS qualifies'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-ecs-troubleshooting', 'docs/storage/dell/ecs/troubleshooting/index.md',
            'Dell ECS — Troubleshooting overview')
def dell_ecs_troubleshooting():
    """Dell ECS troubleshooting — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell ECS — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'ECS troubleshooting: S3 API errors, replication failures, node outages, and capacity issues')))
    lines.append(R(bMid(IV_L, IV_R, 'S3 errors: 403 (auth/ACL), 404 (missing bucket/key), 503 (node overload or rebuild)')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication: lag alerts, site unreachable, bandwidth saturation, or policy mismatch')))
    lines.append(R(bMid(IV_L, IV_R, 'Node issues: node offline, drive failure, rebuild stuck, disk health warnings in Portal')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Identify error → check ECS Portal Alerts → collect support bundle → open Dell TAC SR'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'S3 API Issues'), bMid(B2_L, B2_R, 'Replication'), bMid(B3_L, B3_R, 'Node / Disk'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '403 forbidden'), bMid(B2_L, B2_R, 'Lag alert'), bMid(B3_L, B3_R, 'Node offline'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '404 not found'), bMid(B2_L, B2_R, 'Site unreachable'), bMid(B3_L, B3_R, 'Drive failure'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '503 overload'), bMid(B2_L, B2_R, 'BW saturation'), bMid(B3_L, B3_R, 'Rebuild stuck'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Auth failure'), bMid(B2_L, B2_R, 'Policy mismatch'), bMid(B3_L, B3_R, 'Disk warnings'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Perf degraded'), bMid(B2_L, B2_R, 'RPO breach'), bMid(B3_L, B3_R, 'Capacity full'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Check ECS Portal: Alerts, Nodes status, Disk health, and Geo Replication tabs first'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Symptom', 'Cause', 'Check', 'Fix', 'Escalate If'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['S3 403', 'ACL/policy', 'Bucket policy', 'Fix IAM policy', 'All requests'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Repl lag', 'BW / site', 'Repl dashboard', 'Raise throttle', 'RPO breached'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Node offline', 'HW fault', 'Node health', 'Replace node', 'Immediately'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['503 errors', 'Rebuild load', 'Node status', 'Throttle rebuild', 'Persistent'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: ECS support bundle collected via Portal > Support; contains logs, config, disk status'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  S3 403         = Forbidden; check bucket policy, IAM user, and ACL; most common auth issue'))
    lines.append(txt_row('  S3 404         = Bucket or object not found; verify bucket name, key path, and namespace'))
    lines.append(txt_row('  S3 503         = Service unavailable; often during drive rebuild or node failure; retry logic'))
    lines.append(txt_row('  Repl lag       = Time between object write and geo sync; monitor in ECS Portal > Replication'))
    lines.append(txt_row('  RPO breach     = Replication lag exceeds Recovery Point Objective; DR team must be notified'))
    lines.append(txt_row('  BW saturation  = Replication link full; add throttle or schedule during off-peak hours'))
    lines.append(txt_row('  Policy mismatch = Source and target replication policy differ; causes objects to be skipped'))
    lines.append(txt_row('  Node offline   = ECS detects node unreachable; EC rebuild starts on remaining nodes'))
    lines.append(txt_row('  Rebuild stuck  = EC rebuild paused due to I/O overload; throttle client traffic to recover'))
    lines.append(txt_row('  Disk warnings  = S.M.A.R.T. pre-failure indicators; replace proactively before drive fails'))
    lines.append(txt_row('  Support bundle = ECS diagnostic package; download from Portal > Support > Generate bundle'))
    lines.append(txt_row('  Throttle rebuild = Limit EC rebuild I/O rate via Portal to reduce impact on client workloads'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-fod', 'docs/storage/dell/fod/index.md',
            'Dell Features on Demand — Software feature licensing model')
def dell_fod():
    """Dell Features on Demand — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Features on Demand (FoD)'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FoD: Dell software feature licensing; unlock array capabilities via license key purchase')))
    lines.append(R(bMid(IV_L, IV_R, 'Features unlocked: extra protocols, replication, snapshots, encryption, tiering, FAST VP')))
    lines.append(R(bMid(IV_L, IV_R, 'Key applied via array management UI or CLI; feature active instantly without reboot')))
    lines.append(R(bMid(IV_L, IV_R, 'Supported on PowerStore, PowerMax, Unity XT, PowerScale; managed via Licensing Portal')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Identify needed feature → purchase FoD key → download → apply via array GUI → feature live'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Feature Types'), bMid(B2_L, B2_R, 'Array Support'), bMid(B3_L, B3_R, 'Management'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Protocols'), bMid(B2_L, B2_R, 'PowerStore'), bMid(B3_L, B3_R, 'Licensing portal'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Replication'), bMid(B2_L, B2_R, 'PowerMax / VMAX'), bMid(B3_L, B3_R, 'Array GUI/CLI'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Snapshots'), bMid(B2_L, B2_R, 'Unity XT'), bMid(B3_L, B3_R, 'CloudIQ monitor'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Encryption'), bMid(B2_L, B2_R, 'PowerScale'), bMid(B3_L, B3_R, 'Support portal'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FAST VP tiering'), bMid(B2_L, B2_R, 'PowerStore-X'), bMid(B3_L, B3_R, 'Dell account'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  FoD keys are array-serial-number bound; not transferable between arrays'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Component', 'Role', 'Owner', 'Tool', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['FoD key', 'Unlocks feature', 'Customer buys', 'Licensing portal', 'Per SN'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Array mgr', 'Applies key', 'Storage eng.', 'GUI or CLI', 'Instant effect'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['License portal', 'Key purchase', 'Storage lead', 'Dell portal', 'All key history'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['CloudIQ', 'Feature status', 'Storage ops', 'SaaS portal', 'Optional'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: no hardware change needed; FoD unlocks software capability already on the array'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  FoD            = Features on Demand; Dell software feature licensing model for array capabilities'))
    lines.append(txt_row('  FoD key        = License file purchased and downloaded from Dell Licensing Portal'))
    lines.append(txt_row('  Protocol FoD   = Unlock NFS, SMB, iSCSI, FC, or NVMe-oF protocol support on an array'))
    lines.append(txt_row('  Replication FoD = Unlock array-based replication (e.g. PowerStore replication, SRDF on VMAX)'))
    lines.append(txt_row('  Snapshot FoD   = Unlock snapshot creation beyond the base limit included in hardware purchase'))
    lines.append(txt_row('  Encryption FoD = Unlock data-at-rest encryption capability; AES-256 via array controller'))
    lines.append(txt_row('  FAST VP        = Fully Automated Storage Tiering for Virtual Pools; automated data placement'))
    lines.append(txt_row('  SN bound       = FoD key cryptographically tied to a specific array serial number'))
    lines.append(txt_row('  Instant effect = Feature visible in array UI seconds after key is applied; no reboot'))
    lines.append(txt_row('  Licensing portal = Dell portal for purchasing, downloading, and tracking FoD license keys'))
    lines.append(txt_row('  Base license   = Features included with array purchase without FoD; varies by model/SKU'))
    lines.append(txt_row('  Bundle key     = Some FoD products sold as a bundle; single key unlocks multiple features'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-fod-arch-design-standards',
            'docs/storage/dell/fod/architecture/design-standards/index.md',
            'Dell FoD — Architecture design standards')
def dell_fod_arch_design_standards():
    """Dell FoD architecture design standards — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell FoD — Architecture Design Standards'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FoD design standards: key inventory, firmware prereqs, change control, and CMDB hygiene')))
    lines.append(R(bMid(IV_L, IV_R, 'Pre-apply standard: verify minimum firmware version before applying any FoD key')))
    lines.append(R(bMid(IV_L, IV_R, 'Inventory standard: all purchased FoD keys documented in key inventory with SN and date')))
    lines.append(R(bMid(IV_L, IV_R, 'Change control: all FoD key applications require approved CR; tested in non-prod first')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Plan feature need → verify prereqs → raise CR → purchase key → apply in window → update CMDB'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key Standards'), bMid(B2_L, B2_R, 'Firmware Standards'), bMid(B3_L, B3_R, 'Process Standards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Vault storage'), bMid(B2_L, B2_R, 'Min FW before apply'), bMid(B3_L, B3_R, 'CR required'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key inventory doc'), bMid(B2_L, B2_R, 'Compat matrix check'), bMid(B3_L, B3_R, 'Non-prod test'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SN tracking'), bMid(B2_L, B2_R, 'DDOS / PMAS ver'), bMid(B3_L, B3_R, 'CMDB update'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Bundle awareness'), bMid(B2_L, B2_R, 'Pre-upgrade plan'), bMid(B3_L, B3_R, 'Quarterly audit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Portal re-download'), bMid(B2_L, B2_R, 'Release notes'), bMid(B3_L, B3_R, 'Naming scheme'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Naming: FoD keys stored as <ARRAYNAME>-<FEATURE>-<DATE>.lic in secure vault'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Standard', 'Requirement', 'Reason', 'Reference', 'Owner'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Key vault', 'Store all keys', 'Recovery/audit', 'Sec policy', 'Storage lead'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['FW prereq', 'Check before apply', 'Avoid failure', 'Release notes', 'Storage eng.'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['CR required', 'ITSM CR raised', 'Change control', 'ITSM policy', 'Storage lead'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['CMDB update', 'After apply', 'Accuracy', 'CMDB standard', 'Ops team'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: FoD modifies array firmware feature flags; no hardware change; instant and reversible'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Key inventory  = Spreadsheet or CMDB entry tracking all FoD keys: SN, feature, applied date'))
    lines.append(txt_row('  Vault storage  = FoD .lic files stored in HashiCorp Vault or encrypted file share'))
    lines.append(txt_row('  Min FW         = Each FoD key requires minimum array firmware; check before applying key'))
    lines.append(txt_row('  Compat matrix  = Dell support matrix showing which FoD keys work with which firmware versions'))
    lines.append(txt_row('  PMAS           = PowerMax Array Software; Hypermax OS version on PowerMax arrays'))
    lines.append(txt_row('  Non-prod test  = Apply FoD in test/dev array first; validate feature behavior before production'))
    lines.append(txt_row('  CR required    = Change Request; prevents unauthorized feature activation in production arrays'))
    lines.append(txt_row('  Bundle awareness = Some FoD keys activate multiple features; understand full scope before applying'))
    lines.append(txt_row('  Portal re-download = All FoD keys re-downloadable from Dell Licensing Portal by SN and order'))
    lines.append(txt_row('  Quarterly audit = Review all FoD keys applied per array; confirm CMDB matches array license list'))
    lines.append(txt_row('  Naming scheme  = Consistent file name for FoD keys in vault; aids search and audit'))
    lines.append(txt_row('  Release notes  = Dell FoD release notes list firmware prereqs and feature activation behavior'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-fod-arch-integrations',
            'docs/storage/dell/fod/architecture/integrations/index.md',
            'Dell FoD — Architecture integrations')
def dell_fod_arch_integrations():
    """Dell FoD architecture integrations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell FoD — Architecture Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FoD integrates with Dell Licensing Portal, array management systems, and ITSM workflows')))
    lines.append(R(bMid(IV_L, IV_R, 'Licensing Portal: purchase, download, and track FoD keys; tied to support account + SN')))
    lines.append(R(bMid(IV_L, IV_R, 'Array management: Unisphere, PowerStore Manager, or CLI applies key; feature activates')))
    lines.append(R(bMid(IV_L, IV_R, 'ITSM integration: FoD key application triggers CR; webhook closes CR on completion')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Purchase portal → download key → ITSM CR → apply via array GUI → CMDB updated → CR closed'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Licensing Portal'), bMid(B2_L, B2_R, 'Array Management'), bMid(B3_L, B3_R, 'ITSM / CMDB'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Buy FoD key'), bMid(B2_L, B2_R, 'PowerStore Mgr'), bMid(B3_L, B3_R, 'CR pre-approval'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Download .lic'), bMid(B2_L, B2_R, 'Unisphere'), bMid(B3_L, B3_R, 'Webhook close'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Order history'), bMid(B2_L, B2_R, 'Isilon/OneFS'), bMid(B3_L, B3_R, 'CMDB update'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SN binding'), bMid(B2_L, B2_R, 'Array CLI'), bMid(B3_L, B3_R, 'Audit trail'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'License history'), bMid(B2_L, B2_R, 'Instant effect'), bMid(B3_L, B3_R, 'Inventory doc'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  CloudIQ shows active FoD features per array in Health > Features view (select models)'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['System', 'Function', 'Protocol', 'Auth', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Licensing portal', 'Key purchase', 'HTTPS', 'Dell SSO', 'licensing.dell.com'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['PowerStore Mgr', 'Key apply', 'HTTPS REST', 'Local/LDAP', 'Per array'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['ITSM', 'Change control', 'API/webhook', 'Service token', 'Pre-approved CR'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['CMDB', 'Feature tracking', 'API', 'Svc account', 'Updated post-apply'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: FoD key applied to array controller; no network path to licensing portal required'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Licensing portal = Dell portal for FoD key purchase, download, and history tracking'))
    lines.append(txt_row('  PowerStore Mgr = PowerStore Manager web UI; Settings > Licenses to import FoD key'))
    lines.append(txt_row('  Unisphere      = Web UI for PowerMax and Unity; Administration > License to apply FoD key'))
    lines.append(txt_row('  Isilon / OneFS = PowerScale (formerly Isilon) uses OneFS CLI for FoD key application'))
    lines.append(txt_row('  Array CLI      = Fall-back method for FoD application if GUI is unavailable'))
    lines.append(txt_row('  ITSM webhook   = ITSM auto-closes the CR when FoD application succeeds (optional integration)'))
    lines.append(txt_row('  Audit trail    = ITSM CR + array event log provide complete audit of feature activation'))
    lines.append(txt_row('  CMDB update    = After key apply, update CMDB record for the array with new feature list'))
    lines.append(txt_row('  Inventory doc  = Key inventory spreadsheet updated with feature, SN, date applied, applied by'))
    lines.append(txt_row('  SN binding     = Each FoD key is cryptographically bound to one array serial number'))
    lines.append(txt_row('  Order history  = All FoD purchases in licensing portal; re-download any key by order number'))
    lines.append(txt_row('  CR pre-approval = Standing change request for FoD activation; avoids delay in urgent situations'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-fod-operations', 'docs/storage/dell/fod/operations/index.md',
            'Dell FoD — Day-to-day operations')
def dell_fod_operations():
    """Dell FoD operations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell FoD — Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FoD operations: feature request handling, key purchase, application, and quarterly audit')))
    lines.append(R(bMid(IV_L, IV_R, 'Request: app team requests new feature; storage team validates need and firmware prereq')))
    lines.append(R(bMid(IV_L, IV_R, 'Purchase: raise CR, get approval, buy key from portal, store in vault, apply to array')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit: quarterly review of all active FoD features per array; CMDB reconciliation')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Feature request → prereq check → CR → purchase → apply → verify → CMDB → quarterly audit'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Request Ops'), bMid(B2_L, B2_R, 'Key Ops'), bMid(B3_L, B3_R, 'Audit Ops'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Feature intake'), bMid(B2_L, B2_R, 'Raise CR'), bMid(B3_L, B3_R, 'Quarterly review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Need validation'), bMid(B2_L, B2_R, 'Purchase key'), bMid(B3_L, B3_R, 'CMDB reconcile'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FW prereq check'), bMid(B2_L, B2_R, 'Apply key'), bMid(B3_L, B3_R, 'Key inventory'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Budget sign-off'), bMid(B2_L, B2_R, 'Verify feature'), bMid(B3_L, B3_R, 'Unused key review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Test in non-prod'), bMid(B2_L, B2_R, 'Update CMDB'), bMid(B3_L, B3_R, 'Portal reconcile'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  All FoD key applications require approved CR and documented business justification'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Frequency', 'Task', 'Owner', 'Tool', 'Output'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['On-demand', 'Key purchase', 'Storage lead', 'Licensing portal', 'Key applied'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['On-demand', 'Key apply', 'Storage eng.', 'Array GUI/CLI', 'Feature active'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Quarterly', 'Key audit', 'Storage lead', 'CMDB + portal', 'Audit report'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Annual', 'FW compat check', 'Storage eng.', 'Dell compat matrix', 'Upgrade plan'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: FoD application is online; no downtime; feature available across all array nodes'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Feature intake = Formal request from app or business team; documented in ITSM ticket'))
    lines.append(txt_row('  Need validation = Storage team confirms requested feature is not already active or available'))
    lines.append(txt_row('  FW prereq check = Verify array firmware meets minimum version required for the FoD key'))
    lines.append(txt_row('  Budget sign-off = Finance approval for FoD key cost before purchase; include in request'))
    lines.append(txt_row('  Test in non-prod = Apply identical FoD key on non-production array first; validate feature'))
    lines.append(txt_row('  Verify feature  = After apply, confirm feature appears active in array management UI'))
    lines.append(txt_row('  CMDB reconcile = Compare array license list to CMDB records; update discrepancies'))
    lines.append(txt_row('  Key inventory  = Maintained list of all FoD keys: SN, feature, purchase date, applied date'))
    lines.append(txt_row('  Unused key review = Check for purchased but unapplied keys; ensure stored in vault securely'))
    lines.append(txt_row('  Portal reconcile = Compare licensing portal order history to key inventory; gaps indicate lost keys'))
    lines.append(txt_row('  FW compat check = Annual review of FoD keys against latest firmware; ensure no incompatibility'))
    lines.append(txt_row('  CR             = Change Request; ITSM ticket documenting reason and approver for FoD apply'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-fod-ops-backup',
            'docs/storage/dell/fod/operations/backup-restore/index.md',
            'Dell FoD — Backup and restore operations')
def dell_fod_ops_backup():
    """Dell FoD backup/restore — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell FoD — Backup and Restore'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FoD backup: protect license key files and array configuration for restore scenarios')))
    lines.append(R(bMid(IV_L, IV_R, 'Key backup: store .lic files in vault; keys always re-downloadable from Dell portal')))
    lines.append(R(bMid(IV_L, IV_R, 'Config backup: export array license list before and after each FoD key application')))
    lines.append(R(bMid(IV_L, IV_R, 'Restore: re-apply key from portal if array replaced or controller swap occurs')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Apply key → export license config → store in vault → portal re-download available if needed'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key Backup'), bMid(B2_L, B2_R, 'Config Backup'), bMid(B3_L, B3_R, 'Restore'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Vault storage'), bMid(B2_L, B2_R, 'Pre-apply export'), bMid(B3_L, B3_R, 'Re-download'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Portal re-DL'), bMid(B2_L, B2_R, 'Post-apply export'), bMid(B3_L, B3_R, 'Re-apply key'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Encrypted share'), bMid(B2_L, B2_R, 'Diff verify'), bMid(B3_L, B3_R, 'Ctrl swap'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key inventory'), bMid(B2_L, B2_R, 'CMDB entry'), bMid(B3_L, B3_R, 'Array replace'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Version track'), bMid(B2_L, B2_R, 'Change record'), bMid(B3_L, B3_R, 'Verify feature'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  FoD keys tied to array SN; controller swap on same chassis does not require new key'))
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
                             ['Key re-DL', 'Array replace', 'Licensing portal', 'Storage eng.', 'On-demand'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Verify feature', 'After restore', 'Array GUI', 'Storage eng.', 'Per restore'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: .lic files stored in HashiCorp Vault or CyberArk; do not store in plain-text repos'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Key vault      = Secure secret manager (HashiCorp Vault, CyberArk) for .lic file storage'))
    lines.append(txt_row('  Portal re-DL   = FoD keys always re-downloadable from Dell Licensing Portal by order/SN'))
    lines.append(txt_row('  Pre-apply export = Array license list snapshot before key; used as rollback reference'))
    lines.append(txt_row('  Post-apply export = Array license list after key; diff confirms expected feature activated'))
    lines.append(txt_row('  Diff verify    = Compare pre/post config exports; only new FoD feature should appear'))
    lines.append(txt_row('  Controller swap = Replacing failed controller in same chassis; SN unchanged; key still valid'))
    lines.append(txt_row('  Array replace  = Entire chassis replaced; new SN issued; request key re-issue from Dell'))
    lines.append(txt_row('  Key re-issue   = Dell Licensing team re-binds purchased FoD to new SN after array replace'))
    lines.append(txt_row('  Key inventory  = Master document tracking every FoD key: SN, feature, file name, vault path'))
    lines.append(txt_row('  Version track  = Each key application logged in inventory with version/date for audit trail'))
    lines.append(txt_row('  CMDB entry     = Configuration record updated with new active features post-apply'))
    lines.append(txt_row('  Encrypted share = Secondary backup of .lic files on encrypted file server alongside vault'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-fod-ops-procedures',
            'docs/storage/dell/fod/operations/procedures/index.md',
            'Dell FoD — Operational procedures')
def dell_fod_ops_procedures():
    """Dell FoD operational procedures — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell FoD — Operational Procedures'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FoD procedures: feature request, key purchase, key application, and quarterly audit')))
    lines.append(R(bMid(IV_L, IV_R, 'Request: document feature need in ITSM; validate prereqs; get budget approval')))
    lines.append(R(bMid(IV_L, IV_R, 'Apply: import .lic file via array GUI or CLI within approved CR change window')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit: quarterly reconcile of array license list against CMDB and key inventory')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Request → prereq → CR → purchase → download → vault → apply → verify → CMDB → close CR'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Request Phase'), bMid(B2_L, B2_R, 'Apply Phase'), bMid(B3_L, B3_R, 'Audit Phase'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ITSM ticket'), bMid(B2_L, B2_R, 'Log into array'), bMid(B3_L, B3_R, 'Array lic. list'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FW check'), bMid(B2_L, B2_R, 'Import .lic'), bMid(B3_L, B3_R, 'CMDB compare'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Raise CR'), bMid(B2_L, B2_R, 'Confirm active'), bMid(B3_L, B3_R, 'Inventory update'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Buy key'), bMid(B2_L, B2_R, 'Update CMDB'), bMid(B3_L, B3_R, 'Unused key check'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Store in vault'), bMid(B2_L, B2_R, 'Close CR'), bMid(B3_L, B3_R, 'Portal verify'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  FoD key application takes under 1 minute; no array downtime; all hosts unaffected'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Phase', 'Step', 'Tool', 'Owner', 'Duration'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Request', 'ITSM + prereqs', 'ITSM + portal', 'Storage lead', '1-2 days'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Purchase', 'Buy + download', 'Licensing portal', 'Storage lead', '1-3 days'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Apply', 'Import .lic', 'Array GUI/CLI', 'Storage eng.', '< 5 min'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Audit', 'Quarterly audit', 'CMDB + portal', 'Storage lead', '1-2 hours'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: apply FoD during business hours; no maintenance window required; zero-downtime'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  ITSM ticket    = Feature request logged in ServiceNow / Jira with business justification'))
    lines.append(txt_row('  FW check       = Verify array firmware meets minimum requirement listed in FoD release notes'))
    lines.append(txt_row('  Import .lic    = Array GUI: Settings > Licenses > Import License; browse to .lic file'))
    lines.append(txt_row('  Confirm active = After import, license status shows feature as Active in array license list'))
    lines.append(txt_row('  Close CR       = Mark CR resolved after CMDB updated and feature confirmed active'))
    lines.append(txt_row('  Array lic list = Full list of active licenses on array; export from GUI for audit comparison'))
    lines.append(txt_row('  CMDB compare   = Match array license list to CMDB entries; flag any discrepancies'))
    lines.append(txt_row('  Inventory update = Add new FoD key to inventory doc: feature, SN, applied date, applied by'))
    lines.append(txt_row('  Unused key check = Keys purchased but not applied; confirm stored in vault; plan application'))
    lines.append(txt_row('  Portal verify  = Confirm licensing portal order history matches keys in local inventory'))
    lines.append(txt_row('  Store in vault = Save .lic file to HashiCorp Vault immediately after download from portal'))
    lines.append(txt_row('  Zero-downtime  = FoD application does not interrupt I/O; hosts and workloads unaffected'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-fod-security', 'docs/storage/dell/fod/security/index.md',
            'Dell FoD — Security overview')
def dell_fod_security():
    """Dell FoD security overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell FoD — Security'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FoD security: protect license keys, restrict who can apply features, and audit all changes')))
    lines.append(R(bMid(IV_L, IV_R, 'Key protection: store .lic files in secure vault; never commit to source control or email')))
    lines.append(R(bMid(IV_L, IV_R, 'Access control: only named storage engineers can apply FoD keys; RBAC on array GUI')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit: all FoD applications logged in array event log and ITSM; quarterly reconcile')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key in vault → named engineer with CR → apply via RBAC-controlled GUI → audit trail'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key Security'), bMid(B2_L, B2_R, 'Access Control'), bMid(B3_L, B3_R, 'Audit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Vault storage'), bMid(B2_L, B2_R, 'Named engineers'), bMid(B3_L, B3_R, 'Array event log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No email/SCM'), bMid(B2_L, B2_R, 'Array RBAC'), bMid(B3_L, B3_R, 'ITSM CR record'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Encrypted share'), bMid(B2_L, B2_R, 'CR required'), bMid(B3_L, B3_R, 'Quarterly audit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Portal MFA'), bMid(B2_L, B2_R, '2-person rule'), bMid(B3_L, B3_R, 'CMDB diff'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key rotation N/A'), bMid(B2_L, B2_R, 'Offboard revoke'), bMid(B3_L, B3_R, 'Portal history'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  FoD keys do not expire; lost or leaked keys cannot be remotely revoked; vault is critical'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Control', 'Implementation', 'Standard', 'Tool', 'Owner'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Key storage', 'Vault only', 'Sec policy', 'HashiCorp Vault', 'Storage lead'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Apply access', 'Named + CR', 'Change ctrl', 'Array RBAC', 'Storage lead'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Portal access', 'MFA enforced', 'NIST 800-63', 'Dell SSO + MFA', 'Storage lead'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Audit log', 'Quarterly review', 'SOC 2', 'ITSM + array log', 'Sec team'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: FoD .lic files never stored in unencrypted locations; vault access is MFA-gated'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Vault storage  = All .lic files stored in HashiCorp Vault or CyberArk; access logged'))
    lines.append(txt_row('  No email/SCM   = Never send .lic files via email or store in Git/Jira; vault only'))
    lines.append(txt_row('  Portal MFA     = Dell Licensing Portal requires MFA; enforce org-wide in portal settings'))
    lines.append(txt_row('  Named engineers = Limit FoD apply privilege to 2-3 storage engineers; document by name'))
    lines.append(txt_row('  Array RBAC     = Only Storage Admin role on array can import license keys; not Operator'))
    lines.append(txt_row('  CR required    = No FoD key applied without approved ITSM CR; prevents unauthorized changes'))
    lines.append(txt_row('  2-person rule  = FoD apply observed by second engineer; prevents unauthorized feature unlock'))
    lines.append(txt_row('  Offboard revoke = When storage engineer leaves, remove array RBAC and vault access immediately'))
    lines.append(txt_row('  Key rotation   = FoD keys do not rotate; protect the original; report loss to Dell licensing'))
    lines.append(txt_row('  Quarterly audit = Review portal history vs CMDB; detect unauthorized feature activation'))
    lines.append(txt_row('  Portal history = Dell Licensing Portal logs all key downloads; review for unauthorized access'))
    lines.append(txt_row('  CMDB diff      = Quarterly comparison of array active license list to CMDB; flag surprises'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-fod-security-access',
            'docs/storage/dell/fod/security/access-control/index.md',
            'Dell FoD — Access control')
def dell_fod_security_access():
    """Dell FoD access control — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell FoD — Access Control'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FoD access control: who can purchase keys, download files, apply licenses, and audit')))
    lines.append(R(bMid(IV_L, IV_R, 'Portal access: only named storage leads with MFA-enabled Dell accounts can purchase')))
    lines.append(R(bMid(IV_L, IV_R, 'Array access: only Storage Admin role can import license keys; Operator cannot')))
    lines.append(R(bMid(IV_L, IV_R, 'Vault access: only named engineers can retrieve .lic files; access is MFA-gated')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Purchase (storage lead) → vault store → retrieve (named eng.) → apply (admin role) → logged'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Portal Access'), bMid(B2_L, B2_R, 'Array Access'), bMid(B3_L, B3_R, 'Vault Access'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Named leads only'), bMid(B2_L, B2_R, 'Admin role only'), bMid(B3_L, B3_R, 'Named engineers'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MFA enforced'), bMid(B2_L, B2_R, 'LDAP/AD group'), bMid(B3_L, B3_R, 'MFA required'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dell SSO'), bMid(B2_L, B2_R, 'No shared acct'), bMid(B3_L, B3_R, 'Access log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Account audit'), bMid(B2_L, B2_R, 'CR pre-apply'), bMid(B3_L, B3_R, 'Lease expiry'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'IP restrict'), bMid(B2_L, B2_R, 'Quarterly review'), bMid(B3_L, B3_R, 'Offboard revoke'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  On engineer offboarding: revoke Dell portal access, array RBAC, and vault lease immediately'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['System', 'Who', 'Auth Method', 'Review Freq', 'Owner'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Dell portal', 'Storage leads', 'Dell SSO + MFA', 'Quarterly', 'Storage lead'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Array GUI', 'Named admins', 'LDAP + RBAC', 'Quarterly', 'Storage lead'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Vault', 'Named engineers', 'MFA token', 'Quarterly', 'Sec team'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['CMDB', 'Ops team', 'Service acct', 'Annual', 'Ops lead'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: array GUI RBAC enforced; no direct filesystem or iDRAC access needed for FoD apply'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Portal access  = Access to Dell Licensing Portal; limit to storage leads who handle purchasing'))
    lines.append(txt_row('  Admin role     = Array management role with license import rights; separate from Operator'))
    lines.append(txt_row('  LDAP group     = Array admin rights controlled via AD group; add/remove via directory'))
    lines.append(txt_row('  No shared acct = Each engineer has individual array admin account; shared accounts banned'))
    lines.append(txt_row('  CR pre-apply   = ITSM CR must be approved before any engineer retrieves key from vault'))
    lines.append(txt_row('  Vault lease    = HashiCorp Vault access token with TTL; expires and must be renewed'))
    lines.append(txt_row('  MFA required   = Both Dell portal and vault require MFA; prevents credential-only access'))
    lines.append(txt_row('  Account audit  = Quarterly review of Dell portal accounts; remove leavers and excess access'))
    lines.append(txt_row('  Quarterly review = Storage lead reviews who has array admin and vault access; remove if not needed'))
    lines.append(txt_row('  Offboard revoke = Immediate removal from portal, LDAP group, and vault on engineer departure'))
    lines.append(txt_row('  IP restrict    = Dell portal can restrict login to corporate IP ranges; reduces phishing risk'))
    lines.append(txt_row('  Lease expiry   = Vault lease auto-expires; reduces risk of standing access to .lic files'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-fod-security-auth',
            'docs/storage/dell/fod/security/authentication/index.md',
            'Dell FoD — Authentication')
def dell_fod_security_auth():
    """Dell FoD authentication — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell FoD — Authentication'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FoD authentication: secure access to Dell portal, array management, and key vault')))
    lines.append(R(bMid(IV_L, IV_R, 'Dell portal: Dell SSO with MFA (TOTP or hardware key); tied to support account')))
    lines.append(R(bMid(IV_L, IV_R, 'Array GUI: local accounts or LDAP/AD integration; Storage Admin role for license import')))
    lines.append(R(bMid(IV_L, IV_R, 'Vault: LDAP or AppRole auth with MFA token; short-lived lease; audit log per access')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Dell portal MFA → download key → vault MFA store → array LDAP auth → import license'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Portal Auth'), bMid(B2_L, B2_R, 'Array Auth'), bMid(B3_L, B3_R, 'Vault Auth'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dell SSO'), bMid(B2_L, B2_R, 'Local accounts'), bMid(B3_L, B3_R, 'LDAP method'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TOTP MFA'), bMid(B2_L, B2_R, 'LDAP / AD'), bMid(B3_L, B3_R, 'AppRole method'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Hardware key'), bMid(B2_L, B2_R, 'SSH key auth'), bMid(B3_L, B3_R, 'Short TTL lease'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Session timeout'), bMid(B2_L, B2_R, 'Password policy'), bMid(B3_L, B3_R, 'MFA wrapper'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'IP allowlist'), bMid(B2_L, B2_R, 'Account lockout'), bMid(B3_L, B3_R, 'Access log'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  All three systems require individual named accounts; no service accounts for FoD apply'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['System', 'Method', 'MFA', 'Session TTL', 'Lockout'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Dell portal', 'Dell SSO', 'TOTP/HW key', '30 min idle', '5 attempts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Array GUI', 'LDAP/local', 'N/A (LDAP MFA)', '60 min idle', '5 attempts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Vault', 'LDAP/AppRole', 'TOTP required', 'Lease TTL 1h', 'N/A (lease)'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Array CLI', 'SSH key', 'N/A', 'Session only', '5 attempts'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: auth tokens never stored on shared systems; personal TOTP app or hardware key only'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Dell SSO      = Dell identity provider for support.dell.com and licensing.dell.com'))
    lines.append(txt_row('  TOTP MFA      = Time-based One-Time Password; Google/Microsoft Authenticator app'))
    lines.append(txt_row('  Hardware key  = YubiKey or similar FIDO2 key; strongest MFA option for portal access'))
    lines.append(txt_row('  LDAP auth     = Array authenticates engineers via Active Directory; groups control roles'))
    lines.append(txt_row('  AppRole       = HashiCorp Vault machine auth method; used by automation scripts'))
    lines.append(txt_row('  Short TTL     = Vault lease expires in 1 hour; engineer must re-auth to retrieve another key'))
    lines.append(txt_row('  MFA wrapper   = Vault LDAP auth combined with TOTP second factor; both required'))
    lines.append(txt_row('  SSH key auth  = Array CLI accessed via SSH keypair only; disable password SSH on all arrays'))
    lines.append(txt_row('  Password policy = Array local accounts: 12+ chars, complexity, 90-day rotation'))
    lines.append(txt_row('  Account lockout = 5 failed attempts locks account; admin or LDAP reset required'))
    lines.append(txt_row('  IP allowlist  = Dell portal access restricted to corporate egress IP; home access blocked'))
    lines.append(txt_row('  Session timeout = Portal and array GUI auto-logout after idle period; re-auth required'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-fod-security-encryption',
            'docs/storage/dell/fod/security/encryption/index.md',
            'Dell FoD — Encryption of license key files')
def dell_fod_security_encryption():
    """Dell FoD encryption — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell FoD — Encryption'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FoD encryption: protect .lic key files in transit and at rest; portal uses TLS 1.2+')))
    lines.append(R(bMid(IV_L, IV_R, 'Key files: FoD .lic files are cryptographically signed by Dell; cannot be forged')))
    lines.append(R(bMid(IV_L, IV_R, 'At rest: .lic files stored in encrypted vault (AES-256); never stored in plaintext')))
    lines.append(R(bMid(IV_L, IV_R, 'In transit: portal download over TLS 1.2+; array import over HTTPS management plane')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Portal TLS download → vault AES-256 storage → HTTPS import to array → signature verified'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key File Security'), bMid(B2_L, B2_R, 'Transit'), bMid(B3_L, B3_R, 'At Rest'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dell PKI signed'), bMid(B2_L, B2_R, 'TLS 1.2+'), bMid(B3_L, B3_R, 'Vault AES-256'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SN binding'), bMid(B2_L, B2_R, 'HTTPS portal'), bMid(B3_L, B3_R, 'Encrypted share'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Tamper evident'), bMid(B2_L, B2_R, 'HTTPS array mgmt'), bMid(B3_L, B3_R, 'Never plaintext'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Sig verification'), bMid(B2_L, B2_R, 'No email/FTP'), bMid(B3_L, B3_R, 'Key access log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No re-use'), bMid(B2_L, B2_R, 'Cert pinning'), bMid(B3_L, B3_R, 'Backup encrypted'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Array firmware verifies Dell PKI signature on .lic file; rejects unsigned or modified files'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Layer', 'Algorithm', 'Applied To', 'Owner', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Key signature', 'Dell PKI/RSA', 'Every .lic file', 'Dell', 'Verified on import'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Transit', 'TLS 1.2+', 'Download + import', 'Dell + customer', 'HTTPS only'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['At rest', 'AES-256', 'Vault storage', 'Customer', 'Vault-managed key'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Backup', 'AES-256', 'Encrypted share', 'Customer', 'Mirror of vault'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: .lic files never transit unencrypted network segments; TLS or encrypted channel only'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Dell PKI       = Dell Public Key Infrastructure; signs every FoD .lic file with private key'))
    lines.append(txt_row('  Sig verification = Array firmware checks Dell public key signature on .lic at import time'))
    lines.append(txt_row('  Tamper evident = Any modification to .lic file content invalidates the Dell PKI signature'))
    lines.append(txt_row('  SN binding     = .lic cryptographic content includes the target array serial number'))
    lines.append(txt_row('  No re-use      = A FoD key for SN-A cannot be applied to SN-B; signature check fails'))
    lines.append(txt_row('  TLS 1.2+       = Dell portal and array management plane require TLS 1.2 minimum'))
    lines.append(txt_row('  No email/FTP   = .lic files must not transit unencrypted channels; vault and HTTPS only'))
    lines.append(txt_row('  Cert pinning   = Array management HTTPS; trust only Dell-issued cert; rejects MITM cert'))
    lines.append(txt_row('  Vault AES-256  = HashiCorp Vault encrypts all stored secrets (inc. .lic files) with AES-256'))
    lines.append(txt_row('  Key access log = Vault audit log records every read of a .lic file; who, when, IP'))
    lines.append(txt_row('  Backup encrypted = Secondary .lic backup on encrypted file server; same AES-256 protection'))
    lines.append(txt_row('  Vault-managed key = Vault handles AES-256 key rotation for stored secrets automatically'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-fod-security-hardening',
            'docs/storage/dell/fod/security/hardening/index.md',
            'Dell FoD — Hardening the FoD environment')
def dell_fod_security_hardening():
    """Dell FoD hardening — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell FoD — Hardening'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FoD hardening: secure the portal account, vault, array management, and audit workflow')))
    lines.append(R(bMid(IV_L, IV_R, 'Portal hardening: enforce MFA, IP allowlist, session timeout, and account review')))
    lines.append(R(bMid(IV_L, IV_R, 'Vault hardening: short-lived leases, MFA auth, LDAP backend, access log review')))
    lines.append(R(bMid(IV_L, IV_R, 'Array hardening: disable unused protocols, enforce LDAP auth, SSH key-only CLI')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Harden portal account → harden vault → harden array → audit controls → quarterly review'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Portal Hardening'), bMid(B2_L, B2_R, 'Vault Hardening'), bMid(B3_L, B3_R, 'Array Hardening'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Enforce MFA'), bMid(B2_L, B2_R, 'Short TTL lease'), bMid(B3_L, B3_R, 'SSH key-only'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'IP allowlist'), bMid(B2_L, B2_R, 'MFA + LDAP'), bMid(B3_L, B3_R, 'Disable HTTP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Session timeout'), bMid(B2_L, B2_R, 'Audit log review'), bMid(B3_L, B3_R, 'LDAP auth'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Account review'), bMid(B2_L, B2_R, 'Sealed vault'), bMid(B3_L, B3_R, 'Mgmt VLAN'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Offboard SOP'), bMid(B2_L, B2_R, 'Policy-as-code'), bMid(B3_L, B3_R, 'FW restrict'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Vault sealed when not in use; unseal requires quorum of key shares; reduces breach window'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Layer', 'Control', 'Setting', 'Standard', 'Owner'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Dell portal', 'Enforce MFA', 'Org-wide', 'NIST 800-63', 'Storage lead'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Vault', 'Short TTL', '1h lease max', 'CIS benchmark', 'Sec team'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Array', 'SSH key-only', 'Disable pw SSH', 'CIS L1', 'Infra team'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Network', 'Mgmt VLAN', 'Isolated VLAN', 'Sec policy', 'Network team'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: array management interface on isolated VLAN; only jumphost or VPN can reach it'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Portal MFA     = Enforce MFA for all Dell portal accounts; disable accounts that bypass it'))
    lines.append(txt_row('  IP allowlist   = Restrict portal login to corporate egress IPs; block personal/home access'))
    lines.append(txt_row('  Session timeout = Portal logs out after 30 min idle; vault lease expires in 1h'))
    lines.append(txt_row('  Sealed vault   = HashiCorp Vault sealed state; no secrets accessible until quorum unseal'))
    lines.append(txt_row('  Short TTL      = Vault leases expire in 1 hour; limits window of access after key retrieval'))
    lines.append(txt_row('  Policy-as-code = Vault ACL policies in HCL files under version control; reviewed each quarter'))
    lines.append(txt_row('  SSH key-only   = Disable password-based SSH on array; only pre-approved public keys allowed'))
    lines.append(txt_row('  Disable HTTP   = Array management only on HTTPS 443; no plaintext HTTP redirect'))
    lines.append(txt_row('  LDAP auth      = Array and vault use corporate AD/LDAP; no local service accounts for FoD'))
    lines.append(txt_row('  Mgmt VLAN      = Array management IPs on isolated VLAN; not reachable from user workstations'))
    lines.append(txt_row('  FW restrict    = Firewall allows only jumphost IP to reach array management VLAN'))
    lines.append(txt_row('  CIS L1         = Center for Internet Security Level 1 baseline applied to array OS'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-fod-troubleshooting', 'docs/storage/dell/fod/troubleshooting/index.md',
            'Dell FoD — Troubleshooting overview')
def dell_fod_troubleshooting():
    """Dell FoD troubleshooting — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell FoD — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FoD troubleshooting: key rejection, feature not activating, portal access failures')))
    lines.append(R(bMid(IV_L, IV_R, 'Key rejection: SN mismatch, wrong key scope, corrupt file — re-download from portal')))
    lines.append(R(bMid(IV_L, IV_R, 'Feature not active: firmware prereq not met, bundle partially applied, license conflict')))
    lines.append(R(bMid(IV_L, IV_R, 'Portal issues: account MFA locked, key not in order history, account link missing')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Symptom → check array event log → verify SN and FW → re-download if needed → Dell SR'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key Issues'), bMid(B2_L, B2_R, 'Feature Issues'), bMid(B3_L, B3_R, 'Portal Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Rejection error'), bMid(B2_L, B2_R, 'Not activating'), bMid(B3_L, B3_R, 'Login failure'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SN mismatch'), bMid(B2_L, B2_R, 'FW prereq fail'), bMid(B3_L, B3_R, 'Key not found'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Wrong scope'), bMid(B2_L, B2_R, 'Partial bundle'), bMid(B3_L, B3_R, 'No entitlement'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Corrupt file'), bMid(B2_L, B2_R, 'License conflict'), bMid(B3_L, B3_R, 'Account link'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Already applied'), bMid(B2_L, B2_R, 'Wrong array model'), bMid(B3_L, B3_R, 'MFA locked'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Collect: array SN, event log error text, firmware version, and portal order screenshot'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Symptom', 'Cause', 'Check', 'Fix', 'Escalate If'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Key rejected', 'SN mismatch', 'Array GUI SN', 'Re-download', 'After 2 tries'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Not active', 'FW prereq', 'Firmware ver.', 'Upgrade array', 'Dell TAC SR'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Portal login', 'MFA locked', 'Dell account', 'Account reset', 'Dell support'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Key missing', 'Wrong account', 'Order history', 'Link accounts', 'Dell licensing'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: confirm SN from chassis label; do not rely on documentation which may be outdated'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Rejection error = Array event log shows specific error code; note exact text for Dell TAC'))
    lines.append(txt_row('  SN mismatch    = Key file SN differs from array SN; most common FoD failure; re-download'))
    lines.append(txt_row('  Wrong scope    = Key unlocks different feature or tier than intended; verify before purchase'))
    lines.append(txt_row('  Corrupt file   = Download interrupted; browser saved incomplete .lic; re-download via HTTPS'))
    lines.append(txt_row('  FW prereq fail = Array firmware below minimum required for feature; upgrade before applying'))
    lines.append(txt_row('  Partial bundle = Bundle key partially active; some features of bundle blocked by FW prereq'))
    lines.append(txt_row('  License conflict = Two keys conflict on same feature; contact Dell TAC; do not apply more keys'))
    lines.append(txt_row('  Wrong array model = FoD key model-specific; a Unity key will not apply to a PowerStore'))
    lines.append(txt_row('  Already applied = Duplicate key import attempt; array shows duplicate; harmless but contact Dell'))
    lines.append(txt_row('  No entitlement = Support contract not linked to SN; contact Dell licensing team to link'))
    lines.append(txt_row('  Account link   = Link service tag to Dell support account via support.dell.com portal'))
    lines.append(txt_row('  MFA locked     = Too many failed MFA attempts; Dell support can unlock the portal account'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-fod-troubleshooting-issues',
            'docs/storage/dell/fod/troubleshooting/common-issues/index.md',
            'Dell FoD — Common troubleshooting issues')
def dell_fod_troubleshooting_issues():
    """Dell FoD common issues — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell FoD — Common Issues'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Common FoD issues: key rejection, feature mismatch, portal problems, and audit gaps')))
    lines.append(R(bMid(IV_L, IV_R, 'Key rejection: #1 issue is SN mismatch; verify SN in array GUI before contacting Dell')))
    lines.append(R(bMid(IV_L, IV_R, 'Feature mismatch: key unlocks different feature than expected; check key description')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit gap: keys applied without CMDB update; discovered in quarterly reconciliation')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Identify issue → check event log error → verify SN/FW/scope → fix or escalate → document'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key Problems'), bMid(B2_L, B2_R, 'Feature Problems'), bMid(B3_L, B3_R, 'Process Problems'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SN mismatch'), bMid(B2_L, B2_R, 'Wrong feature'), bMid(B3_L, B3_R, 'No CMDB entry'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Corrupt download'), bMid(B2_L, B2_R, 'FW too old'), bMid(B3_L, B3_R, 'No CR raised'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Wrong model key'), bMid(B2_L, B2_R, 'Bundle mismatch'), bMid(B3_L, B3_R, 'Lost key file'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Already applied'), bMid(B2_L, B2_R, 'Feature hidden'), bMid(B3_L, B3_R, 'Vault not used'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Account link'), bMid(B2_L, B2_R, 'Reboot needed'), bMid(B3_L, B3_R, 'Audit gap'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Prevention: always confirm SN from array GUI, verify FW, and use key inventory before apply'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Issue', 'Root Cause', 'Diagnostic', 'Resolution', 'Prevention'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Key rejected', 'SN mismatch', 'Array GUI SN', 'Re-download', 'Confirm SN first'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Wrong feature', 'Scope error', 'Key desc. text', 'Buy correct key', 'Read key desc.'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['FW too old', 'Prereq not met', 'FW version', 'Upgrade first', 'Check compat'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['No CMDB entry', 'Process skip', 'CMDB vs array', 'Update CMDB', 'CR as reminder'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: chassis SN label is authoritative; array GUI SN must match; check both if uncertain'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SN mismatch    = Most common FoD failure; key cryptographically bound to different SN'))
    lines.append(txt_row('  Corrupt download = Incomplete .lic; browser cache or network issue; clear cache and re-download'))
    lines.append(txt_row('  Wrong model key = FoD keys are model-specific; a PowerMax key will not import on Unity XT'))
    lines.append(txt_row('  Already applied = Same key imported twice; array event log shows duplicate; harmless warning'))
    lines.append(txt_row('  Account link   = FoD key not visible in portal because SN not linked to support account'))
    lines.append(txt_row('  Wrong feature  = Purchased key for Feature A but needed Feature B; verify before checkout'))
    lines.append(txt_row('  FW too old     = Most FoD features require minimum firmware; run compatibility check first'))
    lines.append(txt_row('  Bundle mismatch = Key enables a feature bundle but not all features in bundle apply to model'))
    lines.append(txt_row('  Feature hidden = Feature activated but UI element hidden; check Settings > Features for status'))
    lines.append(txt_row('  Reboot needed  = Some FoD features (rare) require array restart; check release notes'))
    lines.append(txt_row('  No CMDB entry  = Engineer applied key but skipped CMDB update; found at quarterly audit'))
    lines.append(txt_row('  Vault not used = .lic file stored in email or share; security gap; move to vault immediately'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram('dell-fod-troubleshooting-escalation',
            'docs/storage/dell/fod/troubleshooting/escalation/index.md',
            'Dell FoD — Escalation procedures')
def dell_fod_troubleshooting_escalation():
    """Dell FoD escalation — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell FoD — Escalation'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FoD escalation: when self-service fails, escalate to Dell licensing, TAC, or account team')))
    lines.append(R(bMid(IV_L, IV_R, 'Dell licensing: key re-issue for array replacement, SN re-binding, duplicate resolution')))
    lines.append(R(bMid(IV_L, IV_R, 'Dell TAC: feature not activating after valid key; firmware issues; event log errors')))
    lines.append(R(bMid(IV_L, IV_R, 'Account team: contract/entitlement disputes; key not tied to support contract')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Self-service fails → collect diagnostics → open Dell SR → licensing or TAC → account team'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Licensing Team'), bMid(B2_L, B2_R, 'Dell TAC'), bMid(B3_L, B3_R, 'Account Team'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key re-issue'), bMid(B2_L, B2_R, 'Feature inactive'), bMid(B3_L, B3_R, 'Entitlement'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SN re-binding'), bMid(B2_L, B2_R, 'Firmware bug'), bMid(B3_L, B3_R, 'Contract query'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Duplicate key'), bMid(B2_L, B2_R, 'License conflict'), bMid(B3_L, B3_R, 'Pricing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Account merge'), bMid(B2_L, B2_R, 'Event log error'), bMid(B3_L, B3_R, 'Exec escalation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Order history'), bMid(B2_L, B2_R, 'Bundle partial'), bMid(B3_L, B3_R, 'Account link'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Collect before escalating: array SN, .lic file, event log, firmware version, order number'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Issue Type', 'Escalate To', 'Info Needed', 'SLA', 'Contact'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Key rejected', 'Dell Licensing', 'SN + key file', '1 biz day', 'Licensing portal'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Feature inactive', 'Dell TAC', 'FW + event log', '4h P2 SLA', 'support.dell.com'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Contract issue', 'Account team', 'Contract ID', '1 biz day', 'Dell rep'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
                             ['Exec escalate', 'Account exec', 'SR number', 'Same day', 'Account team'])))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: collect chassis SN label photo; compare to portal before opening any escalation'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Dell Licensing = Dell team managing FoD key purchase, SN binding, and re-issue processes'))
    lines.append(txt_row('  SN re-binding  = Re-issuing FoD key for a replacement array with new serial number'))
    lines.append(txt_row('  Account merge  = Consolidating two Dell portal accounts that each hold keys for same array'))
    lines.append(txt_row('  Duplicate key  = Same key applied twice or purchased twice; licensing team resolves billing'))
    lines.append(txt_row('  Dell TAC       = Technical Assistance Center; handles firmware and feature activation issues'))
    lines.append(txt_row('  Bundle partial = Some features in a bundle not activating; TAC debugs feature flag state'))
    lines.append(txt_row('  License conflict = Two conflicting FoD features applied; TAC resolves with Dell backend'))
    lines.append(txt_row('  Event log      = Array event log showing exact error code and text from failed key import'))
    lines.append(txt_row('  Order number   = Dell purchase order number; required for licensing team to locate key history'))
    lines.append(txt_row('  P2 SLA         = 4-hour TAC response; FoD failure blocking production may qualify'))
    lines.append(txt_row('  Account exec   = Dell account executive; involved for contract disputes or exec escalation'))
    lines.append(txt_row('  SR number      = Service Request tracking number; always reference when following up'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powermax',
    'docs/storage/dell/powermax/index.md',
    'Dell PowerMax — NVMe enterprise array; SLO tiers; SRDF replication; TimeFinder snapshots',
)
def dell_powermax():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerMax Enterprise Storage'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'PowerMax: Dell enterprise NVMe array; all-NVMe (2000) or NVMe+SAS (8000) tiers')))
    lines.append(R(bMid(IV_L, IV_R, 'SLO-based provisioning: Diamond/Platinum/Gold/Silver/Bronze maps workload to media tier')))
    lines.append(R(bMid(IV_L, IV_R, 'SRDF replication: Metro (active-active), Sync, Async, Adaptive Copy modes')))
    lines.append(R(bMid(IV_L, IV_R, 'Managed via Unisphere GUI and symcli (SYMAPI); REST API for automation')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Hosts connect via FA directors → SLO maps I/O to SRP tier → SRDF replicates to partner array'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Architecture'), bMid(B2_L, B2_R, 'Operations'), bMid(B3_L, B3_R, 'Security'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Director blades'), bMid(B2_L, B2_R, 'Unisphere GUI'), bMid(B3_L, B3_R, 'DARE encryption'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SRP thin pools'), bMid(B2_L, B2_R, 'symcli / SYMAPI'), bMid(B3_L, B3_R, 'LDAP / AD auth'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SLO tiers'), bMid(B2_L, B2_R, 'TimeFinder snaps'), bMid(B3_L, B3_R, 'Masking views'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SRDF directors'), bMid(B2_L, B2_R, 'SRDF replication'), bMid(B3_L, B3_R, 'Audit logging'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NVMe / SAS media'), bMid(B2_L, B2_R, 'REST API'), bMid(B3_L, B3_R, 'Host access ctrl'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Data path: host HBA → FA director port → SRP pool tier → DA director → NVMe/SAS drives'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Category', 'PowerMax 2000', 'PowerMax 8000', 'Protocol', 'Replication'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Media', 'All-NVMe', 'NVMe + SAS', 'FC / FICON', 'SRDF/Metro'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Capacity', 'Up to 4 PB', 'Up to 4 PB+', 'iSCSI', 'SRDF/Sync'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Directors', '6 directors', '8+ directors', 'NVMe/FC', 'SRDF/Async'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Tier', 'Mid-range', 'Flagship', '—', 'Adaptive Copy'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: PowerMax chassis (2U/4U enclosure); director modules; NVMe/SAS bays; dual power'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SRP          = Storage Resource Pool; thin provisioning pool aligned to SLO tier'))
    lines.append(txt_row('  SLO          = Service Level Objective; Diamond/Platinum/Gold/Silver/Bronze/Optimized'))
    lines.append(txt_row('  SRDF         = Symmetrix Remote Data Facility; block-level array-to-array replication'))
    lines.append(txt_row('  SRDF/Metro   = Active-active sync replication; both sites serve I/O simultaneously'))
    lines.append(txt_row('  TimeFinder   = Local copy: /Snap (thin pointer), /Clone (full), /VP Snap (virtual)'))
    lines.append(txt_row('  FA director  = Front-End Adapter; host-facing FC / iSCSI / NVMe-oF ports'))
    lines.append(txt_row('  DA director  = Disk Adapter; back-end NVMe / SAS drive connectivity'))
    lines.append(txt_row('  RDF director = Remote Data Facility; SRDF link ports between partner arrays'))
    lines.append(txt_row('  DARE         = Data At Rest Encryption; self-encrypting drives managed by key server'))
    lines.append(txt_row('  Masking view = Host access control: storage group + port group + initiator group'))
    lines.append(txt_row('  Unisphere    = Web-based management GUI for PowerMax; REST API surface'))
    lines.append(txt_row('  symcli       = SYMAPI command-line toolkit: syminq, symsg, symdg, symrdf, symsnap'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powermax-arch-design-standards',
    'docs/storage/dell/powermax/architecture/design-standards/index.md',
    'Dell PowerMax design standards — SLO selection, SRDF topology, zoning, SRP sizing',
)
def dell_powermax_arch_design_standards():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerMax Architecture Design Standards'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Design standards define SLO selection, SRDF topology, FC zoning, and SRP sizing rules')))
    lines.append(R(bMid(IV_L, IV_R, 'SLO tier matched to workload IOPS profile: Diamond = latency-critical, Bronze = archive')))
    lines.append(R(bMid(IV_L, IV_R, 'SRDF topology: Metro for zero-RPO HA, Async for DR; Adaptive Copy for data movement')))
    lines.append(R(bMid(IV_L, IV_R, 'FC zoning: single-initiator / single-target per zone; no zone sprawl across fabrics')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Profile workload → select SLO → size SRP → define masking view → configure SRDF topology'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SLO Standards'), bMid(B2_L, B2_R, 'SRDF Standards'), bMid(B3_L, B3_R, 'Zoning Standards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Diamond: <1ms DB'), bMid(B2_L, B2_R, 'Metro: zero RPO'), bMid(B3_L, B3_R, 'SI/ST per zone'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Platinum: <2ms'), bMid(B2_L, B2_R, 'Sync: near-zero'), bMid(B3_L, B3_R, '2 fabrics min'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Gold: <5ms mixed'), bMid(B2_L, B2_R, 'Async: RPO mins'), bMid(B3_L, B3_R, 'VSAN tagging'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Silver: <10ms'), bMid(B2_L, B2_R, 'Adaptive: bulk'), bMid(B3_L, B3_R, 'NPIV per host'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Bronze: archive'), bMid(B2_L, B2_R, 'RDF group per SG'), bMid(B3_L, B3_R, 'No zone sprawl'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  SRP sizing → SRDF consistency group → masking view → host-side multipath (PowerPath/MPIO)'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Standard', 'Rule', 'Rationale', 'Anti-pattern', 'Impact'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['SLO', 'Match IOPS tier', 'Predictable perf', 'All Diamond', 'Cost overrun'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['SRP', 'Per-workload pool', 'Avoid contention', 'One SRP all', 'Noisy neighbor'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['SRDF', 'Metro + Async', 'HA + DR layers', 'Sync only', 'No DR fallback'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Zoning', 'SI/ST per zone', 'Fault isolation', 'Multi-init zone', 'Masking gaps'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: dual-fabric SAN; RDF directors on dedicated SRDF links; separate mgmt network'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SI/ST          = Single-Initiator/Single-Target; one HBA port and one array port per zone'))
    lines.append(txt_row('  SRDF Metro     = Active-active stretch cluster; both R1 and R2 volumes serve production I/O'))
    lines.append(txt_row('  SRDF Async     = Asynchronous replication; RPO in seconds to minutes; DR site standby'))
    lines.append(txt_row('  Adaptive Copy  = Non-disruptive bulk migration or data movement; no consistency guarantee'))
    lines.append(txt_row('  RDF group      = Logical SRDF pairing; each group maps one set of volumes to a remote array'))
    lines.append(txt_row('  NPIV           = N-Port ID Virtualization; virtual WWN per VM for per-VM zoning'))
    lines.append(txt_row('  Consistency grp= SRDF consistency group; ensures write-order fidelity across volumes'))
    lines.append(txt_row('  PowerPath      = Dell multipath driver; load balancing and failover for PowerMax hosts'))
    lines.append(txt_row('  MPIO           = Native OS multipath (Windows/Linux) as alternative to PowerPath'))
    lines.append(txt_row('  Noisy neighbor = SRP contention when unrelated workloads share a pool; mitigated by SLO'))
    lines.append(txt_row('  VSAN tagging   = Brocade/Cisco zoning attribute to restrict zone scope to a VSAN'))
    lines.append(txt_row('  Zone sprawl    = Excessive zone membership causing management overhead and masking risk'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powermax-operations',
    'docs/storage/dell/powermax/operations/index.md',
    'Dell PowerMax operations — day-2 tasks; SRDF management; TimeFinder; health checks',
)
def dell_powermax_operations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerMax Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Day-2 operations: SRDF state management, TimeFinder copies, SLO rebalancing, capacity')))
    lines.append(R(bMid(IV_L, IV_R, 'SRDF suspend/resume, failover/failback, and swap-personality for planned maintenance')))
    lines.append(R(bMid(IV_L, IV_R, 'TimeFinder: create/restore snaps; snap schedules; VP Snap and Clone for test/dev')))
    lines.append(R(bMid(IV_L, IV_R, 'Health: Unisphere alerts, SYMAPI event logs, CloudIQ analytics, SCG-based reporting')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Monitor alerts → run health checks → execute SRDF or TimeFinder action → verify and close'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SRDF Operations'), bMid(B2_L, B2_R, 'TimeFinder Ops'), bMid(B3_L, B3_R, 'Capacity / Health'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Suspend / Resume'), bMid(B2_L, B2_R, 'Snap establish'), bMid(B3_L, B3_R, 'SRP utilization'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Failover / Failbk'), bMid(B2_L, B2_R, 'Snap restore'), bMid(B3_L, B3_R, 'CloudIQ health'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Swap personality'), bMid(B2_L, B2_R, 'Clone split'), bMid(B3_L, B3_R, 'Unisphere alerts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Group consistency'), bMid(B2_L, B2_R, 'VP Snap mount'), bMid(B3_L, B3_R, 'FE port stats'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RDF link monitor'), bMid(B2_L, B2_R, 'Snap schedule'), bMid(B3_L, B3_R, 'Capacity trends'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  SRDF state check → TimeFinder snap/clone → SRP capacity review → alert remediation loop'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Task', 'Tool', 'CLI command', 'Frequency', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['SRDF check', 'symrdf', 'symrdf -g query', 'Daily', 'Check link state'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Snap create', 'symsnap', 'symsnap -sg est', 'Per schedule', 'Verify gen count'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['SRP usage', 'Unisphere', 'symcfg list -srp', 'Weekly', 'Alert >80%'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Health alerts', 'CloudIQ', 'REST API poll', 'Continuous', 'SCG required'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: Unisphere on embedded mgmt network; SCG phone-home for CloudIQ telemetry relay'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  symrdf         = SYMAPI CLI tool for SRDF state management (query, suspend, failover, swap)'))
    lines.append(txt_row('  symsnap        = SYMAPI CLI tool for TimeFinder/Snap operations (establish, restore, term)'))
    lines.append(txt_row('  symdg          = SYMAPI device group tool; groups volumes for consistent SRDF/snap ops'))
    lines.append(txt_row('  symsg          = SYMAPI storage group tool; list, modify, and provision storage groups'))
    lines.append(txt_row('  Swap personality = SRDF planned failover; R1 becomes R2 and vice versa at recovery site'))
    lines.append(txt_row('  VP Snap        = Virtual Provisioning Snap; pointer-based thin snap mounted on a host'))
    lines.append(txt_row('  RDF link       = Physical or virtual ISL between PowerMax arrays for SRDF traffic'))
    lines.append(txt_row('  SCG            = Secure Connect Gateway; phone-home proxy for CloudIQ telemetry'))
    lines.append(txt_row('  SRP utilization= Percentage of thin pool capacity consumed; alert threshold typically 80%'))
    lines.append(txt_row('  FE port stats  = Front-End director port I/O stats; check for hotspot or imbalance'))
    lines.append(txt_row('  Snap schedule  = Automated TimeFinder snap generation policy (hourly/daily/weekly)'))
    lines.append(txt_row('  Clone split    = Full physical copy created from Clone; independent of source after split'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powermax-security',
    'docs/storage/dell/powermax/security/index.md',
    'Dell PowerMax security — DARE encryption, LDAP auth, masking views, audit logging',
)
def dell_powermax_security():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerMax Security'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'PowerMax security: DARE (drive-level encryption), masking views, LDAP/AD, audit log')))
    lines.append(R(bMid(IV_L, IV_R, 'DARE: self-encrypting drives; keys managed by external KMIP server or local vault')))
    lines.append(R(bMid(IV_L, IV_R, 'Host access: masking views (storage group + port group + initiator group) — no masking view')))
    lines.append(R(bMid(IV_L, IV_R, 'LDAP/AD integration for Unisphere GUI roles; local accounts for emergency break-glass')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  DARE encrypts drives at rest → masking view controls host access → LDAP controls admin auth'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Encryption'), bMid(B2_L, B2_R, 'Access Control'), bMid(B3_L, B3_R, 'Auth / Audit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DARE (SED drives)'), bMid(B2_L, B2_R, 'Storage group'), bMid(B3_L, B3_R, 'LDAP / AD roles'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'KMIP key server'), bMid(B2_L, B2_R, 'Port group'), bMid(B3_L, B3_R, 'Local break-glass'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key rotation'), bMid(B2_L, B2_R, 'Initiator group'), bMid(B3_L, B3_R, 'Audit log export'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Crypto erase'), bMid(B2_L, B2_R, 'Masking view'), bMid(B3_L, B3_R, 'SYSLOG forward'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TLS mgmt plane'), bMid(B2_L, B2_R, 'No access = deny'), bMid(B3_L, B3_R, 'SNMP v3'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  SED key rotation → masking view review → LDAP role audit → syslog review cycle'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Control', 'Mechanism', 'Standard', 'Exception', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Encryption', 'DARE + KMIP', 'All volumes', 'Key server down', 'Key audit log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Host access', 'Masking view', 'Deny by default', 'None allowed', 'Masking report'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Admin auth', 'LDAP / AD', 'Role-based', 'Local only', 'Login events'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Logging', 'Syslog/SNMP', 'Offsite SIEM', '—', 'All changes'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SEDs in drive bays; KMIP server on isolated security VLAN; mgmt on OOB network'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  DARE           = Data At Rest Encryption; drive-level encryption using self-encrypting drives'))
    lines.append(txt_row('  SED            = Self-Encrypting Drive; encryption/decryption in drive controller hardware'))
    lines.append(txt_row('  KMIP           = Key Management Interoperability Protocol; standard for external key servers'))
    lines.append(txt_row('  Crypto erase   = Destroy SED encryption key making all data unrecoverable; used for decommission'))
    lines.append(txt_row('  Masking view   = Binding of storage group + port group + initiator group; controls host access'))
    lines.append(txt_row('  Storage group  = Logical collection of volumes presented to a host via masking view'))
    lines.append(txt_row('  Port group     = Collection of array FA director ports included in a masking view'))
    lines.append(txt_row('  Initiator group= Collection of host HBA WWNs or iSCSI IQNs mapped in masking view'))
    lines.append(txt_row('  Break-glass    = Local admin account for emergency access when LDAP is unavailable'))
    lines.append(txt_row('  SIEM           = Security Information and Event Management; receives syslog from PowerMax'))
    lines.append(txt_row('  TLS mgmt plane = Unisphere REST API and GUI encrypted with TLS 1.2+ on management NIC'))
    lines.append(txt_row('  SNMP v3        = Encrypted/authenticated SNMP for monitoring integration'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powermax-troubleshooting',
    'docs/storage/dell/powermax/troubleshooting/index.md',
    'Dell PowerMax troubleshooting — SRDF link issues, masking errors, perf, DARE key faults',
)
def dell_powermax_troubleshooting():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerMax Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Common faults: SRDF link degraded, masking view missing, SRP near-full, DARE key unreachable')))
    lines.append(R(bMid(IV_L, IV_R, 'SRDF: check RDF link state, RDF group consistency, and ISL utilization on fabric')))
    lines.append(R(bMid(IV_L, IV_R, 'Masking: verify initiator group WWN, port group FA ports, and storage group membership')))
    lines.append(R(bMid(IV_L, IV_R, 'Performance: identify hot SLO tier, FA port saturation, or SRP over-commitment')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Alert fires → check Unisphere event log → run symrdf/symcfg → isolate layer → remediate'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SRDF Issues'), bMid(B2_L, B2_R, 'Host / Masking'), bMid(B3_L, B3_R, 'Perf / Capacity'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Link degraded'), bMid(B2_L, B2_R, 'Host sees no LUN'), bMid(B3_L, B3_R, 'SRP >80% full'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Out of sync'), bMid(B2_L, B2_R, 'Wrong initiator'), bMid(B3_L, B3_R, 'FA port saturated'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Suspended state'), bMid(B2_L, B2_R, 'No port group'), bMid(B3_L, B3_R, 'SLO not met'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Group split'), bMid(B2_L, B2_R, 'Masking missing'), bMid(B3_L, B3_R, 'DARE key timeout'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ISL congestion'), bMid(B2_L, B2_R, 'HBA offline'), bMid(B3_L, B3_R, 'Snap gen full'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Isolate layer (fabric / array / host) → confirm with symrdf -g query or symcfg list'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Symptom', 'First check', 'Tool', 'Fix', 'Escalate if'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['SRDF link down', 'RDF link state', 'symrdf -g query', 'Resume link', 'Link stays down'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['No LUN visible', 'Masking view', 'symmask list', 'Fix masking', 'Zoning correct'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Perf degraded', 'SLO compliance', 'Unisphere perf', 'Rebalance SRP', 'SLO breach cont.'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['DARE key error', 'KMIP reachable', 'Unisphere alert', 'Fix KMIP reach', 'Array locked out'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: check RDF director LEDs; FA port LEDs; ISL port counters on SAN switch'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  RDF link state = SRDF link health: In Sync / Suspended / Failed / Consistent states'))
    lines.append(txt_row('  Snap gen full  = TimeFinder/Snap generation limit reached; oldest snap must be terminated'))
    lines.append(txt_row('  SLO compliance = Percentage of volumes meeting their Service Level Objective latency target'))
    lines.append(txt_row('  symmask        = SYMAPI masking tool; list and audit masking views, initiator and port groups'))
    lines.append(txt_row('  ISL congestion = Inter-Switch Link saturation between fabric switches; affects SRDF bandwidth'))
    lines.append(txt_row('  DARE key timeout= KMIP server unreachable; array may lock encrypted volumes after threshold'))
    lines.append(txt_row('  SRP over-commit = Thin pool subscribed beyond physical capacity; data at risk if all written'))
    lines.append(txt_row('  FA port saturated= Front-End director port at bandwidth limit; redistribute hosts to other ports'))
    lines.append(txt_row('  Group split    = SRDF consistency group members diverged; requires re-establish from R1'))
    lines.append(txt_row('  symmaskdb      = SYMAPI database for masking configuration; exportable for audit'))
    lines.append(txt_row('  RDF director LED= Physical indicator on director blade; amber = degraded, red = failed'))
    lines.append(txt_row('  symcfg list    = SYMAPI command to list array config: SRP, director, port, volume info'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powerpath',
    'docs/storage/dell/powerpath/index.md',
    'Dell PowerPath — multipath I/O driver; load balancing; failover; path policy management',
)
def dell_powerpath():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerPath Multipath I/O'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'PowerPath: Dell host-side multipath driver; load balancing and automatic failover')))
    lines.append(R(bMid(IV_L, IV_R, 'Policies: CLAROpt (adaptive LB), Adaptive (round-robin), Basic (failover-only)')))
    lines.append(R(bMid(IV_L, IV_R, 'Supports: PowerMax, Unity, VNX, XtremIO, ECS; FC, iSCSI, FCoE transports')))
    lines.append(R(bMid(IV_L, IV_R, 'Managed via powermt CLI; PowerPath/VE edition for VMware ESXi hosts')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Host HBAs → multiple FC/iSCSI paths → PowerPath load-balances I/O → array FA ports'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Path Policies'), bMid(B2_L, B2_R, 'Operations'), bMid(B3_L, B3_R, 'Platform Support'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CLAROpt (default)'), bMid(B2_L, B2_R, 'powermt display'), bMid(B3_L, B3_R, 'RHEL / SLES'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Adaptive LB'), bMid(B2_L, B2_R, 'powermt restore'), bMid(B3_L, B3_R, 'Windows Server'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Basic failover'), bMid(B2_L, B2_R, 'powermt save'), bMid(B3_L, B3_R, 'VMware ESXi /VE'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Optimized'), bMid(B2_L, B2_R, 'powermt set'), bMid(B3_L, B3_R, 'AIX / Solaris'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Per-LUN policy'), bMid(B2_L, B2_R, 'powermt check'), bMid(B3_L, B3_R, 'Ubuntu LTS'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Path failure detected → I/O rerouted to live paths → dead path polled → re-enabled on recovery'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Policy', 'Description', 'Best for', 'Array type', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['CLAROpt', 'Array-aware LB', 'Unity / VNX', 'CLARiiON-class', 'Default policy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Adaptive', 'Round-robin LB', 'Mixed workload', 'All arrays', 'Per-I/O balance'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Basic', 'Failover only', 'Low I/O apps', 'All arrays', 'One active path'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Optimized', 'Perf-aware LB', 'PowerMax', 'Symmetrix-class', 'Preferred paths'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: HBA ports in host → FC fabric or iSCSI network → array FA director ports'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  CLAROpt        = CLARiiON Optimized; array-aware load balancing for Unity/VNX arrays'))
    lines.append(txt_row('  powermt        = PowerPath management CLI; primary tool for all path and policy operations'))
    lines.append(txt_row('  powermt display= Show all multipath devices, paths, and states on the host'))
    lines.append(txt_row('  powermt restore= Re-apply saved PowerPath configuration after host reboot'))
    lines.append(txt_row('  powermt save   = Persist current path policy and config to disk for restore after reboot'))
    lines.append(txt_row('  powermt set    = Set path policy or other parameter: powermt set policy=adaptive dev=all'))
    lines.append(txt_row('  Dead path      = Path that failed I/O; PowerPath polls it for recovery every few seconds'))
    lines.append(txt_row('  Emulation      = Array class identifier in PowerPath config (emc_symm, emc_clariion, etc.)'))
    lines.append(txt_row('  PowerPath/VE   = PowerPath Virtual Edition for VMware ESXi; replaces native NMP PSP'))
    lines.append(txt_row('  Registration   = License key bound to host system; verified via powermt check_registration'))
    lines.append(txt_row('  Trespass       = Ownership transfer of LUN between array SPs in active/passive arrays'))
    lines.append(txt_row('  ALUA           = Asymmetric Logical Unit Access; standard for preferred/non-preferred paths'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powerpath-arch-design-standards',
    'docs/storage/dell/powerpath/architecture/design-standards/index.md',
    'Dell PowerPath design standards — HBA count, path count, policy selection, failover testing',
)
def dell_powerpath_arch_design_standards():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerPath Architecture Design Standards'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Design standards: minimum 2 HBAs per host on separate fabrics; 4+ paths per LUN for HA')))
    lines.append(R(bMid(IV_L, IV_R, 'Policy: CLAROpt for Unity/VNX; Optimized for PowerMax; Adaptive for mixed environments')))
    lines.append(R(bMid(IV_L, IV_R, 'Path count rule: 4 paths minimum (2 per fabric); 8 paths for business-critical workloads')))
    lines.append(R(bMid(IV_L, IV_R, 'Mandatory: powermt save after config; failover test per LUN after deployment')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  HBA sizing → SAN zoning → PowerPath install → policy set → save config → failover test'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Path Standards'), bMid(B2_L, B2_R, 'Policy Standards'), bMid(B3_L, B3_R, 'Testing Standards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '2+ HBAs per host'), bMid(B2_L, B2_R, 'Match array class'), bMid(B3_L, B3_R, 'Fail each path'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Separate fabrics'), bMid(B2_L, B2_R, 'CLAROpt → Unity'), bMid(B3_L, B3_R, 'Verify I/O cont.'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '4 paths minimum'), bMid(B2_L, B2_R, 'Optimized → PMAX'), bMid(B3_L, B3_R, 'Confirm recovery'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '8 paths for crit.'), bMid(B2_L, B2_R, 'Adaptive → mixed'), bMid(B3_L, B3_R, 'powermt save req'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No single fabric'), bMid(B2_L, B2_R, 'Per-LUN override'), bMid(B3_L, B3_R, 'Annual retest'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Design verified → failover test every path → powermt save → document path topology'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Standard', 'Minimum', 'Recommended', 'Anti-pattern', 'Risk'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['HBAs', '2 per host', '4 per host', '1 HBA only', 'Single point fail'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Paths', '4 per LUN', '8 per LUN', '2 same fabric', 'Fabric SPOF'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Policy', 'Array-matched', 'Per workload', 'Basic all', 'No LB benefit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Failover', 'Test all paths', 'Quarterly test', 'No test done', 'Untested failover'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: dual-fabric SAN (A+B fabric); HBA 0 → Fabric A; HBA 1 → Fabric B per host'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SPOF           = Single Point of Failure; eliminated by dual HBA / dual fabric design'))
    lines.append(txt_row('  CLAROpt policy = Optimal for CLARiiON-class arrays (Unity, VNX); array-aware balancing'))
    lines.append(txt_row('  Optimized policy= Best for PowerMax; uses array preferred path information for I/O routing'))
    lines.append(txt_row('  Adaptive policy = Generic round-robin; suitable when array class is mixed or unknown'))
    lines.append(txt_row('  Per-LUN override= Set different policy on a specific device: powermt set policy=X dev=hdisk2'))
    lines.append(txt_row('  Fabric A/B     = Two independent FC fabrics; host HBAs split across both for redundancy'))
    lines.append(txt_row('  Path failover  = Automatic reroute of I/O when path goes down; no manual intervention needed'))
    lines.append(txt_row('  powermt save   = Writes current config to /etc/powermt.custom; survives reboot if used'))
    lines.append(txt_row('  Dead path poll = PowerPath probes dead paths at configurable interval to detect recovery'))
    lines.append(txt_row('  4-path rule    = Ensures one path loss from each fabric still leaves 2 active paths per LUN'))
    lines.append(txt_row('  Annual retest  = Periodic failover test to confirm path recovery still works in production'))
    lines.append(txt_row('  No single fabric= Both fabrics must carry paths; single-fabric design fails on ISL outage'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powerpath-operations',
    'docs/storage/dell/powerpath/operations/index.md',
    'Dell PowerPath operations — path monitoring, policy changes, registration, save/restore',
)
def dell_powerpath_operations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerPath Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Day-2 operations: path monitoring, dead path investigation, policy tuning, registration')))
    lines.append(R(bMid(IV_L, IV_R, 'powermt display: shows all multipath devices, path states, active I/O distribution')))
    lines.append(R(bMid(IV_L, IV_R, 'Policy changes: powermt set policy=X dev=all; save immediately after with powermt save')))
    lines.append(R(bMid(IV_L, IV_R, 'Registration: powermt check_registration; license tied to host; re-register on rebuild')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Check path state → investigate dead paths → adjust policy → save config → verify distribution'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Path Monitoring'), bMid(B2_L, B2_R, 'Policy Management'), bMid(B3_L, B3_R, 'License / Config'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'powermt display'), bMid(B2_L, B2_R, 'powermt set'), bMid(B3_L, B3_R, 'check_registration'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dead path check'), bMid(B2_L, B2_R, 'Per-device policy'), bMid(B3_L, B3_R, 'powermt save'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Path count verify'), bMid(B2_L, B2_R, 'powermt restore'), bMid(B3_L, B3_R, 'powermt restore'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'I/O distribution'), bMid(B2_L, B2_R, 'Policy verify'), bMid(B3_L, B3_R, 'License renew'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'powermt check'), bMid(B2_L, B2_R, 'Reset to default'), bMid(B3_L, B3_R, 'Emulation audit'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  powermt display → identify dead paths → resolve root cause → verify path recovery'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Task', 'Command', 'Output / Action', 'Frequency', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Path check', 'powermt display', 'Path state list', 'Daily', 'Check dead paths'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Policy set', 'powermt set', 'Policy applied', 'On change', 'Save after set'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Registration', 'check_registr.', 'License valid', 'On install', 'Bound to host'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Config save', 'powermt save', 'Persists config', 'After any change', 'Survives reboot'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: paths shown as hdiskX (AIX), sdX (Linux), or disk# (Windows) in powermt output'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  powermt display= List all PowerPath devices with path health and I/O distribution per path'))
    lines.append(txt_row('  Dead path      = Path that failed I/O; shown as Dead in powermt output; polled for recovery'))
    lines.append(txt_row('  powermt set    = Change path policy: powermt set policy=adaptive dev=all class=emc_symm'))
    lines.append(txt_row('  powermt save   = Write config to /etc/powermt.custom; must run after every policy change'))
    lines.append(txt_row('  powermt restore= Apply config from /etc/powermt.custom; run manually or at boot via init'))
    lines.append(txt_row('  powermt check  = Verify PowerPath sees all expected paths; report any discrepancies'))
    lines.append(txt_row('  check_registration= Validate license key registration on the host (powermt check_registration)'))
    lines.append(txt_row('  Emulation      = Array class (emc_symm, emc_clariion, etc.) assigned to each device'))
    lines.append(txt_row('  I/O distribution= Per-path I/O count shown by powermt; should be roughly balanced for LB'))
    lines.append(txt_row('  Path recovery  = PowerPath re-enables dead path after successful I/O probe to the array port'))
    lines.append(txt_row('  powermt.custom = Config file persisted by powermt save; read at boot by powermt restore'))
    lines.append(txt_row('  License renew  = Obtain new key from Dell licensing portal; powermt remove + re-register'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powerpath-ops-procedures',
    'docs/storage/dell/powerpath/operations/procedures/index.md',
    'Dell PowerPath operational procedures — install, upgrade, decommission, policy change steps',
)
def dell_powerpath_ops_procedures():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerPath Operational Procedures'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Standard procedures: install, upgrade, policy change, decommission, path failover test')))
    lines.append(R(bMid(IV_L, IV_R, 'Install: kernel driver + powermt registration key; reboot required on Linux/Windows')))
    lines.append(R(bMid(IV_L, IV_R, 'Upgrade: uninstall old version → install new → re-register → powermt restore → verify')))
    lines.append(R(bMid(IV_L, IV_R, 'Decommission: powermt remove dev=X → unmap LUN from array → verify no ghost paths')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Pre-check path count → execute procedure → powermt display → powermt save → sign-off'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Install Steps'), bMid(B2_L, B2_R, 'Policy Change'), bMid(B3_L, B3_R, 'Decommission'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Install package'), bMid(B2_L, B2_R, 'Check current'), bMid(B3_L, B3_R, 'Drain I/O'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Register license'), bMid(B2_L, B2_R, 'Set new policy'), bMid(B3_L, B3_R, 'powermt remove'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Reboot host'), bMid(B2_L, B2_R, 'powermt save'), bMid(B3_L, B3_R, 'Unmap at array'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'powermt restore'), bMid(B2_L, B2_R, 'Verify balance'), bMid(B3_L, B3_R, 'Verify ghost=0'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify path count'), bMid(B2_L, B2_R, 'Failover test'), bMid(B3_L, B3_R, 'Update CMDB'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Procedure complete → powermt display dev=all → confirm all paths alive → save and document'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Procedure', 'Duration', 'Reboot needed', 'Rollback', 'Risk'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Install', '30 min', 'Yes (Linux/Win)', 'Uninstall pkg', 'I/O pause'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Upgrade', '45 min', 'Yes', 'Re-install old', 'I/O disruption'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Policy change', '5 min', 'No', 'powermt set old', 'Rebalance lag'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Decommission', '15 min', 'No', 'Re-map LUN', 'Ghost paths'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: package installed on host OS; kernel module loaded; no network required for config'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  powermt remove = Remove a device from PowerPath management; stops multipath tracking for LUN'))
    lines.append(txt_row('  Ghost path     = Stale path entry after LUN unmapped; appears as Dead in powermt output'))
    lines.append(txt_row('  powermt restore= Re-apply /etc/powermt.custom after reboot; part of standard boot sequence'))
    lines.append(txt_row('  Drain I/O      = Gracefully stop application I/O before decommissioning a path or LUN'))
    lines.append(txt_row('  CMDB           = Configuration Management Database; record device removal for asset tracking'))
    lines.append(txt_row('  Kernel module  = PowerPath loads as a kernel driver; requires compatible kernel version'))
    lines.append(txt_row('  Rebalance lag  = Brief period after policy change while I/O re-distributes to new path order'))
    lines.append(txt_row('  Failover test  = Manually disable a path and verify I/O continues on remaining paths'))
    lines.append(txt_row('  Sign-off       = Post-procedure verification step; document path count and policy in record'))
    lines.append(txt_row('  Uninstall pkg  = Remove PowerPath package (rpm -e / dpkg -r / msiexec /x) then reinstall old'))
    lines.append(txt_row('  Re-register    = After upgrade, re-run powermt check_registration with existing license key'))
    lines.append(txt_row('  Ghost=0        = Confirmation that no stale path entries remain after LUN decommission'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powerpath-security',
    'docs/storage/dell/powerpath/security/index.md',
    'Dell PowerPath security — access control, license protection, audit, path integrity',
)
def dell_powerpath_security():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerPath Security'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'PowerPath security: access control for powermt CLI, license key protection, path audit')))
    lines.append(R(bMid(IV_L, IV_R, 'powermt requires root (Linux) or Administrator (Windows); no non-privileged access')))
    lines.append(R(bMid(IV_L, IV_R, 'License keys are host-bound; protect key file; track via Dell support portal')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit: log powermt commands via OS auditing (auditd/Windows Event Log); alert on changes')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Restrict CLI access → protect license file → enable OS audit logging → review path changes'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Access Control'), bMid(B2_L, B2_R, 'License Security'), bMid(B3_L, B3_R, 'Audit / Logging'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Root-only powermt'), bMid(B2_L, B2_R, 'Host-bound key'), bMid(B3_L, B3_R, 'auditd rules'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Sudo policy'), bMid(B2_L, B2_R, 'Portal tracking'), bMid(B3_L, B3_R, 'Event log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No non-priv exec'), bMid(B2_L, B2_R, 'Key file perms'), bMid(B3_L, B3_R, 'SIEM forward'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PAM integration'), bMid(B2_L, B2_R, 'License expiry'), bMid(B3_L, B3_R, 'Policy changes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MFA for admin'), bMid(B2_L, B2_R, 'Renewal alerts'), bMid(B3_L, B3_R, 'Path add/remove'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Privilege control → audit logging → license monitoring → periodic path count reconciliation'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Control', 'Implementation', 'Standard', 'Exception', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['CLI access', 'Root / sudo', 'Named accounts', 'No shared root', 'Sudo log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['License', 'Host-bound key', 'Stored securely', 'No sharing', 'Portal audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Path audit', 'OS audit log', 'SIEM ingest', '—', 'Weekly review'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Policy change', 'Change control', 'CR required', 'Emergency proc', 'Post-change log'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: powermt binary at /sbin (Linux); license file at /etc; restrict file permissions'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Host-bound key = PowerPath license cryptographically tied to host system ID; not transferable'))
    lines.append(txt_row('  auditd         = Linux kernel auditing daemon; log all execve calls matching powermt binary'))
    lines.append(txt_row('  Sudo policy    = /etc/sudoers rule granting named storage admin powermt exec without full root'))
    lines.append(txt_row('  Key file perms = /etc/powermt.custom should be root:root 600; world-readable is a risk'))
    lines.append(txt_row('  PAM integration= Pluggable Authentication Module; enforce MFA for storage admin login'))
    lines.append(txt_row('  SIEM           = Security Information and Event Management; receives powermt audit events'))
    lines.append(txt_row('  License expiry = PowerPath subscription license; expired license disables new registrations'))
    lines.append(txt_row('  Named accounts = No shared root; each admin has own account with sudo to powermt'))
    lines.append(txt_row('  CR required    = Change Request; formal change control approval before policy modification'))
    lines.append(txt_row('  Portal audit   = Dell support portal shows all registered hosts and license key assignments'))
    lines.append(txt_row('  Path count recn= Periodic reconcile of expected vs. actual paths per host to detect removals'))
    lines.append(txt_row('  Emergency proc = Out-of-band change process for production incidents; still post-log required'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powerpath-security-encryption',
    'docs/storage/dell/powerpath/security/encryption/index.md',
    'Dell PowerPath security encryption — transport security, DARE passthrough, iSCSI CHAP',
)
def dell_powerpath_security_encryption():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerPath Security — Encryption'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'PowerPath is transparent to data encryption; DARE operates at array drive layer below it')))
    lines.append(R(bMid(IV_L, IV_R, 'FC transport: no native data encryption; rely on FC-SP or fabric-level encryption SAN ISL')))
    lines.append(R(bMid(IV_L, IV_R, 'iSCSI transport: CHAP for authentication; IPSec for data-in-flight encryption per hop')))
    lines.append(R(bMid(IV_L, IV_R, 'PowerPath does not inspect or modify data; encryption/decryption at host HBA or array')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Host I/O → PowerPath load-balances path → FC/iSCSI transport → array decrypts at DARE layer'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FC Transport'), bMid(B2_L, B2_R, 'iSCSI Transport'), bMid(B3_L, B3_R, 'Array Encryption'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FC-SP (optional)'), bMid(B2_L, B2_R, 'CHAP auth'), bMid(B3_L, B3_R, 'DARE at drives'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ISL encryption'), bMid(B2_L, B2_R, 'IPSec tunnel'), bMid(B3_L, B3_R, 'KMIP key server'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VSAN isolation'), bMid(B2_L, B2_R, 'TLS iSNS'), bMid(B3_L, B3_R, 'Transparent pass'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Zoning boundary'), bMid(B2_L, B2_R, 'Mutual CHAP'), bMid(B3_L, B3_R, 'Key rotation'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No PP inspect'), bMid(B2_L, B2_R, 'No PP inspect'), bMid(B3_L, B3_R, 'Crypto erase'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Enable iSCSI CHAP or IPSec at transport layer; DARE configured at array; PowerPath unaffected'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Layer', 'Transport', 'Mechanism', 'Config location', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Data at rest', 'FC / iSCSI', 'DARE (array)', 'Array GUI', 'Below PowerPath'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Auth', 'iSCSI', 'CHAP secret', 'iSCSI initiator', 'Mutual CHAP'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['In-flight', 'iSCSI', 'IPSec ESP', 'OS / network', 'Per-hop config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['FC link', 'FC', 'FC-SP / ISL enc', 'SAN switch', 'Optional'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: FC-SP on HBA and switch; IPSec on iSCSI NIC/NIC driver; DARE on array drive bays'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  DARE           = Data At Rest Encryption; array-side SED encryption; transparent to PowerPath'))
    lines.append(txt_row('  FC-SP          = Fibre Channel Security Protocol; DH-CHAP authentication on FC links'))
    lines.append(txt_row('  ISL encryption = In-flight encryption between fabric switches; configured at SAN switch level'))
    lines.append(txt_row('  CHAP           = Challenge Handshake Authentication Protocol; iSCSI initiator/target auth'))
    lines.append(txt_row('  Mutual CHAP    = Both initiator and target authenticate each other; stronger than one-way'))
    lines.append(txt_row('  IPSec ESP      = Encapsulating Security Payload; encrypts iSCSI packets in-flight'))
    lines.append(txt_row('  iSNS TLS       = iSCSI Name Service secured with TLS; optional discovery plane protection'))
    lines.append(txt_row('  Transparent pass= PowerPath passes I/O bytes unchanged; does not encrypt or decrypt data'))
    lines.append(txt_row('  KMIP key server= External key manager for DARE; unreachable KMIP can lock array volumes'))
    lines.append(txt_row('  Crypto erase   = Destroy DARE encryption key on decommission; all data permanently unreadable'))
    lines.append(txt_row('  VSAN isolation = FC VSAN separates storage traffic; limits blast radius of any breach'))
    lines.append(txt_row('  Zoning boundary= FC zone restricts which HWWNs can communicate; primary FC security control'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powerpath-security-hardening',
    'docs/storage/dell/powerpath/security/hardening/index.md',
    'Dell PowerPath security hardening — privilege restriction, binary integrity, config protection',
)
def dell_powerpath_security_hardening():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerPath Security Hardening'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Hardening: restrict powermt to named accounts via sudo; protect config and license files')))
    lines.append(R(bMid(IV_L, IV_R, 'Binary integrity: verify PowerPath RPM/DEB signature before install; use Dell repo GPG key')))
    lines.append(R(bMid(IV_L, IV_R, 'Config file /etc/powermt.custom: perms root:root 600; no group or world read')))
    lines.append(R(bMid(IV_L, IV_R, 'Disable unused features: unused emulations should be removed from powermt config')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Verify package signature → restrict CLI → protect config file → enable audit → review monthly'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'OS Hardening'), bMid(B2_L, B2_R, 'Config Hardening'), bMid(B3_L, B3_R, 'Audit Hardening'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Named sudo only'), bMid(B2_L, B2_R, 'powermt.custom'), bMid(B3_L, B3_R, 'auditd rule'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No shared root'), bMid(B2_L, B2_R, 'Perms 600'), bMid(B3_L, B3_R, 'SIEM forward'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Package GPG sig'), bMid(B2_L, B2_R, 'Remove unused'), bMid(B3_L, B3_R, 'Monthly review'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'MFA for storage'), bMid(B2_L, B2_R, 'License protect'), bMid(B3_L, B3_R, 'Change log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SELinux context'), bMid(B2_L, B2_R, 'Minimal emul.'), bMid(B3_L, B3_R, 'Integrity check'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Harden OS → restrict config file perms → audit all powermt commands → alert on anomaly'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Hardening', 'Action', 'Standard', 'Verify with', 'Risk if skipped'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['CLI access', 'Named sudo', 'No shared root', 'sudo -l output', 'Uncontrolled'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Config file', 'chmod 600', 'root:root only', 'ls -la /etc', 'Config leak'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Package', 'GPG verify', 'Dell signed RPM', 'rpm --verify', 'Tampered binary'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Audit', 'auditd rule', 'All execve', 'ausearch', 'No trail'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: /sbin/powermt binary root-owned; /etc/powermt.custom 600; auditd rule on /sbin'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  GPG signature  = Dell signs PowerPath packages; verify with rpm --checksig or dpkg verify'))
    lines.append(txt_row('  powermt.custom = Persisted config file; world-readable allows path policy enumeration'))
    lines.append(txt_row('  Named sudo     = Individual storage admin accounts with specific sudo rule for powermt only'))
    lines.append(txt_row('  SELinux context= AppArmor/SELinux policy for PowerPath binary and config file access'))
    lines.append(txt_row('  Minimal emul.  = Remove unused array emulations from powermt config to reduce attack surface'))
    lines.append(txt_row('  auditd rule    = /etc/audit/rules.d entry: -w /sbin/powermt -p x -k powerpath_exec'))
    lines.append(txt_row('  ausearch       = auditd log query tool: ausearch -k powerpath_exec to review executions'))
    lines.append(txt_row('  Integrity check= Periodic rpm --verify on PowerPath package to detect binary modification'))
    lines.append(txt_row('  SIEM           = Security Information and Event Management; ingest auditd events for alerting'))
    lines.append(txt_row('  License protect= Store registration key file with 600 perms; do not commit to version control'))
    lines.append(txt_row('  Uncontrolled   = Risk when shared root used; any user with root can modify path policy silently'))
    lines.append(txt_row('  Change log     = Record of every powermt policy or config change; tied to CR number'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powerpath-troubleshooting',
    'docs/storage/dell/powerpath/troubleshooting/index.md',
    'Dell PowerPath troubleshooting — dead paths, no LUN, registration failure, path imbalance',
)
def dell_powerpath_troubleshooting():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerPath Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Common issues: dead paths, LUN not visible, registration failure, I/O imbalance')))
    lines.append(R(bMid(IV_L, IV_R, 'Dead path: check HBA port state, SAN zone, and array FA port; remove then rescan')))
    lines.append(R(bMid(IV_L, IV_R, 'LUN missing: verify masking view at array; rescan after masking; powermt check')))
    lines.append(R(bMid(IV_L, IV_R, 'Registration: expired or wrong host ID; re-register with valid key from Dell portal')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Symptom reported → powermt display → identify affected path/device → trace to root cause'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Path Issues'), bMid(B2_L, B2_R, 'LUN / Device'), bMid(B3_L, B3_R, 'Registration'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'All paths dead'), bMid(B2_L, B2_R, 'LUN not visible'), bMid(B3_L, B3_R, 'License expired'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Single path dead'), bMid(B2_L, B2_R, 'Ghost path'), bMid(B3_L, B3_R, 'Wrong host ID'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Path imbalance'), bMid(B2_L, B2_R, 'Masking missing'), bMid(B3_L, B3_R, 'Key file missing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Slow I/O'), bMid(B2_L, B2_R, 'Wrong emulation'), bMid(B3_L, B3_R, 'Portal mismatch'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Trespass loop'), bMid(B2_L, B2_R, 'Rescan needed'), bMid(B3_L, B3_R, 'Re-register'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  powermt display → check dead path layer (HBA / fabric / array) → fix at source → verify'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Symptom', 'First check', 'Command', 'Fix', 'Escalate if'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['All paths dead', 'HBA port state', 'powermt display', 'Fix HBA/zone', 'Array port down'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['LUN missing', 'Array masking', 'powermt check', 'Fix masking', 'Rescan no result'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['I/O imbalance', 'Policy check', 'powermt display', 'Set policy', 'Persists after'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Reg. failure', 'Key validity', 'check_registr.', 'Re-register', 'Key rejected'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: check HBA port LED, SAN switch port counters, array FA port LEDs for dead path'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  All paths dead = No active path to device; I/O queued or returned error to host OS'))
    lines.append(txt_row('  Trespass loop  = Active/passive array SP ownership conflict; path oscillates between SPs'))
    lines.append(txt_row('  Ghost path     = Dead path entry for LUN that was unmapped; powermt remove to clean up'))
    lines.append(txt_row('  Wrong emulation= Device assigned wrong array class; set correct emulation with powermt config'))
    lines.append(txt_row('  I/O imbalance  = Most I/O on one path; caused by Basic policy or sticky preferred path'))
    lines.append(txt_row('  check_registr. = powermt check_registration; validates license key is active on this host'))
    lines.append(txt_row('  Re-register    = powermt remove license + powermt check_registration with new key'))
    lines.append(txt_row('  Rescan         = Host OS HBA rescan after masking change; picks up new or removed LUNs'))
    lines.append(txt_row('  Portal mismatch= Dell portal shows key assigned to different host ID; contact Dell licensing'))
    lines.append(txt_row('  Path imbalance = powermt set policy=adaptive dev=all to re-enable load balancing'))
    lines.append(txt_row('  FA port LED    = Array Front-End director port indicator; dark/amber = fault in path'))
    lines.append(txt_row('  HBA port state = fcinfo hba-port (Solaris), systool (Linux), Get-InitiatorPort (Windows)'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powerscale',
    'docs/storage/dell/powerscale/index.md',
    'Dell PowerScale (Isilon) — scale-out NAS; OneFS; NFS/SMB/S3; SmartPools; SyncIQ',
)
def dell_powerscale():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerScale (Isilon) Scale-Out NAS'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'PowerScale: Dell scale-out NAS cluster; OneFS distributed OS across 3–252 nodes')))
    lines.append(R(bMid(IV_L, IV_R, 'Protocols: NFS v3/v4.1, SMB 2/3, S3, HDFS, FTP; single namespace across all nodes')))
    lines.append(R(bMid(IV_L, IV_R, 'SmartPools: automated data tiering; H-series (hybrid), F-series (flash), A-series (archive)')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication via SyncIQ (async to remote cluster); snapshots via SnapshotIQ')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Client → SmartConnect DNS LB → node NFS/SMB → OneFS namespace → SmartPool tier → drives'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Architecture'), bMid(B2_L, B2_R, 'Operations'), bMid(B3_L, B3_R, 'Security'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'OneFS cluster'), bMid(B2_L, B2_R, 'isi CLI'), bMid(B3_L, B3_R, 'Access zones'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Node pools'), bMid(B2_L, B2_R, 'isi statistics'), bMid(B3_L, B3_R, 'AD / LDAP / KRB'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SmartPools tiers'), bMid(B2_L, B2_R, 'SyncIQ jobs'), bMid(B3_L, B3_R, 'SmartLock WORM'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SmartConnect'), bMid(B2_L, B2_R, 'SnapshotIQ'), bMid(B3_L, B3_R, 'RBAC / roles'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FlexProtect'), bMid(B2_L, B2_R, 'SmartQuotas'), bMid(B3_L, B3_R, 'Audit logging'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Client I/O → node → OneFS journal → data written to drives → SmartPool migrates tier'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Feature', 'H-series', 'F-series', 'A-series', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Media', 'SSD + SAS', 'All-NVMe/SSD', 'SAS + SATA', 'Node type'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Use case', 'Mixed workload', 'High perf NAS', 'Archive/cold', 'Tiered by SmartP'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Cluster min', '3 nodes', '3 nodes', '3 nodes', 'Max 252 nodes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Protocol', 'NFS/SMB/S3', 'NFS/SMB/S3', 'NFS/SMB/S3', 'All in one NS'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: nodes in rack; InfiniBand or 25/100GbE back-end; front-end Ethernet for clients'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  OneFS          = PowerScale distributed OS; runs identically on all cluster nodes'))
    lines.append(txt_row('  SmartPools     = Automated tiering across node pools; moves data by file policy and age'))
    lines.append(txt_row('  SmartConnect   = DNS round-robin or zone-based client connection balancing across nodes'))
    lines.append(txt_row('  SyncIQ         = Async replication to remote PowerScale cluster; policy-driven schedules'))
    lines.append(txt_row('  SnapshotIQ     = Local read-only snapshots; accessible via .snapshot directory'))
    lines.append(txt_row('  SmartQuotas    = Directory/user/group capacity quotas; hard and advisory thresholds'))
    lines.append(txt_row('  FlexProtect    = Dynamic N+M data protection; rebalances after node failure automatically'))
    lines.append(txt_row('  Access zone    = Isolated namespace with own auth providers, IP pools, and share policies'))
    lines.append(txt_row('  SmartLock      = WORM compliance (cannot delete/modify files during retention period)'))
    lines.append(txt_row('  isi            = OneFS CLI tool; isi status, isi statistics, isi sync, isi quota'))
    lines.append(txt_row('  InsightIQ      = Analytics platform for PowerScale performance reporting'))
    lines.append(txt_row('  InfiniBand BE  = Back-end node interconnect for metadata and data traffic within cluster'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powerscale-arch-design-standards',
    'docs/storage/dell/powerscale/architecture/design-standards/index.md',
    'Dell PowerScale design standards — node sizing, protection policy, SmartPool tiers, network',
)
def dell_powerscale_arch_design_standards():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerScale Architecture Design Standards'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Design standards: minimum 4 nodes for production HA; FlexProtect N+2 for 3-node min')))
    lines.append(R(bMid(IV_L, IV_R, 'Network: separate front-end client network and back-end InfiniBand/Ethernet node fabric')))
    lines.append(R(bMid(IV_L, IV_R, 'SmartPool tiers: performance pool for hot data; archive pool for cold; policy-driven move')))
    lines.append(R(bMid(IV_L, IV_R, 'SyncIQ: RPO ≥ minutes; define bandwidth throttle; separate replication IP pool')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Capacity model → node type selection → protection level → SmartPool policy → network design'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Sizing Standards'), bMid(B2_L, B2_R, 'Protection Stds'), bMid(B3_L, B3_R, 'Network Standards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '4 nodes min prod'), bMid(B2_L, B2_R, 'N+2:1 default'), bMid(B3_L, B3_R, 'Front/back split'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Mixed node pools'), bMid(B2_L, B2_R, 'N+3:1 critical'), bMid(B3_L, B3_R, '25/100G front'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cap plan +20%'), bMid(B2_L, B2_R, 'Mirror for WORM'), bMid(B3_L, B3_R, 'InfiniBand back'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'F-series for perf'), bMid(B2_L, B2_R, 'No degraded run'), bMid(B3_L, B3_R, 'Separate repl IP'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'A-series archive'), bMid(B2_L, B2_R, 'Resync on add'), bMid(B3_L, B3_R, 'SmartConnect DNS'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Node pool configured → FlexProtect set → SmartPool tier policy defined → test failover'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Standard', 'Rule', 'Rationale', 'Anti-pattern', 'Risk'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Node count', '4 nodes min', 'Tolerate N+2', '3 nodes prod', 'No failure margin'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Protection', 'N+2:1 default', 'Two-fault tol.', 'N+1:1 only', 'Single fault tol'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Network', 'Separate FE/BE', 'No contention', 'Shared fabric', 'Back-end impact'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Capacity', '+20% headroom', 'Space for jobs', 'Full pool', 'SmartPool stall'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: nodes on ToR switches; back-end IB or 25G switch; separate mgmt VLAN'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  N+2:1         = FlexProtect level; tolerates simultaneous failure of 2 drives or 1 node'))
    lines.append(txt_row('  N+3:1         = Three-fault-tolerant protection; for mission-critical or large node pools'))
    lines.append(txt_row('  FlexProtect   = OneFS auto-protection; dynamically balances protection across available drives'))
    lines.append(txt_row('  Front-end net = Client-facing Ethernet; SmartConnect IP pool for NFS/SMB client connections'))
    lines.append(txt_row('  Back-end net  = Node-to-node InfiniBand or 25/100G Ethernet; carries metadata and data traffic'))
    lines.append(txt_row('  Separate repl IP= SyncIQ uses dedicated IP pool; prevents replication from saturating client LAN'))
    lines.append(txt_row('  Cap plan +20% = Keep 20% free in SmartPool; SmartPool jobs and snapshots need space headroom'))
    lines.append(txt_row('  SmartPool stall= SmartPool tier migration stops when pool is 100% full; data at risk'))
    lines.append(txt_row('  Resync on add = After adding nodes, OneFS rebalances data across the expanded pool'))
    lines.append(txt_row('  Mirror WORM   = SmartLock compliance volumes use mirroring for highest protection'))
    lines.append(txt_row('  ToR switch    = Top of Rack switch; connects node front-end ports to client network'))
    lines.append(txt_row('  No degraded run= Do not operate cluster long-term in degraded state; add node or replace drive'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powerscale-operations',
    'docs/storage/dell/powerscale/operations/index.md',
    'Dell PowerScale operations — isi CLI, SyncIQ jobs, quotas, snapshots, health monitoring',
)
def dell_powerscale_operations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerScale Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Day-2 ops: cluster health, SyncIQ replication, SnapshotIQ lifecycle, quota management')))
    lines.append(R(bMid(IV_L, IV_R, 'isi status: cluster health overview; isi statistics: node/protocol/drive performance')))
    lines.append(R(bMid(IV_L, IV_R, 'SyncIQ: run/pause/resume policies; monitor RPO; failover and failback procedures')))
    lines.append(R(bMid(IV_L, IV_R, 'Quota alerts: track SmartQuota thresholds; isi quota list for space accounting')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  isi status → review alerts → SyncIQ policy check → quota review → snapshot expiry cleanup'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cluster Health'), bMid(B2_L, B2_R, 'Replication'), bMid(B3_L, B3_R, 'Capacity / Data'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'isi status'), bMid(B2_L, B2_R, 'isi sync policy'), bMid(B3_L, B3_R, 'isi quota list'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Drive state'), bMid(B2_L, B2_R, 'isi sync job'), bMid(B3_L, B3_R, 'SmartPool jobs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Node state'), bMid(B2_L, B2_R, 'Failover policy'), bMid(B3_L, B3_R, 'isi snap list'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FlexProtect job'), bMid(B2_L, B2_R, 'Failback policy'), bMid(B3_L, B3_R, 'Snap delete'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Event log'), bMid(B2_L, B2_R, 'RPO alert'), bMid(B3_L, B3_R, 'Capacity trend'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Cluster health → SyncIQ RPO check → quota threshold review → snapshot cleanup cycle'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Task', 'Command', 'Output', 'Frequency', 'Alert threshold'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Health', 'isi status', 'Node/drive OK', 'Daily', 'Any degraded'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['SyncIQ check', 'isi sync job', 'Last run time', 'Daily', 'RPO exceeded'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Quota check', 'isi quota list', 'Usage vs. limit', 'Weekly', '>85% threshold'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Snap cleanup', 'isi snap delete', 'Freed capacity', 'Monthly', 'Policy expired'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SSH to any cluster node; isi commands run on OneFS and return cluster-wide data'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  isi status     = Cluster-wide health: node states, drive states, FlexProtect job status'))
    lines.append(txt_row('  isi statistics = Protocol throughput, node IOPS, latency, drive stats; -c for CSV'))
    lines.append(txt_row('  isi sync policy= List/modify SyncIQ replication policies; target, schedule, throttle'))
    lines.append(txt_row('  isi sync job   = View running SyncIQ jobs; last run, bytes transferred, RPO gap'))
    lines.append(txt_row('  isi quota list = Display directory quotas; hard limit, advisory, grace period status'))
    lines.append(txt_row('  isi snap list  = List snapshots; name, target directory, creation time, size'))
    lines.append(txt_row('  FlexProtect job= Restripe job that repairs data after drive or node failure'))
    lines.append(txt_row('  RPO alert      = SyncIQ replication behind schedule; data loss window exceeded target'))
    lines.append(txt_row('  SmartPool job  = Background tier migration; moves files between pools per file pool policy'))
    lines.append(txt_row('  Quota threshold= SmartQuota hard limit stops writes; advisory sends alert only'))
    lines.append(txt_row('  Snap delete    = Remove expired or manual snapshots; reclaims capacity in snapshot delta'))
    lines.append(txt_row('  Failover policy= SyncIQ policy action to allow writes on target during source cluster outage'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powerscale-ops-install-upgrade',
    'docs/storage/dell/powerscale/operations/install-upgrade/index.md',
    'Dell PowerScale install and upgrade — OneFS rolling upgrade, node addition, decommission',
)
def dell_powerscale_ops_install_upgrade():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerScale Install and Upgrade'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'OneFS rolling upgrade: upgrades nodes sequentially; cluster stays online throughout')))
    lines.append(R(bMid(IV_L, IV_R, 'Node addition: new node joins cluster; FlexProtect restripes data across expanded pool')))
    lines.append(R(bMid(IV_L, IV_R, 'Pre-upgrade: verify isi upgrade start --verify; review compatibility matrix')))
    lines.append(R(bMid(IV_L, IV_R, 'Decommission: evacuate node with isi devices node smartfail then remove from cluster')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Pre-check → upgrade commit → rolling node-by-node reboot → verify cluster → sign-off'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Upgrade Steps'), bMid(B2_L, B2_R, 'Node Addition'), bMid(B3_L, B3_R, 'Decommission'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Pre-check verify'), bMid(B2_L, B2_R, 'Cable new node'), bMid(B3_L, B3_R, 'smartfail node'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Download image'), bMid(B2_L, B2_R, 'Add to cluster'), bMid(B3_L, B3_R, 'Data evacuates'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Commit upgrade'), bMid(B2_L, B2_R, 'FlexProtect run'), bMid(B3_L, B3_R, 'Remove node'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Rolling reboot'), bMid(B2_L, B2_R, 'Pool restripe'), bMid(B3_L, B3_R, 'Pool restripe'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Post verify'), bMid(B2_L, B2_R, 'Verify join'), bMid(B3_L, B3_R, 'Confirm health'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Upgrade duration scales with cluster size; plan maintenance window for FlexProtect restripe'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Operation', 'Command', 'Duration', 'Cluster impact', 'Rollback'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Pre-check', 'isi upgrade', 'Minutes', 'None', 'N/A — read only'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Upgrade', 'isi upgrade start', 'Hours', 'None (rolling)', 'isi upgrade abort'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Node add', 'isi devices add', 'Hours (restripe)', 'I/O continues', 'Remove node'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Decommission', 'isi smartfail', 'Hours (drain)', 'I/O continues', 'Abort if early'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: new node racked and cabled to back-end switch before isi devices add command'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Rolling upgrade= OneFS upgrades one node at a time; node reboots while others serve I/O'))
    lines.append(txt_row('  isi upgrade    = OneFS CLI upgrade tool; --verify checks compatibility before committing'))
    lines.append(txt_row('  smartfail      = Controlled node/drive removal; OneFS evacuates data before marking removed'))
    lines.append(txt_row('  isi devices    = Node and drive management tool; add, remove, smartfail subcommands'))
    lines.append(txt_row('  FlexProtect run= Auto-triggered after node add/remove; restripes data to new protection level'))
    lines.append(txt_row('  Pool restripe  = Data redistribution across updated node count; runs in background'))
    lines.append(txt_row('  Compatibility  = Check OneFS version matrix; protocol clients, SyncIQ, and hardware support'))
    lines.append(txt_row('  isi upgrade abort= Stops in-progress upgrade; reverts upgraded nodes back to prior version'))
    lines.append(txt_row('  Pre-check verify= isi upgrade start --verify; confirms no blocking conditions before commit'))
    lines.append(txt_row('  Maintenance window= Plan for FlexProtect restripe after node addition; I/O performance impact'))
    lines.append(txt_row('  Data evacuates = smartfail moves all data off the target node before it is removed from pool'))
    lines.append(txt_row('  Add to cluster = isi devices node add; OneFS detects new node on back-end and joins it'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powerscale-security',
    'docs/storage/dell/powerscale/security/index.md',
    'Dell PowerScale security — access zones, AD/LDAP auth, SmartLock WORM, audit logging',
)
def dell_powerscale_security():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerScale Security'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'PowerScale security: access zones isolate tenants; AD/LDAP/Kerberos for file auth')))
    lines.append(R(bMid(IV_L, IV_R, 'Access zones: each zone has own auth providers, IP pool, SMB shares, NFS exports')))
    lines.append(R(bMid(IV_L, IV_R, 'SmartLock: WORM retention (compliance = tamper-proof; enterprise = admin override)')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit: protocol audit log per zone; CEE (Common Event Enabler) export to SIEM')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Client auth → access zone lookup → ACL / Unix perm check → SmartLock WORM → audit log'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Access Zones'), bMid(B2_L, B2_R, 'Authentication'), bMid(B3_L, B3_R, 'Data Protection'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Per-zone auth'), bMid(B2_L, B2_R, 'AD Kerberos'), bMid(B3_L, B3_R, 'SmartLock WORM'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Isolated IP pool'), bMid(B2_L, B2_R, 'LDAP provider'), bMid(B3_L, B3_R, 'Compliance mode'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Per-zone shares'), bMid(B2_L, B2_R, 'NIS provider'), bMid(B3_L, B3_R, 'Enterprise mode'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RBAC roles'), bMid(B2_L, B2_R, 'Local accounts'), bMid(B3_L, B3_R, 'CEE audit log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Zone isolation'), bMid(B2_L, B2_R, 'SID / UID map'), bMid(B3_L, B3_R, 'SIEM forward'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Zone auth configured → RBAC roles assigned → SmartLock retention set → audit enabled'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Control', 'Mechanism', 'Standard', 'Exception', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['File auth', 'AD Kerberos', 'All NAS clients', 'LDAP fallback', 'Auth events'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Admin auth', 'RBAC + AD', 'Named accounts', 'Local break-glass', 'Login log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['WORM', 'SmartLock', 'Compliance mode', 'Enterprise only', 'Retention log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Audit log', 'CEE / SIEM', 'All file ops', '—', 'Weekly review'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SSH admin access on mgmt port; CEE agent on cluster node forwards audit events'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Access zone    = Isolated namespace partition; own auth providers, IPs, shares, and exports'))
    lines.append(txt_row('  SmartLock      = OneFS WORM; compliance = no override; enterprise = admin can override'))
    lines.append(txt_row('  Compliance mode= SmartLock mode that prevents even root from deleting WORM-retained files'))
    lines.append(txt_row('  Enterprise mode= SmartLock WORM with admin override capability; less strict than compliance'))
    lines.append(txt_row('  CEE            = Common Event Enabler; OneFS audit log export agent for SIEM integration'))
    lines.append(txt_row('  RBAC roles     = OneFS built-in roles: SystemAdmin, AuditAdmin, SecurityAdmin, BackupAdmin'))
    lines.append(txt_row('  SID/UID map    = Identity mapping between Windows SID and Unix UID for mixed permissions'))
    lines.append(txt_row('  Kerberos       = Protocol for mutual auth between AD domain and OneFS NFS/SMB clients'))
    lines.append(txt_row('  Break-glass    = Local root account on OneFS node for emergency when AD unavailable'))
    lines.append(txt_row('  Zone isolation = Cross-zone access is blocked; tenant A cannot access zone B data'))
    lines.append(txt_row('  NIS provider   = Legacy Unix auth; NIS maps used in mixed Unix environments'))
    lines.append(txt_row('  Retention log  = SmartLock audit record of file commit, retention date, and release events'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powerscale-troubleshooting',
    'docs/storage/dell/powerscale/troubleshooting/index.md',
    'Dell PowerScale troubleshooting — SyncIQ failures, quota exceeded, node degraded, auth',
)
def dell_powerscale_troubleshooting():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerScale Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Common faults: SyncIQ policy failure, node degraded, quota exceeded, auth errors')))
    lines.append(R(bMid(IV_L, IV_R, 'SyncIQ: check isi sync job; stalled replication causes RPO gap; check network path')))
    lines.append(R(bMid(IV_L, IV_R, 'Node degraded: drive failure triggers FlexProtect restripe; do not remove until complete')))
    lines.append(R(bMid(IV_L, IV_R, 'Quota: full hard quota blocks all writes; raise limit or archive data immediately')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Alert fires → isi status + event log → identify fault layer → remediate → verify health'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SyncIQ Issues'), bMid(B2_L, B2_R, 'Cluster Issues'), bMid(B3_L, B3_R, 'Client Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Policy stalled'), bMid(B2_L, B2_R, 'Node degraded'), bMid(B3_L, B3_R, 'Auth failure'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RPO exceeded'), bMid(B2_L, B2_R, 'Drive failure'), bMid(B3_L, B3_R, 'Quota exceeded'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Network blocked'), bMid(B2_L, B2_R, 'FlexProt stall'), bMid(B3_L, B3_R, 'NFS mount fail'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Target cert err'), bMid(B2_L, B2_R, 'Pool 100% full'), bMid(B3_L, B3_R, 'SMB access deny'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Failover stuck'), bMid(B2_L, B2_R, 'Slow restripe'), bMid(B3_L, B3_R, 'Slow I/O'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  isi status → event log filter → isi sync job list → isi quota list → targeted fix'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Symptom', 'First check', 'Command', 'Fix', 'Escalate if'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['SyncIQ stall', 'Network path', 'isi sync job', 'Fix route', 'Policy errors'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Node degraded', 'Drive state', 'isi status', 'Replace drive', 'Node offline'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Quota full', 'Usage vs. limit', 'isi quota list', 'Raise or archive', 'App writes fail'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Auth failure', 'AD join state', 'isi auth status', 'Rejoin AD', 'KDC unreachable'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: check drive bay LEDs for failed drives; verify back-end cable for degraded node'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Policy stalled = SyncIQ job in Error or Needs Attention state; check isi sync job list'))
    lines.append(txt_row('  RPO exceeded   = Last successful sync older than RPO target; data loss risk if source fails'))
    lines.append(txt_row('  FlexProt stall = FlexProtect restripe paused; pool too full to complete; free capacity first'))
    lines.append(txt_row('  Pool 100% full = All usable space consumed; SmartPool migration and FlexProtect both stall'))
    lines.append(txt_row('  isi auth status= Show AD/LDAP provider join state and Kerberos ticket validity'))
    lines.append(txt_row('  KDC unreachable= Kerberos Key Distribution Center offline; all Kerberos auth fails'))
    lines.append(txt_row('  Target cert err= SyncIQ TLS cert mismatch between source and target; regenerate cert'))
    lines.append(txt_row('  NFS mount fail = Check export policy in access zone; confirm client IP in export client list'))
    lines.append(txt_row('  SMB access deny= Check share permissions and ACL in access zone; confirm AD group membership'))
    lines.append(txt_row('  Slow restripe  = FlexProtect running; I/O throttled; normal behavior after node/drive event'))
    lines.append(txt_row('  Failover stuck = SyncIQ failover did not complete; check allow_writes on target policy'))
    lines.append(txt_row('  isi quota list = Show quota usage; -v for details; identify directory exceeding hard limit'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powerstore',
    'docs/storage/dell/powerstore/index.md',
    'Dell PowerStore — NVMe mid-range; block and file; inline dedup/compress; Metro Volume',
)
def dell_powerstore():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerStore Mid-Range NVMe Storage'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'PowerStore: Dell NVMe mid-range array; block (FC/iSCSI/NVMe-oF) and file (NFS/SMB)')))
    lines.append(R(bMid(IV_L, IV_R, 'Inline deduplication and compression; DARE encryption; CloudIQ via SCG for analytics')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication: async native (volume groups); Metro Volume for zero-RPO sync')))
    lines.append(R(bMid(IV_L, IV_R, 'Managed via PowerStore Manager (REST API + web GUI) and pstcli CLI')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Host HBA/NIC → FC/iSCSI/NVMe-oF → PowerStore appliance → NVMe RAID → inline dedup/compress'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Architecture'), bMid(B2_L, B2_R, 'Operations'), bMid(B3_L, B3_R, 'Security'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NVMe appliance'), bMid(B2_L, B2_R, 'PowerStore Mgr'), bMid(B3_L, B3_R, 'DARE encryption'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Block + File'), bMid(B2_L, B2_R, 'pstcli'), bMid(B3_L, B3_R, 'LDAP / AD auth'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Inline dedup'), bMid(B2_L, B2_R, 'REST API'), bMid(B3_L, B3_R, 'RBAC roles'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Metro Volume'), bMid(B2_L, B2_R, 'Snap policies'), bMid(B3_L, B3_R, 'Audit logging'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CloudIQ / SCG'), bMid(B2_L, B2_R, 'Async repl'), bMid(B3_L, B3_R, 'TLS mgmt plane'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Host I/O → NVMe drives → inline dedup/compress → snapshot delta → async/sync replication'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Feature', 'T-series', 'X-series', 'Protocol', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Workload', 'Block + File', 'Block only', 'FC / iSCSI', 'NVMe/FC support'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Efficiency', 'Dedup + comp', 'Dedup + comp', 'NFS / SMB', 'Inline always on'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Replication', 'Async + Metro', 'Async + Metro', 'NVMe/TCP', 'Zero-RPO Metro'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Media', 'All-NVMe', 'All-NVMe', '—', 'RAID 5 inline'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: PowerStore 500T/1000T/3000T appliance (2U); dual node cluster optional'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Metro Volume   = Active-active sync replication between two PowerStore appliances; zero RPO'))
    lines.append(txt_row('  Inline dedup   = Deduplication at write time; data compared against existing blocks before write'))
    lines.append(txt_row('  Inline compress= Compression at write time; reduces media consumption without post-process lag'))
    lines.append(txt_row('  PowerStore Mgr = Web GUI and REST API management interface for PowerStore appliances'))
    lines.append(txt_row('  pstcli         = PowerStore CLI; connects to appliance REST API from admin workstation'))
    lines.append(txt_row('  DARE           = Data At Rest Encryption; SED drives with key management via KMIP'))
    lines.append(txt_row('  CloudIQ        = Dell SaaS analytics platform; receives telemetry from PowerStore via SCG'))
    lines.append(txt_row('  SCG            = Secure Connect Gateway; phone-home proxy for CloudIQ telemetry upload'))
    lines.append(txt_row('  Async repl     = Volume group replication to remote PowerStore; configurable RPO schedule'))
    lines.append(txt_row('  NVMe/FC        = NVMe over Fibre Channel; lower latency than iSCSI for NVMe-native hosts'))
    lines.append(txt_row('  NVMe/TCP       = NVMe over TCP/IP; enables NVMe performance over standard Ethernet'))
    lines.append(txt_row('  RAID 5 inline  = NVMe RAID calculated inline on write; no separate RAID rebuild after failure'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powerstore-operations',
    'docs/storage/dell/powerstore/operations/index.md',
    'Dell PowerStore operations — snapshots, replication, health checks, CloudIQ, pstcli',
)
def dell_powerstore_operations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerStore Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Day-2 ops: snapshot lifecycle, replication monitoring, capacity, CloudIQ health review')))
    lines.append(R(bMid(IV_L, IV_R, 'Snapshots: policy-based volume/group snaps; scheduled or manual; thin pointer model')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication: monitor lag, transfer rate, and RPO gap via PowerStore Manager dashboard')))
    lines.append(R(bMid(IV_L, IV_R, 'pstcli: REST-backed CLI; volume create, snap apply, replication policy, health check')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  CloudIQ alert → PowerStore Manager → check health → pstcli or GUI action → verify'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Snapshot Ops'), bMid(B2_L, B2_R, 'Replication Ops'), bMid(B3_L, B3_R, 'Health / Capacity'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Snap policy run'), bMid(B2_L, B2_R, 'Repl lag check'), bMid(B3_L, B3_R, 'CloudIQ score'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Manual snap'), bMid(B2_L, B2_R, 'RPO monitor'), bMid(B3_L, B3_R, 'Capacity trend'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Snap restore'), bMid(B2_L, B2_R, 'Failover test'), bMid(B3_L, B3_R, 'Drive health'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Snap clone'), bMid(B2_L, B2_R, 'Repl pause'), bMid(B3_L, B3_R, 'Dedup savings'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Snap expire'), bMid(B2_L, B2_R, 'Repl resume'), bMid(B3_L, B3_R, 'Alert review'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Snap policy schedules → replication RPO check → capacity headroom review → alert clear loop'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Task', 'Tool', 'CLI', 'Frequency', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Health', 'CloudIQ', 'pstcli health', 'Daily', 'Check score'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Snapshot', 'PS Manager', 'pstcli snap', 'Per policy', 'Verify gen count'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Replication', 'PS Manager', 'pstcli repl', 'Daily', 'RPO check'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Capacity', 'PS Manager', 'pstcli vol list', 'Weekly', 'Alert >80%'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SCG appliance or VM phone-home; PowerStore Manager on embedded service processor'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  CloudIQ score  = Aggregate health score; checks capacity, performance, config, and replication'))
    lines.append(txt_row('  pstcli         = PowerStore command-line interface; wraps REST API for scripting'))
    lines.append(txt_row('  Snap policy    = Rule defining snapshot schedule, retention, and naming for a volume/group'))
    lines.append(txt_row('  Snap clone     = Writable thin clone created from a snapshot for test/dev use'))
    lines.append(txt_row('  Snap restore   = Revert a volume to a snapshot point-in-time state; overwrites current data'))
    lines.append(txt_row('  Repl lag       = Time difference between last replication sync and current; measures RPO gap'))
    lines.append(txt_row('  Failover test  = Switch writes to replication target; verify application continues; then fail back'))
    lines.append(txt_row('  Dedup savings  = Ratio of logical data written to physical consumed; shown in PS Manager'))
    lines.append(txt_row('  SCG phone-home = SCG proxy sends appliance telemetry to Dell CloudIQ SaaS platform'))
    lines.append(txt_row('  Volume group   = Logical grouping of volumes; snapped and replicated as consistent set'))
    lines.append(txt_row('  Snap expire    = Snapshot past retention date is automatically deleted per policy'))
    lines.append(txt_row('  Drive health   = SSD wear indicator and error count; shown in PowerStore Manager hardware view'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powerstore-security',
    'docs/storage/dell/powerstore/security/index.md',
    'Dell PowerStore security — DARE, LDAP/AD, RBAC, audit logging, TLS management plane',
)
def dell_powerstore_security():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerStore Security'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'PowerStore security: DARE (SED drives), LDAP/AD for admin auth, RBAC, audit log')))
    lines.append(R(bMid(IV_L, IV_R, 'DARE: SED drives + external KMIP key server; crypto erase on decommission')))
    lines.append(R(bMid(IV_L, IV_R, 'Admin access: LDAP/AD group-based roles; local admin for break-glass only')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit: all admin actions logged; export via syslog to SIEM; TLS 1.2+ on REST API')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  DARE at rest → TLS in transit → LDAP/AD admin auth → RBAC role check → audit log write'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Encryption'), bMid(B2_L, B2_R, 'Authentication'), bMid(B3_L, B3_R, 'Audit / Access'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DARE (SED)'), bMid(B2_L, B2_R, 'LDAP / AD'), bMid(B3_L, B3_R, 'Syslog / SIEM'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'KMIP key server'), bMid(B2_L, B2_R, 'Local break-glass'), bMid(B3_L, B3_R, 'RBAC roles'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key rotation'), bMid(B2_L, B2_R, 'MFA supported'), bMid(B3_L, B3_R, 'Admin audit log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Crypto erase'), bMid(B2_L, B2_R, 'API token auth'), bMid(B3_L, B3_R, 'Session timeout'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TLS REST API'), bMid(B2_L, B2_R, 'Cert management'), bMid(B3_L, B3_R, 'Alert on fail'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  DARE key check → LDAP role assignment → audit log export → periodic access review'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Control', 'Mechanism', 'Standard', 'Exception', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Encryption', 'DARE + KMIP', 'All volumes', 'KMIP outage', 'Key audit trail'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Admin auth', 'LDAP / AD', 'Named accounts', 'Local only', 'Login events'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['API access', 'Token + TLS', 'Short-lived token', '—', 'API call log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Logging', 'Syslog/SIEM', 'All admin ops', '—', 'Weekly review'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: KMIP server on isolated VLAN; management IP on OOB network; no shared mgmt'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  DARE           = Data At Rest Encryption; SED drives; keys managed by KMIP server'))
    lines.append(txt_row('  KMIP           = Key Management Interoperability Protocol; standard for external key servers'))
    lines.append(txt_row('  Crypto erase   = Destroy KMIP encryption key; all DARE-encrypted data becomes unreadable'))
    lines.append(txt_row('  RBAC roles     = PowerStore built-in roles: Administrator, Storage Operator, VM Admin, Viewer'))
    lines.append(txt_row('  API token auth = REST API session token; short-lived; invalidated on logout or timeout'))
    lines.append(txt_row('  Syslog         = Admin event log export; all GUI/CLI/API changes forwarded to SIEM'))
    lines.append(txt_row('  TLS REST API   = PowerStore Manager REST API and web GUI require TLS 1.2+'))
    lines.append(txt_row('  Cert management= Custom TLS cert upload for PowerStore Manager GUI; replaces self-signed'))
    lines.append(txt_row('  Break-glass    = Local admin account; use only when LDAP unavailable; log every use'))
    lines.append(txt_row('  MFA supported  = Multi-factor auth via LDAP identity provider integration'))
    lines.append(txt_row('  Session timeout= Configurable idle timeout for GUI and REST sessions; default 30 min'))
    lines.append(txt_row('  Alert on fail  = Failed login attempts trigger syslog event and optionally email alert'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-powerstore-troubleshooting',
    'docs/storage/dell/powerstore/troubleshooting/index.md',
    'Dell PowerStore troubleshooting — drive fault, replication failure, capacity, KMIP outage',
)
def dell_powerstore_troubleshooting():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell PowerStore Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Common faults: NVMe drive failure, replication lag, KMIP unreachable, capacity near-full')))
    lines.append(R(bMid(IV_L, IV_R, 'Drive failure: RAID rebuild auto-starts; replace failed drive; monitor rebuild progress')))
    lines.append(R(bMid(IV_L, IV_R, 'KMIP outage: array continues I/O while keys are cached; fix KMIP before cache expires')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication lag: check network path, bandwidth throttle, and RPO policy schedule')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  CloudIQ alert → PowerStore Manager event → identify fault category → remediate → verify'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Hardware Faults'), bMid(B2_L, B2_R, 'Replication'), bMid(B3_L, B3_R, 'Security / Data'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NVMe drive fail'), bMid(B2_L, B2_R, 'Repl lag >RPO'), bMid(B3_L, B3_R, 'KMIP unreachable'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RAID rebuild'), bMid(B2_L, B2_R, 'Policy paused'), bMid(B3_L, B3_R, 'Capacity >90%'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Node fault'), bMid(B2_L, B2_R, 'Network loss'), bMid(B3_L, B3_R, 'DARE key err'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SSD wear high'), bMid(B2_L, B2_R, 'Failover stuck'), bMid(B3_L, B3_R, 'Snap space full'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Fan / PSU fault'), bMid(B2_L, B2_R, 'Cert expired'), bMid(B3_L, B3_R, 'LDAP auth fail'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Check CloudIQ score → event log → hardware health view → isolate layer → fix and verify'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Symptom', 'First check', 'Tool', 'Fix', 'Escalate if'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Drive failure', 'Drive health', 'PS Manager HW', 'Replace drive', 'RAID rebuild fail'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['KMIP outage', 'KMIP reachable', 'PS Manager sec', 'Fix KMIP reach', 'Volumes locked'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Repl lag', 'Network path', 'PS Manager repl', 'Fix BW throttle', 'RPO exceeded'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Capacity >90%', 'Usage trend', 'CloudIQ', 'Delete/archive', 'Pool full blocks'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: check drive bay LED (amber = degraded); PSU LED; SFP port for replication link'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  RAID rebuild   = PowerStore reconstructs data after NVMe drive failure onto hot spare'))
    lines.append(txt_row('  KMIP unreachable= Key server offline; array serves cached keys temporarily; fix before expiry'))
    lines.append(txt_row('  Volumes locked = DARE-encrypted volumes locked when KMIP key unavailable and cache expired'))
    lines.append(txt_row('  Repl lag >RPO  = Replication behind schedule; data loss exposure exceeds agreed RPO'))
    lines.append(txt_row('  Policy paused  = Replication policy suspended; resume after fixing network or space issue'))
    lines.append(txt_row('  Failover stuck = Metro Volume or async failover did not complete; check event log for error'))
    lines.append(txt_row('  Cert expired   = Replication TLS cert expired on source or target; renew and re-pair'))
    lines.append(txt_row('  SSD wear high  = NVMe drive write endurance approaching limit; replace before failure'))
    lines.append(txt_row('  Snap space full= Snapshot delta store consumed available capacity; delete old snaps first'))
    lines.append(txt_row('  LDAP auth fail = Admin cannot log in; check AD/LDAP connectivity and group membership'))
    lines.append(txt_row('  BW throttle    = Replication bandwidth limit; increase or remove throttle to clear lag'))
    lines.append(txt_row('  Pool full blocks= When usable capacity = 0%, all writes fail; emergency capacity needed'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-scg',
    'docs/storage/dell/secure-connect-gateway/index.md',
    'Dell Secure Connect Gateway (SCG) — phone-home proxy; CloudIQ telemetry; support relay',
)
def dell_scg():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Secure Connect Gateway (SCG)'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'SCG: Dell phone-home gateway; relays support telemetry from on-prem arrays to Dell')))
    lines.append(R(bMid(IV_L, IV_R, 'Outbound HTTPS port 443 to Dell support; no inbound connections required')))
    lines.append(R(bMid(IV_L, IV_R, 'Supports: PowerMax, Unity, PowerScale, PowerStore, VxBlock, iDRAC, VxRail, ECS')))
    lines.append(R(bMid(IV_L, IV_R, 'Deployment: VM or physical appliance; registered devices enroll via support portal')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Array sends telemetry → SCG collects → HTTPS to Dell → CloudIQ ingests → alert/analytics'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Connectivity'), bMid(B2_L, B2_R, 'Managed Devices'), bMid(B3_L, B3_R, 'Functions'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'HTTPS port 443'), bMid(B2_L, B2_R, 'PowerMax'), bMid(B3_L, B3_R, 'Telemetry relay'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No inbound req.'), bMid(B2_L, B2_R, 'Unity'), bMid(B3_L, B3_R, 'Alert forward'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Proxy support'), bMid(B2_L, B2_R, 'PowerScale'), bMid(B3_L, B3_R, 'Log collection'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TLS 1.2+'), bMid(B2_L, B2_R, 'PowerStore'), bMid(B3_L, B3_R, 'CloudIQ feed'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VM or appliance'), bMid(B2_L, B2_R, 'iDRAC / VxRail'), bMid(B3_L, B3_R, 'Support SR open'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Device enrolled → SCG polls or receives events → batches telemetry → forwards to Dell'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Aspect', 'Detail', 'Requirement', 'Alternative', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Network', 'HTTPS 443 out', 'Firewall allow', 'HTTP proxy', 'DNS resolution'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Deployment', 'VM (OVA)', '4 vCPU, 8 GB', 'Physical appl.', 'vCenter needed'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Registration', 'Support acct', 'Active contract', '—', 'Per device SN'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['CloudIQ', 'Auto-feeds', 'SCG enrolled', 'Direct call home', 'SaaS analytics'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SCG VM on management network; DNS and port 443 to esrs.emc.com required'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Phone-home     = Automated outbound telemetry from array to Dell Support; no manual uploads'))
    lines.append(txt_row('  CloudIQ        = Dell SaaS analytics and health platform; receives data from SCG relay'))
    lines.append(txt_row('  ESRS           = EMC Secure Remote Support; earlier name for SCG protocol/service'))
    lines.append(txt_row('  Alert forward  = SCG forwards array alerts to Dell Support; can auto-open Service Requests'))
    lines.append(txt_row('  Log collection = SCG pulls diagnostic logs from enrolled arrays for support case upload'))
    lines.append(txt_row('  Proxy support  = SCG can use HTTP/HTTPS proxy for outbound if direct internet not allowed'))
    lines.append(txt_row('  TLS 1.2+       = All traffic from SCG to Dell uses TLS; no unencrypted support traffic'))
    lines.append(txt_row('  OVA            = Open Virtualization Appliance; SCG deployment format for VMware'))
    lines.append(txt_row('  Support SR     = Service Request; SCG can auto-create SRs when critical alerts fire'))
    lines.append(txt_row('  Enrolled device= Array registered with SCG; SCG relays its events and telemetry to Dell'))
    lines.append(txt_row('  Direct call home= Some arrays can phone home directly without SCG; SCG is preferred'))
    lines.append(txt_row('  Active contract= SCG and CloudIQ require valid Dell support contract for enrolled devices'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-unity',
    'docs/storage/dell/unity/index.md',
    'Dell Unity XT — unified mid-range; dual SP; block FC/iSCSI; file NFS/SMB; FAST VP tiering',
)
def dell_unity():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Unity XT Unified Mid-Range Storage'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Unity XT: Dell unified mid-range; dual Storage Processors (SP A/B); active-passive HA')))
    lines.append(R(bMid(IV_L, IV_R, 'Block: FC and iSCSI LUNs; consistency groups; metro volumes for active-active')))
    lines.append(R(bMid(IV_L, IV_R, 'File: NFS, SMB, FTP, NDMP via NAS Server; multiple NAS servers per array')))
    lines.append(R(bMid(IV_L, IV_R, 'FAST VP automated tiering: Flash, SAS, NL-SAS; schedule-driven data placement')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Host → SP A or SP B → LUN / NAS Server → FAST VP tiering → Flash / SAS / NL-SAS drives'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Architecture'), bMid(B2_L, B2_R, 'Operations'), bMid(B3_L, B3_R, 'Security'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Dual SP HA'), bMid(B2_L, B2_R, 'Unisphere GUI'), bMid(B3_L, B3_R, 'DARE (SED)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'FAST VP tiers'), bMid(B2_L, B2_R, 'uemcli'), bMid(B3_L, B3_R, 'LDAP / AD auth'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NAS Server'), bMid(B2_L, B2_R, 'Snap schedules'), bMid(B3_L, B3_R, 'RBAC roles'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Block + File'), bMid(B2_L, B2_R, 'Async repl'), bMid(B3_L, B3_R, 'Audit logging'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CloudIQ / SCG'), bMid(B2_L, B2_R, 'FAST VP job'), bMid(B3_L, B3_R, 'TLS mgmt plane'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  SP A/B active-passive → LUN or NAS Server → FAST VP moves data → async replication'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Layer', 'Block', 'File', 'Protocol', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Access', 'LUN / CG', 'NAS Server', 'FC / iSCSI', 'NFS / SMB'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Snapshot', 'LUN snap', 'FS snap', 'NDMP backup', 'Per schedule'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Replication', 'Async / Metro', 'Async NAS', 'FC / iSCSI', 'RPO minutes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Tiering', 'FAST VP', 'FAST VP', 'Flash/SAS/NL', 'Auto-policy'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: Unity chassis (2U base); expansion DAEs; dual SP blades; SPE/DPE drive enclosures'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SP A / SP B    = Storage Processors; active-passive pair; SP A owns resources normally'))
    lines.append(txt_row('  FAST VP        = Fully Automated Storage Tiering for Virtual Pools; moves data by heat'))
    lines.append(txt_row('  NAS Server     = Virtual NAS container on Unity; has own IP, auth provider, shares/exports'))
    lines.append(txt_row('  CG             = Consistency Group; set of LUNs snapped/replicated together as a unit'))
    lines.append(txt_row('  Metro Volume   = Active-active sync replication between two Unity arrays; zero RPO'))
    lines.append(txt_row('  uemcli         = Unity CLI tool; REST API-backed; uemcli /stor/prov/luns/lun -list'))
    lines.append(txt_row('  Unisphere      = Web GUI for Unity management; login with AD or local admin credentials'))
    lines.append(txt_row('  DARE           = Data At Rest Encryption; SED drives with KMIP key management'))
    lines.append(txt_row('  NL-SAS         = Near-Line SAS; high-capacity archive tier; lower IOPS than SAS'))
    lines.append(txt_row('  NDMP           = Network Data Management Protocol; backup NAS data via NDMP client'))
    lines.append(txt_row('  SPE            = Storage Processor Enclosure; base chassis containing SP A and SP B'))
    lines.append(txt_row('  DAE            = Disk Array Enclosure; expansion shelf for additional drives'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-unity-operations',
    'docs/storage/dell/unity/operations/index.md',
    'Dell Unity operations — SP health, FAST VP, snapshots, async replication, uemcli tasks',
)
def dell_unity_operations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Unity Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Day-2 ops: SP health check, FAST VP job monitoring, snapshot lifecycle, replication')))
    lines.append(R(bMid(IV_L, IV_R, 'SP health: Unisphere health dashboard; uemcli /sys/general/health -list')))
    lines.append(R(bMid(IV_L, IV_R, 'FAST VP: schedule-driven tier moves; monitor via Unisphere Storage Pool view')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication: async session monitoring; RPO check; failover / failback procedures')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Health check → FAST VP job review → snap schedule verify → replication lag → alert close'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Health / SP'), bMid(B2_L, B2_R, 'Data Services'), bMid(B3_L, B3_R, 'Replication'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SP health check'), bMid(B2_L, B2_R, 'FAST VP job'), bMid(B3_L, B3_R, 'Session state'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Drive health'), bMid(B2_L, B2_R, 'Snap schedule'), bMid(B3_L, B3_R, 'RPO monitor'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Fan / PSU'), bMid(B2_L, B2_R, 'Snap restore'), bMid(B3_L, B3_R, 'Failover'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Pool capacity'), bMid(B2_L, B2_R, 'Snap expire'), bMid(B3_L, B3_R, 'Failback'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CloudIQ score'), bMid(B2_L, B2_R, 'Pool shrink/grow'), bMid(B3_L, B3_R, 'Repl resync'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  SP status → FAST VP tier check → snap policy audit → replication RPO → capacity trend'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Task', 'Tool', 'CLI', 'Frequency', 'Alert threshold'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['SP health', 'Unisphere', 'uemcli health', 'Daily', 'Any degraded'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['FAST VP', 'Unisphere', 'uemcli tier', 'Weekly', 'Stalled job'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Replication', 'Unisphere', 'uemcli repl', 'Daily', 'RPO exceeded'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Capacity', 'CloudIQ', 'uemcli pool', 'Weekly', '>80% used'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: Unisphere on embedded service processor; uemcli connects via HTTPS to SP IP'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  uemcli         = Unity CLI; REST API wrapper: uemcli /stor/prov/luns/lun -list'))
    lines.append(txt_row('  FAST VP job    = Scheduled data migration between Flash, SAS, and NL-SAS tiers'))
    lines.append(txt_row('  Snap schedule  = Automated snapshot rule; hourly/daily/weekly; max snap count limit'))
    lines.append(txt_row('  Snap restore   = Revert LUN or filesystem to snapshot state; overwrites current data'))
    lines.append(txt_row('  Snap expire    = Snapshot past retention date deleted automatically; capacity reclaimed'))
    lines.append(txt_row('  Pool capacity  = Storage pool usable space; alert at >80% used to avoid write failures'))
    lines.append(txt_row('  Repl session   = Unity async replication pairing; shows last sync time and transfer size'))
    lines.append(txt_row('  Failover       = Switch replication target to read/write; application moves to DR site'))
    lines.append(txt_row('  Failback       = Resync data back to primary Unity; resume original replication direction'))
    lines.append(txt_row('  Repl resync    = Re-establish replication after failback; delta sync not full reseed'))
    lines.append(txt_row('  CloudIQ score  = SaaS health score; receives data from Unity via SCG phone-home'))
    lines.append(txt_row('  SP degraded    = One SP fault; remaining SP takes all I/O; repair SP immediately'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-unity-ops-install-upgrade',
    'docs/storage/dell/unity/operations/install-upgrade/index.md',
    'Dell Unity install and upgrade — initial config, OE upgrade, non-disruptive rolling SP upgrade',
)
def dell_unity_ops_install_upgrade():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Unity Install and Upgrade'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Initial install: rack Unity → cable SPs and DAEs → configure via Unisphere wizard')))
    lines.append(R(bMid(IV_L, IV_R, 'OE upgrade: download upgrade package → upload to Unity → health pre-check → commit')))
    lines.append(R(bMid(IV_L, IV_R, 'Rolling upgrade: SP B reboots first → SP A takes all I/O → SP B ready → SP A reboots')))
    lines.append(R(bMid(IV_L, IV_R, 'Non-disruptive: hosts continue I/O during upgrade; one SP always serving')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Health pre-check → upload OE package → commit → SP B upgrade/reboot → SP A upgrade/reboot'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Initial Install'), bMid(B2_L, B2_R, 'OE Upgrade'), bMid(B3_L, B3_R, 'Add Drives/DAE'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Rack and cable'), bMid(B2_L, B2_R, 'Download OE'), bMid(B3_L, B3_R, 'Cable new DAE'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Power on'), bMid(B2_L, B2_R, 'Upload to array'), bMid(B3_L, B3_R, 'Rescan drives'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Unisphere wizard'), bMid(B2_L, B2_R, 'Pre-check run'), bMid(B3_L, B3_R, 'Expand pool'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Network config'), bMid(B2_L, B2_R, 'SP B upgrade'), bMid(B3_L, B3_R, 'FAST VP rebal'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCG enroll'), bMid(B2_L, B2_R, 'SP A upgrade'), bMid(B3_L, B3_R, 'Verify health'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  OE upgrade non-disruptive; hosts continue I/O; each SP takes ~15-20 min to reboot'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Operation', 'Duration', 'Disruptive', 'Rollback', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Initial install', '2–4 hours', 'Yes (new system)', 'N/A', 'Follow wizard'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['OE upgrade', '30–60 min', 'No (rolling)', 'Prior OE image', 'Pre-check first'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['DAE add', '15 min', 'No', 'Remove DAE', 'Rescan required'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Drive add', '5 min', 'No', 'N/A', 'Pool expand opt.'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SPE base unit; DAEs connect via SAS expansion cable from SP to first DAE chain'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  OE             = Operating Environment; Unity OS upgrade package (.tgz file from Dell)')    )
    lines.append(txt_row('  Rolling upgrade= SP B upgraded first while SP A serves I/O; then roles swap for SP A upgrade'))
    lines.append(txt_row('  Pre-check      = Automated health validation before upgrade commit; blocks on unresolved alerts'))
    lines.append(txt_row('  Unisphere wizard= Web-based initial configuration wizard; run once after first power-on'))
    lines.append(txt_row('  SPE            = Storage Processor Enclosure; base 2U chassis containing SP A and SP B'))
    lines.append(txt_row('  DAE            = Disk Array Enclosure; 2U or 4U expansion shelf; chained from SPE'))
    lines.append(txt_row('  FAST VP rebal  = After adding drives, FAST VP distributes data across new capacity'))
    lines.append(txt_row('  Pool expand    = Add drives to existing storage pool; capacity available after rescan'))
    lines.append(txt_row('  SCG enroll     = Register Unity with SCG after install for CloudIQ and phone-home support'))
    lines.append(txt_row('  Rollback OE    = If upgrade fails mid-way, Unity can revert to previous OE version'))
    lines.append(txt_row('  SAS expansion  = Back-end SAS cabling between SPE and DAE; daisy-chain up to max DAEs'))
    lines.append(txt_row('  15-20 min reboot= Each SP reboot time during OE upgrade; I/O served by partner SP'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-unity-security',
    'docs/storage/dell/unity/security/index.md',
    'Dell Unity security — DARE, LDAP/AD, RBAC, NAS server auth, audit logging',
)
def dell_unity_security():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Unity Security'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Unity security: DARE (SED drives), LDAP/AD for admin and NAS auth, RBAC, audit log')))
    lines.append(R(bMid(IV_L, IV_R, 'Admin auth: LDAP/AD group mapped to Unity roles; local accounts for break-glass')))
    lines.append(R(bMid(IV_L, IV_R, 'NAS auth: each NAS Server has own AD/LDAP provider; Kerberos for SMB authentication')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit: all Unisphere and uemcli actions logged; export via syslog to SIEM')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  DARE at rest → TLS REST API → LDAP role check → NAS Kerberos → file ACL → audit log'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Encryption'), bMid(B2_L, B2_R, 'Admin Auth'), bMid(B3_L, B3_R, 'NAS / Audit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DARE (SED)'), bMid(B2_L, B2_R, 'LDAP / AD'), bMid(B3_L, B3_R, 'NAS AD/Kerberos'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'KMIP key server'), bMid(B2_L, B2_R, 'RBAC roles'), bMid(B3_L, B3_R, 'Syslog SIEM'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key rotation'), bMid(B2_L, B2_R, 'Local break-glass'), bMid(B3_L, B3_R, 'Admin audit log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Crypto erase'), bMid(B2_L, B2_R, 'TLS REST API'), bMid(B3_L, B3_R, 'NAS file audit'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'In-transit TLS'), bMid(B2_L, B2_R, 'Session timeout'), bMid(B3_L, B3_R, 'CEE export'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  DARE + KMIP → LDAP role assignment → NAS Kerberos → file ACL → syslog audit review'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Control', 'Mechanism', 'Standard', 'Exception', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Encryption', 'DARE + KMIP', 'All volumes', 'KMIP outage', 'Key audit trail'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Admin auth', 'LDAP / AD', 'Named accounts', 'Local only', 'Login events'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['NAS file auth', 'AD Kerberos', 'Per NAS Server', 'NTLM fallback', 'Auth events'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Logging', 'Syslog + CEE', 'SIEM ingest', '—', 'Weekly review'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: KMIP on isolated VLAN; Unity management IP on OOB network; no shared mgmt'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  DARE           = Data At Rest Encryption; SED drives; key managed by external KMIP server'))
    lines.append(txt_row('  RBAC roles     = Unity roles: Administrator, Storage Admin, VM Admin, Operator, Auditor'))
    lines.append(txt_row('  NAS Server AD  = Each NAS Server joined to its own AD domain for SMB Kerberos auth'))
    lines.append(txt_row('  Kerberos       = Mutual auth for SMB clients and Unity NAS Server via AD tickets'))
    lines.append(txt_row('  NTLM fallback  = Legacy SMB auth when Kerberos unavailable; weaker; disable if possible'))
    lines.append(txt_row('  CEE            = Common Event Enabler; NAS file audit export to SIEM'))
    lines.append(txt_row('  File audit     = NAS Server logs file access events (open, delete, rename) via CEE'))
    lines.append(txt_row('  Syslog         = Admin action log (Unisphere / uemcli changes) forwarded to SIEM'))
    lines.append(txt_row('  Session timeout= Configurable idle timeout for Unisphere and uemcli sessions'))
    lines.append(txt_row('  Crypto erase   = Destroy SED encryption key on drive decommission; data unrecoverable'))
    lines.append(txt_row('  KMIP outage    = Unity caches keys temporarily; fix KMIP before cache expires'))
    lines.append(txt_row('  Break-glass    = Local Unity admin account; use only when LDAP unavailable; log all use'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-unity-troubleshooting',
    'docs/storage/dell/unity/troubleshooting/index.md',
    'Dell Unity troubleshooting — SP failover, drive rebuild, FAST VP stall, NAS fault',
)
def dell_unity_troubleshooting():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell Unity Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Common faults: SP failure (failover to peer), drive failure, FAST VP stall, NAS fault')))
    lines.append(R(bMid(IV_L, IV_R, 'SP failure: peer SP takes all I/O; replace faulted SP; monitor for stability')))
    lines.append(R(bMid(IV_L, IV_R, 'Drive failure: RAID rebuild starts automatically; do not remove drive until rebuild done')))
    lines.append(R(bMid(IV_L, IV_R, 'FAST VP stall: pool too full to tier; free space or expand pool before VP can run')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Unisphere alert → health view → identify fault (SP/drive/NAS/pool) → remediate → verify'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SP / Hardware'), bMid(B2_L, B2_R, 'Data Services'), bMid(B3_L, B3_R, 'NAS / Network'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SP fault'), bMid(B2_L, B2_R, 'FAST VP stall'), bMid(B3_L, B3_R, 'NAS unreachable'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Drive failure'), bMid(B2_L, B2_R, 'Snap space full'), bMid(B3_L, B3_R, 'SMB auth fail'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RAID rebuild'), bMid(B2_L, B2_R, 'Repl lag'), bMid(B3_L, B3_R, 'NFS mount fail'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Fan / PSU fault'), bMid(B2_L, B2_R, 'Pool near-full'), bMid(B3_L, B3_R, 'AD join fail'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SFP / port fault'), bMid(B2_L, B2_R, 'KMIP outage'), bMid(B3_L, B3_R, 'Slow NFS I/O'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Check Unisphere health → event log filter → uemcli health query → fix layer → verify'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Symptom', 'First check', 'Tool', 'Fix', 'Escalate if'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['SP fault', 'SP state LEDs', 'Unisphere HW', 'Replace SP', 'Both SPs failed'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Drive failure', 'Drive bay LED', 'uemcli disk', 'Replace drive', 'Rebuild fails'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['FAST VP stall', 'Pool capacity', 'Unisphere pool', 'Free space', 'Pool >95% full'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['NAS unreachable', 'NAS Server state', 'Unisphere NAS', 'Failover NAS', 'SP owning fault'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SP A/B LEDs; drive bay amber LED; SFP port light; PSU green/amber indicator'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SP failover    = When SP A fails, SP B takes ownership of all LUNs and NAS Servers'))
    lines.append(txt_row('  RAID rebuild   = Drive replacement triggers automatic data reconstruction onto new drive'))
    lines.append(txt_row('  FAST VP stall  = Pool <10% free; automated tiering cannot move data; free space first'))
    lines.append(txt_row('  NAS failover   = NAS Server migrated to peer SP when owning SP faults'))
    lines.append(txt_row('  AD join fail   = NAS Server cannot rejoin AD domain; SMB auth will fail for all shares'))
    lines.append(txt_row('  Pool near-full = Pool >80% used; alert threshold; FAST VP stalls at ~95%'))
    lines.append(txt_row('  KMIP outage    = DARE key unavailable; Unity uses cached key temporarily; fix urgently'))
    lines.append(txt_row('  uemcli disk    = uemcli /stor/hw/disk -list; shows drive state, slot, and tier'))
    lines.append(txt_row('  Both SPs failed= Complete array outage; contact Dell TAC immediately; P1 case'))
    lines.append(txt_row('  SFP port fault = Fibre Channel or iSCSI port SFP failed; host paths go dead'))
    lines.append(txt_row('  Failover NAS   = Manually move NAS Server to peer SP via Unisphere migration wizard'))
    lines.append(txt_row('  Slow NFS I/O   = Check SP CPU, network saturation, and FAST VP job contending for I/O'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-vplex',
    'docs/storage/dell/vplex/index.md',
    'Dell VPLEX — storage federation; virtual volumes; Metro active-active; GeoSynchrony OS',
)
def dell_vplex():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell VPLEX Storage Federation'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VPLEX: Dell storage virtualization/federation; presents virtual volumes to hosts')))
    lines.append(R(bMid(IV_L, IV_R, 'VPLEX Local: single cluster; virtualizes back-end arrays; pooling and migration')))
    lines.append(R(bMid(IV_L, IV_R, 'VPLEX Metro: two clusters linked via WAN; distributed volumes for active-active')))
    lines.append(R(bMid(IV_L, IV_R, 'GeoSynchrony OS: VPLEX management; directors (I/O and Storage); witness for Metro')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Host → I/O Director → virtual volume → Storage Director → back-end array LUN'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Architecture'), bMid(B2_L, B2_R, 'Operations'), bMid(B3_L, B3_R, 'Metro / HA'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'I/O Director'), bMid(B2_L, B2_R, 'VPLEX CLI'), bMid(B3_L, B3_R, 'Distributed vol'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Storage Director'), bMid(B2_L, B2_R, 'Virtual vol prov'), bMid(B3_L, B3_R, 'Witness VM'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'GeoSynchrony OS'), bMid(B2_L, B2_R, 'CG management'), bMid(B3_L, B3_R, 'WAN link <5ms'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'DRAM write cache'), bMid(B2_L, B2_R, 'Storage view'), bMid(B3_L, B3_R, 'Split-brain prot'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Back-end arrays'), bMid(B2_L, B2_R, 'Director health'), bMid(B3_L, B3_R, 'Metro failover'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  I/O director receives host write → DRAM cache → Storage Director → back-end array'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Mode', 'VPLEX Local', 'VPLEX Metro', 'Protocol', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Clusters', '1 cluster', '2 clusters', 'FC host', 'iSCSI optional'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Volume type', 'Virtual vol', 'Distributed vol', 'FC back-end', 'Array-agnostic'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['RPO', 'N/A local', 'Zero (sync)', 'WAN IP link', '<5ms RTT req.'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Witness', 'Not required', 'Required', '—', 'Tie-breaker VM'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: VPLEX chassis with director blades; FC fabric to hosts and back-end arrays'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  I/O Director   = Front-end VPLEX blade; handles host FC connections and virtual volume I/O'))
    lines.append(txt_row('  Storage Director= Back-end VPLEX blade; connects to physical array FC ports'))
    lines.append(txt_row('  Virtual volume = Logical volume presented to host; backed by one or more array LUNs'))
    lines.append(txt_row('  Distributed vol= Metro volume visible and writable from both VPLEX clusters simultaneously'))
    lines.append(txt_row('  GeoSynchrony   = VPLEX management OS; configuration, CLI access, director orchestration'))
    lines.append(txt_row('  Storage view   = VPLEX host access control; maps virtual volumes to initiator ports'))
    lines.append(txt_row('  DRAM cache     = Write cache in director; coalesces writes before committing to array'))
    lines.append(txt_row('  Witness VM     = Third-site VM; breaks tie in Metro split-brain; must be on neutral site'))
    lines.append(txt_row('  Split-brain    = Both clusters lose WAN; each thinks it is the only survivor; witness decides'))
    lines.append(txt_row('  Metro failover = One cluster takes full I/O after site loss; witness determines survivor'))
    lines.append(txt_row('  CG             = Consistency Group; set of distributed volumes with write-order fidelity'))
    lines.append(txt_row('  VPLEX CLI      = vplex-shell; management console on GeoSynchrony for all VPLEX config'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-vplex-operations',
    'docs/storage/dell/vplex/operations/index.md',
    'Dell VPLEX operations — virtual volume provisioning, CG management, Metro ops, health checks',
)
def dell_vplex_operations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell VPLEX Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Day-2 ops: virtual volume provisioning, CG operations, Metro volume health, WAN monitoring')))
    lines.append(R(bMid(IV_L, IV_R, 'Provision: claim back-end LUN → create storage volume → virtual volume → storage view')))
    lines.append(R(bMid(IV_L, IV_R, 'Metro ops: check distributed volume state, WAN link health, and witness connectivity')))
    lines.append(R(bMid(IV_L, IV_R, 'Health: director status, cache utilization, back-end path health via VPLEX CLI')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Back-end LUN claimed → virtual volume created → CG added → storage view updated → host sees'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Provisioning'), bMid(B2_L, B2_R, 'Metro Ops'), bMid(B3_L, B3_R, 'Health'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Claim back-end'), bMid(B2_L, B2_R, 'Dist vol state'), bMid(B3_L, B3_R, 'Director status'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Create virt vol'), bMid(B2_L, B2_R, 'WAN link health'), bMid(B3_L, B3_R, 'Cache stats'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Add to CG'), bMid(B2_L, B2_R, 'Witness check'), bMid(B3_L, B3_R, 'BE path check'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Storage view'), bMid(B2_L, B2_R, 'Metro failover'), bMid(B3_L, B3_R, 'Event log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Host rescan'), bMid(B2_L, B2_R, 'Metro failback'), bMid(B3_L, B3_R, 'Alert review'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Director health → WAN link state → distributed volume check → storage view audit'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Task', 'CLI context', 'Command', 'Frequency', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Director health', 'engines', 'ls directors', 'Daily', 'Any degraded'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Vol state', 'virtual-volumes', 'ls -t', 'Daily', 'Check detached'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['WAN link', 'clusters', 'ls comm-links', 'Daily (Metro)', 'Check latency'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Witness', 'clusters', 'ls witnesses', 'Weekly', 'Must be reachable'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: VPLEX chassis FC ports to SAN fabric; IP WAN ports for Metro cluster link'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Claim back-end = VPLEX takes ownership of an array LUN for use as a storage volume'))
    lines.append(txt_row('  Storage volume = VPLEX internal representation of a claimed back-end LUN'))
    lines.append(txt_row('  Virtual volume = External-facing volume presented to hosts via VPLEX storage view'))
    lines.append(txt_row('  Storage view   = Maps virtual volumes to host initiator ports; VPLEX access control'))
    lines.append(txt_row('  Distributed vol= Metro volume type; accessible from both clusters simultaneously'))
    lines.append(txt_row('  WAN comm-link  = IP link between two VPLEX Metro clusters; must be <5ms RTT'))
    lines.append(txt_row('  Witness        = Third-site VM; provides quorum for Metro split decisions'))
    lines.append(txt_row('  Detached vol   = Virtual volume not currently accessible due to director or BE fault'))
    lines.append(txt_row('  Metro failover = One cluster takes full write ownership after WAN loss; witness arbitrates'))
    lines.append(txt_row('  Metro failback = After site recovery, resync cluster and restore distributed volume state'))
    lines.append(txt_row('  ls directors   = VPLEX CLI: list all directors and their operational state'))
    lines.append(txt_row('  ls comm-links  = VPLEX CLI: list Metro WAN communication links and latency stats'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-vplex-security',
    'docs/storage/dell/vplex/security/index.md',
    'Dell VPLEX security — LDAP admin auth, storage view access control, TLS, audit logging',
)
def dell_vplex_security():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell VPLEX Security'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VPLEX security: storage views for host access control; LDAP for admin auth; audit log')))
    lines.append(R(bMid(IV_L, IV_R, 'Storage view: binds virtual volumes to host initiator WWNs; deny by default')))
    lines.append(R(bMid(IV_L, IV_R, 'Admin auth: LDAP/AD group mapped to GeoSynchrony roles; local admin for emergency')))
    lines.append(R(bMid(IV_L, IV_R, 'TLS on management API; audit log of all CLI and GUI changes exportable via syslog')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Host WWN in storage view → virtual volume access granted → LDAP admin auth → audit log'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Host Access'), bMid(B2_L, B2_R, 'Admin Auth'), bMid(B3_L, B3_R, 'Audit / Logging'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Storage view'), bMid(B2_L, B2_R, 'LDAP / AD'), bMid(B3_L, B3_R, 'CLI audit log'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'WWN binding'), bMid(B2_L, B2_R, 'RBAC roles'), bMid(B3_L, B3_R, 'Syslog export'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Deny by default'), bMid(B2_L, B2_R, 'Local break-glass'), bMid(B3_L, B3_R, 'Event filter'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SAN zoning'), bMid(B2_L, B2_R, 'TLS mgmt API'), bMid(B3_L, B3_R, 'SIEM forward'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Port zoning'), bMid(B2_L, B2_R, 'Session timeout'), bMid(B3_L, B3_R, 'Login events'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Storage view review → LDAP role audit → SAN zone check → syslog review cycle'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Control', 'Mechanism', 'Standard', 'Exception', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Host access', 'Storage view', 'WWN whitelist', 'No open views', 'View audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Admin auth', 'LDAP / AD', 'Named accounts', 'Local only', 'Login log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['CLI access', 'Role-based', 'Storage admin', 'Read-only role', 'CLI audit trail'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Logging', 'Syslog/SIEM', 'All changes', '—', 'Weekly review'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: VPLEX management port on OOB network; SAN fabric for I/O; WAN port for Metro'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Storage view   = VPLEX host access control: virtual volume + initiator group + port group'))
    lines.append(txt_row('  WWN binding    = Specific host HBA WWN(s) included in storage view; unlisted WWNs denied'))
    lines.append(txt_row('  Deny by default= VPLEX presents no volumes to any host until a storage view is created'))
    lines.append(txt_row('  SAN zoning     = FC fabric zones restrict which HBAs see which VPLEX front-end ports'))
    lines.append(txt_row('  RBAC roles     = GeoSynchrony roles: Admin, Operator, Monitor (read-only)'))
    lines.append(txt_row('  Local break-glass= Local admin account on GeoSynchrony; use only when LDAP down'))
    lines.append(txt_row('  TLS mgmt API   = VPLEX management API and CLI secured with TLS; REST and SSH'))
    lines.append(txt_row('  CLI audit log  = GeoSynchrony logs all vplex-shell commands with user, time, and action'))
    lines.append(txt_row('  Event filter   = VPLEX event log filter by severity; export to syslog for SIEM correlation'))
    lines.append(txt_row('  Open view      = Storage view with all-WWN access; prohibited; every view must be explicit'))
    lines.append(txt_row('  Session timeout= Idle timeout on vplex-shell and GUI; default 30 min'))
    lines.append(txt_row('  Port group     = Collection of VPLEX I/O director ports mapped in a storage view'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-vplex-troubleshooting',
    'docs/storage/dell/vplex/troubleshooting/index.md',
    'Dell VPLEX troubleshooting — director fault, WAN loss, split-brain, detached volumes',
)
def dell_vplex_troubleshooting():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell VPLEX Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Common faults: director failure, WAN link loss, split-brain, back-end path, cache fault')))
    lines.append(R(bMid(IV_L, IV_R, 'Director fault: peer director in cluster takes I/O; replace blade; check DRAM cache')))
    lines.append(R(bMid(IV_L, IV_R, 'WAN loss (Metro): witness determines survivor; losing cluster fences volumes')))
    lines.append(R(bMid(IV_L, IV_R, 'Detached volumes: virtual volume not accessible; check back-end path and director state')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Alert fires → VPLEX CLI → director/volume state check → isolate fault → remediate → verify'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Director Issues'), bMid(B2_L, B2_R, 'Metro Issues'), bMid(B3_L, B3_R, 'Volume Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Director failed'), bMid(B2_L, B2_R, 'WAN link lost'), bMid(B3_L, B3_R, 'Volume detached'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Cache fault'), bMid(B2_L, B2_R, 'Split-brain'), bMid(B3_L, B3_R, 'Back-end path'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Port offline'), bMid(B2_L, B2_R, 'Witness loss'), bMid(B3_L, B3_R, 'Host no I/O'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Director degrad'), bMid(B2_L, B2_R, 'Fenced cluster'), bMid(B3_L, B3_R, 'Storage view'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Power fault'), bMid(B2_L, B2_R, 'Failover stuck'), bMid(B3_L, B3_R, 'Rebuild volume'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  VPLEX CLI → ls directors → ls virtual-volumes -t → check comm-links → fix root cause'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Symptom', 'First check', 'CLI command', 'Fix', 'Escalate if'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Director fail', 'Director LEDs', 'ls directors', 'Replace blade', 'Cache corrupt'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['WAN loss', 'Comm-link state', 'ls comm-links', 'Fix WAN route', 'Split-brain'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Vol detached', 'BE path state', 'ls virtual-vols', 'Fix BE path', 'Vol unrecoverable'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Split-brain', 'Witness state', 'ls witnesses', 'Restore witness', 'Manual fence req'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: director blade LEDs in chassis; FC SFP port lights; WAN IP link ping test'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Director fault = I/O or Storage director blade failure; peer director takes over in cluster'))
    lines.append(txt_row('  Cache fault    = DRAM write cache error; may require director replacement to clear'))
    lines.append(txt_row('  WAN link lost  = Metro cluster communication disrupted; both clusters wait for witness'))
    lines.append(txt_row('  Split-brain    = Both clusters operational but disconnected; witness arbitrates survivor'))
    lines.append(txt_row('  Fenced cluster = Losing Metro cluster fences its volumes; I/O stops at losing site'))
    lines.append(txt_row('  Witness loss   = Witness unreachable; Metro cluster cannot resolve split-brain safely'))
    lines.append(txt_row('  Volume detached= Virtual volume not serving I/O; check back-end path and director state'))
    lines.append(txt_row('  Back-end path  = FC path from Storage Director to array port; failure detaches volumes'))
    lines.append(txt_row('  ls directors   = Show director operational state: Online, Degraded, Faulted'))
    lines.append(txt_row('  ls comm-links  = Show WAN link state and latency between Metro clusters'))
    lines.append(txt_row('  Manual fence   = Force one cluster to fence when witness is also unreachable'))
    lines.append(txt_row('  Rebuild volume = After BE path recovery, VPLEX re-attaches volume and syncs distributed state'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Dell CloudIQ sub-pages ────────────────────────────────────────────────────

@kb_diagram(
    'dell-cloudiq-arch',
    'docs/storage/dell/cloudiq/architecture/index.md',
    'Dell CloudIQ architecture overview — cloud-based AIOps platform for Dell storage',
)
def dell_cloudiq_arch():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ Architecture'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ: SaaS AIOps platform collecting telemetry from Dell storage and servers')))
    lines.append(R(bMid(IV_L, IV_R, 'Telemetry flows from Secure Connect Gateway (SCG) to Dell cloud backend')))
    lines.append(R(bMid(IV_L, IV_R, 'Provides capacity planning, performance analytics, and predictive health scoring')))
    lines.append(R(bMid(IV_L, IV_R, 'No on-premises compute required; SCG is the only local component')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Storage arrays → SCG collects telemetry → CloudIQ cloud → dashboards + AI insights'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Data Collection'), bMid(B2_L, B2_R, 'Cloud Platform'), bMid(B3_L, B3_R, 'Capabilities'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCG on-prem'), bMid(B2_L, B2_R, 'Dell SaaS cloud'), bMid(B3_L, B3_R, 'Health scoring'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'REST API polling'), bMid(B2_L, B2_R, 'ML/AI engine'), bMid(B3_L, B3_R, 'Capacity predict'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Event forwarding'), bMid(B2_L, B2_R, 'Telemetry ingest'), bMid(B3_L, B3_R, 'Perf analytics'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Alert aggregation'), bMid(B2_L, B2_R, 'Multi-tenant'), bMid(B3_L, B3_R, 'Anomaly detect'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Secure outbound'), bMid(B2_L, B2_R, 'API gateway'), bMid(B3_L, B3_R, 'Recommendations'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  SCG sends telemetry outbound HTTPS 443 → CloudIQ ingests → AI scoring → UI alerts'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Layer', 'Component', 'Function', 'Protocol', 'Notes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Edge', 'SCG VM', 'Telemetry relay', 'HTTPS 443', 'Outbound only'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Transport', 'Internet/proxy', 'Secure tunnel', 'TLS 1.2+', 'Proxy supported'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Cloud', 'CloudIQ SaaS', 'AI analytics', 'REST API', 'Dell-hosted'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Access', 'Web browser', 'Dashboards', 'HTTPS', 'SSO/MFA'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SCG VM runs on ESXi or Hyper-V on-premises; arrays connect via management IP'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  CloudIQ      = Dell SaaS AIOps platform; receives telemetry via SCG; provides AI-driven insights'))
    lines.append(txt_row('  SCG          = Secure Connect Gateway; on-premises VM relaying telemetry to Dell cloud'))
    lines.append(txt_row('  Health score = AI-generated 0-100 score per system; green/yellow/red risk bands'))
    lines.append(txt_row('  Capacity IQ  = CloudIQ module projecting when storage will fill based on growth trends'))
    lines.append(txt_row('  Performance  = CloudIQ latency/IOPS/bandwidth dashboards per workload over time'))
    lines.append(txt_row('  Anomaly      = ML baseline comparison; alerts when metric deviates from normal pattern'))
    lines.append(txt_row('  Telemetry    = Performance, capacity, configuration, and event data sent every 5 minutes'))
    lines.append(txt_row('  Multi-tenant = Single CloudIQ login spans all Dell storage systems across sites'))
    lines.append(txt_row('  AI engine    = Dell ML models trained on fleet-wide data; predict failures before they occur'))
    lines.append(txt_row('  Outbound only= No inbound connections; SCG initiates all communication to CloudIQ'))
    lines.append(txt_row('  Proxy support= SCG can route telemetry through HTTP/HTTPS proxy if direct internet blocked'))
    lines.append(txt_row('  SaaS         = Software-as-a-Service; Dell manages platform updates; no admin overhead'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-cloudiq-arch-how',
    'docs/storage/dell/cloudiq/architecture/how-it-works/index.md',
    'Dell CloudIQ how it works — SCG collection, telemetry pipeline, AI analysis',
)
def dell_cloudiq_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ — How It Works'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'SCG polls storage REST APIs every 5 min; forwards telemetry to CloudIQ cloud')))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ ML engine baselines each system; scores health; fires alerts on anomalies')))
    lines.append(R(bMid(IV_L, IV_R, 'User views insights in web UI; recommendations trigger remediation workflows')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Storage → SCG polls → HTTPS telemetry stream → CloudIQ ingest → AI score → UI alert'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'On-Premises Collection'), bMid(B2_L, B2_R, 'Cloud Processing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCG VM polls storage REST APIs'), bMid(B2_L, B2_R, 'CloudIQ ingests telemetry stream'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Collects perf, capacity, events'), bMid(B2_L, B2_R, 'ML baselines each metric per array'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Compresses and batches data'), bMid(B2_L, B2_R, 'Health score computed 0–100'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'TLS-encrypted outbound HTTPS'), bMid(B2_L, B2_R, 'Anomaly detection fires alerts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No inbound ports required'), bMid(B2_L, B2_R, 'Recommendations generated'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Proxy and CA cert configurable'), bMid(B2_L, B2_R, 'Dashboards updated in UI'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  SCG data collection interval: 5 min for telemetry; 24 h for full configuration snapshot'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Step 1 — SCG discovers arrays via management IP + credentials (added in SCG UI)')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 2 — SCG polls array REST API: metrics, alerts, capacity, config inventory')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 3 — Telemetry batched and forwarded outbound HTTPS to CloudIQ ingest endpoint')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 4 — CloudIQ ML scores health; capacity IQ projects runway; anomalies alert')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 5 — Admin views dashboards; exports reports; acts on recommendations')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SCG VM (2 vCPU, 8 GB RAM, 100 GB disk) on ESXi or Hyper-V; outbound 443'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SCG polling   = SCG REST client queries each storage system management API every 5 min'))
    lines.append(txt_row('  Telemetry batch= Metrics compressed and batched before forwarding to reduce bandwidth'))
    lines.append(txt_row('  ML baseline   = CloudIQ learns normal performance/capacity pattern per system over 7+ days'))
    lines.append(txt_row('  Anomaly alert = Deviation beyond ML confidence band triggers email/webhook notification'))
    lines.append(txt_row('  Configuration snapshot= Full inventory of volumes, pools, hosts sent every 24 hours'))
    lines.append(txt_row('  Runway        = Capacity IQ prediction: days until storage pool reaches defined threshold'))
    lines.append(txt_row('  Health score  = Composite AI score; red <70, yellow 70–89, green 90–100'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-cloudiq-arch-int',
    'docs/storage/dell/cloudiq/architecture/integrations/index.md',
    'Dell CloudIQ integrations — ITSM, email alerts, REST API, ServiceNow, Slack',
)
def dell_cloudiq_arch_int():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ integrates via REST API, webhooks, email, ITSM connectors, and SSO')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert webhooks post to ServiceNow, Slack, or any HTTP endpoint on threshold breach')))
    lines.append(R(bMid(IV_L, IV_R, 'REST API exposes asset inventory, health scores, and metrics for custom dashboards')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  CloudIQ alert → webhook → ITSM ticket or Slack notification; REST API → BI/CMDB'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Alerting'), bMid(B2_L, B2_R, 'API / Data'), bMid(B3_L, B3_R, 'Identity'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Email alerts'), bMid(B2_L, B2_R, 'CloudIQ REST API'), bMid(B3_L, B3_R, 'SSO (SAML 2.0)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Webhook HTTP/S'), bMid(B2_L, B2_R, 'Asset inventory'), bMid(B3_L, B3_R, 'Dell account'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ServiceNow conn.'), bMid(B2_L, B2_R, 'Metrics export'), bMid(B3_L, B3_R, 'RBAC roles'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Slack webhook'), bMid(B2_L, B2_R, 'Report export'), bMid(B3_L, B3_R, 'MFA supported'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PagerDuty'), bMid(B2_L, B2_R, 'CSV/JSON'), bMid(B3_L, B3_R, 'Org grouping'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  API token from CloudIQ settings → REST calls for health/capacity → CMDB or BI ingest'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Integration', 'Method', 'Trigger', 'Use case', 'Auth'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['ServiceNow', 'Webhook', 'Alert fires', 'Auto ticket', 'API key'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Slack', 'Webhook', 'Alert fires', 'ChatOps notify', 'Webhook URL'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Custom BI', 'REST API', 'Scheduled', 'Dashboards', 'Bearer token'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['CMDB', 'REST API', 'On-demand', 'Asset sync', 'Bearer token'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Webhook        = HTTP POST sent by CloudIQ to external URL when alert condition met'))
    lines.append(txt_row('  REST API       = CloudIQ public API; authenticated with OAuth bearer token; GET/POST'))
    lines.append(txt_row('  SSO            = SAML 2.0 identity federation; Dell accounts or corp IdP supported'))
    lines.append(txt_row('  ServiceNow     = CloudIQ native connector creates incidents in ServiceNow on alert'))
    lines.append(txt_row('  Report export  = PDF/CSV capacity and health reports downloadable or emailed on schedule'))
    lines.append(txt_row('  Org grouping   = Group systems by site/customer in CloudIQ for MSP multi-tenancy'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-cloudiq-ops-backup',
    'docs/storage/dell/cloudiq/operations/backup-restore/index.md',
    'Dell CloudIQ backup/restore — SaaS config backup, SCG settings export',
)
def dell_cloudiq_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ Backup and Restore'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ SaaS platform backed up by Dell; SCG configuration exported manually')))
    lines.append(R(bMid(IV_L, IV_R, 'SCG VM snapshot or OVA export preserves system credentials and settings')))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ telemetry data retained in Dell cloud for 90 days by default')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  SCG VM snapshot → export settings → restore to new SCG VM → re-register in CloudIQ'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCG Backup'), bMid(B2_L, B2_R, 'CloudIQ SaaS'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VM snapshot (ESXi/Hyper-V)'), bMid(B2_L, B2_R, 'Dell manages SaaS backup'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Settings export via SCG UI'), bMid(B2_L, B2_R, 'Historical data: 90 days'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'System credential backup'), bMid(B2_L, B2_R, 'Config replicated geo'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Certificate backup'), bMid(B2_L, B2_R, 'No customer action needed'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'OVA re-deploy for DR'), bMid(B2_L, B2_R, 'Org data persists after SCG loss'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  SCG restore: deploy new OVA → import settings → re-register with CloudIQ org → verify'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Restore procedure: 1) Deploy fresh SCG OVA on VMware/Hyper-V')))
    lines.append(R(bMid(IV_L, IV_R, '2) Import exported settings file via SCG admin UI')))
    lines.append(R(bMid(IV_L, IV_R, '3) Re-register SCG with CloudIQ organisation token')))
    lines.append(R(bMid(IV_L, IV_R, '4) Verify storage systems reconnect and telemetry resumes')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SCG settings export = JSON export of all system credentials, proxy config, and certs'))
    lines.append(txt_row('  Org token          = CloudIQ organisation registration token; links SCG to correct tenant'))
    lines.append(txt_row('  90-day retention   = CloudIQ keeps 90 days of telemetry; older data rolled off automatically'))
    lines.append(txt_row('  SaaS backup        = Dell guarantees CloudIQ platform HA and geo-redundant backup'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-cloudiq-ops-cli',
    'docs/storage/dell/cloudiq/operations/cli-reference/index.md',
    'Dell CloudIQ CLI reference — SCG CLI commands, REST API endpoints',
)
def dell_cloudiq_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ CLI Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ management via SCG CLI (SSH to SCG VM) and CloudIQ REST API')))
    lines.append(R(bMid(IV_L, IV_R, 'SCG CLI: system status, device list, connectivity test, log collection')))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ REST API: retrieve assets, health scores, metrics, alert history')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCG Status'), bMid(B2_L, B2_R, 'SCG Device Mgmt'), bMid(B3_L, B3_R, 'CloudIQ API'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'scg status'), bMid(B2_L, B2_R, 'scg device list'), bMid(B3_L, B3_R, 'GET /v1/assets'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'scg connectivity'), bMid(B2_L, B2_R, 'scg device add'), bMid(B3_L, B3_R, 'GET /v1/health'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'scg log collect'), bMid(B2_L, B2_R, 'scg device remove'), bMid(B3_L, B3_R, 'GET /v1/metrics'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'scg version'), bMid(B2_L, B2_R, 'scg device test'), bMid(B3_L, B3_R, 'GET /v1/alerts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'scg upgrade'), bMid(B2_L, B2_R, 'scg device show'), bMid(B3_L, B3_R, 'POST /v1/reports'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Common workflows: check status → list devices → test connectivity → collect logs'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'scg status                — show SCG service state, version, registered devices')))
    lines.append(R(bMid(IV_L, IV_R, 'scg connectivity --test   — verify outbound HTTPS to CloudIQ endpoints')))
    lines.append(R(bMid(IV_L, IV_R, 'scg device list           — show all registered storage systems and poll state')))
    lines.append(R(bMid(IV_L, IV_R, 'scg log collect           — bundle SCG logs for support; output to /tmp')))
    lines.append(R(bMid(IV_L, IV_R, 'curl -H "Authorization: Bearer $TOKEN" https://cloudiq.dell.com/v1/assets')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SCG CLI      = SSH to SCG VM (admin user); menu-driven or direct scg commands'))
    lines.append(txt_row('  Bearer token = OAuth 2.0 token from CloudIQ API key; passed in Authorization header'))
    lines.append(txt_row('  scg device test= Validates REST API credentials and connectivity for a registered system'))
    lines.append(txt_row('  /v1/assets   = CloudIQ REST endpoint: returns all storage assets with attributes'))
    lines.append(txt_row('  /v1/health   = CloudIQ REST endpoint: returns health scores for all systems'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-cloudiq-ops-health',
    'docs/storage/dell/cloudiq/operations/health-checks/index.md',
    'Dell CloudIQ health checks — verify telemetry, SCG status, alert review',
)
def dell_cloudiq_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ Health Checks'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Verify CloudIQ and SCG health: telemetry currency, SCG connectivity, alert review')))
    lines.append(R(bMid(IV_L, IV_R, 'Check last telemetry timestamp per system; red/yellow health scores; open alerts')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCG Health'), bMid(B2_L, B2_R, 'CloudIQ Health'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCG service status: running'), bMid(B2_L, B2_R, 'All systems: last seen < 15 min'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Outbound connectivity OK'), bMid(B2_L, B2_R, 'Health scores: no red systems'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'All devices: poll state green'), bMid(B2_L, B2_R, 'Active alerts reviewed'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCG version current'), bMid(B2_L, B2_R, 'Capacity runway > 30 days'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Certificate validity'), bMid(B2_L, B2_R, 'No stale/disconnected systems'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Check', 'Where', 'Pass criteria', 'Fail action', 'Frequency'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['SCG status', 'SCG CLI', 'All green', 'Restart SCG', 'Daily'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Telemetry age', 'CloudIQ UI', '< 15 min', 'Test SCG conn', 'Daily'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Health scores', 'CloudIQ dash', 'All green', 'Review alerts', 'Daily'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Capacity IQ', 'CloudIQ dash', '>30 days', 'Expand pools', 'Weekly'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Telemetry age  = Time since last successful telemetry upload per system; > 15 min = gap'))
    lines.append(txt_row('  Stale system   = System in CloudIQ with no telemetry for > 1 hour; SCG poll failure'))
    lines.append(txt_row('  Capacity runway= Days until storage pool reaches fill threshold based on growth rate'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-cloudiq-ops-scripts',
    'docs/storage/dell/cloudiq/operations/scripts/index.md',
    'Dell CloudIQ scripts — REST API query scripts, report automation, asset export',
)
def dell_cloudiq_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ Scripts'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Automate CloudIQ operations with REST API scripts: asset queries, health reports')))
    lines.append(R(bMid(IV_L, IV_R, 'Use Bearer token authentication; base URL: https://cloudiq.dell.com/cloudiq/rest')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, '# Get Bearer token')))
    lines.append(R(bMid(IV_L, IV_R, 'TOKEN=$(curl -s -X POST https://cloudiq.dell.com/auth/token \\')))
    lines.append(R(bMid(IV_L, IV_R, '  -d "grant_type=client_credentials&client_id=$ID&client_secret=$SECRET" \\')))
    lines.append(R(bMid(IV_L, IV_R, '  | jq -r .access_token)')))
    lines.append(R(bMid(IV_L, IV_R, '')))
    lines.append(R(bMid(IV_L, IV_R, '# List all storage systems and health scores')))
    lines.append(R(bMid(IV_L, IV_R, 'curl -s -H "Authorization: Bearer $TOKEN" \\')))
    lines.append(R(bMid(IV_L, IV_R, '  https://cloudiq.dell.com/cloudiq/rest/v1/storage-systems \\')))
    lines.append(R(bMid(IV_L, IV_R, '  | jq ".results[] | {name, health_score, capacity_used_pct}"')))
    lines.append(R(bMid(IV_L, IV_R, '')))
    lines.append(R(bMid(IV_L, IV_R, '# Export capacity report to CSV')))
    lines.append(R(bMid(IV_L, IV_R, 'curl -s -H "Authorization: Bearer $TOKEN" \\')))
    lines.append(R(bMid(IV_L, IV_R, '  "https://cloudiq.dell.com/cloudiq/rest/v1/metrics?type=capacity" \\')))
    lines.append(R(bMid(IV_L, IV_R, '  | jq -r ".results[] | [.system,.date,.used_gb,.total_gb] | @csv"')))
    lines.append(R(bMid(IV_L, IV_R, '')))
    lines.append(R(bMid(IV_L, IV_R, '# SCG: test all device connections')))
    lines.append(R(bMid(IV_L, IV_R, 'ssh admin@<SCG_IP> "scg device list --format json | jq .[].status"')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  client_credentials = OAuth 2.0 flow for API automation; client ID + secret from CloudIQ UI'))
    lines.append(txt_row('  access_token       = Short-lived JWT bearer token; typically 1-hour expiry; refresh as needed'))
    lines.append(txt_row('  health_score       = Numeric 0-100 AI score per system in API response'))
    lines.append(txt_row('  /v1/metrics        = Telemetry endpoint: query capacity, performance, alerts by system'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-cloudiq-ts-issues',
    'docs/storage/dell/cloudiq/troubleshooting/common-issues/index.md',
    'Dell CloudIQ common issues — stale telemetry, SCG offline, missing systems',
)
def dell_cloudiq_ts_issues():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ Common Issues'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Top issues: SCG offline, stale/missing telemetry, system not appearing in CloudIQ')))
    lines.append(R(bMid(IV_L, IV_R, 'Most problems root-cause to SCG connectivity loss or credential expiry on device')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCG Issues'), bMid(B2_L, B2_R, 'Telemetry Issues'), bMid(B3_L, B3_R, 'CloudIQ UI Issues'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCG service down'), bMid(B2_L, B2_R, 'Stale data > 1h'), bMid(B3_L, B3_R, 'System missing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Firewall blocked'), bMid(B2_L, B2_R, 'Device poll fail'), bMid(B3_L, B3_R, 'Wrong health score'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Proxy auth fail'), bMid(B2_L, B2_R, 'Cred expired'), bMid(B3_L, B3_R, 'Alert not firing'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SSL cert error'), bMid(B2_L, B2_R, 'API unreachable'), bMid(B3_L, B3_R, 'Login fails SSO'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCG version old'), bMid(B2_L, B2_R, 'Incomplete data'), bMid(B3_L, B3_R, 'Report blank'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Problem', 'Likely cause', 'First check', 'Fix', 'Verify'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Stale telemetry', 'SCG offline', 'scg status', 'Restart SCG', 'Check UI age'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['System missing', 'Not registered', 'scg device list', 'Add device', 'Appears in UI'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Poll fail', 'Cred/firewall', 'scg device test', 'Fix creds/FW', 'Poll green'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['SCG offline', 'VM powered off', 'vSphere check', 'Power on VM', 'scg status OK'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Stale telemetry = Last-seen timestamp > 1 hour; data gap; UI shows last known state'))
    lines.append(txt_row('  Device poll fail= SCG cannot reach storage REST API; check IP, credentials, and port 443'))
    lines.append(txt_row('  Proxy auth fail = SCG proxy requires authentication; configure proxy creds in SCG settings'))
    lines.append(txt_row('  SSL cert error  = SCG cannot validate CloudIQ endpoint cert; add CA to SCG trust store'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-cloudiq-ts-diag',
    'docs/storage/dell/cloudiq/troubleshooting/diagnostics/index.md',
    'Dell CloudIQ diagnostics — SCG log collection, connectivity test, API debug',
)
def dell_cloudiq_ts_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ Diagnostics'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnose CloudIQ issues with SCG CLI commands, log bundles, and API connectivity')))
    lines.append(R(bMid(IV_L, IV_R, 'scg connectivity --test: validates HTTPS outbound to CloudIQ endpoints')))
    lines.append(R(bMid(IV_L, IV_R, 'scg log collect: bundles all SCG logs for Dell support case upload')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, '# Step 1 — Check SCG service status')))
    lines.append(R(bMid(IV_L, IV_R, 'ssh admin@<SCG_IP>')))
    lines.append(R(bMid(IV_L, IV_R, 'scg status')))
    lines.append(R(bMid(IV_L, IV_R, '')))
    lines.append(R(bMid(IV_L, IV_R, '# Step 2 — Test outbound connectivity')))
    lines.append(R(bMid(IV_L, IV_R, 'scg connectivity --test')))
    lines.append(R(bMid(IV_L, IV_R, '')))
    lines.append(R(bMid(IV_L, IV_R, '# Step 3 — Test specific device connection')))
    lines.append(R(bMid(IV_L, IV_R, 'scg device test --id <device_id>')))
    lines.append(R(bMid(IV_L, IV_R, '')))
    lines.append(R(bMid(IV_L, IV_R, '# Step 4 — Collect logs for support')))
    lines.append(R(bMid(IV_L, IV_R, 'scg log collect --output /tmp/scg_logs.tar.gz')))
    lines.append(R(bMid(IV_L, IV_R, '')))
    lines.append(R(bMid(IV_L, IV_R, '# Step 5 — View SCG system log')))
    lines.append(R(bMid(IV_L, IV_R, 'tail -f /var/log/scg/scg.log')))
    lines.append(R(bMid(IV_L, IV_R, '')))
    lines.append(R(bMid(IV_L, IV_R, '# Step 6 — Check DNS resolution for CloudIQ endpoints')))
    lines.append(R(bMid(IV_L, IV_R, 'nslookup cloudiq.dell.com')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  scg connectivity = Tests TCP/HTTPS reachability to all required CloudIQ cloud endpoints'))
    lines.append(txt_row('  scg device test  = Authenticates to specific storage system and reports poll success/fail'))
    lines.append(txt_row('  scg log collect  = Bundles SCG application logs, config (sanitised), and diagnostics'))
    lines.append(txt_row('  /var/log/scg     = SCG application log directory; scg.log for main service events'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-cloudiq-ts-esc',
    'docs/storage/dell/cloudiq/troubleshooting/escalation/index.md',
    'Dell CloudIQ escalation — support case, log bundle, CloudIQ SR process',
)
def dell_cloudiq_ts_esc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []

    lines.append(title_border(W2, 'Dell CloudIQ Escalation'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Escalate CloudIQ issues to Dell Support with SR; attach SCG log bundle and API trace')))
    lines.append(R(bMid(IV_L, IV_R, 'SCG issues: collect scg logs, note SCG version, capture connectivity test output')))
    lines.append(R(bMid(IV_L, IV_R, 'CloudIQ data issues: note system name, time window, expected vs actual values')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Before Escalating'), bMid(B2_L, B2_R, 'Escalation Steps'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCG version (scg version)'), bMid(B2_L, B2_R, 'Open SR at support.dell.com'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Connectivity test output'), bMid(B2_L, B2_R, 'Attach SCG log bundle'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SCG log bundle collected'), bMid(B2_L, B2_R, 'Note affected system IDs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Affected system name + ID'), bMid(B2_L, B2_R, 'CloudIQ org ID from UI'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Time window of issue'), bMid(B2_L, B2_R, 'Request CloudIQ backend check'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SR             = Service Request; Dell support case opened at support.dell.com'))
    lines.append(txt_row('  CloudIQ org ID = Unique identifier for your CloudIQ tenant; visible in Settings > Org'))
    lines.append(txt_row('  Backend check  = Dell CloudIQ SRE team investigates ingest pipeline for missing data'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── Dell COD sub-pages ────────────────────────────────────────────────────────

@kb_diagram(
    'dell-cod-arch',
    'docs/storage/dell/cod/architecture/index.md',
    'Dell COD architecture overview — Capacity On Demand licensing model',
)
def dell_cod_arch():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell COD Architecture'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'COD (Capacity On Demand): pre-installed storage capacity unlocked via license key')))
    lines.append(R(bMid(IV_L, IV_R, 'Hardware installed at factory; additional capacity activated instantly with no I/O impact')))
    lines.append(R(bMid(IV_L, IV_R, 'Eliminates future expansion downtime; pay as capacity is needed')))
    lines.append(R(bMid(IV_L, IV_R, 'Supported on PowerStore, PowerMax, Unity, PowerScale product families')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Array ships with reserved capacity → license key purchased → capacity unlocked live'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Pre-installed HW'), bMid(B2_L, B2_R, 'License Activation'), bMid(B3_L, B3_R, 'Benefits'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Drives installed'), bMid(B2_L, B2_R, 'License key file'), bMid(B3_L, B3_R, 'No downtime'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Logically locked'), bMid(B2_L, B2_R, 'Applied via GUI'), bMid(B3_L, B3_R, 'Instant expand'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'No config change'), bMid(B2_L, B2_R, 'or REST API'), bMid(B3_L, B3_R, 'Predictable cost'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Physical at install'), bMid(B2_L, B2_R, 'Immediate unlock'), bMid(B3_L, B3_R, 'No truck roll'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Validated at ship'), bMid(B2_L, B2_R, 'Online activation'), bMid(B3_L, B3_R, 'Capacity buffer'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Product', 'COD type', 'Activation', 'Granularity', 'Max units'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['PowerStore', 'Capacity COD', 'License key', 'per TB', 'Varies'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['PowerMax', 'COD/FOD', 'License key', 'per TB', 'Model dep'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Unity XT', 'COD drive', 'License key', 'per drive', 'Per chassis'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['PowerScale', 'Node license', 'License key', 'per node', 'Per cluster'])))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: drives/nodes present in hardware; logically invisible until license applied'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  COD          = Capacity On Demand; pre-installed hardware unlocked via license key'))
    lines.append(txt_row('  FOD          = Feature On Demand; software feature (e.g. protocol, function) unlocked similarly'))
    lines.append(txt_row('  License key  = Cryptographic string from Dell licensing portal; applied to specific array'))
    lines.append(txt_row('  Instant unlock= Capacity available within seconds of applying license; no reboot required'))
    lines.append(txt_row('  Capacity buffer= Buying COD upfront avoids lead time delays when capacity is urgently needed'))
    lines.append(txt_row('  Truck roll   = Physical site visit to install hardware; COD eliminates this for expansion'))
    lines.append(txt_row('  Online activation= COD licensed against specific array serial number; tied to that system'))
    lines.append(txt_row('  Logically locked= Drive/node present in hardware inventory but excluded from pool until unlocked'))
    lines.append(txt_row('  Validated at ship= Dell verifies all COD hardware functional before shipment'))
    lines.append(txt_row('  No I/O impact= COD activation does not disrupt running workloads; fully online operation'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-cod-arch-design',
    'docs/storage/dell/cod/architecture/design-standards/index.md',
    'Dell COD design standards — purchase planning, activation workflow, documentation',
)
def dell_cod_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell COD Design Standards'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'COD design: order COD with initial array purchase; size for 18-month growth horizon')))
    lines.append(R(bMid(IV_L, IV_R, 'Document licensed vs unlocked capacity; track activation dates and remaining COD')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Ordering Standards'), bMid(B2_L, B2_R, 'Operational Standards'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Order with initial purchase'), bMid(B2_L, B2_R, 'Track COD in CMDB/asset register'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Size for 18-month growth'), bMid(B2_L, B2_R, 'Store license keys in vault'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'COD up to max chassis cap'), bMid(B2_L, B2_R, 'Review remaining COD monthly'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Document at purchase'), bMid(B2_L, B2_R, 'Activate via change ticket'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Verify hardware at delivery'), bMid(B2_L, B2_R, 'Alert at 20% COD remaining'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Standard', 'Requirement', 'Reason', 'Owner', 'Review'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['CMDB track', 'All COD units', 'Capacity mgmt', 'Storage team', 'Monthly'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Key storage', 'Password vault', 'License security', 'Storage team', 'Annual'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Activation CHG', 'Change ticket', 'Auditability', 'Change mgr', 'Per event'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['30-day alert', '20% COD left', 'Avoid shortage', 'Monitoring', 'Automated'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  18-month horizon = Plan COD to cover growth without frequent re-orders or lead time risk'))
    lines.append(txt_row('  CMDB tracking    = Record array serial, COD TB ordered, TB activated, TB remaining per system'))
    lines.append(txt_row('  Vault            = Secure credential/key store (CyberArk or similar) for license keys'))
    lines.append(txt_row('  Change ticket    = COD activation via formal change management; document before/after capacity'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-cod-arch-how',
    'docs/storage/dell/cod/architecture/how-it-works/index.md',
    'Dell COD how it works — license key application, capacity unlock steps',
)
def dell_cod_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    lines = []

    lines.append(title_border(W2, 'Dell COD — How It Works'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Hardware ships with locked capacity; Dell licensing portal generates key for array serial')))
    lines.append(R(bMid(IV_L, IV_R, 'Apply license key via array management GUI or REST API; capacity available instantly')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Step 1 — Verify locked capacity visible in array: check available unlicensed drives/TB')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 2 — Log in to Dell Licensing Portal: licensing.dell.com')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 3 — Generate COD license key for specific array serial number')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 4 — Apply key in array management UI: Settings > Licenses > Upload')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 5 — Verify new capacity appears in available pool (no reboot needed)')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 6 — Update CMDB: record activation date, TB unlocked, remaining COD')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 7 — Close change ticket with before/after capacity screenshot')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'PowerStore REST activation:')))
    lines.append(R(bMid(IV_L, IV_R, 'POST /api/rest/license  --data {"key": "<license_string>"}')))
    lines.append(R(bMid(IV_L, IV_R, '')))
    lines.append(R(bMid(IV_L, IV_R, 'Verify on PowerStore:')))
    lines.append(R(bMid(IV_L, IV_R, 'GET /api/rest/capacity  → check used_gb and total_gb change')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Locked capacity  = Drives/nodes installed but not accessible; shown as "reserved" in array'))
    lines.append(txt_row('  Licensing portal = Dell web portal for generating COD/FOD keys per array serial number'))
    lines.append(txt_row('  Key binding      = COD key cryptographically tied to array serial; cannot be reused'))
    lines.append(txt_row('  Instant unlock   = Capacity joins pool within seconds; no volume migration or downtime'))
    lines.append(txt_row('  Before/after     = Screenshot capacity before and after activation; attach to change ticket'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-cod-ops-cli',
    'docs/storage/dell/cod/operations/cli-reference/index.md',
    'Dell COD CLI reference — license commands per product (PowerStore, Unity, PowerMax)',
)
def dell_cod_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []

    lines.append(title_border(W2, 'Dell COD CLI Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'COD license CLI commands vary by product family: PowerStore, Unity, PowerMax')))
    lines.append(R(bMid(IV_L, IV_R, 'All products support GUI activation; CLI/REST provides automation path')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'PowerStore'), bMid(B2_L, B2_R, 'Unity XT'), bMid(B3_L, B3_R, 'PowerMax'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────'), bMid(B2_L, B2_R, '─────────────────'), bMid(B3_L, B3_R, '─────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'pstore> license list'), bMid(B2_L, B2_R, 'uemcli license -list'), bMid(B3_L, B3_R, 'symlic list'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'pstore> license add'), bMid(B2_L, B2_R, 'uemcli license -upload'), bMid(B3_L, B3_R, 'symlic install'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'REST: POST /license'), bMid(B2_L, B2_R, 'REST: POST /license'), bMid(B3_L, B3_R, 'Solutions Enabler'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'REST: GET /capacity'), bMid(B2_L, B2_R, 'GUI: Settings'), bMid(B3_L, B3_R, 'Unisphere GUI'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'GUI: Settings > Lic'), bMid(B2_L, B2_R, '>  Licenses'), bMid(B3_L, B3_R, 'Solutions Enblr'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, '# PowerStore REST — list licenses')))
    lines.append(R(bMid(IV_L, IV_R, 'curl -sk -u admin:$PASS https://<ps>/api/rest/license | jq .[].name')))
    lines.append(R(bMid(IV_L, IV_R, '')))
    lines.append(R(bMid(IV_L, IV_R, '# Unity uemcli — list licenses')))
    lines.append(R(bMid(IV_L, IV_R, 'uemcli -d <unity_ip> -u admin -p $PASS /license show')))
    lines.append(R(bMid(IV_L, IV_R, '')))
    lines.append(R(bMid(IV_L, IV_R, '# PowerMax Solutions Enabler — list licenses')))
    lines.append(R(bMid(IV_L, IV_R, 'symlic -sid <SID> list')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  pstore CLI     = PowerStore management CLI; access via SSH or embedded shell'))
    lines.append(txt_row('  uemcli         = Unisphere for Unity CLI; installed on mgmt workstation or run from Unity'))
    lines.append(txt_row('  symlic         = Solutions Enabler command for PowerMax license management'))
    lines.append(txt_row('  Solutions Enabler= Dell software toolkit for PowerMax management automation'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-cod-ops-health',
    'docs/storage/dell/cod/operations/health-checks/index.md',
    'Dell COD health checks — verify remaining COD, alert thresholds, license validity',
)
def dell_cod_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell COD Health Checks'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Monthly COD health check: verify remaining unlocked capacity, plan next activation')))
    lines.append(R(bMid(IV_L, IV_R, 'Alert when COD remaining < 20%; track activation history in CMDB')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'What to Check'), bMid(B2_L, B2_R, 'Pass Criteria'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'COD remaining per array'), bMid(B2_L, B2_R, '> 20% of purchased COD available'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'License validity'), bMid(B2_L, B2_R, 'All licenses valid, no expiry'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CMDB currency'), bMid(B2_L, B2_R, 'CMDB matches array license state'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key store entry'), bMid(B2_L, B2_R, 'All keys stored in vault'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Growth projection'), bMid(B2_L, B2_R, '> 90 days runway with current COD'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Check', 'Frequency', 'Tool', 'Alert threshold', 'Action'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['COD remaining', 'Monthly', 'CMDB/array', '< 20%', 'Order more COD'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Growth rate', 'Monthly', 'CloudIQ', '< 90 days', 'Activate COD'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['License valid', 'Quarterly', 'Array GUI', 'Any invalid', 'Re-issue key'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['CMDB sync', 'Monthly', 'Manual', 'Mismatch', 'Update CMDB'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  COD remaining = Total COD purchased minus COD already activated; stored in CMDB'))
    lines.append(txt_row('  Growth rate   = Monthly capacity consumption rate; used to project activation trigger date'))
    lines.append(txt_row('  90-day runway = If current rate consumes remaining COD in < 90 days, activate more now'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-cod-ops-install',
    'docs/storage/dell/cod/operations/install-upgrade/index.md',
    'Dell COD install/upgrade — new array COD configuration, license activation steps',
)
def dell_cod_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    lines = []

    lines.append(title_border(W2, 'Dell COD Install / Upgrade'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'COD install: order COD with array; verify hardware at delivery; register license keys')))
    lines.append(R(bMid(IV_L, IV_R, 'COD upgrade: purchase additional COD for existing array; apply keys via licensing portal')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'New array with COD:')))
    lines.append(R(bMid(IV_L, IV_R, '1. Verify COD hardware visible in array management (locked drives/nodes listed)')))
    lines.append(R(bMid(IV_L, IV_R, '2. Log in to Dell Licensing Portal; find array by serial number')))
    lines.append(R(bMid(IV_L, IV_R, '3. Download COD license key file')))
    lines.append(R(bMid(IV_L, IV_R, '4. Store key in password vault before applying')))
    lines.append(R(bMid(IV_L, IV_R, '5. Apply via array Settings > Licenses or REST API')))
    lines.append(R(bMid(IV_L, IV_R, '6. Confirm unlocked capacity appears in pool')))
    lines.append(R(bMid(IV_L, IV_R, '7. Update CMDB: total COD, activated, remaining')))
    lines.append(R(bMid(IV_L, IV_R, '')))
    lines.append(R(bMid(IV_L, IV_R, 'Upgrading existing COD:')))
    lines.append(R(bMid(IV_L, IV_R, '1. Purchase additional COD through Dell account team')))
    lines.append(R(bMid(IV_L, IV_R, '2. Dell issues updated key for array serial')))
    lines.append(R(bMid(IV_L, IV_R, '3. Apply new key; previous activations remain active')))
    lines.append(R(bMid(IV_L, IV_R, '4. Update CMDB with new COD total')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Dell Licensing Portal = licensing.dell.com; manage COD/FOD keys per serial number'))
    lines.append(txt_row('  Updated key           = New COD key includes all previous + new units; apply to replace old'))
    lines.append(txt_row('  Locked drives visible = Array shows reserved drives in inventory before COD applied'))
    lines.append(txt_row('  CMDB update           = Record activation date, TB added, cumulative totals per array'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-cod-ops-scripts',
    'docs/storage/dell/cod/operations/scripts/index.md',
    'Dell COD scripts — license status query, COD remaining report, activation automation',
)
def dell_cod_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    lines = []

    lines.append(title_border(W2, 'Dell COD Scripts'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Scripts to query COD status across products and generate remaining-capacity reports')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, '# PowerStore — list license capacity')))
    lines.append(R(bMid(IV_L, IV_R, 'curl -sk -u admin:$PASS https://<ps>/api/rest/license \\')))
    lines.append(R(bMid(IV_L, IV_R, '  | jq ".[] | {name: .name, is_evaluation: .is_evaluation}"')))
    lines.append(R(bMid(IV_L, IV_R, '')))
    lines.append(R(bMid(IV_L, IV_R, '# PowerStore — check capacity after COD activation')))
    lines.append(R(bMid(IV_L, IV_R, 'curl -sk -u admin:$PASS https://<ps>/api/rest/cluster \\')))
    lines.append(R(bMid(IV_L, IV_R, '  | jq ".[0] | {total_raw_capacity, usable_raw_capacity}"')))
    lines.append(R(bMid(IV_L, IV_R, '')))
    lines.append(R(bMid(IV_L, IV_R, '# Unity — list license status via uemcli')))
    lines.append(R(bMid(IV_L, IV_R, 'uemcli -d <unity> -u admin -p $PASS /license show -output csv')))
    lines.append(R(bMid(IV_L, IV_R, '')))
    lines.append(R(bMid(IV_L, IV_R, '# PowerMax Solutions Enabler — list COD licenses')))
    lines.append(R(bMid(IV_L, IV_R, 'symlic -sid <SID> list | grep -i "capacity on demand"')))
    lines.append(R(bMid(IV_L, IV_R, '')))
    lines.append(R(bMid(IV_L, IV_R, '# Report: all arrays, COD status, capacity summary')))
    lines.append(R(bMid(IV_L, IV_R, 'for ARRAY in "${ARRAYS[@]}"; do')))
    lines.append(R(bMid(IV_L, IV_R, '  echo "=== $ARRAY ==="; curl -sk ... /api/rest/license | jq ...')))
    lines.append(R(bMid(IV_L, IV_R, 'done')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  total_raw_capacity = All physical raw storage including locked COD; in bytes'))
    lines.append(txt_row('  usable_raw_capacity= Capacity available to create pools; increases after COD activation'))
    lines.append(txt_row('  symlic             = Solutions Enabler license command; requires SYMAPI connectivity'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dell-cod-ts-diag',
    'docs/storage/dell/cod/troubleshooting/diagnostics/index.md',
    'Dell COD diagnostics — license activation failure, key validation, support steps',
)
def dell_cod_ts_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Dell COD Diagnostics'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'COD diagnostics: key rejected, capacity not increasing, license portal errors')))
    lines.append(R(bMid(IV_L, IV_R, 'Key rejection: wrong serial number, duplicate use, corrupted file')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Common Problems'), bMid(B2_L, B2_R, 'Diagnostic Steps'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '─────────────────────────────────'), bMid(B2_L, B2_R, '─────────────────────────────────'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key rejected: serial mismatch'), bMid(B2_L, B2_R, 'Verify array serial in portal'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key already applied'), bMid(B2_L, B2_R, 'Check license list in GUI'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Capacity not increasing'), bMid(B2_L, B2_R, 'Verify pool expansion needed'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Portal error generating key'), bMid(B2_L, B2_R, 'Open Dell licensing SR'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Key file corrupted'), bMid(B2_L, B2_R, 'Re-download from portal'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Problem', 'Root cause', 'Fix', 'Verify', 'Escalate if'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['─' * 16, '─' * 16, '─' * 17, '─' * 16, '─' * 18])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Key rejected', 'Wrong serial', 'Get correct key', 'Apply succeeds', 'Portal issues'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['No cap change', 'Pool not expanded', 'Expand pool', 'Capacity grows', 'HW not visible'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['Key used', 'Duplicate apply', 'Check lic list', 'Already active', '—'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], ['File corrupt', 'Download issue', 'Re-download', 'Apply succeeds', 'Portal SR'])))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Serial mismatch = License key generated for different array serial; portal may have wrong SN'))
    lines.append(txt_row('  Pool expansion  = After COD unlock, pool must be expanded to include new drives in capacity'))
    lines.append(txt_row('  Duplicate apply = Applying same key twice; array reports already activated; not an error'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines
