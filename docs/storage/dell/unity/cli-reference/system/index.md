# System & Status

> Part of the Dell Unity CLI Reference (Unisphere CLI).

## System Information

```bash
# General system info — name, model, serial, software version
uemcli -d <ip> -u admin /sys/general show -detail

# Current system time
uemcli -d <ip> -u admin /sys/time show

# Software version and build
uemcli -d <ip> -u admin /sys/sw/version show
```

## Alerts and Events

```bash
# Active alerts (open, unresolved)
uemcli -d <ip> -u admin /prac/alert show

# Alert history
uemcli -d <ip> -u admin /prac/alert show -detail

# Syslog events
uemcli -d <ip> -u admin /event/syslog show

# Audit events (user actions)
uemcli -d <ip> -u admin /event/audit show
```

### Alert Severity Levels

| Severity | Meaning | Action |
|---|---|---|
| INFO | Informational | No action required |
| WARNING | Potential issue | Monitor |
| ERROR | Degraded functionality | Investigate |
| CRITICAL | Service impacting | Immediate response |

## Licenses

```bash
# View installed licenses
uemcli -d <ip> -u admin /sys/lic show

# Check expiry on time-limited licenses
uemcli -d <ip> -u admin /sys/lic show -detail | grep -i expir
```

## ESRS (Remote Support)

```bash
# ESRS (Embedded Service Remote Support) connectivity status
uemcli -d <ip> -u admin /sys/esrs show

# Enable ESRS
uemcli -d <ip> -u admin /sys/esrs set -enabled true

# Manual support call home
uemcli -d <ip> -u admin /sys/esrs callhome -type heartbeat
```

## NTP and DNS

```bash
# NTP configuration
uemcli -d <ip> -u admin /sys/general show -detail | grep -i ntp

# DNS servers
uemcli -d <ip> -u admin /sys/dns show
```

## SP Failover (Trespass)

```bash
# Move a resource (LUN or NAS server) to the other SP
uemcli -d <ip> -u admin /sys/sp/trespass set -res <resource_id> -sp <spa|spb>
```

## Upgrade Status

```bash
# Check if an upgrade is in progress
uemcli -d <ip> -u admin /sys/sw show

# Software upgrade history
uemcli -d <ip> -u admin /sys/sw/version show
```

## Health Summary

```bash
# Overall system health
uemcli -d <ip> -u admin /sys/general show -detail | grep -i health

# All hardware component health
uemcli -d <ip> -u admin /sys/sp show -detail | grep -i health
uemcli -d <ip> -u admin /stor/config/disk show -detail | grep -i health
uemcli -d <ip> -u admin /stor/config/dg show -detail | grep -i health
uemcli -d <ip> -u admin /stor/config/pool show -detail | grep -i health
```
