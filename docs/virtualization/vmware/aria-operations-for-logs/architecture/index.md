# Aria Operations for Logs — Architecture

<div class="kb-summary">
Log analytics platform collecting syslog and LI Agent data from VMware infrastructure. Indexes and correlates logs in a Cassandra-backed hot tier with optional NFS archiving; provides real-time search, alerting, and bidirectional launch-in-context with Aria Operations.
</div>

![Aria Operations for Logs Cluster Architecture](../../../../assets/aria-operations-for-logs-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with ESXi, vCenter, NSX, and Aria Operations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Sizing guidelines, HA design, and ingestion protocol best practices.</span></a>
</div>

## Cluster Topology

| Node Role | Description |
|---|---|
| Master | Primary node — ingestion, indexing, query coordination, cluster management UI |
| Worker | Scale-out nodes — increase ingestion throughput and storage capacity |

Minimum for production HA: **3 nodes** (1 master + 2 workers) on separate ESXi hosts with anti-affinity rules.

