---
tags:
  - architecture
  - linux
---
# MySQL / MariaDB — Architecture

<div class="kb-summary">
MySQL/MariaDB architecture: primary-replica replication topology, Galera cluster design, InnoDB buffer pool sizing, binary log retention, and storage layout.

*Applies to: MySQL 8.x · MariaDB 10.x*
</div>

```text
┌────────────────────────────── MySQL — Relational Database Architecture ───────────────────────────────┐
│                                                                                                       │
│  Open-source RDBMS; InnoDB storage engine; primary-replica replication; MySQL                         │
│  Router for load balancing; InnoDB Cluster (Group Replication) for HA.                                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Engine Architecture              │  │               InnoDB Internals              │   │
│   │            InnoDB: default engine            │  │        Buffer pool: main memory cache       │   │
│   │          MyISAM: read-heavy legacy           │  │           Redo log: crash recovery          │   │
│   │          MEMORY: temp tables in RAM          │  │           Undo log: MVCC rollback           │   │
│   │            MVCC: concurrent reads            │  │          Doublewrite: write safety          │   │
│   │         ACID: transaction guarantees         │  │         Row locking: not table lock         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  InnoDB Buffer Pool should be 70-80% of available RAM for optimal performance.                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Replication Topologies            │  │              HA: InnoDB Cluster             │   │
│   │            Primary-Replica: async            │  │         Group Replication: 3+ nodes         │   │
│   │           GTID: global tx tracking           │  │          MySQL Router: conn routing         │   │
│   │          Semi-sync: 1 replica acked          │  │         MySQL Shell: admin interface        │   │
│   │         GTID auto-position: simpler          │  │          Auto-failover: Router sees         │   │
│   │         Binlog: base of replication          │  │          Paxos: consensus protocol          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Linux VMs or bare metal; local NVMe for data directory preferred; NFS for backups;                   │
│  separate disk for binlogs and redo logs; dedicated network for replication.                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  InnoDB         = default MySQL storage engine; ACID compliant; row locking                           │
│  Buffer Pool    = InnoDB memory cache for data and indexes; set to 70-80% RAM                         │
│  MVCC           = Multi-Version Concurrency Control; readers do not block writers                     │
│  GTID           = Global Transaction ID; unique per-transaction; simplifies failover                  │
│  Binlog         = binary log; records all changes; basis of replication                               │
│  Redo log       = InnoDB WAL; ensures crash recovery; innodb_log_files_in_group                       │
│  Group Replication= multi-primary or single-primary; Paxos consensus across nodes                     │
│  MySQL Router   = connection router; redirects writes to primary, reads to replicas                   │
│  MySQL Shell    = admin tool; configureCluster, addInstance, status checks                            │
│  Semi-sync      = primary waits for at least 1 replica to ACK before commit                           │
│  InnoDB Cluster = Group Replication + Router + Shell; HA solution for MySQL                           │
│  Doublewrite    = InnoDB write-safety buffer; prevents torn page on crash                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![MySQL Architecture Overview](../../../../assets/mysql-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="how-it-works/">How It Works</a>
  <a class="kb-card" href="design-standards/">Design Standards</a>
  <a class="kb-card" href="integrations/">Integrations</a>
</div>
