# Datastore Inventory

```
┌──────────────────────────────────── vSphere — Datastore Inventory ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Per-datastore record for capacity management, storage policy audits, and VM placement     │   │
│   │         Fields: name, type (VMFS/vSAN/NFS/vVol), capacity, free space, hosts, VM count        │   │
│   │      Policy: default SPBM policy applied, datastore cluster membership, replication state     │   │
│   │      Alert thresholds: 80% used = capacity warning; 90% used = critical; action required      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Datastore type determines protocol, redundancy model, and SPBM policy options                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           Identity          │  │           Capacity          │  │         Connectivity        │   │
│   │        Datastore name       │  │     Total capacity (GB)     │  │       Hosts connected       │   │
│   │       Type (VMFS/NFS)       │  │       Free space (GB)       │  │           VM count          │   │
│   │       Version/block sz      │  │            Used %           │  │        Storage policy       │   │
│   │      Datastore cluster      │  │       Thin provisioned      │  │      Replication state      │   │
│   │       NFS server/path       │  │       Overcommit ratio      │  │      Backup target tag      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Capacity and connectivity fields drive VM placement and storage DRS decisions                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Name       │       Type       │     Cap / Free    │    Hosts/VMs     │      Policy      │   │
│   │ ds-vsan-prod-01  │       vSAN       │    40TB / 12TB    │     8 / 220      │   vSAN Default   │   │
│   │  ds-nfs-prod-01  │      NFS v3      │     20TB / 6TB    │      8 / 80      │    NetApp NFS    │   │
│   │   ds-vmfs-mgmt   │      VMFS 6      │    4TB / 1.2TB    │      4 / 15      │    Management    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: vSAN NVMe/SSD disk groups · NFS NAS heads · VMFS on FC/iSCSI LUNs                        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    VMFS          = vSphere VMFS filesystem on block LUN (FC/iSCSI); cluster-aware locking             │
│    vSAN          = Pooled datastore from host-local NVMe/SSD managed by vSAN kernel module            │
│    NFS datastore = NAS share mounted over NFS v3/v4.1; managed at the NAS head level                  │
│    vVol          = Virtual Volumes; per-VM objects on VASA-capable arrays (no VMFS needed)            │
│    SPBM          = Storage Policy Based Management; assigns storage capabilities to VMs               │
│    SDRS          = Storage DRS; balances space/IO across datastores in a datastore cluster            │
│    Thin prov.    = VM disk uses only written space; capacity grows on demand up to disk limit         │
│    Overcommit    = Total thin-provisioned capacity vs actual datastore physical capacity              │
│    Replication   = SnapMirror / vSAN Stretched / SRM protection state of the datastore                │
│    Backup target = Tag marking datastore as backup destination rather than primary workload           │
│    80% threshold = Standard alert point; capacity action required before hitting 90% usage            │
│    Datastore cluster = SDRS-managed group; VMs placed and migrated across member datastores           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
| Field | Example |
|---|---|
| Datastore Name | ds-prod-vsan-01 |
| Type | vSAN |
| Capacity | 100 TB |
| Free Space | 35 TB |
| Cluster | cl-prod-compute-01 |
| Storage Policy | vSAN Default Policy |
| Criticality | Production |
