# Scripts

> Part of the [NetApp SnapCenter](../) reference.

---

## Backup Job Status Monitor (PowerShell)

Connect to SnapCenter, retrieve all backup jobs from the last 24 hours, print a formatted table, and send an email alert if any jobs have failed.

~~~powershell
# SnapCenter Backup Job Status Monitor
# Requirements: SnapCenter PowerShell toolkit (installed with SnapCenter server)
# Usage: .\sc_job_monitor.ps1

param(
    [string]$SC_SERVER  = $env:SC_SERVER,
    [string]$SC_USER    = $env:SC_USER,
    [string]$SC_PASS    = $env:SC_PASS,
    [string]$SmtpServer = $env:SMTP_SERVER,
    [string]$AlertEmail = $env:ALERT_EMAIL,
    [string]$FromEmail  = "snapcenter-alerts@company.com",
    [int]   $LookbackHours = 24
)

if (-not $SC_SERVER -or -not $SC_USER -or -not $SC_PASS) {
    Write-Error "Set SC_SERVER, SC_USER, SC_PASS environment variables."
    exit 3
}

# --------------------------------------------------------------------------
# Connect to SnapCenter
# --------------------------------------------------------------------------
try {
    $SecPass = ConvertTo-SecureString $SC_PASS -AsPlainText -Force
    $Cred    = New-Object System.Management.Automation.PSCredential($SC_USER, $SecPass)
    Open-SmConnection -SMSbaseurl "https://${SC_SERVER}:8146" -Credential $Cred -ErrorAction Stop
    Write-Host "Connected to SnapCenter: $SC_SERVER"
} catch {
    Write-Error "Failed to connect to SnapCenter: $_"
    exit 2
}

# --------------------------------------------------------------------------
# Retrieve jobs from the last N hours
# --------------------------------------------------------------------------
$cutoff  = (Get-Date).AddHours(-$LookbackHours)
$allJobs = Get-SmJob -ErrorAction Stop | Where-Object {
    $_.StartDateTime -ge $cutoff
}

if (-not $allJobs) {
    Write-Host "No jobs found in the last $LookbackHours hours."
    exit 0
}

# --------------------------------------------------------------------------
# Print table
# --------------------------------------------------------------------------
$cols = @(
    @{Label="JobID";     Expression={$_.JobId}},
    @{Label="Type";      Expression={$_.JobType}},
    @{Label="Resource";  Expression={$_.ResourceName}},
    @{Label="Started";   Expression={$_.StartDateTime.ToString("yyyy-MM-dd HH:mm")}},
    @{Label="Ended";     Expression={if ($_.EndDateTime) { $_.EndDateTime.ToString("yyyy-MM-dd HH:mm") } else { "Running" }}},
    @{Label="Status";    Expression={$_.Status}}
)

Write-Host "`n=== SnapCenter Job Report (last ${LookbackHours}h) ==="
$allJobs | Sort-Object StartDateTime -Descending | Format-Table $cols -AutoSize

# --------------------------------------------------------------------------
# Identify failed jobs
# --------------------------------------------------------------------------
$failedJobs = $allJobs | Where-Object { $_.Status -eq "Failed" }
$runningJobs = $allJobs | Where-Object { $_.Status -eq "Running" }

Write-Host "Total jobs : $($allJobs.Count)"
Write-Host "Failed     : $($failedJobs.Count)"
Write-Host "Running    : $($runningJobs.Count)"

# --------------------------------------------------------------------------
# Email alert for failures
# --------------------------------------------------------------------------
if ($failedJobs.Count -gt 0 -and $SmtpServer -and $AlertEmail) {
    $body = "SnapCenter Job Failures — $SC_SERVER`n"
    $body += "Report time: $(Get-Date)`n`n"
    $body += ($failedJobs | Format-Table $cols -AutoSize | Out-String)

    try {
        Send-MailMessage `
            -To         $AlertEmail `
            -From       $FromEmail `
            -Subject    "ALERT: $($failedJobs.Count) SnapCenter job(s) failed on $SC_SERVER" `
            -Body       $body `
            -SmtpServer $SmtpServer `
            -ErrorAction Stop
        Write-Host "Alert email sent to $AlertEmail"
    } catch {
        Write-Warning "Failed to send alert email: $_"
    }
} elseif ($failedJobs.Count -gt 0) {
    Write-Warning "Failed jobs found but SMTP_SERVER / ALERT_EMAIL not configured — no email sent."
}

# Exit with non-zero if failures exist
if ($failedJobs.Count -gt 0) { exit 1 } else { exit 0 }
~~~

#### How to run this script — step by step

**Before you start — what you need**
- The SnapCenter PowerShell plug-in toolkit installed. This is included when you install the SnapCenter server, but you can also install it on a Windows workstation by downloading the SnapCenter plug-in package from your SnapCenter server's web UI at `https://your-snapcenter-server:8146`
- PowerShell 5.1 or later (already on Windows 10/11)
- Network access to your SnapCenter server on port 8146
- A SnapCenter admin username and password

**Step 1 — Save the file**

1. Open **Notepad** (press the Windows key, type `Notepad`, press Enter)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `sc_job_monitor.ps1` — save it to your Desktop

**Step 2 — Fill in your details**

Open PowerShell and set these environment variables before running (or you can edit the `param(...)` defaults in the script directly):

| Variable | What to put here | Where to find it |
|---|---|---|
| `$SC_SERVER` | SnapCenter server hostname or IP | Your IT team |
| `$SC_USER` | SnapCenter admin username | Your IT team |
| `$SC_PASS` | SnapCenter admin password | Your IT team |
| `$SmtpServer` | Your SMTP server address (optional) | Your IT team |
| `$AlertEmail` | Email address to receive failure alerts (optional) | Your preference |

**Step 3 — Open PowerShell as Administrator**

Press the Windows key, type `PowerShell`, right-click **Windows PowerShell**, choose **Run as Administrator**.

**Step 4 — Allow script execution (one-time per session)**

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run the script**

```
$env:SC_SERVER = "snapcenter01"
$env:SC_USER   = "admin"
$env:SC_PASS   = "yourpassword"
cd C:\Users\YourName\Desktop
.\sc_job_monitor.ps1
```

**What you should see**

A table of all SnapCenter backup jobs from the last 24 hours, showing job ID, type, resource name, start time, end time, and status. Below the table it prints total/failed/running counts. If any jobs failed and you have SMTP configured, an alert email is sent automatically.

---

## Resource Health Check (PowerShell)

Connect to SnapCenter, list all protected resources, check the age of the last backup for each, and flag resources that have not been backed up within the expected window.

~~~powershell
# SnapCenter Resource Health Check
# Flags: databases with no backup in > 24h, filesystems with no backup in > 7 days
# Usage: .\sc_resource_health.ps1

param(
    [string]$SC_SERVER = $env:SC_SERVER,
    [string]$SC_USER   = $env:SC_USER,
    [string]$SC_PASS   = $env:SC_PASS,
    [int]   $DBMaxHours  = 24,
    [int]   $FSMaxDays   = 7
)

if (-not $SC_SERVER -or -not $SC_USER -or -not $SC_PASS) {
    Write-Error "Set SC_SERVER, SC_USER, SC_PASS environment variables."
    exit 3
}

# --------------------------------------------------------------------------
# Connect
# --------------------------------------------------------------------------
$SecPass = ConvertTo-SecureString $SC_PASS -AsPlainText -Force
$Cred    = New-Object System.Management.Automation.PSCredential($SC_USER, $SecPass)
Open-SmConnection -SMSbaseurl "https://${SC_SERVER}:8146" -Credential $Cred -ErrorAction Stop

# --------------------------------------------------------------------------
# Get all resources
# --------------------------------------------------------------------------
$resources = Get-SmResource -ErrorAction Stop
$now       = Get-Date
$results   = @()

foreach ($res in $resources) {
    # Determine max backup age based on plugin type
    $isDB     = $res.PluginCode -match "SQL|Oracle|HANA|Exchange"
    $maxHours = if ($isDB) { $DBMaxHours } else { $FSMaxDays * 24 }

    # Get most recent backup for this resource
    $backups = Get-SmBackup -ResourceName $res.ResourceName -ErrorAction SilentlyContinue |
               Sort-Object BackupTime -Descending | Select-Object -First 1

    $lastBackup  = if ($backups) { $backups.BackupTime }  else { $null }
    $ageHours    = if ($lastBackup) { [math]::Round(($now - $lastBackup).TotalHours, 1) } else { [double]::MaxValue }
    $status      = if ($ageHours -gt $maxHours) { "OVERDUE" } else { "OK" }
    $lastBackupStr = if ($lastBackup) { $lastBackup.ToString("yyyy-MM-dd HH:mm") } else { "NEVER" }

    $results += [PSCustomObject]@{
        Resource   = $res.ResourceName
        Plugin     = $res.PluginCode
        LastBackup = $lastBackupStr
        AgeHours   = $ageHours
        MaxHours   = $maxHours
        Status     = $status
    }
}

# --------------------------------------------------------------------------
# Print sorted by age (oldest first)
# --------------------------------------------------------------------------
$sorted = $results | Sort-Object AgeHours -Descending
Write-Host "`n=== SnapCenter Resource Health Report ==="
Write-Host "Server : $SC_SERVER  |  Time : $now"
Write-Host ""
$sorted | Format-Table Resource, Plugin, LastBackup, AgeHours, MaxHours, Status -AutoSize

$overdue = $sorted | Where-Object { $_.Status -eq "OVERDUE" }
Write-Host "Total resources : $($results.Count)"
Write-Host "Overdue         : $($overdue.Count)"

if ($overdue.Count -gt 0) {
    Write-Warning "Resources with overdue backups:"
    $overdue | ForEach-Object { Write-Warning "  - $($_.Resource)  (${$_.AgeHours}h since last backup)" }
    exit 1
} else {
    Write-Host "All resources are within backup SLA."
    exit 0
}
~~~

#### How to run this script — step by step

**Before you start — what you need**
- The SnapCenter PowerShell plug-in toolkit installed (same requirement as the previous script)
- PowerShell 5.1 or later (already on Windows 10/11)
- A SnapCenter admin username and password

**Step 1 — Save the file**

1. Open **Notepad** (press the Windows key, type `Notepad`, press Enter)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `sc_resource_health.ps1` — save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put here | Where to find it |
|---|---|---|
| `$SC_SERVER` | SnapCenter server hostname or IP | Your IT team |
| `$SC_USER` | SnapCenter admin username | Your IT team |
| `$SC_PASS` | SnapCenter admin password | Your IT team |
| `$DBMaxHours` | Hours before a database backup is "overdue" (default: 24) | Your backup policy |
| `$FSMaxDays` | Days before a filesystem backup is "overdue" (default: 7) | Your backup policy |

**Step 3 — Open PowerShell as Administrator**

Press the Windows key, type `PowerShell`, right-click **Windows PowerShell**, choose **Run as Administrator**.

**Step 4 — Allow script execution (one-time per session)**

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run the script**

```
$env:SC_SERVER = "snapcenter01"
$env:SC_USER   = "admin"
$env:SC_PASS   = "yourpassword"
cd C:\Users\YourName\Desktop
.\sc_resource_health.ps1
```

**What you should see**

A table listing all SnapCenter-protected resources, sorted from the longest time since last backup to the shortest. Each row shows the resource name, plugin type, last backup time, how many hours ago that was, the maximum allowed hours, and a status of OK or OVERDUE. Resources that have not been backed up within their window are flagged in the warnings at the end.

---

## Secondary Backup Validation (PowerShell)

For each SnapCenter-protected resource, verify that at least one secondary (SnapVault/SnapMirror) copy exists, and print a PASS/FAIL report for DR readiness validation.

~~~powershell
# SnapCenter Secondary Backup Validation
# Verifies at least one secondary copy exists per protected resource.
# Usage: .\sc_secondary_check.ps1

param(
    [string]$SC_SERVER = $env:SC_SERVER,
    [string]$SC_USER   = $env:SC_USER,
    [string]$SC_PASS   = $env:SC_PASS
)

if (-not $SC_SERVER -or -not $SC_USER -or -not $SC_PASS) {
    Write-Error "Set SC_SERVER, SC_USER, SC_PASS environment variables."
    exit 3
}

# --------------------------------------------------------------------------
# Connect
# --------------------------------------------------------------------------
$SecPass = ConvertTo-SecureString $SC_PASS -AsPlainText -Force
$Cred    = New-Object System.Management.Automation.PSCredential($SC_USER, $SecPass)
Open-SmConnection -SMSbaseurl "https://${SC_SERVER}:8146" -Credential $Cred -ErrorAction Stop

# --------------------------------------------------------------------------
# Evaluate secondary copies per resource
# --------------------------------------------------------------------------
$resources = Get-SmResource -ErrorAction Stop
$pass  = 0
$fail  = 0
$results = @()

foreach ($res in $resources) {
    $backups = Get-SmBackup -ResourceName $res.ResourceName -ErrorAction SilentlyContinue

    # Check for any backup that has a secondary copy
    $hasSecondary = $backups | Where-Object {
        $_.IsSnapMirrorCopied -eq $true -or $_.IsSnapVaultCopied -eq $true
    } | Select-Object -First 1

    if ($hasSecondary) {
        $status = "PASS"
        $secondary = $hasSecondary.BackupName
        $pass++
    } else {
        $status = "FAIL"
        $secondary = "NONE"
        $fail++
    }

    $mostRecent = $backups | Sort-Object BackupTime -Descending | Select-Object -First 1
    $results += [PSCustomObject]@{
        Resource        = $res.ResourceName
        Plugin          = $res.PluginCode
        LastBackup      = if ($mostRecent) { $mostRecent.BackupTime.ToString("yyyy-MM-dd HH:mm") } else { "NEVER" }
        SecondaryBackup = $secondary
        Status          = $status
    }
}

# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------
Write-Host "`n=== SnapCenter Secondary Backup Validation ==="
Write-Host "Server : $SC_SERVER  |  Time : $(Get-Date)"
Write-Host ""
$results | Sort-Object Status -Descending | Format-Table Resource, Plugin, LastBackup, SecondaryBackup, Status -AutoSize

Write-Host "PASS : $pass"
Write-Host "FAIL : $fail"

if ($fail -gt 0) {
    Write-Warning "$fail resource(s) have NO secondary backup copies — DR readiness at risk."
    exit 1
} else {
    Write-Host "All resources have at least one secondary backup copy."
    exit 0
}
~~~

#### How to run this script — step by step

**Before you start — what you need**
- The SnapCenter PowerShell plug-in toolkit installed
- PowerShell 5.1 or later (already on Windows 10/11)
- A SnapCenter admin account
- Your SnapCenter environment must have SnapMirror or SnapVault policies configured for secondary protection to show PASS results

**Step 1 — Save the file**

1. Open **Notepad** (press the Windows key, type `Notepad`, press Enter)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `sc_secondary_check.ps1` — save it to your Desktop

**Step 2 — Fill in your details**

| Variable | What to put here | Where to find it |
|---|---|---|
| `$SC_SERVER` | SnapCenter server hostname or IP | Your IT team |
| `$SC_USER` | SnapCenter admin username | Your IT team |
| `$SC_PASS` | SnapCenter admin password | Your IT team |

**Step 3 — Open PowerShell as Administrator**

Press the Windows key, type `PowerShell`, right-click **Windows PowerShell**, choose **Run as Administrator**.

**Step 4 — Allow script execution (one-time per session)**

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run the script**

```
$env:SC_SERVER = "snapcenter01"
$env:SC_USER   = "admin"
$env:SC_PASS   = "yourpassword"
cd C:\Users\YourName\Desktop
.\sc_secondary_check.ps1
```

**What you should see**

A table showing every protected resource with its last backup time, the name of the most recent secondary backup (if one exists), and a PASS or FAIL status. Resources with no secondary copies show "NONE" and FAIL. The script exits with code 1 if any resource fails, which makes it easy to integrate into monitoring tools.

---

## Ansible SnapCenter Monitoring Playbook

Use the SnapCenter REST API to authenticate, check recent job status, check resource health, and fail the playbook if any job is in a Failed state.

~~~yaml
---
# SnapCenter Monitoring Playbook
# Variables: snapcenter_host, snapcenter_user, snapcenter_pass
#
# Run: ansible-playbook snapcenter_monitor.yml \
#        -e "snapcenter_host=sc01 snapcenter_user=admin snapcenter_pass=secret"

- name: SnapCenter Monitoring
  hosts: localhost
  gather_facts: false
  vars:
    snapcenter_port:     8146
    sc_validate_certs:   false
    job_lookback_hours:  24

  tasks:

    - name: Authenticate to SnapCenter and get token
      ansible.builtin.uri:
        url:          "https://{{ snapcenter_host }}:{{ snapcenter_port }}/api/4.2/auth/login"
        method:       POST
        body_format:  json
        body:
          UserOperationContext:
            User:
              Name:     "{{ snapcenter_user }}"
              Passphrase: "{{ snapcenter_pass }}"
              RoleName: "SnapCenterAdmin"
        validate_certs: "{{ sc_validate_certs }}"
        return_content: true
        status_code: [200, 201]
      register: sc_auth

    - name: Extract auth token
      ansible.builtin.set_fact:
        sc_token: "{{ sc_auth.json.Token }}"

    - name: Get recent backup jobs
      ansible.builtin.uri:
        url: "https://{{ snapcenter_host }}:{{ snapcenter_port }}/api/4.2/jobs"
        method: GET
        headers:
          Token: "{{ sc_token }}"
        validate_certs: "{{ sc_validate_certs }}"
        return_content: true
      register: sc_jobs

    - name: Filter failed jobs
      ansible.builtin.set_fact:
        failed_jobs: >-
          {{ sc_jobs.json.JobList
             | selectattr('Status', 'equalto', 'Failed')
             | list }}

    - name: Print job summary
      ansible.builtin.debug:
        msg: >-
          Job {{ item.JobId }}: {{ item.JobType }}
          | Resource: {{ item.ResourceName | default('N/A') }}
          | Status: {{ item.Status }}
          | Started: {{ item.StartDateTime | default('N/A') }}
      loop: "{{ sc_jobs.json.JobList | default([]) }}"

    - name: Fail if any jobs are in Failed status
      ansible.builtin.fail:
        msg: >-
          {{ failed_jobs | length }} SnapCenter job(s) failed:
          {{ failed_jobs | map(attribute='JobId') | list | join(', ') }}
      when: failed_jobs | length > 0

    - name: Get resource list
      ansible.builtin.uri:
        url: "https://{{ snapcenter_host }}:{{ snapcenter_port }}/api/4.2/resources"
        method: GET
        headers:
          Token: "{{ sc_token }}"
        validate_certs: "{{ sc_validate_certs }}"
        return_content: true
      register: sc_resources

    - name: Print resource health summary
      ansible.builtin.debug:
        msg: >-
          Resource: {{ item.ResourceName }}
          | Type: {{ item.PluginCode | default('N/A') }}
          | Protected: {{ item.IsProtected | default('unknown') }}
      loop: "{{ sc_resources.json.ResourceList | default([]) }}"

    - name: SnapCenter monitoring checks passed
      ansible.builtin.debug:
        msg: "All SnapCenter jobs are healthy. Total resources: {{ sc_resources.json.ResourceList | length }}"
~~~

#### How to run this script — step by step

**Before you start — what you need**
- Ansible installed — on Windows, use WSL (Windows Subsystem for Linux). Open the Microsoft Store, install Ubuntu, then open it from the Start menu and run `sudo apt install ansible`
- Network access to your SnapCenter server on port 8146
- A SnapCenter admin account

**Step 1 — Save the file**

1. Open **Notepad** (press the Windows key, type `Notepad`, press Enter)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `snapcenter_monitor.yml` — save it to your Desktop

**Step 2 — Fill in your details**

You pass all values on the command line — no need to edit the file.

| Variable | What to put here | Where to find it |
|---|---|---|
| `snapcenter_host` | SnapCenter server hostname or IP | Your IT team |
| `snapcenter_user` | SnapCenter admin username | Your IT team |
| `snapcenter_pass` | SnapCenter admin password | Your IT team |

**Step 3 — Open a WSL terminal**

Open the Ubuntu app from the Start menu.

**Step 4 — Copy the file to WSL and run it**

```
cp /mnt/c/Users/YourName/Desktop/snapcenter_monitor.yml ~/
cd ~
ansible-playbook snapcenter_monitor.yml \
  -e "snapcenter_host=snapcenter01 snapcenter_user=admin snapcenter_pass=yourpassword"
```

**What you should see**

Ansible logs in to SnapCenter, retrieves all recent jobs, and prints a summary of each one showing job ID, type, resource name, and status. If any job has a Failed status, the playbook stops and prints the failed job IDs. If all jobs are healthy, it prints a count of all protected resources and succeeds.

---

## Windows: SnapCenter Job Status via REST API (PowerShell)

Log in to the SnapCenter REST API, retrieve recent backup jobs, and print a formatted report showing job name, status, start time, and duration. No SnapCenter PowerShell toolkit required — works on any Windows PC with PowerShell.

~~~powershell
# sc_jobs_rest.ps1 — SnapCenter Job Status via REST API (Windows PowerShell)
# Requires: PowerShell 5.1+ (pre-installed on Windows 10/11)
# Run: .\sc_jobs_rest.ps1

$ScHost = "192.168.1.50"    # Your SnapCenter server hostname or IP
$ScUser = "admin"            # SnapCenter username
$ScPass = "yourpassword"     # SnapCenter password
$ScPort = 8146               # Default SnapCenter API port

# Handle self-signed SSL certificates
if (-not ([System.Management.Automation.PSTypeName]'TrustAll').Type) {
    Add-Type @"
    using System.Net; using System.Security.Cryptography.X509Certificates;
    public class TrustAll : ICertificatePolicy {
        public bool CheckValidationResult(ServicePoint s, X509Certificate c, WebRequest r, int p) { return true; }
    }
"@
    [System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAll
}
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$BaseUrl = "https://${ScHost}:${ScPort}/api"

# --- Step 1: Authenticate and get token ---
Write-Host "Authenticating to SnapCenter at $ScHost ..." -ForegroundColor Cyan

$LoginBody = @{
    UserOperationContext = @{
        User = @{
            Name       = $ScUser
            Passphrase = $ScPass
            Rolename   = "SnapCenterAdmin"
        }
    }
} | ConvertTo-Json -Depth 5

try {
    $AuthResp = Invoke-RestMethod `
        -Uri    "$BaseUrl/4.9/auth/login" `
        -Method POST `
        -Body   $LoginBody `
        -ContentType "application/json" `
        -ErrorAction Stop
} catch {
    Write-Error "Authentication failed: $($_.Exception.Message)"
    exit 1
}

$Token = $AuthResp.Token
if (-not $Token) {
    Write-Error "No token returned. Check credentials."
    exit 1
}

$Headers = @{ Token = $Token }
Write-Host "Authenticated successfully." -ForegroundColor Green

# --- Step 2: Get recent backup jobs ---
Write-Host "`nFetching backup jobs ..." -ForegroundColor Cyan

try {
    $JobsResp = Invoke-RestMethod `
        -Uri     "$BaseUrl/4.9/jobs?JobType=Backup" `
        -Method  GET `
        -Headers $Headers `
        -ErrorAction Stop
} catch {
    Write-Error "Failed to retrieve jobs: $($_.Exception.Message)"
    exit 1
}

$Jobs = $JobsResp.JobList
if (-not $Jobs -or $Jobs.Count -eq 0) {
    Write-Host "No backup jobs found."
    exit 0
}

# --- Step 3: Print formatted report ---
Write-Host "`n=== SnapCenter Backup Job Report ===" -ForegroundColor Cyan
Write-Host "Server: $ScHost  |  Total jobs: $($Jobs.Count)"
Write-Host ("-" * 80)

foreach ($job in ($Jobs | Sort-Object StartDateTime -Descending)) {
    $startTime = $job.StartDateTime
    $endTime   = $job.EndDateTime

    # Calculate duration if both times are available
    if ($startTime -and $endTime) {
        $start    = [datetime]$startTime
        $end      = [datetime]$endTime
        $duration = ($end - $start).ToString("hh\:mm\:ss")
    } else {
        $duration = "N/A"
    }

    $statusColour = switch ($job.Status) {
        "Completed"  { "Green"  }
        "Failed"     { "Red"    }
        "Running"    { "Cyan"   }
        default      { "Yellow" }
    }

    Write-Host ("[{0}] {1,-35} Start: {2,-20} Duration: {3}" -f
        $job.Status.PadRight(10), $job.JobName, $startTime, $duration) -ForegroundColor $statusColour
}

Write-Host ("-" * 80)
$failed = $Jobs | Where-Object { $_.Status -eq "Failed" }
if ($failed.Count -gt 0) {
    Write-Host "$($failed.Count) job(s) FAILED — review SnapCenter for details." -ForegroundColor Red
    exit 1
} else {
    Write-Host "All jobs completed successfully." -ForegroundColor Green
    exit 0
}
~~~

#### How to run this script — step by step

**Before you start — what you need**
- A Windows 10 or Windows 11 PC (PowerShell is already installed — nothing extra to download)
- Network access to your SnapCenter server on port 8146
- A SnapCenter admin username and password

**Step 1 — Save the file**

1. Open **Notepad** (press the Windows key, type `Notepad`, press Enter)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `sc_jobs_rest.ps1` — save it to your Desktop

**Step 2 — Fill in your details**

Open the saved file in Notepad and change these lines near the top:

| Variable | What to put here | Where to find it |
|---|---|---|
| `$ScHost` | SnapCenter server IP or hostname | Your IT team |
| `$ScUser` | SnapCenter admin username | Your IT team |
| `$ScPass` | SnapCenter admin password | Your IT team |
| `$ScPort` | SnapCenter API port (default: 8146) | Your IT team (usually 8146) |

**Step 3 — Open PowerShell as Administrator**

Press the Windows key, type `PowerShell`, right-click **Windows PowerShell**, choose **Run as Administrator**.

**Step 4 — Allow script execution (one-time per session)**

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run the script**

```
cd C:\Users\YourName\Desktop
.\sc_jobs_rest.ps1
```

**What you should see**

The script authenticates to SnapCenter via REST API and prints a list of all backup jobs, one per line, colour-coded: green for completed, red for failed, cyan for running, yellow for anything else. Each line shows the job status, name, start time, and duration. At the end it prints a summary — if any jobs failed, the script exits with code 1.

---

## Windows: SnapCenter Backup Report via curl (CMD)

Use the built-in `curl.exe` on Windows 10/11 to call the SnapCenter REST API, retrieve recent backup jobs, and print a basic report. No installation needed — curl.exe ships with Windows 10 build 1803 and later.

~~~batch
@echo off
REM sc_backup_report.bat — SnapCenter Backup Report via curl.exe (Windows CMD)
REM Uses curl.exe (built into Windows 10/11 — no installation needed).
REM curl.exe is at C:\Windows\System32\curl.exe

set SC_HOST=192.168.1.50
set SC_USER=admin
set SC_PASS=yourpassword
set SC_PORT=8146

echo.
echo === SnapCenter Backup Report ===
echo Server: %SC_HOST%:%SC_PORT%
echo Time: %date% %time%
echo.

REM --- Step 1: Authenticate and capture token ---
echo Authenticating...
curl.exe -k -s -X POST ^
  "https://%SC_HOST%:%SC_PORT%/api/4.9/auth/login" ^
  -H "Content-Type: application/json" ^
  -d "{\"UserOperationContext\":{\"User\":{\"Name\":\"%SC_USER%\",\"Passphrase\":\"%SC_PASS%\",\"Rolename\":\"SnapCenterAdmin\"}}}" ^
  -o sc_auth_response.json

if %ERRORLEVEL% neq 0 (
    echo ERROR: Authentication request failed. Check hostname and network connectivity.
    goto :end
)

REM --- Extract token using PowerShell (built-in on Windows) ---
for /f "delims=" %%T in ('powershell -Command "(Get-Content sc_auth_response.json | ConvertFrom-Json).Token"') do set SC_TOKEN=%%T

if "%SC_TOKEN%"=="" (
    echo ERROR: No token returned. Check credentials.
    type sc_auth_response.json
    goto :end
)

echo Authenticated successfully. Token: %SC_TOKEN:~0,20%...
echo.

REM --- Step 2: Get recent backup jobs ---
echo Fetching backup jobs...
curl.exe -k -s -X GET ^
  "https://%SC_HOST%:%SC_PORT%/api/4.9/jobs?JobType=Backup" ^
  -H "Token: %SC_TOKEN%" ^
  -o sc_jobs_response.json

if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to retrieve jobs.
    goto :end
)

REM --- Step 3: Parse and display results using PowerShell ---
echo.
echo --- Backup Jobs ---
powershell -Command ^
  "$jobs = (Get-Content sc_jobs_response.json | ConvertFrom-Json).JobList; " ^
  "if (-not $jobs) { Write-Host 'No backup jobs found.'; exit 0 }; " ^
  "$jobs | Sort-Object StartDateTime -Descending | ForEach-Object { " ^
  "  $status = $_.Status; $colour = if ($status -eq 'Completed') { 'Green' } elseif ($status -eq 'Failed') { 'Red' } else { 'Yellow' }; " ^
  "  Write-Host ('[' + $status.PadRight(10) + '] ' + $_.JobName) -ForegroundColor $colour " ^
  "}; " ^
  "$failed = ($jobs | Where-Object { $_.Status -eq 'Failed' }).Count; " ^
  "Write-Host ('Failed jobs: ' + $failed) -ForegroundColor (if ($failed -gt 0) { 'Red' } else { 'Green' })"

REM --- Cleanup temporary files ---
del sc_auth_response.json 2>nul
del sc_jobs_response.json 2>nul

echo.
echo === Report complete ===

:end
~~~

#### How to run this script — step by step

**Before you start — what you need**
- Windows 10 build 1803 or later, or Windows 11 (curl.exe is built in — no installation needed)
- Network access to your SnapCenter server on port 8146
- A SnapCenter admin username and password

**Step 1 — Save the file**

1. Open **Notepad** (press the Windows key, type `Notepad`, press Enter)
2. Copy the entire code block above
3. Click **File → Save As**
4. Change "Save as type" to **All Files**
5. Name it `sc_backup_report.bat` — save it to your Desktop

**Step 2 — Fill in your details**

Open the saved file in Notepad and change these lines near the top:

| Variable | What to put here | Where to find it |
|---|---|---|
| `SC_HOST` | SnapCenter server IP or hostname | Your IT team |
| `SC_USER` | SnapCenter admin username | Your IT team |
| `SC_PASS` | SnapCenter admin password | Your IT team |
| `SC_PORT` | SnapCenter API port (default: 8146) | Your IT team |

**Step 3 — Open a terminal**

Press the Windows key, type `cmd`, press Enter to open Command Prompt.

**Step 4 — Run the script**

```
cd %USERPROFILE%\Desktop
sc_backup_report.bat
```

You can also just double-click the `.bat` file on your Desktop.

**What you should see**

The script authenticates to SnapCenter using curl.exe, saves the response to a temporary file, extracts the auth token, then fetches all backup jobs. It prints each job with a colour-coded status (green = Completed, red = Failed, yellow = anything else). Temporary JSON files are cleaned up automatically after the script finishes.
