# FabricOS — Encryption

> Part of the [Security](../) reference.

---

## SNMP v3 Configuration

```bash
# Configure SNMP v3 interactively
snmpconfig --set mibCapability
# Follow prompts to configure:
# - User name
# - Authentication type: SHA
# - Authentication password
# - Privacy type: AES-128
# - Privacy password
# - Access level: readOnly or readWrite

# Verify SNMP configuration
snmpconfig --show
```

---

## Disable Unused Protocols

```bash
# Disable Telnet
# Via configure:
configure
# At "Secure mode" prompt: enable

# Disable HTTP (enable HTTPS only)
httpd --disable   # Disables the web server
httpcfg --set -https 1  # Enable HTTPS

# Verify active services
portshow   # Review management service ports
```

---

## Encryption Standards

| Control | Standard |
|---|---|
| SNMP | SNMPv3 only; community strings in vault; quarterly rotation |
| Management access | SSH only; Telnet disabled |
| HTTPS | HTTP disabled; HTTPS enforced |

---

## TLS and Certificate Management

Add TLS certificate configuration and renewal procedures here as they are defined.
