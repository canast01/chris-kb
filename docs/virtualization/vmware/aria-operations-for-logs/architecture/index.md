---
tags:
  - architecture
  - aria-logs
  - vmware
---
# Aria Operations for Logs — Architecture

<div class="kb-summary">
Log analytics platform collecting syslog and LI Agent data from VMware infrastructure. Indexes and correlates logs in a Cassandra-backed hot tier with optional NFS archiving; provides real-time search, alerting, and bidirectional launch-in-context with Aria Operations.

*Applies to: Aria Operations for Logs 8.x*
</div>

```text
┌──────────────────────── Aria Operations for Logs — Log Analytics Architecture ────────────────────────┐
│                                                                                                       │
│  Collects syslog and LI Agent data; indexes in Cassandra hot tier; optional NFS                       │
│  archive; real-time search, alerting, and launch-in-context with Aria Operations.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Cluster Architecture             │  │                Log Ingestion                │   │
│   │            Master + worker nodes             │  │         Syslog: UDP/TCP 514 (plain)         │   │
│   │          Cassandra: hot-tier index           │  │             Syslog TLS: TCP 1514            │   │
│   │         NFS archive: cold-tier logs          │  │          LI Agent: CFAPI port 9543          │   │
│   │         VIP/LB: multi-node ingestion         │  │        CFAPI: structured JSON events        │   │
│   │        Retention: default 30 days hot        │  │         vCenter: plugin auto-config         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  LI Agent adds structured fields; syslog is plain text — agent preferred for VMware.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Search and Alerting              │  │                 Integrations                │   │
│   │        Query: interactive log search         │  │        Aria Operations: launch-in-ctx       │   │
│   │       Alert: pattern match + threshold       │  │            SNMP: trap forwarding            │   │
│   │         Notification: email/webhook          │  │           Syslog forward: to SIEM           │   │
│   │       Content pack: pre-built filters        │  │        vRNI: network flow correlation       │   │
│   │           Dashboard: saved queries           │  │              AD: LDAP/SAML auth             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Photon OS VMs; NFS share for archive; load balancer (NSX/VIP) for multi-node;                        │
│  UDP 514 / TCP 514 / TCP 1514 / TCP 9543 open on firewall.                                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  LI Agent      = Log Insight Agent; structured log forwarding to Aria Logs                            │
│  CFAPI         = Content Frame API; structured JSON ingestion; port 9543                              │
│  Cassandra     = hot-tier index; in-cluster; fast search on recent logs                               │
│  NFS archive   = cold-tier; compressed log storage; not searchable in-place                           │
│  Content pack  = pre-built filters, queries, alerts for a product                                     │
│  Launch-in-ctx = link from Aria Operations alert to correlated log view                               │
│  Syslog        = UDP/TCP 514 plain; TCP 1514 TLS; no structured fields                                │
│  Retention     = hot: configurable (default 30 days); archive: NFS limit                              │
│  Master node   = primary; handles UI, API, Cassandra coordination                                     │
│  Worker node   = ingestion + indexing; scales horizontally                                            │
│  Alert         = query that fires notification when match count > threshold                           │
│  vRNI          = Aria Operations for Networks; network flow log correlation                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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

