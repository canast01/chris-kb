# Datastore Standards

```
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
- Clear datastore names
- Avoid running production datastores near full capacity
- Monitor thin provisioning risk
- Use storage policies where appropriate
- Remove stale ISOs and old templates
- Review snapshots regularly
- Document datastore ownership and purpose

## Capacity Thresholds

| Threshold | Action |
|---|---|
| 80% used | Review growth trends |
| 85% used | Plan cleanup or expansion |
| 90% used | Open action ticket |
| 95% used | Treat as urgent — immediate action required |

## Expansion and Decommission

- Expansion requires change approval
- Emergency expansion process should be documented in the runbook
- Decommission process: confirm no active VMs, remove from datastores, coordinate with storage team
