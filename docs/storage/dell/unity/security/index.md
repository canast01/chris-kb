# Unity — Security

<div class="kb-summary">
Unity — Security reference.
</div>

```text
┌───────────────────────────────────────── Dell Unity Security ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Unity security: DARE (SED drives), LDAP/AD for admin and NAS auth, RBAC, audit log      │   │
│   │        Admin auth: LDAP/AD group mapped to Unity roles; local accounts for break-glass        │   │
│   │      NAS auth: each NAS Server has own AD/LDAP provider; Kerberos for SMB authentication      │   │
│   │           Audit: all Unisphere and uemcli actions logged; export via syslog to SIEM           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    DARE at rest → TLS REST API → LDAP role check → NAS Kerberos → file ACL → audit log                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Encryption         │  │          Admin Auth         │  │         NAS / Audit         │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │          DARE (SED)         │  │          LDAP / AD          │  │       NAS AD/Kerberos       │   │
│   │       KMIP key server       │  │          RBAC roles         │  │         Syslog SIEM         │   │
│   │         Key rotation        │  │      Local break-glass      │  │       Admin audit log       │   │
│   │         Crypto erase        │  │         TLS REST API        │  │        NAS file audit       │   │
│   │        In-transit TLS       │  │       Session timeout       │  │          CEE export         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    DARE + KMIP → LDAP role assignment → NAS Kerberos → file ACL → syslog audit review                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Control      │    Mechanism     │      Standard     │    Exception     │      Audit       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    Encryption    │   DARE + KMIP    │    All volumes    │   KMIP outage    │ Key audit trail  │   │
│   │    Admin auth    │    LDAP / AD     │   Named accounts  │    Local only    │   Login events   │   │
│   │  NAS file auth   │   AD Kerberos    │   Per NAS Server  │  NTLM fallback   │   Auth events    │   │
│   │     Logging      │   Syslog + CEE   │    SIEM ingest    │        —         │  Weekly review   │   │
│                                                                                                       │
│    Physical: KMIP on isolated VLAN; Unity management IP on OOB network; no shared mgmt                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    DARE           = Data At Rest Encryption; SED drives; key managed by external KMIP server          │
│    RBAC roles     = Unity roles: Administrator, Storage Admin, VM Admin, Operator, Auditor            │
│    NAS Server AD  = Each NAS Server joined to its own AD domain for SMB Kerberos auth                 │
│    Kerberos       = Mutual auth for SMB clients and Unity NAS Server via AD tickets                   │
│    NTLM fallback  = Legacy SMB auth when Kerberos unavailable; weaker; disable if possible            │
│    CEE            = Common Event Enabler; NAS file audit export to SIEM                               │
│    File audit     = NAS Server logs file access events (open, delete, rename) via CEE                 │
│    Syslog         = Admin action log (Unisphere / uemcli changes) forwarded to SIEM                   │
│    Session timeout= Configurable idle timeout for Unisphere and uemcli sessions                       │
│    Crypto erase   = Destroy SED encryption key on drive decommission; data unrecoverable              │
│    KMIP outage    = Unity caches keys temporarily; fix KMIP before cache expires                      │
│    Break-glass    = Local Unity admin account; use only when LDAP unavailable; log all use            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Active Directory, LDAP integration, and audit logging.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>RBAC roles and permissions for Unisphere.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Data at rest, data in flight, and key management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security hardening checklist and compliance notes.</span>
</a>

</div>
