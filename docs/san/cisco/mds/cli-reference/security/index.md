# Security & Users

> Part of the Cisco MDS NX-OS CLI Reference.

## Local Users

```bash
# Show all local users
show users

# Show defined roles
show role

# Create a local user
username <user> password <pass> role <role>

# Delete a user
no username <user>

# Assign admin role
username <user> role network-admin
```

## TACACS+ / RADIUS

```bash
# Show AAA config
show aaa

# Show TACACS+ servers
show tacacs-server

# Show RADIUS servers
show radius-server

# Configure TACACS+ server
tacacs-server host <ip> key <key>
aaa group server tacacs+ <group_name>
  server <ip>
aaa authentication login default group <group_name>
```

## SSH

```bash
# Show SSH server status
show ssh server

# Show SSH sessions
show users

# Generate RSA keys
crypto key generate rsa
show crypto key mypubkey rsa

# Restrict SSH access by source IP
ip access-list <acl_name>
  permit ip <mgmt_subnet> any
line vty 0 4
  access-class <acl_name> in
```

## SNMPv3

```bash
# Show SNMP community/user config
show snmp user
show snmp community

# Create SNMPv3 user
snmp-server user <user> <group> v3 auth sha <auth_pass> priv aes 128 <priv_pass>
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Login fails | Local account or TACACS reachability | Check `show tacacs-server`; test locally |
| SSH key error | Key mismatch | Regenerate: `crypto key generate rsa` |
| AAA lockout | TACACS down | Ensure local fallback: `aaa authentication login default group tacacs+ local` |
| Unauthorized access | Role config | Audit `show role`; remove unnecessary accounts |
