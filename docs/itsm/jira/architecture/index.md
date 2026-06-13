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

