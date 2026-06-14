---
tags:
  - mysql
  - database
  - linux
  - networking
  - firewall
  - ports
---
# MySQL — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for MySQL and MySQL InnoDB Cluster. Covers client connections, X Protocol, Group Replication, and MySQL Shell admin.

*Applies to: MySQL 8.x Community / Enterprise*
</div>

## Inbound — Client Connections

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 3306 | TCP | Application servers, DBA workstations | MySQL classic protocol — standard SQL connections |
| 33060 | TCP | Application servers (X DevAPI clients) | MySQL X Protocol — document store, async queries |
| 33062 | TCP | Admin workstations | MySQL admin port — reserved for management connections even under max_connections limit |

## MySQL InnoDB Cluster / Group Replication (Node-to-Node)

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 3306 | TCP | Cluster members | Standard MySQL port used for group replication seed |
| 33061 | TCP | Cluster members | Group Replication internal communication |
| 6446 | TCP | MySQL Router → primary | MySQL Router write port |
| 6447 | TCP | MySQL Router → replicas | MySQL Router read port |

## Monitoring

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 9104 | TCP | Prometheus server | mysqld_exporter — MySQL metrics |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| App servers | MySQL | 3306 | Restrict to app server IPs only |
| Admin workstations | MySQL | 3306, 33062 | DBA access |
| Cluster nodes | Cluster nodes | 3306, 33061 | Group replication — bidirectional |
| Prometheus | MySQL | 9104 | Metrics scrape |

## Verify

```bash
# From app server
nc -zv <mysql-host> 3306

# From DBA workstation
mysql -h <mysql-host> -u root -p -e "SELECT @@version;"

# Cluster health check
mysqlsh admin@<cluster-host>:3306 -- cluster status
```

## See also

- [MySQL — Architecture](how-it-works/)
- [MySQL — Operations](../operations/)
- [Linux — Ports](../../architecture/ports/)
- [PostgreSQL — Ports](../../postgresql/architecture/ports/)
