# PowerMax — Authentication

## Active Directory / LDAP

Unisphere for PowerMax supports LDAP and Active Directory for administrator authentication:

- Configure under Unisphere → Settings → Security → LDAP.
- Map AD groups to Unisphere roles: `StorageAdmin`, `SecurityAdmin`, `Operator`, `Monitor`.
- Use a service account with read-only LDAP bind permissions; avoid using a personal account.
- Test LDAP connectivity with `ldapsearch` before completing configuration to avoid lockout.
- Retain at least one local admin account as a break-glass credential in the password vault.

## Audit Logging

All configuration changes on PowerMax are logged as audit events:

```bash
# List recent audit events (last 100)
symevent -sid <SID> list -last 100

# Filter audit events for a specific user
symevent -sid <SID> list -filter "user eq <username>"

# Export audit log to file
symevent -sid <SID> list > /tmp/audit_events.txt
```

- Events include: timestamp, user, action, object type, object name, and result.
- Export audit logs to a SIEM (Splunk, QRadar, etc.) via syslog from the Unisphere host.
- Retain audit logs for a minimum of 12 months per most regulatory frameworks.
