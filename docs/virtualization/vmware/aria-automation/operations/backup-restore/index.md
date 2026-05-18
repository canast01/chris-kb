# Aria Automation — Backup & Restore

```
┌─────────────────────────────────────────────────────────────┐
│           Aria Automation Backup Flow                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Aria Automation Cluster                             │   │
│  │  (PostgreSQL DB + config files + ABX + pipelines)   │    │
│  └────────────────────────┬─────────────────────────────┘   │
│                           │  trigger (VAMI schedule/manual) │
│                           ▼                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  vracli backup start                                 │   │
│  │  Encrypts with passphrase (AES)                      │   │
│  │  Exports: blueprints, projects, deployments,         │   │
│  │   policies, ABX, pipelines, role assignments         │   │
│  └────────────────────────┬─────────────────────────────┘   │
│                           │  NFS mount or SFTP              │
│                           ▼                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Backup target (NFS / SFTP)                          │   │
│  │  /exports/vra-backup/                                │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  Restore: VAMI → select backup → enter passphrase           │
│  ► stops services ► restores DB ► restarts ► re-enter       │
│  cloud account credentials (not backed up)                  │
└─────────────────────────────────────────────────────────────┘
```

Aria Automation backup uses a built-in tool that exports the platform configuration and deployment state to an external NFS or SFTP target. The backup does not include running VMs or cloud resources — those are managed by vCenter and the respective cloud providers.

---

## What Is and Is Not Backed Up

| Data | Backed Up | Notes |
|---|---|---|
| Cloud templates / blueprints | Yes | All versions and content |
| Service catalog items and content sources | Yes | Including icon and description |
| Projects, cloud zones, and quotas | Yes | All project configuration |
| Deployment records | Yes | Deployment state and resource tracking |
| Approval policies | Yes | |
| User and group role assignments | Yes | |
| Cloud account configuration | Yes | Credentials are **not** backed up — must be re-entered after restore |
| Notification settings | Yes | |
| Event broker subscriptions | Yes | |
| ABX actions | Yes | |
| Pipeline definitions | Yes | |
| Actual cloud resources (VMs, networks) | **No** | Managed by target clouds — not backed up |
| Kubernetes cluster state | **No** | |

---

## Configuring the Backup Target

**Via VAMI (appliance management UI):**

Open `https://<vra-fqdn>:5480` in a browser.

```
Lifecycle Management → Backup → Add Backup Location
```

| Parameter | Value |
|---|---|
| Location type | NFS or SFTP |
| NFS server | `nas-01.corp.local` |
| NFS export path | `/exports/vra-backup` |
| Passphrase | Strong passphrase — required to encrypt backup and to restore |

**The passphrase is critical.** If lost, the backup cannot be decrypted for restore. Store it in an offline vault alongside the backup location credentials.

---

## Running a Manual Backup

```bash
# Via VAMI UI: Lifecycle Management → Backup → Backup Now
# Backup status is shown inline and via notification email

# Via vracli on the appliance
ssh root@vra-prod-01.corp.local
vracli backup list    # list configured backup targets
vracli backup start   # trigger an immediate backup
vracli backup status  # show status of the latest backup
```

---

## Scheduling Automatic Backups

```
VAMI → Lifecycle Management → Backup → Schedule
```

Recommended:
- Frequency: Daily
- Time: 02:00 (off-peak)
- Retention: 14 copies
- Enable email notification on failure: requires SMTP configured in VAMI

---

## Restore Procedure

Restore from backup replaces the entire Aria Automation platform state. All configuration changes made after the backup point are lost. Running cloud resources are not affected.

**Prerequisites:**
- Aria Automation cluster is deployed and accessible (the cluster must exist to restore into)
- Backup file accessible from NFS/SFTP
- Backup passphrase available

**Via VAMI:**

```
VAMI → Lifecycle Management → Backup → Restore → select backup → enter passphrase → Restore
```

The restore process:
1. Stops all Aria Automation services
2. Restores the PostgreSQL database
3. Restores all configuration files
4. Restarts all services

Expect 20–40 minutes for a restore depending on database size.

**Via CLI:**

```bash
ssh root@vra-prod-01.corp.local
vracli restore list                         # list available backups
vracli restore start --backup-id <id>       # start restore from a specific backup
vracli restore status                       # monitor progress
```

---

## Post-Restore Validation

1. Log into Aria Automation UI — confirm authentication works
2. Navigate to **Infrastructure → Connections → Cloud Accounts** — all cloud accounts are listed
3. Re-enter credentials for each cloud account and click **Validate**:
   - vCenter account: `svc-vra@vsphere.local` credentials
   - NSX-T account: `svc-vra-nsx@corp.local` credentials
4. Confirm cloud zones and image/flavor mappings are intact
5. Navigate to **Design → Cloud Templates** — confirm templates are present
6. Check **Deployments → All Deployments** — existing deployment records are intact
7. Test a new deployment from a simple template to confirm end-to-end provisioning works
8. Confirm ABX actions and event broker subscriptions are active
9. Confirm pipeline definitions are present if Automation Pipelines is in use

---

## VM-Level Backup for Disaster Recovery

For full platform DR (including recovery to a different vCenter or site), use VADP-compatible backup of all Aria Automation appliance VMs:

```powershell
# PowerCLI — snapshot all vRA VMs before a change or backup window
$vms = Get-VM | Where-Object { $_.Name -like "vra-*" }
foreach ($vm in $vms) {
    New-Snapshot -VM $vm `
      -Name "pre-change-$(Get-Date -Format yyyyMMdd)" `
      -Quiesce -Memory:$false
    Write-Host "$($vm.Name): snapshot complete"
}
```

For clustered deployments, back up all 3 nodes together — inconsistent snapshots across nodes can cause database split-brain on restore.
