# Data Domain — Diagnostics

## Diagnostic Commands

```bash
# Filesystem health and space
filesys status
filesys show space
filesys show compression
filesys clean status

# Replication health
replication show
replication status
replication show errors

# DD Boost status and clients
ddboost status
ddboost show clients
ddboost show storage-units

# Active alerts and hardware status
alerts show current
alerts show history
system show
disk show state

# Network diagnostics
net show all
net show stats
ping <hostname-or-ip>

# MTree status and quotas
mtree list
mtree show compression mtree /data/col1/<mtree-name>
mtree show quota /data/col1/<mtree-name>

# NFS and CIFS
nfs show exports
cifs show shares

# VTL diagnostics
vtl show slots
vtl status

# AutoSupport / SCG connectivity
autosupport status
autosupport test

# User and access configuration
user show
adminaccess show
```

## Log Locations

| Log | Location / Command | Contains |
|---|---|---|
| System log | `log view` | DDOS events, service starts/stops, hardware events |
| Audit log | `log view audit` | User logins, configuration changes, administrative actions |
| Replication log | `log view replication` | Replication context events, errors, throughput records |
| Debug log bundle | `support bundle generate` | Full diagnostic bundle for Dell support case |
