---
tags:
  - security
description: "Security Monitoring reference covering Daily Review Checklist, Key Windows Security Events, Linux Security Monitoring, Correlation Rules (SIEM Examples)..."
---
# Security Monitoring

<div class="kb-summary">
Security Monitoring reference covering Daily Review Checklist, Key Windows Security Events, Linux Security Monitoring, Correlation Rules (SIEM Examples), Threat Detection Sources and 1 more sections.
</div>

<div class="kb-grid">
  <a class="kb-card" href="operations/">
    <div class="kb-card-icon">⚙️</div>
    <div class="kb-card-title">Operations</div>
    <div class="kb-card-desc">Daily review checklist, SIEM correlation rules, alerting thresholds, threat detection</div>
  </a>
</div>

## Daily Review Checklist

| Check | Tool | Expected |
|---|---|---|
| SIEM alert queue | Splunk / Graylog / Sentinel | No unacknowledged High/Critical |
| Failed login spikes | SIEM / AD event log | No unusual spike pattern |
| Privileged account activity | CyberArk / AD event log 4648 | All activity matches known change windows |
| New admin accounts created | AD event log 4720 | Only approved accounts |
| Firewall deny logs | Firewall / SIEM | No unexpected internal→external attempts |
| EDR / AV alert queue | CrowdStrike / Defender | No active threats unacknowledged |

## Key Windows Security Events

| Event ID | Description | Why It Matters |
|---|---|---|
| 4624 | Successful logon | Baseline; flag off-hours or remote logons |
| 4625 | Failed logon | Brute force detection |
| 4648 | Explicit credential logon | Pass-the-hash / lateral movement |
| 4720 | User account created | Persistence mechanism |
| 4728 | Added to global security group | Privilege escalation |
| 4740 | Account locked out | Brute force or stale credential |
| 4776 | NTLM auth attempt | Downgrade attack detection |
| 7045 | New service installed | Malware persistence |
| 4698 | Scheduled task created | Persistence |
| 4663 | Object access | File/folder auditing (if enabled) |

```powershell
# Pull recent high-priority security events
Get-WinEvent -FilterHashtable @{
  LogName = 'Security'
  Id      = @(4720, 4728, 7045, 4698)
  StartTime = (Get-Date).AddHours(-24)
} | Select-Object TimeCreated, Id, Message | Format-List
```

## Linux Security Monitoring

```bash
# Failed SSH attempts in last hour
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn | head -10

# Successful root logins
grep "session opened for user root" /var/log/auth.log | tail -20

# New users created
grep "useradd\|adduser" /var/log/auth.log | tail -20

# Sudo usage
grep "sudo:" /var/log/auth.log | grep -v "pam_unix" | tail -30

# Check auditd rules
auditctl -l
```


```text title="Expected output"
5 192.168.1.45
      3 203.0.113.22
      2 10.0.2.18
      2 198.51.100.9
      1 172.16.0.55
      1 203.0.113.88
      1 192.168.50.12

Nov 15 14:32:18 prod-db01 sshd[8924]: session opened for user root by (uid=0)
Nov 15 13:47:02 prod-db01 sshd[7651]: session opened for user root by (uid=0)
Nov 15 12:15:44 prod-db01 sshd[6289]: session opened for user root by (uid=0)

Nov 15 09:22:15 prod-db01 useradd[4521]: new user: name=appuser, UID=1001, GID=1001, home=/home/appuser, shell=/bin/bash
Nov 15 08:45:33 prod-db01 useradd[4398]: new user: name=svcacct, UID=1002, GID=1002, home=/home/svcacct, shell=/bin/false

Nov 15 14:28:09 prod-db01 sudo: admin on pts/2 ; USER=root ; COMMAND=/usr/bin/systemctl restart nginx
Nov 15 14:15:44 prod-db01 sudo: deploy on pts/5 ; USER=root ; COMMAND=/bin/bash
Nov 15 13:52:17 prod-db01 sudo: admin on pts/2 ; USER=root ; COMMAND=/usr/bin/apt update

No rules
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `grep: /var/log/auth.log: No such file or directory` | Check the correct log path with `ls -la /var/log/` and adjust for your system (may be `/var/log/secure` on RHEL or in journalctl on systemd systems). |
    | `No rules` | Install and enable auditd with `sudo systemctl enable auditd && sudo systemctl start auditd`, then load rules from `/etc/audit/rules.d/`. |
## Correlation Rules (SIEM Examples)

**Brute force detection:**
```bash
# >10 failed logons from same source in 5 minutes
index=security EventCode=4625
| stats count by src_ip, user
| where count > 10
```


```text title="Expected output"
src_ip          user              count
192.168.1.45    administrator     14
10.0.2.89       jsmith            12
172.16.50.201   guest             11
203.0.113.78    root              15
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error in 'where' command: Unknown field 'count'` | Ensure the stats command completes successfully and verify field names match exactly in the where clause. |
    | `index=security: Unknown index 'security'` | Confirm the index name exists in your Splunk instance; use `| rest /services/data/indexes` to list available indexes. |
**Lateral movement — new admin account:**
```bash
# Account created then added to privileged group within 60 minutes
index=security (EventCode=4720 OR EventCode=4728)
| transaction user maxspan=60m
| where eventcount > 1
```


```text title="Expected output"
index=security (EventCode=4720 OR EventCode=4728)
| transaction user maxspan=60m
| where eventcount > 1

user=Administrator eventcount=2 duration=45m earliest=2024-01-15T09:23:14 latest=2024-01-15T10:08:47
user=svc_deploy eventcount=2 duration=18m earliest=2024-01-15T11:42:31 latest=2024-01-15T12:00:49
user=jsmith eventcount=2 duration=52m earliest=2024-01-15T14:15:22 latest=2024-01-15T15:07:14
user=automation_acct eventcount=2 duration=31m earliest=2024-01-15T16:33:05 latest=2024-01-15T17:04:18
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error in 'where' command: The expression is malformed. An unexpected character has occurred.` | Verify the Splunk version supports the `where` command syntax; use `stats count as eventcount` with `by user` instead if on older versions. |
    | `No results found` | Confirm the index name is correct and contains Windows Security event logs (EventCode 4720 and 4728); check index permissions with `| rest /services/data/indexes`. |
**Off-hours privileged access:**
```text
index=security EventCode=4648
| eval hour=strftime(_time,"%H")
| where hour < 6 OR hour > 20
| table _time, user, src_ip, dest
```

## Threat Detection Sources

| Source | What It Monitors |
|---|---|
| Windows Event Log | Logon events, privilege use, object access |
| Linux auditd | Syscall-level audit, file access, exec |
| Firewall deny logs | Blocked traffic, port scans |
| EDR / AV | Process-level threat detection, behavioural |
| DNS logs | C2 domain queries, DNS tunnelling |
| Netflow | Lateral movement, data exfiltration volume |
| AD audit log | Group changes, password resets, account creation |

## Alerting Thresholds

| Metric | Warning | Critical |
|---|---|---|
| Failed logins per host / 5 min | >5 | >20 |
| New admin account created | Any | — |
| External connection from server (unexpected) | Any | — |
| AV/EDR detection | Any | Active threat (not quarantined) |
| Privileged account used outside change window | Any | — |
