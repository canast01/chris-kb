# ServiceNow — Architecture

<div class="kb-summary">
ServiceNow is a multi-instance SaaS platform with fully isolated per-customer stacks. On-premises integration is handled via MID Servers — outbound-only Java agents that eliminate inbound firewall requirements.
</div>

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Instance model, node topology, MID Servers, platform components, and upgrade lifecycle.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>

---

## Instance Hierarchy

| Instance | Purpose |
|---|---|
| Dev | Development and initial testing |
| Test / UAT | Validation before production promotion |
| Production | Live environment |

---

## Platform Node Topology

```mermaid
graph TD
    LB["Load Balancer\n(ServiceNow-managed)"]

    subgraph App["App Tier"]
        N1["App Node 1"]
        N2["App Node 2"]
        N3["App Node 3"]
    end

    subgraph DB["DB Tier"]
        PRI["Primary DB"]
        REP["Replica DB"]
    end

    subgraph MID["MID Tier (on-prem)"]
        MID1["MID Server 1"]
        MID2["MID Server 2"]
    end

    LB --> N1
    LB --> N2
    LB --> N3
    N1 --> PRI
    PRI -- replication --> REP
    N1 <-->|"HTTPS outbound only"| MID1
    N1 <-->|"HTTPS outbound only"| MID2
```
