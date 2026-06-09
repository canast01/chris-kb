# MySQL / MariaDB

<div class="kb-summary">
MySQL and MariaDB relational database for Linux — InnoDB, replication, backup, HA.
</div>

```text
┌─────────────────────────────────── MySQL / MariaDB — Reference Hub ───────────────────────────────────┐
│                                                                                                       │
│   MySQL and MariaDB relational databases on Linux — InnoDB storage engine, replication, and HA        │
│   Five sections: architecture, deploy, operations, security, and troubleshooting                      │
│   Production deployments require HA topology, backup strategy, and hardened auth before go-live       │
│                                                                                                       │
│   Architecture                                                                                        │
│   InnoDB engine: ACID-compliant, row-level locking, clustered primary key index, redo/undo logs       │
│   HA topologies: async replication, semi-sync, Group Replication, InnoDB Cluster, ProxySQL            │
│   Integrations: Prometheus (mysqld_exporter), PMM, ProxySQL, Orchestrator, pt-toolkit                 │
│                                                                                                       │
│   Operations                                                                                          │
│   Health checks: replication lag, thread counts, InnoDB buffer pool hit rate, slow query log          │
│   Backup: mysqldump (logical), xtrabackup (physical hot backup), binlog-based PITR                    │
│   Upgrade path: one major version at a time (5.7 → 8.0 → 8.4); always run upgrade checker first       │
│                                                                                                       │
│   Security                                                                                            │
│   Auth plugins: caching_sha2_password (8.0 default), mysql_native_password, auth_socket               │
│   Access control: GRANT/REVOKE per user@host, roles, privilege hierarchy, mysql_audit plugin          │
│   Hardening: disable remote root, remove anonymous users, enforce SSL, set password policy            │
│                                                                                                       │
│   Key terms:                                                                                          │
│   InnoDB        = MySQL default storage engine; ACID, row-level locks, MVCC                           │
│   Binlog        = binary log; records all changes; used for replication and PITR recovery             │
│   GTID          = Global Transaction ID; uniquely identifies each committed transaction in the binlog │
│   Semi-sync     = replication mode where primary waits for at least one replica ACK before committing │
│   ProxySQL      = connection proxy; transparent read/write split and failover routing                 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-5">
  <a class="kb-card" href="architecture/">Architecture</a>
  <a class="kb-card" href="deploy/">Deploy</a>
  <a class="kb-card" href="operations/">Operations</a>
  <a class="kb-card" href="security/">Security</a>
  <a class="kb-card" href="troubleshooting/">Troubleshooting</a>
</div>
