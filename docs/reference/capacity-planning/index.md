---
tags:
  - capacity-planning
  - architecture
  - vmware
  - storage
---

# Capacity Planning Reference

!!! summary "kb-summary"
    Sizing formulas, rules of thumb, and worksheets for compute, storage, and network capacity planning.

<div class="kb-grid" markdown>
<div class="kb-card" markdown>

**Compute** — CPU and memory sizing formulas for mixed, VDI, and latency-sensitive workloads with HA headroom built in.

</div>
<div class="kb-card" markdown>

**Storage** — vSAN usable capacity tables, thin provisioning limits, snapshot overhead rules, and dedup/compression savings estimates.

</div>
<div class="kb-card" markdown>

**Network** — Bandwidth estimates for vSAN, NFS/iSCSI, and FC/FCoE, with per-host and per-port rules of thumb.

</div>
<div class="kb-card" markdown>

**Worksheet** — Blank-fillable table for current, 12-month, and 36-month projections across every resource dimension.

</div>
</div>

---

## Compute Capacity (VMware vSphere)

### CPU Sizing

**Rules of thumb**

| Workload Type | vCPU:pCPU Ratio |
|---|---|
| Mixed enterprise workloads | 10:1 |
| VDI (persistent/linked clone) | 4:1 |
| Real-time / latency-sensitive | 1:1 |
| Dev/test environments | 15:1 – 20:1 |

**Sizing formula**

```text
Required pCPUs = (Total vCPUs × Avg_Utilisation%) ÷ (Target_pCPU_Utilisation% × Cores_per_Socket)
```

- `Total_vCPUs` — sum of all vCPUs assigned across all VMs in the cluster.
- `Avg_Utilisation%` — measured from vCenter performance charts over a representative 30-day window (peak business hours, not average of averages).
- `Target_pCPU_Utilisation%` — recommended **60–70%** for production; leaves room for burst and scheduled maintenance.
- `Cores_per_Socket` — physical cores per socket (not logical threads; disable Hyper-Threading count if scheduling latency matters).

**Worked example — 500-VM mixed estate**

| Parameter | Value |
|---|---|
| Total vCPUs assigned | 4,000 |
| Measured avg utilisation | 35% |
| Target pCPU utilisation | 65% |
| Cores per socket | 20 |
| **Required pCPUs** | **(4,000 × 0.35) ÷ (0.65 × 20) = 1,400 ÷ 13 ≈ 108 cores** |
| Hosts required (20c/host) | 108 ÷ 20 = **6 hosts** |
| +N+1 HA buffer | **7 hosts** (one host failure tolerated) |
| Recommended order | **8 hosts** (one spare + room for 12-month growth) |

!!! tip "vSphere DRS baseline"
    Pull the **Cluster Utilisation** chart from vCenter → Monitor → Utilisation. Set the time range to 30 days and export to CSV. Calculate P95 utilisation, not average — average undersizes by 20–30%.

---

### Memory Sizing

**Rules of thumb**

| Scenario | Max Overcommit Ratio |
|---|---|
| Production VMs (any workload) | 1.5:1 (physical RAM vs. configured vRAM) |
| Dev/test, disposable VMs | 2:1 |
| Latency-sensitive / real-time | 1:1 (no overcommit) |
| VDI with linked clones | 1.25:1 with TPS enabled |

**Formula with balloon/swap overhead**

```text
Required_Physical_RAM = (Sum_vRAM × Overcommit_Ratio) + Balloon_Reserve + Swap_Reserve + VMkernel_Overhead

Balloon_Reserve  ≈ 5% of total configured vRAM (worst-case balloon driver activation)
Swap_Reserve     ≈ 0% target (swap = performance degradation; size to avoid it entirely)
VMkernel_Overhead ≈ 1 GB per host + ~100 MB per running VM (for VM executable overhead)
```

**N+1 HA memory sizing**

```text
Minimum_Host_RAM_for_HA = (Total_Cluster_vRAM_Active) ÷ (Host_Count - 1)
```

Where `Total_Cluster_vRAM_Active` is the sum of memory actively consumed (not configured), measured at P95.

!!! warning "Swap kills performance"
    vSphere memory swap to disk is a last resort. If any host reports non-zero `swapOut` in vCenter performance charts, add RAM immediately — I/O latency increases by 10–100× during swap events.

---

### vSAN Capacity

**Formulas**

| Policy | Usable Capacity Formula |
|---|---|
| FTT=1 RAID-1 (Mirroring) | `Raw ÷ 2 × 0.70` (30% slack retained) |
| FTT=1 RAID-5 (Erasure Coding, 4-host min) | `Raw × 0.75 × 0.70` |
| FTT=2 RAID-6 (Erasure Coding, 6-host min) | `Raw × 0.67 × 0.70` |

The **30% slack** is mandatory — vSAN stops accepting writes and enters a read-only emergency state when free space drops below 25%. Maintain ≥30% to keep a safe operational buffer.

**Raw → Usable reference table**

| Raw Capacity | RAID-1 Usable | RAID-5 Usable | RAID-6 Usable |
|---|---|---|---|
| 10 TB | 3.5 TB | 5.25 TB | 4.69 TB |
| 50 TB | 17.5 TB | 26.25 TB | 23.45 TB |
| 100 TB | 35 TB | 52.5 TB | 46.9 TB |
| 500 TB | 175 TB | 262.5 TB | 234.5 TB |

!!! note "All-Flash vs Hybrid"
    All-Flash clusters benefit most from RAID-5/6 — the performance penalty of erasure coding is negligible on NVMe. Hybrid clusters should prefer RAID-1 to avoid cache-miss amplification during rebuild operations.

---

## Storage Capacity (General)

### Thin Provisioning Overhead

**Rule:** Never provision more than **2× physical raw capacity** across all thin-provisioned volumes on a single aggregate/datastore. Beyond 2:1, the risk of a space exhaustion event causing simultaneous VM pause across multiple workloads increases sharply.

**Aggregate overcommit formula (ONTAP)**

```text
Overcommit_Ratio = Sum(Provisioned_Volume_Sizes) ÷ Aggregate_Physical_Capacity

Safe threshold:  ≤ 2.0×
Warning:         2.0× – 2.5×
Critical:        > 2.5×
```

To calculate available thin-provision headroom:

```text
Available_to_Provision = (Aggregate_Physical × 2.0) - Sum(Already_Provisioned)
```

!!! tip "ONTAP volume autogrow"
    Enable `volume autogrow` with a ceiling to absorb bursts, but always set the aggregate-level autogrow limit lower than the physical capacity to prevent cascading space exhaustion.

---

### Snapshot Space

**Rules of thumb**

| Workload | Recommended Snap Reserve |
|---|---|
| General VM workloads (moderate change rate) | 20% of volume size |
| Databases (Oracle, SQL Server, PostgreSQL) | 50% of volume size |
| VDI (high IOPS, frequent writes) | 30% of volume size |
| Archive / cold data | 5–10% of volume size |

**ONTAP snap reserve formula**

```text
Snap_Reserve_GB = Volume_Size_GB × (Change_Rate% ÷ 100) × Retention_Hours ÷ 24

Example: 1 TB DB volume, 5% daily change rate, 7-day retention
= 1024 GB × 0.05 × 7 = 358 GB snap reserve (35% of volume)
```

!!! warning "Snapshot spill"
    When the snap reserve is exhausted, ONTAP borrows space from the active file system. This causes apparent free space to shrink without new data being written — a common source of "disk full" surprises. Always monitor `snap-reserve-used%` separately from `volume-used%`.

---

### Dedup/Compression Savings Estimates

| Workload | Expected Reduction | Notes |
|---|---|---|
| VDI (linked clones) | 5:1 – 10:1 | Shared base image blocks deduplicate extremely well |
| General VM workloads | 2:1 – 4:1 | Mixed OS + app data; compression adds ~1.5× on top |
| Databases | 1.5:1 – 2:1 | Compression more effective than dedup on DB data |
| Backup data | 3:1 – 6:1 | Dedup across similar backup streams; varies by source |
| Media / unstructured | 1:1 | Already compressed; dedup/compression yields near-zero gain |

!!! note "Measure, don't assume"
    These are industry averages. Always run ONTAP Storage Efficiency Savings reports (`volume efficiency show -fields savings-percent`) after 30 days of production use to validate actual ratios before sizing the next capacity increment.

---

## Network Capacity

### vSAN Network

**Minimum bandwidth per host**

| vSAN Tier | Minimum NIC | Recommended |
|---|---|---|
| Hybrid (HDD + SSD cache) | 10 GbE | 10 GbE |
| All-Flash | 10 GbE | **25 GbE** |
| All-Flash, large cluster (16+ hosts) | 25 GbE | **25 GbE × 2 (LACP)** |

**Bandwidth estimate formula**

```text
Required_vSAN_BW = Hosts × Avg_Disk_Throughput_per_Host × Replication_Factor

Example: 8 hosts, 2 GB/s disk throughput each, FTT=1 RAID-1 (factor = 2)
= 8 × 2 GB/s × 2 = 32 GB/s cluster-internal bandwidth
Each host needs: 32 ÷ 8 = 4 GB/s ≈ 40 Gbps → 2× 25 GbE
```

---

### Storage Network (NFS / iSCSI)

**Rules of thumb**

| Bandwidth | Approximate IOPS |
|---|---|
| 1 Gbps | ~200 IOPS @ 4K random write |
| 10 Gbps | ~2,000 IOPS @ 4K random write |
| 25 Gbps | ~5,000 IOPS @ 4K random write |

These are conservative estimates for small-block random I/O. Sequential throughput saturates bandwidth before IOPS limits are reached — size for the dominant I/O profile of the workload.

**NFS/iSCSI host port sizing**

```text
Required_Ports = CEIL(Peak_IOPS ÷ IOPS_per_Port) × 2   (×2 for redundancy)
```

---

### SAN (FC / FCoE)

**Rules of thumb**

| FC Speed | Sustained Throughput |
|---|---|
| 8 Gbps FC port | ~600 MB/s usable (75% efficiency) |
| 16 Gbps FC port | ~1.2 GB/s usable |
| 32 Gbps FC port | ~2.4 GB/s usable |

**Port sizing rule:** 1 FC port per 8–10 Gbps of sustained aggregate throughput. Always plan in pairs (initiator + target path redundancy) and account for zoning overhead.

```text
Required_FC_Ports_per_Host = CEIL(Host_Peak_Throughput_Gbps ÷ FC_Port_Speed_Gbps) × 2
```

---

## Capacity Planning Worksheet

Use this table as a starting point for capacity reviews. Complete a new copy at each quarterly review cycle.

| Parameter | Current | 12-Month Projection | 36-Month Projection |
|---|---|---|---|
| VM count | | | |
| vCPU total (assigned) | | | |
| vCPU total (active P95) | | | |
| RAM configured (TB) | | | |
| RAM active P95 (TB) | | | |
| Storage raw (TB) | | | |
| Storage usable (TB) | | | |
| vSAN slack % | | | |
| Network bandwidth peak (Gbps) | | | |
| Backup data generated (TB/week) | | | |
| Backup repo used (TB) | | | |
| Snapshot reserve used (TB) | | | |
| FC / NFS ports in use | | | |
| **Headroom CPU** | | | |
| **Headroom RAM** | | | |
| **Headroom Storage** | | | |

!!! tip "Projection method"
    Apply a **CAGR (Compound Annual Growth Rate)** to current figures: `Future = Current × (1 + Growth_Rate)^Years`. A conservative default for mixed enterprise environments is **15–20% annual growth** for compute and **30–40%** for storage.

---

## Headroom Rules

| Resource | Warning | Critical | Recommended Action |
|---|---|---|---|
| CPU (cluster avg utilisation) | >60% | >80% | Add hosts; review VM right-sizing |
| Memory (cluster avg active) | >70% | >85% | Add RAM DIMMs or add hosts |
| Datastore / volume used | >75% | >85% | Expand datastore or add new DS |
| vSAN free slack | <30% | <20% | Add capacity disks or hosts |
| Thin-provision overcommit ratio | >2.0× | >2.5× | Expand aggregate or reclaim space |
| Backup repository used | >80% | >90% | Extend repo (add extent or new target) |
| Snapshot reserve used | >80% | >100% | Increase snap reserve; prune old snaps |
| FC / NFS network utilisation | >65% | >80% | Add ports or upgrade port speed |

!!! warning "Act at Warning, not Critical"
    Procurement and delivery lead times for servers and storage typically run 4–12 weeks. Triggering orders at the **Warning** threshold gives enough runway. Waiting for **Critical** means you are already operating at risk.

---

## See Also

- [vSAN](../../virtualization/vmware/vsan/index.md) — Detailed vSAN capacity, policy, and health-check procedures
- [ONTAP](../../storage/netapp/ontap/index.md) — NetApp ONTAP storage capacity management and efficiency features
- [vCenter](../../virtualization/vmware/vcenter/index.md) — Cluster monitoring, DRS configuration, and performance baselines
