# Datastore Inventory

```text
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
> Part of the [Inventory](../index.md) reference.

---

## Overview

Track all datastores presented to the vSphere environment. Update this inventory after any datastore creation, expansion, removal, or re-presentation event.

## Datastore Inventory Table

| Datastore Name | Type | Capacity (TB) | Free (TB) | % Used | Hosts Mounted | Backing Array | Protocol | VMFS Version | Notes |
|---|---|---|---|---|---|---|---|---|---|
| ds-prod-powermax-fc-01 | VMFS | 20 | 8 | 60% | All prod compute hosts | Dell PowerMax 2500 | FC | VMFS 6 | General production VMs |
| ds-prod-powermax-fc-02 | VMFS | 20 | 5 | 75% | All prod compute hosts | Dell PowerMax 2500 | FC | VMFS 6 | General production VMs |
| ds-prod-flasharray-fc-01 | VMFS | 10 | 6 | 40% | All prod compute hosts | Pure FlashArray //XL | FC | VMFS 6 | Latency-sensitive workloads |
| vsanDatastore | vSAN | 46 | 22 | 52% | cl-prod-compute-01 | vSAN (internal) | vSAN | — | Production vSAN cluster |
| ds-nfs-netapp-01 | NFS | 50 | 30 | 40% | All prod + mgmt hosts | NetApp AFF A400 | NFS v3 | — | ISOs, templates, backups |

## Fields Reference

| Field | Description |
|---|---|
| Datastore Name | Follows naming standard: `<site>-<storage>-<protocol>-<##>` |
| Type | VMFS, vSAN, NFS, vVols |
| Capacity (TB) | Total provisioned size |
| Free (TB) | Available space at last check |
| % Used | Utilisation percentage |
| Hosts Mounted | Which hosts or clusters have the datastore mounted |
| Backing Array | Storage array providing the LUN or NFS export |
| Protocol | FC, iSCSI, NFS v3, NFS v4.1, vSAN |
| VMFS Version | VMFS 5 or VMFS 6 (not applicable for NFS/vSAN) |
| Notes | Owner, usage, any capacity warnings or exceptions |

## Capacity Thresholds

| Threshold | Action |
|---|---|
| > 70% used | Monitor closely — plan expansion or VM migration |
| > 80% used | Alert raised — schedule expansion within 2 weeks |
| > 90% used | Critical — immediate action required to free space or expand |

## Datastore Checklist

When presenting a new datastore:

- [ ] Datastore name follows the naming standard
- [ ] LUN or NFS export is zoned/routed correctly and only to intended hosts
- [ ] VMFS 6 used for all new block datastores
- [ ] Datastore mounted to all required hosts (not just one)
- [ ] Storage policy or tag applied to identify backing tier
- [ ] Datastore added to monitoring capacity alerting
- [ ] Inventory updated
