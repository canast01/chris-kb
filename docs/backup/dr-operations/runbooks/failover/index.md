---
tags:
  - dr
description: "DR failover procedure: verify backup schedule currency and RPO compliance before cutover, confirm replication sync state with symrdf query or snapmirror..."
---
# DR Failover Procedure

<div class="kb-summary">
DR failover procedure: verify backup schedule currency and RPO compliance before cutover, confirm replication sync state with <code>symrdf query</code> or <code>snapmirror show</code>, activate DR site storage, redirect compute hosts, and validate application health. Trigger weekly backup schedule on DR site immediately after failover to maintain retention continuity.

*Applies to: all products with DR replication*
</div>

```bash
symrdf -g <rdfgroup> query
# Confirm R2 volumes are Synchronized or Consistent before failing over
```

```powershell
# Register and power on VM from replica datastore
$ds = Get-Datastore -Name "<dr-datastore>"
$vmx = "[<dr-datastore>] <vm-name>/<vm-name>.vmx"
$vm = New-VM -VMFilePath $vmx -VMHost (Get-VMHost "<dr-host>") -Datastore $ds -RunAsync
Start-VM -VM "<vm-name>"
```
```bash
# Confirm storage volumes visible to DR hosts
multipath -ll
lsblk

# Confirm filesystems mounted
df -h | grep <expected-mount>

# Start application services
systemctl start <service>
systemctl status <service>
```

```text title="Expected output"
mpatha (36001405abc123def456789012345678) dm-0 NETAPP,LUN C-Mode
size=500G features='3 queue_if_no_path pg_init_retries 50' hwhandler='1 alua' wp=rw
`-+- policy='service-time 0' prio=50 status=active
  |- 2:0:0:0 sda 8:0  active ready running
  `- 3:0:0:0 sdb 8:16 active ready running

NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0    0  500G  0 disk
└─sda1   8:1    0  500G  0 part /mnt/dr-data
sdb      8:16   0  500G  0 disk
└─sdb1   8:17   0  500G  0 part /mnt/dr-data

Filesystem     Size  Used Avail Use% Mounted on
/dev/mapper/mpatha-part1  500G  245G  255G  49% /mnt/dr-data

● app-service.service - Application Service
   Loaded: loaded (/etc/systemd/system/app-service.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2s ago
   Main PID: 8742 (java)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `multipath: command not found` | Install device-mapper-multipath package with `yum install device-mapper-multipath` or `apt install multipath-tools`. |
    | `Unit <service> not found.` | Verify the service name exists with `systemctl list-unit-files | grep <service>` and use the correct unit file name. |
    | `mount: /mnt/dr-data: No such file or directory` | Create the mount point directory with `mkdir -p /mnt/dr-data` before mounting volumes. |
```bash
# HTTP health check
curl -vk https://<dr-app-url>/health

# DB connectivity
psql -h <dr-db-host> -U <user> -c "SELECT 1;"
```
```powershell
# Confirm services started
Get-Service | Where-Object { $_.Status -ne 'Running' -and $_.StartType -eq 'Automatic' }

# Test connectivity
Test-NetConnection -ComputerName <dr-app-server> -Port 443
```

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```

## See also

- [DR Runbooks](../index.md)
- [Failback](../failback/index.md)
- [Full DR Runbook](../dr-runbook/index.md)
- [DR Design](../../dr-design/index.md)
- [Health Checks](../../health-checks/index.md)
