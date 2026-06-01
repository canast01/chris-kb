# ServiceNow — Authentication


<div class="kb-summary">
ServiceNow authentication covers how users, administrators, and integrations prove identity before accessing the platform. ServiceNow supports local accounts, LDAP, SAML 2.0 SSO, OAuth 2.0, and MFA through multiple providers.
</div>

---

## Authentication Methods Overview

| Method | Scope | Strength | Notes |
|---|---|---|---|
| Local accounts | All users | Low | Avoid for regular users |
| LDAP / Active Directory | Users | Medium | Sync only — authentication via LDAP bind |
| SAML 2.0 SSO | Users | High | Preferred for enterprise |
| OAuth 2.0 | Integrations | High | For REST API access |
| Basic authentication | REST API | Low | Deprecated — disable |
| Mutual TLS (mTLS) | Integrations | Very High | Certificate-based API auth |
| MID Server account | MID Server | Medium | Service account with limited rights |

---

## LDAP Integration

ServiceNow LDAP is used for user provisioning and group synchronisation. Authentication is handled by the LDAP server via bind operations.

### LDAP Configuration

Navigate to: System Security → LDAP → LDAP Servers

| Field | Recommended Value |
|---|---|
| Name | `Corporate AD` |
| Server URL | `ldaps://dc.corp.example.com:636` |
| Use SSL | Yes |
| User name | `CN=snow-svc,OU=ServiceAccounts,DC=corp,DC=example,DC=com` |
| Password | Stored in ServiceNow credential store |
| Base DN | `DC=corp,DC=example,DC=com` |
| Search Scope | Subtree |
| User record search attribute | `sAMAccountName` |
| User object class | `person` |
| User object filter | `(&(objectClass=person)(memberOf=CN=SNOW-Users,...))` |

```javascript
// Test LDAP configuration from ServiceNow Script Editor
var ldap = new GlideLDAP();
var result = ldap.getGroups('username@corp.example.com');
gs.info('LDAP test result: ' + JSON.stringify(result));
```
```text
┌────────────────────────────────────── ServiceNow Authentication ──────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐                                                    │
│   │                 SSO Methods                  │                                                    │
│   │          SAML 2.0 (Okta/ADFS/Azure)          │                                                    │
│   │               OIDC / OAuth 2.0               │                                                    │
│   │              Multi-provider SSO              │                                                    │
│   │          Just-in-time provisioning           │                                                    │
│   └──────────────────────────────────────────────┘                                                    │
│                                                     ┌─────────────────────────────────────────────┐   │
│                                                     │                 MFA Options                 │   │
│                                                     │            TOTP authenticator app           │   │
│                                                     │           Push notification (Duo)           │   │
│                                                     │              SMS OTP (fallback)             │   │
│                                                     │              Hardware FIDO2 key             │   │
│                                                     └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            Local Authentication (break-glass only)                            │   │
│   │                      Local admin account: used only when IdP unavailable                      │   │
│   │                    Password policy: 16+ chars, complexity, 90-day rotation                    │   │
│   │                       Failed login lockout: 5 attempts → 30-min lockout                       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  IdP servers (Okta/ADFS/Azure AD) · RADIUS/LDAP · ServiceNow SaaS                                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SAML 2.0   = XML-based SSO protocol; IdP asserts identity; SP trusts assertion                       │
│  OIDC       = OpenID Connect; JSON-based identity layer on OAuth 2.0                                  │
│  JIT        = Just-In-Time provisioning; creates user on first SSO login                              │
│  MFA        = Multi-Factor Authentication; requires second factor after password                      │
│  TOTP       = Time-based One-Time Password; 6-digit code from authenticator app                       │
│  FIDO2      = hardware security key standard; phishing-resistant authentication                       │
│  Break-glass= emergency local account; used only when SSO/IdP is unavailable                          │
│  IdP        = Identity Provider; Okta, Azure AD, or ADFS asserting user identity                      │
│  SP         = Service Provider; ServiceNow instance trusting the IdP assertion                        │
│  OAuth 2.0  = authorisation framework; used by OIDC and REST API integrations                         │
│  Lockout    = account locked after N failed attempts; prevents brute-force                            │
│  Duo        = MFA provider; push notification to mobile app for approval                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text

### ServiceNow IdP Configuration

```javascript
// Script: Map SAML groups to ServiceNow roles
// In the Identity Provider config → User Provisioning
// Group attribute name: groups
// Group sync: enabled

// Map specific groups to roles
var groupMappings = {
  "CN=SNOW-Admins,OU=Groups,...": "admin",
  "CN=SNOW-ITSM,OU=Groups,...": "itil",
  "CN=SNOW-CSM,OU=Groups,...": "sn_customerservice_agent",
  "CN=SNOW-ReadOnly,OU=Groups,...": "report_admin"
};
```

### Enforcing SSO

```javascript
// System Properties → glide.authenticate.sso.required = true
// Prevents local login bypass — set after SSO is confirmed working

gs.getProperty('glide.authenticate.sso.required')  // Returns 'true' if enforced
```

**Test SSO before enforcing:**
- Create a break-glass local account first
- Test with a non-admin account
- Verify group mappings work correctly
- Then set `glide.authenticate.sso.required = true`

---

## OAuth 2.0 for REST API Access

OAuth 2.0 is used for integration authentication (REST API calls from external systems).

### Creating an OAuth Application Registry

Navigate to: System OAuth → Application Registry → New → Create an OAuth API endpoint for external clients

| Field | Value |
|---|---|
| Name | `CMDB Sync Integration` |
| Client ID | Auto-generated |
| Client Secret | Auto-generated (store securely) |
| Redirect URL | `https://integration.corp.example.com/callback` |
| Active | Yes |
| Refresh Token Lifespan | 8,640,000 seconds (100 days) |
| Access Token Lifespan | 1,800 seconds (30 minutes) |

```bash
# Obtain an OAuth token (client credentials flow)
curl -X POST \
  "https://<instance>.service-now.com/oauth_token.do" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=<CLIENT_ID>" \
  -d "client_secret=<CLIENT_SECRET>"

# Use the access token
curl -X GET \
  "https://<instance>.service-now.com/api/now/table/incident?sysparm_limit=10" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Accept: application/json"

# Refresh an expired token
curl -X POST \
  "https://<instance>.service-now.com/oauth_token.do" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "client_id=<CLIENT_ID>" \
  -d "client_secret=<CLIENT_SECRET>" \
  -d "refresh_token=<REFRESH_TOKEN>"
```

### Mutual TLS (mTLS) for High-Assurance Integrations

```bash
# Configure client certificate on ServiceNow integration endpoint
# System Web Services → REST Message → (your integration)
# Authentication type: Mutual Authentication
# Certificate: Upload client certificate (PEM format)

# Test with curl
curl -X GET \
  "https://<instance>.service-now.com/api/now/table/cmdb_ci" \
  --cert /path/to/client.crt \
  --key /path/to/client.key \
  --cacert /path/to/ca.crt \
  -H "Accept: application/json"
```

---

## Multi-Factor Authentication

### Native MFA (ServiceNow)

System Security → Multi-Factor Authentication

| Factor | Configuration |
|---|---|
| Email OTP | Built-in — sends OTP to registered email |
| TOTP authenticator | Built-in — generates QR code for authenticator app |
| Duo Security | Plugin: com.snc.two_factor_authentication.duo |
| Microsoft Authenticator | Via Azure AD Conditional Access + SAML |

**MFA enforcement by user type:**

| User Type | MFA Required | Method |
|---|---|---|
| All users | Yes | Via IdP (Azure AD Conditional Access) |
| Admin users | Yes | Hardware key preferred |
| Service accounts | No MFA | OAuth 2.0 / mTLS instead |
| Break-glass accounts | Yes | TOTP stored in Vault |

### Enforcing MFA via Azure AD Conditional Access

```text
Azure AD → Security → Conditional Access → New Policy
Name: "Require MFA for ServiceNow"
Assignments:
  Users: All users / SNOW-Users group
  Cloud apps: ServiceNow (your Enterprise App)
Access controls:
  Grant access
  Require multi-factor authentication
  Require compliant device (optional)
Session:
  Sign-in frequency: 8 hours (re-prompt for long sessions)
```

---

## Session Management

| Setting | Property | Recommended Value |
|---|---|---|
| Session timeout | `glide.ui.session_timeout` | 480 (8 hours) |
| Idle timeout | `glide.ui.session.idle_timeout` | 30 (minutes) |
| Concurrent sessions | `glide.authenticate.multisession` | false |
| Cookie secure flag | `glide.cookies.secure` | true |
| Cookie HttpOnly | `glide.cookies.httponly` | true |
| Remember me | `glide.ui.login_persist` | false |

```javascript
// Verify session properties via Script Editor
var props = [
  'glide.ui.session_timeout',
  'glide.ui.session.idle_timeout',
  'glide.cookies.secure',
  'glide.cookies.httponly'
];
props.forEach(function(p) {
  gs.info(p + ': ' + gs.getProperty(p));
});
```

---

## Service Account Standards

| Account | Purpose | Auth Method | Password Rotation |
|---|---|---|---|
| `svc-snow-cmdb` | CMDB sync from discovery | OAuth 2.0 | Token: 30 days |
| `svc-snow-monitoring` | Read-only metrics | OAuth 2.0 | Token: 90 days |
| `svc-snow-ldap` | LDAP bind account | Basic (LDAP) | 90 days |
| `svc-snow-mid` | MID Server identity | Local + cert | 90 days |
| `snow-breakglass` | Emergency admin access | Local + TOTP | 90 days |

- Service accounts must never use interactive SAML SSO login.
- Credentials stored in CyberArk / HashiCorp Vault — never in scripts.
- All service account activity logged and reviewed monthly.

---

## Related Pages

- [ServiceNow — Access Control](../access-control/index.md)
- [ServiceNow — Encryption](../encryption/index.md)
- [ServiceNow — Hardening](../hardening/index.md)
---

## Related Reference

- [Standard LDAP Integration](../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
