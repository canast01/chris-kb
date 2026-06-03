```text
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
```
```text
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
```
```text
```
```text
┌─────────────────────────────────────────────────────┐
│  NTP Health (all nodes must be < 1 second drift)                                                      │
│  chronyc tracking (per node)                                                                          │
│  chronyc makestep (force sync if drifted)                                                             │
└─────────────────────────────────────────────────────┘
```

```text
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
```
```bash
## List adapters with verbose collection state
vracli adapter list --verbose

## Check the collector service log for adapter errors
tail -200 /data/vcops/log/collector.log | grep -i "error\|exception\|fail"

## Restart an adapter that is stuck in "Not Collecting"
## UI: Administration → Solutions → select adapter → Restart Instance
## Or via API:
curl -sk -X POST -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/adapters/<adapter-id>/monitoringstatedescriptor" \
  -H "Content-Type: application/json" \
  -d '{"collectorId": "<collector-id>", "resourceKindKey": "ADAPTER", "adapterKindKey": "VMWARE"}'
```
```bash
ssh admin@vrops-prod-01.example.local

## Check disk usage on primary node
df -h /storage/db /storage/log /storage/core

## Check Cassandra data directory sizes (main metrics store)
du -sh /storage/db/cassandra/data/*

## Check available inodes — can cause "disk full" errors even with space remaining
df -i /storage/db
```
```bash
## Check all vmware services on the primary node
systemctl list-units 'vmware-*' --state=active

## Check a specific service that appears failed
systemctl status vmware-vcops-analytics
journalctl -u vmware-vcops-analytics --since "1 hour ago" | tail -100

## Key services and expected states
## vmware-vcops-analytics   — active (running)
## vmware-vcops-cassandra   — active (running)
## vmware-vcops-postgres    — active (running)
## vmware-vcops-gemfire     — active (running)
## vmware-casa              — active (running)
## nginx                    — active (running)
## vmware-vcops-watchdog    — active (running)
```
```bash
## Check NTP sync on each cluster node
for node in vrops-prod-01 vrops-prod-02 vrops-prod-03; do
  echo -n "$node.example.local: "
  ssh admin@"$node.example.local" "chronyc tracking 2>/dev/null | grep 'System time'"
done

## Force sync if drift is detected
chronyc makestep

## Verify NTP sources
chronyc sources -v
```
```bash
## Get all active alerts grouped by criticality via API
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/alerts?activeOnly=true" | \
  jq '[.alerts[] | .criticality] | group_by(.) | map({criticality: .[0], count: length})'

## Get all CRITICAL alerts with their object and alert name
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/alerts?activeOnly=true&criticality=CRITICAL" | \
  jq '.alerts[] | {alert: .type.name, object: .resourceName, since: .startTimeUTC}'
```
```bash
## Check cluster-level capacity summary via API
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/resources?resourceKind=ClusterComputeResource" | \
  jq '.resourceList[] | {name: .resourceKey.name}'
```
```text
Administration → Alert Settings → Alert Definitions
```
