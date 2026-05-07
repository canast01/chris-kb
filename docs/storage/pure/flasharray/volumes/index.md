# FlashArray Volumes

## List Volumes

```bash
purecli volume list
purecli volume list --space      # includes capacity and data reduction stats
purecli volume list --details    # includes host connections and QoS settings
```

## Create a Volume

```bash
purecli volume create <volume_name> --size 1T
```

Size suffixes: `K`, `M`, `G`, `T`, `P`.

## Resize a Volume

```bash
purecli volume setattr <volume_name> --size 2T
```

Volumes can only be grown, not shrunk.

## Connect a Volume to a Host

```bash
purecli host connect <hostname> --vol <volume_name>
```

## Disconnect a Volume

```bash
purecli host disconnect <hostname> --vol <volume_name>
```

## Snapshot a Volume

```bash
# Create a snapshot
purecli volume snapshot <volume_name> --suffix <snap_suffix>

# List snapshots for a volume
purecli volume list <volume_name>.*
```

## Restore from Snapshot

```bash
# Overwrite volume with snapshot content
purecli volume copy <volume_name>.<snap_suffix> --overwrite <volume_name>
```

## Create a Clone

```bash
purecli volume copy <source_vol> <clone_name>
```

## Delete a Volume

```bash
# Volumes go to the destroyed state first (recoverable for 24 hours)
purecli volume destroy <volume_name>

# Permanently delete (eradicate)
purecli volume eradicate <volume_name>
```

## Recover a Destroyed Volume

```bash
purecli volume recover <volume_name>
```

## Volume Tags (for grouping/reporting)

```bash
# Set a tag on a volume
purecli volume settag <volume_name> --tag-name <key> --tag-value <value>

# List tags
purecli volume listtags <volume_name>
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Volume not visible to host | Host connection | `purecli host list --connect` |
| Resize fails | Size smaller than current | Volumes can only grow |
| Volume missing | Destroyed/eradicated | Check `purecli volume list --destroyed` |
| High capacity usage | Snapshots | Review and eradicate old snapshots |
