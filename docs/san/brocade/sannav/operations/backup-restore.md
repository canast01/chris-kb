---
tags:
  - operations
  - san
---
# Brocade SANnav — Backup and Restore
![Brocade SANnav — Backup and Restore](../../../../assets/san-brocade-sannav-operations-backup-restore.svg)

```bash
ssh admin@sannav-dc1.corp.example.com

# Trigger a manual backup
sannav backup --type full --destination /opt/sannav/backups/

# Monitor backup progress
sannav backup --status

# List available local backups
ls -lh /opt/sannav/backups/

# Copy backup to remote server (if not using SANnav's built-in remote transfer)
scp /opt/sannav/backups/sannav-backup-20260506.tar.gz \
    bkp-user@backup-server.corp.example.com:/backups/sannav/dc1/
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Sannav — Procedures](../procedures/)
- [Sannav — Health Checks](../health-checks/)
- [Sannav — Common Issues](../../troubleshooting/common-issues/)
