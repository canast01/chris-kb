# Rollback Planning

Rollback options differ significantly by component. Establish the rollback path before the maintenance window — not during an incident.
## Rollback Readiness by Component

| Component | Rollback Method | Practical Rollback? | Notes |
|---|---|---|---|
| vCenter VCSA | File-based backup restore | Yes | Restore takes 30–60 min; restores to pre-upgrade state |
| ESXi host | Boot from previous bootbank | Yes | `esxcfg-bootcfg --server` or BIOS boot order |
| NSX Manager | NSX backup + restore | Partial | NSX restore is complex; plan for 2–4h |
| vSAN | No direct rollback | No | ESXi rollback covers vSAN; test object health post-upgrade |
| VxRail | VxRail support-assisted | Vendor-only | Dell must be engaged for any VxRail rollback |
| Aria LCM / Products | Snapshot before upgrade | Yes (if snapped) | Requires snapshot taken on appliance before upgrade starts |
| SRM | SRM backup + redeploy | Partial | Site pair must be broken and re-established if SRM is redeployed |
| VMware Tools | Automatic downgrade via vCenter | Yes | Tools version can be pinned |
| VM Hardware | No rollback | No | Hardware version upgrades are permanent |

## vCenter Rollback (File-Based Backup)

```bash
# Verify backup exists (VAMI → Backup → show recent backups)
# Backup location: defined at backup job configuration time

# To restore: boot VCSA installer ISO → choose Restore
# Provide backup file path (FTP/HTTP/SCP/SMB) and SSO admin credentials
# Restoration process: ~45 minutes + replication sync time
```

**Before upgrade:**
1. Confirm a file-based backup completed within 24 hours of the maintenance window.
2. Verify the backup is accessible from the restore location.
3. Document the current vCenter build number: `Get-View ServiceInstance | Select-Object -ExpandProperty ServerVersion`.

## ESXi Bootbank Rollback

ESXi maintains two bootbanks — the active one and the previous version:

```bash
# SSH to ESXi host — check bootbank contents
esxcli system version get
ls /bootbank /altbootbank

# Switch to previous bootbank (requires reboot)
nextbootdir=/altbootbank
# Or via Host Client: Manage → System → Boot Options → select previous
```

This works immediately post-upgrade before any configuration changes are made. After hosts are rejoined to vCenter and NSX re-prepared, bootbank rollback becomes impractical.

## NSX Backup Before Upgrade

```bash
# Trigger NSX Manager backup via API
POST https://nsxmanager/api/v1/cluster/backups?action=start

# Verify backup completed
GET https://nsxmanager/api/v1/cluster/backups/history

# Backup stored to external SFTP target (configured in NSX → Backup & Restore)
```

## Aria Product Rollback (Snapshots)

Snapshot all Aria appliances before upgrade via LCM or directly:

```powershell
# Snapshot all Aria appliances before upgrade
$ariaVMs = @("aria-ops-01","aria-auto-01","aria-li-01","aria-lcm-01")
foreach ($vm in $ariaVMs) {
    New-Snapshot -VM $vm -Name "pre-upgrade-$(Get-Date -Format 'yyyyMMdd')" -Memory $false -Quiesce $false
}

# After upgrade validation — delete snapshots (performance impact)
foreach ($vm in $ariaVMs) {
    Get-VM $vm | Get-Snapshot | Where-Object { $_.Name -match "pre-upgrade" } | Remove-Snapshot -Confirm:$false
}
```

## Go / No-Go Decision Framework

Define a decision point at the end of the upgrade window:

| Condition | Decision |
|---|---|
| All hosts connected, all VMs running, no critical alarms | Go — close window |
| 1–2 non-critical issues, workarounds available | Go with action items |
| Core service degraded (vSAN, NSX DFW, vMotion broken) | No-Go — assess rollback |
| Production VMs inaccessible | No-Go — initiate rollback immediately |

Document decision and rationale in the change record.

## Rollback Communication

1. Declare rollback decision in the change record and notify change bridge.
2. Engage vendor support proactively (VMware/Broadcom, Dell) — have SR open before initiating rollback.
3. Communicate estimated recovery time to application owners.
4. Post-rollback: do not close the change — open a problem record and replan upgrade.
