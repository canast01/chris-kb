# Aria Operations for Logs — Health Checks

<div class="kb-summary">
Health checks for Aria Operations for Logs — cluster node status, disk and ingestion rate, alert configuration, archive jobs, syslog source connectivity, and integration health.
</div>

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

## Run This Routine

Run these 8 checks in order at the start of each shift or after any infrastructure change.

1. **Master node health** — `curl -sk -u 'admin:<password>' https://<log-insight-fqdn>/api/v2/cluster/nodes` — confirm all nodes return `"state": "ACTIVE"`
2. **Ingestion rate** — Admin → System Monitor → confirm events/sec is within the expected baseline range; a drop to zero means sources have stopped sending
3. **Disk usage** — Admin → System Monitor → Storage → confirm no partition is above 80% used; the hot partition at `/storage/var/loginsight/` fills fastest
4. **Agent connectivity** — Admin → Agents → confirm all expected agents show Connected and have a recent last-seen timestamp
5. **Alert count** — Alerts → Interactive Analytics → review open critical alerts and confirm each is acknowledged or has an active investigation
6. **Content pack versions** — Administration → Content Packs → check all installed packs and flag any that have an update available
7. **Archiving** — Admin → Archiving → check the last archive job timestamp; flag if no successful export has run within the expected schedule
8. **Syslog sources** — Admin → Sources → confirm all expected source IPs are present and sending logs; investigate any that have not sent data in the last hour

---

## Cluster Node Status Commands

```bash
# Check all cluster nodes via API
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/nodes" | \
  jq '.nodes[] | {host: .hostname, state: .state, role: .role, version: .version}'
# Expected: all nodes state = "ACTIVE"
```

## Alert Configuration Commands

```bash
# Check that all alert definitions are enabled
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/alerts" | \
  jq '.alerts[] | select(.enabled == false) | {name: .name, enabled: .enabled}'
# Output should be empty — no alerts should be disabled unintentionally
```
## Ingestion and Source Activity

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
Notification channel test: **Administration → Notification Channels → select channel → Test**

## Platform Log Checks

```bash
# Watch main runtime log for errors
tail -f /var/log/loginsight/runtime.log | grep -i "error\|warn\|exception"

# Check ingestion errors (dropped events, parsing failures)
grep -i "error\|drop\|fail" /var/log/loginsight/ingestion.log | tail -50

# Check Cassandra storage health
tail -100 /var/log/loginsight/cassandra/system.log | grep -i "error\|warn"
```
