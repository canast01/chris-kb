# Aria Ops for Logs — Security

```
┌─────────────────────────────────────────────────────────────┐
│         Aria Ops for Logs Security Overview                 │
├──────────────────────┬──────────────────────────────────────┤
│  Authentication      │  Access Control                      │
│  Local / AD (LDAPS)  │  Super Admin / Admin / User          │
│  VIDM (LCM-managed)  │  AD groups mapped to roles           │
│  HTTP Basic (API)    │  Local: break-glass only             │
│  No token; per-call  │  Highest role wins if multi-group    │
├──────────────────────┼──────────────────────────────────────┤
│  Encryption          │  Hardening                           │
│  TLS 1.2/1.3 UI/API  │  CA cert (no self-signed)            │
│  cfapi TLS :9543     │  LDAPS only (block :389)             │
│  ESXi UDP 514 no TLS │  SSH: mgmt network CIDR              │
│  Storage-layer at-   │  TLS 1.0/1.1 disabled                │
│  rest (vSAN/SAN)     │  Syslog → SIEM for audit             │
└──────────────────────┴──────────────────────────────────────┘
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
  <span>TLS certificate management and log data encryption.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines and compliance configuration.</span>
</a>

</div>
