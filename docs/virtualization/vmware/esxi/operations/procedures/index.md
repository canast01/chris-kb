# ESXi — Procedures


<div class="kb-summary">
Procedures reference covering Change Readiness, Maintenance Window, Post-Change Validation, Incident Triage.
</div>

```
┌───────────────────────────────────── ESXi — Standard Procedures ──────────────────────────────────────┐
│                                                                                                       │
│  Maintenance mode, change control, and host decommission standard procedures.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Maintenance Mode Procedure          │  │              Change Management              │   │
│   │          Drain VMs via vMotion/DRS           │  │          Raise change request (CR)          │   │
│   │        Enter maintenance: vCenter UI         │  │          Pre-change health snapshot         │   │
│   │        esxcli system maintenanceMode         │  │          Maintenance window agreed          │   │
│   │         Verify no VMs remain on host         │  │            Post-change validation           │   │
│   │        Perform task, exit maintenance        │  │            Close CR with evidence           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Maintenance mode drains VMs; change control wraps every host-level change.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Host Decommission               │  │             Emergency Procedures            │   │
│   │           Migrate all VMs off host           │  │           Force maintenance if HA           │   │
│   │         Remove from vSAN disk group          │  │          PSOD: capture vmkernel log         │   │
│   │           Disconnect from vCenter            │  │          Isolate host from network          │   │
│   │             Remove from cluster              │  │            Power off affected VMs           │   │
│   │           Deregister from vCenter            │  │            Escalate to VMware GSS           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 host, iDRAC/IPMI for OOB control, management network, vCenter appliance                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Maintenance mode = host state; vCenter stops VM placement; drains existing                           │
│  vMotion     = live VM migration; used to drain host before maintenance                               │
│  PSOD        = Purple Screen Of Death; ESXi kernel panic / crash dump                                 │
│  CR          = Change Request; ITSM ticket authorising planned changes                                │
│  DRS         = Distributed Resource Scheduler; auto-migrates VMs                                      │
│  HA          = High Availability; restarts VMs on remaining hosts                                     │
│  Decommission= formal process to remove host from inventory and cluster                               │
│  iDRAC       = Dell OOB management; power control when host unresponsive                              │
│  vmkernel log= /var/log/vmkernel.log; primary diagnostic log on ESXi                                  │
│  vSAN evac   = removes host disks from vSAN before decommission                                       │
│  Force maint = maintenance without VM evacuation; HA failure scenario only                            │
│  Health snap = pre/post change comparison of alarms/metrics/log tail                                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── ESXi — Standard Procedures ──────────────────────────────────────┐
│                                                                                                       │
│  Maintenance mode, change control, and host decommission standard procedures.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Maintenance Mode Procedure          │  │              Change Management              │   │
│   │          Drain VMs via vMotion/DRS           │  │          Raise change request (CR)          │   │
│   │        Enter maintenance: vCenter UI         │  │          Pre-change health snapshot         │   │
│   │        esxcli system maintenanceMode         │  │          Maintenance window agreed          │   │
│   │         Verify no VMs remain on host         │  │            Post-change validation           │   │
│   │        Perform task, exit maintenance        │  │            Close CR with evidence           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Maintenance mode drains VMs; change control wraps every host-level change.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Host Decommission               │  │             Emergency Procedures            │   │
│   │           Migrate all VMs off host           │  │           Force maintenance if HA           │   │
│   │         Remove from vSAN disk group          │  │          PSOD: capture vmkernel log         │   │
│   │           Disconnect from vCenter            │  │          Isolate host from network          │   │
│   │             Remove from cluster              │  │            Power off affected VMs           │   │
│   │           Deregister from vCenter            │  │            Escalate to VMware GSS           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 host, iDRAC/IPMI for OOB control, management network, vCenter appliance                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Maintenance mode = host state; vCenter stops VM placement; drains existing                           │
│  vMotion     = live VM migration; used to drain host before maintenance                               │
│  PSOD        = Purple Screen Of Death; ESXi kernel panic / crash dump                                 │
│  CR          = Change Request; ITSM ticket authorising planned changes                                │
│  DRS         = Distributed Resource Scheduler; auto-migrates VMs                                      │
│  HA          = High Availability; restarts VMs on remaining hosts                                     │
│  Decommission= formal process to remove host from inventory and cluster                               │
│  iDRAC       = Dell OOB management; power control when host unresponsive                              │
│  vmkernel log= /var/log/vmkernel.log; primary diagnostic log on ESXi                                  │
│  vSAN evac   = removes host disks from vSAN before decommission                                       │
│  Force maint = maintenance without VM evacuation; HA failure scenario only                            │
│  Health snap = pre/post change comparison of alarms/metrics/log tail                                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
