# Alert Management


<div class="kb-summary">
Alert Management reference covering Common Alert Sources, Alert Noise Reduction Checklist, Escalation Matrix (template).
</div>

```text
┌──────────────────────────────────── Monitoring — Alert Management ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Alert Management — Routing, Suppression, Escalation, and Notification Policies        │   │
│   │      Alert sources: Aria Operations · CloudIQ · Dell AIOps · Nexus Dashboard NDI · Pure1      │   │
│   │       Routing targets: email · SMTP relay · PagerDuty · ServiceNow ITSM · Slack webhooks      │   │
│   │         Suppression rules: maintenance windows · severity thresholds · dedup intervals        │   │
│   │          Escalation tiers: L1 auto-ticket → L2 paging → L3 vendor engage → P1 bridge          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Alert policies govern who is notified, how quickly, and what actions auto-trigger                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Alert Sources        │  │        Routing Rules        │  │          Escalation         │   │
│   │       Aria Ops alerts       │  │       Severity filter       │  │       L1: auto-ticket       │   │
│   │    CloudIQ health alerts    │  │      Object-type filter     │  │       L2: on-call page      │   │
│   │      NDI anomaly alerts     │  │      Maintenance window     │  │        L3: vendor TAM       │   │
│   │    Pure1 capacity alerts    │  │     Dedup interval 5 min    │  │     P1: war room bridge     │   │
│   │     AIOps predicted fail    │  │     Correlated grouping     │  │     SLA: 15-min response    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  SMTP relay: on-prem MTA (Postfix/Exchange) · PagerDuty: SaaS · ServiceNow: on-prem or SaaS           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Severity          = Critical/Warning/Info classification applied to each alert                       │
│  Suppression rule  = Policy silencing alerts during maintenance or known-issue windows                │
│  Deduplication     = Preventing repeat notifications for the same active alert condition              │
│  Escalation policy = Tiered response path: L1 auto-ticket → L2 page → L3 vendor → P1 bridge           │
│  Maintenance window= Scheduled suppression period applied to specific objects or groups               │
│  PagerDuty         = SaaS on-call paging platform; ingests alerts via API or email integration        │
│  ServiceNow ITSM   = Incident and change management platform; receives alert-driven tickets           │
│  SMTP relay        = Internal mail transfer agent routing notification emails                         │
│  Correlated group  = Multiple alerts from different sources mapped to a single incident               │
│  SLA               = Service Level Agreement; defines maximum acceptable response time                │
│  P1 bridge         = Priority-1 war-room call convened when critical systems are impacted             │
│  Alert fatigue     = Operator desensitisation caused by excessive or low-quality alerts               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Common Alert Sources

### High CPU

```bash
# Top processes
ps aux --sort=-%cpu | head -15
top -bn1 | head -20

# Historical (sar)
sar -u 1 10
```

### High Memory

```bash
free -h
ps aux --sort=-%mem | head -10
# Check for swap usage
swapon --show
```

### Disk Space

```bash
df -h | awk '$5+0 > 75'       # filesystems over 75%
du -sh /var/* | sort -rh | head -10
```

### Storage Latency (ONTAP)

```bash
statistics show -object volume -counter read_latency,write_latency -interval 5
qos statistics workload latency show
```

### Network Interface Errors

```bash
# Linux
ip -s link show <interface>
ethtool -S <interface> | grep -i error

# Cisco NX-OS
show interface <int> counters errors
```

## Alert Noise Reduction Checklist

- [ ] Are thresholds based on documented baselines?
- [ ] Are there duplicate alerts from multiple tools for the same condition?
- [ ] Are acknowledged-but-not-resolved alerts being tracked?
- [ ] Are low-severity alerts reviewed at least weekly, not just critical ones?
- [ ] Are any suppressions older than 30 days without a ticket?

## Escalation Matrix (template)

| Tier | On-call | Escalate After |
|---|---|---|
| L1 | Infra on-call | 30 min no progress |
| L2 | Platform / storage team | 1 hour on Critical |
| L3 | Vendor TAC / architect | 2 hours on Critical |
