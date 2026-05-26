# Nexus Dashboard: Insights, Orchestrator, and Data Broker Integrations

Cisco Nexus Dashboard acts as a hosting platform for multiple services: Nexus Dashboard Insights (NDI), Nexus Dashboard Orchestrator (NDO), and Nexus Dashboard Data Broker (NDDB). This page covers how to install, configure, and verify these service integrations.

## Nexus Dashboard Services Overview

Nexus Dashboard is the hosting platform — individual services are installed as separate applications.

| Service | Purpose | Primary Fabric Type |
|---|---|---|
| Nexus Dashboard Insights (NDI) | Telemetry, anomaly detection, health scoring | ACI, NX-OS (NDFC) |
| Nexus Dashboard Orchestrator (NDO) | Multi-site ACI policy management | ACI multi-site |
| Nexus Dashboard Data Broker (NDDB) | Traffic tapping, monitoring port groups | ACI, NX-OS |
| Nexus Dashboard Fabric Controller (NDFC) | NX-OS fabric provisioning and management | NX-OS |

## Installing a Service Application

```bash
# List installed services on Nexus Dashboard
curl -sk -X GET \
  "https://nexus-dashboard.example.com/nexus/infra/api/v1/apps" \
  -H "Authorization: Bearer <token>" \
  | jq '.data[] | {name, version, status}'

# Trigger service installation from a local image
curl -sk -X POST \
  "https://nexus-dashboard.example.com/nexus/infra/api/v1/apps/install" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@nd-insights-4.2.1.tar.gz"
```
┌─────────────────────────────────── Nexus Dashboard — Integrations ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                Fabric Sources                │               Management Targets               │   │
│   │             ACI multi-site APIC              │           Cisco TAC Smart Call Home            │   │
│   │               NX-OS DCNM/NDFC                │            ServiceNow CMDB + events            │   │
│   │             HyperFlex Intersight             │           PagerDuty on-call routing            │   │
│   │                SD-WAN vManage                │             Splunk / Elastic SIEM              │   │
│   │             Kubernetes (ND Apps)             │              Webex Teams / Slack               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  ND data network to fabrics · ND management to cloud SaaS targets · TCP 443 outbound                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Multi-site APIC = Multiple ACI fabrics each with their own APIC registered in ND                     │
│  Smart Call Home = Cisco TAC automatic support case from ND critical events                           │
│  CMDB = ServiceNow Configuration Management DB; ND updates CIs from fabric inventory                  │
│  HyperFlex = Cisco HCI; managed via Intersight; ND can pull cluster health                            │
│  SD-WAN vManage = Cisco SD-WAN controller; ND integration for WAN edge visibility                     │
│  ND Apps = NDI, NDFC, NDO run as Kubernetes apps inside ND cluster                                    │
│  Webex Teams = Cisco collaboration; NDI posts events to room via webhook                              │
│  Splunk / Elastic = SIEM platforms receiving ND syslog or HEC event streams                           │
│  PagerDuty = On-call routing; ND sends events via Events API v2                                       │
│  Cisco TAC = Technical Assistance Centre; Smart Call Home auto-opens cases                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## NDDB Traffic Tapping

NDDB allows traffic from production ACI ports to be mirrored to monitoring tool ports without dedicated TAPs.

Configuration steps:
1. Navigate to **NDDB > Monitoring Domains > Add**.
2. Define monitoring tool ports (where traffic is sent).
3. Create a filter (match traffic by VLAN, IP prefix, or port).
4. Create a monitoring session linking production ports to tool ports.

```bash
# List NDDB monitoring sessions
curl -sk -X GET \
  "https://nexus-dashboard.example.com/nddb/api/v1/sessions" \
  -H "Authorization: Bearer <token>" | jq '.sessions[] | {name, status, filterCount}'
```

## Common Integration Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| NDI fabric shows "Disconnected" | APIC credentials changed or expired | Update credentials in NDI > Settings > Fabric Connections |
| NDO site sync failing | ND and APIC version incompatibility | Check Cisco compatibility matrix |
| Service app stuck in "Installing" | Insufficient cluster resources | Verify ND node CPU/memory meets requirements |
| NDDB session not capturing traffic | SPAN filter mismatch | Review VLAN/EPG filter configuration |
| NDI telemetry gaps | Network path between leaf and ND blocked | Open UDP 5640 (ERSPAN) between fabric and ND cluster |
