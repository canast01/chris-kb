# Alert Management

```
Alert Lifecycle
┌─────────────┐
│   Trigger   │  (threshold breach / anomaly / hardware fault)
└──────┬──────┘
       ▼
┌─────────────┐
│  Severity   │  Critical / High / Medium / Low
│  Assignment │
└──────┬──────┘
       ▼
┌─────────────┐
│    Triage   │  claim → assess impact → identify cause
└──────┬──────┘
       ▼
┌─────────────┐
│ Acknowledge │  linked ticket, owner assigned
└──────┬──────┘
       ▼
┌─────────────┐
│   Resolve   │  fix applied, verified
└──────┬──────┘
       ▼
┌─────────────┐
│    Close    │  root cause documented in ticket
└──────┬──────┘
       ▼
┌─────────────┐
│  Post-      │  threshold review, noise reduction
│  Incident   │
└─────────────┘
```

## Alert Severity Levels

| Severity | Meaning | Response Time |
|---|---|---|
| Critical | Service impact or imminent outage | Immediate (15 min) |
| High | Degraded performance or threshold approaching | 1 hour |
| Medium | Warning — trend needs attention | Business day |
| Low | Informational / advisory | Next scheduled review |

## Alert Response Workflow

1. **Acknowledge** — claim the alert so others know it's owned
2. **Assess impact** — is a service affected? How many users?
3. **Triage root cause** — use the relevant runbook or dashboard
4. **Resolve or escalate** — fix, or hand to the right team with context
5. **Close and document** — note root cause and action taken in the ticket

## Silencing and Suppression Rules

- Never silence without a linked ticket and expiry time
- Maintenance window suppressions: set duration = window + 30 min buffer
- Recurring false positives: fix the threshold, don't silence permanently

```bash
# Zabbix — suppress a host for 2 hours (API example via curl)
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"maintenance.create","params":{...},"auth":"<token>","id":1}' \
  http://<zabbix>/api_jsonrpc.php
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
