# Aria Operations — Health Checks

```text
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
┌──────────────────────────────────── Aria Operations Health Checks ────────────────────────────────────┐
│                                                                                                       │
│  Node status, adapter health, and collection status checks for Aria Operations (vROps).               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Cluster Node Health              │  │                Adapter Health               │   │
│   │         Admin > Cluster: all green?          │  │           Data Sources: all green?          │   │
│   │            Master: ONLINE status             │  │          Last collection < 10 min?          │   │
│   │         Data nodes: ONLINE + joined          │  │           Adapter logs: no errors?          │   │
│   │         Collector: COLLECTING status         │  │          Object count as expected?          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Node and adapter health are primary checks; collection status confirms data flow.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Collection Status Checks           │  │           Platform Resource Checks          │   │
│   │           Alerts firing normally?            │  │           Disk: /storage/db < 80%?          │   │
│   │           Dashboards loading data?           │  │           RAM usage within sizing?          │   │
│   │          Capacity data up to date?           │  │                NTP: in sync?                │   │
│   │            Reports generating OK?            │  │              Cert: not expired?             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps cluster on vSphere; SSD-backed datastore; NTP server; SMTP for alert delivery                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cluster Status      = vROps Admin UI showing all node roles and health states                        │
│  ONLINE Status       = Node is fully joined, serving requests, and collecting data                    │
│  COLLECTING Status   = Remote collector actively sending metrics to master cluster                    │
│  Adapter Green       = Data source collecting without errors in last 10 minutes                       │
│  Last Collection     = Timestamp of most recent successful adapter data pull                          │
│  Object Count        = Expected number of monitored resources; drop = issue                           │
│  /storage/db         = vROps metric database path; monitor disk consumption                           │
│  Alert Firing        = Verify known issue triggers alert; confirms policy active                      │
│  Dashboard Data      = Widgets show current metrics; blank = collection problem                       │
│  Capacity Freshness  = Capacity model updates every cycle; stale = issue                              │
│  NTP Sync            = Required for accurate metric timestamps and alert timing                       │
│  Cert Expiry         = vROps UI cert; expired cert blocks browser and API access                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

---

## Cluster Node Health via API

```bash
# Authenticate
TOKEN=$(curl -sk -X POST \
  "https://vrops-prod-01.example.local/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<password>","authSource":"Local"}' | \
  jq -r '.token')

# List all cluster nodes and their status
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/cluster/nodes" | \
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
  "https://vrops-prod-01.example.local/suite-api/api/adapters/<adapter-id>/monitoringstatedescriptor" \
  -H "Content-Type: application/json" \
  -d '{"collectorId": "<collector-id>", "resourceKindKey": "ADAPTER", "adapterKindKey": "VMWARE"}'
```

---

## Disk and Storage Health

```bash
ssh admin@vrops-prod-01.example.local

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
  echo -n "$node.example.local: "
  ssh admin@"$node.example.local" "chronyc tracking 2>/dev/null | grep 'System time'"
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
  "https://vrops-prod-01.example.local/suite-api/api/alerts?activeOnly=true" | \
  jq '[.alerts[] | .criticality] | group_by(.) | map({criticality: .[0], count: length})'

# Get all CRITICAL alerts with their object and alert name
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/alerts?activeOnly=true&criticality=CRITICAL" | \
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
  "https://vrops-prod-01.example.local/suite-api/api/resources?resourceKind=ClusterComputeResource" | \
  jq '.resourceList[] | {name: .resourceKey.name}'
```

Via UI: **Optimize → Capacity Overview** — review which clusters or datastores are approaching capacity limits. Investigate any resource that shows a time remaining of less than 60 days.

### Report Review

- Run the **Rightsizing** report: **Optimize → Reclaim → Oversized VMs** — review and action top candidates
- Run the **Idle VMs** report: **Optimize → Reclaim → Idle VMs** — validate with VM owners before powering off

### Alert Policy Review

Review alert policies monthly and tune noisy alert definitions:

```text
Administration → Alert Settings → Alert Definitions
```

- Sort by **Alert Count (Last 30 Days)** — investigate any alert firing more than 10 times per day with no action being taken
- Add symptom wait cycles to reduce transient alerts (minimum 3 cycles before firing is recommended for non-critical alerts)
- Suppress known-benign alerts using **Maintenance Schedules** rather than cancelling them manually
