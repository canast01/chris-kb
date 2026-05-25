# Nexus Dashboard: Fabric Health Score, Endpoint Reachability, and Flow Telemetry

```text
Fabric Health — Nexus Dashboard
┌──────────────────────────────────────────────┐
│  Spine/Leaf Status   BGP Sessions   VTEPs    │
│  ┌────────┐          ┌───────────┐           │
│  │Spine 1 │ healthy  │ BGP: 8/8  │ VTEP: 12 │
│  │Spine 2 │ healthy  │ OSPF: 4/4 │ active   │
│  │Leaf 1  │ healthy  └───────────┘           │
│  │Leaf 2  │ warning ◄── port errors          │
│  │Leaf 3  │ healthy                          │
│  └────────┘                                  │
├──────────────────────────────────────────────┤
│  Inter-Fabric Links      Endpoint Reach.     │
│  ISL-1  ████  45% util   10.0.0.1  reachable │
│  ISL-2  █     8% util    10.0.0.2  reachable │
│                          10.0.0.50 stale  !  │
└──────────────────────────────────────────────┘
```

Cisco Nexus Dashboard Insights provides a fabric health score for ACI and NX-OS fabrics, along with endpoint reachability tracking and flow telemetry visualisation. This page covers how to interpret the health score, verify endpoint reachability, and use flow data for troubleshooting.

## Fabric Health Score

The fabric health score (0–100) is a composite metric derived from anomaly counts, severity weighting, and fabric size.

Navigation: **Nexus Dashboard > Insights > Overview**

```bash
# Get fabric health score via API
curl -sk -X GET \
  "https://nexus-dashboard.example.com/nexus/infra/api/v3/insights/fabricHealthScore" \
  -H "Authorization: Bearer <token>" | jq '.data[] | {fabricName, healthScore, delta}'
```

Health score components:

| Component | Weight | Description |
|---|---|---|
| Anomaly count | High | Number of active anomalies weighted by severity |
| Configuration compliance | Medium | Deviations from fabric best practices |
| Connectivity health | High | BGP, OSPF, fabric link status |
| Hardware health | Medium | Interface errors, transceiver alarms |
| Resource utilisation | Low | TCAM, buffer, CPU headroom |

## Interpreting Health Score Changes

| Score Change | Trigger Examples |
|---|---|
| Drop > 10 points | Major connectivity event, multiple critical anomalies |
| Drop 5–10 points | New warning anomalies detected |
| Drop 1–5 points | Minor configuration drift |
| Score increasing | Anomalies resolving, maintenance completed |

## Endpoint Reachability

NDI tracks endpoint (IP/MAC) reachability across the fabric and can detect when an endpoint moves, disappears, or is unreachable.

Navigation: **Insights > Endpoints**

```bash
# Search for an endpoint by IP address
curl -sk -X POST \
  "https://nexus-dashboard.example.com/nexus/infra/api/v3/insights/endpoints/query" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"ip": "10.0.10.50"}}'

# Get endpoint reachability history
curl -sk -X GET \
  "https://nexus-dashboard.example.com/nexus/infra/api/v3/insights/endpoints/<endpointId>/reachability" \
  -H "Authorization: Bearer <token>" | jq '.data'
```

Endpoint reachability states:

| State | Meaning |
|---|---|
| Reachable | Endpoint responding and fabric path intact |
| Unreachable | No ICMP response or ARP not resolved |
| Moved | Endpoint detected on different leaf/port |
| Stale | Last seen > configurable threshold ago |

## Flow Telemetry

Nexus Dashboard Insights collects NetFlow/sFlow data to provide per-flow visibility including source, destination, protocol, and latency.

Navigation: **Insights > Flow Analytics**

```bash
# Query top flows by byte count
curl -sk -X POST \
  "https://nexus-dashboard.example.com/nexus/infra/api/v3/insights/flows/query" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "fabricName": "prod-aci-fabric",
      "timeRange": {"start": "2026-05-07T00:00:00Z", "end": "2026-05-07T23:59:59Z"}
    },
    "sort": [{"field": "bytes", "order": "desc"}],
    "limit": 20
  }'
```

Flow telemetry fields:

| Field | Description |
|---|---|
| `src_ip` / `dst_ip` | Source and destination IP |
| `src_port` / `dst_port` | Transport layer ports |
| `protocol` | TCP, UDP, ICMP |
| `bytes` | Total bytes transferred |
| `latency_us` | Fabric latency in microseconds |
| `drop_count` | Packets dropped in fabric |

## Using Flow Data for Troubleshooting

```bash
# Identify dropped flows between two hosts
curl -sk -X POST \
  "https://nexus-dashboard.example.com/nexus/infra/api/v3/insights/flows/query" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "src_ip": "10.0.10.100",
      "dst_ip": "10.0.20.50",
      "drop_count_gt": 0
    }
  }'
```

## Common Fabric Health Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Health score drops after upgrade | Post-upgrade anomalies detected | Review anomalies; acknowledge known post-upgrade events |
| Endpoint shown as unreachable | ARP entry expired or NIC offline | Check physical connectivity and ARP table on leaf |
| Flow telemetry missing | Telemetry not configured on switches | Enable NetFlow/ERSPAN on fabric switches |
| Health score not updating | NDI service connectivity issue | Check NDI cluster status in Nexus Dashboard services page |
| Endpoint shown in wrong EPG | VM migrated but policy not followed | Check VMM integration policy and port-group mapping |
