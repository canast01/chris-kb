# FabricOS — Hardening

> Part of the [Security](../) reference.

---

## Hardening Checklist

- [ ] Telnet and HTTP disabled; SSH and HTTPS only
- [ ] Root account password changed; stored in vault; break-glass use only
- [ ] RADIUS configured pointing to Active Directory; local accounts as fallback only
- [ ] RBAC roles assigned — `switchadmin` for ops, `zoneadmin` for zoning-only changes
- [ ] IPfilter policy restricting management plane access to approved management subnet
- [ ] SNMP v3 configured; default community strings removed
- [ ] Audit logging (`auditlog`) enabled and forwarded to SIEM
- [ ] NTP configured and synced (required for log correlation and certificate-based auth)
- [ ] Password policy enforced: minimum length, complexity, expiry

---

## Audit Logging

```bash
# Enable audit logging
auditcfg --class 1,2,3,4   # Log zone changes (3), security events (2), firmware (4), fabric (1)

# View recent audit log entries
auditlog --show

# Forward audit log via syslog
syslogadmin --add -ip <siem-ip>

# Verify syslog configuration
syslogadmin --show
```

---

## Security Baselines

| Control | Standard |
|---|---|
| SNMP | SNMPv3 only; community strings in vault; quarterly rotation |
| Management access | SSH only; Telnet disabled; `sshutil disable telnet` |
| RADIUS/TACACS+ | All fabrics must use central AAA; local accounts for break-glass only |
| Audit logging | `auditcfg --set 1` — all logins and config changes logged |
| IPfilter | Management subnet restriction on all production switches |
