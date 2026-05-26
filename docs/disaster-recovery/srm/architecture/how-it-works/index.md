# SRM — How It Works

## Overview

VMware Site Recovery Manager (SRM) is a DR orchestration platform deployed as a vCenter plugin on both the protected and recovery sites. It automates VM failover by coordinating storage presentation, VM registration, power-on sequencing, IP customisation, and custom scripts — without manual intervention at the storage or compute layer. SRM supports both array-based replication (via SRAs) and built-in vSphere Replication.

## Topology

```mermaid
graph LR
  VC_A["vCenter A\n+ SRM Server A + SRA"] --> STG_A[("Storage A")]
  VC_B["vCenter B\n+ SRM Server B + SRA"] --> STG_B[("Storage B")]
  VC_A <-->|"SRM pairing"| VC_B
  STG_A -->|"replication\nvSphere Rep / array"| STG_B
  H_A(["Production VMs\nSite A"]) --> VC_A
  H_B(["DR VMs\nSite B"]) -.-> VC_B
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class VC_A ctrl
  class VC_B dr
  class STG_A,STG_B store
  class H_A host
  class H_B dr
```

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
