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
```

## Configuring NDO Multi-Site

NDO manages policy across multiple ACI sites from a single pane.

Navigation: **NDO > Infrastructure > Sites > Add Site**

```bash
# Register an APIC site to NDO
curl -sk -X POST \
  "https://nexus-dashboard.example.com/mso/api/v1/sites" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "site-london",
    "type": "aci",
    "apicUrls": ["https://apic-lon.example.com"],
    "username": "ndo-admin",
    "password": "password",
    "useProxy": false
  }'
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
