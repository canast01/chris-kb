---
tags:
  - vsphere-replication
  - backup-dr
---
# vSphere Replication Cheat Sheet

*Applies to: All products*

<div class="kb-summary">
Top-10 vSphere Replication commands for replication configuration, status monitoring, and recovery via PowerCLI and VRMS REST API.
</div>

```d2
direction: down

powercli: "PowerCLI" {shape: rectangle}
vrms_rest_api: "VRMS REST API" {shape: rectangle}

powercli -> vrms_rest_api: uses
```

## PowerCLI

```powershell
Connect-VIServer vcenter.lab.local
Import-Module VMware.VimAutomation.Srm

# List replicated VMs and their status
Get-VM | Get-VrReplication                                                 # all VMs with replication
Get-VrReplication | Select VM, ReplicationState, RPO, LastReplicationTime  # status overview

# Configure replication on a VM
$vm = Get-VM -Name myvm
$target = Get-VrServer -Name vrms-target.lab.local
New-VrReplication -VM $vm -DestinationServer $target -RPO 60              # 60-min RPO

# Manage existing replication
Suspend-VrReplication -VM $vm                                              # pause replication
Resume-VrReplication -VM $vm                                               # resume replication
Remove-VrReplication -VM $vm                                               # remove replication config

# Recovery (failover to replica)
Start-VrRecovery -VM $vm -DestinationServer $target -Planned $true        # planned recovery
```

## VRMS REST API

```bash
BASE="https://vrms/api"
AUTH="-u administrator@vsphere.local:VMware1!"

curl -sk $AUTH $BASE/vms | python3 -m json.tool                            # replicated VMs
curl -sk $AUTH $BASE/vms/<id> | python3 -m json.tool                       # VM replication detail
curl -sk $AUTH $BASE/config | python3 -m json.tool                         # VRMS server config
curl -sk $AUTH $BASE/health | python3 -m json.tool                         # VRMS health status
```


```text title="Expected output"
{
  "vms": [
    {
      "id": "vm-42",
      "name": "prod-web-01",
      "state": "synced",
      "rpo": 300,
      "last_sync": "2024-01-15T14:32:18Z"
    },
    {
      "id": "vm-87",
      "name": "prod-db-02",
      "state": "syncing",
      "rpo": 600,
      "last_sync": "2024-01-15T14:28:45Z"
    },
    {
      "id": "vm-156",
      "name": "dev-app-03",
      "state": "synced",
      "rpo": 1800,
      "last_sync": "2024-01-15T14:15:22Z"
    }
  ]
}
{
  "id": "vm-42",
  "name": "prod-web-01",
  "source_site": "dc-primary",
  "target_site": "dc-secondary",
  "state": "synced",
  "rpo": 300,
  "last_sync": "2024-01-15T14:32:18Z",
  "replicated_bytes": 524288000,
  "network_compression": 0.68
}
{
  "version": "8.7.1.0-21567890",
  "hostname": "vrms-prod-01.corp.local",
  "max_concurrent_replications": 16,
  "storage_path": "/var/lib/vrms/data",
  "ssl_enabled": true,
  "syslog_enabled": false
}
{
  "status": "healthy",
  "uptime_seconds": 2592000,
  "cpu_usage_percent": 12.4,
  "memory_usage_percent": 58.7,
  "disk_usage_percent": 71.2,
  "last_check": "2024-01-15T14:35:01Z"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip SSL verification (already present in example; verify VRMS certificate is trusted or regenerate it).
    **`curl: (7) Failed to connect to vrms port 443: Connection refused`** — Verify VRMS service is running with `systemctl status vrms` and confirm the hostname/IP and port are correct.
    **`jq: parse error: Invalid JSON at line 1`** — Ensure the API endpoint is correct and VRMS is responding with valid JSON; check credentials with `curl -sk $AUTH $BASE/health` first.
## See also

- [vSphere Replication Operations](../../../virtualization/vmware/products/vsphere-replication/operations/procedures/)
- [vSphere Replication Troubleshooting](../../../virtualization/vmware/products/vsphere-replication/troubleshooting/common-issues/)
