# Veeam — Authentication

## Multi-Factor Authentication

For Veeam Backup Enterprise Manager (if deployed):
- Enable MFA under Settings → Users → configure TOTP or SAML provider
- Require MFA for all administrative accounts

## CyberArk Integration

VBR can retrieve infrastructure credentials from CyberArk at runtime:

1. VBR console → Credentials → Add → CyberArk
2. Configure CCP (Central Credential Provider) URL, application ID, and safe name
3. Credentials retrieved at job runtime — never stored in VBR config DB

---

## VBR Windows Authentication Modes

VBR supports three authentication modes for console and remote access:

| Mode | Description | Use Case |
|---|---|---|
| Local Windows | Accounts local to the VBR server OS | Standalone/lab deployments; avoid in production |
| Active Directory | Domain accounts authenticated via Kerberos/NTLM | Standard enterprise deployments |
| LDAP | Direct LDAP bind to a directory service (non-AD) | Cross-domain or non-Windows directory environments |

Configure the authentication mode in VBR console under **Users and Roles** → select the account type when granting access. AD group membership is supported — assign roles to AD security groups rather than individual accounts.

---

## Service Account Requirements

### Minimum Permissions for VBR Service Account

The VBR service account (`svc-veeam` or equivalent) requires the following:

| Scope | Permission | Notes |
|---|---|---|
| VBR server OS | Local Administrator | Required for VBR installation and service operation |
| vCenter | Veeam-defined privilege set | Use the Veeam vCenter role (assigned during setup wizard) |
| Proxy servers | Local Administrator | VBR deploys and manages proxy components |
| Repository servers | Local Administrator or share write | Needed to write backup files and manage extents |
| SQL Server (VBR config DB) | `db_owner` on VBR config DB | `sysadmin` only required during initial DB setup |
| Guest OS (application-aware) | Local Administrator on guest | For VSS quiescing and log truncation |

> Do not use a Domain Admin account as the VBR service account. Scope permissions to the minimum above.

---

## REST API Authentication

VBR exposes a REST API on port 9419 (HTTPS). Authentication uses OAuth 2.0 bearer tokens.

### Obtain a Token

```bash
# Request a bearer token (username/password exchange)
curl -s -X POST "https://<vbr-server>:9419/api/oauth2/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password&username=<user>&password=<pass>&use_short_term_refresh=false"
```

Response includes `access_token` and `refresh_token`.

### Use the Token

```bash
# Example: list all jobs
curl -s -X GET "https://<vbr-server>:9419/api/v1/jobs" \
  -H "Authorization: Bearer <access_token>"
```

### Token Expiry

| Token Type | Default Lifetime | Notes |
|---|---|---|
| Access token | 15 minutes | Passed in every API request header |
| Refresh token | 24 hours | Exchange for a new access token without re-authenticating |

Use `grant_type=refresh_token` with the refresh token to get a new access token before expiry. Automate token refresh in scripts to avoid mid-run failures.

---

## Backup Infrastructure Credentials Management

VBR stores credentials for managed infrastructure components (proxies, repositories, tape servers, etc.) in its configuration database.

### Managing Credentials

- VBR console → **Credentials** — central store for all managed account credentials
- Credentials are encrypted using the VBR configuration database encryption key
- Rotate passwords in **Credentials** first, then push changes to affected components

### Encryption Key Warning

> **Critical:** If the VBR configuration backup encryption key is lost, encrypted backups created with that key become permanently unrecoverable. There is no key escrow or recovery mechanism.

Best practices:

- Store the encryption password in a secrets manager (CyberArk, HashiCorp Vault) or a sealed, access-controlled document
- Enable **Encrypt configuration backup** under General Options and document the passphrase at the time of setup
- Test configuration restore annually — include the passphrase in your DR documentation

---

## Controls Summary

| Control | Configuration | Notes |
|---|---|---|
| MFA for Enterprise Manager | Settings → Users → TOTP or SAML | Required for all admin accounts |
| CyberArk credential retrieval | Credentials → Add → CyberArk; CCP URL + safe | Credentials never persisted in VBR DB |
| AD authentication | Users and Roles → assign AD groups | Prefer group assignment over individual accounts |
| VBR service account | Scoped local admin + vCenter role | No Domain Admin; use dedicated `svc-veeam` account |
| REST API token expiry | Access: 15 min / Refresh: 24 hr | Automate refresh in any scripted API consumers |
| Configuration backup encryption | General Options → Encrypt config backup | Store passphrase in secrets manager; test restore annually |
| Guest credential scope | Per-job credentials, local admin on guest | Limit to jobs requiring application-aware processing |
---

## Related Reference

- [Standard LDAP Integration](../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
