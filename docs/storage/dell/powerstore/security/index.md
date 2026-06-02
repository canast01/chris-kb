# PowerStore — Security

<div class="kb-summary">
PowerStore — Security reference.
</div>

```
┌────────────────────────────────────── Dell PowerStore Security ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        PowerStore security: DARE (SED drives), LDAP/AD for admin auth, RBAC, audit log        │   │
│   │           DARE: SED drives + external KMIP key server; crypto erase on decommission           │   │
│   │           Admin access: LDAP/AD group-based roles; local admin for break-glass only           │   │
│   │        Audit: all admin actions logged; export via syslog to SIEM; TLS 1.2+ on REST API       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    DARE at rest → TLS in transit → LDAP/AD admin auth → RBAC role check → audit log write             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Encryption         │  │        Authentication       │  │        Audit / Access       │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │          DARE (SED)         │  │          LDAP / AD          │  │        Syslog / SIEM        │   │
│   │       KMIP key server       │  │      Local break-glass      │  │          RBAC roles         │   │
│   │         Key rotation        │  │        MFA supported        │  │       Admin audit log       │   │
│   │         Crypto erase        │  │        API token auth       │  │       Session timeout       │   │
│   │         TLS REST API        │  │       Cert management       │  │        Alert on fail        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    DARE key check → LDAP role assignment → audit log export → periodic access review                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Control      │    Mechanism     │      Standard     │    Exception     │      Audit       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    Encryption    │   DARE + KMIP    │    All volumes    │   KMIP outage    │ Key audit trail  │   │
│   │    Admin auth    │    LDAP / AD     │   Named accounts  │    Local only    │   Login events   │   │
│   │    API access    │   Token + TLS    │ Short-lived token │        —         │   API call log   │   │
│   │     Logging      │   Syslog/SIEM    │   All admin ops   │        —         │  Weekly review   │   │
│                                                                                                       │
│    Physical: KMIP server on isolated VLAN; management IP on OOB network; no shared mgmt               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    DARE           = Data At Rest Encryption; SED drives; keys managed by KMIP server                  │
│    KMIP           = Key Management Interoperability Protocol; standard for external key servers       │
│    Crypto erase   = Destroy KMIP encryption key; all DARE-encrypted data becomes unreadable           │
│    RBAC roles     = PowerStore built-in roles: Administrator, Storage Operator, VM Admin, Viewer      │
│    API token auth = REST API session token; short-lived; invalidated on logout or timeout             │
│    Syslog         = Admin event log export; all GUI/CLI/API changes forwarded to SIEM                 │
│    TLS REST API   = PowerStore Manager REST API and web GUI require TLS 1.2+                          │
│    Cert management= Custom TLS cert upload for PowerStore Manager GUI; replaces self-signed           │
│    Break-glass    = Local admin account; use only when LDAP unavailable; log every use                │
│    MFA supported  = Multi-factor auth via LDAP identity provider integration                          │
│    Session timeout= Configurable idle timeout for GUI and REST sessions; default 30 min               │
│    Alert on fail  = Failed login attempts trigger syslog event and optionally email alert             │
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
  <span>Data-at-rest encryption and secure communication.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines and compliance configuration.</span>
</a>

</div>
