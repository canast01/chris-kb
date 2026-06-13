---
tags:
  - security
  - vcf
  - vmware
---
# VCF — Security

<div class="kb-summary">
Security reference for VMware Cloud Foundation. Covers SDDC Manager authentication, role-based access control, certificate and key management, and hardening baselines across the full VCF stack.

*Applies to: VCF 4.x / 5.x*
</div>

```text
┌─────────────────────────────────────────── VCF — Security ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       SDDC Manager RBAC with admin/viewer roles; Identity Manager SSO across all domains      │   │
│   │      Component password policy via SoS; audit events logged in SDDC Manager activity log      │   │
│   │      vSAN encryption per domain with KMS; NSX TLS fabric for all inter-component traffic      │   │
│   │    Certificate management: SDDC Manager rotates certs for vCenter, NSX, and SDDC components   │   │
│   │  Break-glass admin account for emergency access; credential vault for service account storage │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication gates VCF access · RBAC scopes management · encryption protects domain data at rest │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │       Identity Mgr SSO      │  │      SDDC roles: admin      │  │       vSAN encr/domain      │   │
│   │         AD/LDAP intg        │  │      SDDC roles: viewer     │  │        NSX TLS fabric       │   │
│   │        API token auth       │  │        NSX+vCtr RBAC        │  │        vCtr cert mgmt       │   │
│   │      Break-glass admin      │  │       Domain-level acc      │  │       SDDC cert rotate      │   │
│   │       User management       │  │         Audit events        │  │       Credential vault      │   │
│   │      SDDC Manager auth      │  │       Password policy       │  │          KMS config         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Auth controls who accesses VCF · RBAC limits domain scope                                          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Auth       │   Access Ctrl    │     Encryption    │    Hardening     │      Audit       │   │
│   │   Identity Mgr   │    SDDC admin    │    vSAN encrypt   │  Cert rotation   │   SDDC events    │   │
│   │     AD/LDAP      │   SDDC viewer    │      NSX TLS      │ Password policy  │  NSX audit log   │   │
│   │    API tokens    │  Domain access   │    vCenter cert   │    KMS config    │  vCenter events  │   │
│   │   Break-glass    │ Least privilege  │     SDDC cert     │     SoS scan     │   SIEM forward   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 servers · TPM 2.0 · NVMe/SSD (vSAN) · PCIe NICs · Key Management Server · OOB network            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SDDC Manager RBAC = Admin and Viewer roles in SDDC Manager; controls domain and lifecycle access     │
│  Identity Manager  = VMware vIDM provides SSO across VCF vCenter, NSX, and SDDC Manager UIs           │
│  Workload domain isolation = Each domain has independent vCenter, NSX, and access control boundaries  │
│  SoS password rotation = SDDC Manager rotates all component passwords via SoS on schedule             │
│  vSAN encryption   = Per-domain data-at-rest encryption using KMS-managed keys; enabled per policy    │
│  NSX TLS           = All NSX management plane traffic encrypted with TLS; cert managed by SDDC Mgr    │
│  Certificate rotation = SDDC Manager renews certificates for all VCF components automatically         │
│  API token         = SDDC Manager REST API bearer token; scoped to user role and domain               │
│  Break-glass account = Emergency local admin in SDDC Manager; used when SSO is unavailable            │
│  KMS/KMIP          = External Key Management Server; manages vSAN and VM encryption keys via KMIP     │
│  Audit events      = SDDC Manager logs all user and system actions for compliance review              │
│  Credential vault  = SDDC Manager stores all component service account passwords securely             │
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
  <span>Data encryption, key management, and TLS configuration.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines, compliance, and STIG configuration.</span>
</a>

</div>

