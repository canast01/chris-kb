# MDS — Hardening

> Part of the [Cisco MDS](../../) reference.

---

## Hardening Checklist

- [ ] Telnet, HTTP, and TFTP disabled; SSH and HTTPS only
- [ ] AAA configured (TACACS+ primary, RADIUS fallback) pointing to Active Directory
- [ ] Local `admin` account password stored in vault; used for break-glass only
- [ ] RBAC roles assigned: `network-admin` for ops, `network-operator` for monitoring
- [ ] VSAN isolation in place — production and replication VSANs separated
- [ ] Management interface IP ACL restricts access to management subnet only
- [ ] NTP configured and synced (required for certificate-based auth and log correlation)
- [ ] SNMP v3 configured; v1/v2c community strings disabled or restricted
- [ ] All config changes logged via `aaa accounting` to TACACS+ or syslog

---

## Disable Unused Services

```
# Disable Telnet
no feature telnet

# Disable HTTP (HTTPS only)
no feature http-server
feature https-server

# Disable TFTP server if not required
no feature tftp-server

# Verify only SSH and HTTPS are active
show feature | include telnet\|http\|tftp\|ssh
```
