# FlashBlade — Health Checks

```
FlashBlade Health Check Sequence
  purefb alert list ──► Any active alerts?
         │
         ▼
  purefb blade list ──► All blades healthy (no failed/missing)?
         │
         ▼
  purefb hardware list ──► Chassis / PSU / fans ok?
         │
         ▼
  purefb array list --space ──► Capacity < 80%?
         │
         ▼
  purefb replication list ──► ActiveDR lag within RPO?
         │
         ▼
  Pure1 portal ──► Fleet-level anomaly check
```

> Part of the [FlashBlade Operations](../index.md) reference.

---

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| [ ] Run `purefb alert list` | `purefb alert list` | review all active alerts; flag any hardware, capacity, or replication warnings |
| [ ] Run `purefb blade list` | `purefb blade list` | confirm all blades are in `healthy` state; flag any `failed` or `missing` blades |
| [ ] Run `purefb hardware list` | `purefb hardware list` | confirm all hardware components (power supplies, fans, fabric modules) are healthy |
| [ ] Run `purefb filesystem list` | `purefb filesystem list` | review filesystem utilization; flag any filesystem above 80% of provisioned limit |
| [ ] Run `purefb bucket list` | `purefb bucket list` | check S3 bucket count and data growth trends |
| [ ] Run `purefb replication list` | `purefb replication list` | confirm all ActiveDR links are in `active` status with lag within RPO |
| [ ] Check Pure1 portal for capacity growth forecasts, anomalies, and hardware alerts | | |

## Health Check

- [ ] No active alerts in `purefb alert list`
- [ ] All blades are `healthy` — no `failed` or `missing` blades in `purefb blade list`
- [ ] All hardware components healthy — no PSU, fan, or FM (fabric module) failures
- [ ] No filesystems at or above provisioned limit — clients would receive ENOSPC errors
- [ ] All ActiveDR replication links are `active` and lag is within RPO
- [ ] All network interfaces are `up`: `purefb network interface list`
- [ ] Purity//FB version is within Pure's supported N-2 release window

```bash
# FlashBlade array status and Purity//FB version
purefb array list

# All blades and their health state
purefb blade list

# All hardware components (PSUs, fans, FMs) and status
purefb hardware list

# All filesystems with provisioned and used capacity
purefb filesystem list

# All S3 buckets and usage
purefb bucket list

# All active alerts
purefb alert list

# ActiveDR replication links and lag
purefb replication list

# All snapshots for filesystems and object store
purefb snap list

# Network interfaces and their operational state
purefb network interface list
```

## Array Health

```bash
purefb array
purefb hardware
purefb alert list
```

Or via the FlashBlade GUI:
- **Overview → Array** — overall health summary
- **Storage → File Systems** / **Object Store** — capacity and status
- **Alerts → Active** — unacknowledged alerts

## Blade Health

```bash
purefb blade list
```

All blades should show `status: healthy`. Any blade showing `unhealthy` or `failed` requires investigation.

## Drive / Media Health

FlashBlade uses direct-attached blade storage. Drive-level health is abstracted — monitor at the blade level:

```bash
purefb blade list --all
```

## Network Interface Health

```bash
purefb network-interface list
```

All data VIPs should show `enabled: true` and `type: vip`.

## Replication Health

```bash
purefb fs-replica-link list
purefb bucket-replica-link list
```

Verify replica links show `lag-time` within expected RPO.

## Pre-Change Checklist

- [ ] All blades `healthy`
- [ ] No active critical alerts
- [ ] All network VIPs enabled
- [ ] Replication healthy (lag within RPO)
- [ ] Capacity below 80%

## Health Summary Table

| Check | Command | Expected |
|---|---|---|
| Array health | `purefb array` | No warnings |
| Blades | `purefb blade list` | All healthy |
| Alerts | `purefb alert list` | No critical |
| Network | `purefb network-interface list` | All VIPs enabled |
| Replication | `purefb fs-replica-link list` | Low lag |
