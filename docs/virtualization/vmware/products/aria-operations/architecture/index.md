---
tags:
  - architecture
  - aria-operations
  - vmware
---
# Aria Operations — Architecture

<div class="kb-summary">
Analytics cluster for vSphere performance, capacity, and compliance monitoring. Adapters collect metrics from vCenter, NSX, and storage; remote collectors extend reach into remote sites and DMZs without direct cluster connectivity.

*Applies to: Aria Operations 8.x*
</div>

![Aria Operations — Architecture — Diagram](../../../../../assets/virtualization-vmware-aria-operations-architecture-diagram.svg)
![Aria Operations Cluster Architecture](../../../../../assets/aria-operations-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with vCenter, NSX, storage, and external monitoring tools.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Sizing guidelines, adapter configuration, and cluster design best practices.</span></a>
</div>

## Node Roles

| Node Role | Description |
|---|---|
| Primary | Hosts the UI, analytics controller, and cluster coordination |
| Primary Replica | Hot standby — automatically promoted if Primary fails |
| Data | Scale-out metric ingestion and storage nodes |
| Remote Collector | Lightweight proxy for remote sites/DMZs; forwards to cluster without joining it |
| Cloud Proxy | SaaS-hosted proxy for VMware Cloud on AWS integrations |

## Deployment Sizing

| Deployment Size | Nodes | Use Case |
|---|---|---|
| Small (xSmall) | 1 node | Lab / proof-of-concept |
| Medium | Primary + Replica | Up to ~3,000 VMs |
| Large | Primary + Replica + 2–4 Data Nodes | Up to ~10,000 VMs |
| Extra Large | Primary + Replica + 4+ Data Nodes | Enterprise fleet |

---

## Analytics Cluster Topology
