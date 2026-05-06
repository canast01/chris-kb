# Operations

> Part of the [ESXi](../) reference.

---

## Daily Checks

- [ ] Run `Get-VMHost | Select Name,ConnectionState,PowerState` — confirm all hosts are Connected and PoweredOn
- [ ] Check hardware health alerts in vCenter — flag any red or yellow alarms on ESXi host objects
- [ ] Run `esxcli storage core path list | grep -c dead` — result should be 0; any dead paths require immediate investigation
- [ ] Run `esxcli network vswitch dvs vmware list` — verify dvSwitch uplinks are all connected with expected active NICs
- [ ] Review vCenter alarms dashboard for any triggered host-level alarms
- [ ] Verify NTP sync on all hosts: `esxcli system ntp get` — confirm `Running: true` and servers configured
- [ ] Review ESXi vmkernel log for NMP, SCSI, or network errors: check `/var/log/vmkernel.log`
- [ ] Confirm no hosts are in maintenance mode unexpectedly

## Health Check

- [ ] All hosts Connected and PoweredOn: `Get-VMHost | Select Name,ConnectionState,PowerState`
- [ ] No hardware health warnings or critical alerts: `esxcli hardware health get`
- [ ] All storage paths active — no dead paths: `esxcli storage nmp device list`
- [ ] All vmnic uplinks connected: `esxcli network nic list`
- [ ] NTP running and synchronized: `esxcli system ntp get`
- [ ] No vmkernel errors in recent log entries
- [ ] PowerCLI hardware summary clean: `Get-VMHostHardware`
- [ ] No unexpected maintenance mode hosts

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

## Change Readiness

- [ ] vMotion tested and working between affected hosts before any maintenance
- [ ] Host not in maintenance mode — no other concurrent work on same host
- [ ] HA admission control checked: cluster has capacity to tolerate host loss
- [ ] All storage paths healthy and no dead paths before starting: `esxcli storage core path list | grep dead`
- [ ] vCenter backup is current (file-based backup or VAMI snapshot taken recently)
- [ ] DRS is enabled and configured to fully automated — VMs will migrate automatically
- [ ] Change window approved and communicated; storage and compute teams notified

| Item | Status | Notes |
|---|---|---|
| vMotion tested | | Test migration successful |
| HA admission control OK | | Cluster has failover capacity |
| Storage paths healthy | | `grep dead` returns 0 |
| vCenter backup current | | Backup timestamp |
| Change window approved | | Ticket reference |

## Incident Triage

- [ ] Check host connection state in vCenter — is the host Connected, Disconnected, or Not Responding?
- [ ] Run `esxcli hardware health get` — identify any hardware component reporting Warning or Error status
- [ ] Check storage paths: `esxcli storage core path list | grep dead` — dead paths indicate storage connectivity issue
- [ ] Check network uplinks: `esxcli network nic list` — look for down links on affected host
- [ ] Review vmkernel log for the time of the incident: `tail -500 /var/log/vmkernel.log`
- [ ] Check NTP status — a drifted clock can cause certificate and authentication failures
- [ ] Review vCenter events for the affected host around the incident time
- [ ] If host is Not Responding, attempt IPMI/iDRAC/iLO console access for out-of-band diagnosis

| Question | Answer |
|---|---|
| What is the host's connection state in vCenter? | Connected / Disconnected / Not Responding |
| Are there hardware health alerts? | `esxcli hardware health get` |
| Are storage paths dead? | `esxcli storage core path list \| grep dead` |
| Are vmnic uplinks down? | `esxcli network nic list` |
| What does vmkernel.log show at incident time? | `/var/log/vmkernel.log` — SCSI, NMP, network errors |

## Maintenance Window

1. Confirm host is healthy and not already in maintenance mode: `Get-VMHost | Select Name,ConnectionState`
2. Check HA admission control — ensure cluster can tolerate one less host during maintenance
3. Put host into maintenance mode: `Set-VMHost -VMHost <hostname> -State Maintenance`
4. Wait for all VMs to vMotion off the host — monitor via vCenter Tasks pane
5. Confirm zero VMs running on the host before proceeding: `Get-VM -Location <host> | Where-Object {$_.PowerState -eq "PoweredOn"}`
6. Perform the required maintenance work (patching, hardware replacement, config change)
7. Exit maintenance mode: `Set-VMHost -VMHost <hostname> -State Connected`
8. Validate host is Connected, all storage paths active, NTP in sync, and VMs have migrated back or are running correctly

## Post-Change Validation

- [ ] Host shows Connected and PoweredOn in vCenter
- [ ] No hardware health alarms triggered: `esxcli hardware health get`
- [ ] All storage paths active, no dead paths: `esxcli storage core path list | grep dead`
- [ ] All vmnic uplinks connected: `esxcli network nic list`
- [ ] VMs running correctly on the host or successfully migrated back
- [ ] NTP synchronized: `esxcli system ntp get` confirms `Running: true`
- [ ] No new vCenter alarms or vmkernel errors introduced by the change
- [ ] Close change ticket with validation evidence attached
