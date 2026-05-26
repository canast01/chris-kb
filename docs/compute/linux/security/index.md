# Linux — Security


```
┌────────────────────────────────────────── Linux — Security ───────────────────────────────────────────┐
│                                                                                                       │
│  Linux security layers: access control, authentication, encryption, and hardening.                    │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Access Control       │  │        Authentication       │  │          Hardening          │   │
│   │       DAC: chmod/chown      │  │      SSH key-based auth     │  │    Patch: yum/apt update    │   │
│   │    MAC: SELinux/AppArmor    │  │     PAM: pluggable auth     │  │    Firewall: iptables/nft   │   │
│   │  sudo: privilege escalation │  │      SSSD: AD/LDAP join     │  │   CIS benchmark: baseline   │   │
│   │    ACLs: getfacl/setfacl    │  │      MFA: TOTP via PAM      │  │   auditd: syscall logging   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Physical or virtual server · TPM chip · UEFI Secure Boot · HSM (optional)                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  DAC          = Discretionary Access Control; owner sets permissions (chmod/chown)                    │
│  MAC          = Mandatory Access Control; kernel enforces labels (SELinux/AppArmor)                   │
│  SELinux      = Security-Enhanced Linux; type enforcement, context labels                             │
│  AppArmor     = path-based MAC; simpler than SELinux; default on Ubuntu/Debian                        │
│  PAM          = Pluggable Authentication Modules; auth pipeline for login/sudo                        │
│  SSSD         = System Security Services Daemon; integrates with AD/LDAP                              │
│  sudo         = run command as another user (usually root); logged in /var/log/secure                 │
│  auditd       = kernel audit subsystem; logs file access, syscalls, user actions                      │
│  ACL          = Access Control List; per-user/group permissions beyond owner/group                    │
│  CIS          = Center for Internet Security; publishes Linux hardening benchmarks                    │
│  Secure Boot  = UEFI feature verifying bootloader signature before execution                          │
│  TPM          = Trusted Platform Module; hardware for key storage and measured boot                   │
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
