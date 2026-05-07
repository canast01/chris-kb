# Replication

> Part of the Dell Unity CLI Reference (Unisphere CLI).
## Replication Sessions

```bash
# List all replication sessions
uemcli -d <ip> -u admin /prot/rep/session show

# Detailed view — state, lag, source/destination resources
uemcli -d <ip> -u admin /prot/rep/session show -detail

# Specific session
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> show -detail
```

## Session States

| State | Meaning |
|---|---|
| Active | Replication running normally |
| Idle | No sync in progress; awaiting next interval |
| Syncing | Data transfer in progress |
| Paused | Manually suspended |
| Failed | Error — check alerts |
| Failed Over | DR site is now active |

## Pause and Resume

```bash
# Pause replication (source continues accepting writes)
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> pause

# Resume replication (re-syncs data accumulated during pause)
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> resume
```

## Manual Sync

```bash
# Trigger an immediate sync outside the RPO schedule
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> sync
```

## Planned Failover

```bash
# Failover with final sync — syncs, then activates DR copy (recommended)
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> failover -keepSync

# Emergency failover without sync (data may be behind RPO)
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> failover
```

## Failback

```bash
# Step 1 — reverse replication (DR becomes source, primary becomes destination)
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> reverse

# Step 2 — sync data back to primary
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> sync

# Step 3 — fail back to original primary
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> failback
```

## Replication Connections

```bash
# List connections (Unity ↔ Unity or Unity ↔ PowerStore)
uemcli -d <ip> -u admin /prot/rep/connect show

# Create a replication connection
uemcli -d <ip> -u admin /prot/rep/connect create \
    -destAddress <destination_sp_ip> \
    -destUsername admin \
    -destPassword <password>
```

## Create a Replication Session

```bash
# Replicate a LUN to a remote Unity
uemcli -d <ip> -u admin /prot/rep/session create \
    -srcRes <lun_id> \
    -dstSys <connection_id> \
    -dstResName <remote_lun_name> \
    -rpo 3600   # RPO in seconds (3600 = 1 hour)
```

## Health Check

```bash
# Check all sessions for non-healthy states
uemcli -d <ip> -u admin /prot/rep/session show | grep -v "Active\|Idle\|Session"

# Replication-related alerts
uemcli -d <ip> -u admin /prac/alert show | grep -i repl
```
