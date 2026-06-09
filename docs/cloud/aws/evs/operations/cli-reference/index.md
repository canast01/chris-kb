# Amazon EVS — CLI Reference

<div class="kb-summary">
AWS CLI commands for EVS cluster and host management, PowerCLI for vSphere operations, and esxcli for ESXi-level diagnostics on EVS bare-metal hosts.
</div>

```text
┌───────────────────────────────────── Amazon EVS — CLI Reference ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   AWS CLI: cluster/host lifecycle, capacity, and status; requires EVS IAM permissions          │  │
│   │   PowerCLI: vSphere cluster, vSAN, and VM management; connect to vCenter in EVS VPC           │   │
│   │   esxcli: host-level storage, network, and VMkernel diagnostics on bare-metal ESXi             │  │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## AWS CLI — EVS Cluster

```bash
# List all EVS environments
aws evs list-environments --query 'environmentSummaries[*].[environmentId,environmentName,state]' \
  --output table

# Get environment details
aws evs get-environment --environment-id env-xxx

# List hosts in cluster
aws evs list-environment-hosts --environment-id env-xxx \
  --query 'hostSummaries[*].[hostId,instanceType,state]' --output table

# Add a host to cluster
aws evs create-environment-host \
  --environment-id env-xxx \
  --host '{"instanceType":"i4i.metal","keyName":"evs-cluster-key"}'

# Delete (remove) a host
aws evs delete-environment-host --environment-id env-xxx --host-id host-xxx

# Get VLANs for the environment
aws evs list-environment-vlans --environment-id env-xxx
```

## AWS CLI — Host Replacement

```bash
# When AWS notifies of a scheduled host maintenance or failure:
# 1. Put the ESXi host into maintenance mode first (via PowerCLI or vCenter)
# 2. Wait for vSAN to fully evacuate and resyncs to complete
# 3. Then delete the host via EVS API → AWS provisions a replacement

# Monitor vSAN resync after adding replacement host
# PowerCLI: Get-VsanResyncDashboard -Cluster (cluster object)
```

## PowerCLI — vSphere Operations

```powershell
# Connect to vCenter in EVS
Connect-VIServer -Server vcenter.vcf.internal -User administrator@vsphere.local -Password 'P@ssw0rd'

# Cluster health overview
Get-Cluster | Select Name, HAEnabled, DRSEnabled

# Host summary
Get-VMHost | Select Name, ConnectionState, PowerState, NumCpu, MemoryTotalGB, MemoryUsageGB

# vSAN cluster health
$cluster = Get-Cluster -Name "EVS-Management-Cluster"
Get-VsanView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system" |
  ForEach-Object { $_.QueryVsanClusterHealthSummary($cluster.Id, $null, $null, $true, $null, $null, "defaultView") } |
  Select -ExpandProperty Groups |
  ForEach-Object { Write-Host "$($_.GroupName): $($_.GroupHealth)" }

# vSAN disk groups
Get-VsanDiskGroup | Select VMHost, @{N="CacheDisks";E={($_.ExtensionData.SSD).Count}}, @{N="CapDisks";E={($_.ExtensionData.NonSSD).Count}}

# VM inventory
Get-VM | Select Name, PowerState, NumCpu, MemoryGB, @{N="Host";E={$_.VMHost.Name}} | Sort Name

# vMotion a VM to a different host
Move-VM -VM "myvm" -Destination (Get-VMHost "evs-host-02.vcf.internal")

# Put host in maintenance mode (vSAN data evacuation)
Set-VMHost -VMHost "evs-host-01.vcf.internal" -State Maintenance -Evacuate $true

# Exit maintenance mode
Set-VMHost -VMHost "evs-host-01.vcf.internal" -State Connected
```

## esxcli — ESXi Host Diagnostics

```bash
# SSH to ESXi host (enable SSH via vCenter or DCUI first)
ssh root@evs-host-01.vcf.internal

# Storage adapter / vSAN disk info
esxcli storage core adapter list
esxcli vsan storage list

# Network VMkernel interfaces
esxcli network ip interface list

# VMkernel routing
esxcli network ip route list

# Check vSAN health from host
esxcli vsan health cluster list

# Check NVMe devices (EVS hosts use NVMe for vSAN)
esxcli nvme device list

# Network connectivity test from VMkernel
vmkping -I vmk0 <target-ip>
vmkping -I vmk1 <vtep-gateway-ip>   # NSX-T VTEP VMkernel
```
