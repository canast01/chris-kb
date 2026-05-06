# Users & Security

> Part of the Dell Data Domain CLI Reference.

## Local Users

```bash
# List all local users
user list

# User detail (role, last login)
user show <username>

# Add a local user
user add <username>

# Change a user's password
user change password <username>

# Delete a user
user del <username>
```

## User Roles

| Role | Permissions |
|---|---|
| `admin` | Full administrative access |
| `user` | Limited — can view, change own password |
| `backup-operator` | DDBoost access; cannot manage system settings |
| `none` | Disabled account |

```bash
# Show available roles
user role show

# List all roles
role list

# Assign a role to a user
user modify <username> --role <role_name>
```

## Authentication Settings

```bash
# Show authentication configuration (local, LDAP, AD)
auth show

# Enable LDAP authentication
auth add ldap server <ldap_ip> bind-dn <dn> bind-password <pass> base-dn <base_dn>

# Enable Active Directory
auth add active-directory <domain>

# Test LDAP authentication
auth test ldap server <ldap_ip>
```

## Password Policy

```bash
# View password policy
user password-policy show

# Set minimum password length
user password-policy set min-length 12

# Set maximum password age (days)
user password-policy set max-age 90
```

## SSH Keys

```bash
# Show authorized SSH keys for a user
user ssh-keys show <username>

# Add an SSH public key
user ssh-keys add <username> key "<public_key_string>"

# Remove an SSH key
user ssh-keys del <username> key <key_id>
```

## Login and Session Management

```bash
# Active login sessions
user login show

# Terminate a specific session
user login terminate <session_id>
```

## Audit Log

```bash
# View authentication audit log
log view | grep -i "login\|auth\|failed"

# Export audit events
log dump system | grep -i auth
```
