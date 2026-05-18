# vSAN — Security

<div class="kb-summary">
Security reference for VMware vSAN. Covers vCenter SSO authentication, role-based access control, data-at-rest encryption, KMS integration, and hardening baselines aligned to VMware security guidance and DISA STIGs.
</div>

```
vSAN SECURITY LAYERS

  ┌─────────────────────────────────────────────────────┐
  │  Identity & Access                                  │
  │  User/Service Account → vCenter SSO → RBAC role     │
  │  (AD / LDAP / SAML MFA → vSAN operations gated      │
  │   by cluster-level vCenter permission)              │
  └────────────────────────┬────────────────────────────┘
                           │
  ┌────────────────────────▼────────────────────────────┐
  │  Network Security                                   │
  │  ESXi Firewall → restrict SSH, management ports     │
  │  NIOC → vSAN traffic bandwidth reservation          │
  │  vSAN network: dedicated VLAN, MTU 9000             │
  └────────────────────────┬────────────────────────────┘
                           │
  ┌────────────────────────▼────────────────────────────┐
  │  Encryption                                         │
  │  Data-in-Transit: AES-256-GCM (host-to-host)        │
  │  Data-at-Rest (D@RE): AES-256-XTS per disk group    │
  │  Key chain: KMS → KEK (per host) → DEK (per DG)     │
  └────────────────────────┬────────────────────────────┘
                           │
  ┌────────────────────────▼────────────────────────────┐
  │  Hardening & Audit                                  │
  │  Host Profiles → enforce baseline, detect drift     │
  │  Syslog → SIEM (SSH logins, disk events, health)    │
  │  SCG / DISA STIG compliance checks                  │
  └─────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>SSO integration, identity sources, and local accounts.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Roles, permissions, and least privilege access.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>vSAN data-at-rest encryption and key management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines, compliance, and STIG configuration.</span>
</a>

</div>
