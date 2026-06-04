# Jira — Authentication

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
```text
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
```properties
# jira-config.properties — require SAML, disable local login
jira.saml.sso.loginpath.exclude=/rest/,/secure/Dashboard.jspa
jira.saml.sso.force=true
```
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
