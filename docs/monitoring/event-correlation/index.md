# Event Correlation

Event correlation links related alerts and log entries across systems to identify root causes rather than treating each symptom individually.
## Core Principle

An alert is a symptom. Event correlation reveals whether multiple alerts share a single cause — a storage array losing a controller causes host I/O errors, application timeouts, and monitoring alerts simultaneously. Without correlation, that's 20 tickets instead of 1.

## Time Synchronisation — Prerequisite

All correlation depends on accurate timestamps. Verify NTP before investigating any multi-system event.

```bash
# Linux
timedatectl status
chronyc tracking

# Windows
w32tm /query /status

# Cisco IOS / NX-OS
show ntp status
show clock detail
```

## Correlation Workflow

1. **Collect timeline** — gather events from all affected systems within the suspected window (use UTC timestamps)
2. **Identify common start time** — when did the first alert fire?
3. **Map dependencies** — which systems feed into each other?
4. **Narrow to single root cause** — storage, network, or compute failure?
5. **Confirm by elimination** — does resolving the root cause clear all downstream alerts?

## Building a Correlation Timeline

```bash
# Linux — extract events from a specific window across log files
journalctl --since "2026-05-05 14:00:00" --until "2026-05-05 14:30:00" -p err --no-pager

# Grep multiple log files for a time window
grep "May  5 14:0[0-9]" /var/log/messages /var/log/syslog /var/log/nginx/error.log
```

## Common Correlation Patterns

| Symptom Cluster | Probable Root Cause |
|---|---|
| Multiple hosts: I/O errors + application timeouts | Storage array or fabric fault |
| Multiple hosts: network unreachable at same time | Upstream switch / router failure |
| VM slowness + storage latency on one array | Array controller issue or disk rebuild |
| Authentication failures across multiple services | AD / LDAP / DNS failure |
| Backup failures + high host CPU | Resource contention during backup window |
| One host: multiple service alerts simultaneously | Host hardware (memory/disk) or kernel panic |

## SIEM Correlation Rules (Examples)

**Graylog / Splunk — correlated alert logic:**
```
# Multiple auth failures from same source within 5 minutes
index=security sourcetype=auth action=failure
| stats count by src_ip, user
| where count > 10
| eval alert="Possible brute force"

# Storage latency spike + host I/O error within 2-minute window
index=infra (sourcetype=ontap OR sourcetype=os_ioerr)
| transaction maxspan=2m host
| where eventcount > 1
```

## Dependency Map (template)

Document for each critical service:

```
Service: ERP Application
  → App server: app01, app02
      → Database: db01 (Oracle)
          → Storage: ONTAP SVM prod-svm, volume erp-data
              → SAN fabric: MDS-A, MDS-B, Zone: erp_zone
      → Load balancer: F5-prod VIP 10.10.10.100
  → Auth: AD domain controllers dc01, dc02
  → DNS: 10.10.10.53
```

## Cross-Platform Log Locations

| System | Log location |
|---|---|
| Linux OS | `/var/log/messages`, `/var/log/syslog`, `journalctl` |
| Windows | Event Viewer: System, Application, Security |
| ONTAP | EMS: `event log show -severity error` |
| VMware | `/var/log/vmkernel.log`, vCenter Events |
| Cisco NX-OS | `show logging last 100` |
| Brocade FOS | `errShow` |
