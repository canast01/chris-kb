# Operations

> Part of the [NSX](../) reference.

---

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| [ ] NSX-T Manager UI → System → Overview |  | confirm overall system health is green, no component warnings |
| [ ] `GET /api/v1/cluster/status` | `GET /api/v1/cluster/status` | management cluster status should show `STABLE`; flag any `DEGRADED` or `UNSTABLE` nodes |
| [ ] `GET /api/v1/transport-nodes/status` | `GET /api/v1/transport-nodes/status` | all transport nodes should report `UP`; flag any `DOWN` or `DEGRADED` |
| [ ] Check Edge cluster health | `GET /api/v1/edge-clusters` | all Edge nodes reachable and healthy |
| [ ] `GET /api/v1/alarms?status=OPEN` | `GET /api/v1/alarms?status=OPEN` | review all open alarms; action any at HIGH or CRITICAL severity |
| [ ] Verify T0/T1 BGP sessions are established (if BGP in use): NSX-T UI → Networking → T0 Gateways → BGP Neighbors, or from Edge CLI | `get logical-router <id> bgp neighbor summary` |  |
| [ ] Check DFW rule count is not approaching platform limits |  |  |
| [ ] Review NSX Manager backup status |  |  |

## Health Check

- [ ] Management cluster stable: `GET /api/v1/cluster/status`
- [ ] All transport nodes UP: `GET /api/v1/transport-nodes/status`
- [ ] All Edge nodes reachable: `GET /api/v1/edge-clusters`
- [ ] No open HIGH or CRITICAL alarms: `GET /api/v1/alarms?status=OPEN`
- [ ] BGP sessions established on all T0 gateways
- [ ] Overlay tunnels healthy (GENEVE): `GET /api/v1/tunnel-endpoints`
- [ ] DFW rule count within safe limits
- [ ] NSX Manager backup current

```bash
# NSX-T REST API health checks (replace <nsx-manager> and use a valid session token)
curl -sk -u 'admin' https://<nsx-manager>/api/v1/cluster/status
curl -sk -u 'admin' https://<nsx-manager>/api/v1/transport-nodes/status
curl -sk -u 'admin' https://<nsx-manager>/api/v1/alarms?status=OPEN

# From Edge node CLI (SSH to Edge)
get logical-router <tier0-router-id> bgp neighbor summary
get tunnel-port status
```

## Change Readiness

- [ ] NSX Manager backup is current — confirm backup completed within the last 24 hours
- [ ] Edge cluster healthy — all Edge nodes UP and BGP sessions established before any change
- [ ] All transport node health confirmed UP: `GET /api/v1/transport-nodes/status`
- [ ] DFW rule change reviewed for impact — confirm rule ordering and scope are correct before push
- [ ] Rollback plan for routing changes documented — BGP prefix filter or static route revert procedure confirmed
- [ ] Change window approved and communicated to networking and compute teams
- [ ] BFD session health confirmed if used for fast failover detection

| Item | Status | Notes |
|---|---|---|
| NSX Manager backup current | | Backup timestamp confirmed |
| Edge cluster healthy | | All Edge nodes UP |
| Transport nodes all UP | | API status check |
| DFW rule change reviewed | | Peer review completed |
| Change window approved | | Ticket reference |

## Incident Triage

- [ ] Check transport node status: `GET /api/v1/transport-nodes/status` — identify any DOWN or DEGRADED nodes
- [ ] Check Edge node health: NSX-T UI → System → Fabric → Nodes → Edge Transport Nodes
- [ ] Review open alarms: `GET /api/v1/alarms?status=OPEN` — filter by severity HIGH or CRITICAL
- [ ] Check specific segment or gateway for overlay connectivity: `GET /api/v1/logical-ports?logical_switch_id=<id>`
- [ ] Check DFW for unintended block rules if VM connectivity is affected: review recent DFW rule changes in NSX audit log
- [ ] Verify BGP sessions from Edge CLI: `get logical-router <id> bgp neighbor summary` — look for sessions in Idle or Connect state
- [ ] Check BFD session health if fast convergence is configured
- [ ] If management cluster is degraded, check NSX Manager VM health, disk space, and service status on the appliance

| Question | Answer |
|---|---|
| Are transport nodes UP? | `GET /api/v1/transport-nodes/status` |
| Are Edge nodes reachable? | NSX-T UI → Fabric → Edge Transport Nodes |
| What alarms are open? | `GET /api/v1/alarms?status=OPEN` |
| Are BGP sessions established? | Edge CLI: `get logical-router <id> bgp neighbor summary` |
| Is DFW blocking traffic? | Review recent DFW rule changes and audit log |

## Maintenance Window

1. Confirm all transport nodes are UP and no open HIGH/CRITICAL alarms before starting
2. Take NSX Manager backup via UI → System → Backup & Restore — confirm backup completes successfully
3. For Edge node maintenance: migrate Edge workloads off the affected Edge node if possible (active/standby failover)
4. Perform the required work on the Edge node or transport node
5. After work is complete, confirm the node is back UP: `GET /api/v1/transport-nodes/status`
6. Validate routing: check BGP neighbor sessions are re-established from Edge CLI
7. Confirm BFD sessions restored if BFD is configured
8. Verify DFW rules are still applied correctly: spot-check connectivity for key VMs through the affected segment

## Post-Change Validation

- [ ] All transport nodes UP: `GET /api/v1/transport-nodes/status` — no DOWN or DEGRADED entries
- [ ] No open HIGH or CRITICAL alarms: `GET /api/v1/alarms?status=OPEN`
- [ ] BGP sessions established on all T0 gateways — confirmed from Edge CLI
- [ ] BFD sessions restored (if applicable)
- [ ] DFW rules applied correctly — test VM-to-VM connectivity through affected segments
- [ ] Overlay network connectivity verified — GENEVE tunnels healthy
- [ ] NSX Manager backup taken post-change to capture final configuration state
- [ ] Close change ticket with transport node status and BGP summary output attached
