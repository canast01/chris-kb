# Dell Unity CLI Reference (Unisphere CLI)

Commonly used `uemcli` commands for managing Dell Unity storage systems.

> Connect with: `uemcli -d <array_ip> -u <user> -p <password>` or set a connection profile.

---

## System & Status

```bash
# System info
uemcli -d <ip> /sys/general show -detail
uemcli -d <ip> /sys/time show
uemcli -d <ip> /sys/sw/version show

# Alerts and events
uemcli -d <ip> /prac/alert show
uemcli -d <ip> /event/syslog show

# Licenses
uemcli -d <ip> /sys/lic show

# Support / ESRS
uemcli -d <ip> /sys/esrs show
```

---

## Storage Pools

```bash
# List pools
uemcli -d <ip> /stor/config/pool show
uemcli -d <ip> /stor/config/pool show -detail

# Create pool (RAID5 example)
uemcli -d <ip> /stor/config/pool create -name <pool_name> -diskGroup <dg_id> -raidType RAID5

# Modify pool
uemcli -d <ip> /stor/config/pool -id <pool_id> set -name <new_name>

# Delete pool
uemcli -d <ip> /stor/config/pool -id <pool_id> delete
```

---

## LUNs

```bash
# List LUNs
uemcli -d <ip> /stor/config/lun show
uemcli -d <ip> /stor/config/lun show -detail

# Create LUN
uemcli -d <ip> /stor/config/lun create -name <lun_name> -pool <pool_id> -size 100G

# Modify LUN
uemcli -d <ip> /stor/config/lun -id <lun_id> set -size 200G
uemcli -d <ip> /stor/config/lun -id <lun_id> set -name <new_name>

# Delete LUN
uemcli -d <ip> /stor/config/lun -id <lun_id> delete

# LUN snapshots
uemcli -d <ip> /prot/snap show -res <lun_id>
uemcli -d <ip> /prot/snap create -name <snap_name> -res <lun_id>
uemcli -d <ip> /prot/snap -id <snap_id> delete
uemcli -d <ip> /prot/snap -id <snap_id> restore
```

---

## File Systems (NAS)

```bash
# NAS servers
uemcli -d <ip> /net/nas/server show
uemcli -d <ip> /net/nas/server show -detail
uemcli -d <ip> /net/nas/server create -name <nas_name> -sp <sp_id> -pool <pool_id>

# File systems
uemcli -d <ip> /stor/config/fs show
uemcli -d <ip> /stor/config/fs show -detail
uemcli -d <ip> /stor/config/fs create -name <fs_name> -nasServer <nas_id> -pool <pool_id> -size 1T
uemcli -d <ip> /stor/config/fs -id <fs_id> set -size 2T
uemcli -d <ip> /stor/config/fs -id <fs_id> delete

# NFS shares
uemcli -d <ip> /stor/config/nfs show
uemcli -d <ip> /stor/config/nfs create -fs <fs_id> -path / -nfsVersion NFSv3
uemcli -d <ip> /stor/config/nfs -id <nfs_id> set -hostAccess "<ip>(rw)"
uemcli -d <ip> /stor/config/nfs -id <nfs_id> delete

# CIFS shares
uemcli -d <ip> /stor/config/cifs show
uemcli -d <ip> /stor/config/cifs create -name <share_name> -fs <fs_id> -path /
uemcli -d <ip> /stor/config/cifs -id <cifs_id> delete
```

---

## Hosts & Access

```bash
# Hosts
uemcli -d <ip> /remote/host show
uemcli -d <ip> /remote/host show -detail
uemcli -d <ip> /remote/host create -name <host_name> -type Initiator

# Initiators
uemcli -d <ip> /remote/initiator show
uemcli -d <ip> /remote/initiator create -host <host_id> -uid <wwn_or_iqn> -type FC

# LUN access (host-to-LUN mapping)
uemcli -d <ip> /stor/config/lunacl show
uemcli -d <ip> /stor/config/lunacl create -lun <lun_id> -host <host_id>
uemcli -d <ip> /stor/config/lunacl -id <acl_id> delete
```

---

## Network Interfaces

```bash
# Interfaces
uemcli -d <ip> /net/if show
uemcli -d <ip> /net/if show -detail

# Create iSCSI interface
uemcli -d <ip> /net/if create -type iSCSI -ipv4 <ip> -netmask <mask> -gateway <gw> -sp <sp_id> -port <port_id>

# iSCSI portals
uemcli -d <ip> /net/iscsi/node show
```

---

## Replication

```bash
# Replication sessions
uemcli -d <ip> /prot/rep/session show
uemcli -d <ip> /prot/rep/session show -detail

# Pause / resume
uemcli -d <ip> /prot/rep/session -id <session_id> pause
uemcli -d <ip> /prot/rep/session -id <session_id> resume

# Failover
uemcli -d <ip> /prot/rep/session -id <session_id> failover -keepSync

# Sync
uemcli -d <ip> /prot/rep/session -id <session_id> sync
```

---

## Physical Disks & Hardware

```bash
# Disks
uemcli -d <ip> /stor/config/disk show
uemcli -d <ip> /stor/config/disk show -detail

# Disk groups
uemcli -d <ip> /stor/config/dg show
uemcli -d <ip> /stor/config/dg show -detail

# Storage processors
uemcli -d <ip> /sys/sp show
uemcli -d <ip> /sys/sp show -detail
```
