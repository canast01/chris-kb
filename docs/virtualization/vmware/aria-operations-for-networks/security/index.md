# Aria Ops for Networks — Security

```
┌──────────── Aria Networks Security Overview ───────────────────────────────────┐
│                                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐    │
│  │Authentication│  │Access Control│  │  Encryption  │  │   Hardening     │     │
│  │ Local admin  │  │  Role-based  │  │  TLS 1.2/1.3 │  │  SSH hardening  │     │
│  │ LDAP/AD      │  │  Super Admin │  │  CA-signed   │  │  iptables ACL   │     │
│  │ SAML/vIDM    │  │  Net Engineer│  │  cert        │  │  API token      │     │
│  │ API tokens   │  │  Sec Engineer│  │  AES-256     │  │  hygiene        │     │
│  └──────────────┘  │  Auditor     │  │  credentials │  │  Syslog/SIEM   │      │
│                    └──────────────┘  └──────────────┘  └──────────────────┘    │
└────────────────────────────────────────────────────────────────────────────────┘
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
  <span>Data encryption and certificate management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines and compliance configuration.</span>
</a>

</div>
