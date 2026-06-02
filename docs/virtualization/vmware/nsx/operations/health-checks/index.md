# NSX — Health Checks


<div class="kb-summary">
Health Checks reference covering Daily Checks, Health Check Commands, Weekly Checks, Change Readiness Checklist.
</div>

## Daily Checks

| Check | Command / Location | Expected State |
|---|---|---|
| [ ] NSX Manager system health | UI → System → Overview | All green |
| [ ] Management cluster status | `GET /api/v1/cluster/status` | `STABLE` |
| [ ] Transport node status | `GET /api/v1/transport-nodes/status` | All UP (down_count = 0) |
| [ ] Edge cluster health | `GET /api/v1/edge-clusters` | All Edge nodes reachable |
| [ ] Open alarms | `GET /api/v1/alarms?status=OPEN` | Zero CRITICAL or HIGH |
| [ ] BGP neighbours | UI → Networking → T0 Gateways → BGP Neighbors | All peers `Established` |
| [ ] DFW rule count | UI → Security → Distributed Firewall | Not approaching platform limits |
| [ ] NSX Manager backup | UI → System → Backup & Restore | Last backup < 25 hours ago |
| [ ] Geneve tunnel health | `get tunnel status` on Manager CLI | All TEP pairs UP |

---

## Health Check Commands

### NSX Manager Cluster

```bash
# SSH to any NSX Manager node
nsxcli

# Cluster status (must show STABLE)
get cluster status

# Individual node reachability (all should show CONNECTED)
get managers

# Corfu (Raft DB) — control plane health
get corfu-cluster status

# All services running
get services | grep -v " running"
# The above grep shows any service NOT in running state — output should be empty
```
```
┌───────────────────────────────────────── NSX — Health Checks ─────────────────────────────────────────┐
│                                                                                                       │
│  Daily/weekly health runbook: cluster, transport nodes, edges, and DFW state.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Manager Cluster Health            │  │            Transport Node Health            │   │
│   │              All 3 nodes STABLE              │  │           All ESXi nodes: Success           │   │
│   │         CCP cluster: leader elected          │  │                Edge nodes: Up               │   │
│   │            MP: policy sync active            │  │              N-VDS status green             │   │
│   │           Certificate expiry check           │  │              Tunnel endpoint up             │   │
│   │            Backup age < 24 hours             │  │           BGP sessions established          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Manager health → transport nodes → edge BGP → DFW rule count check.                                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Edge Gateway Health              │  │            DFW and Policy Health            │   │
│   │          T0 gateway active standby           │  │             DFW rule sync green             │   │
│   │           BGP sessions up/prefixes           │  │           No policy realise errors          │   │
│   │             ECMP paths balanced              │  │          Groups resolved correctly          │   │
│   │               NAT rules active               │  │            Segment VNI table sync           │   │
│   │          Edge CPU < 70%, mem < 80%           │  │              Alarm queue empty              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  NSX Manager VMs, Edge VMs, ESXi transport nodes, physical ToR switches                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CCP         = Central Control Plane; distributes config to dataplane                                 │
│  MP          = Management Plane; NSX policy API and UI backend                                        │
│  N-VDS       = NSX virtual distributed switch; dataplane on ESXi/Edge                                 │
│  TEP         = Tunnel Endpoint; VTEP for GENEVE overlay encapsulation                                 │
│  GENEVE      = tunnel protocol; carries overlay traffic between TEPs                                  │
│  T0 gateway  = Tier-0; north-south routing; BGP to physical fabric                                    │
│  DFW         = Distributed Firewall; stateful kernel-level L4 firewall                                │
│  ECMP        = Equal Cost Multi-Path; load-balances traffic across paths                              │
│  Policy realise = NSX applying config changes to dataplane                                            │
│  VNI         = VXLAN Network Identifier; unique ID per overlay segment                                │
│  STABLE      = NSX Manager cluster status meaning all nodes healthy                                   │
│  BGP session = Edge peering with physical router; must be Established                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### BGP Neighbor Health (Edge CLI)

```bash
# SSH to each Edge node
vrf <tier0-vrf-id>
get bgp neighbor summary

# Expected output shows each peer with state=Established
# Any peer not Established = BGP issue; see Common Issues

# Specific peer detail
get bgp neighbor <peer-ip>
```

### Open Alarms

```bash
# Critical alarms (action required immediately)
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/alarms?status=OPEN&severity=CRITICAL" | python3 -c "
import sys, json
d = json.load(sys.stdin)
cnt = d.get('result_count', 0)
print(f'CRITICAL alarms open: {cnt}')
for a in d.get('results', []):
    print(f'  {a.get(\"alarm_source\",{}).get(\"display_name\",\"?\")} — {a.get(\"summary\",\"\")[:80]}')
"

# Medium alarms (monitor and plan)
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/alarms?status=OPEN&severity=MEDIUM" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'MEDIUM alarms open: {d.get(\"result_count\",0)}')
"
```

### DFW Platform Limits

NSX-T has platform limits on DFW objects. Monitor these to avoid hitting limits that would prevent policy changes:

| Object | Limit (per cluster) | Check |
|---|---|---|
| Security policies | 10,000 | UI → Security → Distributed Firewall → count |
| Rules per policy | 1,000 | API: list rules per policy |
| Total DFW rules | 100,000 | `GET /api/v1/firewall/sections` total rule count |
| Security groups | 10,000 | `GET /policy/api/v1/infra/domains/default/groups` |
| IP sets | 10,000 | — |

Alert when usage exceeds 70% of any limit.

---

## Weekly Checks

| Check | How | Expected State |
|---|---|---|
| [ ] Certificate expiry | `GET /api/v1/trust-management/certificates?details=true` | All certs > 60 days remaining |
| [ ] Backup verification | Verify SFTP has backup file from last 7 days | File present and non-zero |
| [ ] IP pool utilisation | `GET /api/v1/pools/ip-pools/<id>` | TEP pool has > 10 free IPs |
| [ ] Edge cluster HA test | Review HA state; test failover in lab | Active/Standby correctly assigned |
| [ ] vSphere cluster size changes | Any hosts added/removed from TNP scope? | All new hosts prepared as transport nodes |

### Certificate Check Script

```bash
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/trust-management/certificates?details=true" | \
  python3 -c "
import sys, json
from datetime import datetime, timezone
d = json.load(sys.stdin)
now = datetime.now(timezone.utc)
for c in d.get('results', []):
    name  = c.get('display_name', c.get('id','?'))
    exp   = c.get('not_after','')
    if exp:
        exp_dt = datetime.fromisoformat(exp.replace('Z','+00:00'))
        days   = (exp_dt - now).days
        flag   = '  OK' if days > 60 else '  *** EXPIRING' if days > 14 else '  *** CRITICAL'
        print(f'  {name:<40}  expires={exp[:10]}  days={days}{flag}')
"
```

### IP Pool Utilisation

```bash
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/pools/ip-pools" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for pool in d.get('results', []):
    name = pool.get('display_name','?')
    pid  = pool.get('id','')
    print(f'Pool: {name}  (id={pid})')
" 2>/dev/null

# For each pool ID, check allocations
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/pools/ip-pools/<pool-id>" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for s in d.get('subnets', []):
    t = s.get('total_ips',0); f = s.get('free_ips',0)
    pct = round((t-f)/t*100,1) if t else 0
    print(f'  {s.get(\"cidr\",\"?\")}  total={t}  free={f}  used={pct}%')
"
```

---

## Change Readiness Checklist

Complete before any NSX configuration change, DFW policy modification, upgrade, or maintenance:

### Cluster Health

- [ ] NSX Manager cluster status: STABLE (`get cluster status`)
- [ ] All Manager nodes connected (`get managers` — all CONNECTED)
- [ ] No CRITICAL alarms open (`GET /api/v1/alarms?status=OPEN&severity=CRITICAL` — result_count = 0)

### Transport and Overlay Health

- [ ] All transport nodes UP (`GET /api/v1/transport-nodes/status` — down_count = 0)
- [ ] All Geneve tunnels UP (`get tunnel status` — no DOWN tunnels)
- [ ] Edge cluster healthy — all Edge nodes UP and reachable

### Routing Health

- [ ] All BGP sessions Established (verify from each Edge node)
- [ ] Routing table intact (`vrf <id>` → `get route` — expected prefixes present)

### Backup and Rollback

- [ ] NSX Manager backup current and verified on SFTP (< 24 hours old)
- [ ] Rollback plan documented for the specific change
- [ ] Change window approved and communicated to networking and compute teams

### Post-Change Validation

After every NSX configuration change:

```bash
# 1. Check for new alarms
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/alarms?status=OPEN&severity=CRITICAL"

# 2. Verify transport nodes still UP
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/transport-nodes/status"

# 3. Verify BGP still up (if routing was changed)
# SSH to Edge, run: get bgp neighbor summary

# 4. Test VM connectivity if DFW was changed
# Use Traceflow: Plan & Troubleshoot → Traceflow

# 5. Check realisation of the specific change
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/policy/api/v1/infra/realized-state/realized-entities?intent_path=<changed-object-path>"
```
