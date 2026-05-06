# DDBoost

> Part of the Dell Data Domain CLI Reference.

DDBoost (Dell Data Domain Boost) offloads deduplication processing to the backup client, reducing network traffic and improving backup performance. It is used by NetBackup, Networker, Avamar, Veeam, and other backup applications.

## Service Status

```bash
# DDBoost service status and connection count
ddboost status

# Active client connections
ddboost show clients
ddboost show clients --verbose
```

## Storage Units

Storage units are the logical mount points backup applications connect to:

```bash
# List all storage units
ddboost storage-unit list
ddboost storage-unit show <storage_unit_name>

# Create a storage unit
ddboost storage-unit create <storage_unit_name>

# Create with MTree path
ddboost storage-unit create <name> --user <ddboost_user>

# Delete a storage unit
ddboost storage-unit delete <storage_unit_name>

# Storage unit usage and quota
ddboost storage-unit show <name> --verbose
```

## Users

Each backup application needs a dedicated DDBoost user:

```bash
# List DDBoost users
ddboost user list

# Add a user
ddboost user add <username>

# Change password
ddboost user change password <username>

# Assign user to a storage unit
ddboost user assign <username> storage-unit <storage_unit_name>

# Remove user
ddboost user del <username>
```

## Performance and Throughput

```bash
# DDBoost throughput statistics
ddboost show stats

# Connection statistics per client
ddboost show clients --verbose | grep -E "host|throughput|bytes"
```

## Distributed Segment Processing (DSP)

DSP moves deduplication to the client side, reducing network load:

```bash
# DSP status
ddboost option show | grep -i "dist-seg"

# Enable DSP
ddboost option set distributed-segment-processing enabled
```

## Troubleshooting

| Issue | Check | Command |
|---|---|---|
| Backup fails to connect | DDBoost enabled and user exists | `ddboost status` |
| Slow backup speed | DSP not enabled | `ddboost option show` |
| Authentication errors | User/password mismatch | `ddboost user list` |
| Storage unit full | Quota or filesystem space | `ddboost storage-unit show <name>` |
| Client not in list | Wrong hostname or not connected | `ddboost show clients` |
