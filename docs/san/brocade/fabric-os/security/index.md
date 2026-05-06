# Brocade Fabric OS Security

Switch access is hardened by disabling Telnet and HTTP, leaving SSH and HTTPS as the only management protocols. RBAC is enforced using built-in Fabric OS roles: `admin` for full access, `switchadmin` for switch-level operations, `zoneadmin` for zoning-only changes, and `operator` for read-only monitoring. Active Directory authentication is configured via RADIUS, with local accounts retained only as a break-glass fallback. All configuration changes are logged via `auditlog` and forwarded to the SIEM via secure syslog. IPfilter policies restrict management plane access to approved management network subnets only.

| Control | Implementation |
|---|---|
| Management protocols | SSH, HTTPS only (Telnet/HTTP disabled) |
| RBAC | FOS built-in roles (admin, switchadmin, zoneadmin, operator) |
| Authentication | RADIUS to Active Directory; local break-glass account |
| Audit logging | `auditlog` — all config changes logged |
| Syslog | Secure syslog to SIEM |
| IP access control | IPfilter policy — management subnet only |
