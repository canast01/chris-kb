# Jira — Architecture

<div class="kb-summary">
Jira Data Center runs as an active-active Java cluster backed by a shared PostgreSQL database, shared NFS home, and distributed Hazelcast cache. Load balancer sticky sessions are mandatory.
</div>

```
┌──────────────────────────────────── Jira — Architecture Overview ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 Jira Data Center Architecture                                 │   │
│   │          Load balancer → multiple Tomcat app nodes → shared PostgreSQL DB + NFS home          │   │
│   │           Shared home: stores Lucene index, attachments, plugins, and avatars on NFS          │   │
│   │          Ehcache clustering: Jira DC uses distributed Ehcache for cache across nodes          │   │
│   │         Job scheduling: Jira DC uses cluster-aware scheduler to prevent duplicate jobs        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Jira architecture mirrors Confluence DC: stateless app nodes sharing DB and NFS                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Application Tier               │  │                  Data Tier                  │   │
│   │             Tomcat: 8 vCPU/16 GB             │  │              PostgreSQL primary             │   │
│   │               JVM heap: 4-8 GB               │  │              Streaming replica              │   │
│   │             Ehcache: distributed             │  │               NFS shared home               │   │
│   │             REST API: port 8080              │  │             Lucene index on NFS             │   │
│   │             Scheduler: DC-aware              │  │              JDBC: jira DB user             │   │
│   │             LB: sticky sessions              │  │               pg_dump nightly               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  2+ app VMs · DB VM with SSD · NFS datastore · L4/L7 load balancer                                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Ehcache      = distributed Java cache library; Jira DC uses it for issue and user caching            │
│  Shared home  = JIRA_HOME on NFS; same path on all nodes; holds index and attachments                 │
│  Tomcat       = Java servlet container; Jira runs as a WAR on Tomcat listening port 8080              │
│  DC scheduler = Jira cluster-aware job scheduler; only one node runs each scheduled task              │
│  JDBC pool    = connection pool; Jira uses HikariCP; tune maxPoolSize for concurrent users            │
│  Lucene       = embedded search; index on NFS; rebuilt after restore or corruption                    │
│  Sticky session = LB routes user to same node; avoids Ehcache cache miss cost                         │
│  Streaming replica = PostgreSQL WAL replica; provides read scale and failover target                  │
│  pg_dump      = PostgreSQL backup; schedule nightly with custom format for fast restore               │
│  NFS mount    = JIRA_HOME on NFS; must be available before Jira starts                                │
│  LB           = load balancer; HAProxy, nginx, or F5; handles TLS termination                         │
│  JVM heap     = -Xmx in setenv.sh; 4 GB minimum, 8 GB for large instances                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Jira Architecture](../../../assets/jira-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Deployment models, cluster topology, component roles, and port reference.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>

---

## Deployment Models

| Model | Hosting | Clustering | DB Control | Customisation |
|---|---|---|---|---|
| Server (EOL) | Self-hosted | Single node | Full | Full |
| **Data Center** | Self-hosted | Active-active | Full | Full |
| Cloud | Atlassian-managed | Managed | None | Limited |

---

## Data Center Topology


