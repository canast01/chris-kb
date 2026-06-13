---
tags:
  - security
  - srm
  - vmware
---
# SRM — Authentication


<div class="kb-summary">
Authentication reference covering Site Pairing Authentication (Certificate-Based), SRA Authentication to Storage Array, REST API Authentication, vSphere Replication Authentication, Break-Glass Access to SRM and 1 more sections.

*Applies to: SRM 8.x / 9.x*
</div>

  SRM Authentication Chain
```text
┌───────────────────────────────────── VMware SRM — Authentication ─────────────────────────────────────┐
│                                                                                                       │
│  SRM uses vCenter SSO for user authentication; site pair uses TLS certificates                        │
│  for inter-site trust; SRM REST API uses bearer tokens.                                               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             User Authentication              │  │               Site Pair Trust               │   │
│   │           vCenter SSO: all logins            │  │              TLS cert exchange              │   │
│   │            AD groups: role-mapped            │  │            Self-signed or CA cert           │   │
│   │             SAML token from SSO              │  │             Trust on first pair             │   │
│   │         MFA: via vCenter SSO policy          │  │           Re-pair if cert changes           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  User auth is entirely vCenter SSO; site trust is certificate-based TLS.                              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                REST API Auth                 │  │            Certificate Management           │   │
│   │             POST /api/rest/login             │  │         SRM cert: Windows cert store        │   │
│   │          Bearer token: short-lived           │  │           Replace via IIS bindings          │   │
│   │            Basic auth: automation            │  │              TLS 1.2+ enforced              │   │
│   │         Refresh: re-login on expiry          │  │            Re-pair: cert rotation           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AD must be reachable from both SRM Servers on management network; cert must be                       │
│  trusted by remote SRM Server for site pair to establish.                                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vCenter SSO   = SRM delegates all user auth to vCenter SSO                                           │
│  SAML token    = SSO assertion; used for SRM session                                                  │
│  Bearer token  = REST API token; short-lived JWT                                                      │
│  Site pair TLS = mutual TLS between the two SRM Servers                                               │
│  Trust-on-pair = exchange certs when creating site pair                                               │
│  Re-pair       = required if SRM cert is replaced                                                     │
│  IIS binding   = SRM Server binds TLS cert via Windows IIS                                            │
│  TLS 1.2+      = minimum for site pair and REST API                                                   │
│  Basic auth    = REST API; base64 user:pass; use only over TLS                                        │
│  MFA           = enforced at vCenter SSO layer; applies to SRM                                        │
│  AD reachable  = SSO requires AD for group membership lookup                                          │
│  Cert rotation = requires re-pair; plan maintenance window                                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## See also

- [SRM — Access Control](access-control/)
- [SRM — Hardening](hardening/)
