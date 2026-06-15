---
tags:
  - architecture
  - confluence
---
# Confluence — Architecture

<div class="kb-summary">
Confluence Data Center runs as an active-active Java cluster sharing a single PostgreSQL database, a distributed NFS/EFS home, and Hazelcast for cache invalidation. Sticky sessions are mandatory at the load balancer.

*Applies to: Confluence Cloud / Data Center*
</div>

```text
┌────────────────────────────────── Confluence Architecture Overview ───────────────────────────────────┐
│                                                                                                       │
│  Atlassian Confluence is a team wiki and knowledge management platform. Content                       │
│  lives in Spaces; each Space holds Pages in a tree hierarchy. Available as Cloud                      │
│  SaaS or self-hosted Data Center (DC) with clustered app nodes.                                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Content Layer                 │  │                  Data Layer                 │   │
│   │         Spaces: top-level containers         │  │         PostgreSQL or MS SQL Server         │   │
│   │      Pages: hierarchical wiki articles       │  │           Attachments on NFS or S3          │   │
│   │        Macros: dynamic content blocks        │  │         Lucene search index per node        │   │
│   │       Templates: reusable page layouts       │  │         Shared home dir for DC nodes        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │       Application Layer (Data Center)        │  │              Integration Layer              │   │
│   │        Tomcat app server; WAR deploy         │  │        Jira: linked issues, roadmaps        │   │
│   │         Nodes share DB + shared home         │  │        REST API v2: page CRUD, search       │   │
│   │        Synchrony: collaborative edit         │  │       Marketplace: Atlassian SDK apps       │   │
│   │           HAProxy or ELB in front            │  │        SCIM provisioning (Cloud only)       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical infrastructure: DC nodes on bare-metal or VMs; shared PostgreSQL cluster;                   │
│  NFS or S3-compatible store for attachments; load balancer (sticky sessions required)                 │
│  for DC cluster; CDN or reverse proxy for Cloud tenants.                                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Space          = top-level content container; has own permissions and home page                      │
│  Page           = wiki article; versioned; supports inline comments                                   │
│  Macro          = dynamic block (TOC, Jira issues, roadmap, code snippet)                             │
│  Data Center    = self-hosted; clustered active-active app nodes                                      │
│  Synchrony      = real-time collaborative editing service bundled with DC                             │
│  Shared home    = NFS directory mounted by all DC nodes for config and attachments                    │
│  Lucene         = embedded search index; rebuilt on startup or via reindex job                        │
│  Template       = pre-structured page layout; global or space-level                                   │
│  Marketplace    = Atlassian app store; P2, DC, and Cloud compatible apps                              │
│  REST API v2    = Confluence Cloud REST API; page, space, comment, user endpoints                     │
│  Blueprint      = guided template with prompts; generates a structured page                           │
│  Space key      = short unique identifier for a space (e.g. ENG, OPS, ARCH)                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Confluence Architecture](../../../assets/confluence-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Deployment models, cluster topology, component roles, and port reference.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>

---

## Deployment Models

| Model | Hosting | HA | Clustering | Atlassian Managed |
|---|---|---|---|---|
| Server (EOL) | Self-hosted | No | No | No |
| **Data Center** | Self-hosted | Yes | Yes (active/active) | No |
| Cloud | Atlassian infrastructure | Yes | Managed | Yes |

---

## Data Center Topology

