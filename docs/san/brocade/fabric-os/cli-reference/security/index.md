# Security & Users

> Part of the Brocade Fabric OS CLI Reference.

## User Accounts

```bash
# List all user accounts
userConfig --show

# Change a user's password
passwd <username>

# Create a user
userConfig --add <username> -r <role> -l <chassis|switch>

# Delete a user
userConfig --delete <username>
```

## Roles

```bash
# List available roles
roleConfig --show
```

Built-in roles:
| Role | Permissions |
|---|---|
| admin | Full access |
| switchadmin | Switch-level operations |
| zoneadmin | Zone management only |
| fabricadmin | Fabric-wide read/write |
| operator | Read-only + basic operations |
| user | Read-only |

## Authentication (RADIUS / TACACS+)

```bash
# Show AAA configuration
aaaConfig --show

# Show auth settings
authUtil --show

# Configure RADIUS
aaaConfig --add <server_ip> -p <port> -s <secret> -t radius

# Configure TACACS+
aaaConfig --add <server_ip> -p <port> -s <secret> -t tacacs+

# Test authentication
authUtil --authenlogout
```

## Secure Fabric OS (SCC / DCC Policies)

```bash
# Show security policies
secPolicyShow
secPolicyShow "SCC_POLICY"    # Switch Connection Control — which switches can join fabric
secPolicyShow "DCC_POLICY"    # Device Connection Control — which WWNs can log in
```

## SSH Configuration

```bash
# Show SSH status
sshUtil --show

# Generate SSH host keys
sshUtil --genkey -t rsa
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Login fails | RADIUS/TACACS reachable | Check `aaaConfig --show`; test fallback to local |
| Account locked | Failed attempts | Reset via console or admin account |
| Unauthorized device joining | DCC policy | Review and restrict `DCC_POLICY` |
| SSH key error | Host key | Regenerate with `sshUtil --genkey` |
