# Dell Storage

<div class="kb-summary">
Dell enterprise storage portfolio — block, file, object, and data protection platforms. Coverage includes architecture, provisioning, multipathing, replication, and operational procedures for each product.
</div>

```text
┌─────────────────────────────────────── Dell Storage Portfolio ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                    Dell Storage Management                                    │   │
│   │            Unisphere: unified web UI for PowerMax, PowerStore, and Unity management           │   │
│   │      CloudIQ: cloud analytics, health scoring, capacity forecasting, and proactive alerts     │   │
│   │         InsightIQ: performance analytics and capacity management for PowerScale/OneFS         │   │
│   │              REST API: programmatic management across all Dell storage platforms              │   │
│   │        Dell AIOps: AI-driven recommendations and anomaly detection across the portfolio       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Unisphere and CloudIQ manage arrays via REST APIs — on-prem UI or cloud analytics portal           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Dell PowerMax        │  │       Dell PowerStore       │  │        Dell Unity XT        │   │
│   │  Enterprise all-flash block │  │ Mid-range all-flash unified │  │  Mid-range unified storage  │   │
│   │     FC · iSCSI · NVMe/FC    │  │ Block + file in one platform│  │ Block · file · VMware ready │   │
│   │   SRDF: sync + async repl   │  │ AppsON: containers on-array │  │    FC · iSCSI · NFS · SMB   │   │
│   │ TimeFinder: local snapshots │  │ Intelligent automation + ML │  │  Async replication + snaps  │   │
│   │  NVMe end-to-end, up to 4PB │  │   NVMe-based storage nodes  │  │   VAAI/VASA VMware support  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Block arrays expose LUNs to hosts via FC, iSCSI, or NVMe; file via NFS and SMB                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Dell PowerScale       │  │       Dell Data Domain      │  │           Dell ECS          │   │
│   │   Scale-out NAS, OneFS OS   │  │  Purpose-built backup dedup │  │  Enterprise object storage  │   │
│   │    NFS · SMB · HDFS · S3    │  │ DD Boost: client-side dedup │  │   S3 · Swift · Atmos APIs   │   │
│   │   SmartQuotas: quota mgmt   │  │  DD Replicator: remote copy │  │   Geo-distribution + WORM   │   │
│   │  SyncIQ: async replication  │  │  WORM: compliance retention │  │Erasure coding for durability│   │
│   │   Up to 100PB per cluster   │  │Cloud Tier: long-term archive│  │   Petabyte-scale capacity   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    VPLEX: storage federation and active-active data mobility across arrays and sites                  │
│    PowerPath: host multipathing software; automatic path failover and load balancing                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Fibre Channel   │      iSCSI       │        NFS        │    SMB / CIFS    │   S3 / Object    │   │
│   │ SAN block access │ IP block access  │  Unix file mounts │  Windows shares  │REST object store │   │
│   │ 16G · 32G · 64G  │  TCP/IP · iSNS   │   NFS v3 · v4.1   │   CIFS · DFS-N   │HTTP · REST · SDK │   │
│   │ HBA → SAN switch │ iSCSI initiator  │    Mount via IP   │   SMB sessions   │Buckets + prefixes│   │
│   │ Zoning + masking │ CHAP auth · iSNS │  Export policies  │ Share perms+ACL  │  Policies + IAM  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  NVMe/SSD/NL-SAS drives · FC HBAs · 10/25/100 GbE NICs · SAN switches · Power & Cooling               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  PowerMax     = Dell high-end all-flash block array; NVMe end-to-end, up to 4PB usable capacity       │
│  PowerStore   = Dell mid-range unified array; block + file, AppsON containers, intelligent automation │
│  Unity XT     = Dell mid-range unified array; block, file, and deep VMware integration                │
│  PowerScale   = Dell scale-out NAS running OneFS; supports NFS, SMB, HDFS, S3; scales to 100PB        │
│  Data Domain  = Dell purpose-built backup appliance; DD Boost dedup, replication, cloud tier          │
│  ECS          = Dell Enterprise Content Storage; S3-compatible object with geo-distribution and WORM  │
│  VPLEX        = Dell storage federation; active-active data mobility across arrays and sites          │
│  PowerPath    = Dell host multipathing software; automatic path failover and load balancing           │
│  SRDF         = Symmetrix Remote Data Facility; sync or async replication between PowerMax arrays     │
│  TimeFinder   = Dell local snapshot technology for PowerMax; point-in-time copies of volumes          │
│  DD Boost     = Data Domain client-side dedup library; reduces data sent to the backup target         │
│  OneFS        = PowerScale distributed file system OS; spans all nodes as a single namespace          │
│  SyncIQ       = PowerScale async replication engine; policy-based replication to DR site              │
│  SmartQuotas  = PowerScale quota management; enforces hard/soft limits per directory or user          │
│  AppsON       = PowerStore capability to run VMs and containers directly on the storage array         │
│  CloudIQ      = Dell cloud analytics SaaS; health scoring, capacity forecasting, proactive alerts     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="powermax/"><strong>PowerMax</strong><span>High-end all-flash array — SRDF replication, NVMe, multicloud, and enterprise performance.</span></a>
<a class="kb-card" href="powerscale/"><strong>PowerScale</strong><span>Scale-out NAS — OneFS, SmartQuotas, SyncIQ, and multi-protocol file services.</span></a>
<a class="kb-card" href="powerstore/"><strong>PowerStore</strong><span>Mid-range all-flash — unified block and file with AppsON and intelligent automation.</span></a>
<a class="kb-card" href="unity/"><strong>Unity XT</strong><span>Unified storage — block, file, and VMware integration for mid-range workloads.</span></a>
<a class="kb-card" href="vplex/"><strong>VPLEX</strong><span>Storage federation and active-active data mobility across arrays and sites.</span></a>
<a class="kb-card" href="data-domain/"><strong>Data Domain</strong><span>Purpose-built backup appliance — deduplication, replication, and long-term retention.</span></a>
<a class="kb-card" href="ecs/"><strong>ECS</strong><span>Object storage platform — S3-compatible, geo-distribution, and compliance retention.</span></a>
<a class="kb-card" href="powerpath/"><strong>PowerPath</strong><span>Multipathing software — path management, load balancing, and failover for Dell arrays.</span></a>
<a class="kb-card" href="apex-storage-as-a-service/"><strong>Apex STaaS</strong><span>Storage as a Service — Dell-owned hardware on-premises, consumed and billed as a cloud service.</span></a>
<a class="kb-card" href="cloudiq/"><strong>CloudIQ</strong><span>SaaS AIOps platform — health scoring, capacity forecasting, and proactive analytics via SCG.</span></a>
<a class="kb-card" href="cod/"><strong>Capacity on Demand</strong><span>Pre-installed capacity unlocked via license key — no downtime expansion for Dell arrays.</span></a>
<a class="kb-card" href="fod/"><strong>Features on Demand</strong><span>Software feature licensing — protocols, replication, snapshots, and encryption unlocked via key.</span></a>
<a class="kb-card" href="secure-connect-gateway/"><strong>Secure Connect Gateway</strong><span>Phone-home proxy — relays telemetry from on-prem arrays to Dell Support and CloudIQ.</span></a>
</div>
