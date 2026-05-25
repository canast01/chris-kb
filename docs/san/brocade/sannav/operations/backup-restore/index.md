---
title: SANnav — Backup & Restore
---

# SANnav — Backup & Restore

> Part of the [SANnav](../../) reference.

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

---

## Restore Procedure

### Restore to Same Appliance

Use this procedure when the SANnav appliance is still functional but data needs to be recovered (e.g., after accidental configuration deletion).

1. Navigate to **Administration > Backup > Restore**.
2. Click **Upload Backup File** and select the backup archive.
3. Click **Restore**. SANnav services restart during restore.
4. After restore, verify: switch inventory, alert policies, user accounts, and active zone sets.

### Restore to New Appliance (DR Recovery)

Use this procedure when the original SANnav VM is unrecoverable.

```bash
# Step 1: Deploy a new SANnav OVA with the same version as the backup
# (version must match exactly — restore does not support cross-version)
# Configure the same management IP, hostname, and NTP

# Step 2: Transfer the backup file to the new appliance
scp sannav-backup-20260506.tar.gz admin@new-sannav-dc1.corp.example.com:/tmp/

# Step 3: SSH to new appliance and run restore
ssh admin@new-sannav-dc1.corp.example.com
sannav restore /tmp/sannav-backup-20260506.tar.gz

# Monitor restore
tail -f /opt/sannav/logs/restore.log

# Step 4: After restore completes, verify services
sannav status

# Step 5: Update SNMP trap destinations on managed switches if SANnav IP changed
# (If same IP: no switch-side changes needed)
```

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
