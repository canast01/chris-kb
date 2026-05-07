# Operations

> Part of the [vCenter](../) reference.

---

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| [ ] Confirm vCenter GUI is accessible and all VCSA services are health |  |  |
| [ ] Run `Get-Cluster | Select Name,DrsEnabled,HAEnabled` | `Get-Cluster | Select Name,DrsEnabled,HAEnabled` | DRS and HA enabled on all clusters |
| [ ] Run `Get-VMHost | Where-Object {$_.ConnectionState -ne "Connected" | `Get-VMHost | Where-Object {$_.ConnectionState -ne "Connected"}` | result should be empty; any non-connected hosts require investigation |
| [ ] Run `Get-VM | Where-Object {$_.PowerState -eq "PoweredOff"} | Wher | `Get-VM | Where-Object {$_.PowerState -eq "PoweredOff"} | Where-Object {$_.Notes -notmatch "intentional"}` | flag unexpected powered-off VMs |
| [ ] Run `Get-VM | Get-Snapshot | Where-Object {$_.Created -lt (Get-Dat | `Get-VM | Get-Snapshot | Where-Object {$_.Created -lt (Get-Date).AddDays(-3)}` | flag snapshots older than 3 days |
| [ ] Check vCenter alarms dashboard |  | no critical unacknowledged alarms outstanding |
| [ ] Check certificate expiry for VCSA and ESXi hosts |  | flag any expiring within 60 days |
| [ ] Review vCenter Monitor → Tasks for recent task failures or error-s |  |  |

## Health Check

- [ ] All VCSA services running: VAMI → Services, all in Started state
- [ ] All ESXi hosts connected: `Get-VMHost | Select Name,ConnectionState`
- [ ] DRS and HA active on all clusters: `Get-Cluster | Select Name,DrsEnabled,HAEnabled`
- [ ] No critical unacknowledged vCenter alarms
- [ ] No recent error-level events: `Get-VIEvent -MaxSamples 100 -Type Error`
- [ ] Certificate validity confirmed for VCSA and hosts
- [ ] vCenter REST API responding: `GET /api/vcenter/health/system`
- [ ] SSO/PSC health confirmed via VAMI

```bash
# PowerCLI health checks
Get-VMHost | Select Name,ConnectionState,PowerState
Get-Cluster | Select Name,DrsEnabled,HAEnabled,HAEnabled
Get-VIEvent -MaxSamples 100 -Type Error | Select CreatedTime,FullFormattedMessage
Get-VM | Get-Snapshot | Where-Object {$_.Created -lt (Get-Date).AddDays(-3)} | Select VM,Name,Created

# vCenter REST API (run from jump host with valid session)
curl -sk -u 'administrator@vsphere.local' https://<vcenter>/api/vcenter/health/system
```

## Change Readiness

- [ ] vCenter backup is current — file-based backup or VAMI snapshot completed and verified
- [ ] No active DRS migrations in progress: confirm vCenter Tasks pane is idle
- [ ] HA admission control capacity checked: cluster can tolerate intended host changes
- [ ] Certificates valid for more than 30 days — do not proceed if expiry is imminent
- [ ] SSO and PSC health confirmed before any appliance-level change
- [ ] Rollback plan documented: VCSA restore procedure confirmed and tested
- [ ] Change window approved and communicated to all dependent teams

| Item | Status | Notes |
|---|---|---|
| vCenter backup current | | Backup timestamp confirmed |
| No active DRS migrations | | Tasks pane idle |
| HA admission control OK | | Cluster capacity headroom |
| Certificates valid > 30 days | | Earliest expiry date |
| Change window approved | | Ticket reference |

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

## Maintenance Window

1. Take a VCSA backup via VAMI → Backup, or snapshot the VCSA VM if running virtualized
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
