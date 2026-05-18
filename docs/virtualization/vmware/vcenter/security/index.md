# vCenter — Security

<div class="kb-summary">
Security reference for VMware vCenter Server. Covers SSO authentication, identity sources, role-based access control, certificate management, and hardening aligned to VMware security guidance and DISA STIGs.
</div>

```
vCenter Security Architecture
════════════════════════════════════════════════════════

  Network Perimeter
  ┌────────────────────────────────────────────────────┐
  │  Firewall: :443 (API/UI), :5480 (VAMI), :22 (SSH) │
  │  Restrict to admin jump hosts and monitoring only  │
  └───────────────────────┬────────────────────────────┘
                          │
  Authentication Layer    ▼
  ┌────────────────────────────────────────────────────┐
  │  SSO (vsphere.local)                               │
  │  ┌──────────────┐   ┌─────────────────────────┐   │
  │  │ Local accts  │   │ AD / LDAPS identity src  │   │
  │  │ (break-glass)│   │ (named user accounts)    │   │
  │  └──────────────┘   └─────────────────────────┘   │
  │  ┌─────────────────────────────────────────────┐   │
  │  │ SAML (ADFS/Okta) ← MFA enforcement at IdP  │   │
  │  └─────────────────────────────────────────────┘   │
  └───────────────────────┬────────────────────────────┘
                          │
  Authorisation Layer     ▼
  ┌────────────────────────────────────────────────────┐
  │  RBAC: principal + role + inventory scope          │
  │  Administrator · VM Operator · Read-Only           │
  │  Custom roles (Backup Operator, NSX Integration)   │
  └───────────────────────┬────────────────────────────┘
                          │
  Encryption Layer        ▼
  ┌────────────────────────────────────────────────────┐
  │  Transit: TLS 1.2+ (all APIs, VAMI, LDAPS)         │
  │  At rest: VM Encryption (NKP / external KMS)       │
  │  Certs:   VMCA (internal CA) or enterprise CA      │
  └────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Local accounts, directory integration, MFA, and certificate-based auth.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>RBAC, roles, permissions, and service accounts.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Data-at-rest, data-in-transit, and key management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines, hardening guides, and compliance controls.</span>
</a>

</div>
