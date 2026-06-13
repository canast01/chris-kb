---
tags:
  - san
  - security
---
# SANnav — Security


<div class="kb-summary">
SANnav hardening — RBAC, TLS configuration, user management, and secure communication with managed switches.
</div>

```text
┌────────────────────────────────────────── SANnav — Security ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       SANnav security: LDAP/AD authentication, RBAC, TLS enforcement, and audit logging       │   │
│   │    Authentication: LDAP/AD integration with AD group-to-role mapping; local admin fallback    │   │
│   │     RBAC: Network Administrator / Network Operator / Read-only roles; fabric-level scoping    │   │
│   │   Audit: all login events, zone changes, and admin operations logged with user and timestamp  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication gate → role-based scope → encrypted channel → immutable audit trail                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │       Encryption/Audit      │   │
│   │         LDAP/AD SSO         │  │        Network Admin        │  │        HTTPS TLS 1.2+       │   │
│   │       AD group mapping      │  │       Network Operator      │  │       API TLS enforced      │   │
│   │       Local admin acct      │  │          Read-only          │  │         Login audit         │   │
│   │       Session timeout       │  │         Fabric scope        │  │      Config change log      │   │
│   │       Password policy       │  │       Least privilege       │  │        Syslog export        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    SANnav access restricted to jump host network; direct internet access not permitted                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Control      │     Standard     │     RBAC role     │   Enforcement    │      Review      │   │
│   │   Auth method    │   LDAP primary   │     All roles     │ SANnav settings  │    Quarterly     │   │
│   │   Zone changes   │    Admin only    │     Net Admin     │ Role enforcement │    Per change    │   │
│   │    Audit log     │   All actions    │        N/A        │  Syslog/SANnav   │     Monthly      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SANnav on management VLAN; jump host required for browser access                         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    LDAP/AD       = SANnav authenticates against Active Directory via LDAP or LDAPS                    │
│    AD group map  = AD security group mapped to SANnav role; changes in AD take effect on login        │
│    Network Admin = SANnav role with full fabric management including zone changes                     │
│    Net Operator  = SANnav role allowing port admin and monitoring; no zone set changes                │
│    Read-only     = SANnav viewer role; dashboard and reports only, no configuration access            │
│    Fabric scope  = Limit role to specific fabrics; useful for multi-customer environments             │
│    Session timeout = Idle session terminated; default 30 minutes; configurable                        │
│    TLS 1.2+      = Minimum TLS version for SANnav HTTPS and REST API; TLS 1.0/1.1 disabled            │
│    Audit log     = SANnav internal log of all user actions; exportable to syslog                      │
│    Syslog export = SANnav sends audit events to external syslog/SIEM for retention                    │
│    Local admin   = Built-in local account; break-glass only; stored in vault                          │
│    Password pol. = Complexity and rotation requirements applied to local SANnav accounts              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>LDAP/RADIUS integration, local accounts, and session management.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>RBAC roles, privilege assignment, and least-privilege configuration.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>TLS configuration, certificate management, and data protection.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baseline, audit logging, and compliance settings.</span>
</a>

</div>

