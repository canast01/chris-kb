# Dell PowerScale (Isilon) CLI Reference

Commonly used `isi` commands for managing Dell PowerScale (formerly Isilon) scale-out NAS clusters.

> Commands run from the cluster CLI. Use `isi --help` or `isi <subcommand> --help` for full option lists.

---

## Cluster Status & Identity

```bash
# Cluster identity and version
isi version
isi status
isi cluster identity view
isi cluster config view

# Node list and status
isi node list
isi node view <node_id>
isi status -n <node_id>

# Cluster statistics summary
isi statistics cluster list
isi statistics drive list
```

---

## Nodes

```bash
# List nodes
isi node list
isi node view <node_id>

# Node hardware details
isi node hardware view <node_id>

# Node drives
isi node drives list <node_id>
isi node drives view <node_id> <bay>

# Node sensors
isi node sensors view <node_id>

# Smartfail / readd a node
isi devices smartfail -d <node_id>
isi devices add -d <node_id>
```

---

## Storage Pools & Tiers

```bash
# Storage pools
isi storagepool nodepools list
isi storagepool nodepools view <pool_name>
isi storagepool tiers list
isi storagepool tiers view <tier_name>

# File pool policies
isi filepool policies list
isi filepool policies view <policy_name>
isi filepool default-policy view

# SmartPools status
isi job status | grep -i pool
```

---

## File System — Directories & Quotas

```bash
# Browse
ls /ifs/
ls -la /ifs/<path>

# Directory info
isi get /ifs/<path>
isi get -D /ifs/<path>

# Create directory
mkdir -p /ifs/<path>

# Permissions
chmod 755 /ifs/<path>
chown <user>:<group> /ifs/<path>
isi get -a /ifs/<path>
```

---

## Quotas

```bash
# List quotas
isi quota quotas list
isi quota quotas list --type directory
isi quota quotas list --path /ifs/<path>

# View quota details
isi quota quotas view --path /ifs/<path> --type directory

# Create quota
isi quota quotas create /ifs/<path> directory --hard-threshold <size>G --soft-threshold <size>G --advisory-threshold <size>G

# Modify quota
isi quota quotas modify --path /ifs/<path> --type directory --hard-threshold <size>G

# Delete quota
isi quota quotas delete --path /ifs/<path> --type directory

# Quota reports
isi quota reports list
isi quota reports create
```

---

## NFS Exports

```bash
# List exports
isi nfs exports list
isi nfs exports view <export_id>

# Create export
isi nfs exports create /ifs/<path> --clients <ip_or_cidr> --read-write-clients <ip_or_cidr> --root-clients <ip_or_cidr>

# Modify export
isi nfs exports modify <export_id> --addroot-clients <ip>
isi nfs exports modify <export_id> --read-write-clients <ip>

# Delete export
isi nfs exports delete <export_id>

# Reload / check NFS
isi nfs exports check
isi nfs settings global view
isi nfs settings export view
```

---

## SMB Shares

```bash
# List shares
isi smb shares list
isi smb shares view <share_name>

# Create share
isi smb shares create <share_name> /ifs/<path>

# Modify share
isi smb shares modify <share_name> --description "<text>"

# Delete share
isi smb shares delete <share_name>

# Share permissions
isi smb shares permission list <share_name>
isi smb shares permission create <share_name> --authority <domain\\user> --permission-type allow --permission full

# SMB settings
isi smb settings global view
isi smb settings service view

# Sessions
isi smb sessions list
```

---

## Network

```bash
# Interfaces
isi network interfaces list
isi network interfaces view <iface>

# Subnets
isi network subnets list
isi network subnets view <subnet_name>

# IP pools
isi network pools list
isi network pools view <pool_name>
isi network pools create --name <pool> --subnet <subnet> --access-zone <zone>

# Rules (SmartConnect)
isi network rules list
isi network rules view <rule_name>

# DNS
isi network dns view
isi network external settings view

# Ping / connectivity
ping <ip>
isi network interfaces list --node-id <node_id>
```

---

## Access Zones

```bash
# List zones
isi zone zones list
isi zone zones view <zone_name>

# Create / delete zone
isi zone zones create <zone_name> --path /ifs/<path>
isi zone zones delete <zone_name>

# Modify zone
isi zone zones modify <zone_name> --add-auth-providers <provider>
```

---

## Authentication & Users

```bash
# Auth providers
isi auth providers list
isi auth providers ad list
isi auth providers ad view <provider_name>

# Join AD domain
isi auth ads create --name <domain> --user <admin_user> --password <password>

# Local users and groups
isi auth users list
isi auth users view <username>
isi auth users create --name <username> --password <password>
isi auth users delete <username>
isi auth groups list
isi auth groups view <group_name>

# Map rules
isi auth mappings rules list
```

---

## Snapshots

```bash
# List snapshots
isi snapshot snapshots list
isi snapshot snapshots view <snap_id>

# Create snapshot
isi snapshot snapshots create /ifs/<path> --name <snap_name>

# Delete snapshot
isi snapshot snapshots delete <snap_id>
isi snapshot snapshots delete --path /ifs/<path> --name <snap_name>

# Restore (copy back from snapshot)
cp -a /ifs/.snapshot/<snap_name>/<path>/* /ifs/<path>/

# Snapshot schedules
isi snapshot schedules list
isi snapshot schedules view <schedule_name>
isi snapshot schedules create <schedule_name> /ifs/<path> <frequency>

# Snapshot aliases
isi snapshot aliases list
```

---

## SyncIQ — Replication

```bash
# List policies
isi sync policies list
isi sync policies view <policy_name>

# Create policy
isi sync policies create --name <policy_name> --action sync --source-root-path /ifs/<src> --target-host <ip> --target-path /ifs/<dst>

# Run / pause / cancel
isi sync jobs list
isi sync jobs start <policy_name>
isi sync jobs pause <policy_name>
isi sync jobs cancel <policy_name>

# View job progress
isi sync jobs view <job_id>

# Reports
isi sync reports list
isi sync reports view <report_id>

# Performance rules
isi sync rules list
isi sync rules create bandwidth --limit <kbps> --schedule always

# Failover / failback
isi sync policies disable <policy_name>
isi sync recover policies list
```

---

## Jobs (Background Tasks)

```bash
# List running jobs
isi job status
isi job jobs list
isi job jobs view <job_id>

# Job types
isi job types list
isi job types view <type_name>

# Start / cancel a job
isi job jobs start <type_name>
isi job jobs cancel <job_id>

# Job history
isi job history list
isi job events list
```

---

## Performance & Statistics

```bash
# Live cluster stats
isi statistics system list
isi statistics client list
isi statistics protocol list

# Protocol breakdown
isi statistics protocol list --protocol nfs3
isi statistics protocol list --protocol smb2

# Drive stats
isi statistics drive list

# Node-level stats
isi statistics node list
isi statistics node list --node-id <node_id>

# Throughput and IOPS
isi statistics query current --stats node.clientstats.active.nfs

# Performance history
isi statistics history list
```

---

## Events & Alerts

```bash
# View events
isi event events list
isi event events list --severity critical
isi event events list --start-time <YYYY-MM-DD>

# Acknowledge / resolve events
isi event events resolve <event_id>

# Alert channels
isi event channels list
isi event channels view <channel_name>

# SNMP
isi snmp settings view
```

---

## Licenses & Support

```bash
# License status
isi license licenses list
isi license licenses view <license_name>

# Support connectivity
isi esrs settings view
isi esrs connectivity test

# Cluster config export
isi config dump
```

---

## Firmware & Upgrades

```bash
# Current version
isi version

# Drive firmware
isi devices drives firmware list
isi devices drives firmware upgrade start

# Cluster upgrade (OneFS rolling)
isi upgrade cluster --upgrade-image <image>
isi upgrade cluster check
isi upgrade nodes list
isi upgrade nodes view <node_id>
```
