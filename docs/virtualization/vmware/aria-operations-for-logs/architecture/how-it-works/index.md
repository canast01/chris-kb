# Aria Operations for Logs — How It Works

## Overview

Aria Operations for Logs (formerly vRealize Log Insight) collects, indexes, and correlates log data from VMware infrastructure and other sources. It provides real-time search, pattern-based alerting, content pack dashboards, and bidirectional launch-in-context integration with Aria Operations. Logs are retained in a hot Cassandra index and optionally archived to NFS for long-term storage.

## Log Pipeline Architecture

```mermaid
graph TB
  SRC1(["ESXi / vCenter syslog"]) & SRC2(["NSX / VMs syslog"]) & SRC3(["Linux / Windows agent"]) --> VRLI["Aria Operations for Logs\n(Log Intelligence cluster)"]
  VRLI --> IDX[("Log Index\nhot + warm retention")]
  VRLI --> ALERTS["Alert Rules & Notifications"]
  ADMIN(["Operator"]) -->|"browser"| VRLI
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class VRLI ctrl
  class IDX store
  class SRC1,SRC2,SRC3,ADMIN host
```
┌─────────────────────────────── Aria Operations for Logs — How It Works ───────────────────────────────┐
│                                                                                                       │
│  Centralised log aggregation, indexing, and alerting for VMware and multi-cloud environments.         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Ingestion Layer                │  │                Analysis Layer               │   │
│   │        Syslog: UDP/TCP 514, TLS 6514         │  │       Real-time indexing of log events      │   │
│   │       vSphere agent: ESXi/vCenter logs       │  │     Interactive analytics: filter+group     │   │
│   │       CF/vRLI agent: app log shipping        │  │       Field extraction: auto + custom       │   │
│   │      REST ingest API for custom sources      │  │        Dashboards: saved query views        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Alerts fire on query thresholds; Aria Ops integration correlates logs with metrics.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Alerting and Forwarding            │  │                 Integration                 │   │
│   │        Alert: query matches threshold        │  │    Aria Operations: log launch-in-context   │   │
│   │       Notify: email/webhook/ServiceNow       │  │         vCenter: VM log correlation         │   │
│   │       Forward: syslog to SIEM (Splunk)       │  │        NSX: DFW rule match log events       │   │
│   │       Archive: export to S3/NFS for DR       │  │       VxRail: hardware event ingestion      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Linux VM (vRLI appliance) · NIC for syslog ingestion · vCenter · ESXi hosts · NTP                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vRLI              = vRealize Log Insight; former name for Aria Operations for Logs                   │
│  Syslog            = Protocol for log transmission; UDP 514 (unreliable) or TCP/TLS 6514              │
│  vSphere agent     = vRLI agent on ESXi and vCenter; ships structured logs directly                   │
│  Field extraction  = vRLI parses log text to create queryable structured fields                       │
│  Interactive analytics= vRLI UI for free-text search, filter, group, and timeline analysis            │
│  Alert             = Query-based trigger; fires when event count or pattern exceeds threshold         │
│  Content pack      = Pre-built dashboards and alerts for a specific product (e.g. NSX, vSAN)          │
│  Launch in context = Aria Ops alert opens vRLI filtered to same host/timeframe                        │
│  SIEM forwarding   = vRLI forwards selected events to Splunk or other SIEM via syslog                 │
│  Archive           = Long-term log export to NFS or S3 for compliance retention                       │
│  Worker node       = Additional vRLI VM for horizontal scale; master distributes ingestion            │
│  Ingestion API     = REST endpoint for pushing structured JSON logs from custom applications          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

## ESXi Syslog Configuration

```bash
esxcli system syslog config set --loghost="udp://<vrli-fqdn>:514"
esxcli system syslog reload
esxcli network firewall ruleset set --ruleset-id=syslog --enabled=true
```
