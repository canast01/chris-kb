# RecoverPoint — Health Checks

> Part of the [RecoverPoint](../) reference.

---

## Overview

RecoverPoint health checks cover four areas: RPA cluster node health, consistency group (CG) replication state, journal utilization, and inter-site link status. Run these checks daily as a minimum, and before/after any change window.

| Area | Tool | Frequency |
|---|---|---|
| RPA cluster nodes | SSH `system status` | Daily |
| CG replication state | SSH `groups status` | Daily |
| Journal utilization | SSH `journals list` | Daily |
| Link statistics | SSH `links statistics` | Pre/post change |
| RPO compliance | REST API or RPMA | Daily (automated) |

---

## Daily Health Check Commands

```bash
# SSH to RPA cluster management IP
ssh admin@<rpa-cluster-ip>

# RPA cluster and node health
system status

# All CGs — expect ACTIVE for all production CGs
groups status

# Detailed CG view including lag, RPO, and journal fill
groups status detail

# Journal utilization for all CGs
journals list

# Active alarms (hardware and software)
alarms list

# Inter-site link statistics (latency, bandwidth)
links statistics

# Cluster quorum state
cluster quorum check
```

---

## REST API Health Checks

```bash
RP="https://<rpa-mgmt-ip>/fapi/rest/5_1"
AUTH="-u admin:password --insecure"

# Cluster health summary
curl -s $AUTH "$RP/cluster/all_clusters_details" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for c in data.get('clustersDetails', []):
    print(f\"Cluster: {c.get('name','?')}  Quorum: {c.get('quorum','?')}\")
"

# All CGs — state and lag
curl -s $AUTH "$RP/group/all_groups_details" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for g in data.get('innerSet', []):
    print(f\"CG={g.get('name','?'):30s}  enabled={g.get('enabled','?')}\")
"

# RPA node states
curl -s $AUTH "$RP/rp/all_rps_details" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for r in data.get('innerSet', []):
    print(f\"RPA {r.get('rpUID',{}).get('id','?')}  state={r.get('rpState','?')}\")
"
```

---

## RPO Compliance Check

```bash
# Check per-CG RPO against current lag (SSH)
group status --gname <cg_name>

# Expected output fields:
#   Replication state:  ACTIVE
#   Current lag:        3s
#   Configured RPO:     300s
#   Compliant:          YES
```

| RPO Tier | Target | Alert Threshold |
|---|---|---|
| Tier 1 (Critical) | < 15 seconds | > 60 seconds |
| Tier 2 (Business) | < 5 minutes | > 15 minutes |
| Tier 3 (Standard) | < 30 minutes | > 60 minutes |

---

## Journal Utilization Check

Journal overflow causes CG replication to halt. Alert thresholds:

```bash
# List journal volumes with utilization
journals list

# Expected output columns:
#   Journal Name   CG Name         Used%   Free%   Status
#   JRN-CG-ORA-DR  CG-ORACLE-PROD  34%     66%     OK
```

| Utilization | Status | Action |
|---|---|---|
| 0–69% | OK | No action |
| 70–79% | Warning | Monitor; investigate write rate spike |
| 80–89% | Critical | Plan journal expansion; check link state |
| 90%+ | Emergency | Immediate action — expand or CG will halt |

---

## Weekly and Monthly Checks

```bash
# Confirm splitter health (for RP4VM software splitters on ESXi)
esxcli software vib list | grep -i rp

# Confirm RPA software versions are consistent across cluster
boxmgmt verify_rpa_version

# Review audit log for unexpected operations (logins, image access events)
get_audit_log -last 500

# Confirm DR site RPA cluster is also healthy
ssh admin@<dr-rpa-cluster-ip> "system status"
ssh admin@<dr-rpa-cluster-ip> "groups status"
```
