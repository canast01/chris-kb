# ESXi — Health Checks

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| [ ] Host connection state | `Get-VMHost \| Select Name,ConnectionState,PowerState` | Confirm all Connected and PoweredOn |
| [ ] Hardware health alerts in vCenter | — | Flag any red or yellow alarms on ESXi host objects |
| [ ] Dead storage paths | `esxcli storage core path list \| grep -c dead` | Result should be 0 |
| [ ] dvSwitch uplinks | `esxcli network vswitch dvs vmware list` | Verify expected active NICs |
| [ ] vCenter alarms dashboard | — | Review any triggered host-level alarms |
| [ ] NTP sync | `esxcli system ntp get` | Confirm `Running: true` and servers configured |
| [ ] vmkernel log errors | `/var/log/vmkernel.log` | Check for NMP, SCSI, or network errors |
| [ ] Maintenance mode | — | Confirm no hosts unexpectedly in maintenance mode |

## Health Check Commands

```bash
# ESXi host health sweep (run per host via SSH or esxcli -s)
esxcli hardware health get
esxcli storage nmp device list
esxcli storage core path list | grep dead
esxcli network nic list
esxcli system ntp get

# PowerCLI (run from management workstation)
Get-VMHost | Select Name,ConnectionState,PowerState
Get-VMHostHardware | Select VMHost,Manufacturer,Model,CpuCount,MemorySize
```

## Health Checklist

- [ ] All hosts Connected and PoweredOn
- [ ] No hardware health warnings or critical alerts
- [ ] All storage paths active — no dead paths
- [ ] All vmnic uplinks connected
- [ ] NTP running and synchronized
- [ ] No vmkernel errors in recent log entries
- [ ] PowerCLI hardware summary clean
- [ ] No unexpected maintenance mode hosts
