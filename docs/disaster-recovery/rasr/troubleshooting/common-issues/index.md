# RASR — Common Issues

> Part of the [RASR Troubleshooting](../index.md) reference.

---

## Backup Failures

### Agent service not starting

```powershell
# Check service status
Get-Service RASRAgent

# Check Windows Event Log for service failure reason
Get-WinEvent -LogName System -MaxEvents 50 |
  Where-Object { $_.Message -match "RASRAgent" }

# Common fix: dependencies not started (Workstation service, TCP/IP NetBIOS Helper)
Get-Service -Name LanmanWorkstation, lmhosts | Start-Service
Start-Service RASRAgent
```
```

### Image capture completes but file is corrupted

```powershell
# Verify image integrity post-capture
# RASR images can be mounted and verified with DISM
dism /Get-ImageInfo /ImageFile:"\\nas01\rasr-images\prod\app01\app01_prod_20260510_001.wim"
# If this returns an error, the image is corrupt — initiate another capture immediately
```

---

## Recovery Failures

### WinPE boots but cannot see the network share

**Symptom:** RASR wizard starts, but the network share path returns "path not found" or "access denied".

**Causes and fixes:**

| Cause | Fix |
|---|---|
| Network driver not loaded | Verify server generation matches media driver pack; rebuild media for 15G/16G if needed |
| No IP assigned in WinPE | Run `wpeutil` → check IP; manually assign: `netsh interface ip set address "Ethernet" static 10.x.x.x 255.255.255.0 10.x.x.1` |
| Authentication failure | WinPE cannot use Kerberos — use NTLM/local credentials: `net use Z: \\nas01\rasr-images /user:nashost\localuser` |
| Firewall blocking 445 | Confirm no firewall rule blocks SMB from the recovery network VLAN to the NAS |

```cmd
:: From WinPE command prompt — test and map share
ping nas01
net use Z: \\nas01\rasr-images\prod\app01 /user:nashost\localuser
dir Z:\
```

### WinPE cannot see local disks

**Symptom:** RASR shows no disks or RAID array not visible during restore target selection.

```cmd
:: In WinPE: check if disks visible to diskpart
diskpart
list disk
exit

:: If no disks listed — storage driver not loaded
:: Load PERC driver from USB or share:
drvload D:\drivers\perc\percsas3i.inf
```

If the disk is still not visible, the RASR media may predate the server generation — rebuild using the correct driver pack.

### Restore completes but OS won't boot

**Symptom:** Image restored successfully, server reboots, but hangs at boot screen or fails with `BOOTMGR is missing`.

```cmd
:: From WinPE: repair boot record manually
bootrec /fixmbr
bootrec /fixboot
bootrec /rebuildbcd

:: If BitLocker was enabled, recovery key required at this point
manage-bde -unlock C: -RecoveryPassword <48-digit-key>
```

If the server hardware changed (new PERC controller generation), the restored OS may lack the storage driver. Inject it before rebooting:

```powershell
# Inject missing PERC driver into offline restored OS
dism /Image:C:\ /Add-Driver /Driver:D:\drivers\perc\percsas3i.inf /ForceUnsigned
```

### Restore takes much longer than expected

| Cause | Diagnosis | Fix |
|---|---|---|
| Single network path (no multipath) | Check NIC teaming in WinPE — only one adapter active | Manually configure NIC teaming in WinPE if supported |
| Share on spinning disk with high latency | Check NAS I/O during restore | No fix in-flight; schedule future restores during off-peak |
| Image fragmented on share | Image file has high fragmentation | Defragment the share after migration; store new images sequentially |

---

## Agent and Schedule Issues

### Scheduled backup not running

```powershell
# Verify RASR schedule is configured
Get-ScheduledTask | Where-Object { $_.TaskName -match "RASR" }

# Check last run time and result
Get-ScheduledTaskInfo -TaskName "RASR_DailyBackup"

# If task exists but not running: check task conditions (power, network, idle conditions)
$task = Get-ScheduledTask -TaskName "RASR_DailyBackup"
$task.Settings | Select-Object RunOnlyIfNetworkAvailable, RunOnlyIfIdle, WakeToRun
```

### Backup log shows VSS errors

```text
Error: VSS writer reported failure — Microsoft Hyper-V VSS Writer / SQL Server VSS Writer
```

```powershell
# Check VSS writer status
vssadmin list writers | Select-String -Pattern "State:|Writer name:"

# Restart VSS service and writers
Restart-Service -Name VSS, vds
# For SQL VSS writer:
Restart-Service -Name SQLWriter
```

---

## Common Issue Summary

| Symptom | Most likely cause | First action |
|---|---|---|
| Backup fails nightly | Share credential expired or account locked | Reset RASR service account password; unlock account |
| WinPE shows no network | Wrong driver pack for server generation | Rebuild media using correct Dell driver pack |
| WinPE shows no disks | PERC driver missing from media | Load PERC driver from USB; rebuild media |
| Restore completes, OS won't boot | BCD corruption or driver mismatch | Run `bootrec /rebuildbcd`; inject missing storage driver |
| Image file is 0 bytes | Agent crashed mid-capture | Check VSS writers; restart agent; re-run capture |
| Agent service crashes on start | Corrupted installation | Reinstall RASR agent from Dell OpenManage package |
