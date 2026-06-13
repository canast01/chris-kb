---
tags:
  - architecture
  - san
---
# SANnav — How It Works


<div class="kb-summary">
How It Works reference covering Overview, Deployment Topology, Supported Hardware, Network Requirements, VM Sizing and 2 more sections.

*Applies to: Brocade FOS 9.x*
</div>

```text
┌──────────────────────────────────── Brocade SANnav — How It Works ────────────────────────────────────┐
│                                                                                                       │
│  SANnav discovers switches via SNMP/REST, aggregates MAPS events, manages zones centrally.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Discovery & Polling              │  │           Zone Management Workflow          │   │
│   │         Add switch IP → SNMP v3 poll         │  │         GUI: browse fabric topology         │   │
│   │         FOS REST API credential auth         │  │          Zone wizard: alias + zone          │   │
│   │        Topology built: domain + ports        │  │          Push zone config to fabric         │   │
│   │         Inventory: SFP/HBA/port data         │  │          cfgsave + cfgenable remote         │   │
│   │        MAPS alerts: event forwarding         │  │          Zone diff: compare changes         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SANnav polls switches for state; zone changes are staged and pushed via FOS API.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Performance Monitoring            │  │             Firmware Management             │   │
│   │         Port utilisation: 5-min poll         │  │          Upload FOS image to SANnav         │   │
│   │           Dashboards: top talkers            │  │          Stage firmware per switch          │   │
│   │         Historical: 90-day retention         │  │         Schedule: maintenance window        │   │
│   │         Alerts: email/SNMP on breach         │  │          HA upgrade: non-disruptive         │   │
│   │         Bottleneck detection report          │  │         Post-upgrade version verify         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SANnav VM · management network · Brocade FC switches · NTP for time sync                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SNMPv3          = polling protocol; SANnav uses for switch discovery and alerting                    │
│  FOS REST API    = Fabric OS northbound API; SANnav uses for zone/config management                   │
│  MAPS alert      = switch-side threshold event forwarded to SANnav as notification                    │
│  Zone wizard     = SANnav GUI workflow for creating aliases and zones step-by-step                    │
│  cfgsave/cfgenable= zone config save and activation; SANnav triggers on switches                      │
│  Zone diff       = SANnav shows before/after zone changes before committing                           │
│  Top talkers     = ports/flows with highest utilisation; identified in performance view               │
│  HA upgrade      = firmware loaded to standby CP first; switch-over then upgrade active               │
│  5-min poll      = default SANnav performance data collection interval per port                       │
│  Stage firmware  = upload FOS image to switch flash without activating; activate later                │
│  Bottleneck report= SANnav identifies congested ISLs and credit-starved ports                         │
│  90-day retention= default performance data history in SANnav Elasticsearch store                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

Brocade SANnav is a SAN management platform delivered in two variants:

- **SANnav Management Portal** — single-fabric or multi-fabric management for day-to-day operations: zoning, firmware management, MAPS policies, performance dashboards, inventory, and event management. Deployed as a standalone virtual appliance (OVA/ISO).
- **SANnav Global View** — aggregation layer for large environments with multiple portal instances. Provides a consolidated dashboard, cross-fabric health summary, and centralised alert aggregation.

## Deployment Topology

## Supported Hardware

| Platform | Gen | Max Ports | Notes |
|---|---|---|---|
| G730 Director | Gen 7 | 384 | 64G FC, NVMe-oF |
| G720 Director | Gen 7 | 192 | 32/64G FC |
| G630 Director | Gen 6 | 384 | 32G FC |
| G620 Director | Gen 6 | 128 | 32G FC |
| X7-8 Director | Gen 7 | 512 | 64G FC, high density |
| X6-8 Director | Gen 6 | 512 | 32G FC |

Legacy Gen 5 hardware (6510, 6520, DCX 8510) is supported in monitoring mode with reduced feature availability.

## Network Requirements

| Communication | Protocol | Port | Direction |
|---|---|---|---|
| SANnav → switch | HTTPS | 443 | Outbound from SANnav |
| SANnav → switch | SNMP v3 | 161/UDP | Outbound from SANnav |
| Switch → SANnav | SNMP trap | 162/UDP | Inbound to SANnav |
| Browser → SANnav | HTTPS | 443 | Inbound to SANnav |
| SANnav → LDAP | LDAPS | 636 | Outbound from SANnav |
| Portal → Global View | HTTPS | 443 | Outbound from Portal |

## VM Sizing

### Management Portal

| Environment | vCPU | RAM | Storage | Max Switches |
|---|---|---|---|---|
| Small (≤ 50 switches) | 8 | 32 GB | 300 GB | 50 |
| Medium (≤ 150 switches) | 16 | 64 GB | 500 GB | 150 |
| Large (≤ 300 switches) | 24 | 96 GB | 1 TB | 300 |

### Global View

| Environment | vCPU | RAM | Storage | Max Portals |
|---|---|---|---|---|
| Standard | 8 | 32 GB | 500 GB | 10 |

Hypervisors supported: VMware ESXi 6.7+, 7.x; KVM.

## Internal Services

```mermaid
graph TB
  SW1["Brocade Switch A\nFabricOS · REST/SNMP telemetry"]
  SW2["Brocade Switch B\nFabricOS · REST/SNMP telemetry"]
  SW3["Brocade Switch C\nFabricOS · REST/SNMP telemetry"]

  subgraph SANnav["SANnav Management Portal — Collection Layer"]
    REST["REST API Server\nFOS northbound API client"]
    SNMPR["SNMP Receiver\nv3 polling + trap ingestion"]
  end

  subgraph SVC["SANnav Internal Services"]
    ES["Elasticsearch\nFabric topology &amp; inventory"]
    TSDB["TimescaleDB\nPerformance time-series data"]
    AE["Alerting Engine\nMAPS events · threshold rules"]
  end

  OUT1["Fabric Map UI\nTopology visualisation"]
  OUT2["Performance Dashboard\nPort utilisation · top talkers"]
  OUT3["Alert Console\nEvent management · email/SNMP"]
  OUT4["REST API\nThird-party integration"]

  SW1 -->|"REST + SNMP"| REST
  SW2 -->|"REST + SNMP"| REST
  SW3 -->|"SNMP trap"| SNMPR
  REST --> ES
  REST --> TSDB
  SNMPR --> AE
  ES --> OUT1
  TSDB --> OUT2
  AE --> OUT3
  REST --> OUT4

  classDef switch fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef svc fill:#15803d,stroke:#166534,color:#fff
  classDef db fill:#b45309,stroke:#92400e,color:#fff
  classDef out fill:#7c3aed,stroke:#6d28d9,color:#fff
  class SW1,SW2,SW3 switch
  class REST,SNMPR svc
  class ES,TSDB,AE db
  class OUT1,OUT2,OUT3,OUT4 out
```

| Service | Role |
|---|---|
| Discovery engine | Continuous fabric topology polling via HTTPS/SNMP |
| Event engine | SNMP trap processing, alert evaluation, email/SNMP forwarding |
| MAPS analytics | MAPS policy violation monitoring and trending |
| SAN analytics | I/O performance data ingestion and visualisation |
| Image management | Firmware repository, staged upgrades |
| Zone manager | Zoning configuration push, alias management |
| Time-series DB | Performance metric retention (internal InfluxDB) |
| PostgreSQL | Configuration, inventory, user, and event data |

## Integrations

| System | Integration |
|---|---|
| VMware vCenter | Pulls host WWN data for end-to-end path visibility |
| ServiceNow / ticketing | Alert forwarding via email or webhook (HTTPS POST) |
| SIEM | Syslog forwarding from SANnav; SNMP trap forwarding |
| Active Directory / LDAP | User authentication and group-based role assignment |

---

## See also

- [Sannav — Design Standards](design-standards/)
- [Sannav — Integrations](integrations/)
- [Sannav — Deploy](../deploy/)
