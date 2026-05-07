# Superna Eyeglass — Validation

> Part of the [Superna Eyeglass](../) reference.

---

## Overview

DR validation for Eyeglass covers three scenarios: pre-failover readiness, DR test (rehearsal), and post-failover/failback confirmation. Run a full validation at least quarterly and before any planned failover.

| Validation Type | Frequency | Tool |
|---|---|---|
| DR preflight | Weekly / pre-change | `egcli drtest preflight` |
| DR test (rehearsal) | Quarterly | `egcli drtest run` |
| Post-failover validation | After every failover | Manual + `egcli` |
| Post-failback validation | After every failback | Manual + `egcli` |

---

## Eyeglass DR Preflight

The preflight check verifies all prerequisites for a failover without making any changes.

```bash
# Run preflight against the DR cluster
egcli drtest preflight --cluster <dr-cluster>

# Run preflight for a specific policy
egcli drtest preflight --policy <policy_name>

# Expected output — all items should show PASS:
#   [PASS] SyncIQ policy last run: 3 minutes ago
#   [PASS] Access zones configured on DR cluster
#   [PASS] NFS exports replicated to DR cluster
#   [PASS] SMB shares replicated to DR cluster
#   [PASS] DNS zones configured
#   [PASS] Eyeglass connectivity to both clusters confirmed
#   [PASS] SyncIQ service running on both clusters

# Review any WARN or FAIL items and remediate before proceeding
```

---

## DR Test (Rehearsal)

A DR test performs all failover steps but rolls back at the end, returning to normal replication.

```bash
# Step 1 — Run Eyeglass DR test (non-destructive rehearsal)
egcli drtest run --policy <policy_name>

# Step 2 — Monitor test progress
egcli drtest status --policy <policy_name>

# Step 3 — Validate access zones activated on DR cluster
egcli accesszone status --cluster <dr-cluster>

# Step 4 — Validate NFS exports on DR cluster
ssh admin@<dr-cluster> "isi nfs exports list"

# Step 5 — Validate SMB shares on DR cluster
ssh admin@<dr-cluster> "isi smb shares list"

# Step 6 — Confirm DNS resolution (if Eyeglass DNS integration active)
nslookup <smartconnect_zone_name>

# Step 7 — After validation, confirm DR test rollback is complete
egcli drtest status --policy <policy_name>
# Expected: State = Rolled Back / Replicating
```

---

## Post-Failover Validation

Run after a declared DR failover to confirm the DR cluster is fully operational.

```bash
# Confirm DR policy is in Failed Over state
egcli drpolicy status --all

# Confirm DR cluster is healthy
ssh admin@<dr-cluster> "isi status"
ssh admin@<dr-cluster> "isi alerts list --category critical"

# Confirm access zones are active on DR cluster
egcli accesszone status --cluster <dr-cluster>

# Confirm NFS/SMB access for clients
ssh admin@<dr-cluster> "isi nfs exports list"
ssh admin@<dr-cluster> "isi smb shares list"

# Test NFS mount from a client
mount -t nfs <dr-smartconnect-ip>:/<export_path> /mnt/drtest
ls -la /mnt/drtest

# Confirm SyncIQ is stopped on original production policy (not running)
ssh admin@<production-cluster> "isi sync policies list"
```

---

## Post-Failback Validation

```bash
# Confirm DR policy is back to Replicating state
egcli drpolicy status --all

# Confirm production cluster is healthy
ssh admin@<production-cluster> "isi status"

# Confirm access zones are back on production cluster
egcli accesszone status --cluster <production-cluster>

# Confirm SyncIQ is running in the normal direction (production → DR)
ssh admin@<production-cluster> "isi sync policies list"

# Confirm last SyncIQ run completed successfully
ssh admin@<production-cluster> "isi sync reports list --limit 5"

# Confirm client access is restored to production
nslookup <production-smartconnect-zone>
```

---

## Validation Record Template

| Check | Date | Result | Notes |
|---|---|---|---|
| DR preflight passed | | | |
| DR test completed successfully | | | |
| NFS exports accessible at DR site | | | |
| SMB shares accessible at DR site | | | |
| DNS failover confirmed | | | |
| Failback completed | | | |
| SyncIQ replicating (prod → DR) | | | |
| Client access restored to production | | | |
