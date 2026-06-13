---
tags:
  - security
  - windows
---
# SQL Server — Security

<div class="kb-summary">
Access control, authentication, encryption, and hardening.

*Applies to: Windows Server 2019 / 2022*
</div>

```text
┌──────────────────────────────────────── SQL Server — Security ────────────────────────────────────────┐
│                                                                                                       │
│   Four security pillars: access control, authentication, encryption, and hardening                    │
│   Windows Authentication (Kerberos) is preferred; SQL logins used only when Windows auth is not       │
│   TDE encrypts data files at rest; Always Encrypted provides client-side column encryption            │
│                                                                                                       │
│   Sub-sections                                                                                        │
│   Access Control: logins vs users, server/database roles, GRANT/DENY, permission auditing             │
│   Authentication: Windows vs Mixed Mode, gMSA service accounts, AD group logins, password policy      │
│   Encryption: TDE (at-rest), Always Encrypted (column), TLS (in-transit), backup encryption           │
│   Hardening: disable xp_cmdshell/CLR, SQL Browser, sa account, audit logging, CIS controls            │
│                                                                                                       │
│   Key terms:                                                                                          │
│   TDE           = Transparent Data Encryption; encrypts .mdf/.ldf files and backups at rest           │
│   Always Encrypted = column-level encryption; key never leaves client; SQL Server sees ciphertext     │
│   gMSA          = Group Managed Service Account; AD-managed; auto-rotating password                   │
│   xp_cmdshell   = extended proc for OS commands; major attack surface; must be disabled               │
│   sysadmin      = server role with unrestricted access; limit to DBA accounts only                    │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-4">
  <a class="kb-card" href="access-control/">Access Control</a>
  <a class="kb-card" href="authentication/">Authentication</a>
  <a class="kb-card" href="encryption/">Encryption</a>
  <a class="kb-card" href="hardening/">Hardening</a>
</div>
