# Nexus Dashboard: Endpoint Tracking, Flow Visibility, and Topology View

Cisco Nexus Dashboard Insights provides comprehensive visibility into fabric endpoints, traffic flows, and the physical and logical topology of ACI and NX-OS fabrics. This page covers how to use these visibility features for day-to-day operations and troubleshooting.

## Endpoint Tracking

NDI continuously tracks all endpoints (IP/MAC pairs) learned in the fabric. This is useful for confirming VM connectivity, tracing moves, and verifying policy enforcement.

Navigation: **NDI > Browse > Endpoints**

```bash
# Search for an endpoint by IP
curl -sk -X POST \
  "https://nexus-dashboard.example.com/nexus/infra/api/v3/insights/endpoints/query" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"ip": "10.10.20.50"}, "limit": 10}'

# Search for an endpoint by MAC address
curl -sk -X POST \
  "https://nexus-dashboard.example.com/nexus/infra/api/v3/insights/endpoints/query" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"mac": "00:50:56:ab:cd:ef"}}'
```

Endpoint detail fields:

| Field | Description |
|---|---|
| `ip` | IP address of the endpoint |
| `mac` | MAC address |
| `epg` | ACI EPG the endpoint belongs to |
| `node` | Leaf switch it is attached to |
| `port` | Physical port on the leaf |
| `encap` | VLAN or VXLAN encapsulation |
| `lastSeen` | Timestamp of last activity |

## Flow Visibility

NDI collects flow records from the fabric to provide per-connection visibility.

Navigation: **NDI > Browse > Flows**

```bash
# Query flows between two endpoints
curl -sk -X POST \
  "https://nexus-dashboard.example.com/nexus/infra/api/v3/insights/flows/query" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "src_ip": "10.10.20.50",
      "dst_ip": "10.10.30.100",
      "protocol": "TCP"
    },
    "timeRange": {"start": "2026-05-07T08:00:00Z", "end": "2026-05-07T10:00:00Z"},
    "limit": 50
  }'

# Check for flows with fabric drops
curl -sk -X POST \
  "https://nexus-dashboard.example.com/nexus/infra/api/v3/insights/flows/query" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"drop_count_gt": 0}, "limit": 20}'
```

Flow record fields useful for troubleshooting:

| Field | Description |
|---|---|
| `latency_us` | One-way fabric latency in microseconds |
| `drop_count` | Packets dropped (policy or congestion) |
| `drop_reason` | Reason code for drops |
| `bytes` | Total bytes in the flow |
| `leaf_node` | Fabric node where flow was observed |

## Topology View

The topology view provides a visual map of the ACI or NX-OS fabric, showing node health, link utilisation, and connectivity.

Navigation: **NDI > Overview > Topology**

Features of the topology view:

| Feature | Description |
|---|---|
| Node health colouring | Green/yellow/red based on anomaly count |
| Link utilisation | Bandwidth saturation visualised on links |
| Drill-down | Click a node to see its anomalies and stats |
| Path trace | Trace the path between two endpoints through the fabric |

## Path Trace for Troubleshooting

Path trace is one of the most powerful NDI features — it shows the exact fabric path between two endpoints including interfaces, nodes, and any policy drops.

Navigation: **NDI > Troubleshoot > Path Trace**

```bash
# Initiate a path trace via API
curl -sk -X POST \
  "https://nexus-dashboard.example.com/nexus/infra/api/v3/insights/pathtrace" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "srcIP": "10.10.20.50",
    "dstIP": "10.10.30.100",
    "srcPort": 443,
    "dstPort": 0,
    "protocol": "TCP",
    "fabricName": "prod-aci-fabric"
  }'

# Get path trace result
curl -sk -X GET \
  "https://nexus-dashboard.example.com/nexus/infra/api/v3/insights/pathtrace/<traceId>" \
  -H "Authorization: Bearer <token>" | jq '.pathNodes[] | {node, interface, policy, action}'
```

## Common Visibility Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Endpoint not found | Not yet learned or aged out | Check on leaf: `show endpoint ip <ip>` |
| Flow data missing | Telemetry not enabled on leaf | Verify ERSPAN/sFlow config on fabric switches |
| Path trace shows "No path" | Policy contract missing | Check ACI contracts between source and destination EPGs |
| Topology not loading | NDI not connected to APIC | Re-check fabric connection in NDI settings |
| Latency values all zero | Latency telemetry requires specific hardware | Verify leaf hardware supports latency reporting |
