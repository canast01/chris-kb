---
tags:
  - architecture
  - vmware
  - vsan
  - vsphere-8
---
# vSAN — Component States

<div class="kb-summary">
How vSAN classifies each object component's health — from the initial ABSENT state through DEGRADED and STALE to REBUILDING — and what each state means operationally for data protection and admin action.

*Applies to: vSAN 7.x · 8.x*
</div>

---

## The Four Operational States

### ABSENT

**What it means:** The component's host or disk group is temporarily unreachable. The data is not confirmed lost — vSAN does not yet know if the host will return.

**When it happens:**
- Host rebooted (e.g. patching, driver update)
- Network partition isolating the host
- Host put into maintenance mode with Ensure Accessibility (not Full Migration)
- Temporary power interruption to a single host

**What vSAN does:** Nothing yet. The `clomRepairDelay` timer starts counting. Default is 60 minutes.

**What you should do:** If the outage is planned and short (reboot, patch), do nothing — let the timer run. If the host doesn't return within the timer window, investigate.

```bash
# Check for absent components
esxcli vsan debug component list | grep -i absent

# Check which objects own absent components
esxcli vsan debug object list | grep -i absent
```


```text title="Expected output"
Name                                    Health Status
vsan-health-check-vsan-cluster-health   absent
vsan-health-check-vsan-physical-disk    absent
vsan-health-check-vsan-object-health    absent

Object UUID                              Owner Node    Status
52e4c8f1-a2b4-4d7e-9c1f-8b3a2e5d6f9a   esx-node-02   absent
7f9d2c1e-5a3b-4c6d-8e9f-1a2b3c4d5e6f   esx-node-04   absent
```

!!! warning "Common errors"
    **`grep: (standard input): No such file or directory`** — Verify the ESXi host is vSAN-enabled and the vSAN service is running with `systemctl status vsanvpd`.
    **`Error: Unknown command or namespace vsan.debug`** — Ensure you are running the command on a vSAN cluster member; this command is not available on non-vSAN hosts.
**Risk during ABSENT:** The object is running with reduced redundancy but is fully accessible. One more failure of a different component means data loss (for FTT=1 objects). For FTT=2, one absent + one degraded still leaves the object accessible.

---

### DEGRADED

**What it means:** The component is confirmed lost. Either the `clomRepairDelay` timer expired without the host returning, or the disk failed permanently. vSAN now knows it needs to create a replacement component.

**When it happens:**
- `clomRepairDelay` timer expires and host has not returned
- Disk group failed (cache SSD or multiple capacity disk failures)
- Disk marked as failed via the vSAN UI or CLI
- Host permanently removed from the cluster

**What vSAN does:** CLOM schedules a rebuild. It selects a target host and disk group with sufficient free capacity to place the new component. The object transitions to REBUILDING.

**What you should do:** Monitor resync. If the rebuild does not start within 5–10 minutes of the state changing to DEGRADED, check capacity headroom and cluster health.

```bash
# List degraded objects
esxcli vsan debug object list | grep -i degraded

# Check resync queue — rebuild should appear here
esxcli vsan debug resync summary get

# Check capacity — rebuild requires free space
esxcli vsan storage list | grep -E "Used Capacity|Free Capacity"
```


```text title="Expected output"
Object UUID                          Health State      Policy
52a4c8f1-7d2e-4a9c-b1e3-9f2c6d8a1b3c Degraded         raid1
7c9e3f2a-1b4d-8c6e-9a2f-5d3c1e8b4a7f Degraded         raid5
a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6 Degraded         raid1

Resync Queue Summary:
  Total objects to resync: 3
  Objects currently resyncing: 1
  Estimated time remaining: 45 minutes
  Resync rate: 125 MB/s

Used Capacity: 2.8 TB
Free Capacity: 1.2 TB
```

!!! warning "Common errors"
    **`grep: (standard input): No such file or directory`** — Ensure vSAN is enabled on the cluster and the ESXi host is part of a vSAN cluster; run `esxcli vsan cluster get` to verify.
    **`Error: Unknown command or namespace`** — Update ESXi to a supported version that includes the vsan debug command set, or verify vSAN license is active.
    **`Resync Queue Summary: (empty)`** — This is normal if no objects are degraded; check actual object health with `esxcli vsan object list` to confirm cluster state.
**Risk during DEGRADED:** The object has zero redundancy for FTT=1. Any further failure of the remaining component causes data loss and the object becomes INACCESSIBLE. Treat all DEGRADED objects as P1 until rebuild completes.

---

### STALE

**What it means:** The component exists on a healthy disk, but its data is behind. The host was offline or partitioned while writes occurred to other copies of the object. When the host reconnects, the component needs to catch up before it can serve reads.

**When it happens:**
- Host returns after a brief outage during which the VM was still running
- Network partition resolved — the host was isolated but the cluster continued operating
- Host exits maintenance mode (Ensure Accessibility mode — data was not fully migrated)

**What vSAN does:** CLOM schedules a delta-sync — only the changed blocks need to be copied, not the full object. This is significantly faster than a full rebuild.

**What you should do:** Wait. STALE components resolve automatically via delta-sync. Do not remove the disk or the host while sync is in progress.

```bash
# STALE components appear in resync list
esxcli vsan debug resync list | grep -i stale

# Monitor delta-sync completion
watch -n 30 "esxcli vsan debug resync summary get"
```


```text title="Expected output"
STALE components appear in resync list
Object UUID: 52e4f1a8-7c3a-4d92-b1e2-9f8c6d2a1b4e, Component UUID: a3b2c1d0-e5f4-4a3b-9c8d-7e6f5a4b3c2d, Status: STALE
Object UUID: 7f6e5d4c-3b2a-1a0f-9e8d-7c6b5a4f3e2d, Component UUID: b4c3d2e1-f6a5-5b4c-0d9e-8f7a6b5c4d3e, Status: STALE
Object UUID: 1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d, Component UUID: c5d4e3f2-a7b6-6c5d-1e0f-9a8b7c6d5e4f, Status: STALE

Every 30.0s: esxcli vsan debug resync summary get
```
**Risk during STALE:** The object remains accessible — reads go to the up-to-date copies while the STALE component syncs. Protection is temporarily reduced (similar to DEGRADED) but recovery is faster because data already exists on the disk.

---

### REBUILDING

**What it means:** vSAN is actively writing a new component to replace a DEGRADED one. Data is being copied from the healthy component(s) to a new location.

**When it happens:**
- After a DEGRADED state triggers CLOM to schedule a rebuild
- After policy change (e.g. FTT increase requires additional components)
- After rebalance operation moves a component to a different host

**What vSAN does:** Copies data from remaining healthy components to the new target location. During rebuild, I/O continues normally — the VM is not paused. However, rebuild I/O competes with VM workload I/O.

**What you should do:** Monitor progress. Do not perform further changes to the cluster (adding/removing hosts or disks) until rebuild completes.

```bash
# Monitor rebuild progress
esxcli vsan debug resync summary get
# Shows: Active resyncing components, bytes remaining, estimated time

# Detailed per-object rebuild status
esxcli vsan debug resync list
```


```text title="Expected output"
Active Resyncing Components: 12
Bytes Remaining: 847.3 GB
Estimated Time Remaining: 2h 14m
Resync Rate: 104.5 MB/s
Objects Being Resynced: 8
Cluster UUID: 52d4a8f0-7c2a-4d91-b3e2-1a9c8f7e6d5b

Object UUID                              Object Name          Bytes Remaining  Progress
52d4a8f0-7c2a-4d91-b3e2-1a9c8f7e6d5b    vm-prod-01.vmdk      156.2 GB         45%
7f3e1b9c-8d2a-4f91-c3e2-2b0d9g8f7e6c    vm-prod-02.vmdk      203.5 GB         32%
8g4f2c0d-9e3b-5g02-d4f3-3c1e0h9g8f7d    vm-backup-01.vmdk    187.8 GB         28%
9h5g3d1e-0f4c-6h13-e5g4-4d2f1i0h9g8e    vm-test-01.vmdk      124.6 GB         61%
0i6h4e2f-1g5d-7i24-f6h5-5e3g2j1i0h9f    vm-dev-01.vmdk       175.2 GB         38%
...
```

!!! warning "Common errors"
    **`vsan cluster is not healthy`** — Verify all hosts are online and network connectivity is stable with `esxcli vsan cluster get`.
    **`Permission denied`** — Run the command with root privileges or ensure your vSphere user has the required VSAN administrator role.
**Throttle rebuild during business hours:**

```bash
# Limit rebuild to 500 IOPS (reduce VM impact)
esxcli vsan debug resync throttle set --throttle 500

# Remove throttle during off-hours for faster completion
esxcli vsan debug resync throttle set --throttle 0
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: Unknown command or namespace vsan debug resync`** — Verify vSAN is licensed and enabled on the cluster; this command requires vSAN to be active on the host.
    **`Error: The object or item could not be found`** — Ensure the ESXi host is part of a vSAN cluster; standalone hosts do not support vSAN resync throttling commands.
**Risk during REBUILDING:** Same as DEGRADED — the object still has only one copy until the rebuild completes. Do not perform any maintenance on other hosts during a rebuild unless it is unavoidable.

---

## State Transition Diagram

```text
                    Host rebooted / network partition
                              │
                              ▼
                          ABSENT
                     (clomRepairDelay timer)
                         /          \
              Host returns        Timer expires
              (< 60 min)          (default 60 min)
                  │                      │
                  ▼                      ▼
               HEALTHY             DEGRADED
                                        │
                              CLOM schedules rebuild
                                        │
                                        ▼
                                  REBUILDING
                                        │
                              Rebuild completes
                                        │
                                        ▼
                                    HEALTHY

Host returns after write-divergence:
    ABSENT → (reconnect) → STALE → (delta-sync) → HEALTHY
```

---

## The clomRepairDelay Timer

`clomRepairDelay` is the number of minutes vSAN waits after a component goes ABSENT before treating it as DEGRADED and triggering a rebuild.

**Default:** 60 minutes

**Why it exists:** Unnecessary rebuilds waste I/O bandwidth and increase resync time. If a host reboots for a patch and returns in 20 minutes, there is no point triggering a full rebuild. The timer prevents that.

**Trade-off:** A longer timer means the cluster runs in a reduced-protection state for longer. If a second failure happens during the wait, the object becomes INACCESSIBLE.

**Recommended values:**

| Environment | Value | Rationale |
|---|---|---|
| Standard production | 60 min | Default — balanced between unnecessary rebuild and protection window |
| Frequent rolling reboots (patch cycles) | 120–180 min | Avoid rebuild churn during planned maintenance |
| High-value data (databases) | 30 min | Shorter protection window; accept more rebuild I/O |
| Never exceed | 240 min | Risk of 4-hour unprotected window is too high |

**Adjust the timer:**

```bash
# View current value
esxcli vsan cluster get | grep -i repair

# Set via vCenter UI
# Cluster → Configure → vSAN → Advanced Options → clomRepairDelay
```


```text title="Expected output"
Repair Delay (seconds): 60
Repair Timer: enabled
Automatic Repair: true
```

!!! warning "Common errors"
    **`Error: Unknown command or namespace vsan`** — Ensure vSAN is licensed and enabled on the cluster, and run the command on an ESXi host that is part of the vSAN cluster.
    **`Error: Could not connect to the vSAN cluster`** — Verify the host has network connectivity to other cluster members and that vSAN clustering is properly initialized with `esxcli vsan cluster list`.
---

## When Objects Become INACCESSIBLE

INACCESSIBLE is not a component state — it is an object-level state that occurs when there are no accessible copies of a component remaining. The VM stops responding to I/O.

**Causes:**
- FTT=1 object: both copies become unavailable simultaneously (two host failures, network partition splitting both copies off)
- FTT=1 stretched cluster: both sites go down (witness alone cannot serve data)
- Majority of components absent/degraded simultaneously before rebuild completes

**Immediate response:**
1. Do not reboot or power-cycle hosts — the data is likely still on disk.
2. Check which hosts are unreachable and restore connectivity first.
3. If a host hardware failure caused it, restore the host rather than immediately decommissioning.
4. If data is genuinely lost, restore from backup.

```bash
# Identify inaccessible objects
esxcli vsan debug object list | grep -i inaccessible

# Check which components are involved
esxcli vsan debug component list | grep -i inaccessible
```


```text title="Expected output"
Object UUID                              Inaccessible Components
52a4c8f1-2b3e-4a9c-b1d2-7f8e9c0a1b2c    1
7c9d1e2f-3a4b-5c6d-7e8f-9a0b1c2d3e4f    2
9f0a1b2c-3d4e-5f6a-7b8c-9d0e1f2a3b4c    3

Component UUID                           Inaccessible Count
a1b2c3d4-e5f6-7a8b-9c0d-1e2f-3a4b5c6d   1
d4e5f6a7-b8c9-d0e1-f2a3-b4c5-d6e7f8a9   2
```

!!! warning "Common errors"
    **`grep: (standard input): No such file or directory`** — Verify the VSAN cluster is healthy and the ESXi host has VSAN enabled by running `esxcli vsan cluster get`.
    **`Unknown command or namespace`** — Ensure you are running this command on a VSAN-enabled ESXi host with VSAN service running; check with `esxcli vsan cluster get`.
Escalate immediately to VMware GSS for any inaccessible object state — see Troubleshooting → Escalation.
