# FlashArray Protection Groups

Protection groups (pgroups) define sets of volumes for consistent snapshot and replication operations.

## List Protection Groups

```bash
purecli pg list
purecli pg list --schedule
purecli pg list --space
```

## View Protection Group Members

```bash
purecli pg list <pg_name> --volumes
purecli pg list <pg_name> --hosts
purecli pg list <pg_name> --hgroups
```

## Create a Protection Group

```bash
purecli pg create <pg_name>
```

## Add Volumes to a Protection Group

```bash
purecli pg addvolumes <pg_name> --vol <vol1>,<vol2>
```

## Add Hosts to a Protection Group

```bash
purecli pg addhosts <pg_name> --hosts <hostname>
purecli pg addhgroups <pg_name> --hgroups <hgroupname>
```

## Configure Snapshot Schedule

```bash
# Set snapshot schedule (every 1 hour, retain 24 per day, 7 days)
purecli pg schedule <pg_name> \
    --snap-enabled true \
    --snap-frequency 3600 \
    --snap-per-day 24 \
    --snap-for-days 7
```

## Configure Replication Schedule (Async to Remote)

```bash
# Enable replication target
purecli pg connect <pg_name> --target <remote_array_name>

# Set replication schedule
purecli pg schedule <pg_name> \
    --replicate-enabled true \
    --replicate-frequency 3600
```

## Take a Manual Snapshot

```bash
purecli pgsnapshot create --pgroup <pg_name> --suffix <snap_name>
```

## List Snapshots

```bash
purecli pgsnapshot list --pgroup <pg_name>
```

## Delete a Protection Group

```bash
purecli pg delete <pg_name>
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Snapshot not running | Schedule enabled? | Enable with `--snap-enabled true` |
| Replication failing | Target connectivity | Check inter-array connectivity and credentials |
| Volume missing from PG | Members list | Add with `pg addvolumes` |
| Space growing fast | Snapshot retention | Reduce `snap-for-days` |
