# ESXi — Security

<div class="kb-summary">
Security reference for VMware ESXi. Covers vCenter SSO authentication, lockdown mode, role-based access control, VM and vSAN encryption, and host hardening aligned to VMware security guidance and DISA STIGs.
</div>

```
ESXi Security Layers
┌────────────────────────────────────────────────────────┐
│  Network Perimeter                                     │
│  ├── Host-based firewall (esxcli network firewall)     │
│  └── SSH restricted to admin subnet by IP allowlist    │
├────────────────────────────────────────────────────────┤
│  Access Control                                        │
│  ├── Lockdown Mode (Normal / Strict)                   │
│  │   └── All mgmt via vCenter — no direct host access  │
│  ├── vCenter RBAC → roles propagated to ESXi           │
│  └── Local accounts: root + 1 break-glass only         │
├────────────────────────────────────────────────────────┤
│  Authentication                                        │
│  ├── vCenter SSO → AD identity source (preferred)      │
│  ├── Password policy: length, complexity, lockout      │
│  └── SSH key-based auth for break-glass access         │
├────────────────────────────────────────────────────────┤
│  Encryption                                            │
│  ├── VM Encryption (VMCA / NKP / external KMS)         │
│  ├── vSAN encryption (at-rest + in-transit)            │
│  ├── Encrypted vMotion (opportunistic / required)      │
│  └── UEFI Secure Boot + TPM 2.0 attestation            │
├────────────────────────────────────────────────────────┤
│  Audit & Compliance                                    │
│  ├── Syslog → SIEM (auth.log, shell.log, hostd.log)   │
│  ├── Host Profiles enforce baseline continuously       │
│  └── VMware SCG / CIS / DISA STIG alignment            │
└────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>SSO, LDAP, local accounts, and identity sources.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Roles, permissions, lockdown mode, and least privilege.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>VM encryption, vSAN encryption, and key management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Host hardening, STIG compliance, and security baselines.</span>
</a>

</div>
