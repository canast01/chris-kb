# Capacity Forecasting


<div class="kb-summary">
Capacity forecasting predicts when a resource will be exhausted based on historical trend data, enabling proactive expansion before impact occurs.
</div>

## Forecasting Model

```text
Days to exhaustion = (Current capacity - Current usage) / Growth rate per day
```
┌───────────────────────────────── Performance — Capacity Forecasting ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Project future capacity needs from historical growth trends for compute/storage/network    │   │
│   │     Collect 90-day trend data; extrapolate to 12/18/24 month horizon; add headroom buffer     │   │
│   │         Alert at 75% usage; plan procurement at 80%; never operate above 90% sustained        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Metrics to Forecast              │  │               Forecast Process              │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │          CPU: peak + average util %          │  │            Collect 90-day history           │   │
│   │          RAM: committed vs balloon           │  │            Calculate growth rate            │   │
│   │         Storage: used + growth/month         │  │           Extrapolate to 12/24 mo           │   │
│   │          Network: peak bandwidth %           │  │           Add 20% headroom buffer           │   │
│   │           VM count + density ratio           │  │          Raise procurement request          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Headroom     = Buffer above projected peak; allows for spikes and unplanned growth                 │
│    Balloon mem  = VMware memory balloon driver; reclaims VM memory under host pressure                │
│    Growth rate  = Measured increase per month/quarter; used to project future consumption             │
│    Procurement lead = Time from request to delivered capacity; plan 3-6 months ahead                  │
│    Overcommit   = Allocating more vCPU/RAM than physical; acceptable with headroom tracking           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text

**Pure FlashArray:**
```bash
purecli volume list --space   # per-volume capacity
purecli array get             # array-wide reduction ratio and used capacity
```

## Forecasting by Resource Type

### Storage

```bash
# Current usage and growth estimate
df -h /data
# Compare with last month's snapshot
# If usage grows 50 GB/month and 200 GB free → 4 months to full

# ONTAP aggregate capacity
storage aggregate show -fields size,used,percent-used,availsize
```

### Compute (CPU/Memory)

```bash
# Average CPU over last 30 days from sar
for day in $(seq 1 30); do
  sar -u -f /var/log/sa/sa$(date -d "$day days ago" +%d) 2>/dev/null | \
    awk '/Average/ {print $3}' | tail -1
done | awk '{sum+=$1; count++} END {print "30d avg CPU:", sum/count "%"}'
```

### Network

```bash
# Interface utilisation trend (sar)
sar -n DEV 1 10 | grep eth0
# Historical: sar -n DEV -f /var/log/sa/saDD
```

## Forecasting Thresholds

| Resource | Alert at | Plan expansion at |
|---|---|---|
| Storage (array/volume) | 75% used | 60 days to full |
| CPU (sustained avg) | >70% | >60% sustained trend |
| Memory | >80% | >75% sustained trend |
| Network (sustained) | >60% of link speed | >50% sustained trend |
| Backup window | >90% of allowed window | 75% |

## Capacity Report Template

```markdown
Date:          2026-05-06
System:        prod-storage-01 (ONTAP)
Current Usage: 68% (34 TB / 50 TB)
Growth rate:   ~400 GB/month (3-month avg)
Days to 85%:   ~105 days (est. mid-August)
Days to 100%:  ~180 days (est. November)

Recommendation:
  Order 20 TB additional capacity by July.
  Submit hardware request by 2026-06-01 (6-week lead time).
```

## Automation — Monthly Report Script

```bash
#!/bin/bash
echo "=== Capacity Forecast $(date +%Y-%m-%d) ==="
df -h | awk 'NR>1 && $5+0 > 70 {print "WARNING:", $6, "at", $5}'
echo ""
echo "Storage volumes near capacity:"
# Add ONTAP/Pure/array CLI calls here for production use
```
