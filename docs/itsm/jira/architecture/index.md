---
tags:
  - architecture
  - jira
---
# Jira — Architecture

<div class="kb-summary">
Jira Data Center runs as an active-active Java cluster backed by a shared PostgreSQL database, shared NFS home, and distributed Hazelcast cache. Load balancer sticky sessions are mandatory.

*Applies to: Jira Cloud / Data Center*
</div>

```text
┌──────────────────────────── Jira — Project Tracking Platform Architecture ────────────────────────────┐
│                                                                                                       │
│  Jira Data Center: clustered Java app; PostgreSQL backend; shared NFS for attachments;                │
│  load balancer in front; Jira Cloud is SaaS alternative managed by Atlassian.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Data Center Architecture           │  │              Storage Components             │   │
│   │           2+ nodes: active-active            │  │            PostgreSQL: primary DB           │   │
│   │           Hazelcast: cluster cache           │  │          Oracle/SQL Server: also ok         │   │
│   │        Load balancer: sticky session         │  │             NFS: shared home dir            │   │
│   │        REST API: external automation         │  │           Attachments on NFS share          │   │
│   │         Tomcat: embedded web server          │  │          Lucene: local search index         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Each node has own Lucene index; must be rebuilt if a node falls behind.                              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Key Concepts                 │  │             Cloud vs Data Center            │   │
│   │           Project: work container            │  │        Cloud: Atlassian-managed SaaS        │   │
│   │         Issue: individual work item          │  │           DC: self-hosted on prem           │   │
│   │         Workflow: state transitions          │  │         DC: unlimited customisation         │   │
│   │          Board: sprint/kanban view           │  │          DC: own DR/backup control          │   │
│   │           JQL: Jira Query Language           │  │             Cloud: auto-upgrades            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  2+ Linux VMs (8 vCPU, 32 GB RAM each); NFS server or NAS for shared home;                            │
│  PostgreSQL cluster; load balancer (HAProxy or F5); internet access for app store.                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Jira           = Atlassian project tracking; issues, boards, sprints, workflows                      │
│  Data Center    = Jira DC; self-hosted clustered edition; license required                            │
│  Hazelcast      = distributed in-memory cache used by Jira DC cluster members                         │
│  Lucene         = search indexing library; Jira uses per-node index replicas                          │
│  NFS home       = shared filesystem; all nodes mount same path for attachments                        │
│  JQL            = Jira Query Language; SQL-like issue search                                          │
│  Workflow       = state machine for issues (To Do → In Progress → Done)                               │
│  App store      = Atlassian Marketplace; plugins extend Jira functionality                            │
│  Sticky session = load balancer directs user to same node for session state                           │
│  PostgreSQL     = preferred database; Oracle and SQL Server also supported                            │
│  Tomcat         = Java servlet container; Jira runs embedded within Tomcat                            │
│  REST API       = Jira REST v2/v3; create/update issues, query boards                                 │
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

