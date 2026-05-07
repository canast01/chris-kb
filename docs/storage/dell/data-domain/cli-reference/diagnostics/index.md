# Diagnostics

> Part of the Dell Data Domain CLI Reference.

```mermaid
flowchart LR
    Diagnostics["Diagnostics"]
    Diagnostics --> S0["Log Access"]
    Diagnostics --> S1["Support Bundle"]
    Diagnostics --> S2["System Shell (ddsh)"]
    Diagnostics --> S3["Network Diagnostics"]
    Diagnostics --> S4["Hardware Diagnostics"]
    Diagnostics --> S5["Performance Capture"]
    Diagnostics --> S6["Alert History for TAC"]
```

## Log Access

```bash
# View system log (most recent events)
log view

# List available log files
log list

# Dump the full system log to stdout
log dump system

# Follow the log in real time
log watch

# Specific log file
log view <log_filename>
```

## Support Bundle

Support bundles collect all logs and diagnostics for TAC cases:

```bash
# Create a support bundle
support bundle create

# List available bundles
support bundle show

# Export bundle to remote server (SCP)
support bundle export scp://user@host:/path/bundle.tar.gz

# Export bundle to FTP
support bundle export ftp://user:pass@host/path/
```

## System Shell (ddsh)

`ddsh` provides a Unix-like shell with additional diagnostic tools:

```bash
# Enter the diagnostic shell
ddsh

# Inside ddsh:
diagnose all             # full system diagnostic run
iostat 1 10              # I/O statistics (1s interval, 10 iterations)
vmstat 1 10              # Virtual memory and CPU stats
netstat -an              # Active network connections
df -h                    # Filesystem usage
top                      # Process list
```

## Network Diagnostics

```bash
# Ping from the Data Domain
net ping <ip>

# Traceroute
net traceroute <ip>

# Interface error counters
net show stats | grep -i error
```

## Hardware Diagnostics

```bash
# Overall health check (hardware + software)
health check show

# Disk health
disk show state
disk show detail | grep -E "error|sector"

# Enclosure sensors (temperature, power, fan)
enclosure show hardware
```

## Performance Capture

```bash
# Inside ddsh — capture IOPS and throughput
iostat -x 1 30

# Filesystem stats snapshot
filesys show stats

# DDBoost throughput
ddboost show stats
```

## Alert History for TAC

```bash
# Export all current and historical alerts
alert show history > /tmp/alert_history.txt
support bundle create   # includes alert history automatically
```
