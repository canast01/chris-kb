---
tags:
  - operations
  - vcenter
  - vmware
  - vsphere-8
---
# vCenter File-Based Backup Runbook

<div class="kb-summary">

| Field | Value |
|---|---|
| Risk | Low — read-only operation on the VCSA |
| Approval | No formal change required for scheduled backups; ad-hoc backup before major changes is best practice |
| Estimated time | 15–45 minutes depending on VCSA size |
| Impact | No service interruption; vCenter remains fully operational during backup |

*Applies to: vSphere 7.x / 8.x*
</div>

```text
┌──────────────────────────── vCenter File-Based Backup — Runbook ──────────────────────────────────────┐
│                                                                                                       │
│  OVERVIEW                                                                                             │
│  VCSA ships with a built-in file-based backup to SFTP, FTP, FTPS, HTTP, or NFS                        │
│  Backup includes: configuration, inventory, licences, stats, events, alarms, tasks                    │
│  Does NOT back up VM data — use Veeam/Commvault for VM-level backup                                   │
│                                                                                                       │
│  SCHEDULE                                                                                             │
│  Daily backup recommended; retain at least 3 copies                                                   │
│  Always run an ad-hoc backup before a major upgrade or change                                         │
│                                                                                                       │
│  RESTORE                                                                                              │
│  Restore via VCSA installer → Stage 1 deploys new appliance → Stage 2 restores backup                 │
│  Restore replaces all configuration; requires the exact VCSA version that created the backup          │
│                                                                                                       │
│  Key terms:                                                                                           │
│  VCSA         = vCenter Server Appliance; the Linux OVA that runs vCenter services                    │
│  VAMI         = Virtual Appliance Management Interface; https://<vcsa>:5480                           │
│  File-based   = VCSA-native backup; not the same as a VM snapshot of the VCSA                         │
│  Backup token = encrypted passphrase protecting the backup; required for restore                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

!!! warning "vCenter downtime"
    Restoring vCenter from backup replaces the running instance. The environment will be unmanaged for the duration of the restore (typically 20–60 minutes).

## Run This Routine

### Ad-hoc backup via VAMI

1. **Open VAMI** — navigate to `https://<vcenter-fqdn>:5480` and log in as `root`.

2. **Navigate to backup** — left menu → **Backup** → **Backup Now**.

3. **Configure backup target**:
   - Protocol: `SFTP` (recommended) or `NFS`
   - Server: backup server FQDN or IP
   - Directory path: `/backups/vcenter/`
   - Username and password for the SFTP target
   - Backup password (encryption token): set a strong passphrase and record it in the password vault — required for any future restore

4. **Enable data options** — select "Include statistics, events, and tasks" for a full backup.

5. **Start backup** — click **Start**. Progress appears in the VAMI.

6. **Verify backup file** — on the SFTP target, confirm a new directory like `sn-vcenter01-<timestamp>/` was created and contains `.bak` files.

### Ad-hoc backup via API

```bash
# Trigger backup via REST API
VCENTER="vcenter.example.local"
TOKEN=$(curl -sk -X POST -u "administrator@vsphere.local:<password>" \
  "https://$VCENTER/rest/com/vmware/cis/session" | jq -r '.value')

curl -sk -X POST \
  -H "vmware-api-session-id: $TOKEN" \
  -H "Content-Type: application/json" \
  "https://$VCENTER/rest/appliance/recovery/backup/job" \
  -d '{
    "piece": {
      "location_type": "SFTP",
      "location": "sftp://backup-server.example.local/backups/vcenter/",
      "location_user": "vcbackup",
      "location_password": "<sftp-password>",
      "parts": ["seat","common"],
      "comment": "pre-change backup",
      "password": "<backup-encryption-password>"
    }
  }' | jq .
```

### Scheduled backup via VAMI

1. VAMI → Backup → **Schedule**.
2. Enable the schedule.
3. Set frequency: **Daily**, retention count: **3** (keeps last 3 backups; older are auto-deleted).
4. Configure the SFTP target (same fields as ad-hoc above).
5. Save — confirm the next scheduled run time is shown.

---

## Verify Backup Integrity

After each backup, confirm:

```bash
# List backup files on SFTP target
ls -lh /backups/vcenter/sn-*/

# Check the manifest file — lists all backup components and sizes
cat /backups/vcenter/sn-<timestamp>/manifest.json
```

A valid backup contains:
- `manifest.json` — metadata and component list
- `*.bak` — encrypted backup data files
- Total size typically 1–10 GB depending on VCSA configuration and history

---

## Restore Procedure (Summary)

Full restore requires a complete re-deploy — do not attempt during normal operations without a DR plan:

```text
1. Mount the VCSA installer ISO
2. Run the VCSA installer → Stage 1: Deploy new VCSA appliance
   (deploy to same ESXi host; use same FQDN as original)
3. Stage 2: restore from backup
   — Choose "Restore" mode
   — Enter SFTP backup location and backup encryption password
   — Wait for restore to complete (30–90 minutes)
4. After restore: DNS must resolve the VCSA FQDN to the new appliance IP
5. Verify all hosts reconnect and inventory is intact
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Backup fails with "SFTP connection refused" | SFTP target unreachable from VCSA management network | Verify firewall rule: VCSA mgmt IP → backup server TCP 22; test with `nc -vz backup-server 22` from VCSA shell |
| Backup fails with "Insufficient disk space" | Target directory full | Clean up old backup directories; ensure 20+ GB free on SFTP target |
| Backup job shows "Running" but no progress | VCSA services under load | Check VAMI → Monitor → CPU/memory; wait 15 min before cancelling |
| Cannot find backup encryption password | Password not recorded at setup | Without the password the backup cannot be restored; re-establish a fresh scheduled backup with a recorded password |
