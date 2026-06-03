# Commvault

<div class="kb-summary">
Commvault enterprise backup and recovery — CommServe command and control, MediaAgent data movement with deduplication, and multi-site storage library management.
</div>

```text
┌────────────────────────── Commvault — Enterprise Backup and Data Management ──────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                       Commvault Platform                                      │   │
│   │      Enterprise-grade backup, recovery, archiving, and compliance for hybrid environments     │   │
│   │          Core components: CommServe (scheduler+DB), MediaAgent (data mover), Clients          │   │
│   │           Interfaces: CommCell Console (Java GUI), Command Center (web UI), REST API          │   │
│   │            Deployment: on-premises, cloud (Azure/AWS/GCP), or Commvault Cloud SaaS            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Platform decomposes into control plane (CommServe), data plane (MediaAgents), and sources (Clients)│
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               CommServe Server               │  │                  MediaAgent                 │   │
│   │    Central scheduler and catalog database    │  │    Data movement and deduplication engine   │   │
│   │      SQL Server backend for CommCell DB      │  │  DDB (Deduplication Database) on local disk │   │
│   │      Manages jobs, alerts, and policies      │  │   Writes to disk libraries, tape, or cloud  │   │
│   │     Port 8400 (client comms), 8401 (GUI)     │  │     Port 8403 (data tunnel), NDMP 10000     │   │
│   │     Active/passive HA with DR CommServe      │  │     Scale-out: multiple MAs per CommCell    │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    CommServe orchestrates; MediaAgents move data; Clients are the backup sources                      │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Clients        │        Storage        │       Automation      │       Reporting       │   │
│   │  File · VM · DB · App │  Disk · Tape · Cloud  │     CLI · REST API    │     Command Center    │   │
│   │  iDA agents installed │    Storage policies   │   qoperation / qlist  │    Dashboards & SLA   │   │
│   │Exchange · Oracle · SAP│   WORM / compliance   │   Workflows & alerts  │   Audit & compliance  │   │
│   │ Subclients per source │  Dedup + compression  │  Ansible integration  │   Chargeback reports  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  CommServe: 2-socket rack server · 32+ GB RAM · SQL Server storage on SSD RAID-10                     │
│  MediaAgent: high-throughput NIC (10/25 GbE) · FC HBA for tape · fast local DDB SSD                   │
│  Network: dedicated backup VLAN · 10 GbE client-to-MA links · out-of-band iDRAC/iLO                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CommServe      = Central control server; holds CommCell DB (SQL Server) and job scheduler            │
│  MediaAgent     = Data movement engine; reads from clients, writes to storage targets                 │
│  CommCell       = The entire Commvault deployment: CS + all MAs + all Clients                         │
│  iDA            = Intelligent Data Agent installed on each client to protect workloads                │
│  Subclient      = Logical grouping of data within a client (defines what to back up)                  │
│  Storage Policy = Rules binding subclients to storage libraries (copies, retention, dedup)            │
│  DDB            = Deduplication Database; stores fingerprints for block-level dedup                   │
│  IntelliSnap    = Hardware snapshot integration (SAN/NAS arrays) for near-zero-RPO                    │
│  CSDB           = CommServe Database; SQL Server instance holding CommCell metadata                   │
│  Command Center = Modern web UI replacing legacy CommCell Console (port 443)                          │
│  qoperation     = CLI tool for submitting backup/restore/admin operations from shell                  │
│  CommCell DR    = Disaster recovery copy of the CommServe for failover continuity                     │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


```text
┌────────────────────────────────── Commvault — Installation Sequence ──────────────────────────────────┐
│                                                                                                       │
│  Step 1 · Prerequisites                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Windows Server 2019/2022  ·  16 vCPU  ·  64 GB RAM  ·  SQL Server 2019+ for CommServe DB             │
│  Separate Windows or Linux MediaAgent nodes  ·  10 GbE data path to storage                           │
│  TCP 8400/8401 (client comms)  ·  443 (Command Center)  ·  service account in domain                  │
│  DNS resolution for all CommServe, MediaAgent, and client FQDNs  ·  NTP synced                        │
│  Commvault licence file (.lic) obtained from support portal before install                            │
│                                                                                                       │
│                                        │  install CommServe                                           │
│                                        ▼                                                              │
│  Step 2 · CommServe                                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Run Commvault installer on Windows  ·  select CommServe role  ·  point to SQL instance               │
│  Activate licence  ·  login to Command Center at https://<hostname>/commandcenter                     │
│  Configure CommCell: time zone, email SMTP, security settings, audit log                              │
│  Add CommServe DR backup destination  ·  enable automatic disaster recovery export                    │
│  Verify CommServe DB size and SQL maintenance jobs  ·  set SQL backup schedule                        │
│                                                                                                       │
│                                        │  add MediaAgent nodes                                        │
│                                        ▼                                                              │
│  Step 3 · MediaAgents                                                                                 │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Run installer on each MA host  ·  select MediaAgent role  ·  register to CommServe                   │
│  Configure index cache path (fast local SSD)  ·  set working directory                                │
│  Enable deduplication database (DDB) on each MA  ·  assign DDB to a dedicated disk                    │
│  Verify MA appears Online in CommCell Console under Storage → MediaAgents                             │
│  Test data path: run a small backup job routing through each new MA                                   │
│                                                                                                       │
│                                        │  configure storage libraries                                 │
│                                        ▼                                                              │
│  Step 4 · Storage Libraries                                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Add disk library: local path, NFS/CIFS share, or cloud storage (S3/Azure/GCP)                        │
│  Create storage policy: select MA, assign library, set retention rules (days + cycles)                │
│  Enable WORM/immutability on cloud or disk library for ransomware protection                          │
│  Create global dedup storage policy for large environments to share DDB across MAs                    │
│  Verify library free space  ·  configure alert at 80% full                                            │
│                                                                                                       │
│                                        │  add clients and proxies                                     │
│                                        ▼                                                              │
│  Step 5 · Clients & Proxies                                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Add clients via Command Center → Add Server  ·  push Commvault agent or run locally                  │
│  Add virtualization proxy: vCenter access node  ·  IntelliSnap proxy for array snaps                  │
│  Install File System agent on Windows/Linux  ·  add Exchange/SQL/Oracle agents as needed              │
│  Verify client appears Online  ·  run discovery to populate content (VMs, DB instances)               │
│                                                                                                       │
│                                        │  create plans and schedules                                  │
│                                        ▼                                                              │
│  Step 6 · Plans & Schedules                                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create server backup plan: storage policy, RPO schedule, retention, encryption toggle                │
│  Assign plan to client groups  ·  override per-client if granular retention needed                    │
│  Enable SLA compliance view  ·  set alert for missed SLA                                              │
│  Run first full backup  ·  verify job completes  ·  test restore from Command Center                  │
│  Schedule reports: capacity, compliance, and missed-backup summary to operations team                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>CommServe topology, MediaAgent dedup, storage library types, multi-site design, and port requirements.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
