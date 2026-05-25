# Jira — Authentication

Jira supports multiple authentication methods across its deployment models: Jira Software/Service Management Data Center (self-managed) and Jira Cloud. Authentication configuration is critical because Jira often contains sensitive project data, incident records, and change management workflows.

---

## Authentication Methods Overview

| Method | Jira Data Center | Jira Cloud | Strength |
|---|---|---|---|
| Local accounts | Yes | Yes | Low — avoid |
| LDAP / Active Directory | Yes | No | Medium |
| SAML 2.0 SSO | Yes | Yes (Atlassian Access) | High |
| OpenID Connect (OIDC) | Yes (via plugin) | Yes | High |
| API tokens | Yes | Yes | Medium-High |
| OAuth 2.0 (apps) | Yes | Yes | High |
| Atlassian Access (Cloud SSO) | No | Yes | High |
| Personal Access Tokens (Data Center) | Yes (v8.14+) | No | Medium-High |

---

## LDAP / Active Directory Integration (Data Center)

### Configuration Path

Administration → User Management → User Directories → Add Directory → Microsoft Active Directory

### Key Settings

| Setting | Recommended Value |
|---|---|
| LDAP URL | `ldaps://dc.corp.example.com:636` |
| Use SSL | Yes (LDAPS or StartTLS) |
| Base DN | `DC=corp,DC=example,DC=com` |
| User DN | `CN=jira-svc,OU=ServiceAccounts,DC=corp,DC=example,DC=com` |
| User Object Class | `person` |
| User Object Filter | `(&(objectClass=person)(memberOf=CN=Jira-Users,OU=Groups,...))` |
| Synchronisation | Every 60 minutes |
| Nested groups | Enable if using nested AD groups |

```xml
<!-- atlassian-user.xml snippet for LDAP (Data Center) -->
<directory type="com.atlassian.crowd.directory.ActiveDirectory">
  <attribute name="ldap.url" value="ldaps://dc.corp.example.com:636"/>
  <attribute name="ldap.userdn" value="CN=jira-svc,OU=ServiceAccounts,DC=corp,DC=example,DC=com"/>
  <attribute name="ldap.password" value="ENCRYPTED_PASSWORD"/>
  <attribute name="ldap.basedn" value="DC=corp,DC=example,DC=com"/>
  <attribute name="ldap.usersdn" value="OU=Users,DC=corp,DC=example,DC=com"/>
  <attribute name="ldap.groupsdn" value="OU=Groups,DC=corp,DC=example,DC=com"/>
  <attribute name="ldap.usessl" value="true"/>
</directory>
```

```bash
# Test LDAP connectivity from the Jira server
ldapsearch -H ldaps://dc.corp.example.com:636 \
  -D "CN=jira-svc,OU=ServiceAccounts,DC=corp,DC=example,DC=com" \
  -W \
  -b "DC=corp,DC=example,DC=com" \
  "(sAMAccountName=testuser)"
```

### Synchronisation and Failover

- Configure a secondary LDAP server for resilience.
- Set synchronisation interval to 60 minutes (reduce load on DC).
- Enable incremental sync using `uSNChanged` attribute for large directories.

---

## SAML 2.0 Single Sign-On

### Jira Data Center SAML Configuration

Administration → User Management → SAML 2.0 Single Sign-On

| Field | Value |
|---|---|
| IdP Entity ID | From IdP metadata (e.g., `https://sts.windows.net/{tenant-id}/`) |
| IdP SSO URL | `https://login.microsoftonline.com/{tenant-id}/saml2` |
| IdP certificate | X.509 certificate from IdP metadata |
| Attribute for username | `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name` |
| SP Entity ID | `https://jira.corp.example.com` |
| Assertion Consumer Service URL | `https://jira.corp.example.com/plugins/servlet/saml/auth` |

### Azure AD (Entra ID) Enterprise Application Setup

```yaml
1. Azure Portal → Enterprise Applications → New Application → Jira SAML SSO
2. Single sign-on → SAML
3. Basic SAML Configuration:
   - Identifier (Entity ID): https://jira.corp.example.com
   - Reply URL: https://jira.corp.example.com/plugins/servlet/saml/auth
   - Sign on URL: https://jira.corp.example.com
4. Attributes & Claims:
   - name: user.mail  (maps to Jira username)
   - displayName: user.displayname
   - groups: user.groups  (map to Jira groups)
5. Download Federation Metadata XML
6. Upload to Jira SAML configuration
```

### Enforcing SSO (Data Center)

```properties
# jira-config.properties — require SAML, disable local login
jira.saml.sso.loginpath.exclude=/rest/,/secure/Dashboard.jspa
jira.saml.sso.force=true
```

### Jira Cloud — Atlassian Access SAML

Requires Atlassian Access subscription:

1. admin.atlassian.com → Security → SAML single sign-on
2. Configure IdP with:
   - SP Entity ID: `https://auth.atlassian.com/saml/...`
   - ACS URL: Provided by Atlassian
3. Enforce SSO on the organisation domain
4. Enable **Authentication policies** → Assign all managed accounts to SSO policy

---

## API Tokens

### Jira Cloud — API Tokens

Users authenticate REST API calls with API tokens (not passwords).

```bash
# Generate at: https://id.atlassian.com/manage-profile/security/api-tokens

# Test API token authentication
curl -u "user@corp.example.com:API_TOKEN" \
  -H "Accept: application/json" \
  "https://your-org.atlassian.net/rest/api/3/myself"

# List Jira projects
curl -u "user@corp.example.com:API_TOKEN" \
  "https://your-org.atlassian.net/rest/api/3/project/search" | jq '.values[].key'
```

**API token controls (Atlassian Access):**
- admin.atlassian.com → Security → API token controls
- Block API tokens from unmanaged accounts
- Set token expiry policy

### Jira Data Center — Personal Access Tokens (v8.14+)

```bash
# Create a PAT via REST API
curl -u "admin:password" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://jira.corp.example.com/rest/pat/latest/tokens" \
  -d '{
    "name": "CI Pipeline Token",
    "expirationDuration": 90
  }'

# List all tokens for a user
curl -u "admin:password" \
  "https://jira.corp.example.com/rest/pat/latest/tokens"

# Revoke a token by ID
curl -u "admin:password" \
  -X DELETE \
  "https://jira.corp.example.com/rest/pat/latest/tokens/{tokenId}"
```

---

## Multi-Factor Authentication

### Jira Cloud (Atlassian Access)

Authentication policies enforce MFA:

1. admin.atlassian.com → Security → Authentication policies
2. Create policy → Two-step verification → Required
3. Assign to all managed accounts

Supported factors:

| Factor | Phishing Resistant | Recommended |
|---|---|---|
| Security key (FIDO2/WebAuthn) | Yes | Highest |
| Authenticator app (TOTP) | No | Standard |
| SMS | No | Avoid |

### Jira Data Center — MFA via Plugins

Data Center does not include native MFA. Use:

- **Duo Security for Atlassian** (marketplace plugin)
- **miniOrange MFA** (marketplace plugin)
- IdP-enforced MFA when using SAML SSO (preferred — no plugin needed)

---

## Session Management

### Session Security Settings (Data Center)

Administration → System → Security → Global Settings:

| Setting | Recommended Value |
|---|---|
| Session timeout | 8 hours (480 minutes) |
| Remember me | Disabled |
| Secure cookies | Enabled (HTTPS only) |
| Cookie domain | Specific domain only |

```xml
<!-- web.xml session configuration -->
<session-config>
  <session-timeout>480</session-timeout>
  <cookie-config>
    <http-only>true</http-only>
    <secure>true</secure>
  </cookie-config>
  <tracking-mode>COOKIE</tracking-mode>
</session-config>
```

---

## Service Account Standards

| Purpose | Naming Convention | AD Group | PAT Expiry |
|---|---|---|---|
| CI/CD read access | `svc-jira-ci-read` | `Jira-ServiceAccounts` | 30 days |
| CI/CD write access | `svc-jira-ci-write` | `Jira-ServiceAccounts` | 30 days |
| Monitoring | `svc-jira-monitor` | `Jira-ServiceAccounts` | 90 days |
| Integration | `svc-jira-<app>` | `Jira-Integrations` | 90 days |

- Service accounts must not have Jira Administrator rights.
- Rotate credentials on personnel change and on schedule.
- Audit last-used dates quarterly — disable accounts unused for 30 days.

---

## Related Pages

- [Jira — Access Control](../access-control/index.md)
- [Jira — Encryption](../encryption/index.md)
- [Jira — Hardening](../hardening/index.md)
