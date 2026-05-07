# Dell Unity CLI Reference (Unisphere CLI)

Commonly used `uemcli` commands for managing Dell Unity storage systems. Unity is a dual-controller mid-range array supporting both block (SAN) and file (NAS) workloads.

> Connect with: `uemcli -d <array_ip> -u <user> -p <password>` — or set a connection profile to avoid retyping credentials.

---

## System & Status

These commands show you the overall health of the array — software version, active alerts, license status, and remote support connectivity. Start here when something seems wrong.

### System Information

```bash
# General system info — name, model, serial, software version
uemcli -d <ip> -u admin /sys/general show -detail

# Current system time
uemcli -d <ip> -u admin /sys/time show

# Software version and build
uemcli -d <ip> -u admin /sys/sw/version show
```

### Alerts and Events

```bash
# Active alerts (open, unresolved)
uemcli -d <ip> -u admin /prac/alert show

# Alert history
uemcli -d <ip> -u admin /prac/alert show -detail

# Syslog events
uemcli -d <ip> -u admin /event/syslog show

# Audit events (user actions)
uemcli -d <ip> -u admin /event/audit show
```

### Alert Severity Levels

| Severity | Meaning | Action |
|---|---|---|
| INFO | Informational | No action required |
| WARNING | Potential issue | Monitor |
| ERROR | Degraded functionality | Investigate |
| CRITICAL | Service impacting | Immediate response |

### Licenses and ESRS

```bash
# View installed licenses
uemcli -d <ip> -u admin /sys/lic show

# Check expiry on time-limited licenses
uemcli -d <ip> -u admin /sys/lic show -detail | grep -i expir

# ESRS (remote support) connectivity status
uemcli -d <ip> -u admin /sys/esrs show

# Enable ESRS
uemcli -d <ip> -u admin /sys/esrs set -enabled true

# Manual support call home
uemcli -d <ip> -u admin /sys/esrs callhome -type heartbeat
```

### SP Failover and Upgrade Status

```bash
# Move a resource (LUN or NAS server) to the other SP
uemcli -d <ip> -u admin /sys/sp/trespass set -res <resource_id> -sp <spa|spb>

# Check if an upgrade is in progress
uemcli -d <ip> -u admin /sys/sw show
```

### Hardware Health Summary

```bash
# Overall system health
uemcli -d <ip> -u admin /sys/general show -detail | grep -i health

# All hardware components
uemcli -d <ip> -u admin /sys/sp show -detail | grep -i health
uemcli -d <ip> -u admin /stor/config/disk show -detail | grep -i health
uemcli -d <ip> -u admin /stor/config/pool show -detail | grep -i health
```

---

## Storage Pools

A storage pool is a logical group of disk drives organized into RAID sets. LUNs and file systems are allocated from pools. You need at least one pool to provision storage.

### List Pools

```bash
# All pools (summary)
uemcli -d <ip> -u admin /stor/config/pool show

# Detailed — name, size, used, free, health, RAID type
uemcli -d <ip> -u admin /stor/config/pool show -detail

# Specific pool by ID
uemcli -d <ip> -u admin /stor/config/pool -id <pool_id> show -detail
```

### Capacity Thresholds

| Free Space | Action |
|---|---|
| > 30% | Healthy — no action |
| 20–30% | Monitor closely |
| 10–20% | Alert — plan expansion |
| < 10% | Emergency — add capacity immediately |

### Create a Pool

```bash
uemcli -d <ip> -u admin /stor/config/pool create \
    -name Production_Pool \
    -diskGroup dg_1 \
    -raidType RAID5 \
    -stripeWidth 5 \
    -descr "Primary production pool - SAS SSD"
```

### Expand a Pool

```bash
uemcli -d <ip> -u admin /stor/config/pool -id <pool_id> set \
    -addDiskGroup <dg_id>

# Verify size after expansion
uemcli -d <ip> -u admin /stor/config/pool -id <pool_id> show -detail | \
    grep -E "Size|Used|Free"
```

### Modify and Delete

```bash
# Rename a pool
uemcli -d <ip> -u admin /stor/config/pool -id <pool_id> set -name <new_name>

# Delete a pool (must be empty — no LUNs or file systems)
uemcli -d <ip> -u admin /stor/config/pool -id <pool_id> delete
```

### RAID Types

| RAID Type | Overhead | Protection | Use Case |
|---|---|---|---|
| RAID5 | 1 disk | 1 drive failure | General purpose SSD/SAS |
| RAID6 | 2 disks | 2 drive failures | High-capacity NL-SAS |
| RAID10 | 50% | 1 disk per mirrored pair | High IOPS workloads |

### Pool Health States

| State | Meaning | Action |
|---|---|---|
| OK | Healthy | None |
| Degraded | A disk group is degraded | Check disk health |
| Major | Significant degradation | Immediate investigation |
| Critical | Service impacting | Emergency response |

---

## LUNs

A LUN (Logical Unit Number) is a block storage volume — it appears to a server as a raw disk. Servers connect to LUNs via Fibre Channel or iSCSI. You create a LUN, then grant host access to it.

### List LUNs

```bash
uemcli -d <ip> /stor/config/lun show
uemcli -d <ip> /stor/config/lun show -detail
```

### Create / Expand / Rename / Delete

```bash
# Create a 100 GB LUN
uemcli -d <ip> /stor/config/lun create \
    -name <lun_name> \
    -pool <pool_id> \
    -size 100G

# Expand a LUN
uemcli -d <ip> /stor/config/lun -id <lun_id> set -size 200G

# Rename
uemcli -d <ip> /stor/config/lun -id <lun_id> set -name <new_name>

# Delete (ensure the LUN is unmasked from all hosts first)
uemcli -d <ip> /stor/config/lun -id <lun_id> delete
```

### LUN Host Access (Masking)

Masking controls which servers can see a LUN. Without masking, no server can access the LUN.

```bash
# Show host access for a LUN
uemcli -d <ip> /stor/config/lun -id <lun_id> show -detail

# Grant host access
uemcli -d <ip> /stor/config/lun -id <lun_id> set -hostAccess <host_id>:hlu=<hlu_id>
```

### LUN Snapshots

```bash
# List snapshots for a LUN
uemcli -d <ip> /prot/snap show -res <lun_id>

# Create a snapshot
uemcli -d <ip> /prot/snap create -name <snap_name> -res <lun_id>

# Restore a snapshot
uemcli -d <ip> /prot/snap -id <snap_id> restore

# Delete a snapshot
uemcli -d <ip> /prot/snap -id <snap_id> delete
```

### LUN Common Issues

| Issue | Check | Action |
|---|---|---|
| LUN not visible to host | Host masking | Set `-hostAccess` |
| LUN expand fails | Pool capacity | Check pool free space |
| Snapshot restore fails | Active I/O | Quiesce host I/O first |
| Delete fails | Active connections | Unmask from all hosts first |

---

## File Systems (NAS)

Unity can also serve as a NAS — sharing files over NFS (for Linux) and CIFS/SMB (for Windows). A NAS server is a logical container that holds file systems and protocols. Each NAS server runs on one SP but can be failed over to the other.

### NAS Servers

```bash
# List NAS servers
uemcli -d <ip> /net/nas/server show
uemcli -d <ip> /net/nas/server show -detail

# Create a NAS server
uemcli -d <ip> /net/nas/server create \
    -name <nas_name> \
    -sp <sp_id> \
    -pool <pool_id>
```

### File Systems

```bash
# List file systems
uemcli -d <ip> /stor/config/fs show
uemcli -d <ip> /stor/config/fs show -detail

# Create a file system
uemcli -d <ip> /stor/config/fs create \
    -name <fs_name> \
    -nasServer <nas_id> \
    -pool <pool_id> \
    -size 1T

# Resize
uemcli -d <ip> /stor/config/fs -id <fs_id> set -size 2T

# Delete
uemcli -d <ip> /stor/config/fs -id <fs_id> delete
```

### NFS Shares

```bash
# List NFS shares
uemcli -d <ip> /stor/config/nfs show

# Create an NFS share
uemcli -d <ip> /stor/config/nfs create -fs <fs_id> -path / -nfsVersion NFSv3

# Set host access
uemcli -d <ip> /stor/config/nfs -id <nfs_id> set -hostAccess "<ip>(rw)"

# Delete
uemcli -d <ip> /stor/config/nfs -id <nfs_id> delete
```

### CIFS Shares

```bash
# List CIFS shares
uemcli -d <ip> /stor/config/cifs show

# Create
uemcli -d <ip> /stor/config/cifs create -name <share_name> -fs <fs_id> -path /

# Delete
uemcli -d <ip> /stor/config/cifs -id <cifs_id> delete
```

### File System Snapshots

```bash
uemcli -d <ip> /prot/snap show -res <fs_id>
uemcli -d <ip> /prot/snap create -name <snap_name> -res <fs_id>
uemcli -d <ip> /prot/snap -id <snap_id> restore
uemcli -d <ip> /prot/snap -id <snap_id> delete
```

### File System Common Issues

| Issue | Check | Action |
|---|---|---|
| NFS mount fails | NFS share access | Set `-hostAccess` with correct IP |
| File system full | Capacity | Resize with `-size` |
| NAS server not responding | SP health | Check SP status in Unisphere |
| CIFS share inaccessible | AD join | Verify NAS server AD status |

---

## Hosts & Access

Hosts are the servers that connect to Unity storage. Each host has initiators — the HBA WWNs (for Fibre Channel) or IQNs (for iSCSI) that the server uses to log in to the SAN.

### Hosts

```bash
# List all hosts
uemcli -d <ip> -u admin /remote/host show

# Detailed host view — name, OS type, initiators, LUN access
uemcli -d <ip> -u admin /remote/host show -detail

# Create a host
uemcli -d <ip> -u admin /remote/host create \
    -name <hostname> \
    -type Initiator \
    -osType Linux
```

### Host OS Types

| OS Type | Value |
|---|---|
| Linux | `Linux` |
| Windows | `Windows` |
| VMware | `VMware` |
| AIX | `AIX` |

### Initiators

```bash
# List all initiators
uemcli -d <ip> -u admin /remote/initiator show
uemcli -d <ip> -u admin /remote/initiator show -detail

# Register a Fibre Channel initiator (WWN)
uemcli -d <ip> -u admin /remote/initiator create \
    -host <host_id> \
    -uid 20:00:00:90:fa:12:34:56 \
    -type FC

# Register an iSCSI initiator (IQN)
uemcli -d <ip> -u admin /remote/initiator create \
    -host <host_id> \
    -uid iqn.2024-01.com.example:host01 \
    -type iSCSI

# Delete an initiator
uemcli -d <ip> -u admin /remote/initiator -id <initiator_id> delete
```

### LUN Access Control (Masking)

```bash
# List all LUN access control entries
uemcli -d <ip> -u admin /stor/config/lunacl show

# Grant a host access to a LUN
uemcli -d <ip> -u admin /stor/config/lunacl create \
    -lun <lun_id> \
    -host <host_id> \
    -accessType production

# Revoke LUN access
uemcli -d <ip> -u admin /stor/config/lunacl -id <acl_id> delete
```

### End-to-End LUN Presentation

```bash
# Step 1 — create or identify host
uemcli -d <ip> -u admin /remote/host create -name server01 -type Initiator -osType Linux

# Step 2 — register initiators
uemcli -d <ip> -u admin /remote/initiator create -host <host_id> -uid <wwn> -type FC

# Step 3 — grant LUN access
uemcli -d <ip> -u admin /stor/config/lunacl create -lun <lun_id> -host <host_id>

# Step 4 — rescan HBAs on the host
# Linux: rescan-scsi-bus.sh or echo "- - -" > /sys/class/scsi_host/host*/scan
```

---

## Network Interfaces

Unity needs network interfaces for management traffic, iSCSI block access, and NAS file traffic. Each interface is bound to a specific SP (Storage Processor) and physical port.

```bash
# All network interfaces
uemcli -d <ip> -u admin /net/if show
uemcli -d <ip> -u admin /net/if show -detail
```

### Interface Types

| Type | Use |
|---|---|
| Management | Admin access to Unisphere UI and CLI |
| iSCSI | Block storage access over Ethernet |
| File | NAS NFS/SMB traffic |
| Replication | Inter-array replication traffic |

### Create / Modify / Delete Interfaces

```bash
# Create iSCSI interface on SPA, Ethernet port 0
uemcli -d <ip> -u admin /net/if create \
    -type iSCSI \
    -ipv4 <iscsi_ip> \
    -netmask <subnet_mask> \
    -gateway <gateway_ip> \
    -sp spa \
    -port <eth_port_id>

# Change IP address
uemcli -d <ip> -u admin /net/if -id <if_id> set -ipv4 <new_ip> -netmask <mask> -gateway <gw>

# Delete
uemcli -d <ip> -u admin /net/if -id <if_id> delete
```

### iSCSI Portals and Ethernet Ports

```bash
# List iSCSI nodes/portals
uemcli -d <ip> -u admin /net/iscsi/node show -detail

# List physical Ethernet ports
uemcli -d <ip> -u admin /net/port/eth show -detail

# FC ports
uemcli -d <ip> -u admin /net/port/fc show -detail
```

### Network Troubleshooting

| Issue | Check | Command |
|---|---|---|
| iSCSI initiator can't connect | Interface IP reachable? | `uemcli ... /net/if show -detail` |
| Wrong SP for interface | SP association | `uemcli ... /net/if show -detail | grep SP` |
| Interface down | Physical port state | `uemcli ... /net/port/eth show -detail` |

---

## Replication

Unity can replicate LUNs and file systems to a remote Unity array. Replication creates an exact copy at the destination and keeps it in sync according to your RPO (Recovery Point Objective).

### View Sessions

```bash
# List all replication sessions
uemcli -d <ip> -u admin /prot/rep/session show

# Detailed view — state, lag, source/destination resources
uemcli -d <ip> -u admin /prot/rep/session show -detail

# Specific session
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> show -detail
```

### Session States

| State | Meaning |
|---|---|
| Active | Replication running normally |
| Idle | No sync in progress |
| Syncing | Data transfer in progress |
| Paused | Manually suspended |
| Failed | Error — check alerts |
| Failed Over | DR site is now active |

### Pause, Resume, Sync, Failover

```bash
# Pause replication
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> pause

# Resume replication
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> resume

# Trigger an immediate sync
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> sync

# Planned failover with final sync (recommended)
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> failover -keepSync

# Emergency failover without sync
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> failover
```

### Failback

```bash
# Step 1 — reverse replication (DR becomes source)
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> reverse

# Step 2 — sync data back to primary
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> sync

# Step 3 — fail back to original primary
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> failback
```

### Replication Connections

```bash
# List connections (Unity ↔ Unity)
uemcli -d <ip> -u admin /prot/rep/connect show

# Create a replication connection
uemcli -d <ip> -u admin /prot/rep/connect create \
    -destAddress <destination_sp_ip> \
    -destUsername admin \
    -destPassword <password>

# Create a replication session (replicate a LUN)
uemcli -d <ip> -u admin /prot/rep/session create \
    -srcRes <lun_id> \
    -dstSys <connection_id> \
    -dstResName <remote_lun_name> \
    -rpo 3600   # RPO in seconds (3600 = 1 hour)
```

---

## Physical Disks & Hardware

These commands show you the health of the physical hardware inside the Unity array — drives, disk groups, storage processors, enclosures, power supplies, and batteries.

### Disks

```bash
# List all disks
uemcli -d <ip> -u admin /stor/config/disk show

# Detailed disk view — model, speed, capacity, health, location
uemcli -d <ip> -u admin /stor/config/disk show -detail

# Filter by health
uemcli -d <ip> -u admin /stor/config/disk show -detail | grep -i "health\|failed\|degraded"
```

### Disk Health States

| State | Meaning | Action |
|---|---|---|
| OK | Healthy | None |
| Degraded | Performance issue or predictive failure | Monitor closely |
| Failed | Drive has failed | Replace immediately |
| Faulted | Array has quarantined the disk | Replace |

### Disk Groups

```bash
# List disk groups (RAID sets)
uemcli -d <ip> -u admin /stor/config/dg show
uemcli -d <ip> -u admin /stor/config/dg show -detail

# Filter degraded disk groups
uemcli -d <ip> -u admin /stor/config/dg show -detail | grep -i degraded
```

### Storage Processors

```bash
# SP status (SPA and SPB)
uemcli -d <ip> -u admin /sys/sp show
uemcli -d <ip> -u admin /sys/sp show -detail
uemcli -d <ip> -u admin /sys/sp show -detail | grep -E "CPU|Memory|Health"
```

### Enclosures, Power, Fans, Batteries

```bash
uemcli -d <ip> -u admin /sys/encl show -detail
uemcli -d <ip> -u admin /sys/powersupply show
uemcli -d <ip> -u admin /sys/fan show

# BBU status (protects write cache on SP failure)
uemcli -d <ip> -u admin /sys/battery show -detail
```
