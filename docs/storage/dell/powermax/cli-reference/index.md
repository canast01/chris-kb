# Dell PowerMax CLI Reference (SYMCLI)

Commonly used Solutions Enabler (SYMCLI) commands for managing Dell PowerMax and VMAX arrays.

> All commands require `-sid <SymmID>` to target a specific array. Run `symcfg list` first to identify the SID.

---

## Discovery & Array Info

```bash
# List all known arrays
symcfg list
symcfg discover
symcfg -sid <sid> list -v
symcfg -sid <sid> show

# Directors and ports
symcfg -sid <sid> list -dir all
symcfg -sid <sid> list -port all

# Cache and memory
symcfg -sid <sid> list -cache
symcfg -sid <sid> list -pool -all
```

---

## Devices

```bash
# List devices
symdev list -sid <sid>
symdev list -sid <sid> -v
symdev list -sid <sid> -assigned
symdev list -sid <sid> -unassigned
symdev list -sid <sid> -mapped
symdev list -sid <sid> -spare
symdev list -sid <sid> -failed
symdev list -sid <sid> -tdev

# Device details
symdev show <devname> -sid <sid>
symdev show <devname> -sid <sid> -v

# Device performance
symdev list -sid <sid> -perf
```

---

## Storage Groups

```bash
# List
symsg list -sid <sid>
symsg list -sid <sid> -v
symsg show <sg_name> -sid <sid>
symsg show <sg_name> -sid <sid> -v

# Create / delete
symsg create <sg_name> -sid <sid> -type regular
symsg create <sg_name> -sid <sid> -type parent
symsg delete <sg_name> -sid <sid>

# Add / remove devices
symsg -sid <sid> -sg <sg_name> add dev <devname>
symsg -sid <sid> -sg <sg_name> remove dev <devname>

# Add child SG to parent SG
symsg -sid <sid> -sg <parent_sg> add sg <child_sg>
symsg -sid <sid> -sg <parent_sg> remove sg <child_sg>

# Rename
symsg rename <old_sg> -new_sg_name <new_sg> -sid <sid>
```

---

## Masking Views & Access

```bash
# List masking views
symaccess list view -sid <sid>
symaccess show view <view_name> -sid <sid>

# Create / delete masking view
symaccess create view -name <view_name> -sg <sg_name> -pg <pg_name> -ig <ig_name> -sid <sid>
symaccess delete view -name <view_name> -sid <sid>

# Initiator Groups
symaccess list -sid <sid> -type initiator
symaccess show <ig_name> -sid <sid> -type initiator
symaccess create -name <ig_name> -type initiator -sid <sid>
symaccess delete -name <ig_name> -type initiator -sid <sid>
symaccess -sid <sid> -name <ig_name> -type initiator add devport -wwn <wwn>
symaccess -sid <sid> -name <ig_name> -type initiator remove devport -wwn <wwn>

# Port Groups
symaccess list -sid <sid> -type port
symaccess show <pg_name> -sid <sid> -type port
symaccess create -name <pg_name> -type port -sid <sid>
symaccess delete -name <pg_name> -type port -sid <sid>
symaccess -sid <sid> -name <pg_name> -type port add devport <dir>:<port>
symaccess -sid <sid> -name <pg_name> -type port remove devport <dir>:<port>

# Storage Groups in access context
symaccess list -sid <sid> -type storage

# Check host connectivity
symaccess -sid <sid> list logins -dirport <dir>:<port>
symaccess -sid <sid> -type initiator show <ig_name> -detail
```

---

## Ports

```bash
# List all ports
symport list -sid <sid>
symport list -sid <sid> -v
symport -sid <sid> -dir <dir> -p <port> show

# Fibre Channel login info
symport list -sid <sid> -logged_in
symport -sid <sid> -dir <dir> -p <port> list -logged_in
```

---

## SRDF — Replication

```bash
# List SRDF groups
symrdf -sid <sid> list
symrdf -sid <sid> -rdfg <rdfg_num> list
symrdf -sid <sid> -rdfg <rdfg_num> query

# Device group operations (requires a DG or SG)
symrdf -sid <sid> -sg <sg_name> query
symrdf -sid <sid> -sg <sg_name> establish
symrdf -sid <sid> -sg <sg_name> split
symrdf -sid <sid> -sg <sg_name> suspend
symrdf -sid <sid> -sg <sg_name> resume
symrdf -sid <sid> -sg <sg_name> update
symrdf -sid <sid> -sg <sg_name> failover
symrdf -sid <sid> -sg <sg_name> failback
symrdf -sid <sid> -sg <sg_name> swap
symrdf -sid <sid> -sg <sg_name> verify

# SRDF/A specific
symrdf -sid <sid> -sg <sg_name> query -srdf_a
symrdf -sid <sid> -rdfg <rdfg_num> verify -srdf_a

# SRDF cycle / lag info
symrdf -sid <sid> -rdfg <rdfg_num> list -v
```

---

## SnapVX — Snapshots

```bash
# List snapshots
symsnapvx list -sid <sid>
symsnapvx list -sid <sid> -sg <sg_name>
symsnapvx list -sid <sid> -sg <sg_name> -snapshot_name <snap_name>

# Create snapshot
symsnapvx -sid <sid> snap -sg <sg_name> -name <snap_name> establish

# Delete / terminate snapshot
symsnapvx -sid <sid> snap -sg <sg_name> -name <snap_name> terminate
symsnapvx -sid <sid> snap -sg <sg_name> -name <snap_name> terminate --force

# Link snapshot to target SG
symsnapvx -sid <sid> snap -sg <sg_name> -name <snap_name> link -lnsg <target_sg>
symsnapvx -sid <sid> snap -sg <sg_name> -name <snap_name> link -lnsg <target_sg> -copy

# Unlink
symsnapvx -sid <sid> snap -sg <sg_name> -name <snap_name> unlink -lnsg <target_sg>

# Restore
symsnapvx -sid <sid> snap -sg <sg_name> -name <snap_name> restore

# Rename snapshot
symsnapvx -sid <sid> snap -sg <sg_name> -name <snap_name> rename -new_name <new_snap_name>
```

---

## Physical Disks & Hardware

```bash
# Physical disks
sympd list -sid <sid>
sympd list -sid <sid> -failed
sympd list -sid <sid> -spare
sympd show <pd_name> -sid <sid>

# Disk groups
symdisk list -sid <sid>
symdisk list -sid <sid> -failed
symdisk list -sid <sid> -v

# Hardware status
symcfg -sid <sid> list -disk
symcfg -sid <sid> list -bay
```

---

## Performance & Statistics

```bash
# Storage group stats
symstat -sid <sid> list -type sg
symstat -sid <sid> list -type sg -sg <sg_name>

# Device stats
symstat -sid <sid> list -type dev

# Director stats
symstat -sid <sid> list -type dir

# Backend / disk stats
symstat -sid <sid> list -type be

# Cache stats
symstat -sid <sid> list -type cache

# Port stats
symstat -sid <sid> list -type port
```

---

## Events & Audit

```bash
# Events
symevent list -sid <sid>
symevent list -sid <sid> -v
symevent list -sid <sid> -start_time "01/01/2025 00:00:00"
symevent list -sid <sid> -start_time "01/01/2025 00:00:00" -end_time "01/02/2025 00:00:00"

# Audit log
symaudit list -sid <sid>
symaudit list -sid <sid> -v
symaudit list -sid <sid> -start_time "01/01/2025 00:00:00"
symaudit list -sid <sid> -user <username>
```

---

## Device Groups (Legacy / Scripting)

```bash
# Create and manage device groups
symdg list -sid <sid>
symdg show <dg_name> -sid <sid>
symdg create <dg_name> -type regular -sid <sid>
symdg delete <dg_name> -sid <sid>
symdg -g <dg_name> add dev <devname> -sid <sid>
symdg -g <dg_name> remove dev <devname> -sid <sid>
```
