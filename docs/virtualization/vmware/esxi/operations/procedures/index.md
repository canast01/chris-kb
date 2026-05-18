# ESXi — Procedures

```
ESXi Maintenance Window — Procedure Flow
┌───────────────────────────────────────────────────────┐
│  PRE-CHECKS                                           │
│  ├── vMotion working between affected hosts?          │
│  ├── HA admission control — cluster has N+1 headroom? │
│  ├── Dead storage paths? (grep dead → must be 0)      │
│  ├── vCenter backup current?                          │
│  └── DRS Fully Automated?                             │
└──────────────────────┬────────────────────────────────┘
                       │ All checks pass
          ┌────────────▼──────────────┐
          │  Enter Maintenance Mode   │
          │  Set-VMHost -State Maint  │
          │  VMs vMotion to peers     │
          └────────────┬──────────────┘
                       │
          ┌────────────▼──────────────┐
          │  Perform Approved Work    │
          │  (patch / HW / config)    │
          └────────────┬──────────────┘
                       │
          ┌────────────▼──────────────┐
          │  Exit Maintenance Mode    │
          │  Set-VMHost -State Conn   │
          └────────────┬──────────────┘
                       │
┌──────────────────────▼────────────────────────────────┐
│  POST-CHANGE VALIDATION                               │
│  ├── Host Connected in vCenter?                       │
│  ├── Hardware health: esxcli hardware health get      │
│  ├── Storage paths active: grep dead → 0              │
│  ├── vmnic uplinks up: esxcli network nic list        │
│  ├── NTP synced: esxcli system ntp get                │
│  └── No new vCenter alarms or vmkernel errors         │
└───────────────────────────────────────────────────────┘
```

## Change Readiness

- [ ] vMotion tested and working between affected hosts before any maintenance
- [ ] Host not in maintenance mode — no other concurrent work on same host
- [ ] HA admission control checked: cluster has capacity to tolerate host loss
- [ ] All storage paths healthy and no dead paths: `esxcli storage core path list | grep dead`
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

## Maintenance Window

1. Confirm host is healthy and not already in maintenance mode: `Get-VMHost | Select Name,ConnectionState`
2. Check HA admission control — ensure cluster can tolerate one less host during maintenance
3. Put host into maintenance mode: `Set-VMHost -VMHost <hostname> -State Maintenance`
4. Wait for all VMs to vMotion off the host — monitor via vCenter Tasks pane
5. Confirm zero VMs running on the host: `Get-VM -Location <host> | Where-Object {$_.PowerState -eq "PoweredOn"}`
6. Perform the required maintenance work (patching, hardware replacement, config change)
7. Exit maintenance mode: `Set-VMHost -VMHost <hostname> -State Connected`
8. Validate host is Connected, all storage paths active, NTP in sync, and VMs have migrated back

## Post-Change Validation

- [ ] Host shows Connected and PoweredOn in vCenter
- [ ] No hardware health alarms triggered: `esxcli hardware health get`
- [ ] All storage paths active, no dead paths: `esxcli storage core path list | grep dead`
- [ ] All vmnic uplinks connected: `esxcli network nic list`
- [ ] VMs running correctly on the host or successfully migrated back
- [ ] NTP synchronized: `esxcli system ntp get` confirms `Running: true`
- [ ] No new vCenter alarms or vmkernel errors introduced by the change
- [ ] Close change ticket with validation evidence attached

## Incident Triage

- [ ] Check host connection state in vCenter — Connected, Disconnected, or Not Responding?
- [ ] Run `esxcli hardware health get` — identify any hardware component in Warning or Error state
- [ ] Check storage paths: `esxcli storage core path list | grep dead`
- [ ] Check network uplinks: `esxcli network nic list` — look for down links
- [ ] Review vmkernel log: `tail -500 /var/log/vmkernel.log`
- [ ] Check NTP status — a drifted clock can cause certificate and auth failures
- [ ] Review vCenter events for the affected host around the incident time
- [ ] If host is Not Responding, attempt IPMI/iDRAC/iLO console access

| Question | Answer |
|---|---|
| Host connection state? | Connected / Disconnected / Not Responding |
| Hardware health alerts? | `esxcli hardware health get` |
| Dead storage paths? | `esxcli storage core path list \| grep dead` |
| vmnic uplinks down? | `esxcli network nic list` |
| vmkernel.log at incident time? | `/var/log/vmkernel.log` — SCSI, NMP, network errors |
