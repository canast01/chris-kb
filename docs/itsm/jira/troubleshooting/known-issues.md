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
┌────────────────────────────────────────── Jira Data Center ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                Issue tracking — clustering, Lucene index, DB connection pooling               │   │
│   │                          Protocols: HTTP/HTTPS · Hazelcast (TCP 5701)                         │   │
│   │                            Management: Jira Administration Console                            │   │
│   │            Issue create/update -> DB write -> Lucene reindex -> Cluster cache sync            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             App             │  │          Jira node          │  │     Stateless, behind LB    │   │
│   │           Cluster           │  │          Hazelcast          │  │     Cache+cluster member    │   │
│   │              DB             │  │    Postgres/Oracle/MSSQL    │  │     Pool sized per node     │   │
│   │            Index            │  │            Lucene           │  │    Per-node, rebuildable    │   │
│   │           Storage           │  │      Shared home (NFS)      │  │    Attach/plugins/config    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │    Jira node     │     Web app      │     HTTP/HTTPS    │    SSO/local     │Many in DC cluster│   │
│   │    Hazelcast     │  Cluster cache   │      TCP 5701     │     Internal     │ Split-brain risk │   │
│   │   Lucene index   │   Issue search   │      Internal     │       N/A        │ Reindex off-peak │   │
│   │     DB pool      │ Connection pool  │    DB-specific    │     DB creds     │ c3p0 in dbconfig │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: Jira DC nodes - load balancer - shared DB - shared home (NFS)                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Hazelcast      = in-memory clustering library backing the DC cache layer                             │
│  Lucene index   = full-text search engine backing Jira issue search                                   │
│  c3p0           = connection pooling library configured in dbconfig.xml                               │
│  Shared home    = NFS/shared storage required for DC clustering                                       │
│  Split-brain    = cluster nodes diverge after losing contact                                          │
│  Reindex        = rebuilds the Lucene index after bulk data changes                                   │
│  Cluster node   = one Jira instance in a Data Center cluster                                          │
│  Jira home      = filesystem dir with config, logs, caches, plugins                                   │
│  Pool exhaustion= too many concurrent DB requests for pool size                                       │
│  Support zip    = bundled diagnostic export for Atlassian Support                                     │
│  Thread dump    = JVM snapshot for hangs; take 3 spaced 10s apart                                     │
│  Safe mode      = starts Jira without user-installed plugins                                          │
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

- [Jira — Common Issues](common-issues/)
- [Confluence — Known Issues](../../confluence/troubleshooting/known-issues.md)
- [PostgreSQL — Known Issues](../../../compute/linux/postgresql/troubleshooting/known-issues.md)
