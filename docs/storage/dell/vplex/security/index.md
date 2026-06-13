---
tags:
  - dell
  - security
---
# Dell VPLEX — Security

<div class="kb-summary">
Dell VPLEX — Security reference: Authentication, Access Control, Encryption, Hardening.
</div>

```text
┌───────────────────────────────────────── Dell VPLEX Security ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     VPLEX security: storage views for host access control; LDAP for admin auth; audit log     │   │
│   │          Storage view: binds virtual volumes to host initiator WWNs; deny by default          │   │
│   │       Admin auth: LDAP/AD group mapped to GeoSynchrony roles; local admin for emergency       │   │
│   │       TLS on management API; audit log of all CLI and GUI changes exportable via syslog       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Host WWN in storage view → virtual volume access granted → LDAP admin auth → audit log             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Host Access         │  │          Admin Auth         │  │       Audit / Logging       │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │         Storage view        │  │          LDAP / AD          │  │        CLI audit log        │   │
│   │         WWN binding         │  │          RBAC roles         │  │        Syslog export        │   │
│   │       Deny by default       │  │      Local break-glass      │  │         Event filter        │   │
│   │          SAN zoning         │  │         TLS mgmt API        │  │         SIEM forward        │   │
│   │         Port zoning         │  │       Session timeout       │  │         Login events        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Storage view review → LDAP role audit → SAN zone check → syslog review cycle                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Control      │    Mechanism     │      Standard     │    Exception     │      Audit       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │   Host access    │   Storage view   │   WWN whitelist   │  No open views   │    View audit    │   │
│   │    Admin auth    │    LDAP / AD     │   Named accounts  │    Local only    │    Login log     │   │
│   │    CLI access    │    Role-based    │   Storage admin   │  Read-only role  │ CLI audit trail  │   │
│   │     Logging      │   Syslog/SIEM    │    All changes    │        —         │  Weekly review   │   │
│                                                                                                       │
│    Physical: VPLEX management port on OOB network; SAN fabric for I/O; WAN port for Metro             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Storage view   = VPLEX host access control: virtual volume + initiator group + port group          │
│    WWN binding    = Specific host HBA WWN(s) included in storage view; unlisted WWNs denied           │
│    Deny by default= VPLEX presents no volumes to any host until a storage view is created             │
│    SAN zoning     = FC fabric zones restrict which HBAs see which VPLEX front-end ports               │
│    RBAC roles     = GeoSynchrony roles: Admin, Operator, Monitor (read-only)                          │
│    Local break-glass= Local admin account on GeoSynchrony; use only when LDAP down                    │
│    TLS mgmt API   = VPLEX management API and CLI secured with TLS; REST and SSH                       │
│    CLI audit log  = GeoSynchrony logs all vplex-shell commands with user, time, and action            │
│    Event filter   = VPLEX event log filter by severity; export to syslog for SIEM correlation         │
│    Open view      = Storage view with all-WWN access; prohibited; every view must be explicit         │
│    Session timeout= Idle timeout on vplex-shell and GUI; default 30 min                               │
│    Port group     = Collection of VPLEX I/O director ports mapped in a storage view                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="authentication/"><strong>Authentication</strong><span>SSO, LDAP, local accounts, and identity sources.</span></a>
<a class="kb-card" href="access-control/"><strong>Access Control</strong><span>Roles, permissions, and least privilege access.</span></a>
<a class="kb-card" href="encryption/"><strong>Encryption</strong><span>TLS certificate management and data encryption.</span></a>
<a class="kb-card" href="hardening/"><strong>Hardening</strong><span>Security baselines and compliance configuration.</span></a>
</div>

