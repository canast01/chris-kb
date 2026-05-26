# CloudIQ: Health Score, Component Status, and Connectivity

```
┌───────────────────────────────────── CloudIQ — Health Monitoring ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                         Health Score Model: 0-100 composite per array                         │   │
│   │           Component inputs: hardware faults, performance, capacity, software events           │   │
│   │         Score 90-100: Green — healthy · 70-89: Yellow — warning · 0-69: Red — critical        │   │
│   │               Trend indicator: improving / steady / degrading over last 24 hours              │   │
│   │         Issue list: individual problems contributing to score reduction with weighting        │   │
│   │              Fleet view: all arrays ranked by health score; outliers highlighted              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Health score computed in Dell cloud from telemetry · updated approximately every 5 minutes           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Health score = Weighted composite of hardware, performance, capacity, and software inputs            │
│  Issue = Individual contributing problem; each has a weight and recommended fix                       │
│  Trend = Direction of health score movement over trailing 24-hour window                              │
│  Fleet view = Dashboard showing all registered arrays ordered by health score                         │
│  Red array = Health score below 70; requires immediate investigation                                  │
│  Yellow array = Health score 70-89; monitor closely and plan remediation                              │
│  Hardware fault = Physical component issue (drive, fan, power supply) reducing score                  │
│  Performance issue = Sustained latency or IOPS anomaly contributing to score reduction                │
│  Software event = Firmware error or software exception recorded by array                              │
│  Weight = Relative contribution of an issue to total score reduction                                  │
│  Resolved issue = Problem that cleared; score increases when issue count decreases                    │
│  Score history = 30-day time-series of health score; viewable in CloudIQ UI per array                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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
