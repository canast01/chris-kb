# Aria Operations — Backup & Restore

```
Aria Operations — Backup Architecture
┌─────────────────────────────────────────────────────┐
│  Aria Operations Cluster                            │
│  ┌──────────┐  ┌──────────┐  ┌────────────────┐   │
│  │ Primary  │  │ Replica  │  │ Data nodes     │   │
│  └──────────┘  └──────────┘  └────────────────┘   │
└──────────────────────┬──────────────────────────────┘
                       │ file-based backup
                       │ (config only — not metric data)
                       ▼
┌─────────────────────────────────────────────────────┐
│  Backup Target                                      │
│  NFS: nas-01.corp.local:/aria-ops-backups           │
│  SFTP: backup-srv.corp.local (port 22)              │
│                                                     │
│  What IS backed up:                                 │
│    alert definitions · dashboards · user accounts  │
│    adapter configs (not credentials) · policies    │
│                                                     │
│  What is NOT backed up:                             │
│    metric time-series data · alert history         │
│    log data                                         │
└──────────────────────┬──────────────────────────────┘
                       │ restore
                       ▼
┌─────────────────────────────────────────────────────┐
│  Restore Process                                    │
│  Admin → Backup/Restore → select backup → Restore  │
│  10–20 min unavailability during restore            │
│  Re-enter all adapter credentials after restore     │
│                                                     │
│  Full DR (with metric history):                     │
│  VM-level backup (Veeam/Commvault) of all nodes     │
│  + Cassandra repair after restore                   │
└─────────────────────────────────────────────────────┘
```

Aria Operations provides a built-in **file-based backup** mechanism that writes backups to an NFS or SFTP target. The backup includes the configuration database (policies, alert definitions, dashboards, user accounts, adapter configurations) but not the metric time-series data. Metric history is not restorable from backup — only configuration state is.

---

## Configuring the Backup Schedule

**Via UI:**

```
Administration → Backup/Restore → External Location → Add Location
```

Provide:
- Location type: NFS or SFTP
- NFS: `<nfs-server>:<export-path>` (e.g., `nas-01.corp.local:/aria-ops-backups`)
- SFTP: hostname, port (22), username, password or SSH key
- Folder path on the target (auto-created if NFS)

**Schedule:**

```
Administration → Backup/Restore → Backup → Enable Scheduled Backup
```

Recommended settings:
- Frequency: Daily
- Retention: 14 copies
- Notification: enable email alert on backup failure (requires SMTP configured under **Administration → SMTP Settings**)

---

## Manual Backup via CLI

```bash
ssh admin@vrops-prod-01.corp.local

# Trigger an immediate backup using the vracli tool
vracli backup --location <backup-id>
# <backup-id> is the ID of the configured external location (visible in UI)

# List configured backup locations
vracli backup list-locations

# Check backup status
vracli backup status
```

---

## Backup via REST API

```bash
# Authenticate
TOKEN=$(curl -sk -X POST "https://vrops-prod-01.corp.local/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>","authSource":"Local"}' | \
  jq -r '.token')

# List backup configurations
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.corp.local/suite-api/api/backups" | jq '.'

# Trigger an immediate backup
curl -sk -X POST -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.corp.local/suite-api/api/backups/<backup-config-id>/actions/backup" | \
  jq '.'
```

---

## What Is and Is Not Backed Up

| Data | Backed Up | Notes |
|---|---|---|
| Alert definitions and symptoms | Yes | All custom and policy-based alerts |
| Dashboard definitions | Yes | All custom dashboards and views |
| User accounts and roles | Yes | Local accounts and LDAP group mappings |
| Adapter/cloud account configurations | Yes | Credentials are **not** included — must be re-entered after restore |
| Policies and compliance packs | Yes | Custom and built-in policy assignments |
| Report schedules | Yes | Scheduled report definitions |
| Metric time-series data | **No** | Historical metrics are not restorable from backup |
| Alert history | **No** | Existing alert history is lost after restore |
| Log data (if integrated with Aria Ops for Logs) | **No** | Logs are stored in Aria Ops for Logs, not here |

---

## Restore Procedure

Restore replaces the current cluster configuration with the backup. This is a destructive operation — all configuration changes made after the backup point are lost.

**Prerequisites:**
- Aria Operations cluster is running and accessible
- Backup file is accessible from the configured NFS/SFTP location
- All adapter credentials are documented (they must be re-entered after restore)

**Via UI:**

```
Administration → Backup/Restore → Restore → select backup → Restore
```

The UI shows a list of available backups by timestamp. Select the desired restore point and confirm. The cluster restarts services during restore — expect 10–20 minutes of unavailability.

**Via CLI:**

```bash
ssh admin@vrops-prod-01.corp.local
vracli restore --backup-id <backup-timestamp-id>
```

**Post-restore validation:**

1. Log into the Aria Operations UI — confirm the login works
2. Navigate to **Administration → Solutions** — confirm all adapters are listed
3. Re-enter credentials for all cloud accounts and adapters:

```
Administration → Solutions → select adapter → Edit Instance → update credentials → Test Connection
```

4. Confirm collection is running: **Administration → Cluster Management** — all nodes Online, adapter instances Collecting
5. Review dashboards — confirm custom dashboards are present
6. Send a test alert to confirm alerting pipeline (email/SNMP) is functional

---

## VM-Level Backup (Disaster Recovery)

For full disaster recovery (including metric data), use a VM-level backup of all Aria Operations nodes:

- Use VADP-compatible backup (Veeam, Commvault) with quiesce enabled
- Back up all nodes: Primary, Replica, and Data nodes — they must be backed up from the same crash-consistent snapshot point
- Recovery from VM backup restores metric history but may require Cassandra consistency repair:

```bash
# After restoring all nodes from VM backup, run Cassandra repair on the primary node
ssh admin@vrops-prod-01.corp.local
vracli cluster cassandra repair
# This can take hours on large deployments — monitor progress in /storage/log/cassandra.log
```
