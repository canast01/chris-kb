# RecoverPoint — Authentication

> Part of the [RecoverPoint](../../index.md) > [Security](../index.md) reference.

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

Forward to SIEM via syslog: Management Console → System Settings → Syslog Notifications. Alert on:
- Any admin account login outside business hours
- `enable_image_access` events (indicates failover test or actual DR)
- User account creation or role changes
