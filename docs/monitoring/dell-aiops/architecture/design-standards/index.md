# Dell AIOps — Design Standards

<div class="kb-summary">
SCG prerequisites, configuration baselines, alert acknowledgement workflow, and operational standards for Dell AIOps.
</div>

```
┌──────────────────────────────────── Dell AIOps — Design Standards ────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Deployment Standards             │  │            Operational Standards            │   │
│   │             Dedicated AIOps VMs              │  │            All Dell infra covered           │   │
│   │            SSD for time-series DB            │  │             Adapters per product            │   │
│   │               HA pair minimum                │  │            Consistent thresholds            │   │
│   │                Backup nightly                │  │             Alert to ITSM always            │   │
│   │              TLS 1.2 end-to-end              │  │            Review recommendations           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  AIOps VMs on management cluster · SSD datastore · management VLAN only                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Dedicated VMs = AIOps runs on reserved VMs; not co-located with monitored workloads                  │
│  SSD datastore = Fast storage required for time-series DB write throughput                            │
│  HA pair = Two AIOps nodes for redundancy; active/passive or load-balanced                            │
│  Threshold consistency = Same alert trigger values across all environments; documented in runbook     │
│  Adapter per product = Each Dell product type has a dedicated adapter configured                      │
│  ITSM always = Every fired alert routed to ServiceNow; no silent monitoring                           │
│  Recommendation review = Weekly process to act on or dismiss open AI recommendations                  │
│  Nightly backup = AIOps config and DB snapshot to NFS or object store                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────── Dell AIOps — Design Standards ────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Deployment Standards             │  │            Operational Standards            │   │
│   │             Dedicated AIOps VMs              │  │            All Dell infra covered           │   │
│   │            SSD for time-series DB            │  │             Adapters per product            │   │
│   │               HA pair minimum                │  │            Consistent thresholds            │   │
│   │                Backup nightly                │  │             Alert to ITSM always            │   │
│   │              TLS 1.2 end-to-end              │  │            Review recommendations           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  AIOps VMs on management cluster · SSD datastore · management VLAN only                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Dedicated VMs = AIOps runs on reserved VMs; not co-located with monitored workloads                  │
│  SSD datastore = Fast storage required for time-series DB write throughput                            │
│  HA pair = Two AIOps nodes for redundancy; active/passive or load-balanced                            │
│  Threshold consistency = Same alert trigger values across all environments; documented in runbook     │
│  Adapter per product = Each Dell product type has a dedicated adapter configured                      │
│  ITSM always = Every fired alert routed to ServiceNow; no silent monitoring                           │
│  Recommendation review = Weekly process to act on or dismiss open AI recommendations                  │
│  Nightly backup = AIOps config and DB snapshot to NFS or object store                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Prerequisites

Dell AIOps capability is delivered through the CloudIQ platform — no separate AIOps appliance is deployed. The prerequisites mirror the CloudIQ SCG deployment:

| Requirement | Standard |
|---|---|
| SCG deployed | One SCG per site (see CloudIQ design standards) |
| Arrays connected | All managed arrays registered and collection green in CloudIQ |
| Portal access | CloudIQ portal account with admin or operator role |
| Licensing | AIOps features included in CloudIQ subscription (no extra licence) |

## Recommendation Acknowledgement Workflow

AIOps surfaces prioritised recommendations. Follow this workflow to close the loop:

1. **Review** recommendations weekly in the CloudIQ APEX Console
2. **Assign** each active recommendation to the responsible team member
3. **Act** — apply the recommendation within the SLA below, or document a deferral reason
4. **Dismiss** recommendations that are accepted risks (with a comment)

| Recommendation Severity | Action SLA |
|---|---|
| Critical (capacity or health risk) | 5 business days |
| High | 15 business days |
| Medium | 30 days or next change window |
| Low | Review quarterly |

## Alert Threshold Baselines

Thresholds are configured in CloudIQ and feed into the AIOps anomaly engine:

| Metric | Warning | Critical |
|---|---|---|
| Capacity utilisation | 75% | 85% |
| IOPS anomaly (% above baseline) | 50% | 100% |
| Latency anomaly (% above baseline) | 50% | 100% |
| Component health fault | Any component fault | Multiple component faults |

## Configuration Checklist

- [ ] SCG deployed and all arrays reporting collection-healthy
- [ ] AIOps / CloudIQ portal login verified for storage team accounts
- [ ] Notification rules set (email + ServiceNow for Critical)
- [ ] Weekly recommendation review scheduled as recurring calendar event
- [ ] APEX Console bookmarked and access verified for on-call engineer
