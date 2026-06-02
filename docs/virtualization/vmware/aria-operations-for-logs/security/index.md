# Aria Ops for Logs — Security

<div class="kb-summary">
Aria Ops for Logs — Security reference.
</div>

```
┌──────────────────────────────────────── Aria Logs — Security ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Active Directory/LDAP for SSO; role-based access for dashboards and alerts per user group   │   │
│   │         TLS for agent connections and syslog TCP/TLS; REST API served over HTTPS only         │   │
│   │           FIPS 140-2 mode available; encrypted passwords at rest in credential store          │   │
│   │     Audit trail captures all admin actions: login events, config changes, source additions    │   │
│   │         Certificate rotation for agent TLS, cluster UI cert, and syslog TLS endpoints         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication gates access · role-based access scopes dashboards                                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │         AD/LDAP auth        │  │         Admin: full         │  │          Agent TLS          │   │
│   │       LDAP integration      │  │       User: dashboards      │  │        Syslog TCP/TLS       │   │
│   │         Local admin         │  │       Dashboard roles       │  │       REST over HTTPS       │   │
│   │          Role-based         │  │        Source access        │  │       Cert management       │   │
│   │          API token          │  │          Alert mgmt         │  │          FIPS mode          │   │
│   │         SAML support        │  │       Content pk admin      │  │        Pwd encrypted        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Auth controls who logs in · access control scopes dashboards · encryption secures all log paths    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Auth       │   Access Ctrl    │     Encryption    │    Hardening     │      Audit       │   │
│   │   AD/LDAP SSO    │    Admin role    │     Agent TLS     │  Cert rotation   │   Admin events   │   │
│   │    API tokens    │    User role     │     Syslog TLS    │    FIPS mode     │    Query log     │   │
│   │   SAML support   │  Dashboard role  │     HTTPS REST    │    Pwd policy    │   Alert audit    │   │
│   │   Local admin    │  Source access   │     Cert mgmt     │   Min-perm API   │  Config changes  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VMs (cluster) · RAM DIMMs · Network NICs · AD/LDAP server · CA infrastructure                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  AD/LDAP            = Active Directory/LDAP; group membership mapped to Aria Logs roles               │
│  SAML               = Security Assertion Markup Language; federated SSO for Aria Logs UI login        │
│  Role-based access   = Admin/user/viewer roles; scoped to dashboard sets and log source access        │
│  Admin role         = Full Aria Logs access: manage sources, alerts, content packs, and users         │
│  User role          = Dashboard view and query access; cannot manage sources or system config         │
│  TLS agent connection = Encrypted channel between vRLI agent and cluster ingestion endpoint           │
│  Syslog over TLS    = RFC5425 TLS-wrapped syslog on port 6514; encrypts log transit from sources      │
│  FIPS 140-2         = Federal cryptographic standard; enabled at cluster level for compliance         │
│  Certificate management = Rotate UI, agent, and syslog TLS certificates via admin settings            │
│  API token          = Bearer token for REST API calls; scoped to authenticated user role              │
│  Audit trail        = Immutable log of admin actions: logins, config changes, source management       │
│  Encrypted credentials = Passwords and secrets stored encrypted in cluster credential vault           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>SSO, LDAP, local accounts, and identity sources.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Roles, permissions, and least privilege access.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>TLS certificate management and log data encryption.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines and compliance configuration.</span>
</a>

</div>
