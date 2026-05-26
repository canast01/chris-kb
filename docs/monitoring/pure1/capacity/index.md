# Pure1 — Capacity

```text
Capacity Trending — Pure1
                                   threshold (80%)
                                   │
Used ▲                             │
     │                    ╭────────╯ ← projected full
     │               ╭────╯
     │          ╭────╯
     │     ╭────╯   trend line
     │╭────╯
     └──────────────────────────────────► time
       now        +30d      +60d    +90d

Alert Thresholds:
┌──────────────────┬───────────┬──────────┐
│ Array space warn │    70%    │ Warning  │
│ Array space crit │    80%    │  Error   │
│ Volume near full │    90%    │ Warning  │
│ Snapshot excess  │  >50% use │ Warning  │
└──────────────────┴───────────┴──────────┘
```
┌───────────────────────────────────── Pure1 — Capacity Management ─────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Capacity Overview               │  │                 Forecasting                 │   │
│   │              Total raw capacity              │  │             30/60/90 day horizon            │   │
│   │               Effective used %               │  │               ML growth model               │   │
│   │              Data reduction 1:X              │  │             Projected full date             │   │
│   │              Unique vs reduced               │  │               Seasonal adjust               │   │
│   │                Snapshot space                │  │              Capacity alert 90d             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Capacity metrics from Purity OS via phonehome · Pure1 processes and forecasts                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Effective capacity = Usable capacity after RAID; starting point for data placement                   │
│  Data reduction = Combined dedup + compression ratio (e.g., 3.5:1)                                    │
│  Unique data = Data before dedup; actual bytes written by hosts                                       │
│  Reduced data = Physical footprint after dedup and compression                                        │
│  Snapshot space = Physical space used by snapshots; tracked separately                                │
│  Projected full date = ML forecast of when effective capacity will be exhausted                       │
│  30/60/90 day = Default forecast horizons; Pure1 alerts at < 90 days                                  │
│  Seasonal adjust = ML accounting for periodic usage spikes in forecast                                │
│  Capacity alert = Pure1 alert + TAC case when horizon < 90 days                                       │
│  Evergreen refresh = Capacity expansion via Pure subscription hardware refresh                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```bash
ssh pureuser@<flashblade-ip>

# FlashBlade capacity
purearray list --space

# File system capacity
purefs list --space | sort -k4 -rh | head -20

# Object store bucket usage
purebucket list --space
```

## Capacity via Pure1 API

```bash
TOKEN="<pure1-token>"

# All arrays with capacity data
curl -s "https://api.pure1.purestorage.com/api/1.latest/arrays?fields=name,capacity,space" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Arrays above 80% used
curl -s "https://api.pure1.purestorage.com/api/1.latest/arrays?fields=name,space" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for a in data.get('items', []):
    space = a.get('space', {})
    total = a.get('capacity', 0)
    used  = space.get('unique', 0) + space.get('snapshots', 0)
    if total > 0 and (used / total) > 0.8:
        print(f\"{a['name']}: {used/total*100:.1f}% used\")
"
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

## Common Capacity Issues

| Symptom | Cause | Action |
|---|---|---|
| Used growing faster than expected | Snapshot accumulation | Review snapshot policies; delete stale snapshots |
| Data reduction ratio dropped | New data type (already-compressed data like video) | Normal — not actionable; pure capacity has grown |
| Volume space used ≠ array space used | Thin provisioning — volumes report provisioned, array reports actual | Expected behaviour |
| Forecast shows < 30 days to full | Rapid data growth or snapshot accumulation | Escalate to storage team; open Evergreen expansion request |
