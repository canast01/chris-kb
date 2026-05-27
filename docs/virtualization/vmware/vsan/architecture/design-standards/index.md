# vSAN — Design Standards

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

**Switch configuration requirements:**

| Setting | Value |
|---|---|
| MTU | 9000 (jumbo frames) — switch, vDS, and vmk must all match |
| Port type | Access (not trunk) for vSAN VLAN |
| Flow control | Disabled (vSAN handles congestion internally) |
| Spanning Tree | PortFast / Edge Port on all vSAN-connected ports |

**vDS port group settings for vSAN VMkernel:**

- VLAN: dedicated VLAN (not shared with vMotion or management)
- Load balancing: Route based on physical NIC load (or LACP if supported)
- Failover order: Active-Active if two pNICs dedicated to vSAN

**Bandwidth sizing guidance:**

| Traffic type | Minimum | Recommended |
|---|---|---|
| vSAN replication (per host) | 10 GbE | 25 GbE |
| ESA (NVMe-based) | 25 GbE | 25 GbE or 2×10 GbE LACP |
| Stretched cluster inter-site | 10 GbE | 25 GbE + < 5 ms RTT |

---

## Stretched Cluster Architecture

A vSAN stretched cluster spans two physical sites with a witness at a third location. Each site is a fault domain. FTT=1 RAID-1 places one mirror at each site, with the witness providing quorum arbitration.

```text
Site A (preferred)          Site B (secondary)
┌─────────────────┐         ┌─────────────────┐
│ ESXi-01         │         │ ESXi-03         │
│ ESXi-02         │         │ ESXi-04         │
│ Component A ────┼─────────┼──► Component B  │
└─────────────────┘         └─────────────────┘
         │                          │
         └──────────┬───────────────┘
                    │
              ┌─────┴──────┐
              │  Witness    │
              │ (Site C /  │
              │  vCloud)   │
              └────────────┘
```

**Stretched cluster requirements:**

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
