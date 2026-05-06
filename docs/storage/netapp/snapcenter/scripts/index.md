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
