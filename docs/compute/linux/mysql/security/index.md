---
tags:
  - linux
  - security
---
# MySQL / MariaDB — Security

<div class="kb-summary">
Access control, authentication, encryption, and hardening.

*Applies to: RHEL / Ubuntu LTS*
</div>

```text
┌───────────────────────────────────── MySQL — Security Reference ──────────────────────────────────────┐
│                                                                                                       │
│   Four security dimensions: access control, authentication, encryption, and hardening                 │
│   Secure a MySQL server by layering: network binding + account hygiene + TLS + audit logging          │
│   Minimum production baseline: no remote root, no anonymous users, TLS required, audit enabled        │
│                                                                                                       │
│   Access control                                                                                      │
│   GRANT/REVOKE at global, database, table, or column scope per user@host                              │
│   Roles (8.0+): group privileges into named sets; assign to multiple accounts                         │
│   Audit: SHOW GRANTS FOR 'user'@'host'; SELECT * FROM information_schema.USER_PRIVILEGES              │
│                                                                                                       │
│   Authentication                                                                                      │
│   Default plugin (8.0): caching_sha2_password; legacy clients may need mysql_native_password          │
│   SSL/TLS: REQUIRE SSL per account; REQUIRE X509 for mutual TLS                                       │
│   Password policy: validate_password component enforces length and complexity                         │
│                                                                                                       │
│   Encryption                                                                                          │
│   At rest: InnoDB TDE via keyring plugin; per-table or per-schema encryption                          │
│   In transit: require_secure_transport=ON rejects all non-TLS connections                             │
│   Backups: encrypt mysqldump output or use xtrabackup --encrypt                                       │
│                                                                                                       │
│   Key terms:                                                                                          │
│   user@host    = MySQL account scope; 'root'@'localhost' is different from 'root'@'%'                 │
│   TDE          = Transparent Data Encryption; encrypts InnoDB tablespace files on disk                │
│   caching_sha2 = MySQL 8.0 default auth plugin; stronger than legacy native_password                  │
│   validate_password = server component enforcing password complexity and rotation policy              │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-4">
  <a class="kb-card" href="access-control/">Access Control</a>
  <a class="kb-card" href="authentication/">Authentication</a>
  <a class="kb-card" href="encryption/">Encryption</a>
  <a class="kb-card" href="hardening/">Hardening</a>
</div>

