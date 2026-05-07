# Dell Data Domain CLI Reference

Commonly used Data Domain OS (DDOS) commands for managing Dell EMC backup appliances. Data Domain is a purpose-built deduplication backup target — backup software writes to it, and it deduplicates data on the fly to save space.

> Connect via SSH: `ssh sysadmin@<dd_hostname>`. Use `ddsh` for extended diagnostics.

---

## System Status

These commands give you a quick view of the appliance's health — version, hardware, active alerts, and whether all components are functioning. Start here for any investigation.

### System Information

```bash
# Full system overview
system show all

# Software version
system show version

# Hardware inventory (disks, enclosures, NIC, HBA)
system show hardware

# Current system statistics (CPU, memory, throughput)
system show stats

# Uptime
system show uptime

# Serial number and model
system show summary
```

### Health Checks

```bash
# Run built-in health check
health check show

# Active alerts (open, unacknowledged)
alert show current

# Alert history (all alerts, resolved and unresolved)
alert show history

# Brief alert history (most recent)
alert show history brief

# Clear a resolved alert
alert acknowledge --id <alert_id>
```

### Alert Levels

| Level | Meaning |
|---|---|
| INFO | Informational only |
| WARNING | Action may be required |
| ERROR | Degraded functionality — investigate |
| CRITICAL | Service impacting — immediate action required |

### Software, Licensing, and Power

```bash
# Show installed software packages
system software version show

# License status
elicense show

# Power supply status
enclosure show hardware | grep -i power

# Fan and temperature
enclosure show hardware | grep -i fan
enclosure show hardware | grep -i temp
```

### System Time and NTP

```bash
ntp status
ntp show
ntp add timeserver <ntp_ip>
```

### Reboot and Support Bundle

```bash
# Safe shutdown
system shutdown

# Restart DDOS software (not a full reboot)
system restart

# Full reboot
system reboot

# Create a support bundle (for TAC cases)
support bundle create
support bundle show
support bundle export scp://user@host:/path/bundle.tar.gz
```

---

## Filesystem

The Data Domain filesystem (DDFS) is what does all the magic — it deduplicates and compresses every byte of backup data written to it. All user data lives in the active tier under `/data/col1/`. The filesystem must be enabled before you can receive backup data.

### Filesystem Status

```bash
# Filesystem state (enabled/disabled)
filesys status

# Full status overview
filesys show

# Compression and deduplication statistics
filesys show compression

# Space usage breakdown (pre-comp, post-comp, physical)
filesys show space
```

### Enable and Disable

```bash
# Enable the filesystem (required before accepting backup data)
filesys enable

# Disable the filesystem (maintenance only — stops all I/O)
filesys disable
```

### Cleaning (Garbage Collection)

Cleaning reclaims space from deleted or expired backup files. It runs automatically but can be triggered manually:

```bash
# Start a cleaning cycle
filesys clean start

# Show cleaning status
filesys clean status

# Stop an in-progress clean
filesys clean stop
```

> Cleaning is I/O intensive. Schedule during off-peak hours if running manually.

### Capacity and Compression Analysis

```bash
# Overall capacity summary
filesys show space

# Compression ratio and savings
filesys show compression summary

# Logical vs physical usage
filesys show space | grep -E "Used|Available|Total"
```

### Compression Ratio Fields

| Field | Meaning |
|---|---|
| Pre-comp | Total logical data written (before dedup/compression) |
| Post-comp | Physical space used on disk |
| Global comp factor | Overall compression ratio |
| Dedup savings | Percentage saved by deduplication |

### Space Recovery

```bash
# After backup data is expired by backup application — run cleaning to reclaim space
filesys clean start

# Monitor reclaim progress
filesys clean status
filesys show space
```

### Filesystem Integrity

```bash
filesys check
filesys show log
```

---

## MTrees (Data Management Units)

MTrees are logical partitions of the Data Domain filesystem. Think of them like separate buckets — each one can have its own quota, replication policy, and retention lock. Different backup applications or departments typically get their own MTree.

### List and View MTrees

```bash
# List all MTrees
mtree list

# Detail for a specific MTree
mtree show /data/col1/<mtree_name>

# All MTrees with usage stats
mtree list --verbose
```

### Create and Delete

```bash
# Create an MTree
mtree create /data/col1/<mtree_name>

# Delete an MTree (must be empty or use force)
mtree delete /data/col1/<mtree_name>
```

### Quotas

Quotas limit MTree disk usage and prevent one tenant from consuming all space:

```bash
# View current quotas
mtree quota show

# Set hard limit (backup fails when limit is reached)
mtree quota set hard-limit 10 TiB /data/col1/<mtree_name>

# Set soft limit (alert raised when exceeded)
mtree quota set soft-limit 8 TiB /data/col1/<mtree_name>

# Remove a quota
mtree quota reset /data/col1/<mtree_name>
```

### MTree Retention Lock (Compliance / Enterprise)

Retention lock prevents anyone from deleting backup data before a set period — required for compliance (GDPR, HIPAA, etc.):

```bash
# Enable retention lock on an MTree
mtree retention-lock enable mode enterprise /data/col1/<mtree_name>

# Set minimum/maximum retention period
mtree retention-lock set min-retention-period 30days /data/col1/<mtree_name>
mtree retention-lock set max-retention-period 7years /data/col1/<mtree_name>

# View retention lock settings
mtree retention-lock status /data/col1/<mtree_name>
```

### Common Operations

| Task | Command |
|---|---|
| Create MTree | `mtree create /data/col1/<name>` |
| Set hard quota | `mtree quota set hard-limit <size> TiB /data/col1/<name>` |
| View quotas | `mtree quota show` |
| Delete MTree | `mtree delete /data/col1/<name>` |
| Enable retention lock | `mtree retention-lock enable mode enterprise /data/col1/<name>` |

---

## Replication

Data Domain replication copies MTree data to a remote Data Domain appliance. It is a source-destination model — data flows one way, and the destination is a read-only copy (until failover). Used for DR and off-site backup copies.

### Status Overview

```bash
# All replication contexts (summary)
replication show all

# Per-context statistics (lag, bytes sent, compression)
replication show stats

# Quick status — state of all contexts
replication status
```

### Replication States

| State | Meaning |
|---|---|
| `replicating` | Actively syncing data |
| `idle` | Up to date, waiting for next sync |
| `initializing` | First-time sync in progress |
| `error` | Replication failed — check logs |
| `disabled` | Replication suspended |

### Configure a Replication Context

```bash
# Add MTree-level replication
replication add source mtree://<src_host>/data/col1/<mtree_name> \
    destination mtree://<dst_host>/data/col1/<mtree_name>

# Initialize replication (first sync — can take hours for large datasets)
replication initialize <context_id>
```

### Ongoing Operations

```bash
# Trigger an immediate sync
replication sync <context_id>

# Pause replication
replication disable <context_id>

# Resume replication
replication enable <context_id>

# Break a context (removes replication relationship)
replication break <context_id>
```

### Monitoring Replication Lag

```bash
# Lag in bytes (amount of data not yet replicated)
replication show stats | grep lag

# Lag in time
replication status | grep -E "context|lag"
```

### Failover

Run on the **destination** Data Domain when primary is unavailable:

```bash
# Break the context (makes destination writeable)
replication failover <context_id>

# After primary recovers — resync
replication resync <context_id>
```

### Replication Troubleshooting

| Issue | Check | Command |
|---|---|---|
| Context stuck in error | Alert detail | `alert show current` |
| High lag | Network bandwidth or congestion | `replication show stats` |
| Initialization stalled | Filesystem busy | `filesys show stats` on both systems |
| No data replicating | Context disabled | `replication show all` |

---

## DDBoost

DDBoost (Dell Data Domain Boost) integrates directly with backup applications (NetBackup, Networker, Avamar, Veeam) to offload deduplication processing to the backup client. This reduces network traffic and speeds up backups significantly.

### Service Status

```bash
# DDBoost service status and connection count
ddboost status

# Active client connections
ddboost show clients
ddboost show clients --verbose
```

### Storage Units

Storage units are the logical mount points backup applications connect to:

```bash
# List all storage units
ddboost storage-unit list
ddboost storage-unit show <storage_unit_name>

# Create a storage unit
ddboost storage-unit create <storage_unit_name>

# Delete a storage unit
ddboost storage-unit delete <storage_unit_name>
```

### Users

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

### Performance and DSP

```bash
# DDBoost throughput statistics
ddboost show stats

# DSP (Distributed Segment Processing) status — moves dedup to the client
ddboost option show | grep -i "dist-seg"

# Enable DSP
ddboost option set distributed-segment-processing enabled
```

### DDBoost Troubleshooting

| Issue | Check | Command |
|---|---|---|
| Backup fails to connect | DDBoost enabled and user exists | `ddboost status` |
| Slow backup speed | DSP not enabled | `ddboost option show` |
| Authentication errors | User/password mismatch | `ddboost user list` |
| Storage unit full | Quota or filesystem space | `ddboost storage-unit show <name>` |

---

## NFS & CIFS/SMB

Data Domain can be accessed directly over NFS or CIFS/SMB as an alternative to DDBoost — some backup applications mount the Data Domain like a regular file share and write backup files to it.

### NFS

```bash
# List all NFS exports
nfs show exports

# NFS service status
nfs status

# NFS client connections
nfs show clients
```

#### Managing NFS Exports

```bash
# Create an NFS export for an MTree
nfs add export /data/col1/<mtree_name> clients <ip_or_cidr>

# Allow multiple clients
nfs add export /data/col1/<mtree_name> clients <ip1>,<ip2>

# Modify export options
nfs modify export /data/col1/<mtree_name> clients <ip> options rw,root-squash

# Remove a client from an export
nfs del export /data/col1/<mtree_name> clients <ip_or_cidr>

# Remove the entire export
nfs del export /data/col1/<mtree_name>
```

#### NFS Options Reference

| Option | Meaning |
|---|---|
| `rw` | Read-write access |
| `ro` | Read-only access |
| `root-squash` | Map root user to anonymous (more secure) |
| `no-root-squash` | Root retains root privileges (needed for some backup apps) |
| `async` | Asynchronous writes — faster but risk on crash |

### CIFS / SMB

```bash
# CIFS service status
cifs show

# Active client connections
cifs show clients

# All CIFS shares
cifs share show

# Create a CIFS share for an MTree
cifs share add /data/col1/<mtree_name>

# Remove a CIFS share
cifs share del /data/col1/<mtree_name>
```

### NFS/CIFS Troubleshooting

| Issue | Check | Command |
|---|---|---|
| NFS mount fails | Export exists for client IP? | `nfs show exports` |
| Access denied on mount | `no-root-squash` needed? | `nfs modify export ... options no-root-squash` |
| CIFS share not visible | CIFS enabled? | `cifs show` |

---

## Network

Network commands manage the Data Domain's IP interfaces, routing, DNS, and NTP configuration. Correct networking is essential — backup clients need to reach the appliance, and replication requires connectivity to the remote Data Domain.

### Interface Status

```bash
# All interfaces — IP, speed, state
net show all

# Interface configuration
net show config

# Interface statistics (rx/tx, errors, drops)
net show stats
```

### Interface Configuration

```bash
# Configure an interface IP
net config eth1 <ip_address> netmask <mask>

# Bring an interface up or down
net enable eth1
net disable eth1
```

### Routing

```bash
# Current routing table
net route show

# Add a host route
net route add host <destination_ip> gateway <gateway_ip> dev <interface>

# Add a network route
net route add net <network_ip> netmask <mask> gateway <gateway_ip>

# Delete a route
net route del host <destination_ip>
```

### DNS

```bash
net hosts show
net config hosts add <ip_address> <hostname>
net show settings | grep -i dns
```

### NTP

```bash
ntp show
ntp status
ntp add timeserver <ntp_ip>
ntp del timeserver <ntp_ip>
```

### Ping, Traceroute, Bonding

```bash
# Connectivity test
net ping <destination_ip>
net traceroute <destination_ip>

# Bonding / LACP
net config bond show
net config bond create bond0 <eth1> <eth2> lacp
```

---

## Users & Security

These commands manage who can log in to the Data Domain and what they can do. The admin account has full control; other roles have limited access. You can also integrate with LDAP or Active Directory.

### Local Users

```bash
user list
user show <username>
user add <username>
user change password <username>
user del <username>
```

### User Roles

| Role | Permissions |
|---|---|
| `admin` | Full administrative access |
| `user` | Limited — view, change own password |
| `backup-operator` | DDBoost access; no system settings |

```bash
# List roles
role list

# Assign a role to a user
user modify <username> --role <role_name>
```

### Authentication Settings

```bash
# Show authentication configuration
auth show

# Enable LDAP authentication
auth add ldap server <ldap_ip> bind-dn <dn> bind-password <pass> base-dn <base_dn>

# Enable Active Directory
auth add active-directory <domain>

# Test LDAP authentication
auth test ldap server <ldap_ip>
```

### Password Policy

```bash
user password-policy show
user password-policy set min-length 12
user password-policy set max-age 90
```

### SSH Keys

```bash
user ssh-keys show <username>
user ssh-keys add <username> key "<public_key_string>"
user ssh-keys del <username> key <key_id>
```

---

## Disk & Storage

These commands show the physical disk health, RAID group status, and tier configuration. A failing disk triggers a RAID rebuild — monitor this carefully as a second failure during rebuild can cause data loss.

### Disk Status

```bash
# All disks with state (normal, unknown, suspect, failed)
disk show state

# Full hardware detail per disk
disk show hardware

# Disk performance statistics
disk show stats
```

### Disk States

| State | Meaning | Action |
|---|---|---|
| `normal` | Healthy and in use | None |
| `spare` | Hot spare, available | None |
| `reconstructing` | Rebuilding RAID after failure | Monitor; do not remove disks |
| `failed` | Drive failure | Replace immediately |

### Enclosures and Tiers

```bash
# Enclosure hardware overview
enclosure show hardware
enclosure show all

# Tier list (active, cloud)
tier list
tier show detail
```

### RAID Group Status

```bash
raid show all
raid show detail
raid show detail | grep -E "Rebuilding|Complete"
```

### Replacing a Failed Disk

1. Identify the failed disk slot: `disk show state | grep failed`
2. Note the enclosure and slot number.
3. Physically replace the disk.
4. Verify the system picks up the new disk: `disk show state`
5. Monitor RAID rebuild: `raid show detail | grep -i rebuild`

### Capacity Summary

```bash
filesys show space
filesys show compression summary
tier show detail
```

---

## Diagnostics

These tools help you troubleshoot problems and generate information for Dell support cases. The `ddsh` shell gives you access to Unix-level diagnostics when the regular CLI isn't enough.

### Log Access

```bash
# View system log (most recent events)
log view

# List available log files
log list

# Follow the log in real time
log watch

# Dump the full system log
log dump system
```

### Support Bundle

```bash
support bundle create
support bundle show
support bundle export scp://user@host:/path/bundle.tar.gz
```

### System Shell (ddsh)

`ddsh` provides a Unix-like shell with additional diagnostic tools:

```bash
# Enter the diagnostic shell
ddsh

# Inside ddsh:
diagnose all             # full system diagnostic run
iostat 1 10              # I/O statistics
vmstat 1 10              # virtual memory and CPU stats
netstat -an              # active network connections
df -h                    # filesystem usage
top                      # process list
```

### Hardware Diagnostics

```bash
health check show
disk show state
disk show detail | grep -E "error|sector"
enclosure show hardware
```

### Performance Capture

```bash
# Inside ddsh
iostat -x 1 30
filesys show stats
ddboost show stats
```

---

## Backup & Configuration

These commands let you save and restore the Data Domain's configuration settings — useful before upgrades, replacements, or troubleshooting.

```bash
# Create a config backup
config backup create

# List available backups
config backup list

# Restore from a named backup
config backup restore <backup_name>

# Show current system config summary
config show

# Capture config state before any change
config backup create
system show version
net show config
filesys show compression
replication show all
```

### SNMP & Syslog Configuration

```bash
snmp show config
alerts notify-list show
log show config
```
