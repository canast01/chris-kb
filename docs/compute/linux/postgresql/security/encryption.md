---
tags:
  - linux
  - security
---
# PostgreSQL — Encryption

<div class="kb-summary">
PostgreSQL encryption — SSL/TLS for connections, pgcrypto for column-level encryption, transparent data encryption options, and WAL/backup encryption.

*Applies to: RHEL / Ubuntu LTS*
</div>

```text
┌────────────────────────────────────── Compute Linux Postgresql ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            Linux: Compute Linux Postgresql platform                           │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                    Management: Compute Linux Postgresql management console                    │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Compute Linux Postgresql infrastructure · management network · monitoring                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Linux              = Compute Linux Postgresql platform overview and core concepts                  │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## SSL/TLS for Connections

PostgreSQL uses OpenSSL for SSL. Generated automatically during `initdb` on most distributions.

```ini
# postgresql.conf
ssl = on
ssl_cert_file = 'server.crt'
ssl_key_file = 'server.key'
ssl_ca_file = 'root.crt'
ssl_min_protocol_version = 'TLSv1.2'
```

```bash
# Verify SSL is active
psql -U postgres -c "SHOW ssl;"
# Confirm connection is encrypted
psql -U appuser -h db.example.com -d app_prod -c "SELECT ssl, version, cipher FROM pg_stat_ssl WHERE pid = pg_backend_pid();"
```

## Require SSL for All Connections

```text
# pg_hba.conf — use hostssl instead of host
hostssl  all  all  0.0.0.0/0  scram-sha-256
```

## pgcrypto — Column-Level Encryption

```sql
-- Enable extension
CREATE EXTENSION pgcrypto;

-- Encrypt at insert
INSERT INTO sensitive (data) VALUES (pgp_sym_encrypt('secret', 'key'));

-- Decrypt at query
SELECT pgp_sym_decrypt(data, 'key') FROM sensitive;

-- Hash (one-way, for passwords)
INSERT INTO users (password_hash) VALUES (crypt('userpassword', gen_salt('bf', 12)));
-- Verify
SELECT * FROM users WHERE password_hash = crypt('userpassword', password_hash);
```

## WAL Encryption

PostgreSQL does not have native WAL encryption. Options:
- **pgBackRest**: supports `--cipher-type=aes-256-cbc` for backup and WAL archive encryption
- **OS-level**: encrypt the WAL archive destination (encrypted filesystem or S3 SSE)
- **Transparent Filesystem Encryption**: LUKS on the PostgreSQL data partition

## Transparent Data Encryption

Native TDE is available in PostgreSQL 17+ and commercial forks (Percona, EnterpriseDB). For PostgreSQL 16 and earlier:
- Use OS-level disk encryption (LUKS/BitLocker)
- Store data on encrypted cloud volumes (AWS EBS, Azure Managed Disk)

---

## See also

- [Postgresql — Hardening](hardening/)
- [Postgresql — Authentication](authentication/)
- [Postgresql — Access Control](access-control/)
