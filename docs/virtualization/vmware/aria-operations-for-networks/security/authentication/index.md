# Aria Operations for Networks — Authentication

---

## Authentication Methods

| Method | Description | Use Case |
|---|---|---|
| Local | Built-in admin@local | Initial setup, break-glass |
| LDAP / AD | AD group-to-role mapping | Standard enterprise |
| SAML / vIDM | Workspace ONE SSO | SSO environments |
| API Token | Bearer token for REST API | Automation, monitoring |

---

## Local Authentication

Default credential after OVA deployment: `admin@local` — password set during OVA wizard.

Password policy (Settings → Security):
- Minimum length: 12+ characters (increase from default 8)
- Complexity: uppercase, lowercase, number, special character
- Lockout: 5 failed attempts → 30-minute lockout

Change password:
```text
Settings → My Account → Change Password
```
┌───────────────────────────────────────── vRNI Authentication ─────────────────────────────────────────┐
│                                                                                                       │
│  Local, LDAP, vIDM SSO, and API token authentication methods for vRNI.                                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Local Authentication             │  │           LDAP / AD Authentication          │   │
│   │             admin@local account              │  │          Settings > Authentication          │   │
│   │          Set during OVA deployment           │  │            LDAP server + bind DN            │   │
│   │           Use only as break-glass            │  │           Base DN for user search           │   │
│   │          Rotate password regularly           │  │         Group mapping: Admin/Member         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Local is break-glass only; LDAP or vIDM SSO for normal operations; API token for scripts.            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                   vIDM SSO                   │  │                API Token Auth               │   │
│   │            Register vRNI in vIDM             │  │           POST /api/ni/auth/token           │   │
│   │           vIDM groups map to roles           │  │          Body: username + password          │   │
│   │           SAML2 redirect on login            │  │            Response: Bearer token           │   │
│   │            MFA enforced via vIDM             │  │         Token TTL: 24 hours default         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRNI platform VM; AD/LDAP server; vIDM appliance for SSO; PKI for LDAPS certs                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  admin@local         = Default local administrator; used as break-glass account                       │
│  LDAP Bind DN        = Service account DN vRNI uses to authenticate to directory                      │
│  Base DN             = Root of directory tree vRNI searches for user accounts                         │
│  Group Mapping       = Links AD group to vRNI Admin or Member role                                    │
│  vIDM                = VMware Identity Manager; provides SAML2 SSO for vRNI                           │
│  SAML2               = Security Assertion Markup Language; SSO federation protocol                    │
│  MFA                 = Multi-Factor Auth enforced at vIDM layer for all vRNI logins                   │
│  API Token           = Bearer token obtained via REST POST; used for script auth                      │
│  Token TTL           = Time-to-live for API token; default 24h; re-auth required                      │
│  Break-glass         = Emergency local account used when directory is unreachable                     │
│  LDAPS               = LDAP over TLS on port 636; required for secure directory auth                  │
│  SSO Redirect        = Browser redirected to vIDM login page on vRNI access                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

After LDAP is configured, add Role Mappings (Settings → Authentication → Role Mappings) to map AD groups to vRNI roles.

---

## SAML / VMware Identity Manager

```text
Settings → Authentication → SAML

  IdP Metadata URL: https://vidm.example.local/SAAS/API/1.0/GET/metadata/idp.xml
  SP Entity ID:     https://vrni.example.local  (auto-populated)
  NameID Format:    urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress

  Download SP Metadata → import into vIDM as Service Provider
```

Attribute mapping in vIDM:
- NameID → user email
- Groups attribute → AD groups synced to vIDM (map to vRNI roles)

---

## API Token Authentication

Create long-lived tokens in UI (Settings → API Tokens → Generate Token). Store in secrets manager — never hard-code.

```bash
# Session token (short-lived — for interactive scripting)
TOKEN=$(curl -sk -X POST \
  https://vrni.example.local/api/ni/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"<pass>","domain":{"domain_type":"LOCAL"}}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['token'])")

# Use token
curl -sk -H "Authorization: NetworkInsight $TOKEN" \
  "https://vrni.example.local/api/ni/data-sources/vcenters"
```

---

## Session Management

| Setting | Default | Recommended |
|---|---|---|
| Idle session timeout | 30 minutes | 15 minutes |
| Failed login lockout | 5 attempts | 5 attempts |
| Lockout duration | 30 minutes | 30 minutes |

Configure: Settings → Security → Session Timeout.

---

## LDAP Certificate Trust (LDAPS)

If using LDAPS (port 636), the LDAP CA certificate must be trusted by the Platform VM:

```bash
# SSH to Platform VM
ssh ubuntu@vrni.example.local

# Install CA certificate
sudo cp /tmp/corp-root-ca.crt /usr/local/share/ca-certificates/corp-root-ca.crt
sudo update-ca-certificates

# Restart vRNI after cert trust update
sudo systemctl restart hms
```

---

## Token Rotation Policy

| Token Type | Expiry | Rotation |
|---|---|---|
| Session tokens (API login) | 24 hours | Auto-expire |
| Long-lived API tokens | 90–365 days | Calendar reminder, revoke old on renewal |
| Service account tokens | 365 days | Rotate when personnel changes |

Review active tokens quarterly (Settings → API Tokens) and revoke any with no recent activity.
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
