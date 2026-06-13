# Nutanix — Security

<div class="kb-summary">
Security configuration for Nutanix HCI — OS hardening, SSH lockdown, Active Directory integration, RBAC access control, and data-at-rest encryption. Aligned with the Nutanix Security Configuration Guide.

*Applies to: AOS 6.x · AHV*
</div>

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                       NUTANIX SECURITY LAYERS                                                         │
│                                                                                                       │
│  LAYER 1: PERIMETER                                                                                   │
│  ──────────────────────────────────────────────────────────────                                       │
│  Cluster Lockdown (SSH key-only) · Port firewall (iptables)                                           │
│  TLS 1.2+ only · Custom SSL cert on Prism                                                             │
│                                                                                                       │
│  LAYER 2: IDENTITY                                                                                    │
│  ──────────────────────────────────────────────────────────────                                       │
│  AD/LDAP integration · SAML/SSO (Prism Central)                                                       │
│  MFA via IdP · Local account lockout policy                                                           │
│                                                                                                       │
│  LAYER 3: AUTHORISATION                                                                               │
│  ──────────────────────────────────────────────────────────────                                       │
│  PE built-in roles (Admin/Viewer/UserAdmin)                                                           │
│  PC custom RBAC · Categories-based VM scope · Projects                                                │
│                                                                                                       │
│  LAYER 4: DATA                                                                                        │
│  ──────────────────────────────────────────────────────────────                                       │
│  AES-256 data-at-rest encryption (software or SED)                                                    │
│  Native KMS or KMIP (Thales, IBM SKLM, HashiCorp Vault)                                               │
│  TLS for replication traffic                                                                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid">
  <a class="kb-card" href="hardening/">
    <strong>Hardening</strong>
    <span>CVM OS hardening, SSH lockdown, password policy, TLS configuration, port exposure, and Nutanix SCG alignment.</span>
  </a>
  <a class="kb-card" href="authentication/">
    <strong>Authentication</strong>
    <span>AD/LDAP integration, SAML/SSO for Prism Central, local account management, and session timeout settings.</span>
  </a>
  <a class="kb-card" href="access-control/">
    <strong>Access Control</strong>
    <span>Prism Element built-in roles, Prism Central custom RBAC, categories-based VM access, and projects.</span>
  </a>
  <a class="kb-card" href="encryption/">
    <strong>Encryption</strong>
    <span>Data-at-rest encryption (software and SED), native key manager, KMIP external KMS, and key rotation.</span>
  </a>
</div>
