# Datastore Standard


<div class="kb-summary">
Datastore Standard reference covering Overview, Naming, VMFS Version, Maximum Datastore Size, Mounting and 3 more sections.
</div>

```text
┌──────────────────────────────────── vSphere — Datastore Standard ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Standards governing datastore naming, sizing, storage policy assignment, and vSAN config   │   │
│   │        Naming: ds-{type}-{site}-{nn}; type = vsan / nfs / vmfs; site = datacenter code        │   │
│   │       Capacity: 80% used triggers warning; 90% used triggers critical and blocks new VMs      │   │
│   │      SPBM: all VMs must have an explicit storage policy; no VMs on default policy in prod     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Naming standard + SPBM policy + capacity thresholds define the datastore compliance state          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Naming Rules        │  │        Capacity Rules       │  │         Policy Rules        │   │
│   │       ds-{type}-{site}      │  │          80% = warn         │  │        SPBM required        │   │
│   │        Lowercase only       │  │        90% = critical       │  │        vSAN FTT=1 min       │   │
│   │        No spaces/dots       │  │        Max 64TB VMFS        │  │        Dedup/compress       │   │
│   │       Site code suffix      │  │         SDRS at 85%         │  │       Backup tag reqd       │   │
│   │        Sequential nn        │  │         Thin < 150%         │  │        Tiering policy       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Non-compliant datastores flagged in vCenter; reviewed in weekly capacity meeting                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Type       │  Naming example  │      Max size     │   SPBM policy    │    Threshold     │   │
│   │       vSAN       │  ds-vsan-lon-01  │   Cluster-bound   │    vSAN FTT=1    │     80% warn     │   │
│   │       NFS        │  ds-nfs-lon-01   │     NAS-bound     │   NetApp Gold    │     80% warn     │   │
│   │       VMFS       │  ds-vmfs-lon-01  │        64TB       │   SAN Standard   │     80% warn     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: NVMe/SSD disk groups (vSAN) · NFS NAS arrays · FC/iSCSI LUNs (VMFS)                      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SPBM          = Storage Policy Based Management; VM-level storage capability assignment            │
│    FTT           = Failures To Tolerate; vSAN redundancy level (FTT=1 means 1 host failure ok)        │
│    SDRS          = Storage DRS; migrates VMs when datastore exceeds utilisation threshold             │
│    Datastore cluster = SDRS-managed group; enables automated space and IO balancing                   │
│    Thin overcommit = Provisioned thin capacity as ratio of physical; max 150% recommended             │
│    Dedup/compress = vSAN space efficiency; reduces effective capacity needed per VM                   │
│    Backup tag    = Custom vCenter tag marking backup target datastores vs workload stores             │
│    Tiering policy = FabricPool / vSAN policy for cold data migration to capacity tier                 │
│    Sequential nn = Two-digit suffix (-01, -02) for ordered datastore identification                   │
│    Site code     = Two-to-four letter datacenter code embedded in datastore name                      │
│    64TB VMFS     = Maximum VMFS 6 datastore size on a single LUN                                      │
│    Capacity warn = 80% threshold triggers capacity planning; 90% blocks new provisioning              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [Standards](../index.md) reference.

---

## Overview

This standard governs how datastores are named, created, presented, and managed across the vSphere environment. All new datastores must follow this standard before VMs are placed on them.

## Naming

Follow the datastore naming standard: `ds-<env>-<storage>-<protocol>-<##>`

Examples:
- `ds-prod-powermax-fc-01`
- `ds-prod-flasharray-fc-02`
- `ds-mgmt-netapp-nfs-01`
- `ds-dev-vsan-vsan-01`

Do not use autogenerated names from the array (e.g., LUN identifiers or default NFS export names).

## VMFS Version

| Setting | Requirement |
|---|---|
| VMFS Version | VMFS 6 for all new block datastores |
| VMFS 5 | No new VMFS 5 datastores. Existing VMFS 5 must be upgraded during next maintenance window. |
| Block Size | 1 MB (default — do not change) |

## Maximum Datastore Size

| Type | Max Size | Notes |
|---|---|---|
| VMFS | 64 TB (theoretical). Recommended max: 20 TB | Larger datastores increase recovery time and impact scope of failures |
| NFS | No hard limit — align with array export sizing | Keep individual exports under 50 TB for manageability |
| vSAN | Bounded by cluster capacity | Managed automatically |

Keep datastores to a manageable size. A 20 TB VMFS datastore is easier to recover, rebalance, or migrate than a single 64 TB volume.

## Mounting

| Requirement | Detail |
|---|---|
| Mount to all hosts in cluster | Every host in the cluster must have the datastore mounted, not just a subset |
| Per-host LUN presentation | Storage zoning or masking must present each LUN to all required hosts via all available paths |
| Path count | Minimum 2 paths per host (Active/Active or Active/Passive depending on array) |
| PSP (Path Selection Policy) | Round Robin for Active/Active arrays. MRU or Fixed for Active/Passive. Follow array vendor recommendation. |

## Backup Tagging

Tag each datastore to indicate backup tier:

| Tag | Meaning |
|---|---|
| `backup-gold` | Nightly backup, 30-day retention, tested quarterly |
| `backup-silver` | Daily backup, 14-day retention |
| `backup-bronze` | Weekly backup, 7-day retention |
| `backup-none` | No backup (dev/test/scratch only — requires approval) |

Tags are applied in vCenter under the `Backup Tier` category. The backup tool (Veeam) uses these tags for job scoping.

## Capacity Management

| Threshold | Action |
|---|---|
| > 70% used | Create monitoring alert. Plan expansion or VM migration. |
| > 80% used | Alert triggered. Schedule expansion or storage vMotion within 2 weeks. |
| > 90% used | Critical. Immediate action. Do not place new VMs until resolved. |

## New Datastore Checklist

- [ ] LUN presented from array with correct size and RAID type
- [ ] Zoning or masking configured to all required hosts
- [ ] Datastore named per standard
- [ ] VMFS 6 formatted (for block)
- [ ] Mounted to all hosts in the target cluster
- [ ] Path count verified on each host
- [ ] PSP set per array vendor recommendation
- [ ] Backup tier tag applied
- [ ] Datastore capacity alert configured in monitoring
- [ ] Datastore Inventory updated
- [ ] Change record closed with post-validation
