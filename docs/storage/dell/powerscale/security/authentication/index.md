# PowerScale — Authentication

> SSO, LDAP, local accounts, and identity sources for Dell PowerScale.

## Overview

PowerScale access zones each have their own authentication providers. Supported identity sources include Active Directory, LDAP, NIS, and local OneFS accounts.

## Active Directory

```bash
# Join an Active Directory domain for an access zone
isi auth ads create --name EXAMPLE.COM --user Administrator --password <pw> --zone <zone-name>

# Verify AD join status
isi auth ads list --zone <zone-name>

# View AD provider details
isi auth providers ad view <provider_name>
```

- Use a dedicated service account for AD join; avoid domain admin credentials.
- For multi-protocol (NFS + SMB) environments, configure both AD (for Windows SIDs) and LDAP/NIS (for Unix UIDs/GIDs) on the same zone, and enable identity mapping.

## LDAP

```bash
# Add an LDAP provider for a zone
isi auth ldap create --name ldap-prod --server ldap://ldap.example.com \
  --base-dn "dc=example,dc=com" --zone <zone-name>

# List all auth providers for a zone
isi auth providers list --zone <zone-name>
```

## Local Accounts

```bash
# List local users
isi auth users list

# View a user
isi auth users view <username>

# Create a local user
isi auth users create --name <username> --password <password>

# Delete a local user
isi auth users delete <username>

# List local groups
isi auth groups list
isi auth groups view <group_name>
```

## Identity Mapping

```bash
# List identity mapping rules
isi auth mappings rules list
```
