# Aria Ops for Logs — Authentication

```text
┌─────────────────────────────────────────────────────────────┐
│         Aria Ops for Logs Authentication Flow               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Browser / API Client                                       │
│       │                                                     │
│       ├── Local account → admin (System Domain, break-glass)│
│       │                                                     │
│       ├── AD (LDAPS) → Administration → Authentication      │
│       │   dc01.example.local:636  ·  svc-vrli-ldap bind        │
│       │   group membership → role at login time             │
│       │                                                     │
│       └── VIDM (SSO) → redirect to VIDM login page          │
│           (LCM-managed deployments)                         │
│                           │                                 │
│                           ▼                                 │
│  Aria Ops for Logs session (UI) or HTTP Basic (API)         │
│  API: -u 'admin:<pw>' per request — no token                │
│  UI: session timeout 10 hours (no configurable setting)     │
└─────────────────────────────────────────────────────────────┘
```

## Authentication Methods

| Method | Use Case | Configuration Location |
|---|---|---|
| **Local** | Break-glass admin; lab | Built-in; admin account created during setup wizard |
| **Active Directory (LDAPS)** | Production enterprise users | Administration → Authentication → Active Directory |
| **Workspace ONE Access (VIDM)** | SSO when deployed with LCM | Administration → Authentication → VMware Identity Manager |

---

## Active Directory / LDAP Configuration

Use LDAPS (port 636) for production — plain LDAP (port 389) is not acceptable as it transmits bind credentials in cleartext.

**Import the domain CA certificate first:**

```text
Administration → SSL → Import Certificate → paste root CA PEM
```

**Configure AD:**

```text
Administration → Authentication → Active Directory → Configure
```

Settings:
- Domain: `corp.local`
- Primary domain controller: `dc01.example.local:636`
- Secondary domain controller: `dc02.example.local:636` (optional, for HA)
- Use SSL: **Yes**
- Bind DN: `CN=svc-vrli-ldap,OU=Service Accounts,DC=corp,DC=local`
- Bind password: service account password

Test the connection before saving — Aria Ops for Logs performs a test LDAP bind and group search.

---

## Workspace ONE Access (VIDM) Integration

When deployed via LCM, VIDM is available as an SSO provider. For standalone deployments, configure VIDM integration manually:

```text
Administration → Authentication → VMware Identity Manager
```

- VMware Identity Manager FQDN: `vidm.example.local`
- Enable redirect to VIDM login page

After configuration, the Aria Ops for Logs login page shows a "VMware Identity Manager" button. Users authenticate via VIDM and are assigned roles based on their AD group membership (mapped in the AD group configuration).

---

## Verify LDAP Authentication from CLI

```bash
# Test LDAP bind from the Aria Ops for Logs appliance
ldapsearch -H ldaps://dc01.example.local:636 \
  -D "CN=svc-vrli-ldap,OU=Service Accounts,DC=corp,DC=local" \
  -w '<password>' \
  -b "DC=corp,DC=local" \
  "(sAMAccountName=testuser)" \
  sAMAccountName mail memberOf

# Test SSL connection to domain controller
openssl s_client -connect dc01.example.local:636 -CAfile /tmp/corp-ca.pem 2>&1 | \
  grep -E "Verify return code|subject="
# Expected: Verify return code: 0 (ok)
```

---

## Session Policies

| Setting | Default | Notes |
|---|---|---|
| UI session timeout | 10 hours | No configurable timeout in standard edition |
| API authentication | HTTP Basic (per-request) | No session token; credentials sent each request |
| AD group sync | On login | Group membership re-evaluated at each login |
| Failed login lockout | Enforced at AD level | No built-in lockout for local accounts |

---

## Forcing HTTPS

Aria Ops for Logs listens on port 80 (HTTP) and 443 (HTTPS). HTTP automatically redirects to HTTPS — this is the default behaviour and should not be changed. Verify:

```bash
curl -sI http://vrli-prod-01.example.local/ | grep "Location:"
# Expected: Location: https://vrli-prod-01.example.local/
```

Ensure the firewall permits inbound TCP 443 and TCP 80 from admin workstations. Block all other inbound ports except those required for log ingestion (514, 1514, 9543).
