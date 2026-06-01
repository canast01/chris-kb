# Infrastructure Health Monitoring


<div class="kb-summary">
Infrastructure Health Monitoring reference covering Server Health (Windows), Storage Array Health, Network Health, Monitoring Agent Validation, Escalation Thresholds (reference).
</div>

```text
┌─────────────────────────────────── Monitoring — Health Monitoring ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             Health Monitoring — Composite Health Scores and Component-Level Checks            │   │
│   │     Domains: vSphere (Aria) · Dell storage (CloudIQ) · Fabric (NDI) · Pure storage (Pure1)    │   │
│   │     Check types: availability · performance · capacity · configuration · security posture     │   │
│   │         Health score: 0-100 composite; weighted by criticality; drives alert priority         │   │
│   │       Cadence: real-time streaming (NDI/Pure1) · 5-min polling (Aria) · hourly (CloudIQ)      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    A degraded health score is a leading indicator — act before a component fails fully                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Check Categories      │  │        Scoring Method       │  │       Response Actions      │   │
│   │      Availability check     │  │       0-100 composite       │  │      Alert auto-trigger     │   │
│   │      Performance check      │  │       Weighted by role      │  │      Ticket auto-create     │   │
│   │        Capacity check       │  │       Trend adjustment      │  │     Runbook link attach     │   │
│   │      Config compliance      │  │       Anomaly penalty       │  │       Escalation fire       │   │
│   │       Security posture      │  │     Historical baseline     │  │       Dashboard update      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Health checks run in: Aria Analytics node · CloudIQ SaaS · NDI Insights app · Pure1 SaaS             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Health score      = 0-100 composite aggregating availability, performance, and capacity metrics      │
│  Availability check= Ping/API test confirming a component is reachable and responding                 │
│  Performance check = Metric comparison against baseline thresholds (e.g. CPU/latency/IOPS)            │
│  Capacity check    = Remaining headroom evaluation; flags when approaching configured limits          │
│  Config compliance = Verifying running config matches approved baseline or compliance pack            │
│  Security posture  = Check for open ports, default credentials, missing patches                       │
│  Anomaly penalty   = Score deduction applied when ML model detects unusual behaviour                  │
│  Trend adjustment  = Score modifier based on trajectory; degrading trend lowers score faster          │
│  Runbook link      = URL to remediation steps automatically attached to a health alert                │
│  Weighted scoring  = Higher-criticality checks contribute proportionally more to overall score        │
│  Leading indicator = Metric that degrades before an outage; enables proactive response                │
│  Historical baseline= Learned normal behaviour used to calibrate anomaly detection                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Storage Array Health

**NetApp ONTAP:**
```bash
system health status show          # overall health
system health alert show           # open alerts
storage disk show -broken          # failed disks
volume show -percent-used >85      # volumes near capacity
```

**Pure FlashArray:**
```bash
purecli array get                  # overall status
purecli drive list | grep -v healthy
purecli volume list --space        # capacity view
```

**Dell PowerMax / Unity:**
```bash
# PowerMax — Solutions Enabler
symcfg list -health
symsys -sid <sid> list -failed

# Unity — CLI
uemcli -d <ip> /sys/general show
uemcli -d <ip> /sys/alert show
```

## Network Health

```bash
# OSPF neighbours (Cisco IOS / NX-OS)
show ip ospf neighbor

# BGP summary
show bgp ipv4 unicast summary

# Interface error counters
show interface | include "line protocol|input errors|output errors|CRC"
```

## Monitoring Agent Validation

```bash
# Check monitoring agent is running (Zabbix example)
systemctl status zabbix-agent2

# Check last contact with monitoring server
grep "sending data" /var/log/zabbix/zabbix_agent2.log | tail -5
```

## Escalation Thresholds (reference)

| Metric | Warning | Critical |
|---|---|---|
| CPU (sustained 15 min) | >70% | >90% |
| Memory | >80% | >95% |
| Disk usage | >75% | >90% |
| Storage latency (avg) | >5ms | >20ms |
| Backup failure | 1 job | 2+ consecutive |
