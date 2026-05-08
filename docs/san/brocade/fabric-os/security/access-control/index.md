# FabricOS — Access Control

> Part of the [Security](../) reference.

---

## RBAC Roles

| Role | Access |
|---|---|
| admin | Full switch access — config, firmware, certificates |
| switchadmin | Switch operations — port management, diagnostics |
| zoneadmin | Zoning changes only — cannot modify switch config |
| fabricadmin | Fabric-level operations |
| operator | Read-only — show commands only |
| user | Very limited view access |

```bash
# Assign a role to a local user
userconfig --add <username> -r zoneadmin -p <password>

# View current user accounts and roles
userconfig --show

# List available roles
roleConfig --show
```

---

## IPfilter Policy

IPfilter restricts which source IP addresses can connect to the switch management plane.

```bash
# Create an IPfilter policy
ipfilter --create mgmt_policy -type ipv4

# Add rules to allow management subnet only
ipfilter --addrule mgmt_policy -sip <mgmt-subnet>/<prefix> -dp 22 -proto tcp -act permit    # SSH
ipfilter --addrule mgmt_policy -sip <mgmt-subnet>/<prefix> -dp 443 -proto tcp -act permit   # HTTPS
ipfilter --addrule mgmt_policy -sip <snmp-server-ip>/32 -dp 161 -proto udp -act permit      # SNMP
ipfilter --addrule mgmt_policy -sip 0.0.0.0/0 -dp 0 -proto any -act deny                   # Default deny

# Save and activate the policy
ipfilter --save mgmt_policy
ipfilter --activate mgmt_policy

# Verify
ipfilter --show mgmt_policy
```

---

## Secure Fabric OS Policies

```bash
secPolicyShow
secPolicyShow "SCC_POLICY"    # Switch Connection Control — which switches can join fabric
secPolicyShow "DCC_POLICY"    # Device Connection Control — which WWNs can log in
```

---

## Access Control Standards

- `switchadmin` role for ops, `zoneadmin` for zoning-only changes
- Management plane access restricted to approved management subnet via IPfilter
- SNMP v3 configured; default community strings removed
