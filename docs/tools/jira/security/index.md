# Jira — Security



<div class="kb-summary">
Jira — Security reference.
</div>

```
┌────────────────────────────────────── Jira — Security Overview ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     Jira Security Domains                                     │   │
│   │             Authentication: LDAP/SAML SSO; PAT for API; local break-glass accounts            │   │
│   │           Authorisation: global perms → permission schemes → issue security schemes           │   │
│   │               Encryption: TLS 1.2+ in transit; DB and JIRA_HOME encrypt at rest               │   │
│   │           Hardening: disable anonymous access, restrict admin path, apply advisories          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Jira security follows same principles as Confluence: identity, access, transport                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │         LDAP/AD sync        │  │      Global permissions     │  │        TLS 1.2+ HTTPS       │   │
│   │       SAML SSO via IdP      │  │      Permission scheme      │  │      DB encrypt at rest     │   │
│   │       MFA at IdP layer      │  │        Issue security       │  │     NFS encrypt at rest     │   │
│   │         PAT for API         │  │         Admin IP ACL        │  │        Key management       │   │
│   │      Local break-glass      │  │       Anon access: off      │  │        Cert rotation        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LDAP/AD · IdP (Okta/ADFS) · reverse proxy for TLS · DB VM with encrypted disk                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Permission scheme = project-level ACL; maps operations to project roles/groups                       │
│  Issue security scheme = per-issue visibility restriction; hides issues from non-members              │
│  Global permission = instance-wide right: Administer Jira, Create Projects, Browse Users              │
│  Anonymous access = Admin > Global Permissions; remove "Any logged in user" for browse                │
│  SAML SSO        = Jira as SP; IdP provides signed assertion; no password in Jira                     │
│  PAT             = Personal Access Token; Admin > Profile > PATs; use as Bearer token                 │
│  IP ACL          = restrict /admin and /secure/admin to corporate IP ranges via proxy                 │
│  Issue security  = security level scheme; assign issues to a level; control visibility                │
│  TLS termination = reverse proxy (nginx/F5); Tomcat sees plain HTTP on port 8080                      │
│  MFA             = enforced at IdP; Jira trusts SAML assertion without re-checking                    │
│  Audit log       = Admin > Audit Log; records admin and permission events                             │
│  Security advisory = Atlassian PSIRT publishes CVEs; patch within SLA window                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────────── Jira — Security Overview ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     Jira Security Domains                                     │   │
│   │             Authentication: LDAP/SAML SSO; PAT for API; local break-glass accounts            │   │
│   │           Authorisation: global perms → permission schemes → issue security schemes           │   │
│   │               Encryption: TLS 1.2+ in transit; DB and JIRA_HOME encrypt at rest               │   │
│   │           Hardening: disable anonymous access, restrict admin path, apply advisories          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Jira security follows same principles as Confluence: identity, access, transport                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │         LDAP/AD sync        │  │      Global permissions     │  │        TLS 1.2+ HTTPS       │   │
│   │       SAML SSO via IdP      │  │      Permission scheme      │  │      DB encrypt at rest     │   │
│   │       MFA at IdP layer      │  │        Issue security       │  │     NFS encrypt at rest     │   │
│   │         PAT for API         │  │         Admin IP ACL        │  │        Key management       │   │
│   │      Local break-glass      │  │       Anon access: off      │  │        Cert rotation        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LDAP/AD · IdP (Okta/ADFS) · reverse proxy for TLS · DB VM with encrypted disk                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Permission scheme = project-level ACL; maps operations to project roles/groups                       │
│  Issue security scheme = per-issue visibility restriction; hides issues from non-members              │
│  Global permission = instance-wide right: Administer Jira, Create Projects, Browse Users              │
│  Anonymous access = Admin > Global Permissions; remove "Any logged in user" for browse                │
│  SAML SSO        = Jira as SP; IdP provides signed assertion; no password in Jira                     │
│  PAT             = Personal Access Token; Admin > Profile > PATs; use as Bearer token                 │
│  IP ACL          = restrict /admin and /secure/admin to corporate IP ranges via proxy                 │
│  Issue security  = security level scheme; assign issues to a level; control visibility                │
│  TLS termination = reverse proxy (nginx/F5); Tomcat sees plain HTTP on port 8080                      │
│  MFA             = enforced at IdP; Jira trusts SAML assertion without re-checking                    │
│  Audit log       = Admin > Audit Log; records admin and permission events                             │
│  Security advisory = Atlassian PSIRT publishes CVEs; patch within SLA window                          │
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
  <span>Project and issue permission management.</span>
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
