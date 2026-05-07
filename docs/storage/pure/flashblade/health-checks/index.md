# FlashBlade Health Checks

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

## File System Health

```bash
purefb fs list
purefb fs list --all
```

All file systems should show `destroyed: false` and correct capacity.

## Object Store Health

```bash
purefb bucket list
purefb object-store-account list
```

Verify expected buckets are present and not destroyed.

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
