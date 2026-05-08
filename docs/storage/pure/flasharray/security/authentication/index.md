# FlashArray — Authentication

> SSO, LDAP, local accounts, and identity sources.

## Active Directory (AD)

1. Join the FlashArray to AD: `puredirectoryservice setattr --base-dn <base_dn> --bind-user <user> --bind-password <pwd> --domain <domain> --uri ldaps://<dc_ip>`
2. Create admin groups in AD mapped to FlashArray roles (e.g., `purearray-admins` → `array_admin`)
3. Test AD login with a domain account before removing local accounts
4. Configure the group-to-role mapping: `pureadmin setattr --role array_admin --group <ad_group>`

## LDAP (non-AD)

- Configure LDAP URI, base DN, bind credentials, and user/group attribute mapping under Directory Service settings
- Supports OpenLDAP, Red Hat Directory Server, and similar LDAP providers

## SAML SSO

- Supported on Purity//FA 6.x and later
- Configure the FlashArray as a SAML Service Provider in your IdP (Okta, Azure AD, ADFS)
- Export the FlashArray SP metadata and import into the IdP
- Set `puredirectoryservice saml` configuration with IdP metadata URL and certificate

## Local Accounts

```bash
# Create a local admin account
pureadmin create --role storage_admin <username>

# Set password
pureadmin setattr <username> --password

# Disable / lock an account
pureadmin reset <username> --lockout

# List all accounts
pureadmin list
```

## Audit Logging

Purity//FA logs all administrative actions including logins, configuration changes, volume operations, and snapshot management.

**What is logged:**
- All CLI and GUI login/logout events (success and failure)
- All configuration changes with the admin account name and timestamp
- All data operations (volume create/delete/connect, snapshot create/delete, replication changes)
- API token creation and deletion
- Failed authentication attempts

```bash
# View audit log on the array
pureadmin list --audit

# Add a syslog server for external forwarding
puresyslog create --uri udp://<syslog_ip>:514 <syslog_name>

# TLS syslog
puresyslog create --uri tls://<syslog_ip>:6514 <syslog_name>

# List configured syslog destinations
puresyslog list
```
