---
tags:
  - operations
  - san
---
# Cisco Nexus Dashboard — Operations Backup & Restore
![Cisco Nexus Dashboard — Operations Backup & Restore](../../../../assets/san-cisco-nexus-dashboard-operations-backup-restore.svg)


```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Trigger manual backup to remote SCP target
acs backup create \
  --remote-server backup-server.corp.example.com \
  --remote-path /backups/nexus-dashboard/dc1/ \
  --remote-user nd-bkp \
  --encryption-passphrase-file /home/ndadmin/.nd-backup-pass

# Check backup status
acs backup status

# List available backups
acs backup list
```


```d2
direction: right

hub: "Nexus Dashboard\nOperations" {shape: hexagon}
verify: "Verify" {shape: rectangle}

hub -> verify
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

- [Nexus Dashboard — Procedures](procedures/)
- [Nexus Dashboard — Health Checks](health-checks/)
- [Nexus Dashboard — Common Issues](../troubleshooting/common-issues/)
