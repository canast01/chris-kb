# RecoverPoint — Recovery

> Part of the [RecoverPoint](../) reference.

---

## Overview

RecoverPoint supports three recovery scenarios, each using the journal to restore data to a consistent point in time:

| Scenario | Description | Disruption |
|---|---|---|
| DR Test (Image Access) | Mount DR copy at a point in time; validate without impacting replication | Minimal — replication pauses during access |
| Full Failover | Production site unavailable; DR copy becomes new production | Disruptive — requires failback to restore direction |
| Point-in-Time Recovery | Recover to a specific bookmark or timestamp (e.g., before ransomware or corruption) | Targeted — only affects the specific CG |

---

## DR Test — Image Access Recovery

```bash
# SSH to RPA cluster
ssh admin@<rpa-cluster-ip>

# Step 1 — List available bookmarks for the CG
group list_bookmarks --gname <cg_name>

# Step 2 — Enable image access at a specific bookmark (virtual — no data movement)
group enable-image-access --gname <cg_name> --copy DR_Copy \
  --image <bookmark_name_or_timestamp> --access-mode virtual

# Step 3 — Confirm image access is active
group status --gname <cg_name>

# Step 4 — Mount volumes at DR site and validate application (host-level step)
# Step 5 — After validation: disable image access to resume replication
group disable-image-access --gname <cg_name>

# Step 6 — Confirm CG returns to ACTIVE
groups status
```

---

## Full Failover — Production Site Down

```bash
# Step 1 — Confirm production site is unreachable (not a false alarm)
# Step 2 — Enable image access on DR copy (logged mode — allows writes)
group enable-image-access --gname <cg_name> --copy DR_Copy \
  --image latest --access-mode logged

# Step 3 — Confirm image access is active and volumes are accessible
group status --gname <cg_name>

# Step 4 — Mount and start applications at DR site
# Step 5 — Recover production (promote DR copy to production role)
group recover-production --gname <cg_name>

# Step 6 — Confirm DR copy is now in production role
groups status detail
```

| Step | Command | Verification |
|---|---|---|
| Enable image access | `group enable-image-access` | State: ImageAccess |
| Validate application | Host-level validation | App responds correctly |
| Recover production | `group recover-production` | DR copy = Production |
| Check CG state | `groups status detail` | ACTIVE with correct roles |

---

## Point-in-Time Recovery

Recover to a specific point in time — for example, before a ransomware event or a bad database transaction.

```bash
# Step 1 — List journals and bookmarks to identify the target time
group list_bookmarks --gname <cg_name>
journals list

# Step 2 — Enable image access at the target timestamp (virtual mode)
group enable-image-access --gname <cg_name> --copy DR_Copy \
  --image "2026-05-06 14:30:00" --access-mode virtual

# Step 3 — Mount volumes in read-only mode and copy/validate data
# Step 4 — If recovered data is good, switch to logged access to allow writes
group enable-image-access --gname <cg_name> --copy DR_Copy \
  --image "2026-05-06 14:30:00" --access-mode logged

# Step 5 — When done: disable image access
group disable-image-access --gname <cg_name>
```

---

## Post-Recovery Validation

```bash
# Confirm no image access sessions remain active
groups status | grep -i "image"

# Confirm CG is ACTIVE and replicating
groups status detail

# Confirm RPO is back within SLA
group status --gname <cg_name>

# Confirm journal utilization has returned to normal
journals list

# Confirm no active alarms
alarms list
```

---

## Recovery RTO/RPO Reference

| Recovery Type | Typical RTO | RPO |
|---|---|---|
| DR Test (image access) | 15–30 minutes | RPO at time of bookmark |
| Full failover | 30–90 minutes (plus app validation) | RPO at last journal point |
| Point-in-time recovery | 30–60 minutes | Any point within journal window |
