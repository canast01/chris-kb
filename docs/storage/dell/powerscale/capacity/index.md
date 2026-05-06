# PowerScale Capacity

Capacity monitoring, quotas, and planning on Dell PowerScale.

## Cluster Capacity Overview

```bash
# Overall cluster used vs. free
isi statistics system list | grep -E "Cluster Capacity|Used|Free|HDD|SSD"

# Capacity by storage pool / node pool
isi storagepool nodepools list
isi storagepool tiers list

# Live statistics query
isi statistics query current \
    --stats cluster.disk.xfers.rate.read,cluster.disk.xfers.rate.write,\
cluster.disk.bytes.rate.read,cluster.disk.bytes.rate.write
```

## Storage Pool Detail

```bash
# Node pool capacity breakdown
isi storagepool nodepools list -v

# File pool policies and tiering
isi filepool policies list
isi filepool default-policy view

# SmartPools job status
isi job status | grep -i SmartPools
isi job jobs list | grep SmartPool
```

## Quotas (SmartQuotas)

```bash
# List all directory quotas
isi quota quotas list --type directory

# View a specific quota
isi quota quotas view --path /ifs/data/project1 --type directory

# Create a hard limit quota (10 TB)
isi quota quotas create --path /ifs/data/project1 \
    --type directory \
    --hard-threshold 10T \
    --soft-threshold 9T \
    --soft-grace 1W

# Modify quota threshold
isi quota quotas modify --path /ifs/data/project1 \
    --type directory \
    --hard-threshold 20T

# Delete a quota
isi quota quotas delete --path /ifs/data/project1 --type directory

# Show quota usage report
isi quota quotas list --type directory | awk '{print $1, $2, $3, $4}'
```

## Quota Notifications

```bash
# List quota notification rules
isi quota notifications list

# View current notification settings
isi quota settings notifications view
```

## Identifying Large Consumers

```bash
# Largest directories under /ifs (run from cluster shell)
du -sh /ifs/* 2>/dev/null | sort -h | tail -20

# Directories nearing quota threshold
isi quota quotas list --type directory | awk '
    NR>1 {
        if ($3 != "---" && $2 != "---") {
            pct = $3/$2*100
            if (pct > 80) print "WARNING:", pct"%", $1
        }
    }'
```

## Capacity Trend and Forecasting

```bash
# Historical capacity statistics
isi statistics history list \
    --stats cluster.disk.bytes.used,cluster.disk.bytes.free

# Estimate days until full (rough — divide free bytes by daily consumption rate)
isi statistics query current --stats cluster.disk.bytes.used,cluster.disk.bytes.free
```

For longer-term trending, use:
- **InsightIQ** — on-premises analytics for PowerScale
- **CloudIQ** — cloud-connected capacity forecasting with trend alerts

## Capacity Management Actions

| Situation | Action |
|---|---|
| > 80% used | Alert, review quotas, identify top consumers |
| > 90% used | Emergency — identify and remove/archive data |
| Node pool full but cluster has free space | File pool policy not moving data — check SmartPools job |
| SSD tier full | Check SSD caching policies; consider adding SSD nodes |
| Quota exceeded by application | Increase quota with change approval |
