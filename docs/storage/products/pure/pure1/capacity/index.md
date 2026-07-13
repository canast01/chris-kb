---
tags:
  - pure
description: "Capacity reference covering Capacity via Pure1 API, Capacity Alerts, Capacity Planning, Snapshot Space Management, Common Capacity Issues."
---
# Pure1 — Capacity

<div class="kb-summary">
Capacity reference covering Capacity via Pure1 API, Capacity Alerts, Capacity Planning, Snapshot Space Management, Common Capacity Issues.

*Applies to: Pure1*
</div>

```vegalite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "title": {
    "text": "Capacity \u2014 Thresholds",
    "fontSize": 13,
    "fontWeight": "normal"
  },
  "width": 480,
  "height": {
    "step": 26
  },
  "data": {
    "values": [
      {
        "metric": "Snapshot excessive",
        "zone": "Safe",
        "val": 50
      },
      {
        "metric": "Snapshot excessive",
        "zone": "Alert",
        "val": 50
      }
    ]
  },
  "mark": {
    "type": "bar",
    "cornerRadiusEnd": 3
  },
  "encoding": {
    "y": {
      "field": "metric",
      "type": "nominal",
      "axis": {
        "title": null,
        "labelLimit": 200
      },
      "sort": null
    },
    "x": {
      "field": "val",
      "type": "quantitative",
      "stack": "normalize",
      "axis": {
        "title": "Threshold boundary",
        "format": ".0%"
      }
    },
    "color": {
      "field": "zone",
      "type": "nominal",
      "scale": {
        "domain": [
          "Safe",
          "Alert"
        ],
        "range": [
          "#15803d",
          "#dc2626"
        ]
      },
      "legend": {
        "title": "Zone"
      }
    },
    "order": {
      "field": "zone",
      "sort": [
        "Safe",
        "Alert"
      ]
    },
    "tooltip": [
      {
        "field": "metric",
        "type": "nominal",
        "title": "Metric"
      },
      {
        "field": "zone",
        "type": "nominal",
        "title": "Zone"
      },
      {
        "field": "val",
        "type": "quantitative",
        "title": "Segment %",
        "format": ".0f"
      }
    ]
  }
}
```

## Capacity Alerts

Pure1 raises automatic capacity alerts at these thresholds:

| Alert | Default threshold | Severity |
|---|---|---|
| Array space warning | 70% usable used | Warning |
| Array space critical | 80% usable used | Error |
| Volume nearly full | 90% of volume size | Warning |
| Snapshot excessive | > 50% of usable used by snapshots | Warning |

Thresholds can be adjusted under **Pure1 → Settings → Alert Policies**.

## Capacity Planning

```bash
# Pure1 UI: Arrays → Capacity → Forecast
# Shows projected days to full at current growth rate

# Recommended actions when forecast < 90 days:
# 1. Review and delete aged snapshots
# 2. Identify top space consumers (purevol list --space)
# 3. Check volumes without thin provisioning savings (large unique)
# 4. Open Evergreen sizing request if expansion needed
```

## Snapshot Space Management

Stale snapshots are the most common cause of unexpected capacity growth:

```bash
# List snapshots older than 30 days sorted by size
puresnapshot list --space | awk 'NR==1 || $6 > 30' | sort -k5 -rh

# Destroy snapshots matching a pattern
puresnapshot destroy --name "vol01.*" --notail

# Eradicate immediately (skip 24h pending period)
puresnapshot eradicate --name "vol01.*"

# Show pending eradication queue
puresnapshot list --pending-only
```


```text title="Expected output"
NAME                          CREATED              SIZE      DAYS_OLD  PROVISIONED
vol01.snap-2024-08-15         2024-08-15T09:23:14Z 847.3GB   47        1.2TB
vol01.snap-2024-08-10         2024-08-10T14:51:02Z 612.1GB   52        1.2TB
vol01.snap-2024-07-28         2024-07-28T22:17:45Z 521.8GB   61        1.2TB
vol01.snap-2024-07-15         2024-07-15T11:33:19Z 389.5GB   75        1.2TB
vol01.snap-2024-07-02         2024-07-02T03:45:22Z 256.7GB   89        1.2TB
...
Destroyed 12 snapshots matching 'vol01.*'
Eradicated 12 snapshots matching 'vol01.*'
NAME                          CREATED              SIZE      ERADICATE_AT
vol01.snap-2024-06-18         2024-06-18T16:22:08Z 178.2GB   2024-09-16T16:22:08Z
vol01.snap-2024-06-05         2024-06-05T08:19:33Z 94.6GB    2024-09-04T08:19:33Z
```

!!! warning "Common errors"
    **`Error: Snapshot 'vol01.*' not found`** — Verify the snapshot name pattern exists using `puresnapshot list | grep vol01` before attempting destroy.
    **`Error: Cannot eradicate snapshot in use by replication target`** — Check active replication jobs with `purerepsnap list` and wait for replication to complete before eradicating.
## Common Capacity Issues

| Symptom | Cause | Action |
|---|---|---|
| Used growing faster than expected | Snapshot accumulation | Review snapshot policies; delete stale snapshots |
| Data reduction ratio dropped | New data type (already-compressed data like video) | Normal — not actionable; pure capacity has grown |
| Volume space used ≠ array space used | Thin provisioning — volumes report provisioned, array reports actual | Expected behaviour |
| Forecast shows < 30 days to full | Rapid data growth or snapshot accumulation | Escalate to storage team; open Evergreen expansion request |
