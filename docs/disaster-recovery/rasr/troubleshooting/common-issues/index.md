# RASR — Common Issues


<div class="kb-summary">
> Part of the [RASR Troubleshooting](../index.md) reference.
</div>

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
```text
┌──────────────────────────────────────── RASR — Common Issues ─────────────────────────────────────────┐
│                                                                                                       │
│   │     Symptom      │   Likely Cause   │    First Check    │       Fix        │      Verify      │   │
│   │   Sync failed    │vault unreachable │ check airgap swit │ verify VLAN path │  ping vault mgm  │   │
│   │    Lock error    │vault already loc │ cr_vault_cli stat │force unlock+relo │    vault logs    │   │
│   │ CyberSense hang  │ scan job stalled │  cs_diag collect  │restart cs servic │    cs_status     │   │
│   │   Restore fail   │clean room nic er │ check clean-room  │ re-map portgroup │   vmnic check    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     General Triage Pattern                                    │   │
│   │          Is the issue new or recurring? New = recent change; Recurring = config problem       │   │
│   │             Is it isolated to one source or all? Isolated = agent; All = server/repo          │   │
│   │                                Check logs first: cybersense scan                              │   │
│   │                    If unresolved in 2h: open vendor case with full log bundle                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Isolated network segment (airgap switch) · Vault PowerStore/DD appliance · Clean-room ESXi hosts     │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RASR          = Ransomware Air-gap Secure Recovery; full workflow from detection to clean rest       │
│  Vault         = isolated, air-gapped storage appliance receiving periodic replication copies         │
│  Vault Lock    = WORM lock applied after sync; prevents modification or deletion of vault copies      │
│  CyberSense    = ML analytics engine scanning vault data for corruption, encryption signatures        │
│  PPDM          = PowerProtect Data Manager; orchestrates protection policies, jobs, and recovery      │
│  Air Gap       = physical or logical network isolation preventing attacker lateral movement to        │
│  Delta Set     = incremental changed blocks replicated from production to vault each cycle            │
│  Clean Room    = isolated recovery environment: separate vCenter, network, and workstations           │
│  Recovery Point= specific vault snapshot timestamp from which clean recovery is performed             │
│  Integrity Lock= two-person authorization required to open vault; prevents insider unlock attac       │
│  Journal       = write-order-consistent journal on vault enabling point-in-time recovery              │
│  Scan Report   = CyberSense output: clean/suspect classification per file and block                   │
│  Retention     = vault copy lifespan; typically 30–90 days of daily snapshots kept                    │
│  RTO           = Recovery Time Objective; time from failover decision to restored service             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

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
