# SRM — Backup and Restore

```text
  SRM Backup Sources
┌──────────────────────────────────────────────────────────────┐
│  vCenter VCSA Backup (covers most SRM config)                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  Recovery Plans + Protection Groups + IP rules       │    │
│  │  → stored in vCenter Postgres DB (seat + common)     │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  SRM Appliance Snapshot (covers SRA credentials + certs)     │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  Site pairing cert trust + SRA array credentials     │    │
│  │  → govc snapshot.create / VM snapshot                │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  VR Appliance Snapshot + VAMI config backup                  │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  VRA registration + certificates                     │    │
│  │  → VRA VAMI → Administration → Backup               │     │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

## What SRM Stores and Where

SRM does not have its own independent database for most critical configuration. Understanding where data lives is essential for backup planning.

| Data | Storage Location | Backup Method |
|---|---|---|
| Recovery Plans | vCenter database (Postgres, embedded or external) | vCenter backup |
| Protection Group definitions | vCenter database | vCenter backup |
| Inventory mappings (network, folder, resource) | vCenter database | vCenter backup |
| IP customization rules | vCenter database | vCenter backup |
| SRA credentials (array usernames/passwords) | SRM local config files (encrypted) | SRM config backup / appliance snapshot |
| Site pairing certificate trust | SRM Server config | SRM config backup |
| SRM Server settings | SRM Server (appliance or Windows) | Appliance snapshot / OS backup |
| vSphere Replication config (per-VM replication jobs) | VR Appliance + vCenter | VR appliance backup |
| VR Appliance config | VR Appliance local | VR appliance snapshot / OVF export |

**Key point:** Backing up vCenter covers the majority of SRM's logical configuration. The SRM appliance or Windows server itself holds the certificate trust and SRA credentials — these must be backed up separately.

---

## Back Up vCenter (Covers SRM Config)

### VCSA File-Based Backup

```bash
# Access VCSA VAMI backup:
# https://<vcenter-fqdn>:5480 → Backup → Backup Now

# Or via API:
curl -sk -X POST \
  "https://vcenter.example.com/api/appliance/recovery/backup/job" \
  -H "vmware-api-session-id: $VC_SESSION" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "sftp://backup-server.example.com/vcsa-backups/",
    "location_user": "backupuser",
    "location_password": "secretpassword",
    "parts": ["seat", "common"],
    "comment": "Daily scheduled backup"
  }'
```

**Backup parts that include SRM data:**

| Part | Contents |
|---|---|
| `seat` | vCenter inventory service — includes SRM extension data (Protection Groups, Recovery Plans) |
| `common` | vCenter Postgres database — core vCenter inventory |

Both `seat` and `common` must be included in every vCenter backup for complete SRM recovery.

### Backup Schedule Recommendation

| Component | Frequency | Retention |
|---|---|---|
| vCenter VCSA (includes SRM config) | Daily | 14 days minimum |
| SRM appliance snapshot | Weekly | 2 snapshots |
| VR appliance snapshot | Weekly | 2 snapshots |
| Recovery Plan PDF export | After each change | Stored in documentation system |

---

## SRM Configuration Export (Migration / Documentation)

SRM provides a config export utility useful when migrating SRM to a new server or documenting current state.

### Export via SRM Appliance CLI

```bash
ssh root@srm-appliance.example.com

# Run the SRM configuration export tool
/usr/lib/vmware-dr/bin/vmware-dr-configure --action exportConfig \
  --outputFile /tmp/srm-config-export.xml

# Copy the export off the appliance
scp root@srm-appliance.example.com:/tmp/srm-config-export.xml \
  /backup/srm/srm-config-$(date +%Y%m%d).xml
```

The exported XML contains:
- Site pairing information.
- SRA configuration (array manager entries — credentials are encrypted and may not be re-importable directly).
- General SRM settings.

Recovery Plans and Protection Groups are **not** in this export — they live in vCenter DB and are recovered with vCenter.

### Export via SRM REST API

```bash
# Authenticate to get session token
SRM_TOKEN=$(curl -sk -X POST \
  "https://srm-appliance.example.com/api/session" \
  -H "Content-Type: application/json" \
  -d '{"username":"administrator@vsphere.local","password":"VMware1!"}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

# List Recovery Plans (for documentation)
curl -sk -X GET \
  "https://srm-appliance.example.com/api/recovery-plans" \
  -H "Authorization: Bearer $SRM_TOKEN" | python3 -m json.tool > \
  /backup/srm/recovery-plans-$(date +%Y%m%d).json
```

---

## vSphere Replication Appliance Backup

### Snapshot-Based Backup

```bash
# Take a snapshot of the VR appliance via govc (do during low-change-rate window)
govc snapshot.create -vm "vr-appliance-01" \
  "VR-Backup-$(date +%Y%m%d)" \
  -d "Scheduled VR appliance backup"

# List existing snapshots
govc snapshot.tree -vm "vr-appliance-01"

# Remove old snapshots (keep only last 2)
govc snapshot.remove -vm "vr-appliance-01" "VR-Backup-20260401"
```

**Note:** Do not leave snapshots on the VR Appliance indefinitely. The VR Appliance receives replication data continuously — snapshot growth can fill the datastore.

### OVF Export (for cold backups or migration)

```bash
# Power off the VR Appliance (during maintenance window)
govc vm.power -off vr-appliance-01

# Export to OVF
govc export.ovf \
  -vm "vr-appliance-01" \
  -o /backup/vrm/vr-appliance-01-$(date +%Y%m%d).ovf

# Power on
govc vm.power -on vr-appliance-01
```

### VR VAMI Config Backup

The VAMI provides a configuration export that captures network settings, registration info, and certificates:

```text
https://<vr-appliance>:5480 → Administration → Backup
```

Download the backup tar file and store with the OVF export.

---

## Recovery Plan PDF Export

SRM can generate a PDF summary of a Recovery Plan from the UI. This is useful for:
- Change management documentation.
- Audit evidence.
- Offline reference during a DR event when vCenter may be unavailable.

Export path: SRM UI → Recovery Plan → **Export** → Export as PDF

Contents include:
- All steps in priority group order.
- Per-VM IP customization rules.
- Pre/post power-on commands.
- Network and resource mappings applied.

Export after every change to a Recovery Plan and store in your documentation system or DR runbook.

---

## SRM Database Considerations

### Embedded Database (Default)

SRM Server (Windows, pre-8.x) uses an embedded SQL Server Express database by default.

- Max size: 4 GB (SQL Express limit).
- Suitable for: ≤ 250 protected VMs.
- Location: `C:\Program Files\VMware\VMware vCenter Site Recovery Manager\db\`

Backup:

```powershell
# Backup SRM embedded database (Windows)
$backupPath = "C:\SRMBackup\srm-db-$(Get-Date -Format yyyyMMdd).bak"
Invoke-Sqlcmd -Query "BACKUP DATABASE [VMware DR] TO DISK = '$backupPath'" `
  -ServerInstance "localhost\VIMSERVICESRM"
```

### External Database (Enterprise deployments)

For > 250 VMs, use an external SQL Server or Oracle database. Configure during SRM Server installation.

Backup is handled by your standard SQL Server backup policy — include the SRM database (`VMware DR`) in your backup jobs.

### SRM Appliance (8.x+)

The SRM appliance uses an embedded vPostgres database. All configuration is stored in vCenter's DB (for Recovery Plans/Protection Groups) and the appliance's local config. The appliance has no separate DB backup procedure — use snapshot + vCenter VCSA backup.

---

## Protection Group Inventory Backup

Protection Group definitions live in vCenter, but the list of protected VMs and their configuration should also be documented externally for use during recovery when vCenter may be unavailable.

```powershell
# PowerCLI: Export all Protection Groups and their protected VMs
Import-Module VMware.VimAutomation.Srm

Connect-VIServer -Server vcenter-protected.example.com
$srm = Connect-SrmServer -SrmServerAddress srm-protected.example.com

$srmApi = $srm.ExtensionData

$output = @()
$pgs = $srmApi.Protection.ListProtectionGroups()
foreach ($pgRef in $pgs) {
    $pg = $pgRef.GetInfo()
    $vms = $pgRef.ListProtectedVms()
    foreach ($vm in $vms) {
        $output += [PSCustomObject]@{
            ProtectionGroup = $pg.Name
            VMName          = $vm.Vm.MoRef.Value
            State           = $vm.State
            PeerState       = $vm.PeerState
        }
    }
}

$output | Export-Csv -Path "C:\Backup\srm-protection-groups-$(Get-Date -Format yyyyMMdd).csv" -NoTypeInformation
Write-Host "Exported $($output.Count) protected VM entries"
```

---

## Restore SRM After vCenter Restore

When vCenter is restored from backup, SRM configuration (Recovery Plans, Protection Groups) is restored with it automatically — it lives in the vCenter database.

### Post-Restore Steps

1. **Verify site pairing** — if vCenter was restored to a point before pairing, re-pair the sites.
2. **Re-register SRA** — if SRM Server was also reinstalled, re-add Array Manager entries (credentials must be re-entered manually).
3. **Verify placeholder VMs** — run a **Configure All** on each Protection Group to ensure placeholder VMs exist at recovery site.
4. **Verify network mappings** — check that mappings are still valid (recovery site port groups may have changed).
5. **Run a test failover** — confirm Recovery Plans execute correctly post-restore.

### SRM Appliance Re-Deploy and Re-Register

If the SRM appliance itself must be re-deployed (not just restored):

```bash
# 1. Deploy new SRM OVA
# 2. During setup wizard, register with vCenter
# 3. If vCenter still has SRM extension from old appliance, unregister first:
#    vCenter → Administration → Solutions → Client Plugins
#    Remove old SRM plugin entries

# 4. After new registration, re-pair sites:
#    SRM UI → Site Recovery → New Site Pair

# 5. SRM reads Protection Groups and Recovery Plans from vCenter DB automatically
#    after pairing is established

# 6. Re-add Array Managers (SRA credentials not recovered from vCenter backup)
# 7. Scan arrays to re-discover replicated devices
# 8. Run Configure All on all Protection Groups
```

### Verify Recovery After Restore

```powershell
# PowerCLI: Check Protection Group health post-restore
$pgs = $srmApi.Protection.ListProtectionGroups()
foreach ($pgRef in $pgs) {
    $pg = $pgRef.GetInfo()
    Write-Host "PG: $($pg.Name) | State: $($pg.State)"
}

# Check placeholder VMs exist
$vms = $pgRef.ListProtectedVms()
foreach ($vm in $vms) {
    if ($vm.PeerState -ne "OK") {
        Write-Warning "Placeholder issue for VM: $($vm.Vm.MoRef.Value) — PeerState: $($vm.PeerState)"
    }
}
```
