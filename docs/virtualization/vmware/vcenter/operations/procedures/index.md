# vCenter — Procedures

## Incident Triage

- [ ] Check vCenter services via VAMI → Services — identify any stopped or failed services
- [ ] Check SSO / PSC health — authentication failures often root-cause in SSO component
- [ ] Review vCenter logs: `/var/log/vmware/vpxd/vpxd.log` on VCSA for errors at incident time
- [ ] Check database health — VCSA embedded Postgres: `service-control --status vmware-vpostgres`
- [ ] Review vCenter events for the affected objects: `Get-VIEvent -Entity <cluster/host/vm> -MaxSamples 200`
- [ ] Check certificate validity — expired cert causes cascading authentication and agent failures
- [ ] Verify network connectivity to VCSA — DNS resolution, vCenter FQDN reachable from hosts
- [ ] Escalate to VMware Support if VPXD service cannot be restarted or database corruption suspected

| Question | Answer |
|---|---|
| Which VCSA services are stopped? | VAMI → Services — identify failed service |
| Is SSO/PSC healthy? | VAMI → SSO, or check `lookupservice` log |
| What does vpxd.log show? | `/var/log/vmware/vpxd/vpxd.log` at incident time |
| Are certificates valid? | VAMI → Certificate Management — check expiry |
| Can hosts connect to vCenter? | Host agent log: `/var/log/vmware/hostd.log` on ESXi |

## Maintenance Window Procedure

1. Take a VCSA backup via VAMI → Backup, or snapshot the VCSA VM if running virtualised
2. Confirm no active DRS migrations or critical tasks running in vCenter
3. Notify all teams that vCenter will be unavailable during maintenance — workloads remain running on ESXi
4. If performing VCSA update: follow the VAMI → Update workflow; do not interrupt mid-update
5. After update or change, verify all VCSA services have started: VAMI → Services, all in Started state
6. Test PowerCLI connection: `Connect-VIServer -Server <vcenter>` — confirm connection succeeds
7. Validate all ESXi hosts are Connected: `Get-VMHost | Where-Object {$_.ConnectionState -ne "Connected"}`
8. Confirm DRS and HA are active, no new alarms, and tasks are processing normally

## Post-Change Validation

- [ ] All VCSA services running: VAMI → Services shows all Started
- [ ] All ESXi hosts Connected: `Get-VMHost | Where-Object {$_.ConnectionState -ne "Connected"}` returns empty
- [ ] DRS and HA active on all clusters: `Get-Cluster | Select Name,DrsEnabled,HAEnabled`
- [ ] No critical unacknowledged alarms in vCenter
- [ ] PowerCLI connection successful: `Connect-VIServer` completes without error
- [ ] vCenter REST API responding: `GET /api/vcenter/health/system` returns GREEN
- [ ] No new vpxd.log errors introduced by the change
- [ ] Close change ticket with VAMI service status screenshot and PowerCLI connection confirmation

## Restarting Services Safely

Only restart services after checking disk space and reviewing recent changes.

```bash
# Check disk space first
df -h

# Restart one service at a time where possible
service-control --restart vpxd

# Full restart (causes brief vCenter unavailability)
service-control --stop --all
service-control --start --all
```

## Inventory Hygiene Tasks

```powershell
# Find all orphaned / unexpectedly powered-off VMs
Get-VM | Where-Object { $_.PowerState -eq "PoweredOff" } |
    Select-Object Name, @{N="Host";E={$_.VMHost.Name}},
    @{N="LastChange";E={$_.ExtensionData.Config.ChangeVersion}}

# Find VMs needing disk consolidation
Get-VM | Where-Object { $_.ExtensionData.Runtime.ConsolidationNeeded } | Select-Object Name

# Find all snapshots older than 7 days
Get-VM | Get-Snapshot |
    Where-Object { $_.Created -lt (Get-Date).AddDays(-7) } |
    Select-Object @{N="VM";E={$_.VM.Name}}, Name, Created,
    @{N="SizeGB";E={[math]::Round($_.SizeGB, 2)}}

# Export full VM inventory
Get-VM | Select-Object Name, PowerState, NumCpu, MemoryGB,
    @{N="VMHost";E={$_.VMHost.Name}},
    @{N="Cluster";E={$_.VMHost.Parent.Name}},
    @{N="Datastore";E={($_ | Get-Datastore).Name -join ";"}} |
    Export-Csv -Path vm_inventory.csv -NoTypeInformation
```
