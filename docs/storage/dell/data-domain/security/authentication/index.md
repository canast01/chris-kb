# Data Domain — Authentication

## LDAP and Active Directory

Data Domain supports LDAP/Active Directory for management authentication, avoiding local user sprawl.

```bash
# Configure LDAP
authentication ldap enable
authentication ldap set bind-dn "CN=svc-dd-ldap,OU=ServiceAccounts,DC=corp,DC=example,DC=com"
authentication ldap set server <ldap-server-ip>
authentication ldap set base-dn "DC=corp,DC=example,DC=com"

# Verify LDAP connectivity
authentication ldap status
authentication ldap test user <username>
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

## Disable Local Admin When LDAP Is Operational

```bash
# Disable local sysadmin login if LDAP is fully operational
# (Keep break-glass credentials documented in a secure vault)
adminaccess set admin-auth-method ldap

# Force all management access through LDAP groups
authentication roles assign role admin group <ad-group-storage-admins>
```

## Local Users

```bash
# List all local users
user list

# Add a local user
user add <username>

# Change a user's password
user change password <username>

# Delete a user
user del <username>
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
