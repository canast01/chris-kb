# Aria Ops for Logs — Health Checks


<div class="kb-summary">
Health Checks reference covering Daily Health Checks, Weekly Health Checks, Pre-Upgrade Health Gate, Log File Locations on Appliance.
</div>

## Daily Health Checks

### Cluster Node Status

```bash
# Check all cluster nodes via API
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/nodes" | \
  jq '.nodes[] | {host: .hostname, state: .state, role: .role, version: .version}'

# Expected: all nodes state = "ACTIVE"
```
```text
┌────────────────────────────── Aria Operations for Logs — Health Checks ───────────────────────────────┐
│                                                                                                       │
│  Daily vRLI health check: disk, ingestion rate, cluster nodes, alerts, and source flow.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Cluster Health                │  │               Ingestion Health              │   │
│   │     All nodes: green in Cluster section      │  │       Events/sec: steady baseline rate      │   │
│   │        Disk: hot partition <80% used         │  │      Sources: all expected sending logs     │   │
│   │          CPU/RAM: under 80% average          │  │      vSphere sources: heartbeat recent      │   │
│   │          NTP: all nodes time-synced          │  │       Drop rate: near zero if healthy       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Alert and forwarding health confirm the notification pipeline is operational.                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Alert Health                 │  │              Integration Health             │   │
│   │     Alerts: all enabled (none disabled)      │  │          Aria Ops connection: green         │   │
│   │     Test alert: fire and receive notify      │  │      SIEM forward: test event received      │   │
│   │      Alert history: no unexpected gaps       │  │        SSO: AD login test user works        │   │
│   │        Webhook: HTTP 200 from target         │  │      Archive: last export job succeeded     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRLI master/worker VMs · disk storage · NTP · ESXi syslog config · SIEM target                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Hot partition      = /storage/var/loginsight/ disk; fills with indexed log data                      │
│  Events/sec         = Real-time ingestion rate; baseline varies by environment size                   │
│  Drop rate          = Percentage of received syslog messages discarded; should be ~0%                 │
│  Heartbeat          = vSphere agent sends periodic log; gap indicates source disconnected             │
│  Cluster nodes      = Master + workers visible in Administration → Cluster section                    │
│  Alert test         = Manually trigger alert query to confirm notification delivery                   │
│  Webhook 200        = Successful HTTP response from notification target on alert fire                 │
│  Archive job        = Scheduled task exporting logs to NFS/S3; check last success time                │
│  Aria Ops conn      = vRLI integration with Aria Operations; shows in Aria Ops admin page             │
│  SSO test           = Browser login test confirming LDAP/AD authentication still working              │
│  SIEM test event    = Send synthetic log and verify it appears in SIEM after forwarding               │
│  NTP sync           = All vRLI nodes must be NTP-synced; time skew breaks cluster consensus           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Via UI: **Administration → Agents** — agents with a last check-in older than 15 minutes are potentially offline.

---

### Alert Definitions Health

```bash
# Check that all alert definitions are enabled
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/alerts" | \
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
  -X POST "https://vrli-prod-01.example.local/api/v2/events/ingest" \
  -d '{
    "query": "",
    "start-time": "'$(date -d "1 hour ago" +%s000)'",
    "end-time": "'$(date +%s000)'",
    "content-pack-fields": ["hostname"],
    "limit": 0
  }' | jq '.fieldValues[] | .value'
```

### Notification Channel Test

```text
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
