# Networks

> Part of the [vCenter CLI Reference (PowerCLI & DCLI)](../).

---

## Networks

```powershell
# Standard switches
Get-VirtualSwitch -VMHost <host>
Get-VirtualPortGroup -VMHost <host>

# Distributed switches
Get-VDSwitch
Get-VDSwitch | Select-Object Name, NumPorts, Version
Get-VDPortgroup

# VMkernel adapters
Get-VMHostNetworkAdapter -VMHost <host> -VMKernel
Get-VMHostNetworkAdapter -VMHost <host> -VMKernel | Select-Object Name, IP, SubnetMask, VMotionEnabled, ManagementTrafficEnabled
```
