---
tags:
  - troubleshooting
  - confluence
  - itsm
  - known-issues
---
# Confluence — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Confluence Data Center bugs, error codes, and workarounds covering Synchrony (collaborative editing), clustering, and database issues.

*Applies to: Confluence Data Center 8.x*
</div>

```text
┌─────────────────────────────────────── Confluence Data Center ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               Team wiki/collaboration — Synchrony, clustering, shared DB backend              │   │
│   │              Protocols: HTTP/HTTPS · Synchrony (TCP 8091) · Hazelcast (TCP 5701)              │   │
│   │                              Management: Confluence Admin Console                             │   │
│   │            Page edit -> Synchrony collab -> DB write -> Cluster cache sync -> Index           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             App             │  │       Confluence node       │  │     Stateless, behind LB    │   │
│   │            Collab           │  │          Synchrony          │  │     Real-time co-editing    │   │
│   │           Cluster           │  │          Hazelcast          │  │     Cache+cluster member    │   │
│   │              DB             │  │    Postgres/Oracle/MSSQL    │  │       Single shared DB      │   │
│   │            Search           │  │         Lucene index        │  │    Per-node, rebuildable    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │ Confluence node  │     Web app      │     HTTP/HTTPS    │    SSO/local     │Many in DC cluster│   │
│   │    Synchrony     │ Collab. editing  │      TCP 8091     │     Internal     │Separate JVM proc.│   │
│   │    Hazelcast     │  Cluster cache   │      TCP 5701     │     Internal     │ Split-brain risk │   │
│   │   Lucene index   │      Search      │      Internal     │       N/A        │Rebuild via admin │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: Confluence DC nodes - load balancer - shared DB - shared storage                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Synchrony      = separate process providing real-time collaborative editing                          │
│  Hazelcast      = in-memory clustering library backing the DC cache layer                             │
│  Confluence home= filesystem dir with config, logs, indexes, plugins                                  │
│  Shared home    = NFS/shared storage required for DC clustering                                       │
│  Split-brain    = cluster nodes diverge after losing contact                                          │
│  Lucene         = full-text search indexing library                                                   │
│  Support zip    = bundled diagnostic export (logs, config, dumps)                                     │
│  Thread dump    = JVM snapshot for hangs; take 3 spaced 10s apart                                     │
│  Heap dump      = full JVM memory capture for OOM diagnosis                                           │
│  Safe mode      = starts Confluence without user-installed plugins                                    │
│  CQL            = Confluence Query Language; macros and REST search                                   │
│  Data Center    = clustered HA edition (vs Server/Cloud)                                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Confluence logs: `<confluence-home>/logs/atlassian-confluence.log`.
- Synchrony (collaborative editing) logs: `<confluence-home>/logs/atlassian-synchrony.log`.
- Most collaborative editing failures are Synchrony (port 8091) connectivity issues.

## Synchrony (Collaborative Editing)

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Cannot collaborate — Synchrony not available` | Confluence DC 8.x | Synchrony process not running or port 8091 blocked | Restart Synchrony; verify TCP 8091 between browser and Confluence server | N/A |
| Collaborative editing not syncing between users | Confluence DC 8.x | Synchrony cluster split — nodes not communicating | Check `<confluence-home>/synchrony-args.properties` cluster config; verify TCP 25500 between nodes | N/A |

## Clustering

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Node joining cluster failed` | Confluence DC 8.x | Hazelcast port 5701 blocked | Verify TCP 5701 between all Confluence DC nodes | N/A |
| Cache inconsistency after node restart | Confluence DC 8.x | Node rejoined cluster with stale cache | Full node restart; cache refreshes automatically on join | N/A |

## Database

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Confluence startup fails: `Cannot connect to database` | Confluence DC 8.x | Database server unreachable or wrong credentials in `confluence.cfg.xml` | Verify DB connectivity; update credentials in `<confluence-home>/confluence.cfg.xml` | N/A |

## See also

- [Confluence — Common Issues](common-issues/)
- [Jira — Known Issues](../../jira/troubleshooting/known-issues.md)
- [PostgreSQL — Known Issues](../../../compute/linux/postgresql/troubleshooting/known-issues.md)
