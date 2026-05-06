# Events & Audit

> Part of the Dell PowerMax CLI Reference (SYMCLI). Review events after any array alert, before opening a support case, and as part of regular health checks.

## System Events

```bash
# List all recent events
symevent list -sid <sid>
symevent list -sid <sid> -v

# Filter by time range
symevent list -sid <sid> -start_time "01/01/2026 00:00:00"
symevent list -sid <sid> -start_time "01/01/2026 00:00:00" -end_time "01/02/2026 00:00:00"

# Filter by severity
symevent list -sid <sid> -v | grep -i "WARNING\|ERROR\|FATAL"

# Event count summary
symevent list -sid <sid> | wc -l
```

## Audit Log

```bash
# List all audit entries
symaudit list -sid <sid>
symaudit list -sid <sid> -v

# Filter by time
symaudit list -sid <sid> -start_time "01/01/2026 00:00:00"

# Filter by user
symaudit list -sid <sid> -user <username>

# Filter by action type
symaudit list -sid <sid> -v | grep -i "Create\|Delete\|Modify\|SRDF"
```

## Health Checks via Events

```bash
# Check for any uncleared events (active alerts)
symevent list -sid <sid> -v | grep -i "uncleared\|active"

# Check for drive-related events
symevent list -sid <sid> -v | grep -i "disk\|drive\|BE\|DAE"

# Check for replication events
symevent list -sid <sid> -v | grep -i "RDF\|SRDF\|replication"

# Check for port/director events
symevent list -sid <sid> -v | grep -i "port\|director\|link"
```

## Export for Support Case

```bash
# Export events to file for Dell TAC
symevent list -sid <sid> -v -output csv > /tmp/events-$(date +%Y%m%d).csv
symaudit list -sid <sid> -v > /tmp/audit-$(date +%Y%m%d).txt
```

## Alerting Integration

Events on PowerMax can be forwarded via:
- Unisphere for PowerMax → Settings → Alert Policies (email, SNMP trap)
- Solutions Enabler SYMAPI server event daemon
- Dell CloudIQ (cloud-connected monitoring) — see [CloudIQ Operations](../../../../../monitoring/cloudiq/operations/)

## Quick Reference

| Task | Command |
|---|---|
| List all events | `symevent list -sid <sid>` |
| Events with detail | `symevent list -sid <sid> -v` |
| Events since date | `symevent list -sid <sid> -start_time "MM/DD/YYYY HH:MM:SS"` |
| Audit log | `symaudit list -sid <sid>` |
| Audit by user | `symaudit list -sid <sid> -user <username>` |
