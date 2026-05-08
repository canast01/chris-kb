# vSAN — Procedures

## Disk Groups

Disk group health, cache/capacity devices, failures, and replacement notes.

### Daily Checks

| Check | Command | Notes |
|---|---|---|
| Review active alarms. |  |  |
| Check recent failed tasks. |  |  |
| Confirm service health. |  |  |
| Confirm capacity and performance are normal. |  |  |
| Check recent changes. |  |  |

### Health Commands

```bash
# Add environment-specific commands here
```

### Common Issues

- Failed or stuck tasks.
- Certificate, DNS, or authentication issues.
- Capacity pressure.
- Service health warnings.
- Version mismatch after maintenance.
- Monitoring gaps.

### Operational Tasks

| Task | Command |
|---|---|
| Review alarms and events. |  |
| Confirm ownership and support notes. |  |
| Validate dependencies. |  |
| Document changes. |  |
| Confirm monitoring coverage. |  |

### Upgrade Notes

- Confirm compatibility.
- Review known issues.
- Confirm rollback plan.
- Validate health before and after the change.

### Best Practices

| Recommendation | Detail |
|---|---|
| Keep naming consistent. | Keep naming consistent. |
| Keep versions aligned. | Keep versions aligned. |
| Avoid unsupported version combinations. | Avoid unsupported version combinations. |
| Document exceptions. | Document exceptions. |
| Validate after every change. | Validate after every change. |

---

## Storage Policies

Policy design, compliance checks, failures to tolerate, and object placement.

### Daily Checks

| Check | Command | Notes |
|---|---|---|
| Review active alarms. |  |  |
| Check recent failed tasks. |  |  |
| Confirm service health. |  |  |
| Confirm capacity and performance are normal. |  |  |
| Check recent changes. |  |  |

### Health Commands

```bash
# Add environment-specific commands here
```

### Common Issues

- Failed or stuck tasks.
- Certificate, DNS, or authentication issues.
- Capacity pressure.
- Service health warnings.
- Version mismatch after maintenance.
- Monitoring gaps.

### Operational Tasks

| Task | Command |
|---|---|
| Review alarms and events. |  |
| Confirm ownership and support notes. |  |
| Validate dependencies. |  |
| Document changes. |  |
| Confirm monitoring coverage. |  |

### Upgrade Notes

- Confirm compatibility.
- Review known issues.
- Confirm rollback plan.
- Validate health before and after the change.

### Best Practices

| Recommendation | Detail |
|---|---|
| Keep naming consistent. | Keep naming consistent. |
| Keep versions aligned. | Keep versions aligned. |
| Avoid unsupported version combinations. | Avoid unsupported version combinations. |
| Document exceptions. | Document exceptions. |
| Validate after every change. | Validate after every change. |

---

## Resync and Object Health

### Checking Resync Status

```bash
# From an ESXi host in the cluster
esxcli vsan debug resync summary get
```

Or in vCenter: **vSAN** → **Skyline Health** → **Data** → **vSAN Object Health**

### Understanding Resync Types

| Type | Meaning |
|---|---|
| Repair | Rebuilding a component after a failure |
| Rebalance | Redistributing data after capacity or host changes |
| Evacuation | Migrating data for maintenance mode |
| Policy change | Applying a new storage policy |

### When Resync Is Expected

- Host just returned from maintenance mode
- Disk replacement completed
- Capacity added to the cluster
- Storage policy changed on VMs

### When Resync Is Concerning

- Resync active for more than 24 hours without progress
- Object health showing Degraded with no active resync
- Resync blocked due to capacity or network issues

### Checking Object Health

In vCenter: **vSAN** → **Virtual Objects**

- Filter by health status — investigate Degraded, Non-compliant, or Absent objects
- Note the VM name, object type, and storage policy

### Common Causes of Degraded Objects

- Host removed from cluster without full evacuation
- Disk group failure
- Network partition between hosts
- Capacity too low to meet the FTT policy

### Support Bundle Collection

If resync or object issues do not resolve after the expected timeframe:

1. Collect a vSAN support bundle from the vCenter support bundle tool
2. Include ESXi host logs from affected nodes
3. Open a VMware support case with the bundle and a timeline of events

---

## Resync and Rebuild

### What Is Resync?

Resync is the process by which vSAN redistributes data across the cluster to satisfy the active storage policy (PFTT — Primary Failures to Tolerate, or SFTT — Secondary Failures to Tolerate). It is triggered by events such as:

- A host returning from maintenance mode
- A disk group being added or replaced
- A storage policy change applied to existing VMs
- A capacity rebalance after adding new capacity to the cluster

During a resync, vSAN copies object components from one disk or host to another. This is normal, expected behaviour and does not by itself indicate a problem.

### What Is Rebuild?

Rebuild is a specific type of resync triggered when a component enters an **Absent** or **Degraded** state — typically because a host is down, a disk has failed, or a disk group is offline. vSAN tracks how long the component has been absent before initiating a full rebuild to a healthy location.

**Default absent timer: 60 minutes.** After a host or disk has been absent for 60 minutes, vSAN automatically begins rebuilding the affected object components onto remaining healthy capacity. This timer exists to avoid unnecessary data movement for brief maintenance events.

You can view and adjust the absent timer in vSAN Advanced Configuration:

- **vCenter** → **Cluster** → **Configure** → **vSAN** → **Advanced Options** → `clomRepairDelay`
- Default is `60` (minutes). Increase this if you routinely have short maintenance windows to reduce unnecessary rebuilds.

### Checking Resync Progress

#### ESXi CLI (run on any host in the cluster)

```bash
esxcli vsan debug resync summary get
```

This returns a summary of active resync operations including bytes remaining and estimated completion time.

#### PowerCLI

```powershell
# Connect to vCenter first
Connect-VIServer -Server vcsa-prod-01.example.com

# Get resync throttle status
Get-VsanResyncThrottle -Cluster (Get-Cluster "cl-prod-compute-01")
```

#### vCenter UI

Navigate to: **Cluster** → **Monitor** → **vSAN** → **Resyncing Objects**

This view shows all objects currently resyncing, broken down by type (repair, rebalance, evacuation, policy change) along with bytes remaining.

### Resync Throttle

During peak production hours, resync can consume significant I/O bandwidth. vSAN allows you to throttle resync to protect workload performance.

#### Check current throttle

```bash
esxcli vsan debug resync throttle get
```

#### Set throttle (IOPS cap)

```bash
# Set resync throughput limit to 1000 IOPS (per host)
esxcli vsan debug resync throttle set --throttle 1000
```

A value of `0` means no throttle (unlimited). During business hours, setting a limit of `500`–`2000` IOPS is typical depending on workload sensitivity. Remove the throttle during off-hours maintenance windows to allow faster completion.

#### PowerCLI throttle

```powershell
# Set resync throttle (IopsForResync) for the cluster
Set-VsanResyncThrottle -Cluster (Get-Cluster "cl-prod-compute-01") -IopsForResync 1000
```

### Performance Impact During Rebuild

Rebuild generates significant back-end I/O between hosts. Expect:

- **Increased disk latency** on hosts involved in the rebuild, particularly for VMs on the same disk groups
- **Increased network utilisation** on vSAN VMkernel adapters (10/25 GbE traffic between hosts)
- **Reduced effective cluster IOPS** proportional to how much capacity is being rebuilt

Monitor `vSAN Backend Read Latency` and `vSAN Backend Write Latency` counters in vCenter performance charts during active rebuilds. Latency above 20 ms sustained warrants investigation or throttle adjustment.

### How Long Should Resync Take?

| Scenario | Expected Duration |
|---|---|
| Single VM policy change | Minutes to hours depending on VM size |
| Host returning from short maintenance (< 1 hour) | 30 minutes – 4 hours |
| Full disk group replacement (e.g. 8 TB) | Several hours to overnight |
| Full host replacement (large capacity) | 12–48 hours |
| Cluster rebalance after adding capacity | Hours to days |

If resync has been running for more than **24 hours without measurable progress**, investigate blocked components.

### Key Commands Reference

| Command | Purpose |
|---|---|
| `esxcli vsan debug resync summary get` | Show active resync summary |
| `esxcli vsan debug resync throttle get` | Show current throttle setting |
| `esxcli vsan debug resync throttle set --throttle <n>` | Set throttle in IOPS (0 = unlimited) |
| `esxcli vsan debug object list` | List all vSAN objects and health states |
| `esxcli vsan debug disk list` | List disks and their health |
| `Get-VsanResyncThrottle` | PowerCLI: get throttle for a cluster |
| `Set-VsanResyncThrottle -IopsForResync <n>` | PowerCLI: set throttle for a cluster |

### Checking Object Health

In vCenter: **Cluster** → **Monitor** → **vSAN** → **Virtual Objects**

Filter by status:
- **Healthy** — all components present and compliant
- **Non-compliant** — policy cannot be met (often capacity or host count issue)
- **Degraded** — one or more components are absent or failed
- **Inaccessible** — object cannot be read (critical — immediate action required)

For inaccessible objects, check that all hosts in the cluster are connected and that vSAN network connectivity between hosts is healthy.

### When to Call VMware Support

Open a VMware (Broadcom) support case if:

- Objects remain in **Inaccessible** state after verifying host and network connectivity
- Resync has been running for more than **48 hours** with no forward progress
- `esxcli vsan debug resync summary get` shows errors or reports a stalled operation
- vSAN health in Skyline Health shows **red** for Data Integrity or Object Health even after expected completion
- A disk group enters a **Degraded** state unexpectedly (hardware failure suspected)

When opening a support case, collect:
1. vSAN support bundle from vCenter (Support → Generate Support Bundle, include vSAN data)
2. ESXi host logs from affected nodes (`/var/log/vmkernel.log`, `/var/log/vsanmgmt.log`)
3. Timeline of events (when host went down, when rebuild started, current status)
4. Output of `esxcli vsan debug resync summary get` and `esxcli vsan debug object list`

---

## Capacity

Capacity planning, slack space, thin provisioning, growth trends, and alert thresholds.

### Daily Checks

| Check | Command | Notes |
|---|---|---|
| Review active alarms. |  |  |
| Check recent failed tasks. |  |  |
| Confirm service health. |  |  |
| Confirm capacity and performance are normal. |  |  |
| Check recent changes. |  |  |

### Health Commands

```bash
# Add environment-specific commands here
```

### Common Issues

- Failed or stuck tasks.
- Certificate, DNS, or authentication issues.
- Capacity pressure.
- Service health warnings.
- Version mismatch after maintenance.
- Monitoring gaps.

### Operational Tasks

| Task | Command |
|---|---|
| Review alarms and events. |  |
| Confirm ownership and support notes. |  |
| Validate dependencies. |  |
| Document changes. |  |
| Confirm monitoring coverage. |  |

### Upgrade Notes

- Confirm compatibility.
- Review known issues.
- Confirm rollback plan.
- Validate health before and after the change.

### Best Practices

| Recommendation | Detail |
|---|---|
| Keep naming consistent. | Keep naming consistent. |
| Keep versions aligned. | Keep versions aligned. |
| Avoid unsupported version combinations. | Avoid unsupported version combinations. |
| Document exceptions. | Document exceptions. |
| Validate after every change. | Validate after every change. |
