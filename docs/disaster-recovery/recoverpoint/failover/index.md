# RecoverPoint — Failover

> Part of the [RecoverPoint](../) reference.

---

## Overview

RecoverPoint supports two failover modes:

| Mode | Description | Impact on Replication |
|---|---|---|
| Image Access (DR Test) | Non-disruptive — accesses a DR copy snapshot; production replication continues | Replication paused during image access; resumes on disable |
| Failover (Production DR) | Disruptive — production copy is demoted; DR copy becomes production | Requires failback procedure to restore normal replication direction |

For planned DR tests, use Image Access. Invoke a full failover only on declared DR events.

---

## Pre-Failover Checklist

Complete before enabling image access or invoking failover.

```bash
# Confirm all CGs are in ACTIVE state
ssh admin@<rpa-cluster-ip> "groups status"

# Confirm journal capacity (should be < 70% going into a test)
ssh admin@<rpa-cluster-ip> "journals list"

# Confirm no existing image access sessions
ssh admin@<rpa-cluster-ip> "groups status detail"

# Record current RPO baseline
ssh admin@<rpa-cluster-ip> "group status --gname <cg_name>"
```

---

## DR Test — Image Access (Non-Disruptive)

```bash
# 1. Create a pre-test bookmark
group create_bookmark --gname <cg_name> --name "dr-test-$(date +%Y%m%d)"

# 2. Enable image access on the DR copy (virtual, no data movement)
group enable-image-access --gname <cg_name> --copy DR_Copy \
  --image latest --access-mode virtual

# 3. Mount and validate volumes at DR site (host-level step, outside RecoverPoint)
# 4. Run application validation checks
# 5. Disable image access and return to normal replication
group disable-image-access --gname <cg_name>

# 6. Confirm CG returns to ACTIVE
group status --gname <cg_name>
```

---

## Full Failover (Declared DR Event)

```bash
# Step 1 — Enable image access at DR site (logged access — records writes)
group enable-image-access --gname <cg_name> --copy DR_Copy \
  --image latest --access-mode logged

# Step 2 — Confirm volumes are accessible and mount at DR site
# (Host/vSphere steps — present volumes to DR hosts)

# Step 3 — Start applications at DR site; validate

# Step 4 — Recover production (complete failover — DR copy becomes production)
group recover-production --gname <cg_name>

# Step 5 — Confirm new production copy state
group status --gname <cg_name>
```

---

## Post-Failover Validation

```bash
# Confirm DR copy is now in production role
groups status detail

# Confirm no stale image access sessions
groups status | grep -i "image access"

# Check journal state at new production site
journals list

# Check for any active alarms
alarms list
```

| Check | Expected Result |
|---|---|
| DR copy role | Now marked as Production |
| CG state | ACTIVE (replicating back to original site, or paused) |
| Image access | None active |
| Journal | < 70% utilization |
| Alarms | No critical alarms |

---

## Failback — Return to Original Production Site

After DR operations are complete and the primary site is restored:

```bash
# Step 1 — Ensure primary site storage is ready
# Step 2 — Initiate reverse replication (DR → Production)
group reverse-replication --gname <cg_name>

# Step 3 — Wait for primary site to catch up (monitor lag)
group status --gname <cg_name>

# Step 4 — Enable image access at primary site and validate
group enable-image-access --gname <cg_name> --copy PROD_Copy \
  --image latest --access-mode virtual

# Step 5 — Fail back — restore original replication direction
group failback --gname <cg_name>

# Step 6 — Confirm ACTIVE state with correct production copy
groups status
```
