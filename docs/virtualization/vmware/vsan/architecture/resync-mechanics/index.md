# vSAN — Resync Mechanics

<div class="kb-summary">
Why vSAN resyncs happen, how CLOM decides when and where to rebuild, what drives resync throughput and duration, and the capacity headroom requirement that makes rebuilds possible.
</div>

```text
┌─────────────────────────────────────── vSAN — Resync Mechanics ───────────────────────────────────────┐
│                                                                                                       │
│  Resync is vSAN rebuilding or rebalancing component data. Every disk replacement, host failure,       │
│  policy change, or rebalance triggers it. Understanding resync mechanics prevents surprises.          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Why Resync Triggers              │  │               How CLOM Decides              │   │
│   │           Component goes DEGRADED            │  │          Scan all degraded objects          │   │
│   │            Storage policy changes            │  │     Find host + disk with free capacity     │   │
│   │            Host added (rebalance)            │  │        Check FTT policy requirements        │   │
│   │           Dedup/encryption enabled           │  │         Schedule rebuild operations         │   │
│   │            On-disk format upgrade            │  │       Prioritise by object criticality      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Resync competes with VM I/O for disk and network bandwidth on all participating hosts.               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Bandwidth and Duration            │  │            Capacity Headroom Rule           │   │
│   │      Throughput limited by slowest disk      │  │         30% free required to rebuild        │   │
│   │     Network bottleneck on small clusters     │  │       Without headroom: resync queued       │   │
│   │        Throttle: 0 = unlimited (fast)        │  │    Over-commit blocks all future rebuilds   │   │
│   │      Throttle: 500 IOPS = business-safe      │  │       Alert at 70%; hard stop near 80%      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Resync I/O travels over the vSAN VMkernel network (25 GbE recommended); disk throughput              │
│  on destination host limits rebuild speed; CLOM runs on the cluster master host.                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CLOM           = Cluster Level Object Manager; schedules and tracks all rebuild operations           │
│  DOM            = Distributed Object Manager; handles per-object I/O and component writes             │
│  Resync         = the actual data copy operation from source to destination component                 │
│  Delta-sync     = partial resync for STALE components — only changed blocks, not full copy            │
│  Throttle       = IOPS limit applied to resync I/O; 0 = unlimited; 500 = production-safe              │
│  Headroom       = free capacity needed to place the new component before old is removed               │
│  Rebalance      = proactive move of components to equalise utilisation across hosts                   │
│  Policy resync  = triggered by FTT change, stripe width change, or dedup/encrypt toggle               │
│  clomRepairDelay= minutes between component going ABSENT and CLOM starting rebuild                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

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
