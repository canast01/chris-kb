# Aria Ops for Logs — Common Issues

```text
┌─────────────────────────────────────────────────────────────┐
│         Aria Ops for Logs Issue Triage Flow                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Ingestion 0 events/sec?                                    │
│  └──► ss -tulnp | grep 514/1514/9543  (ports listening?)    │
│       df -h /var/log/loginsight  (disk full = stop ingest)  │
│       grep drop ingestion.log                               │
│                                                             │
│  Agent stale / not delivering?                              │
│  └──► systemctl status liagentd                             │
│       nc -zv vrli-prod-01:9543  (TCP reachable?)            │
│       liagent.log → ssl/connect errors                      │
│                                                             │
│  Queries slow / timing out?                                 │
│  └──► nodetool compactionstats (Cassandra compacting?)      │
│       nodetool info | grep heap  (>90% = slow)              │
│                                                             │
│  Cluster node not joining?                                  │
│  └──► DNS forward+reverse · NTP delta (<60s) · cert match   │
│                                                             │
│  Alerts not firing?                                         │
│  └──► alert enabled? threshold too high? SMTP reachable?    │
└─────────────────────────────────────────────────────────────┘
```

## Log Ingestion Stopped or Dropped to Zero

Symptoms: the ingestion rate in Administration → Cluster shows 0 events/sec; dashboards show no recent events; log sources are still active.

```bash
# Check ingestion stats from master node
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/stats" | \
  jq '{eventsPerSecond: .eventsIngested, diskPct: .diskUsagePercent}'

# Verify syslog listeners are running
ss -tulnp | grep -E "514|1514|9543"
# Expected: UDP 514, TCP 1514, TCP 9543 all listening
# If any port is not listening: restart the loginsight service
systemctl restart loginsight

# Test syslog reception from a source
logger -n vrli-prod-01.example.local -P 514 -d "test ingestion check"
# Then check Interactive Analytics for "test ingestion check" within 30 seconds

# Check ingestion log for parse failures or drops
grep -i "drop\|overflow\|parse error\|reject" /var/log/loginsight/ingestion.log | tail -50
```

| Cause | Symptom | Resolution |
|---|---|---|
| Disk > 90% full | Cluster stops accepting events; no syslog listener response | Free disk space or add a worker node |
| All cluster nodes offline | Syslog sources connect but events not indexed | Restore from snapshot; restart loginsight service |
| Ingestion filter too broad | Events matching the filter are silently dropped | Review Administration → Ingestion Filters |
| Network firewall blocking ports | Sources sending but nothing arriving | Check firewall rules for UDP 514, TCP 1514, TCP 9543 |

---

## Searching ESXi Host Logs

Search for a specific host by name or IP and filter by log source appname:

| `appname` value | Log Source | Common Searches |
|---|---|---|
| `hostd` | VM and host operation daemon | `hostd AND (error OR failed)` |
| `vpxa` | vCenter agent on the host | `vpxa AND disconnect` |
| `vmkernel` | Kernel-level events | `vmkernel AND (SCSI OR NFS OR warning)` |
| `vobd` | Hardware and storage observer | `vobd AND (APD OR PDL OR disk)` |
| `vmkwarning` | Kernel warning messages | `vmkwarning` |

Quick searches for common ESXi problems:

```bash
# Host connectivity lost
text contains "lost connectivity" AND appname = "vpxa"

# SCSI or storage errors
(appname = "vmkernel" OR appname = "vobd") AND (text contains "SCSI" OR text contains "APD" OR text contains "PDL")

# vMotion failures
text contains "VMotionFailed" OR (text contains "vmotion" AND text contains "error")

# HA failover events
text contains "ha.vm.restart" OR text contains "HA failover"

# Certificate or SSO errors
text contains "certificate" AND text contains "invalid"
text contains "STS" AND text contains "error"
```

---

## Searching vCenter Events

Use the vCenter log source and filter by event type or keyword:

| Use Case | Search Pattern |
|---|---|
| Login events | `appname = "vpxd" AND text contains "SessionManager"` |
| Task failures | `appname = "vpxd" AND text contains "TaskManager" AND text contains "error"` |
| Certificate events | `appname = "vpxd" AND text contains "STS"` |
| Permission changes | `appname = "vpxd" AND text contains "Permission"` |
| Snapshot operations | `appname = "vpxd" AND text contains "snapshot"` |
| VM power operations | `appname = "vpxd" AND (text contains "PowerOn" OR text contains "PowerOff")` |

---

## Agent Not Delivering Logs

Symptoms: agent shows as stale or offline in Administration → Agents; logs from that host are absent.

```bash
# Check agent service status on the source host (Linux)
systemctl status liagentd
journalctl -u liagentd --since "1 hour ago" | tail -50

# Check agent log for connection errors
tail -100 /var/log/vmware/loginsight-agent/liagent.log | grep -i "error\|ssl\|connect\|timeout"

# Test TCP connectivity from agent to Aria Ops for Logs
nc -zv vrli-prod-01.example.local 9543
# Expected: Connection to vrli-prod-01.example.local 9543 succeeded

# Verify agent configuration is correct
grep -v "^#\|^$" /var/lib/loginsight-agent/liagent.ini
# Check hostname, port (9543), and ssl setting

# Restart the agent
systemctl restart liagentd
systemctl status liagentd
```

For Windows agents:

```powershell
# Check agent service status
Get-Service "VMware Log Insight Agent"

# View agent event log
Get-EventLog -LogName Application -Source "VMware*" -Newest 50 | Format-List

# Restart agent
Restart-Service "VMware Log Insight Agent"
```

---

## Interactive Analytics Queries Time Out or Are Slow

Symptoms: queries over large time windows return a timeout error; dashboards are slow to load.

```bash
# Check Cassandra compaction — long compaction causes slow queries
ssh admin@vrli-prod-01.example.local
nodetool compactionstats

# Check Cassandra heap usage — high heap (>90%) causes query slowness
nodetool info | grep -i "heap"

# Check current query load
tail -50 /var/log/loginsight/query.log | grep -i "slow\|timeout\|error\|duration"

# Reduce query load by narrowing time ranges and adding field filters
# Use: last 1 hour instead of last 7 days when investigating active incidents
```

Best practices for fast queries:
- Always set a specific time range — avoid querying "All Time"
- Filter on indexed fields (`hostname`, `appname`, `source`) before free-text search
- Use **text contains** rather than **text matches** (regex) where possible — regex is slower
- For very large clusters, add worker nodes to distribute Cassandra read load

---

## Cluster Node Not Joining (Worker Fails to Join)

Symptoms: a new worker node is powered on and the setup wizard completed, but it does not appear in Administration → Cluster.

```bash
# Check the cluster nodes via API from the master
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/nodes" | \
  jq '.nodes[] | {host: .hostname, state: .state}'

# SSH to the worker node and check the loginsight service
ssh admin@vrli-prod-02.example.local
systemctl status loginsight
tail -100 /var/log/loginsight/runtime.log | grep -i "join\|cluster\|error\|master"

# Test connectivity from worker to master on required ports
nc -zv vrli-prod-01.example.local 443
nc -zv vrli-prod-01.example.local 16520  # cluster internal communication port
```

Common causes:
- **DNS mismatch**: the worker's FQDN resolves to a different IP than what the master sees — verify forward and reverse DNS for the worker FQDN
- **NTP drift**: if the worker's clock differs from the master by more than 60 seconds, the join will fail — `chronyc tracking` on both nodes and force sync: `chronyc makestep`
- **Certificate mismatch**: if the master has a CA-signed certificate but the worker has a self-signed certificate, the join TLS handshake may fail — replace the worker certificate first

---

## Alert Notifications Not Firing

Symptoms: an alert definition is enabled and the query matches events, but no notification is sent.

```bash
# Verify alert is enabled
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/alerts/<alert-id>" | \
  jq '{name: .name, enabled: .enabled, numHits: .numHits}'

# Test the notification channel
curl -sk -X POST -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/notification/<channel-id>/test"

# Check the runtime log for notification delivery errors
grep -i "notification\|email\|webhook\|smtp\|fail" /var/log/loginsight/runtime.log | tail -50
```

| Issue | Check |
|---|---|
| Alert threshold too high | Alert count threshold set to 100 events, but query only matches 10 — lower the threshold |
| Notification channel disabled | Administration → Notification Channels → check enabled state |
| Webhook URL changed | Test the webhook manually with `curl -X POST <webhook-url>` |
| SMTP relay unreachable | Test SMTP: `curl -v smtp://smtp.example.local:25` from appliance SSH |
| Alert recently disabled by operator | Check runtime.log for a recent disable event |

---

## NTP Diagnostics

Certificate operations and log timestamp alignment fail when NTP is not synchronised:

```bash
# Check NTP on the Aria Ops for Logs appliance
chronyc tracking
chronyc sources -v

# If NTP is drifting: restart chronyd and check sources
systemctl restart chronyd
chronyc sources

# Verify all cluster nodes are synced to the same NTP source
for node in vrli-prod-01 vrli-prod-02 vrli-prod-03; do
  echo -n "$node.example.local: "
  ssh admin@$node.example.local "chronyc tracking 2>/dev/null | grep 'System time'"
done
```

---

## Disk Full — Cluster Stops Ingesting

When a node's disk reaches 100%, Aria Ops for Logs stops accepting log events on that node. The cluster continues on remaining nodes until their disk also fills.

Immediate actions:

```bash
# Confirm disk usage
df -h /var/log/loginsight

# Check if hot retention is set too long for current disk size
# Reduce retention to free space: Administration → General → Retention → reduce days

# Remove old archives from the NFS target if archiving is enabled
# Do NOT manually delete files from /var/log/loginsight — Cassandra manages this path

# If retention cannot be reduced, add a worker node with additional disk
# Workers can be added without downtime: deploy OVA → setup wizard → Join Cluster
```

After freeing disk space, the cluster automatically resumes ingestion — no manual restart is required. Verify by checking the events/sec counter in Administration → Cluster.
