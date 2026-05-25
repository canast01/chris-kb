# Confluence — Authentication

SSO/SAML, LDAP/AD integration, local accounts, and two-factor authentication for Confluence Data Center and Server.

## Authentication Methods

Confluence supports several authentication mechanisms, and they can coexist. Order of precedence is: SSO > LDAP > local accounts.

| Method | Use Case | Configuration Location |
|---|---|---|
| SAML 2.0 SSO | Enterprise SSO via IdP (Okta, ADFS, Azure AD) | General Configuration > SAML Authentication |
| LDAP / Active Directory | Sync users and groups from AD | User Management > User Directories |
| Local accounts | Break-glass accounts, service accounts | User Management > Create User |
| Atlassian Access (Cloud) | Centralised SSO/SCIM for cloud | Atlassian Access admin console |

## SAML 2.0 SSO (Data Center)

SAML SSO delegates authentication to an external Identity Provider (IdP). Users are redirected to the IdP login page and return to Confluence with an assertion.

### Configuration Steps

1. Navigate to **General Configuration** > **SAML Authentication** (requires System Administrator role).
2. Set **Authentication** to **SAML 2.0**.
3. Download the **Confluence SP metadata** XML from the configuration page.
4. Import the SP metadata into your IdP (Okta, Azure AD, ADFS).
5. Copy the IdP's **Single Sign-On URL**, **Entity ID**, and **Certificate** back into Confluence.
6. Set **Name ID Format** to match your IdP's configuration (typically `urn:oasis:names:tc:SAML:2.0:nameid-format:emailAddress`).
7. Test with a non-admin user before enforcing SAML for all users.

### SAML Attribute Mapping

Confluence maps SAML attributes to user profile fields. Typical mapping:

| Confluence Field | SAML Attribute |
|---|---|
| Username | `uid` or `sAMAccountName` |
| Full name | `displayName` or `cn` |
| Email | `mail` or `emailAddress` |
| Groups | `memberOf` (used for group sync) |

### SAML Security Settings

```yaml
Recommended SAML configuration:
- Sign Authentication Requests: Enabled
- Require Signed Assertions: Enabled
- Require Signed Response: Enabled
- Signature Algorithm: RSA-SHA256 minimum
- Session timeout: Align with IdP session timeout (e.g., 8 hours for corporate SSO)
```

## LDAP / Active Directory Integration

LDAP integration syncs user accounts and group memberships from Active Directory without delegating authentication (users still authenticate through Confluence unless SSO is also enabled).

### Adding an LDAP Directory

1. Go to **User Management** > **User Directories** > **Add Directory** > **Microsoft Active Directory**.
2. Configure:

| Field | Example Value |
|---|---|
| Server | `dc01.example.local` |
| Port | 636 (LDAPS — preferred) or 389 (LDAP) |
| Use SSL | Yes (LDAPS) |
| Base DN | `DC=corp,DC=local` |
| Username DN | `CN=svc-confluence,OU=ServiceAccounts,DC=corp,DC=local` |
| Password | Service account password (from PAM vault) |
| User Search Base | `OU=Users,DC=corp,DC=local` |
| Group Search Base | `OU=Groups,DC=corp,DC=local` |

3. Configure **User Schema** settings to match your AD attribute names:
   - Username Attribute: `sAMAccountName`
   - Full Name Attribute: `displayName`
   - Email Attribute: `mail`
   - Group Member Attribute: `member`

4. Set **Synchronisation** interval (e.g., every 60 minutes).

### LDAP Security

```yaml
LDAP hardening:
- Always use LDAPS (port 636) — plain LDAP sends credentials in cleartext
- Use a dedicated read-only service account for the LDAP bind
- Service account: password managed in CyberArk/Vault, rotated every 90 days
- Restrict service account: Read-only access to the User and Group OUs only
- Import the AD CA certificate into Confluence's Java truststore for LDAPS verification
```

```bash
# Import AD CA cert into Confluence Java truststore (Linux server)
keytool -import -trustcacerts \
  -alias corp-ad-ca \
  -file /tmp/corp-root-ca.cer \
  -keystore /opt/atlassian/confluence/jre/lib/security/cacerts \
  -storepass changeit -noprompt

# Restart Confluence after importing
systemctl restart confluence
```

## Local Accounts

Local accounts should be limited to break-glass admin accounts and system integration accounts.

```yaml
Local account policy:
- Minimum: 3 local accounts (primary sysadmin, secondary sysadmin, monitoring service account)
- All local admin accounts: password managed in PAM vault
- Non-admin local accounts: not permitted; use LDAP/SSO for all regular users
- Review local accounts quarterly; disable unused accounts
```

### Managing Local Accounts

1. Go to **User Management** > **Users** > **Create User**.
2. Assign to the `confluence-administrators` or `confluence-users` group.
3. Set a strong random password; store in PAM vault.

```bash
# Audit local users via Confluence REST API
curl -u admin:password -H "Content-Type: application/json" \
  https://confluence.example.local/rest/api/user?type=known \
  | python3 -m json.tool | grep -E "username|userKey"
```

## Two-Factor Authentication (2FA)

### Confluence Data Center — Plugin-Based 2FA

Confluence Data Center does not include built-in TOTP 2FA; it requires a plugin or IdP-level enforcement.

**Recommended approach:** Enforce MFA at the IdP level (Okta, Azure AD, ADFS) before the SAML assertion reaches Confluence. This ensures all authentication paths require MFA.

**Plugins** (if direct Confluence 2FA is required):
- **Two Factor Authentication for Confluence** (Midori, marketplace)
- **Authenticator plugin** (various vendors)

### IdP-Level MFA Enforcement

When using SAML SSO, configure MFA at the IdP:

| IdP | MFA Configuration |
|---|---|
| Okta | Sign-On Policy > require MFA for Confluence app |
| Azure AD | Conditional Access Policy > require MFA for Confluence SAML app |
| ADFS | Authentication Policy > MFA required for Confluence relying party trust |

### TOTP Plugin Configuration

```text
Plugin configuration (Midori TOTP example):
1. Install plugin from Marketplace
2. Go to Administration > Two-Factor Authentication
3. Enforce 2FA for: All users / Administrators only (minimum: administrators)
4. Allow: TOTP apps (Google Authenticator, Authy)
5. Backup codes: Generate and store in PAM vault for each admin account
6. Grace period: 0 days (enforce immediately)
```

## Session Management

```yaml
Recommended session settings (General Configuration > Security Configuration):
- Maximum Authentication Attempts: 5 (then lock account for 30 minutes)
- Session Timeout: 480 minutes (8 hours) or match IdP session length
- Secure flag on cookies: Enabled (requires HTTPS)
- HttpOnly flag on cookies: Enabled (prevents JavaScript access)
- SameSite cookie attribute: Lax or Strict
- Remember Me: Disabled on shared/kiosk systems
```

## Authentication Audit

```bash
# View Confluence audit log (Data Center)
# Administration > Audit Log

# Or query via REST API
curl -u admin:password \
  "https://confluence.example.local/rest/api/audit?startDate=$(date -d '-7 days' +%Y-%m-%d)&limit=100" \
  | python3 -m json.tool | grep -E '"user"|"type"|"description"'

# Check failed login events in Confluence application log
grep -i "authentication failure\|invalid credentials\|failed login" \
  /var/atlassian/application-data/confluence/logs/atlassian-confluence.log | tail -50

# Check if any users are using local auth when SSO should be enforced
# In Confluence Admin: User Directories > review which directory each user authenticates against
```

## Quick Reference

| Topic | Location / Command |
|---|---|
| SAML configuration | General Configuration > SAML Authentication |
| LDAP directories | User Management > User Directories |
| Local users | User Management > Users |
| Session settings | General Configuration > Security Configuration |
| Audit log | Administration > Audit Log |
| LDAPS cert import | `keytool -import -keystore cacerts` |
| REST API users | `GET /rest/api/user?type=known` |
| Failed login check | `grep "authentication failure" atlassian-confluence.log` |
