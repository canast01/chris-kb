# Health Checks

## Daily Health Check

```bash
# 1. System alerts — any unacknowledged issues?
alert show current

# 2. Filesystem status
filesys status
filesys show space

# 3. Disk state — all normal?
disk show state

# 4. Replication lag
replication status
replication show stats | grep lag

# 5. Cleaning status
filesys clean status
```

## Weekly Health Check

```bash
# Compression and deduplication ratio
filesys show compression summary

# DDBoost active clients
ddboost show clients

# NFS and CIFS connections
nfs show clients
cifs show clients

# Alert history (look for recurring alerts)
alert show history brief

# System uptime and performance stats
system show uptime
system show stats
```

## Capacity Monitoring

| Metric | Threshold | Action |
|---|---|---|
| Post-comp used | > 80% | Plan expansion or cleaning cycle |
| MTree quota used | > 85% | Increase quota or expire old data |
| Cleaning last run | > 7 days | Trigger `filesys clean start` |
| Replication lag | > 4 hours | Investigate network or source load |

## Replication Health

```bash
# All replication contexts
replication show all

# Contexts not in replicating or idle state
replication status | grep -v "replicating\|idle"

# Lag detail per context
replication show stats
```

## Hardware Health

```bash
# Disk states (no failed or reconstructing disks)
disk show state | grep -v normal

# Enclosure health (power, fans, temperature)
enclosure show hardware | grep -iE "fault|failed|warning"

# RAID group status
raid show all | grep -v "normal\|OK"
```

## Pre-Change Checklist

- [ ] No critical or error alerts active
- [ ] Filesystem enabled and healthy
- [ ] All disks in normal state
- [ ] No RAID rebuild in progress
- [ ] Replication lag within acceptable range
- [ ] Cleaning not in progress (or aware it may run)
- [ ] Support bundle taken for baseline

## Health Summary Table

| Check | Expected | Command |
|---|---|---|
| Active alerts | None critical | `alert show current` |
| Filesystem state | Enabled | `filesys status` |
| Disk state | All normal | `disk show state` |
| RAID state | Normal | `raid show all` |
| Replication lag | < 4 hours | `replication show stats` |
| Capacity used | < 80% | `filesys show space` |
| Last cleaning | < 7 days | `filesys clean status` |
