# Cluster Status & Identity

> Part of the Dell PowerScale (Isilon) CLI Reference.
## Cluster Identity

```bash
# OneFS version
isi version

# Cluster status overview (nodes, capacity, health)
isi status

# Cluster name, contact info, timezone
isi cluster identity view

# Cluster configuration — join mode, ifs mount point
isi cluster config view
```

## Node Status

```bash
# List all nodes with ID, name, state
isi node list

# Specific node detail
isi node view <node_id>

# Node status on the cluster
isi status -n <node_id>
```

## Cluster Statistics

```bash
# Cluster-wide throughput and latency
isi statistics cluster list

# Drive statistics summary
isi statistics drive list

# Current IOPS and throughput
isi statistics system list

# Protocol breakdown (NFS, SMB, iSCSI)
isi statistics protocol list
```

## Node Hardware

```bash
# Hardware inventory per node
isi node hardware view <node_id>

# Drive list for a node
isi node drives list <node_id>

# Drive detail (bay, state, model, size)
isi node drives view <node_id> <bay_id>

# Environmental sensors (temp, power, fans)
isi node sensors view <node_id>
```

## Adding and Removing Nodes

```bash
# Smartfail a node (evacuates data before removal)
isi devices smartfail -d <node_id>

# Re-add a node after replacement
isi devices add -d <node_id>

# Check smartfail progress
isi status | grep smartfail
```

## Cluster Events and Jobs

```bash
# Active events (alerts)
isi events list

# Running jobs (FlexProtect, SmartPools, etc.)
isi job jobs list

# Job detail
isi job jobs view <job_id>
```

## Quick Cluster Health

```bash
# Combined status view
isi status
isi events list | grep -i "error\|critical\|warning"
isi job jobs list | grep -i running
```
