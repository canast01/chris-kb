# FlashArray Health Checks
## Daily Health Check

```bash
# Array summary — capacity, data reduction, Purity version
purecli array list

# Drive health
purecli drive list

# Hardware component health
purecli hardware list

# Active alerts
purecli alert list
```

## Controller Health

```bash
purecli hardware list | grep -i ct
```

Both controllers (CT0, CT1) should show `status: ok` and `temperature` within normal range.

## Drive Health

```bash
purecli drive list
```

All drives should show `status: healthy`. Any drive in `failed`, `unhealthy`, or `recovering` state requires attention.

## Volume Health

```bash
purecli volume list
purecli volume list --space
```

Verify no volumes are in an unexpected state and capacity is within expected range.

## Host Connectivity

```bash
# List hosts and their connected volumes
purecli host list
purecli host list --connect

# List host connections
purecli connection list
```

Confirm all expected hosts are connected.

## Replication Health

```bash
# FlashArray Async Replication (ActiveDR or async)
purecli pg list
purecli pg list --schedule
purecli pg list --space
```

Verify pod/protection group replication is healthy.

## Pure1 Cloud Monitoring

Pure1 provides proactive health monitoring and AI-driven alerts:
- Log in to **Pure1 → Arrays** → verify all arrays show green
- **Analysis → Capacity** — no arrays approaching full
- **Alerts** — no critical unacknowledged alerts

## Pre-Change Checklist

- [ ] All drives `healthy`
- [ ] Both controllers `ok`
- [ ] No critical active alerts
- [ ] Replication healthy
- [ ] Capacity below 80%

## Health Summary Table

| Check | Command | Expected |
|---|---|---|
| Array health | `purecli array list` | No warnings |
| Drives | `purecli drive list` | All healthy |
| Hardware | `purecli hardware list` | All ok |
| Alerts | `purecli alert list` | No critical |
| Capacity | GUI or `--space` | < 80% used |
