# CloudIQ: Health Score, Component Status, and Connectivity

```text
Health Score Composition
┌───────────────────────────────────────────┐
│  Component Scores → Weighted System Score │
│                                           │
│  Controllers  ████████████░░  89/100     │
│  Drives/SSDs  ████████████████ 100/100   │
│  Fabric/Net   ████████░░░░░░░  60/100  ! │
│  Enclosures   ████████████░░░  85/100    │
│               ─────────────────────────  │
│  System Score ██████████░░░░░  79/100    │
│                (weighted average)        │
└───────────────────────────────────────────┘
         │                                  
         ▼                                  
┌──────────────────────────────────┐        
│        Fleet View                │        
│  SYS-A  ████  92 ✓               │        
│  SYS-B  ████  79 ⚠               │        
│  SYS-C  ██    45 ✗ (critical)    │        
└──────────────────────────────────┘        
```

Dell CloudIQ assigns a health score to each registered system based on active alerts, hardware status, and connectivity. This page covers how the health score is calculated, how to interpret component status, and how to verify and restore system connectivity.

## Health Score Overview

Each system receives a health score from 0 to 100 (100 = fully healthy). The score is computed from the number and severity of active issues.

Navigation: **CloudIQ > Health**

Health score bands:

| Score Range | Status | Interpretation |
|---|---|---|
| 90 – 100 | Healthy (green) | No significant issues |
| 70 – 89 | Warning (yellow) | Minor or informational issues present |
| 40 – 69 | Degraded (orange) | Major issues require attention |
| 0 – 39 | Critical (red) | Critical issues; service impact likely |

```bash
# Get health score for all registered systems
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/storage_systems?select=id,name,health_score,health_issues_count" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '.results[] | {name, health_score, issues: .health_issues_count}'

# Get health details for a specific system
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/storage_systems/<systemId>/health" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json"
```

## Component-Level Health

Clicking into a system shows component-level status. Components vary by system type but typically include:

| Component | System Types | Common Issues |
|---|---|---|
| Drives / SSDs | PowerStore, PowerMax, PowerScale | Predictive failure, read errors |
| Controllers / Engines | PowerStore, PowerMax | Controller offline, firmware mismatch |
| Nodes | PowerScale | Node offline, network partition |
| Enclosures | All | Fans, power supplies, temperature |
| Replication Links | PowerStore, PowerMax | SRDF link degraded, replication lag |
| Battery Backup Units | PowerStore | BBU charge < threshold |

## Connectivity Checks

CloudIQ relies on the system's phone-home channel (SRS or ESRS) to receive telemetry. If a system goes grey or shows stale data, check connectivity first.

```bash
# Check last contact time for all systems
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/storage_systems?select=name,last_contact_timestamp,connectivity_status" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '.results[] | {name, last_contact: .last_contact_timestamp, status: .connectivity_status}'
```

Connectivity status values:

| Status | Meaning | Action |
|---|---|---|
| Connected | Telemetry flowing normally | None |
| Disconnected | No data received | Check SRS/ESRS gateway and firewall rules |
| Degraded | Intermittent connectivity | Review proxy/network path between system and gateway |

Outbound connectivity requirements for SRS/ESRS:

| Destination | Port | Protocol |
|---|---|---|
| esrs.emc.com | 443 | HTTPS |
| cloudiq.dell.com | 443 | HTTPS |
| api.dell.com | 443 | HTTPS |

## Verifying SRS Connectivity on PowerScale

```bash
# On PowerScale OneFS CLI
ssh admin@powerscale.example.com

# Check SRS (SmartConnect Remote Support) status
isi remotesupport connectemc status

# Trigger a manual connectivity test
isi remotesupport connectemc start

# View SRS daemon logs
grep -i "connectemc" /var/log/messages | tail -30
```

## Common Health Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| System shows grey in CloudIQ | Phone-home disconnected | Verify SRS/ESRS gateway, check firewall |
| Health score drops unexpectedly | New hardware alert generated | Check Alerts tab, drill into component detail |
| Component status stale | Delayed telemetry | Last contact > 1 hour indicates connectivity issue |
| Drive predictive failure alert | Vendor analysis from telemetry | Open support case — proactive replacement |
| Replication link health degraded | WAN latency or packet loss | Check network path between replication endpoints |
