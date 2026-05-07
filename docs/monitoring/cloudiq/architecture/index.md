# CloudIQ Architecture
## Overview

Dell CloudIQ is a cloud-native SaaS AIOps platform that collects telemetry from Dell storage, server, and networking systems. All communication is outbound HTTPS from an on-premises Secure Connect Gateway (SCG) virtual appliance — no inbound firewall rules are required. The platform provides health scores, capacity forecasts, anomaly detection, and AI-driven recommendations via a web dashboard and REST API.

## Architecture Diagram

```
On-Premises                           Dell Cloud
┌─────────────────────────────┐       ┌─────────────────────────────┐
│  Dell Arrays / Servers       │       │  CloudIQ SaaS Platform       │
│  (PowerStore, PowerMax,      │──────►│  - Health scoring engine     │
│   PowerScale, Unity XT,      │       │  - AI/AIOps recommendations  │
│   Data Domain, PowerEdge)    │       │  - Capacity forecasting      │
│                              │       │  - REST API                  │
│  Secure Connect Gateway(SCG) │──────►│  - Web dashboard             │
│  (OVA on-prem)               │ HTTPS │                              │
└─────────────────────────────┘  443   └─────────────────────────────┘
```

## Component Roles

| Component | Role |
|---|---|
| CloudIQ Cloud | SaaS platform hosted and managed by Dell |
| Secure Connect Gateway (SCG) | On-premises virtual appliance; collects telemetry from arrays and relays to CloudIQ over HTTPS |
| CloudIQ Dashboard | Web UI presenting health scores, alerts, capacity trends, and anomaly detections |
| CloudIQ REST API | Programmatic access to fleet data, alerts, and capacity metrics |
| Dell AIOps (integrated) | AI recommendations layer within CloudIQ for root cause analysis and predictive insights |

## Secure Connect Gateway (SCG)

The SCG is the sole on-premises component. Key characteristics:

- Deployed as a Linux-based OVA (VMware or KVM)
- Communicates to Dell cloud endpoints on TCP 443 outbound only
- Supports proxy configuration for environments without direct internet egress
- Collects from arrays via management IP — requires reachability to all array management interfaces
- Supports multiple sites; a single SCG can collect from arrays across multiple subnets if routable

### SCG System Requirements

| Resource | Minimum | Recommended |
|---|---|---|
| vCPU | 4 | 8 |
| RAM | 8 GB | 16 GB |
| Disk | 100 GB | 200 GB |
| OS | RHEL/CentOS 7/8 or OVA | OVA preferred |

## Telemetry Collection

- Collection interval: typically every 5 minutes for performance metrics; health scores refresh every 15–30 minutes
- Protocol: HTTPS (REST API calls from SCG to array management endpoint)
- Supported platforms: PowerStore, PowerMax/VMAX, PowerScale/Isilon, Unity XT, Data Domain/PowerProtect, PowerVault, PowerEdge (via iDRAC)

## Data Residency

CloudIQ telemetry is processed and stored in Dell's cloud infrastructure. Confirm with Dell that data is stored in the appropriate region for compliance requirements (EU customers should verify GDPR residency options).

## Network Requirements

| Source | Destination | Port | Purpose |
|---|---|---|---|
| SCG | Dell cloud (cloudiq.dell.com) | TCP 443 | Telemetry upload |
| SCG | Array management IPs | TCP 443 / 8443 | Telemetry collection |
| Browser (admin) | SCG management UI | TCP 9443 | SCG administration |
| Browser (ops) | cloudiq.dell.com | TCP 443 | CloudIQ web dashboard |
