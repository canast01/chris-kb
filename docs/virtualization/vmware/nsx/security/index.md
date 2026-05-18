# NSX — Security

<div class="kb-summary">
Security reference for VMware NSX. Covers NSX Manager authentication, role-based access control, data-in-transit encryption, certificate management, and DFW hardening baselines.
</div>

```
┌─────────────────────────────────────────────────────────────┐
│                 NSX Security Posture                        │
├───────────────┬──────────────┬──────────────┬──────────────┤
│     RBAC      │     Auth     │  Encryption  │  Hardening   │
├───────────────┼──────────────┼──────────────┼──────────────┤
│ Roles bound   │ Local +      │ TLS 1.2+     │ API/SSH      │
│ to AD groups  │ LDAP/AD +    │ for mgmt     │ jump-host    │
│               │ cert-based   │ plane        │ only         │
│ enterprise_   │ principal ID │              │              │
│ admin /       │              │ IPsec option │ Default deny │
│ network_eng / │ Password     │ for Geneve   │ DFW rule     │
│ security_admin│ policy: 20+  │ overlay      │ 65535=DROP   │
│ operator /    │ chars, 90d   │              │              │
│ auditor       │ max, lockout │ AES-256      │ Syslog TLS   │
│               │              │ backup       │ → SIEM       │
│ Audit: GET    │ Auth events  │ passphrase   │              │
│ /aaa/role-    │ → audit.log  │              │ Cert expiry  │
│ bindings      │ → SIEM       │              │ monitoring   │
└───────────────┴──────────────┴──────────────┴──────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>SSO integration, local accounts, and API authentication.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Roles, permissions, and least privilege access.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Data-in-transit encryption and certificate management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines, DFW policy, and compliance.</span>
</a>

</div>
