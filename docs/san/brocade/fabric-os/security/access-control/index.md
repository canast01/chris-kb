# FabricOS — Access Control

> Part of the [Security](../) reference.

---

## Overview

Access control on Brocade FabricOS operates at two levels:

1. **Management plane** — who can log in to the switch CLI, web interface, or SNMP. Controlled via RBAC roles, IPfilter policies, and AAA configuration.
2. **Fabric plane** — which devices can join the fabric and which ports can talk to each other. Controlled via Secure Fabric OS policies (SCC, DCC) and zoning.

Both levels must be configured in production environments. Management plane access controls protect the switch operating system. Fabric plane access controls protect the SAN fabric topology and device connectivity.

---

## RBAC Roles

Role-Based Access Control restricts what each user can do after authentication. Roles are assigned per user (local accounts) or mapped from RADIUS/TACACS+ attributes.

| Role | Capabilities |
|---|---|
| `admin` | Full switch and chassis access — all commands, all configuration |
| `switchadmin` | Switch operations — port management, diagnostics, firmware (no security config) |
| `fabricadmin` | Fabric-wide operations — can operate all switches in the fabric |
| `zoneadmin` | Zone management only — zone create/modify/delete, cfgenable, cfgsave |
| `securityadmin` | Security configuration — certificates, IPfilter, DCC/SCC policies |
| `operator` | Read-only — all show commands; no modifications |
| `user` | Minimal read access — very limited show commands |

### Assign Roles to Local Accounts

```bash
# Create a user with a specific role
userconfig --add opsuser1 -r operator -p <password>
userconfig --add zoneeng1 -r zoneadmin -p <password>
userconfig --add sanadmin1 -r switchadmin -p <password>

# Modify a user's role
userconfig --change <username> -r <new-role>

# View all accounts and assigned roles
userconfig --show

# List all available roles
roleconfig --show
```

### Role Assignment Standards

| Team | Assigned Role | Justification |
|---|---|---|
| SAN engineering | `switchadmin` | Full switch operations excluding security config |
| Zone management team | `zoneadmin` | Zone changes without access to switch config |
| NOC / monitoring | `operator` | Read-only access for monitoring and triage |
| Security engineering | `securityadmin` | Certificate and policy management only |
| Break-glass (vault) | `admin` | Emergency full access — restricted to vault retrieval |

---

## IPfilter Policy

IPfilter restricts which source IP addresses or subnets can reach the switch management plane. This is the primary network-layer control for management access — even if an attacker has valid credentials, they cannot connect from an unauthorised source IP.

### Create and Apply an IPfilter Policy

```bash
# Create a new IPv4 IPfilter policy
ipfilter --create san_mgmt_policy -type ipv4

# Allow SSH from management subnet
ipfilter --addrule san_mgmt_policy \
  -sip 10.10.100.0/24 -dp 22 -proto tcp -act permit

# Allow HTTPS from management subnet
ipfilter --addrule san_mgmt_policy \
  -sip 10.10.100.0/24 -dp 443 -proto tcp -act permit

# Allow SNMP v3 from monitoring server only
ipfilter --addrule san_mgmt_policy \
  -sip 10.10.50.10/32 -dp 161 -proto udp -act permit

# Allow SNMP traps (outbound — no inbound rule needed)

# Allow NTP (switch initiates to NTP server — no inbound rule needed)

# Default-deny all other inbound traffic
ipfilter --addrule san_mgmt_policy \
  -sip 0.0.0.0/0 -dp 0 -proto any -act deny

# Save the policy (writes to persistent storage)
ipfilter --save san_mgmt_policy

# Activate the policy (takes effect immediately — verify SSH access before activating)
ipfilter --activate san_mgmt_policy

# Verify the active policy
ipfilter --show san_mgmt_policy
```

> **Warning:** Always verify your management workstation's source IP is in the permitted range before activating an IPfilter policy. An incorrect policy will lock you out of the switch — recovery requires console access.

### Modify an Existing IPfilter Policy

```bash
# Clone the active policy before modifying (safe approach)
ipfilter --clone san_mgmt_policy -name san_mgmt_policy_new

# Add a rule to the cloned policy
ipfilter --addrule san_mgmt_policy_new \
  -sip 10.10.200.0/24 -dp 22 -proto tcp -act permit

# Activate the updated policy
ipfilter --activate san_mgmt_policy_new

# Delete the old policy
ipfilter --delete san_mgmt_policy
```

### Show Current IPfilter State

```bash
# List all IPfilter policies
ipfilter --show

# Show rules in a specific policy
ipfilter --show san_mgmt_policy

# Show which policy is active
ipfilter --show -active
```

---

## Secure Fabric OS Policies

Secure Fabric OS provides fabric-plane access control — controlling which switches can join the fabric (SCC) and which devices can log in on specific ports (DCC).

### SCC Policy (Switch Connection Control)

SCC defines which switches are permitted to form ISLs and join the fabric. Any switch not in the SCC policy is rejected when it attempts to connect.

```bash
# Show current SCC policy
secpolicyshow "SCC_POLICY"

# Add a switch to the SCC policy (by switch WWN)
secpolicyadd "SCC_POLICY", "<switch-wwn>"

# Show all defined security policies
secpolicyshow

# Activate the security policy database
secpolicyactivate

# Save the security policy database
secpolicysave
```

### DCC Policy (Device Connection Control)

DCC restricts which device WWPNs are permitted to log into specific switch ports. This prevents unauthorised devices from connecting to the SAN fabric even if they have physical access to a switch port.

```bash
# Show current DCC policy
secpolicyshow "DCC_POLICY"

# Add a device WWPN to a specific port in the DCC policy
# Format: <device-wwpn> on port <domain_id>,<port>
secpolicyadd "DCC_POLICY", "<device-wwpn>;*"    # Allow on any port
secpolicyadd "DCC_POLICY", "<device-wwpn>;<domain-id>,<port>"   # Allow on specific port only

# Activate changes
secpolicyactivate
```

DCC is most valuable in high-security environments where physical port access cannot be fully controlled. For most enterprise SANs, zoning provides sufficient fabric-plane access control without the overhead of DCC management.

---

## Fabric Binding

Fabric binding prevents unauthorised switches from joining the fabric by requiring all member switches to be listed in the fabric binding list. It is enforced at the ISL level.

```bash
# Show fabric binding status
fabricbinding --show

# Show the list of permitted switches in the binding
fabricbinding --show -details

# Add a switch to the binding list
fabricbinding --add <switch-wwn>

# Enable fabric binding enforcement
fabricbinding --enable

# Verify
fabricbinding --show
```

---

## Access Control Standards

| Control | Standard | Verification |
|---|---|---|
| Management access role | `operator` minimum for NOC; `switchadmin` for SAN engineering | `userconfig --show` |
| Zone changes | `zoneadmin` role — separate from switch admin | `userconfig --show` |
| Break-glass account | `admin` role; stored in vault; not used in daily ops | Vault policy |
| IPfilter | Management subnet restriction on all production switches | `ipfilter --show` |
| SNMP | Read-only SNMP v3 for monitoring platforms | `snmpconfig --show` |
| Fabric binding | Enabled on all production fabrics | `fabricbinding --show` |

---

## Troubleshooting Access Control

| Symptom | Triage | Fix |
|---|---|---|
| User can log in but cannot run commands | Role too restrictive | `userconfig --show <username>` — adjust role |
| SSH refused from management workstation | IPfilter blocking source IP | `ipfilter --show` — add management IP to policy |
| New switch rejected when connecting ISL | Fabric binding or SCC policy | `secpolicyshow SCC_POLICY` — add switch WWN |
| Unauthorised device logged into fabric | DCC policy not enforced | Enable DCC policy; add authorised WWPNs |
| IPfilter locked out all access | Incorrect policy activated | Recover via console port; review and correct policy |
