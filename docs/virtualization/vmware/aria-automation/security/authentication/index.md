# Aria Automation — Authentication

## Authentication Architecture

Aria Automation delegates all authentication to **Workspace ONE Access (VIDM)**. There is no standalone AD/LDAP connector in Aria Automation itself — VIDM acts as the identity broker between Aria Automation and Active Directory.

```text
Browser → Aria Automation UI → VIDM (SAML redirect) → AD/LDAP → VIDM session → Aria Automation JWT
API clients → Aria Automation /csp/gateway/am/api/login → VIDM credentials → Bearer token
```
┌────────────────────────────────── Aria Automation — Authentication ───────────────────────────────────┐
│                                                                                                       │
│  vRA authentication flows through vIDM (Workspace ONE) via SAML; local accounts are minimal.          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Authentication Methods            │  │               vIDM / SSO Flow               │   │
│   │          Primary: SAML via vIDM/WS1          │  │        Browser → vRA → redirect vIDM        │   │
│   │       API: Bearer JWT from CSP gateway       │  │        vIDM → LDAP/SAML IdP validate        │   │
│   │        Local admin: break-glass only         │  │         vIDM returns SAML assertion         │   │
│   │        MFA: enforced via vIDM policy         │  │     vRA validates assertion, issues JWT     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  API authentication uses a short-lived JWT; service accounts use refresh tokens.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                API Auth Flow                 │  │                MFA and Policy               │   │
│   │        POST /csp/gateway/am/api/login        │  │       MFA: TOTP, push, or hardware key      │   │
│   │        Payload: {username, password}         │  │      Policy: step-up for admin actions      │   │
│   │      Returns: access_token (JWT/1h TTL)      │  │         Session timeout: 8h default         │   │
│   │     Refresh: use refresh_token to renew      │  │        Failed logins: lockout after 5       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vIDM/WS1 appliance · vRA appliance · AD/LDAP directory · NTP (for SAML timestamps)                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vIDM              = VMware Identity Manager; SAML IdP for all Aria suite products                    │
│  SAML assertion    = XML token vIDM returns after authenticating user; vRA validates signature        │
│  JWT               = JSON Web Token; short-lived bearer token for vRA REST API calls                  │
│  CSP gateway       = Cloud Services Platform auth gateway endpoint in vRA                             │
│  Refresh token     = Long-lived token for service accounts; exchange for new access token             │
│  MFA               = Multi-Factor Authentication; enforced via vIDM access policy                     │
│  TOTP              = Time-based One-Time Password; one MFA method supported by vIDM                   │
│  Break-glass admin = Local vRA admin account used only when vIDM is unavailable                       │
│  Access policy     = vIDM policy defining auth method, MFA, and device requirements                   │
│  Session timeout   = Duration before vRA redirects user back to vIDM for re-authentication            │
│  Lockout           = Account locked after N failed logins; admin must unlock via vIDM                 │
│  Token TTL         = Access token expires in 1 hour; refresh token lasts days/weeks                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Provide:
- VIDM hostname: `vidm.example.local`
- Admin credentials for VIDM
- Accept the VIDM certificate (or ensure it is trusted by the Aria Automation appliance)

After configuration, all Aria Automation users authenticate via VIDM. The local `admin` account becomes a fallback that authenticates via VIDM using the `System Domain`.

---

## Active Directory Integration via VIDM

AD integration is configured in VIDM, not in Aria Automation directly:

1. **VIDM console → Identity & Access Management → Directories → Add Directory**
2. Select **Active Directory over LDAP/LDAPS**
3. Provide:
   - Domain: `corp.local`
   - Domain controllers: `dc01.example.local:636`, `dc02.example.local:636`
   - Bind DN: `CN=svc-vidm,OU=Service Accounts,DC=corp,DC=local`
   - Bind password
   - Base DN for user search: `DC=corp,DC=local`
4. Select OUs to sync (choose specific OUs, not the full domain)
5. Set sync schedule: every 60 minutes

After sync, AD users can log into Aria Automation using their domain credentials via the VIDM login page.

---

## API Authentication

All Aria Automation REST API calls require a Bearer token obtained from VIDM.

**Acquire a token (local admin account):**

```bash
TOKEN=$(curl -sk -X POST \
  "https://vra-prod-01.example.local/csp/gateway/am/api/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>","domain":"System Domain"}' | \
  jq -r '.token')

# Use in subsequent requests
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.example.local/iaas/api/zones" | jq '.'
```

**Acquire a token (AD user):**

```bash
TOKEN=$(curl -sk -X POST \
  "https://vra-prod-01.example.local/csp/gateway/am/api/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"svc.vra@corp.local","password":"<password>","domain":"corp.local"}' | \
  jq -r '.token')
```

**Token validity:** 8 hours by default. For long-running scripts, implement token refresh logic:

```bash
# Refresh token before expiry (every 7 hours)
TOKEN=$(curl -sk -X POST \
  "https://vra-prod-01.example.local/csp/gateway/am/api/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"svc-vra-api","password":"<password>","domain":"System Domain"}' | \
  jq -r '.token')
```

---

## API Service Account

Create a dedicated local account for API access rather than using the platform `admin` account:

1. Log in to VIDM with admin credentials
2. **VIDM console → Users & Groups → Users → Add User**
3. Create user `svc-vra-api` in the **System Domain**
4. Set a strong password; store in enterprise vault
5. Assign the minimum required Aria Automation role in **Identity & Access Management → Aria Automation → Role Assignments**

---

## Session and Token Policies

| Setting | Default | Configuration |
|---|---|---|
| API token lifetime | 8 hours | VIDM console → Identity & Access Management → Policies |
| UI session timeout | 8 hours | VIDM console → Policies → Session Policies |
| AD group sync interval | 60 minutes | VIDM → Directories → edit directory |
| MFA enforcement | Via VIDM access policies | VIDM console → Policies → Access Policies → add MFA step |
| Failed login lockout | 5 attempts (VIDM default) | VIDM console → Policies → Password Policies |

---

## Certificate Trust for API Clients

Aria Automation uses TLS for all API endpoints. Clients must trust the CA that signed the Aria Automation certificate:

```bash
# Add Aria Automation CA to the OS trust store on a Linux client
cp internal-ca.pem /usr/local/share/ca-certificates/internal-ca.crt
update-ca-certificates   # Debian/Ubuntu

# Python clients
import requests
requests.get("https://vra-prod-01.example.local/iaas/api/zones",
             headers={"Authorization": f"Bearer {token}"},
             verify="/etc/ssl/certs/ca-certificates.crt")
```
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
