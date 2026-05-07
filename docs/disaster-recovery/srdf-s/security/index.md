# SRDF/S Security
## Solutions Enabler RBAC

Control who can execute SRDF failover and resync operations:

```bash
# List current user roles
symauth -sid <SID> list

# Add DR operator role — failover-capable, scoped to specific SRDF groups
symauth -sid <SID> add -username svc_dr_ops -role StorageAdmin -scope rdfg:<group_number>

# Add monitoring account — read-only
symauth -sid <SID> add -username svc_monitoring -role StorageMonitor
```

| Role | Allowed Commands | Prohibited Commands |
|---|---|---|
| `StorageAdmin` | symrdf failover, establish, split, suspend, set mode | — |
| `StorageMonitor` | symrdf query, symcfg list | All state-changing ops |

Never assign `StorageAdmin` to automated monitoring or backup accounts.

## Preventing Accidental Failover

SRDF/S failovers are zero-data-loss but cause site-wide impact. Guard against accidental execution:

- Require second-factor confirmation for `symrdf failover` in production:
  ```bash
  export SYMCLI_CONFIRM=prompt    # Requires manual y/n before executing
  ```
- Implement a two-person rule: all production SRDF failovers require peer approval before execution
- Restrict `symrdf establish -full` (full resync) to break-glass account — this destroys R2 content

## FCIP Encryption

SRDF/E encrypts data over FCIP links using AES-256:

```bash
# Check encryption status per SRDF group
symcfg list -rdfg -v | grep -E "RDF Group|Encryption"

# Enable encryption on an existing group (requires group to be in Split state)
symrdf -g <rdfg> split -noprompt
symrdf -g <rdfg> set encrypt enable
symrdf -g <rdfg> establish -noprompt
```

## FC Fabric Zoning

SRDF director ports must be hard-zoned to prevent unauthorised array-to-array communication:

- Create dedicated SRDF zones containing only the SRDF director port WWPNs of the two arrays
- No other initiators/targets in SRDF zones
- Use hard zoning (WWPN-based) — soft zone aliases are acceptable for documentation only
- Zone naming: `SRDF_<source_array_port>_<target_array_port>`

Verify SRDF director port WWPNs:
```bash
symcfg list -rdfg <rdfg> -v | grep "Director"
```

## Management API Security

The Unisphere REST API should be secured:

- Enable HTTPS only (disable HTTP on port 8080)
- Use client certificate authentication for service accounts
- Scope API accounts to minimum required capabilities
- Rotate service account certificates annually

Verify TLS configuration:
```bash
curl -k https://<unisphere>:8443/univmax/restapi/system/version
# Production systems should use trusted CA cert (remove -k flag)
```

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
