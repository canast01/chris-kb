---
tags:
  - architecture
  - netapp
---
# InsightIQ — Integrations

<div class="kb-summary">
InsightIQ integrates exclusively with PowerScale (Isilon) clusters via the OneFS REST API. External integrations are limited to email alerting, syslog forwarding, and the InsightIQ REST API for report automation.
</div>

```text
┌──────────────────────────────── InsightIQ — Architecture Integrations ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                    Inputs                    │                    Outputs                     │   │
│   │          PowerScale PAPI (primary)           │               Web UI dashboards                │   │
│   │          Multiple clusters per IIQ           │             PDF/CSV report export              │   │
│   │            PAPI TCP 8080 or 8083             │           Email alert notifications            │   │
│   │           SmartConnect for DNS LB            │             API for custom tooling             │   │
│   │           Cluster admin read-only            │             Grafana via REST proxy             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  InsightIQ VM → PAPI TCP 8080 → PowerScale nodes · UI on TCP 443 from browser                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  PAPI = PowerScale Platform API; primary data source for InsightIQ                                    │
│  TCP 8080 = Default PAPI port; 8083 used for TLS PAPI                                                 │
│  SmartConnect = PowerScale DNS name for PAPI; InsightIQ connects via SmartConnect zone                │
│  Multiple clusters = Single InsightIQ VM can monitor multiple PowerScale clusters                     │
│  Email alert = SMTP notification when threshold exceeded; recipient list in InsightIQ settings        │
│  REST API = InsightIQ exposes limited API for programmatic data retrieval                             │
│  Grafana = Custom metrics panels built by exposing InsightIQ data via REST proxy                      │
│  CSV export = Downloading metric data for external BI or spreadsheet analysis                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Scope Limitation

- InsightIQ monitors **PowerScale only** — it does not support PowerStore, Unity, or PowerMax
- For multi-vendor monitoring, use CloudIQ (Dell) or Aria Operations with storage Management Packs
- No native CMDB connector — update CMDB entries manually or via API scripting
