# Commvault

<div class="kb-summary">
Commvault enterprise backup and recovery — CommServe command and control, MediaAgent data movement with deduplication, and multi-site storage library management.
</div>

```
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
