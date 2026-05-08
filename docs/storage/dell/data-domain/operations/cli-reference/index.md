# Data Domain — CLI Reference

Commonly used Data Domain OS (DDOS) commands for managing Dell EMC backup appliances. Data Domain is a purpose-built deduplication backup target — backup software writes to it, and it deduplicates data on the fly to save space.

> Connect via SSH: `ssh sysadmin@<dd_hostname>`. Use `ddsh` for extended diagnostics.

## Backup & Configuration

### Configuration Backup

```bash
# Create a config backup
config backup create

# List available backups
config backup list

# Show backup details
config backup show

# Restore from a named backup
config backup restore <backup_name>
```

### System Configuration Export

```bash
# Show current system config summary
config show

# Show network configuration
net show config

# Show all interface settings
net show hostname
net show dns
```

### NTP Configuration

```bash
# Show current NTP settings
ntp status
ntp show

# Add NTP server
ntp add timesever <ntp_server_ip>

# Enable/disable NTP
ntp enable
ntp disable
```

### SNMP & Alerting Configuration

```bash
# Show SNMP configuration
snmp show config

# Show alert notification config
alerts notify-list show
```

### Syslog Configuration

```bash
# Show syslog configuration
log show config

# Forward logs to syslog server (via GUI or config file)
# Admintools → Maintenance → Syslog
```

### Pre-Change Config Capture

Before any change, capture current state:

```bash
config backup create
system show version
net show config
filesys show compression
replication show all
```

### Common Issues

| Issue | Check | Action |
|---|---|---|
| Config backup fails | Disk space | Check `filesys show space` |
| Restore fails | Backup name typo | Run `config backup list` first |
| NTP drift | NTP server unreachable | Check network and NTP config |

---

## DDBoost

DDBoost (Dell Data Domain Boost) offloads deduplication processing to the backup client, reducing network traffic and improving backup performance. It is used by NetBackup, Networker, Avamar, Veeam, and other backup applications.

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

# Create with MTree path
ddboost storage-unit create <name> --user <ddboost_user>

# Delete a storage unit
ddboost storage-unit delete <storage_unit_name>

# Storage unit usage and quota
ddboost storage-unit show <name> --verbose
```

### Users

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

### Performance and Throughput

```bash
# DDBoost throughput statistics
ddboost show stats

# Connection statistics per client
ddboost show clients --verbose | grep -E "host|throughput|bytes"
```

### Distributed Segment Processing (DSP)

DSP moves deduplication to the client side, reducing network load:

```bash
# DSP status
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
| Client not in list | Wrong hostname or not connected | `ddboost show clients` |

---

## Diagnostics

### Log Access

```bash
# View system log (most recent events)
log view

# List available log files
log list

# Dump the full system log to stdout
log dump system

# Follow the log in real time
log watch

# Specific log file
log view <log_filename>
```

### Support Bundle

Support bundles collect all logs and diagnostics for TAC cases:

```bash
# Create a support bundle
support bundle create

# List available bundles
support bundle show

# Export bundle to remote server (SCP)
support bundle export scp://user@host:/path/bundle.tar.gz

# Export bundle to FTP
support bundle export ftp://user:pass@host/path/
```

### System Shell (ddsh)

`ddsh` provides a Unix-like shell with additional diagnostic tools:

```bash
# Enter the diagnostic shell
ddsh

# Inside ddsh:
diagnose all             # full system diagnostic run
iostat 1 10              # I/O statistics (1s interval, 10 iterations)
vmstat 1 10              # Virtual memory and CPU stats
netstat -an              # Active network connections
df -h                    # Filesystem usage
top                      # Process list
```

### Network Diagnostics

```bash
# Ping from the Data Domain
net ping <ip>

# Traceroute
net traceroute <ip>

# Interface error counters
net show stats | grep -i error
```

### Hardware Diagnostics

```bash
# Overall health check (hardware + software)
health check show

# Disk health
disk show state
disk show detail | grep -E "error|sector"

# Enclosure sensors (temperature, power, fan)
enclosure show hardware
```

### Performance Capture

```bash
# Inside ddsh — capture IOPS and throughput
iostat -x 1 30

# Filesystem stats snapshot
filesys show stats

# DDBoost throughput
ddboost show stats
```

### Alert History for TAC

```bash
# Export all current and historical alerts
alert show history > /tmp/alert_history.txt
support bundle create   # includes alert history automatically
```

---

## Disk & Storage

### Disk Status

```bash
# All disks with state (normal, unknown, suspect, failed)
disk show state

# Full hardware detail per disk
disk show hardware

# Disk performance statistics
disk show stats

# Disk error counts
disk show detail | grep -E "slot|error"
```

### Disk States

| State | Meaning | Action |
|---|---|---|
| `normal` | Healthy and in use | None |
| `spare` | Hot spare, available | None |
| `reconstructing` | Rebuilding RAID after failure | Monitor; do not remove disks |
| `failed` | Drive failure | Replace immediately |
| `unknown` | Newly inserted or not recognized | Check seating; may need `disk show hardware` to confirm |
| `absent` | Bay empty | Expected if slot unused |

### Enclosures and Shelves

```bash
# Enclosure hardware overview
enclosure show hardware

# All enclosures with status
enclosure show all

# Specific enclosure
enclosure show hardware enclosure <enc_id>
```

### Tier Management

Data Domain supports tiering to object storage (Cloud Tier) or tape:

```bash
# List all tiers (active, cloud)
tier list

# Detail on each tier (capacity, compression, usage)
tier show detail

# Cloud tier configuration (if licensed)
tier show detail cloud
```

### RAID Group Status

```bash
# RAID group state and disk members
raid show all
raid show detail

# RAID rebuilding progress (after disk replacement)
raid show detail | grep -E "Rebuilding|Complete"
```

### Replacing a Failed Disk

1. Identify the failed disk slot:
   ```bash
   disk show state | grep failed
   ```
2. Note the enclosure and slot number.
3. Physically replace the disk.
4. Verify the system picks up the new disk:
   ```bash
   disk show state
   ```
5. Monitor RAID rebuild:
   ```bash
   raid show detail | grep -i rebuild
   ```

### Capacity Summary

```bash
# Filesystem space usage
filesys show space

# Compressed vs logical usage
filesys show compression summary

# Tier capacity breakdown
tier show detail
```

---

## File Sharing (NFS & CIFS/SMB)

### NFS

Data Domain exports MTrees over NFS for backup applications that use the filesystem protocol (e.g., Networker, some Veeam configurations).

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

# Modify export options (root squash, read-write)
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
| `sync` | Synchronous writes — safer but slower |
| `async` | Asynchronous writes — faster but risk on crash |

### CIFS / SMB

```bash
# CIFS service status and configuration
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

#### CIFS Share Options

```bash
# Restrict share access to specific AD groups
cifs share modify <share_name> add-writable-users <DOMAIN>\<group>

# View share permissions
cifs share show <share_name>
```

### NFS + CIFS Dual Protocol

An MTree can be exported over both NFS and CIFS simultaneously for mixed environments. Ensure access controls are configured on both protocols to avoid permission conflicts.

### NFS/CIFS Troubleshooting

| Issue | Check | Command |
|---|---|---|
| NFS mount fails | Export exists for client IP? | `nfs show exports` |
| Access denied on mount | `no-root-squash` needed? | `nfs modify export ... options no-root-squash` |
| CIFS share not visible | CIFS enabled? | `cifs show` |
| Slow NFS backup | `async` option enabled? | `nfs show exports` → check options |

---

## Filesystem

The Data Domain filesystem (DDFS) manages all deduplication and compression. All user data lives in the active tier under `/data/col1/`.

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

Cleaning reclaims space from deleted or expired files. It runs automatically but can be triggered manually:

```bash
# Start a cleaning cycle
filesys clean start

# Show cleaning status
filesys clean status

# Stop an in-progress clean
filesys clean stop
```

Cleaning is I/O intensive. Schedule during off-peak hours if running manually.

### Capacity and Compression Analysis

```bash
# Overall capacity summary
filesys show space

# Compression ratio and savings
filesys show compression summary

# Per-MTree compression
filesys show compression | grep -A5 "mtree"

# Logical vs physical usage
filesys show space | grep -E "Used|Available|Total"
```

### Compression Ratio Fields

| Field | Meaning |
|---|---|
| Pre-comp | Total logical data written (before dedup/compression) |
| Post-comp | Physical space used on disk |
| Global comp factor | Overall compression ratio |
| Local comp factor | Per-stream compression ratio |
| Dedup savings | Percentage saved by deduplication |

### Space Recovery Actions

```bash
# Expire old backup data (via backup application policy — not DD CLI)
# Data Domain only deletes data when the backup app marks it expired

# After deletions, run cleaning to reclaim space
filesys clean start

# Monitor reclaim progress
filesys clean status
filesys show space   # compare before/after
```

### Filesystem Checks

```bash
# Check filesystem integrity
filesys check

# View filesystem event log
filesys show log
```

---

## MTrees (Data Management Units)

MTrees are logical partitions of the Data Domain filesystem. Each MTree has its own quota, replication, and retention settings. All backup data lives under `/data/col1/`.

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

```bash
# Enable retention lock on an MTree
mtree retention-lock enable mode enterprise /data/col1/<mtree_name>

# Set minimum/maximum retention period
mtree retention-lock set min-retention-period 30days /data/col1/<mtree_name>
mtree retention-lock set max-retention-period 7years /data/col1/<mtree_name>

# View retention lock settings
mtree retention-lock status /data/col1/<mtree_name>
```

### MTree Replication

```bash
# Add an MTree as a replication source (see replication CLI ref for full setup)
replication add source mtree://<src_host>/data/col1/<mtree_name> destination mtree://<dst_host>/data/col1/<mtree_name>

# View replication contexts for this MTree
replication show all | grep <mtree_name>
```

### Capacity Summary

```bash
# Space used by each MTree
mtree list --verbose | grep -E "name|pre-comp|post-comp|quota"

# Compare pre-compression vs post-compression (dedup savings)
filesys show compression | grep -A5 "mtree"
```

### Common Operations Table

| Task | Command |
|---|---|
| Create MTree | `mtree create /data/col1/<name>` |
| Set hard quota | `mtree quota set hard-limit <size> TiB /data/col1/<name>` |
| View quotas | `mtree quota show` |
| Delete MTree | `mtree delete /data/col1/<name>` |
| Enable retention lock | `mtree retention-lock enable mode enterprise /data/col1/<name>` |

---

## Network

Network commands manage the Data Domain's IP interfaces, routing, DNS, and NTP configuration. Correct networking is essential — backup clients need to reach the appliance, and replication requires connectivity to the remote Data Domain.

### Interface Status

```bash
# All interfaces — IP, speed, state
net show all

# Interface configuration (IP, netmask, MTU, bonding)
net show config

# Network settings summary
net show settings

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
# Hosts file entries
net hosts show

# Add a static host entry
net config hosts add <ip_address> <hostname>

# DNS server configuration
net show settings | grep -i dns
```

### NTP

```bash
# NTP server list
ntp show

# NTP sync status
ntp status

# Add NTP server
ntp add timeserver <ntp_ip>

# Remove NTP server
ntp del timeserver <ntp_ip>
```

### Ping and Connectivity Testing

```bash
# Ping from Data Domain
net ping <destination_ip>
net ping <destination_ip> count 10

# Traceroute
net traceroute <destination_ip>
```

### Bonding / LACP

```bash
# Show bonding configuration
net config bond show

# Create a bond
net config bond create bond0 <eth1> <eth2> lacp
```

### Firewall

```bash
# Show open ports and firewall rules
net config firewall show
```

---

## Replication

Data Domain replication runs at the MTree level and uses a source-destination model. Both systems must have network connectivity and matching software versions.

### Status Overview

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
# Add MTree-level replication (directional — source to destination)
replication add source mtree://<src_host>/data/col1/<mtree_name> \
    destination mtree://<dst_host>/data/col1/<mtree_name>

# Initialize replication (first sync — can take hours for large datasets)
replication initialize <context_id>
```

### Ongoing Operations

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

### Monitoring Replication Lag

```bash
# Lag in bytes (amount of data not yet replicated)
replication show stats | grep lag

# Lag in time
replication status | grep -E "context|lag"
```

### Failover (Passive Site Activation)

Run on the **destination** Data Domain when primary is unavailable:

```bash
# Break the context (makes destination writeable)
replication failover <context_id>
```

After failover, configure backup applications to point to the destination system.

### Re-establishing Replication After Failover

```bash
# Step 1 — resync (when primary recovers)
replication resync <context_id>

# Step 2 — confirm sync complete
replication status
replication show stats | grep lag

# Step 3 — failback: swap source/destination roles
# (requires breaking and recreating context in reverse)
```

### Replication Certificates

```bash
# Trust a remote DD (exchange certs — required for encrypted replication)
replication add source ... --encryption aes128
admintool certify <remote_dd_hostname>
```

### Replication Troubleshooting

| Issue | Check | Command |
|---|---|---|
| Context stuck in error | Alert detail | `alert show current` |
| High lag | Network bandwidth or congestion | `replication show stats` → bytes/sec |
| Initialization stalled | Filesystem busy | `filesys show stats` on both systems |
| No data replicating | Context disabled | `replication show all` → state |

---

## System Status

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

### Software and Licensing

```bash
# Show installed software packages
system software version show

# License status
elicense show
```

### Power and Environment

```bash
# Power supply status
enclosure show hardware | grep -i power

# Fan status
enclosure show hardware | grep -i fan

# Temperature sensors
enclosure show hardware | grep -i temp
```

### System Time and NTP

```bash
# Current time
ntp status

# NTP servers configured
ntp show

# Add NTP server
ntp add timeserver <ntp_ip>
```

### Rebooting and Shutdown

```bash
# Safe shutdown (completes in-progress operations)
system shutdown

# Restart the DDOS software (not a full reboot)
system restart

# Full reboot
system reboot
```

### Support Bundle

```bash
# Create a support bundle (for TAC cases)
support bundle create

# List available bundles
support bundle show

# Transfer to external server
support bundle export scp://user@host:/path/bundle.tar.gz
```

---

## Users & Security

### Local Users

```bash
# List all local users
user list

# User detail (role, last login)
user show <username>

# Add a local user
user add <username>

# Change a user's password
user change password <username>

# Delete a user
user del <username>
```

### User Roles

| Role | Permissions |
|---|---|
| `admin` | Full administrative access |
| `user` | Limited — can view, change own password |
| `backup-operator` | DDBoost access; cannot manage system settings |
| `none` | Disabled account |

```bash
# Show available roles
user role show

# List all roles
role list

# Assign a role to a user
user modify <username> --role <role_name>
```

### Authentication Settings

```bash
# Show authentication configuration (local, LDAP, AD)
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
# View password policy
user password-policy show

# Set minimum password length
user password-policy set min-length 12

# Set maximum password age (days)
user password-policy set max-age 90
```

### SSH Keys

```bash
# Show authorized SSH keys for a user
user ssh-keys show <username>

# Add an SSH public key
user ssh-keys add <username> key "<public_key_string>"

# Remove an SSH key
user ssh-keys del <username> key <key_id>
```

### Login and Session Management

```bash
# Active login sessions
user login show

# Terminate a specific session
user login terminate <session_id>
```

### Audit Log

```bash
# View authentication audit log
log view | grep -i "login\|auth\|failed"

# Export audit events
log dump system | grep -i auth
```
