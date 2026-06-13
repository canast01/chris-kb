---
tags:
  - pure
  - troubleshooting
---
# FlashBlade — Diagnostics


<div class="kb-summary">
Diagnostics reference covering Diagnostic Commands, Performance Diagnostics, Log Locations, Before Calling Support.
</div>

```text
FlashBlade Diagnostic Sequence
  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │  1. purefb array list       ─ version + capacity │
  │  2. purefb alert list       ─ active alerts      │
  │  3. purefb blade list       ─ blade health       │
  │  4. purefb hardware list    ─ chassis components │
  │  5. purefb fs list          ─ filesystem state   │
  │  6. purefb replication list ─ ActiveDR status    │
  │  7. purefb support info     ─ support bundle     │
  └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
                         │  if escalating
                         ▼
  Pure1 telemetry ──► Support case ──► upload diagnostic bundle
```

> Part of the [FlashBlade Troubleshooting](../index.md) reference.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Diagnostic Commands

```bash
# Overall FlashBlade status and Purity//FB version
purefb array list

# All blade health and capacity contribution
purefb blade list

# Hardware component status (FMs, PSUs, fans)
purefb hardware list

# All active alerts
purefb alert list

# Filesystem list with provisioned and used capacity
purefb filesystem list

# S3 bucket list with usage
purefb bucket list

# Object store accounts and users
purefb objectstoreaccount list
purefb objectstoreuser list

# Network interface status (data VIPs and replication)
purefb network interface list

# Snapshot list
purefb snap list

# Replication link status and lag
purefb replication list
purefb replication arrayconnection list

# NFS export policies
purefb policy list

# Active directory and directory service status
purefb directoryservice list

# Collect diagnostic bundle
purefb support diag         # sends to Pure Support if phone-home is active
```

## Performance Diagnostics

```bash
# Array-level performance metrics
purefb array --performance

# Key metrics:
# read_bytes_per_sec / write_bytes_per_sec — throughput
# reads_per_sec / writes_per_sec — IOPS
# usec_per_read_op / usec_per_write_op — latency

# File system performance
purefb fs list --performance
purefb fs list <fs_name> --performance

# Object store performance
purefb bucket list --performance

# Rank file systems by throughput
purefb fs list --performance | sort -k3 -rn

# Check network interface utilization
purefb network-interface list
```

**FlashBlade Performance Targets:**

| Protocol | Expected Latency | Notes |
|---|---|---|
| NFS (sequential) | < 1 ms | High-bandwidth workloads |
| NFS (small random) | < 5 ms | Metadata-heavy workloads |
| S3 | < 5 ms | Object GET/PUT |

**Performance troubleshooting:**

| Symptom | Check | Action |
|---|---|---|
| Low NFS throughput | Client mount options | Use `rsize/wsize=1048576` |
| High latency | Network congestion | Check switch utilization |
| S3 slow | Large object count | Optimize key namespace; check prefix distribution |
| Blade degraded | Blade health | `purefb blade list` — contact Pure Support |

## Log Locations

| Log | Location / Command |
|---|---|
| System and Purity//FB events | `purefb array list --logs` or via Pure1 portal > Events |
| Alert history | `purefb alert list` (include resolved alerts with `--resolved`) |
| Audit log (admin actions) | `purefb admin list --audit` |
| Replication log | `purefb replication list` |
| Diagnostic bundle | `purefb support diag` — includes system logs, configuration, and metrics |
| NFS export policy log | `purefb policy list` — review policy rules and associations |
| Pure1 event timeline | Pure1 portal > Arrays > select FlashBlade > Events |

## Before Calling Support

Collect the following before opening a Pure support case:

- [ ] Array name and serial number: `purefb array list`
- [ ] Purity//FB version: `purefb array list` (Version field)
- [ ] Blade health status: `purefb blade list` — copy full output
- [ ] Hardware component status: `purefb hardware list`
- [ ] Active alerts: `purefb alert list` — copy full output
- [ ] Network interface status: `purefb network interface list`
- [ ] Replication status (if replication is involved): `purefb replication list`
- [ ] Filesystem or bucket details (if data-access related): `purefb filesystem list` or `purefb bucket list`
- [ ] NFS mount options from affected clients (output of `mount | grep nfs`)
- [ ] Symptom description: what changed before the issue, when it started, and business impact
- [ ] Diagnostic bundle: `purefb support diag` and attach to the case

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
