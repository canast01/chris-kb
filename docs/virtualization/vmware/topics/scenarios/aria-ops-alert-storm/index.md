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

Open Aria Operations → **Alerts** → sort by **Triggered Time** ascending to identify the incident start timestamp.

Look for: a cluster of alerts starting within a 30-second window — every alert after that point is likely a cascade. Check which object type carries the first alert; if it is a host, all subsequent VM alerts on that host are children.

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

Select the earliest-alerting host or cluster in Aria Operations → **Relationships** to surface the cascade visually.

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

These four events produce the most frequent alert storms in VMware environments — confirm in the source shown:

| Root cause | Signature in alert list | Where to confirm |
|---|---|---|
| Host failure | All VM alerts on one host, host shows HA event | vCenter → Events on the host |
| vSAN degradation | All VM storage latency alerts across a cluster | vCenter → vSAN → Skyline Health |
| Network congestion | East-west latency alerts on many VMs | NSX Manager → T0/T1 → BGP, edge health |
| NTP drift | Certificate errors, SSO failures, cross-product auth alerts | ESXi shell: `ntpq -pn` |

---

## 5. Cancel vs Suppress — Do the Right Thing

Choose the correct action once the root cause is confirmed:

- **Cancel** — marks alerts resolved; use when the fix is underway. Alerts will not re-fire once the condition clears.
- **Suppress** — silences without resolving; use only for planned maintenance windows.

To cancel: Aria Operations → **Alerts** → filter to the affected cluster → select all → **Cancel** → add the incident ticket number.

---

## 6. Correlate with Aria Operations for Logs

If the root cause is not obvious from alerts, open any storm alert → **Details** → **Related Logs** to query Aria Logs within ±5 minutes of the trigger time.

Look for: `WARN` or `ERROR` entries that predate the first alert by 30–120 seconds — the event just before the first alert is the originating cause.

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

After the incident, find the definition with the highest trigger count: Aria Operations → **Alerts** → **Configuration** → **Alert Definitions** → edit symptom thresholds.

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

## Key Terms

| Term | Definition |
|---|---|
| Aria Operations | VMware observability platform — collects metrics from vSphere, NSX, and storage; evaluates symptom definitions to generate alerts |
| Symptom definition | A threshold or condition rule in Aria Operations that, when triggered, contributes to an alert firing (e.g., CPU ready > 10% for 5 min) |
| Alert definition | A named rule in Aria Operations combining one or more symptom definitions; the unit shown in the Alerts list |
| Alert criticality | Severity level assigned to an alert — Critical, Warning, Immediate, or Information; determines colour and sort order in the Alerts view |
| Object relationship | Parent-child link between monitored objects (e.g., cluster → host → VM); used in the Relationship view to trace cascade origin |
| Aria Logs (Aria Operations for Logs) | VMware log analytics product — ingests syslog and structured events; integrated with Aria Operations via the Related Logs pane |
| IPFIX | IP Flow Information Export — a network flow protocol; Aria Logs can ingest IPFIX records from NSX to correlate network events with alert storms |
| Root cause | The single originating event that triggered all subsequent cascade alerts; identified by sorting alerts by Triggered Time ascending |
| Cascading alert | A secondary alert fired because a parent object's failure propagated to child objects (e.g., host failure → all VMs on that host alert) |
| REST API bearer token | Short-lived token returned by the Aria Operations `/suite-api/api/auth/token/acquire` endpoint; passed as `Authorization: Bearer <token>` on all subsequent API calls |
| Cancel (alert action) | Marks an active alert as resolved in Aria Operations; used when the underlying condition has been fixed or the root cause is confirmed |
| Suppress (alert action) | Silences an alert without resolving it; intended for planned maintenance windows only — suppressed alerts mask real future problems if left in place |
| Alert threshold | The numeric limit in a symptom definition at which a metric is considered anomalous; tuned post-incident to reduce noise without masking real problems |

---

## Related Scenarios

- [vSAN Disk or Component Failure](../vsan-disk-component-failure/index.md) — vSAN degradation is one of the most common single events that triggers a cluster-wide alert storm.
- [NSX Edge Failure / BGP Down](../nsx-edge-failure-bgp-down/index.md) — A BGP session drop on a T0 gateway produces a cascade of east-west latency and connectivity alerts.
- [NTP Drift / SSO Certificate Issues](../ntp-drift-sso-certificate/index.md) — NTP drift generates cross-product auth and certificate alerts that appear as a storm with no obvious hardware cause.
