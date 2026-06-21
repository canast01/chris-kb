---
tags:
  - nsx
  - nsx-4
  - operations
  - vmware
---
# NSX — Health Checks

<div class="kb-summary">
Health checks for NSX — Manager cluster status, transport node health, Edge BGP sessions, DFW policy state, certificate expiry, alarm review, backup age, and post-change verification.

*Applies to: NSX-T 3.x / NSX 4.x*
</div>



## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

Paste these commands in sequence from a host with API access to the NSX Manager. Replace `<nsx-manager>` and `admin:password` with your environment values.

```bash
# 1. NSX Manager cluster status — must show overall_status: STABLE
curl -sk -u 'admin:password' "https://<nsx-manager>/api/v1/cluster/status" \
  | python3 -m json.tool | grep -E '"status"|"state"|"overall"'
```

```bash
# 2. Edge cluster member health — check individual member status
curl -sk -u 'admin:password' "https://<nsx-manager>/api/v1/edge-clusters" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
for ec in d.get('results', []):
    print(f'Edge cluster: {ec[\"display_name\"]}')
    for m in ec.get('members', []):
        print(f'  member={m.get(\"transport_node_id\",\"?\")}  available={m.get(\"member_status\",{}).get(\"status\",\"?\")}')
"
```

```bash
# 3. Transport node health — all nodes should show status: SUCCESS
curl -sk -u 'admin:password' "https://<nsx-manager>/api/v1/transport-nodes/status" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
for n in d.get('results', []):
    status = n.get('node_deployment_state', {}).get('state', '?')
    print(f'  {n.get(\"display_name\",\"?\"): <40}  state={status}')
"
```

```bash
# 4. BGP neighbor summary — run on each Edge VM via nsxcli
# SSH to Edge VM, then:
nsxcli
vrf <tier0-vrf-id>
get bgp neighbor summary
# All peers must show state=Established; any non-Established peer is an incident
```

```bash
# 5. DFW security policy list — confirm policies are published and not in ERROR state
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/policy/api/v1/infra/domains/default/security-policies" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
for p in d.get('results', []):
    print(f'  {p.get(\"display_name\",\"?\"):<40}  sequence={p.get(\"sequence_number\",\"?\")}  category={p.get(\"category\",\"?\")}')
"
```

```bash
# 6. Controller/cluster node connectivity — all nodes should be reachable
curl -sk -u 'admin:password' "https://<nsx-manager>/api/v1/cluster/nodes" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
for n in d.get('results', []):
    addr = n.get('controller_role', {}).get('api_listen_addr', {}).get('ip_address', '?')
    status = n.get('controller_role', {}).get('connectivity_status', '?')
    print(f'  node={addr}  connectivity={status}')
"
```

```bash
# 7. Certificate expiry — flag anything expiring within 60 days
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/trust-management/certificates?details=true" \
  | python3 -c "
import sys, json
from datetime import datetime, timezone
d = json.load(sys.stdin)
now = datetime.now(timezone.utc)
for c in d.get('results', []):
    name = c.get('display_name', c.get('id', '?'))
    exp  = c.get('not_after', '')
    if exp:
        exp_dt = datetime.fromisoformat(exp.replace('Z', '+00:00'))
        days   = (exp_dt - now).days
        flag   = 'OK' if days > 60 else '*** EXPIRING SOON' if days > 14 else '*** CRITICAL'
        print(f'  {name:<40}  expires={exp[:10]}  days_left={days}  {flag}')
"
```

```bash
# 8. Open alarms — critical severity only; any output here needs immediate attention
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/alarms?status=OPEN&severity=CRITICAL" \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
cnt = d.get('result_count', 0)
print(f'CRITICAL alarms open: {cnt}')
for a in d.get('results', []):
    print(f'  {a.get(\"alarm_source\",{}).get(\"display_name\",\"?\")}: {a.get(\"summary\",\"\")[:80]}')
"
```

```bash
# 9. Manager backup history — last backup must be within 24 hours
curl -sk -u 'admin:password' "https://<nsx-manager>/api/v1/cluster/backups/history" \
  | python3 -c "
import sys, json
from datetime import datetime, timezone
d = json.load(sys.stdin)
backups = d.get('results', [])
if not backups:
    print('WARNING: no backup records found')
else:
    last = backups[0]
    ts = last.get('end_time', 0) / 1000
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    age_h = (datetime.now(timezone.utc) - dt).total_seconds() / 3600
    status = last.get('success', False)
    print(f'  Last backup: {dt.strftime(\"%Y-%m-%d %H:%M UTC\")}  age={age_h:.1f}h  success={status}')
    if age_h > 24:
        print('  WARNING: last backup is older than 24 hours')
"
```

```bash
# SSH to each Edge node
vrf <tier0-vrf-id>
get bgp neighbor summary

# Expected output shows each peer with state=Established
# Any peer not Established = BGP issue; see Common Issues

# Specific peer detail
get bgp neighbor <peer-ip>
```

## NSX Manager CLI Quick Reference

![NSX Manager CLI Quick Reference](../../../../assets/virtualization-vmware-nsx-hc-nsx-manager-cli-quick-reference.svg)

```bash
# SSH to any NSX Manager node
nsxcli

# Cluster status (must show STABLE)
get cluster status

# Individual node reachability (all should show CONNECTED)
get managers

# Corfu (Raft DB) — control plane health
get corfu-cluster status

# All services running (output should be empty — grep removes "running" lines)
get services | grep -v " running"
```

## Alarm Review

![Alarm Review](../../../../assets/virtualization-vmware-nsx-hc-alarm-review.svg)

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
## Certificate Expiry Check

![Certificate Expiry Check](../../../../assets/virtualization-vmware-nsx-hc-certificate-expiry-check.svg)

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

## IP Pool Utilisation

![IP Pool Utilisation](../../../../assets/virtualization-vmware-nsx-hc-ip-pool-utilisation.svg)

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
## Post-Change Verification

![Post-Change Verification](../../../../assets/virtualization-vmware-nsx-hc-post-change-verification.svg)

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

---

## See also

- [NSX — Common Issues](../troubleshooting/common-issues/)
- [NSX — Standard Procedures](procedures/)
- [NSX — CLI Reference](cli-reference/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
