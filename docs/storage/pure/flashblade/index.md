# Pure FlashBlade

<div class="kb-summary">
Unified fast file and object storage running Purity//FB — NFS, SMB, S3, and HDFS from a single scale-out platform. Architecture, operations, security, and troubleshooting for AI/ML, analytics, backup, and unstructured data workloads.
</div>

```text
┌──────────────────────────────────────── Pure FlashBlade Stack ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              Pure FlashBlade — Unified Fast File and Object Storage (Purity//FB)              │   │
│   │      Scale-out blade architecture: blade modules add capacity + performance; no hot spots     │   │
│   │        Protocols: NFS v3/v4.1 · SMB 2/3 · S3 API · HDFS — unified from single platform        │   │
│   │     Use cases: AI/ML training data, analytics, backup targets, unstructured data at scale     │   │
│   │      Replication: asynchronous object and file replication to another FlashBlade or cloud     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    FlashBlade management spans blade hardware, protocol services, operations, and security            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │   Blade modules: F-series   │  │    purefb CLI + REST API    │  │     RBAC: roles + tokens    │   │
│   │     Chassis: 4–15 blades    │  │   File system + bucket ops  │  │    Data-at-rest: AES-256    │   │
│   │   NFS exports + SMB shares  │  │   Snapshots: dir + object   │  │   Network: subnet policies  │   │
│   │  S3 buckets + IAM policies  │  │ Capacity: blades + forecast │  │      Audit log + syslog     │   │
│   │   Replication: async FB→FB  │  │    Health: blade, network   │  │ Directory services: AD/LDAP │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture defines scale-out layout · Operations manage shares and buckets                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │  NFS mount fail  │   purefb list    │  Blade health OK  │  Case: array SN  │    purefb get    │   │
│   │ S3 auth failure  │ purelog download │   Network: ports  │  Log bundle req  │  purefb fs list  │   │
│   │   Repl lag: BW   │ purebuddy check  │  Capacity: >80%?  │  Remote assist   │ purefb bucket ls │   │
│   │ SMB slow writes  │ netconfig verify │   Repl state: OK  │  P1/P2 severity  │ purefb snap list │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  FlashBlade chassis · F-series blade modules · 10/25/100 GbE NICs · Ethernet switches                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Purity//FB   = FlashBlade operating system; manages file, object, and HDFS data services             │
│  F-series     = FlashBlade blade module type; NVMe-based, each adds capacity and throughput           │
│  NFS          = Network File System; file protocol used by Linux/Unix clients; v3 and v4.1 supported  │
│  SMB          = Server Message Block; Windows file sharing protocol; SMB 2.0 and 3.0 on FlashBlade    │
│  S3           = AWS-compatible object storage API; FlashBlade implements S3 bucket/object model       │
│  HDFS         = Hadoop Distributed File System API; FlashBlade serves as HDFS-compatible target       │
│  purefb       = FlashBlade CLI entry point; purefb fs/bucket/snap/hw commands for management          │
│  Scale-out    = Adding blades increases both capacity and performance simultaneously (no hot spots)   │
│  Replication  = Async file/object replication to another FlashBlade or object store; RPO-based        │
│  Subnet policy= Network access rules bound to FlashBlade interfaces for NFS, SMB, S3, replication     │
│  RBAC         = Role-Based Access Control; Array Admin, Storage Admin, Read-Only roles on FlashBlade  │
│  Pure1        = Cloud management portal; monitors all FlashBlade arrays; capacity and health analytics│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
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
