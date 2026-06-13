---
tags:
  - pure
  - security
---
# FlashBlade — Security


<div class="kb-summary">
FlashBlade — Security reference: Authentication, Access Control, Encryption, Hardening.
</div>

FlashBlade Security Layers
```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Identity & Auth                                                                                      │
│  ├── SAML SSO for GUI                                                                                 │
│  ├── AD for SMB authentication + NFS Kerberos                                                         │
│  └── API tokens for automation                                                                        │
├──────────────────────────────────────────────────────────┤
│  RBAC                                                                                                 │
│  array_admin │ storage_admin │ ops_admin │ readonly                                                   │
├──────────────────────────────────────────────────────────┤
│  Protocol Controls                                                                                    │
│  ├── NFS export policy (allowed IPs / CIDR)                                                           │
│  ├── SMB share ACLs (AD groups)                                                                       │
│  └── S3 bucket policies + IAM-style keys                                                              │
├──────────────────────────────────────────────────────────┤
│  Data at Rest                                                                                         │
│  └── XTS-AES-256 (always-on, cannot be disabled)                                                      │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="authentication/"><strong>Authentication</strong><span>SSO, LDAP, local accounts, and identity sources.</span></a>
<a class="kb-card" href="access-control/"><strong>Access Control</strong><span>Roles, permissions, and least privilege access.</span></a>
<a class="kb-card" href="encryption/"><strong>Encryption</strong><span>TLS certificate management and data encryption.</span></a>
<a class="kb-card" href="hardening/"><strong>Hardening</strong><span>Security baselines and compliance configuration.</span></a>
</div>

