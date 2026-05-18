# VCF — Security

<div class="kb-summary">
Security reference for VMware Cloud Foundation. Covers SDDC Manager authentication, role-based access control, certificate and key management, and hardening baselines across the full VCF stack.
</div>

```
VCF Security Architecture
┌─────────────────────────────────────────────────────┐
│  Identity Plane                                     │
│  Active Directory ──► SDDC Manager SSO identity     │
│                  ──► vCenter identity source        │
│                  ──► NSX Manager identity source    │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│  Access Control (RBAC)                              │
│                                                     │
│  SDDC Manager roles:                                │
│    ADMIN → full lifecycle + security access         │
│    OPERATOR → health/tasks; no credentials          │
│    VIEWER → read-only dashboards                    │
│                                                     │
│  NSX roles: Enterprise Admin · Network Eng          │
│             Security Eng · Auditor                  │
│                                                     │
│  vCenter: AD group → vCenter Global Permissions     │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│  Certificate Management (SDDC Manager)              │
│  VMCA (embedded) or third-party CA                  │
│  Rotate order: SDDC Mgr → vCenter → NSX → ESXi      │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│  Network Isolation                                  │
│  Management traffic ─► management network only      │
│  SDDC Manager UI (443) ─► jump-host CIDR only       │
│  Syslog ──► SIEM (TLS 6514)                         │
└─────────────────────────────────────────────────────┘
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
