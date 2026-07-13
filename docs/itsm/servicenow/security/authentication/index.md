---
tags:
  - security
  - servicenow
---
# ServiceNow Authentication

```javascript
// Test LDAP configuration from ServiceNow Script Editor
var ldap = new GlideLDAP();
var result = ldap.getGroups('username@corp.example.com');
gs.info('LDAP test result: ' + JSON.stringify(result));
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

```text title="Expected output"
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvYXV0aF9jbGllbnQiLCJpYXQiOjE3MDk4MTIzNDUsImV4cCI6MTcwOTgxNTk0NX0.a2F0dGFjYXQxMjM0NTY3ODk",
  "refresh_token": "refresh_token_9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c",
  "scope": "useragent",
  "token_type": "Bearer",
  "expires_in": 3600
}
{
  "result": [
    {
      "number": "INC0010234",
      "short_description": "Network connectivity issue",
      "state": "2",
      "priority": "3",
      "created_on": "2024-03-06 14:22:15"
    },
    {
      "number": "INC0010233",
      "short_description": "Password reset request",
      "state": "1",
      "priority": "4",
      "created_on": "2024-03-06 13:45:22"
    }
  ]
}
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvYXV0aF9jbGllbnQiLCJpYXQiOjE3MDk4MTI2NDUsImV4cCI6MTcwOTgxNjI0NX0.b3F1dGRhdGExMjM0NTY3ODk",
  "refresh_token": "refresh_token_8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b",
  "scope": "useragent",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `{"error":"invalid_client","error_description":"Client authentication failed"}` | Verify that `<CLIENT_ID>` and `<CLIENT_SECRET>` are correct and match the OAuth application registered in ServiceNow. |
    | `{"error":"invalid_grant","error_description":"Refresh token has expired"}` | Request a new access token using the client credentials flow instead, as refresh tokens expire after a configured period (typically 30–90 days). |
    | `{"error":"invalid_request","error_description":"Missing required parameter: grant_type"}` | Ensure all `-d` parameters are included and properly formatted; check that the Content-Type header is set to `application/x-www-form-urlencoded`. |
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

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "User / Service" as USR
participant "ServiceNow" as SVC
participant "Identity Provider\n(LDAP / OIDC / AD)" as IDP
participant "Token / Session Store" as TOKEN

USR -> SVC: Authentication request
SVC -> IDP: Validate credentials
IDP --> SVC: Identity confirmed
SVC -> TOKEN: Issue session token
TOKEN --> SVC: Token granted
SVC --> USR: Access allowed

@enduml
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Servicenow — Access Control](../access-control/)
- [Servicenow — Hardening](../hardening/)
- [Servicenow — Encryption](../encryption/)
