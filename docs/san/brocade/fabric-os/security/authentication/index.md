# FabricOS — Authentication

> Part of the [Security](../) reference.

---

## RADIUS Authentication

```bash
# Configure RADIUS server
aaaconfig --add <radius-server-ip> -conf radius -p <port> -s <shared-secret>

# Set authentication order: RADIUS primary, local fallback
aaaconfig --authorder RADIUS;LOCAL

# Verify RADIUS is configured
aaaconfig --show

# Test RADIUS authentication
aaaconfig --validate -user <test-user>
```

**Local fallback account** — retain the local `admin` account as break-glass. Store the password in the enterprise vault.

---

## RADIUS Role Mapping

RADIUS-authenticated users receive their role from the RADIUS server via the `Foundry-User-Priv` AV-pair or the configured role-mapping on the switch.

---

## TACACS+ Authentication

```bash
# Configure TACACS+
aaaConfig --add <server_ip> -p <port> -s <secret> -t tacacs+

# Show auth settings
authUtil --show
```

---

## SSH Configuration

```bash
# Show SSH status
sshUtil --show

# Generate SSH host keys
sshUtil --genkey -t rsa
```

---

## NTP Requirement

NTP must be configured and synced — required for log correlation and certificate-based authentication.

---

## Local Account Standards

- Root account password changed; stored in vault; break-glass use only
- All non-break-glass access via RADIUS with local as fallback only
- Password policy enforced: minimum length, complexity, expiry
