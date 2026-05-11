# RASR — Health Checks

> Part of the [RASR Operations](../) reference.

---

Regular health checks verify that RASR is ready to perform a recovery — before an incident occurs. Run these on a monthly cadence and after any change to protected servers.

## Quick Health Check (5 minutes)

Run on each RASR-protected server:

```powershell
# Collect all key indicators in one pass
$rasrKey = "HKLM:\SOFTWARE\Dell\RASR"
$share   = "\\nas01\rasr-images\prod\$(hostname)"

[PSCustomObject]@{
    Server          = hostname
    AgentStatus     = (Get-Service RASRAgent).Status
    AgentVersion    = (Get-ItemProperty $rasrKey -ErrorAction SilentlyContinue).Version
    LastBackup      = (Get-ItemProperty $rasrKey -ErrorAction SilentlyContinue).LastBackupTime
    LastResult      = (Get-ItemProperty $rasrKey -ErrorAction SilentlyContinue).LastBackupResult
    BackupAge_h     = [math]::Round(((Get-Date) - [datetime](Get-ItemProperty $rasrKey).LastBackupTime).TotalHours, 1)
    ShareReachable  = (Test-Path $share)
    LatestImage     = (Get-ChildItem $share -Filter "*.wim" -ErrorAction SilentlyContinue |
                       Sort-Object LastWriteTime -Descending | Select-Object -First 1).Name
} | Format-List
```

**Pass criteria:**

| Check | Pass condition |
|---|---|
| AgentStatus | Running |
| LastResult | Success |
| BackupAge_h | < 26 (daily schedule) or < 170 (weekly schedule) |
| ShareReachable | True |
| LatestImage | File present, name matches expected naming standard |

## Full Health Check (30 minutes)

Run monthly and after any server change.

### 1. Agent and Schedule

```powershell
# Verify scheduled task is enabled and last run was successful
$task = Get-ScheduledTaskInfo -TaskName "RASR_DailyBackup" -ErrorAction SilentlyContinue
if ($task) {
    Write-Host "Last run: $($task.LastRunTime) | Result: $($task.LastTaskResult)"
    # LastTaskResult = 0 = success
} else {
    Write-Warning "RASR scheduled task not found"
}
```

### 2. Image Integrity

```powershell
# Verify the most recent image is readable (DISM metadata check — does not restore)
$imagePath = (Get-ChildItem "\\nas01\rasr-images\prod\$(hostname)" -Filter "*.wim" |
              Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName

if ($imagePath) {
    $result = dism /Get-ImageInfo /ImageFile:$imagePath 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "PASS: Image readable — $imagePath"
    } else {
        Write-Warning "FAIL: Image unreadable — $imagePath"
        Write-Warning $result
    }
} else {
    Write-Warning "No image found in share"
}
```

### 3. Recovery Share Capacity

```powershell
# Check free space on the recovery share host
$share = "\\nas01\rasr-images"
$disk  = Get-PSDrive -Name Z -ErrorAction SilentlyContinue
if (-not $disk) { net use Z: $share /persistent:no | Out-Null; $disk = Get-PSDrive Z }

$freeGB  = [math]::Round($disk.Free / 1GB, 1)
$totalGB = [math]::Round(($disk.Free + $disk.Used) / 1GB, 1)
$pctFree = [math]::Round($disk.Free / ($disk.Free + $disk.Used) * 100, 1)

Write-Host "Recovery share: ${freeGB} GB free of ${totalGB} GB (${pctFree}% free)"
if ($pctFree -lt 20) { Write-Warning "ALERT: Less than 20% free on recovery share" }
```

### 4. VSS Writer Health

```powershell
# Check VSS writers are in stable state
$writers = vssadmin list writers 2>&1
$failed = $writers | Select-String "State: \[8\] Failed"
if ($failed) {
    Write-Warning "FAIL: VSS writers in failed state:"
    $failed
} else {
    Write-Host "PASS: All VSS writers stable"
}
```

### 5. iDRAC Media Mapping Test

Test via iDRAC web UI (cannot be scripted without Redfish):

```
iDRAC → Configuration → Virtual Media → Verify ISO is mapped
iDRAC → Overview → Boot → Boot Next = Virtual Optical Drive
(Optional: perform test boot in next maintenance window)
```

```bash
# Via Redfish API
curl -sk -u root:<password> \
  https://<idrac-ip>/redfish/v1/Managers/iDRAC.Embedded.1/VirtualMedia \
  | python3 -m json.tool
```

## Fleet-Wide Health Check

Run monthly across all RASR-protected servers:

```powershell
$servers = @("app01", "app02", "db01", "web01")   # update per environment

$report = foreach ($server in $servers) {
    try {
        $result = Invoke-Command -ComputerName $server -ScriptBlock {
            $k = "HKLM:\SOFTWARE\Dell\RASR"
            $lastBkp = [datetime](Get-ItemProperty $k -ErrorAction Stop).LastBackupTime
            @{
                Agent   = (Get-Service RASRAgent).Status
                AgeH    = [math]::Round(((Get-Date) - $lastBkp).TotalHours, 1)
                Result  = (Get-ItemProperty $k).LastBackupResult
            }
        } -ErrorAction Stop

        [PSCustomObject]@{
            Server  = $server
            Agent   = $result.Agent
            AgeH    = $result.AgeH
            Result  = $result.Result
            Status  = if ($result.Agent -eq "Running" -and $result.Result -eq "Success" -and $result.AgeH -lt 26) {"OK"} else {"REVIEW"}
        }
    } catch {
        [PSCustomObject]@{ Server = $server; Agent = "UNREACHABLE"; AgeH = 0; Result = "N/A"; Status = "REVIEW" }
    }
}

$report | Sort-Object Status -Descending | Format-Table
```

## Health Check Sign-Off

Document results monthly in the DR register:

```
Date: ___________  Performed by: ___________
Servers checked: ___ / ___
Servers passing all checks: ___ / ___
Issues found: ___________
Actions taken: ___________
Next check due: ___________
```
