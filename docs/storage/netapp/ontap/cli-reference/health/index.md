# System Health & Events

> Part of the NetApp ONTAP CLI Reference.

## System Health

```bash
# Overall health status
system health status show
# Expected: ok

# Health alerts (unresolved issues)
system health alert show

# Health subsystems
system health subsystem show

# Node-level connectivity
system health node-connectivity show
```

## EMS Event Log

```bash
# Recent events (default: last 1000)
event log show

# Filter by severity
event log show -severity emergency
event log show -severity alert
event log show -severity error

# Filter by node
event log show -node <node_name>

# Filter by time window
event log show -time ">1h"
event log show -time ">24h"

# Filter by message name
event log show -messagename wafl.vol.full
```

## EMS Notification Config

```bash
# Show EMS destinations (email, syslog, etc.)
event notification show
event notification destination show
```

## Firmware & Software

```bash
# Show current installed image versions
system node image show

# Update firmware (disk, shelf, SP)
system node firmware update -node <node>

# Show pending upgrades
system node upgrade-revert show
```

## AutoSupport

```bash
# Check AutoSupport status
system node autosupport show
system node autosupport show -fields state,last-successful-destination

# Send manual AutoSupport
system node autosupport invoke -node <node> -type all -message "Manual test"
```

## Quick Reference

| Command | Purpose |
|---|---|
| `system health status show` | Overall health |
| `system health alert show` | Active alerts |
| `event log show -severity error` | Recent errors |
| `storage failover show` | HA pair state |
| `cluster show` | Node health |
| `network interface show -status-oper down` | Down LIFs |
