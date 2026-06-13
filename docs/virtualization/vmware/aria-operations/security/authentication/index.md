---
tags:
  - aria-operations
  - security
  - vmware
---
# Aria Operations — Authentication


<div class="kb-summary">
Authentication reference covering Authentication Sources, Configuring Active Directory / LDAP, LDAP Group Import and Role Assignment, Workspace ONE Access (VIDM) / SAML Integration, API Authentication and 3 more sections.

*Applies to: Aria Ops 8.x*
</div>

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Authentication Sources

Aria Operations supports multiple authentication sources. Users can authenticate against any configured source.

| Source | Type | Use Case |
|---|---|---|
| **Local** | Built-in user accounts | Break-glass admin, lab environments |
| **Active Directory** | LDAP/LDAPS | Primary enterprise authentication |
| **OpenLDAP** | LDAP | Non-AD LDAP directories |
| **Workspace ONE Access (VIDM)** | SAML 2.0 | SSO integration with LCM-deployed environments |

---

## Configuring Active Directory / LDAP

**Via UI:**

```text
┌─────────────────────────────────── Aria Operations Authentication ────────────────────────────────────┐
│                                                                                                       │
│  Local, AD/LDAP, vIDM SSO, and API token authentication for Aria Operations (vROps).                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Local Authentication             │  │           LDAP / AD Authentication          │   │
│   │          admin@local: set at deploy          │  │            Admin > Access Control           │   │
│   │             Break-glass use only             │  │              Add LDAP/AD source             │   │
│   │           Rotate password 90 days            │  │          Import AD groups to roles          │   │
│   │             Keep creds in vault              │  │          LDAPS (port 636) required          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Local is break-glass; LDAP/vIDM for all users; API token for automation.                             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           vIDM SSO Authentication            │  │                API Token Auth               │   │
│   │            Register vROps in vIDM            │  │        POST /suite-api/api/auth/token       │   │
│   │           vIDM groups map to roles           │  │             Returns Bearer token            │   │
│   │           SAML2 redirect on login            │  │         Use in Authorization header         │   │
│   │             MFA enforced at vIDM             │  │           Refresh on token expiry           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps cluster; AD/LDAP server; vIDM appliance for SSO; PKI for LDAPS certs                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  admin@local         = Built-in local admin; set during OVA wizard; break-glass only                  │
│  LDAP Source         = Directory server added in vROps Access Control settings                        │
│  LDAPS               = LDAP over TLS port 636; required for secure auth in vROps                      │
│  AD Group Import     = Pull AD group into vROps to assign a role                                      │
│  vIDM Registration   = Add vROps as an app in vIDM for SAML SSO                                       │
│  SAML2               = Authentication protocol for SSO between vIDM and vROps                         │
│  MFA                 = Multi-Factor Auth enforced at vIDM layer; not in vROps itself                  │
│  Bearer Token        = Temporary API credential; set in Authorization: Bearer header                  │
│  Token Expiry        = Default 24h; automate refresh in scripts on 401 response                       │
│  Break-glass         = Local admin used when AD/vIDM is unreachable                                   │
│  Password Vault      = Secrets manager storing local admin credential securely                        │
│  Bind Account        = Service account for LDAP queries; read-only, dedicated                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Expected result: "Connection successful — X users found."

---

## LDAP Group Import and Role Assignment

After adding the AD source, import groups to assign roles:

```text
Administration → Access Control → User Groups → Import Groups from Source
```

Search for the group name (e.g., `GG-VROPS-Admins`) → select → Import.

Assign a role to the imported group:

```text
Administration → Access Control → User Groups → select group → Assign Role → select role
```

| AD Group | Aria Operations Role |
|---|---|
| `GG-VROPS-Admins` | Administrator |
| `GG-VROPS-ContentAdmins` | Content Admin |
| `GG-VROPS-Operators` | Operator |
| `GG-VROPS-ReadOnly` | Read Only |

---

## Workspace ONE Access (VIDM) / SAML Integration

When Aria Operations is deployed and managed by LCM, VIDM is automatically registered as the SSO provider. For standalone deployments:

```text
Administration → Global Settings → Authentication → Enable SSO → Configure VIDM
```

Provide:
- VIDM FQDN
- Admin credentials for VIDM registration

After configuration, the Aria Operations login page shows "Log in with VMware Identity Manager." AD users authenticated via VIDM can be assigned Aria Operations roles by importing VIDM groups.

---

## API Authentication

The Aria Operations REST API supports two authentication methods:

**Token-based (preferred):**

```bash
# Acquire a token — valid for 30 minutes
TOKEN=$(curl -sk -X POST \
  "https://vrops-prod-01.example.local/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>","authSource":"Local"}' | \
  jq -r '.token')

# Use token in subsequent API calls
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/adapterkinds"
```

**Basic authentication (scripts and monitoring):**

```bash
curl -sk -u 'admin:<password>' \
  "https://vrops-prod-01.example.local/suite-api/api/alertdefinitions" | jq '.'
```

For AD-authenticated API calls, include `authSource`:

```bash
TOKEN=$(curl -sk -X POST \
  "https://vrops-prod-01.example.local/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d '{"username":"svc.vrops@corp.local","password":"<password>","authSource":"corp.local"}' | \
  jq -r '.token')
```

---

## Token Expiry and Rotation

Tokens expire after 30 minutes. Scripts that run longer must re-authenticate or keep a token-renewal loop:

```bash
#!/usr/bin/env bash
# Re-authenticate function for long-running scripts
get_token() {
  curl -sk -X POST "https://vrops-prod-01.example.local/suite-api/api/auth/token/acquire" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"$VROPS_USER\",\"password\":\"$VROPS_PASS\",\"authSource\":\"Local\"}" | \
    jq -r '.token'
}

TOKEN=$(get_token)
TOKEN_AGE=0

while [[ ... ]]; do
  TOKEN_AGE=$((TOKEN_AGE + 1))
  if [[ $TOKEN_AGE -ge 25 ]]; then  # renew before 30-minute expiry
    TOKEN=$(get_token)
    TOKEN_AGE=0
  fi
  # ... script body using $TOKEN
  sleep 60
done
```

---

## Session Management

| Setting | Default | Location |
|---|---|---|
| Session timeout (UI) | 30 minutes inactivity | Global Settings → Authentication |
| Token lifetime (API) | 30 minutes | Not configurable |
| LDAP sync interval | 60 minutes | Authentication Sources → Edit → Sync Interval |
| Failed login lockout | No lockout (local) | Enforced at AD level for LDAP users |
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
