---
tags:
  - architecture
  - san
---
# SANnav — Architecture

<div class="kb-summary">
Brocade SANnav is a SAN management platform in two variants: Management Portal (per-fabric operations) and Global View (multi-portal aggregation). Deployed as Linux virtual appliances; communicates with switches via HTTPS and SNMP v3.

*Applies to: Brocade FOS 9.x*
</div>

```text
┌──────────────────────────── SANnav — SAN Management Platform Architecture ────────────────────────────┐
│                                                                                                       │
│  Two variants: Management Portal (per-fabric ops) and Global View (multi-portal);                     │
│  Linux virtual appliances; communicates with switches via HTTPS and SNMP v3.                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Deployment Variants              │  │            Platform Architecture            │   │
│   │        Management Portal: per-fabric         │  │         Linux VM (RHEL/CentOS base)         │   │
│   │         Global View: multi-portal UI         │  │        PostgreSQL: config + event DB        │   │
│   │         Portal: one per fabric pair          │  │         Elasticsearch: search + logs        │   │
│   │          GV: aggregates all portals          │  │           REST API v3: northbound           │   │
│   │        DR: passive standby supported         │  │           HTTPS 443: switch comms           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Management Portal manages switches directly; Global View aggregates read-only view.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Switch Integration              │  │            Monitoring and Alerts            │   │
│   │           HTTPS: REST/supportsave            │  │            MAPS: rules + policies           │   │
│   │            SNMP v3: trap receiver            │  │            Dashboard: port health           │   │
│   │         Syslog: optional from switch         │  │          CRC/signal alerts: fabric          │   │
│   │           SSH: supportsave collect           │  │           Email/SNMP: notification          │   │
│   │        Certificate: switch TLS verify        │  │         Inventory: live + historical        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  VMware or KVM VM (8 vCPU, 32 GB RAM, 500 GB disk minimum); management network                        │
│  access to all FC switches on TCP 443 and UDP 162 (SNMP).                                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Management Portal= per-fabric SANnav instance; full fabric management                                │
│  Global View   = multi-portal aggregator; read-only cross-fabric dashboard                            │
│  SNMP v3       = secure traps from switches; authPriv encryption                                      │
│  Elasticsearch = full-text search engine; powers SANnav log search                                    │
│  PostgreSQL    = relational DB; config, inventory, and event storage                                  │
│  MAPS          = Monitoring and Alerting Policy Suite; pushed from switch                             │
│  Supportsave   = FOS support bundle; SANnav can trigger and collect                                   │
│  DR standby    = passive SANnav VM; promoted if active fails                                          │
│  REST API v3   = SANnav northbound API; fabric config and monitoring                                  │
│  CRC error     = Cyclic Redundancy Check error; key FC signal health metric                           │
│  Port health   = per-port state including CRC, signal, congestion                                     │
│  Inventory     = real-time switch + host + storage discovered topology                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![SANnav Architecture](../../../../assets/sannav-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with Brocade FC switches, vCenter, LDAP, and SIEM.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Sizing guidelines, HA design, and deployment best practices.</span></a>
</div>

## VM Sizing

| Variant | Environment | vCPU | RAM | Storage | Max Switches |
|---|---|---|---|---|---|
| Management Portal | Small | 8 | 32 GB | 300 GB | 50 |
| Management Portal | Medium | 16 | 64 GB | 500 GB | 150 |
| Management Portal | Large | 24 | 96 GB | 1 TB | 300 |
| Global View | Standard | 8 | 32 GB | 500 GB | 10 portals |

## Management Topology

