---
tags:
  - operations
  - san
---
# Brocade SANnav — Backup and Restore

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
```text
┌───────────────────────────────── Brocade SANnav — Backup and Restore ─────────────────────────────────┐
│                                                                                                       │
│  SANnav backup covers config DB, performance data, zone snapshots, and switch firmware.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                SANnav Backup                 │  │              Switch Zone Backup             │   │
│   │        Daily: NFS destination backup         │  │           configupload per switch           │   │
│   │         Backup includes: DB + config         │  │        Zoning snapshot before change        │   │
│   │        Schedule: GUI → Admin → Backup        │  │         Store in NFS or version ctrl        │   │
│   │        Retention: 30 days recommended        │  │        cfgshow: verify active config        │   │
│   │            Test restore quarterly            │  │         supportsave before firmware         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SANnav config backup and zone backups are independent; both required for full recovery.              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           SANnav Restore Procedure           │  │            Switch Config Restore            │   │
│   │          1. Deploy fresh SANnav OVA          │  │           configdownload to switch          │   │
│   │        2. Restore DB from NFS backup         │  │         Zone restore: cfgsave first         │   │
│   │          3. Verify switch discovery          │  │         cfgenable to activate zones         │   │
│   │         4. Re-validate TACACS+ auth          │  │         Verify: nsshow + fabricshow         │   │
│   │           5. Test alert forwarding           │  │         Test: host I/O after restore        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SANnav VM · NFS backup server · Brocade FC switch chassis · vSphere host                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  NFS backup      = SANnav configuration and database exported to NFS mount point                      │
│  configupload    = Fabric OS CLI; uploads switch config (zones + system) to FTP/SCP                   │
│  configdownload  = Fabric OS CLI; restores switch config from FTP/SCP file                            │
│  cfgsave         = saves zone database changes to switch NVRAM flash                                  │
│  cfgenable       = activates named zone configuration across the fabric                               │
│  supportsave     = full diagnostic capture; run before any firmware or major change                   │
│  Zone snapshot   = cfgshow output captured before zone change as rollback reference                   │
│  SANnav OVA      = fresh SANnav VM deployed from Broadcom-provided OVA template                       │
│  nsshow          = name server show; verifies devices re-login after restore                          │
│  fabricshow      = topology show; verifies fabric re-forms after config restore                       │
│  Retention policy= keep 30 days of SANnav backups; prune older to manage storage                      │
│  Restore test    = quarterly test of full restore to validate backup integrity                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
