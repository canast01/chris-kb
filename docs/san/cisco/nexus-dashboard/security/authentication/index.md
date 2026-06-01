# Nexus Dashboard — Authentication


<div class="kb-summary">
> Part of the [Nexus Dashboard](../../index.md) reference.
</div>

---

## Overview

Nexus Dashboard uses Keycloak as its internal identity provider. It supports local accounts, LDAP/Active Directory, TACACS+, RADIUS, and SAML 2.0 SSO. Production environments should use LDAP or SAML for named user accounts, with a single local admin account reserved as break-glass.

---

## 1. Local Accounts

Local accounts are managed under **Admin Console > Security > Local Users**.

### Creating a Local Account

1. Navigate to **Admin Console > Security > Local Users > Add User**.
2. Enter username, full name, and email.
3. Set a strong initial password.
4. Assign a role (see [Access Control](../access-control/index.md)).
5. Click **Save**.

### Password Policy

Configure under **Admin Console > Security > Security Settings > Password Policy**:

| Setting | Recommended Value |
|---|---|
| Minimum length | 12 characters |
| Require uppercase | Yes |
| Require lowercase | Yes |
| Require numbers | Yes |
| Require special characters | Yes |
| Maximum age | 90 days |
| Password history | 12 (cannot reuse last 12) |
| Account lockout after | 5 failed attempts |
| Lockout duration | 30 minutes |

### Break-Glass Account

Maintain exactly one local admin account as break-glass:
- Username: `admin` (default) or `nd-breakglass`
- Password: stored in vault (HashiCorp Vault, CyberArk) — not known to individual engineers
- Rotate quarterly
- All use must be recorded in the audit trail
- Used only when LDAP/SAML is unavailable

---

## 2. LDAP / Active Directory

Configure under **Admin Console > Security > Authentication > Login Domains > Add**:

| Field | Value |
|---|---|
| Domain name | `CORP-AD` |
| Type | Active Directory |
| Server address | `ldap.corp.example.com` |
| Port | 636 (LDAPS) |
| Base DN | `DC=corp,DC=example,DC=com` |
| Bind DN | `CN=nd-svc,OU=Service Accounts,DC=corp,DC=example,DC=com` |
| Bind password | Service account password |
| User attribute | `sAMAccountName` |
| Group search base | `OU=ND-Groups,DC=corp,DC=example,DC=com` |

### Import CA Certificate for LDAPS

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Import corporate CA certificate for LDAPS trust
acs certificates import-ca --cert /tmp/corp-ca.crt --name corp-ldap-ca

# Verify
acs certificates show-ca
```
```
┌─────────────────────────── Cisco Nexus Dashboard — Security Authentication ───────────────────────────┐
│                                                                                                       │
│  ND supports local, LDAP, RADIUS, TACACS+, and SAML 2.0 authentication providers.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Local Authentication             │  │            Remote Authentication            │   │
│   │         Built-in user DB on cluster          │  │            RADIUS: PAP/CHAP auth            │   │
│   │           Bcrypt password hashing            │  │         TACACS+: per-cmd accounting         │   │
│   │           Min 8 chars + complexity           │  │         LDAP: bind DN + search base         │   │
│   │         Account lockout: 5 attempts          │  │         SAML 2.0: IdP-initiated SSO         │   │
│   │        Local fallback if remote down         │  │         Priority: order of providers        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Remote providers tried in priority order; local fallback activates if all unreachable                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                SAML SSO Flow                 │  │              Session Management             │   │
│   │          SP-initiated: ND redirects          │  │           JWT: signed bearer token          │   │
│   │         Assertion: groups → ND roles         │  │          Token TTL: 60 min default          │   │
│   │         Signing cert: IdP public key         │  │          Refresh: re-auth required          │   │
│   │          MFA enforced at IdP layer           │  │         Concurrent sessions: allowed        │   │
│   │          Metadata URL: auto-import           │  │           Idle timeout: UI logout           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND cluster · RADIUS/TACACS+ server · LDAP/AD server · SAML IdP · management network                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SAML 2.0       = XML-based SSO standard; ND acts as Service Provider                                 │
│  IdP            = Identity Provider; issues SAML assertions (e.g. Okta, Azure AD)                     │
│  SP-initiated   = User clicks ND login, is redirected to IdP for authentication                       │
│  SAML assertion = XML document from IdP containing user identity and group claims                     │
│  Bcrypt         = Adaptive password hashing algorithm; resistant to brute-force                       │
│  Bind DN        = LDAP distinguished name used by ND to query the directory                           │
│  Search base    = LDAP OU from which ND searches for user and group objects                           │
│  JWT            = JSON Web Token; signed session credential returned after auth                       │
│  Account lockout= Disables login after 5 consecutive failed authentication attempts                   │
│  PAP            = Password Authentication Protocol; sends password in clear over TLS                  │
│  Local fallback = Admin-account local auth if all remote servers are unreachable                      │
│  Metadata URL   = SAML IdP endpoint exposing signing cert and SSO URL automatically                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
