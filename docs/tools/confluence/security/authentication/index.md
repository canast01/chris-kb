# Confluence — Authentication


<div class="kb-summary">
SSO/SAML, LDAP/AD integration, local accounts, and two-factor authentication for Confluence Data Center and Server.
</div>

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
┌───────────────────────────────────── Confluence — Authentication ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               Confluence Authentication Methods                               │   │
│   │           LDAP: user/group sync from AD/OpenLDAP; Confluence handles credential bind          │   │
│   │    SAML SSO: Confluence as SP; IdP (Okta/ADFS) issues signed assertion; no password stored    │   │
│   │        Crowd: Atlassian SSO server; centralized auth across Confluence, Jira, Bitbucket       │   │
│   │         PAT: Personal Access Token; HTTP Bearer header; scoped; revocable via profile         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Multiple auth methods serve different user types; SSO preferred for all human login                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Human Auth Methods              │  │               Service/API Auth              │   │
│   │            SAML 2.0 SSO (primary)            │  │              PAT: Bearer token              │   │
│   │              LDAP bind fallback              │  │             Basic auth (legacy)             │   │
│   │            Crowd SSO (DC option)             │  │                OAuth app link               │   │
│   │               MFA at IdP layer               │  │               Service account               │   │
│   │             Session: 30 min idle             │  │              API rate limiting              │   │
│   │          Local account: break-glass          │  │              Scope: read/write              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LDAP/AD DCs · IdP (Okta/ADFS) with HA · Crowd server (if used) · Confluence app VMs                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SAML 2.0     = federated SSO standard; Confluence validates IdP-signed XML assertion                 │
│  LDAP bind    = Confluence authenticates user by binding to LDAP with their credentials               │
│  Crowd        = Atlassian identity server; issues Crowd SSO token shared across products              │
│  PAT          = Personal Access Token; created in Confluence profile; used as Bearer token            │
│  Basic auth   = Base64-encoded user:pass in Authorization header; deprecated; use PAT                 │
│  OAuth app link = OAuth 1.0a/2.0 trust between Confluence and Jira for macros/API                     │
│  Break-glass  = local admin account used when IdP/LDAP is unavailable                                 │
│  Session timeout = idle session expiry; set in Admin > Security Configuration                         │
│  MFA          = second factor enforced at IdP; Confluence receives only the SAML assertion            │
│  Service account = dedicated LDAP account for automation; PAT preferred for API                       │
│  Rate limiting = Confluence REST API: no native limit; rely on reverse proxy throttling               │
│  Assertion    = SAML XML document signed by IdP containing user identity and attributes               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
---

## Related Reference

- [Standard LDAP Integration](../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
