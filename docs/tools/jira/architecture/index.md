# Jira — Architecture

<div class="kb-summary">
Jira Data Center runs as an active-active Java cluster backed by a shared PostgreSQL database, shared NFS home, and distributed Hazelcast cache. Load balancer sticky sessions are mandatory.
</div>

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

```mermaid
graph TB
    subgraph LB["Load Balancer (sticky sessions)"]
        HAP["HAProxy / F5 / ALB"]
    end

    subgraph App["Application Tier (Active-Active)"]
        N1["Node 1"]
        N2["Node 2"]
        N3["Node 3"]
    end

    subgraph Data["Data & Cache Tier"]
        PG[("PostgreSQL")]
        OS["OpenSearch"]
        NFS["Shared Home\n(NFS)"]
        EH["Hazelcast\nCache"]
    end

    HAP -->|sticky| N1
    HAP -->|sticky| N2
    HAP -->|sticky| N3
    N1 <--> EH
    N2 <--> EH
    N3 <--> EH
    N1 --> PG
    N2 --> PG
    N3 --> PG
    N1 --> OS
    N1 --> NFS
    N2 --> NFS
    N3 --> NFS
```
