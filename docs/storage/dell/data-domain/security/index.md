# Data Domain — Security

<div class="kb-summary">
Data Domain — Security reference: Authentication, Access Control, Encryption, Hardening.
</div>

```text
┌───────────────────────────────────── Dell Data Domain — Security ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Data Domain security: encryption at rest, in transit, Retention Lock, RBAC, and compliance  │   │
│   │   Encryption at rest: AES-256 for stored segments; software or hardware encryption key mgmt   │   │
│   │      Retention Lock: WORM compliance mode; data immutable until retention period expires      │   │
│   │     RBAC: local users, LDAP/AD integration; sysadmin, backup-admin, restricted-admin roles    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Backup data written → encrypted inline → stored in segments → locked with retention policy         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Encryption         │  │        Retention Lock       │  │        Access Control       │   │
│   │       AES-256 at rest       │  │       WORM compliance       │  │           LDAP/AD           │   │
│   │        TLS in transit       │  │       Governance mode       │  │         Local users         │   │
│   │         SW key mgmt         │  │         Period lock         │  │          Role-based         │   │
│   │        Ext KMS (KMIP)       │  │          Legal hold         │  │         SSH key auth        │   │
│   │         Key rotation        │  │          Audit log          │  │         IP allowlist        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Compliance mode Retention Lock cannot be disabled by any admin; requires physical replacement      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Control      │     Standard     │       Scope       │      Config      │      Owner       │   │
│   │     AES-256      │    FIPS 140-2    │    All segments   │  Enable in GUI   │   Storage eng.   │   │
│   │  Retention Lock  │    SEC 17a-4     │    MTree level    │ Compliance mode  │ Legal + storage  │   │
│   │     LDAP/AD      │   NIST 800-63    │     All users     │  Group mapping   │    Infra team    │   │
│   │    Audit log     │      SOC 2       │    All actions    │  Syslog export   │  Security team   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: DD appliance in locked rack; access card required; no KVM; iDRAC for remote mgmt         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Retention Lock = WORM feature that prevents deletion/modification until retention period expires   │
│    Compliance mode = Strongest Retention Lock; even sysadmin cannot shorten period; SEC 17a-4 ready   │
│    Governance mode = Retention Lock where admin can adjust period; for internal policy enforcement    │
│    Legal hold     = Indefinite retention applied per-file; overrides retention period for litigation  │
│    AES-256        = DD encrypts all stored segments with AES-256; no performance penalty on modern HW │
│    SW key mgmt    = DD manages encryption keys internally; keys stored encrypted on the appliance     │
│    Ext KMS / KMIP = External Key Management Server via KMIP protocol (e.g. Thales, HashiCorp)         │
│    LDAP/AD        = Bind DD to corporate LDAP or Active Directory for centralized user management     │
│    SSH key auth   = Disable password SSH; use only public-key authentication for CLI access           │
│    IP allowlist   = Restrict GUI and SSH access to specific management host IP addresses              │
│    KMIP           = Key Management Interoperability Protocol; standard for external KMS integration   │
│    Audit log      = DD event log exported to syslog; records all admin and access events              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="authentication/"><strong>Authentication</strong><span>SSO, LDAP, local accounts, and identity sources.</span></a>
<a class="kb-card" href="access-control/"><strong>Access Control</strong><span>Roles, permissions, and least privilege access.</span></a>
<a class="kb-card" href="encryption/"><strong>Encryption</strong><span>TLS certificate management and data encryption.</span></a>
<a class="kb-card" href="hardening/"><strong>Hardening</strong><span>Security baselines and compliance configuration.</span></a>
</div>
