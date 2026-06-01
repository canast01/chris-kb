# CloudIQ: Health Score, Component Status, and Connectivity


<div class="kb-summary">
CloudIQ: Health Score, Component Status, and Connectivity reference covering Component-Level Health, Connectivity Checks, Verifying SRS Connectivity on PowerScale, Common Health Issues.
</div>

```text
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

## Common Health Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| System shows grey in CloudIQ | Phone-home disconnected | Verify SRS/ESRS gateway, check firewall |
| Health score drops unexpectedly | New hardware alert generated | Check Alerts tab, drill into component detail |
| Component status stale | Delayed telemetry | Last contact > 1 hour indicates connectivity issue |
| Drive predictive failure alert | Vendor analysis from telemetry | Open support case — proactive replacement |
| Replication link health degraded | WAN latency or packet loss | Check network path between replication endpoints |
