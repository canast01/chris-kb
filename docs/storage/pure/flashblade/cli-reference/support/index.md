# Support & Diagnostics

> Part of the [Pure FlashBlade CLI Reference](../).
## Phone Home (Call Home)

Pure FlashBlade proactively sends diagnostic data to Pure Support:

```bash
# View phone home configuration and status
purefb phonehome show

# Send a phone home bundle (manual trigger)
purefb phonehome send --type auto

# Send a specific type
purefb phonehome send --type test   # test connectivity only
```

## Support Connectivity

```bash
# View remote support configuration
purefb support show

# Enable remote support (Pure1 / Secure Remote Assist)
purefb support update --enabled true

# Disable remote support
purefb support update --enabled false
```

## Log Collection

```bash
# Export logs for TAC support cases
purefb support log export

# The exported log bundle is saved locally (SCP or HTTPS download)
```

## System Diagnostics

```bash
# Overall system health
purefb array show

# Hardware component health (blades, chassis, network)
purefb blade show
purefb blade show --detailed

# Network interface status
purefb network-interface show
```

## Alerts

```bash
# Active alerts
purefb alert show

# Alert history
purefb alert show --all

# Acknowledge an alert
purefb alert update --id <alert_id> --status closed
```

## Software Version

```bash
# Current Purity//FB version
purefb array show | grep -i version

# Available software upgrades
purefb software show
```

## Connecting to Pure1

Pure1 is the cloud-based management and analytics platform:

- All FlashBlade arrays that have phone home enabled feed data to Pure1
- Access at pure1.purestorage.com
- Provides capacity forecasting, AI-driven support, and lifecycle management

```bash
# Confirm Pure1 connectivity via phone home
purefb phonehome show | grep -i status
```

## Common Support Scenarios

| Issue | First Step | Command |
|---|---|---|
| System alert | Check alert detail | `purefb alert show` |
| Blade failure | Check blade health | `purefb blade show --detailed` |
| Replication issue | Check replica link state | `purefb fs-replica-link show --detailed` |
| Capacity concern | Check capacity | `purefb array show` |
| Phone home not working | Check connectivity | `purefb support show` |
