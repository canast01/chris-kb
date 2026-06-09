# PowerCLI — Security

<div class="kb-summary">
PowerCLI security: RBAC and role management, credential and certificate handling, service account hardening, and audit logging for vSphere automation.
</div>

```text
┌──────────────────────────────────── PowerCLI — Security Reference ────────────────────────────────────┐
│                                                                                                       │
│   PowerCLI security covers four areas: access control, authentication, encryption, and hardening      │
│   Automation service accounts must follow least-privilege; never use an admin account in scripts      │
│   All TLS connections must validate certificates in production (InvalidCertificateAction = Fail)      │
│                                                                                                       │
│   Access control                                                                                      │
│   Audit existing permissions: Get-VIPermission lists all role assignments per vCenter object          │
│   Create automation roles with minimum required privileges; scope to the smallest possible object     │
│   Detect permission sprawl: compare current role assignments against the automation account list      │
│                                                                                                       │
│   Authentication                                                                                      │
│   Credential storage: Store-VICredentialStoreItem saves encrypted credentials for unattended scripts  │
│   Certificate-based auth: available for VCSA API endpoints; requires certificate provisioning         │
│   Multi-session: $global:DefaultVIServers holds active connections; check before reconnecting         │
│                                                                                                       │
│   Encryption                                                                                          │
│   vSAN encryption: enable at datastore level with Set-VsanClusterConfiguration; key rotation cmdlets  │
│   VM encryption (VMcrypt): configure via SPBM encryption policy and KMS cluster assignment            │
│   Credential file encryption: Export-Clixml with secure string; machine-bound by default              │
│                                                                                                       │
│   Hardening                                                                                           │
│   Cert validation: Set-PowerCLIConfiguration -InvalidCertificateAction Fail                           │
│   Execution policy: Set-ExecutionPolicy RemoteSigned or AllSigned in production pipelines             │
│   Session audit: review vCenter event log for automation service account login and action events      │
│                                                                                                       │
│   Key terms:                                                                                          │
│   VIPermission            = vCenter permission: role + principal + entity + propagation flag          │
│   InvalidCertificateAction = Fail (prod) / Ignore (lab only) / Warn (default in older versions)       │
│   Store-VICredentialStoreItem = saves encrypted username+password bound to the target host name       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>RBAC roles, permission scoping, least-privilege automation accounts, and role auditing.</span>
</a>

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Credential storage, certificate validation, SSO integration, and token-based auth.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Session controls, connection security settings, script signing, and audit log review.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>vSAN encryption and key rotation, VM encryption (VMcrypt), KMS management, and TLS configuration.</span>
</a>

</div>
