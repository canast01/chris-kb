# Aria Suite Lifecycle — Authentication

```text
  LCM Authentication Architecture
┌─────────────────────────────────────────────────────────────────┐
│  Interactive Users                                              │
│  Browser → LCM UI → VIDM (SAML redirect) → AD/LDAP              │
│               └──────────────────────────────► LCM session      │
│                                                                 │
│  API / Scripts                                                  │
│  POST /lcm/authz/api/v2/login (admin@local or svc acct)         │
│    → Bearer token (30 min TTL) → use in x-xenon-auth-token hdr  │
│                                                                 │
│  VIDM Integration                                               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ VIDM ── LDAPS 636 ──► AD (group sync every 60 min)      │    │
│  │ LCM → Settings → Identity Manager → register VIDM FQDN  │    │
│  │ AD groups mapped to LCM roles via Settings → Access Ctrl │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Local accounts (break-glass only):                             │
│  admin@local (UI/API) │ root (SSH) │ admin (limited shell)      │
└─────────────────────────────────────────────────────────────────┘
```

## Authentication Architecture

LCM uses **Workspace ONE Access (VIDM)** as the primary identity provider for web UI and API access. A local `admin` account exists as a break-glass fallback and for initial setup before VIDM is registered.

```text
Browser → LCM UI → VIDM (SAML/OAuth2 redirect) → AD/LDAP → LCM session token
API clients → LCM /lcm/authz/api/v2/login → Basic auth → Bearer token
```

---

## Workspace ONE Access Integration

All interactive users should authenticate through VIDM. VIDM can be federated with Active Directory, LDAP, or upstream SAML identity providers.

**Register VIDM with LCM:**

```text
LCM → Settings → Identity Manager → Configure
```

Provide:
- VIDM FQDN (must be resolvable from LCM)
- VIDM admin credentials
- Accept the VIDM SSL certificate (or ensure it is trusted by the LCM appliance trust store)

Verify VIDM connectivity from LCM:

```bash
ssh admin@lcm-prod-01.example.local
curl -sk https://vidm.example.local/SAAS/API/1.0/REST/system/health
# Expected: {"status": "UP"}
```

After registration, the LCM login page shows a "Log In with Workspace ONE" button that redirects to VIDM for authentication.

---

## Active Directory Group Sync via VIDM

LCM does not connect to AD directly. AD group membership is resolved through VIDM.

**Configure AD connector in VIDM:**

1. VIDM console → **Catalog → Connectors** → select the connector appliance
2. **Add Directory** → Active Directory over LDAP/LDAPS
3. Provide:
   - Domain controller FQDN (use LDAPS port 636 for production)
   - Bind DN: `CN=svc-vidm,OU=Service Accounts,DC=corp,DC=local`
   - Bind password
   - Base DN: `DC=corp,DC=local`
   - Sync scope: select specific OUs containing admin groups (avoid syncing the entire domain)
4. Map user attributes: `sAMAccountName` → Username, `mail` → Email
5. Schedule group sync: every 60 minutes

**Map AD groups to LCM roles:**

```text
LCM → Settings → Access Control → Add Role Assignment
```

| AD Group | LCM Role |
|---|---|
| `GG-LCM-Admins` | LCM Admin |
| `GG-LCM-Operators` | LCM Content Developer |
| `GG-LCM-Viewers` | Viewer |

---

## API Authentication

Service accounts and automation scripts use the LCM REST API with token-based authentication.

```bash
# Obtain a session token (token is valid for 30 minutes by default)
TOKEN=$(curl -sk -X POST "https://lcm-prod-01.example.local/lcm/authz/api/v2/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"svc-lcm-api@local","password":"<password>"}' | jq -r '.token')

# Use the token in subsequent calls
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://lcm-prod-01.example.local/lcm/lcmservice/api/v2/environments"
```

For automation pipelines, store the service account password in a secrets manager (HashiCorp Vault, CyberArk) and retrieve it at runtime rather than hardcoding in scripts.

---

## Local Accounts

| Account | Default Username | Purpose |
|---|---|---|
| LCM Admin | `admin@local` | Web UI and API access — break-glass fallback |
| Appliance SSH | `root` | OS-level shell — restrict to privileged users |
| Appliance SSH (non-root) | `admin` | Limited shell — use for diagnostics |

**Hardening local accounts:**

- Change the `admin@local` password immediately after deployment
- Disable or rotate `root` SSH access — prefer `admin` for routine access
- Do not share credentials — use named VIDM-backed accounts for day-to-day access
- Store break-glass passwords in an offline vault or privileged access workstation

```bash
# Change local admin password via API
curl -sk -X PATCH -H "x-xenon-auth-token: $TOKEN" \
  -H "Content-Type: application/json" \
  "https://lcm-prod-01.example.local/lcm/authz/api/v2/user/password" \
  -d '{"oldPassword":"<old>","newPassword":"<new>"}'
```

---

## Certificate Trust for API Clients

LCM uses TLS for all API endpoints. Scripts connecting to LCM must either:

1. Trust the LCM certificate CA (add CA to the OS trust store on the client)
2. Use `-sk` (skip verify) for internal tooling only — not acceptable for production pipelines

```bash
# Add LCM CA to trust store (Linux/macOS) so scripts can omit -k
cp lcm-ca.crt /usr/local/share/ca-certificates/lcm-ca.crt
update-ca-certificates   # Debian/Ubuntu
# or
trust anchor lcm-ca.crt  # RHEL/Fedora
```

---

## Session and Token Policies

| Setting | Value | Location |
|---|---|---|
| API token lifetime | 30 minutes (default) | LCM internal — not configurable via UI |
| VIDM session timeout | 8 hours (configurable) | VIDM console → Policies → Session Policies |
| Failed login lockout | 5 attempts (VIDM default) | VIDM console → Policies → Password Policies |
| MFA enforcement | Via VIDM access policies | VIDM console → Policies → Access Policies |
