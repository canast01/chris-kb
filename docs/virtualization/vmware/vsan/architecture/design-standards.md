---
tags:
  - architecture
  - vmware
  - vsan
  - vsphere-8
---
# vSAN — Design Standards


<div class="kb-summary">
Design Standards reference covering Cluster Configuration, Stretched Cluster Architecture, Storage Policy Baseline, Naming Conventions, Capacity Management.

*Applies to: vSAN 7.x · 8.x*
</div>

```text
┌─────────────────────────────────────── vSAN — Design Standards ───────────────────────────────────────┐
│                                                                                                       │
│  vSAN design standards cover host sizing, disk group ratios, network requirements,                    │
│  fault tolerance policy selection, and cluster expansion rules.                                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Host & Disk Standards             │  │              Network Standards              │   │
│   │             Min 3 hosts (FTT=1)              │  │        10GbE minimum; 25GbE preferred       │   │
│   │         Homogeneous hosts preferred          │  │            Dedicated VMkernel NIC           │   │
│   │          Cache:capacity 1:10 ratio           │  │            Jumbo frames: MTU 9000           │   │
│   │          vSAN HCL: all disks listed          │  │          Latency <1ms host to host          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  All hardware must appear on the vSAN HCL; off-HCL disks cause unsupported state.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Policy Standards               │  │              Capacity Planning              │   │
│   │            Prod VMs: FTT=1 RAID-1            │  │            Slack: 30% free always           │   │
│   │            Critical: FTT=2 RAID-6            │  │           Resync headroom: 1 host           │   │
│   │           Test/dev: FTT=0 (no HA)            │  │         Expand by 3 hosts (FD rule)         │   │
│   │           Encryption: policy-based           │  │           Dedup/compress: OSA only          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  All ESXi hosts contribute their local NVMe/SSD/HDD to the shared vSAN datastore;                     │
│  TOR switches must support jumbo frames and LLDP for vSAN network health.                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  HCL          = Hardware Compatibility List; VMware approved disk list                                │
│  FTT          = Failures To Tolerate; defines redundancy level                                        │
│  RAID-1       = mirroring; FTT=1 needs 3 hosts; simple, higher cost                                   │
│  RAID-5/6     = erasure coding; space-efficient; FTT=1 needs 4, FTT=2 needs 6                         │
│  Cache ratio  = 1:10 cache to capacity; e.g., 400GB cache → 4TB capacity                              │
│  30% slack    = required for resync operations after disk/host failure                                │
│  Resync headroom= capacity to rebuild one failed host worth of data                                   │
│  OSA          = Original Storage Architecture; HDD+SSD; supports dedup                                │
│  ESA          = Express Storage Architecture; all-NVMe; no dedup needed                               │
│  Homogeneous  = same CPU/RAM/disk model per host; simplifies policy math                              │
│  MTU 9000     = jumbo frames; reduces CPU overhead for large I/O                                      │
│  LLDP         = Link Layer Discovery Protocol; used for vSAN net health                               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Cluster Configuration

Apply the following configuration baseline to every vSAN cluster before placing it in production.

**Host requirements:**

| Item | Requirement |
|---|---|
| Minimum nodes | 3 (FTT=1 RAID-1); 4 for RAID-5; 6 for RAID-6 |
| vSAN vmkernel adapter | Dedicated vmk on each host (vmk2 by convention) |
| Network speed | 10 GbE minimum; 25 GbE recommended for ESA or high-density |
| MTU | 9000 (jumbo frames) end-to-end on vSAN network |
| NIC allocation | Dedicated NIC or NIC pair for vSAN traffic (separate from management and vMotion) |
| RDMA | Optional (RDMA over RoCE v2) for ESA ultra-low latency |
| All hosts identical | Identical CPU, RAM, and disk group configuration per cluster for balanced capacity |

**Network validation before cluster creation:**

```bash
# Verify MTU 9000 end-to-end
vmkping -I vmk2 -d -s 8972 <remote-vsan-vmk-ip>
```

### Stretched Cluster Requirements

| Item | Requirement |
|---|---|
| Minimum hosts | 2 per site (4 total) + 1 witness |
| Witness | vSAN Witness Appliance (OVA) — not a full ESXi host |
| Inter-site latency | ≤ 5 ms RTT for standard workloads; ≤ 1 ms for latency-sensitive |
| Inter-site bandwidth | 10 GbE minimum; size for full resync of one site's data |
| Witness network | Low-bandwidth sufficient (metadata only — no data I/O) |
| vCenter | Must be accessible from both sites (deploy on shared management cluster or separate) |

**Failure domain behaviour:**

- **Site A failure:** VMs restart on Site B; witness maintains quorum. RTO depends on HA admission control settings.
- **Site B failure:** Same as above, reversed.
- **Witness failure:** Cluster continues operating but loses quorum arbitration capability — fix immediately.
- **Split-brain (both sites lose connectivity to each other):** vSAN pauses I/O on the site that cannot reach the witness. Preferred site takes precedence if configured.

**VM affinity:** Use VM-to-Host affinity groups to pin VMs to a preferred site. Without affinity, DRS may migrate VMs across sites, increasing cross-site I/O.

---

## Storage Policy Baseline

Define storage policies in vCenter before provisioning VMs. Assign policies by workload tier.

| Workload Tier | Policy Name | FTT | RAID | Checksum | Notes |
|---|---|---|---|---|---|
| Tier-1 Databases | `VSAN-T1-FTT2-RAID6` | 2 | RAID-6 | Enabled | 6+ node cluster required |
| Tier-2 General | `VSAN-T2-FTT1-RAID5` | 1 | RAID-5 | Enabled | 4+ node cluster required |
| Dev/Test | `VSAN-DEV-FTT1-RAID1` | 1 | RAID-1 | Enabled | 3+ node cluster |
| Stretched Cluster | `VSAN-STRETCH-FTT1-SITE` | 1 | RAID-1 per site | Enabled | Affinity rule per site |

**Object space reservation:** Set to 0% unless workloads require thick provisioning. Thin provisioning is the default for vSAN.

**Flash read cache reservation:** Set to 0% for all-flash clusters (not applicable). OSA hybrid clusters may benefit from a non-zero value for latency-sensitive workloads.

**Checksum:** Enable object checksum on all production storage policies. Checksum detects silent data corruption at the component level and triggers resync automatically.

**Capacity overhead by FTT and RAID method:**

| FTT | RAID Method | Minimum Hosts | Space Overhead |
|---|---|---|---|
| 1 | RAID-1 (Mirroring) | 3 | 2× |
| 1 | RAID-5 (Erasure Coding) | 4 | 1.33× |
| 2 | RAID-6 (Erasure Coding) | 6 | 1.5× |
| 2 | RAID-1 (Mirroring) | 5 | 3× |
| 3 | RAID-1 (Mirroring) | 7 | 4× |

---

## Naming Conventions

Consistent naming makes multi-cluster environments manageable and aligns with vCenter inventory organisation.

| Object | Pattern | Example |
|---|---|---|
| vSAN Cluster | `VSAN-<SITE>-<NN>` | `VSAN-LON-01` |
| Storage Policy (Tier-1) | `VSAN-T1-FTT<n>-RAID<n>` | `VSAN-T1-FTT2-RAID6` |
| Storage Policy (Tier-2) | `VSAN-T2-FTT<n>-RAID<n>` | `VSAN-T2-FTT1-RAID5` |
| Storage Policy (Dev) | `VSAN-DEV-FTT<n>-RAID<n>` | `VSAN-DEV-FTT1-RAID1` |
| Stretched Cluster Policy | `VSAN-STRETCH-<tag>` | `VSAN-STRETCH-FTT1-SITE` |
| Witness Appliance | `vsanwitness-<site>` | `vsanwitness-lon` |

Disk group components are not individually named in vSAN (managed at the host level). Document the physical disk-to-disk-group mapping in the host build record.

---

## Capacity Management

vSAN capacity management requires proactive monitoring. Resync operations during host failures or upgrades consume capacity above and beyond normal usage.

**Alert thresholds:**

| Threshold | Action |
|---|---|
| 70% used capacity | Alert — plan cluster expansion or data migration |
| 80% used capacity | Escalation alert — immediate action required; vSAN operations reserve is at risk |
| > 80% used capacity | vSAN may refuse new write operations or object provisioning |

**Capacity reserve (slack):**

Always maintain a minimum 30% free capacity:

- 10% for vSAN operations reserve (internal metadata and resync)
- 10% for resync buffer during host maintenance (one host's worth of data must be resynced)
- 10% operational headroom

**Monitoring commands:**

```bash
# Check cluster capacity from any ESXi host
esxcli vsan storage list
esxcli vsan cluster get

# PowerCLI capacity overview
Get-VsanSpaceUsage -Cluster <clustername>
```

Capacity monitoring should also be configured in Aria Operations with an alert policy targeting the 70% threshold.

---

## Sizing Guidance

Use this section to size a new vSAN cluster or validate whether an existing cluster can absorb additional workload.

### Input Variables

Before sizing, collect the following from the workload team:

| Variable | Description | Example |
|---|---|---|
| VM count | Total VMs to run on the cluster | 200 VMs |
| vCPU per VM (average) | Average virtual CPU count | 4 vCPUs |
| RAM per VM (average) | Average VM memory | 16 GB |
| Storage per VM (average) | Usable disk space needed per VM | 200 GB |
| I/O profile | Mostly read, mostly write, mixed | 70/30 read/write |
| Peak IOPS per VM | Maximum sustained IOPS for busy VMs | 500 IOPS |
| FTT policy | Failures to tolerate | FTT=1 RAID-5 |

### CPU Sizing

vSAN has minimal CPU overhead on each host (typically < 5%). CPU sizing is driven by VM workload, not vSAN itself.

```text
Total vCPUs needed = VM count × average vCPUs per VM
Target vCPU:pCPU ratio = 4:1 to 8:1 (compute-light) or 2:1 to 4:1 (compute-heavy)
Physical cores per host = Total vCPUs / ratio / number of hosts
```

**Example:** 200 VMs × 4 vCPUs = 800 vCPUs. At 4:1 ratio across 6 hosts = 34 physical cores per host. A dual-socket host with 18 cores per socket (36 pCPU) satisfies this.

### RAM Sizing

vSAN reserves memory for its own processes (~5–8 GB per host for OSA; ~8–12 GB for ESA). Account for this in host RAM sizing.

```text
Total VM RAM = VM count × average RAM per VM
vSAN overhead per host = 8 GB (add to host RAM requirement)
Target RAM per host = (Total VM RAM / hosts) + 8 GB vSAN overhead
```

**Example:** 200 VMs × 16 GB = 3,200 GB total. Across 6 hosts = 534 GB per host + 8 GB overhead = 542 GB. Size to 512 GB or 768 GB DIMMs depending on available configurations.

### Storage Capacity Sizing

vSAN capacity is calculated after accounting for FTT overhead and the required 30% slack:

```text
Raw storage per VM = usable storage × FTT overhead multiplier
FTT overhead:
  RAID-1 (FTT=1): 2× (each object stored twice)
  RAID-5 (FTT=1): 1.33× (4 data + 1 parity stripe; 33% overhead)
  RAID-6 (FTT=2): 1.5×  (4 data + 2 parity; 50% overhead)

Total raw storage = VM count × storage per VM × FTT multiplier
Add 30% slack: total_with_slack = total_raw / 0.70
Capacity per host = total_with_slack / host count
```

**Example (RAID-5, FTT=1):**
- 200 VMs × 200 GB = 40 TB usable
- × 1.33 RAID-5 overhead = 53.2 TB raw
- ÷ 0.70 (30% slack) = 76 TB total raw needed
- ÷ 6 hosts = 12.7 TB raw capacity per host
- Round up to 14 TB per host (e.g. 2× 7.68 TB NVMe SSDs per disk group)

### IOPS and Throughput Sizing

| Disk type | Typical sustained IOPS per disk | Notes |
|---|---|---|
| NVMe SSD (capacity, ESA) | 200,000–500,000 | Depends on queue depth and I/O size |
| SATA/SAS SSD (OSA capacity) | 50,000–100,000 | Lower throughput than NVMe |
| NVMe SSD (OSA cache) | 300,000+ | Cache layer absorbs writes; capacity IOPS matter for reads |

```text
Total IOPS needed = VM count × peak IOPS per VM × write amplification
Write amplification (RAID-1 FTT=1) = 2× (write goes to 2 hosts)
Write amplification (RAID-5 FTT=1) = ~1.33× (parity compute overhead)

IOPS per host = total IOPS / host count
Disk groups per host = IOPS per host / per-disk IOPS
```

For most all-flash vSAN deployments, IOPS is not the bottleneck — latency and capacity are. Only size for IOPS if running extremely latency-sensitive workloads (OLTP databases, NVMe-backed VDI).

### Reference Cluster Sizes

| Use case | Hosts | Config per host | Estimated usable capacity | Notes |
|---|---|---|---|---|
| Small production (FTT=1 RAID-5) | 4 | 2× 7.68 TB NVMe, 256 GB RAM | ~46 TB usable | Minimum for RAID-5 |
| Medium production (FTT=1 RAID-5) | 6 | 2× 7.68 TB NVMe, 512 GB RAM | ~70 TB usable | Recommended starting point |
| Large production (FTT=2 RAID-6) | 8 | 4× 7.68 TB NVMe, 768 GB RAM | ~164 TB usable | Tier-1 databases |
| ROBO 2-node | 2 + witness | 2× 3.84 TB NVMe, 128 GB RAM | ~7.7 TB usable | Branch office |
| ESA cluster | 4–8 | 4× 7.68 TB NVMe (no cache tier), 512 GB RAM | Varies | All-NVMe; simpler disk management |

### Scaling Rules

- **Scale out (add hosts):** preferred method. More hosts = more IOPS, more capacity, and better FTT coverage. Minimum increment: 1 host.
- **Scale up (add disks to existing hosts):** adds capacity only, not IOPS headroom. Useful for capacity-bound clusters.
- **Never scale below minimum FTT host count:** removing a host from a 4-node RAID-5 cluster breaks FTT=1 compliance for all objects.
- **Homogeneous hosts:** all hosts in a cluster should have identical disk configurations. Heterogeneous disk groups cause uneven utilisation and complicate capacity planning.

### vSAN Cluster Maximums (vSAN 8.x)

| Parameter | Maximum |
|---|---|
| Hosts per cluster | 64 |
| Disk groups per host (OSA) | 5 |
| Capacity disks per disk group (OSA) | 7 |
| VMs per cluster | 6,400 |
| Objects per cluster | 45,000 |
| Clusters per vCenter | 128 |

Do not size clusters close to these maximums — leave at least 20% headroom for growth and operational overhead.

## See also

- [vSAN — How It Works](how-it-works/)
- [vSAN — Deploy](../deploy/)
