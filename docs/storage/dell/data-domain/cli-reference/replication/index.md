# Replication

> Part of the Dell Data Domain CLI Reference.

Data Domain replication runs at the MTree level and uses a source-destination model. Both systems must have network connectivity and matching software versions.
## Status Overview

```bash
# All replication contexts (summary)
replication show all

# Replication configuration
replication show config

# Per-context statistics (lag, bytes sent, compression)
replication show stats

# Quick status — state of all contexts
replication status
```

## Replication States

| State | Meaning |
|---|---|
| `replicating` | Actively syncing data |
| `idle` | Up to date, waiting for next sync |
| `initializing` | First-time sync in progress |
| `error` | Replication failed — check logs |
| `disabled` | Replication suspended |

## Configure a Replication Context

```bash
# Add MTree-level replication (directional — source to destination)
replication add source mtree://<src_host>/data/col1/<mtree_name> \
    destination mtree://<dst_host>/data/col1/<mtree_name>

# Initialize replication (first sync — can take hours for large datasets)
replication initialize <context_id>
```

## Ongoing Operations

```bash
# Trigger an immediate sync (outside scheduled window)
replication sync <context_id>

# Pause replication (source continues; changes accumulated)
replication disable <context_id>

# Resume replication
replication enable <context_id>

# Break a context (irreversible — removes replication relationship)
replication break <context_id>
```

## Monitoring Replication Lag

```bash
# Lag in bytes (amount of data not yet replicated)
replication show stats | grep lag

# Lag in time
replication status | grep -E "context|lag"
```

## Failover (Passive Site Activation)

Run on the **destination** Data Domain when primary is unavailable:

```bash
# Break the context (makes destination writeable)
replication failover <context_id>
```

After failover, configure backup applications to point to the destination system.

## Re-establishing Replication After Failover

```bash
# Step 1 — resync (when primary recovers)
replication resync <context_id>

# Step 2 — confirm sync complete
replication status
replication show stats | grep lag

# Step 3 — failback: swap source/destination roles
# (requires breaking and recreating context in reverse)
```

## Replication Certificates

```bash
# Trust a remote DD (exchange certs — required for encrypted replication)
replication add source ... --encryption aes128
admintool certify <remote_dd_hostname>
```

## Troubleshooting

| Issue | Check | Command |
|---|---|---|
| Context stuck in error | Alert detail | `alert show current` |
| High lag | Network bandwidth or congestion | `replication show stats` → bytes/sec |
| Initialization stalled | Filesystem busy | `filesys show stats` on both systems |
| No data replicating | Context disabled | `replication show all` → state |
