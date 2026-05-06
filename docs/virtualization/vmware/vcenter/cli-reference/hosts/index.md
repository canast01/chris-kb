# Hosts

> Part of the [vCenter CLI Reference (PowerCLI & DCLI)](../).

---

## Hosts

```powershell
# List all hosts
Get-VMHost
Get-VMHost | Select-Object Name, State, PowerState, ConnectionState, Version | Format-Table

# Host by name or cluster
Get-VMHost -Name <hostname>
Get-Cluster <cluster_name> | Get-VMHost

# Host details
Get-VMHost <host> | Select-Object *
Get-VMHost <host> | Get-VMHostHardware

# Maintenance mode
Set-VMHost -VMHost <host> -State Maintenance
Set-VMHost -VMHost <host> -State Connected

# Host services
Get-VMHostService -VMHost <host>
Start-VMHostService -HostService (Get-VMHostService -VMHost <host> | Where-Object { $_.Key -eq "TSM-SSH" })
Stop-VMHostService -HostService (Get-VMHostService -VMHost <host> | Where-Object { $_.Key -eq "TSM-SSH" })

# NTP
Get-VMHostNtpServer -VMHost <host>
Add-VMHostNtpServer -VMHost <host> -NtpServer <ip>

# Syslog
Get-VMHostSysLogServer -VMHost <host>
Set-VMHostSysLogServer -VMHost <host> -SysLogServer udp://<ip>:514
```
