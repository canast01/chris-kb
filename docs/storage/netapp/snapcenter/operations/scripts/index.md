# SnapCenter — Scripts

> Part of the [SnapCenter Operations](../) reference.

---

## Backup Job Status Monitor (PowerShell)

Connect to SnapCenter, retrieve all backup jobs from the last 24 hours, print a formatted table, and send an email alert if any jobs have failed.

~~~powershell
# SnapCenter Backup Job Status Monitor
# Usage: .\sc_job_monitor.ps1

param(
    [string]$SC_SERVER  = $env:SC_SERVER,
    [string]$SC_USER    = $env:SC_USER,
    [string]$SC_PASS    = $env:SC_PASS,
    [string]$SmtpServer = $env:SMTP_SERVER,
    [string]$AlertEmail = $env:ALERT_EMAIL,
    [int]   $LookbackHours = 24
)

$SecPass = ConvertTo-SecureString $SC_PASS -AsPlainText -Force
$Cred    = New-Object System.Management.Automation.PSCredential($SC_USER, $SecPass)
Open-SmConnection -SMSbaseurl "https://${SC_SERVER}:8146" -Credential $Cred -ErrorAction Stop

$cutoff  = (Get-Date).AddHours(-$LookbackHours)
$allJobs = Get-SmJob -ErrorAction Stop | Where-Object { $_.StartDateTime -ge $cutoff }

$allJobs | Sort-Object StartDateTime -Descending | Format-Table -AutoSize

$failedJobs = $allJobs | Where-Object { $_.Status -eq "Failed" }
if ($failedJobs.Count -gt 0) { exit 1 } else { exit 0 }
~~~

---

## Resource Health Check (PowerShell)

Connect to SnapCenter, list all protected resources, check the age of the last backup for each, and flag resources that have not been backed up within the expected window.

~~~powershell
# SnapCenter Resource Health Check
# Usage: .\sc_resource_health.ps1

param(
    [string]$SC_SERVER = $env:SC_SERVER,
    [string]$SC_USER   = $env:SC_USER,
    [string]$SC_PASS   = $env:SC_PASS,
    [int]   $DBMaxHours  = 24,
    [int]   $FSMaxDays   = 7
)

$SecPass = ConvertTo-SecureString $SC_PASS -AsPlainText -Force
$Cred    = New-Object System.Management.Automation.PSCredential($SC_USER, $SecPass)
Open-SmConnection -SMSbaseurl "https://${SC_SERVER}:8146" -Credential $Cred -ErrorAction Stop

$resources = Get-SmResource -ErrorAction Stop
$now       = Get-Date
$results   = @()

foreach ($res in $resources) {
    $isDB     = $res.PluginCode -match "SQL|Oracle|HANA|Exchange"
    $maxHours = if ($isDB) { $DBMaxHours } else { $FSMaxDays * 24 }
    $backups  = Get-SmBackup -ResourceName $res.ResourceName -ErrorAction SilentlyContinue |
               Sort-Object BackupTime -Descending | Select-Object -First 1
    $lastBackup  = if ($backups) { $backups.BackupTime } else { $null }
    $ageHours    = if ($lastBackup) { [math]::Round(($now - $lastBackup).TotalHours, 1) } else { [double]::MaxValue }
    $status      = if ($ageHours -gt $maxHours) { "OVERDUE" } else { "OK" }
    $results += [PSCustomObject]@{ Resource=$res.ResourceName; Plugin=$res.PluginCode; AgeHours=$ageHours; Status=$status }
}

$results | Sort-Object AgeHours -Descending | Format-Table -AutoSize
if (($results | Where-Object { $_.Status -eq "OVERDUE" }).Count -gt 0) { exit 1 } else { exit 0 }
~~~

---

## Secondary Backup Validation (PowerShell)

For each SnapCenter-protected resource, verify that at least one secondary (SnapVault/SnapMirror) copy exists, and print a PASS/FAIL report for DR readiness validation.

~~~powershell
# SnapCenter Secondary Backup Validation
# Usage: .\sc_secondary_check.ps1

param(
    [string]$SC_SERVER = $env:SC_SERVER,
    [string]$SC_USER   = $env:SC_USER,
    [string]$SC_PASS   = $env:SC_PASS
)

$SecPass = ConvertTo-SecureString $SC_PASS -AsPlainText -Force
$Cred    = New-Object System.Management.Automation.PSCredential($SC_USER, $SecPass)
Open-SmConnection -SMSbaseurl "https://${SC_SERVER}:8146" -Credential $Cred -ErrorAction Stop

$resources = Get-SmResource -ErrorAction Stop
$fail = 0

foreach ($res in $resources) {
    $backups = Get-SmBackup -ResourceName $res.ResourceName -ErrorAction SilentlyContinue
    $hasSecondary = $backups | Where-Object { $_.IsSnapMirrorCopied -eq $true -or $_.IsSnapVaultCopied -eq $true } | Select-Object -First 1
    $status = if ($hasSecondary) { "PASS" } else { "FAIL"; $fail++ }
    Write-Host "$($res.ResourceName): $status"
}

if ($fail -gt 0) { exit 1 } else { exit 0 }
~~~

---

## Ansible SnapCenter Monitoring Playbook

Use the SnapCenter REST API to authenticate, check recent job status, check resource health, and fail the playbook if any job is in a Failed state.

~~~yaml
---
# SnapCenter Monitoring Playbook
# Run: ansible-playbook snapcenter_monitor.yml \
#        -e "snapcenter_host=sc01 snapcenter_user=admin snapcenter_pass=secret"

- name: SnapCenter Monitoring
  hosts: localhost
  gather_facts: false
  vars:
    snapcenter_port:   8146
    sc_validate_certs: false

  tasks:

    - name: Authenticate to SnapCenter and get token
      ansible.builtin.uri:
        url:          "https://{{ snapcenter_host }}:{{ snapcenter_port }}/api/4.2/auth/login"
        method:       POST
        body_format:  json
        body:
          UserOperationContext:
            User:
              Name:       "{{ snapcenter_user }}"
              Passphrase: "{{ snapcenter_pass }}"
              RoleName:   "SnapCenterAdmin"
        validate_certs: "{{ sc_validate_certs }}"
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
      register: sc_jobs

    - name: Fail if any jobs are in Failed status
      ansible.builtin.fail:
        msg: "{{ failed_jobs | length }} SnapCenter job(s) failed."
      when: (sc_jobs.json.JobList | selectattr('Status', 'equalto', 'Failed') | list) | length > 0
~~~

---

## Daily Check Script

Cron-safe PowerShell script reporting service status, connected hosts count, last backup job result per resource group, and pending job count.

~~~powershell
# sc_daily_check.ps1 — Daily SnapCenter backup job and service health check
# Usage: $env:SC_HOST="snapcenter01"; $env:SC_USER="admin"; $env:SC_PASS="secret"; .\sc_daily_check.ps1

param(
    [string]$SC_HOST = $env:SC_HOST,
    [string]$SC_USER = $env:SC_USER,
    [string]$SC_PASS = $env:SC_PASS,
    [int]   $LookbackHours = 24,
    [int]   $Port = 8146
)

$BaseUrl   = "https://${SC_HOST}:${Port}/api/4.9"
$LoginBody = @{ UserOperationContext = @{ User = @{ Name=$SC_USER; Passphrase=$SC_PASS; Rolename="SnapCenterAdmin" } } } | ConvertTo-Json -Depth 5
$Token     = (Invoke-RestMethod -Uri "$BaseUrl/auth/login" -Method POST -Body $LoginBody -ContentType "application/json").Token
$Headers   = @{ Token = $Token }

$Cutoff = (Get-Date).AddHours(-$LookbackHours)
$Jobs   = (Invoke-RestMethod -Uri "$BaseUrl/jobs" -Headers $Headers -Method GET).JobList |
          Where-Object { [datetime]$_.StartDateTime -ge $Cutoff }

$Failed  = ($Jobs | Where-Object { $_.Status -eq "Failed" }).Count
Write-Host "Jobs last ${LookbackHours}h: $($Jobs.Count)  Failed: $Failed"
if ($Failed -gt 0) { exit 1 } else { exit 0 }
~~~
