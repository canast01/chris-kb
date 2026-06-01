# CloudIQ — Architecture (Monitoring)

<div class="kb-summary">
CloudIQ is a SaaS AIOps platform. The only on-premises component is the Secure Connect Gateway (SCG) virtual appliance, which collects telemetry from Dell arrays and forwards it outbound over HTTPS — no inbound firewall rules required.
</div>

```
┌─────────────────────────────────────── CloudIQ — Architecture ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                          Dell Cloud (cloudiq.dell.com) — SaaS backend                         │   │
│   │                AI/ML Engine · Time-series DB · Alert Engine · REST API · Web UI               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Telemetry flows outbound from arrays over HTTPS/443 to Dell cloud; no inbound connections          │
│                                                                                                       │
│                                                  ▼                                                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             On-Premises Sources              │  │                 Connectivity                │   │
│   │              PowerStore native               │  │            Direct: array → cloud            │   │
│   │              PowerScale native               │  │             Gateway VM optional             │   │
│   │               PowerFlex native               │  │              HTTPS TCP 443 only             │   │
│   │               Unity XT native                │  │               Proxy supported               │   │
│   │               PowerMax with DM               │  │                SNI-based mTLS               │   │
│   │                 VMAX via SRM                 │  │               No VPN required               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Dell arrays: physical hardware on-prem · Gateway VM: 2 vCPU/4 GB if needed · TCP 443 outbound        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SaaS = Software as a Service; CloudIQ hosted and operated by Dell in cloud                           │
│  Gateway VM = Optional on-prem virtual machine proxying telemetry for arrays without direct reach     │
│  Telemetry = Metrics, logs, events, and configuration data pushed from arrays to CloudIQ              │
│  mTLS = Mutual TLS; both client and server authenticate with certificates                             │
│  SNI = Server Name Indication; TLS extension allowing multiple hostnames on one IP                    │
│  DM = Data Mobility component for PowerMax CloudIQ registration                                       │
│  Time-series DB = Database optimised for sequential metric storage and range queries                  │
│  AI/ML engine = Machine learning models trained on Dell fleet data for anomaly and failure prediction │
│  REST API = CloudIQ programmatic interface for custom dashboards and automation                       │
│  Native integration = Array firmware sends telemetry directly without additional software             │
│  Proxy support = HTTP proxy configuration on gateway or array for internet access                     │
│  No inbound = CloudIQ never initiates connections to customer network; telemetry is push-only         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────────── CloudIQ — Architecture ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                          Dell Cloud (cloudiq.dell.com) — SaaS backend                         │   │
│   │                AI/ML Engine · Time-series DB · Alert Engine · REST API · Web UI               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Telemetry flows outbound from arrays over HTTPS/443 to Dell cloud; no inbound connections          │
│                                                                                                       │
│                                                  ▼                                                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             On-Premises Sources              │  │                 Connectivity                │   │
│   │              PowerStore native               │  │            Direct: array → cloud            │   │
│   │              PowerScale native               │  │             Gateway VM optional             │   │
│   │               PowerFlex native               │  │              HTTPS TCP 443 only             │   │
│   │               Unity XT native                │  │               Proxy supported               │   │
│   │               PowerMax with DM               │  │                SNI-based mTLS               │   │
│   │                 VMAX via SRM                 │  │               No VPN required               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Dell arrays: physical hardware on-prem · Gateway VM: 2 vCPU/4 GB if needed · TCP 443 outbound        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SaaS = Software as a Service; CloudIQ hosted and operated by Dell in cloud                           │
│  Gateway VM = Optional on-prem virtual machine proxying telemetry for arrays without direct reach     │
│  Telemetry = Metrics, logs, events, and configuration data pushed from arrays to CloudIQ              │
│  mTLS = Mutual TLS; both client and server authenticate with certificates                             │
│  SNI = Server Name Indication; TLS extension allowing multiple hostnames on one IP                    │
│  DM = Data Mobility component for PowerMax CloudIQ registration                                       │
│  Time-series DB = Database optimised for sequential metric storage and range queries                  │
│  AI/ML engine = Machine learning models trained on Dell fleet data for anomaly and failure prediction │
│  REST API = CloudIQ programmatic interface for custom dashboards and automation                       │
│  Native integration = Array firmware sends telemetry directly without additional software             │
│  Proxy support = HTTP proxy configuration on gateway or array for internet access                     │
│  No inbound = CloudIQ never initiates connections to customer network; telemetry is push-only         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![CloudIQ Architecture](../../../assets/cloudiq-monitoring-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>SaaS architecture, SCG sizing, telemetry collection, data residency, and network requirements.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Supported Dell platforms, ServiceNow, SIEM, and notification integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>SCG deployment standards, naming conventions, and configuration baselines.</span></a>
</div>

---

## Component Roles

| Component | Role |
|---|---|
| CloudIQ Cloud | SaaS platform hosted by Dell — health scores, capacity forecasts, AI recommendations |
| Secure Connect Gateway (SCG) | On-premises OVA; collects telemetry and relays to CloudIQ over HTTPS |
| CloudIQ REST API | Programmatic access to fleet data, alerts, and capacity metrics |

---

## Architecture


