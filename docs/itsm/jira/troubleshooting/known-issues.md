---
tags:
  - troubleshooting
  - jira
  - itsm
  - known-issues
---
# Jira — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Jira Data Center bugs, error codes, and workarounds covering cluster health, database connectivity, and indexing.

*Applies to: Jira Data Center 9.x*
</div>

```text
┌────────────────────────────────────── Itsm Jira Troubleshooting ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            Jira: Itsm Jira Troubleshooting platform                           │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                    Management: Itsm Jira Troubleshooting management console                   │   │
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
│    Physical: Itsm Jira Troubleshooting infrastructure · management network · monitoring               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Jira               = Itsm Jira Troubleshooting platform overview and core concepts                 │
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

- Jira logs: `<jira-home>/log/atlassian-jira.log`.
- Jira cluster node status: Administration → System → Clustering.
- Most Jira issues are database (connection pool exhaustion) or index (Lucene corruption) problems.

## Database

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Cannot get a connection, pool error Timeout waiting for connection` | Jira DC 9.x | Connection pool exhausted — too many concurrent DB requests | Increase `c3p0.maxPoolSize` in `dbconfig.xml`; check slow query log for long-running queries | N/A |
| Jira returning 500 errors on all pages | Jira DC 9.x | Database server unreachable | Verify DB server health; check TCP 5432 (PostgreSQL) or 1433 (SQL Server) from Jira nodes | N/A |

## Clustering

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Node shows `Offline` in cluster management | Jira DC 9.x | Hazelcast port 5701 blocked between nodes | Verify TCP 5701 between all Jira DC nodes | N/A |
| `Cache synchronization failed` between nodes | Jira DC 9.x | Hazelcast split-brain during network partition | Restart affected node; check cluster membership after restart | N/A |

## Index

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Issue search returning incomplete results | Jira DC 9.x | Lucene index out of sync | Re-index: Administration → System → Indexing → Full Re-index (off-peak) | N/A |
| `IndexOutOfBoundsException` in logs | Jira DC 9.x | Corrupt Lucene index segment | Stop Jira; delete `<jira-home>/caches/indexes/`; restart and re-index | N/A |

## See also

- [Jira — Common Issues](common-issues.md)
- [Confluence — Known Issues](../../confluence/troubleshooting/known-issues/)
- [PostgreSQL — Known Issues](../../../compute/linux/postgresql/troubleshooting/known-issues/)
