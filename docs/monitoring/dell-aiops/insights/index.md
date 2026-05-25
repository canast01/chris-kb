# Dell AIOps: Workload Insights, Performance Predictions, and Bottleneck Detection

```text
Proactive Insights — Dell AIOps
┌──────────────────────────────────────────────┐
│  Correlate events across systems             │
│  SYS-A: write latency +60%  (T+0)           │
│  SYS-A: cache write-pending high  (T+0)      │
│  SYS-A: disk SMART warn (slot 4)  (T-2h)    │
└────────────────────┬─────────────────────────┘
                     ▼ pattern match
┌──────────────────────────────────────────────┐
│  Identify pattern: degrading backend drive   │
│  leading to cache pressure → latency spike   │
└────────────────────┬─────────────────────────┘
                     ▼
┌──────────────────────────────────────────────┐
│  Proactive insight raised                    │
│  before outage occurs                        │
│  ┌────────────────────────────────────────┐  │
│  │ Insight: "Impending performance event  │  │
│  │ on SYS-A — replace disk in slot 4"     │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

Dell AIOps Insights analyses workload behaviour patterns to surface performance predictions and identify bottlenecks before they cause service degradation. This page covers workload insight types, how to interpret prediction data, and how to act on bottleneck detections.

## Insight Types Overview

Navigation: **CloudIQ > AIOps > Insights**

| Insight Type | Description |
|---|---|
| Workload Characterisation | Classification of I/O pattern (sequential, random, mixed) |
| Performance Prediction | Projected latency/IOPS trend over next 7–30 days |
| Bottleneck Detection | Active constraint on a system (CPU, cache, bandwidth) |
| Noisy Neighbour | Volume or workload consuming disproportionate resources |
| Growth Trend | Projected resource exhaustion based on workload growth |

## Workload Characterisation

AIOps classifies each volume or file system's I/O workload based on observed read/write ratios, block sizes, and sequentiality.

```bash
# Get workload characterisation for all volumes
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/workload_insights?select=volume_name,system_name,io_pattern,read_percent,avg_block_size_kb" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '.results[] | {volume_name, io_pattern, read_percent}'
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
