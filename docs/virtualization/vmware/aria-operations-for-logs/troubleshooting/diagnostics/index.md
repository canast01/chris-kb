# Aria Ops for Logs — Diagnostics

```text
┌─────────────────────────────────────────────────────────────┐
│         Aria Ops for Logs Diagnostic Sources                │
├──────────────────────────────┬──────────────────────────────┤
│  Log Files (on appliance)    │  API Diagnostics             │
│  ─────────────────────────   │  ──────────────────────────  │
│  runtime.log  (main app)     │  GET /api/v2/cluster/nodes   │
│  ingestion.log (drops/parse) │  GET /api/v2/cluster/stats   │
│  query.log  (query perf)     │  POST /api/v2/support/bundle │
│  cassandra/system.log        │  GET /api/v2/agents          │
│  agent/agentd.log            │                              │
│  nginx/access.log            │  Cassandra (on-box)          │
│  /var/log/messages (OS)      │  nodetool compactionstats    │
│                              │  nodetool info (heap usage)  │
├──────────────────────────────┼──────────────────────────────┤
│  Cluster SSH Check           │  Support Bundle              │
│  ─────────────────────────   │  ──────────────────────────  │
│  systemctl status loginsight │  Via UI or API               │
│  systemctl status nginx      │  app logs · Cassandra logs   │
│  df -h /var/log/loginsight   │  system metrics · topology   │
│  ss -tulnp | grep 514/9543   │  (no passwords included)     │
└──────────────────────────────┴──────────────────────────────┘
```

## Log File Locations

| Log | Path | Purpose |
|---|---|---|
| Runtime / application | `/var/log/loginsight/runtime.log` | Main application events, cluster, and service status |
| Ingestion | `/var/log/loginsight/ingestion.log` | Log receiving, parsing, and indexing events |
| Query | `/var/log/loginsight/query.log` | Interactive analytics query execution |
| Cassandra | `/var/log/loginsight/cassandra/system.log` | Storage backend health and compaction |
| LI Agent (receiver) | `/var/log/loginsight/agent/agentd.log` | cfapi agent connections |
| Nginx | `/var/log/nginx/access.log` | HTTP requests to the UI and API |
| System | `/var/log/messages` | OS-level events, NFS, networking |

```bash
# Watch main application log in real time
tail -f /var/log/loginsight/runtime.log

# Search for errors across all logs
grep -i "error\|exception\|fail" /var/log/loginsight/runtime.log | tail -100
grep -i "error\|drop"           /var/log/loginsight/ingestion.log | tail -50
grep -i "error\|warn"           /var/log/loginsight/cassandra/system.log | tail -50
```

---

## Cluster Node Diagnostics

```bash
# Check all cluster nodes status
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/nodes" | \
  jq '.nodes[] | {host: .hostname, state: .state, role: .role, version: .version}'

# Check cluster ingestion statistics
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/stats" | jq '.'

# Check disk usage on all nodes
for node in vrli-prod-01 vrli-prod-02 vrli-prod-03; do
  echo "=== $node ==="
  ssh admin@$node.example.local "df -h /var/log/loginsight && du -sh /var/log/loginsight/*"
done

# Check if services are running on the master node
ssh admin@vrli-prod-01.example.local
systemctl status loginsight
systemctl status nginx
systemctl status cassandra
```

---

## Generating a Support Bundle

Collect a support bundle before opening a Broadcom SR:

```bash
# Via API — trigger support bundle generation
curl -sk -u 'admin:<password>' -X POST \
  "https://vrli-prod-01.example.local/api/v2/support/bundle" | jq '.'

# The bundle is generated asynchronously — check status
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/support/bundle/status" | jq '.'

# Download the bundle when status is "COMPLETE"
curl -sk -u 'admin:<password>' -o vrli-support-bundle.zip \
  "https://vrli-prod-01.example.local/api/v2/support/bundle/download"
```

Via UI: **Administration → Cluster → Support Bundle → Generate and Download**.

The support bundle contains: application logs, Cassandra logs, system metrics, configuration (no passwords), and cluster topology.

---

## Diagnosing Ingestion Issues

When log events stop arriving or ingestion rate drops to zero:

```bash
# Check ingestion stats
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/stats" | \
  jq '{eventsPerSecond: .eventsIngested, diskPct: .diskUsagePercent}'

# Verify syslog listener is running
ss -tulnp | grep -E "514|1514|9543"
# Expected: ports 514 (UDP), 1514 (TCP), 9543 (TCP) listening

# Test syslog reception (from a syslog source)
logger -n vrli-prod-01.example.local -P 514 -d "test message from diagnostic"
# Check if the test event appears in Interactive Analytics within 30 seconds

# Check for ingestion errors (parse failures, dropped events)
grep -i "drop\|parse error\|overflow" /var/log/loginsight/ingestion.log | tail -50
```

---

## Diagnosing Query Performance Issues

If interactive analytics queries are slow or time out:

```bash
# Check Cassandra compaction status — long compaction can cause query slowness
ssh admin@vrli-prod-01.example.local
nodetool compactionstats

# Check Cassandra heap usage — if heap > 90%, queries slow significantly
nodetool info | grep -i "heap"

# Check current query load
tail -50 /var/log/loginsight/query.log | grep -i "slow\|timeout\|error"
```

---

## Verifying Agent Connectivity

When an agent is not delivering logs:

```bash
# On the agent host — check agent service
systemctl status liagentd

# Check agent log
tail -100 /var/log/vmware/loginsight-agent/liagent.log | grep -i "error\|connect\|ssl"

# Test connectivity from agent to Aria Ops for Logs on port 9543
nc -zv vrli-prod-01.example.local 9543
# Expected: Connection to vrli-prod-01.example.local 9543 port [tcp/*] succeeded!

# Verify agent configuration
grep -v "^#\|^$" /var/lib/loginsight-agent/liagent.ini
```

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
```
