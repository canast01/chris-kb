# Linux — Security

```
┌───────────────────────────────────────────────────────┐
│               Linux Security Layers                   │
├───────────────────────────────────────────────────────┤
│  Authentication: PAM → SSSD → AD/LDAP → sudo          │
│  SSH: pubkey only, no root, fail2ban / pam_faillock    │
├───────────────────────────────────────────────────────┤
│  Access Control                                       │
│  ┌─────────────┬──────────────┬──────────────────┐    │
│  │  POSIX ACLs │  SELinux     │  AppArmor        │    │
│  │  chown/chmod│  contexts    │  profiles        │    │
│  └─────────────┴──────────────┴──────────────────┘    │
├───────────────────────────────────────────────────────┤
│  Network: firewalld (zones) → nftables → kernel       │
├───────────────────────────────────────────────────────┤
│  Encryption: LUKS (disk) │ TLS (services) │ GPG       │
├───────────────────────────────────────────────────────┤
│  Audit: auditd → /var/log/audit/audit.log             │
└───────────────────────────────────────────────────────┘
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
