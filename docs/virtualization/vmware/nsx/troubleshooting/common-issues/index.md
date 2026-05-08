# NSX — Common Issues

## Incident Triage

- [ ] Check transport node status: `GET /api/v1/transport-nodes/status` — identify DOWN or DEGRADED nodes
- [ ] Check Edge node health: UI → System → Fabric → Nodes → Edge Transport Nodes
- [ ] Review open alarms: `GET /api/v1/alarms?status=OPEN` — filter by HIGH or CRITICAL
- [ ] Check segment/gateway overlay connectivity: `GET /api/v1/logical-ports?logical_switch_id=<id>`
- [ ] Check DFW for unintended block rules if VM connectivity is affected — review recent DFW changes in NSX audit log
- [ ] Verify BGP sessions from Edge CLI: `get logical-router <id> bgp neighbor summary`
- [ ] Check BFD session health if fast convergence is configured
- [ ] If management cluster degraded: check NSX Manager VM health, disk space, and service status

| Question | First Check |
|---|---|
| Are transport nodes UP? | `GET /api/v1/transport-nodes/status` |
| Are Edge nodes reachable? | UI → Fabric → Edge Transport Nodes |
| What alarms are open? | `GET /api/v1/alarms?status=OPEN` |
| Are BGP sessions established? | Edge CLI: `get logical-router <id> bgp neighbor summary` |
| Is DFW blocking traffic? | Review recent DFW rule changes and audit log |

## Quick Diagnostics

### Edge Node Health

```bash
# On NSX Manager API
GET /api/v1/transport-nodes/<edge-node-id>/status

# Via CLI on Edge node (SSH)
get service router
get bgp neighbor summary
get logical-routers
ping ++netstack=vxlan <remote-tep-ip>
```

### Transport Node Status

```bash
GET /api/v1/transport-nodes?transport_zone_id=<tz-id>
GET /api/v1/transport-nodes/<node-id>

# On ESXi host — confirm TEP IP assigned
esxcli network ip interface ipv4 get
esxcli network ip route ipv4 list
```
