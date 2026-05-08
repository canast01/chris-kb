# FabricOS — Authentication

> Part of the [Security](../) reference.

---

## Authentication Flow

```mermaid
flowchart TD
    loginAttempt["SSH / HTTPS login attempt"] --> ipCheck{"IPfilter\nsource IP permitted?"}
    ipCheck -->|Denied| reject["Connection refused"]
    ipCheck -->|Permitted| authOrder{"Auth order\nRADIUS first?"}
    authOrder -->|Yes| radiusReach{"RADIUS server\nreachable?"}
    radiusReach -->|No| localFallback["Fallback to LOCAL\naccounts on switch"]
    radiusReach -->|Yes| radiusAuth{"RADIUS\nauthentication?"}
    radiusAuth -->|Fail| reject2["Login denied\n(no local fallback if\nLOCAL not in authorder)"]
    radiusAuth -->|Success| vsaRole["Map VSA attribute\nto FabricOS role"]
    authOrder -->|"TACACS+"| tacacsAuth{"TACACS+\nauthentication?"}
    tacacsAuth -->|Success| tacacsRole["Role from TACACS+\nper-command authz available"]
    tacacsAuth -->|Fail| localFallback
    localFallback --> localAuth{"Local account\nvalid credentials?"}
    localAuth -->|Yes| localRole["Assign local role"]
    localAuth -->|No| reject3["Login denied"]
    vsaRole & tacacsRole & localRole --> session["CLI / Web session\nopened with assigned role"]
```

## Overview

Brocade FabricOS supports three authentication methods for management access:

1. **Local accounts** — stored on the switch; used for break-glass access only in production
2. **RADIUS** — recommended for enterprise environments; integrates with Active Directory via NPS
3. **TACACS+** — alternative to RADIUS; provides per-command authorization

All production switches must be configured with RADIUS or TACACS+ as the primary authentication method, with local accounts as a fallback. Local account credentials for break-glass must be stored in the enterprise vault (CyberArk, HashiCorp Vault, etc.) and rotated quarterly.

---

## RADIUS Authentication

### Configure RADIUS

```bash
# Add primary RADIUS server
aaaconfig --add <radius-server-ip> -conf radius -p 1812 -s <shared-secret>

# Add secondary RADIUS server (failover)
aaaconfig --add <radius-server2-ip> -conf radius -p 1812 -s <shared-secret>

# Set authentication order: RADIUS primary, local accounts as fallback
aaaconfig --authorder RADIUS;LOCAL

# Verify RADIUS configuration
aaaconfig --show
```

### Role Mapping via RADIUS

RADIUS users receive their FabricOS role from the RADIUS server via the VSA (Vendor-Specific Attribute) `Foundry-Privilege-Level` or a role-map configured on the switch.

**Brocade VSA (Vendor ID 1588):**

| Attribute | Value | FabricOS Role |
|---|---|---|
| Foundry-Privilege-Level | 2 | `admin` — full access |
| Foundry-Privilege-Level | 3 | `switchadmin` — switch operations |
| Foundry-Privilege-Level | 5 | `zoneadmin` — zone management only |
| Foundry-Privilege-Level | 6 | `operator` — read-only |

Configure the RADIUS server (Microsoft NPS / FreeRADIUS) to return the VSA based on Active Directory group membership:

- AD Group: `SAN-Admins` → `Foundry-Privilege-Level = 2`
- AD Group: `SAN-Operators` → `Foundry-Privilege-Level = 6`

### Test RADIUS Authentication

```bash
# Validate RADIUS connection and user authentication
aaaconfig --validate -user <test-username>
# The switch connects to the RADIUS server and authenticates — output shows SUCCESS or failure reason

# Show RADIUS server reachability (from switch)
# The switch must have IP connectivity to the RADIUS server on the management VLAN
ping <radius-server-ip>
```

If RADIUS authentication fails, the fallback to `LOCAL` authentication ensures break-glass access remains available. Always test RADIUS before relying on it.

---

## TACACS+ Authentication

TACACS+ provides finer-grained authorization than RADIUS — it can enforce per-command authorization in addition to per-user role assignment.

### Configure TACACS+

```bash
# Add TACACS+ server
aaaconfig --add <tacacs-server-ip> -conf tacacs+ -p 49 -s <shared-secret>

# Set authentication order: TACACS+ primary, local fallback
aaaconfig --authorder TACACS+;LOCAL

# Show current AAA configuration
aaaconfig --show
authutil --show
```

### TACACS+ vs RADIUS — Choosing Between Them

| Feature | RADIUS | TACACS+ |
|---|---|---|
| Authentication | Yes | Yes |
| Authorization (per-command) | No | Yes |
| Accounting | Limited | Full |
| Transport | UDP | TCP |
| Encryption | Password only | Full packet |
| Common use | Most enterprise SANs | Environments requiring audit of individual commands |

If the environment uses Cisco ISE or ClearPass as the AAA platform, check whether it supports TACACS+ for device administration (most do). Either is acceptable for Brocade switch authentication.

---

## Local Accounts

Local accounts are stored on the switch. They bypass RADIUS/TACACS+ and authenticate directly against the switch credential store.

### Manage Local Accounts

```bash
# List all local accounts and their roles
userconfig --show

# Create a local account with a specific role
userconfig --add <username> -r <role> -p <password>

# Modify an existing account's role
userconfig --change <username> -r <role>

# Delete a local account
userconfig --delete <username>

# Change a password
passwd <username>

# List available roles
roleconfig --show
```

### Built-in Roles

| Role | Capabilities |
|---|---|
| `admin` | Full switch and chassis access — all commands |
| `switchadmin` | Switch-level operations — port management, diagnostics, no security config |
| `fabricadmin` | Fabric-level operations — can manage all switches in fabric |
| `zoneadmin` | Zone management only — cannot change port config or security settings |
| `operator` | Read-only access — all show commands, no modifications |
| `user` | Minimal read access — very limited show commands |
| `securityadmin` | Security configuration only — certificates, IPfilter, policies |

### Break-Glass Account Standards

- The local `admin` account on every switch must have a strong, unique password stored in the enterprise vault.
- Break-glass accounts must not be used for day-to-day operations — all regular access via RADIUS/TACACS+.
- Break-glass password retrieval must be logged in the vault and reviewed quarterly.
- After any break-glass use, rotate the local admin password and update the vault entry.

---

## SSH Configuration

### SSH Key Management

```bash
# Show current SSH configuration and enabled services
sshutil --show

# Generate RSA host key (2048-bit minimum; 4096-bit recommended)
sshutil --genkey -t rsa

# Generate ECDSA host key (preferred on FOS 9.x)
sshutil --genkey -t ecdsa

# Import an authorized public key for key-based authentication
sshutil --add -user <username> -host <management-server-ip> -file /path/to/id_rsa.pub

# Show imported public keys
sshutil --show -user <username>
```

### Disabling Telnet

Telnet must be disabled on all production switches. Verify after every new switch deployment and firmware upgrade.

```bash
# Disable Telnet via configure
configure
# Navigate to: System Services → Telnet → enter 0 (disable)

# Verify Telnet is disabled
sshutil --show
# Expected: "telnetd" = disabled
```

---

## NTP Requirement

NTP synchronisation is mandatory for:

- Accurate log timestamps — required for security incident correlation
- Certificate-based authentication — certificates fail validation if the clock is wrong
- RADIUS authentication — some RADIUS servers enforce time-based token validation

```bash
# Configure NTP server (minimum two servers for redundancy)
tsclockserver "<ntp-server-1> <ntp-server-2>"

# Verify NTP synchronisation
tsclockserver              # Show configured NTP servers
date                       # Check current system time against expected

# Check NTP sync status (FOS 9.x)
ntpshow
```

NTP servers should be on the management network, reachable from the switch management IP. Use internal NTP stratum 2 servers — do not rely on public internet NTP from a SAN switch.

---

## Authentication Troubleshooting

| Symptom | Triage | Fix |
|---|---|---|
| RADIUS login fails for all users | `ping <radius-server-ip>` from switch | Verify network path; check RADIUS server is running |
| RADIUS login fails for one user | Test user account on RADIUS server directly | Check AD group membership; verify VSA attribute |
| Local fallback not working | `aaaconfig --show` — check order is `RADIUS;LOCAL` | Confirm `authorder` includes LOCAL |
| Account locked after failed attempts | Account lock threshold hit | Unlock via local console or another admin account |
| SSH connection refused | `sshutil --show` — SSH enabled? | Enable SSH; check IPfilter is not blocking port 22 |
| Certificate errors on SSH connection | Host key changed (after regen) | Clear known_hosts entry on management workstation |
| TACACS+ authentication slow | TCP connection timeout | Check TACACS+ server reachability; firewall rules on port 49 |
