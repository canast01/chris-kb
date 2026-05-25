"""
Disaster Recovery — Backup Tools (Commvault, NetBackup, RASR) diagram functions.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)

# ── COMMVAULT ─────────────────────────────────────────────────────────────────

@kb_diagram(
    'dr-commvault',
    'docs/disaster-recovery/commvault/index.md',
    'Commvault — Enterprise backup and data management platform overview',
)
def dr_commvault():
    """Commvault Platform Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    LL, LR = 3, 50;  LMID = (LL + LR) // 2
    RL2, RR2 = 53, 99; RMID = (RL2 + RR2) // 2
    MID = (FL + FR) // 2
    D1, D2, D3 = 27, 51, 75

    lines = []
    lines.append(title_border(W2, 'Commvault — Enterprise Backup and Data Management'))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Commvault Platform')))
    lines.append(R(bMid(FL, FR, 'Enterprise-grade backup, recovery, archiving, and compliance for hybrid environments')))
    lines.append(R(bMid(FL, FR, 'Core components: CommServe (scheduler+DB), MediaAgent (data mover), Clients')))
    lines.append(R(bMid(FL, FR, 'Interfaces: CommCell Console (Java GUI), Command Center (web UI), REST API')))
    lines.append(R(bMid(FL, FR, 'Deployment: on-premises, cloud (Azure/AWS/GCP), or Commvault Cloud SaaS')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('  Platform decomposes into control plane (CommServe), data plane (MediaAgents), and sources (Clients)'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LL, LR), bTop(RL2, RR2))))
    lines.append(R(merge(bMid(LL, LR, 'CommServe Server'), bMid(RL2, RR2, 'MediaAgent'))))
    lines.append(R(merge(bMid(LL, LR, 'Central scheduler and catalog database'), bMid(RL2, RR2, 'Data movement and deduplication engine'))))
    lines.append(R(merge(bMid(LL, LR, 'SQL Server backend for CommCell DB'), bMid(RL2, RR2, 'DDB (Deduplication Database) on local disk'))))
    lines.append(R(merge(bMid(LL, LR, 'Manages jobs, alerts, and policies'), bMid(RL2, RR2, 'Writes to disk libraries, tape, or cloud'))))
    lines.append(R(merge(bMid(LL, LR, 'Port 8400 (client comms), 8401 (GUI)'), bMid(RL2, RR2, 'Port 8403 (data tunnel), NDMP 10000'))))
    lines.append(R(merge(bMid(LL, LR, 'Active/passive HA with DR CommServe'), bMid(RL2, RR2, 'Scale-out: multiple MAs per CommCell'))))
    lines.append(R(merge(bBot(LL, LR), bBot(RL2, RR2))))

    lines.append(txt_row())
    lines.append(txt_row('  CommServe orchestrates; MediaAgents move data; Clients are the backup sources'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Clients', 'Storage', 'Automation', 'Reporting'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['File · VM · DB · App', 'Disk · Tape · Cloud', 'CLI · REST API', 'Command Center'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['iDA agents installed', 'Storage policies', 'qoperation / qlist', 'Dashboards & SLA'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Exchange · Oracle · SAP', 'WORM / compliance', 'Workflows & alerts', 'Audit & compliance'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Subclients per source', 'Dedup + compression', 'Ansible integration', 'Chargeback reports'])))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('CommServe: 2-socket rack server · 32+ GB RAM · SQL Server storage on SSD RAID-10'))
    lines.append(txt_row('MediaAgent: high-throughput NIC (10/25 GbE) · FC HBA for tape · fast local DDB SSD'))
    lines.append(txt_row('Network: dedicated backup VLAN · 10 GbE client-to-MA links · out-of-band iDRAC/iLO'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CommServe      = Central control server; holds CommCell DB (SQL Server) and job scheduler'))
    lines.append(txt_row('MediaAgent     = Data movement engine; reads from clients, writes to storage targets'))
    lines.append(txt_row('CommCell       = The entire Commvault deployment: CS + all MAs + all Clients'))
    lines.append(txt_row('iDA            = Intelligent Data Agent installed on each client to protect workloads'))
    lines.append(txt_row('Subclient      = Logical grouping of data within a client (defines what to back up)'))
    lines.append(txt_row('Storage Policy = Rules binding subclients to storage libraries (copies, retention, dedup)'))
    lines.append(txt_row('DDB            = Deduplication Database; stores fingerprints for block-level dedup'))
    lines.append(txt_row('IntelliSnap    = Hardware snapshot integration (SAN/NAS arrays) for near-zero-RPO'))
    lines.append(txt_row('CSDB           = CommServe Database; SQL Server instance holding CommCell metadata'))
    lines.append(txt_row('Command Center = Modern web UI replacing legacy CommCell Console (port 443)'))
    lines.append(txt_row('qoperation     = CLI tool for submitting backup/restore/admin operations from shell'))
    lines.append(txt_row('CommCell DR    = Disaster recovery copy of the CommServe for failover continuity'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-commvault-architecture',
    'docs/disaster-recovery/commvault/architecture/index.md',
    'Commvault Architecture — Component topology and data flows',
)
def dr_commvault_architecture():
    """Commvault Architecture Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    LL, LR = 3, 50;  LMID = (LL + LR) // 2
    RL2, RR2 = 53, 99; RMID = (RL2 + RR2) // 2
    MID = (FL + FR) // 2
    D1, D2 = 36, 66

    lines = []
    lines.append(title_border(W2, 'Commvault Architecture — Component Topology'))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'CommCell Architecture')))
    lines.append(R(bMid(FL, FR, 'Three-tier: CommServe (control) → MediaAgent (data plane) → Client (source)')))
    lines.append(R(bMid(FL, FR, 'All communications encrypted TLS 1.2+; certificate-based mutual auth')))
    lines.append(R(bMid(FL, FR, 'CommCell ID uniquely identifies the deployment; required for cross-CommCell ops')))
    lines.append(R(bMid(FL, FR, 'Firewall tunnels: clients connect outbound to CommServe 8400 / MA 8403')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('  Control plane (CS) and data plane (MA) are separated for independent scaling'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LL, LR), bTop(RL2, RR2))))
    lines.append(R(merge(bMid(LL, LR, 'Control Plane (CommServe)'), bMid(RL2, RR2, 'Data Plane (MediaAgents)'))))
    lines.append(R(merge(bMid(LL, LR, 'SQL Server CommCell DB (CSDB)'), bMid(RL2, RR2, 'Deduplication Database (DDB)'))))
    lines.append(R(merge(bMid(LL, LR, 'Job Manager: schedule/queue/retry'), bMid(RL2, RR2, 'Chunk-based data pipeline'))))
    lines.append(R(merge(bMid(LL, LR, 'Event Manager: alerts and SNMP'), bMid(RL2, RR2, 'Compression + encryption at MA'))))
    lines.append(R(merge(bMid(LL, LR, 'CommServe Cache: DR metadata'), bMid(RL2, RR2, 'Mount paths: disk/tape/cloud targets'))))
    lines.append(R(merge(bMid(LL, LR, 'HA: active/passive CS failover'), bMid(RL2, RR2, 'MA groups: load-balance across MAs'))))
    lines.append(R(merge(bBot(LL, LR), bBot(RL2, RR2))))

    lines.append(txt_row())
    lines.append(txt_row('  Data flows from Client iDA → MediaAgent → Storage Library (bypassing CommServe)'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Data Flow: Backup Job')))
    lines.append(R(bMid(FL, FR, '1. CS Job Manager fires job → sends instructions to Client iDA and MediaAgent')))
    lines.append(R(bMid(FL, FR, '2. Client iDA reads source data (VSS snapshot, DB quiesce, or live read)')))
    lines.append(R(bMid(FL, FR, '3. Data stream transferred Client → MA over TCP (port 8403 tunnel)')))
    lines.append(R(bMid(FL, FR, '4. MA deduplicates (DDB lookup), compresses, encrypts, writes to library')))
    lines.append(R(bMid(FL, FR, '5. MA reports chunk metadata to CS; CSDB records job completion')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('CommServe: 2U rack server · 32-64 GB RAM · SQL Server on NVMe RAID-10 · 10 GbE NIC'))
    lines.append(txt_row('MediaAgent: 2U server · 16-32 GB RAM · FC HBA 8/16 Gb for tape · 10/25 GbE NIC'))
    lines.append(txt_row('Disk Library: NAS/SAN target · FC or iSCSI LUNs · WORM-capable for compliance'))
    lines.append(txt_row('Tape Library: FC-attached autoloader or enterprise tape library (LTO-8/9)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CommCell DB    = SQL Server database holding all job history, policies, and metadata'))
    lines.append(txt_row('Job Manager    = CommServe service that schedules, launches, and monitors backup jobs'))
    lines.append(txt_row('iDA            = Intelligent Data Agent; client-side component that reads/writes data'))
    lines.append(txt_row('VSS            = Volume Shadow Copy Service; Windows quiesce mechanism used by iDA'))
    lines.append(txt_row('Chunk          = Fixed-size data block written to library; unit of dedup and tracking'))
    lines.append(txt_row('Silo           = Isolated MA group for multi-tenant or compliance storage separation'))
    lines.append(txt_row('MA Group       = Named set of MediaAgents used for load balancing backup streams'))
    lines.append(txt_row('Firewall Proxy = CV Tunnel Service enabling outbound-only client connectivity'))
    lines.append(txt_row('CommCell DR    = Warm standby CommServe; CSDB replicated via SQL log shipping'))
    lines.append(txt_row('CSDB Backup    = Automated backup of CommServe DB; critical for disaster recovery'))
    lines.append(txt_row('Library        = Logical storage target: disk path, tape drive, or cloud container'))
    lines.append(txt_row('Retention      = Policy defining how many days/cycles backup data is kept on each copy'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-commvault-arch-how-it-works',
    'docs/disaster-recovery/commvault/architecture/how-it-works/index.md',
    'Commvault How It Works — Backup job lifecycle and data pipeline',
)
def dr_commvault_arch_how_it_works():
    """Commvault How It Works — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2
    LL, LR = 3, 50;  LMID = (LL + LR) // 2
    RL2, RR2 = 53, 99; RMID = (RL2 + RR2) // 2

    lines = []
    lines.append(title_border(W2, 'Commvault — How It Works: Job Lifecycle'))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Job Trigger')))
    lines.append(R(bMid(FL, FR, 'Backup initiated by schedule (storage policy window) or on-demand from GUI/CLI')))
    lines.append(R(bMid(FL, FR, 'CommServe Job Manager evaluates resource availability (MA, bandwidth)')))
    lines.append(R(bMid(FL, FR, 'Priority queue: queued if resource slots full; max concurrent jobs configurable')))
    lines.append(R(bMid(FL, FR, 'Subclient pre-post scripts execute before/after data collection phase')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('  Step 1: CommServe assigns MediaAgent and dispatches job control packets to client iDA'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Data Collection (Client iDA)')))
    lines.append(R(bMid(FL, FR, 'File iDA: changed-block tracking (CBT) via journal or full scan on first run')))
    lines.append(R(bMid(FL, FR, 'VM iDA: VMware CBT API or Hyper-V RCT for incremental VM backup')))
    lines.append(R(bMid(FL, FR, 'DB iDA: Oracle RMAN / SQL VDI / SAP BR*Tools integration for consistent backup')))
    lines.append(R(bMid(FL, FR, 'IntelliSnap: array-level snapshot via storage array API before data transfer')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('  Step 2: iDA streams changed data to assigned MediaAgent over TCP 8403 data tunnel'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Data Pipeline (MediaAgent)')))
    lines.append(R(bMid(FL, FR, 'Deduplication: SHA-256 fingerprint per 64-128 KB block checked against DDB')))
    lines.append(R(bMid(FL, FR, 'Compression: LZ4 or gzip applied to unique blocks before write')))
    lines.append(R(bMid(FL, FR, 'Encryption: AES-256 with key managed by CommServe Key Management')))
    lines.append(R(bMid(FL, FR, 'Chunks written to library (disk path, tape, or cloud object store)')))
    lines.append(R(bMid(FL, FR, 'Chunk metadata (size, offset, dedup refs) sent back to CommServe CSDB')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('  Step 3: MA writes data to library; CommServe records metadata for catalog/restore'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LL, LR), bTop(RL2, RR2))))
    lines.append(R(merge(bMid(LL, LR, 'Auxiliary Copy (Replication)'), bMid(RL2, RR2, 'Restore Flow'))))
    lines.append(R(merge(bMid(LL, LR, 'Aux copy job replicates primary'), bMid(RL2, RR2, 'User browses CommCell catalog'))))
    lines.append(R(merge(bMid(LL, LR, 'copy to secondary (tape/cloud)'), bMid(RL2, RR2, 'CS locates chunk locations in CSDB'))))
    lines.append(R(merge(bMid(LL, LR, 'MA-to-MA direct transfer (no CS)'), bMid(RL2, RR2, 'MA reads chunks from library'))))
    lines.append(R(merge(bMid(LL, LR, 'Schedules: continuous or weekly'), bMid(RL2, RR2, 'Data decompressed/decrypted in MA'))))
    lines.append(R(merge(bMid(LL, LR, 'Cloud: S3 / Azure Blob / GCS'), bMid(RL2, RR2, 'Streams back to client iDA'))))
    lines.append(R(merge(bBot(LL, LR), bBot(RL2, RR2))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Data tunnel: client NIC → switch → backup VLAN → MA NIC (10/25 GbE recommended)'))
    lines.append(txt_row('Disk library: NAS share (NFS/CIFS) or SAN LUN formatted with NTFS/ext4'))
    lines.append(txt_row('Tape library: FC-attached via HBA; media management through CommServe tape manager'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CBT            = Changed Block Tracking; OS/hypervisor mechanism to identify modified blocks'))
    lines.append(txt_row('RCT            = Resilient Change Tracking; Hyper-V equivalent of VMware CBT'))
    lines.append(txt_row('DDB            = Deduplication Database; stores block fingerprints for dedup lookup'))
    lines.append(txt_row('IntelliSnap    = Pre-backup hardware snapshot at array level for application consistency'))
    lines.append(txt_row('Chunk          = Variable-size data segment (64-128 KB) written as unit to library'))
    lines.append(txt_row('Aux Copy       = Secondary replication job moving primary copy to another destination'))
    lines.append(txt_row('RMAN           = Oracle Recovery Manager; used by Oracle iDA for consistent DB backup'))
    lines.append(txt_row('VDI            = SQL Server Virtual Device Interface; used by SQL iDA for hot backups'))
    lines.append(txt_row('Subclient      = Named subset of client data with its own schedule and storage policy'))
    lines.append(txt_row('Synthetic Full = Full backup built from incremental chains on MA (no client re-read)'))
    lines.append(txt_row('Job Queue      = CommServe priority queue; throttles concurrent jobs per resource'))
    lines.append(txt_row('Catalog        = CommCell browse index enabling file-level restore from any backup'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-commvault-arch-design',
    'docs/disaster-recovery/commvault/architecture/design-standards/index.md',
    'Commvault Design Standards — Sizing, topology, and best practices',
)
def dr_commvault_arch_design():
    """Commvault Design Standards — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2
    LL, LR = 3, 50
    RL2, RR2 = 53, 99
    D1, D2, D3 = 27, 51, 75

    lines = []
    lines.append(title_border(W2, 'Commvault Design Standards — Sizing and Topology'))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Design Principles')))
    lines.append(R(bMid(FL, FR, 'Separate CommServe and MediaAgent roles onto dedicated servers')))
    lines.append(R(bMid(FL, FR, 'Place MediaAgents close to data sources (same site/rack) to reduce WAN traffic')))
    lines.append(R(bMid(FL, FR, 'Size DDB on fast local NVMe: 1 GB DDB per 1 TB source data (post-dedup ratio)')))
    lines.append(R(bMid(FL, FR, 'Minimum 2 MA per site for redundancy; use MA groups for automatic failover')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('  Component sizing drives performance; under-sized MA is the most common bottleneck'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LL, LR), bTop(RL2, RR2))))
    lines.append(R(merge(bMid(LL, LR, 'CommServe Sizing'), bMid(RL2, RR2, 'MediaAgent Sizing'))))
    lines.append(R(merge(bMid(LL, LR, 'CPU: 8-16 vCPU (SQL-heavy)'), bMid(RL2, RR2, 'CPU: 16-32 vCPU for throughput'))))
    lines.append(R(merge(bMid(LL, LR, 'RAM: 32-64 GB for large CommCells'), bMid(RL2, RR2, 'RAM: 16-32 GB + DDB cache'))))
    lines.append(R(merge(bMid(LL, LR, 'SQL: NVMe RAID-10 for CSDB'), bMid(RL2, RR2, 'DDB: NVMe SSD, separate from OS'))))
    lines.append(R(merge(bMid(LL, LR, 'NIC: 10 GbE for GUI/CLI traffic'), bMid(RL2, RR2, 'NIC: 25 GbE for data streams'))))
    lines.append(R(merge(bMid(LL, LR, 'OS: Windows Server 2019/2022'), bMid(RL2, RR2, 'OS: Windows or Linux (RHEL)'))))
    lines.append(R(merge(bBot(LL, LR), bBot(RL2, RR2))))

    lines.append(txt_row())
    lines.append(txt_row('  Storage policy design directly impacts restore time and dedup efficiency'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Storage Design', 'Retention', 'Network', 'HA / DR'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Primary: fast disk', 'Daily: 30 days', 'Backup VLAN', 'DR CommServe'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Secondary: tape/cloud', 'Weekly: 12 weeks', '10/25 GbE NIC', 'SQL log shipping'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Dedup ratio 5:1-20:1', 'Monthly: 12 months', 'QoS throttling', 'CommCell DR site'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['WORM for compliance', 'Yearly archive', 'Firewall proxy', 'RPO < 1 hour'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Cloud tier: S3/Blob', 'Legal hold caps', 'Bandwidth limits', 'RTO < 4 hours'])))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('CommServe: physical server preferred; avoid shared VMs for production CommCells'))
    lines.append(txt_row('DDB drives: enterprise NVMe (Samsung PM9A3 / Intel P4510); avoid SAS/SATA for DDB'))
    lines.append(txt_row('Backup network: dedicated 10/25 GbE switch; separate from production VLAN'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CommCell DR    = Passive CommServe replica at secondary site for CS failover'))
    lines.append(txt_row('DDB Resync     = Process to rebuild DDB fingerprint index from library chunks'))
    lines.append(txt_row('Storage Policy = Container linking subclients to libraries with retention and copy rules'))
    lines.append(txt_row('Dedup Ratio    = Ratio of source data size to post-dedup storage consumed'))
    lines.append(txt_row('MA Group       = Named pool of MediaAgents for load balancing and failover'))
    lines.append(txt_row('Primary Copy   = First storage policy copy; used for fast restores'))
    lines.append(txt_row('Secondary Copy = Aux-copy destination (tape or cloud) for long-term retention'))
    lines.append(txt_row('WORM           = Write Once Read Many; immutable storage for compliance locks'))
    lines.append(txt_row('RPO            = Recovery Point Objective; max acceptable data loss (time since last backup)'))
    lines.append(txt_row('RTO            = Recovery Time Objective; max acceptable time to complete restore'))
    lines.append(txt_row('Bandwidth Cap  = Throttle on MA data transfer rate to protect production network'))
    lines.append(txt_row('SQL Log Ship   = SQL Server log shipping replicating CSDB to DR CommServe'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-commvault-arch-integrations',
    'docs/disaster-recovery/commvault/architecture/integrations/index.md',
    'Commvault Integrations — Supported platforms, arrays, and cloud connectors',
)
def dr_commvault_arch_integrations():
    """Commvault Architecture Integrations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2
    D1, D2, D3 = 27, 51, 75
    LL, LR = 3, 50
    RL2, RR2 = 53, 99

    lines = []
    lines.append(title_border(W2, 'Commvault Integrations — Platforms, Arrays, and Cloud'))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Integration Scope')))
    lines.append(R(bMid(FL, FR, 'Commvault integrates with hypervisors, databases, storage arrays, and cloud providers')))
    lines.append(R(bMid(FL, FR, 'IntelliSnap: native array API (REST/SMI-S) for hardware-accelerated snapshots')))
    lines.append(R(bMid(FL, FR, 'Application iDAs provide quiesce and consistent backup for DBs and messaging')))
    lines.append(R(bMid(FL, FR, 'Cloud: S3-compatible, Azure Blob, GCS as secondary copy or primary target')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('  Each integration has a dedicated iDA or connector; licensing is per data source type'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Hypervisors', 'Databases', 'Storage Arrays', 'Cloud & SaaS'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['VMware vSphere 7/8', 'Oracle DB (RMAN)', 'Dell PowerStore', 'AWS S3 / Glacier'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Hyper-V 2019/2022', 'SQL Server (VDI)', 'Dell PowerMax', 'Azure Blob / ADLS'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Nutanix AHV', 'SAP HANA / BR*Tools', 'NetApp ONTAP', 'Google Cloud GCS'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['KVM (libvirt)', 'Exchange / M365', 'Pure Storage', 'Commvault Cloud'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['AWS EC2 / Azure VM', 'PostgreSQL / MySQL', 'HPE Primera/3PAR', 'Salesforce backup'])))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('  IntelliSnap offloads snapshot to array; backup job copies snapshot to MA with minimal host I/O'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LL, LR), bTop(RL2, RR2))))
    lines.append(R(merge(bMid(LL, LR, 'IntelliSnap Flow'), bMid(RL2, RR2, 'Cloud Integration'))))
    lines.append(R(merge(bMid(LL, LR, '1. CS triggers snap via array API'), bMid(RL2, RR2, 'Cloud library: object container'))))
    lines.append(R(merge(bMid(LL, LR, '2. Array creates crash-consistent snap'), bMid(RL2, RR2, 'MA authenticates with IAM/SAS token'))))
    lines.append(R(merge(bMid(LL, LR, '3. MA mounts snap for data read'), bMid(RL2, RR2, 'Multipart upload for large chunks'))))
    lines.append(R(merge(bMid(LL, LR, '4. Data streamed to disk library'), bMid(RL2, RR2, 'Lifecycle: move old copies to Glacier'))))
    lines.append(R(merge(bMid(LL, LR, '5. Snap unmounted; retained per policy'), bMid(RL2, RR2, 'WORM via S3 Object Lock'))))
    lines.append(R(merge(bBot(LL, LR), bBot(RL2, RR2))))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('IntelliSnap: MA needs FC/iSCSI access to array snap LUNs for mount; HBA/iSCSI initiator'))
    lines.append(txt_row('Array API: dedicated management NIC or VLAN for REST/SMI-S calls from CommServe'))
    lines.append(txt_row('Cloud: outbound HTTPS 443 from MA to cloud endpoints; proxy support available'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('IntelliSnap    = Commvault snap management using native storage array APIs'))
    lines.append(txt_row('SMI-S          = Storage Management Initiative Specification; standard array management API'))
    lines.append(txt_row('VDI            = SQL Server Virtual Device Interface for hot online backup'))
    lines.append(txt_row('RMAN           = Oracle Recovery Manager; Commvault Oracle iDA wraps RMAN commands'))
    lines.append(txt_row('BR*Tools       = SAP backup tools; Commvault integrates as backint backend'))
    lines.append(txt_row('ADLS           = Azure Data Lake Storage Gen2; supported as cloud library target'))
    lines.append(txt_row('Object Lock    = S3 immutability feature used for WORM compliance copies'))
    lines.append(txt_row('IAM Role       = AWS identity for MA EC2 instance; used instead of static credentials'))
    lines.append(txt_row('SAS Token      = Azure shared access signature; time-limited credential for Blob access'))
    lines.append(txt_row('Cloud Library  = Commvault logical library pointing to object store bucket/container'))
    lines.append(txt_row('Backint        = SAP backup API standard; Commvault implements as SAP HANA target'))
    lines.append(txt_row('RCT            = Hyper-V Resilient Change Tracking; incremental VM backup mechanism'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── COMMVAULT OPERATIONS ──────────────────────────────────────────────────────

@kb_diagram(
    'dr-commvault-operations',
    'docs/disaster-recovery/commvault/operations/index.md',
    'Commvault Operations — Day-to-day operational tasks overview',
)
def dr_commvault_operations():
    """Commvault Operations Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2
    D1, D2, D3 = 27, 51, 75

    lines = []
    lines.append(title_border(W2, 'Commvault Operations — Day-to-Day Tasks'))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Commvault Operations Scope')))
    lines.append(R(bMid(FL, FR, 'Covers: backup/restore, health checks, CLI, install/upgrade, scripts, procedures')))
    lines.append(R(bMid(FL, FR, 'Primary interfaces: Command Center (web), CommCell Console (Java), qoperation CLI')))
    lines.append(R(bMid(FL, FR, 'Daily: monitor job activity, check alerts, verify SLA compliance, review failures')))
    lines.append(R(bMid(FL, FR, 'Weekly: run reports, validate aux copies, check DDB health, review storage usage')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('  Operational domains map to separate runbooks: backup-restore, health, install, procedures'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Backup/Restore', 'Health Checks', 'Install/Upgrade', 'Scripts/CLI'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Job monitoring', 'CV_DIAG logs', 'SP download', 'qoperation run'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['On-demand backup', 'DDB validation', 'Upgrade wizard', 'qlist jobs'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Granular restore', 'MA connectivity', 'Pre-req checker', 'qmodify policy'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['SLA report', 'Alerts review', 'Rollback plan', 'REST API calls'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Aux copy status', 'Disk space check', 'Post-upgrade test', 'Python SDK'])))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Operations workstation needs Java JRE (CommCell Console) or browser (Command Center)'))
    lines.append(txt_row('CLI qoperation runs on CommServe or any Windows/Linux host with CV client installed'))
    lines.append(txt_row('Network: ops console needs TCP 8401 to CommServe, 443 for Command Center'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('qoperation     = Commvault CLI binary on CommServe for submitting jobs and changes'))
    lines.append(txt_row('qlist          = Commvault CLI for listing jobs, clients, policies, and library status'))
    lines.append(txt_row('qmodify        = Commvault CLI for modifying subclients, schedules, and policies'))
    lines.append(txt_row('SLA            = Service Level Agreement; Commvault tracks backup success rate vs target'))
    lines.append(txt_row('Job Activity   = CommCell Console/Command Center view of all running and queued jobs'))
    lines.append(txt_row('Alerts         = Configured thresholds triggering email/SNMP on job failures or disk low'))
    lines.append(txt_row('DDB Validation = Integrity scan of dedup database to detect/repair corruption'))
    lines.append(txt_row('Aux Copy       = Secondary copy replication job; must be monitored for lag/failures'))
    lines.append(txt_row('SP             = Service Pack; Commvault patch bundle (e.g. SP32, SP33)'))
    lines.append(txt_row('CV_DIAG        = Commvault diagnostic log collector; gathers logs from all components'))
    lines.append(txt_row('REST API       = Commvault REST API (v4) for programmatic management and automation'))
    lines.append(txt_row('Command Center = Modern web-based management UI on CommServe port 443'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-commvault-ops-backup',
    'docs/disaster-recovery/commvault/operations/backup-restore/index.md',
    'Commvault Backup and Restore — Job types, procedures, and restore options',
)
def dr_commvault_ops_backup():
    """Commvault Backup and Restore Operations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2
    LL, LR = 3, 50
    RL2, RR2 = 53, 99

    lines = []
    lines.append(title_border(W2, 'Commvault Backup and Restore — Procedures'))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LL, LR), bTop(RL2, RR2))))
    lines.append(R(merge(bMid(LL, LR, 'Backup Job Types'), bMid(RL2, RR2, 'Restore Types'))))
    lines.append(R(merge(bMid(LL, LR, 'Full: all data in subclient scope'), bMid(RL2, RR2, 'In-place: restore to original path'))))
    lines.append(R(merge(bMid(LL, LR, 'Incremental: changed since last'), bMid(RL2, RR2, 'Out-of-place: alternate path/client'))))
    lines.append(R(merge(bMid(LL, LR, 'Differential: changed since Full'), bMid(RL2, RR2, 'Cross-client: different target host'))))
    lines.append(R(merge(bMid(LL, LR, 'Synthetic Full: built on MA from inc'), bMid(RL2, RR2, 'Granular: item-level from VM/Exchange'))))
    lines.append(R(merge(bMid(LL, LR, 'Snap backup: array snapshot + backup'), bMid(RL2, RR2, 'Live Browse: mount backup for reads'))))
    lines.append(R(merge(bBot(LL, LR), bBot(RL2, RR2))))

    lines.append(txt_row())
    lines.append(txt_row('  Full backup cycle: Full (weekly) → Incrementals (daily) → Synthetic Full (next week)'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'On-Demand Backup (Command Center)')))
    lines.append(R(bMid(FL, FR, '1. Navigate: Protect → Virtualization (or File Servers / Databases)')))
    lines.append(R(bMid(FL, FR, '2. Select subclient → right-click → Backup Now → choose Full/Incremental')))
    lines.append(R(bMid(FL, FR, '3. Monitor job in Job Activity pane; check logs if status ≠ Completed')))
    lines.append(R(bMid(FL, FR, '4. Verify protected size and dedup savings in job summary report')))
    lines.append(R(bMid(FL, FR, '5. CLI: qoperation execschedule -clientName HOST -subclientName default')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('  Restore: right-click subclient → Browse and Restore → select files → Restore'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Restore Verification')))
    lines.append(R(bMid(FL, FR, 'After restore: verify file checksums, check application startup, validate data')))
    lines.append(R(bMid(FL, FR, 'VM restore: power on, run OS checks, verify application services running')))
    lines.append(R(bMid(FL, FR, 'DB restore: validate row counts, run DBCC CHECKDB (SQL) or RMAN validate')))
    lines.append(R(bMid(FL, FR, 'Scheduled restore tests: monthly verified restore to isolated environment')))
    lines.append(R(bMid(FL, FR, 'SLA reporting: track %backup success; target ≥ 99% weekly completion rate')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Restore target must have iDA agent; network path from MA to target must be open'))
    lines.append(txt_row('VM restores: target datastore must have sufficient free space (source VM size + 20%)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Synthetic Full = Full backup constructed on MA from existing incrementals; no client I/O'))
    lines.append(txt_row('Snap Backup    = IntelliSnap array-level snapshot followed by backup-from-snap to library'))
    lines.append(txt_row('Live Browse    = Mount backup copy as NFS/CIFS share for direct file browsing'))
    lines.append(txt_row('Granular Recov = Item-level restore (e.g., single email, SQL row, VM disk file)'))
    lines.append(txt_row('DBCC CHECKDB   = SQL Server command to verify database consistency after restore'))
    lines.append(txt_row('Browse Window  = Time range visible in CommCell browse based on retention settings'))
    lines.append(txt_row('Cross-client   = Restore to a different machine than the original backup source'))
    lines.append(txt_row('Job Activity   = Real-time view of all running, queued, and recently completed jobs'))
    lines.append(txt_row('Protected Size = Total data covered by backup policy on a given client/subclient'))
    lines.append(txt_row('qoperation     = CLI to trigger on-demand backup: execschedule or backup subcommand'))
    lines.append(txt_row('SLA Report     = Commvault report showing backup success rate vs configured targets'))
    lines.append(txt_row('Retention Copy = Backup copy kept for extended period (monthly/yearly) on tape/cloud'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-commvault-ops-cli',
    'docs/disaster-recovery/commvault/operations/cli-reference/index.md',
    'Commvault CLI Reference — qoperation, qlist, qmodify, and REST API',
)
def dr_commvault_ops_cli():
    """Commvault CLI Reference — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2
    LL, LR = 3, 50
    RL2, RR2 = 53, 99

    lines = []
    lines.append(title_border(W2, 'Commvault CLI Reference — qoperation, qlist, qmodify'))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LL, LR), bTop(RL2, RR2))))
    lines.append(R(merge(bMid(LL, LR, 'qoperation — Job Control'), bMid(RL2, RR2, 'qlist — Read/Query'))))
    lines.append(R(merge(bMid(LL, LR, 'execschedule: run backup now'), bMid(RL2, RR2, 'qlist jobs: show all active jobs'))))
    lines.append(R(merge(bMid(LL, LR, 'restore: initiate restore job'), bMid(RL2, RR2, 'qlist client: list all clients'))))
    lines.append(R(merge(bMid(LL, LR, 'auxcopy: trigger aux copy job'), bMid(RL2, RR2, 'qlist subclient: list subclients'))))
    lines.append(R(merge(bMid(LL, LR, 'release: release held media'), bMid(RL2, RR2, 'qlist storage: disk/tape libraries'))))
    lines.append(R(merge(bMid(LL, LR, 'kill: abort a running job'), bMid(RL2, RR2, 'qlist jobdetails: verbose job info'))))
    lines.append(R(merge(bBot(LL, LR), bBot(RL2, RR2))))

    lines.append(txt_row())
    lines.append(txt_row('  qoperation and qlist run on CommServe; add -cs <host> for remote CommServe target'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LL, LR), bTop(RL2, RR2))))
    lines.append(R(merge(bMid(LL, LR, 'qmodify — Configuration Changes'), bMid(RL2, RR2, 'REST API (v4)'))))
    lines.append(R(merge(bMid(LL, LR, 'subclient: update content paths'), bMid(RL2, RR2, 'Base URL: https://CS/webconsole/api'))))
    lines.append(R(merge(bMid(LL, LR, 'schedule: change backup window'), bMid(RL2, RR2, 'Auth: POST /Login → authtoken'))))
    lines.append(R(merge(bMid(LL, LR, 'storagepolicy: edit retention'), bMid(RL2, RR2, 'GET /Client: list all clients'))))
    lines.append(R(merge(bMid(LL, LR, 'client: enable/disable backup'), bMid(RL2, RR2, 'POST /CreateTask: trigger backup'))))
    lines.append(R(merge(bMid(LL, LR, 'mediaagent: enable/disable MA'), bMid(RL2, RR2, 'GET /Job/{id}: poll job status'))))
    lines.append(R(merge(bBot(LL, LR), bBot(RL2, RR2))))

    lines.append(txt_row())
    lines.append(txt_row('  Common qoperation examples:'))
    lines.append(txt_row('    qoperation execschedule -clientName myhost -subclientName default -backuptype full'))
    lines.append(txt_row('    qoperation restore -clientName myhost -subclientName default -fromtime "01/01/2026"'))
    lines.append(txt_row('    qlist jobs -jobtype backup -status running'))
    lines.append(txt_row('    qmodify subclient -clientName myhost -subclientName default -content /data/new'))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('CLI runs on CommServe host; PATH must include CV installation bin directory'))
    lines.append(txt_row('REST API accessible from any host with HTTPS 443 reach to CommServe'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('qoperation     = Command-line tool for submitting Commvault operations from shell/scripts'))
    lines.append(txt_row('qlist          = Read-only query tool for listing CommCell objects and job status'))
    lines.append(txt_row('qmodify        = Configuration change tool for subclients, schedules, and policies'))
    lines.append(txt_row('execschedule   = qoperation subcommand to immediately run a scheduled backup'))
    lines.append(txt_row('authtoken      = Session token returned by REST /Login; included in all API headers'))
    lines.append(txt_row('CreateTask     = REST API endpoint for submitting backup, restore, and aux copy jobs'))
    lines.append(txt_row('-cs flag       = Specifies remote CommServe hostname for cross-CS CLI operations'))
    lines.append(txt_row('backuptype     = full | incremental | differential | synthetic_full'))
    lines.append(txt_row('Job ID         = Integer assigned to each job; used for status polling and log lookups'))
    lines.append(txt_row('auxcopy        = qoperation subcommand to immediately trigger a secondary copy job'))
    lines.append(txt_row('jobdetails     = qlist subcommand returning verbose per-phase timing and error codes'))
    lines.append(txt_row('CV Python SDK  = Commvault.sdk Python package wrapping REST API with OOP interface'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-commvault-ops-health',
    'docs/disaster-recovery/commvault/operations/health-checks/index.md',
    'Commvault Health Checks — Daily and weekly verification procedures',
)
def dr_commvault_ops_health():
    """Commvault Health Checks — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2
    LL, LR = 3, 50
    RL2, RR2 = 53, 99

    lines = []
    lines.append(title_border(W2, 'Commvault Health Checks — Daily and Weekly'))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LL, LR), bTop(RL2, RR2))))
    lines.append(R(merge(bMid(LL, LR, 'Daily Health Checks'), bMid(RL2, RR2, 'Weekly Health Checks'))))
    lines.append(R(merge(bMid(LL, LR, 'Review overnight job failures'), bMid(RL2, RR2, 'Run SLA compliance report'))))
    lines.append(R(merge(bMid(LL, LR, 'Check CommServe services up'), bMid(RL2, RR2, 'Validate aux copy completion'))))
    lines.append(R(merge(bMid(LL, LR, 'Verify disk library free space'), bMid(RL2, RR2, 'Check DDB health and fragmentation'))))
    lines.append(R(merge(bMid(LL, LR, 'Review alert emails for anomalies'), bMid(RL2, RR2, 'Review library capacity trends'))))
    lines.append(R(merge(bMid(LL, LR, 'Check MA status (active/offline)'), bMid(RL2, RR2, 'Verify DR CommServe sync status'))))
    lines.append(R(merge(bBot(LL, LR), bBot(RL2, RR2))))

    lines.append(txt_row())
    lines.append(txt_row('  Health checks use Command Center dashboards, qlist CLI, and CommServe event log'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'CommServe Service Health')))
    lines.append(R(bMid(FL, FR, 'Check Windows services: CommVault Communications (GxCVD), Job Manager (GxJobMgr)')))
    lines.append(R(bMid(FL, FR, 'Check SQL Server: CSDB query response time < 2s; check for blocking queries')))
    lines.append(R(bMid(FL, FR, 'Check CV log directory: disk < 80% full; rotate logs if needed')))
    lines.append(R(bMid(FL, FR, 'Windows Event Log: look for GxJobMgr, MSSQL errors in last 24h')))
    lines.append(R(bMid(FL, FR, 'CommServe DR sync: SQL log shipping lag < 15 min; test failover quarterly')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('  MediaAgent health includes DDB consistency and connectivity from all clients'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'MediaAgent Health')))
    lines.append(R(bMid(FL, FR, 'MA status: all configured MAs should show Ready in CommCell Console')))
    lines.append(R(bMid(FL, FR, 'DDB fragmentation: run DDB Verification job monthly; check for corrupt chunks')))
    lines.append(R(bMid(FL, FR, 'Disk library: free space > 20%; monitor growth trend weekly')))
    lines.append(R(bMid(FL, FR, 'Network throughput: MA backup streams should sustain > 500 MB/s per MA')))
    lines.append(R(bMid(FL, FR, 'MA log: C:\\Program Files\\Commvault\\Log Files\\MediaAgent.log')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Monitor disk library mount points (NFS/CIFS/LUN) for connectivity and free space'))
    lines.append(txt_row('MA server: check CPU/RAM utilization during peak backup windows (target < 80% CPU)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('GxCVD          = CommVault Communications Service; handles all inter-component comms'))
    lines.append(txt_row('GxJobMgr       = CommVault Job Manager service; schedules and monitors all backup jobs'))
    lines.append(txt_row('DDB Verify     = Job that reads all DDB fingerprints and validates against stored chunks'))
    lines.append(txt_row('CSDB           = CommServe Database (SQL Server); holds all CommCell configuration'))
    lines.append(txt_row('MA Ready       = Status indicating MA service is running and library is accessible'))
    lines.append(txt_row('SLA Report     = Compliance report: % subclients with successful backup in SLA window'))
    lines.append(txt_row('Log Shipping   = SQL Server mechanism replicating CSDB transaction logs to DR CommServe'))
    lines.append(txt_row('Aux Copy Lag   = Time between primary backup completion and secondary copy completion'))
    lines.append(txt_row('CV_DIAG        = Commvault diagnostic tool; collects all logs and config for support'))
    lines.append(txt_row('Library Prune  = Aged-out backup chunks removed from disk library per retention policy'))
    lines.append(txt_row('Fragmentation  = DDB fragmentation degrades dedup performance; fixed by DDB defrag job'))
    lines.append(txt_row('CommServe DR   = Passive standby CommServe; kept in sync via SQL log shipping'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-commvault-ops-install',
    'docs/disaster-recovery/commvault/operations/install-upgrade/index.md',
    'Commvault Install and Upgrade — Procedures, service packs, and rollback',
)
def dr_commvault_ops_install():
    """Commvault Install and Upgrade — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2
    LL, LR = 3, 50
    RL2, RR2 = 53, 99

    lines = []
    lines.append(title_border(W2, 'Commvault Install and Upgrade — Procedures'))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LL, LR), bTop(RL2, RR2))))
    lines.append(R(merge(bMid(LL, LR, 'New Installation'), bMid(RL2, RR2, 'Upgrade (Service Pack)'))))
    lines.append(R(merge(bMid(LL, LR, '1. Download CV software from cloud.commvault.com'), bMid(RL2, RR2, '1. Download SP from cloud.commvault.com'))))
    lines.append(R(merge(bMid(LL, LR, '2. Run prerequisite checker tool'), bMid(RL2, RR2, '2. Backup CSDB before upgrade'))))
    lines.append(R(merge(bMid(LL, LR, '3. Install CommServe first (SQL req)'), bMid(RL2, RR2, '3. Upgrade CommServe first'))))
    lines.append(R(merge(bMid(LL, LR, '4. Install MediaAgents next'), bMid(RL2, RR2, '4. Upgrade MediaAgents next'))))
    lines.append(R(merge(bMid(LL, LR, '5. Push client agents from CommServe'), bMid(RL2, RR2, '5. Push agent updates to clients'))))
    lines.append(R(merge(bBot(LL, LR), bBot(RL2, RR2))))

    lines.append(txt_row())
    lines.append(txt_row('  Always upgrade CommServe before MAs and Clients; never skip more than 2 SP versions'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Pre-Upgrade Checklist')))
    lines.append(R(bMid(FL, FR, '[ ] Full CSDB backup completed and verified (SQL backup + CV CommServe DR sync)')))
    lines.append(R(bMid(FL, FR, '[ ] All running jobs quiesced or completed; maintenance window communicated')))
    lines.append(R(bMid(FL, FR, '[ ] Prerequisite checker: .NET version, SQL version, OS patch level, disk space')))
    lines.append(R(bMid(FL, FR, '[ ] Rollback plan documented: restore CSDB SQL backup, reinstall prior SP')))
    lines.append(R(bMid(FL, FR, '[ ] Post-upgrade tests: run backup and restore job on representative subclients')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Upgrade requires CommServe downtime (~30-90 min); plan during off-peak window'))
    lines.append(txt_row('MA upgrade can be pushed silently from CommServe; minimal impact to running jobs'))
    lines.append(txt_row('Client agent upgrades: push from CommCell Console or deploy via software distribution'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Service Pack   = Commvault cumulative patch bundle (SP30, SP31, SP32, SP33...)'))
    lines.append(txt_row('SP Hotfix      = Targeted fix for critical issues between Service Pack releases'))
    lines.append(txt_row('Prereq Checker = Commvault tool validating environment readiness before installation'))
    lines.append(txt_row('Silent Install = MSI-based client push from CommServe with no user interaction'))
    lines.append(txt_row('CSDB Backup    = SQL Server backup of CommCell database; critical upgrade prerequisite'))
    lines.append(txt_row('Rollback       = Restore prior SP by reinstalling from backup media + CSDB SQL restore'))
    lines.append(txt_row('Upgrade Order  = CommServe → MediaAgents → Clients (never reverse this sequence)'))
    lines.append(txt_row('cloud.commvault.com = Commvault download portal for software and service packs'))
    lines.append(txt_row('CommServe Upgrade = Core upgrade updating SQL schema and all CV services simultaneously'))
    lines.append(txt_row('iDA Upgrade    = Client-side agent update; backward compatible with CS one SP behind'))
    lines.append(txt_row('Maintenance Win = Scheduled downtime window communicated to stakeholders for upgrades'))
    lines.append(txt_row('Post-Upgrade   = Mandatory validation: run backup + restore test before returning to prod'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-commvault-ops-procedures',
    'docs/disaster-recovery/commvault/operations/procedures/index.md',
    'Commvault Procedures — Standard operational runbooks',
)
def dr_commvault_ops_procedures():
    """Commvault Operational Procedures — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2
    D1, D2, D3 = 27, 51, 75

    lines = []
    lines.append(title_border(W2, 'Commvault Operational Procedures — Runbooks'))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Procedure Library')))
    lines.append(R(bMid(FL, FR, 'Standard runbooks for recurring Commvault operational tasks')))
    lines.append(R(bMid(FL, FR, 'Each procedure: purpose, prerequisites, steps, validation, rollback')))
    lines.append(R(bMid(FL, FR, 'Change-controlled: procedures require CAB approval for production changes')))
    lines.append(R(bMid(FL, FR, 'Test quarterly in staging CommCell before production execution')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('  Procedures cover storage, client management, DR, compliance, and recovery'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Storage Mgmt', 'Client Mgmt', 'DR / Recovery', 'Compliance'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Add disk library', 'Add new client', 'CS failover test', 'WORM extension'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Extend library LUN', 'Push iDA agent', 'Restore to DR site', 'Audit log export'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Add tape drive', 'Retire client', 'CommCell DR drill', 'Legal hold apply'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['DDB move to new disk', 'Edit storage policy', 'Cloud recovery test', 'SLA report gen'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Library pruning', 'Subclient changes', 'CSDB restore test', 'Retention review'])))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('  CommServe Failover Procedure (abbreviated):'))
    lines.append(txt_row('    1. Verify SQL log shipping is current (< 15 min lag) on DR CommServe'))
    lines.append(txt_row('    2. Stop CommVault services on primary CommServe'))
    lines.append(txt_row('    3. Apply pending SQL logs on DR CommServe; bring CSDB online'))
    lines.append(txt_row('    4. Update DNS A record to point CommServe FQDN to DR server IP'))
    lines.append(txt_row('    5. Start CommVault services on DR CommServe; verify Job Manager starts'))
    lines.append(txt_row('    6. Run test backup on representative client to confirm CommCell operational'))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('CS failover: DR CommServe needs same hostname/IP reachability as primary (DNS/IP change)'))
    lines.append(txt_row('Library access: DR MAs must have mount path access to all disk libraries post-failover'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CAB            = Change Advisory Board; approves production changes to backup infrastructure'))
    lines.append(txt_row('WORM Lock      = Compliance lock preventing deletion of backup data before expiry'))
    lines.append(txt_row('Legal Hold     = Indefinite retention lock applied to data involved in litigation'))
    lines.append(txt_row('CS Failover    = Switching CommCell to DR CommServe after primary failure'))
    lines.append(txt_row('DR Drill       = Periodic test of CommServe failover and restore procedures'))
    lines.append(txt_row('DDB Move       = Migrating DDB from one disk to another without data loss'))
    lines.append(txt_row('Library Pruning = Removing expired backup chunks from disk library to reclaim space'))
    lines.append(txt_row('Retire Client  = Removing client from CommCell; requires data expiry and decommission'))
    lines.append(txt_row('iDA Push       = Installing client agent remotely from CommServe without local access'))
    lines.append(txt_row('Subclient Edit = Modifying content, schedule, or storage policy assignment for a subclient'))
    lines.append(txt_row('SQL Log Ship   = Transaction log replication from primary CSDB to DR CommServe'))
    lines.append(txt_row('Mount Path     = File system path on MediaAgent where disk library chunks are stored'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-commvault-ops-scripts',
    'docs/disaster-recovery/commvault/operations/scripts/index.md',
    'Commvault Scripts — Automation and reporting scripts',
)
def dr_commvault_ops_scripts():
    """Commvault Operations Scripts — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2
    LL, LR = 3, 50
    RL2, RR2 = 53, 99

    lines = []
    lines.append(title_border(W2, 'Commvault Scripts — Automation and Reporting'))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LL, LR), bTop(RL2, RR2))))
    lines.append(R(merge(bMid(LL, LR, 'PowerShell / Bash Scripts'), bMid(RL2, RR2, 'Python (CV SDK)'))))
    lines.append(R(merge(bMid(LL, LR, 'Daily job failure report email'), bMid(RL2, RR2, 'cvpysdk: OOP REST wrapper'))))
    lines.append(R(merge(bMid(LL, LR, 'SLA compliance CSV export'), bMid(RL2, RR2, 'CommCell() → client.backups()'))))
    lines.append(R(merge(bMid(LL, LR, 'Disk library space alert'), bMid(RL2, RR2, 'Trigger backup programmatically'))))
    lines.append(R(merge(bMid(LL, LR, 'MA status health check script'), bMid(RL2, RR2, 'Query job history to DB'))))
    lines.append(R(merge(bMid(LL, LR, 'qlist jobs | parse failures'), bMid(RL2, RR2, 'Automated new client onboard'))))
    lines.append(R(merge(bBot(LL, LR), bBot(RL2, RR2))))

    lines.append(txt_row())
    lines.append(txt_row('  Scripts use qoperation/qlist CLI or REST API; store credentials in vault (not plain text)'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Common Script Examples')))
    lines.append(R(bMid(FL, FR, 'Daily report: qlist jobs -jobtype backup -status failed | mail -s "CV Failures" ops@')))
    lines.append(R(bMid(FL, FR, 'Disk check: qlist storage -type disk | awk \'{if ($5>80) print "WARN:"$1}\'')))
    lines.append(R(bMid(FL, FR, 'New client: qoperation addclient -clientName HOST -username admin -os windows')))
    lines.append(R(bMid(FL, FR, 'Aux copy trigger: qoperation auxcopy -storagepolicy SP_Name -allCopies')))
    lines.append(R(bMid(FL, FR, 'Python SDK: from cvpysdk.commcell import Commcell; cc=Commcell(cs, user, pw)')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Scripts run on CommServe host or jump host with cv CLI in PATH'))
    lines.append(txt_row('Python SDK: pip install cvpysdk; requires Python 3.8+; HTTPS 443 to CommServe'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('cvpysdk        = Commvault Python SDK (pip install cvpysdk); open-source REST wrapper'))
    lines.append(txt_row('Commcell()     = Primary cvpysdk class; authenticates and connects to CommServe'))
    lines.append(txt_row('qlist output   = Tab-separated or CSV output suitable for shell parsing'))
    lines.append(txt_row('Pre-Post Script= Script run before/after subclient backup (app quiesce, notify, etc.)'))
    lines.append(txt_row('Alert Script   = Script triggered by CommServe alert event (job fail, disk low, etc.)'))
    lines.append(txt_row('REST Token     = Session token from POST /Login; used as header for subsequent API calls'))
    lines.append(txt_row('Job History DB = SQL view in CSDB exposing completed job data for custom reporting'))
    lines.append(txt_row('Cron / Task    = OS scheduler (cron on Linux, Task Scheduler on Windows) for reports'))
    lines.append(txt_row('Mail Relay     = SMTP server configured in CommServe for alert email delivery'))
    lines.append(txt_row('Secret Vault   = HashiCorp Vault or CyberArk; store CV admin credentials, not plaintext'))
    lines.append(txt_row('addclient      = qoperation subcommand to register new client in CommCell'))
    lines.append(txt_row('allCopies      = Flag in auxcopy command to replicate all storage policy copies'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── COMMVAULT SECURITY ────────────────────────────────────────────────────────

@kb_diagram(
    'dr-commvault-security',
    'docs/disaster-recovery/commvault/security/index.md',
    'Commvault Security — Access control, auth, encryption, and hardening overview',
)
def dr_commvault_security():
    """Commvault Security Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2
    D1, D2, D3 = 27, 51, 75

    lines = []
    lines.append(title_border(W2, 'Commvault Security — Controls Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Commvault Security Model')))
    lines.append(R(bMid(FL, FR, 'Defence-in-depth: transport encryption, RBAC, MFA, hardening, audit logs')))
    lines.append(R(bMid(FL, FR, 'All component communications use TLS 1.2+ with mutual certificate auth')))
    lines.append(R(bMid(FL, FR, 'RBAC: roles limit access to CommCell objects (clients, policies, libraries)')))
    lines.append(R(bMid(FL, FR, 'Data encryption: AES-256 for backup data at rest and in transit')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('  Four security domains: access control, authentication, encryption, hardening'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Access Control', 'Authentication', 'Encryption', 'Hardening'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['RBAC roles', 'Local + AD auth', 'AES-256 data', 'Minimal install'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['CommCell users', 'MFA (TOTP)', 'TLS 1.2+ comms', 'Host firewall'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['User groups', 'SAML SSO', 'Key management', 'No unneeded svc'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Object security', 'Cert-based auth', 'FIPS 140-2 mode', 'Audit logging'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Least privilege', 'Session timeout', 'Immutable copies', 'SIEM forwarding'])))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('CommServe hardened: minimal OS install, host firewall (only ports 8400/8401/443 open)'))
    lines.append(txt_row('Certificate PKI: internal CA issues CommCell certs; rotate annually'))
    lines.append(txt_row('Network: CommServe and MAs on dedicated backup VLAN, not directly reachable from clients'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RBAC           = Role-Based Access Control; CommCell roles define allowed operations'))
    lines.append(txt_row('CommCell User  = Local user account in CommServe database (not OS/AD user)'))
    lines.append(txt_row('AD Integration = CommServe can authenticate users against Active Directory LDAP'))
    lines.append(txt_row('SAML SSO       = SAML 2.0 federation; allows IdP-based login to Command Center'))
    lines.append(txt_row('MFA            = Multi-Factor Authentication; TOTP-based for CommCell Console login'))
    lines.append(txt_row('AES-256        = Encryption algorithm for backup data; key managed by CommServe'))
    lines.append(txt_row('FIPS 140-2     = US government crypto standard; Commvault supports FIPS mode'))
    lines.append(txt_row('TLS Mutual     = Both client and server present certificates for authentication'))
    lines.append(txt_row('Immutable Copy = Backup copy protected from deletion by WORM or Object Lock'))
    lines.append(txt_row('Audit Trail    = CommServe log of all user actions; forwarded to SIEM via syslog'))
    lines.append(txt_row('Object Security= Per-object permissions in CommCell (client, policy, library level)'))
    lines.append(txt_row('Key Manager    = CommServe service managing encryption key lifecycle and escrow'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-commvault-sec-access',
    'docs/disaster-recovery/commvault/security/access-control/index.md',
    'Commvault Access Control — RBAC roles, users, and permissions',
)
def dr_commvault_sec_access():
    """Commvault Access Control — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2
    LL, LR = 3, 50
    RL2, RR2 = 53, 99

    lines = []
    lines.append(title_border(W2, 'Commvault Access Control — RBAC and Permissions'))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LL, LR), bTop(RL2, RR2))))
    lines.append(R(merge(bMid(LL, LR, 'Built-in Roles'), bMid(RL2, RR2, 'Custom Roles'))))
    lines.append(R(merge(bMid(LL, LR, 'Master Admin: full CommCell access'), bMid(RL2, RR2, 'Define capability set per role'))))
    lines.append(R(merge(bMid(LL, LR, 'Tenant Admin: manage user group'), bMid(RL2, RR2, 'Assign to user group + entity'))))
    lines.append(R(merge(bMid(LL, LR, 'View: read-only console access'), bMid(RL2, RR2, 'Entity: client, library, policy'))))
    lines.append(R(merge(bMid(LL, LR, 'Operator: run backup/restore'), bMid(RL2, RR2, 'Scope: CommCell-wide or subset'))))
    lines.append(R(merge(bMid(LL, LR, 'Report Viewer: reports only'), bMid(RL2, RR2, 'Audit: all role changes logged'))))
    lines.append(R(merge(bBot(LL, LR), bBot(RL2, RR2))))

    lines.append(txt_row())
    lines.append(txt_row('  Least privilege: operators get backup/restore rights only on their assigned clients'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'User and Group Management')))
    lines.append(R(bMid(FL, FR, 'Users: local CommCell accounts or AD domain accounts (LDAP sync)')))
    lines.append(R(bMid(FL, FR, 'Groups: CommCell user groups mirror AD groups for bulk role assignment')))
    lines.append(R(bMid(FL, FR, 'Association: user-group + role + entity = effective permission set')))
    lines.append(R(bMid(FL, FR, 'Password policy: min 12 chars, complexity, 90-day rotation, no reuse (12)')))
    lines.append(R(bMid(FL, FR, 'Service accounts: named accounts for automation; no shared credentials')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('AD integration: CommServe needs LDAP/LDAPS access to domain controller (port 389/636)'))
    lines.append(txt_row('Service accounts: stored in PAM vault (CyberArk/Vault); rotated automatically'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Capability     = Atomic permission unit (e.g. "Run Backup", "View Job", "Modify Client")'))
    lines.append(txt_row('Association    = Binding of user/group + role + entity; determines effective access'))
    lines.append(txt_row('Entity         = CommCell object (client, client group, library, storage policy, etc.)'))
    lines.append(txt_row('Master Admin   = All-powerful CommCell account; restrict to break-glass only'))
    lines.append(txt_row('Tenant Admin   = Delegated admin for a user group; cannot see other tenants'))
    lines.append(txt_row('LDAP Sync      = AD group membership synchronized to CommCell user groups periodically'))
    lines.append(txt_row('PAM            = Privileged Access Management; vault for service account credentials'))
    lines.append(txt_row('Break-glass    = Emergency admin account; access triggers immediate alert'))
    lines.append(txt_row('Role Clone     = Creating custom role by copying and modifying a built-in role'))
    lines.append(txt_row('Object Security= Per-client or per-library permissions overriding role defaults'))
    lines.append(txt_row('Audit Log      = Record of all CommCell user actions: login, backup trigger, config change'))
    lines.append(txt_row('LDAPS          = LDAP over TLS (port 636); required for secure AD authentication'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-commvault-sec-auth',
    'docs/disaster-recovery/commvault/security/authentication/index.md',
    'Commvault Authentication — Local, AD, SAML, MFA, and certificate auth',
)
def dr_commvault_sec_auth():
    """Commvault Authentication — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2
    D1, D2 = 36, 66

    lines = []
    lines.append(title_border(W2, 'Commvault Authentication — Methods and Controls'))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(sections(FL, FR, [D1, D2], ['Local Authentication', 'AD/LDAP Authentication', 'SAML/SSO'])))
    lines.append(R(sections(FL, FR, [D1, D2], ['CommCell local user DB', 'Bind to AD via LDAP/S', 'SAML 2.0 IdP (ADFS/Okta)'])))
    lines.append(R(sections(FL, FR, [D1, D2], ['Password: 12+ chars complex', 'Kerberos or NTLM fallback', 'SP metadata exchange'])))
    lines.append(R(sections(FL, FR, [D1, D2], ['90-day rotation policy', 'Group sync on login', 'JIT provisioning'])))
    lines.append(R(sections(FL, FR, [D1, D2], ['MFA: TOTP per user', 'Domain join not required', 'Attribute mapping'])))
    lines.append(R(sections(FL, FR, [D1, D2], ['Session timeout 30 min', 'LDAP port 389 / 636', 'Session: 8h default'])))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('  Recommendation: integrate AD/LDAP for user lifecycle; enforce MFA for all admins'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Certificate-Based Authentication (Component Auth)')))
    lines.append(R(bMid(FL, FR, 'All CommCell components (CS, MA, client) authenticate with TLS certificates')))
    lines.append(R(bMid(FL, FR, 'Internal CA (CommServe CA): issues certs automatically at agent install')))
    lines.append(R(bMid(FL, FR, 'Certificate renewal: automatic 30 days before expiry via CommServe')))
    lines.append(R(bMid(FL, FR, 'Custom CA: enterprise PKI certs supported; import via CommCell Console')))
    lines.append(R(bMid(FL, FR, 'CRL/OCSP: revocation check supported for enterprise PKI integration')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('AD/LDAP: CommServe needs port 389 (LDAP) or 636 (LDAPS) to domain controller'))
    lines.append(txt_row('MFA: TOTP secrets stored encrypted in CSDB; no external radius server needed'))
    lines.append(txt_row('PKI: if using enterprise CA, CommServe must reach CRL/OCSP distribution point'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SAML 2.0       = XML-based SSO standard; Commvault acts as SP; IdP: Okta/ADFS/Ping'))
    lines.append(txt_row('TOTP           = Time-based One-Time Password (RFC 6238); Google Auth/Microsoft Auth'))
    lines.append(txt_row('Kerberos       = Windows domain auth protocol used when AD integration is configured'))
    lines.append(txt_row('JIT Provision  = Just-in-time user creation in CommCell on first SAML login'))
    lines.append(txt_row('CommServe CA   = Built-in certificate authority issuing component TLS certificates'))
    lines.append(txt_row('CRL            = Certificate Revocation List; checked to validate cert not revoked'))
    lines.append(txt_row('OCSP           = Online Certificate Status Protocol; real-time cert revocation check'))
    lines.append(txt_row('Session Timeout= Idle session limit; default 30 min; configurable per security policy'))
    lines.append(txt_row('LDAP Bind      = CommServe connects to AD using a service account for user searches'))
    lines.append(txt_row('Attribute Map  = Mapping SAML attributes (email, groups) to CommCell user properties'))
    lines.append(txt_row('MFA Bypass     = Per-user MFA exception (e.g. service accounts); must be documented'))
    lines.append(txt_row('PKI            = Public Key Infrastructure; enterprise CA managing component certs'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-commvault-sec-encryption',
    'docs/disaster-recovery/commvault/security/encryption/index.md',
    'Commvault Encryption — Data at rest, in transit, and key management',
)
def dr_commvault_sec_encryption():
    """Commvault Encryption — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2
    LL, LR = 3, 50
    RL2, RR2 = 53, 99

    lines = []
    lines.append(title_border(W2, 'Commvault Encryption — At Rest, In Transit, Key Mgmt'))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LL, LR), bTop(RL2, RR2))))
    lines.append(R(merge(bMid(LL, LR, 'Data In Transit'), bMid(RL2, RR2, 'Data At Rest'))))
    lines.append(R(merge(bMid(LL, LR, 'TLS 1.2+ between all components'), bMid(RL2, RR2, 'AES-256 CBC or XTS mode'))))
    lines.append(R(merge(bMid(LL, LR, 'Certificate mutual authentication'), bMid(RL2, RR2, 'Encryption at MediaAgent layer'))))
    lines.append(R(merge(bMid(LL, LR, 'CS ↔ MA: TLS tunnel port 8403'), bMid(RL2, RR2, 'Passphrase or key file per policy'))))
    lines.append(R(merge(bMid(LL, LR, 'Client ↔ CS: TLS port 8400'), bMid(RL2, RR2, 'FIPS 140-2 mode available'))))
    lines.append(R(merge(bMid(LL, LR, 'GUI → CS: HTTPS port 443'), bMid(RL2, RR2, 'Cloud target: server-side encrypt'))))
    lines.append(R(merge(bBot(LL, LR), bBot(RL2, RR2))))

    lines.append(txt_row())
    lines.append(txt_row('  Encryption policy set in storage policy copy; applies to all jobs using that copy'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Key Management')))
    lines.append(R(bMid(FL, FR, 'Passphrase-based: user-defined passphrase → PBKDF2 key derivation → AES-256')))
    lines.append(R(bMid(FL, FR, 'Key file: randomly generated 256-bit key stored in CommServe CSDB')))
    lines.append(R(bMid(FL, FR, 'External KMS: integration with HashiCorp Vault, AWS KMS, Azure Key Vault')))
    lines.append(R(bMid(FL, FR, 'Key escrow: Commvault Key Management Server stores master key backup')))
    lines.append(R(bMid(FL, FR, 'Key rotation: re-encrypt job triggers re-encryption of DDB and chunks')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('MA CPU: AES-NI hardware acceleration (Intel/AMD) reduces encryption overhead'))
    lines.append(txt_row('KMS: external KMS requires HTTPS 443 from CommServe; verify latency < 10ms'))
    lines.append(txt_row('FIPS mode: requires FIPS-validated crypto libraries on CommServe and MA OS'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('AES-256        = Advanced Encryption Standard 256-bit; NIST-approved symmetric cipher'))
    lines.append(txt_row('PBKDF2         = Password-Based Key Derivation Function 2; derives AES key from passphrase'))
    lines.append(txt_row('FIPS 140-2     = US NIST standard for cryptographic module validation (Level 1 min)'))
    lines.append(txt_row('KMS            = Key Management Server; external system managing encryption keys'))
    lines.append(txt_row('AES-NI         = Intel/AMD CPU instruction set extension for hardware AES acceleration'))
    lines.append(txt_row('Passphrase     = User-supplied secret used to derive per-backup encryption key'))
    lines.append(txt_row('Key Escrow     = Secure backup of encryption keys to prevent permanent data loss'))
    lines.append(txt_row('Key File       = Random binary key stored in CSDB; used instead of passphrase'))
    lines.append(txt_row('Re-Encrypt Job = CommCell job that re-encrypts backup data with a new key'))
    lines.append(txt_row('SSE            = Server-Side Encryption; cloud provider encrypts objects at rest (S3/Blob)'))
    lines.append(txt_row('TLS Mutual     = Both sides present certs; prevents man-in-the-middle on backup streams'))
    lines.append(txt_row('CBC / XTS      = AES block cipher modes; XTS preferred for disk/chunk encryption'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-commvault-sec-hardening',
    'docs/disaster-recovery/commvault/security/hardening/index.md',
    'Commvault Security Hardening — OS, network, and application hardening',
)
def dr_commvault_sec_hardening():
    """Commvault Security Hardening — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2
    D1, D2, D3 = 27, 51, 75

    lines = []
    lines.append(title_border(W2, 'Commvault Security Hardening — OS, Network, App'))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['OS Hardening', 'Network Hardening', 'App Hardening', 'Monitoring'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['CIS Benchmark L1', 'Backup VLAN', 'Disable HTTP (80)', 'SIEM syslog'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Remove unused roles', 'Host firewall ACLs', 'TLS 1.2+ only', 'Audit log ship'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Disable guest/anon', 'Port whitelist', 'Disable weak ciphers', 'Alert on fail'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['Patching: 30-day SLA', 'No direct internet', 'Passphrase policy', 'Quarterly scan'])))
    lines.append(R(sections(FL, FR, [D1, D2, D3], ['AV exclusions set', 'Jump host access', 'FIPS 140-2 mode', 'Vuln disclosure'])))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('  CommServe and MAs are high-value targets; treat them as Tier 0 critical infrastructure'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Port Hardening — Required Ports Only')))
    lines.append(R(bMid(FL, FR, 'CommServe inbound: 8400 (clients), 8401 (GUI/console), 443 (Command Center)')))
    lines.append(R(bMid(FL, FR, 'MediaAgent inbound: 8403 (data tunnel from clients), NDMP 10000 (NAS)')))
    lines.append(R(bMid(FL, FR, 'SQL Server: 1433 inbound from CommServe host only (not from network)')))
    lines.append(R(bMid(FL, FR, 'Block all other inbound; allow CS→MA 8403 outbound for push jobs')))
    lines.append(R(bMid(FL, FR, 'iDRAC/iLO management: separate OOB network, no IP routing from backup VLAN')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('CommServe physical server preferred; not shared with production workloads'))
    lines.append(txt_row('Dedicated backup VLAN with ACLs; firewall between production and backup VLANs'))
    lines.append(txt_row('Out-of-band access via iDRAC/iLO on separate management network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CIS Benchmark  = Center for Internet Security hardening guide; Level 1 = baseline'))
    lines.append(txt_row('Backup VLAN    = Isolated network segment for backup traffic; separate from prod'))
    lines.append(txt_row('AV Exclusions  = Antivirus must exclude CV DDB path and library mount paths'))
    lines.append(txt_row('FIPS Mode      = CommServe/MA configured to use only FIPS-validated crypto libs'))
    lines.append(txt_row('Weak Ciphers   = TLS_RSA_WITH_3DES, RC4, MD5; disable via OS TLS configuration'))
    lines.append(txt_row('Jump Host      = Bastion server required to access CommServe console; no direct RDP'))
    lines.append(txt_row('Tier 0         = Most critical infrastructure; same security tier as AD domain controllers'))
    lines.append(txt_row('Port Whitelist = Firewall ACL allowing only required CV ports; deny-all default'))
    lines.append(txt_row('NDMP           = Network Data Management Protocol (port 10000); NAS backup protocol'))
    lines.append(txt_row('SIEM           = Security Information and Event Management; receives CV audit syslog'))
    lines.append(txt_row('Vuln Scan      = Quarterly Nessus/Qualys scan of CommServe and MA servers'))
    lines.append(txt_row('OOB Network    = Out-of-band management network for iDRAC/iLO; isolated from data'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── COMMVAULT TROUBLESHOOTING ─────────────────────────────────────────────────

@kb_diagram(
    'dr-commvault-troubleshooting',
    'docs/disaster-recovery/commvault/troubleshooting/index.md',
    'Commvault Troubleshooting — Overview and decision tree',
)
def dr_commvault_troubleshooting():
    """Commvault Troubleshooting Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2
    LL, LR = 3, 50
    RL2, RR2 = 53, 99

    lines = []
    lines.append(title_border(W2, 'Commvault Troubleshooting — Decision Tree'))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Problem Reported')))
    lines.append(R(bMid(FL, FR, 'Backup job failed · Restore failed · Slow backup · CommServe unreachable')))
    lines.append(R(bMid(FL, FR, 'First check: CommCell Console Job Activity → view job details and error code')))
    lines.append(R(bMid(FL, FR, 'Error code lookup: Commvault KB (ma.commvault.com) or cv_help <error_code>')))
    lines.append(R(bMid(FL, FR, 'Collect: job ID, client name, MA name, error message, log files')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('  Triage by component: CommServe → MediaAgent → Client → Network → Storage'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LL, LR), bTop(RL2, RR2))))
    lines.append(R(merge(bMid(LL, LR, 'CommServe Issues'), bMid(RL2, RR2, 'MediaAgent Issues'))))
    lines.append(R(merge(bMid(LL, LR, 'Services down: check GxCVD/GxJobMgr'), bMid(RL2, RR2, 'MA offline: check GxCLMgrS service'))))
    lines.append(R(merge(bMid(LL, LR, 'SQL errors: check CSDB log, reindex'), bMid(RL2, RR2, 'DDB corrupt: run DDB Verify + repair'))))
    lines.append(R(merge(bMid(LL, LR, 'Job stuck queued: check resource pool'), bMid(RL2, RR2, 'Disk full: prune or expand library'))))
    lines.append(R(merge(bMid(LL, LR, 'Log: C:\\CV\\Log Files\\CommServe.log'), bMid(RL2, RR2, 'Log: C:\\CV\\Log Files\\MediaAgent.log'))))
    lines.append(R(merge(bMid(LL, LR, 'CS restart: net stop/start GxCVD'), bMid(RL2, RR2, 'MA restart: net stop/start GxCLMgrS'))))
    lines.append(R(merge(bBot(LL, LR), bBot(RL2, RR2))))

    lines.append(txt_row())
    lines.append(txt_row('  For unresolved issues: collect CV_DIAG bundle → open Commvault Support case'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Client / Network Issues')))
    lines.append(R(bMid(FL, FR, 'Client unreachable: ping, telnet CS:8400, check firewall/proxy config')))
    lines.append(R(bMid(FL, FR, 'iDA not responding: restart GxFWD / GxCVD service on client')))
    lines.append(R(bMid(FL, FR, 'Network: check bandwidth, test MA:8403 reachability from client')))
    lines.append(R(bMid(FL, FR, 'App backup fail: check VSS/RMAN/VDI integration; review app agent log')))
    lines.append(R(bMid(FL, FR, 'CV_DIAG: CommCell → Help → Diagnostics → Run Diagnostics; zip and upload')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Network: traceroute client → MA (port 8403); verify MTU and QoS settings'))
    lines.append(txt_row('Storage: check MA disk I/O (iostat); full library is common backup failure cause'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('GxCVD          = CommVault Communications Service; core daemon on all CV components'))
    lines.append(txt_row('GxJobMgr       = Job Manager service on CommServe; schedules and monitors all jobs'))
    lines.append(txt_row('GxCLMgrS       = Client Manager Service; manages iDA agents on client machines'))
    lines.append(txt_row('GxFWD          = CommVault Firewall Daemon; handles tunnel/proxy communications'))
    lines.append(txt_row('CV_DIAG        = Diagnostic collection tool; generates zip of all logs and config'))
    lines.append(txt_row('Error Code     = 4-digit Commvault error code; searchable in ma.commvault.com KB'))
    lines.append(txt_row('DDB Verify     = Job scanning all DDB entries for corruption; run monthly or on error'))
    lines.append(txt_row('Resource Pool  = CommServe construct limiting concurrent jobs per MA or client group'))
    lines.append(txt_row('CSDB Integrity = SQL DBCC CHECKDB on CommCell database; run quarterly'))
    lines.append(txt_row('Job Details    = Per-phase job log with timestamps, data rates, and error codes'))
    lines.append(txt_row('ma.commvault.com = Commvault support portal; KB articles and case management'))
    lines.append(txt_row('Triage Order   = CS services → MA services → Client connectivity → App agent → Network'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-commvault-ts-issues',
    'docs/disaster-recovery/commvault/troubleshooting/common-issues/index.md',
    'Commvault Common Issues — Symptoms, causes, and fixes',
)
def dr_commvault_ts_issues():
    """Commvault Common Issues — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2

    lines = []
    lines.append(title_border(W2, 'Commvault Common Issues — Symptoms and Fixes'))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Issue: Backup Jobs Consistently Failing')))
    lines.append(R(bMid(FL, FR, 'Symptom: jobs show "Failed" status; error in job details')))
    lines.append(R(bMid(FL, FR, 'Cause A: disk library full → fix: prune expired data or expand library')))
    lines.append(R(bMid(FL, FR, 'Cause B: client iDA offline → fix: restart GxCVD on client host')))
    lines.append(R(bMid(FL, FR, 'Cause C: MA unreachable → fix: check network, restart GxCLMgrS on MA')))
    lines.append(R(bMid(FL, FR, 'Cause D: DDB corruption → fix: run DDB Verification + repair job')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Issue: Slow Backup Performance')))
    lines.append(R(bMid(FL, FR, 'Symptom: backup throughput < expected; jobs taking 3x longer than baseline')))
    lines.append(R(bMid(FL, FR, 'Cause A: DDB fragmentation → fix: run DDB defrag job; schedule monthly')))
    lines.append(R(bMid(FL, FR, 'Cause B: network saturation → fix: enable bandwidth throttling or QoS')))
    lines.append(R(bMid(FL, FR, 'Cause C: MA CPU/disk bottleneck → fix: check iostat; add MA or upgrade disk')))
    lines.append(R(bMid(FL, FR, 'Cause D: too many concurrent jobs → fix: reduce max concurrent streams')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Issue: CommServe Unreachable')))
    lines.append(R(bMid(FL, FR, 'Symptom: CommCell Console cannot connect; clients cannot register')))
    lines.append(R(bMid(FL, FR, 'Check A: Windows services GxCVD, GxJobMgr, SQL Server running')))
    lines.append(R(bMid(FL, FR, 'Check B: port 8400/8401 open; test: telnet <CS_IP> 8400')))
    lines.append(R(bMid(FL, FR, 'Check C: CSDB accessible; test: sqlcmd -S localhost -Q "SELECT 1"')))
    lines.append(R(bMid(FL, FR, 'Fix: restart CV services; if SQL down, restore from CSDB backup')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Disk full: check mount path with df -h (Linux) or Get-PSDrive (Windows PowerShell)'))
    lines.append(txt_row('Network: use iperf3 between client and MA to measure actual throughput'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('DDB Defrag     = MediaAgent job that rewrites DDB to reduce fragmentation overhead'))
    lines.append(txt_row('Library Full   = Disk library mount path at 100% usage; new backup writes fail'))
    lines.append(txt_row('Pruning        = Commvault job removing expired chunks from library to free space'))
    lines.append(txt_row('Throughput     = Backup data rate in MB/s; baseline by running benchmark backup'))
    lines.append(txt_row('Concurrent Streams = Number of parallel data streams to a single MA'))
    lines.append(txt_row('GxJobMgr       = CommServe Job Manager; if stopped, no jobs will run'))
    lines.append(txt_row('sqlcmd         = SQL Server CLI tool; use to verify CSDB is responding'))
    lines.append(txt_row('iperf3         = Network throughput test tool; use between client and MA servers'))
    lines.append(txt_row('GxCLMgrS       = MediaAgent component service; if stopped, MA shows offline in CS'))
    lines.append(txt_row('Max Streams    = CommCell setting limiting parallel backup jobs per MA'))
    lines.append(txt_row('DDB Repair     = Automated repair mode of DDB Verification job; fixes detectable errors'))
    lines.append(txt_row('CSDB Restore   = Last-resort recovery: restore SQL backup + replay transaction logs'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-commvault-ts-diagnostics',
    'docs/disaster-recovery/commvault/troubleshooting/diagnostics/index.md',
    'Commvault Diagnostics — Log locations, diagnostic tools, and commands',
)
def dr_commvault_ts_diagnostics():
    """Commvault Diagnostics — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2
    LL, LR = 3, 50
    RL2, RR2 = 53, 99

    lines = []
    lines.append(title_border(W2, 'Commvault Diagnostics — Logs, Tools, Commands'))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LL, LR), bTop(RL2, RR2))))
    lines.append(R(merge(bMid(LL, LR, 'Log File Locations'), bMid(RL2, RR2, 'Diagnostic Tools'))))
    lines.append(R(merge(bMid(LL, LR, 'CS: C:\\CV\\Log Files\\CommServe.log'), bMid(RL2, RR2, 'CV_DIAG: collect all logs + config'))))
    lines.append(R(merge(bMid(LL, LR, 'MA: C:\\CV\\Log Files\\MediaAgent.log'), bMid(RL2, RR2, 'CommVaultDiagnostics.exe on CS'))))
    lines.append(R(merge(bMid(LL, LR, 'JobMgr: GxJobMgrService.log'), bMid(RL2, RR2, 'cvping: test component connectivity'))))
    lines.append(R(merge(bMid(LL, LR, 'Client: C:\\CV\\Log Files\\clBackup.log'), bMid(RL2, RR2, 'cvdiskperf: benchmark MA disk I/O'))))
    lines.append(R(merge(bMid(LL, LR, 'Linux: /var/log/commvault/Log_Files/'), bMid(RL2, RR2, 'cvnetwork: test MA network bandwidth'))))
    lines.append(R(merge(bBot(LL, LR), bBot(RL2, RR2))))

    lines.append(txt_row())
    lines.append(txt_row('  Always collect CV_DIAG before opening a support case; include job ID and error code'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Key Diagnostic Commands')))
    lines.append(R(bMid(FL, FR, 'qlist jobs -jobid <id> -verbose       → detailed job phase log')))
    lines.append(R(bMid(FL, FR, 'qlist client -name <host>             → client registration status')))
    lines.append(R(bMid(FL, FR, 'qlist storage -type disk -verbose     → disk library mount paths + usage')))
    lines.append(R(bMid(FL, FR, 'cvping -clientName <host>             → test CS-to-client connectivity')))
    lines.append(R(bMid(FL, FR, 'CommVaultDiagnostics.exe -collect all → generate full diagnostic bundle')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Log rotation: CV logs rotate at 10 MB by default; 30-day retention'))
    lines.append(txt_row('Disk for logs: CommServe log partition should be separate from CSDB partition'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CV_DIAG        = Diagnostic bundle: all component logs, config exports, event logs'))
    lines.append(txt_row('cvping         = CommVault connectivity test tool (not ICMP ping; tests CV comms)'))
    lines.append(txt_row('cvdiskperf     = Measures sequential read/write performance of MA disk library path'))
    lines.append(txt_row('cvnetwork      = Tests throughput and latency between CommVault components'))
    lines.append(txt_row('clBackup.log   = Client-side backup agent log; shows pre/post scripts, CBT activity'))
    lines.append(txt_row('GxJobMgrSvc    = CommServe Job Manager service log; shows job dispatch and errors'))
    lines.append(txt_row('MediaAgent.log = MA-side data pipeline log; shows dedup, compress, write operations'))
    lines.append(txt_row('CommServe.log  = Main CommServe service log; CS startup, DB queries, scheduler'))
    lines.append(txt_row('Job Phase      = Individual step within a backup job (scan, transfer, dedup, write)'))
    lines.append(txt_row('Error Code     = 4-5 digit CV error; search on ma.commvault.com for KB resolution'))
    lines.append(txt_row('-verbose flag  = qlist flag enabling detailed per-object output for all list commands'))
    lines.append(txt_row('Log Rotation   = Commvault auto-rotates logs at size limit; old logs archived to .gz'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-commvault-ts-escalation',
    'docs/disaster-recovery/commvault/troubleshooting/escalation/index.md',
    'Commvault Escalation — Support tiers, case handling, and vendor escalation',
)
def dr_commvault_ts_escalation():
    """Commvault Escalation Path — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    FL, FR = 3, 99
    MID = (FL + FR) // 2
    LL, LR = 3, 50
    RL2, RR2 = 53, 99

    lines = []
    lines.append(title_border(W2, 'Commvault Escalation — Support and Case Handling'))
    lines.append(txt_row())

    lines.append(R(merge(bTop(LL, LR), bTop(RL2, RR2))))
    lines.append(R(merge(bMid(LL, LR, 'Internal Tier 1 — L1 Ops'), bMid(RL2, RR2, 'Internal Tier 2 — L2 Backup Eng'))))
    lines.append(R(merge(bMid(LL, LR, 'Check Job Activity for failures'), bMid(RL2, RR2, 'Deep log analysis (CV_DIAG)'))))
    lines.append(R(merge(bMid(LL, LR, 'Restart CV services (GxCVD)'), bMid(RL2, RR2, 'DDB repair and library fixes'))))
    lines.append(R(merge(bMid(LL, LR, 'Check disk library free space'), bMid(RL2, RR2, 'CommServe DB troubleshooting'))))
    lines.append(R(merge(bMid(LL, LR, 'Run CV_DIAG collection'), bMid(RL2, RR2, 'Config change and policy review'))))
    lines.append(R(merge(bMid(LL, LR, 'Escalate if not resolved in 2h'), bMid(RL2, RR2, 'Escalate to Commvault Support'))))
    lines.append(R(merge(bBot(LL, LR), bBot(RL2, RR2))))

    lines.append(txt_row())
    lines.append(txt_row('  Escalation path: L1 Ops → L2 Backup Engineering → Commvault Vendor Support'))
    lines.append(txt_row())
    lines.append(R(arrow([MID])))
    lines.append(txt_row())

    lines.append(R(bTop(FL, FR)))
    lines.append(R(bMid(FL, FR, 'Commvault Vendor Support (Tier 3)')))
    lines.append(R(bMid(FL, FR, 'Portal: ma.commvault.com → Create Case; login with entitled account')))
    lines.append(R(bMid(FL, FR, 'Severity 1 (production down): 24x7 response SLA 1h; call hotline immediately')))
    lines.append(R(bMid(FL, FR, 'Severity 2 (degraded): business hours response SLA 4h; email + portal')))
    lines.append(R(bMid(FL, FR, 'Required info: CS version, SP level, CV_DIAG bundle, error codes, job IDs')))
    lines.append(R(bMid(FL, FR, 'Remote assist: Commvault engineer joins via WebEx/remote session if needed')))
    lines.append(R(bBot(FL, FR)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Commvault Support may request firewall exception for remote session (WebEx/Teams)'))
    lines.append(txt_row('Ensure CV_DIAG bundle uploadable to Commvault FTP or case attachment (< 2 GB)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ma.commvault.com = Commvault support portal for case management and KB articles'))
    lines.append(txt_row('Severity 1     = Complete production outage; CommServe down or all backups failing'))
    lines.append(txt_row('Severity 2     = Significant impact; some backups failing or restore degraded'))
    lines.append(txt_row('CV_DIAG Bundle = Compressed log and config archive required for all support cases'))
    lines.append(txt_row('SP Level       = Service Pack version installed; check Help → About in CommCell Console'))
    lines.append(txt_row('Entitled Acct  = Commvault support portal account tied to licensed CommCell ID'))
    lines.append(txt_row('Remote Session = Commvault engineer connects to CommServe for live troubleshooting'))
    lines.append(txt_row('CommCell ID    = Unique identifier for the CommCell installation; required for support'))
    lines.append(txt_row('Case Number    = Reference ID from Commvault portal; track via ma.commvault.com'))
    lines.append(txt_row('L2 Backup Eng  = Internal SME for CommVault; owns platform config and deep diagnosis'))
    lines.append(txt_row('Hotline        = Commvault 24x7 phone support for Sev1; number on support portal'))
    lines.append(txt_row('Entitlement    = Active support contract tied to CommCell serial number'))
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'dr-netbackup',
    'docs/disaster-recovery/netbackup/index.md',
    'Enterprise backup and recovery — master/media/client architecture with deduplication',
)
def _dr_netbackup_overview():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Overview'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'NetBackup')))
    lines.append(R(bMid(3, 99, 'Enterprise backup and recovery — master/media/client architecture with deduplication')))
    lines.append(R(bMid(3, 99, 'Master Server     — scheduler, catalog, policy engine, job controller')))
    lines.append(R(bMid(3, 99, 'Media Server      — data mover, dedup engine, storage unit management')))
    lines.append(R(bMid(3, 99, 'Client Agent      — installed on protected host; sends data to media server')))
    lines.append(R(bMid(3, 99, 'Management: 443 (Web UI) · Auth: NBU CA host-ID certificates; AD/LDAP for web UI lo')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Architecture: components work together to deliver NetBackup capabilities'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Architecture'), bMid(53, 99, 'Operations'))))
    lines.append(R(merge(bMid(3, 50, 'Master Server     — scheduler, catalog, pol'), bMid(53, 99, 'bpbackup / bprestore'))))
    lines.append(R(merge(bMid(3, 50, 'Media Server      — data mover, dedup engin'), bMid(53, 99, 'bplist / bpdbjobs'))))
    lines.append(R(merge(bMid(3, 50, 'Client Agent      — installed on protected '), bMid(53, 99, 'nbpemreq / bpps'))))
    lines.append(R(merge(bMid(3, 50, 'NetBackup Web UI  — browser admin portal on'), bMid(53, 99, 'tpconfig / nbstlutil'))))
    lines.append(R(merge(bMid(3, 50, 'Catalog           — PostgreSQL DB tracking '), bMid(53, 99, 'bpexpdate / bpimmediate'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-architecture',
    'docs/disaster-recovery/netbackup/architecture/index.md',
    'NetBackup — architecture overview, components, data flow',
)
def _dr_netbackup_architecture():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Architecture'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'NetBackup — Component Architecture')))
    lines.append(R(bMid(3, 99, 'Master Server     — scheduler, catalog, policy engine, job controller')))
    lines.append(R(bMid(3, 99, 'Media Server      — data mover, dedup engine, storage unit management')))
    lines.append(R(bMid(3, 99, 'Client Agent      — installed on protected host; sends data to media server')))
    lines.append(R(bMid(3, 99, 'Ports: 443 (Web UI) · 1556 (vnetd) · 13724 (bprd)')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Three-tier component model — control plane, data plane, and management'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Control Plane'), bMid(36, 66, 'Data Plane'), bMid(69, 99, 'Management'))))
    lines.append(R(merge(bMid(3, 33, 'Master Server     — schedule'), bMid(36, 66, 'Media Server      — data mov'), bMid(69, 99, 'NetBackup Web UI  — browser '))))
    lines.append(R(merge(bMid(3, 33, 'Scheduling'), bMid(36, 66, 'Replication/Backup'), bMid(69, 99, '443 (Web UI)'))))
    lines.append(R(merge(bMid(3, 33, 'Policy mgmt'), bMid(36, 66, 'Data movement'), bMid(69, 99, 'REST API'))))
    lines.append(R(merge(bMid(3, 33, 'Catalog/DB'), bMid(36, 66, 'Dedup/compress'), bMid(69, 99, 'RBAC'))))
    lines.append(R(merge(bMid(3, 33, 'Job engine'), bMid(36, 66, '1556 (vnetd)'), bMid(69, 99, 'Alerting'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-arch-how-it-works',
    'docs/disaster-recovery/netbackup/architecture/how-it-works/index.md',
    'NetBackup — how replication or backup data flows step by step',
)
def _dr_netbackup_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('  NetBackup data flow — from source to target through the protection pipeline:'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, '1  Source / Production System')))
    lines.append(R(bMid(3, 99, '   Master Server     — scheduler, catalog, policy engine, job controller')))
    lines.append(R(bMid(3, 99, '   Host writes are intercepted or snapshotted by the NetBackup agent/proxy')))
    lines.append(R(bMid(3, 99, '   Changed blocks tracked via CBT / journal / delta-set mechanism')))
    lines.append(R(bMid(3, 99, '   Consistency ensured at quiesce point before data transfer begins')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Changed data forwarded to the NetBackup engine — compression and encryption applied in transit'))
    lines.append(txt_row())
    lines.append(R(arrow([51])))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, '2  NetBackup Engine')))
    lines.append(R(bMid(3, 99, '   Media Server      — data mover, dedup engine, storage unit management')))
    lines.append(R(bMid(3, 99, '   Data compressed, deduplicated, and encrypted before storage')))
    lines.append(R(bMid(3, 99, '   Metadata catalog updated; job status reported to control plane')))
    lines.append(R(bMid(3, 99, '   bpbackup / bprestore')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([51])))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, '3  Target / Repository')))
    lines.append(R(bMid(3, 99, '   Client Agent      — installed on protected host; sends data to media server')))
    lines.append(R(bMid(3, 99, '   Recovery point written; retention policy applied automatically')))
    lines.append(R(bMid(3, 99, '   Restore: bplist / bpdbjobs')))
    lines.append(R(bMid(3, 99, '   RTO driven by target storage performance and data volume')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-arch-design',
    'docs/disaster-recovery/netbackup/architecture/design-standards/index.md',
    'NetBackup — sizing, design rules, capacity, HA guidelines',
)
def _dr_netbackup_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Design Standards'))
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
    lines.append(txt_row('  Ports: 443 (Web UI) · 1556 (vnetd) · 13724 (bprd)'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Standard NetBackup Design Rules')))
    lines.append(R(bMid(3, 99, 'RPO target drives snapshot/cycle frequency — document in service design')))
    lines.append(R(bMid(3, 99, 'RTO target drives recovery tier: instant, warm standby, or cold restore')))
    lines.append(R(bMid(3, 99, 'Dedicated backup network VLAN — no shared production traffic')))
    lines.append(R(bMid(3, 99, 'Encryption enabled on all channels: AES-256 backup encryption; KMS key management; TLS 1.2+ on all channel')))
    lines.append(R(bMid(3, 99, 'Service accounts: minimum privilege; rotate credentials quarterly')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-arch-integrations',
    'docs/disaster-recovery/netbackup/architecture/integrations/index.md',
    'NetBackup — integration points with external systems and APIs',
)
def _dr_netbackup_arch_integrations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Architecture Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'NetBackup — External Integration Points')))
    lines.append(R(bMid(3, 99, 'Auth: NBU CA host-ID certificates; AD/LDAP for web UI login; RBAC roles')))
    lines.append(R(bMid(3, 99, 'Storage: connected via 443 (Web UI) · 1556 (vnetd)')))
    lines.append(R(bMid(3, 99, 'Monitoring: SNMP traps / syslog / REST API to ITSM and alerting systems')))
    lines.append(R(bMid(3, 99, 'Encryption: AES-256 backup encryption; KMS key management; TLS 1.2+ on all channels')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Identity'), bMid(36, 66, 'Storage'), bMid(69, 99, 'Monitoring'))))
    lines.append(R(merge(bMid(3, 33, 'AD / LDAP'), bMid(36, 66, '443 (Web UI)'), bMid(69, 99, 'SNMP / syslog'))))
    lines.append(R(merge(bMid(3, 33, 'SAML SSO'), bMid(36, 66, '1556 (vnetd)'), bMid(69, 99, 'REST webhook'))))
    lines.append(R(merge(bMid(3, 33, 'RBAC roles'), bMid(36, 66, 'NFS / iSCSI / FC'), bMid(69, 99, 'Email alerts'))))
    lines.append(R(merge(bMid(3, 33, 'MFA optional'), bMid(36, 66, 'Dedup appliance'), bMid(69, 99, 'ServiceNow'))))
    lines.append(R(merge(bMid(3, 33, 'Cert auth'), bMid(36, 66, 'Object storage'), bMid(69, 99, 'Prometheus'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-operations',
    'docs/disaster-recovery/netbackup/operations/index.md',
    'NetBackup — operations overview, key tasks, day-to-day procedures',
)
def _dr_netbackup_operations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'NetBackup — Day-to-Day Operations')))
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
    lines.append(R(merge(bMid(3, 33, 'bpbackup / bprestore'), bMid(36, 66, 'nbpemreq / bpps'), bMid(69, 99, 'bplist / bpdbjobs'))))
    lines.append(R(merge(bMid(3, 33, 'Schedule jobs'), bMid(36, 66, 'Health checks'), bMid(69, 99, 'Instant restore'))))
    lines.append(R(merge(bMid(3, 33, 'Retention mgmt'), bMid(36, 66, 'Capacity alerts'), bMid(69, 99, 'Failover test'))))
    lines.append(R(merge(bMid(3, 33, 'Consistency grp'), bMid(36, 66, 'Log review'), bMid(69, 99, 'DR runbook'))))
    lines.append(R(merge(bMid(3, 33, 'Policy updates'), bMid(36, 66, 'SLA tracking'), bMid(69, 99, 'Validate RTO'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-ops-backup',
    'docs/disaster-recovery/netbackup/operations/backup-restore/index.md',
    'NetBackup — backup and restore procedures',
)
def _dr_netbackup_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Backup & Restore'))
    lines.append(txt_row())
    lines.append(txt_row('  Backup flow: quiesce source → snapshot/copy → transfer → write to target → catalog'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Backup (Protection)'), bMid(53, 99, 'Restore (Recovery)'))))
    lines.append(R(merge(bMid(3, 50, 'bpbackup / bprestore'), bMid(53, 99, 'bplist / bpdbjobs'))))
    lines.append(R(merge(bMid(3, 50, 'Quiesce source I/O'), bMid(53, 99, 'Select recovery point'))))
    lines.append(R(merge(bMid(3, 50, 'Take snapshot / CBT'), bMid(53, 99, 'Mount or copy to target'))))
    lines.append(R(merge(bMid(3, 50, 'Transfer changed blocks'), bMid(53, 99, 'Validate integrity'))))
    lines.append(R(merge(bMid(3, 50, 'Commit to repository'), bMid(53, 99, 'Restart application'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Key NetBackup Commands')))
    lines.append(R(bMid(3, 99, '  Backup trigger  : bpbackup / bprestore')))
    lines.append(R(bMid(3, 99, '  List points     : bplist / bpdbjobs')))
    lines.append(R(bMid(3, 99, '  Health status   : nbpemreq / bpps')))
    lines.append(R(bMid(3, 99, '  Retention mgmt  : bpexpdate / bpimmediate')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-ops-cli',
    'docs/disaster-recovery/netbackup/operations/cli-reference/index.md',
    'NetBackup — CLI commands reference',
)
def _dr_netbackup_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — CLI Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'NetBackup — Command Reference')))
    lines.append(R(bMid(3, 99, 'Use these commands for routine operations, scripting, and troubleshooting')))
    lines.append(R(bMid(3, 99, '  bpbackup / bprestore')))
    lines.append(R(bMid(3, 99, '  bplist / bpdbjobs')))
    lines.append(R(bMid(3, 99, '  nbpemreq / bpps')))
    lines.append(R(bMid(3, 99, '  tpconfig / nbstlutil')))
    lines.append(R(bMid(3, 99, '  bpexpdate / bpimmediate')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Ports: 443 (Web UI) · 1556 (vnetd) · 13724 (bprd)'))
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
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-ops-health',
    'docs/disaster-recovery/netbackup/operations/health-checks/index.md',
    'NetBackup — health check procedures and monitoring commands',
)
def _dr_netbackup_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Health Checks'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'NetBackup — Health Check Procedures')))
    lines.append(R(bMid(3, 99, 'Run these checks daily/weekly to confirm protection is working')))
    lines.append(R(bMid(3, 99, '  nbpemreq / bpps')))
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
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-ops-install',
    'docs/disaster-recovery/netbackup/operations/install-upgrade/index.md',
    'NetBackup — install and upgrade procedures',
)
def _dr_netbackup_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Install & Upgrade'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'NetBackup — Installation Prerequisites')))
    lines.append(R(bMid(3, 99, '  OS: supported Linux or Windows Server (see vendor compatibility matrix)')))
    lines.append(R(bMid(3, 99, '  Network: 443 (Web UI) · 1556 (vnetd) — ensure firewall allows these')))
    lines.append(R(bMid(3, 99, '  Auth: NBU CA host-ID certificates; AD/LDAP for web UI login; RBAC roles')))
    lines.append(R(bMid(3, 99, '  Storage: Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection')))
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
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-ops-procedures',
    'docs/disaster-recovery/netbackup/operations/procedures/index.md',
    'NetBackup — operational procedures and runbooks',
)
def _dr_netbackup_ops_procedures():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Procedures'))
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
    lines.append(R(bMid(3, 99, 'Change Control Requirements for NetBackup')))
    lines.append(R(bMid(3, 99, '  All changes to protection policies require change ticket with rollback plan')))
    lines.append(R(bMid(3, 99, '  Failover tests must be scheduled in maintenance window')))
    lines.append(R(bMid(3, 99, '  Firmware/software upgrades need 48 h pre-approval and backup snapshot')))
    lines.append(R(bMid(3, 99, '  Post-change: verify jobs run successfully for 2 backup cycles')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-ops-scripts',
    'docs/disaster-recovery/netbackup/operations/scripts/index.md',
    'NetBackup — automation scripts and examples',
)
def _dr_netbackup_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Scripts'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'NetBackup — Automation Scripts')))
    lines.append(R(bMid(3, 99, 'Scripts automate routine NetBackup operations — run via cron or CI/CD')))
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
    lines.append(R(merge(bMid(3, 50, 'nbpemreq / bpps'), bMid(53, 99, 'tpconfig / nbstlutil'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-security',
    'docs/disaster-recovery/netbackup/security/index.md',
    'NetBackup — security overview, controls, compliance posture',
)
def _dr_netbackup_security():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Security'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'NetBackup — Security Posture')))
    lines.append(R(bMid(3, 99, 'Authentication: NBU CA host-ID certificates; AD/LDAP for web UI login; RBAC roles')))
    lines.append(R(bMid(3, 99, 'Encryption: AES-256 backup encryption; KMS key management; TLS 1.2+ on all channels')))
    lines.append(R(bMid(3, 99, 'Network: management VLAN separated; 13724 (bprd) management port')))
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
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-sec-access',
    'docs/disaster-recovery/netbackup/security/access-control/index.md',
    'NetBackup — RBAC, permissions, service accounts',
)
def _dr_netbackup_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Access Control'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'NetBackup — RBAC and Access Control')))
    lines.append(R(bMid(3, 99, 'Auth: NBU CA host-ID certificates; AD/LDAP for web UI login; RBAC roles')))
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
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-sec-auth',
    'docs/disaster-recovery/netbackup/security/authentication/index.md',
    'NetBackup — authentication methods, certificate management',
)
def _dr_netbackup_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Authentication'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'NetBackup — Authentication Methods')))
    lines.append(R(bMid(3, 99, 'NBU CA host-ID certificates; AD/LDAP for web UI login; RBAC roles')))
    lines.append(R(bMid(3, 99, 'Management UI: HTTPS on 443 (Web UI) — browser-based login')))
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
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-sec-enc',
    'docs/disaster-recovery/netbackup/security/encryption/index.md',
    'NetBackup — encryption at rest and in transit',
)
def _dr_netbackup_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Encryption'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'NetBackup — Encryption Configuration')))
    lines.append(R(bMid(3, 99, 'AES-256 backup encryption; KMS key management; TLS 1.2+ on all channels')))
    lines.append(R(bMid(3, 99, 'In-transit: TLS 1.2+ for all management; data channel also encrypted')))
    lines.append(R(bMid(3, 99, 'At-rest: AES-256 on repository or vault storage; key managed by KMS')))
    lines.append(R(bMid(3, 99, 'Key lifecycle: generate → use → rotate (annual) → retire → destroy')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'In-Transit'), bMid(53, 99, 'At-Rest'))))
    lines.append(R(merge(bMid(3, 50, 'TLS 1.2+ (minimum)'), bMid(53, 99, 'AES-256 encryption'))))
    lines.append(R(merge(bMid(3, 50, '443 (Web UI) HTTPS'), bMid(53, 99, 'KMS key management'))))
    lines.append(R(merge(bMid(3, 50, 'Mutual TLS internal'), bMid(53, 99, 'WORM / immutable'))))
    lines.append(R(merge(bMid(3, 50, 'Cert rotation annual'), bMid(53, 99, 'Key rotation annual'))))
    lines.append(R(merge(bMid(3, 50, 'No plain-text admin'), bMid(53, 99, 'Audit key access'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-sec-hardening',
    'docs/disaster-recovery/netbackup/security/hardening/index.md',
    'NetBackup — hardening guide, CIS controls, secure configuration',
)
def _dr_netbackup_sec_hardening():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Hardening'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'NetBackup — Hardening Checklist')))
    lines.append(R(bMid(3, 99, '  [ ] Disable default/admin accounts; create named admin accounts only')))
    lines.append(R(bMid(3, 99, '  [ ] Enable MFA for all interactive logins via IdP / SAML SSO')))
    lines.append(R(bMid(3, 99, '  [ ] Restrict management port (443 (Web UI)) to jump host / management VLAN')))
    lines.append(R(bMid(3, 99, '  [ ] Enable audit logging and forward to SIEM (syslog, TLS port 6514)')))
    lines.append(R(bMid(3, 99, '  [ ] Apply all security patches within 30 days of vendor release')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Network Hardening')))
    lines.append(R(bMid(3, 99, '  [ ] Separate backup VLAN — no direct production host access to repo')))
    lines.append(R(bMid(3, 99, '  [ ] Firewall: allow only 443 (Web UI) · 1556 (vnetd) · 13724 (bprd)')))
    lines.append(R(bMid(3, 99, '  [ ] Disable unused ports and protocols on management interface')))
    lines.append(R(bMid(3, 99, '  [ ] Immutable repository: enable WORM or object lock on backup target')))
    lines.append(R(bMid(3, 99, '  [ ] Encryption in transit: disable TLS 1.0/1.1; enforce TLS 1.2+')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-troubleshooting',
    'docs/disaster-recovery/netbackup/troubleshooting/index.md',
    'NetBackup — troubleshooting overview and triage approach',
)
def _dr_netbackup_troubleshooting():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'NetBackup — Troubleshooting Approach')))
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
    lines.append(R(merge(bMid(3, 33, '443 (Web UI)'), bMid(36, 66, 'Timeout errors'), bMid(69, 99, 'Restore test'))))
    lines.append(R(merge(bMid(3, 33, 'Firewall rules'), bMid(36, 66, 'Version compat'), bMid(69, 99, 'RPO drift'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-ts-issues',
    'docs/disaster-recovery/netbackup/troubleshooting/common-issues/index.md',
    'NetBackup — common issues, root causes, and fixes',
)
def _dr_netbackup_ts_issues():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Common Issues'))
    lines.append(txt_row())
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Symptom', 'Likely Cause', 'First Check', 'Fix', 'Verify'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Status 96', 'client not respon', 'ping + bpps on cl', 'restart nbclient', 'bpps -x'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Status 2106', 'MSDP pool full', 'bpexpdate / nbstl', 'expand or expire', 'nbstlutil list'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Status 58', 'media write error', 'check disk/tape h', 'new storage unit', 'tpconfig -d'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Status 84', 'media manager dow', 'check ltid proces', 'restart ltid', 'vmquery'])))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'General Triage Pattern')))
    lines.append(R(bMid(3, 99, '  Is the issue new or recurring? New = recent change; Recurring = config problem')))
    lines.append(R(bMid(3, 99, '  Is it isolated to one source or all? Isolated = agent; All = server/repo')))
    lines.append(R(bMid(3, 99, '  Check logs first: nbpemreq / bpps')))
    lines.append(R(bMid(3, 99, '  If unresolved in 2h: open vendor case with full log bundle')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-ts-diag',
    'docs/disaster-recovery/netbackup/troubleshooting/diagnostics/index.md',
    'NetBackup — diagnostic commands and log collection',
)
def _dr_netbackup_ts_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Diagnostics'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'NetBackup — Diagnostic Commands')))
    lines.append(R(bMid(3, 99, 'Collect these before opening a vendor support case')))
    lines.append(R(bMid(3, 99, '  nbpemreq / bpps')))
    lines.append(R(bMid(3, 99, '  tpconfig / nbstlutil')))
    lines.append(R(bMid(3, 99, '  Check system logs: /var/log/ or Windows Event Viewer')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Log Collection'), bMid(53, 99, 'Live Diagnostics'))))
    lines.append(R(merge(bMid(3, 50, 'Application log bundle'), bMid(53, 99, 'Network connectivity'))))
    lines.append(R(merge(bMid(3, 50, 'OS syslog (journalctl)'), bMid(53, 99, 'Storage path check'))))
    lines.append(R(merge(bMid(3, 50, 'Core dump if crashed'), bMid(53, 99, 'Process list check'))))
    lines.append(R(merge(bMid(3, 50, 'Config export/backup'), bMid(53, 99, 'Port reachability'))))
    lines.append(R(merge(bMid(3, 50, 'nbpemreq / bpps'), bMid(53, 99, 'tpconfig / nbstlutil'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-netbackup-ts-escalation',
    'docs/disaster-recovery/netbackup/troubleshooting/escalation/index.md',
    'NetBackup — escalation path, vendor support, and SLA',
)
def _dr_netbackup_ts_escalation():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'NetBackup — Escalation'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'NetBackup — Escalation Path')))
    lines.append(R(bMid(3, 99, 'L1 Triage: review logs, match to known issues in runbook (0–30 min)')))
    lines.append(R(bMid(3, 99, 'L2 Engineering: deep analysis, config review, lab reproduction (30 min – 4 h)')))
    lines.append(R(bMid(3, 99, 'Vendor Support: open case with log bundle if unresolved at L2 (> 4 h)')))
    lines.append(R(bMid(3, 99, 'Sev1 (data loss / production impact): page on-call + open critical case')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Information to Collect Before Escalating')))
    lines.append(R(bMid(3, 99, '  Product version: NetBackup version string from About / version command')))
    lines.append(R(bMid(3, 99, '  Full log bundle: nbpemreq / bpps')))
    lines.append(R(bMid(3, 99, '  Symptom timeline: when first occurred; any changes made')))
    lines.append(R(bMid(3, 99, '  Scope: single job / all jobs / all components — narrows root cause')))
    lines.append(R(bMid(3, 99, '  Error codes: exact error messages and exit codes from logs')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Master Server = central controller: scheduler, catalog, job manager, policy engine'))
    lines.append(txt_row('Media Server  = data mover between client and storage; can be co-located with master'))
    lines.append(txt_row('MSDP          = Media Server Deduplication Pool; inline variable-length block dedup'))
    lines.append(txt_row('Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot'))
    lines.append(txt_row('Policy        = defines what, when, and where to back up; contains schedules and clients'))
    lines.append(txt_row('Schedule      = full / differential-incremental / cumulative-incremental timing within policy'))
    lines.append(txt_row('Retention     = how long an image is kept; set per schedule, enforced by catalog expiry'))
    lines.append(txt_row('Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config'))
    lines.append(txt_row('NBU CA        = auto-issued certificate authority; signs host IDs for secure comms'))
    lines.append(txt_row('vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556'))
    lines.append(txt_row('bpdbjobs      = CLI to query job history: status, duration, exit code, errors'))
    lines.append(txt_row('bplist        = CLI to list available backup images for a client, policy, or date range'))
    lines.append(txt_row('KMS           = Key Management Service for encryption keys used in backup data encryption'))
    lines.append(txt_row('NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines


@kb_diagram(
    'dr-rasr',
    'docs/disaster-recovery/rasr/index.md',
    'Ransomware Air-gap Secure Recovery — isolated vault with CyberSense analytics',
)
def _dr_rasr_overview():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Overview'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RASR')))
    lines.append(R(bMid(3, 99, 'Ransomware Air-gap Secure Recovery — isolated vault with CyberSense analytics')))
    lines.append(R(bMid(3, 99, 'Vault Appliance      — air-gapped PowerStore/DD in isolated network segment')))
    lines.append(R(bMid(3, 99, 'CyberSense Engine    — ML-based malware and corruption detection on vault data')))
    lines.append(R(bMid(3, 99, 'PowerProtect Manager — orchestrates replication jobs, retention, and recovery')))
    lines.append(R(bMid(3, 99, 'Management: 443 (PPDM REST API) · Auth: Vault operator role; 2-person integrity for unlock')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Architecture: components work together to deliver RASR capabilities'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Architecture'), bMid(53, 99, 'Operations'))))
    lines.append(R(merge(bMid(3, 50, 'Vault Appliance      — air-gapped PowerStor'), bMid(53, 99, 'cr_vault_cli sync'))))
    lines.append(R(merge(bMid(3, 50, 'CyberSense Engine    — ML-based malware and'), bMid(53, 99, 'cr_vault_cli status'))))
    lines.append(R(merge(bMid(3, 50, 'PowerProtect Manager — orchestrates replica'), bMid(53, 99, 'cybersense scan'))))
    lines.append(R(merge(bMid(3, 50, 'Vault Lock           — immutable WORM lock '), bMid(53, 99, 'vault lock / unlock'))))
    lines.append(R(merge(bMid(3, 50, 'Clean Room           — isolated vCenter + w'), bMid(53, 99, 'ppdm recover vm'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-architecture',
    'docs/disaster-recovery/rasr/architecture/index.md',
    'RASR — architecture overview, components, data flow',
)
def _dr_rasr_architecture():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Architecture'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RASR — Component Architecture')))
    lines.append(R(bMid(3, 99, 'Vault Appliance      — air-gapped PowerStore/DD in isolated network segment')))
    lines.append(R(bMid(3, 99, 'CyberSense Engine    — ML-based malware and corruption detection on vault data')))
    lines.append(R(bMid(3, 99, 'PowerProtect Manager — orchestrates replication jobs, retention, and recovery')))
    lines.append(R(bMid(3, 99, 'Ports: 443 (PPDM REST API) · 2049 (NFS vault) · 9080 (CyberSense)')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Three-tier component model — control plane, data plane, and management'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Control Plane'), bMid(36, 66, 'Data Plane'), bMid(69, 99, 'Management'))))
    lines.append(R(merge(bMid(3, 33, 'Vault Appliance      — air-g'), bMid(36, 66, 'CyberSense Engine    — ML-ba'), bMid(69, 99, 'Vault Lock           — immut'))))
    lines.append(R(merge(bMid(3, 33, 'Scheduling'), bMid(36, 66, 'Replication/Backup'), bMid(69, 99, '443 (PPDM REST API)'))))
    lines.append(R(merge(bMid(3, 33, 'Policy mgmt'), bMid(36, 66, 'Data movement'), bMid(69, 99, 'REST API'))))
    lines.append(R(merge(bMid(3, 33, 'Catalog/DB'), bMid(36, 66, 'Dedup/compress'), bMid(69, 99, 'RBAC'))))
    lines.append(R(merge(bMid(3, 33, 'Job engine'), bMid(36, 66, '2049 (NFS vault)'), bMid(69, 99, 'Alerting'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-arch-how-it-works',
    'docs/disaster-recovery/rasr/architecture/how-it-works/index.md',
    'RASR — how replication or backup data flows step by step',
)
def _dr_rasr_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('  RASR data flow — from source to target through the protection pipeline:'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, '1  Source / Production System')))
    lines.append(R(bMid(3, 99, '   Vault Appliance      — air-gapped PowerStore/DD in isolated network segment')))
    lines.append(R(bMid(3, 99, '   Host writes are intercepted or snapshotted by the RASR agent/proxy')))
    lines.append(R(bMid(3, 99, '   Changed blocks tracked via CBT / journal / delta-set mechanism')))
    lines.append(R(bMid(3, 99, '   Consistency ensured at quiesce point before data transfer begins')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Changed data forwarded to the RASR engine — compression and encryption applied in transit'))
    lines.append(txt_row())
    lines.append(R(arrow([51])))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, '2  RASR Engine')))
    lines.append(R(bMid(3, 99, '   CyberSense Engine    — ML-based malware and corruption detection on vault data')))
    lines.append(R(bMid(3, 99, '   Data compressed, deduplicated, and encrypted before storage')))
    lines.append(R(bMid(3, 99, '   Metadata catalog updated; job status reported to control plane')))
    lines.append(R(bMid(3, 99, '   cr_vault_cli sync')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([51])))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, '3  Target / Repository')))
    lines.append(R(bMid(3, 99, '   PowerProtect Manager — orchestrates replication jobs, retention, and recovery')))
    lines.append(R(bMid(3, 99, '   Recovery point written; retention policy applied automatically')))
    lines.append(R(bMid(3, 99, '   Restore: cr_vault_cli status')))
    lines.append(R(bMid(3, 99, '   RTO driven by target storage performance and data volume')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-arch-design',
    'docs/disaster-recovery/rasr/architecture/design-standards/index.md',
    'RASR — sizing, design rules, capacity, HA guidelines',
)
def _dr_rasr_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Design Standards'))
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
    lines.append(txt_row('  Ports: 443 (PPDM REST API) · 2049 (NFS vault) · 9080 (CyberSense)'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Standard RASR Design Rules')))
    lines.append(R(bMid(3, 99, 'RPO target drives snapshot/cycle frequency — document in service design')))
    lines.append(R(bMid(3, 99, 'RTO target drives recovery tier: instant, warm standby, or cold restore')))
    lines.append(R(bMid(3, 99, 'Dedicated backup network VLAN — no shared production traffic')))
    lines.append(R(bMid(3, 99, 'Encryption enabled on all channels: AES-256 at rest on vault; TLS 1.3 for all management; vault lock enfor')))
    lines.append(R(bMid(3, 99, 'Service accounts: minimum privilege; rotate credentials quarterly')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-arch-integrations',
    'docs/disaster-recovery/rasr/architecture/integrations/index.md',
    'RASR — integration points with external systems and APIs',
)
def _dr_rasr_arch_integrations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Architecture Integrations'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RASR — External Integration Points')))
    lines.append(R(bMid(3, 99, 'Auth: Vault operator role; 2-person integrity for unlock; AD integration for PPDM UI')))
    lines.append(R(bMid(3, 99, 'Storage: connected via 443 (PPDM REST API) · 2049 (NFS vault)')))
    lines.append(R(bMid(3, 99, 'Monitoring: SNMP traps / syslog / REST API to ITSM and alerting systems')))
    lines.append(R(bMid(3, 99, 'Encryption: AES-256 at rest on vault; TLS 1.3 for all management; vault lock enforces immutability')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(arrow([26, 51, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 33), bTop(36, 66), bTop(69, 99))))
    lines.append(R(merge(bMid(3, 33, 'Identity'), bMid(36, 66, 'Storage'), bMid(69, 99, 'Monitoring'))))
    lines.append(R(merge(bMid(3, 33, 'AD / LDAP'), bMid(36, 66, '443 (PPDM REST API)'), bMid(69, 99, 'SNMP / syslog'))))
    lines.append(R(merge(bMid(3, 33, 'SAML SSO'), bMid(36, 66, '2049 (NFS vault)'), bMid(69, 99, 'REST webhook'))))
    lines.append(R(merge(bMid(3, 33, 'RBAC roles'), bMid(36, 66, 'NFS / iSCSI / FC'), bMid(69, 99, 'Email alerts'))))
    lines.append(R(merge(bMid(3, 33, 'MFA optional'), bMid(36, 66, 'Dedup appliance'), bMid(69, 99, 'ServiceNow'))))
    lines.append(R(merge(bMid(3, 33, 'Cert auth'), bMid(36, 66, 'Object storage'), bMid(69, 99, 'Prometheus'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-operations',
    'docs/disaster-recovery/rasr/operations/index.md',
    'RASR — operations overview, key tasks, day-to-day procedures',
)
def _dr_rasr_operations():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Operations'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RASR — Day-to-Day Operations')))
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
    lines.append(R(merge(bMid(3, 33, 'cr_vault_cli sync'), bMid(36, 66, 'cybersense scan'), bMid(69, 99, 'cr_vault_cli status'))))
    lines.append(R(merge(bMid(3, 33, 'Schedule jobs'), bMid(36, 66, 'Health checks'), bMid(69, 99, 'Instant restore'))))
    lines.append(R(merge(bMid(3, 33, 'Retention mgmt'), bMid(36, 66, 'Capacity alerts'), bMid(69, 99, 'Failover test'))))
    lines.append(R(merge(bMid(3, 33, 'Consistency grp'), bMid(36, 66, 'Log review'), bMid(69, 99, 'DR runbook'))))
    lines.append(R(merge(bMid(3, 33, 'Policy updates'), bMid(36, 66, 'SLA tracking'), bMid(69, 99, 'Validate RTO'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-ops-backup',
    'docs/disaster-recovery/rasr/operations/backup-restore/index.md',
    'RASR — backup and restore procedures',
)
def _dr_rasr_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Backup & Restore'))
    lines.append(txt_row())
    lines.append(txt_row('  Backup flow: quiesce source → snapshot/copy → transfer → write to target → catalog'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Backup (Protection)'), bMid(53, 99, 'Restore (Recovery)'))))
    lines.append(R(merge(bMid(3, 50, 'cr_vault_cli sync'), bMid(53, 99, 'cr_vault_cli status'))))
    lines.append(R(merge(bMid(3, 50, 'Quiesce source I/O'), bMid(53, 99, 'Select recovery point'))))
    lines.append(R(merge(bMid(3, 50, 'Take snapshot / CBT'), bMid(53, 99, 'Mount or copy to target'))))
    lines.append(R(merge(bMid(3, 50, 'Transfer changed blocks'), bMid(53, 99, 'Validate integrity'))))
    lines.append(R(merge(bMid(3, 50, 'Commit to repository'), bMid(53, 99, 'Restart application'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Key RASR Commands')))
    lines.append(R(bMid(3, 99, '  Backup trigger  : cr_vault_cli sync')))
    lines.append(R(bMid(3, 99, '  List points     : cr_vault_cli status')))
    lines.append(R(bMid(3, 99, '  Health status   : cybersense scan')))
    lines.append(R(bMid(3, 99, '  Retention mgmt  : ppdm recover vm')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-ops-cli',
    'docs/disaster-recovery/rasr/operations/cli-reference/index.md',
    'RASR — CLI commands reference',
)
def _dr_rasr_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — CLI Reference'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RASR — Command Reference')))
    lines.append(R(bMid(3, 99, 'Use these commands for routine operations, scripting, and troubleshooting')))
    lines.append(R(bMid(3, 99, '  cr_vault_cli sync')))
    lines.append(R(bMid(3, 99, '  cr_vault_cli status')))
    lines.append(R(bMid(3, 99, '  cybersense scan')))
    lines.append(R(bMid(3, 99, '  vault lock / unlock')))
    lines.append(R(bMid(3, 99, '  ppdm recover vm')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('  Ports: 443 (PPDM REST API) · 2049 (NFS vault) · 9080 (CyberSense)'))
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
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-ops-health',
    'docs/disaster-recovery/rasr/operations/health-checks/index.md',
    'RASR — health check procedures and monitoring commands',
)
def _dr_rasr_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Health Checks'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RASR — Health Check Procedures')))
    lines.append(R(bMid(3, 99, 'Run these checks daily/weekly to confirm protection is working')))
    lines.append(R(bMid(3, 99, '  cybersense scan')))
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
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-ops-install',
    'docs/disaster-recovery/rasr/operations/install-upgrade/index.md',
    'RASR — install and upgrade procedures',
)
def _dr_rasr_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Install & Upgrade'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RASR — Installation Prerequisites')))
    lines.append(R(bMid(3, 99, '  OS: supported Linux or Windows Server (see vendor compatibility matrix)')))
    lines.append(R(bMid(3, 99, '  Network: 443 (PPDM REST API) · 2049 (NFS vault) — ensure firewall allows these')))
    lines.append(R(bMid(3, 99, '  Auth: Vault operator role; 2-person integrity for unlock; AD integration for PPDM UI')))
    lines.append(R(bMid(3, 99, '  Storage: Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ES')))
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
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-ops-procedures',
    'docs/disaster-recovery/rasr/operations/procedures/index.md',
    'RASR — operational procedures and runbooks',
)
def _dr_rasr_ops_procedures():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Procedures'))
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
    lines.append(R(bMid(3, 99, 'Change Control Requirements for RASR')))
    lines.append(R(bMid(3, 99, '  All changes to protection policies require change ticket with rollback plan')))
    lines.append(R(bMid(3, 99, '  Failover tests must be scheduled in maintenance window')))
    lines.append(R(bMid(3, 99, '  Firmware/software upgrades need 48 h pre-approval and backup snapshot')))
    lines.append(R(bMid(3, 99, '  Post-change: verify jobs run successfully for 2 backup cycles')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-ops-scripts',
    'docs/disaster-recovery/rasr/operations/scripts/index.md',
    'RASR — automation scripts and examples',
)
def _dr_rasr_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Scripts'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RASR — Automation Scripts')))
    lines.append(R(bMid(3, 99, 'Scripts automate routine RASR operations — run via cron or CI/CD')))
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
    lines.append(R(merge(bMid(3, 50, 'cybersense scan'), bMid(53, 99, 'vault lock / unlock'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-security',
    'docs/disaster-recovery/rasr/security/index.md',
    'RASR — security overview, controls, compliance posture',
)
def _dr_rasr_security():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Security'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RASR — Security Posture')))
    lines.append(R(bMid(3, 99, 'Authentication: Vault operator role; 2-person integrity for unlock; AD integration for PPDM UI')))
    lines.append(R(bMid(3, 99, 'Encryption: AES-256 at rest on vault; TLS 1.3 for all management; vault lock enforces immutability')))
    lines.append(R(bMid(3, 99, 'Network: management VLAN separated; 9080 (CyberSense) management port')))
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
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-sec-access',
    'docs/disaster-recovery/rasr/security/access-control/index.md',
    'RASR — RBAC, permissions, service accounts',
)
def _dr_rasr_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Access Control'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RASR — RBAC and Access Control')))
    lines.append(R(bMid(3, 99, 'Auth: Vault operator role; 2-person integrity for unlock; AD integration for PPDM UI')))
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
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-sec-auth',
    'docs/disaster-recovery/rasr/security/authentication/index.md',
    'RASR — authentication methods, certificate management',
)
def _dr_rasr_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Authentication'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RASR — Authentication Methods')))
    lines.append(R(bMid(3, 99, 'Vault operator role; 2-person integrity for unlock; AD integration for PPDM UI')))
    lines.append(R(bMid(3, 99, 'Management UI: HTTPS on 443 (PPDM REST API) — browser-based login')))
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
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-sec-enc',
    'docs/disaster-recovery/rasr/security/encryption/index.md',
    'RASR — encryption at rest and in transit',
)
def _dr_rasr_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Encryption'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RASR — Encryption Configuration')))
    lines.append(R(bMid(3, 99, 'AES-256 at rest on vault; TLS 1.3 for all management; vault lock enforces immutability')))
    lines.append(R(bMid(3, 99, 'In-transit: TLS 1.2+ for all management; data channel also encrypted')))
    lines.append(R(bMid(3, 99, 'At-rest: AES-256 on repository or vault storage; key managed by KMS')))
    lines.append(R(bMid(3, 99, 'Key lifecycle: generate → use → rotate (annual) → retire → destroy')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'In-Transit'), bMid(53, 99, 'At-Rest'))))
    lines.append(R(merge(bMid(3, 50, 'TLS 1.2+ (minimum)'), bMid(53, 99, 'AES-256 encryption'))))
    lines.append(R(merge(bMid(3, 50, '443 (PPDM REST API) HTTPS'), bMid(53, 99, 'KMS key management'))))
    lines.append(R(merge(bMid(3, 50, 'Mutual TLS internal'), bMid(53, 99, 'WORM / immutable'))))
    lines.append(R(merge(bMid(3, 50, 'Cert rotation annual'), bMid(53, 99, 'Key rotation annual'))))
    lines.append(R(merge(bMid(3, 50, 'No plain-text admin'), bMid(53, 99, 'Audit key access'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-sec-hardening',
    'docs/disaster-recovery/rasr/security/hardening/index.md',
    'RASR — hardening guide, CIS controls, secure configuration',
)
def _dr_rasr_sec_hardening():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Hardening'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RASR — Hardening Checklist')))
    lines.append(R(bMid(3, 99, '  [ ] Disable default/admin accounts; create named admin accounts only')))
    lines.append(R(bMid(3, 99, '  [ ] Enable MFA for all interactive logins via IdP / SAML SSO')))
    lines.append(R(bMid(3, 99, '  [ ] Restrict management port (443 (PPDM REST API)) to jump host / management VLAN')))
    lines.append(R(bMid(3, 99, '  [ ] Enable audit logging and forward to SIEM (syslog, TLS port 6514)')))
    lines.append(R(bMid(3, 99, '  [ ] Apply all security patches within 30 days of vendor release')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Network Hardening')))
    lines.append(R(bMid(3, 99, '  [ ] Separate backup VLAN — no direct production host access to repo')))
    lines.append(R(bMid(3, 99, '  [ ] Firewall: allow only 443 (PPDM REST API) · 2049 (NFS vault) · 9080 (CyberSense)')))
    lines.append(R(bMid(3, 99, '  [ ] Disable unused ports and protocols on management interface')))
    lines.append(R(bMid(3, 99, '  [ ] Immutable repository: enable WORM or object lock on backup target')))
    lines.append(R(bMid(3, 99, '  [ ] Encryption in transit: disable TLS 1.0/1.1; enforce TLS 1.2+')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-troubleshooting',
    'docs/disaster-recovery/rasr/troubleshooting/index.md',
    'RASR — troubleshooting overview and triage approach',
)
def _dr_rasr_troubleshooting():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Troubleshooting'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RASR — Troubleshooting Approach')))
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
    lines.append(R(merge(bMid(3, 33, '443 (PPDM REST API)'), bMid(36, 66, 'Timeout errors'), bMid(69, 99, 'Restore test'))))
    lines.append(R(merge(bMid(3, 33, 'Firewall rules'), bMid(36, 66, 'Version compat'), bMid(69, 99, 'RPO drift'))))
    lines.append(R(merge(bBot(3, 33), bBot(36, 66), bBot(69, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-ts-issues',
    'docs/disaster-recovery/rasr/troubleshooting/common-issues/index.md',
    'RASR — common issues, root causes, and fixes',
)
def _dr_rasr_ts_issues():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Common Issues'))
    lines.append(txt_row())
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Symptom', 'Likely Cause', 'First Check', 'Fix', 'Verify'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Sync failed', 'vault unreachable', 'check airgap swit', 'verify VLAN path', 'ping vault mgm'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Lock error', 'vault already loc', 'cr_vault_cli stat', 'force unlock+relo', 'vault logs'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['CyberSense hang', 'scan job stalled', 'cs_diag collect', 'restart cs servic', 'cs_status'])))
    lines.append(R(sections(3, 99, [22, 41, 61, 80],
        ['Restore fail', 'clean room nic er', 'check clean-room ', 're-map portgroup', 'vmnic check'])))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'General Triage Pattern')))
    lines.append(R(bMid(3, 99, '  Is the issue new or recurring? New = recent change; Recurring = config problem')))
    lines.append(R(bMid(3, 99, '  Is it isolated to one source or all? Isolated = agent; All = server/repo')))
    lines.append(R(bMid(3, 99, '  Check logs first: cybersense scan')))
    lines.append(R(bMid(3, 99, '  If unresolved in 2h: open vendor case with full log bundle')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-ts-diag',
    'docs/disaster-recovery/rasr/troubleshooting/diagnostics/index.md',
    'RASR — diagnostic commands and log collection',
)
def _dr_rasr_ts_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Diagnostics'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RASR — Diagnostic Commands')))
    lines.append(R(bMid(3, 99, 'Collect these before opening a vendor support case')))
    lines.append(R(bMid(3, 99, '  cybersense scan')))
    lines.append(R(bMid(3, 99, '  vault lock / unlock')))
    lines.append(R(bMid(3, 99, '  Check system logs: /var/log/ or Windows Event Viewer')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(merge(bTop(3, 50), bTop(53, 99))))
    lines.append(R(merge(bMid(3, 50, 'Log Collection'), bMid(53, 99, 'Live Diagnostics'))))
    lines.append(R(merge(bMid(3, 50, 'Application log bundle'), bMid(53, 99, 'Network connectivity'))))
    lines.append(R(merge(bMid(3, 50, 'OS syslog (journalctl)'), bMid(53, 99, 'Storage path check'))))
    lines.append(R(merge(bMid(3, 50, 'Core dump if crashed'), bMid(53, 99, 'Process list check'))))
    lines.append(R(merge(bMid(3, 50, 'Config export/backup'), bMid(53, 99, 'Port reachability'))))
    lines.append(R(merge(bMid(3, 50, 'cybersense scan'), bMid(53, 99, 'vault lock / unlock'))))
    lines.append(R(merge(bBot(3, 50), bBot(53, 99))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines

@kb_diagram(
    'dr-rasr-ts-escalation',
    'docs/disaster-recovery/rasr/troubleshooting/escalation/index.md',
    'RASR — escalation path, vendor support, and SLA',
)
def _dr_rasr_ts_escalation():
    W2 = 103
    R, txt_row = make_helpers(W2)
    lines = []
    lines.append(title_border(W2, 'RASR — Escalation'))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'RASR — Escalation Path')))
    lines.append(R(bMid(3, 99, 'L1 Triage: review logs, match to known issues in runbook (0–30 min)')))
    lines.append(R(bMid(3, 99, 'L2 Engineering: deep analysis, config review, lab reproduction (30 min – 4 h)')))
    lines.append(R(bMid(3, 99, 'Vendor Support: open case with log bundle if unresolved at L2 (> 4 h)')))
    lines.append(R(bMid(3, 99, 'Sev1 (data loss / production impact): page on-call + open critical case')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(R(bTop(3, 99)))
    lines.append(R(bMid(3, 99, 'Information to Collect Before Escalating')))
    lines.append(R(bMid(3, 99, '  Product version: RASR version string from About / version command')))
    lines.append(R(bMid(3, 99, '  Full log bundle: cybersense scan')))
    lines.append(R(bMid(3, 99, '  Symptom timeline: when first occurred; any changes made')))
    lines.append(R(bMid(3, 99, '  Scope: single job / all jobs / all components — narrows root cause')))
    lines.append(R(bMid(3, 99, '  Error codes: exact error messages and exit codes from logs')))
    lines.append(R(bBot(3, 99)))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure:'))
    lines.append(txt_row('Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts'))
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest'))
    lines.append(txt_row('Vault         = isolated, air-gapped storage appliance receiving periodic replication copies'))
    lines.append(txt_row('Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies'))
    lines.append(txt_row('CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures'))
    lines.append(txt_row('PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery'))
    lines.append(txt_row('Air Gap       = physical or logical network isolation preventing attacker lateral movement to '))
    lines.append(txt_row('Delta Set     = incremental changed blocks replicated from production to vault each cycle'))
    lines.append(txt_row('Clean Room    = isolated recovery environment: separate vCenter, network, and workstations'))
    lines.append(txt_row('Recovery Point= specific vault snapshot timestamp from which clean recovery is performed'))
    lines.append(txt_row('Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac'))
    lines.append(txt_row('Journal       = write-order-consistent journal on vault enabling point-in-time recovery'))
    lines.append(txt_row('Scan Report   = CyberSense output: clean/suspect classification per file and block'))
    lines.append(txt_row('Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept'))
    lines.append(txt_row('RTO           = Recovery Time Objective; time from failover decision to restored service'))
    lines.append(txt_row())
    lines.append('\u2514' + '\u2500' * W2 + '\u2518')
    return lines