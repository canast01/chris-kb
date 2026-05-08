# MDS — Authentication

> Part of the [Cisco MDS](../../) reference.

---

## AAA Configuration (TACACS+)

```
# Add TACACS+ server
tacacs-server host <tacacs-server-ip> key <shared-secret>

# Configure AAA to use TACACS+ for authentication, authorisation, and accounting
aaa authentication login default group tacacs+ local
aaa authorization commands default group tacacs+ local
aaa accounting default group tacacs+

# Keep local fallback in case TACACS+ is unreachable
username admin password <strong-password> role network-admin
```

**Verify AAA is working:**

```
test aaa group tacacs+ <test-username> <test-password>
```

---

## Local Accounts

- Local `admin` account password stored in vault; used for break-glass only
- One local admin per fabric
- All other access via TACACS+/RADIUS

```bash
# Show all local users
show users

# Create a local user
username <user> password <pass> role <role>

# Delete a user
no username <user>
```

---

## Standards

| Control | Standard |
|---|---|
| AAA | TACACS+ primary, RADIUS fallback |
| Local accounts | Break-glass only; one local admin per fabric |
| Role | `network-admin` for infrastructure team; `network-operator` for read-only |
| TACACS+ encryption | Enable key encryption: `tacacs-server key 7 <encrypted>` |

---

## Audit Logging

```
# Enable accounting for all exec and config commands
aaa accounting default group tacacs+

# Configure local syslog with accounting detail
logging level aaa 6
logging server <siem-ip> 5 facility local7

# Verify accounting is capturing config changes
show accounting log
```
