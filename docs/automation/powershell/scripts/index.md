# Scripts

> Part of the [PowerShell](../) reference.

---

## Windows Server Health Check (PowerShell)

Connect to remote servers via `Invoke-Command`, collect disk, memory, CPU, top processes, stopped automatic services, last boot time, and pending reboot status, then export results to CSV.

~~~powershell
#!/usr/bin/env pwsh
# windows-health-check.ps1
# Usage: ./windows-health-check.ps1 -Servers server1,server2,server3 [-ExportCsv health-report.csv]

param(
    [Parameter(Mandatory)]
    [string[]]$Servers,

    [System.Management.Automation.PSCredential]
    $Credential,

    [string]$ExportCsv = "health-report-$(Get-Date -Format 'yyyyMMdd-HHmmss').csv"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Results = [System.Collections.Generic.List[PSObject]]::new()

$ScriptBlock = {
    $os      = Get-CimInstance -ClassName Win32_OperatingSystem
    $cs      = Get-CimInstance -ClassName Win32_ComputerSystem
    $cpu     = (Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 2 -MaxSamples 2).CounterSamples |
               Measure-Object CookedValue -Average | Select-Object -ExpandProperty Average

    # Disk usage
    $disks = Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Used -gt 0 } | ForEach-Object {
        $total = $_.Used + $_.Free
        $pct   = if ($total -gt 0) { [math]::Round(($_.Used / $total) * 100, 1) } else { 0 }
        [PSCustomObject]@{ Drive = $_.Name; UsedGB = [math]::Round($_.Used/1GB,2); TotalGB = [math]::Round($total/1GB,2); UsedPct = $pct }
    }
    $highDisks = $disks | Where-Object { $_.UsedPct -ge 85 }

    # Memory
    $totalMemGB = [math]::Round($cs.TotalPhysicalMemory / 1GB, 2)
    $freeMemGB  = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
    $usedMemPct = [math]::Round((($totalMemGB - $freeMemGB) / $totalMemGB) * 100, 1)

    # Top 5 processes by working set
    $topProcs = Get-Process | Sort-Object WorkingSet64 -Descending |
                Select-Object -First 5 -Property Name, Id,
                    @{n='MemMB';e={[math]::Round($_.WorkingSet64/1MB,1)}}

    # Stopped automatic services
    $stoppedSvcs = Get-Service |
                   Where-Object { $_.Status -eq 'Stopped' -and $_.StartType -eq 'Automatic' } |
                   Select-Object Name, DisplayName

    # Last boot
    $lastBoot = $os.LastBootUpTime

    # Pending reboot (check common registry keys)
    $pendingReboot = $false
    $rebootKeys = @(
        'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired',
        'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\PendingFileRenameOperations',
        'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending'
    )
    foreach ($key in $rebootKeys) {
        if (Test-Path $key) { $pendingReboot = $true; break }
    }

    return [PSCustomObject]@{
        Hostname        = $env:COMPUTERNAME
        CPUPct          = [math]::Round($cpu, 1)
        MemTotalGB      = $totalMemGB
        MemUsedPct      = $usedMemPct
        HighDiskDrives  = ($highDisks | ForEach-Object { "$($_.Drive): $($_.UsedPct)%" }) -join '; '
        StoppedAutoSvcs = ($stoppedSvcs | ForEach-Object { $_.Name }) -join '; '
        LastBoot        = $lastBoot.ToString('yyyy-MM-dd HH:mm:ss')
        PendingReboot   = $pendingReboot
        TopProcs        = ($topProcs | ForEach-Object { "$($_.Name)($($_.MemMB)MB)" }) -join '; '
    }
}

Write-Host "`n=== Windows Server Health Check ===" -ForegroundColor Cyan
Write-Host "Servers: $($Servers -join ', ')"
Write-Host "Time   : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n"

foreach ($Server in $Servers) {
    Write-Host "Checking $Server..." -NoNewline
    try {
        $params = @{ ComputerName = $Server; ScriptBlock = $ScriptBlock }
        if ($Credential) { $params['Credential'] = $Credential }
        $result = Invoke-Command @params
        $Results.Add($result)
        Write-Host " OK" -ForegroundColor Green
    } catch {
        Write-Host " FAILED: $($_.Exception.Message)" -ForegroundColor Red
        $Results.Add([PSCustomObject]@{ Hostname = $Server; Error = $_.Exception.Message })
    }
}

# Print table
Write-Host ""
$Results | Format-Table -AutoSize

# Flag issues
Write-Host "Issues:" -ForegroundColor Yellow
foreach ($r in $Results) {
    if ($r.CPUPct -ge 90)          { Write-Host "  [$($r.Hostname)] HIGH CPU: $($r.CPUPct)%" -ForegroundColor Red }
    if ($r.MemUsedPct -ge 90)      { Write-Host "  [$($r.Hostname)] HIGH MEMORY: $($r.MemUsedPct)%" -ForegroundColor Red }
    if ($r.HighDiskDrives)         { Write-Host "  [$($r.Hostname)] HIGH DISK: $($r.HighDiskDrives)" -ForegroundColor Red }
    if ($r.StoppedAutoSvcs)        { Write-Host "  [$($r.Hostname)] STOPPED SERVICES: $($r.StoppedAutoSvcs)" -ForegroundColor Yellow }
    if ($r.PendingReboot -eq $true){ Write-Host "  [$($r.Hostname)] PENDING REBOOT" -ForegroundColor Yellow }
}

# Export to CSV
$Results | Export-Csv -Path $ExportCsv -NoTypeInformation
Write-Host "`nExported: $ExportCsv"
~~~

---

## Active Directory User Audit (PowerShell)

Audit Active Directory for inactive accounts, non-expiring passwords, expired passwords, privileged group membership, and orphaned admin accounts. Exports each finding to CSV.

~~~powershell
#!/usr/bin/env pwsh
# ad-user-audit.ps1
# Usage: ./ad-user-audit.ps1 [-OutputDir C:\Reports]
# Requires: ActiveDirectory module (RSAT)

param(
    [string]$OutputDir = ".",
    [int]$InactiveDays = 90
)

Import-Module ActiveDirectory -ErrorAction Stop

$Timestamp   = Get-Date -Format 'yyyyMMdd-HHmmss'
$InactiveDate = (Get-Date).AddDays(-$InactiveDays)
$PrivGroups  = @('Domain Admins', 'Enterprise Admins', 'Schema Admins', 'Backup Operators', 'Account Operators')

Write-Host "`n=== Active Directory User Audit ===" -ForegroundColor Cyan
Write-Host "Domain  : $((Get-ADDomain).DNSRoot)"
Write-Host "Time    : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n"

# --- 1. Inactive accounts (no logon > N days) ---
Write-Host "1. Accounts inactive for > $InactiveDays days..."
$Inactive = Search-ADAccount -AccountInactive -TimeSpan ([TimeSpan]::FromDays($InactiveDays)) -UsersOnly |
    Get-ADUser -Properties LastLogonDate, Enabled, DistinguishedName |
    Select-Object SamAccountName, DisplayName, Enabled, LastLogonDate, DistinguishedName
Write-Host "   Found: $($Inactive.Count)"
$Inactive | Export-Csv "$OutputDir\audit-inactive-$Timestamp.csv" -NoTypeInformation

# --- 2. Passwords set to never expire ---
Write-Host "2. Accounts with passwords set to never expire..."
$NeverExpire = Get-ADUser -Filter { PasswordNeverExpires -eq $true -and Enabled -eq $true } `
    -Properties PasswordNeverExpires, PasswordLastSet, LastLogonDate |
    Select-Object SamAccountName, DisplayName, PasswordLastSet, LastLogonDate
Write-Host "   Found: $($NeverExpire.Count)"
$NeverExpire | Export-Csv "$OutputDir\audit-never-expire-$Timestamp.csv" -NoTypeInformation

# --- 3. Accounts with expired passwords ---
Write-Host "3. Accounts with expired passwords..."
$PasswordExpired = Search-ADAccount -PasswordExpired -UsersOnly |
    Get-ADUser -Properties PasswordExpired, PasswordLastSet, Enabled |
    Where-Object { $_.Enabled } |
    Select-Object SamAccountName, DisplayName, PasswordLastSet
Write-Host "   Found: $($PasswordExpired.Count)"
$PasswordExpired | Export-Csv "$OutputDir\audit-pw-expired-$Timestamp.csv" -NoTypeInformation

# --- 4. Members of sensitive privileged groups ---
Write-Host "4. Members of sensitive groups..."
$PrivReport = [System.Collections.Generic.List[PSObject]]::new()
foreach ($GroupName in $PrivGroups) {
    try {
        $Members = Get-ADGroupMember -Identity $GroupName -Recursive |
                   Where-Object { $_.objectClass -eq 'user' } |
                   Get-ADUser -Properties LastLogonDate, Enabled, PasswordLastSet
        foreach ($m in $Members) {
            $PrivReport.Add([PSCustomObject]@{
                Group           = $GroupName
                SamAccountName  = $m.SamAccountName
                DisplayName     = $m.DisplayName
                Enabled         = $m.Enabled
                LastLogon       = $m.LastLogonDate
                PasswordLastSet = $m.PasswordLastSet
            })
        }
        Write-Host "   $GroupName : $($Members.Count) member(s)"
    } catch {
        Write-Host "   $GroupName : not found or access denied" -ForegroundColor Yellow
    }
}
$PrivReport | Export-Csv "$OutputDir\audit-priv-groups-$Timestamp.csv" -NoTypeInformation

# --- 5. Orphaned admin accounts (adminCount=1 but not in any known priv group) ---
Write-Host "5. Checking for orphaned admin accounts (adminCount=1)..."
$AdminCount1 = Get-ADUser -LDAPFilter '(adminCount=1)' -Properties adminCount, MemberOf, LastLogonDate, Enabled |
    Select-Object SamAccountName, DisplayName, Enabled, LastLogonDate,
        @{n='GroupCount';e={($_.MemberOf | Measure-Object).Count}}
$PrivGroupDNs = $PrivGroups | ForEach-Object {
    try { (Get-ADGroup -Identity $_).DistinguishedName } catch { $null }
} | Where-Object { $_ }
$Orphaned = $AdminCount1 | Where-Object {
    $user = Get-ADUser -Identity $_.SamAccountName -Properties MemberOf
    ($user.MemberOf | Where-Object { $PrivGroupDNs -contains $_ }).Count -eq 0
}
Write-Host "   Orphaned admin accounts: $($Orphaned.Count)"
$Orphaned | Export-Csv "$OutputDir\audit-orphaned-admin-$Timestamp.csv" -NoTypeInformation

# --- Summary ---
Write-Host ""
Write-Host "=== Audit Summary ===" -ForegroundColor Cyan
Write-Host "Inactive accounts (>$InactiveDays days) : $($Inactive.Count)"
Write-Host "Passwords never expire                   : $($NeverExpire.Count)"
Write-Host "Passwords expired (enabled)              : $($PasswordExpired.Count)"
Write-Host "Privileged group members                 : $($PrivReport.Count)"
Write-Host "Orphaned admin accounts                  : $($Orphaned.Count)"
Write-Host ""
Write-Host "Reports saved to: $OutputDir" -ForegroundColor Green
~~~

---

## Certificate Expiry Monitor (PowerShell)

Scan Windows servers for expiring certificates in the LocalMachine\My store and IIS SSL bindings, flag those expiring within configurable warning and critical thresholds, and send an email report.

~~~powershell
#!/usr/bin/env pwsh
# cert-expiry-monitor.ps1
# Usage: ./cert-expiry-monitor.ps1 -Servers server1,server2 -SmtpServer smtp.example.com -AlertEmail ops@example.com

param(
    [Parameter(Mandatory)]
    [string[]]$Servers,

    [System.Management.Automation.PSCredential]
    $Credential,

    [int]$WarnDays  = 30,
    [int]$CritDays  = 14,
    [string]$SmtpServer  = $env:SMTP_SERVER,
    [string]$AlertEmail  = $env:ALERT_EMAIL,
    [string]$FromEmail   = "cert-monitor@$((Get-ADDomain -ErrorAction SilentlyContinue).DNSRoot)"
)

Set-StrictMode -Version Latest

$AllCerts = [System.Collections.Generic.List[PSObject]]::new()

$CertScript = {
    param($WarnDays, $CritDays)

    $findings = [System.Collections.Generic.List[PSObject]]::new()
    $now      = Get-Date

    # LocalMachine\My store
    $certs = Get-ChildItem Cert:\LocalMachine\My
    foreach ($cert in $certs) {
        $daysLeft = ($cert.NotAfter - $now).Days
        $severity = if ($daysLeft -le $CritDays) { "CRITICAL" }
                    elseif ($daysLeft -le $WarnDays) { "WARNING" }
                    else { "OK" }
        $findings.Add([PSCustomObject]@{
            Server      = $env:COMPUTERNAME
            Subject     = $cert.Subject
            Thumbprint  = $cert.Thumbprint
            Expiry      = $cert.NotAfter.ToString('yyyy-MM-dd')
            DaysLeft    = $daysLeft
            Store       = "LocalMachine\My"
            Service     = "Certificate Store"
            Severity    = $severity
        })
    }

    # IIS SSL bindings (if IIS is installed)
    try {
        Import-Module WebAdministration -ErrorAction Stop
        $sites = Get-WebSite
        foreach ($site in $sites) {
            $bindings = $site.Bindings.Collection | Where-Object { $_.Protocol -eq 'https' }
            foreach ($binding in $bindings) {
                $hash = $binding.CertificateHash
                if (-not $hash) { continue }
                $thumbprint = ($hash | ForEach-Object { $_.ToString('X2') }) -join ''
                $cert = Get-ChildItem Cert:\LocalMachine\My |
                        Where-Object { $_.Thumbprint -eq $thumbprint } |
                        Select-Object -First 1
                if (-not $cert) { continue }
                $daysLeft = ($cert.NotAfter - $now).Days
                $severity = if ($daysLeft -le $CritDays) { "CRITICAL" }
                            elseif ($daysLeft -le $WarnDays) { "WARNING" }
                            else { "OK" }
                $findings.Add([PSCustomObject]@{
                    Server      = $env:COMPUTERNAME
                    Subject     = $cert.Subject
                    Thumbprint  = $thumbprint
                    Expiry      = $cert.NotAfter.ToString('yyyy-MM-dd')
                    DaysLeft    = $daysLeft
                    Store       = "IIS Binding"
                    Service     = "$($site.Name) ($($binding.BindingInformation))"
                    Severity    = $severity
                })
            }
        }
    } catch {
        # IIS not installed or WebAdministration not available — skip silently
    }

    return $findings
}

Write-Host "`n=== Certificate Expiry Monitor ===" -ForegroundColor Cyan
Write-Host "Servers  : $($Servers -join ', ')"
Write-Host "Warn     : < $WarnDays days | Crit: < $CritDays days`n"

foreach ($Server in $Servers) {
    Write-Host "Scanning $Server..." -NoNewline
    try {
        $params = @{
            ComputerName = $Server
            ScriptBlock  = $CertScript
            ArgumentList = $WarnDays, $CritDays
        }
        if ($Credential) { $params['Credential'] = $Credential }
        $certs = Invoke-Command @params
        $AllCerts.AddRange($certs)
        Write-Host " OK ($($certs.Count) certs)" -ForegroundColor Green
    } catch {
        Write-Host " FAILED: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Display results
Write-Host ""
$AllCerts | Sort-Object DaysLeft |
    Format-Table Server, Subject, Expiry, DaysLeft, Severity, Service -AutoSize

$CritList = $AllCerts | Where-Object { $_.Severity -eq 'CRITICAL' }
$WarnList = $AllCerts | Where-Object { $_.Severity -eq 'WARNING' }

Write-Host "CRITICAL ($($CritList.Count))  |  WARNING ($($WarnList.Count))  |  Total scanned: $($AllCerts.Count)"

# Email report if there are any alerts and SMTP is configured
if (($CritList.Count -gt 0 -or $WarnList.Count -gt 0) -and $SmtpServer -and $AlertEmail) {
    $Subject = "Certificate Expiry Alert: $($CritList.Count) CRITICAL, $($WarnList.Count) WARNING"
    $Body = "Certificate Expiry Monitor Report`n"
    $Body += "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n`n"

    $Body += "CRITICAL (expiring within $CritDays days):`n"
    foreach ($c in $CritList) {
        $Body += "  $($c.Server) | $($c.Subject) | Expires: $($c.Expiry) ($($c.DaysLeft) days) | $($c.Service)`n"
    }

    $Body += "`nWARNING (expiring within $WarnDays days):`n"
    foreach ($c in $WarnList) {
        $Body += "  $($c.Server) | $($c.Subject) | Expires: $($c.Expiry) ($($c.DaysLeft) days) | $($c.Service)`n"
    }

    Send-MailMessage -To $AlertEmail -From $FromEmail -Subject $Subject `
        -Body $Body -SmtpServer $SmtpServer
    Write-Host "Alert email sent to $AlertEmail"
}
~~~

---

## Service Health Monitor (PowerShell)

Check that required services are running across a server fleet. Optionally attempt automatic restart for stopped services. Exits with a monitoring-compatible code.

~~~powershell
#!/usr/bin/env pwsh
# service-health-monitor.ps1
# Usage: ./service-health-monitor.ps1 [-AttemptRestart]
#
# Define $ServiceMap to match your environment.

param(
    [bool]$AttemptRestart = $false,
    [System.Management.Automation.PSCredential]$Credential
)

Set-StrictMode -Version Latest

# --- Define required services per server ---
# Format: 'ServerName' = @('ServiceName1', 'ServiceName2', ...)
$ServiceMap = [ordered]@{
    'webserver01'   = @('W3SVC', 'WAS', 'wuauserv')
    'appserver01'   = @('MyAppService', 'MSSQLServer', 'SQLServerAgent')
    'fileserver01'  = @('LanmanServer', 'LanmanWorkstation', 'W32Time')
    'dc01'          = @('ADWS', 'DNS', 'KDC', 'Netlogon', 'NTDS')
}

$LOGFILE = "service-monitor-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"
$ExitCode = 0

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $entry = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] [$Level] $Message"
    Add-Content -Path $LOGFILE -Value $entry
    switch ($Level) {
        "ERROR" { Write-Host $entry -ForegroundColor Red }
        "WARN"  { Write-Host $entry -ForegroundColor Yellow }
        default { Write-Host $entry }
    }
}

Write-Log "=== Service Health Monitor ==="
Write-Log "Attempt restart: $AttemptRestart"
Write-Host ""

$AllResults = [System.Collections.Generic.List[PSObject]]::new()

foreach ($Server in $ServiceMap.Keys) {
    $RequiredServices = $ServiceMap[$Server]

    foreach ($ServiceName in $RequiredServices) {
        $result = [PSCustomObject]@{
            Server      = $Server
            Service     = $ServiceName
            Status      = "UNKNOWN"
            StartType   = "UNKNOWN"
            Restarted   = $false
            Error       = $null
        }

        try {
            $params = @{
                ComputerName = $Server
                ScriptBlock  = {
                    param($svc)
                    $s = Get-Service -Name $svc -ErrorAction Stop
                    return [PSCustomObject]@{ Status = $s.Status.ToString(); StartType = $s.StartType.ToString() }
                }
                ArgumentList = $ServiceName
            }
            if ($Credential) { $params['Credential'] = $Credential }
            $svcInfo = Invoke-Command @params

            $result.Status    = $svcInfo.Status
            $result.StartType = $svcInfo.StartType

            if ($svcInfo.Status -ne 'Running' -and $svcInfo.StartType -eq 'Automatic') {
                Write-Log "STOPPED (Automatic): $Server/$ServiceName" -Level "WARN"
                $script:ExitCode = 1

                if ($AttemptRestart) {
                    Write-Log "Attempting restart of $ServiceName on $Server..." -Level "WARN"
                    try {
                        $restartParams = @{
                            ComputerName = $Server
                            ScriptBlock  = { param($svc) Restart-Service -Name $svc -Force }
                            ArgumentList = $ServiceName
                        }
                        if ($Credential) { $restartParams['Credential'] = $Credential }
                        Invoke-Command @restartParams
                        $result.Restarted = $true
                        Write-Log "Restart submitted for $ServiceName on $Server." -Level "WARN"
                    } catch {
                        Write-Log "Restart FAILED for $ServiceName on $Server: $($_.Exception.Message)" -Level "ERROR"
                        $result.Error = $_.Exception.Message
                    }
                }
            }
        } catch {
            $result.Status = "ERROR"
            $result.Error  = $_.Exception.Message
            Write-Log "ERROR checking $ServiceName on $Server: $($_.Exception.Message)" -Level "ERROR"
            $script:ExitCode = 2
        }

        $AllResults.Add($result)
    }
}

# Print summary table
Write-Host ""
Write-Host "=== Service Status Summary ===" -ForegroundColor Cyan
$AllResults | Format-Table Server, Service, Status, StartType, Restarted -AutoSize

$NotRunning = $AllResults | Where-Object { $_.Status -ne 'Running' }
if ($NotRunning.Count -gt 0) {
    Write-Host "Not Running:" -ForegroundColor Red
    $NotRunning | ForEach-Object {
        Write-Host "  $($_.Server)/$($_.Service): $($_.Status) (Restarted: $($_.Restarted))" -ForegroundColor Red
    }
} else {
    Write-Host "All services running." -ForegroundColor Green
}

Write-Log "Check complete. ExitCode=$ExitCode | Log: $LOGFILE"
exit $ExitCode
~~~
