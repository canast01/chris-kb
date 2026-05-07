# Superna Eyeglass — Failback

> Part of the [Superna Eyeglass](../) reference.

---

## Overview

Failback is the process of returning data and user access from the DR PowerScale cluster back to the production cluster after a failover. Eyeglass orchestrates failback by reversing the SyncIQ replication direction and reassigning access zone configurations.

| Phase | Description |
|---|---|
| Production readiness | Verify production cluster is healthy and storage is ready |
| Reverse replication | Run SyncIQ from DR back to production to sync changes made during failover |
| Access zone failback | Re-map access zones, NFS exports, and SMB shares to production |
| DNS cutover | Return DNS entries to production SmartConnect zones |
| Validation | Confirm client access and data integrity on production |

---

## Pre-Failback Checklist

```bash
# Confirm production PowerScale cluster is online and healthy
isi status

# Confirm all nodes are up and no critical alerts
isi devices node list
isi alerts list --category critical

# Confirm SyncIQ service is running on production
isi sync service view

# Confirm network interfaces and SmartConnect zones are configured on production
isi network interfaces list
isi network pools list

# Check Eyeglass DR assistant readiness on production Eyeglass instance
egcli drtest preflight --cluster <production-cluster>
```

---

## Initiating Failback via Eyeglass

```bash
# Log in to Eyeglass DR Assistant (web UI or CLI)
# Eyeglass UI: https://<eyeglass-ip>:8443

# List configured DR policies — confirm current state (failed over)
egcli drpolicy list

# Check which policies are in DR state
egcli drpolicy status --all

# Initiate failback for a specific DR policy
egcli drfailback --policy <policy_name> --confirm

# Monitor failback progress
egcli drfailback status --policy <policy_name>
```

---

## Reversing SyncIQ Replication

During the DR period, users may have written data to the DR cluster. This data must be synced back to production before access is cut back.

```bash
# On DR PowerScale cluster — create a reverse SyncIQ policy
# (Eyeglass automates this, but manual verification is required)
isi sync policies list

# Confirm reverse SyncIQ policy exists and is enabled
isi sync policies view <reverse_policy_name>

# Run the reverse sync manually to trigger immediate catchup
isi sync jobs start <reverse_policy_name>

# Monitor reverse sync job completion
isi sync jobs list
watch -n 30 "isi sync jobs list"
```

---

## Access Zone Cutover Back to Production

```bash
# On production PowerScale — confirm access zones are configured
isi zone zones list

# Eyeglass: re-activate access zones on production
egcli accesszone activate --cluster <production-cluster> --zone <zone_name>

# Update DNS to point SmartConnect zone back to production VIP pool
# (DNS delegation record update — done at DNS server level)
# Verify DNS resolution for NFS/SMB clients resolves to production IPs
nslookup <smartconnect_zone_name>

# Confirm NFS exports are accessible on production
isi nfs exports list

# Confirm SMB shares are accessible on production
isi smb shares list
```

---

## Post-Failback Validation

| Check | Command | Expected |
|---|---|---|
| Production cluster health | `isi status` | All nodes active |
| SyncIQ policies | `isi sync policies list` | All enabled, last run success |
| Access zones | `isi zone zones list` | All zones on production |
| NFS exports | `isi nfs exports list` | All exports present |
| SMB shares | `isi smb shares list` | All shares accessible |
| DR policy state | `egcli drpolicy status --all` | Back to normal (production) |
| Client access test | Mount and write a test file | Success, no errors |

```bash
# Final confirmation: run Eyeglass preflight on production
egcli drtest preflight --cluster <production-cluster>

# Disable reverse SyncIQ policy (DR-to-prod direction) after failback is confirmed
isi sync policies disable <reverse_policy_name>
```
