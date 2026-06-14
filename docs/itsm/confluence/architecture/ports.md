---
tags:
  - confluence
  - itsm
  - atlassian
  - networking
  - firewall
  - ports
---
# Confluence — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Confluence (Data Center, self-hosted). Covers web UI, Synchrony (collaborative editing), cluster, database, and SMTP.

*Applies to: Confluence Data Center 8.x*
</div>

## Inbound — Client Access

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 443 | TCP | All users | HTTPS — Confluence web UI and REST API (via reverse proxy) |
| 8090 | TCP | Internal clients | Confluence direct port (Tomcat) |
| 8091 | TCP | Users | Synchrony — collaborative editing websocket |

## Confluence Data Center Cluster

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 5701 | TCP | Confluence nodes | Hazelcast cluster (node membership and cache) |
| 25500 | TCP | Confluence nodes | Synchrony cluster communication |
| 5701 | UDP | Confluence nodes | Hazelcast multicast discovery |

## Confluence to Database

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 5432 | TCP | PostgreSQL | Confluence database (recommended) |
| 1433 | TCP | SQL Server | Confluence database (MSSQL) |

## Confluence Outbound Services

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 25 | TCP | SMTP relay | Email notifications |
| 443 | TCP | Marketplace, license server | Plugin/add-on downloads and licensing |
| 636/389 | TCP | Active Directory / LDAP | User directory |
| 88 | TCP/UDP | Active Directory | Kerberos SSO |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Users | Load balancer / Confluence | 443 | Web UI — Synchrony websocket also via 443 with proxy |
| Confluence nodes | Confluence nodes | 5701, 25500 | Cluster and Synchrony |
| Confluence | PostgreSQL / SQL | 5432 or 1433 | Database |
| Confluence | SMTP relay | 25 | Email |

## Verify

```bash
# From user — test Confluence web
curl -sk -o /dev/null -w "%{http_code}" https://<confluence-host>/

# From Confluence node — test DB
nc -zv <postgres-host> 5432

# From second node — test Hazelcast
nc -zv <peer-confluence-node> 5701

# From second node — test Synchrony
nc -zv <peer-confluence-node> 25500
```

## See also

- [Confluence — Architecture](how-it-works/)
- [Jira — Ports](../../jira/architecture/ports/)
