# Confluence — How It Works

Confluence is Atlassian's enterprise wiki and collaboration platform, available in three deployment models: **Server** (EOL), **Data Center** (self-managed, HA-capable), and **Cloud** (SaaS). This page covers the internal component architecture and deployment topology for on-premises Data Center deployments.

---

## Deployment Models

| Model | Hosting | HA | Clustering | Atlassian Managed |
|---|---|---|---|---|
| Server | Self-hosted | No | No | No |
| Data Center | Self-hosted | Yes | Yes (active/active) | No |
| Cloud | Atlassian infrastructure | Yes | Managed | Yes |

> Confluence Server reached End of Life on **February 15, 2024**. All self-managed deployments should be on Data Center.

---

## Core Components

### Application Server

Confluence runs as a Java web application inside an embedded **Apache Tomcat** servlet container.

| File | Purpose |
|---|---|
| `<CONFLUENCE_HOME>/confluence.cfg.xml` | Database connection, home directory, cluster settings |
| `<CONFLUENCE_INSTALL>/conf/server.xml` | Tomcat connector ports, TLS offload, AJP |
| `<CONFLUENCE_INSTALL>/bin/setenv.sh` | JVM heap, GC flags, system properties |
| `<CONFLUENCE_HOME>/confluence-init.properties` | Override home directory path |

### Database

| Database | Minimum Version | Notes |
|---|---|---|
| PostgreSQL | 14 | Recommended; best tested |
| Microsoft SQL Server | 2017 | Requires JDBC driver drop-in |
| MySQL | 8.0 | Requires explicit collation config |
| Oracle | 19c | Supported; least common |

### Search (Lucene)

Confluence uses an embedded **Apache Lucene** index for full-text search. In Data Center mode, the index lives in the **shared home** directory so all nodes share a single index.

- Index location: `<SHARED_HOME>/index/`
- Rebuilding: **Admin > General Configuration > Content Indexing**

### File / Attachment Storage

| Mode | Location |
|---|---|
| Single node (Server) | `<LOCAL_HOME>/attachments/` |
| Data Center | `<SHARED_HOME>/attachments/` (must be accessible by all nodes) |

### Shared Home vs Local Home (Data Center)

| Directory | Scope | Contents |
|---|---|---|
| Local home (`confluence.home`) | Per node | Temp files, caches, local logs |
| Shared home (`confluence.shared-home`) | Cluster-wide | Attachments, index, avatars, backups, plugins |

---

## Deployment Topology

### Data Center — Active/Active Cluster

```mermaid
flowchart TD
    Users["End Users / Browsers"] --> LB

    subgraph LB["Load Balancer (sticky sessions)"]
        direction LR
        LB1[nginx / F5 / ALB]
    end

    LB --> N1
    LB --> N2
    LB --> N3

    subgraph Cluster["Confluence Data Center Cluster"]
        N1["Node 1\nTomcat JVM"]
        N2["Node 2\nTomcat JVM"]
        N3["Node 3\nTomcat JVM"]
        N1 <-->|Hazelcast\ncluster bus| N2
        N2 <-->|Hazelcast\ncluster bus| N3
        N1 <-->|Hazelcast\ncluster bus| N3
    end

    subgraph Shared["Shared Tier"]
        SH["Shared Home\n(NFS / EFS)\nAttachments, Index, Avatars"]
        DB[("Database\nPostgreSQL")]
    end

    N1 --> SH
    N2 --> SH
    N3 --> SH
    N1 --> DB
    N2 --> DB
    N3 --> DB
```
```text
┌────────────────────────────────────── Confluence — How It Works ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                Confluence Request and Data Flow                               │   │
│   │          Browser → LB → Tomcat (Confluence app) → DB read/write + NFS attachment I/O          │   │
│   │         Page render: Velocity templates transform wiki markup to HTML on each request         │   │
│   │     Search: Lucene index on NFS; rebuilt with full re-index from Admin > Content Indexing     │   │
│   │            Collab editing: Synchrony service (port 8091) manages OT over WebSocket            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Confluence processes three parallel flows: HTTP, search indexing, and collaborative edits          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      HTTP Request Flow      │  │         Search Flow         │  │       Collab Edit Flow      │   │
│   │      Browser → HTTPS LB     │  │     Create/edit triggers    │  │      User opens editor      │   │
│   │       LB → Tomcat node      │  │     Lucene index update     │  │    WebSocket → Synchrony    │   │
│   │      Auth: session/SAML     │  │     Async indexing queue    │  │     OT conflict resolve     │   │
│   │      DB query via JDBC      │  │     Shared index on NFS     │  │        DB draft save        │   │
│   │       NFS: attachments      │  │     Per-node cache warm     │  │      Publish: DB commit     │   │
│   │     Velocity → HTML resp    │  │      Re-index: admin UI     │  │     Version stored in DB    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    All three flows converge on the shared PostgreSQL DB as the authoritative data store               │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Tomcat JVM VMs · PostgreSQL VM with fast SSD · NFS datastore · network load balancer                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Velocity     = Apache Velocity; Java template engine used to render Confluence HTML pages            │
│  OT           = Operational Transformation; algorithm resolving concurrent edit conflicts             │
│  Synchrony    = Confluence collab editing service; manages document state via WebSocket               │
│  Lucene index = inverted index of page content; enables fast full-text search                         │
│  Re-index     = full rebuild of Lucene index from DB; needed after restore or corruption              │
│  JDBC pool    = connection pool (HikariCP) managed by Confluence for DB access                        │
│  SAML         = Confluence delegates authentication to IdP (Okta/AD FS/Ping) via SAML 2.0             │
│  NFS mount    = shared home directory; same path on every DC node for attachment access               │
│  Draft        = Synchrony saves drafts to DB before publish to avoid data loss                        │
│  Page version = every save increments version counter; prior versions retained in DB                  │
│  Attachment   = binary file stored on NFS under confluence.home/attachments                           │
│  LB session   = load balancer uses sticky sessions or shared Hazelcast session store                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Network Port Reference

| Port | Protocol | Component | Notes |
|---|---|---|---|
| 8090 | TCP | Confluence HTTP | Default; front with nginx/443 |
| 5801 | TCP | Hazelcast | Inter-node cluster comms |
| 5432 | TCP | PostgreSQL | From app nodes to DB |
| 25 / 587 | TCP | SMTP | Outbound email |
| 636 / 389 | TCP | LDAP/AD | User directory sync |

---

## Plugin Architecture

Confluence plugins use the **Atlassian Plugin Framework (APF2)**. Plugin states and compatibility flags are stored in the database table `PLUGINVERSION`.

- `<SHARED_HOME>/plugins-osgi-cache/` — compiled plugin artifacts
- `<SHARED_HOME>/bundled-plugins/` — plugins shipped with Confluence

---

## Key Admin URLs

| URL | Purpose |
|---|---|
| `/admin/systeminfo.action` | JVM info, memory, uptime |
| `/admin/clustering.action` | Cluster node status |
| `/admin/indexqueue.action` | Search index queue |
| `/admin/scheduledjobs.action` | Scheduled task status |
| `/admin/logging.action` | Log level control |
