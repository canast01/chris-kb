# Jira — Authentication


<div class="kb-summary">
Jira supports multiple authentication methods across its deployment models: Jira Software/Service Management Data Center (self-managed) and Jira Cloud.
</div>

 Authentication configuration is critical because Jira often contains sensitive project data, incident records, and change management workflows.

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
┌──────────────────────────────────────── Jira — Authentication ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  Jira Authentication Methods                                  │   │
│   │           LDAP: user/group sync from AD; Jira binds with user credentials for login           │   │
│   │          SAML SSO: Jira as SP; Okta/ADFS as IdP; signed assertion; no password stored         │   │
│   │              PAT: Personal Access Token; HTTP Bearer; profile-managed; revocable              │   │
│   │               Crowd: optional Atlassian SSO; centralises auth across DC products              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    SSO preferred for humans; PAT for automation; local break-glass for emergencies                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Human Auth                  │  │               Service/API Auth              │   │
│   │            SAML 2.0 SSO (primary)            │  │              PAT: Bearer token              │   │
│   │              LDAP bind fallback              │  │             Basic auth (legacy)             │   │
│   │             Crowd SSO (optional)             │  │                OAuth app link               │   │
│   │               MFA at IdP layer               │  │               Service account               │   │
│   │             Session: 30 min idle             │  │             API rate: via proxy             │   │
│   │              Local: break-glass              │  │              Scope: read/write              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LDAP/AD DCs · IdP (Okta/ADFS) with HA · Crowd server (optional) · Jira app VMs                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SAML 2.0     = federated SSO; Jira validates signed IdP XML assertion                                │
│  LDAP bind    = Jira binds to LDAP with user creds; auth happens at directory                         │
│  PAT          = Personal Access Token; Jira Profile > Personal Access Tokens                          │
│  Basic auth   = base64 user:pass; deprecated; disable in favour of PAT                                │
│  Crowd        = Atlassian SSO; issues Crowd token accepted by all linked products                     │
│  OAuth app link = OAuth 1.0a/2.0 for trusted Jira-to-Confluence API calls                             │
│  Break-glass  = local admin; used when LDAP/IdP is unreachable                                        │
│  Session      = idle timeout; Admin > Security > Session Configuration                                │
│  MFA          = enforced at IdP; Jira trusts SAML assertion without extra factor                      │
│  Service account = dedicated LDAP user for automation; prefer PAT instead                             │
│  Rate limiting = no native Jira rate limit; implement at reverse proxy (nginx)                        │
│  Assertion    = SAML XML signed by IdP; contains user attributes and groups                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text

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
---

## Related Reference

- [Standard LDAP Integration](../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
