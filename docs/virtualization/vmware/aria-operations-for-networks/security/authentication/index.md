# Aria Operations for Networks — Authentication

```text
┌──────────── Aria Networks Authentication: vIDM SSO Flow ───────────────────────┐
│                                                                                 │
│  Method 1: Local (break-glass)                                                  │
│  admin@local ──► password set during OVA deploy ──► Settings ► Change Pwd      │
│                                                                                 │
│  Method 2: LDAP / Active Directory                                              │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  Platform VM ──ldaps:636──► AD server                                   │   │
│  │  bind DN ► user search ► sAMAccountName match ► group lookup            │   │
│  │  Settings ► Role Mappings: AD group ──► vRNI role                       │   │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│  Method 3: SAML / vIDM (SSO)                                                   │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  User browser ──► vRNI SP ──► redirect ──► vIDM IdP                    │    │
│  │  vIDM authenticates ──► SAML assertion ──► vRNI role mapping            │   │
│  │  SP Metadata export ──► import into vIDM service provider               │   │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│  Method 4: API Token                                                            │
│  POST /api/ni/auth/token ──► bearer token (24h session or long-lived)          │
│  Header: Authorization: NetworkInsight <token>                                  │
└────────────────────────────────────────────────────────────────────────────────┘
```

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

---

## LDAP / Active Directory

```text
Settings → Authentication → LDAP → Configure

  Server URL:     ldaps://dc01.example.local:636
  Base DN:        DC=corp,DC=local
  Bind DN:        CN=svc-vrni,OU=ServiceAccounts,DC=corp,DC=local
  Bind Password:  <password>
  User Attribute: sAMAccountName
  Group Attribute: memberOf

  → Test Connection → "Connection successful"
  → Save
```

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
