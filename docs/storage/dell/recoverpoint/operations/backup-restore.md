---
tags:
  - dell
  - operations
---
# RecoverPoint — Backup & Restore
![RecoverPoint — Backup & Restore](../../../../assets/storage-dell-recoverpoint-operations-backup-restore.svg)


```bash
# Connect to RecoverPoint appliance
ssh admin@rpa01.example.com

# List consistency groups
get_consistency_groups

# Add a bookmark to a specific CG
add_bookmark --cg "CG_PROD_SQL" --name "Pre-Patch-2026-05-08" --type CRASH_CONSISTENT

# List bookmarks for a CG
get_bookmarks --cg "CG_PROD_SQL"
```

```mermaid
sequenceDiagram
    participant Admin
    participant RP as RecoverPoint
    participant Journal as Journal Store
    participant AccessHost as Access Host

    Admin->>RP: Enable Image Access (Logged Access, read-only)
    RP->>Journal: Identify requested journal point
    Journal->>RP: Acknowledge — image ready
    RP->>AccessHost: Present volume at selected point in time
    AccessHost->>AccessHost: Volume visible as disk
    Admin->>AccessHost: Mount volume / browse data / validate
    Admin->>RP: Disable Image Access
    RP->>AccessHost: Remove volume
    RP->>Journal: Resume normal journal write processing
    Note over RP: Replication was not interrupted
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

- [Recoverpoint — Procedures](procedures/)
- [Recoverpoint — Health Checks](health-checks/)
- [Recoverpoint — Common Issues](../troubleshooting/common-issues/)
