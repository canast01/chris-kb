# RASR — Diagnostics

> Part of the [RASR Troubleshooting](../) reference.

---

## Log Locations

| Log | Path | When to check |
|---|---|---|
| RASR application log | `C:\Logs\RASR\rasrutil_<date>.log` | All backup and restore failures |
| RASR agent log | `C:\Logs\RASR\rasragent_<date>.log` | Agent start failures, scheduler issues |
| Windows Application Event Log | Event Viewer → Application (Source: `Dell RASR`) | Agent crashes, VSS errors, service errors |
| Windows System Event Log | Event Viewer → System | Service control errors, disk errors |
| Windows Setup Event Log | `C:\Windows\Panther\setupact.log` | WinPE driver and ADK failures during media creation |
| iDRAC Lifecycle Controller log | iDRAC web UI → Maintenance → Lifecycle Log | Boot failures, hardware events during recovery |
| WinPE session log | `X:\Windows\Panther\setupact.log` | WinPE environment errors during recovery |

### Collecting RASR logs

```powershell
# View most recent RASR logs
$logDir = "C:\Logs\RASR"
Get-ChildItem -Path $logDir -Filter "*.log" | Sort-Object LastWriteTime -Descending | Select-Object -First 5

# Tail the current log for live output
Get-Content "C:\Logs\RASR\rasrutil_$(Get-Date -Format 'yyyyMMdd').log" -Wait -Tail 50

# Export Windows Application events from Dell RASR source
Get-WinEvent -FilterHashtable @{LogName='Application'; ProviderName='DellRASR'} -MaxEvents 100 |
    Select-Object TimeCreated, Id, LevelDisplayName, Message |
    Export-Csv "C:\Temp\RASR-AppEvents.csv" -NoTypeInformation
```

---

## Agent and Service Diagnostics

```powershell
# Check RASR agent service state
Get-Service -Name RASRAgent | Select-Object Name, Status, StartType

# Check dependent services are running
Get-Service -Name LanmanWorkstation, lmhosts | Select-Object Name, Status

# View recent service control events (Event ID 7000/7034/7036 = service errors)
Get-WinEvent -FilterHashtable @{LogName='System'; Id=7000,7034,7036} -MaxEvents 20 |
    Where-Object { $_.Message -match "RASR" }

# Start the agent service
Start-Service RASRAgent

# If service fails to start: check binary and path
Get-Item "C:\Program Files\Dell\RASR\rasrutil.exe" | Select-Object FullName, VersionInfo

# Check RASR version
(Get-Item "C:\Program Files\Dell\RASR\rasrutil.exe").VersionInfo.FileVersion
```

---

## Backup Job Diagnostics

```powershell
# Run a manual backup and capture exit code
& "C:\Program Files\Dell\RASR\rasrutil.exe" /backup /destination "\\nas01\rasr-images\$env:COMPUTERNAME"
Write-Host "Exit code: $LASTEXITCODE"

# RASR exit codes:
# 0  = Success
# 1  = General error
# 3  = Destination not accessible
# 4  = Insufficient space on destination
# 5  = Image file corrupt
# 6  = Restore target disk not found
# 10 = Authentication failure

# Verify an existing image
& "C:\Program Files\Dell\RASR\rasrutil.exe" /verify /source "\\nas01\rasr-images\$env:COMPUTERNAME\latest.wim"
Write-Host "Verify exit code: $LASTEXITCODE"

# List images on share to confirm backup exists
Get-ChildItem "\\nas01\rasr-images\$env:COMPUTERNAME" | Sort-Object LastWriteTime -Descending | Select-Object -First 10
```

---

## Network Share Diagnostics

```powershell
# Test TCP connectivity to NAS on SMB port
Test-NetConnection -ComputerName nas01 -Port 445

# Test share path is reachable
Test-Path "\\nas01\rasr-images\$env:COMPUTERNAME"

# Test authentication explicitly
net use \\nas01\rasr-images /user:domain\rasr-svc
# If fails: check password expiry, account lockout, firewall on port 445

# Check SMB signing compatibility (mismatch can cause silent failures)
Get-SmbClientConfiguration | Select-Object RequireSecuritySignature
Get-SmbServerConfiguration | Select-Object RequireSecuritySignature

# Check share space available
$share = "\\nas01\rasr-images"
$drive = New-PSDrive -Name "NASCheck" -PSProvider FileSystem -Root $share -Credential (Get-Credential) -Temporary
Get-PSDrive NASCheck | Select-Object Name, Used, Free
```

---

## VSS Diagnostics

RASR uses Windows Volume Shadow Copy Service (VSS) for consistent image capture. VSS failures cause backup aborts.

```powershell
# Check all VSS writer states — all should show "Stable"
vssadmin list writers | Select-String -Pattern "Writer name:|State:|Last error:"

# Common problematic writers:
# Microsoft Hyper-V VSS Writer — if Hyper-V is installed
# SQL Server VSS Writer — if SQL is installed
# Registry Writer, System Writer — always present

# Restart VSS and related services to clear stuck writers
Restart-Service -Name VSS, vds -Force
Start-Sleep -Seconds 10

# Restart specific writers if needed
Restart-Service -Name SQLWriter    # SQL Server VSS writer
Restart-Service -Name wbengine     # Windows Backup VSS writer

# Re-check writers after restart
vssadmin list writers | Select-String -Pattern "Writer name:|State:|Last error:"
```

---

## Scheduled Task Diagnostics

```powershell
# Find RASR scheduled tasks
Get-ScheduledTask | Where-Object { $_.TaskName -match "RASR" }

# Check last run time and result code
Get-ScheduledTaskInfo -TaskName "RASR_DailyBackup"
# LastTaskResult: 0 = success, non-zero = error

# Check task conditions that could prevent execution
$task = Get-ScheduledTask -TaskName "RASR_DailyBackup"
$task.Settings | Select-Object RunOnlyIfNetworkAvailable, RunOnlyIfIdle, WakeToRun, StopIfGoingOnBatteries

# Run task manually to test
Start-ScheduledTask -TaskName "RASR_DailyBackup"

# View scheduled task history (requires history enabled)
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-TaskScheduler/Operational'} -MaxEvents 50 |
    Where-Object { $_.Message -match "RASR" } |
    Select-Object TimeCreated, Id, Message
```

---

## WinPE Recovery Environment Diagnostics

Run these commands from the WinPE command prompt during a recovery session.

```cmd
:: Confirm network adapter is up and has an IP
ipconfig /all

:: If no IP — set manually
netsh interface ip set address "Ethernet" static 10.10.10.50 255.255.255.0 10.10.10.1
netsh interface ip set dns "Ethernet" static 10.10.10.10

:: Test connectivity to NAS
ping nas01
net use Z: \\nas01\rasr-images\SERVER01 /user:nashost\localuser

:: Check if local disks are visible to diskpart
diskpart
list disk
exit

:: If no disks visible — load PERC/storage driver
drvload D:\drivers\perc\percsas3i.inf
```

After a restore completes but the OS does not boot:

```cmd
:: Repair boot configuration data from WinPE
bootrec /fixmbr
bootrec /fixboot
bootrec /scanos
bootrec /rebuildbcd
```

---

## iDRAC Diagnostics for Recovery Boot Failures

```bash
# Export Lifecycle Controller log via racadm (from management host)
racadm -r <idrac-ip> -u root -p <password> lclog export -f lclog.xml -t XML

# Export System Event Log
racadm -r <idrac-ip> -u root -p <password> getsel > sel.txt

# Check POST status
racadm -r <idrac-ip> -u root -p <password> getsysinfo

# Mount ISO via virtual media (for headless recovery)
racadm -r <idrac-ip> -u root -p <password> remoteimage -c -l "\\fileserver\iso\rasr_winpe.iso"
racadm -r <idrac-ip> -u root -p <password> remoteimage -s
```

Or from the iDRAC web UI: **Maintenance** → **Virtual Media** → connect ISO, then **Power** → **Boot to Virtual CD**.

---

## System Information Collection

```powershell
# Collect system and RASR version info for support cases
$info = @{
    Hostname      = $env:COMPUTERNAME
    OS            = (Get-WmiObject Win32_OperatingSystem).Caption
    OSBuild       = (Get-WmiObject Win32_OperatingSystem).BuildNumber
    RASRVersion   = (Get-Item "C:\Program Files\Dell\RASR\rasrutil.exe").VersionInfo.FileVersion
    DellModel     = (Get-WmiObject Win32_ComputerSystem).Model
    ServiceTag    = (Get-WmiObject Win32_BIOS).SerialNumber
    RASRService   = (Get-Service RASRAgent -ErrorAction SilentlyContinue).Status
}

$info | ConvertTo-Json | Tee-Object -FilePath "C:\Temp\RASR-SystemInfo.json"
```
