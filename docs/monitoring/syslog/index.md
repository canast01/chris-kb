# Syslog and Centralized Logging

```text
Syslog Flow
┌─────────────────────────────────────────────────┐
│  Device (facility.severity)                     │
│  e.g. local7.error — FlashArray alert           │
└───────────────────────┬─────────────────────────┘
                        ▼ UDP/TCP port 514
┌─────────────────────────────────────────────────┐
│  Syslog message                                 │
│  <priority> timestamp hostname tag: message     │
└───────────────────────┬─────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────┐
│  Syslog Collector                               │
│  (rsyslog / syslog-ng / Graylog input)          │
└───────────────────────┬─────────────────────────┘
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
┌─────────────────────┐   ┌─────────────────────┐
│  SIEM               │   │  Log store          │
│  (Splunk / Graylog) │   │  (ELK / object      │
│  correlation rules  │   │   storage archive)  │
└─────────────────────┘   └─────────────────────┘
```
┌───────────────────────────────────────── Monitoring — Syslog ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            Syslog — Centralised Log Collection: RFC 5424 over UDP/514 and TLS/6514            │   │
│   │        Sources: ESXi hosts · vCenter · NSX managers · storage arrays · network switches       │   │
│   │          Collectors: rsyslog/syslog-ng on-prem · Aria Log Insight · Splunk forwarder          │   │
│   │          Parsing: structured data fields: facility · severity · hostname · msgid · SD         │   │
│   │         ESXi config: esxcli system syslog config set --loghost=<IP>:514 --protocol=udp        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    TLS transport (port 6514) is required for syslog crossing security zone boundaries                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           Sources           │  │          Collectors         │  │          Consumers          │   │
│   │        ESXi: UDP 514        │  │       rsyslog HA pair       │  │       Aria Log Insight      │   │
│   │       vCenter: UDP 514      │  │       syslog-ng relay       │  │        Splunk indexer       │   │
│   │        NSX: TLS 6514        │  │      Log Insight agent      │  │       SIEM correlation      │   │
│   │     Storage: SNMP+syslog    │  │       Queue: 10k msg/s      │  │      Alert rules engine     │   │
│   │      Switches: UDP 514      │  │      TLS cert rotation      │  │       Retention policy      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  rsyslog VMs: 2x on dedicated VLAN · Log Insight cluster on vSphere · NFS for log storage             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RFC 5424          = IETF standard defining syslog message format with structured data                │
│  Facility          = Log category code (e.g. kern=0, user=1, mail=2, daemon=3)                        │
│  Severity          = Log level: 0=Emergency · 1=Alert · 2=Crit · 3=Err · 4=Warn · 5=Notice            │
│  rsyslog           = High-performance Linux syslog daemon; supports TCP/UDP/TLS/RELP                  │
│  syslog-ng         = Enterprise syslog daemon with advanced filtering and routing                     │
│  Log Insight       = VMware Aria Log Insight; structured log search and alerting                      │
│  TLS 6514          = Encrypted syslog transport; required for cross-zone log forwarding               │
│  RELP              = Reliable Event Logging Protocol; guaranteed delivery over TCP                    │
│  SD (structured)   = RFC 5424 key=value pairs in the structured-data section of syslog                │
│  esxcli syslog     = ESXi command to configure remote syslog destination and protocol                 │
│  SIEM              = Security Information and Event Management; consumes syslog for threat detection  │
│  Queue depth       = In-memory message buffer in collector; overflow causes message loss              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
```bash
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
