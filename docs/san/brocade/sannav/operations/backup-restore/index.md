---
title: SANnav — Backup & Restore
---

# SANnav — Backup & Restore


<div class="kb-summary">
> Part of the [SANnav](../../index.md) reference.
</div>

---

## Overview

SANnav backup captures the full appliance configuration and data, including:
- Switch inventory and credentials
- Zone configurations
- Alert policies and MAPS monitoring configuration
- User accounts and LDAP settings
- Historical events and performance data (optional)
- License information

Backups are essential for appliance recovery after hardware failure and as a pre-change snapshot before upgrades or major configuration changes.

---

## Backup Configuration

### Schedule and Destination

Configure under **Administration > Backup > Settings**:

| Setting | Recommended Value |
|---|---|
| Schedule | Weekly, Sunday 02:00 local time |
| Backup type | Full |
| Include performance data | No (large; restore not typically needed) |
| Remote destination | SCP or SFTP to backup server |
| Remote path | `/backups/sannav/dc1/` |
| Remote username | `sannav-bkp` (read-write on target directory) |
| Encryption | Enabled (AES-256) |
| Retention count | 4 (keep last 4 weekly backups) |

Test the remote destination connection before relying on it. SANnav UI provides a **Test Connection** button in the backup settings.

### Manual Backup (GUI)

1. Navigate to **Administration > Backup**.
2. Click **Backup Now**.
3. Select backup type: **Full**.
4. Click **Start**. The backup job runs in the background.
5. Monitor status under **Administration > Backup > History**.

### Manual Backup (CLI)

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

### Post-Restore Validation

| Check | Method |
|---|---|
| All switches reachable | Dashboard > Fabric Summary — all Online |
| Zone configurations present | Inventory > Fabrics > Zones |
| Alert policies restored | Administration > Alert Policies |
| LDAP authentication working | Attempt login with AD account |
| Email notifications working | Administration > Test Email |
| License valid | Administration > License Management |

---

## Zone Configuration Export (Standalone)

In addition to full appliance backup, export zone configurations before every zoning change:

### GUI Export

1. Navigate to **Inventory > Fabrics > [Fabric Name]**.
2. Select the fabric and click **Actions > Export Zone Configuration**.
3. Save the file with a timestamped name: `DC1-FABRIC-A-zones-20260506.json`.
4. Store in the change management system ticket.

### CLI / API Export

```bash
TOKEN=$(curl -sk -X POST https://sannav-dc1.corp.example.com/rest/login \
  -H "Content-Type: application/json" \
  -d '{"credentials":{"loginName":"admin","password":"<pass>"}}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['authToken'])")

# Export zone database for a specific fabric (replace <fabricId>)
curl -sk "https://sannav-dc1.corp.example.com/rest/resourcegroups/<fabricId>/zonedb" \
  -H "Authorization: Bearer $TOKEN" \
  -o dc1-fabric-a-zones-$(date +%Y%m%d).json

# Logout
curl -sk -X DELETE https://sannav-dc1.corp.example.com/rest/logout \
  -H "Authorization: Bearer $TOKEN"
```

---

## Backup Retention Policy

| Backup Type | Frequency | Retention | Storage Location |
|---|---|---|---|
| Full appliance backup | Weekly | 4 weeks | Remote backup server |
| Pre-upgrade backup | Before each upgrade | Indefinite | Remote backup server |
| Zone export | Before each zone change | 90 days | Change management system |
| VM snapshot | Before each upgrade | Delete within 48h | vCenter datastore |

Do not rely on VM snapshots as the primary backup — they are a safety net for upgrades only. Snapshots held long-term degrade VM I/O performance significantly.
