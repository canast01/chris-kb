# NSX — Health Checks

## Daily Checks

| Check | Command / Location | Notes |
|---|---|---|
| [ ] NSX Manager system health | UI → System → Overview | Overall health should be green |
| [ ] Management cluster status | `GET /api/v1/cluster/status` | Should show `STABLE` |
| [ ] Transport node status | `GET /api/v1/transport-nodes/status` | All should report `UP` |
| [ ] Edge cluster health | `GET /api/v1/edge-clusters` | All Edge nodes reachable |
| [ ] Open alarms | `GET /api/v1/alarms?status=OPEN` | Action any HIGH or CRITICAL |
| [ ] BGP neighbours | UI → Networking → T0 Gateways → BGP Neighbors | All peers `Established` |
| [ ] DFW rule count | UI → Security → Distributed Firewall | Not approaching platform limits |
| [ ] NSX Manager backup | UI → System → Backup & Restore | Confirm last backup timestamp |

## Health Check Commands

```bash
# NSX-T REST API health checks
curl -sk -u 'admin' https://<nsx-manager>/api/v1/cluster/status
curl -sk -u 'admin' https://<nsx-manager>/api/v1/transport-nodes/status
curl -sk -u 'admin' https://<nsx-manager>/api/v1/alarms?status=OPEN

# From Edge node CLI (SSH to Edge)
get logical-router <tier0-router-id> bgp neighbor summary
get tunnel-port status
```

## Change Readiness

- [ ] NSX Manager backup current (within 24 hours)
- [ ] Edge cluster healthy — all Edge nodes UP and BGP sessions established
- [ ] All transport nodes UP
- [ ] DFW rule change reviewed — rule ordering and scope confirmed correct
- [ ] Rollback plan documented for routing changes
- [ ] Change window approved and communicated to networking and compute teams

| Item | Status | Notes |
|---|---|---|
| NSX Manager backup current | | Backup timestamp confirmed |
| Edge cluster healthy | | All Edge nodes UP |
| Transport nodes all UP | | API status check |
| DFW rule change reviewed | | Peer review completed |
| Change window approved | | Ticket reference |
