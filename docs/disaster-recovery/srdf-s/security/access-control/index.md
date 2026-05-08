# SRDF/S — Access Control

> Part of the [SRDF/S Security](../) reference.

---

## Preventing Accidental Failover

SRDF/S failovers are zero-data-loss but cause site-wide impact. Guard against accidental execution:

- Require second-factor confirmation for `symrdf failover` in production:
  ```bash
  export SYMCLI_CONFIRM=prompt    # Requires manual y/n before executing
  ```
- Implement a two-person rule: all production SRDF failovers require peer approval before execution
- Restrict `symrdf establish -full` (full resync) to break-glass account — this destroys R2 content

---

## Audit Logging

All SRDF state changes are recorded in the PowerMax audit log:

```bash
# View recent RDF events
symevent list -sid <SID> -type rdf -last 100

# Export for SIEM ingest
symevent list -sid <SID> -type rdf -output csv > /tmp/rdf_events.csv
```

Configure Unisphere → Notifications → Syslog to forward SRDF events to SIEM. Alert on:
- `SRDF Split` outside maintenance windows
- `SRDF Failover` (any occurrence)
- `SRDF Suspend` without corresponding maintenance ticket
- `SRDF Invalid` (indicates device state inconsistency)
