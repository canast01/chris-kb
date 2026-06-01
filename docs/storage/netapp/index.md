# NetApp Storage

<div class="kb-summary">
NetApp storage knowledge base covering ONTAP, SnapMirror, SnapCenter, and Keystone. Includes architecture references, operational procedures, CLI commands, replication, SnapMirror Active Sync, MetroCluster, and troubleshooting guides.
</div>

```
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

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="ontap/"><strong>ONTAP</strong><span>NetApp data management OS — NAS, SAN, S3, SnapMirror Active Sync, and MetroCluster.</span></a>
<a class="kb-card" href="snapmirror/"><strong>SnapMirror</strong><span>Asynchronous and synchronous data replication for DR and data distribution.</span></a>
<a class="kb-card" href="snapcenter/"><strong>SnapCenter</strong><span>Application-consistent backup, restore, and clone management for NetApp storage.</span></a>
<a class="kb-card" href="keystone/"><strong>Keystone</strong><span>Storage-as-a-service — consumption-based NetApp infrastructure with SLA guarantees.</span></a>
</div>
