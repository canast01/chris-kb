# Aria Operations — Common Issues


<div class="kb-summary">
Common Issues reference covering Adapter Collection Failures, Cluster Node Offline or Degraded, Dashboard Shows Stale or No Data, Capacity Data Not Updating, LDAP Authentication Failure and 2 more sections.
</div>

## Adapter Collection Failures

Symptoms: adapter shows **Not Collecting** in Administration → Solutions; metric data for the monitored system stops updating; dashboards show stale data.

```bash
# SSH to primary node and inspect adapter state
ssh admin@vrops-prod-01.example.local
vracli adapter list --verbose

# Check the collector log for adapter-specific errors
tail -500 /data/vcops/log/collector.log | grep -i "error\|exception\|fail"

# Check per-adapter log
ls /data/vcops/log/adapters/
tail -200 /data/vcops/log/adapters/VMwareAdapter/adapter.log | grep -i "error\|auth\|connect"

# Restart the watchdog (restarts failed services automatically)
service vmware-vcops-watchdog restart
```
```
┌──────────────────────────────────── Aria Operations Common Issues ────────────────────────────────────┐
│                                                                                                       │
│  Common issues: adapter disconnected, no data in dashboards, and alert storms.                        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Adapter Disconnected             │  │            No Data in Dashboards            │   │
│   │          Check adapter credentials           │  │          Check adapter green status         │   │
│   │          Verify source reachability          │  │          Check collection interval          │   │
│   │           Service account locked?            │  │          Widget: correct resource?          │   │
│   │          Re-test adapter connection          │  │           Time range: too narrow?           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Adapter and data issues are most frequent; alert storms require policy tuning.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Alert Storm                  │  │         Node Offline / Cluster Issue        │   │
│   │            Identify noisy symptom            │  │          Check VAMI cluster status          │   │
│   │            Raise alert threshold             │  │         Verify node VM is powered on        │   │
│   │           Use wait cycles setting            │  │           Check inter-node network          │   │
│   │         Suppress during maintenance          │  │           Restart vmware-vcops svc          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vROps cluster on vSphere; AD/LDAP for adapter auth; management network for nodes                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Adapter Disconnected = Data source not collecting; shown as red/yellow in UI                         │
│  Service Acct Lock    = AD lockout from repeated failed vROps authentication                          │
│  No Dashboard Data    = Widget blank; adapter issue or wrong resource scope                           │
│  Alert Storm          = Excessive alert volume; caused by over-sensitive thresholds                   │
│  Wait Cycles          = Alert setting requiring symptom to persist N cycles to fire                   │
│  Symptom Suppression  = Temporarily disable alert during planned maintenance                          │
│  Node Offline         = Cluster node unreachable; check VM power and network                          │
│  vmware-vcops         = Main vROps service; restart if node appears stuck                             │
│  Cluster Status       = VAMI Admin page showing all node roles and health states                      │
│  Collection Interval  = Default 5 min; gap > 10 min indicates collection failure                      │
│  Re-test Connection   = vROps built-in adapter test; run after credential update                      │
│  Time Range           = Dashboard widget setting; widen if no data appears                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

If the node is running but not joining the cluster:
1. Check NTP — time drift > 1 second between nodes prevents cluster consensus
2. Check ports 9543, 10010 between nodes (firewall rules between cluster nodes)
3. Restart the watchdog service on the degraded node: `service vmware-vcops-watchdog restart`
4. If the node still does not join, check the analytics log for cluster election errors

---

## Dashboard Shows Stale or No Data

Symptoms: a dashboard widget shows "No data" or data is many hours old despite the adapter showing Collecting.

```bash
# Check analytics processing — if analytics queue is backed up, processing is delayed
tail -200 /data/vcops/log/analytics.log | grep -i "queue\|backlog\|warn\|error"

# Check GemFire (real-time cache) health
tail -100 /data/vcops/log/gemfire/vcopssuite_gemfire.log | grep -i "warn\|error"

# Confirm the adapter is actually collecting (not just in a Collecting state with zero data)
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/adapterkinds/VMWARE/resourcekinds/VirtualMachine/resources?pageSize=5" | \
  jq '.resourceList[] | {name: .resourceKey.name, lastCollected: .identifier}'
```

If a dashboard widget shows "No data" for a specific metric on a specific object:
- Verify the object is not in a maintenance schedule (alerts and metrics may be suppressed)
- Check that the metric is available for the object type: **Environment → Object Browser → select object → Metrics tab**
- Check if the metric collection interval was recently changed in the policy assigned to this object

---

## Capacity Data Not Updating

Symptoms: the capacity dashboard shows old projections; rightsizing recommendations have not refreshed.

Capacity analytics runs as a background job. By default it recalculates every 5 minutes for real-time data and once per day for long-term projections.

```bash
# Force a capacity recalculation
curl -sk -X POST -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/analytics/run" \
  -H "Content-Type: application/json" \
  -d '{"analyticsJobName": "CapacityAnalytics"}'

# Check analytics job status
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/analytics" | \
  jq '.[] | select(.name == "CapacityAnalytics") | {status: .status, lastRun: .lastRunTime}'
```

---

## LDAP Authentication Failure

Symptoms: AD users cannot log in; the login page returns "authentication failed" even with correct credentials.

```bash
# Test LDAP connectivity from the Aria Operations appliance
ssh admin@vrops-prod-01.example.local
vracli auth test --source <ldap-source-name>

# Manually test LDAP bind
ldapsearch -H ldaps://dc01.example.local:636 \
  -D "CN=svc-vrops-ldap,OU=Service Accounts,DC=corp,DC=local" \
  -w '<password>' \
  -b "DC=corp,DC=local" \
  "(sAMAccountName=testuser)" sAMAccountName | head -10
```

Common causes:
- Bind account password expired — reset in AD and update in Administration → Authentication Sources
- Domain CA certificate expired — re-import the root CA into Administration → Certificates
- Domain controller FQDN changed or unreachable — update the LDAP source with the new DC address
- Group sync not run — force a sync: Administration → Authentication Sources → select source → Sync

---

## Alert Notification Not Delivered

Symptoms: an alert fires in Aria Operations but no email or webhook notification is received.

```bash
# Verify SMTP configuration
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/notifications" | \
  jq '.notificationList[] | {name: .name, plugin: .pluginTypeId, enabled: .active}'

# Send a test notification via API
curl -sk -X POST -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://vrops-prod-01.example.local/suite-api/api/notifications/<notification-id>/actions/test"

# Check outbound SMTP from the appliance
ssh admin@vrops-prod-01.example.local
curl -v smtp://smtp.example.local:25 --mail-from aria-ops@corp.local \
  --mail-rcpt test@corp.local 2>&1 | head -30
```

| Issue | Check |
|---|---|
| SMTP not configured | Administration → Outbound Settings — confirm SMTP plugin exists |
| Notification rule disabled | Alerts → Notifications → check Active column |
| Alert criticality filter mismatch | Notification rule only fires for specific criticalities — verify the alert matches |
| Alert cancelled before notification fired | If alert resolved within one collection cycle, notification may not fire |

---

## UI Performance Degraded (Slow Loading)

Symptoms: the Aria Operations web UI is slow to load; dashboard queries time out.

```bash
# Check CPU and memory pressure on the primary node
ssh admin@vrops-prod-01.example.local
top -bn1 | head -20

# Check GemFire heap usage (in-memory cache)
tail -20 /data/vcops/log/gemfire/vcopssuite_gemfire.log | grep -i "heap\|memory"

# Check Cassandra compaction — heavy compaction causes query slowness
ssh admin@vrops-prod-01.example.local
nodetool compactionstats

# Check for very large queries — long-running queries appear in the analytics log
tail -200 /data/vcops/log/analytics.log | grep -i "slow\|timeout\|duration"
```

If performance is consistently poor:
- Consider adding a data node to distribute metric storage: **Administration → Cluster Management → Add Node**
- Reduce the number of metrics collected per object via policy tuning — disable metrics that are not used in dashboards or alerts
- Archive old metric data if the Cassandra data directory is >70% full
