# Pure1 — Capacity


<div class="kb-summary">
Capacity reference covering Capacity via Pure1 API, Capacity Alerts, Capacity Planning, Snapshot Space Management, Common Capacity Issues.
</div>

```text
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
