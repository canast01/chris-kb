# Syslog and Centralized Logging

## Architecture Overview

```
Hosts (rsyslog / syslog-ng / journald)
    → Syslog server / SIEM (Splunk / Graylog / ELK / Syslog-NG)
        → Long-term archive (object storage / NFS)
```

## Syslog Service Health

```bash
# Check rsyslog running
systemctl status rsyslog

# Check syslog-ng
systemctl status syslog-ng

# Test log ingestion — inject a test message and verify receipt
logger -t TEST "Health check message"
grep "Health check message" /var/log/messages

# Check disk on log server
df -h /var/log
```

## Configure rsyslog to Forward to Central Collector

```bash
# /etc/rsyslog.conf or /etc/rsyslog.d/forward.conf

# UDP (less reliable)
*.* @<syslog-server>:514

# TCP (preferred)
*.* @@<syslog-server>:514

# TLS (secure)
*.* action(type="omfwd" target="<syslog-server>" port="6514" protocol="tcp"
         StreamDriver="gtls" StreamDriverMode="1" StreamDriverAuthMode="anon")
```

```bash
# Apply after editing
systemctl restart rsyslog

# Test
logger -t TEST "Forwarding test from $(hostname)"
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

**Graylog / Splunk search examples:**
```
# Graylog GELF query
source:<hostname> AND level:<4 AND facility:daemon

# Splunk SPL
index=infra host=<hostname> sourcetype=syslog level=error | timechart count by host
```

## Troubleshooting — Logs Not Arriving

| Symptom | Check | Action |
|---|---|---|
| No logs from host | rsyslog running? | `systemctl start rsyslog` |
| Logs stopped mid-stream | Disk full on collector? | `df -h /var/log` — rotate or expand |
| Time mismatch in logs | NTP sync? | `timedatectl status`; fix NTP |
| TLS forwarding fails | Cert expired / CA mismatch | Check cert chain; renew |
| UDP packets dropped | Firewall rule | Open UDP/514 or switch to TCP |
