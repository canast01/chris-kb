---
tags:
  - networking
description: "Syslog and Centralized Logging reference covering Syslog Service Health, Configure rsyslog to Forward to Central Collector, journald to Syslog Bridge..."
---
# Syslog and Centralized Logging

<div class="kb-summary">
Syslog and Centralized Logging reference covering Syslog Service Health, Configure rsyslog to Forward to Central Collector, journald to Syslog Bridge, Windows Event Forwarding, Syslog Severity Levels (RFC 5424) and 2 more sections.
</div>

```bash
# Apply after editing
systemctl restart rsyslog

# Test
logger -t TEST "Forwarding test from $(hostname)"
```

```d2
direction: down

journald_to_syslog_bridge: "journald to Syslog Bridge" {shape: rectangle}
windows_event_forwarding: "Windows Event Forwarding" {shape: rectangle}
syslog_severity_levels_rfc_5424: "Syslog Severity Levels (RFC 5424)" {shape: rectangle}
querying_logs: "Querying Logs" {shape: rectangle}
troubleshooting_logs_not_arriving: "Troubleshooting — Logs Not Arriving" {shape: rectangle}

journald_to_syslog_bridge -> windows_event_forwarding: uses
windows_event_forwarding -> syslog_severity_levels_rfc_5424: uses
syslog_severity_levels_rfc_5424 -> querying_logs: uses
querying_logs -> troubleshooting_logs_not_arriving: uses
```

## journald to Syslog Bridge

```bash
# Forward journald to rsyslog (already default on most distros)
# /etc/systemd/journald.conf:
# ForwardToSyslog=yes

# Verify journal disk usage
journalctl --disk-usage

# Vacuum old entries
journalctl --vacuum-time=30d
journalctl --vacuum-size=2G
```


```text title="Expected output"
Archived and active journals take up 487.2M on disk.
Vacuuming done, freed 156.3M of previously allocated disk space.
Vacuuming done, freed 89.7M of previously allocated disk space.
```

!!! warning "Common errors"
    **`Failed to vacuum journal: Permission denied`** — Run the command with `sudo` since journal management requires root privileges.
    **`Vacuuming done, but no space was freed`** — The retention policy is already met; check current usage with `journalctl --disk-usage` and adjust `--vacuum-time` or `--vacuum-size` parameters to match your actual journal size.
## Windows Event Forwarding

```powershell
# Configure Windows Event Collector
winrm quickconfig

# Subscription on collector (WEF)
wecutil cs subscription.xml

# View forwarded events
Get-WinEvent -LogName ForwardedEvents -MaxEvents 20
```

## Syslog Severity Levels (RFC 5424)

| Level | Code | Meaning |
|---|---|---|
| Emergency | 0 | System unusable |
| Alert | 1 | Immediate action required |
| Critical | 2 | Critical condition |
| Error | 3 | Error condition |
| Warning | 4 | Warning condition |
| Notice | 5 | Normal but significant |
| Informational | 6 | Informational |
| Debug | 7 | Debug messages |

Filter to errors and above: `*.err` or severity ≤ 3.

## Querying Logs

**Linux — journalctl:**
```bash
# Filter by unit
journalctl -u nginx -n 100 --no-pager

# Filter by priority
journalctl -p err -b --no-pager

# Filter by time
journalctl --since "2026-05-01 08:00:00" --until "2026-05-01 10:00:00"

# Follow live
journalctl -f -u <service>
```


```text title="Expected output"
-- Logs begin at Wed 2026-05-01 06:15:22 UTC, end at Wed 2026-05-01 09:47:33 UTC. --
May 01 08:12:44 web-prod-01 nginx[2847]: 192.168.1.105 - - [01/May/2026:08:12:44 +0000] "GET /api/health HTTP/1.1" 200 145 "-" "curl/7.68.0"
May 01 08:13:12 web-prod-01 nginx[2847]: 192.168.1.106 - - [01/May/2026:08:13:12 +0000] "POST /api/users HTTP/1.1" 201 892 "-" "Mozilla/5.0"
May 01 08:14:55 web-prod-01 nginx[2847]: 2026-05-01T08:14:55+00:00 [error] 2847#2847: *1024 connect() failed (111: Connection refused)
May 01 08:15:33 web-prod-01 nginx[2847]: 192.168.1.107 - - [01/May/2026:08:15:33 +0000] "GET /static/app.js HTTP/1.1" 304 0 "-" "Mozilla/5.0"
May 01 08:16:02 web-prod-01 nginx[2847]: 2026-05-01T08:16:02+00:00 [error] 2847#2847: *1025 upstream timed out (110: Connection timed out)
May 01 08:17:18 web-prod-01 nginx[2847]: 192.168.1.108 - - [01/May/2026:08:17:18 +0000] "DELETE /api/sessions/abc123 HTTP/1.1" 204 0 "-" "curl/7.68.0"
...
lines 1-100

May 01 08:45:22 web-prod-01 kernel: [ERR] audit: type=1400 audit(1746086722.445:8901): apparmor="DENIED" operation="capable" profile="nginx" pid=2847 comm="nginx" capability=36 capname="block_suspend"
May 01 09:02:15 web-prod-01 systemd[1]: [ERR] Failed to start PostgreSQL Database Server.
May 01 09:15:44 web-prod-01 sudo[4521]: [ERR] user NOT in sudoers; TTY=pts/0; PWD=/home/admin; USER=root; COMMAND=/usr/bin/systemctl restart nginx

May 01 08:00:15 web-prod-01 nginx[2847]: 192.168.1.110 - - [01/May/2026:08:00:15 +0000] "GET / HTTP/1.1" 200 5234 "-" "Mozilla/5.0"
May 01 08:15:42 web-prod-01 nginx[2847]: 192.168.1.111 - - [01/May/2026:08:15:42 +0000]
```
**Graylog / Splunk search examples:**
```bash
# Graylog GELF query
source:<hostname> AND level:<4 AND facility:daemon

# Splunk SPL
index=infra host=<hostname> sourcetype=syslog level=error | timechart count by host
```


```text title="Expected output"
(no output — these are query syntax examples, not executable commands)
```
## Troubleshooting — Logs Not Arriving

| Symptom | Check | Action |
|---|---|---|
| No logs from host | rsyslog running? | `systemctl start rsyslog` |
| Logs stopped mid-stream | Disk full on collector? | `df -h /var/log` — rotate or expand |
| Time mismatch in logs | NTP sync? | `timedatectl status`; fix NTP |
| TLS forwarding fails | Cert expired / CA mismatch | Check cert chain; renew |
| UDP packets dropped | Firewall rule | Open UDP/514 or switch to TCP |
