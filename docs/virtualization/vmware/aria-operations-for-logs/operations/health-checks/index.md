# Aria Ops for Logs — Health Checks

```
┌─────────────────────────────────────────────────────────────┐
│         Aria Ops for Logs Health Check Stack                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Cluster Nodes                                       │  │
│  │  GET /api/v2/cluster/nodes  ·  all state=ACTIVE      │  │
│  └──────────────────────────────────┬───────────────────┘  │
│                                     │                      │
│                                     ▼                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Disk Usage                                          │  │
│  │  df -h /var/log/loginsight  ·  < 70%: normal         │  │
│  │  GET /api/v2/cluster/stats  ·  diskUsagePercent      │  │
│  └──────────────────────────────────┬───────────────────┘  │
│                                     │                      │
│                                     ▼                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Ingestion Rate + Agent Connectivity                 │  │
│  │  eventsIngested > 0  ·  no stale agents (>15 min)   │  │
│  └──────────────────────────────────┬───────────────────┘  │
│                                     │                      │
│                                     ▼                      │
│  Alert Definitions: none accidentally disabled             │
└─────────────────────────────────────────────────────────────┘
```

## Daily Health Checks

### Cluster Node Status

```bash
# Check all cluster nodes via API
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.corp.local/api/v2/cluster/nodes" | \
  jq '.nodes[] | {host: .hostname, state: .state, role: .role, version: .version}'

# Expected: all nodes state = "ACTIVE"
```

Via UI: **Administration → Cluster** — all nodes should show a green indicator and **Active** state.

---

### Ingestion Rate and Disk Usage

```bash
# Cluster ingestion stats
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.corp.local/api/v2/cluster/stats" | \
  jq '{eventsPerSecond: .eventsIngested, diskUsedPct: .diskUsagePercent}'

# Per-node disk usage from SSH
ssh admin@vrli-prod-01.corp.local
df -h /var/log/loginsight
du -sh /var/log/loginsight/*
```

**Disk thresholds:**
- < 70% used: normal
- 70–80% used: schedule capacity expansion
- > 80% used: immediate action required — oldest data will be deleted to free space
- 100% used: ingestion stops

---

### Agent Connectivity

```bash
# List all registered agents and their last check-in time
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.corp.local/api/v2/agents" | \
  jq '.agents[] | {host: .hostname, lastActive: .lastActive, state: .state}' | \
  jq -s 'sort_by(.lastActive)'
```

Via UI: **Administration → Agents** — agents with a last check-in older than 15 minutes are potentially offline.

---

### Alert Definitions Health

```bash
# Check that all alert definitions are enabled
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.corp.local/api/v2/alerts" | \
  jq '.alerts[] | select(.enabled == false) | {name: .name, enabled: .enabled}'
# Output should be empty — no alerts should be disabled unintentionally
```

Via UI: **Alerts → Alert Definitions** — review the Enabled column and confirm no alerts have been accidentally disabled.

---

## Weekly Health Checks

### Log Source Coverage

Verify that all expected syslog sources are sending data. Open the Aria Ops for Logs UI and navigate to **Interactive Analytics**. Run the following field-based queries:

- **Source coverage**: Group by `hostname` → confirm all vCenter, NSX, and ESXi hostnames appear with recent events
- **Log gaps**: Filter `Last 7 days` — any hostname with zero events in the past 24 hours is a potential problem

```bash
# Via API — get unique hosts seen in the last hour
curl -sk -u 'admin:<password>' \
  -H "Content-Type: application/json" \
  -X POST "https://vrli-prod-01.corp.local/api/v2/events/ingest" \
  -d '{
    "query": "",
    "start-time": "'$(date -d "1 hour ago" +%s000)'",
    "end-time": "'$(date +%s000)'",
    "content-pack-fields": ["hostname"],
    "limit": 0
  }' | jq '.fieldValues[] | .value'
```

### Notification Channel Test

```
Administration → Notification Channels → select channel → Test
```

Confirm email, webhook (Slack/Teams), or SNMP notifications are delivered successfully. Investigate delivery failures before they are needed during a real incident.

---

## Pre-Upgrade Health Gate

Run before any Aria Ops for Logs upgrade:

- [ ] All nodes show **ACTIVE** in cluster view
- [ ] No nodes show disk > 80% used
- [ ] Ingestion rate is within normal range (baseline from last 7 days)
- [ ] No unacknowledged critical alerts in **Alerts → Active Alerts**
- [ ] VM snapshots taken for all cluster nodes
- [ ] NFS archive target accessible (if archiving is configured)
- [ ] Compatible content packs listed — check Marketplace for compatibility with the target version

---

## Log File Locations on Appliance

| Log | Path | Purpose |
|---|---|---|
| Runtime log | `/var/log/loginsight/runtime.log` | Main application events |
| Ingestion log | `/var/log/loginsight/ingestion.log` | Log receiving events and errors |
| Query log | `/var/log/loginsight/query.log` | Interactive analytics query history |
| Cassandra log | `/var/log/loginsight/cassandra/system.log` | Storage backend events |
| Agent log | `/var/log/loginsight/agent/agentd.log` | LI Agent receiver events |

```bash
# Watch main runtime log for errors
tail -f /var/log/loginsight/runtime.log | grep -i "error\|warn\|exception"

# Check ingestion errors (dropped events, parsing failures)
grep -i "error\|drop\|fail" /var/log/loginsight/ingestion.log | tail -50

# Check Cassandra storage health
tail -100 /var/log/loginsight/cassandra/system.log | grep -i "error\|warn"
```
