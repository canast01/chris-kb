# Pure1 Architecture
## Overview

Pure1 is Pure Storage's cloud-based management and analytics platform for FlashArray and FlashBlade systems. It requires no on-premises management infrastructure — each array connects to Pure1 directly via outbound HTTPS. Pure1 provides AI-driven analytics (Pure1 Meta), capacity forecasting, health scoring, and a REST API for programmatic fleet management.

## Architecture

```
On-Premises                                Pure Storage Cloud
┌──────────────────────────┐              ┌──────────────────────────────────┐
│  FlashArray//X            │──[HTTPS]────►│  Pure1 SaaS Platform             │
│  FlashArray//C            │──[HTTPS]────►│  - Health monitoring              │
│  FlashBlade/S             │──[HTTPS]────►│  - Capacity forecasting           │
│  FlashArray//XL           │──[HTTPS]────►│  - Performance analytics          │
└──────────────────────────┘              │  - Alert engine                   │
                                          │  - Pure1 Meta (AI/ML engine)      │
                                          │  - REST API v1/v2                 │
                                          └──────────────────────────────────┘
```

## Component Roles

| Component | Role |
|---|---|
| Pure1 Cloud | SaaS platform — health, capacity, performance data, alerts, REST API |
| Array Purity OS | Generates telemetry; uploads to Pure1 via outbound HTTPS automatically |
| Pure1 Meta | AI/ML engine — workload analytics, anomaly detection, capacity forecasting |
| Pure1 REST API | Programmatic access to fleet data: v1 (arrays) and v2 (tags, subscriptions) |

## Telemetry Collection

- Arrays initiate outbound HTTPS connections to Pure1 cloud endpoints
- No inbound firewall rules required
- No on-premises proxy or collector appliance needed
- Collection interval: every 30 seconds for performance metrics; health and capacity data refreshes more frequently
- Data is associated with the array's serial number and tied to the customer's Pure1 tenant

### Telemetry Data Types

| Data Type | Examples |
|---|---|
| Performance metrics | IOPS, throughput (read/write), latency (read/write/mirror) |
| Capacity | Used, provisioned, physical used, data reduction ratio, snapshot capacity |
| Health | Component health (controllers, shelves, drives), Purity version |
| Configuration | Volume names, host connections, protection groups (metadata only) |

## Pure1 Meta

Pure1 Meta is the AI/ML analytics layer. Capabilities include:

- **Workload fingerprinting**: identifies workload types and patterns per array and per volume
- **Anomaly detection**: surfaces performance anomalies against learned baselines
- **Capacity forecasting**: predicts days to capacity exhaustion per array
- **Recommended actions**: capacity expansion suggestions, configuration optimisations

## Data Retention

| Metric Type | Retention |
|---|---|
| Performance metrics | 90 days rolling (default) |
| Capacity trends | 90 days rolling |
| Health event history | Available for the array's lifetime in Pure1 |

Note: Pure Storage retains the data longer internally for trend analysis — the 90-day window applies to customer-accessible API queries.

## Network Requirements

| Source | Destination | Port | Purpose |
|---|---|---|---|
| FlashArray / FlashBlade (management IP) | pure1.purestorage.com | TCP 443 | Telemetry upload |
| Browser | pure1.purestorage.com | TCP 443 | Pure1 web UI |
| Automation scripts | api.pure1.purestorage.com | TCP 443 | REST API access |

If arrays are behind a proxy:
```text
Purity CLI: purearray set --proxy https://<proxy-host>:<port>
Verify: purearray list --network
```

## High Availability

Pure1 is managed entirely by Pure Storage as a SaaS platform. Availability SLA and disaster recovery are Dell's responsibility. Customer action is not required for Pure1 infrastructure HA.
