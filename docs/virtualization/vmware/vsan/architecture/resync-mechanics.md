---
tags:
  - architecture
  - vmware
  - vsan
  - vsphere-8
---
# vSAN — Resync Mechanics

<div class="kb-summary">
Why vSAN resyncs happen, how CLOM decides when and where to rebuild, what drives resync throughput and duration, and the capacity headroom requirement that makes rebuilds possible.

*Applies to: vSAN 7.x · 8.x*
</div>

---

```d2
direction: down

why_resync_happens: "Why Resync Happens" {shape: rectangle}
how_clom_decides_where_to_rebuild: "How CLOM Decides Where to Rebuild" {shape: rectangle}
capacity_headroom_why_30_matters: "Capacity Headroom: Why 30% Matters" {shape: rectangle}
resync_duration_and_throughput: "Resync Duration and Throughput" {shape: rectangle}
the_throttle_trading_speed_for_vm_st: "The Throttle: Trading Speed for VM Stability" {shape: rectangle}
deltasync_vs_full_rebuild: "Delta-Sync vs Full Rebuild" {shape: rectangle}

why_resync_happens -> how_clom_decides_where_to_rebuild: uses
how_clom_decides_where_to_rebuild -> capacity_headroom_why_30_matters: uses
capacity_headroom_why_30_matters -> resync_duration_and_throughput: uses
resync_duration_and_throughput -> the_throttle_trading_speed_for_vm_st: uses
the_throttle_trading_speed_for_vm_st -> deltasync_vs_full_rebuild: uses
```

## Why Resync Happens

Resync is vSAN's mechanism for maintaining the data protection promises defined in storage policies. It runs whenever the current state of an object does not match its policy.

### Trigger 1 — Component Lost (Failure-Driven)

When a disk or host fails, some object components become ABSENT. After the `clomRepairDelay` timer expires (default 60 minutes), CLOM marks those components DEGRADED and schedules a rebuild on a healthy host.

This is the most common resync trigger. It is reactive — vSAN responds to an infrastructure failure.

**What gets rebuilt:** The missing component is created from scratch by reading data from the remaining healthy component(s) and writing it to a new location on a healthy host.

### Trigger 2 — Storage Policy Change

When you change a VM's storage policy (e.g. raise FTT from 1 to 2, switch from RAID-1 to RAID-5, or change stripe width), vSAN needs to create new components to satisfy the new policy and may need to move existing ones.

This is policy-driven resync. It runs against VMs that are powered on and running — the VM does not pause.

**Example:** A VM with FTT=1 RAID-1 (2 components + witness) is changed to FTT=2 RAID-6. CLOM must create 5 components (a 4+2 erasure code stripe) and rebuild all existing data into that layout.

### Trigger 3 — Rebalance

When a new host is added to the cluster or the distribution of components across hosts becomes uneven, vSAN rebalances by migrating components to equalise utilisation. This is proactive and non-urgent — it runs in the background with lower priority than failure-driven rebuilds.

Rebalance can also be triggered manually:

```bash
esxcli vsan cluster rebalance start
```


```text title="Expected output"
Rebalance operation started on cluster domain-c8.
Cluster UUID: 522e3d4a-1b2c-4d8f-9e7a-3c5b8f2a1d9e
Rebalance task ID: task-12847
Status: RUNNING
Estimated time remaining: 2 hours 15 minutes
Data to rebalance: 847.3 GB
Current throughput: 12.5 MB/s
```

!!! warning "Common errors"
    **`Error: VSAN cluster is not enabled on this host`** — Verify VSAN is enabled on all hosts in the cluster using `esxcli vsan cluster get`.
    **`Error: Rebalance operation already in progress`** — Wait for the current rebalance to complete or cancel it with `esxcli vsan cluster rebalance stop` before starting a new one.
    **`Error: Insufficient resources to start rebalance`** — Ensure all hosts in the cluster are in maintenance mode is not active and have adequate free capacity (minimum 30% recommended).
### Trigger 4 — Configuration Changes

Certain cluster-wide changes force a full or partial resync of all objects:

| Configuration change | Why resync runs |
|---|---|
| Enable deduplication + compression | All data must be rewritten in deduplicated form |
| Enable encryption at rest | All data must be re-encrypted onto capacity disks |
| On-disk format upgrade | Disk groups are reformatted host-by-host; data is migrated |
| Host enters maintenance mode (Full Migration) | All components on that host are evacuated to other hosts |

---

## How CLOM Decides Where to Rebuild

CLOM (Cluster Level Object Manager) runs on the cluster master host. It continuously monitors all objects and component states. When a rebuild is needed, CLOM follows this logic:

1. **Identify degraded objects** — scan all objects for components in DEGRADED or ABSENT-past-timer state.

2. **Find a placement target** — select a destination host and disk group that:
   - Has enough free capacity to hold the new component
   - Is not the same host as the remaining healthy component (for FTT=1 RAID-1, the two copies must be on different hosts)
   - Satisfies fault domain constraints (if fault domains are configured, components must span domains)
   - Has the lowest current utilisation among eligible targets (to balance load)

3. **Check capacity headroom** — if no eligible destination has enough free space, the rebuild is queued. The object remains DEGRADED until space is freed.

4. **Prioritise** — failure-driven rebuilds (DEGRADED) run before policy-change resyncs, which run before rebalance operations.

5. **Stream data** — CLOM instructs the DOM (Distributed Object Manager) to read from the healthy component and write to the new destination. I/O continues to the VM during the entire rebuild.

---

## Capacity Headroom: Why 30% Matters

The 30% free capacity rule exists because vSAN must be able to place a **complete new component** before removing the failed one. This is a copy-before-delete operation — vSAN does not overwrite.

**Scenario:** A 4-host cluster, each host has 10 TB raw capacity. Total usable capacity (FTT=1 RAID-1) ≈ 20 TB.

- If 18 TB is in use (90%): there is no room to place a replacement component. Any disk failure leaves objects permanently DEGRADED.
- If 14 TB is in use (70%): there is 6 TB free — enough for one component rebuild. Tight but workable.
- If 12 TB is in use (60%): comfortable headroom for rebuilds and a full host evacuation during maintenance.

**Alert thresholds:**

| Capacity used | Status | Action |
|---|---|---|
| < 60% | Healthy | Normal operations |
| 60–70% | Monitor | Plan capacity expansion |
| 70–75% | Warning | Alert — stop adding VMs until expanded |
| > 75% | Critical | Immediate risk — rebuild may fail if any disk fails |
| > 80% | Blocked | vSAN may refuse to write new data |

```bash
# Check cluster-wide capacity
esxcli vsan storage list | grep -E "Used Capacity|Total Capacity"
```

```powershell
# PowerCLI capacity check with percentage
$u = Get-VsanSpaceUsage -Cluster (Get-Cluster "VSAN-LON-01")
[Math]::Round($u.UsedCapacityGB / $u.TotalCapacityGB * 100, 1)
```

---

## Resync Duration and Throughput

How long a rebuild takes depends on three factors: component size, network bandwidth, and disk write throughput at the destination.

### Component size

A RAID-1 rebuild copies 100% of the object's data. A RAID-5 or RAID-6 rebuild copies only the stripe portions — typically smaller per object but more compute-intensive.

**Rule of thumb:** Expect 50–100 MB/s of resync throughput per host with 25 GbE NICs and NVMe disks. A 1 TB object takes 3–6 hours under typical production load.

### Network bottleneck

Resync I/O travels over the vSAN VMkernel network. On a 10 GbE cluster, available resync bandwidth (shared with VM I/O) may be as low as 500 MB/s cluster-wide. On 25 GbE clusters, this is rarely the bottleneck.

### Disk write throughput

The destination disk's sequential write throughput limits rebuild speed. NVMe SSDs (ESA or OSA all-flash) are rarely the bottleneck. Hybrid clusters (HDD capacity disks) can limit rebuild to 100–200 MB/s per disk.

### Estimating rebuild time

```bash
# Get current resync queue
esxcli vsan debug resync summary get
# Shows: bytes remaining + current throughput → estimate ETA
```


```text title="Expected output"
Cluster UUID: 52e8f4c1-7a2b-4d9e-b1a3-8c6f2e9d1b4a
Resync Queue Summary:
  Total bytes to resync: 847.3 GB
  Bytes remaining: 412.7 GB
  Current throughput: 156.2 MB/s
  Estimated time to completion: 44 minutes 23 seconds
  Active resync objects: 1247
  Completed objects: 3891
  Failed objects: 0
  Resync rate: 98.7%
```

!!! warning "Common errors"
    **`Error: Unknown command or namespace vsan debug resync`** — Verify vSAN is licensed and enabled on the host with `esxcli vsan cluster get`, and ensure you are running ESXi 6.5 or later.
    **`Error: Permission denied`** — Run the command with root privileges or ensure your user account has vSAN administrator role assigned in vCenter.
    **`Error: VSAN is not enabled on this host`** — Enable vSAN on the host through vCenter UI or confirm the host is part of an active vSAN cluster with `esxcli vsan cluster get`.
---

## The Throttle: Trading Speed for VM Stability

The resync throttle limits the IOPS consumed by rebuild operations per host. It protects VM performance during production hours at the cost of slower recovery.

```bash
# Check current throttle
esxcli vsan debug resync throttle get

# Set to 500 IOPS per host (business-hours safe)
esxcli vsan debug resync throttle set --throttle 500

# Remove throttle — run at full speed (maintenance windows)
esxcli vsan debug resync throttle set --throttle 0
```


```text title="Expected output"
Current resync throttle setting: 100 IOPS
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: Unknown command or namespace vsan debug resync`** — Verify the ESXi host is vSAN-enabled and running vSAN 6.6 or later; check with `esxcli vsan cluster get`.
    **`Error: Invalid --throttle value: 500. Must be between 0 and 100000`** — Adjust the throttle value to fall within the valid range (typically 0–100000 IOPS depending on vSAN version).
**Recommended schedule:**

| Time | Throttle | Rationale |
|---|---|---|
| Business hours (9–17) | 500 IOPS | Protect VM latency |
| Off-hours / weekend | 0 (unlimited) | Complete rebuilds before business hours |
| During P1 (data at risk) | 0 regardless | Fast recovery trumps performance |

**Important:** A throttled resync extends the window during which the cluster has reduced redundancy. A DEGRADED object under a 500-IOPS throttle might take 3× longer to rebuild. If another failure occurs during that window, you have a data loss event.

If a disk has failed and FTT=1 objects are DEGRADED, set throttle to 0 and accept the I/O impact.

---

## Delta-Sync vs Full Rebuild

Not all resyncs copy the full object. vSAN distinguishes between two resync types:

### Full rebuild (DEGRADED component)

The original component is gone — the data must be copied in full from the remaining healthy copy to a new location. The entire object size is transmitted over the network.

### Delta-sync (STALE component)

The component still exists on its original disk (host was offline temporarily), but it missed some writes. Only the changed blocks need to be copied — this is significantly faster.

**How vSAN tracks what changed:** When a write is committed to a RAID-1 object, a per-block dirty bitmap is maintained for each component. When a host reconnects, CLOM uses the dirty bitmap to send only the changed blocks.

```bash
# Resync list shows operation type
esxcli vsan debug resync list
# Look for "type" field: DELTA vs FULL
```


```text title="Expected output"
Resync UUID                          Object UUID                      Type  Progress
52a4c8f1-7e3a-4d2b-9f1c-3b8a2c5d9e1f 6f2d1a4c-8b3e-5f9c-2a7d-1e4b3c8f5a9d DELTA 45%
7c9e2f3a-1b5d-8a4c-6e2f-9d3a1c5b7e8f a1f4c7e2-3b9d-5a8c-1f6e-4d2a7c9b3e5f DELTA 78%
9f1c3e5a-2d7b-4a8f-6c1e-3b9d5f2a7c4e c5a2f8d1-7e3b-9c4a-2f6d-8a1e5b3c7f9d FULL 12%
3d6a1f8c-5e2b-9a4d-7c3f-1e8b2a5d9c6f 2e7a4f1c-9b3d-6a8e-5c2f-1d4a7b9e3c6f DELTA 92%
1a4c7e9f-3b2d-8f5a-6e1c-4d9b2f3a7c5e 8f2c5a9d-1e7b-4f3a-6c8d-2a9e1b5f3c7d DELTA 56%
```
```text

!!! warning "Common errors"
    **`error: Unknown command or namespace`** — Ensure you are running this command on an ESXi host with vSAN enabled; the vsan namespace may not be available on non-vSAN clusters.
    **`error: Unable to connect to the local vSAN cluster`** — Verify the host is part of an active vSAN cluster and has network connectivity to other cluster members.
Delta-sync is why a host that returns from a short reboot syncs in minutes, while a replacement disk might take hours — even if the object sizes are identical.

---

## Resync and the Stretched Cluster

In a stretched cluster, resync has an additional dimension: **site preference**. CLOM prefers to rebuild components within the preferred site first, then the secondary site.

During an inter-site network partition:
- The preferred site + witness have quorum → VMs continue
- Components on the isolated site become ABSENT
- After `clomRepairDelay`, CLOM rebuilds those components on the preferred site
- When the partition resolves, CLOM must re-synchronise the isolated site back

This can trigger large resync volumes after a site partition event. Monitor inter-site bandwidth carefully — the vSAN stretched cluster replication link carries both VM write traffic and resync traffic.

```bash
# Check inter-site resync specifically (stretched cluster)
esxcli vsan debug resync list | grep -i "remote\|site"
```


```text title="Expected output"
RemoteSyncProgress: 98.5%
RemoteSiteLatency: 12.3ms
RemoteSyncObjects: 1247
RemoteSyncRate: 45.2 MB/s
RemoteSiteStatus: CONNECTED
RemoteSyncETA: 2h 14m
RemoteSyncErrors: 0
```

!!! warning "Common errors"
    **`Unknown command or namespace vsan debug resync`** — Verify vSAN is licensed and enabled on the cluster; run `esxcli vsan cluster get` to confirm vSAN status.
    **`grep: (standard input) is empty`** — The command executed but returned no results; this typically means no active remote resync is occurring, which is normal during steady state.