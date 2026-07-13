---
tags:
  - security
description: "This policy defines mandatory retention periods, storage tier assignments, and deletion procedures for all data types across the enterprise. Retention..."
---
# Data Retention Policy

<div class="kb-summary">
This policy defines mandatory retention periods, storage tier assignments, and deletion procedures for all data types across the enterprise. Retention decisions are driven by business need, legal obligation, and regulatory requirement — not storage cost alone.
</div>

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Data Lifecycle Overview

```d2
direction: right

A: "Data Created" {shape: rectangle}
B: "Active Use\nHot Storage" {shape: rectangle}
F: "Legal Hold\nStorage — no deletion" {shape: rectangle}
G: "G" {shape: rectangle}
J: "Cold / Archive Storage\nTape / Object Storage" {shape: rectangle}
D: "Warm Storage\nNear-line / slower tier" {shape: rectangle}
H: "Deletion Approved?" {shape: rectangle}
I: "Secure Deletion\nNIST 800-88" {shape: rectangle}

A -> B
F -> G
J -> G
```

---

## Log Retention Implementation

### SIEM — Splunk Index Retention

```ini
# /opt/splunk/etc/system/local/indexes.conf

[security_logs]
homePath   = $SPLUNK_DB/security_logs/db
coldPath   = $SPLUNK_DB/security_logs/colddb
thawedPath = $SPLUNK_DB/security_logs/thaweddb
frozenTimePeriodInSecs = 63072000   # 2 years = 730 days online
coldToFrozenDir = /mnt/archive/splunk/security_logs  # cold storage path
maxDataSize = auto_high_volume

[audit_logs]
homePath   = $SPLUNK_DB/audit_logs/db
coldPath   = $SPLUNK_DB/audit_logs/colddb
thawedPath = $SPLUNK_DB/audit_logs/thaweddb
frozenTimePeriodInSecs = 157680000  # 5 years archive
coldToFrozenDir = /mnt/archive/splunk/audit_logs
```

### Windows Event Log Forwarding and Retention

```powershell
# Set Windows Event Log max size and retention policy on source systems via GPO
# GPO Path: Computer Configuration > Policies > Windows Settings > Security Settings > Event Log

# Or via PowerShell on individual hosts:
Limit-EventLog -LogName Security -MaximumSize 1GB -OverflowAction OverwriteOlder
Limit-EventLog -LogName System   -MaximumSize 512MB -OverflowAction OverwriteOlder
Limit-EventLog -LogName Application -MaximumSize 512MB -OverflowAction OverwriteOlder

# Enable Windows Event Forwarding subscription (run on collector)
wecutil cs "C:\WEF\SecurityEventsSubscription.xml"
wecutil rs SecurityEvents
```

Windows Event Logs forwarded to SIEM are retained per SIEM policy (1 year online, archive thereafter). Local logs are a buffer only — do not rely on local retention for compliance.

### Linux Syslog Retention (rsyslog + logrotate)

```bash
# /etc/logrotate.d/syslog
/var/log/syslog {
    daily
    rotate 365
    compress
    delaycompress
    missingok
    notifempty
    postrotate
        /usr/lib/rsyslog/rsyslog-rotate
    endscript
}
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`/etc/logrotate.d/syslog: line 2: syntax error near unexpected token '{'`** — Ensure the logrotate configuration file uses proper syntax; this error typically occurs if the file is edited with incorrect line endings or missing newlines—use `dos2unix /etc/logrotate.d/syslog` to fix.
    **`error: stat of /var/log/syslog failed: No such file or directory`** — Create the syslog file before applying logrotate rules with `touch /var/log/syslog && chown syslog:adm /var/log/syslog && chmod 640 /var/log/syslog`.
    **`error: error executing postrotate script for /var/log/syslog`** — Verify that `/usr/lib/rsyslog/rsyslog-rotate` exists and is executable with `ls -la /usr/lib/rsyslog/rsyslog-rotate && chmod +x /usr/lib/rsyslog/rsyslog-rotate`.
Remote forwarding to SIEM is required; local rotation is a buffer for connectivity loss.

---

## Legal Hold Process

Legal hold suspends normal retention and deletion for data relevant to litigation, investigation, or regulatory inquiry.

### Legal Hold Procedure

1. **Initiation** — Legal or Compliance team issues a Legal Hold Notice identifying custodians, date range, and data types in scope.
2. **CMDB tag applied** — All affected data assets tagged `legal-hold: true` in the CMDB.
3. **Technical hold applied**:
   - Microsoft Purview: eDiscovery hold placed on mailboxes and SharePoint sites.
   - Veeam: retention lock enabled on relevant restore points via Immutable Backup Repository flag.
   - Commvault: hold flag applied to affected subclients — deletion jobs blocked.
4. **DBA / Sysadmin confirmation** — Custodians confirm hold applied and sign acknowledgement.
5. **Hold register updated** — Entry created in GRC system: matter reference, custodians, data scope, hold date.
6. **Hold release** — Legal team issues release notice. Holds released within 5 business days. Normal retention resumes; data that has passed its retention date is queued for deletion.

```powershell
# Microsoft Purview — place eDiscovery hold on mailbox and SharePoint
Connect-IPPSSession -UserPrincipalName admin@corp.onmicrosoft.com

New-CaseHoldPolicy -Name "Hold-LitigationMatter-2026-001" `
    -Case "Litigation-2026-001" `
    -ExchangeLocation "john.doe@corp.com" `
    -SharePointLocation "https://corp.sharepoint.com/sites/Finance"

New-CaseHoldRule -Name "Hold-Rule-2026-001" `
    -Policy "Hold-LitigationMatter-2026-001" `
    -ContentMatchQuery "subject:ProjectAlpha AND date>=2025-01-01"
```

---

## Secure Data Deletion Procedure

Deletion must follow NIST SP 800-88 Rev. 1 guidelines.

| Media Type | Method | Standard | Notes |
|---|---|---|---|
| Magnetic HDD (spinning) | Overwrite (1-pass) then degauss | NIST 800-88 Clear + Purge | Use DBAN or blancco for overwrite |
| SSD / NVMe (ATA Secure Erase) | ATA Secure Erase command | NIST 800-88 Purge | `hdparm --security-erase` or vendor tool |
| SAN LUN (PowerMax / Pure) | Crypto-erase (if self-encrypting drive) or LUN zero-out | NIST 800-88 Purge | Use array vendor tool (PowerMax CLI, purity erase) |
| Tape (LTO) | Degauss + physical destruction | NIST 800-88 Destroy | Third-party destruction with certificate |
| Cloud object storage (S3, Azure Blob) | API delete + bucket crypto-key deletion (if BYOK) | CSP policy + key destruction | Confirm with CSP data destruction certificate |
| Paper / printed records | Cross-cut shredding (DIN 66399 P-4 minimum) | GDPR Art. 5 | Witnessed shredding for Restricted data |

### PowerMax — Crypto-Erase a Volume

```bash
# Identify volume
symdev -sid 001 list -v | grep <volume-name>

# Mark volume for crypto-erase (requires array admin role)
symdev -sid 001 -dev <DeviceID> set secure_erase

# Confirm erase completion
symdev -sid 001 -dev <DeviceID> show | grep -i erase
```


```text title="Expected output"
# Identify volume
DeviceID VolumeID Size(MB) Pool Emulation Status
0A1B     prod-db-vol-03 2048000 POOL_SSD VMAX enabled
0A1C     prod-db-vol-04 2048000 POOL_SSD VMAX enabled

# Mark volume for crypto-erase (requires array admin role)
(no output — command completes silently)

# Confirm erase completion
Secure_Erase_Status: IN_PROGRESS
Secure_Erase_Percent_Complete: 87
Secure_Erase_Estimated_Time_Remaining: 45 minutes
```

!!! warning "Common errors"
    **`symdev: Error: Device 0A1B not found in array 001`** — Verify the DeviceID exists on the specified array SID using `symdev -sid 001 list`.
    **`symdev: Error: Insufficient privileges for secure_erase operation`** — Ensure your user account has array admin role; contact your storage administrator to grant permissions.
---

## Retention Compliance Monitoring

```powershell
# Weekly check: Veeam jobs with restore points older than policy allows
$jobs = Get-VBRJob -Type Backup
foreach ($job in $jobs) {
    $oldPoints = Get-VBRRestorePoint -Job $job | Where-Object {
        $_.CreationTime -lt (Get-Date).AddDays(-365)
    }
    if ($oldPoints) {
        Write-Warning "Job '$($job.Name)' has $($oldPoints.Count) restore points older than 1 year — review retention policy"
    }
}
```

```bash
# Check for files on archive NFS share older than retention limit
# Example: flag files in audit archive older than 6 years
find /mnt/archive/audit_logs -type f -mtime +2190 -exec ls -lh {} \; > /tmp/expired_audit_files.txt
wc -l /tmp/expired_audit_files.txt
```


```text title="Expected output"
-rw-r--r-- 1 root root 2.3M Jan 15 2018 /mnt/archive/audit_logs/2018/01/audit_20180115.log.gz
-rw-r--r-- 1 root root 1.8M Jan 22 2018 /mnt/archive/audit_logs/2018/01/audit_20180122.log.gz
-rw-r--r-- 1 root root 2.1M Feb 03 2018 /mnt/archive/audit_logs/2018/02/audit_20180203.log.gz
-rw-r--r-- 1 root root 1.9M Feb 14 2018 /mnt/archive/audit_logs/2018/02/audit_20180214.log.gz
-rw-r--r-- 1 root root 2.4M Mar 01 2018 /mnt/archive/audit_logs/2018/03/audit_20180301.log.gz
-rw-r--r-- 1 root root 2.0M Mar 18 2018 /mnt/archive/audit_logs/2018/03/audit_20180318.log.gz
...
847 /tmp/expired_audit_files.txt
```

!!! warning "Common errors"
    **`find: '/mnt/archive/audit_logs': No such file or directory`** — Verify the NFS share is mounted with `mount | grep archive` and mount it if necessary using `mount -t nfs server:/export/audit_logs /mnt/archive/audit_logs`.
    **`Permission denied`** — Run the command with `sudo` or ensure your user has read permissions on the archive directory with `sudo chmod g+rx /mnt/archive/audit_logs`.
    **`find: paths must begin with "." or "/"`** — Check for typos in the path and ensure `/mnt/archive/audit_logs` is an absolute path starting with `/`.
---

## Exceptions and Escalation

Retention exceptions require formal approval before they are implemented.

| Scenario | Approver | Documentation Required |
|---|---|---|
| Extended retention beyond policy (business request) | Data Owner + CISO | Written business justification, risk acknowledgement |
| Early deletion before retention period (e.g., data minimisation exercise) | Legal + Data Owner | Legal sign-off confirming no litigation risk, no hold in place |
| Legal hold extension | Legal team | Updated hold notice with revised release date |
| Deletion of data subject to active legal hold | Not permitted | Must escalate to Legal — do not proceed |

All exceptions are logged in the GRC system with approver name, date, and justification. Exceptions are reviewed at the quarterly governance meeting.
