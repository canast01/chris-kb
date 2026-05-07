# Replication Operations

Operational guidance for managing Data Domain replication — monitoring, troubleshooting, and failover.
## Routine Checks

```bash
# All replication contexts and their state
replication show all

# Contexts with issues (not replicating or idle)
replication status | grep -v "replicating\|idle"

# Current lag (bytes behind)
replication show stats | grep lag
```

## Replication Lag Thresholds

| Lag | Action |
|---|---|
| < 1 hour | Healthy |
| 1–4 hours | Monitor — could indicate network or load issue |
| > 4 hours | Alert — investigate immediately |
| Not updating | Context may be in error state |

## Troubleshooting Replication

```bash
# 1. Check context state
replication show all | grep <context_id>

# 2. Check for alerts related to replication
alert show current | grep -i repl

# 3. Network connectivity to destination
net ping <destination_dd_ip>

# 4. Check filesystem health on both systems
filesys status
filesys show space

# 5. Check if destination has space
# (Log into destination DD and run:)
filesys show space
```

## Common Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Context in `error` state | Network, auth, or filesystem issue | Check `alert show current` |
| High lag | Bandwidth saturation or high source I/O | Check `replication show stats` — bytes/sec |
| Initialization stalled | Destination filesystem full | Check `filesys show space` on destination |
| Context stuck | Process issue on DD | `replication disable <id>` then `replication enable <id>` |

## Manual Operations

```bash
# Trigger an immediate sync
replication sync <context_id>

# Pause replication (source continues writing; changes accumulate)
replication disable <context_id>

# Resume
replication enable <context_id>

# Resync (re-establishes after break or failover)
replication resync <context_id>
```

## Failover Procedure

Run on the **destination** Data Domain when the source is unavailable:

```bash
# Step 1 — break the context to make destination writeable
replication failover <context_id>

# Step 2 — redirect backup application to destination DD
# (update backup application target configuration)

# Step 3 — validate backup jobs complete successfully
ddboost show clients   # or nfs show clients
```

## Recovery After Primary Returns

```bash
# Step 1 — re-establish and resync
replication resync <context_id>

# Step 2 — confirm sync complete (lag = 0)
replication show stats | grep lag

# Step 3 — redirect backup application back to primary
```
