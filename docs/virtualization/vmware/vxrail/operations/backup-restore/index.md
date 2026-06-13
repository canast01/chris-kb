---
tags:
  - operations
  - vmware
  - vxrail
---
# VxRail — Backup & Restore

<div class="kb-summary">
Backup and restore coverage for VxRail clusters. Covers VxRail Manager VM backup, pre-LCM snapshots, ESXi host configuration export, vCenter VAMI file-based backup, and restore considerations for each component if lost.

*Applies to: VxRail 7.x / 8.x*
</div>

```text
┌────────────────────────────────────── VxRail — Backup & Restore ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   VxRail Manager VM: back up daily via Veeam or equivalent; retain 14 days                   │    │
│   │   Pre-LCM snapshot: temporary safety net only — delete within 24h; not a backup              │    │
│   │   ESXi config export: Get-VMHostFirmware per node; store off-cluster for rebuild              │   │
│   │   vCenter VAMI backup: SFTP schedule daily; retain 14 copies; required for embedded vCenter  │    │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      VxRail Manager VM      │  │       vCenter Server        │  │      ESXi Node Config       │   │
│   │   Veeam daily backup        │  │   VAMI file-based backup    │  │   Get-VMHostFirmware        │   │
│   │   Retain: 14 days           │  │   SFTP daily schedule       │  │   One bundle per node       │   │
│   │   Pre-LCM snapshot: temp    │  │   Retain: 14 copies         │  │   Store off-cluster         │   │
│   │   Delete snapshot < 24h     │  │   Not handled by VxRail Mgr │  │   Run before LCM upgrade    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Dell PowerEdge servers · vSAN datastore · iDRAC OOB · external backup target (SFTP/Veeam repo)       │
│                                                                                                       │
│  Key terms:                                                                                           │
│  VxRail Manager  = Linux appliance VM; holds cluster config, LCM state, node inventory                │
│  VAMI            = vCenter Appliance Management Interface; port 5480; provides file-based backup      │
│  VMHostFirmware  = PowerCLI cmdlet that exports ESXi host config bundle (.tgz) for offline restore    │
│  Snapshot        = Point-in-time vSphere snapshot; degrades vSAN performance if left active > 24h     │
│  File-based BK   = VAMI backup method; exports vCenter DB, certificates, and config to SFTP target    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## VxRail Manager VM Backup

VxRail Manager is a Linux appliance VM running on the first VxRail node. It holds:

- Cluster configuration and topology data
- Node inventory and health history
- LCM bundle metadata and upgrade history
- vCenter plugin state and credentials

**If VxRail Manager is lost without a backup, the cluster continues to run but LCM upgrades, node expansion, and VxRail Plugin functionality are unavailable until VxRail Manager is restored or redeployed.**

### Veeam Backup Policy

Back up the VxRail Manager VM as you would any other critical infrastructure VM:

- **Frequency:** Daily
- **Retention:** 14 recovery points (14 days)
- **Target:** External backup repository (not on the same vSAN cluster being backed up)
- **Application consistency:** Veeam guest agent not required — file-system quiesce is sufficient

In Veeam Backup & Replication: add the VxRail Manager VM to a backup job with the above schedule. VxRail Manager does not need to be shut down for backup.

### Pre-LCM Snapshot (Temporary Safety Net)

Before starting an LCM upgrade, take a snapshot of the VxRail Manager VM as a quick rollback point:

```text
vCenter → VxRail Manager VM → Snapshots → Take Snapshot
Name: "Pre-LCM-<bundle-version>-<date>"
Description: "Pre-upgrade snapshot before LCM to <version>"
```

**Critical:** Delete this snapshot within 24 hours of a successful upgrade. Active snapshots on VMs backed by vSAN degrade vSAN performance and can cause rebuild storms if left active.

```powershell
# PowerCLI — take a pre-LCM snapshot
$vm = Get-VM "VxRail-Manager"
New-Snapshot -VM $vm -Name "Pre-LCM-7.0.401-$(Get-Date -Format 'yyyyMMdd')" `
  -Description "Pre-upgrade snapshot — delete within 24h" -Quiesce $false -Memory $false

# Delete the snapshot after confirming upgrade success
Get-Snapshot -VM $vm | Where-Object {$_.Name -like "Pre-LCM-*"} | Remove-Snapshot -Confirm:$false
```

---

## ESXi Host Configuration Export

Export each VxRail node's ESXi configuration bundle before LCM upgrades or node replacement. This bundle captures the host's networking, storage, and advanced settings — it can be used to restore a replacement node to the same configuration.

```powershell
# Connect to vCenter
Connect-VIServer -Server vcenter.example.local -Credential (Get-Credential)

# Export configuration bundle for each VxRail node
$nodes = @(
    "vxrail-node-01.example.local",
    "vxrail-node-02.example.local",
    "vxrail-node-03.example.local",
    "vxrail-node-04.example.local"
)

$destPath = "C:\backups\vxrail\esxi-config"
New-Item -ItemType Directory -Force -Path $destPath | Out-Null

foreach ($node in $nodes) {
    $host = Get-VMHost $node
    $destFile = Join-Path $destPath "$($node.Split('.')[0])-$(Get-Date -Format 'yyyyMMdd').tgz"
    Get-VMHostFirmware -VMHost $host -BackupConfiguration -DestinationPath $destPath
    Write-Host "Exported: $node → $destFile"
}
```

Store the exported `.tgz` files on an off-cluster location (NAS, SFTP server, or backup repo — not on the vSAN datastore being protected).

---

## vCenter File-Based Backup (VAMI)

VxRail Manager does **not** handle vCenter backup. vCenter must be backed up separately via the VAMI (vCenter Appliance Management Interface).

**VAMI URL:** `https://<vcenter-ip>:5480`

**For VxRail clusters with embedded vCenter:** this is the only supported backup method. Embedded vCenter cannot be backed up via Veeam or snapshot in the same way as external vCenter.

### Configure VAMI Backup Schedule

```yaml
URL:       https://<vcenter-ip>:5480
Navigate:  Backup → Configure
Protocol:  SFTP
Location:  sftp://<backup-server>/vcenter-backups/
Username:  <sftp-username>
Password:  <sftp-password>
Frequency: Daily
Time:      02:00 (off-peak window)
Retain:    14 backups
Encrypt:   Yes (set a passphrase — record it securely)
```

Verify the backup schedule is running: **VAMI → Backup → Backup Status** — the last backup timestamp should match the scheduled time.

### Validate VAMI Backup

Periodically confirm backup files are present on the SFTP target:

```bash
# List recent vCenter backup directories on SFTP target
ls -lth /vcenter-backups/ | head -20

# Each successful backup creates a directory with timestamp
# Example: 2026-06-01_02-00-00
```

---

## Restore Considerations

### If VxRail Manager VM is Lost

1. **Cluster continues operating** — ESXi, vSAN, and VMs continue to run without VxRail Manager
2. **Restore from Veeam backup** — restore the VxRail Manager VM to the same cluster using Veeam Instant Recovery or a full VM restore
3. **If backup is unavailable** — contact Dell Support to redeploy VxRail Manager from scratch. This requires the cluster serial number and Dell support credentials. Redeployment does not affect running VMs or vSAN data.
4. **After restore** — log in to VxRail Manager and verify the plugin reconnects to vCenter. Check that node inventory is populated and LCM shows the correct current version.

```bash
# Verify VxRail Manager has reconnected after restore
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxm-ip>/rest/vxm/v1/cluster" | python3 -m json.tool
```

### If vCenter is Lost

1. **VMs continue to run** on ESXi hosts — vSphere HA and DRS stop functioning but workloads are unaffected
2. **VxRail Plugin becomes unavailable** — LCM and node management via VxRail Plugin require vCenter
3. **Restore vCenter from VAMI backup:**
   - Deploy a new vCenter appliance (same version as backup)
   - During setup, select **Restore from backup**
   - Provide SFTP credentials and select the backup to restore
   - Provide the encryption passphrase set during backup
4. **After restore** — vCenter reconnects to ESXi hosts; VxRail Plugin reregisters automatically with VxRail Manager

### If an ESXi Node Must Be Rebuilt

1. VxRail nodes cannot be reinstalled with standard ESXi — the VxRail-specific ESXi image must be used
2. Use VxRail Manager to trigger a node reimaging via the **VxRail Plugin → Cluster → Nodes → Re-image Node** workflow
3. The node's ESXi configuration backup (from `Get-VMHostFirmware`) can be applied after reimaging to restore advanced settings
4. After reimaging and rejoining the cluster, vSAN rebalances data onto the restored node automatically

---

## Backup Schedule Summary

| Component | Method | Frequency | Retention | Target |
|---|---|---|---|---|
| VxRail Manager VM | Veeam backup job | Daily | 14 days | External Veeam repo |
| VxRail Manager VM | vSphere snapshot (pre-LCM only) | Before each LCM | Delete within 24h | vSAN (temporary) |
| ESXi node config | `Get-VMHostFirmware` | Before each LCM | Keep last 2 per node | Off-cluster SFTP/NAS |
| vCenter Server | VAMI file-based backup | Daily | 14 copies | External SFTP target |
