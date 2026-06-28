---
tags:
  - aria-operations
  - operations
  - vmware
---
# Aria Operations Backup & Restore
![Aria Operations Backup & Restore](../../../../assets/virtualization-vmware-aria-operations-operations-backup-rest.svg)




```bash
ssh admin@vrops-prod-01.example.local

```d2
direction: right

hub: "Aria Operations\nOperations" {shape: hexagon}
trigger_an_immediate_backup_using_th: "Trigger an immediate backup using the vracli tool" {shape: rectangle}
backupid_is_the_id_of_the_configured: "<backup-id> is the ID of the configured external location (v" {shape: rectangle}
list_configured_backup_locations: "List configured backup locations" {shape: rectangle}
check_backup_status: "Check backup status" {shape: rectangle}
authenticate: "Authenticate" {shape: rectangle}
list_backup_configurations: "List backup configurations" {shape: rectangle}

hub -> trigger_an_immediate_backup_using_th
hub -> backupid_is_the_id_of_the_configured
hub -> list_configured_backup_locations
hub -> check_backup_status
hub -> authenticate
hub -> list_backup_configurations
```

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

## See also

- [Aria Operations Procedures](procedures/)
- [Aria Operations Common Issues](../troubleshooting/common-issues/)
- [Aria Operations Health Checks](health-checks/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
