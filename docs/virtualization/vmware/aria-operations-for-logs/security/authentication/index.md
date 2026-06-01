# Aria Ops for Logs — Authentication


<div class="kb-summary">
Authentication reference covering Authentication Methods, Active Directory / LDAP Configuration, Workspace ONE Access (VIDM) Integration, Verify LDAP Authentication from CLI, Session Policies and 2 more sections.
</div>

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
```
┌────────────────────────────── Aria Operations for Logs — Authentication ──────────────────────────────┐
│                                                                                                       │
│  vRLI supports local auth, LDAP/AD integration, and vIDM SSO for enterprise environments.             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Authentication Methods            │  │            LDAP/AD Configuration            │   │
│   │        Local: built-in admin account         │  │     Admin → Authentication → Active Dir     │   │
│   │       LDAP: AD groups mapped to roles        │  │     Bind DN: service account credentials    │   │
│   │         vIDM SSO: SAML if in LCM env         │  │        Search base: DC=corp,DC=local        │   │
│   │      API: session token from login POST      │  │       Group filter: memberOf attribute      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  vIDM SSO is preferred in Aria Suite deployments for centralised identity management.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                vIDM SSO Flow                 │  │              Session Management             │   │
│   │        Browser → vRLI → redirect vIDM        │  │         Session TTL: 30 min default         │   │
│   │          vIDM validates user + MFA           │  │        Idle timeout: re-auth required       │   │
│   │      SAML assertion → vRLI grants role       │  │          Multiple sessions: allowed         │   │
│   │     Role derived from AD group via vIDM      │  │         Lockout: handled by vIDM/AD         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRLI appliance · AD/LDAP server · vIDM (optional SSO) · NTP (SAML timestamp)                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Local admin       = Default vRLI built-in account; change password immediately after install         │
│  LDAP bind DN      = Service account used by vRLI to search AD; read-only permissions                 │
│  Search base       = AD OU or domain root where vRLI searches for users and groups                    │
│  memberOf filter   = LDAP attribute used to check which group a user belongs to                       │
│  vIDM SSO          = SAML-based SSO; configured when vRLI is part of Aria Suite LCM env               │
│  SAML assertion    = XML token from vIDM confirming user identity and group membership                │
│  Session token     = Short-lived bearer token for REST API; from POST /api/v1/sessions                │
│  Session TTL       = 30-minute inactivity timeout; re-auth required after expiry                      │
│  MFA via vIDM      = Multi-Factor Authentication enforced at vIDM level for all Aria products         │
│  Role from group   = vRLI maps AD group to Super Admin or User; no fine-grained RBAC                  │
│  Lockout policy    = AD account lockout applies; managed in AD not in vRLI                            │
│  API session       = POST /api/v1/sessions {username, password}; returns sessionId                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```python

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
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
