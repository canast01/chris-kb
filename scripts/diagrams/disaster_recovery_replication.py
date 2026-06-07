"""
Disaster Recovery — Replication & Orchestration (RecoverPoint, SRDF-A/S, SRM, Superna Eyeglass, Veeam, misc DR pages) diagram functions.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)


# ── RecoverPoint ─────────────────────────────────────────────────────────────

@kb_diagram(
    'dr-recoverpoint',
    'docs/storage/dell/recoverpoint/index.md',
    'Dell RecoverPoint for VMs — continuous data protection overview',
)
def dr_recoverpoint():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []

    lines.append(title_border(W2, 'RecoverPoint — Overview'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Dell RecoverPoint for VMs (RP4VM): Continuous Data Protection for VMware environments')))
    lines.append(R(bMid(IV_L, IV_R, 'Intercepts every write via a splitter; journals writes to enable any-point-in-time recovery')))
    lines.append(R(bMid(IV_L, IV_R, 'Supports local protection, remote replication (single/multi-site), and cascade topologies')))
    lines.append(R(bMid(IV_L, IV_R, 'RPO: seconds (CDP journal); RTO: minutes (image access or failover)')))
    lines.append(R(bMid(IV_L, IV_R, 'Core objects: RPA cluster, splitter, consistency group, journal volume, copy')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Protected Site ──splitter intercepts──► RPA Cluster ──journal replication──► Recovery RPA'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Protected Site Components'), bMid(B2_L, B2_R, 'Recovery Site Components'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RPA cluster (2–8 appliances)'), bMid(B2_L, B2_R, 'RPA cluster (matching count)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ESXi splitter (vSphere plugin)'), bMid(B2_L, B2_R, 'Remote journal volumes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Production VMs (consistency grp)'), bMid(B2_L, B2_R, 'Remote copy (replica disks)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Local journal volumes (CDP)'), bMid(B2_L, B2_R, 'vCenter (image access/failover)'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vCenter + RP4VM plugin'), bMid(B2_L, B2_R, 'Network replication link'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: RPAs are VMs or appliances; journal vols on shared datastore; replication IP'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  RPA              = RecoverPoint Appliance; manages replication, journaling, and failover logic'))
    lines.append(txt_row('  Splitter         = Write-interceptor at ESXi kernel or array layer; splits I/O to journal'))
    lines.append(txt_row('  Journal          = Sequential write log on target side; enables any-point-in-time image access'))
    lines.append(txt_row('  Consistency Group= Named set of VMs/volumes that fail over and recover together atomically'))
    lines.append(txt_row('  Copy             = A replication destination (local or remote); each CG has ≥1 copy'))
    lines.append(txt_row('  Bookmark         = Named point-in-time marker in the journal; used for crash-consistent recovery'))
    lines.append(txt_row('  CDP              = Continuous Data Protection; every write captured; journal depth = RPO window'))
    lines.append(txt_row('  Image Access     = Mount a journal image as read/write VM without committing to production'))
    lines.append(txt_row('  Failover         = Activate remote copy; production traffic moves to recovery site'))
    lines.append(txt_row('  Failback         = Reverse replication; sync changes back; cut over to original production'))
    lines.append(txt_row('  Test Copy        = Non-disruptive test failover; recovery VMs isolated on bubble network'))
    lines.append(txt_row('  RPO              = Recovery Point Objective; max acceptable data loss (seconds with CDP)'))
    lines.append(txt_row('  RTO              = Recovery Time Objective; time to restore service after declaring failover'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-recoverpoint-architecture',
    'docs/storage/dell/recoverpoint/architecture/index.md',
    'RecoverPoint Architecture — RPA cluster, splitter, journals, replication topology',
)
def dr_recoverpoint_architecture():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []

    lines.append(title_border(W2, 'RecoverPoint — Architecture'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'RP4VM Architecture: ESXi splitter ──► RPA cluster ──► journal volumes ──► remote RPA')))
    lines.append(R(bMid(IV_L, IV_R, 'RPA cluster: active/active pair; each RPA handles subset of consistency groups')))
    lines.append(R(bMid(IV_L, IV_R, 'Splitter intercepts every VM write at ESXi kernel; sends copy to RPA without blocking I/O')))
    lines.append(R(bMid(IV_L, IV_R, 'Journal stores delta writes; replication link carries deltas from source to target RPA')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Write Path'), bMid(B2_L, B2_R, 'RPA Cluster'), bMid(B3_L, B3_R, 'Journal / Copy'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VM issues write'), bMid(B2_L, B2_R, '2–8 RPA nodes'), bMid(B3_L, B3_R, 'Local journal'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'ESXi splitter forks'), bMid(B2_L, B2_R, 'Active/active HA'), bMid(B3_L, B3_R, 'Remote journal'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Prod write → array'), bMid(B2_L, B2_R, 'Owns CG set'), bMid(B3_L, B3_R, 'CDP depth = RPO'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Copy → RPA buffer'), bMid(B2_L, B2_R, 'vSphere plugin'), bMid(B3_L, B3_R, 'Replica volumes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RPA applies to jrnl'), bMid(B2_L, B2_R, 'WAN compression'), bMid(B3_L, B3_R, 'Bookmark timeline'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: RPAs run as VMs (4 vCPU/8 GB) on dedicated ESXi host; journal vols on separate datastore'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  RPA cluster      = 2–8 RecoverPoint Appliance VMs per site; active/active; no SPOF'))
    lines.append(txt_row('  ESXi splitter    = Kernel module on each ESXi host; intercepts VM disk writes non-disruptively'))
    lines.append(txt_row('  Local copy       = Protection within same site (cluster); journal on same or separate DS'))
    lines.append(txt_row('  Remote copy      = Cross-site replication; delta compressed over IP WAN; bandwidth-adaptive'))
    lines.append(txt_row('  Journal volume   = Dedicated VMDK per copy; stores write deltas; sized for desired CDP window'))
    lines.append(txt_row('  Replica volume   = Copy of production VMDK at target site; updated by journal apply process'))
    lines.append(txt_row('  Delta set        = Unit of replication transfer between source and target RPA'))
    lines.append(txt_row('  WAN compression  = RPA compresses and deduplicates replication traffic before sending across WAN'))
    lines.append(txt_row('  Active/active    = Both RPAs handle I/O simultaneously; failover automatic on RPA loss'))
    lines.append(txt_row('  CG ownership     = Each CG assigned to one RPA; redistributed automatically on RPA failure'))
    lines.append(txt_row('  vSphere plugin   = RP4VM vCenter plugin; exposes CG management, failover, and image access in UI'))
    lines.append(txt_row('  Bubble network   = Isolated portgroup for test VMs; no production traffic reaches copies'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-recoverpoint-arch-how-it-works',
    'docs/storage/dell/recoverpoint/architecture/how-it-works/index.md',
    'RecoverPoint How It Works — write splitting, journal mechanics, replication flow',
)
def dr_recoverpoint_arch_how_it_works():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []

    lines.append(title_border(W2, 'RecoverPoint — How It Works'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Write Flow: VM write → ESXi splitter forks I/O → production path + RPA buffer')))
    lines.append(R(bMid(IV_L, IV_R, 'RPA bundles writes into delta sets → compresses → sends to remote RPA over IP')))
    lines.append(R(bMid(IV_L, IV_R, 'Remote RPA applies delta set to journal; journal tracks sequence and timestamps')))
    lines.append(R(bMid(IV_L, IV_R, 'Recovery: select bookmark or time → RPA rolls journal forward/back → present image')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Step 1: Write  ──► Step 2: Split  ──► Step 3: Journal  ──► Step 4: Replicate  ──► Step 5: Apply'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Source Side'), bMid(B2_L, B2_R, 'Target Side'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'VM disk write issued'), bMid(B2_L, B2_R, 'Remote RPA receives delta'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Splitter forks to RPA'), bMid(B2_L, B2_R, 'Writes to remote journal'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RPA buffers in memory'), bMid(B2_L, B2_R, 'Updates replica VMDK'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Bundles into delta set'), bMid(B2_L, B2_R, 'Advances journal pointer'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Compresses, sends WAN'), bMid(B2_L, B2_R, 'Logs bookmark timestamps'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: journal = dedicated VMDK on datastore; splitter = ESXi kernel module; RPA = VM appliance'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Write splitting     = Non-blocking fork of every VM disk write at hypervisor layer'))
    lines.append(txt_row('  Delta set           = Batch of compressed write deltas transferred from source to target RPA'))
    lines.append(txt_row('  Journal apply       = Process of writing delta sets to journal VMDK in sequence on target side'))
    lines.append(txt_row('  Journal pointer     = Current position in the journal; marks which deltas have been applied'))
    lines.append(txt_row('  Bookmark         = Named timestamp in journal; recovery to a known-good application state'))
    lines.append(txt_row('  Crash-consistent    = All VMs in CG captured at the same write sequence; safe for OS-level recovery'))
    lines.append(txt_row('  App-consistent      = Quiesced snapshot of CG (VMware Tools quiesce); safe for DB-level recovery'))
    lines.append(txt_row('  Image access        = Temporary mount of journal image; test without committing; auto rolls back'))
    lines.append(txt_row('  CDP window          = Journal depth in time; configurable; determines how far back recovery reaches'))
    lines.append(txt_row('  Replication lag     = Difference between source write time and target journal apply time (=RPO)'))
    lines.append(txt_row('  WAN throttle        = Bandwidth cap on replication link per CG; prevents production WAN saturation'))
    lines.append(txt_row('  Compression ratio   = Typical 2:1–4:1 reduction on replication traffic via RPA dedup/compress'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-recoverpoint-arch-design',
    'docs/storage/dell/recoverpoint/architecture/design-standards/index.md',
    'RecoverPoint Design Standards — sizing, journal, network, consistency group design',
)
def dr_recoverpoint_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []

    lines.append(title_border(W2, 'RecoverPoint — Design Standards'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Design principles: right-size RPAs, journal volumes, and WAN bandwidth before deployment')))
    lines.append(R(bMid(IV_L, IV_R, 'RPA count: 2 minimum per site; add one RPA per 50 protected VMs or 500 MB/s write throughput')))
    lines.append(R(bMid(IV_L, IV_R, 'Journal size: (peak write MB/s) × (CDP window hours) × 3600 × 1.3 overhead factor')))
    lines.append(R(bMid(IV_L, IV_R, 'WAN bandwidth: match replication throughput; deduplicated traffic typically 30–50% of raw')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RPA Sizing'), bMid(B2_L, B2_R, 'Journal Sizing'), bMid(B3_L, B3_R, 'Network Design'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '2 RPA minimum'), bMid(B2_L, B2_R, '2–24 hr CDP window'), bMid(B3_L, B3_R, 'Dedicated repl VLAN'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '1 RPA / 50 VMs'), bMid(B2_L, B2_R, '×1.3 overhead factor'), bMid(B3_L, B3_R, 'MTU 9000 jumbo'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '4 vCPU / 8 GB RAM'), bMid(B2_L, B2_R, 'Separate datastore'), bMid(B3_L, B3_R, 'QoS priority class'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Anti-affinity rules'), bMid(B2_L, B2_R, 'VMDK thin provision'), bMid(B3_L, B3_R, 'WAN dedup enabled'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Mgmt IP per RPA'), bMid(B2_L, B2_R, 'Alarm on >80% full'), bMid(B3_L, B3_R, 'Latency <100 ms'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: RPA VMs pinned to dedicated ESXi hosts; journal on separate LUNs from prod'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  RPA sizing          = Calculate RPA count from VM count and write throughput; minimum 2 per site'))
    lines.append(txt_row('  Journal sizing      = Peak writes × CDP window × overhead; use RP Sizer tool for accuracy'))
    lines.append(txt_row('  CDP window          = How far back in time the journal allows recovery; typically 2–24 hours'))
    lines.append(txt_row('  Overhead factor     = 1.3× buffer for journal metadata, sequencing, and burst write absorption'))
    lines.append(txt_row('  Anti-affinity       = DRS rule keeping RPA VMs on separate ESXi hosts for HA'))
    lines.append(txt_row('  Dedicated VLAN      = Isolate RPA replication traffic from production VM and management traffic'))
    lines.append(txt_row('  Jumbo frames        = MTU 9000 on replication VLAN; reduces fragmentation; improves throughput'))
    lines.append(txt_row('  QoS                 = DSCP marking on replication traffic; prioritised over bulk data transfers'))
    lines.append(txt_row('  CG design           = Group VMs by application tier; same CG = same RPO and same failover unit'))
    lines.append(txt_row('  RP Sizer            = Dell sizing tool; inputs write rate, change rate, and WAN link speed'))
    lines.append(txt_row('  Thin provision      = Journal VMDKs thin-provisioned; grow on demand up to alarm threshold'))
    lines.append(txt_row('  WAN dedup           = RPA deduplicates replication stream; reduces bandwidth by ~30–50%'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-recoverpoint-arch-integrations',
    'docs/storage/dell/recoverpoint/architecture/integrations/index.md',
    'RecoverPoint Integrations — vCenter, array SRAs, VPLEX, PowerMax',
)
def dr_recoverpoint_arch_integrations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []

    lines.append(title_border(W2, 'RecoverPoint — Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'RP4VM integrates with vCenter, VMware SRM, PowerMax/VMAX array splitters, and VPLEX')))
    lines.append(R(bMid(IV_L, IV_R, 'SRM integration: RP4VM SRA enables SRM to orchestrate failover via RecoverPoint journals')))
    lines.append(R(bMid(IV_L, IV_R, 'Array splitter (PowerMax): writes intercepted at array; no ESXi splitter required')))
    lines.append(R(bMid(IV_L, IV_R, 'VPLEX integration: RP4VM protects VPLEX virtual volumes across geo-stretched clusters')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  vCenter ◄──► RP4VM plugin ◄──► RPA cluster ◄──► SRM SRA ◄──► SRM recovery plans'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'vSphere / SRM Integration'), bMid(B2_L, B2_R, 'Array / VPLEX Integration'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RP4VM vCenter plugin'), bMid(B2_L, B2_R, 'PowerMax array splitter'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'SRM SRA for RecoverPoint'), bMid(B2_L, B2_R, 'VMAX array splitter'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Protection group mapping'), bMid(B2_L, B2_R, 'VPLEX virtual volumes'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Recovery plan execution'), bMid(B2_L, B2_R, 'No ESXi splitter needed'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Test failover automation'), bMid(B2_L, B2_R, 'XtremIO integration'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SRA plugin on SRM server; array splitter on PowerMax; VPLEX needs RP licence'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  SRA              = Storage Replication Adapter; on SRM server; translates SRM → RP API'))
    lines.append(txt_row('  RP4VM plugin     = vCenter plugin; CG management, failover, image access in UI'))
    lines.append(txt_row('  Array splitter   = Intercepts writes in array firmware; higher performance than ESXi'))
    lines.append(txt_row('  VPLEX integration= RP journals VPLEX virtual volumes; enables CDP for geo-stretched metro clusters'))
    lines.append(txt_row('  Protection group = SRM construct; maps to RP4VM consistency group; defines what SRM protects'))
    lines.append(txt_row('  Recovery plan    = SRM ordered script of steps for failover; calls RP4VM SRA at failover step'))
    lines.append(txt_row('  XtremIO          = All-flash array from Dell; supports RP4VM via array splitter licence'))
    lines.append(txt_row('  PowerMax splitter= Writes forked inside PowerMax engine; RPA receives copy without ESXi module'))
    lines.append(txt_row('  API endpoint     = RP REST API on RPA management IP; used by SRA and automation scripts'))
    lines.append(txt_row('  CG-to-PG mapping = Each SRM protection group maps 1:1 to an RP4VM consistency group'))
    lines.append(txt_row('  Bubble network   = Isolated VLAN created by SRM for test failover; test VMs unreachable from prod'))
    lines.append(txt_row('  VPLEX Metro      = Synchronous stretch cluster; RP adds CDP layer for any-point recovery on top'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-recoverpoint-operations',
    'docs/storage/dell/recoverpoint/operations/index.md',
    'RecoverPoint Operations — daily tasks, monitoring, CG management',
)
def dr_recoverpoint_operations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []

    lines.append(title_border(W2, 'RecoverPoint — Operations Overview'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Operational tasks: monitor CG replication lag, journal usage, RPA health, and link state')))
    lines.append(R(bMid(IV_L, IV_R, 'Daily: verify all CGs are Active/Synchronizing; check journal fill level < 70%')))
    lines.append(R(bMid(IV_L, IV_R, 'Weekly: test copy drill on non-prod CG; review RPO compliance report')))
    lines.append(R(bMid(IV_L, IV_R, 'Access via: RP Management Application (Unisphere for RP), vCenter plugin, or CLI')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Monitoring'), bMid(B2_L, B2_R, 'CG Management'), bMid(B3_L, B3_R, 'Maintenance'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Replication lag'), bMid(B2_L, B2_R, 'Add/remove VMs'), bMid(B3_L, B3_R, 'RPA upgrade'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Journal fill %'), bMid(B2_L, B2_R, 'Set bookmark'), bMid(B3_L, B3_R, 'Splitter update'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RPA CPU/memory'), bMid(B2_L, B2_R, 'Enable/disable CG'), bMid(B3_L, B3_R, 'Journal resize'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Link bandwidth'), bMid(B2_L, B2_R, 'Change RPO policy'), bMid(B3_L, B3_R, 'CG re-sync'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Alarm dashboard'), bMid(B2_L, B2_R, 'Image access test'), bMid(B3_L, B3_R, 'Failover drill'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: access Unisphere for RP via browser; RPA management port on dedicated management VLAN'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Replication lag     = Time between source write and target journal apply; goal < 30 seconds'))
    lines.append(txt_row('  Journal fill %      = Percentage of journal VMDK consumed; alert at 70%; critical at 90%'))
    lines.append(txt_row('  CG state            = Active, Paused, Error, Initializing, or Transferring; check daily'))
    lines.append(txt_row('  Unisphere for RP    = Web GUI for RecoverPoint; manage CGs, view topology, run reports'))
    lines.append(txt_row('  Image access test   = Mount a CDP image non-disruptively; validate data integrity without failover'))
    lines.append(txt_row('  RPO compliance      = Report showing whether actual lag stayed within configured RPO per CG'))
    lines.append(txt_row('  Bookmark            = Set before maintenance windows; provides a known-good recovery target'))
    lines.append(txt_row('  Re-sync             = After CG pause/error; resynchronises source and target without full rescan'))
    lines.append(txt_row('  Failover drill      = Scheduled test of full failover procedure; uses bubble network isolation'))
    lines.append(txt_row('  RPA health          = Check CPU, memory, fan, PSU status in Unisphere hardware dashboard'))
    lines.append(txt_row('  WAN bandwidth util  = Monitor replication link utilisation; alert if sustained >80% of allocated'))
    lines.append(txt_row('  Splitter state      = Verify splitter loaded on each ESXi host; alert if splitter unloaded'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-recoverpoint-ops-backup',
    'docs/storage/dell/recoverpoint/operations/backup-restore/index.md',
    'RecoverPoint Backup & Restore — image access, failover, test copy procedures',
)
def dr_recoverpoint_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []

    lines.append(title_border(W2, 'RecoverPoint — Backup & Restore'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'RecoverPoint provides CDP-based recovery; no traditional backup agent needed for replicated VMs')))
    lines.append(R(bMid(IV_L, IV_R, 'Recovery options: image access (non-disruptive), test copy, failover, and restore to production')))
    lines.append(R(bMid(IV_L, IV_R, 'RPA config backup: export system settings from Unisphere; store off-site after every change')))
    lines.append(R(bMid(IV_L, IV_R, 'Recovery granularity: any point in journal window, or named bookmark')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Recovery flow: select CG ──► choose point-in-time ──► image access or failover ──► validate'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Recovery Methods'), bMid(B2_L, B2_R, 'Config Backup'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Image access (read-only)'), bMid(B2_L, B2_R, 'Export system config XML'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Image access (r/w enabled)'), bMid(B2_L, B2_R, 'Store after every change'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Test copy (bubble VLAN)'), bMid(B2_L, B2_R, 'RPA appliance snapshot'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Failover (prod cutover)'), bMid(B2_L, B2_R, 'Re-import on rebuild'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Failback (resync + cutback)'), bMid(B2_L, B2_R, 'Test import on lab'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: failover powers on replica VMs at DR site; requires pre-configured networks'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Image access     = Non-disruptive mount of journal image; source VMs continue running unchanged'))
    lines.append(txt_row('  Read/write image = Enable writes to image copy; journal paused; useful for data mining recovery'))
    lines.append(txt_row('  Test copy        = Full VM boot of replica in isolated bubble network; validates recoverability'))
    lines.append(txt_row('  Failover         = Commit image to replica; power on VMs at DR site; redirect production traffic'))
    lines.append(txt_row('  Failback         = After failover; reverse replicate from DR to prod; restore original direction'))
    lines.append(txt_row('  Bookmark         = Named time marker; set before patching, app changes, or maintenance windows'))
    lines.append(txt_row('  Config export    = Unisphere → System → Export Config; saves all CG definitions and RPA settings'))
    lines.append(txt_row('  Journal rollback = Roll journal pointer back to earlier timestamp; expose older write sequence'))
    lines.append(txt_row('  Bubble VLAN      = Isolated portgroup; test copy VMs powered on here; no prod network access'))
    lines.append(txt_row('  RPO validation   = Confirm lag at time of failover; determines actual data loss window'))
    lines.append(txt_row('  Resync           = After failback; re-establish replication from production to DR direction'))
    lines.append(txt_row('  Recovery point   = Specific second-level timestamp in journal window chosen for recovery'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-recoverpoint-ops-cli',
    'docs/storage/dell/recoverpoint/operations/cli-reference/index.md',
    'RecoverPoint CLI Reference — boxmgmt, get all cgs, set group, failover commands',
)
def dr_recoverpoint_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []

    lines.append(title_border(W2, 'RecoverPoint — CLI Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'RecoverPoint CLI: SSH to RPA management IP; login as admin; CLI mode (boxmgmt is hardware)')))
    lines.append(R(bMid(IV_L, IV_R, 'Main commands: get all cgs, set group, set bookmark, failover, enable/disable group')))
    lines.append(R(bMid(IV_L, IV_R, 'boxmgmt: low-level RPA appliance management; hardware status, NTP, network config')))
    lines.append(R(bMid(IV_L, IV_R, 'Scripting: RP REST API (port 443); JSON responses; auth via basic or token')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  SSH admin@<RPA-IP> ──► CLI prompt ──► get all cgs / set group <n> / failover group <n>'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Monitoring Commands'), bMid(B2_L, B2_R, 'Control Commands'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'get all cgs'), bMid(B2_L, B2_R, 'failover group <name>'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'get group <name>'), bMid(B2_L, B2_R, 'enable group <name>'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'get system'), bMid(B2_L, B2_R, 'disable group <name>'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'get links'), bMid(B2_L, B2_R, 'set bookmark <name>'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'get rpa status'), bMid(B2_L, B2_R, 'start image access'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: SSH to RPA management IP on mgmt VLAN; boxmgmt for hardware; admin CLI for CG ops'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  boxmgmt          = Hardware-level CLI; configure NTP, network, passwords, and factory reset'))
    lines.append(txt_row('  get all cgs      = List all consistency groups with state, lag, and journal fill'))
    lines.append(txt_row('  get group        = Detailed view of single CG; copies, VMs, lag, policy, bookmarks'))
    lines.append(txt_row('  get system       = RPA cluster health; node states, link status, and replication summary'))
    lines.append(txt_row('  failover group   = Initiate failover for named CG; confirms before executing'))
    lines.append(txt_row('  enable/disable   = Start or pause replication for a CG; disable before maintenance'))
    lines.append(txt_row('  set bookmark     = Create named timestamp in journal; specify CG and bookmark name'))
    lines.append(txt_row('  start image access = Mount journal image at selected time; choose read-only or read-write'))
    lines.append(txt_row('  get links        = Show replication links; bandwidth utilisation, latency, packet loss'))
    lines.append(txt_row('  REST API         = RP REST endpoint; same operations as CLI; used by SRA and automation'))
    lines.append(txt_row('  admin CLI        = SSH-accessible CLI; differs from boxmgmt; all CG and replication commands'))
    lines.append(txt_row('  failback         = CLI command to reverse replication after failover; requires resync first'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-recoverpoint-ops-health',
    'docs/storage/dell/recoverpoint/operations/health-checks/index.md',
    'RecoverPoint Health Checks — RPA status, CG lag, journal fill, splitter state',
)
def dr_recoverpoint_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []

    lines.append(title_border(W2, 'RecoverPoint — Health Checks'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Health check cadence: daily CG lag/journal, weekly test copy, monthly failover drill')))
    lines.append(R(bMid(IV_L, IV_R, 'Critical alerts: CG in error state, journal >90% full, RPA node failure, link down')))
    lines.append(R(bMid(IV_L, IV_R, 'Check sources: Unisphere for RP, vCenter plugin, SNMP traps, REST API polling')))
    lines.append(R(bMid(IV_L, IV_R, 'Baseline: all CGs Active; lag <30 s; journal <70%; all RPA nodes Online')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'RPA Health'), bMid(B2_L, B2_R, 'CG Health'), bMid(B3_L, B3_R, 'Link Health'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Node state: Online'), bMid(B2_L, B2_R, 'State: Active'), bMid(B3_L, B3_R, 'Link state: Up'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'CPU < 80%'), bMid(B2_L, B2_R, 'Lag < 30 sec'), bMid(B3_L, B3_R, 'Latency < 100 ms'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Memory < 85%'), bMid(B2_L, B2_R, 'Journal < 70%'), bMid(B3_L, B3_R, 'Packet loss 0%'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Fan/PSU OK'), bMid(B2_L, B2_R, 'Splitter loaded'), bMid(B3_L, B3_R, 'BW util < 80%'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'NTP synced'), bMid(B2_L, B2_R, 'No errors 24 h'), bMid(B3_L, B3_R, 'Compression OK'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: RPA hardware health viewable in Unisphere; splitter state visible per ESXi host'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  CG state Active  = Replication is running; writes being journaled; lag within RPO target'))
    lines.append(txt_row('  Lag (RPO lag)    = Seconds between last source write and journal apply on target; primary KPI'))
    lines.append(txt_row('  Journal fill %   = Consumed / allocated journal VMDK; >90% causes CG to pause replication'))
    lines.append(txt_row('  Splitter loaded  = ESXi kernel module active; check per host in Unisphere splitter view'))
    lines.append(txt_row('  SNMP traps       = RPA sends traps to NMS on CG error, journal fill, and RPA node failure'))
    lines.append(txt_row('  Link utilisation = WAN replication bandwidth; sustained >80% may cause lag increase'))
    lines.append(txt_row('  NTP sync         = Critical for journal timestamps and cross-site consistency; must be in sync'))
    lines.append(txt_row('  Packet loss      = Any loss on replication link degrades throughput; investigate immediately'))
    lines.append(txt_row('  RPA node failure = Surviving RPA takes over all CGs; CGs continue with reduced throughput'))
    lines.append(txt_row('  Unisphere alert  = Red badge in Unisphere dashboard; drill down to CG, link, or hardware'))
    lines.append(txt_row('  REST poll        = GET /system/clusters; /groups; /links; use for monitoring integration'))
    lines.append(txt_row('  Monthly drill    = Full failover test with VM power-on at DR site; documents RTO achieved'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-recoverpoint-ops-install',
    'docs/storage/dell/recoverpoint/operations/install-upgrade/index.md',
    'RecoverPoint Install & Upgrade — RPA deployment, splitter install, version upgrade',
)
def dr_recoverpoint_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []

    lines.append(title_border(W2, 'RecoverPoint — Install & Upgrade'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Install order: deploy RPA OVF → configure network → pair sites → install splitter on ESXi hosts')))
    lines.append(R(bMid(IV_L, IV_R, 'Pre-req: vCenter credentials, management VLAN, replication VLAN, journal datastore')))
    lines.append(R(bMid(IV_L, IV_R, 'Upgrade: rolling RPA upgrade (one node at a time); CGs remain active during upgrade')))
    lines.append(R(bMid(IV_L, IV_R, 'Splitter upgrade: done via VIB update on ESXi; requires host maintenance mode')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Deploy RPA OVF ──► network config ──► site pairing ──► install splitter ──► create CGs'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Fresh Install Steps'), bMid(B2_L, B2_R, 'Upgrade Steps'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '1. Deploy RPA OVF per site'), bMid(B2_L, B2_R, '1. Download new RPA image'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '2. Configure mgmt/repl IPs'), bMid(B2_L, B2_R, '2. Upload to Unisphere'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '3. Pair protected/recovery'), bMid(B2_L, B2_R, '3. Rolling node upgrade'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '4. Install ESXi splitter VIB'), bMid(B2_L, B2_R, '4. Upgrade splitter VIBs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '5. Create consistency groups'), bMid(B2_L, B2_R, '5. Validate all CGs active'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: RPA VMs need 4 vCPU, 8 GB RAM, 3 vNICs (mgmt, replication, data); use anti-affinity rules'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  OVF deploy       = Deploy RPA as virtual appliance from OVF template in vCenter'))
    lines.append(txt_row('  Site pairing     = Connect protected site RPA cluster to recovery site RPA cluster over IP'))
    lines.append(txt_row('  Splitter VIB     = VMware Installation Bundle; installed on ESXi via esxcli software vib install'))
    lines.append(txt_row('  Management IP    = RPA vNIC for Unisphere access and admin CLI; on management VLAN'))
    lines.append(txt_row('  Replication IP   = RPA vNIC for site-to-site journal replication traffic; on replication VLAN'))
    lines.append(txt_row('  Data IP          = RPA vNIC for write split data from ESXi splitter to RPA; on storage VLAN'))
    lines.append(txt_row('  Rolling upgrade  = Upgrade one RPA node at a time; surviving node handles all CGs during upgrade'))
    lines.append(txt_row('  VIB update       = ESXi host in maintenance mode; esxcli updates splitter kernel module'))
    lines.append(txt_row('  Post-upgrade     = Verify all CGs Active; check lag; confirm splitter version per host'))
    lines.append(txt_row('  License          = Apply RP4VM licence in Unisphere before creating first CG'))
    lines.append(txt_row('  Compatibility    = Check RP4VM compatibility matrix; ESXi version must match supported list'))
    lines.append(txt_row('  Journal datastore= Dedicated datastore for journal VMDKs; separate from production datastores'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-recoverpoint-ops-procedures',
    'docs/storage/dell/recoverpoint/operations/procedures/index.md',
    'RecoverPoint Procedures — failover, failback, test copy, image access step-by-step',
)
def dr_recoverpoint_ops_procedures():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    lines = []

    lines.append(title_border(W2, 'RecoverPoint — Procedures'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Standard procedures: failover, failback, test copy, image access, bookmark creation')))
    lines.append(R(bMid(IV_L, IV_R, 'Always set a bookmark before any maintenance or planned failover for clean recovery point')))
    lines.append(R(bMid(IV_L, IV_R, 'Failover pre-check: confirm lag, journal %, network readiness, VM power state at DR')))
    lines.append(R(bMid(IV_L, IV_R, 'Failback pre-check: production site healthy, reverse replication established, data synced')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Failover'), bMid(B2_L, B2_R, 'Failback'), bMid(B3_L, B3_R, 'Test Copy'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '1. Set bookmark'), bMid(B2_L, B2_R, '1. Verify prod OK'), bMid(B3_L, B3_R, '1. Create bubble net'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '2. Disable prod VMs'), bMid(B2_L, B2_R, '2. Reverse replicate'), bMid(B3_L, B3_R, '2. Select bookmark'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '3. Failover CG'), bMid(B2_L, B2_R, '3. Wait for sync'), bMid(B3_L, B3_R, '3. Start test copy'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '4. Power on DR VMs'), bMid(B2_L, B2_R, '4. Failback CG'), bMid(B3_L, B3_R, '4. Power on test VMs'))))
    lines.append(R(merge(bMid(B1_L, B1_R, '5. Redirect traffic'), bMid(B2_L, B2_R, '5. Re-enable CG'), bMid(B3_L, B3_R, '5. Validate & end test'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: test VMs on bubble portgroup (no uplinks); DR network must be pre-configured'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  Failover         = Commit journal image; power on VMs at DR site; production traffic moves'))
    lines.append(txt_row('  Failback         = Reverse replication; sync DR changes back to prod; cut over to prod'))
    lines.append(txt_row('  Reverse replicate= After failover; replication runs DR→prod direction; syncs delta writes'))
    lines.append(txt_row('  Test copy        = Non-disruptive; replica boots on bubble VLAN; no prod impact'))
    lines.append(txt_row('  Image access     = Read-only or r/w mount; source continues; no VM power-on at DR'))
    lines.append(txt_row('  Bookmark         = Set before maintenance; provides clean point for any recovery type'))
    lines.append(txt_row('  Pre-check        = Verify lag, journal fill, DR network config, and ESXi connectivity'))
    lines.append(txt_row('  Bubble network   = Isolated portgroup created for test; removed after test ends'))
    lines.append(txt_row('  Traffic redirect = DNS/load balancer update to point to DR site IP addresses'))
    lines.append(txt_row('  Resync           = After failback; establishes forward replication again (prod → DR)'))
    lines.append(txt_row('  CG disable       = Pause replication before planned failover; prevents writes during cutover'))
    lines.append(txt_row('  Post-failover    = Confirm all VMs running; validate application; set new bookmark'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-recoverpoint-ops-scripts',
    'docs/storage/dell/recoverpoint/operations/scripts/index.md',
    'RecoverPoint Scripts — automation via REST API, health check scripts, CG reporting',
)
def dr_recoverpoint_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1, M2 = 26, 76
    lines = []

    lines.append(title_border(W2, 'RecoverPoint — Scripts'))
    lines.append(txt_row())
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'RP automation: REST API (HTTPS/443) or CLI scripting via SSH; Python/PowerShell common')))
    lines.append(R(bMid(IV_L, IV_R, 'Common scripts: CG health report, journal fill monitor, lag alert, bulk bookmark creation')))
    lines.append(R(bMid(IV_L, IV_R, 'API base: https://<RPA-IP>/fapi/rest/5_1; auth: Basic or session token')))
    lines.append(R(bMid(IV_L, IV_R, 'SDK: Dell RecoverPoint PowerShell module (unofficial); wraps REST calls')))
    lines.append(R(bBot(IV_L, IV_R)))
    lines.append(txt_row())
    lines.append(txt_row('  Script triggers: cron/Task Scheduler ──► REST/SSH ──► RPA API ──► parse response ──► alert'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'Monitoring Scripts'), bMid(B2_L, B2_R, 'Automation Scripts'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'get_cg_lag.py'), bMid(B2_L, B2_R, 'create_bookmark.py'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'journal_fill_alert.py'), bMid(B2_L, B2_R, 'bulk_enable_cgs.sh'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'rpa_health_check.py'), bMid(B2_L, B2_R, 'failover_cg.py'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'rpo_compliance_report.py'), bMid(B2_L, B2_R, 'test_copy_automation.ps1'))))
    lines.append(R(merge(bMid(B1_L, B1_R, 'link_status_check.sh'), bMid(B2_L, B2_R, 'config_backup.py'))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))
    lines.append(txt_row())
    lines.append(txt_row('  Physical: scripts run from jump host on management VLAN with HTTPS/SSH access to RPA management IPs'))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('  REST API base    = https://<RPA-IP>/fapi/rest/5_1; GET /clusters, /groups, /links endpoints'))
    lines.append(txt_row('  Session token    = POST to /sessions; returns token; use X-RP-Auth header in subsequent calls'))
    lines.append(txt_row('  CG lag script    = Poll GET /groups; parse transferTimeLag; alert if > threshold seconds'))
    lines.append(txt_row('  Journal fill     = GET /groups/<id>/copies; check journalUsagePercent; alert if > 70%'))
    lines.append(txt_row('  Bulk bookmark    = POST /groups/<id>/bookmarks; run for all CGs before maintenance window'))
    lines.append(txt_row('  RPO report       = Pull lag history; calculate % time within RPO; export to CSV/email'))
    lines.append(txt_row('  Config backup    = GET /system/config; export XML; store in version-controlled repo'))
    lines.append(txt_row('  SSH scripting    = Paramiko or subprocess SSH to RPA; run get all cgs; parse text output'))
    lines.append(txt_row('  PowerShell module= Import-Module RecoverPoint; wraps REST; Windows automation environments'))
    lines.append(txt_row('  Cron schedule    = Health checks every 5 min; journal fill every 15 min; RPO report daily'))
    lines.append(txt_row('  Alert routing    = Scripts send email or post to Slack/Teams webhook on threshold breach'))
    lines.append(txt_row('  Error handling   = Catch HTTP 4xx/5xx; retry with backoff; log to syslog on persistent failure'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-recoverpoint-security',
    'docs/storage/dell/recoverpoint/security/index.md',
    'RecoverPoint — security overview, controls, compliance posture',
)
def _dr_recoverpoint_security():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RecoverPoint — Security'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RecoverPoint — Security Posture')))
    lines.append(R(bMid(3, 99, 'Authentication: RPA admin / monitor roles; LDAP integration; certificate-based inter-RPA auth')))
    lines.append(R(bMid(3, 99, 'Encryption: AES-256 WAN compression+encryption; journal vols at rest unencrypted by default')))
    lines.append(R(bMid(3, 99, 'Network: management VLAN separated; 8888 (splitter API) management port')))
    lines.append(R(bMid(3, 99, 'Audit: all admin actions logged; log retention minimum 1 year')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Access Control'), bMid(36, 66, 'Encryption'), bMid(69, 99, 'Audit'))))
    lines.append(R(merge(bMid(3, 33, 'RBAC roles'), bMid(36, 66, 'AES-256 at rest'), bMid(69, 99, 'Admin actions'))))
    lines.append(R(merge(bMid(3, 33, 'Least privilege'), bMid(36, 66, 'TLS in transit'), bMid(69, 99, 'Login events'))))
    lines.append(R(merge(bMid(3, 33, 'MFA optional'), bMid(36, 66, 'Key rotation'), bMid(69, 99, 'Syslog export'))))
    lines.append(R(merge(bMid(3, 33, 'SVC acct rotate'), bMid(36, 66, 'WORM / immutable'), bMid(69, 99, 'SIEM forward'))))
    lines.append(R(merge(bMid(3, 33, 'Just-In-Time'), bMid(36, 66, 'KMS managed'), bMid(69, 99, 'Quarterly review'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('RPA virtual appliances on ESXi · Journal volumes on storage array · WAN link between sites'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPA           = RecoverPoint Appliance — virtual appliance managing journal and replication'))
    lines.append(txt_row('Splitter      = intercepts host I/O at hypervisor or array level; sends copy to RPA'))
    lines.append(txt_row('Journal       = write-order-consistent storage capturing all writes for point-in-time access'))
    lines.append(txt_row('Consistency Group= set of volumes protected together; writes are applied in order across all'))
    lines.append(txt_row('Bookmark      = named marker in journal; enables deterministic recovery to a known state'))
    lines.append(txt_row('Image Access  = mounting a journal point-in-time image to a host for testing or recovery'))
    lines.append(txt_row('Failover      = activating the replica at the recovery site; breaks replication relationship'))
    lines.append(txt_row('Test Copy     = non-disruptive image access for validation without breaking replication'))
    lines.append(txt_row('RPO           = Recovery Point Objective; how much data loss is acceptable; CDP = near-zero'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover to service restored'))
    lines.append(txt_row('Reverse       = after failover, replicates from recovery site back to re-sync production'))
    lines.append(txt_row('Splitter Lag  = delay between host write and journal commit; monitor for replication health'))
    lines.append(txt_row('CDP           = Continuous Data Protection; every write journaled, not just scheduled snaps'))
    lines.append(txt_row('Distributed CG= consistency group spanning volumes on multiple storage arrays'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-recoverpoint-sec-access',
    'docs/storage/dell/recoverpoint/security/access-control/index.md',
    'RecoverPoint — RBAC, permissions, service accounts',
)
def _dr_recoverpoint_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RecoverPoint — Access Control'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RecoverPoint — RBAC and Access Control')))
    lines.append(R(bMid(3, 99, 'Auth: RPA admin / monitor roles; LDAP integration; certificate-based inter-RPA auth')))
    lines.append(R(bMid(3, 99, 'Principle of least privilege: each role gets only required permissions')))
    lines.append(R(bMid(3, 99, 'Service accounts: dedicated, non-interactive; rotation every 90 days')))
    lines.append(R(bMid(3, 99, 'Emergency break-glass: documented, monitored, time-limited access')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Role', 'Access Level', 'Typical User', 'Review Freq', 'Granted By'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Admin', 'Full config/ops', 'Sr Backup Eng', 'Quarterly', 'Security team'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Operator', 'Start/stop jobs', 'Backup Eng', 'Quarterly', 'Team lead'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Monitor', 'Read-only view', 'NOC / L1', 'Quarterly', 'Team lead'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Service Acct', 'API / headless', 'Automation', 'Per rotation', 'Security team'])))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('RPA virtual appliances on ESXi · Journal volumes on storage array · WAN link between sites'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPA           = RecoverPoint Appliance — virtual appliance managing journal and replication'))
    lines.append(txt_row('Splitter      = intercepts host I/O at hypervisor or array level; sends copy to RPA'))
    lines.append(txt_row('Journal       = write-order-consistent storage capturing all writes for point-in-time access'))
    lines.append(txt_row('Consistency Group= set of volumes protected together; writes are applied in order across all'))
    lines.append(txt_row('Bookmark      = named marker in journal; enables deterministic recovery to a known state'))
    lines.append(txt_row('Image Access  = mounting a journal point-in-time image to a host for testing or recovery'))
    lines.append(txt_row('Failover      = activating the replica at the recovery site; breaks replication relationship'))
    lines.append(txt_row('Test Copy     = non-disruptive image access for validation without breaking replication'))
    lines.append(txt_row('RPO           = Recovery Point Objective; how much data loss is acceptable; CDP = near-zero'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover to service restored'))
    lines.append(txt_row('Reverse       = after failover, replicates from recovery site back to re-sync production'))
    lines.append(txt_row('Splitter Lag  = delay between host write and journal commit; monitor for replication health'))
    lines.append(txt_row('CDP           = Continuous Data Protection; every write journaled, not just scheduled snaps'))
    lines.append(txt_row('Distributed CG= consistency group spanning volumes on multiple storage arrays'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-recoverpoint-sec-auth',
    'docs/storage/dell/recoverpoint/security/authentication/index.md',
    'RecoverPoint — authentication methods, certificate management',
)
def _dr_recoverpoint_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RecoverPoint — Authentication'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RecoverPoint — Authentication Methods')))
    lines.append(R(bMid(3, 99, 'RPA admin / monitor roles; LDAP integration; certificate-based inter-RPA auth')))
    lines.append(R(bMid(3, 99, 'Management UI: HTTPS on 443 (mgmt HTTPS) — browser-based login')))
    lines.append(R(bMid(3, 99, 'API: bearer token or service account; rotate credentials quarterly')))
    lines.append(R(bMid(3, 99, 'Inter-component: certificate-based mutual TLS between engines')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Human Access'), bMid(53, 99, 'Machine Access'))))
    lines.append(R(merge(bMid(3, 50, 'AD / LDAP integration'), bMid(53, 99, 'Service account'))))
    lines.append(R(merge(bMid(3, 50, 'SAML SSO optional'), bMid(53, 99, 'API key / token'))))
    lines.append(R(merge(bMid(3, 50, 'MFA via IdP'), bMid(53, 99, 'Certificate auth'))))
    lines.append(R(merge(bMid(3, 50, 'Session timeout 15 min'), bMid(53, 99, 'Rotate every 90 d'))))
    lines.append(R(merge(bMid(3, 50, 'Audit login events'), bMid(53, 99, 'Vault-stored secrets'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('RPA virtual appliances on ESXi · Journal volumes on storage array · WAN link between sites'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPA           = RecoverPoint Appliance — virtual appliance managing journal and replication'))
    lines.append(txt_row('Splitter      = intercepts host I/O at hypervisor or array level; sends copy to RPA'))
    lines.append(txt_row('Journal       = write-order-consistent storage capturing all writes for point-in-time access'))
    lines.append(txt_row('Consistency Group= set of volumes protected together; writes are applied in order across all'))
    lines.append(txt_row('Bookmark      = named marker in journal; enables deterministic recovery to a known state'))
    lines.append(txt_row('Image Access  = mounting a journal point-in-time image to a host for testing or recovery'))
    lines.append(txt_row('Failover      = activating the replica at the recovery site; breaks replication relationship'))
    lines.append(txt_row('Test Copy     = non-disruptive image access for validation without breaking replication'))
    lines.append(txt_row('RPO           = Recovery Point Objective; how much data loss is acceptable; CDP = near-zero'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover to service restored'))
    lines.append(txt_row('Reverse       = after failover, replicates from recovery site back to re-sync production'))
    lines.append(txt_row('Splitter Lag  = delay between host write and journal commit; monitor for replication health'))
    lines.append(txt_row('CDP           = Continuous Data Protection; every write journaled, not just scheduled snaps'))
    lines.append(txt_row('Distributed CG= consistency group spanning volumes on multiple storage arrays'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-recoverpoint-sec-enc',
    'docs/storage/dell/recoverpoint/security/encryption/index.md',
    'RecoverPoint — encryption at rest and in transit',
)
def _dr_recoverpoint_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RecoverPoint — Encryption'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RecoverPoint — Encryption Configuration')))
    lines.append(R(bMid(3, 99, 'AES-256 WAN compression+encryption; data at rest on journal volumes unencrypted by default')))
    lines.append(R(bMid(3, 99, 'In-transit: TLS 1.2+ for all management; data channel also encrypted')))
    lines.append(R(bMid(3, 99, 'At-rest: AES-256 on repository or vault storage; key managed by KMS')))
    lines.append(R(bMid(3, 99, 'Key lifecycle: generate → use → rotate (annual) → retire → destroy')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'In-Transit'), bMid(53, 99, 'At-Rest'))))
    lines.append(R(merge(bMid(3, 50, 'TLS 1.2+ (minimum)'), bMid(53, 99, 'AES-256 encryption'))))
    lines.append(R(merge(bMid(3, 50, '443 (mgmt HTTPS) HTTPS'), bMid(53, 99, 'KMS key management'))))
    lines.append(R(merge(bMid(3, 50, 'Mutual TLS internal'), bMid(53, 99, 'WORM / immutable'))))
    lines.append(R(merge(bMid(3, 50, 'Cert rotation annual'), bMid(53, 99, 'Key rotation annual'))))
    lines.append(R(merge(bMid(3, 50, 'No plain-text admin'), bMid(53, 99, 'Audit key access'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('RPA virtual appliances on ESXi · Journal volumes on storage array · WAN link between sites'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPA           = RecoverPoint Appliance — virtual appliance managing journal and replication'))
    lines.append(txt_row('Splitter      = intercepts host I/O at hypervisor or array level; sends copy to RPA'))
    lines.append(txt_row('Journal       = write-order-consistent storage capturing all writes for point-in-time access'))
    lines.append(txt_row('Consistency Group= set of volumes protected together; writes are applied in order across all'))
    lines.append(txt_row('Bookmark      = named marker in journal; enables deterministic recovery to a known state'))
    lines.append(txt_row('Image Access  = mounting a journal point-in-time image to a host for testing or recovery'))
    lines.append(txt_row('Failover      = activating the replica at the recovery site; breaks replication relationship'))
    lines.append(txt_row('Test Copy     = non-disruptive image access for validation without breaking replication'))
    lines.append(txt_row('RPO           = Recovery Point Objective; how much data loss is acceptable; CDP = near-zero'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover to service restored'))
    lines.append(txt_row('Reverse       = after failover, replicates from recovery site back to re-sync production'))
    lines.append(txt_row('Splitter Lag  = delay between host write and journal commit; monitor for replication health'))
    lines.append(txt_row('CDP           = Continuous Data Protection; every write journaled, not just scheduled snaps'))
    lines.append(txt_row('Distributed CG= consistency group spanning volumes on multiple storage arrays'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-recoverpoint-sec-hardening',
    'docs/storage/dell/recoverpoint/security/hardening/index.md',
    'RecoverPoint — hardening guide, CIS controls, secure configuration',
)
def _dr_recoverpoint_sec_hardening():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RecoverPoint — Hardening'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RecoverPoint — Hardening Checklist')))
    lines.append(R(bMid(3, 99, '  [ ] Disable default/admin accounts; create named admin accounts only')))
    lines.append(R(bMid(3, 99, '  [ ] Enable MFA for all interactive logins via IdP / SAML SSO')))
    lines.append(R(bMid(3, 99, '  [ ] Restrict management port (443 (mgmt HTTPS)) to jump host / management VLAN')))
    lines.append(R(bMid(3, 99, '  [ ] Enable audit logging and forward to SIEM (syslog, TLS port 6514)')))
    lines.append(R(bMid(3, 99, '  [ ] Apply all security patches within 30 days of vendor release')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Network Hardening')))
    lines.append(R(bMid(3, 99, '  [ ] Separate backup VLAN — no direct production host access to repo')))
    lines.append(R(bMid(3, 99, '  [ ] Firewall: allow only 443 (mgmt HTTPS) · 2222 (RPA SSH) · 8888 (splitter API)')))
    lines.append(R(bMid(3, 99, '  [ ] Disable unused ports and protocols on management interface')))
    lines.append(R(bMid(3, 99, '  [ ] Immutable repository: enable WORM or object lock on backup target')))
    lines.append(R(bMid(3, 99, '  [ ] Encryption in transit: disable TLS 1.0/1.1; enforce TLS 1.2+')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('RPA virtual appliances on ESXi · Journal volumes on storage array · WAN link between sites'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPA           = RecoverPoint Appliance — virtual appliance managing journal and replication'))
    lines.append(txt_row('Splitter      = intercepts host I/O at hypervisor or array level; sends copy to RPA'))
    lines.append(txt_row('Journal       = write-order-consistent storage capturing all writes for point-in-time access'))
    lines.append(txt_row('Consistency Group= set of volumes protected together; writes are applied in order across all'))
    lines.append(txt_row('Bookmark      = named marker in journal; enables deterministic recovery to a known state'))
    lines.append(txt_row('Image Access  = mounting a journal point-in-time image to a host for testing or recovery'))
    lines.append(txt_row('Failover      = activating the replica at the recovery site; breaks replication relationship'))
    lines.append(txt_row('Test Copy     = non-disruptive image access for validation without breaking replication'))
    lines.append(txt_row('RPO           = Recovery Point Objective; how much data loss is acceptable; CDP = near-zero'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover to service restored'))
    lines.append(txt_row('Reverse       = after failover, replicates from recovery site back to re-sync production'))
    lines.append(txt_row('Splitter Lag  = delay between host write and journal commit; monitor for replication health'))
    lines.append(txt_row('CDP           = Continuous Data Protection; every write journaled, not just scheduled snaps'))
    lines.append(txt_row('Distributed CG= consistency group spanning volumes on multiple storage arrays'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-recoverpoint-troubleshooting',
    'docs/storage/dell/recoverpoint/troubleshooting/index.md',
    'RecoverPoint — troubleshooting overview and triage approach',
)
def _dr_recoverpoint_troubleshooting():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RecoverPoint — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RecoverPoint — Troubleshooting Approach')))
    lines.append(R(bMid(3, 99, '1  Identify: which job, component, or resource is failing')))
    lines.append(R(bMid(3, 99, '2  Scope: single job vs all jobs; one source vs all sources')))
    lines.append(R(bMid(3, 99, '3  Collect: logs and run status command; review recent change history')))
    lines.append(R(bMid(3, 99, '4  Diagnose: match symptoms to known issues; check error codes')))
    lines.append(R(bMid(3, 99, '5  Fix: apply resolution; verify fix; monitor next run')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Infrastructure'), bMid(36, 66, 'Application'), bMid(69, 99, 'Data'))))
    lines.append(R(merge(bMid(3, 33, 'Network checks'), bMid(36, 66, 'Log analysis'), bMid(69, 99, 'Catalog check'))))
    lines.append(R(merge(bMid(3, 33, 'Storage space'), bMid(36, 66, 'Job error codes'), bMid(69, 99, 'Consistency'))))
    lines.append(R(merge(bMid(3, 33, 'Process health'), bMid(36, 66, 'Auth failures'), bMid(69, 99, 'Corruption scan'))))
    lines.append(R(merge(bMid(3, 33, '443 (mgmt HTTPS)'), bMid(36, 66, 'Timeout errors'), bMid(69, 99, 'Restore test'))))
    lines.append(R(merge(bMid(3, 33, 'Firewall rules'), bMid(36, 66, 'Version compat'), bMid(69, 99, 'RPO drift'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('RPA virtual appliances on ESXi · Journal volumes on storage array · WAN link between sites'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPA           = RecoverPoint Appliance — virtual appliance managing journal and replication'))
    lines.append(txt_row('Splitter      = intercepts host I/O at hypervisor or array level; sends copy to RPA'))
    lines.append(txt_row('Journal       = write-order-consistent storage capturing all writes for point-in-time access'))
    lines.append(txt_row('Consistency Group= set of volumes protected together; writes are applied in order across all'))
    lines.append(txt_row('Bookmark      = named marker in journal; enables deterministic recovery to a known state'))
    lines.append(txt_row('Image Access  = mounting a journal point-in-time image to a host for testing or recovery'))
    lines.append(txt_row('Failover      = activating the replica at the recovery site; breaks replication relationship'))
    lines.append(txt_row('Test Copy     = non-disruptive image access for validation without breaking replication'))
    lines.append(txt_row('RPO           = Recovery Point Objective; how much data loss is acceptable; CDP = near-zero'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover to service restored'))
    lines.append(txt_row('Reverse       = after failover, replicates from recovery site back to re-sync production'))
    lines.append(txt_row('Splitter Lag  = delay between host write and journal commit; monitor for replication health'))
    lines.append(txt_row('CDP           = Continuous Data Protection; every write journaled, not just scheduled snaps'))
    lines.append(txt_row('Distributed CG= consistency group spanning volumes on multiple storage arrays'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-recoverpoint-ts-issues',
    'docs/storage/dell/recoverpoint/troubleshooting/common-issues/index.md',
    'RecoverPoint — common issues, root causes, and fixes',
)
def _dr_recoverpoint_ts_issues():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RecoverPoint — Common Issues'))
    lines.append(txt_row())
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Symptom', 'Likely Cause', 'First Check', 'Fix', 'Verify'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['High lag', 'WAN congestion', 'get compression s', 'throttle or upgra', 'get all rpas'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['CG suspended', 'journal full', 'check journal cap', 'expand journal vo', 'get journal st'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Splitter offline', 'ESXi host restart', 'vSphere events lo', 're-register split', 'get splitter i'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Image stuck', 'stale image acces', 'image access disa', 'force release', 'get all groups'])))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'General Triage Pattern')))
    lines.append(R(bMid(3, 99, '  Is the issue new or recurring? New = recent change; Recurring = config problem')))
    lines.append(R(bMid(3, 99, '  Is it isolated to one source or all? Isolated = agent; All = server/repo')))
    lines.append(R(bMid(3, 99, '  Check logs first: image access enable/disable')))
    lines.append(R(bMid(3, 99, '  If unresolved in 2h: open vendor case with full log bundle')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('RPA virtual appliances on ESXi · Journal volumes on storage array · WAN link between sites'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPA           = RecoverPoint Appliance — virtual appliance managing journal and replication'))
    lines.append(txt_row('Splitter      = intercepts host I/O at hypervisor or array level; sends copy to RPA'))
    lines.append(txt_row('Journal       = write-order-consistent storage capturing all writes for point-in-time access'))
    lines.append(txt_row('Consistency Group= set of volumes protected together; writes are applied in order across all'))
    lines.append(txt_row('Bookmark      = named marker in journal; enables deterministic recovery to a known state'))
    lines.append(txt_row('Image Access  = mounting a journal point-in-time image to a host for testing or recovery'))
    lines.append(txt_row('Failover      = activating the replica at the recovery site; breaks replication relationship'))
    lines.append(txt_row('Test Copy     = non-disruptive image access for validation without breaking replication'))
    lines.append(txt_row('RPO           = Recovery Point Objective; how much data loss is acceptable; CDP = near-zero'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover to service restored'))
    lines.append(txt_row('Reverse       = after failover, replicates from recovery site back to re-sync production'))
    lines.append(txt_row('Splitter Lag  = delay between host write and journal commit; monitor for replication health'))
    lines.append(txt_row('CDP           = Continuous Data Protection; every write journaled, not just scheduled snaps'))
    lines.append(txt_row('Distributed CG= consistency group spanning volumes on multiple storage arrays'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-recoverpoint-ts-diag',
    'docs/storage/dell/recoverpoint/troubleshooting/diagnostics/index.md',
    'RecoverPoint — diagnostic commands and log collection',
)
def _dr_recoverpoint_ts_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RecoverPoint — Diagnostics'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RecoverPoint — Diagnostic Commands')))
    lines.append(R(bMid(3, 99, 'Collect these before opening a vendor support case')))
    lines.append(R(bMid(3, 99, '  image access enable/disable')))
    lines.append(R(bMid(3, 99, '  failover / reverse')))
    lines.append(R(bMid(3, 99, '  Check system logs: /var/log/ or Windows Event Viewer')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Log Collection'), bMid(53, 99, 'Live Diagnostics'))))
    lines.append(R(merge(bMid(3, 50, 'Application log bundle'), bMid(53, 99, 'Network connectivity'))))
    lines.append(R(merge(bMid(3, 50, 'OS syslog (journalctl)'), bMid(53, 99, 'Storage path check'))))
    lines.append(R(merge(bMid(3, 50, 'Core dump if crashed'), bMid(53, 99, 'Process list check'))))
    lines.append(R(merge(bMid(3, 50, 'Config export/backup'), bMid(53, 99, 'Port reachability'))))
    lines.append(R(merge(bMid(3, 50, 'image access enable/disable'), bMid(53, 99, 'failover / reverse'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('RPA virtual appliances on ESXi · Journal volumes on storage array · WAN link between sites'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPA           = RecoverPoint Appliance — virtual appliance managing journal and replication'))
    lines.append(txt_row('Splitter      = intercepts host I/O at hypervisor or array level; sends copy to RPA'))
    lines.append(txt_row('Journal       = write-order-consistent storage capturing all writes for point-in-time access'))
    lines.append(txt_row('Consistency Group= set of volumes protected together; writes are applied in order across all'))
    lines.append(txt_row('Bookmark      = named marker in journal; enables deterministic recovery to a known state'))
    lines.append(txt_row('Image Access  = mounting a journal point-in-time image to a host for testing or recovery'))
    lines.append(txt_row('Failover      = activating the replica at the recovery site; breaks replication relationship'))
    lines.append(txt_row('Test Copy     = non-disruptive image access for validation without breaking replication'))
    lines.append(txt_row('RPO           = Recovery Point Objective; how much data loss is acceptable; CDP = near-zero'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover to service restored'))
    lines.append(txt_row('Reverse       = after failover, replicates from recovery site back to re-sync production'))
    lines.append(txt_row('Splitter Lag  = delay between host write and journal commit; monitor for replication health'))
    lines.append(txt_row('CDP           = Continuous Data Protection; every write journaled, not just scheduled snaps'))
    lines.append(txt_row('Distributed CG= consistency group spanning volumes on multiple storage arrays'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-recoverpoint-ts-escalation',
    'docs/storage/dell/recoverpoint/troubleshooting/escalation/index.md',
    'RecoverPoint — escalation path, vendor support, and SLA',
)
def _dr_recoverpoint_ts_escalation():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RecoverPoint — Escalation'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RecoverPoint — Escalation Path')))
    lines.append(R(bMid(3, 99, 'L1 Triage: review logs, match to known issues in runbook (0–30 min)')))
    lines.append(R(bMid(3, 99, 'L2 Engineering: deep analysis, config review, lab reproduction (30 min – 4 h)')))
    lines.append(R(bMid(3, 99, 'Vendor Support: open case with log bundle if unresolved at L2 (> 4 h)')))
    lines.append(R(bMid(3, 99, 'Sev1 (data loss / production impact): page on-call + open critical case')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Information to Collect Before Escalating')))
    lines.append(R(bMid(3, 99, '  Product version: RecoverPoint version string from About / version command')))
    lines.append(R(bMid(3, 99, '  Full log bundle: image access enable/disable')))
    lines.append(R(bMid(3, 99, '  Symptom timeline: when first occurred; any changes made')))
    lines.append(R(bMid(3, 99, '  Scope: single job / all jobs / all components — narrows root cause')))
    lines.append(R(bMid(3, 99, '  Error codes: exact error messages and exit codes from logs')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('RPA virtual appliances on ESXi · Journal volumes on storage array · WAN link between sites'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPA           = RecoverPoint Appliance — virtual appliance managing journal and replication'))
    lines.append(txt_row('Splitter      = intercepts host I/O at hypervisor or array level; sends copy to RPA'))
    lines.append(txt_row('Journal       = write-order-consistent storage capturing all writes for point-in-time access'))
    lines.append(txt_row('Consistency Group= set of volumes protected together; writes are applied in order across all'))
    lines.append(txt_row('Bookmark      = named marker in journal; enables deterministic recovery to a known state'))
    lines.append(txt_row('Image Access  = mounting a journal point-in-time image to a host for testing or recovery'))
    lines.append(txt_row('Failover      = activating the replica at the recovery site; breaks replication relationship'))
    lines.append(txt_row('Test Copy     = non-disruptive image access for validation without breaking replication'))
    lines.append(txt_row('RPO           = Recovery Point Objective; how much data loss is acceptable; CDP = near-zero'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover to service restored'))
    lines.append(txt_row('Reverse       = after failover, replicates from recovery site back to re-sync production'))
    lines.append(txt_row('Splitter Lag  = delay between host write and journal commit; monitor for replication health'))
    lines.append(txt_row('CDP           = Continuous Data Protection; every write journaled, not just scheduled snaps'))
    lines.append(txt_row('Distributed CG= consistency group spanning volumes on multiple storage arrays'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines


@kb_diagram(
    'dr-srdf-a',
    'docs/storage/dell/srdf-a/index.md',
    'Asynchronous replication for PowerMax/VMAX — delta-set cycle-based RPO in seconds',
)
def _dr_srdf_a_overview():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Overview'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/A')))
    lines.append(R(bMid(3, 99, 'Asynchronous replication for PowerMax/VMAX — delta-set cycle-based RPO in seconds')))
    lines.append(R(bMid(3, 99, 'R1 Volume (Source)  — primary data on production PowerMax; host writes here')))
    lines.append(R(bMid(3, 99, 'R2 Volume (Target)  — replica on DR PowerMax; receives delta sets asynchronously')))
    lines.append(R(bMid(3, 99, 'SRDF/A Engine       — delta-set formation: groups writes per cycle, ships to R2')))
    lines.append(R(bMid(3, 99, 'Management: FC dark fiber / DWDM · Auth: Symmetrix/PowerMax admin credentials; Solutions En')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Architecture: components work together to deliver SRDF/A capabilities'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Architecture'), bMid(53, 99, 'Operations'))))
    lines.append(R(merge(bMid(3, 50, 'R1 Volume (Source)  — primary data on produ'), bMid(53, 99, 'symrdf establish'))))
    lines.append(R(merge(bMid(3, 50, 'R2 Volume (Target)  — replica on DR PowerMa'), bMid(53, 99, 'symrdf failover / failback'))))
    lines.append(R(merge(bMid(3, 50, 'SRDF/A Engine       — delta-set formation: '), bMid(53, 99, 'symrdf query'))))
    lines.append(R(merge(bMid(3, 50, 'PowerMax Mgmt       — Unisphere for PowerMa'), bMid(53, 99, 'symrdf suspend / resume'))))
    lines.append(R(merge(bMid(3, 50, 'SRDF Link           — dedicated FC or FCIP '), bMid(53, 99, 'symrdf verify'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-architecture',
    'docs/storage/dell/srdf-a/architecture/index.md',
    'SRDF/A — architecture overview, components, data flow',
)
def _dr_srdf_a_architecture():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Architecture'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/A — Component Architecture')))
    lines.append(R(bMid(3, 99, 'R1 Volume (Source)  — primary data on production PowerMax; host writes here')))
    lines.append(R(bMid(3, 99, 'R2 Volume (Target)  — replica on DR PowerMax; receives delta sets asynchronously')))
    lines.append(R(bMid(3, 99, 'SRDF/A Engine       — delta-set formation: groups writes per cycle, ships to R2')))
    lines.append(R(bMid(3, 99, 'Ports: FC dark fiber / DWDM · FCIP (TCP 3225) · 9443 (Unisphere HTTPS)')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Three-tier component model — control plane, data plane, and management'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Control Plane'), bMid(36, 66, 'Data Plane'), bMid(69, 99, 'Management'))))
    lines.append(R(merge(bMid(3, 33, 'R1 Volume (Source)  — primar'), bMid(36, 66, 'R2 Volume (Target)  — replic'), bMid(69, 99, 'PowerMax Mgmt       — Unisph'))))
    lines.append(R(merge(bMid(3, 33, 'Scheduling'), bMid(36, 66, 'Replication/Backup'), bMid(69, 99, 'FC dark fiber / DWDM'))))
    lines.append(R(merge(bMid(3, 33, 'Policy mgmt'), bMid(36, 66, 'Data movement'), bMid(69, 99, 'REST API'))))
    lines.append(R(merge(bMid(3, 33, 'Catalog/DB'), bMid(36, 66, 'Dedup/compress'), bMid(69, 99, 'RBAC'))))
    lines.append(R(merge(bMid(3, 33, 'Job engine'), bMid(36, 66, 'FCIP (TCP 3225)'), bMid(69, 99, 'Alerting'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-arch-how-it-works',
    'docs/storage/dell/srdf-a/architecture/how-it-works/index.md',
    'SRDF/A — how replication or backup data flows step by step',
)
def _dr_srdf_a_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('  SRDF/A data flow — from source to target through the protection pipeline:'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, '1  Source / Production System')))
    lines.append(R(bMid(3, 99, '   R1 Volume (Source)  — primary data on production PowerMax; host writes here')))
    lines.append(R(bMid(3, 99, '   Host writes are intercepted or snapshotted by the SRDF/A agent/proxy')))
    lines.append(R(bMid(3, 99, '   Changed blocks tracked via CBT / journal / delta-set mechanism')))
    lines.append(R(bMid(3, 99, '   Consistency ensured at quiesce point before data transfer begins')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Changed data forwarded to the SRDF/A engine — compression and encryption applied in transit'))
    lines.append(txt_row())
    lines.append(R(arrow([51])))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, '2  SRDF/A Engine')))
    lines.append(R(bMid(3, 99, '   R2 Volume (Target)  — replica on DR PowerMax; receives delta sets asynchronously')))
    lines.append(R(bMid(3, 99, '   Data compressed, deduplicated, and encrypted before storage')))
    lines.append(R(bMid(3, 99, '   Metadata catalog updated; job status reported to control plane')))
    lines.append(R(bMid(3, 99, '   symrdf establish')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([51])))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, '3  Target / Repository')))
    lines.append(R(bMid(3, 99, '   SRDF/A Engine       — delta-set formation: groups writes per cycle, ships to R2')))
    lines.append(R(bMid(3, 99, '   Recovery point written; retention policy applied automatically')))
    lines.append(R(bMid(3, 99, '   Restore: symrdf failover / failback')))
    lines.append(R(bMid(3, 99, '   RTO driven by target storage performance and data volume')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-arch-design',
    'docs/storage/dell/srdf-a/architecture/design-standards/index.md',
    'SRDF/A — sizing, design rules, capacity, HA guidelines',
)
def _dr_srdf_a_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Design Standards'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Sizing Guidelines'), bMid(53, 99, 'HA Requirements'))))
    lines.append(R(merge(bMid(3, 50, 'Deduplicate where supported'), bMid(53, 99, 'N+1 component redundancy'))))
    lines.append(R(merge(bMid(3, 50, 'Bandwidth: 10 GbE minimum'), bMid(53, 99, 'Heartbeat / health monitor'))))
    lines.append(R(merge(bMid(3, 50, 'Storage: 130% of raw data'), bMid(53, 99, 'Separate mgmt / data VLANs'))))
    lines.append(R(merge(bMid(3, 50, 'Latency: < 10 ms to storage'), bMid(53, 99, 'Out-of-band access (IPMI)'))))
    lines.append(R(merge(bMid(3, 50, 'CPU: 8+ vCPU for engine'), bMid(53, 99, 'Anti-affinity VM placement'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('  Ports: FC dark fiber / DWDM · FCIP (TCP 3225) · 9443 (Unisphere HTTPS)'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Standard SRDF/A Design Rules')))
    lines.append(R(bMid(3, 99, 'RPO target drives snapshot/cycle frequency — document in service design')))
    lines.append(R(bMid(3, 99, 'RTO target drives recovery tier: instant, warm standby, or cold restore')))
    lines.append(R(bMid(3, 99, 'Dedicated backup network VLAN — no shared production traffic')))
    lines.append(R(bMid(3, 99, 'Encryption: SRDF at FA/RF port level; Unisphere HTTPS; Solutions Enabler TLS')))
    lines.append(R(bMid(3, 99, 'Service accounts: minimum privilege; rotate credentials quarterly')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-arch-integrations',
    'docs/storage/dell/srdf-a/architecture/integrations/index.md',
    'SRDF/A — integration points with external systems and APIs',
)
def _dr_srdf_a_arch_integrations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Architecture Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/A — External Integration Points')))
    lines.append(R(bMid(3, 99, 'Auth: Symmetrix/PowerMax admin credentials; Solutions Enabler (SYMAPI); role-based Unisphere')))
    lines.append(R(bMid(3, 99, 'Storage: connected via FC dark fiber / DWDM · FCIP (TCP 3225)')))
    lines.append(R(bMid(3, 99, 'Monitoring: SNMP traps / syslog / REST API to ITSM and alerting systems')))
    lines.append(R(bMid(3, 99, 'Encryption: SRDF encryption at the FA/RF port level; Unisphere HTTPS; SE service TLS')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Identity'), bMid(36, 66, 'Storage'), bMid(69, 99, 'Monitoring'))))
    lines.append(R(merge(bMid(3, 33, 'AD / LDAP'), bMid(36, 66, 'FC dark fiber / DWDM'), bMid(69, 99, 'SNMP / syslog'))))
    lines.append(R(merge(bMid(3, 33, 'SAML SSO'), bMid(36, 66, 'FCIP (TCP 3225)'), bMid(69, 99, 'REST webhook'))))
    lines.append(R(merge(bMid(3, 33, 'RBAC roles'), bMid(36, 66, 'NFS / iSCSI / FC'), bMid(69, 99, 'Email alerts'))))
    lines.append(R(merge(bMid(3, 33, 'MFA optional'), bMid(36, 66, 'Dedup appliance'), bMid(69, 99, 'ServiceNow'))))
    lines.append(R(merge(bMid(3, 33, 'Cert auth'), bMid(36, 66, 'Object storage'), bMid(69, 99, 'Prometheus'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-operations',
    'docs/storage/dell/srdf-a/operations/index.md',
    'SRDF/A — operations overview, key tasks, day-to-day procedures',
)
def _dr_srdf_a_operations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/A — Day-to-Day Operations')))
    lines.append(R(bMid(3, 99, 'Daily: review job status · check health alerts · verify last backup/replica')))
    lines.append(R(bMid(3, 99, 'Weekly: review capacity trends · test restore sample · review error logs')))
    lines.append(R(bMid(3, 99, 'Monthly: full restore test · review retention · audit service accounts')))
    lines.append(R(bMid(3, 99, 'Quarterly: DR failover test · firmware review · update documentation')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Backup/Replicate'), bMid(36, 66, 'Monitor'), bMid(69, 99, 'Recover'))))
    lines.append(R(merge(bMid(3, 33, 'symrdf establish'), bMid(36, 66, 'symrdf query'), bMid(69, 99, 'symrdf failover / failback'))))
    lines.append(R(merge(bMid(3, 33, 'Schedule jobs'), bMid(36, 66, 'Health checks'), bMid(69, 99, 'Instant restore'))))
    lines.append(R(merge(bMid(3, 33, 'Retention mgmt'), bMid(36, 66, 'Capacity alerts'), bMid(69, 99, 'Failover test'))))
    lines.append(R(merge(bMid(3, 33, 'Consistency grp'), bMid(36, 66, 'Log review'), bMid(69, 99, 'DR runbook'))))
    lines.append(R(merge(bMid(3, 33, 'Policy updates'), bMid(36, 66, 'SLA tracking'), bMid(69, 99, 'Validate RTO'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-ops-backup',
    'docs/storage/dell/srdf-a/operations/backup-restore/index.md',
    'SRDF/A — backup and restore procedures',
)
def _dr_srdf_a_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Backup & Restore'))
    lines.append(txt_row())
    lines.append(txt_row('  Backup flow: quiesce source → snapshot/copy → transfer → write to target → catalog'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Backup (Protection)'), bMid(53, 99, 'Restore (Recovery)'))))
    lines.append(R(merge(bMid(3, 50, 'symrdf establish'), bMid(53, 99, 'symrdf failover / failback'))))
    lines.append(R(merge(bMid(3, 50, 'Quiesce source I/O'), bMid(53, 99, 'Select recovery point'))))
    lines.append(R(merge(bMid(3, 50, 'Take snapshot / CBT'), bMid(53, 99, 'Mount or copy to target'))))
    lines.append(R(merge(bMid(3, 50, 'Transfer changed blocks'), bMid(53, 99, 'Validate integrity'))))
    lines.append(R(merge(bMid(3, 50, 'Commit to repository'), bMid(53, 99, 'Restart application'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Key SRDF/A Commands')))
    lines.append(R(bMid(3, 99, '  Backup trigger  : symrdf establish')))
    lines.append(R(bMid(3, 99, '  List points     : symrdf failover / failback')))
    lines.append(R(bMid(3, 99, '  Health status   : symrdf query')))
    lines.append(R(bMid(3, 99, '  Retention mgmt  : symrdf verify')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-ops-cli',
    'docs/storage/dell/srdf-a/operations/cli-reference/index.md',
    'SRDF/A — CLI commands reference',
)
def _dr_srdf_a_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — CLI Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/A — Command Reference')))
    lines.append(R(bMid(3, 99, 'Use these commands for routine operations, scripting, and troubleshooting')))
    lines.append(R(bMid(3, 99, '  symrdf establish')))
    lines.append(R(bMid(3, 99, '  symrdf failover / failback')))
    lines.append(R(bMid(3, 99, '  symrdf query')))
    lines.append(R(bMid(3, 99, '  symrdf suspend / resume')))
    lines.append(R(bMid(3, 99, '  symrdf verify')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Ports: FC dark fiber / DWDM · FCIP (TCP 3225) · 9443 (Unisphere HTTPS)'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Command Categories')))
    lines.append(R(bMid(3, 99, '  Status / Query  — check current state, list jobs, show config')))
    lines.append(R(bMid(3, 99, '  Operations      — start, stop, failover, restore, sync, expire')))
    lines.append(R(bMid(3, 99, '  Configuration   — add/modify policies, schedules, storage targets')))
    lines.append(R(bMid(3, 99, '  Diagnostics     — collect logs, run health checks, test connectivity')))
    lines.append(R(bMid(3, 99, '  Scripting       — REST API or CLI for automation and reporting')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-ops-health',
    'docs/storage/dell/srdf-a/operations/health-checks/index.md',
    'SRDF/A — health check procedures and monitoring commands',
)
def _dr_srdf_a_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Health Checks'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/A — Health Check Procedures')))
    lines.append(R(bMid(3, 99, 'Run these checks daily/weekly to confirm protection is working')))
    lines.append(R(bMid(3, 99, '  symrdf query')))
    lines.append(R(bMid(3, 99, '  Review job completion rate — target 100%; investigate failures')))
    lines.append(R(bMid(3, 99, '  Check replication/backup lag against RPO target')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Check', 'What to verify', 'Expected', 'Frequency', 'Action if bad'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Job status', 'All jobs complete', '100% success', 'Daily', 'Triage failures'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Lag / RPO', 'Replication lag', '< RPO target', 'Daily', 'Tune bandwidth'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Capacity', 'Repo space used', '< 80% full', 'Weekly', 'Expand or expire'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Restore test', 'Random restore', 'Data intact', 'Monthly', 'Fix backup chain'])))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-ops-install',
    'docs/storage/dell/srdf-a/operations/install-upgrade/index.md',
    'SRDF/A — install and upgrade procedures',
)
def _dr_srdf_a_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Install & Upgrade'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/A — Installation Prerequisites')))
    lines.append(R(bMid(3, 99, '  OS: supported Linux or Windows Server (see vendor compatibility matrix)')))
    lines.append(R(bMid(3, 99, '  Network: FC dark fiber / DWDM · FCIP (TCP 3225) — ensure firewall allows these')))
    lines.append(R(bMid(3, 99, '  Auth: Symmetrix/PowerMax admin credentials; Solutions Enabler (SYMAPI); role-based Unisphere')))
    lines.append(R(bMid(3, 99, '  Storage: Two PowerMax arrays (prod + DR) · FC/FCIP SRDF link (dedicated bandwidth)')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([51])))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Install Sequence')))
    lines.append(R(bMid(3, 99, '  1  Deploy control plane component and configure network access')))
    lines.append(R(bMid(3, 99, '  2  Configure storage and network connectivity')))
    lines.append(R(bMid(3, 99, '  3  Install agent/proxy/splitter on protected hosts')))
    lines.append(R(bMid(3, 99, '  4  Register sources and configure protection policies')))
    lines.append(R(bMid(3, 99, '  5  Run first job; verify completion; test restore')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Upgrade Sequence')))
    lines.append(R(bMid(3, 99, '  1  Review release notes and compatibility matrix before upgrade')))
    lines.append(R(bMid(3, 99, '  2  Snapshot or backup the control plane VM before upgrading')))
    lines.append(R(bMid(3, 99, '  3  Upgrade control plane first, then proxies/agents/appliances')))
    lines.append(R(bMid(3, 99, '  4  Validate jobs resume automatically after upgrade')))
    lines.append(R(bMid(3, 99, '  5  Document version change and update CMDB record')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-ops-procedures',
    'docs/storage/dell/srdf-a/operations/procedures/index.md',
    'SRDF/A — operational procedures and runbooks',
)
def _dr_srdf_a_ops_procedures():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Procedures'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Routine Procedures'), bMid(53, 99, 'DR Procedures'))))
    lines.append(R(merge(bMid(3, 50, 'Add new protection source'), bMid(53, 99, 'Initiate failover'))))
    lines.append(R(merge(bMid(3, 50, 'Modify retention policy'), bMid(53, 99, 'Validate replica'))))
    lines.append(R(merge(bMid(3, 50, 'Expire old recover points'), bMid(53, 99, 'Redirect host I/O'))))
    lines.append(R(merge(bMid(3, 50, 'Add storage capacity'), bMid(53, 99, 'Test failover (non-disrupt)'))))
    lines.append(R(merge(bMid(3, 50, 'Service account rotation'), bMid(53, 99, 'Failback to production'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Change Control Requirements for SRDF/A')))
    lines.append(R(bMid(3, 99, '  All changes to protection policies require change ticket with rollback plan')))
    lines.append(R(bMid(3, 99, '  Failover tests must be scheduled in maintenance window')))
    lines.append(R(bMid(3, 99, '  Firmware/software upgrades need 48 h pre-approval and backup snapshot')))
    lines.append(R(bMid(3, 99, '  Post-change: verify jobs run successfully for 2 backup cycles')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-ops-scripts',
    'docs/storage/dell/srdf-a/operations/scripts/index.md',
    'SRDF/A — automation scripts and examples',
)
def _dr_srdf_a_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Scripts'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/A — Automation Scripts')))
    lines.append(R(bMid(3, 99, 'Scripts automate routine SRDF/A operations — run via cron or CI/CD')))
    lines.append(R(bMid(3, 99, 'Always store credentials in vault (not in script); log all output')))
    lines.append(R(bMid(3, 99, 'Test scripts in non-production before scheduling in production')))
    lines.append(R(bMid(3, 99, 'Scope scripts to least-privilege service account')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Status / Reporting Scripts'), bMid(53, 99, 'Automation Scripts'))))
    lines.append(R(merge(bMid(3, 50, 'Job success rate report'), bMid(53, 99, 'Auto-expire old points'))))
    lines.append(R(merge(bMid(3, 50, 'Capacity trending'), bMid(53, 99, 'Auto-add new VMs to policy'))))
    lines.append(R(merge(bMid(3, 50, 'SLA compliance report'), bMid(53, 99, 'Nightly DR test validation'))))
    lines.append(R(merge(bMid(3, 50, 'RPO / RTO dashboard'), bMid(53, 99, 'Alert on job failure'))))
    lines.append(R(merge(bMid(3, 50, 'symrdf query'), bMid(53, 99, 'symrdf suspend / resume'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-security',
    'docs/storage/dell/srdf-a/security/index.md',
    'SRDF/A — security overview, controls, compliance posture',
)
def _dr_srdf_a_security():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Security'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/A — Security Posture')))
    lines.append(R(bMid(3, 99, 'Authentication: PowerMax admin creds; Solutions Enabler (SYMAPI); role-based Unisphere')))
    lines.append(R(bMid(3, 99, 'Encryption: SRDF encryption at the FA/RF port level; Unisphere HTTPS; SE service TLS')))
    lines.append(R(bMid(3, 99, 'Network: management VLAN separated; 9443 (Unisphere HTTPS) management port')))
    lines.append(R(bMid(3, 99, 'Audit: all admin actions logged; log retention minimum 1 year')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Access Control'), bMid(36, 66, 'Encryption'), bMid(69, 99, 'Audit'))))
    lines.append(R(merge(bMid(3, 33, 'RBAC roles'), bMid(36, 66, 'AES-256 at rest'), bMid(69, 99, 'Admin actions'))))
    lines.append(R(merge(bMid(3, 33, 'Least privilege'), bMid(36, 66, 'TLS in transit'), bMid(69, 99, 'Login events'))))
    lines.append(R(merge(bMid(3, 33, 'MFA optional'), bMid(36, 66, 'Key rotation'), bMid(69, 99, 'Syslog export'))))
    lines.append(R(merge(bMid(3, 33, 'SVC acct rotate'), bMid(36, 66, 'WORM / immutable'), bMid(69, 99, 'SIEM forward'))))
    lines.append(R(merge(bMid(3, 33, 'Just-In-Time'), bMid(36, 66, 'KMS managed'), bMid(69, 99, 'Quarterly review'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-sec-access',
    'docs/storage/dell/srdf-a/security/access-control/index.md',
    'SRDF/A — RBAC, permissions, service accounts',
)
def _dr_srdf_a_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Access Control'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/A — RBAC and Access Control')))
    lines.append(R(bMid(3, 99, 'Auth: Symmetrix/PowerMax admin credentials; Solutions Enabler (SYMAPI); role-based Unisphere')))
    lines.append(R(bMid(3, 99, 'Principle of least privilege: each role gets only required permissions')))
    lines.append(R(bMid(3, 99, 'Service accounts: dedicated, non-interactive; rotation every 90 days')))
    lines.append(R(bMid(3, 99, 'Emergency break-glass: documented, monitored, time-limited access')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Role', 'Access Level', 'Typical User', 'Review Freq', 'Granted By'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Admin', 'Full config/ops', 'Sr Backup Eng', 'Quarterly', 'Security team'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Operator', 'Start/stop jobs', 'Backup Eng', 'Quarterly', 'Team lead'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Monitor', 'Read-only view', 'NOC / L1', 'Quarterly', 'Team lead'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Service Acct', 'API / headless', 'Automation', 'Per rotation', 'Security team'])))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-sec-auth',
    'docs/storage/dell/srdf-a/security/authentication/index.md',
    'SRDF/A — authentication methods, certificate management',
)
def _dr_srdf_a_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Authentication'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/A — Authentication Methods')))
    lines.append(R(bMid(3, 99, 'Symmetrix/PowerMax admin credentials; Solutions Enabler (SYMAPI); role-based Unisphere')))
    lines.append(R(bMid(3, 99, 'Management UI: HTTPS on FC dark fiber / DWDM — browser-based login')))
    lines.append(R(bMid(3, 99, 'API: bearer token or service account; rotate credentials quarterly')))
    lines.append(R(bMid(3, 99, 'Inter-component: certificate-based mutual TLS between engines')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Human Access'), bMid(53, 99, 'Machine Access'))))
    lines.append(R(merge(bMid(3, 50, 'AD / LDAP integration'), bMid(53, 99, 'Service account'))))
    lines.append(R(merge(bMid(3, 50, 'SAML SSO optional'), bMid(53, 99, 'API key / token'))))
    lines.append(R(merge(bMid(3, 50, 'MFA via IdP'), bMid(53, 99, 'Certificate auth'))))
    lines.append(R(merge(bMid(3, 50, 'Session timeout 15 min'), bMid(53, 99, 'Rotate every 90 d'))))
    lines.append(R(merge(bMid(3, 50, 'Audit login events'), bMid(53, 99, 'Vault-stored secrets'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-sec-enc',
    'docs/storage/dell/srdf-a/security/encryption/index.md',
    'SRDF/A — encryption at rest and in transit',
)
def _dr_srdf_a_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Encryption'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/A — Encryption Configuration')))
    lines.append(R(bMid(3, 99, 'SRDF encryption at the FA/RF port level; Unisphere HTTPS; SE service TLS')))
    lines.append(R(bMid(3, 99, 'In-transit: TLS 1.2+ for all management; data channel also encrypted')))
    lines.append(R(bMid(3, 99, 'At-rest: AES-256 on repository or vault storage; key managed by KMS')))
    lines.append(R(bMid(3, 99, 'Key lifecycle: generate → use → rotate (annual) → retire → destroy')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'In-Transit'), bMid(53, 99, 'At-Rest'))))
    lines.append(R(merge(bMid(3, 50, 'TLS 1.2+ (minimum)'), bMid(53, 99, 'AES-256 encryption'))))
    lines.append(R(merge(bMid(3, 50, 'FC dark fiber / DWDM HTTPS'), bMid(53, 99, 'KMS key management'))))
    lines.append(R(merge(bMid(3, 50, 'Mutual TLS internal'), bMid(53, 99, 'WORM / immutable'))))
    lines.append(R(merge(bMid(3, 50, 'Cert rotation annual'), bMid(53, 99, 'Key rotation annual'))))
    lines.append(R(merge(bMid(3, 50, 'No plain-text admin'), bMid(53, 99, 'Audit key access'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-sec-hardening',
    'docs/storage/dell/srdf-a/security/hardening/index.md',
    'SRDF/A — hardening guide, CIS controls, secure configuration',
)
def _dr_srdf_a_sec_hardening():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Hardening'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/A — Hardening Checklist')))
    lines.append(R(bMid(3, 99, '  [ ] Disable default/admin accounts; create named admin accounts only')))
    lines.append(R(bMid(3, 99, '  [ ] Enable MFA for all interactive logins via IdP / SAML SSO')))
    lines.append(R(bMid(3, 99, '  [ ] Restrict management port (FC dark fiber / DWDM) to jump host / management VLAN')))
    lines.append(R(bMid(3, 99, '  [ ] Enable audit logging and forward to SIEM (syslog, TLS port 6514)')))
    lines.append(R(bMid(3, 99, '  [ ] Apply all security patches within 30 days of vendor release')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Network Hardening')))
    lines.append(R(bMid(3, 99, '  [ ] Separate backup VLAN — no direct production host access to repo')))
    lines.append(R(bMid(3, 99, '  [ ] Firewall: allow only FC dark fiber / DWDM · FCIP (TCP 3225) · 9443 (Unisphere HTTPS)')))
    lines.append(R(bMid(3, 99, '  [ ] Disable unused ports and protocols on management interface')))
    lines.append(R(bMid(3, 99, '  [ ] Immutable repository: enable WORM or object lock on backup target')))
    lines.append(R(bMid(3, 99, '  [ ] Encryption in transit: disable TLS 1.0/1.1; enforce TLS 1.2+')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-troubleshooting',
    'docs/storage/dell/srdf-a/troubleshooting/index.md',
    'SRDF/A — troubleshooting overview and triage approach',
)
def _dr_srdf_a_troubleshooting():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/A — Troubleshooting Approach')))
    lines.append(R(bMid(3, 99, '1  Identify: which job, component, or resource is failing')))
    lines.append(R(bMid(3, 99, '2  Scope: single job vs all jobs; one source vs all sources')))
    lines.append(R(bMid(3, 99, '3  Collect: logs and run status command; review recent change history')))
    lines.append(R(bMid(3, 99, '4  Diagnose: match symptoms to known issues; check error codes')))
    lines.append(R(bMid(3, 99, '5  Fix: apply resolution; verify fix; monitor next run')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Infrastructure'), bMid(36, 66, 'Application'), bMid(69, 99, 'Data'))))
    lines.append(R(merge(bMid(3, 33, 'Network checks'), bMid(36, 66, 'Log analysis'), bMid(69, 99, 'Catalog check'))))
    lines.append(R(merge(bMid(3, 33, 'Storage space'), bMid(36, 66, 'Job error codes'), bMid(69, 99, 'Consistency'))))
    lines.append(R(merge(bMid(3, 33, 'Process health'), bMid(36, 66, 'Auth failures'), bMid(69, 99, 'Corruption scan'))))
    lines.append(R(merge(bMid(3, 33, 'FC dark fiber / DWDM'), bMid(36, 66, 'Timeout errors'), bMid(69, 99, 'Restore test'))))
    lines.append(R(merge(bMid(3, 33, 'Firewall rules'), bMid(36, 66, 'Version compat'), bMid(69, 99, 'RPO drift'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-ts-issues',
    'docs/storage/dell/srdf-a/troubleshooting/common-issues/index.md',
    'SRDF/A — common issues, root causes, and fixes',
)
def _dr_srdf_a_ts_issues():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Common Issues'))
    lines.append(txt_row())
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Symptom', 'Likely Cause', 'First Check', 'Fix', 'Verify'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['High RPO', 'cycle time exceed', 'symrdf query -cyc', 'increase bandwidt', 'symrdf -v'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Link down', 'RF port failure', 'symrdf query stat', 'failover ports', 'symcfg list -r'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Pair invalid', 'R1/R2 mismatch', 'symrdf verify', 're-establish pair', 'symrdf establi'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Failover fail', 'R2 not ready', 'check R2 state', 'split then failov', 'symrdf -sid'])))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'General Triage Pattern')))
    lines.append(R(bMid(3, 99, '  Is the issue new or recurring? New = recent change; Recurring = config problem')))
    lines.append(R(bMid(3, 99, '  Is it isolated to one source or all? Isolated = agent; All = server/repo')))
    lines.append(R(bMid(3, 99, '  Check logs first: symrdf query')))
    lines.append(R(bMid(3, 99, '  If unresolved in 2h: open vendor case with full log bundle')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-ts-diag',
    'docs/storage/dell/srdf-a/troubleshooting/diagnostics/index.md',
    'SRDF/A — diagnostic commands and log collection',
)
def _dr_srdf_a_ts_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Diagnostics'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/A — Diagnostic Commands')))
    lines.append(R(bMid(3, 99, 'Collect these before opening a vendor support case')))
    lines.append(R(bMid(3, 99, '  symrdf query')))
    lines.append(R(bMid(3, 99, '  symrdf suspend / resume')))
    lines.append(R(bMid(3, 99, '  Check system logs: /var/log/ or Windows Event Viewer')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Log Collection'), bMid(53, 99, 'Live Diagnostics'))))
    lines.append(R(merge(bMid(3, 50, 'Application log bundle'), bMid(53, 99, 'Network connectivity'))))
    lines.append(R(merge(bMid(3, 50, 'OS syslog (journalctl)'), bMid(53, 99, 'Storage path check'))))
    lines.append(R(merge(bMid(3, 50, 'Core dump if crashed'), bMid(53, 99, 'Process list check'))))
    lines.append(R(merge(bMid(3, 50, 'Config export/backup'), bMid(53, 99, 'Port reachability'))))
    lines.append(R(merge(bMid(3, 50, 'symrdf query'), bMid(53, 99, 'symrdf suspend / resume'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-a-ts-escalation',
    'docs/storage/dell/srdf-a/troubleshooting/escalation/index.md',
    'SRDF/A — escalation path, vendor support, and SLA',
)
def _dr_srdf_a_ts_escalation():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/A — Escalation'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/A — Escalation Path')))
    lines.append(R(bMid(3, 99, 'L1 Triage: review logs, match to known issues in runbook (0–30 min)')))
    lines.append(R(bMid(3, 99, 'L2 Engineering: deep analysis, config review, lab reproduction (30 min – 4 h)')))
    lines.append(R(bMid(3, 99, 'Vendor Support: open case with log bundle if unresolved at L2 (> 4 h)')))
    lines.append(R(bMid(3, 99, 'Sev1 (data loss / production impact): page on-call + open critical case')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Information to Collect Before Escalating')))
    lines.append(R(bMid(3, 99, '  Product version: SRDF/A version string from About / version command')))
    lines.append(R(bMid(3, 99, '  Full log bundle: symrdf query')))
    lines.append(R(bMid(3, 99, '  Symptom timeline: when first occurred; any changes made')))
    lines.append(R(bMid(3, 99, '  Scope: single job / all jobs / all components — narrows root cause')))
    lines.append(R(bMid(3, 99, '  Error codes: exact error messages and exit codes from logs')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays (production + DR site) · FC/FCIP SRDF link (dedicated bandwidth) · RF ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF          = Symmetrix Remote Data Facility; EMC array-based replication technology'))
    lines.append(txt_row('R1            = source SRDF volume on production array; host writes flow here'))
    lines.append(txt_row('R2            = target SRDF volume on DR array; receives replicated data asynchronously'))
    lines.append(txt_row('Delta Set     = batch of host writes accumulated per SRDF/A cycle; shipped to R2 atomically'))
    lines.append(txt_row('Cycle Time    = SRDF/A replication interval (15–60 seconds); determines maximum RPO'))
    lines.append(txt_row('symrdf        = Solutions Enabler CLI for SRDF operations: establish, split, failover, restore'))
    lines.append(txt_row('SRDF Link     = FC or FCIP path between R1 and R2 arrays; dedicated, monitored bandwidth'))
    lines.append(txt_row('Suspended     = SRDF pair state where replication is paused; R2 data frozen at last cycle'))
    lines.append(txt_row('Failover      = SRDF operation making R2 read-write; R1 becomes Not Ready to hosts'))
    lines.append(txt_row('Restore       = after failover resolution, re-establishes replication with R1 as source'))
    lines.append(txt_row('Establish     = initial sync or re-sync operation that copies R1 to R2 in full'))
    lines.append(txt_row('Split         = breaks SRDF pair temporarily; both R1 and R2 are R/W; no replication'))
    lines.append(txt_row('FCIP          = Fibre Channel over IP; tunnels FC SRDF traffic over IP WAN link'))
    lines.append(txt_row('Unisphere     = Dell PowerMax management GUI; REST API; array health and provisioning'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines


@kb_diagram(
    'dr-srdf-s',
    'docs/storage/dell/srdf-s/index.md',
    'Synchronous replication for PowerMax/VMAX — RPO=0, write not acknowledged until R2 confirms',
)
def _dr_srdf_s_overview():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Overview'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/S')))
    lines.append(R(bMid(3, 99, 'Synchronous replication for PowerMax/VMAX — RPO=0, write not acknowledged until R2 confirms')))
    lines.append(R(bMid(3, 99, 'R1 Volume (Source)  — production PowerMax; write holds until R2 acknowledges')))
    lines.append(R(bMid(3, 99, 'R2 Volume (Target)  — DR PowerMax; must confirm write before host I/O completes')))
    lines.append(R(bMid(3, 99, 'SRDF/S Engine       — synchronous write mirroring; adds WAN RTT to write latency')))
    lines.append(R(bMid(3, 99, 'Management: Dark fiber FC (< 5 ms RTT) · Auth: Symmetrix admin; Solutions Enabler')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Architecture: components work together to deliver SRDF/S capabilities'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Architecture'), bMid(53, 99, 'Operations'))))
    lines.append(R(merge(bMid(3, 50, 'R1 Volume (Source)  — production PowerMax; '), bMid(53, 99, 'symrdf establish -type s'))))
    lines.append(R(merge(bMid(3, 50, 'R2 Volume (Target)  — DR PowerMax; must con'), bMid(53, 99, 'symrdf failover'))))
    lines.append(R(merge(bMid(3, 50, 'SRDF/S Engine       — synchronous write mir'), bMid(53, 99, 'symrdf query'))))
    lines.append(R(merge(bMid(3, 50, 'PowerMax Mgmt       — Unisphere + symrdf; f'), bMid(53, 99, 'symrdf -rdfg list'))))
    lines.append(R(merge(bMid(3, 50, 'SRDF Link           — ultra-low-latency FC/'), bMid(53, 99, 'symrdf restore'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-architecture',
    'docs/storage/dell/srdf-s/architecture/index.md',
    'SRDF/S — architecture overview, components, data flow',
)
def _dr_srdf_s_architecture():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Architecture'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/S — Component Architecture')))
    lines.append(R(bMid(3, 99, 'R1 Volume (Source)  — production PowerMax; write holds until R2 acknowledges')))
    lines.append(R(bMid(3, 99, 'R2 Volume (Target)  — DR PowerMax; must confirm write before host I/O completes')))
    lines.append(R(bMid(3, 99, 'SRDF/S Engine       — synchronous write mirroring; adds WAN RTT to write latency')))
    lines.append(R(bMid(3, 99, 'Ports: Dark fiber FC (< 5 ms RTT) · DWDM long-haul FC · 9443 (Unisphere)')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Three-tier component model — control plane, data plane, and management'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Control Plane'), bMid(36, 66, 'Data Plane'), bMid(69, 99, 'Management'))))
    lines.append(R(merge(bMid(3, 33, 'R1 Volume (Source)  — produc'), bMid(36, 66, 'R2 Volume (Target)  — DR Pow'), bMid(69, 99, 'PowerMax Mgmt       — Unisph'))))
    lines.append(R(merge(bMid(3, 33, 'Scheduling'), bMid(36, 66, 'Replication/Backup'), bMid(69, 99, 'Dark fiber FC (< 5 ms RTT)'))))
    lines.append(R(merge(bMid(3, 33, 'Policy mgmt'), bMid(36, 66, 'Data movement'), bMid(69, 99, 'REST API'))))
    lines.append(R(merge(bMid(3, 33, 'Catalog/DB'), bMid(36, 66, 'Dedup/compress'), bMid(69, 99, 'RBAC'))))
    lines.append(R(merge(bMid(3, 33, 'Job engine'), bMid(36, 66, 'DWDM long-haul FC'), bMid(69, 99, 'Alerting'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-arch-how-it-works',
    'docs/storage/dell/srdf-s/architecture/how-it-works/index.md',
    'SRDF/S — how replication or backup data flows step by step',
)
def _dr_srdf_s_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('  SRDF/S data flow — from source to target through the protection pipeline:'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, '1  Source / Production System')))
    lines.append(R(bMid(3, 99, '   R1 Volume (Source)  — production PowerMax; write holds until R2 acknowledges')))
    lines.append(R(bMid(3, 99, '   Host writes are intercepted or snapshotted by the SRDF/S agent/proxy')))
    lines.append(R(bMid(3, 99, '   Changed blocks tracked via CBT / journal / delta-set mechanism')))
    lines.append(R(bMid(3, 99, '   Consistency ensured at quiesce point before data transfer begins')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Changed data forwarded to the SRDF/S engine — compression and encryption applied in transit'))
    lines.append(txt_row())
    lines.append(R(arrow([51])))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, '2  SRDF/S Engine')))
    lines.append(R(bMid(3, 99, '   R2 Volume (Target)  — DR PowerMax; must confirm write before host I/O completes')))
    lines.append(R(bMid(3, 99, '   Data compressed, deduplicated, and encrypted before storage')))
    lines.append(R(bMid(3, 99, '   Metadata catalog updated; job status reported to control plane')))
    lines.append(R(bMid(3, 99, '   symrdf establish -type s')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([51])))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, '3  Target / Repository')))
    lines.append(R(bMid(3, 99, '   SRDF/S Engine       — synchronous write mirroring; adds WAN RTT to write latency')))
    lines.append(R(bMid(3, 99, '   Recovery point written; retention policy applied automatically')))
    lines.append(R(bMid(3, 99, '   Restore: symrdf failover')))
    lines.append(R(bMid(3, 99, '   RTO driven by target storage performance and data volume')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-arch-design',
    'docs/storage/dell/srdf-s/architecture/design-standards/index.md',
    'SRDF/S — sizing, design rules, capacity, HA guidelines',
)
def _dr_srdf_s_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Design Standards'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Sizing Guidelines'), bMid(53, 99, 'HA Requirements'))))
    lines.append(R(merge(bMid(3, 50, 'Deduplicate where supported'), bMid(53, 99, 'N+1 component redundancy'))))
    lines.append(R(merge(bMid(3, 50, 'Bandwidth: 10 GbE minimum'), bMid(53, 99, 'Heartbeat / health monitor'))))
    lines.append(R(merge(bMid(3, 50, 'Storage: 130% of raw data'), bMid(53, 99, 'Separate mgmt / data VLANs'))))
    lines.append(R(merge(bMid(3, 50, 'Latency: < 10 ms to storage'), bMid(53, 99, 'Out-of-band access (IPMI)'))))
    lines.append(R(merge(bMid(3, 50, 'CPU: 8+ vCPU for engine'), bMid(53, 99, 'Anti-affinity VM placement'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('  Ports: Dark fiber FC (< 5 ms RTT) · DWDM long-haul FC · 9443 (Unisphere)'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Standard SRDF/S Design Rules')))
    lines.append(R(bMid(3, 99, 'RPO target drives snapshot/cycle frequency — document in service design')))
    lines.append(R(bMid(3, 99, 'RTO target drives recovery tier: instant, warm standby, or cold restore')))
    lines.append(R(bMid(3, 99, 'Dedicated backup network VLAN — no shared production traffic')))
    lines.append(R(bMid(3, 99, 'Encryption: Data identical at R2; FA port encryption optional; Unisphere TLS')))
    lines.append(R(bMid(3, 99, 'Service accounts: minimum privilege; rotate credentials quarterly')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-arch-integrations',
    'docs/storage/dell/srdf-s/architecture/integrations/index.md',
    'SRDF/S — integration points with external systems and APIs',
)
def _dr_srdf_s_arch_integrations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Architecture Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/S — External Integration Points')))
    lines.append(R(bMid(3, 99, 'Auth: Symmetrix admin credentials; Solutions Enabler; Unisphere role-based access')))
    lines.append(R(bMid(3, 99, 'Storage: connected via Dark fiber FC (< 5 ms RTT) · DWDM long-haul FC')))
    lines.append(R(bMid(3, 99, 'Monitoring: SNMP traps / syslog / REST API to ITSM and alerting systems')))
    lines.append(R(bMid(3, 99, 'Encryption: Data identical to R1 at R2; FA port encryption optional; Unisphere TLS/HTTPS')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Identity'), bMid(36, 66, 'Storage'), bMid(69, 99, 'Monitoring'))))
    lines.append(R(merge(bMid(3, 33, 'AD / LDAP'), bMid(36, 66, 'Dark fiber FC (< 5 ms RTT)'), bMid(69, 99, 'SNMP / syslog'))))
    lines.append(R(merge(bMid(3, 33, 'SAML SSO'), bMid(36, 66, 'DWDM long-haul FC'), bMid(69, 99, 'REST webhook'))))
    lines.append(R(merge(bMid(3, 33, 'RBAC roles'), bMid(36, 66, 'NFS / iSCSI / FC'), bMid(69, 99, 'Email alerts'))))
    lines.append(R(merge(bMid(3, 33, 'MFA optional'), bMid(36, 66, 'Dedup appliance'), bMid(69, 99, 'ServiceNow'))))
    lines.append(R(merge(bMid(3, 33, 'Cert auth'), bMid(36, 66, 'Object storage'), bMid(69, 99, 'Prometheus'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-operations',
    'docs/storage/dell/srdf-s/operations/index.md',
    'SRDF/S — operations overview, key tasks, day-to-day procedures',
)
def _dr_srdf_s_operations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/S — Day-to-Day Operations')))
    lines.append(R(bMid(3, 99, 'Daily: review job status · check health alerts · verify last backup/replica')))
    lines.append(R(bMid(3, 99, 'Weekly: review capacity trends · test restore sample · review error logs')))
    lines.append(R(bMid(3, 99, 'Monthly: full restore test · review retention · audit service accounts')))
    lines.append(R(bMid(3, 99, 'Quarterly: DR failover test · firmware review · update documentation')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Backup/Replicate'), bMid(36, 66, 'Monitor'), bMid(69, 99, 'Recover'))))
    lines.append(R(merge(bMid(3, 33, 'symrdf establish -type s'), bMid(36, 66, 'symrdf query'), bMid(69, 99, 'symrdf failover'))))
    lines.append(R(merge(bMid(3, 33, 'Schedule jobs'), bMid(36, 66, 'Health checks'), bMid(69, 99, 'Instant restore'))))
    lines.append(R(merge(bMid(3, 33, 'Retention mgmt'), bMid(36, 66, 'Capacity alerts'), bMid(69, 99, 'Failover test'))))
    lines.append(R(merge(bMid(3, 33, 'Consistency grp'), bMid(36, 66, 'Log review'), bMid(69, 99, 'DR runbook'))))
    lines.append(R(merge(bMid(3, 33, 'Policy updates'), bMid(36, 66, 'SLA tracking'), bMid(69, 99, 'Validate RTO'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-ops-backup',
    'docs/storage/dell/srdf-s/operations/backup-restore/index.md',
    'SRDF/S — backup and restore procedures',
)
def _dr_srdf_s_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Backup & Restore'))
    lines.append(txt_row())
    lines.append(txt_row('  Backup flow: quiesce source → snapshot/copy → transfer → write to target → catalog'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Backup (Protection)'), bMid(53, 99, 'Restore (Recovery)'))))
    lines.append(R(merge(bMid(3, 50, 'symrdf establish -type s'), bMid(53, 99, 'symrdf failover'))))
    lines.append(R(merge(bMid(3, 50, 'Quiesce source I/O'), bMid(53, 99, 'Select recovery point'))))
    lines.append(R(merge(bMid(3, 50, 'Take snapshot / CBT'), bMid(53, 99, 'Mount or copy to target'))))
    lines.append(R(merge(bMid(3, 50, 'Transfer changed blocks'), bMid(53, 99, 'Validate integrity'))))
    lines.append(R(merge(bMid(3, 50, 'Commit to repository'), bMid(53, 99, 'Restart application'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Key SRDF/S Commands')))
    lines.append(R(bMid(3, 99, '  Backup trigger  : symrdf establish -type s')))
    lines.append(R(bMid(3, 99, '  List points     : symrdf failover')))
    lines.append(R(bMid(3, 99, '  Health status   : symrdf query')))
    lines.append(R(bMid(3, 99, '  Retention mgmt  : symrdf restore')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-ops-cli',
    'docs/storage/dell/srdf-s/operations/cli-reference/index.md',
    'SRDF/S — CLI commands reference',
)
def _dr_srdf_s_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — CLI Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/S — Command Reference')))
    lines.append(R(bMid(3, 99, 'Use these commands for routine operations, scripting, and troubleshooting')))
    lines.append(R(bMid(3, 99, '  symrdf establish -type s')))
    lines.append(R(bMid(3, 99, '  symrdf failover')))
    lines.append(R(bMid(3, 99, '  symrdf query')))
    lines.append(R(bMid(3, 99, '  symrdf -rdfg list')))
    lines.append(R(bMid(3, 99, '  symrdf restore')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Ports: Dark fiber FC (< 5 ms RTT) · DWDM long-haul FC · 9443 (Unisphere)'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Command Categories')))
    lines.append(R(bMid(3, 99, '  Status / Query  — check current state, list jobs, show config')))
    lines.append(R(bMid(3, 99, '  Operations      — start, stop, failover, restore, sync, expire')))
    lines.append(R(bMid(3, 99, '  Configuration   — add/modify policies, schedules, storage targets')))
    lines.append(R(bMid(3, 99, '  Diagnostics     — collect logs, run health checks, test connectivity')))
    lines.append(R(bMid(3, 99, '  Scripting       — REST API or CLI for automation and reporting')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-ops-health',
    'docs/storage/dell/srdf-s/operations/health-checks/index.md',
    'SRDF/S — health check procedures and monitoring commands',
)
def _dr_srdf_s_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Health Checks'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/S — Health Check Procedures')))
    lines.append(R(bMid(3, 99, 'Run these checks daily/weekly to confirm protection is working')))
    lines.append(R(bMid(3, 99, '  symrdf query')))
    lines.append(R(bMid(3, 99, '  Review job completion rate — target 100%; investigate failures')))
    lines.append(R(bMid(3, 99, '  Check replication/backup lag against RPO target')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Check', 'What to verify', 'Expected', 'Frequency', 'Action if bad'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Job status', 'All jobs complete', '100% success', 'Daily', 'Triage failures'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Lag / RPO', 'Replication lag', '< RPO target', 'Daily', 'Tune bandwidth'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Capacity', 'Repo space used', '< 80% full', 'Weekly', 'Expand or expire'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Restore test', 'Random restore', 'Data intact', 'Monthly', 'Fix backup chain'])))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-ops-install',
    'docs/storage/dell/srdf-s/operations/install-upgrade/index.md',
    'SRDF/S — install and upgrade procedures',
)
def _dr_srdf_s_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Install & Upgrade'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/S — Installation Prerequisites')))
    lines.append(R(bMid(3, 99, '  OS: supported Linux or Windows Server (see vendor compatibility matrix)')))
    lines.append(R(bMid(3, 99, '  Network: Dark fiber FC (< 5 ms RTT) · DWDM long-haul FC — ensure firewall allows these')))
    lines.append(R(bMid(3, 99, '  Auth: Symmetrix admin credentials; Solutions Enabler; Unisphere role-based access')))
    lines.append(R(bMid(3, 99, '  Storage: Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency (< 200 km)')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([51])))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Install Sequence')))
    lines.append(R(bMid(3, 99, '  1  Deploy control plane component and configure network access')))
    lines.append(R(bMid(3, 99, '  2  Configure storage and network connectivity')))
    lines.append(R(bMid(3, 99, '  3  Install agent/proxy/splitter on protected hosts')))
    lines.append(R(bMid(3, 99, '  4  Register sources and configure protection policies')))
    lines.append(R(bMid(3, 99, '  5  Run first job; verify completion; test restore')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Upgrade Sequence')))
    lines.append(R(bMid(3, 99, '  1  Review release notes and compatibility matrix before upgrade')))
    lines.append(R(bMid(3, 99, '  2  Snapshot or backup the control plane VM before upgrading')))
    lines.append(R(bMid(3, 99, '  3  Upgrade control plane first, then proxies/agents/appliances')))
    lines.append(R(bMid(3, 99, '  4  Validate jobs resume automatically after upgrade')))
    lines.append(R(bMid(3, 99, '  5  Document version change and update CMDB record')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-ops-procedures',
    'docs/storage/dell/srdf-s/operations/procedures/index.md',
    'SRDF/S — operational procedures and runbooks',
)
def _dr_srdf_s_ops_procedures():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Procedures'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Routine Procedures'), bMid(53, 99, 'DR Procedures'))))
    lines.append(R(merge(bMid(3, 50, 'Add new protection source'), bMid(53, 99, 'Initiate failover'))))
    lines.append(R(merge(bMid(3, 50, 'Modify retention policy'), bMid(53, 99, 'Validate replica'))))
    lines.append(R(merge(bMid(3, 50, 'Expire old recover points'), bMid(53, 99, 'Redirect host I/O'))))
    lines.append(R(merge(bMid(3, 50, 'Add storage capacity'), bMid(53, 99, 'Test failover (non-disrupt)'))))
    lines.append(R(merge(bMid(3, 50, 'Service account rotation'), bMid(53, 99, 'Failback to production'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Change Control Requirements for SRDF/S')))
    lines.append(R(bMid(3, 99, '  All changes to protection policies require change ticket with rollback plan')))
    lines.append(R(bMid(3, 99, '  Failover tests must be scheduled in maintenance window')))
    lines.append(R(bMid(3, 99, '  Firmware/software upgrades need 48 h pre-approval and backup snapshot')))
    lines.append(R(bMid(3, 99, '  Post-change: verify jobs run successfully for 2 backup cycles')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-ops-scripts',
    'docs/storage/dell/srdf-s/operations/scripts/index.md',
    'SRDF/S — automation scripts and examples',
)
def _dr_srdf_s_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Scripts'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/S — Automation Scripts')))
    lines.append(R(bMid(3, 99, 'Scripts automate routine SRDF/S operations — run via cron or CI/CD')))
    lines.append(R(bMid(3, 99, 'Always store credentials in vault (not in script); log all output')))
    lines.append(R(bMid(3, 99, 'Test scripts in non-production before scheduling in production')))
    lines.append(R(bMid(3, 99, 'Scope scripts to least-privilege service account')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Status / Reporting Scripts'), bMid(53, 99, 'Automation Scripts'))))
    lines.append(R(merge(bMid(3, 50, 'Job success rate report'), bMid(53, 99, 'Auto-expire old points'))))
    lines.append(R(merge(bMid(3, 50, 'Capacity trending'), bMid(53, 99, 'Auto-add new VMs to policy'))))
    lines.append(R(merge(bMid(3, 50, 'SLA compliance report'), bMid(53, 99, 'Nightly DR test validation'))))
    lines.append(R(merge(bMid(3, 50, 'RPO / RTO dashboard'), bMid(53, 99, 'Alert on job failure'))))
    lines.append(R(merge(bMid(3, 50, 'symrdf query'), bMid(53, 99, 'symrdf -rdfg list'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-security',
    'docs/storage/dell/srdf-s/security/index.md',
    'SRDF/S — security overview, controls, compliance posture',
)
def _dr_srdf_s_security():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Security'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/S — Security Posture')))
    lines.append(R(bMid(3, 99, 'Authentication: Symmetrix admin credentials; Solutions Enabler; Unisphere role-based access')))
    lines.append(R(bMid(3, 99, 'Encryption: Data identical to R1 at R2; FA port encryption optional; Unisphere TLS/HTTPS')))
    lines.append(R(bMid(3, 99, 'Network: management VLAN separated; 9443 (Unisphere) management port')))
    lines.append(R(bMid(3, 99, 'Audit: all admin actions logged; log retention minimum 1 year')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Access Control'), bMid(36, 66, 'Encryption'), bMid(69, 99, 'Audit'))))
    lines.append(R(merge(bMid(3, 33, 'RBAC roles'), bMid(36, 66, 'AES-256 at rest'), bMid(69, 99, 'Admin actions'))))
    lines.append(R(merge(bMid(3, 33, 'Least privilege'), bMid(36, 66, 'TLS in transit'), bMid(69, 99, 'Login events'))))
    lines.append(R(merge(bMid(3, 33, 'MFA optional'), bMid(36, 66, 'Key rotation'), bMid(69, 99, 'Syslog export'))))
    lines.append(R(merge(bMid(3, 33, 'SVC acct rotate'), bMid(36, 66, 'WORM / immutable'), bMid(69, 99, 'SIEM forward'))))
    lines.append(R(merge(bMid(3, 33, 'Just-In-Time'), bMid(36, 66, 'KMS managed'), bMid(69, 99, 'Quarterly review'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-sec-access',
    'docs/storage/dell/srdf-s/security/access-control/index.md',
    'SRDF/S — RBAC, permissions, service accounts',
)
def _dr_srdf_s_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Access Control'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/S — RBAC and Access Control')))
    lines.append(R(bMid(3, 99, 'Auth: Symmetrix admin credentials; Solutions Enabler; Unisphere role-based access')))
    lines.append(R(bMid(3, 99, 'Principle of least privilege: each role gets only required permissions')))
    lines.append(R(bMid(3, 99, 'Service accounts: dedicated, non-interactive; rotation every 90 days')))
    lines.append(R(bMid(3, 99, 'Emergency break-glass: documented, monitored, time-limited access')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Role', 'Access Level', 'Typical User', 'Review Freq', 'Granted By'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Admin', 'Full config/ops', 'Sr Backup Eng', 'Quarterly', 'Security team'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Operator', 'Start/stop jobs', 'Backup Eng', 'Quarterly', 'Team lead'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Monitor', 'Read-only view', 'NOC / L1', 'Quarterly', 'Team lead'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Service Acct', 'API / headless', 'Automation', 'Per rotation', 'Security team'])))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-sec-auth',
    'docs/storage/dell/srdf-s/security/authentication/index.md',
    'SRDF/S — authentication methods, certificate management',
)
def _dr_srdf_s_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Authentication'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/S — Authentication Methods')))
    lines.append(R(bMid(3, 99, 'Symmetrix admin credentials; Solutions Enabler; Unisphere role-based access')))
    lines.append(R(bMid(3, 99, 'Management UI: HTTPS on Dark fiber FC (< 5 ms RTT) — browser-based login')))
    lines.append(R(bMid(3, 99, 'API: bearer token or service account; rotate credentials quarterly')))
    lines.append(R(bMid(3, 99, 'Inter-component: certificate-based mutual TLS between engines')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Human Access'), bMid(53, 99, 'Machine Access'))))
    lines.append(R(merge(bMid(3, 50, 'AD / LDAP integration'), bMid(53, 99, 'Service account'))))
    lines.append(R(merge(bMid(3, 50, 'SAML SSO optional'), bMid(53, 99, 'API key / token'))))
    lines.append(R(merge(bMid(3, 50, 'MFA via IdP'), bMid(53, 99, 'Certificate auth'))))
    lines.append(R(merge(bMid(3, 50, 'Session timeout 15 min'), bMid(53, 99, 'Rotate every 90 d'))))
    lines.append(R(merge(bMid(3, 50, 'Audit login events'), bMid(53, 99, 'Vault-stored secrets'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-sec-enc',
    'docs/storage/dell/srdf-s/security/encryption/index.md',
    'SRDF/S — encryption at rest and in transit',
)
def _dr_srdf_s_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Encryption'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/S — Encryption Configuration')))
    lines.append(R(bMid(3, 99, 'Data identical to R1 at R2; FA port encryption optional; Unisphere TLS/HTTPS')))
    lines.append(R(bMid(3, 99, 'In-transit: TLS 1.2+ for all management; data channel also encrypted')))
    lines.append(R(bMid(3, 99, 'At-rest: AES-256 on repository or vault storage; key managed by KMS')))
    lines.append(R(bMid(3, 99, 'Key lifecycle: generate → use → rotate (annual) → retire → destroy')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'In-Transit'), bMid(53, 99, 'At-Rest'))))
    lines.append(R(merge(bMid(3, 50, 'TLS 1.2+ (minimum)'), bMid(53, 99, 'AES-256 encryption'))))
    lines.append(R(merge(bMid(3, 50, 'Dark fiber FC (< 5 ms RTT) HTTPS'), bMid(53, 99, 'KMS key management'))))
    lines.append(R(merge(bMid(3, 50, 'Mutual TLS internal'), bMid(53, 99, 'WORM / immutable'))))
    lines.append(R(merge(bMid(3, 50, 'Cert rotation annual'), bMid(53, 99, 'Key rotation annual'))))
    lines.append(R(merge(bMid(3, 50, 'No plain-text admin'), bMid(53, 99, 'Audit key access'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-sec-hardening',
    'docs/storage/dell/srdf-s/security/hardening/index.md',
    'SRDF/S — hardening guide, CIS controls, secure configuration',
)
def _dr_srdf_s_sec_hardening():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Hardening'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/S — Hardening Checklist')))
    lines.append(R(bMid(3, 99, '  [ ] Disable default/admin accounts; create named admin accounts only')))
    lines.append(R(bMid(3, 99, '  [ ] Enable MFA for all interactive logins via IdP / SAML SSO')))
    lines.append(R(bMid(3, 99, '  [ ] Restrict management port (Dark fiber FC (< 5 ms RTT)) to jump host / management VLAN')))
    lines.append(R(bMid(3, 99, '  [ ] Enable audit logging and forward to SIEM (syslog, TLS port 6514)')))
    lines.append(R(bMid(3, 99, '  [ ] Apply all security patches within 30 days of vendor release')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Network Hardening')))
    lines.append(R(bMid(3, 99, '  [ ] Separate backup VLAN — no direct production host access to repo')))
    lines.append(R(bMid(3, 99, '  [ ] Firewall: allow only Dark fiber FC (< 5 ms RTT) · DWDM long-haul FC · 9443 (Unisphere)')))
    lines.append(R(bMid(3, 99, '  [ ] Disable unused ports and protocols on management interface')))
    lines.append(R(bMid(3, 99, '  [ ] Immutable repository: enable WORM or object lock on backup target')))
    lines.append(R(bMid(3, 99, '  [ ] Encryption in transit: disable TLS 1.0/1.1; enforce TLS 1.2+')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-troubleshooting',
    'docs/storage/dell/srdf-s/troubleshooting/index.md',
    'SRDF/S — troubleshooting overview and triage approach',
)
def _dr_srdf_s_troubleshooting():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/S — Troubleshooting Approach')))
    lines.append(R(bMid(3, 99, '1  Identify: which job, component, or resource is failing')))
    lines.append(R(bMid(3, 99, '2  Scope: single job vs all jobs; one source vs all sources')))
    lines.append(R(bMid(3, 99, '3  Collect: logs and run status command; review recent change history')))
    lines.append(R(bMid(3, 99, '4  Diagnose: match symptoms to known issues; check error codes')))
    lines.append(R(bMid(3, 99, '5  Fix: apply resolution; verify fix; monitor next run')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Infrastructure'), bMid(36, 66, 'Application'), bMid(69, 99, 'Data'))))
    lines.append(R(merge(bMid(3, 33, 'Network checks'), bMid(36, 66, 'Log analysis'), bMid(69, 99, 'Catalog check'))))
    lines.append(R(merge(bMid(3, 33, 'Storage space'), bMid(36, 66, 'Job error codes'), bMid(69, 99, 'Consistency'))))
    lines.append(R(merge(bMid(3, 33, 'Process health'), bMid(36, 66, 'Auth failures'), bMid(69, 99, 'Corruption scan'))))
    lines.append(R(merge(bMid(3, 33, 'Dark fiber FC (< 5 ms RTT'), bMid(36, 66, 'Timeout errors'), bMid(69, 99, 'Restore test'))))
    lines.append(R(merge(bMid(3, 33, 'Firewall rules'), bMid(36, 66, 'Version compat'), bMid(69, 99, 'RPO drift'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-ts-issues',
    'docs/storage/dell/srdf-s/troubleshooting/common-issues/index.md',
    'SRDF/S — common issues, root causes, and fixes',
)
def _dr_srdf_s_ts_issues():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Common Issues'))
    lines.append(txt_row())
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Symptom', 'Likely Cause', 'First Check', 'Fix', 'Verify'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Write latency', 'RTT > budget', 'symrdf query -per', 'distance / bandwi', 'symstat'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Pair Consistent', 'transient congest', 'symrdf query', 'monitor; usually ', 'symrdf -v'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Link failure', 'RF port down', 'symcfg list -rdfg', 'failover immediat', 'symrdf failove'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['R2 not ready', 'array fault', 'check R2 Unispher', 'fix array, re-est', 'symrdf establi'])))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'General Triage Pattern')))
    lines.append(R(bMid(3, 99, '  Is the issue new or recurring? New = recent change; Recurring = config problem')))
    lines.append(R(bMid(3, 99, '  Is it isolated to one source or all? Isolated = agent; All = server/repo')))
    lines.append(R(bMid(3, 99, '  Check logs first: symrdf query')))
    lines.append(R(bMid(3, 99, '  If unresolved in 2h: open vendor case with full log bundle')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-ts-diag',
    'docs/storage/dell/srdf-s/troubleshooting/diagnostics/index.md',
    'SRDF/S — diagnostic commands and log collection',
)
def _dr_srdf_s_ts_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Diagnostics'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/S — Diagnostic Commands')))
    lines.append(R(bMid(3, 99, 'Collect these before opening a vendor support case')))
    lines.append(R(bMid(3, 99, '  symrdf query')))
    lines.append(R(bMid(3, 99, '  symrdf -rdfg list')))
    lines.append(R(bMid(3, 99, '  Check system logs: /var/log/ or Windows Event Viewer')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Log Collection'), bMid(53, 99, 'Live Diagnostics'))))
    lines.append(R(merge(bMid(3, 50, 'Application log bundle'), bMid(53, 99, 'Network connectivity'))))
    lines.append(R(merge(bMid(3, 50, 'OS syslog (journalctl)'), bMid(53, 99, 'Storage path check'))))
    lines.append(R(merge(bMid(3, 50, 'Core dump if crashed'), bMid(53, 99, 'Process list check'))))
    lines.append(R(merge(bMid(3, 50, 'Config export/backup'), bMid(53, 99, 'Port reachability'))))
    lines.append(R(merge(bMid(3, 50, 'symrdf query'), bMid(53, 99, 'symrdf -rdfg list'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-srdf-s-ts-escalation',
    'docs/storage/dell/srdf-s/troubleshooting/escalation/index.md',
    'SRDF/S — escalation path, vendor support, and SLA',
)
def _dr_srdf_s_ts_escalation():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'SRDF/S — Escalation'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'SRDF/S — Escalation Path')))
    lines.append(R(bMid(3, 99, 'L1 Triage: review logs, match to known issues in runbook (0–30 min)')))
    lines.append(R(bMid(3, 99, 'L2 Engineering: deep analysis, config review, lab reproduction (30 min – 4 h)')))
    lines.append(R(bMid(3, 99, 'Vendor Support: open case with log bundle if unresolved at L2 (> 4 h)')))
    lines.append(R(bMid(3, 99, 'Sev1 (data loss / production impact): page on-call + open critical case')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Information to Collect Before Escalating')))
    lines.append(R(bMid(3, 99, '  Product version: SRDF/S version string from About / version command')))
    lines.append(R(bMid(3, 99, '  Full log bundle: symrdf query')))
    lines.append(R(bMid(3, 99, '  Symptom timeline: when first occurred; any changes made')))
    lines.append(R(bMid(3, 99, '  Scope: single job / all jobs / all components — narrows root cause')))
    lines.append(R(bMid(3, 99, '  Error codes: exact error messages and exit codes from logs')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment'))
    lines.append(txt_row('R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency'))
    lines.append(txt_row('R2            = target volume; must acknowledge each write; acts as synchronous mirror'))
    lines.append(txt_row('RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency'))
    lines.append(txt_row('RPO=0         = zero recovery point objective; no data loss possible under normal operation'))
    lines.append(txt_row('RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min'))
    lines.append(txt_row('symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver'))
    lines.append(txt_row('Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split'))
    lines.append(txt_row('Consistent    = transient state where R1 write is in transit but not yet confirmed on R2'))
    lines.append(txt_row('Failover      = makes R2 read-write; production continues from DR site after R1 failure'))
    lines.append(txt_row('Restore       = re-synchronises after failover; direction is reversed until R1 catches up'))
    lines.append(txt_row('RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters'))
    lines.append(txt_row('FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)'))
    lines.append(txt_row('RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines


@kb_diagram(
    'dr-superna',
    'docs/storage/netapp/superna-eyeglass/index.md',
    'NAS DR and ransomware protection for Dell PowerScale — SyncIQ integration and failover automation',
)
def _dr_superna_overview():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Overview'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Superna Eyeglass')))
    lines.append(R(bMid(3, 99, 'NAS DR and ransomware protection for Dell PowerScale — SyncIQ integration and failover autom')))
    lines.append(R(bMid(3, 99, 'Eyeglass Appliance   — VM monitoring PowerScale clusters; REST API-driven')))
    lines.append(R(bMid(3, 99, 'RAPA Engine          — Ransomware Protection with Automated Response; quarantine on detect')))
    lines.append(R(bMid(3, 99, 'DFS Namespace Mgr    — Windows DFS-N failover automation; transparent client redirect')))
    lines.append(R(bMid(3, 99, 'Management: 443 (Eyeglass web UI) · Auth: Eyeglass admin roles; PowerScale admin credentials')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Architecture: components work together to deliver Superna Eyeglass capabilities'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Architecture'), bMid(53, 99, 'Operations'))))
    lines.append(R(merge(bMid(3, 50, 'Eyeglass Appliance   — VM monitoring PowerS'), bMid(53, 99, 'igls quota list'))))
    lines.append(R(merge(bMid(3, 50, 'RAPA Engine          — Ransomware Protectio'), bMid(53, 99, 'igls dr runbook'))))
    lines.append(R(merge(bMid(3, 50, 'DFS Namespace Mgr    — Windows DFS-N failov'), bMid(53, 99, 'igls sync status'))))
    lines.append(R(merge(bMid(3, 50, 'Sync Jobs            — configuration replic'), bMid(53, 99, 'igls rapa status'))))
    lines.append(R(merge(bMid(3, 50, 'DR Assistant         — guided failover work'), bMid(53, 99, 'igls failover start'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-architecture',
    'docs/storage/netapp/superna-eyeglass/architecture/index.md',
    'Superna Eyeglass — architecture overview, components, data flow',
)
def _dr_superna_architecture():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Architecture'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Superna Eyeglass — Component Architecture')))
    lines.append(R(bMid(3, 99, 'Eyeglass Appliance   — VM monitoring PowerScale clusters; REST API-driven')))
    lines.append(R(bMid(3, 99, 'RAPA Engine          — Ransomware Protection with Automated Response; quarantine on detect')))
    lines.append(R(bMid(3, 99, 'DFS Namespace Mgr    — Windows DFS-N failover automation; transparent client redirect')))
    lines.append(R(bMid(3, 99, 'Ports: 443 (Eyeglass web UI) · 8080 (REST API) · 8116 (Isilon/PowerScale mgmt)')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Three-tier component model — control plane, data plane, and management'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Control Plane'), bMid(36, 66, 'Data Plane'), bMid(69, 99, 'Management'))))
    lines.append(R(merge(bMid(3, 33, 'Eyeglass Appliance   — VM mo'), bMid(36, 66, 'RAPA Engine          — Ranso'), bMid(69, 99, 'Sync Jobs            — confi'))))
    lines.append(R(merge(bMid(3, 33, 'Scheduling'), bMid(36, 66, 'Replication/Backup'), bMid(69, 99, '443 (Eyeglass web UI)'))))
    lines.append(R(merge(bMid(3, 33, 'Policy mgmt'), bMid(36, 66, 'Data movement'), bMid(69, 99, 'REST API'))))
    lines.append(R(merge(bMid(3, 33, 'Catalog/DB'), bMid(36, 66, 'Dedup/compress'), bMid(69, 99, 'RBAC'))))
    lines.append(R(merge(bMid(3, 33, 'Job engine'), bMid(36, 66, '8080 (REST API)'), bMid(69, 99, 'Alerting'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-arch-how-it-works',
    'docs/storage/netapp/superna-eyeglass/architecture/how-it-works/index.md',
    'Superna Eyeglass — how replication or backup data flows step by step',
)
def _dr_superna_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('  Superna Eyeglass data flow — from source to target through the protection pipeline:'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, '1  Source / Production System')))
    lines.append(R(bMid(3, 99, '   Eyeglass Appliance   — VM monitoring PowerScale clusters; REST API-driven')))
    lines.append(R(bMid(3, 99, '   Host writes are intercepted or snapshotted by the Superna Eyeglass agent/proxy')))
    lines.append(R(bMid(3, 99, '   Changed blocks tracked via CBT / journal / delta-set mechanism')))
    lines.append(R(bMid(3, 99, '   Consistency ensured at quiesce point before data transfer begins')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Changed data forwarded to Superna Eyeglass — compression and encryption in transit'))
    lines.append(txt_row())
    lines.append(R(arrow([51])))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, '2  Superna Eyeglass Engine')))
    lines.append(R(bMid(3, 99, '   RAPA Engine          — Ransomware Protection with Automated Response; quarantine on dete')))
    lines.append(R(bMid(3, 99, '   Data compressed, deduplicated, and encrypted before storage')))
    lines.append(R(bMid(3, 99, '   Metadata catalog updated; job status reported to control plane')))
    lines.append(R(bMid(3, 99, '   igls quota list')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([51])))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, '3  Target / Repository')))
    lines.append(R(bMid(3, 99, '   DFS Namespace Mgr    — Windows DFS-N failover automation; transparent client redirect')))
    lines.append(R(bMid(3, 99, '   Recovery point written; retention policy applied automatically')))
    lines.append(R(bMid(3, 99, '   Restore: igls dr runbook')))
    lines.append(R(bMid(3, 99, '   RTO driven by target storage performance and data volume')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-arch-design',
    'docs/storage/netapp/superna-eyeglass/architecture/design-standards/index.md',
    'Superna Eyeglass — sizing, design rules, capacity, HA guidelines',
)
def _dr_superna_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Design Standards'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Sizing Guidelines'), bMid(53, 99, 'HA Requirements'))))
    lines.append(R(merge(bMid(3, 50, 'Deduplicate where supported'), bMid(53, 99, 'N+1 component redundancy'))))
    lines.append(R(merge(bMid(3, 50, 'Bandwidth: 10 GbE minimum'), bMid(53, 99, 'Heartbeat / health monitor'))))
    lines.append(R(merge(bMid(3, 50, 'Storage: 130% of raw data'), bMid(53, 99, 'Separate mgmt / data VLANs'))))
    lines.append(R(merge(bMid(3, 50, 'Latency: < 10 ms to storage'), bMid(53, 99, 'Out-of-band access (IPMI)'))))
    lines.append(R(merge(bMid(3, 50, 'CPU: 8+ vCPU for engine'), bMid(53, 99, 'Anti-affinity VM placement'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('  Ports: 443 (Eyeglass web UI) · 8080 (REST API) · 8116 (Isilon/PowerScale mgmt)'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Standard Superna Eyeglass Design Rules')))
    lines.append(R(bMid(3, 99, 'RPO target drives snapshot/cycle frequency — document in service design')))
    lines.append(R(bMid(3, 99, 'RTO target drives recovery tier: instant, warm standby, or cold restore')))
    lines.append(R(bMid(3, 99, 'Dedicated backup network VLAN — no shared production traffic')))
    lines.append(R(bMid(3, 99, 'Encryption: HTTPS/TLS for all management; SyncIQ replication encryption (AES-256)')))
    lines.append(R(bMid(3, 99, 'Service accounts: minimum privilege; rotate credentials quarterly')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-arch-integrations',
    'docs/storage/netapp/superna-eyeglass/architecture/integrations/index.md',
    'Superna Eyeglass — integration points with external systems and APIs',
)
def _dr_superna_arch_integrations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Architecture Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Superna Eyeglass — External Integration Points')))
    lines.append(R(bMid(3, 99, 'Auth: Eyeglass admin roles; PowerScale admin credentials; AD integration for DFS-N management')))
    lines.append(R(bMid(3, 99, 'Storage: connected via 443 (Eyeglass web UI) · 8080 (REST API)')))
    lines.append(R(bMid(3, 99, 'Monitoring: SNMP traps / syslog / REST API to ITSM and alerting systems')))
    lines.append(R(bMid(3, 99, 'Encryption: HTTPS/TLS for all management; SyncIQ replication AES-256 in transit')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Identity'), bMid(36, 66, 'Storage'), bMid(69, 99, 'Monitoring'))))
    lines.append(R(merge(bMid(3, 33, 'AD / LDAP'), bMid(36, 66, '443 (Eyeglass web UI)'), bMid(69, 99, 'SNMP / syslog'))))
    lines.append(R(merge(bMid(3, 33, 'SAML SSO'), bMid(36, 66, '8080 (REST API)'), bMid(69, 99, 'REST webhook'))))
    lines.append(R(merge(bMid(3, 33, 'RBAC roles'), bMid(36, 66, 'NFS / iSCSI / FC'), bMid(69, 99, 'Email alerts'))))
    lines.append(R(merge(bMid(3, 33, 'MFA optional'), bMid(36, 66, 'Dedup appliance'), bMid(69, 99, 'ServiceNow'))))
    lines.append(R(merge(bMid(3, 33, 'Cert auth'), bMid(36, 66, 'Object storage'), bMid(69, 99, 'Prometheus'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-operations',
    'docs/storage/netapp/superna-eyeglass/operations/index.md',
    'Superna Eyeglass — operations overview, key tasks, day-to-day procedures',
)
def _dr_superna_operations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Superna Eyeglass — Day-to-Day Operations')))
    lines.append(R(bMid(3, 99, 'Daily: review job status · check health alerts · verify last backup/replica')))
    lines.append(R(bMid(3, 99, 'Weekly: review capacity trends · test restore sample · review error logs')))
    lines.append(R(bMid(3, 99, 'Monthly: full restore test · review retention · audit service accounts')))
    lines.append(R(bMid(3, 99, 'Quarterly: DR failover test · firmware review · update documentation')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Backup/Replicate'), bMid(36, 66, 'Monitor'), bMid(69, 99, 'Recover'))))
    lines.append(R(merge(bMid(3, 33, 'igls quota list'), bMid(36, 66, 'igls sync status'), bMid(69, 99, 'igls dr runbook'))))
    lines.append(R(merge(bMid(3, 33, 'Schedule jobs'), bMid(36, 66, 'Health checks'), bMid(69, 99, 'Instant restore'))))
    lines.append(R(merge(bMid(3, 33, 'Retention mgmt'), bMid(36, 66, 'Capacity alerts'), bMid(69, 99, 'Failover test'))))
    lines.append(R(merge(bMid(3, 33, 'Consistency grp'), bMid(36, 66, 'Log review'), bMid(69, 99, 'DR runbook'))))
    lines.append(R(merge(bMid(3, 33, 'Policy updates'), bMid(36, 66, 'SLA tracking'), bMid(69, 99, 'Validate RTO'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-ops-backup',
    'docs/storage/netapp/superna-eyeglass/operations/backup-restore/index.md',
    'Superna Eyeglass — backup and restore procedures',
)
def _dr_superna_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Backup & Restore'))
    lines.append(txt_row())
    lines.append(txt_row('  Backup flow: quiesce source → snapshot/copy → transfer → write to target → catalog'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Backup (Protection)'), bMid(53, 99, 'Restore (Recovery)'))))
    lines.append(R(merge(bMid(3, 50, 'igls quota list'), bMid(53, 99, 'igls dr runbook'))))
    lines.append(R(merge(bMid(3, 50, 'Quiesce source I/O'), bMid(53, 99, 'Select recovery point'))))
    lines.append(R(merge(bMid(3, 50, 'Take snapshot / CBT'), bMid(53, 99, 'Mount or copy to target'))))
    lines.append(R(merge(bMid(3, 50, 'Transfer changed blocks'), bMid(53, 99, 'Validate integrity'))))
    lines.append(R(merge(bMid(3, 50, 'Commit to repository'), bMid(53, 99, 'Restart application'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Key Superna Eyeglass Commands')))
    lines.append(R(bMid(3, 99, '  Backup trigger  : igls quota list')))
    lines.append(R(bMid(3, 99, '  List points     : igls dr runbook')))
    lines.append(R(bMid(3, 99, '  Health status   : igls sync status')))
    lines.append(R(bMid(3, 99, '  Retention mgmt  : igls failover start')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-ops-cli',
    'docs/storage/netapp/superna-eyeglass/operations/cli-reference/index.md',
    'Superna Eyeglass — CLI commands reference',
)
def _dr_superna_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — CLI Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Superna Eyeglass — Command Reference')))
    lines.append(R(bMid(3, 99, 'Use these commands for routine operations, scripting, and troubleshooting')))
    lines.append(R(bMid(3, 99, '  igls quota list')))
    lines.append(R(bMid(3, 99, '  igls dr runbook')))
    lines.append(R(bMid(3, 99, '  igls sync status')))
    lines.append(R(bMid(3, 99, '  igls rapa status')))
    lines.append(R(bMid(3, 99, '  igls failover start')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Ports: 443 (Eyeglass web UI) · 8080 (REST API) · 8116 (Isilon/PowerScale mgmt)'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Command Categories')))
    lines.append(R(bMid(3, 99, '  Status / Query  — check current state, list jobs, show config')))
    lines.append(R(bMid(3, 99, '  Operations      — start, stop, failover, restore, sync, expire')))
    lines.append(R(bMid(3, 99, '  Configuration   — add/modify policies, schedules, storage targets')))
    lines.append(R(bMid(3, 99, '  Diagnostics     — collect logs, run health checks, test connectivity')))
    lines.append(R(bMid(3, 99, '  Scripting       — REST API or CLI for automation and reporting')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-ops-health',
    'docs/storage/netapp/superna-eyeglass/operations/health-checks/index.md',
    'Superna Eyeglass — health check procedures and monitoring commands',
)
def _dr_superna_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Health Checks'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Superna Eyeglass — Health Check Procedures')))
    lines.append(R(bMid(3, 99, 'Run these checks daily/weekly to confirm protection is working')))
    lines.append(R(bMid(3, 99, '  igls sync status')))
    lines.append(R(bMid(3, 99, '  Review job completion rate — target 100%; investigate failures')))
    lines.append(R(bMid(3, 99, '  Check replication/backup lag against RPO target')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Check', 'What to verify', 'Expected', 'Frequency', 'Action if bad'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Job status', 'All jobs complete', '100% success', 'Daily', 'Triage failures'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Lag / RPO', 'Replication lag', '< RPO target', 'Daily', 'Tune bandwidth'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Capacity', 'Repo space used', '< 80% full', 'Weekly', 'Expand or expire'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Restore test', 'Random restore', 'Data intact', 'Monthly', 'Fix backup chain'])))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-ops-install',
    'docs/storage/netapp/superna-eyeglass/operations/install-upgrade/index.md',
    'Superna Eyeglass — install and upgrade procedures',
)
def _dr_superna_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Install & Upgrade'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Superna Eyeglass — Installation Prerequisites')))
    lines.append(R(bMid(3, 99, '  OS: supported Linux or Windows Server (see vendor compatibility matrix)')))
    lines.append(R(bMid(3, 99, '  Network: 443 (Eyeglass web UI) · 8080 (REST API) — ensure firewall allows these')))
    lines.append(R(bMid(3, 99, '  Auth: Eyeglass admin roles; PowerScale admin credentials; AD integration for DFS-N management')))
    lines.append(R(bMid(3, 99, '  Storage: Eyeglass VM · PowerScale pair (prod + DR) · SyncIQ replication link')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([51])))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Install Sequence')))
    lines.append(R(bMid(3, 99, '  1  Deploy control plane component and configure network access')))
    lines.append(R(bMid(3, 99, '  2  Configure storage and network connectivity')))
    lines.append(R(bMid(3, 99, '  3  Install agent/proxy/splitter on protected hosts')))
    lines.append(R(bMid(3, 99, '  4  Register sources and configure protection policies')))
    lines.append(R(bMid(3, 99, '  5  Run first job; verify completion; test restore')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Upgrade Sequence')))
    lines.append(R(bMid(3, 99, '  1  Review release notes and compatibility matrix before upgrade')))
    lines.append(R(bMid(3, 99, '  2  Snapshot or backup the control plane VM before upgrading')))
    lines.append(R(bMid(3, 99, '  3  Upgrade control plane first, then proxies/agents/appliances')))
    lines.append(R(bMid(3, 99, '  4  Validate jobs resume automatically after upgrade')))
    lines.append(R(bMid(3, 99, '  5  Document version change and update CMDB record')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-ops-procedures',
    'docs/storage/netapp/superna-eyeglass/operations/procedures/index.md',
    'Superna Eyeglass — operational procedures and runbooks',
)
def _dr_superna_ops_procedures():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Procedures'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Routine Procedures'), bMid(53, 99, 'DR Procedures'))))
    lines.append(R(merge(bMid(3, 50, 'Add new protection source'), bMid(53, 99, 'Initiate failover'))))
    lines.append(R(merge(bMid(3, 50, 'Modify retention policy'), bMid(53, 99, 'Validate replica'))))
    lines.append(R(merge(bMid(3, 50, 'Expire old recover points'), bMid(53, 99, 'Redirect host I/O'))))
    lines.append(R(merge(bMid(3, 50, 'Add storage capacity'), bMid(53, 99, 'Test failover (non-disrupt)'))))
    lines.append(R(merge(bMid(3, 50, 'Service account rotation'), bMid(53, 99, 'Failback to production'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Change Control Requirements for Superna Eyeglass')))
    lines.append(R(bMid(3, 99, '  All changes to protection policies require change ticket with rollback plan')))
    lines.append(R(bMid(3, 99, '  Failover tests must be scheduled in maintenance window')))
    lines.append(R(bMid(3, 99, '  Firmware/software upgrades need 48 h pre-approval and backup snapshot')))
    lines.append(R(bMid(3, 99, '  Post-change: verify jobs run successfully for 2 backup cycles')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-ops-scripts',
    'docs/storage/netapp/superna-eyeglass/operations/scripts/index.md',
    'Superna Eyeglass — automation scripts and examples',
)
def _dr_superna_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Scripts'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Superna Eyeglass — Automation Scripts')))
    lines.append(R(bMid(3, 99, 'Scripts automate routine Superna Eyeglass operations — run via cron or CI/CD')))
    lines.append(R(bMid(3, 99, 'Always store credentials in vault (not in script); log all output')))
    lines.append(R(bMid(3, 99, 'Test scripts in non-production before scheduling in production')))
    lines.append(R(bMid(3, 99, 'Scope scripts to least-privilege service account')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Status / Reporting Scripts'), bMid(53, 99, 'Automation Scripts'))))
    lines.append(R(merge(bMid(3, 50, 'Job success rate report'), bMid(53, 99, 'Auto-expire old points'))))
    lines.append(R(merge(bMid(3, 50, 'Capacity trending'), bMid(53, 99, 'Auto-add new VMs to policy'))))
    lines.append(R(merge(bMid(3, 50, 'SLA compliance report'), bMid(53, 99, 'Nightly DR test validation'))))
    lines.append(R(merge(bMid(3, 50, 'RPO / RTO dashboard'), bMid(53, 99, 'Alert on job failure'))))
    lines.append(R(merge(bMid(3, 50, 'igls sync status'), bMid(53, 99, 'igls rapa status'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-security',
    'docs/storage/netapp/superna-eyeglass/security/index.md',
    'Superna Eyeglass — security overview, controls, compliance posture',
)
def _dr_superna_security():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Security'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Superna Eyeglass — Security Posture')))
    lines.append(R(bMid(3, 99, 'Authentication: Eyeglass admin roles; PowerScale creds; AD integration for DFS-N mgmt')))
    lines.append(R(bMid(3, 99, 'Encryption: HTTPS/TLS for all management; SyncIQ replication AES-256 in transit')))
    lines.append(R(bMid(3, 99, 'Network: management VLAN separated; 8116 (Isilon/PowerScale mgmt) management port')))
    lines.append(R(bMid(3, 99, 'Audit: all admin actions logged; log retention minimum 1 year')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Access Control'), bMid(36, 66, 'Encryption'), bMid(69, 99, 'Audit'))))
    lines.append(R(merge(bMid(3, 33, 'RBAC roles'), bMid(36, 66, 'AES-256 at rest'), bMid(69, 99, 'Admin actions'))))
    lines.append(R(merge(bMid(3, 33, 'Least privilege'), bMid(36, 66, 'TLS in transit'), bMid(69, 99, 'Login events'))))
    lines.append(R(merge(bMid(3, 33, 'MFA optional'), bMid(36, 66, 'Key rotation'), bMid(69, 99, 'Syslog export'))))
    lines.append(R(merge(bMid(3, 33, 'SVC acct rotate'), bMid(36, 66, 'WORM / immutable'), bMid(69, 99, 'SIEM forward'))))
    lines.append(R(merge(bMid(3, 33, 'Just-In-Time'), bMid(36, 66, 'KMS managed'), bMid(69, 99, 'Quarterly review'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-sec-access',
    'docs/storage/netapp/superna-eyeglass/security/access-control/index.md',
    'Superna Eyeglass — RBAC, permissions, service accounts',
)
def _dr_superna_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Access Control'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Superna Eyeglass — RBAC and Access Control')))
    lines.append(R(bMid(3, 99, 'Auth: Eyeglass admin roles; PowerScale admin credentials; AD integration for DFS-N management')))
    lines.append(R(bMid(3, 99, 'Principle of least privilege: each role gets only required permissions')))
    lines.append(R(bMid(3, 99, 'Service accounts: dedicated, non-interactive; rotation every 90 days')))
    lines.append(R(bMid(3, 99, 'Emergency break-glass: documented, monitored, time-limited access')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Role', 'Access Level', 'Typical User', 'Review Freq', 'Granted By'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Admin', 'Full config/ops', 'Sr Backup Eng', 'Quarterly', 'Security team'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Operator', 'Start/stop jobs', 'Backup Eng', 'Quarterly', 'Team lead'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Monitor', 'Read-only view', 'NOC / L1', 'Quarterly', 'Team lead'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Service Acct', 'API / headless', 'Automation', 'Per rotation', 'Security team'])))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-sec-auth',
    'docs/storage/netapp/superna-eyeglass/security/authentication/index.md',
    'Superna Eyeglass — authentication methods, certificate management',
)
def _dr_superna_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Authentication'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Superna Eyeglass — Authentication Methods')))
    lines.append(R(bMid(3, 99, 'Eyeglass admin roles; PowerScale admin credentials; AD integration for DFS-N management')))
    lines.append(R(bMid(3, 99, 'Management UI: HTTPS on 443 (Eyeglass web UI) — browser-based login')))
    lines.append(R(bMid(3, 99, 'API: bearer token or service account; rotate credentials quarterly')))
    lines.append(R(bMid(3, 99, 'Inter-component: certificate-based mutual TLS between engines')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Human Access'), bMid(53, 99, 'Machine Access'))))
    lines.append(R(merge(bMid(3, 50, 'AD / LDAP integration'), bMid(53, 99, 'Service account'))))
    lines.append(R(merge(bMid(3, 50, 'SAML SSO optional'), bMid(53, 99, 'API key / token'))))
    lines.append(R(merge(bMid(3, 50, 'MFA via IdP'), bMid(53, 99, 'Certificate auth'))))
    lines.append(R(merge(bMid(3, 50, 'Session timeout 15 min'), bMid(53, 99, 'Rotate every 90 d'))))
    lines.append(R(merge(bMid(3, 50, 'Audit login events'), bMid(53, 99, 'Vault-stored secrets'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-sec-enc',
    'docs/storage/netapp/superna-eyeglass/security/encryption/index.md',
    'Superna Eyeglass — encryption at rest and in transit',
)
def _dr_superna_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Encryption'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Superna Eyeglass — Encryption Configuration')))
    lines.append(R(bMid(3, 99, 'HTTPS/TLS for all management; SyncIQ data replication encryption (AES-256 in transit)')))
    lines.append(R(bMid(3, 99, 'In-transit: TLS 1.2+ for all management; data channel also encrypted')))
    lines.append(R(bMid(3, 99, 'At-rest: AES-256 on repository or vault storage; key managed by KMS')))
    lines.append(R(bMid(3, 99, 'Key lifecycle: generate → use → rotate (annual) → retire → destroy')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'In-Transit'), bMid(53, 99, 'At-Rest'))))
    lines.append(R(merge(bMid(3, 50, 'TLS 1.2+ (minimum)'), bMid(53, 99, 'AES-256 encryption'))))
    lines.append(R(merge(bMid(3, 50, '443 (Eyeglass web UI) HTTPS'), bMid(53, 99, 'KMS key management'))))
    lines.append(R(merge(bMid(3, 50, 'Mutual TLS internal'), bMid(53, 99, 'WORM / immutable'))))
    lines.append(R(merge(bMid(3, 50, 'Cert rotation annual'), bMid(53, 99, 'Key rotation annual'))))
    lines.append(R(merge(bMid(3, 50, 'No plain-text admin'), bMid(53, 99, 'Audit key access'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-sec-hardening',
    'docs/storage/netapp/superna-eyeglass/security/hardening/index.md',
    'Superna Eyeglass — hardening guide, CIS controls, secure configuration',
)
def _dr_superna_sec_hardening():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Hardening'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Superna Eyeglass — Hardening Checklist')))
    lines.append(R(bMid(3, 99, '  [ ] Disable default/admin accounts; create named admin accounts only')))
    lines.append(R(bMid(3, 99, '  [ ] Enable MFA for all interactive logins via IdP / SAML SSO')))
    lines.append(R(bMid(3, 99, '  [ ] Restrict management port (443 (Eyeglass web UI)) to jump host / management VLAN')))
    lines.append(R(bMid(3, 99, '  [ ] Enable audit logging and forward to SIEM (syslog, TLS port 6514)')))
    lines.append(R(bMid(3, 99, '  [ ] Apply all security patches within 30 days of vendor release')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Network Hardening')))
    lines.append(R(bMid(3, 99, '  [ ] Separate backup VLAN — no direct production host access to repo')))
    lines.append(R(bMid(3, 99, '  [ ] Firewall: allow 443 (web UI) · 8080 (REST API) · 8116 (Isilon/PowerScale mgmt)')))
    lines.append(R(bMid(3, 99, '  [ ] Disable unused ports and protocols on management interface')))
    lines.append(R(bMid(3, 99, '  [ ] Immutable repository: enable WORM or object lock on backup target')))
    lines.append(R(bMid(3, 99, '  [ ] Encryption in transit: disable TLS 1.0/1.1; enforce TLS 1.2+')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-troubleshooting',
    'docs/storage/netapp/superna-eyeglass/troubleshooting/index.md',
    'Superna Eyeglass — troubleshooting overview and triage approach',
)
def _dr_superna_troubleshooting():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Superna Eyeglass — Troubleshooting Approach')))
    lines.append(R(bMid(3, 99, '1  Identify: which job, component, or resource is failing')))
    lines.append(R(bMid(3, 99, '2  Scope: single job vs all jobs; one source vs all sources')))
    lines.append(R(bMid(3, 99, '3  Collect: logs and run status command; review recent change history')))
    lines.append(R(bMid(3, 99, '4  Diagnose: match symptoms to known issues; check error codes')))
    lines.append(R(bMid(3, 99, '5  Fix: apply resolution; verify fix; monitor next run')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Infrastructure'), bMid(36, 66, 'Application'), bMid(69, 99, 'Data'))))
    lines.append(R(merge(bMid(3, 33, 'Network checks'), bMid(36, 66, 'Log analysis'), bMid(69, 99, 'Catalog check'))))
    lines.append(R(merge(bMid(3, 33, 'Storage space'), bMid(36, 66, 'Job error codes'), bMid(69, 99, 'Consistency'))))
    lines.append(R(merge(bMid(3, 33, 'Process health'), bMid(36, 66, 'Auth failures'), bMid(69, 99, 'Corruption scan'))))
    lines.append(R(merge(bMid(3, 33, '443 (Eyeglass web UI)'), bMid(36, 66, 'Timeout errors'), bMid(69, 99, 'Restore test'))))
    lines.append(R(merge(bMid(3, 33, 'Firewall rules'), bMid(36, 66, 'Version compat'), bMid(69, 99, 'RPO drift'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-ts-issues',
    'docs/storage/netapp/superna-eyeglass/troubleshooting/common-issues/index.md',
    'Superna Eyeglass — common issues, root causes, and fixes',
)
def _dr_superna_ts_issues():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Common Issues'))
    lines.append(txt_row())
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Symptom', 'Likely Cause', 'First Check', 'Fix', 'Verify'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Sync lag', 'SyncIQ policy slo', 'igls sync status', 'check bandwidth', 'isi sync polic'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['RAPA alert', 'ransomware detect', 'igls rapa status', 'quarantine + esca', 'rapa report'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['DFS broken', 'namespace not upd', 'igls dfs status', 'retry DFS update', 'dfsutil view'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Failover fail', 'pre-check error', 'igls dr precheck', 'fix issue + re-ru', 'igls log'])))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'General Triage Pattern')))
    lines.append(R(bMid(3, 99, '  Is the issue new or recurring? New = recent change; Recurring = config problem')))
    lines.append(R(bMid(3, 99, '  Is it isolated to one source or all? Isolated = agent; All = server/repo')))
    lines.append(R(bMid(3, 99, '  Check logs first: igls sync status')))
    lines.append(R(bMid(3, 99, '  If unresolved in 2h: open vendor case with full log bundle')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-ts-diag',
    'docs/storage/netapp/superna-eyeglass/troubleshooting/diagnostics/index.md',
    'Superna Eyeglass — diagnostic commands and log collection',
)
def _dr_superna_ts_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Diagnostics'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Superna Eyeglass — Diagnostic Commands')))
    lines.append(R(bMid(3, 99, 'Collect these before opening a vendor support case')))
    lines.append(R(bMid(3, 99, '  igls sync status')))
    lines.append(R(bMid(3, 99, '  igls rapa status')))
    lines.append(R(bMid(3, 99, '  Check system logs: /var/log/ or Windows Event Viewer')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Log Collection'), bMid(53, 99, 'Live Diagnostics'))))
    lines.append(R(merge(bMid(3, 50, 'Application log bundle'), bMid(53, 99, 'Network connectivity'))))
    lines.append(R(merge(bMid(3, 50, 'OS syslog (journalctl)'), bMid(53, 99, 'Storage path check'))))
    lines.append(R(merge(bMid(3, 50, 'Core dump if crashed'), bMid(53, 99, 'Process list check'))))
    lines.append(R(merge(bMid(3, 50, 'Config export/backup'), bMid(53, 99, 'Port reachability'))))
    lines.append(R(merge(bMid(3, 50, 'igls sync status'), bMid(53, 99, 'igls rapa status'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-superna-ts-escalation',
    'docs/storage/netapp/superna-eyeglass/troubleshooting/escalation/index.md',
    'Superna Eyeglass — escalation path, vendor support, and SLA',
)
def _dr_superna_ts_escalation():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Superna Eyeglass — Escalation'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Superna Eyeglass — Escalation Path')))
    lines.append(R(bMid(3, 99, 'L1 Triage: review logs, match to known issues in runbook (0–30 min)')))
    lines.append(R(bMid(3, 99, 'L2 Engineering: deep analysis, config review, lab reproduction (30 min – 4 h)')))
    lines.append(R(bMid(3, 99, 'Vendor Support: open case with log bundle if unresolved at L2 (> 4 h)')))
    lines.append(R(bMid(3, 99, 'Sev1 (data loss / production impact): page on-call + open critical case')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Information to Collect Before Escalating')))
    lines.append(R(bMid(3, 99, '  Product version: Superna Eyeglass version string from About / version command')))
    lines.append(R(bMid(3, 99, '  Full log bundle: igls sync status')))
    lines.append(R(bMid(3, 99, '  Symptom timeline: when first occurred; any changes made')))
    lines.append(R(bMid(3, 99, '  Scope: single job / all jobs / all components — narrows root cause')))
    lines.append(R(bMid(3, 99, '  Error codes: exact error messages and exit codes from logs')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection'))
    lines.append(txt_row('RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats'))
    lines.append(txt_row('SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies'))
    lines.append(txt_row('DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS '))
    lines.append(txt_row('Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster'))
    lines.append(txt_row('Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product'))
    lines.append(txt_row('Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits'))
    lines.append(txt_row('Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site'))
    lines.append(txt_row('Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team'))
    lines.append(txt_row('Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha'))
    lines.append(txt_row('Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation'))
    lines.append(txt_row('igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations'))
    lines.append(txt_row('SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation'))
    lines.append(txt_row('Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines


@kb_diagram(
    'dr-veeam',
    'docs/backup/veeam/index.md',
    'VM backup and DR — agentless VMware/Hyper-V backup with instant recovery and replication',
)
def _dr_veeam_overview():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Overview'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Veeam')))
    lines.append(R(bMid(3, 99, 'VM backup and DR — agentless VMware/Hyper-V backup with instant recovery and replication')))
    lines.append(R(bMid(3, 99, 'Veeam Backup Server — scheduler, job engine, catalog, REST API (port 9419)')))
    lines.append(R(bMid(3, 99, 'Backup Proxy        — data mover; VMware VADP for CBT snapshots; SAN/NAS/LAN modes')))
    lines.append(R(bMid(3, 99, 'Backup Repository   — target storage: SOBR, CIFS/NFS, S3 object, dedup appliance')))
    lines.append(R(bMid(3, 99, 'Management: 9419 (Veeam REST API) · Auth: Windows/AD auth for Veeam console; service account')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Architecture: components work together to deliver Veeam capabilities'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Architecture'), bMid(53, 99, 'Operations'))))
    lines.append(R(merge(bMid(3, 50, 'Veeam Backup Server — scheduler, job engine'), bMid(53, 99, 'Add-VBRJob / Start-VBRJob'))))
    lines.append(R(merge(bMid(3, 50, 'Backup Proxy        — data mover; VMware VA'), bMid(53, 99, 'Get-VBRRestorePoint'))))
    lines.append(R(merge(bMid(3, 50, 'Backup Repository   — target storage: SOBR,'), bMid(53, 99, 'Start-VBRInstantVMRecovery'))))
    lines.append(R(merge(bMid(3, 50, 'Mount Server        — used for instant VM r'), bMid(53, 99, 'Get-VBRJob | fl'))))
    lines.append(R(merge(bMid(3, 50, 'Veeam ONE           — optional monitoring: '), bMid(53, 99, 'Invoke-VBRHealthCheck'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-architecture',
    'docs/backup/veeam/architecture/index.md',
    'Veeam — architecture overview, components, data flow',
)
def _dr_veeam_architecture():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Architecture'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Veeam — Component Architecture')))
    lines.append(R(bMid(3, 99, 'Veeam Backup Server — scheduler, job engine, catalog, REST API (port 9419)')))
    lines.append(R(bMid(3, 99, 'Backup Proxy        — data mover; VMware VADP for CBT snapshots; SAN/NAS/LAN modes')))
    lines.append(R(bMid(3, 99, 'Backup Repository   — target storage: SOBR, CIFS/NFS, S3 object, dedup appliance')))
    lines.append(R(bMid(3, 99, 'Ports: 9419 (Veeam REST API) · 6160 (Veeam Agent) · 443 (vCenter)')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Three-tier component model — control plane, data plane, and management'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Control Plane'), bMid(36, 66, 'Data Plane'), bMid(69, 99, 'Management'))))
    lines.append(R(merge(bMid(3, 33, 'Veeam Backup Server — schedu'), bMid(36, 66, 'Backup Proxy        — data m'), bMid(69, 99, 'Mount Server        — used f'))))
    lines.append(R(merge(bMid(3, 33, 'Scheduling'), bMid(36, 66, 'Replication/Backup'), bMid(69, 99, '9419 (Veeam REST API)'))))
    lines.append(R(merge(bMid(3, 33, 'Policy mgmt'), bMid(36, 66, 'Data movement'), bMid(69, 99, 'REST API'))))
    lines.append(R(merge(bMid(3, 33, 'Catalog/DB'), bMid(36, 66, 'Dedup/compress'), bMid(69, 99, 'RBAC'))))
    lines.append(R(merge(bMid(3, 33, 'Job engine'), bMid(36, 66, '6160 (Veeam Agent)'), bMid(69, 99, 'Alerting'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-arch-how-it-works',
    'docs/backup/veeam/architecture/how-it-works/index.md',
    'Veeam — how replication or backup data flows step by step',
)
def _dr_veeam_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('  Veeam data flow — from source to target through the protection pipeline:'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, '1  Source / Production System')))
    lines.append(R(bMid(3, 99, '   Veeam Backup Server — scheduler, job engine, catalog, REST API (port 9419)')))
    lines.append(R(bMid(3, 99, '   Host writes are intercepted or snapshotted by the Veeam agent/proxy')))
    lines.append(R(bMid(3, 99, '   Changed blocks tracked via CBT / journal / delta-set mechanism')))
    lines.append(R(bMid(3, 99, '   Consistency ensured at quiesce point before data transfer begins')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Changed data forwarded to the Veeam engine — compression and encryption applied in transit'))
    lines.append(txt_row())
    lines.append(R(arrow([51])))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, '2  Veeam Engine')))
    lines.append(R(bMid(3, 99, '   Backup Proxy        — data mover; VMware VADP for CBT snapshots; SAN/NAS/LAN modes')))
    lines.append(R(bMid(3, 99, '   Data compressed, deduplicated, and encrypted before storage')))
    lines.append(R(bMid(3, 99, '   Metadata catalog updated; job status reported to control plane')))
    lines.append(R(bMid(3, 99, '   Add-VBRJob / Start-VBRJob')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([51])))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, '3  Target / Repository')))
    lines.append(R(bMid(3, 99, '   Backup Repository   — target storage: SOBR, CIFS/NFS, S3 object, dedup appliance')))
    lines.append(R(bMid(3, 99, '   Recovery point written; retention policy applied automatically')))
    lines.append(R(bMid(3, 99, '   Restore: Get-VBRRestorePoint')))
    lines.append(R(bMid(3, 99, '   RTO driven by target storage performance and data volume')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-arch-design',
    'docs/backup/veeam/architecture/design-standards/index.md',
    'Veeam — sizing, design rules, capacity, HA guidelines',
)
def _dr_veeam_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Design Standards'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Sizing Guidelines'), bMid(53, 99, 'HA Requirements'))))
    lines.append(R(merge(bMid(3, 50, 'Deduplicate where supported'), bMid(53, 99, 'N+1 component redundancy'))))
    lines.append(R(merge(bMid(3, 50, 'Bandwidth: 10 GbE minimum'), bMid(53, 99, 'Heartbeat / health monitor'))))
    lines.append(R(merge(bMid(3, 50, 'Storage: 130% of raw data'), bMid(53, 99, 'Separate mgmt / data VLANs'))))
    lines.append(R(merge(bMid(3, 50, 'Latency: < 10 ms to storage'), bMid(53, 99, 'Out-of-band access (IPMI)'))))
    lines.append(R(merge(bMid(3, 50, 'CPU: 8+ vCPU for engine'), bMid(53, 99, 'Anti-affinity VM placement'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('  Ports: 9419 (Veeam REST API) · 6160 (Veeam Agent) · 443 (vCenter)'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Standard Veeam Design Rules')))
    lines.append(R(bMid(3, 99, 'RPO target drives snapshot/cycle frequency — document in service design')))
    lines.append(R(bMid(3, 99, 'RTO target drives recovery tier: instant, warm standby, or cold restore')))
    lines.append(R(bMid(3, 99, 'Dedicated backup network VLAN — no shared production traffic')))
    lines.append(R(bMid(3, 99, 'Encryption: AES-256 backup (key in Veeam DB); TLS on all management; WORM repo supported')))
    lines.append(R(bMid(3, 99, 'Service accounts: minimum privilege; rotate credentials quarterly')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-arch-integrations',
    'docs/backup/veeam/architecture/integrations/index.md',
    'Veeam — integration points with external systems and APIs',
)
def _dr_veeam_arch_integrations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Architecture Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Veeam — External Integration Points')))
    lines.append(R(bMid(3, 99, 'Auth: Windows/AD auth for Veeam console; service account with vSphere admin; repo credentials')))
    lines.append(R(bMid(3, 99, 'Storage: connected via 9419 (Veeam REST API) · 6160 (Veeam Agent)')))
    lines.append(R(bMid(3, 99, 'Monitoring: SNMP traps / syslog / REST API to ITSM and alerting systems')))
    lines.append(R(bMid(3, 99, 'Encryption: AES-256 backup (key in Veeam config DB); TLS on all management; WORM repos')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Identity'), bMid(36, 66, 'Storage'), bMid(69, 99, 'Monitoring'))))
    lines.append(R(merge(bMid(3, 33, 'AD / LDAP'), bMid(36, 66, '9419 (Veeam REST API)'), bMid(69, 99, 'SNMP / syslog'))))
    lines.append(R(merge(bMid(3, 33, 'SAML SSO'), bMid(36, 66, '6160 (Veeam Agent)'), bMid(69, 99, 'REST webhook'))))
    lines.append(R(merge(bMid(3, 33, 'RBAC roles'), bMid(36, 66, 'NFS / iSCSI / FC'), bMid(69, 99, 'Email alerts'))))
    lines.append(R(merge(bMid(3, 33, 'MFA optional'), bMid(36, 66, 'Dedup appliance'), bMid(69, 99, 'ServiceNow'))))
    lines.append(R(merge(bMid(3, 33, 'Cert auth'), bMid(36, 66, 'Object storage'), bMid(69, 99, 'Prometheus'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-operations',
    'docs/backup/veeam/operations/index.md',
    'Veeam — operations overview, key tasks, day-to-day procedures',
)
def _dr_veeam_operations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Veeam — Day-to-Day Operations')))
    lines.append(R(bMid(3, 99, 'Daily: review job status · check health alerts · verify last backup/replica')))
    lines.append(R(bMid(3, 99, 'Weekly: review capacity trends · test restore sample · review error logs')))
    lines.append(R(bMid(3, 99, 'Monthly: full restore test · review retention · audit service accounts')))
    lines.append(R(bMid(3, 99, 'Quarterly: DR failover test · firmware review · update documentation')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Backup/Replicate'), bMid(36, 66, 'Monitor'), bMid(69, 99, 'Recover'))))
    lines.append(R(merge(bMid(3, 33, 'Add-VBRJob / Start-VBRJob'), bMid(36, 66, 'Start-VBRInstantVMRecovery'), bMid(69, 99, 'Get-VBRRestorePoint'))))
    lines.append(R(merge(bMid(3, 33, 'Schedule jobs'), bMid(36, 66, 'Health checks'), bMid(69, 99, 'Instant restore'))))
    lines.append(R(merge(bMid(3, 33, 'Retention mgmt'), bMid(36, 66, 'Capacity alerts'), bMid(69, 99, 'Failover test'))))
    lines.append(R(merge(bMid(3, 33, 'Consistency grp'), bMid(36, 66, 'Log review'), bMid(69, 99, 'DR runbook'))))
    lines.append(R(merge(bMid(3, 33, 'Policy updates'), bMid(36, 66, 'SLA tracking'), bMid(69, 99, 'Validate RTO'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-ops-backup',
    'docs/backup/veeam/operations/backup-restore/index.md',
    'Veeam — backup and restore procedures',
)
def _dr_veeam_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Backup & Restore'))
    lines.append(txt_row())
    lines.append(txt_row('  Backup flow: quiesce source → snapshot/copy → transfer → write to target → catalog'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Backup (Protection)'), bMid(53, 99, 'Restore (Recovery)'))))
    lines.append(R(merge(bMid(3, 50, 'Add-VBRJob / Start-VBRJob'), bMid(53, 99, 'Get-VBRRestorePoint'))))
    lines.append(R(merge(bMid(3, 50, 'Quiesce source I/O'), bMid(53, 99, 'Select recovery point'))))
    lines.append(R(merge(bMid(3, 50, 'Take snapshot / CBT'), bMid(53, 99, 'Mount or copy to target'))))
    lines.append(R(merge(bMid(3, 50, 'Transfer changed blocks'), bMid(53, 99, 'Validate integrity'))))
    lines.append(R(merge(bMid(3, 50, 'Commit to repository'), bMid(53, 99, 'Restart application'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Key Veeam Commands')))
    lines.append(R(bMid(3, 99, '  Backup trigger  : Add-VBRJob / Start-VBRJob')))
    lines.append(R(bMid(3, 99, '  List points     : Get-VBRRestorePoint')))
    lines.append(R(bMid(3, 99, '  Health status   : Start-VBRInstantVMRecovery')))
    lines.append(R(bMid(3, 99, '  Retention mgmt  : Invoke-VBRHealthCheck')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-ops-cli',
    'docs/backup/veeam/operations/cli-reference/index.md',
    'Veeam — CLI commands reference',
)
def _dr_veeam_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — CLI Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Veeam — Command Reference')))
    lines.append(R(bMid(3, 99, 'Use these commands for routine operations, scripting, and troubleshooting')))
    lines.append(R(bMid(3, 99, '  Add-VBRJob / Start-VBRJob')))
    lines.append(R(bMid(3, 99, '  Get-VBRRestorePoint')))
    lines.append(R(bMid(3, 99, '  Start-VBRInstantVMRecovery')))
    lines.append(R(bMid(3, 99, '  Get-VBRJob | fl')))
    lines.append(R(bMid(3, 99, '  Invoke-VBRHealthCheck')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Ports: 9419 (Veeam REST API) · 6160 (Veeam Agent) · 443 (vCenter)'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Command Categories')))
    lines.append(R(bMid(3, 99, '  Status / Query  — check current state, list jobs, show config')))
    lines.append(R(bMid(3, 99, '  Operations      — start, stop, failover, restore, sync, expire')))
    lines.append(R(bMid(3, 99, '  Configuration   — add/modify policies, schedules, storage targets')))
    lines.append(R(bMid(3, 99, '  Diagnostics     — collect logs, run health checks, test connectivity')))
    lines.append(R(bMid(3, 99, '  Scripting       — REST API or CLI for automation and reporting')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-ops-health',
    'docs/backup/veeam/operations/health-checks/index.md',
    'Veeam — health check procedures and monitoring commands',
)
def _dr_veeam_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Health Checks'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Veeam — Health Check Procedures')))
    lines.append(R(bMid(3, 99, 'Run these checks daily/weekly to confirm protection is working')))
    lines.append(R(bMid(3, 99, '  Start-VBRInstantVMRecovery')))
    lines.append(R(bMid(3, 99, '  Review job completion rate — target 100%; investigate failures')))
    lines.append(R(bMid(3, 99, '  Check replication/backup lag against RPO target')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Check', 'What to verify', 'Expected', 'Frequency', 'Action if bad'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Job status', 'All jobs complete', '100% success', 'Daily', 'Triage failures'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Lag / RPO', 'Replication lag', '< RPO target', 'Daily', 'Tune bandwidth'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Capacity', 'Repo space used', '< 80% full', 'Weekly', 'Expand or expire'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Restore test', 'Random restore', 'Data intact', 'Monthly', 'Fix backup chain'])))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-ops-install',
    'docs/backup/veeam/operations/install-upgrade/index.md',
    'Veeam — install and upgrade procedures',
)
def _dr_veeam_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Install & Upgrade'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Veeam — Installation Prerequisites')))
    lines.append(R(bMid(3, 99, '  OS: supported Linux or Windows Server (see vendor compatibility matrix)')))
    lines.append(R(bMid(3, 99, '  Network: 9419 (Veeam REST API) · 6160 (Veeam Agent) — ensure firewall allows these')))
    lines.append(R(bMid(3, 99, '  Auth: Windows/AD auth for Veeam console; service account with vSphere admin; repo credentials')))
    lines.append(R(bMid(3, 99, '  Storage: Windows Backup Server · Proxy VMs on ESXi · Backup storage (NAS/SAN)')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([51])))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Install Sequence')))
    lines.append(R(bMid(3, 99, '  1  Deploy control plane component and configure network access')))
    lines.append(R(bMid(3, 99, '  2  Configure storage and network connectivity')))
    lines.append(R(bMid(3, 99, '  3  Install agent/proxy/splitter on protected hosts')))
    lines.append(R(bMid(3, 99, '  4  Register sources and configure protection policies')))
    lines.append(R(bMid(3, 99, '  5  Run first job; verify completion; test restore')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Upgrade Sequence')))
    lines.append(R(bMid(3, 99, '  1  Review release notes and compatibility matrix before upgrade')))
    lines.append(R(bMid(3, 99, '  2  Snapshot or backup the control plane VM before upgrading')))
    lines.append(R(bMid(3, 99, '  3  Upgrade control plane first, then proxies/agents/appliances')))
    lines.append(R(bMid(3, 99, '  4  Validate jobs resume automatically after upgrade')))
    lines.append(R(bMid(3, 99, '  5  Document version change and update CMDB record')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-ops-procedures',
    'docs/backup/veeam/operations/procedures/index.md',
    'Veeam — operational procedures and runbooks',
)
def _dr_veeam_ops_procedures():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Procedures'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Routine Procedures'), bMid(53, 99, 'DR Procedures'))))
    lines.append(R(merge(bMid(3, 50, 'Add new protection source'), bMid(53, 99, 'Initiate failover'))))
    lines.append(R(merge(bMid(3, 50, 'Modify retention policy'), bMid(53, 99, 'Validate replica'))))
    lines.append(R(merge(bMid(3, 50, 'Expire old recover points'), bMid(53, 99, 'Redirect host I/O'))))
    lines.append(R(merge(bMid(3, 50, 'Add storage capacity'), bMid(53, 99, 'Test failover (non-disrupt)'))))
    lines.append(R(merge(bMid(3, 50, 'Service account rotation'), bMid(53, 99, 'Failback to production'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Change Control Requirements for Veeam')))
    lines.append(R(bMid(3, 99, '  All changes to protection policies require change ticket with rollback plan')))
    lines.append(R(bMid(3, 99, '  Failover tests must be scheduled in maintenance window')))
    lines.append(R(bMid(3, 99, '  Firmware/software upgrades need 48 h pre-approval and backup snapshot')))
    lines.append(R(bMid(3, 99, '  Post-change: verify jobs run successfully for 2 backup cycles')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-ops-scripts',
    'docs/backup/veeam/operations/scripts/index.md',
    'Veeam — automation scripts and examples',
)
def _dr_veeam_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Scripts'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Veeam — Automation Scripts')))
    lines.append(R(bMid(3, 99, 'Scripts automate routine Veeam operations — run via cron or CI/CD')))
    lines.append(R(bMid(3, 99, 'Always store credentials in vault (not in script); log all output')))
    lines.append(R(bMid(3, 99, 'Test scripts in non-production before scheduling in production')))
    lines.append(R(bMid(3, 99, 'Scope scripts to least-privilege service account')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Status / Reporting Scripts'), bMid(53, 99, 'Automation Scripts'))))
    lines.append(R(merge(bMid(3, 50, 'Job success rate report'), bMid(53, 99, 'Auto-expire old points'))))
    lines.append(R(merge(bMid(3, 50, 'Capacity trending'), bMid(53, 99, 'Auto-add new VMs to policy'))))
    lines.append(R(merge(bMid(3, 50, 'SLA compliance report'), bMid(53, 99, 'Nightly DR test validation'))))
    lines.append(R(merge(bMid(3, 50, 'RPO / RTO dashboard'), bMid(53, 99, 'Alert on job failure'))))
    lines.append(R(merge(bMid(3, 50, 'Start-VBRInstantVMRecovery'), bMid(53, 99, 'Get-VBRJob | fl'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-security',
    'docs/backup/veeam/security/index.md',
    'Veeam — security overview, controls, compliance posture',
)
def _dr_veeam_security():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Security'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Veeam — Security Posture')))
    lines.append(R(bMid(3, 99, 'Authentication: Windows/AD for Veeam console; vSphere admin service acct; repo creds')))
    lines.append(R(bMid(3, 99, 'Encryption: AES-256 backup (key in Veeam config DB); TLS on all management; WORM repos')))
    lines.append(R(bMid(3, 99, 'Network: management VLAN separated; 443 (vCenter) management port')))
    lines.append(R(bMid(3, 99, 'Audit: all admin actions logged; log retention minimum 1 year')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Access Control'), bMid(36, 66, 'Encryption'), bMid(69, 99, 'Audit'))))
    lines.append(R(merge(bMid(3, 33, 'RBAC roles'), bMid(36, 66, 'AES-256 at rest'), bMid(69, 99, 'Admin actions'))))
    lines.append(R(merge(bMid(3, 33, 'Least privilege'), bMid(36, 66, 'TLS in transit'), bMid(69, 99, 'Login events'))))
    lines.append(R(merge(bMid(3, 33, 'MFA optional'), bMid(36, 66, 'Key rotation'), bMid(69, 99, 'Syslog export'))))
    lines.append(R(merge(bMid(3, 33, 'SVC acct rotate'), bMid(36, 66, 'WORM / immutable'), bMid(69, 99, 'SIEM forward'))))
    lines.append(R(merge(bMid(3, 33, 'Just-In-Time'), bMid(36, 66, 'KMS managed'), bMid(69, 99, 'Quarterly review'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-sec-access',
    'docs/backup/veeam/security/access-control/index.md',
    'Veeam — RBAC, permissions, service accounts',
)
def _dr_veeam_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Access Control'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Veeam — RBAC and Access Control')))
    lines.append(R(bMid(3, 99, 'Auth: Windows/AD auth for Veeam console; service account with vSphere admin; repo credentials')))
    lines.append(R(bMid(3, 99, 'Principle of least privilege: each role gets only required permissions')))
    lines.append(R(bMid(3, 99, 'Service accounts: dedicated, non-interactive; rotation every 90 days')))
    lines.append(R(bMid(3, 99, 'Emergency break-glass: documented, monitored, time-limited access')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Role', 'Access Level', 'Typical User', 'Review Freq', 'Granted By'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Admin', 'Full config/ops', 'Sr Backup Eng', 'Quarterly', 'Security team'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Operator', 'Start/stop jobs', 'Backup Eng', 'Quarterly', 'Team lead'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Monitor', 'Read-only view', 'NOC / L1', 'Quarterly', 'Team lead'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Service Acct', 'API / headless', 'Automation', 'Per rotation', 'Security team'])))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-sec-auth',
    'docs/backup/veeam/security/authentication/index.md',
    'Veeam — authentication methods, certificate management',
)
def _dr_veeam_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Authentication'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Veeam — Authentication Methods')))
    lines.append(R(bMid(3, 99, 'Windows/AD auth for Veeam console; service account with vSphere admin; repo credentials')))
    lines.append(R(bMid(3, 99, 'Management UI: HTTPS on 9419 (Veeam REST API) — browser-based login')))
    lines.append(R(bMid(3, 99, 'API: bearer token or service account; rotate credentials quarterly')))
    lines.append(R(bMid(3, 99, 'Inter-component: certificate-based mutual TLS between engines')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Human Access'), bMid(53, 99, 'Machine Access'))))
    lines.append(R(merge(bMid(3, 50, 'AD / LDAP integration'), bMid(53, 99, 'Service account'))))
    lines.append(R(merge(bMid(3, 50, 'SAML SSO optional'), bMid(53, 99, 'API key / token'))))
    lines.append(R(merge(bMid(3, 50, 'MFA via IdP'), bMid(53, 99, 'Certificate auth'))))
    lines.append(R(merge(bMid(3, 50, 'Session timeout 15 min'), bMid(53, 99, 'Rotate every 90 d'))))
    lines.append(R(merge(bMid(3, 50, 'Audit login events'), bMid(53, 99, 'Vault-stored secrets'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-sec-enc',
    'docs/backup/veeam/security/encryption/index.md',
    'Veeam — encryption at rest and in transit',
)
def _dr_veeam_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Encryption'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Veeam — Encryption Configuration')))
    lines.append(R(bMid(3, 99, 'AES-256 backup encryption (key stored in Veeam config DB); TLS on all management; WORM repos')))
    lines.append(R(bMid(3, 99, 'In-transit: TLS 1.2+ for all management; data channel also encrypted')))
    lines.append(R(bMid(3, 99, 'At-rest: AES-256 on repository or vault storage; key managed by KMS')))
    lines.append(R(bMid(3, 99, 'Key lifecycle: generate → use → rotate (annual) → retire → destroy')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'In-Transit'), bMid(53, 99, 'At-Rest'))))
    lines.append(R(merge(bMid(3, 50, 'TLS 1.2+ (minimum)'), bMid(53, 99, 'AES-256 encryption'))))
    lines.append(R(merge(bMid(3, 50, '9419 (Veeam REST API) HTTPS'), bMid(53, 99, 'KMS key management'))))
    lines.append(R(merge(bMid(3, 50, 'Mutual TLS internal'), bMid(53, 99, 'WORM / immutable'))))
    lines.append(R(merge(bMid(3, 50, 'Cert rotation annual'), bMid(53, 99, 'Key rotation annual'))))
    lines.append(R(merge(bMid(3, 50, 'No plain-text admin'), bMid(53, 99, 'Audit key access'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-sec-hardening',
    'docs/backup/veeam/security/hardening/index.md',
    'Veeam — hardening guide, CIS controls, secure configuration',
)
def _dr_veeam_sec_hardening():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Hardening'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Veeam — Hardening Checklist')))
    lines.append(R(bMid(3, 99, '  [ ] Disable default/admin accounts; create named admin accounts only')))
    lines.append(R(bMid(3, 99, '  [ ] Enable MFA for all interactive logins via IdP / SAML SSO')))
    lines.append(R(bMid(3, 99, '  [ ] Restrict management port (9419 (Veeam REST API)) to jump host / management VLAN')))
    lines.append(R(bMid(3, 99, '  [ ] Enable audit logging and forward to SIEM (syslog, TLS port 6514)')))
    lines.append(R(bMid(3, 99, '  [ ] Apply all security patches within 30 days of vendor release')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Network Hardening')))
    lines.append(R(bMid(3, 99, '  [ ] Separate backup VLAN — no direct production host access to repo')))
    lines.append(R(bMid(3, 99, '  [ ] Firewall: allow only 9419 (Veeam REST API) · 6160 (Veeam Agent) · 443 (vCenter)')))
    lines.append(R(bMid(3, 99, '  [ ] Disable unused ports and protocols on management interface')))
    lines.append(R(bMid(3, 99, '  [ ] Immutable repository: enable WORM or object lock on backup target')))
    lines.append(R(bMid(3, 99, '  [ ] Encryption in transit: disable TLS 1.0/1.1; enforce TLS 1.2+')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-troubleshooting',
    'docs/backup/veeam/troubleshooting/index.md',
    'Veeam — troubleshooting overview and triage approach',
)
def _dr_veeam_troubleshooting():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Veeam — Troubleshooting Approach')))
    lines.append(R(bMid(3, 99, '1  Identify: which job, component, or resource is failing')))
    lines.append(R(bMid(3, 99, '2  Scope: single job vs all jobs; one source vs all sources')))
    lines.append(R(bMid(3, 99, '3  Collect: logs and run status command; review recent change history')))
    lines.append(R(bMid(3, 99, '4  Diagnose: match symptoms to known issues; check error codes')))
    lines.append(R(bMid(3, 99, '5  Fix: apply resolution; verify fix; monitor next run')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Infrastructure'), bMid(36, 66, 'Application'), bMid(69, 99, 'Data'))))
    lines.append(R(merge(bMid(3, 33, 'Network checks'), bMid(36, 66, 'Log analysis'), bMid(69, 99, 'Catalog check'))))
    lines.append(R(merge(bMid(3, 33, 'Storage space'), bMid(36, 66, 'Job error codes'), bMid(69, 99, 'Consistency'))))
    lines.append(R(merge(bMid(3, 33, 'Process health'), bMid(36, 66, 'Auth failures'), bMid(69, 99, 'Corruption scan'))))
    lines.append(R(merge(bMid(3, 33, '9419 (Veeam REST API)'), bMid(36, 66, 'Timeout errors'), bMid(69, 99, 'Restore test'))))
    lines.append(R(merge(bMid(3, 33, 'Firewall rules'), bMid(36, 66, 'Version compat'), bMid(69, 99, 'RPO drift'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-ts-issues',
    'docs/backup/veeam/troubleshooting/common-issues/index.md',
    'Veeam — common issues, root causes, and fixes',
)
def _dr_veeam_ts_issues():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Common Issues'))
    lines.append(txt_row())
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Symptom', 'Likely Cause', 'First Check', 'Fix', 'Verify'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Snapshot not relea', 'proxy error mid-j', 'check proxy logs', 'run snapshot clea', 'Get-VBRJob'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['CBT reset', 'VMware tools upda', 'rescan VM disks', 'force full backup', 'Reset-VBRVMCBT'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Repo full', 'retention not del', 'check GFS config', 'expire old points', 'Remove-VBRBack'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Instant recovery s', 'NFS mount latency', 'check mount serve', 'migrate to datast', 'veeam log'])))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'General Triage Pattern')))
    lines.append(R(bMid(3, 99, '  Is the issue new or recurring? New = recent change; Recurring = config problem')))
    lines.append(R(bMid(3, 99, '  Is it isolated to one source or all? Isolated = agent; All = server/repo')))
    lines.append(R(bMid(3, 99, '  Check logs first: Start-VBRInstantVMRecovery')))
    lines.append(R(bMid(3, 99, '  If unresolved in 2h: open vendor case with full log bundle')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-ts-diag',
    'docs/backup/veeam/troubleshooting/diagnostics/index.md',
    'Veeam — diagnostic commands and log collection',
)
def _dr_veeam_ts_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Diagnostics'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Veeam — Diagnostic Commands')))
    lines.append(R(bMid(3, 99, 'Collect these before opening a vendor support case')))
    lines.append(R(bMid(3, 99, '  Start-VBRInstantVMRecovery')))
    lines.append(R(bMid(3, 99, '  Get-VBRJob | fl')))
    lines.append(R(bMid(3, 99, '  Check system logs: /var/log/ or Windows Event Viewer')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Log Collection'), bMid(53, 99, 'Live Diagnostics'))))
    lines.append(R(merge(bMid(3, 50, 'Application log bundle'), bMid(53, 99, 'Network connectivity'))))
    lines.append(R(merge(bMid(3, 50, 'OS syslog (journalctl)'), bMid(53, 99, 'Storage path check'))))
    lines.append(R(merge(bMid(3, 50, 'Core dump if crashed'), bMid(53, 99, 'Process list check'))))
    lines.append(R(merge(bMid(3, 50, 'Config export/backup'), bMid(53, 99, 'Port reachability'))))
    lines.append(R(merge(bMid(3, 50, 'Start-VBRInstantVMRecovery'), bMid(53, 99, 'Get-VBRJob | fl'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-veeam-ts-escalation',
    'docs/backup/veeam/troubleshooting/escalation/index.md',
    'Veeam — escalation path, vendor support, and SLA',
)
def _dr_veeam_ts_escalation():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Veeam — Escalation'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Veeam — Escalation Path')))
    lines.append(R(bMid(3, 99, 'L1 Triage: review logs, match to known issues in runbook (0–30 min)')))
    lines.append(R(bMid(3, 99, 'L2 Engineering: deep analysis, config review, lab reproduction (30 min – 4 h)')))
    lines.append(R(bMid(3, 99, 'Vendor Support: open case with log bundle if unresolved at L2 (> 4 h)')))
    lines.append(R(bMid(3, 99, 'Sev1 (data loss / production impact): page on-call + open critical case')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Information to Collect Before Escalating')))
    lines.append(R(bMid(3, 99, '  Product version: Veeam version string from About / version command')))
    lines.append(R(bMid(3, 99, '  Full log bundle: Start-VBRInstantVMRecovery')))
    lines.append(R(bMid(3, 99, '  Symptom timeline: when first occurred; any changes made')))
    lines.append(R(bMid(3, 99, '  Scope: single job / all jobs / all components — narrows root cause')))
    lines.append(R(bMid(3, 99, '  Error codes: exact error messages and exit codes from logs')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Windows Server (Backup Server) · Proxy VMs on ESXi · Backup storage (NAS/SAN) · Management LAN'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Backup Server = central Veeam component: scheduler, job engine, catalog, REST API'))
    lines.append(txt_row('Backup Proxy  = data mover between vSphere and repository; runs in virtual-appliance mode or H'))
    lines.append(txt_row('CBT           = Changed Block Tracking; VMware VADP mechanism to track changed disk sectors'))
    lines.append(txt_row('VADP          = VMware vSphere APIs for Data Protection; enables agentless VM backup'))
    lines.append(txt_row('SOBR          = Scale-Out Backup Repository; tiers extents; moves cold data to object storage'))
    lines.append(txt_row('Instant Recovery= mounts VM disks from backup directly to ESXi; VM live in seconds'))
    lines.append(txt_row('SureBackup    = automated backup verification; test-restores VM in isolated virtual lab'))
    lines.append(txt_row('Replication   = creates VM replica at DR site; enables failover without full restore time'))
    lines.append(txt_row('GFS Retention = Grandfather-Father-Son retention: daily, weekly, monthly, yearly restore points'))
    lines.append(txt_row('Immutable Repo= object storage (S3 WORM) or Linux XFS (immutable flag) repo; ransomware protec'))
    lines.append(txt_row('Mount Server  = Windows host presenting backup as iSCSI/NFS datastore for instant recovery'))
    lines.append(txt_row('VeeamZIP      = ad-hoc compressed portable backup of a single VM; no job required'))
    lines.append(txt_row('Health Check  = periodic backup integrity scan; verifies restore points are readable'))
    lines.append(txt_row('Forward Incremental= default mode; one full + daily incrementals; synthetic full created perio'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines


@kb_diagram(
    'dr-failover',
    'docs/backup/runbooks/failover/index.md',
    'DR Failover Procedure — declare disaster, activate DR site, redirect hosts, validate',
)
def _dr_failover():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'DR Failover Procedure'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'DR Failover Procedure — declare disaster, activate DR site, redirect hosts, validate')))
    lines.append(R(bMid(3, 99, 'See product-specific sub-sections for detailed procedures')))
    lines.append(R(bMid(3, 99, 'DR success depends on: documented runbooks · tested failover · validated RTO')))
    lines.append(R(bMid(3, 99, 'Minimum DR posture: defined RPO/RTO · tested backups · known escalation path')))
    lines.append(R(bMid(3, 99, 'Test DR procedures quarterly; document results; update runbooks after each test')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Production site · DR site · Replication link · Management network · Vault network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPO           = Recovery Point Objective; max acceptable data loss window'))
    lines.append(txt_row('RTO           = Recovery Time Objective; max acceptable downtime before restore'))
    lines.append(txt_row('Failover      = activating the DR site; redirecting hosts to replica resources'))
    lines.append(txt_row('Failback      = returning operations to production site after DR resolved'))
    lines.append(txt_row('Runbook       = step-by-step documented procedure for a specific DR scenario'))
    lines.append(txt_row('IRE           = Isolated Recovery Environment; air-gapped clean-room for recovery'))
    lines.append(txt_row('Clean Room    = isolated vCenter + workstations for cyber recovery validation'))
    lines.append(txt_row('Air Gap       = network isolation preventing attacker lateral movement to vault'))
    lines.append(txt_row('DR Test       = planned failover test; validates RTO without real disaster'))
    lines.append(txt_row('Replication   = continuous or periodic data copy to secondary site or vault'))
    lines.append(txt_row('Recovery Tier = classification: hot/warm/cold based on RTO requirement'))
    lines.append(txt_row('BIA           = Business Impact Analysis; drives RPO/RTO targets per system'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-failback',
    'docs/backup/runbooks/failback/index.md',
    'DR Failback Procedure — reverse replicate, re-sync, validate, cut back to production',
)
def _dr_failback():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'DR Failback Procedure'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'DR Failback Procedure — reverse replicate, re-sync, validate, cut back to production')))
    lines.append(R(bMid(3, 99, 'See product-specific sub-sections for detailed procedures')))
    lines.append(R(bMid(3, 99, 'DR success depends on: documented runbooks · tested failover · validated RTO')))
    lines.append(R(bMid(3, 99, 'Minimum DR posture: defined RPO/RTO · tested backups · known escalation path')))
    lines.append(R(bMid(3, 99, 'Test DR procedures quarterly; document results; update runbooks after each test')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Production site · DR site · Replication link · Management network · Vault network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPO           = Recovery Point Objective; max acceptable data loss window'))
    lines.append(txt_row('RTO           = Recovery Time Objective; max acceptable downtime before restore'))
    lines.append(txt_row('Failover      = activating the DR site; redirecting hosts to replica resources'))
    lines.append(txt_row('Failback      = returning operations to production site after DR resolved'))
    lines.append(txt_row('Runbook       = step-by-step documented procedure for a specific DR scenario'))
    lines.append(txt_row('IRE           = Isolated Recovery Environment; air-gapped clean-room for recovery'))
    lines.append(txt_row('Clean Room    = isolated vCenter + workstations for cyber recovery validation'))
    lines.append(txt_row('Air Gap       = network isolation preventing attacker lateral movement to vault'))
    lines.append(txt_row('DR Test       = planned failover test; validates RTO without real disaster'))
    lines.append(txt_row('Replication   = continuous or periodic data copy to secondary site or vault'))
    lines.append(txt_row('Recovery Tier = classification: hot/warm/cold based on RTO requirement'))
    lines.append(txt_row('BIA           = Business Impact Analysis; drives RPO/RTO targets per system'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-runbook',
    'docs/backup/runbooks/dr-runbook/index.md',
    'DR Runbook — pre-defined response steps for declared disaster across all DR tools',
)
def _dr_runbook():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'DR Runbook'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'DR Runbook — pre-defined response steps for declared disaster across all DR tools')))
    lines.append(R(bMid(3, 99, 'See product-specific sub-sections for detailed procedures')))
    lines.append(R(bMid(3, 99, 'DR success depends on: documented runbooks · tested failover · validated RTO')))
    lines.append(R(bMid(3, 99, 'Minimum DR posture: defined RPO/RTO · tested backups · known escalation path')))
    lines.append(R(bMid(3, 99, 'Test DR procedures quarterly; document results; update runbooks after each test')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Production site · DR site · Replication link · Management network · Vault network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPO           = Recovery Point Objective; max acceptable data loss window'))
    lines.append(txt_row('RTO           = Recovery Time Objective; max acceptable downtime before restore'))
    lines.append(txt_row('Failover      = activating the DR site; redirecting hosts to replica resources'))
    lines.append(txt_row('Failback      = returning operations to production site after DR resolved'))
    lines.append(txt_row('Runbook       = step-by-step documented procedure for a specific DR scenario'))
    lines.append(txt_row('IRE           = Isolated Recovery Environment; air-gapped clean-room for recovery'))
    lines.append(txt_row('Clean Room    = isolated vCenter + workstations for cyber recovery validation'))
    lines.append(txt_row('Air Gap       = network isolation preventing attacker lateral movement to vault'))
    lines.append(txt_row('DR Test       = planned failover test; validates RTO without real disaster'))
    lines.append(txt_row('Replication   = continuous or periodic data copy to secondary site or vault'))
    lines.append(txt_row('Recovery Tier = classification: hot/warm/cold based on RTO requirement'))
    lines.append(txt_row('BIA           = Business Impact Analysis; drives RPO/RTO targets per system'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-ire',
    'docs/backup/ire/index.md',
    'Isolated Recovery Environment — air-gapped clean-room for ransomware recovery',
)
def _dr_ire():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'Isolated Recovery Environment'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Isolated Recovery Environment — air-gapped clean-room for ransomware recovery')))
    lines.append(R(bMid(3, 99, 'See product-specific sub-sections for detailed procedures')))
    lines.append(R(bMid(3, 99, 'DR success depends on: documented runbooks · tested failover · validated RTO')))
    lines.append(R(bMid(3, 99, 'Minimum DR posture: defined RPO/RTO · tested backups · known escalation path')))
    lines.append(R(bMid(3, 99, 'Test DR procedures quarterly; document results; update runbooks after each test')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Production site · DR site · Replication link · Management network · Vault network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPO           = Recovery Point Objective; max acceptable data loss window'))
    lines.append(txt_row('RTO           = Recovery Time Objective; max acceptable downtime before restore'))
    lines.append(txt_row('Failover      = activating the DR site; redirecting hosts to replica resources'))
    lines.append(txt_row('Failback      = returning operations to production site after DR resolved'))
    lines.append(txt_row('Runbook       = step-by-step documented procedure for a specific DR scenario'))
    lines.append(txt_row('IRE           = Isolated Recovery Environment; air-gapped clean-room for recovery'))
    lines.append(txt_row('Clean Room    = isolated vCenter + workstations for cyber recovery validation'))
    lines.append(txt_row('Air Gap       = network isolation preventing attacker lateral movement to vault'))
    lines.append(txt_row('DR Test       = planned failover test; validates RTO without real disaster'))
    lines.append(txt_row('Replication   = continuous or periodic data copy to secondary site or vault'))
    lines.append(txt_row('Recovery Tier = classification: hot/warm/cold based on RTO requirement'))
    lines.append(txt_row('BIA           = Business Impact Analysis; drives RPO/RTO targets per system'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-ire-cleanroom',
    'docs/backup/ire/clean-room/index.md',
    'IRE Clean Room — isolated ESXi + vCenter + workstations for validated recovery',
)
def _dr_ire_cleanroom():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'IRE Clean Room'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'IRE Clean Room — isolated ESXi + vCenter + workstations for validated recovery')))
    lines.append(R(bMid(3, 99, 'See product-specific sub-sections for detailed procedures')))
    lines.append(R(bMid(3, 99, 'DR success depends on: documented runbooks · tested failover · validated RTO')))
    lines.append(R(bMid(3, 99, 'Minimum DR posture: defined RPO/RTO · tested backups · known escalation path')))
    lines.append(R(bMid(3, 99, 'Test DR procedures quarterly; document results; update runbooks after each test')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Production site · DR site · Replication link · Management network · Vault network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPO           = Recovery Point Objective; max acceptable data loss window'))
    lines.append(txt_row('RTO           = Recovery Time Objective; max acceptable downtime before restore'))
    lines.append(txt_row('Failover      = activating the DR site; redirecting hosts to replica resources'))
    lines.append(txt_row('Failback      = returning operations to production site after DR resolved'))
    lines.append(txt_row('Runbook       = step-by-step documented procedure for a specific DR scenario'))
    lines.append(txt_row('IRE           = Isolated Recovery Environment; air-gapped clean-room for recovery'))
    lines.append(txt_row('Clean Room    = isolated vCenter + workstations for cyber recovery validation'))
    lines.append(txt_row('Air Gap       = network isolation preventing attacker lateral movement to vault'))
    lines.append(txt_row('DR Test       = planned failover test; validates RTO without real disaster'))
    lines.append(txt_row('Replication   = continuous or periodic data copy to secondary site or vault'))
    lines.append(txt_row('Recovery Tier = classification: hot/warm/cold based on RTO requirement'))
    lines.append(txt_row('BIA           = Business Impact Analysis; drives RPO/RTO targets per system'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-ire-isolation',
    'docs/backup/ire/isolation/index.md',
    'IRE Network Isolation — air-gap switch config, VLAN separation, no production routes',
)
def _dr_ire_isolation():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'IRE Network Isolation'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'IRE Network Isolation — air-gap switch config, VLAN separation, no production routes')))
    lines.append(R(bMid(3, 99, 'See product-specific sub-sections for detailed procedures')))
    lines.append(R(bMid(3, 99, 'DR success depends on: documented runbooks · tested failover · validated RTO')))
    lines.append(R(bMid(3, 99, 'Minimum DR posture: defined RPO/RTO · tested backups · known escalation path')))
    lines.append(R(bMid(3, 99, 'Test DR procedures quarterly; document results; update runbooks after each test')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Production site · DR site · Replication link · Management network · Vault network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPO           = Recovery Point Objective; max acceptable data loss window'))
    lines.append(txt_row('RTO           = Recovery Time Objective; max acceptable downtime before restore'))
    lines.append(txt_row('Failover      = activating the DR site; redirecting hosts to replica resources'))
    lines.append(txt_row('Failback      = returning operations to production site after DR resolved'))
    lines.append(txt_row('Runbook       = step-by-step documented procedure for a specific DR scenario'))
    lines.append(txt_row('IRE           = Isolated Recovery Environment; air-gapped clean-room for recovery'))
    lines.append(txt_row('Clean Room    = isolated vCenter + workstations for cyber recovery validation'))
    lines.append(txt_row('Air Gap       = network isolation preventing attacker lateral movement to vault'))
    lines.append(txt_row('DR Test       = planned failover test; validates RTO without real disaster'))
    lines.append(txt_row('Replication   = continuous or periodic data copy to secondary site or vault'))
    lines.append(txt_row('Recovery Tier = classification: hot/warm/cold based on RTO requirement'))
    lines.append(txt_row('BIA           = Business Impact Analysis; drives RPO/RTO targets per system'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-ire-restore',
    'docs/backup/ire/restore/index.md',
    'IRE Restore — step-by-step clean restore from vault to clean-room environment',
)
def _dr_ire_restore():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'IRE Restore'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'IRE Restore — step-by-step clean restore from vault to clean-room environment')))
    lines.append(R(bMid(3, 99, 'See product-specific sub-sections for detailed procedures')))
    lines.append(R(bMid(3, 99, 'DR success depends on: documented runbooks · tested failover · validated RTO')))
    lines.append(R(bMid(3, 99, 'Minimum DR posture: defined RPO/RTO · tested backups · known escalation path')))
    lines.append(R(bMid(3, 99, 'Test DR procedures quarterly; document results; update runbooks after each test')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Production site · DR site · Replication link · Management network · Vault network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPO           = Recovery Point Objective; max acceptable data loss window'))
    lines.append(txt_row('RTO           = Recovery Time Objective; max acceptable downtime before restore'))
    lines.append(txt_row('Failover      = activating the DR site; redirecting hosts to replica resources'))
    lines.append(txt_row('Failback      = returning operations to production site after DR resolved'))
    lines.append(txt_row('Runbook       = step-by-step documented procedure for a specific DR scenario'))
    lines.append(txt_row('IRE           = Isolated Recovery Environment; air-gapped clean-room for recovery'))
    lines.append(txt_row('Clean Room    = isolated vCenter + workstations for cyber recovery validation'))
    lines.append(txt_row('Air Gap       = network isolation preventing attacker lateral movement to vault'))
    lines.append(txt_row('DR Test       = planned failover test; validates RTO without real disaster'))
    lines.append(txt_row('Replication   = continuous or periodic data copy to secondary site or vault'))
    lines.append(txt_row('Recovery Tier = classification: hot/warm/cold based on RTO requirement'))
    lines.append(txt_row('BIA           = Business Impact Analysis; drives RPO/RTO targets per system'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-ire-security',
    'docs/backup/ire/security/index.md',
    'IRE Security — access control, two-person integrity, audit logging in the vault',
)
def _dr_ire_security():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'IRE Security'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'IRE Security — access control, two-person integrity, audit logging in the vault')))
    lines.append(R(bMid(3, 99, 'See product-specific sub-sections for detailed procedures')))
    lines.append(R(bMid(3, 99, 'DR success depends on: documented runbooks · tested failover · validated RTO')))
    lines.append(R(bMid(3, 99, 'Minimum DR posture: defined RPO/RTO · tested backups · known escalation path')))
    lines.append(R(bMid(3, 99, 'Test DR procedures quarterly; document results; update runbooks after each test')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Production site · DR site · Replication link · Management network · Vault network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPO           = Recovery Point Objective; max acceptable data loss window'))
    lines.append(txt_row('RTO           = Recovery Time Objective; max acceptable downtime before restore'))
    lines.append(txt_row('Failover      = activating the DR site; redirecting hosts to replica resources'))
    lines.append(txt_row('Failback      = returning operations to production site after DR resolved'))
    lines.append(txt_row('Runbook       = step-by-step documented procedure for a specific DR scenario'))
    lines.append(txt_row('IRE           = Isolated Recovery Environment; air-gapped clean-room for recovery'))
    lines.append(txt_row('Clean Room    = isolated vCenter + workstations for cyber recovery validation'))
    lines.append(txt_row('Air Gap       = network isolation preventing attacker lateral movement to vault'))
    lines.append(txt_row('DR Test       = planned failover test; validates RTO without real disaster'))
    lines.append(txt_row('Replication   = continuous or periodic data copy to secondary site or vault'))
    lines.append(txt_row('Recovery Tier = classification: hot/warm/cold based on RTO requirement'))
    lines.append(txt_row('BIA           = Business Impact Analysis; drives RPO/RTO targets per system'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-ire-validation',
    'docs/backup/ire/validation/index.md',
    'IRE Validation — application testing, data integrity checks, sign-off before cutback',
)
def _dr_ire_validation():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'IRE Validation'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'IRE Validation — application testing, data integrity checks, sign-off before cutback')))
    lines.append(R(bMid(3, 99, 'See product-specific sub-sections for detailed procedures')))
    lines.append(R(bMid(3, 99, 'DR success depends on: documented runbooks · tested failover · validated RTO')))
    lines.append(R(bMid(3, 99, 'Minimum DR posture: defined RPO/RTO · tested backups · known escalation path')))
    lines.append(R(bMid(3, 99, 'Test DR procedures quarterly; document results; update runbooks after each test')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Production site · DR site · Replication link · Management network · Vault network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPO           = Recovery Point Objective; max acceptable data loss window'))
    lines.append(txt_row('RTO           = Recovery Time Objective; max acceptable downtime before restore'))
    lines.append(txt_row('Failover      = activating the DR site; redirecting hosts to replica resources'))
    lines.append(txt_row('Failback      = returning operations to production site after DR resolved'))
    lines.append(txt_row('Runbook       = step-by-step documented procedure for a specific DR scenario'))
    lines.append(txt_row('IRE           = Isolated Recovery Environment; air-gapped clean-room for recovery'))
    lines.append(txt_row('Clean Room    = isolated vCenter + workstations for cyber recovery validation'))
    lines.append(txt_row('Air Gap       = network isolation preventing attacker lateral movement to vault'))
    lines.append(txt_row('DR Test       = planned failover test; validates RTO without real disaster'))
    lines.append(txt_row('Replication   = continuous or periodic data copy to secondary site or vault'))
    lines.append(txt_row('Recovery Tier = classification: hot/warm/cold based on RTO requirement'))
    lines.append(txt_row('BIA           = Business Impact Analysis; drives RPO/RTO targets per system'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines
