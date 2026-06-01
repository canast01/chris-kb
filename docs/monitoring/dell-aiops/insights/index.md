# Dell AIOps: Workload Insights, Performance Predictions, and Bottleneck Detection


<div class="kb-summary">
Dell AIOps: Workload Insights, Performance Predictions, and Bottleneck Detection reference covering Performance Predictions, Bottleneck Detection, Noisy Neighbour Detection, Common Insight Issues.
</div>

```text
┌──────────────────────────────────────── Dell AIOps — Insights ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             AIOps Insights: AI-generated summaries of infrastructure health trends            │   │
│   │                 Categories: Efficiency, Risk, Capacity, Performance, Security                 │   │
│   │         Insight = aggregated pattern observed across multiple objects and time windows        │   │
│   │                    Includes estimated business impact and priority ranking                    │   │
│   │                    Updated daily from ML analysis of all ingested telemetry                   │   │
│   │             Actionable: each insight links to recommendations and affected systems            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Insights computed in AIOps ML engine · stored in AIOps DB · displayed in UI and API                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Insight = Aggregated finding from ML analysis covering multiple systems or time windows              │
│  Efficiency insight = Identifying over-provisioned or under-utilised resources                        │
│  Risk insight = Patterns suggesting increased failure probability across a group of systems           │
│  Capacity insight = Fleet-wide capacity outlook; systems at risk within 90 days                       │
│  Performance insight = Workload patterns causing latency degradation across multiple arrays           │
│  Security insight = Configuration gaps or unusual access patterns detected by ML                      │
│  Business impact = Estimated operational risk or cost of not acting on insight                        │
│  Priority ranking = Insights ordered by estimated impact and urgency                                  │
│  Affected systems = List of infrastructure objects contributing to the insight                        │
│  Linked recommendations = Specific actions to address the identified pattern                          │
│  Daily refresh = Insight model runs nightly on new telemetry; UI updated each morning                 │
│  Pattern = Recurring behaviour observed across objects over time; basis for insight generation        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

I/O pattern classifications:

| Pattern | Read/Write Split | Block Size | Typical Workload |
|---|---|---|---|
| Sequential Read | >70% read | >128 KB | Backup restore, analytics |
| Sequential Write | >70% write | >128 KB | Log streaming, backup |
| Random Read | >70% read | <32 KB | Database index scans |
| Random Write | >70% write | <32 KB | OLTP databases |
| Mixed Random | ~50/50 | <64 KB | Virtualisation |

## Performance Predictions

AIOps provides a 7 and 30-day forward projection of key performance metrics based on current trends.

```bash
# Get performance prediction for a specific system
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/performance_predictions?system_id=<systemId>" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '.predictions[] | {metric, current_value, predicted_7d, predicted_30d, confidence}'
```

Key predicted metrics:

| Metric | Alert Threshold | Action if Trending High |
|---|---|---|
| Average read latency (ms) | > 5 ms for block, > 2 ms for all-flash | Investigate cache hit rate, queue depth |
| Write latency (ms) | > 3 ms sustained | Check destage rate, cache pressure |
| Controller CPU (%) | > 80% | Evaluate workload distribution across controllers |
| Cache hit rate (%) | < 70% | Analyse working set size vs. cache capacity |

## Bottleneck Detection

Bottleneck insights identify the active constraint limiting performance at a given time.

Navigation: **CloudIQ > AIOps > Insights > Bottlenecks**

```bash
# List active bottleneck insights
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/bottlenecks?filter=state%20eq%20%27ACTIVE%27" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '.results[] | {system_name, bottleneck_type, severity, recommendation}'
```

Common bottleneck types and remediation:

| Bottleneck Type | Root Cause | Typical Remediation |
|---|---|---|
| Front-end bandwidth saturated | Host-facing port congestion | Add front-end ports or upgrade to 32G FC |
| Cache write-pending high | Backend write throughput insufficient | Check backend drives health, RAID rebuild? |
| Controller CPU bound | Too many volumes or complex RAID | Rebalance volumes; consider tiering |
| Back-end bandwidth saturated | Drive enclosure bandwidth limit | Spread volumes across enclosures |

## Noisy Neighbour Detection

AIOps can identify when one workload is monopolising shared resources and impacting co-located workloads.

```bash
# Get noisy neighbour insights
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/insights?filter=type%20eq%20%27NOISY_NEIGHBOUR%27" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '.results[] | {noisy_volume, affected_volumes, impact_percent}'
```

## Common Insight Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| No insights generated | System recently added | Allow 7–14 days for model training |
| Bottleneck not detected despite obvious issue | System metrics below detection threshold | Use native system UI for immediate diagnosis |
| Prediction confidence < 0.6 | Irregular workload pattern | Extend data collection window |
| Noisy neighbour false positive | Coincident backup job | Review time correlation; dismiss if scheduled |
