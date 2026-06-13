---
tags:
  - commvault
  - security
---
# Commvault — Security



<div class="kb-summary">
Commvault hardening — RBAC, encryption keys, audit logging, CommServe access control, and network security configuration.
</div>

```text
┌─────────────────────────────── Commvault Security — Controls Overview ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                    Commvault Security Model                                   │   │
│   │            Defence-in-depth: transport encryption, RBAC, MFA, hardening, audit logs           │   │
│   │             All component communications use TLS 1.2+ with mutual certificate auth            │   │
│   │          RBAC: roles limit access to CommCell objects (clients, policies, libraries)          │   │
│   │                Data encryption: AES-256 for backup data at rest and in transit                │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Four security domains: access control, authentication, encryption, hardening                       │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Access Control    │     Authentication    │       Encryption      │       Hardening       │   │
│   │       RBAC roles      │    Local + AD auth    │      AES-256 data     │    Minimal install    │   │
│   │     CommCell users    │       MFA (TOTP)      │     TLS 1.2+ comms    │     Host firewall     │   │
│   │      User groups      │        SAML SSO       │     Key management    │    No unneeded svc    │   │
│   │    Object security    │    Cert-based auth    │    FIPS 140-2 mode    │     Audit logging     │   │
│   │    Least privilege    │    Session timeout    │    Immutable copies   │    SIEM forwarding    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  CommServe hardened: minimal OS install, host firewall (only ports 8400/8401/443 open)                │
│  Certificate PKI: internal CA issues CommCell certs; rotate annually                                  │
│  Network: CommServe and MAs on dedicated backup VLAN, not directly reachable from clients             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RBAC           = Role-Based Access Control; CommCell roles define allowed operations                 │
│  CommCell User  = Local user account in CommServe database (not OS/AD user)                           │
│  AD Integration = CommServe can authenticate users against Active Directory LDAP                      │
│  SAML SSO       = SAML 2.0 federation; allows IdP-based login to Command Center                       │
│  MFA            = Multi-Factor Authentication; TOTP-based for CommCell Console login                  │
│  AES-256        = Encryption algorithm for backup data; key managed by CommServe                      │
│  FIPS 140-2     = US government crypto standard; Commvault supports FIPS mode                         │
│  TLS Mutual     = Both client and server present certificates for authentication                      │
│  Immutable Copy = Backup copy protected from deletion by WORM or Object Lock                          │
│  Audit Trail    = CommServe log of all user actions; forwarded to SIEM via syslog                     │
│  Object Security= Per-object permissions in CommCell (client, policy, library level)                  │
│  Key Manager    = CommServe service managing encryption key lifecycle and escrow                      │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-4">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>2FA, SAML, TOTP, and CyberArk credential management.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>RBAC roles, user groups, AD integration, and audit trail.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Backup encryption, immutable repositories, and key management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Network security, port restrictions, and hardening checklist.</span>
</a>

</div>
