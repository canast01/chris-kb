---
tags:
  - vsan
  - storage
  - architecture
---
# vSAN Storage Policy Decision Tree

<div class="kb-summary">
Choose the right vSAN storage policy: FTT level, RAID type (mirror vs erasure coding), encryption, and dedup/compression based on cluster size and requirements.
</div>
![vSAN Storage Policy Decision Tree](../../assets/reference-decision-trees-vsan-policy.svg)




```mermaid
flowchart TD
    A([Start: Configure vSAN Storage Policy]) --> B{Failures to tolerate?}

    B -->|FTT = 1| C{Cluster has ≥ 6 hosts?}
    B -->|FTT = 2| D{Cluster has ≥ 6 hosts?}
    B -->|FTT = 3| E[RAID-1 Mirror FTT=3\nMinimum 7 hosts\n4× storage overhead]

    C -->|Yes| F[RAID-5 Erasure Coding\n4 hosts min · 1.33× overhead]
    C -->|No — 3 hosts min| G[RAID-1 Mirror FTT=1\n3 hosts min · 2× overhead]

    D -->|Yes| H[RAID-6 Erasure Coding\n6 hosts min · 1.5× overhead]
    D -->|No — 5 hosts min| I[RAID-1 Mirror FTT=2\n5 hosts min · 3× overhead]

    F --> J{Encryption at rest needed?}
    G --> J
    H --> J
    I --> J
    E --> J

    J -->|Yes| K[Enable Data-at-Rest Encryption\nKMIP KMS integration required\nvCenter trust authority or external KMS]
    J -->|No| L

    K --> L{Dedup and compression?}

    L -->|vSAN OSA all-flash| M[Dedup + Compression\nCluster-wide · ESXi 6.6+\nNot compatible with D@RE on OSA]
    L -->|vSAN ESA — NVMe only| N[Compression only\nPer-object · no dedup on ESA\nCompatible with encryption]
    L -->|Hybrid or skip| O([No dedup/compression\nSimplest configuration\nHighest raw capacity usage])
    M --> P([Policy defined — apply via SPBM\nin vCenter Storage Policies])
    N --> P
```

```d2
direction: right

center: "Decision Trees" {shape: hexagon}
quick_reference: "Quick reference" {shape: rectangle}
key_rules: "Key rules" {shape: rectangle}

center -> quick_reference
center -> key_rules
```

## Quick reference

| FTT | RAID | Min hosts | Overhead | Use case |
|---|---|---|---|---|
| 1 | RAID-1 Mirror | 3 | 2× | Small clusters, dev/test |
| 1 | RAID-5 EC | 4 | 1.33× | Production, ≥4 nodes |
| 2 | RAID-1 Mirror | 5 | 3× | Critical workloads, small cluster |
| 2 | RAID-6 EC | 6 | 1.5× | Production, best efficiency |
| 3 | RAID-1 Mirror | 7 | 4× | Mission-critical only |

## Key rules

- **FTT=1 + RAID-5** requires exactly 4 hosts minimum (4+1 parity striping across 4 nodes).
- **FTT=2 + RAID-6** requires exactly 6 hosts minimum.
- **D@RE (Data-at-Rest Encryption)** on vSAN OSA is **incompatible with dedup** — enabling both will revert dedup to disabled.
- **vSAN ESA** (8.x, NVMe-only) uses compression only — no traditional dedup; encryption is compatible.
- Policies are applied per-VM or per-VMDK via SPBM in vCenter → Policies and Profiles.

## See also

- [vSAN Cheat Sheet](../cheat-sheets/vsan/)
- [vSAN Architecture](../../virtualization/vmware/vsan/architecture/)
- [vSAN Operations](../../virtualization/vmware/vsan/operations/procedures/)
- [Back to Decision Trees](index.md)
