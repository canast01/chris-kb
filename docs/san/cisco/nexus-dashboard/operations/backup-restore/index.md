# Nexus Dashboard — Backup & Restore

> Part of the [Nexus Dashboard](../../) reference.

---

## Overview

Nexus Dashboard backup captures the full cluster state:
- Platform configuration (users, LDAP, certificates, site registrations)
- NDFC database (fabrics, zones, device aliases, inventory, events)
- NDI configuration and anomaly history (optional — large)
- Application configuration and state

Backups are critical for cluster recovery after node failure and as pre-upgrade snapshots. ND backup uses an external SCP or SFTP target — local-only backups are insufficient for DR.

---

## Backup Configuration

### Configure Remote Backup Destination

Navigate to **Admin Console > Operations > Backup & Restore > Settings**:

| Setting | Recommended Value |
|---|---|
| Backup type | SCP or SFTP |
| Remote host | `backup-server.corp.example.com` |
| Remote path | `/backups/nexus-dashboard/dc1/` |
| Username | `nd-bkp` (write permission on target path) |
| Authentication | SSH key (preferred) or password |
| Encryption | Enabled — set a strong passphrase (store in vault) |
| Retention count | 4 (keep last 4 backups) |

Test the remote destination by clicking **Test Connection** before relying on it.

### Schedule Automated Backups

Navigate to **Admin Console > Operations > Backup & Restore > Schedule**:

| Field | Value |
|---|---|
| Frequency | Weekly |
| Day | Sunday |
| Time | 02:00 (local appliance time) |
| Include app data | Yes for NDFC; optional for NDI (large) |

### Manual Backup (GUI)

1. Navigate to **Admin Console > Operations > Backup & Restore**.
2. Click **Backup Now**.
3. Select: include or exclude NDI telemetry data (exclude for faster backup unless telemetry history is required).
4. Click **Start Backup**.
5. Monitor progress — backup status updates in the UI. Completion time depends on data size: 10-30 minutes typical.

### Manual Backup (CLI)

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

---

## Restore Procedure

### Restore to Same Cluster

Use when the cluster is functional but data needs recovery (e.g., accidental zone deletion, NDFC misconfiguration).

1. Navigate to **Admin Console > Operations > Backup & Restore > Restore**.
2. Select the backup to restore from (either from the remote target list or upload a file).
3. Click **Restore**. The cluster restarts its application services during restore.
4. After restore completes (10-30 minutes), validate:
   - NDFC fabric inventory and zone databases
   - ND user accounts and LDAP settings
   - Site registrations

**Warning:** Restore overwrites all current state. Any changes made after the backup point are lost. Always export zone databases immediately before triggering a restore.

### Restore to a New Cluster (DR Recovery)

Use when the original ND cluster is unrecoverable (all nodes lost).

```bash
# Step 1: Deploy a fresh 3-node ND cluster (same version as the backup)
# Follow the install procedure in Install & Upgrade

# Step 2: On the new cluster, configure the remote backup destination
acs backup remote add \
  --server backup-server.corp.example.com \
  --path /backups/nexus-dashboard/dc1/ \
  --user nd-bkp

# Step 3: List available backups
acs backup list --remote

# Step 4: Restore from the remote backup
acs restore \
  --backup-id <backup-id-from-list> \
  --encryption-passphrase-file /home/ndadmin/.nd-backup-pass

# Step 5: Monitor restore
acs restore status

# Step 6: After restore, validate
acs health
acs apps status
```

**If the ND management IP changed (new hardware):**
- Update DNS records for the cluster management FQDN
- Update any switch-side SNMP trap destinations that send traps to ND

### Post-Restore Validation

| Check | Method |
|---|---|
| All ND nodes healthy | `acs health` or Admin Console > Nodes |
| NDFC fabrics populated | NDFC > Fabrics — all switches visible |
| Zone sets intact | NDFC > Zoning — all zone sets present |
| Device aliases intact | NDFC > Device Alias |
| LDAP authentication working | Login with an AD account |
| NDI anomalies visible (if NDI installed) | NDI > Dashboard |
| Site registrations present | Admin Console > Infrastructure > Sites |
| TLS certificate valid | Browser — no cert warning |

---

## NDFC Zone Database Export (Standalone)

In addition to cluster-level backups, export NDFC zone databases before every zone change:

### GUI Export

1. Navigate to **NDFC > Fabrics > [Fabric Name] > Actions > Export**.
2. Select export format: **JSON** (native NDFC format).
3. Save with a timestamp: `DC1-FABRIC-A-zones-20260508.json`.
4. Attach to the change management ticket.

### REST API Export

```bash
# Authenticate to ND
TOKEN=$(curl -sk -X POST https://nd-dc1.corp.example.com/login \
  -H "Content-Type: application/json" \
  -d '{"userName":"svc-automation","userPasswd":"<pass>","domain":"local"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

# Get fabric list
FABRICS=$(curl -sk \
  "https://nd-dc1.corp.example.com/appcenter/cisco/ndfc/api/v1/san/fabrics" \
  -H "Authorization: Bearer ${TOKEN}" \
  | python3 -c "import sys,json; [print(f['fabricName']) for f in json.load(sys.stdin)['DATA']]")

# Export zone database per fabric
for FABRIC in ${FABRICS}; do
  curl -sk \
    "https://nd-dc1.corp.example.com/appcenter/cisco/ndfc/api/v1/san/zoning?fabricName=${FABRIC}" \
    -H "Authorization: Bearer ${TOKEN}" \
    -o "${FABRIC}-zones-$(date +%Y%m%d).json"
  echo "Exported: ${FABRIC}"
done
```

---

## Backup Retention Policy

| Backup Type | Frequency | Retention | Storage |
|---|---|---|---|
| ND cluster full backup | Weekly | 4 copies | Remote SCP/SFTP |
| Pre-upgrade ND backup | Before every upgrade | Indefinite | Remote SCP/SFTP |
| NDFC zone export | Before every zone change | 90 days | Change management system |
| VM snapshots | Before each upgrade | Delete within 48h post-upgrade | vCenter datastore |

Do not rely on VM snapshots as the primary recovery mechanism. Snapshots held longer than 48 hours degrade VM I/O performance and should be deleted after confirming the upgrade is stable.

---

## Backup Verification

Test the backup restore procedure at least annually:

1. Deploy a temporary ND cluster (in a test environment or a dedicated DR environment).
2. Restore the most recent production backup.
3. Validate NDFC fabric inventory, zone databases, and user accounts.
4. Document the test results (time to restore, any issues encountered).
5. Delete the test cluster after validation.

A restore that has never been tested in practice is not a reliable recovery plan.
