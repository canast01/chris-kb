# Networks

> Part of the [vCenter CLI Reference (PowerCLI & DCLI)](../).
## Standard vSwitches

```powershell
# List standard vSwitches on a host
Get-VirtualSwitch -VMHost <host>
Get-VirtualSwitch -VMHost <host> | Select-Object Name, NumPorts, Nic, @{N="MTU";E={$_.Mtu}}

# Port groups on a standard switch
Get-VirtualPortGroup -VMHost <host>
Get-VirtualPortGroup -VMHost <host> | Select-Object Name, VLanId, @{N="vSwitch";E={$_.VirtualSwitchName}}
```

## Distributed vSwitches (VDS)

```powershell
# All distributed switches
Get-VDSwitch

# VDS detail — name, version, uplinks, port count
Get-VDSwitch | Select-Object Name, NumPorts, Version, Mtu,
    @{N="Uplinks";E={$_.ExtensionData.Config.UplinkPortPolicy.UplinkPortName -join ", "}}

# Distributed port groups
Get-VDPortgroup
Get-VDPortgroup | Select-Object Name, VlanConfiguration, NumPorts,
    @{N="VDS";E={$_.VDSwitch.Name}}

# VMs connected to a specific DVPortgroup
Get-VDPortgroup -Name "<portgroup_name>" | Get-VM | Select-Object Name, PowerState
```

## VMkernel Adapters

```powershell
# All VMkernel adapters on a host
Get-VMHostNetworkAdapter -VMHost <host> -VMKernel

# With IP, subnet, and traffic type flags
Get-VMHostNetworkAdapter -VMHost <host> -VMKernel |
    Select-Object Name, IP, SubnetMask, Mac,
    VMotionEnabled, ManagementTrafficEnabled,
    FaultToleranceLoggingEnabled, VsanTrafficEnabled
```

## Physical NICs (vmnic)

```powershell
# Physical NICs on a host
Get-VMHostNetworkAdapter -VMHost <host> -Physical |
    Select-Object Name, Mac, BitRatePerSec,
    @{N="Speed";E={$_.BitRatePerSec / 1000000}},
    @{N="LinkUp";E={$_.ExtensionData.LinkSpeed -ne $null}}
```

## DNS and Routing

```powershell
# DNS configuration on a host
Get-VMHostNetwork -VMHost <host> | Select-Object HostName, DomainName, DnsAddress

# Default gateway
(Get-VMHostNetwork -VMHost <host>).ConsoleGateway
```

## NIC Teaming Policy

```powershell
# Teaming policy for a standard port group
$pg = Get-VirtualPortGroup -VMHost <host> -Name "<portgroup_name>"
$pg.ExtensionData.ComputedPolicy.NicTeaming

# Active/standby NICs for a portgroup
$pg.ExtensionData.ComputedPolicy.NicTeaming.NicOrder
```

## VLAN Report

```powershell
# All VLANs in use across VDS port groups
Get-VDPortgroup | Select-Object Name, @{N="VLAN";E={$_.VlanConfiguration.VlanId}} |
    Sort-Object VLAN

# VLAN range trunks (access vs trunk)
Get-VDPortgroup | Select-Object Name,
    @{N="VLANType";E={$_.VlanConfiguration.GetType().Name}},
    @{N="VLANId";E={$_.VlanConfiguration.VlanId}}
```
