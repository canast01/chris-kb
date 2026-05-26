# Confluence — Security


```
┌─────────────────────────────────── Confluence — Security Overview ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  Confluence Security Domains                                  │   │
│   │         Authentication: LDAP/AD sync + SAML SSO (Okta/ADFS) + local fallback accounts         │   │
│   │           Authorisation: Space permissions + page restrictions + global group roles           │   │
│   │           Encryption: TLS 1.2+ in transit; DB and NFS encryption at rest recommended          │   │
│   │       Hardening: disable anonymous access, restrict admin IPs, apply security advisories      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Three security domains — identity, access, and transport — protect Confluence data                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │      LDAP/AD user sync      │  │      Space permissions      │  │        TLS 1.2+ HTTPS       │   │
│   │       SAML SSO via IdP      │  │      Page restrictions      │  │      DB encrypt at rest     │   │
│   │       MFA at IdP layer      │  │      Group-based roles      │  │     NFS encrypt at rest     │   │
│   │      Session management     │  │      Admin-only IP ACL      │  │        Key management       │   │
│   │       PAT for API auth      │  │       Anon access: off      │  │        Cert rotation        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LDAP/AD servers · IdP (Okta/ADFS) · reverse proxy (TLS termination) · DB VM                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Space permission = per-space ACL: View, Add Pages, Add Comments, Admin; set per group/user           │
│  Page restriction = overrides space perms; locks a page to specific users/groups for view/edit        │
│  Anonymous access = global setting; disable to force login for all Confluence content                 │
│  SAML SSO        = Confluence as SP; IdP issues assertions; no password stored in Confluence          │
│  LDAP sync       = Confluence polls AD/LDAP on schedule; imports users and group memberships          │
│  PAT             = Personal Access Token; recommended for REST API; scoped, revocable                 │
│  Session timeout = Admin > Security Configuration; idle session expiry duration                       │
│  IP ACL          = Admin panel restrict to known corporate IP ranges for /admin endpoints             │
│  TLS termination = reverse proxy (nginx/Apache/F5) handles TLS; Tomcat sees plain HTTP                │
│  MFA             = enforced at IdP; Confluence trusts IdP assertion without re-checking               │
│  Security advisory = Atlassian publishes CVEs; apply via version upgrade or patch                     │
│  Audit log       = Admin > Audit Log; tracks permission changes and admin actions                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>SSO, SAML, and authentication configuration.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Space and page permission management.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Data encryption at rest and in transit.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security hardening and compliance settings.</span>
</a>

</div>
