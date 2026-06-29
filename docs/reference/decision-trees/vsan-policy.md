---
tags:
  - vsan
  - storage
  - architecture
---
# vSAN Storage Policy Decision Tree

*Applies to: All products*

<div class="kb-summary">
Choose the right vSAN storage policy: FTT level, RAID type (mirror vs erasure coding), encryption, and dedup/compression based on cluster size and requirements.
</div>

```d2
direction: right

B: "B" {shape: rectangle}
E: "RAID-1 Mirror FTT=3\nMinimum 7 hosts\n4× storage overhead" {shape: rectangle}
C: "C" {shape: rectangle}
F: "RAID-5 Erasure Coding\n4 hosts min · 1.33× overhead" {shape: rectangle}
G: "RAID-1 Mirror FTT=1\n3 hosts min · 2× overhead" {shape: rectangle}
D: "D" {shape: rectangle}
H: "RAID-6 Erasure Coding\n6 hosts min · 1.5× overhead" {shape: rectangle}
I: "RAID-1 Mirror FTT=2\n5 hosts min · 3× overhead" {shape: rectangle}
J: "J" {shape: rectangle}
K: "Enable Data-at-Rest Encryption\nKMIP KMS integration required\nvCenter trust authority or external KMS" {shape: rectangle}
L: "L" {shape: rectangle}
M: "Dedup + Compression\nCluster-wide · ESXi 6.6+\nNot compatible with D@RE on OSA" {shape: rectangle}
N: "Compression only\nPer-object · no dedup on ESA\nCompatible with encryption" {shape: rectangle}
O: "No dedup/compression\nSimplest configuration\nHighest raw capacity usage" {shape: rectangle}
P: "Policy defined — apply via SPBM\nin vCenter Storage Policies" {shape: rectangle}
A: "Start: Configure vSAN Storage Policy" {shape: rectangle}

B -> E
C -> F
C -> G
D -> H
D -> I
G -> J
H -> J
I -> J
E -> J
J -> K
J -> L
L -> M
L -> N
L -> O
M -> P
N -> P
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

- [vSAN Cheat Sheet](../../cheat-sheets/vsan/)
- [vSAN Architecture](../../../virtualization/vmware/vsan/architecture/)
- [vSAN Operations](../../../virtualization/vmware/vsan/operations/procedures/)
- [Back to Decision Trees](index.md)
