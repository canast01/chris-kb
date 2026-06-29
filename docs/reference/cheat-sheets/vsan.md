---
tags:
  - vsan
  - storage
---
# vSAN Cheat Sheet

*Applies to: All products*

<div class="kb-summary">
Top-10 vSAN commands for cluster health, disk groups, object status, and policy via <code>esxcli vsan</code> and PowerCLI.
</div>
![vSAN Cheat Sheet](../../assets/reference-cheat-sheets-vsan.svg)

## Common commands

```bash
# Cluster state (run on any ESXi host in cluster)
esxcli vsan cluster get                        # cluster UUID, node count, health
esxcli vsan cluster unicastagent list          # unicast peers for this host
esxcli vsan network list                       # VMkernel adapter used for vSAN

# Disk groups
esxcli vsan storage list                       # all disks: cache/capacity tier, state
esxcli vsan storage add -s <cache_naa> -d <cap_naa>   # add disk group
esxcli vsan storage remove -u <diskgroup_uuid> # remove disk group (all disks)

# Objects and components
esxcli vsan debug object list                  # all objects: health, policy compliance
esxcli vsan debug component list               # component placement per disk

# Health
esxcli vsan health cluster get                 # overall cluster health summary
esxcli vsan health cluster list                # per-check health results
```


```text title="Expected output"
Cluster UUID: 52d5cad5-e8f3-4a2e-b1c3-7f8e9a0b1c2d
Node count: 4
Health state: healthy

Unicast peers:
  esx-node-02.lab.local (192.168.1.102)
  esx-node-03.lab.local (192.168.1.103)
  esx-node-04.lab.local (192.168.1.104)

VMkernel adapters for vSAN:
  vmk1: 192.168.100.101/24 (vsan)

Disk groups:
  DiskGroup UUID: 52d5cad5-e8f3-4a2e-b1c3-7f8e9a0b1c2d
    Cache tier (SSD): naa.5000c5008a1b2c3d (healthy)
    Capacity tier (HDD): naa.5000c5008a1b2c3e (healthy)
    Capacity tier (HDD): naa.5000c5008a1b2c3f (healthy)

Object summary: 847 objects, 2541 components
  Healthy: 847 (100%)
  Policy compliant: 847 (100%)

Component placement: 2541 components distributed across 4 nodes
  Node esx-node-01: 635 components
  Node esx-node-02: 636 components
  Node esx-node-03: 635 components
  Node esx-node-04: 635 components

Cluster health: green
  Cluster connectivity: green
  Data redundancy: green
  Disk balance: green
  Memory pools: green
```

!!! warning "Common errors"
    **`vsan cluster get: Unknown command or namespace`** — Ensure vSAN is licensed and enabled on the cluster; run `esxcli vsan cluster get` only on hosts that are part of an active vSAN cluster.
    **`Error: The object or item could not be found`** — Verify the disk NAA identifier is correct by running `esxcli storage core device list` and use the exact NAA string in the `-s` and `-d` parameters.
    **`Permission denied`** — Run these commands as root or with appropriate vSAN administrator privileges; use `sudo` or ensure your account has vSAN management permissions.
## PowerCLI (run against vCenter)

```powershell
Connect-VIServer vcenter.lab.local
# Cluster health summary
Get-VsanView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system" |
  ForEach { $_.VsanQueryVcClusterHealthSummary($cluster, $null, $null, $true, $null, $null, "defaultView") }

# Storage policy compliance
Get-SpbmStoragePolicy -Name "vSAN Default Storage Policy"
Get-VM | Get-SpbmEntityConfiguration | Where { $_.ComplianceStatus -ne "compliant" }
```

## See also

- [vSAN Operations](../../../virtualization/vmware/vsan/operations/procedures/)
- [vSAN Health Checks](../../../virtualization/vmware/vsan/operations/health-checks/)
- [vSAN Troubleshooting](../../../virtualization/vmware/vsan/troubleshooting/common-issues/)
