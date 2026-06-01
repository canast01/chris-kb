# Linux — Security



<div class="kb-summary">
Linux — Security reference.
</div>

```
┌────────────────────────────────────── Linux — Security Overview ──────────────────────────────────────┐
│                                                                                                       │
│  Linux security spans access control, authentication, encryption, and system hardening.               │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Access Control       │  │        Authentication       │  │          Hardening          │   │
│   │       DAC: chmod/chown      │  │          PAM stack          │  │        CIS Benchmarks       │   │
│   │         MAC: SELinux        │  │         SSH key auth        │  │       sysctl hardening      │   │
│   │        RBAC via sudo        │  │          MFA / OTP          │  │       Minimal packages      │   │
│   │      File capabilities      │  │       LDAP / Kerberos       │  │        Kernel params        │   │
│   │        ACLs (setfacl)       │  │        Audit logging        │  │        auditd / AIDE        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86-64 servers · TPM chip · hardware HSM · NIC · locked server room                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  DAC         = Discretionary Access Control; owner sets permissions on resources                      │
│  MAC         = Mandatory Access Control; policy enforced by OS, overrides DAC                         │
│  SELinux     = Security-Enhanced Linux; label-based MAC built into the kernel                         │
│  PAM         = Pluggable Authentication Modules; auth pipeline for Linux services                     │
│  capability  = Fine-grained privilege subdivision; alternative to full root access                    │
│  ACL         = Access Control List; per-user/group permissions beyond rwx triplet                     │
│  sudo        = Delegated privilege escalation controlled by /etc/sudoers policy                       │
│  TPM         = Trusted Platform Module; hardware root of trust for key storage                        │
│  auditd      = Linux audit daemon; records system calls and security events                           │
│  AIDE        = Advanced Intrusion Detection Environment; file integrity monitor                       │
│  CIS         = Center for Internet Security; publishes OS hardening benchmarks                        │
│  sysctl      = Runtime kernel parameter tuning; /etc/sysctl.conf persists settings                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────────── Linux — Security Overview ──────────────────────────────────────┐
│                                                                                                       │
│  Linux security spans access control, authentication, encryption, and system hardening.               │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Access Control       │  │        Authentication       │  │          Hardening          │   │
│   │       DAC: chmod/chown      │  │          PAM stack          │  │        CIS Benchmarks       │   │
│   │         MAC: SELinux        │  │         SSH key auth        │  │       sysctl hardening      │   │
│   │        RBAC via sudo        │  │          MFA / OTP          │  │       Minimal packages      │   │
│   │      File capabilities      │  │       LDAP / Kerberos       │  │        Kernel params        │   │
│   │        ACLs (setfacl)       │  │        Audit logging        │  │        auditd / AIDE        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86-64 servers · TPM chip · hardware HSM · NIC · locked server room                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  DAC         = Discretionary Access Control; owner sets permissions on resources                      │
│  MAC         = Mandatory Access Control; policy enforced by OS, overrides DAC                         │
│  SELinux     = Security-Enhanced Linux; label-based MAC built into the kernel                         │
│  PAM         = Pluggable Authentication Modules; auth pipeline for Linux services                     │
│  capability  = Fine-grained privilege subdivision; alternative to full root access                    │
│  ACL         = Access Control List; per-user/group permissions beyond rwx triplet                     │
│  sudo        = Delegated privilege escalation controlled by /etc/sudoers policy                       │
│  TPM         = Trusted Platform Module; hardware root of trust for key storage                        │
│  auditd      = Linux audit daemon; records system calls and security events                           │
│  AIDE        = Advanced Intrusion Detection Environment; file integrity monitor                       │
│  CIS         = Center for Internet Security; publishes OS hardening benchmarks                        │
│  sysctl      = Runtime kernel parameter tuning; /etc/sysctl.conf persists settings                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>PAM, SSH keys, sudo, and authentication configuration.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Users, groups, file permissions, and SELinux/AppArmor.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Disk encryption, TLS, and secure communication.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines, CIS benchmarks, and compliance.</span>
</a>

</div>
