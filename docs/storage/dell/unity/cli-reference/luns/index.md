# Unity LUNs

> Part of the Dell Unity CLI Reference (Unisphere CLI).
## List LUNs

```bash
uemcli -d <ip> /stor/config/lun show
uemcli -d <ip> /stor/config/lun show -detail
```

## Create a LUN

```bash
uemcli -d <ip> /stor/config/lun create \
    -name <lun_name> \
    -pool <pool_id> \
    -size 100G
```

## Expand a LUN

```bash
uemcli -d <ip> /stor/config/lun -id <lun_id> set -size 200G
```

## Rename a LUN

```bash
uemcli -d <ip> /stor/config/lun -id <lun_id> set -name <new_name>
```

## Delete a LUN

```bash
uemcli -d <ip> /stor/config/lun -id <lun_id> delete
```

> Ensure the LUN is unmasked from all hosts before deletion.

## LUN Host Access (Masking)

```bash
# Show host access for a LUN
uemcli -d <ip> /stor/config/lun -id <lun_id> show -detail

# Grant host access
uemcli -d <ip> /stor/config/lun -id <lun_id> set -hostAccess <host_id>:hlu=<hlu_id>
```

## LUN Snapshots

```bash
# List snapshots for a LUN
uemcli -d <ip> /prot/snap show -res <lun_id>

# Create a snapshot
uemcli -d <ip> /prot/snap create -name <snap_name> -res <lun_id>

# Restore a snapshot
uemcli -d <ip> /prot/snap -id <snap_id> restore

# Delete a snapshot
uemcli -d <ip> /prot/snap -id <snap_id> delete
```

## LUN Performance Metrics

```bash
# Show real-time LUN stats
uemcli -d <ip> /metrics/value/rt show -interval 5 \
    -filter "lun.throughput.total.read"
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| LUN not visible to host | Host masking | Set `-hostAccess` |
| LUN expand fails | Pool capacity | Check pool free space |
| Snapshot restore fails | Active I/O | Quiesce host I/O first |
| Delete fails | Active connections | Unmask from all hosts first |
