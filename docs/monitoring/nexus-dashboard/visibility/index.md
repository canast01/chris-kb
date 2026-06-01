# Nexus Dashboard: Endpoint Tracking, Flow Visibility, and Topology View


<div class="kb-summary">
Nexus Dashboard: Endpoint Tracking, Flow Visibility, and Topology View reference covering Flow Visibility, Topology View, Path Trace for Troubleshooting, Common Visibility Issues.
</div>

```text
┌──────────────────────────────────── Nexus Dashboard — Visibility ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        NDI Visibility: comprehensive view of fabric state — topology, endpoints, flows        │   │
│   │             Topology view: interactive map of spine/leaf/border-leaf interconnects            │   │
│   │           Endpoint tracking: VM/container moves, dual-home detection, stale entries           │   │
│   │              Flow analytics: per-flow visibility with source/dest/protocol/bytes              │   │
│   │              Audit trail: who changed what and when across ACI and NX-OS fabrics              │   │
│   │               Multi-site: unified view across multiple ACI domains in single UI               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Visibility data from APIC REST + MDT streaming · stored in NDI DB · rendered in ND UI                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Topology view = Interactive fabric map showing switch interconnects and health                       │
│  Endpoint = VM, container, or bare-metal IP/MAC connected to fabric leaf                              │
│  Dual-home = Endpoint connected to two leaf switches for redundancy                                   │
│  Stale endpoint = Endpoint record remaining after VM is deleted; detected by NDI                      │
│  Flow analytics = NDI tracking actual traffic flows through fabric for visibility                     │
│  Audit trail = NDI logging all APIC configuration changes with user and timestamp                     │
│  Multi-site view = Single ND UI showing health and state for all registered ACI sites                 │
│  EPG = Endpoint Group; ACI policy construct; endpoints grouped by EPG                                 │
│  Contract = ACI inter-EPG connectivity policy; NDI verifies enforcement                               │
│  BD = Bridge Domain; ACI Layer-2 forwarding domain containing EPGs                                    │
│  Border leaf = Leaf switch connecting ACI fabric to external L3 networks                              │
│  Delta analysis = NDI showing configuration changes between two epochs                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
