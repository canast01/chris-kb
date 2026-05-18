# FlashArray — Security

```
FlashArray Security Layers
┌──────────────────────────────────────────────────────────┐
│  Identity & Auth                                         │
│  ├── SAML SSO (Okta / Azure AD) → MFA enforced           │
│  ├── AD/LDAP group → role mapping                        │
│  └── API tokens for automation (storage_admin / readonly)│
├──────────────────────────────────────────────────────────┤
│  RBAC                                                    │
│  array_admin │ storage_admin │ ops_admin │ readonly      │
├──────────────────────────────────────────────────────────┤
│  Network Controls                                        │
│  ├── Management on dedicated VLAN (SSH + HTTPS only)     │
│  └── Replication on dedicated VLAN (TLS)                 │
├──────────────────────────────────────────────────────────┤
│  Data at Rest                                            │
│  └── AES-256-XTS (NVMe SEDs, always-on, hardware)        │
├──────────────────────────────────────────────────────────┤
│  Immutability                                            │
│  └── SafeMode — Pure Support required to destroy snaps   │
└──────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="authentication/"><strong>Authentication</strong><span>SSO, LDAP, local accounts, and identity sources.</span></a>
<a class="kb-card" href="access-control/"><strong>Access Control</strong><span>Roles, permissions, and least privilege access.</span></a>
<a class="kb-card" href="encryption/"><strong>Encryption</strong><span>TLS certificate management and data encryption.</span></a>
<a class="kb-card" href="hardening/"><strong>Hardening</strong><span>Security baselines and compliance configuration.</span></a>
</div>
