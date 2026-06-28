---
tags:
  - postgresql
  - database
  - linux
  - networking
  - firewall
  - ports
---
# PostgreSQL — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for PostgreSQL. Covers client connections, replication (streaming and logical), pgBouncer connection pooler, and Patroni HA cluster.

*Applies to: PostgreSQL 14+ / Patroni 3.x*
</div>
![PostgreSQL — Ports and Network Requirements](../../../../assets/compute-linux-postgresql-architecture-ports.svg)

## Inbound — Client Connections

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 5432 | TCP | Application servers, DBA workstations | PostgreSQL standard client connections |
| 6432 | TCP | Application servers | pgBouncer connection pooler (if deployed in front of PostgreSQL) |

## Streaming Replication (Primary to Replica)

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 5432 | TCP | Replica → Primary | WAL streaming replication — replica connects to primary on 5432 |

## Patroni HA (Cluster Management)

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 8008 | TCP | Patroni nodes (and HAProxy health check) | Patroni REST API — leader election, health check |
| 2379 | TCP | Patroni → etcd cluster | etcd client port (consensus store for Patroni) |
| 2380 | TCP | etcd nodes ↔ etcd nodes | etcd peer replication |
| 5000 | TCP | App servers → HAProxy | HAProxy write VIP (primary) |
| 5001 | TCP | App servers → HAProxy | HAProxy read VIP (replica) |

## Monitoring

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 9187 | TCP | Prometheus server | postgres_exporter — PostgreSQL metrics |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| App servers | PostgreSQL / pgBouncer | 5432 or 6432 | Client connections |
| PostgreSQL replica | PostgreSQL primary | 5432 | Streaming replication |
| Patroni nodes | etcd | 2379 | Cluster consensus |
| etcd nodes | etcd nodes | 2380 | etcd peer replication |
| HAProxy health | Patroni | 8008 | Leader detection |
| Prometheus | PostgreSQL | 9187 | Metrics |

## Verify

```bash
# From app server
psql -h <postgres-host> -U appuser -d appdb -c "SELECT version();"

# Test pgBouncer
psql -h <postgres-host> -p 6432 -U appuser -d pgbouncer -c "SHOW POOLS;"

# Patroni cluster status
patronictl -c /etc/patroni/config.yml list

# Replication lag
psql -c "SELECT now() - pg_last_xact_replay_timestamp() AS replication_lag;"
```

## See also

- [PostgreSQL — Architecture](../how-it-works/)
- [PostgreSQL — Operations](../../operations/)
- [MySQL — Ports](../../mysql/architecture/ports.md)
- [Linux — Ports](../../architecture/ports.md)
