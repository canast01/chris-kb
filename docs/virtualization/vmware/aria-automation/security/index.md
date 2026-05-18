# Aria Automation — Security

```
┌─────────────────────────────────────────────────────────────┐
│         Aria Automation Security Overview                   │
├──────────────────────┬──────────────────────────────────────┤
│  Authentication      │  Access Control                      │
│  VIDM SSO (SAML)     │  Org: Administrator / Member         │
│  AD/LDAP via VIDM    │  Project: Owner / Member / Viewer    │
│  Bearer token (8h)   │  AD groups → project roles           │
│  Local: System Domain│  Approval policies per project       │
├──────────────────────┼──────────────────────────────────────┤
│  Encryption          │  Hardening                           │
│  TLS 1.2/1.3 (UI/API)│  CA cert replaces self-signed        │
│  Encrypted Prop Grps │  SSH mgmt-only · VAMI firewalled     │
│  Vault integration   │  Least-privilege service account     │
│  Storage-layer at-   │  Syslog → vRLI/SIEM · Audit API      │
│  rest encryption     │  Patch via LCM (critical: urgent)    │
└──────────────────────┴──────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>SSO, Workspace ONE Access, and identity sources.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Project-based RBAC, roles, and least privilege access.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>TLS certificates, secrets management, and Vault integration.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines and compliance configuration.</span>
</a>

</div>
