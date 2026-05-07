# Superna Eyeglass — Health Checks

> Part of the [Superna Eyeglass](../) reference.

---

## Overview

Eyeglass health checks cover the Eyeglass appliance itself, PowerScale cluster connectivity, SyncIQ policy status, and DR policy readiness. Run daily as a minimum; automated checks should run every 15–30 minutes.

| Area | Tool | Frequency |
|---|---|---|
| Eyeglass appliance services | `egcli status` | Daily |
| DR policy state | `egcli drpolicy status --all` | Daily |
| SyncIQ replication lag | `isi sync policies list` | Daily |
| PowerScale cluster health | `isi status` | Daily |
| Eyeglass DR preflight | `egcli drtest preflight` | Weekly / pre-change |

---

## Eyeglass Appliance Health

```bash
# Check Eyeglass service status (SSH to Eyeglass appliance)
ssh admin@<eyeglass-ip>

# Eyeglass service status
egcli status

# Eyeglass version
egcli version

# Check Eyeglass cluster connectivity to both PowerScale clusters
egcli clusters list
egcli clusters status

# Check Eyeglass license validity
egcli license status

# Review Eyeglass event log for errors
egcli events list --severity error --last 100
```

---

## DR Policy Status

```bash
# List all DR policies and their current state
egcli drpolicy list

# Detailed status for all policies
egcli drpolicy status --all

# Status for a specific policy
egcli drpolicy status --policy <policy_name>

# Expected output fields:
#   Policy Name         State           Last Test     SyncIQ Lag
#   POL-NAS-PROD        Replicating     2026-05-01    45s
#   POL-HOME-PROD       Replicating     2026-05-01    12s
```

---

## SyncIQ Replication Health

```bash
# On production PowerScale cluster
ssh admin@<production-cluster>

# List all SyncIQ policies managed by Eyeglass
isi sync policies list

# View a specific policy — confirm last run and status
isi sync policies view <policy_name>

# Check for any active or failed SyncIQ jobs
isi sync jobs list

# Check SyncIQ reports for the last 24 hours
isi sync reports list --limit 20

# Check SyncIQ errors
isi sync reports errors list
```

| SyncIQ Status | Meaning | Action |
|---|---|---|
| running | Active sync in progress | Monitor; confirm completion |
| finished | Last run completed successfully | OK |
| failed | Last run failed | Check reports for errors; restart if needed |
| paused | Policy is paused | Confirm intentional; resume if not |
| disabled | Policy is disabled | Confirm intentional; enable if DR policy |

---

## PowerScale Cluster Health

```bash
# On each PowerScale cluster (production and DR)
isi status

# Check for critical alerts
isi alerts list --category critical

# Check for failed or degraded drives
isi devices node list
isi devices drive list | grep -v HEALTHY

# Check SmartConnect VIP pool health (for client access)
isi network pools list

# Confirm SyncIQ service is running
isi sync service view
```

---

## Weekly DR Readiness Check

```bash
# Run Eyeglass preflight on DR cluster — confirms all DR prerequisites are met
egcli drtest preflight --cluster <dr-cluster>

# Expected output: all checks PASS
# Common checks include:
#   - SyncIQ policies configured and running
#   - Access zones configured at DR site
#   - NFS/SMB export/share definitions replicated
#   - DNS integration (if configured) operational
#   - Eyeglass connectivity to both clusters confirmed

# Review Eyeglass DR readiness dashboard
# Eyeglass UI: https://<eyeglass-ip>:8443 → DR Dashboard
```

---

## Health Check Summary Table

| Check | Command | Expected |
|---|---|---|
| Eyeglass services | `egcli status` | All services running |
| DR policy state | `egcli drpolicy status --all` | All in Replicating state |
| SyncIQ jobs | `isi sync jobs list` | No failed jobs |
| Cluster health | `isi status` | All nodes healthy |
| Critical alerts | `isi alerts list --category critical` | No critical alerts |
| Drive health | `isi devices drive list` | All HEALTHY |
| License | `egcli license status` | Valid, not expiring |
