---
tags:
  - aria-operations
  - operations
  - vmware
---
# Aria Operations Backup & Restore

```text
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
```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Restore Process                                                                                      │
│  Admin → Backup/Restore → select backup → Restore                                                     │
│  10–20 min unavailability during restore                                                              │
│  Re-enter all adapter credentials after restore                                                       │
│                                                                                                       │
│  Full DR (with metric history):                                                                       │
│  VM-level backup (Veeam/Commvault) of all nodes                                                       │
│  + Cassandra repair after restore                                                                     │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
ssh admin@vrops-prod-01.example.local

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Trigger an immediate backup using the vracli tool
vracli backup --location <backup-id>
## <backup-id> is the ID of the configured external location (visible in UI)

## List configured backup locations
vracli backup list-locations

## Check backup status
vracli backup status
```
```bash
## Authenticate
TOKEN=$(curl -sk -X POST "https://vrops-prod-01.example.local/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>","authSource":"Local"}' | \
  jq -r '.token')

## List backup configurations
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/backups" | jq '.'

## Trigger an immediate backup
curl -sk -X POST -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/backups/<backup-config-id>/actions/backup" | \
  jq '.'
```
```text
Administration → Backup/Restore → Restore → select backup → Restore
```
```bash
ssh admin@vrops-prod-01.example.local
vracli restore --backup-id <backup-timestamp-id>
```
```text
Administration → Solutions → select adapter → Edit Instance → update credentials → Test Connection
```
```bash
## After restoring all nodes from VM backup, run Cassandra repair on the primary node
ssh admin@vrops-prod-01.example.local
vracli cluster cassandra repair
## This can take hours on large deployments — monitor progress in /storage/log/cassandra.log
```

---

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
