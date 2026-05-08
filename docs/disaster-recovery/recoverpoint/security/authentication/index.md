# RecoverPoint — Authentication

> Part of the [RecoverPoint](../../) > [Security](../) reference.

---

## API Token Management

For automation accounts using the REST API, use token-based auth rather than username/password in scripts:

```bash
# Create session token
curl -k -u admin:password -X POST https://<rpa-ip>/rest/users/sessions
# Response includes: {"sessionId": "<token>"}

# Use token in subsequent calls
curl -k -H "Authorization: Bearer <token>" https://<rpa-ip>/rest/consistency_groups
```

- Store API tokens in CyberArk or HashiCorp Vault — never hard-code in scripts
- Rotate tokens quarterly or on personnel change
- Scope dedicated API accounts to the minimum required role (Monitor for observability, Admin only for failover automation)

---

## Audit Log

RecoverPoint maintains a system audit log of all user actions:

```bash
# View audit log (RecoverPoint CLI)
get_audit_log -last 100
get_audit_log -from_date "2026-01-01" -to_date "2026-01-31"
```

Forward to SIEM via syslog: Management Console → System Settings → Syslog Notifications. Alert on:
- Any admin account login outside business hours
- `enable_image_access` events (indicates failover test or actual DR)
- User account creation or role changes
