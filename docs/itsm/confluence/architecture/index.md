---
tags:
  - architecture
  - confluence
---
# Confluence — Architecture

<div class="kb-summary">
Confluence Data Center runs as an active-active Java cluster sharing a single PostgreSQL database, a distributed NFS/EFS home, and Hazelcast for cache invalidation. Sticky sessions are mandatory at the load balancer.
</div>

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

