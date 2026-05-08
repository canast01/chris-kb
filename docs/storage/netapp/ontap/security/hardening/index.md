# ONTAP — Hardening

> Security baselines and compliance configuration for NetApp ONTAP.

## Hardening Checklist

- [ ] Password authentication disabled for `admin`; public key only
- [ ] Built-in `diag` and `maintenance` accounts locked
- [ ] SSH idle session timeout configured: `security session timeout modify -timeout 600`
- [ ] TLS 1.2 minimum enforced for HTTPS
- [ ] SNMPv1/v2c communities deleted; SNMPv3 only
- [ ] AutoSupport using HTTPS (not HTTP/SMTP) for data transmission
- [ ] NVE or NAE enabled on all production volumes containing sensitive data
- [ ] External KMIP key manager configured (OKM acceptable for non-regulated environments)
- [ ] Admin audit logging enabled and log forwarding to SIEM configured
- [ ] FPolicy configured for production NAS SVMs if file access auditing is required by compliance
- [ ] RBAC service accounts with minimum required permissions for all automation and monitoring tools

## TLS Hardening

```bash
# Enforce TLS 1.2 minimum for HTTPS management
security config modify -interface HTTPS -min-protocol-version TLSv1.2

# Check current TLS/SSL configuration
security config show

# Restrict SSH ciphers and MACs to strong algorithms
security ssh modify -vserver <cluster-name> -ciphers aes256-ctr,aes192-ctr,aes128-ctr -macs hmac-sha2-256,hmac-sha2-512

# Disable Telnet and RSH
security protocol show
# Ensure telnet and rsh show enabled=false
```

## SNMP Hardening

```bash
# Delete all SNMPv1/v2c community strings
system snmp community delete -community-name public
system snmp community delete -community-name <any-other-v1v2-community>

# Configure SNMPv3 with auth and privacy
system snmp user create -username snmpv3user -authmethod md5 -authpassword <auth-pass> -privmethod aes128 -privpassword <priv-pass>
```

## Session and Access Controls

```bash
# Set SSH idle session timeout (seconds)
security session timeout modify -timeout 600

# Lock built-in diagnostic accounts
security login lock -username diag -vserver <cluster>

# Verify no unnecessary accounts are active
security login show
```

## Audit and SIEM Forwarding

```bash
# View recent administrative audit events
security audit log show
security audit log show -user admin -time-range 24h

# Configure EMS log forwarding to syslog/SIEM
event notification destination create -name siem-dest -syslog <siem-ip>
event notification create -filter-name important-events -destinations siem-dest
```

## AutoSupport Security

```bash
# Enforce HTTPS delivery (not HTTP or SMTP)
autosupport modify -node * -transport https

# Verify HTTPS connectivity
autosupport check show

# Confirm AutoSupport is enabled on all nodes
autosupport show -fields state,transport
```
