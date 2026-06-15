---
tags:
  - jira
  - itsm
  - atlassian
  - networking
  - firewall
  - ports
---
# Jira — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Jira (Data Center, self-hosted). Covers web UI, clustering, database, and SMTP.

*Applies to: Jira Data Center 9.x / Jira Software 9.x*
</div>

```text
┌─────────────────────────────────────── Itsm Jira Architecture ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Jira: Itsm Jira Architecture platform                             │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                     Management: Itsm Jira Architecture management console                     │   │
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
│    Physical: Itsm Jira Architecture infrastructure · management network · monitoring                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Jira               = Itsm Jira Architecture platform overview and core concepts                    │
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


## Inbound — Client Access

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 443 | TCP | All users (browser / API) | HTTPS — Jira web UI and REST API (via reverse proxy) |
| 8080 | TCP | Internal clients | Jira application direct port (behind reverse proxy on 443 externally) |
| 80 | TCP | Users | HTTP — redirects to 443 (if configured) |

## Jira Data Center Cluster (Node-to-Node)

| Port | Protocol | Between | Purpose |
|---|---|---|---|
| 40001 | TCP | Jira nodes | Ehcache cluster communication (cache replication) |
| 40011 | TCP | Jira nodes | Ehcache heartbeat |
| 5701 | TCP | Jira nodes | Hazelcast cluster (Jira DC 9.x+) |

## Jira to Database

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 5432 | TCP | PostgreSQL server | Jira database (recommended DB for DC) |
| 1433 | TCP | SQL Server | Jira database (Microsoft SQL Server) |

## Jira Outbound Services

| Port | Protocol | Destination | Purpose |
|---|---|---|---|
| 25 | TCP | SMTP relay | Email notifications (issue updates, watchlists) |
| 443 | TCP | Marketplace plugins, license server | Plugin downloads, license validation |
| 636/389 | TCP | Active Directory / LDAP | User directory authentication |
| 88 | TCP/UDP | Active Directory | Kerberos SSO |

## Firewall Zone Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Users | Load balancer / Jira | 443 | Web UI and API |
| Jira nodes | Jira nodes | 5701, 40001 | Cluster replication |
| Jira | PostgreSQL / SQL | 5432 or 1433 | Database |
| Jira | SMTP relay | 25 | Email |
| Jira | AD / LDAP | 636, 88 | Auth |

## Verify

```bash
# From user workstation — test Jira web
curl -sk -o /dev/null -w "%{http_code}" https://<jira-host>/

# From Jira node — test DB
nc -zv <postgres-host> 5432

# From Jira node — test SMTP
nc -zv <smtp-relay> 25

# From second Jira node — test cluster port
nc -zv <peer-jira-node> 5701
```

## See also

- [Jira — Architecture](how-it-works/)
- [Jira — Operations](../operations/)
- [Confluence — Ports](../../confluence/architecture/ports/)
