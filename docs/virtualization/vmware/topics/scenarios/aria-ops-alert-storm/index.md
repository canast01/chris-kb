# Aria Ops Alert Storm

<div class="kb-summary">
An alert storm is when Aria Operations fires dozens or hundreds of alerts in a short window, typically
triggered by a single root cause that cascades across child objects. Treating each alert individually
misses the real cause. This scenario walks through grouping, correlating, and resolving the storm at
source — then tuning alert definitions to prevent recurrence.
</div>

```text
┌──────────────────────────────── Aria Ops Alert Storm — Investigation Flow ──────────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  START: Aria Operations shows a spike in active critical/warning alerts — dozens fire simultaneously ││
│   └────────────────────────────────────────────┬────────────────────────────────────────────────────────┘│
│                                                │                                                      │
│                   ┌────────────────────────────┼────────────────────────────┐                         │
│                   ▼                            ▼                            ▼                         │
│   ┌───────────────────────────┐   ┌───────────────────────────┐  ┌───────────────────────────┐        │
│   │  All alerts on hosts in   │   │  Alerts on VMs only?      │  │  Mixed VM + host alerts?  │        │
│   │  one cluster?             │   │  → storage or compute     │  │  → cascading failure from │        │
│   │  → host-level event       │   │    contention             │  │    a host or network event│        │
│   └────────────┬──────────────┘   └────────────┬──────────────┘  └────────────┬──────────────┘        │
│                │                               │                               │                      │
│                └───────────────────────────────┼───────────────────────────────┘                      │
│                                                ▼                                                      │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  Sort alerts by Triggered Time → identify incident start timestamp                                  ││
│   │  Use Relationship view on the earliest-alerting object to find root parent                          ││
│   └────────────────────────────────────────────┬────────────────────────────────────────────────────────┘│
│                                                │                                                      │
│                   ┌────────────────────────────┼────────────────────────────┐                         │
│                   ▼                            ▼                            ▼                         │
│   ┌───────────────────────────┐   ┌───────────────────────────┐  ┌───────────────────────────┐        │
│   │  Root cause found &       │   │  Root cause found, fix    │  │  Root cause unknown —     │        │
│   │  fix in progress          │   │  complete                 │  │  correlate Aria Logs      │        │
│   │  → Cancel storm alerts    │   │  → Tune alert definitions │  │  for source event         │        │
│   └───────────────────────────┘   └───────────────────────────┘  └───────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| Aria Operations | Alert engine, symptom definitions, Relationship view, alert cancellation and suppression |
| Aria Operations for Logs | Log correlation against the alert timestamp; surfaces the originating event |
| vCenter | Object inventory; host and VM state visible during the storm |
| NSX | Source of network alerts if east-west congestion or edge failure is the root cause |

---

## 1. Triage by Root Cause — Sort by Triggered Time

Open Aria Operations → **Alerts** → sort the alert list by **Triggered Time** ascending. Look for a cluster
of alerts that all start at the same timestamp or within a 30-second window. That timestamp is the
incident start. Every alert that fired after that point is likely a cascade from the same event.

Note the object types of the first alerts to fire. If the first alert is on a host, all subsequent
VM alerts on that host are children of the host event.

---

## 2. Group by Object Type

Examine which object types are carrying the bulk of alerts:

| Majority of alerts on | Likely root cause |
|---|---|
| Hosts in one cluster | Host failure, NTP drift, or network partition affecting the cluster |
| All VMs across multiple hosts | vSAN degradation or a shared storage event |
| VMs on one host only | That specific host has a problem (CPU, memory, or NIC) |
| Mixed host + VM alerts | Cascading from a network event — check NSX edge and BGP |

---

## 3. Use the Relationship View to Find the Parent Object

In Aria Operations, select the host or cluster where the earliest alerts fired. Navigate to
**Relationships** in the object detail pane. The relationship graph shows which child objects (VMs,
datastores, NICs) also have active alerts. This surfaces the cascade visually — the parent object
with the most children alerting is the root cause node.

```bash
# Aria Ops REST API — get all active critical alerts sorted by start time
curl -sk -X GET \
  "https://ariaops.domain.local/suite-api/api/alerts?alertStatus=ACTIVE&alertCriticality=CRITICAL" \
  -H "Authorization: Bearer <token>" \
  | jq '.alerts | sort_by(.startTimeEpoch) | .[] | {name: .name, object: .resourceId, time: .startTimeEpoch}'
```

```bash
# Get alerts for a specific resource (cluster or host)
curl -sk -X GET \
  "https://ariaops.domain.local/suite-api/api/alerts?resourceId=<resource-uuid>&alertStatus=ACTIVE" \
  -H "Authorization: Bearer <token>" \
  | jq '.alerts[] | {name: .name, criticality: .alertLevel, time: .startTimeEpoch}'
```

---

## 4. Identify Common Root Causes

These four events produce the most frequent alert storms in VMware environments:

| Root cause | Signature in alert list | Where to confirm |
|---|---|---|
| Host failure | All VM alerts on one host, host shows HA event | vCenter → Events on the host |
| vSAN degradation | All VM storage latency alerts across a cluster | vCenter → vSAN → Skyline Health |
| Network congestion | East-west latency alerts on many VMs | NSX Manager → T0/T1 → BGP, edge health |
| NTP drift | Certificate errors, SSO failures, cross-product auth alerts | ESXi shell: `ntpq -pn` |

---

## 5. Cancel vs Suppress — Do the Right Thing

Once the root cause is confirmed and a fix is underway, clear the alert storm correctly:

- **Cancel** — marks alerts as resolved. Use when the root cause is identified and being fixed. Alerts
  will not return once the underlying condition clears.
- **Suppress** — silences alerts without resolving them. Use only as a deliberate temporary measure
  (for example, during a planned maintenance window). Suppress leaves the root cause unaddressed.

To cancel all alerts in the storm: Aria Operations → **Alerts** → filter to the affected cluster or
host → select all → **Cancel**. Add a note referencing the incident ticket number.

---

## 6. Correlate with Aria Operations for Logs

If the root cause is not immediately obvious from the alert list, correlate with Aria Logs:

1. Aria Operations → open any alert from the storm → **Details** → **Related Logs**
   (only available if Aria Logs integration is configured).
2. The Related Logs pane shows log entries from the same object within ±5 minutes of the alert
   trigger time.
3. Look for `WARN` or `ERROR` entries that predate the first alert by 30–120 seconds. The event that
   appears just before the first alert is the originating cause.

```bash
# Aria Logs REST API — query logs for a specific host around the incident time
# epoch_start and epoch_end in milliseconds
curl -sk -X POST \
  "https://arialogs.domain.local/api/v1/events/query" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "constraints": [
      {"name": "hostname", "operator": "CONTAINS", "value": "esxi-host-01"},
      {"name": "text", "operator": "CONTAINS", "value": "ERROR"}
    ],
    "startTimeMillis": 1700000000000,
    "endTimeMillis": 1700000300000
  }' | jq '.events[] | {timestamp: .timestamp, text: .text}'
```

---

## 7. Tune Noisy Alert Definitions After the Storm

After the incident: adjust alert definitions that fired en masse. In Aria Operations →
**Alerts** → **Configuration** → **Alert Definitions** → find the definition with the highest
trigger count during the incident. Edit the symptom thresholds to reduce noise.

| Alert type | Default threshold | Suggested production tuning |
|---|---|---|
| CPU ready high | > 5% for 1 min | > 10% for 5 min |
| Memory balloon active | Any balloon detected | > 100 MB sustained for 10 min |
| vSAN read/write latency | > 10 ms | > 20 ms for 5 min |
| Disk read latency | > 20 ms | > 30 ms for 3 min |
| Network dropped packets | > 0% | > 0.1% for 2 min |

Avoid tuning thresholds so aggressively that real problems go undetected. The goal is
signal-to-noise improvement, not permanent suppression.

---

## Common Mistakes

- **Cancelling alerts without identifying the root cause.** If the underlying condition persists, the
  alerts will re-fire within minutes. Always confirm the cause before cancelling.
- **Using Suppress on production objects indefinitely.** Suppress is a temporary tool for maintenance
  windows. Leaving it in place masks real future incidents on the same object.
- **Treating each alert as a separate incident.** An alert storm is one incident. Open one ticket,
  identify one root cause. Working each alert in isolation wastes time and misses the pattern.
- **Tuning thresholds too aggressively.** Raising every threshold by 2× after a noisy event means a
  future real problem may not alert until it is already critical.

---

## Related Scenarios

- [vSAN Disk or Component Failure](../vsan-disk-component-failure/index.md) — vSAN degradation is one of the most common single events that triggers a cluster-wide alert storm.
- [NSX Edge Failure / BGP Down](../nsx-edge-failure-bgp-down/index.md) — A BGP session drop on a T0 gateway produces a cascade of east-west latency and connectivity alerts.
- [NTP Drift / SSO Certificate Issues](../ntp-drift-sso-certificate/index.md) — NTP drift generates cross-product auth and certificate alerts that appear as a storm with no obvious hardware cause.
