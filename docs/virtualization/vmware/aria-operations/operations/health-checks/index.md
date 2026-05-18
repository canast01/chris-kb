# Aria Operations — Health Checks

```
Aria Operations — Health Check Coverage Map
┌─────────────────────────────────────────────────────┐
│  Cluster Node Health                                │
│  Admin → Cluster Management                         │
│  vracli cluster health                              │
│  Expected: all nodes ONLINE                         │
│  Watch: OFFLINE · DEGRADED · SYNCING                │
└──────────────────────┬──────────────────────────────┘
                       │
          ┌────────────┼────────────────────┐
          ▼            ▼                    ▼
┌──────────────┐ ┌──────────────┐ ┌─────────────────┐
│ Adapter      │ │ Disk         │ │ Service           │
│ Health       │ │ Health       │ │ Health            │
│              │ │              │ │                   │
│ Admin        │ │ /storage/db  │ │ systemctl         │
│ → Solutions  │ │ warn: 70%    │ │ list-units        │
│              │ │ crit: 80%    │ │ 'vmware-*'        │
│ vracli       │ │              │ │                   │
│ adapter list │ │ /storage/log │ │ analytics         │
│              │ │ warn: 75%    │ │ cassandra         │
│ Expected:    │ │ crit: 85%    │ │ gemfire           │
│ Collecting   │ │              │ │ casa / nginx      │
│ < 5 min ago  │ │ check inodes │ │ watchdog          │
└──────────────┘ └──────────────┘ └─────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────┐
│  NTP Health (all nodes must be < 1 second drift)    │
│  chronyc tracking (per node)                        │
│  chronyc makestep (force sync if drifted)           │
└─────────────────────────────────────────────────────┘
```

## Daily Checks

| Check | Location | Expected State |
|-------|----------|----------------|
| Cluster node status | Administration > Cluster Management | All nodes Online |
| Adapter health | Administration > Solutions | All adapters Collecting |
| Active critical alerts | Alerts > All Alerts | Review and acknowledge known issues |
| Capacity headroom | Optimize > Capacity | No red capacity warnings |
| Self-monitoring alerts | Environment > vRealize Operations Health | No critical self-alerts |

## Cluster Health Commands

```bash
ssh admin@<aria-ops-primary-fqdn>

# Overall cluster health summary
vracli cluster health

# Per-service status on this node
vracli status

# List all adapter instances and their collection state
vracli adapter list
```

---

## Cluster Node Health via API

```bash
# Authenticate
TOKEN=$(curl -sk -X POST \
  "https://vrops-prod-01.corp.local/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>","authSource":"Local"}' | \
  jq -r '.token')

# List all cluster nodes and their status
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.corp.local/suite-api/api/cluster/nodes" | \
  jq '.nodes[] | {name: .name, role: .role, status: .nodeStatus}'

# Expected: all nodes show nodeStatus = "ONLINE"
# OFFLINE, DEGRADED, or SYNCING nodes require investigation before any upgrade
```

---

## Adapter Health

1. Navigate to **Administration > Solutions > Cloud Accounts** (or **Adapters**)
2. Confirm each adapter shows **Collection State: Collecting**
3. Last collection time should be within 5 minutes

```bash
# List adapters with verbose collection state
vracli adapter list --verbose

# Check the collector service log for adapter errors
tail -200 /data/vcops/log/collector.log | grep -i "error\|exception\|fail"

# Restart an adapter that is stuck in "Not Collecting"
# UI: Administration → Solutions → select adapter → Restart Instance
# Or via API:
curl -sk -X POST -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.corp.local/suite-api/api/adapters/<adapter-id>/monitoringstatedescriptor" \
  -H "Content-Type: application/json" \
  -d '{"collectorId": "<collector-id>", "resourceKindKey": "ADAPTER", "adapterKindKey": "VMWARE"}'
```

---

## Disk and Storage Health

```bash
ssh admin@vrops-prod-01.corp.local

# Check disk usage on primary node
df -h /storage/db /storage/log /storage/core

# Check Cassandra data directory sizes (main metrics store)
du -sh /storage/db/cassandra/data/*

# Check available inodes — can cause "disk full" errors even with space remaining
df -i /storage/db
```

Thresholds:

| Mount Point | Warning | Critical | Action |
|---|---|---|---|
| `/storage/db` | 70% | 80% | Expand data disk or remove old metric data |
| `/storage/log` | 75% | 85% | Archive or rotate logs |
| `/storage/core` | 75% | 85% | Contact support — core partition should not grow |

---

## Service Health Commands

```bash
# Check all vmware services on the primary node
systemctl list-units 'vmware-*' --state=active

# Check a specific service that appears failed
systemctl status vmware-vcops-analytics
journalctl -u vmware-vcops-analytics --since "1 hour ago" | tail -100

# Key services and expected states
# vmware-vcops-analytics   — active (running)
# vmware-vcops-cassandra   — active (running)
# vmware-vcops-postgres    — active (running)
# vmware-vcops-gemfire     — active (running)
# vmware-casa              — active (running)
# nginx                    — active (running)
# vmware-vcops-watchdog    — active (running)
```

---

## NTP and Time Sync

Time drift causes SSO token validation failures and certificate errors across all Aria Suite products. All cluster nodes must be synchronised.

```bash
# Check NTP sync on each cluster node
for node in vrops-prod-01 vrops-prod-02 vrops-prod-03; do
  echo -n "$node.corp.local: "
  ssh admin@"$node.corp.local" "chronyc tracking 2>/dev/null | grep 'System time'"
done

# Force sync if drift is detected
chronyc makestep

# Verify NTP sources
chronyc sources -v
```

Acceptable drift: < 1 second within the cluster. LCM pre-checks fail if drift exceeds 5 seconds on the LCM appliance.

---

## Alert Summary Health Check

Regularly review the alert landscape to identify noise and catch real problems:

```bash
# Get all active alerts grouped by criticality via API
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.corp.local/suite-api/api/alerts?activeOnly=true" | \
  jq '[.alerts[] | .criticality] | group_by(.) | map({criticality: .[0], count: length})'

# Get all CRITICAL alerts with their object and alert name
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.corp.local/suite-api/api/alerts?activeOnly=true&criticality=CRITICAL" | \
  jq '.alerts[] | {alert: .type.name, object: .resourceName, since: .startTimeUTC}'
```

---

## Pre-Upgrade Health Gate

Run before any upgrade (via LCM or in-product):

- [ ] All cluster nodes show **Online** in Administration → Cluster Management
- [ ] All adapter instances show **Collecting** — no adapters in error or offline state
- [ ] No active critical self-monitoring alerts: **Environment → vRealize Operations Health**
- [ ] Disk usage on `/storage/db` < 70%
- [ ] NTP delta < 1 second on all nodes: `chronyc tracking`
- [ ] Backup completed successfully within last 24 hours
- [ ] VM snapshots taken for all Aria Operations nodes
- [ ] No running LCM requests that involve this product
- [ ] Maintenance window communicated to users who rely on alerts from Aria Operations

---

## Weekly Checks

### Capacity Review

```bash
# Check cluster-level capacity summary via API
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.corp.local/suite-api/api/resources?resourceKind=ClusterComputeResource" | \
  jq '.resourceList[] | {name: .resourceKey.name}'
```

Via UI: **Optimize → Capacity Overview** — review which clusters or datastores are approaching capacity limits. Investigate any resource that shows a time remaining of less than 60 days.

### Report Review

- Run the **Rightsizing** report: **Optimize → Reclaim → Oversized VMs** — review and action top candidates
- Run the **Idle VMs** report: **Optimize → Reclaim → Idle VMs** — validate with VM owners before powering off

### Alert Policy Review

Review alert policies monthly and tune noisy alert definitions:

```
Administration → Alert Settings → Alert Definitions
```

- Sort by **Alert Count (Last 30 Days)** — investigate any alert firing more than 10 times per day with no action being taken
- Add symptom wait cycles to reduce transient alerts (minimum 3 cycles before firing is recommended for non-critical alerts)
- Suppress known-benign alerts using **Maintenance Schedules** rather than cancelling them manually
