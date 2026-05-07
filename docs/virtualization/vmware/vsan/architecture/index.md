# VMware vSAN Architecture
## vSAN Cluster Topology

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                         vSAN Cluster (3-host minimum)                   │
  │                                                                          │
  │  ┌───────────────────────┐  ┌───────────────────────┐  ┌─────────────── │
  │  │       ESXi-01         │  │       ESXi-02         │  │  ESXi-03       │
  │  │  ┌─────┐  ┌────────┐  │  │  ┌─────┐  ┌────────┐  │  │  ┌─────┐  ┌── │
  │  │  │Cache│  │Capacity│  │  │  │Cache│  │Capacity│  │  │  │Cache│  │Ca │
  │  │  │NVMe │  │SSD/NL  │  │  │  │NVMe │  │SSD/NL  │  │  │  │NVMe │  │SS │
  │  │  └──┬──┘  └───┬────┘  │  │  └──┬──┘  └───┬────┘  │  │  └──┬──┘  └── │
  │  │     └────┬────┘       │  │     └────┬────┘       │  │     └────┬──── │
  │  │    Disk Group 1       │  │    Disk Group 1       │  │    Disk Group 1 │
  │  │  vmnic0  vmnic1       │  │  vmnic0  vmnic1       │  │  vmnic0  vmnic1 │
  │  └────┬────────┬─────────┘  └────┬────────┬─────────┘  └────┬────────┬─ │
  └───────┼────────┼─────────────────┼────────┼─────────────────┼────────┼──┘
          │        │                 │        │                 │        │
  ┌───────▼────────▼─────────────────▼────────▼─────────────────▼────────▼──┐
  │             vSAN VMkernel Network (dedicated 10/25 GbE VLAN)            │
  │              [object components distributed across all hosts]           │
  └──────────────────────────────────────────────────────────────────────────┘

  FTT=1 (RAID-1): object has 2 data replicas + 1 witness — survives 1 host loss
  FTT=1 (RAID-5): 4+ hosts required — more space-efficient than RAID-1
  FTT=2 (RAID-6): 6+ hosts required — survives 2 concurrent host failures
```

<div class="kb-grid kb-grid-15">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>esxcli vsan, disk groups, object health, resync, PowerCLI, and RVC commands.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Skyline health, cluster checks, object health, capacity, and policy compliance.</span>
</a>

<a class="kb-card" href="resync-rebuild/">
  <strong>Resync and Rebuild</strong>
  <span>Resync review, rebuild behavior, impact checks, and operational handling.</span>
</a>

<a class="kb-card" href="field-reference/">
  <strong>Field Reference</strong>
  <span>Architecture, dependencies, ports, daily checks, recovery notes, and RCA examples.</span>
</a>

<a class="kb-card" href="technical-deep-dive/">
  <strong>Technical Deep Dive</strong>
  <span>Components, logs, commands, failure points, resync, and upgrade notes.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>PowerCLI vSAN health check, disk group report, RVC diagnostics, and Ansible vSAN playbook.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Daily checks, health check, change readiness, incident triage, maintenance window, and post-change validation.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Resync review, object health, disk group failures, and vSAN recovery procedures.</span>
</a>


<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>Architecture overview, components, and design patterns.</span>
</a>

<a class="kb-card" href="disk-groups/">
  <strong>Disk Groups</strong>
  <span>Disk Groups notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="integration/">
  <strong>Integration</strong>
  <span>Integration with other systems and platforms.</span>
</a>

<a class="kb-card" href="lifecycle/">
  <strong>Lifecycle</strong>
  <span>Installation, upgrades, patching, and decommission.</span>
</a>

<a class="kb-card" href="performance/">
  <strong>Performance</strong>
  <span>Performance monitoring, tuning, and baselining.</span>
</a>

<a class="kb-card" href="standards/">
  <strong>Standards</strong>
  <span>Configuration standards, naming conventions, and baselines.</span>
</a>

<a class="kb-card" href="storage-policies/">
  <strong>Storage Policies</strong>
  <span>Storage Policies notes, checks, commands, and references.</span>
</a>
</div>

## Overview

vSAN is VMware's hyper-converged storage solution, introduced in vSphere 5.5. Unlike traditional shared storage, vSAN pools local disks across ESXi hosts to create a distributed shared datastore. Compute and storage run on the same ESXi hosts, eliminating the need for an external SAN or NAS.

The vSAN datastore is presented as a single shared storage namespace to all hosts in the vSAN cluster. VMs on any host in the cluster can access any object on the datastore because vSAN handles replication and distribution transparently.

vSAN is policy-driven: each VM's storage characteristics (availability, performance, capacity) are defined by a VM Storage Policy assigned at provisioning time.

## Components

| Component | Description |
|---|---|
| **Disk Group** | Unit of storage on each host: one cache device + one or more capacity devices (OSA). ESA uses NVMe only with no separate cache tier. |
| **CLOM** | Cluster Level Object Manager — responsible for policy compliance, placement decisions, and triggering resyncs when policy is violated. |
| **DOM** | Distributed Object Manager — handles I/O for each vSAN object; coordinates reads and writes across components on different hosts. |
| **LSOM** | Local Log-Structured Object Manager — manages on-disk layout within disk groups; handles write buffering on cache tier. |
| **CMMDS** | Cluster Monitoring Membership Directory Service — tracks cluster membership, disk group membership, and health metadata. |
| **vSAN Datastore** | The logical datastore namespace visible to vCenter and all cluster hosts. |
| **vSAN Witness** | A lightweight host or appliance that holds only metadata for 2-node clusters to provide tiebreaker arbitration. |

## Disk Group Design

**Original Storage Architecture (OSA) — vSAN 6.x and 7.x:**

- Each disk group consists of 1 cache SSD (write buffer and read cache) and up to 7 capacity drives (SSD or HDD).
- Each host can have up to 5 disk groups.
- All-Flash (AF) configurations: cache tier is SSD, capacity tier is SSD — cache used for write buffering only.
- Hybrid configurations: cache tier is SSD, capacity tier is HDD — cache used for both read caching and write buffering.

**Express Storage Architecture (ESA) — vSAN 8.0+:**

- NVMe-only architecture; no separate cache tier.
- Each NVMe device contributes directly to capacity with built-in compression and a log-structured layout.
- Minimum 4 hosts required.
- Higher throughput and lower latency compared to OSA.
- Requires NVMe devices on the vSAN HCL for ESA.

## FTT and RAID Policies

vSAN storage policies define the Failures To Tolerate (FTT) and the RAID method used for data protection.

| FTT | RAID Method | Minimum Hosts | Space Overhead | Notes |
|---|---|---|---|---|
| 1 | RAID-1 (Mirroring) | 3 | 2x | Default; suitable for most workloads |
| 1 | RAID-5 (Erasure Coding) | 4 | 1.33x | More efficient; higher CPU and network overhead |
| 2 | RAID-6 (Erasure Coding) | 6 | 1.5x | Best capacity efficiency for FTT=2 |
| 2 | RAID-1 (Mirroring) | 5 | 3x | Maximum redundancy; least capacity efficient |
| 3 | RAID-1 (Mirroring) | 7 | 4x | Rarely used; extreme environments |

Erasure Coding (RAID-5/6) is only supported on All-Flash and ESA configurations. Choose RAID-5 (FTT=1) or RAID-6 (FTT=2) for capacity-sensitive workloads where the additional CPU overhead is acceptable.

## Stretched Cluster

A vSAN Stretched Cluster spans two active data sites with a third witness site:

- **Site A and Site B:** Both sites host production VMs and hold RAID-1 mirrors of each VM object. Both sites are active simultaneously.
- **Witness Site:** Holds only metadata components (no VM data). Acts as tiebreaker if Site A and Site B lose communication (split-brain prevention).

**Network requirements:**

| Link | Maximum Latency |
|---|---|
| Site A to Site B (data sites) | < 5 ms RTT |
| Data sites to Witness | < 200 ms RTT |

The witness can be a physical host or the vSAN Witness Appliance (virtual). The witness appliance can run on a third site's vSphere infrastructure.

In a stretched cluster, the default FTT policy becomes 1 across sites. An FTT=1 RAID-1 policy means one copy per site.

## Sizing Guidelines

**Capacity planning:**

```
Usable capacity = (Raw capacity) / (Space overhead factor × slack factor)
```

- Slack factor: reserve 30% for resync, snapshots, and operational headroom.
- Example: 6-host cluster, 4 × 3.84TB NVMe per host, FTT=1 RAID-5:
  - Raw = 6 × 4 × 3.84 = 92.16 TB
  - Usable ≈ 92.16 / (1.33 × 1.43) ≈ 48.5 TB effective

**CPU overhead:**

- OSA: approximately 10% CPU overhead per host for vSAN operations.
- ESA: slightly higher initial overhead due to inline compression, but improved I/O efficiency.

**Memory:**

- Reserve 32 GB RAM minimum per host for vSAN kernel modules and cache structures.
- ESA requires 512 GB RAM for optimal performance at scale.

**Network:**

- Minimum 10 GbE for all-flash OSA clusters.
- 25 GbE recommended for ESA or high-throughput workloads.
- MTU 9000 (jumbo frames) required on vSAN network.
