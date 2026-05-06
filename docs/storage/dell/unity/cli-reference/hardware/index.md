# Physical Disks & Hardware

> Part of the Dell Unity CLI Reference (Unisphere CLI).

## Disks

```bash
# List all disks
uemcli -d <ip> -u admin /stor/config/disk show

# Detailed disk view — model, speed, capacity, health, location
uemcli -d <ip> -u admin /stor/config/disk show -detail

# Filter by health
uemcli -d <ip> -u admin /stor/config/disk show -detail | grep -i "health\|failed\|degraded"
```

### Disk Health States

| State | Meaning | Action |
|---|---|---|
| OK | Healthy | None |
| Degraded | Performance issue or predictive failure | Monitor closely |
| Failed | Drive has failed | Replace immediately |
| Faulted | Array has quarantined the disk | Replace |
| Unknown | Not recognized | Check seating |

## Disk Groups

```bash
# List disk groups (RAID sets)
uemcli -d <ip> -u admin /stor/config/dg show

# Detail — RAID type, disk count, health, pool association
uemcli -d <ip> -u admin /stor/config/dg show -detail

# Filter degraded disk groups
uemcli -d <ip> -u admin /stor/config/dg show -detail | grep -i degraded
```

## Storage Processors

```bash
# SP status (SPA and SPB)
uemcli -d <ip> -u admin /sys/sp show

# SP detail — model, firmware, network ports, health
uemcli -d <ip> -u admin /sys/sp show -detail

# SP memory and CPU utilisation
uemcli -d <ip> -u admin /sys/sp show -detail | grep -E "CPU|Memory|Health"
```

## Enclosures and DAEs

```bash
# List enclosures (disk array enclosures)
uemcli -d <ip> -u admin /sys/encl show

# Enclosure detail
uemcli -d <ip> -u admin /sys/encl show -detail
```

## Power Supplies and Fans

```bash
# Power supply health
uemcli -d <ip> -u admin /sys/powersupply show

# Fan status
uemcli -d <ip> -u admin /sys/fan show
```

## Battery Backup Units (BBU)

```bash
# BBU status (protects write cache on SP failure)
uemcli -d <ip> -u admin /sys/battery show
uemcli -d <ip> -u admin /sys/battery show -detail
```

## Hardware Health Summary

```bash
# Quick hardware health overview
uemcli -d <ip> -u admin /sys/general show -detail | grep -i health

# All hardware components with non-OK status
uemcli -d <ip> -u admin /sys/sp show -detail | grep -iv "OK\|header"
uemcli -d <ip> -u admin /stor/config/disk show -detail | grep -iv "OK\|header"
```
