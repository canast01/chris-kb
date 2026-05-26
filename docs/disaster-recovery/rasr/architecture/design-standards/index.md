# RASR — Standards

> Part of the [RASR Architecture](../index.md) reference.

---

Standards for RASR deployment, image management, testing, and recovery readiness across Dell PowerEdge environments.

## Backup Frequency Standards

| Server criticality | Capture frequency | Retention |
|---|---|---|
| **Tier 1** — production database/app servers | Daily, after patch events | 7 daily + 4 weekly |
| **Tier 2** — secondary production servers | Weekly | 4 weekly + 2 monthly |
| **Tier 3** — non-production | Monthly or post-build | 3 monthly |
| **Any tier** — after OS change | Within 24 hours of change | Retain indefinitely until next planned capture |

Always capture immediately after:
- OS patching and reboot
- Driver or firmware updates
- Application installation on the OS volume
- System configuration changes

## Image Naming Convention

```text
Format: <hostname>_<environment>_<date>_<sequence>

Examples:
  app01_prod_20260510_001.wim
  db02_prod_20260503_weekly.wim
  dc01_prod_20260101_post-patch.wim
```
```

## Storage Sizing

```text
Estimate per server:
  Compressed image size = OS volume used space × 0.5
  
  Retention space = images_kept × compressed_image_size × 1.1 (headroom)

Example:
  Server with 60 GB used on OS volume
  Compressed image: 60 × 0.5 = 30 GB
  7 daily + 4 weekly = 11 images
  Required space: 11 × 30 × 1.1 = 363 GB per server
```

## Recovery Media Standards

| Requirement | Standard |
|---|---|
| Media format | ISO file stored on the recovery share alongside images |
| iDRAC mapping | Pre-mapped and tested quarterly — do not wait until an incident |
| WinPE version match | Media must match the server generation's driver pack (14G/15G/16G) |
| Media refresh cycle | Rebuild media after each RASR agent update |
| Physical USB | One USB per rack; labeled with server generation and last verified date |

## Test and Validation Schedule

| Test type | Frequency | Scope | Evidence required |
|---|---|---|---|
| **Boot media test** | Quarterly | Boot WinPE from iDRAC; confirm network access and share connectivity | Screenshot of share connection from WinPE |
| **Full restore test** | Semi-annually | Restore to an isolated VM; verify OS boots | Restore completion log + screenshot |
| **Partial restore test** | Quarterly | File-level recovery from image | File hash comparison |
| **Schedule verification** | Monthly | Confirm backups are completing per schedule | Backup log review + OMSA alert check |

```powershell
# Monthly schedule verification script
$servers = @("app01", "db02", "web01")
foreach ($server in $servers) {
    $img = Get-ChildItem "\\nas01\rasr-images\prod\$server\" |
           Sort-Object LastWriteTime -Descending | Select-Object -First 1
    $age = (Get-Date) - $img.LastWriteTime
    [PSCustomObject]@{
        Server     = $server
        LastImage  = $img.LastWriteTime
        AgeHours   = [math]::Round($age.TotalHours, 1)
        Status     = if ($age.TotalHours -lt 26) {"OK"} else {"ALERT — overdue"}
    }
} | Format-Table
```

## Access Control Standards

| Access type | Who | Permission level |
|---|---|---|
| Recovery share — write | RASR service account only | Write to server-specific subfolder |
| Recovery share — read | Recovery operators, DR team | Read-only across all subfolders |
| iDRAC virtual media | DR team, platform leads | Map/mount virtual media |
| RASR Console | Server administrators | Local admin on protected server |
| Boot media ISO | All operators | Read from share |

The RASR service account must not have local admin rights beyond what RASR requires. It should not have interactive logon rights.

## Documentation Requirements

For each protected server, maintain:

1. **Recovery card** — physical or digital record containing:
   - Server hostname and iDRAC IP
   - Recovery share path
   - Last successful backup date
   - Recovery operator contact

2. **Image log** — spreadsheet or CMDB entry tracking:
   - Image filename
   - Capture date
   - OS version and patch level at time of capture
   - Capture trigger (scheduled / post-patch / manual)

3. **Test evidence** — for each test:
   - Date, tester name, test type
   - Pass/fail result
   - Time to complete restore
   - Issues found and resolution

## Monitoring and Alerting

| Alert | Threshold | Destination |
|---|---|---|
| Backup not completed | > 26 hours since last successful image | Email to platform team |
| Agent service not running | RASRAgent stopped | SNMP trap + email |
| Share space < 20% | Recovery share below 20% free | Email to storage team |
| Test overdue | > 90 days since last boot test | Ticketing system (auto-created) |
