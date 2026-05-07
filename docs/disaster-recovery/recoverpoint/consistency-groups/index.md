# RecoverPoint — Consistency Groups

> Part of the [RecoverPoint](../) reference.

---

## Overview

A Consistency Group (CG) is the primary replication unit in RecoverPoint. Each CG groups one or more volumes that must be recovered together as a consistent set — for example, all data and log LUNs for an Oracle database. RecoverPoint guarantees write-order consistency across all volumes in a CG.

| Property | Description |
|---|---|
| Production Copy | The live, writable copy of the data at the production site |
| DR Copy | The replica at the remote (DR) site — read-only unless image access is enabled |
| Local Copy | Optional CDP copy at the production site for local point-in-time recovery |
| Journal | Per-copy rolling delta store; determines recovery window |
| Bookmark | A named or automatic point-in-time marker within the journal |

---

## Viewing CG State

```bash
# SSH to RPA cluster management IP
ssh admin@<rpa-cluster-ip>

# All CGs and their current replication state
groups status

# Detailed CG state including RPO, lag, and journal utilization
groups status detail

# State of a specific CG
group status --gname <cg_name>

# Via REST API — summary of all CGs
RP="https://<rpa-ip>/fapi/rest/5_1"
AUTH="-u admin:password --insecure"
curl -s $AUTH "$RP/group/all_groups_details" | python3 -m json.tool
```

---

## Creating and Configuring a CG

CGs are created via the RecoverPoint Management Application (RPMA) or vSphere plugin (RP4VM). CLI steps below apply to RPMA-managed environments.

```bash
# Step 1 — Add volumes to a new CG (interactive via boxmgmt)
boxmgmt
# Navigate: Group Management → Add Group → follow wizard

# Step 2 — Set RPO alarm threshold for a CG
group set_rpo --gname <cg_name> --rpo_seconds 300   # 5-minute RPO

# Step 3 — Enable a CG after creation
group enable --gname <cg_name>

# Step 4 — Verify CG state post-creation
group status --gname <cg_name>
```

---

## Suspending and Resuming Replication

Suspend CGs before planned maintenance on protected storage or hosts.

```bash
# Suspend a single CG
group disable-replication --gname <cg_name>

# Suspend all CGs (pre-maintenance)
groups disable-replication

# Resume a single CG after maintenance
group enable-replication --gname <cg_name>

# Resume all CGs
groups enable-replication

# Monitor return to ACTIVE state after resume
watch -n 10 "ssh admin@<rpa-ip> 'groups status'"
```

---

## Bookmarks

Bookmarks are named points in time within the journal. Use them for application-consistent DR tests and recovery.

```bash
# Create a manual bookmark (e.g., before a patching window)
group create_bookmark --gname <cg_name> --name "pre-patch-$(date +%Y%m%d)"

# List available bookmarks for a CG
group list_bookmarks --gname <cg_name>

# Enable image access at a specific bookmark
group enable-image-access --gname <cg_name> --copy DR --image <bookmark_name>

# Disable image access (return to replication)
group disable-image-access --gname <cg_name>
```

---

## CG Consistency Group Checklist

Use before any DR test or planned failover.

| Check | Command | Expected |
|---|---|---|
| CG state | `groups status` | All `ACTIVE` |
| Journal utilization | `journals list` | < 70% |
| RPO compliance | `group status --gname <n>` | Within SLA |
| Image access disabled | `groups status detail` | No active image access |
| No active alarms | `alarms list` | No critical alarms |
| DR site reachable | `network connectivity check` | Connected |
