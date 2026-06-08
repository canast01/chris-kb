# NetApp Storage

<div class="kb-summary">
NetApp storage knowledge base covering ONTAP, SnapMirror, SnapCenter, and Keystone. Includes architecture references, operational procedures, CLI commands, replication, SnapMirror Active Sync, MetroCluster, and troubleshooting guides.
</div>

```text
┌──────────────────────────────────────── NetApp Storage Stack ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                       NetApp Management                                       │   │
│   │           ONTAP System Manager: browser-based admin UI for volumes, LUNs, and quotas          │   │
│   │       ActiveIQ: cloud analytics — health scoring, capacity forecasting, proactive alerts      │   │
│   │         REST API: programmatic management across AFF, FAS, Cloud Volumes, StorageGRID         │   │
│   │         ONTAP CLI: SSH-based command-line management for volumes, aggregates, and SVMs        │   │
│   │       BlueXP: unified multi-cloud management — on-prem and cloud ONTAP from one console       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    ONTAP System Manager and BlueXP manage arrays via REST APIs                                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         NetApp ONTAP        │  │      NetApp StorageGRID     │  │       NetApp Keystone       │   │
│   │   AFF · FAS · ONTAP Select  │  │  Enterprise object storage  │  │     Storage-as-a-service    │   │
│   │  Unified block + file + S3  │  │   S3 · Swift · NFS · HDFS   │  │ NetApp-owned HW on-premises │   │
│   │    FC · iSCSI · NFS · SMB   │  │  WORM: compliance retention │  │ Billed by consumption (TiB) │   │
│   │  MetroCluster: sync stretch │  │Erasure coding for durability│  │  SLA-guaranteed performance │   │
│   │ Cloud Volumes ONTAP: AWS/GCP│  │   Petabyte-scale capacity   │  │  Flex burst above committed │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    ONTAP serves block and file workloads · StorageGRID serves object workloads at scale               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          SnapMirror         │  │          SnapCenter         │  │          FabricPool         │   │
│   │   Async + sync replication  │  │   Application-aware backup  │  │    Auto cold-data tiering   │   │
│   │    DR + data distribution   │  │ SQL · Oracle · SAP · VMware │  │  Tier to S3 or cloud object │   │
│   │   ONTAP to ONTAP or cloud   │  │ Consistent snapshot + clone │  │   Reduce on-prem footprint  │   │
│   │      Active Sync: RPO=0     │  │   Restore to alt. location  │  │    Policy-based temp scan   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Data services protect, replicate, and optimise capacity across all ONTAP platforms                 │
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
│  NVMe/SSD/HDD drives · FC HBAs · 10/25/100 GbE NICs · SAN switches · Power & Cooling                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ONTAP        = NetApp unified storage OS; runs on AFF, FAS, Cloud Volumes, and ONTAP Select          │
│  AFF          = All-Flash FAS; NetApp all-NVMe/SSD arrays optimised for performance workloads         │
│  FAS          = Fabric-Attached Storage; NetApp hybrid arrays with HDD and SSD capacity tiers         │
│  SVM          = Storage Virtual Machine; logical ONTAP partition with its own namespace and protocols │
│  SnapMirror   = NetApp replication engine; async or sync volume copies between ONTAP systems          │
│  SnapCenter   = Application-consistent backup tool; integrates with SQL, Oracle, SAP, and VMware      │
│  FabricPool   = ONTAP auto-tiering; moves cold data blocks to S3-compatible object storage            │
│  StorageGRID  = NetApp object store; S3/Swift APIs, WORM compliance, petabyte geo-distribution        │
│  Keystone     = NetApp STaaS; NetApp-owned hardware on-prem, billed by consumption per TiB            │
│  ActiveIQ     = NetApp SaaS analytics; predictive health, capacity forecasting, proactive support     │
│  MetroCluster = ONTAP sync stretch cluster; RPO=0 across two sites with transparent failover          │
│  Active Sync  = SnapMirror Active Sync; granular sync replication for persistent LUN access           │
│  FlexVol      = ONTAP flexible volume; dynamically grows or shrinks within a storage aggregate        │
│  FlexGroup    = ONTAP distributed volume; scales to petabytes across multiple cluster nodes           │
│  BlueXP       = NetApp unified console; manages on-prem and cloud ONTAP from one SaaS portal          │
│  SnapVault    = Policy-based snapshot replication to a secondary system for backup retention          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


```text
┌───────────────────────────── NetApp ONTAP — Cluster Deployment Sequence ──────────────────────────────┐
│                                                                                                       │
│  Step 1 · Physical Readiness                                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Rack nodes  ·  cable cluster interconnect (100 GbE HA and cluster ports)                             │
│  Expansion shelves: SAS/NVMe cabling per shelf cabling guide  ·  shelf IDs unique                     │
│  Management network: e0M management port  ·  e0a/b data ports connected to switches                   │
│  DNS A+PTR records for cluster management LIF and all node management LIFs                            │
│  NTP servers reachable  ·  NetApp licence keys (base + feature) obtained                              │
│                                                                                                       │
│                                        │  run cluster setup wizard                                    │
│                                        ▼                                                              │
│  Step 2 · Cluster Initialisation                                                                      │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Boot first node  ·  run cluster setup at console: cluster create -clustername                        │
│  Set cluster management LIF IP  ·  set admin password  ·  accept EULA                                 │
│  Join additional nodes: cluster setup on each  ·  set node management LIF                             │
│  Verify: cluster show  ·  cluster ring show  ·  storage failover show HA status                       │
│  Apply licences: system licence add -licence-code <keys>  ·  confirm all features                     │
│                                                                                                       │
│                                        │  create aggregates and SVMs                                  │
│                                        ▼                                                              │
│  Step 3 · Aggregates & SVMs                                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create aggregate: aggr create -aggregate <name> -diskcount <n> -raidtype raid_dp                     │
│  Create SVM: vserver create -vserver <name> -rootvolume <vol> -language C.UTF-8                       │
│  Configure SVM protocols: nfs enable  ·  cifs setup (join AD)  ·  iscsi start                         │
│  Assign LIFs to SVM: network interface create per protocol per node (NFS, iSCSI, FC)                  │
│  Set LIF failover policy  ·  verify LIF placement with network interface show                         │
│                                                                                                       │
│                                        │  provision volumes and LUNs                                  │
│                                        ▼                                                              │
│  Step 4 · Volumes & LUNs                                                                              │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create volume: vol create -vserver <svm> -volume <vol> -aggregate <aggr> -size <n>                   │
│  NFS: export-policy create  ·  set export rule  ·  mount NFS share from client                        │
│  iSCSI/FC: lun create  ·  igroup create  ·  lun map -igroup  ·  rescan from host                      │
│  SMB/CIFS: vserver cifs share create  ·  set permissions  ·  test from Windows client                 │
│  Set volume efficiency: dedup enable  ·  compression enable  ·  verify savings                        │
│                                                                                                       │
│                                        │  configure SnapMirror replication                            │
│                                        ▼                                                              │
│  Step 5 · SnapMirror & SnapVault                                                                      │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Peer clusters: cluster peer create  ·  SVM peer: vserver peer create                                 │
│  Create SnapMirror relationship: snapmirror create -type DP (async) or SM (sync)                      │
│  Initialise: snapmirror initialize  ·  monitor transfer with snapmirror show                          │
│  Create vault relationship for long-term retention  ·  set schedule and retention                     │
│  Test failover: snapmirror quiesce  ·  snapmirror break  ·  test DR SVM  ·  resync                    │
│                                                                                                       │
│                                        │  deploy SnapCenter                                           │
│                                        ▼                                                              │
│  Step 6 · SnapCenter                                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Install SnapCenter Server on Windows  ·  point to SQL instance  ·  configure HTTPS                   │
│  Add storage systems: Settings → Storage Systems → Add ONTAP cluster credentials                      │
│  Install SnapCenter plug-ins on application hosts (Windows File, SQL, Oracle, VMware)                 │
│  Create policies: snapshot frequency, retention, replication schedule                                 │
│  Create resource groups  ·  assign policy  ·  run first backup  ·  test restore                       │
│  Configure SnapCenter RBAC  ·  integrate with email/SIEM alerting                                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="deploy/"><strong>Deploy</strong><span>ONTAP cluster deployment, SVM configuration, and initial provisioning procedures.</span></a>
<a class="kb-card" href="operations/"><strong>Operations</strong><span>Daily health checks, capacity management, alert triage, and operational procedures.</span></a>
<a class="kb-card" href="ontap/"><strong>ONTAP</strong><span>NetApp data management OS — NAS, SAN, S3, SnapMirror Active Sync, and MetroCluster.</span></a>
<a class="kb-card" href="snapmirror/"><strong>SnapMirror</strong><span>Asynchronous and synchronous data replication for DR and data distribution.</span></a>
<a class="kb-card" href="snapcenter/"><strong>SnapCenter</strong><span>Application-consistent backup, restore, and clone management for NetApp storage.</span></a>
<a class="kb-card" href="keystone/"><strong>Keystone</strong><span>Storage-as-a-service — consumption-based NetApp infrastructure with SLA guarantees.</span></a>
<a class="kb-card" href="insightiq/"><strong>InsightIQ</strong><span>Performance analytics and capacity management appliance for PowerScale clusters.</span></a>
<a class="kb-card" href="superna-eyeglass/"><strong>Superna Eyeglass</strong><span>DR orchestration for PowerScale — SyncIQ failover automation and ransomware protection.</span></a>
</div>
