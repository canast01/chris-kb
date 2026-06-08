# Storage

<div class="kb-summary">
Block, file, and object storage platforms used across enterprise infrastructure — Dell PowerMax, PowerScale, PowerStore, Unity, VPLEX, Data Domain, and ECS; Pure Storage FlashArray and FlashBlade; NetApp ONTAP; and Ceph distributed storage. Coverage includes architecture, configuration, performance tuning, multipathing, and troubleshooting.
</div>

```text
┌──────────────────────────────────── Enterprise Storage Landscape ─────────────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Pure1            │  │     Unisphere / CloudIQ     │  │     ONTAP System Manager    │   │
│   │      Cloud mgmt portal      │  │  Unisphere: array admin UI  │  │    Browser-based admin UI   │   │
│   │   FlashArray & FlashBlade   │  │   CloudIQ: cloud analytics  │  │   Volume, LUN & quota mgmt  │   │
│   │    Capacity & performance   │  │  Health scoring & forecast  │  │  ActiveIQ: cloud analytics  │   │
│   │   Proactive support alerts  │  │    REST API & automation    │  │  Proactive health alerting  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Management planes connect to arrays via HTTPS / REST APIs                                          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Pure FlashArray       │  │     Dell PowerMax / VMAX    │  │         NetApp ONTAP        │   │
│   │   All-flash block storage   │  │    Mission-critical block   │  │     Unified block + file    │   │
│   │     FC · iSCSI · NVMe-oF    │  │     FC · iSCSI · NVMe/FC    │  │    FC · iSCSI · NFS · SMB   │   │
│   │    Always-on dedup + comp   │  │    SRDF: sync replication   │  │   SnapMirror: replication   │   │
│   │ ActiveCluster: active-active│  │   Dynamic tiering + cache   │  │   SnapCenter: backup mgmt   │   │
│   │  SafeMode: immutable snaps  │  │   PowerPath: multipathing   │  │  FabricPool: cloud tiering  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Arrays expose LUNs (block) or volumes (file) to hosts and VMs via storage protocols                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Pure FlashBlade       │  │   PowerScale / Data Domain  │  │    Keystone / StorageGRID   │   │
│   │   Scale-out file + object   │  │  PowerScale: scale-out NAS  │  │    Keystone: STaaS model    │   │
│   │   NFS · SMB · S3 protocols  │  │  Data Domain: dedup backup  │  │  StorageGRID: object store  │   │
│   │  Unstructured data at scale │  │     NFS · SMB · DD Boost    │  │     Cloud Volumes ONTAP     │   │
│   │    Rapid Restore: backup    │  │  Multi-PB capacity scaling  │  │  Snap replication + backup  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Specialty platforms handle unstructured data, backup, and cloud-connected workloads                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Fibre Channel   │      iSCSI       │        NFS        │    SMB / CIFS    │   S3 / Object    │   │
│   │ SAN block access │ IP block access  │  Unix file mounts │  Windows shares  │REST object store │   │
│   │ 16G · 32G · 64G  │  TCP/IP · iSNS   │   NFS v3 · v4.1   │   CIFS · DFS-N   │HTTP · REST · SDK │   │
│   │ HBA → SAN switch │ iSCSI initiator  │    Mount via IP   │   SMB sessions   │Buckets + prefixes│   │
│   │ Zoning + masking │ CHAP auth + iSNS │  Export policies  │ Share perms+ACL  │  Policies + IAM  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  NVMe/SSD drives · FC HBAs (16G/32G) · 10/25/100 GbE NICs · SAN switches · Power & Cooling            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  LUN          = Logical Unit Number; a block device exposed by a storage array via FC or iSCSI        │
│  SAN          = Storage Area Network; dedicated high-speed network carrying block storage traffic     │
│  NAS          = Network Attached Storage; file-level storage served over IP via NFS or SMB            │
│  FC           = Fibre Channel; high-speed block protocol using HBAs, SAN switches, and WWPN zoning    │
│  iSCSI        = Internet SCSI; block storage over standard TCP/IP — no specialised hardware required  │
│  NFS          = Network File System; Unix/Linux file protocol; mounts remote directories over IP      │
│  SMB          = Server Message Block; Windows file-sharing protocol, also known as CIFS               │
│  SRDF         = Symmetrix Remote Data Facility; Dell EMC sync replication between PowerMax arrays     │
│  SnapMirror   = NetApp replication engine; copies volumes between ONTAP systems or to cloud           │
│  SafeMode     = Pure Storage immutable snapshot feature; protects data against ransomware deletion    │
│  ActiveCluster= Pure active-active stretch cluster; I/O served from both sites simultaneously         │
│  Dedup        = Deduplication; eliminates duplicate data blocks to reduce raw capacity consumption    │
│  FabricPool   = NetApp tiering; auto-moves cold blocks to S3-compatible object storage                │
│  ONTAP        = NetApp unified storage OS running on FAS, AFF, Cloud Volumes, and StorageGRID         │
│  DD Boost     = Data Domain client-side dedup; reduces backup data transferred over the network       │
│  Keystone     = NetApp STaaS subscription; on-prem arrays billed like cloud consumption               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="dell/">
  <strong>Dell Storage</strong>
  <span>PowerMax, PowerScale, ECS, Data Domain, Unity, VPLEX, and PowerPath.</span>
</a>

<a class="kb-card" href="pure/">
  <strong>Pure Storage</strong>
  <span>FlashArray, FlashBlade, Evergreen, and Evergreen One.</span>
</a>

<a class="kb-card" href="netapp/">
  <strong>NetApp Storage</strong>
  <span>ONTAP, SnapMirror, SnapCenter, and Keystone.</span>
</a>

<a class="kb-card" href="ceph/">
  <strong>Ceph</strong>
  <span>Open-source distributed storage — RBD block, CephFS file, and RGW object via RADOS.</span>
</a>

<a class="kb-card" href="certifications/">
  <strong>Certifications</strong>
  <span>Storage certification study notes — vendor tracks, practice notes, weak areas, and review plans.</span>
</a>
</div>
