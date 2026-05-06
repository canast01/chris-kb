# Dell Data Domain CLI Reference

Commonly used Data Domain OS commands for managing backup appliances.

> Connect via SSH: `ssh sysadmin@<dd_hostname>`. Use `ddsh` for extended diagnostics.

---

## System Status

```bash
# System info
system show all
system show version
system show stats
system show hardware

# Health
health check show
alert show current
alert show history
alert show history brief
```

---

## Filesystem

```bash
# Filesystem status
filesys show
filesys show compression
filesys show space
filesys status

# Enable / disable / clean
filesys enable
filesys disable
filesys clean start
filesys clean status

# Capacity
filesys show space
filesys show compression summary
```

---

## MTrees (Data Management Units)

```bash
# List MTrees
mtree list
mtree show <mtree_name>

# Create / delete
mtree create /data/col1/<mtree_name>
mtree delete /data/col1/<mtree_name>

# Quota
mtree quota set hard-limit <size> <unit> /data/col1/<mtree_name>
mtree quota show
```

---

## Replication

```bash
# Status
replication show all
replication show config
replication show stats

# Context operations
replication add source mtree://<src_host>/data/col1/<mtree> destination mtree://<dst_host>/data/col1/<mtree>
replication initialize <context_id>
replication resync <context_id>
replication sync <context_id>
replication break <context_id>

# Monitoring lag
replication status
replication show stats | grep lag

# Failover (passive side)
replication failover <context_id>
```

---

## DDBoost

```bash
# DDBoost status
ddboost status
ddboost show clients

# Users and storage units
ddboost storage-unit list
ddboost storage-unit create <name>
ddboost user list
ddboost user add <username>
```

---

## NFS

```bash
nfs show exports
nfs add export /data/col1/<mtree> clients <ip_or_cidr>
nfs del export /data/col1/<mtree> clients <ip_or_cidr>
nfs show clients
nfs status
```

---

## CIFS / SMB

```bash
cifs show
cifs show clients
cifs share show
cifs share add /data/col1/<mtree>
cifs share del /data/col1/<mtree>
```

---

## Network

```bash
# Interfaces
net show all
net show config
net show settings

# Routes
net route show
net route add host <ip> gateway <gw> dev <if>
net route del host <ip>

# DNS
net hosts show
net config hosts add <ip> <hostname>
```

---

## Users & Security

```bash
# Local users
user list
user add <username>
user change password <username>
user del <username>
user show <username>

# Roles
user role show
role list

# Authentication
auth show
```

---

## Disk & Storage

```bash
# Disk info
disk show state
disk show hardware
disk show stats

# Enclosures
enclosure show hardware
enclosure show all

# Tier status
tier list
tier show detail
```

---

## Diagnostics

```bash
# Logs
log view
log list
log dump system
log watch

# Support bundle
support bundle create
support bundle show

# System diagnostics
ddsh
# Inside ddsh:
#  diagnose all
#  iostat 1 10
#  vmstat 1 10
```

---

## Backup & Configuration

```bash
# Config backup
config backup create
config backup show

# Config restore
config backup list
config backup restore <backup_name>
```
