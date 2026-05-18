# NSX — Backup & Restore

```
┌─────────────────────────────────────────────────────────────┐
│                    NSX Manager Backup Flow                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────┐   trigger (schedule / manual)     │
│  │   NSX Manager Cluster │──────────────────────┐           │
│  │  (3-node, Corfu DB)  │                       ▼           │
│  └──────────────────────┘         ┌─────────────────────┐   │
│            │                      │   Backup Service    │   │
│   encrypts │ AES-256 passphrase   │  (management plane) │   │
│            ▼                      └──────────┬──────────┘   │
│  ┌──────────────────────┐                    │              │
│  │  backup bundle       │◄───────────────────┘              │
│  │  (policy + certs +   │                                   │
│  │   roles + IPAM)      │   SFTP / SCP                      │
│  └──────────────────────┘──────────────────────────────►    │
│                               ┌──────────────────────────┐  │
│                               │  Remote SFTP / S3 Target │  │
│                               │  /backups/nsx/           │  │
│                               └──────────────────────────┘  │
│                                                             │
│  Restore: fresh Manager OVA → UI restore wizard → passphrase│
│  ► re-joins vCenter ► re-pushes config to transport nodes   │
└─────────────────────────────────────────────────────────────┘
```

## What NSX Backup Covers

The NSX Manager backup captures the full management plane state:

| Included | Not Included |
|---|---|
| All policy objects: segments, gateways, DFW rules | ESXi host VIBs (reinstalled during restore) |
| Security groups and tags | Edge node OS state |
| Transport zones and profiles | Running BGP session state |
| IP pools and allocations | NSX Manager appliance OS config |
| LDAP / identity source config | Active network flows |
| Certificates and trust objects | vCenter inventory |
| User roles and permissions | |
| Backup and syslog config | |

After a restore, NSX reconnects to vCenter and re-pushes configuration to transport nodes. BGP sessions re-establish automatically.

---

## Configure Backup

### Via UI

**System → Backup & Restore → Edit**

| Setting | Recommended Value | Notes |
|---|---|---|
| Protocol | SFTP | More secure than FTP |
| SFTP Host | backup.corp.local | Must be reachable from all Manager nodes |
| Port | 22 | |
| Directory | /backups/nsx/ | Pre-create on SFTP server |
| Username | nsx-backup | Dedicated service account, read/write to directory |
| Password | (SSH password or key) | Prefer key-based auth |
| Passphrase | (unique encryption passphrase) | Required to restore; store in vault |
| Backups to retain | 14 | Covers 2 weeks of daily backups |
| Schedule | Daily | Set to off-peak: 02:00 local time |

Click **Save** then **Test** to verify SFTP connectivity before relying on it.

### Via API

```bash
# Configure backup via API
curl -sk -u 'admin:password' \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "backup_config": {
      "backup_enabled": true,
      "remote_file_server": {
        "server": "backup.corp.local",
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

### Trigger a Manual Backup

```bash
# Via API (POST with empty body)
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{}' \
  "https://<nsx-manager>/api/v1/node/backups/create"

# Check backup status
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/cluster/backups/status"

# List backup history
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/cluster/backups/history"
```

Always trigger a manual backup before:
- Any NSX upgrade
- Major DFW policy changes
- Edge cluster modifications
- Certificate replacement

---

## Verify Backup Integrity

The SFTP server should contain timestamped backup bundles. Verify they exist:

```bash
# SSH to the SFTP backup server
ls -lh /backups/nsx/
# Expected: files like nsx-XXX-backup-YYYY-MM-DD-HH-MM-SS.tar.gz

# Check file sizes are non-zero and increasing over time
du -sh /backups/nsx/
```

Periodic restore tests are essential. A backup that cannot be restored has no value. Schedule a restore drill quarterly in a non-production environment.

---

## Restore NSX Manager from Backup

### When to Restore

- Complete NSX Manager cluster failure (all 3 nodes lost)
- Accidental deletion of critical configuration (restore to a point before the deletion)
- Post-upgrade rollback (restore from pre-upgrade backup)
- Cluster corruption (Corfu DB failure with majority node loss)

### Restore Prerequisites

- The backup file is present on the SFTP server and intact
- The backup passphrase is available
- Three new NSX Manager VMs are deployed (same size as original) with networking configured
- DNS records point to the new nodes (or the original nodes have been wiped and redeployed)
- vCenter is accessible

### Restore Procedure

1. Deploy a fresh single NSX Manager node (the primary restore target)

2. On first boot, before joining any cluster: access the restore UI at **https://<new-node>/login.jsp**

3. Navigate to **System → Backup & Restore → Restore**

4. Configure the SFTP connection (same settings as backup):
   - Host, port, directory, username, password
   - Enter the backup passphrase

5. Select the backup timestamp to restore from (most recent, or the pre-change backup if rolling back a config change)

6. Click **Restore** — the process takes 15–30 minutes depending on configuration size

7. The system reboots after restore. Log in and verify:

```bash
nsxcli
get cluster status
get managers
get services
```

8. If restoring to a new cluster (original nodes lost):
   - The restored node is a single-node cluster
   - Deploy nodes 2 and 3 and join them to the restored node using `join management-plane`
   - Verify three-node cluster health after joining

### Post-Restore Validation

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

---

## Partial Configuration Recovery (No Full Restore)

If only a specific DFW policy or gateway configuration was accidentally deleted, use the Policy API to recreate it from documentation or export before opening a full restore:

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

Store these exports in version control or a secure document store alongside each configuration change.

---

## Edge Node Backup

Edge nodes do not have individual backups — their configuration is driven entirely by NSX Manager. If an Edge node VM is lost, redeploy it from the NSX Manager UI:

**System → Fabric → Nodes → Edge Transport Nodes → Add**

Redeploy with the same name and parameters. NSX Manager re-pushes the routing and gateway configuration automatically. BGP sessions re-establish within seconds.

---

## Backup Retention and Compliance

| Retention Policy | Recommended Minimum |
|---|---|
| Daily backups | 14 copies (2 weeks) |
| Weekly backups | 4 copies (1 month) |
| Pre-change backups | Keep for 90 days |
| Pre-upgrade backups | Keep for 6 months |

Store backup files in a location separate from the NSX Manager VMs. If the storage hosting NSX Manager is lost, backups on the same storage are also lost.

### Backup Monitoring

Add a monitoring check for backup age:

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

Alert if no backup exists within the last 25 hours (accounts for schedule drift).
