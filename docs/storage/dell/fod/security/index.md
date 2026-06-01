# FOD — Security

<div class="kb-summary">
FOD — Security reference: Authentication, Access Control, Encryption, Hardening.
</div>

```
┌───────────────────────────────────────── Dell FoD — Security ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   FoD security: protect license keys, restrict who can apply features, and audit all changes  │   │
│   │   Key protection: store .lic files in secure vault; never commit to source control or email   │   │
│   │       Access control: only named storage engineers can apply FoD keys; RBAC on array GUI      │   │
│   │      Audit: all FoD applications logged in array event log and ITSM; quarterly reconcile      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key in vault → named engineer with CR → apply via RBAC-controlled GUI → audit trail                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Key Security        │  │        Access Control       │  │            Audit            │   │
│   │        Vault storage        │  │       Named engineers       │  │       Array event log       │   │
│   │         No email/SCM        │  │          Array RBAC         │  │        ITSM CR record       │   │
│   │       Encrypted share       │  │         CR required         │  │       Quarterly audit       │   │
│   │          Portal MFA         │  │        2-person rule        │  │          CMDB diff          │   │
│   │       Key rotation N/A      │  │       Offboard revoke       │  │        Portal history       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    FoD keys do not expire; lost or leaked keys cannot be remotely revoked; vault is critical          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Control      │  Implementation  │      Standard     │       Tool       │      Owner       │   │
│   │   Key storage    │    Vault only    │     Sec policy    │ HashiCorp Vault  │   Storage lead   │   │
│   │   Apply access   │    Named + CR    │    Change ctrl    │    Array RBAC    │   Storage lead   │   │
│   │  Portal access   │   MFA enforced   │    NIST 800-63    │  Dell SSO + MFA  │   Storage lead   │   │
│   │    Audit log     │ Quarterly review │       SOC 2       │ ITSM + array log │     Sec team     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: FoD .lic files never stored in unencrypted locations; vault access is MFA-gated          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vault storage  = All .lic files stored in HashiCorp Vault or CyberArk; access logged               │
│    No email/SCM   = Never send .lic files via email or store in Git/Jira; vault only                  │
│    Portal MFA     = Dell Licensing Portal requires MFA; enforce org-wide in portal settings           │
│    Named engineers = Limit FoD apply privilege to 2-3 storage engineers; document by name             │
│    Array RBAC     = Only Storage Admin role on array can import license keys; not Operator            │
│    CR required    = No FoD key applied without approved ITSM CR; prevents unauthorized changes        │
│    2-person rule  = FoD apply observed by second engineer; prevents unauthorized feature unlock       │
│    Offboard revoke = When storage engineer leaves, remove array RBAC and vault access immediately     │
│    Key rotation   = FoD keys do not rotate; protect the original; report loss to Dell licensing       │
│    Quarterly audit = Review portal history vs CMDB; detect unauthorized feature activation            │
│    Portal history = Dell Licensing Portal logs all key downloads; review for unauthorized access      │
│    CMDB diff      = Quarterly comparison of array active license list to CMDB; flag surprises         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────────── Dell FoD — Security ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   FoD security: protect license keys, restrict who can apply features, and audit all changes  │   │
│   │   Key protection: store .lic files in secure vault; never commit to source control or email   │   │
│   │       Access control: only named storage engineers can apply FoD keys; RBAC on array GUI      │   │
│   │      Audit: all FoD applications logged in array event log and ITSM; quarterly reconcile      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key in vault → named engineer with CR → apply via RBAC-controlled GUI → audit trail                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Key Security        │  │        Access Control       │  │            Audit            │   │
│   │        Vault storage        │  │       Named engineers       │  │       Array event log       │   │
│   │         No email/SCM        │  │          Array RBAC         │  │        ITSM CR record       │   │
│   │       Encrypted share       │  │         CR required         │  │       Quarterly audit       │   │
│   │          Portal MFA         │  │        2-person rule        │  │          CMDB diff          │   │
│   │       Key rotation N/A      │  │       Offboard revoke       │  │        Portal history       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    FoD keys do not expire; lost or leaked keys cannot be remotely revoked; vault is critical          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Control      │  Implementation  │      Standard     │       Tool       │      Owner       │   │
│   │   Key storage    │    Vault only    │     Sec policy    │ HashiCorp Vault  │   Storage lead   │   │
│   │   Apply access   │    Named + CR    │    Change ctrl    │    Array RBAC    │   Storage lead   │   │
│   │  Portal access   │   MFA enforced   │    NIST 800-63    │  Dell SSO + MFA  │   Storage lead   │   │
│   │    Audit log     │ Quarterly review │       SOC 2       │ ITSM + array log │     Sec team     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: FoD .lic files never stored in unencrypted locations; vault access is MFA-gated          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vault storage  = All .lic files stored in HashiCorp Vault or CyberArk; access logged               │
│    No email/SCM   = Never send .lic files via email or store in Git/Jira; vault only                  │
│    Portal MFA     = Dell Licensing Portal requires MFA; enforce org-wide in portal settings           │
│    Named engineers = Limit FoD apply privilege to 2-3 storage engineers; document by name             │
│    Array RBAC     = Only Storage Admin role on array can import license keys; not Operator            │
│    CR required    = No FoD key applied without approved ITSM CR; prevents unauthorized changes        │
│    2-person rule  = FoD apply observed by second engineer; prevents unauthorized feature unlock       │
│    Offboard revoke = When storage engineer leaves, remove array RBAC and vault access immediately     │
│    Key rotation   = FoD keys do not rotate; protect the original; report loss to Dell licensing       │
│    Quarterly audit = Review portal history vs CMDB; detect unauthorized feature activation            │
│    Portal history = Dell Licensing Portal logs all key downloads; review for unauthorized access      │
│    CMDB diff      = Quarterly comparison of array active license list to CMDB; flag surprises         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="authentication/"><strong>Authentication</strong><span>SSO, LDAP, local accounts, and identity sources.</span></a>
<a class="kb-card" href="access-control/"><strong>Access Control</strong><span>Roles, permissions, and least privilege access.</span></a>
<a class="kb-card" href="encryption/"><strong>Encryption</strong><span>TLS certificate management and data encryption.</span></a>
<a class="kb-card" href="hardening/"><strong>Hardening</strong><span>Security baselines and compliance configuration.</span></a>
</div>
