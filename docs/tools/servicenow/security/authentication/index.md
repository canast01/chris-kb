# ServiceNow Authentication

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
```javascript
// System Properties → glide.authenticate.sso.required = true
// Prevents local login bypass — set after SSO is confirmed working

gs.getProperty('glide.authenticate.sso.required')  // Returns 'true' if enforced
```
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
