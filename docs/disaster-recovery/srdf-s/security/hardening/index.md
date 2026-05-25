# SRDF/S — Hardening

> Part of the [SRDF/S Security](../index.md) reference.

---

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

---

## Operational Hardening Checklist

| Item | Guidance |
|---|---|
| SYMCLI confirmation prompts | Set `SYMCLI_CONFIRM=prompt` on all production SE hosts |
| Break-glass account for full resync | Restrict `symrdf establish -full` to a named break-glass account only |
| Two-person rule for failover | All production SRDF failovers require peer approval before execution |
| Monitoring accounts | Never assign `StorageAdmin` to automated monitoring or backup accounts |
| SRDF zones | Hard-zone SRDF director ports; no other initiators/targets in SRDF zones |
| API HTTP | Disable HTTP on port 8080; enforce HTTPS only on Unisphere |
| Audit log forwarding | Forward SRDF events to SIEM via Unisphere syslog integration |
| Certificate rotation | Rotate service account certificates annually |
