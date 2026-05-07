# System Status

> Part of the Dell Data Domain CLI Reference.
## System Information

```bash
# Full system overview
system show all

# Software version
system show version

# Hardware inventory (disks, enclosures, NIC, HBA)
system show hardware

# Current system statistics (CPU, memory, throughput)
system show stats

# Uptime
system show uptime

# Serial number and model
system show summary
```

## Health Checks

```bash
# Run built-in health check
health check show

# Active alerts (open, unacknowledged)
alert show current

# Alert history (all alerts, resolved and unresolved)
alert show history

# Brief alert history (most recent)
alert show history brief

# Clear a resolved alert
alert acknowledge --id <alert_id>
```

## Alert Levels

| Level | Meaning |
|---|---|
| INFO | Informational only |
| WARNING | Action may be required |
| ERROR | Degraded functionality — investigate |
| CRITICAL | Service impacting — immediate action required |

## Software and Licensing

```bash
# Show installed software packages
system software version show

# License status
elicense show
```

## Power and Environment

```bash
# Power supply status
enclosure show hardware | grep -i power

# Fan status
enclosure show hardware | grep -i fan

# Temperature sensors
enclosure show hardware | grep -i temp
```

## System Time and NTP

```bash
# Current time
ntp status

# NTP servers configured
ntp show

# Add NTP server
ntp add timeserver <ntp_ip>
```

## Rebooting and Shutdown

```bash
# Safe shutdown (completes in-progress operations)
system shutdown

# Restart the DDOS software (not a full reboot)
system restart

# Full reboot
system reboot
```

## Support Bundle

```bash
# Create a support bundle (for TAC cases)
support bundle create

# List available bundles
support bundle show

# Transfer to external server
support bundle export scp://user@host:/path/bundle.tar.gz
```
