# Aria Operations — Authentication

```
┌─────────────────────────────────────────────────────────────┐
│          Aria Operations Authentication Flow                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌───────────┐  ┌────────────────┐  ┌────────────────────┐  │
│  │  Local    │  │  VIDM / SAML   │  │  LDAP / AD         │  │
│  │  (admin)  │  │  SSO           │  │  LDAPS :636        │  │
│  └─────┬─────┘  └───────┬────────┘  └──────────┬─────────┘  │
│        └────────────────┼───────────────────────┘           │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Aria Operations Authentication Service              │   │
│  │  POST /suite-api/api/auth/token/acquire              │   │
│  │  → returns Bearer token (valid 30 min)               │   │
│  └──────────────────────────┬───────────────────────────┘   │
│                             │                               │
│                             ▼                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Role Mapping                                        │   │
│  │  AD Group → Imported to Aria Ops → Role assigned     │   │
│  │  Administrator / Content Admin / Operator / ReadOnly │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  Token expiry: 30 min  ·  LDAP sync: every 60 min           │
└─────────────────────────────────────────────────────────────┘
```

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

```
Administration → Authentication Sources → Add Source
```

Provide:
- **Source Type**: Active Directory
- **Display Name**: `corp.local`
- **Base DN**: `DC=corp,DC=local`
- **Bind User**: `CN=svc-vrops-ldap,OU=Service Accounts,DC=corp,DC=local`
- **Bind Password**: service account password
- **Host**: domain controller FQDN or IP (use multiple for HA)
- **Port**: 636 (LDAPS — required for production) or 389 (LDAP — lab only)
- **Use SSL**: Yes (LDAPS) — import the domain CA certificate into Aria Operations trust store first

```bash
# Import domain CA certificate into Aria Operations trust store
# Via UI: Administration → Certificates → Import Certificate → paste CA PEM
```

**Test the LDAP connection:**

```
Administration → Authentication Sources → select source → Test
```

Expected result: "Connection successful — X users found."

---

## LDAP Group Import and Role Assignment

After adding the AD source, import groups to assign roles:

```
Administration → Access Control → User Groups → Import Groups from Source
```

Search for the group name (e.g., `GG-VROPS-Admins`) → select → Import.

Assign a role to the imported group:

```
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

```
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
