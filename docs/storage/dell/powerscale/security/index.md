---
tags:
  - dell
  - security
---
# PowerScale — Security

<div class="kb-summary">
PowerScale hardening — SmartLock compliance mode, NFS export access control, SMB share permissions, and audit logging.
</div>

```text
┌────────────────────────────────────── Dell PowerScale Security ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       PowerScale security: access zones isolate tenants; AD/LDAP/Kerberos for file auth       │   │
│   │        Access zones: each zone has own auth providers, IP pool, SMB shares, NFS exports       │   │
│   │       SmartLock: WORM retention (compliance = tamper-proof; enterprise = admin override)      │   │
│   │         Audit: protocol audit log per zone; CEE (Common Event Enabler) export to SIEM         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Client auth → access zone lookup → ACL / Unix perm check → SmartLock WORM → audit log              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Access Zones        │  │        Authentication       │  │       Data Protection       │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        Per-zone auth        │  │         AD Kerberos         │  │        SmartLock WORM       │   │
│   │       Isolated IP pool      │  │        LDAP provider        │  │       Compliance mode       │   │
│   │       Per-zone shares       │  │         NIS provider        │  │       Enterprise mode       │   │
│   │          RBAC roles         │  │        Local accounts       │  │        CEE audit log        │   │
│   │        Zone isolation       │  │        SID / UID map        │  │         SIEM forward        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Zone auth configured → RBAC roles assigned → SmartLock retention set → audit enabled               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Control      │    Mechanism     │      Standard     │    Exception     │      Audit       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    File auth     │   AD Kerberos    │  All NAS clients  │  LDAP fallback   │   Auth events    │   │
│   │    Admin auth    │    RBAC + AD     │   Named accounts  │Local break-glass │    Login log     │   │
│   │       WORM       │    SmartLock     │  Compliance mode  │ Enterprise only  │  Retention log   │   │
│   │    Audit log     │    CEE / SIEM    │    All file ops   │        —         │  Weekly review   │   │
│                                                                                                       │
│    Physical: SSH admin access on mgmt port; CEE agent on cluster node forwards audit events           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Access zone    = Isolated namespace partition; own auth providers, IPs, shares, and exports        │
│    SmartLock      = OneFS WORM; compliance = no override; enterprise = admin can override             │
│    Compliance mode= SmartLock mode that prevents even root from deleting WORM-retained files          │
│    Enterprise mode= SmartLock WORM with admin override capability; less strict than compliance        │
│    CEE            = Common Event Enabler; OneFS audit log export agent for SIEM integration           │
│    RBAC roles     = OneFS built-in roles: SystemAdmin, AuditAdmin, SecurityAdmin, BackupAdmin         │
│    SID/UID map    = Identity mapping between Windows SID and Unix UID for mixed permissions           │
│    Kerberos       = Protocol for mutual auth between AD domain and OneFS NFS/SMB clients              │
│    Break-glass    = Local root account on OneFS node for emergency when AD unavailable                │
│    Zone isolation = Cross-zone access is blocked; tenant A cannot access zone B data                  │
│    NIS provider   = Legacy Unix auth; NIS maps used in mixed Unix environments                        │
│    Retention log  = SmartLock audit record of file commit, retention date, and release events         │
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
  <span>TLS certificate management and data encryption.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines and compliance configuration.</span>
</a>

</div>

