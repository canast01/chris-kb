---
tags:
  - nsx
  - nsx-4
  - operations
  - vmware
---
# NSX — Backup and Restore
![NSX — Backup and Restore](../../../../assets/virtualization-vmware-nsx-operations-backup-restore.svg)


```bash
# Configure backup via API
curl -sk -u 'admin:password' \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "backup_config": {
      "backup_enabled": true,
      "remote_file_server": {
        "server": "backup.example.local",
        "port": 22,
        "protocol": {
          "protocol_name": "SFTP",
          "authentication": {
            "authentication_mode": "PASSWORD",
            "username": "nsx-backup",
            "password": "s3cur3P@ss"
          }
        },
        "dir_path": "/backups/nsx/"
      },
      "pass_phrase": "MyVaultStoredPassphrase",
      "backup_schedule": {
        "resource_type": "IntervalBackupSchedule",
        "seconds_between_backups": 86400
      },
      "backup_to_retain": 14
    }
  }' \
  "https://<nsx-manager>/api/v1/cluster/backups/config"
```

```bash
nsxcli
get cluster status
get managers
get services
```
```bash
# Cluster health
get cluster status

# Transport node connectivity (may take 5–10 min to reconnect)
get transport-node-status

# Verify segments are present
nsxcli
get logical-switches

# Verify gateways
get logical-routers

# Check DFW policies restored
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/policy/api/v1/infra/domains/default/security-policies" | python3 -m json.tool

# Check Edge nodes reconnected
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/edge-clusters"
```
```bash
# Export full policy config as JSON (use before changes for comparison)
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/policy/api/v1/infra?filter=Type-SecurityPolicy" \
  > nsx-dfw-export-$(date +%Y%m%d).json

# Export all infra objects
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/policy/api/v1/infra" \
  > nsx-full-infra-$(date +%Y%m%d).json
```
```bash
# Query the last successful backup timestamp
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/cluster/backups/history" | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
backups = data.get('results', [])
if backups:
    latest = sorted(backups, key=lambda x: x.get('end_time', 0), reverse=True)[0]
    import datetime
    ts = datetime.datetime.fromtimestamp(latest['end_time']/1000)
    print(f'Last backup: {ts}  Status: {latest.get(\"status\",\"?\")}'  )
else:
    print('No backups found')
"
```

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## See also

- [NSX — Standard Procedures](procedures/)
- [NSX — Common Issues](../troubleshooting/common-issues/)
- [NSX — Health Checks](health-checks/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
