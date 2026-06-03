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

```text
┌─────────────────────────────────── Dell Data Domain CLI Reference ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       DDOS CLI accessed via SSH (admin user); all commands under hierarchical namespaces      │   │
│   │             Tab completion available; "help <command>" or "<command> ?" for syntax            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Filesystem         │  │         Replication         │  │         System Admin        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │      filesys show space     │  │     replication show all    │  │        sysadmin show        │   │
│   │     filesys show status     │  │      replication resync     │  │     system show version     │   │
│   │          mtree list         │  │     replication throttle    │  │      net show hostname      │   │
│   │       mtree show quota      │  │       replication sync      │  │         alerts show         │   │
│   │     filesys clean start     │  │     replication show lag    │  │     support bundle save     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             filesys show space          — show total, used, available, dedup ratio            │   │
│   │             replication show all        — show all replication contexts and state             │   │
│   │               mtree list                  — list all MTrees with usage and quota              │   │
│   │            filesys clean start         — manually start cleaning (garbage collect)            │   │
│   │              support bundle save <path>  — collect diagnostic bundle for support              │   │
│   │                   system passphrase change     — change local admin password                  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    filesys clean  = DDOS cleaning cycle; reclaims space from expired/deleted backup segments          │
│    replication lag= Time delta between primary last write and replica last received                   │
│    support bundle = tar.gz of DDOS logs, config, and diagnostics; send to Dell support                │
│    mtree quota    = Logical soft/hard limit per MTree; shown in filesys show space output             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Show SNMP configuration
snmp show config

# Show alert notification config
alerts notify-list show
```
```bash
# Show syslog configuration
log show config

# Forward logs to syslog server (via GUI or config file)
# Admintools → Maintenance → Syslog
```
```bash
config backup create
system show version
net show config
filesys show compression
replication show all
```
```bash
# DDBoost service status and connection count
ddboost status

# Active client connections
ddboost show clients
ddboost show clients --verbose
```
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
```bash
# DDBoost throughput statistics
ddboost show stats

# Connection statistics per client
ddboost show clients --verbose | grep -E "host|throughput|bytes"
```
```bash
# DSP status
ddboost option show | grep -i "dist-seg"

# Enable DSP
ddboost option set distributed-segment-processing enabled
```
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
```bash
# Ping from the Data Domain
net ping <ip>

# Traceroute
net traceroute <ip>

# Interface error counters
net show stats | grep -i error
```
```bash
# Overall health check (hardware + software)
health check show

# Disk health
disk show state
disk show detail | grep -E "error|sector"

# Enclosure sensors (temperature, power, fan)
enclosure show hardware
```
```bash
# Inside ddsh — capture IOPS and throughput
iostat -x 1 30

# Filesystem stats snapshot
filesys show stats

# DDBoost throughput
ddboost show stats
```
```bash
# Export all current and historical alerts
alert show history > /tmp/alert_history.txt
support bundle create   # includes alert history automatically
```
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
```bash
# Enclosure hardware overview
enclosure show hardware

# All enclosures with status
enclosure show all

# Specific enclosure
enclosure show hardware enclosure <enc_id>
```
```bash
# List all tiers (active, cloud)
tier list

# Detail on each tier (capacity, compression, usage)
tier show detail

# Cloud tier configuration (if licensed)
tier show detail cloud
```
```bash
# RAID group state and disk members
raid show all
raid show detail

# RAID rebuilding progress (after disk replacement)
raid show detail | grep -E "Rebuilding|Complete"
```
```bash
# Filesystem space usage
filesys show space

# Compressed vs logical usage
filesys show compression summary

# Tier capacity breakdown
tier show detail
```
```bash
# List all NFS exports
nfs show exports

# NFS service status
nfs status

# NFS client connections
nfs show clients
```
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
```bash
# Restrict share access to specific AD groups
cifs share modify <share_name> add-writable-users <DOMAIN>\<group>

# View share permissions
cifs share show <share_name>
```
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
```bash
# Enable the filesystem (required before accepting backup data)
filesys enable

# Disable the filesystem (maintenance only — stops all I/O)
filesys disable
```
```bash
# Start a cleaning cycle
filesys clean start

# Show cleaning status
filesys clean status

# Stop an in-progress clean
filesys clean stop
```
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
```bash
# Expire old backup data (via backup application policy — not DD CLI)
# Data Domain only deletes data when the backup app marks it expired

# After deletions, run cleaning to reclaim space
filesys clean start

# Monitor reclaim progress
filesys clean status
filesys show space   # compare before/after
```
```bash
# Check filesystem integrity
filesys check

# View filesystem event log
filesys show log
```
```bash
# List all MTrees
mtree list

# Detail for a specific MTree
mtree show /data/col1/<mtree_name>

# All MTrees with usage stats
mtree list --verbose
```
```bash
# Create an MTree
mtree create /data/col1/<mtree_name>

# Delete an MTree (must be empty or use force)
mtree delete /data/col1/<mtree_name>
```
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
```bash
# Enable retention lock on an MTree
mtree retention-lock enable mode enterprise /data/col1/<mtree_name>

# Set minimum/maximum retention period
mtree retention-lock set min-retention-period 30days /data/col1/<mtree_name>
mtree retention-lock set max-retention-period 7years /data/col1/<mtree_name>

# View retention lock settings
mtree retention-lock status /data/col1/<mtree_name>
```
```bash
# Add an MTree as a replication source (see replication CLI ref for full setup)
replication add source mtree://<src_host>/data/col1/<mtree_name> destination mtree://<dst_host>/data/col1/<mtree_name>

# View replication contexts for this MTree
replication show all | grep <mtree_name>
```
```bash
# Space used by each MTree
mtree list --verbose | grep -E "name|pre-comp|post-comp|quota"

# Compare pre-compression vs post-compression (dedup savings)
filesys show compression | grep -A5 "mtree"
```
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
```bash
# Configure an interface IP
net config eth1 <ip_address> netmask <mask>

# Bring an interface up or down
net enable eth1
net disable eth1
```
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
```bash
# Hosts file entries
net hosts show

# Add a static host entry
net config hosts add <ip_address> <hostname>

# DNS server configuration
net show settings | grep -i dns
```
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
```bash
# Ping from Data Domain
net ping <destination_ip>
net ping <destination_ip> count 10

# Traceroute
net traceroute <destination_ip>
```
```bash
# Show bonding configuration
net config bond show

# Create a bond
net config bond create bond0 <eth1> <eth2> lacp
```
```bash
# Show open ports and firewall rules
net config firewall show
```
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
```bash
# Add MTree-level replication (directional — source to destination)
replication add source mtree://<src_host>/data/col1/<mtree_name> \
    destination mtree://<dst_host>/data/col1/<mtree_name>

# Initialize replication (first sync — can take hours for large datasets)
replication initialize <context_id>
```
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
```bash
# Lag in bytes (amount of data not yet replicated)
replication show stats | grep lag

# Lag in time
replication status | grep -E "context|lag"
```
```bash
# Break the context (makes destination writeable)
replication failover <context_id>
```
```bash
# Step 1 — resync (when primary recovers)
replication resync <context_id>

# Step 2 — confirm sync complete
replication status
replication show stats | grep lag

# Step 3 — failback: swap source/destination roles
# (requires breaking and recreating context in reverse)
```
```bash
# Trust a remote DD (exchange certs — required for encrypted replication)
replication add source ... --encryption aes128
admintool certify <remote_dd_hostname>
```
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
```bash
# Show installed software packages
system software version show

# License status
elicense show
```
```bash
# Power supply status
enclosure show hardware | grep -i power

# Fan status
enclosure show hardware | grep -i fan

# Temperature sensors
enclosure show hardware | grep -i temp
```
```bash
# Current time
ntp status

# NTP servers configured
ntp show

# Add NTP server
ntp add timeserver <ntp_ip>
```
```bash
# Safe shutdown (completes in-progress operations)
system shutdown

# Restart the DDOS software (not a full reboot)
system restart

# Full reboot
system reboot
```
```bash
# Create a support bundle (for TAC cases)
support bundle create

# List available bundles
support bundle show

# Transfer to external server
support bundle export scp://user@host:/path/bundle.tar.gz
```
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
```bash
# Show available roles
user role show

# List all roles
role list

# Assign a role to a user
user modify <username> --role <role_name>
```
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
```bash
# View password policy
user password-policy show

# Set minimum password length
user password-policy set min-length 12

# Set maximum password age (days)
user password-policy set max-age 90
```
```bash
# Show authorized SSH keys for a user
user ssh-keys show <username>

# Add an SSH public key
user ssh-keys add <username> key "<public_key_string>"

# Remove an SSH key
user ssh-keys del <username> key <key_id>
```
```bash
# Active login sessions
user login show

# Terminate a specific session
user login terminate <session_id>
```
```bash
# View authentication audit log
log view | grep -i "login\|auth\|failed"

# Export audit events
log dump system | grep -i auth
```
