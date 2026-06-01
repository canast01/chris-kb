# Aria Operations — Backup & Restore


<div class="kb-summary">
Backup & Restore reference covering Manual Backup via CLI, Backup via REST API, What Is and Is Not Backed Up, Restore Procedure, VM-Level Backup (Disaster Recovery).
</div>

Aria Operations — Backup Architecture
```
┌─────────────────────────────────────────────────────┐
│  Aria Operations Cluster                            │
│  ┌──────────┐  ┌──────────┐  ┌────────────────┐     │
│  │ Primary  │  │ Replica  │  │ Data nodes     │     │
│  └──────────┘  └──────────┘  └────────────────┘     │
└──────────────────────┬──────────────────────────────┘
```
                       │ file-based backup
                       │ (config only — not metric data)
                       ▼
```
┌─────────────────────────────────────────────────────┐
│  Backup Target                                      │
│  NFS: nas-01.example.local:/aria-ops-backups           │
│  SFTP: backup-srv.example.local (port 22)              │
│                                                     │
│  What IS backed up:                                 │
│    alert definitions · dashboards · user accounts   │
│    adapter configs (not credentials) · policies     │
│                                                     │
│  What is NOT backed up:                             │
│    metric time-series data · alert history          │
│    log data                                         │
└──────────────────────┬──────────────────────────────┘
```
                       │ restore
                       ▼
```
```
┌─────────────────────────────────────────────────────┐
│  Restore Process                                    │
│  Admin → Backup/Restore → select backup → Restore   │
│  10–20 min unavailability during restore            │
│  Re-enter all adapter credentials after restore     │
│                                                     │
│  Full DR (with metric history):                     │
│  VM-level backup (Veeam/Commvault) of all nodes     │
│  + Cassandra repair after restore                   │
└─────────────────────────────────────────────────────┘
```
┌────────────────────────────────── Aria Operations Backup & Restore ───────────────────────────────────┐
│                                                                                                       │
│  Backup CaSA store and configuration; restore steps for Aria Operations (vROps).                      │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               What to Back Up                │  │                Backup Method                │   │
│   │            CaSA store (config DB)            │  │           VAMI: Backup > NFS/SFTP           │   │
│   │          Custom dashboards/policies          │  │            Schedule daily backup            │   │
│   │              Alert definitions               │  │          Snapshot VM before upgrade         │   │
│   │           User accounts and roles            │  │            Retain last 3+ backups           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  CaSA backup covers config; VM snapshot covers full appliance state for rollback.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Restore Procedure               │  │           Post-Restore Validation           │   │
│   │             1. Deploy fresh OVA              │  │           Adapters: green status?           │   │
│   │         2. VAMI: Restore from backup         │  │             Dashboards: loaded?             │   │
│   │          3. Select backup file path          │  │          Alerts: firing correctly?          │   │
│   │         4. Join nodes after restore          │  │            Users: login working?            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps VMs on vSphere; NFS/SFTP backup target; vSphere snapshots for upgrade rollback                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CaSA Store          = Configuration and Support Archive; vROps internal config DB                    │
│  VAMI Backup         = Built-in vROps backup UI at port 5480; targets NFS or SFTP                     │
│  NFS Backup Target   = Network file share where vROps writes backup archive files                     │
│  SFTP Backup Target  = Secure FTP target; alternative to NFS for backup storage                       │
│  Scheduled Backup    = Automated daily CaSA backup; recommended for production                        │
│  VM Snapshot         = vSphere checkpoint of full vROps appliance; use pre-upgrade                    │
│  Restore             = VAMI-driven process to load CaSA data from backup archive                      │
│  Adapter Config      = Stored in CaSA; restored with backup including credentials                     │
│  Dashboard           = Custom views restored with CaSA; verify after restore                          │
│  Alert Definition    = Alert and symptom configs; included in CaSA backup                             │
│  Node Rejoin         = After restore, data/replica nodes re-join the master                           │
│  Metric Data         = Historical metrics NOT in CaSA backup; starts fresh on restore                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Recommended settings:
- Frequency: Daily
- Retention: 14 copies
- Notification: enable email alert on backup failure (requires SMTP configured under **Administration → SMTP Settings**)

---

## Manual Backup via CLI

```bash
ssh admin@vrops-prod-01.example.local

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
TOKEN=$(curl -sk -X POST "https://vrops-prod-01.example.local/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>","authSource":"Local"}' | \
  jq -r '.token')

# List backup configurations
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/backups" | jq '.'

# Trigger an immediate backup
curl -sk -X POST -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/backups/<backup-config-id>/actions/backup" | \
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

```text
Administration → Backup/Restore → Restore → select backup → Restore
```

The UI shows a list of available backups by timestamp. Select the desired restore point and confirm. The cluster restarts services during restore — expect 10–20 minutes of unavailability.

**Via CLI:**

```bash
ssh admin@vrops-prod-01.example.local
vracli restore --backup-id <backup-timestamp-id>
```

**Post-restore validation:**

1. Log into the Aria Operations UI — confirm the login works
2. Navigate to **Administration → Solutions** — confirm all adapters are listed
3. Re-enter credentials for all cloud accounts and adapters:

```text
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
ssh admin@vrops-prod-01.example.local
vracli cluster cassandra repair
# This can take hours on large deployments — monitor progress in /storage/log/cassandra.log
```
