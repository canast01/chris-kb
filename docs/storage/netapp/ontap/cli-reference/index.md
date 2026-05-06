# NetApp ONTAP CLI Reference

Commonly used ONTAP CLI commands for managing NetApp storage systems.

---

## Cluster

```bash
# Identity and status
cluster show
cluster identity show
cluster identity modify -name <new_name>
cluster ring show
cluster ha show
version

# NTP
cluster time-service ntp server show
cluster time-service ntp server create -server <ip>
cluster time-service ntp server delete -server <ip>
```

---

## Nodes

```bash
# Node status
node show
node show -fields node,health,uptime,model,serial-number

# Node-level diagnostics (advanced shell)
node run -node <node> sysconfig
node run -node <node> sysconfig -a
node run -node <node> sysconfig -r
node run -node <node> df -h
node run -node <node> environment status
```

---

## System Health & Events

```bash
# Health
system health status show
system health alert show
system health subsystem show
system health node-connectivity show

# Event log
event log show
event log show -severity emergency
event log show -severity alert
event log show -node <node>
event log show -time >1h

# Firmware / images
system node image show
system node image update -node <node> -package <pkg>
system node upgrade-revert show
```

---

## Storage — Aggregates & Disks

```bash
# Aggregates
storage aggregate show
storage aggregate show -state online
storage aggregate show -fields aggr-name,node,size,availsize,usedsize,state
storage aggregate show-space
storage aggregate show-space -aggregate <aggr>
storage aggregate modify -aggregate <aggr> -maxraidsize <n>

# Disks
storage disk show
storage disk show -broken
storage disk show -fields disk,bay,node,container-type,disk-type,rpm,size,position
storage disk unfail -disk <disk>
storage disk assign -disk <disk> -owner <node>
```

---

## Volumes

```bash
# List / status
volume show
volume show -vserver <svm>
volume show -fields volume,vserver,size,used,available,percent-used,state
volume show -state offline
volume show -junction-path <path>

# Create / modify / delete
volume create -vserver <svm> -volume <vol> -aggregate <aggr> -size <size> -junction-path <path> -policy <export-policy>
volume modify -vserver <svm> -volume <vol> -size <size>
volume modify -vserver <svm> -volume <vol> -percent-snapshot-space <n>
volume rename -vserver <svm> -volume <old> -newname <new>
volume delete -vserver <svm> -volume <vol>

# Mount / unmount
volume mount -vserver <svm> -volume <vol> -junction-path <path>
volume unmount -vserver <svm> -volume <vol>

# Bring online / offline
volume online -vserver <svm> -volume <vol>
volume offline -vserver <svm> -volume <vol>

# Efficiency (dedup / compression)
volume efficiency show
volume efficiency show -vserver <svm> -volume <vol>
volume efficiency start -vserver <svm> -volume <vol>
volume efficiency stop -vserver <svm> -volume <vol>

# FlexClone
volume clone create -vserver <svm> -flexclone <name> -parent-volume <vol>
volume clone create -vserver <svm> -flexclone <name> -parent-volume <vol> -parent-snapshot <snap>
volume clone split start -vserver <svm> -flexclone <name>
volume clone split status -vserver <svm> -flexclone <name>
```

---

## Snapshots

```bash
# List
volume snapshot show
volume snapshot show -vserver <svm> -volume <vol>

# Create / delete / restore
volume snapshot create -vserver <svm> -volume <vol> -snapshot <name>
volume snapshot delete -vserver <svm> -volume <vol> -snapshot <name>
volume snapshot delete -vserver <svm> -volume <vol> -snapshot * -force true
volume snapshot restore -vserver <svm> -volume <vol> -snapshot <name>
volume snapshot rename -vserver <svm> -volume <vol> -snapshot <old> -new-name <new>

# Snapshot policy
volume snapshot policy show
volume snapshot policy create -policy <name> -enabled true
volume snapshot policy add-schedule -policy <name> -schedule <sched> -count <n>
```

---

## SVMs (Storage Virtual Machines)

```bash
# List / status
vserver show
vserver show -vserver <svm>
vserver show -fields vserver,type,state,allowed-protocols

# Create / delete
vserver create -vserver <svm> -rootvolume <vol> -aggregate <aggr> -rootvolume-security-style unix
vserver delete -vserver <svm>

# Modify protocols
vserver modify -vserver <svm> -allowed-protocols nfs,cifs,iscsi
vserver show-protocols
```

---

## Network

```bash
# LIFs (logical interfaces)
network interface show
network interface show -vserver <svm>
network interface show -fields lif,vserver,address,home-node,home-port,status-oper
network interface create -vserver <svm> -lif <lif> -role data -data-protocol nfs -home-node <node> -home-port <port> -address <ip> -netmask <mask>
network interface modify -vserver <svm> -lif <lif> -address <ip> -netmask <mask>
network interface delete -vserver <svm> -lif <lif>
network interface migrate -vserver <svm> -lif <lif> -dest-node <node> -dest-port <port>
network interface revert -vserver <svm> -lif <lif>
network interface failover-groups show

# Ports
network port show
network port show -role data
network port show -fields node,port,speed,health-status,link-status
network port ifgrp show
network port vlan show

# Routes
network route show
network route create -vserver <svm> -destination 0.0.0.0/0 -gateway <gw>
network route delete -vserver <svm> -destination 0.0.0.0/0 -gateway <gw>

# Ping / connectivity
network ping -lif <lif> -vserver <svm> -destination <ip>
```

---

## NFS

```bash
# NFS service
vserver nfs show
vserver nfs create -vserver <svm> -v3 enabled -v4.0 enabled -v4.1 enabled
vserver nfs modify -vserver <svm> -v4.1 enabled

# Export policies
vserver export-policy show
vserver export-policy show -vserver <svm>
vserver export-policy create -vserver <svm> -policyname <name>
vserver export-policy delete -vserver <svm> -policyname <name>

# Export rules
vserver export-policy rule show
vserver export-policy rule show -vserver <svm> -policyname <name>
vserver export-policy rule create -vserver <svm> -policyname <name> -ruleindex 1 -clientmatch <cidr> -rorule sys -rwrule sys -superuser sys
vserver export-policy rule delete -vserver <svm> -policyname <name> -ruleindex <n>

# Assign policy to volume
volume modify -vserver <svm> -volume <vol> -policy <export-policy>

# NFS client check
vserver nfs check-client -vserver <svm> -client-ip <ip>
```

---

## CIFS / SMB

```bash
# CIFS server
vserver cifs show
vserver cifs create -vserver <svm> -cifs-server <name> -domain <domain>
vserver cifs delete -vserver <svm>

# Shares
vserver cifs share show
vserver cifs share show -vserver <svm>
vserver cifs share create -vserver <svm> -share-name <name> -path <path>
vserver cifs share modify -vserver <svm> -share-name <name> -comment <text>
vserver cifs share delete -vserver <svm> -share-name <name>
vserver cifs share access-control show -vserver <svm> -share <name>

# Sessions / connections
vserver cifs session show
vserver cifs session show -vserver <svm>
vserver cifs session show -fields node,vserver,connection-count
```

---

## iSCSI

```bash
# iSCSI service
vserver iscsi show
vserver iscsi create -vserver <svm>
vserver iscsi modify -vserver <svm> -is-admin-enabled true

# LUNs
lun show
lun show -vserver <svm>
lun show -fields path,vserver,size,state,mapped,os-type
lun create -vserver <svm> -path <path> -size <size> -ostype vmware
lun delete -vserver <svm> -path <path>
lun resize -vserver <svm> -path <path> -size <size>
lun online -vserver <svm> -path <path>
lun offline -vserver <svm> -path <path>
lun map -vserver <svm> -path <path> -igroup <igroup>
lun unmap -vserver <svm> -path <path> -igroup <igroup>
lun mapping show
lun mapping show -vserver <svm>

# igroups
lun igroup show
lun igroup show -vserver <svm>
lun igroup create -vserver <svm> -igroup <name> -protocol iscsi -ostype vmware
lun igroup add -vserver <svm> -igroup <name> -initiator <iqn>
lun igroup remove -vserver <svm> -igroup <name> -initiator <iqn>
lun igroup delete -vserver <svm> -igroup <name>
```

---

## Fibre Channel

```bash
# FCP service
vserver fcp show
vserver fcp create -vserver <svm>

# Adapters and ports
fcp adapter show
fcp adapter show -fields node,adapter,state,speed,fabric-established
fcp interface show
fcp initiator show

# igroups (shared with iSCSI commands above)
lun igroup create -vserver <svm> -igroup <name> -protocol fcp -ostype vmware
```

---

## SnapMirror

```bash
# Show relationships
snapmirror show
snapmirror show -destination-path <svm>:<vol>
snapmirror show -fields source-path,destination-path,state,lag-time,healthy

# Create / delete
snapmirror create -source-path <svm>:<vol> -destination-path <svm>:<vol> -type DP -policy MirrorAllSnapshots
snapmirror delete -destination-path <svm>:<vol>
snapmirror release -source-path <svm>:<vol> -destination-path <svm>:<vol>

# Operations
snapmirror initialize -destination-path <svm>:<vol>
snapmirror update -destination-path <svm>:<vol>
snapmirror quiesce -destination-path <svm>:<vol>
snapmirror break -destination-path <svm>:<vol>
snapmirror resync -destination-path <svm>:<vol>
snapmirror abort -destination-path <svm>:<vol>

# History and lag
snapmirror history show -destination-path <svm>:<vol>
snapmirror lag show
```

---

## Quotas

```bash
volume quota show
volume quota report -vserver <svm> -volume <vol>
volume quota on -vserver <svm> -volume <vol>
volume quota off -vserver <svm> -volume <vol>
volume quota resize -vserver <svm> -volume <vol>
volume quota policy rule show -vserver <svm>
volume quota policy rule create -vserver <svm> -policy-name default -type user -target "" -volume <vol> -disk-limit <size>
```

---

## Performance & QoS

```bash
# Statistics
statistics show
statistics start -object volume -sample-id perf_check
statistics stop -sample-id perf_check

# QoS policy groups
qos policy-group show
qos policy-group create -policy-group <name> -vserver <svm> -max-throughput <iops>IOPS
qos policy-group modify -policy-group <name> -max-throughput <iops>IOPS
qos workload show
qos statistics performance show
```

---

## Security & Users

```bash
# Logins
security login show
security login show -vserver <svm>
security login create -username <user> -application ssh -authentication-method password -role admin -vserver <svm>
security login delete -username <user> -application ssh -vserver <svm>
security login password -username <user> -vserver <svm>
security login lock -username <user> -vserver <svm>
security login unlock -username <user> -vserver <svm>

# Roles
security login role show
security login role create -role <name> -vserver <svm> -cmddirname DEFAULT -access none

# Certificates
security certificate show
security certificate show -vserver <svm>
security certificate install -vserver <svm> -type server
security certificate generate-csr -common-name <cn> -size 2048 -country US -state <state> -locality <city> -organization <org>
```

---

## AutoSupport

```bash
autosupport show
autosupport show -node <node>
autosupport invoke -node <node> -type test
autosupport invoke -node <node> -type all -message "Manual upload"
autosupport history show
autosupport history show -node <node>
autosupport modify -node <node> -state enable
autosupport modify -node <node> -mail-hosts <smtp>
```
