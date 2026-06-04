# Cisco Nexus Dashboard — Security Authentication

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Import corporate CA certificate for LDAPS trust
acs certificates import-ca --cert /tmp/corp-ca.crt --name corp-ldap-ca

# Verify
acs certificates show-ca
```text
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
