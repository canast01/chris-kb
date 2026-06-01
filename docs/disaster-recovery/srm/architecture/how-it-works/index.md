# SRM — How It Works


<div class="kb-summary">
How It Works reference covering Overview, Topology, Recovery Plan Modes, Storage Replication Adapters (SRAs), Protection Groups and 1 more sections.
</div>

```
┌───────────────────────────────────────── SRM — How It Works ──────────────────────────────────────────┐
│                                                                                                       │
│    SRM data flow — from source to target through the protection pipeline:                             │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 1  Source / Production System                                 │   │
│   │       SRM Server (Protected) — vCenter plugin at production site; manages protection groups   │   │
│   │                 Host writes are intercepted or snapshotted by the SRM agent/proxy             │   │
│   │                  Changed blocks tracked via CBT / journal / delta-set mechanism               │   │
│   │                 Consistency ensured at quiesce point before data transfer begins              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Changed data forwarded to the SRM engine — compression and encryption applied in transit           │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                         2  SRM Engine                                         │   │
│   │              SRM Server (Recovery)  — vCenter plugin at DR site; runs recovery plans          │   │
│   │                    Data compressed, deduplicated, and encrypted before storage                │   │
│   │                  Metadata catalog updated; job status reported to control plane               │   │
│   │                                          srm-cli vm list                                      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     3  Target / Repository                                    │   │
│   │      SRA (Storage Replication Adapter) — translates SRM calls to array replication commands   │   │
│   │                  Recovery point written; retention policy applied automatically               │   │
│   │                                   Restore: srm-cli recovery run                               │   │
│   │                     RTO driven by target storage performance and data volume                  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two vCenter instances (protected + recovery) · SRA on SRM server · Array replication link            │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRM           = Site Recovery Manager; VMware product for DR orchestration and testing               │
│  SRA           = Storage Replication Adapter; plugin linking SRM to specific array replication        │
│  Protection Group= logical grouping of VMs covered by a single replication consistency group          │
│  Recovery Plan = automated DR runbook: power-off order, datastore failover, IP customization          │
│  IP Customization= per-VM network settings applied at recovery site (different subnet/gateway)        │
│  Test Failover = non-disruptive plan validation using snapshot; production unaffected                 │
│  Planned Migration= graceful workload movement; VMs shutdown at protected, started at recovery        │
│  Emergency Failover= disaster scenario; VMs powered on from latest available replica                  │
│  Failback      = after recovery, re-protect VMs and migrate back to production site                   │
│  Re-protect    = reverses replication direction; DR site becomes new protected site                   │
│  Recovery Point= specific replication snapshot used for VM recovery; RPO = interval                   │
│  vCenter Pair  = SRM connection between two vCenter instances enables cross-site orchestration        │
│  Startup Priority= ordering within recovery plan; lower number = powers on first                      │
│  Site Pair     = trust relationship between protected and recovery SRM servers                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

VMware Site Recovery Manager (SRM) is a DR orchestration platform deployed as a vCenter plugin on both the protected and recovery sites. It automates VM failover by coordinating storage presentation, VM registration, power-on sequencing, IP customisation, and custom scripts — without manual intervention at the storage or compute layer. SRM supports both array-based replication (via SRAs) and built-in vSphere Replication.

## Topology



## Recovery Plan Modes

| Mode | Description |
|---|---|
| Test | SRM creates a temporary snapshot of R2/replica; powers on VMs in isolated network; production replication continues; test cleanup removes snapshot |
| Planned migration | Orderly shutdown of protected VMs, final sync, then power-on at recovery site |
| Unplanned failover | Protected site unavailable; SRM fails over using most recent replicated state |

## Storage Replication Adapters (SRAs)

| Vendor | SRA | Supported Replication |
|---|---|---|
| Dell EMC | Dell EMC SRA for PowerMax | SRDF/A, SRDF/S |
| Pure Storage | Pure Storage SRA | ActiveCluster (sync), async replication |
| NetApp | NetApp SRA for ONTAP | SnapMirror (async), SnapMirror Synchronous |

SRAs must be installed on both sites and must match the same major version.

## Protection Groups

| Type | Granularity | Replication Backend |
|---|---|---|
| Array-based | Datastore (all VMs on the datastore) | SRA (vendor-specific) |
| vSphere Replication | Per-VM | Built-in vSphere Replication appliance |

## vSphere Replication

- RPO: 5 minutes minimum (no lower)
- Consistency: crash-consistent by default; application-consistent with quiescing enabled
- Bandwidth: compressed and deduplicated; can be throttled per-VM
- No SRA required — replication engine is embedded in the vSphere Replication appliance (one per site)
