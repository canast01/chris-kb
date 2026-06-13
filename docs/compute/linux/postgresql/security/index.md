---
tags:
  - linux
  - security
---
# PostgreSQL — Security

<div class="kb-summary">
Access control, authentication, encryption, and hardening.
</div>

```text
┌──────────────────────────────────────── PostgreSQL — Security ────────────────────────────────────────┐
│                                                                                                       │
│   Four security pillars: access control, authentication, encryption, and hardening                    │
│   pg_hba.conf controls client authentication; evaluated top-to-bottom, first match wins               │
│   scram-sha-256 is the recommended authentication method for all production deployments               │
│                                                                                                       │
│   Sub-sections                                                                                        │
│   Access Control: role-based permissions, GRANT/REVOKE, row-level security (RLS)                      │
│   Authentication: pg_hba.conf rules, scram-sha-256, LDAP/AD integration, SSL certificates             │
│   Encryption: TLS in transit, pgcrypto for column-level encryption, WAL encryption                    │
│   Hardening: minimal superuser use, firewall rules, audit logging, pg_audit extension                 │
│                                                                                                       │
│   Key terms:                                                                                          │
│   pg_hba.conf   = host-based authentication config; controls who can connect and how                  │
│   scram-sha-256 = salted challenge-response auth; replaces md5; required for PCI/SOC2                 │
│   RLS           = Row-Level Security; restricts row visibility per role within a table                │
│   pg_audit      = extension for detailed SQL audit logging; records DDL and object access             │
│   superuser     = PostgreSQL superuser bypasses all access controls; must be restricted               │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-4">
  <a class="kb-card" href="access-control/">Access Control</a>
  <a class="kb-card" href="authentication/">Authentication</a>
  <a class="kb-card" href="encryption/">Encryption</a>
  <a class="kb-card" href="hardening/">Hardening</a>
</div>
