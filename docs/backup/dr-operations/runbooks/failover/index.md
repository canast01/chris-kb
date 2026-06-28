---
tags:
  - dr
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

## See also

- [DR Runbooks](../index.md)
- [Failback](../failback/index.md)
- [Full DR Runbook](../dr-runbook/index.md)
- [DR Design](../../dr-design/index.md)
- [Health Checks](../../health-checks/index.md)
