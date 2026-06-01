# Aria Ops for Logs — Diagnostics


<div class="kb-summary">
Diagnostics reference covering Log File Locations, Generating a Support Bundle, Diagnosing Ingestion Issues, Diagnosing Query Performance Issues, Verifying Agent Connectivity and 1 more sections.
</div>

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
┌─────────────────────────────── Aria Operations for Logs — Diagnostics ────────────────────────────────┐
│                                                                                                       │
│  Diagnose vRLI problems using system monitor, runtime logs, API checks, and support bundle.           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Built-in Diagnostics             │  │               Log File Review               │   │
│   │       Admin → System Monitor: disk/CPU       │  │       /var/log/loginsight/runtime.log       │   │
│   │         Admin → Cluster: node status         │  │       /var/log/loginsight/queries.log       │   │
│   │        API: GET /api/v1/cluster/nodes        │  │        /var/log/loginsight/alerts.log       │   │
│   │      Explore: search for ingest errors       │  │        /var/log/vmware/vra/ (if LCM)        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Generate support bundle from VAMI before contacting VMware support for complex issues.               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Support Bundle                │  │             Network Diagnostics             │   │
│   │       VAMI → Support → Download bundle       │  │       netstat -tulpn: ports listening       │   │
│   │      Includes: logs + config + DB state      │  │        tcpdump: verify syslog packets       │   │
│   │      LCM logscraper: multi-product diag      │  │       nc -zv host 514: test port reach      │   │
│   │       Upload to VMware SR for analysis       │  │      curl -k :443/api/v1: API reachable     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRLI appliance · VAMI at :9543 · LCM logscraper · AD/LDAP · firewall                                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  System Monitor    = vRLI Admin section showing real-time disk/CPU/RAM/ingestion metrics              │
│  runtime.log       = Main vRLI log; Java exceptions, startup errors, cluster events                   │
│  queries.log       = Records slow or failed queries; diagnose search performance                      │
│  alerts.log        = Alert firing log; check if alerts fired and notifications sent                   │
│  Cluster nodes API = GET /api/v1/cluster/nodes; shows node state and role                             │
│  VAMI support bundle= Downloads all vRLI logs and config in one archive                               │
│  LCM logscraper    = Multi-product diagnostic tool for Aria Suite managed environments                │
│  tcpdump           = Capture syslog packets on vRLI NIC to confirm devices are sending                │
│  nc -zv            = Netcat port test; confirm syslog port reachable from source host                 │
│  curl -k           = Quick API connectivity test; check vRLI REST API responds                        │
│  netstat -tulpn     = List listening ports; verify 514, 6514, 443, 9543 are open                      │
│  VMware SR         = Support Request; provide bundle + timeline + version details                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash

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
