# Operations

> Part of the [vSAN](../) reference.

---

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| [ ] Run `Get-VsanClusterHealthSummary` | `Get-VsanClusterHealthSummary` | all health tests should return green; any yellow or red requires investigation |
| [ ] Check vSAN object health in vCenter → vSAN → Monitor → Virtual Obj |  | flag any inaccessible or degraded objects |
| [ ] Run `Get-VsanDiskGroup` | `Get-VsanDiskGroup` | all disk groups healthy, no drives in evacuating or absent state |
| [ ] vCenter → vSAN → Monitor → Resyncing Objects |  | confirm no resync is in progress from previous failure or change |
| [ ] Check capacity per host |  |  |
| [ ] Verify vSAN witness appliance is reachable (2-node or stretched cluster) |  |  |
| [ ] Review vSAN performance dashboard for latency or throughput anomal |  |  |
| [ ] Confirm vSAN Health Service is running and the health check data i |  |  |

## Health Check

- [ ] All vSAN health tests green: `Get-VsanClusterHealthSummary`
- [ ] No degraded or inaccessible VM objects
- [ ] All disk groups healthy and no evacuating drives: `Get-VsanDiskGroup`
- [ ] No active resync in progress
- [ ] Disk group capacity below 70% per host
- [ ] Witness appliance reachable (2-node/stretched)
- [ ] No performance anomalies in vSAN performance dashboard
- [ ] vSAN Health Service up to date

```powershell
# PowerCLI vSAN health sweep
Get-VsanClusterHealthSummary -Cluster (Get-Cluster) | Select -ExpandProperty Groups | Select GroupName,GroupHealth

Get-VsanDiskGroup | Select VMHost,State,@{N='DiskCount';E={$_.Disks.Count}}

# Check for degraded/inaccessible objects
Get-VsanView -Id "VsanObjectSystem-vsan-object-system" |
  ForEach-Object { $_.QueryVsanObjectUuidsByFilter($null, 100, 0) }
```

## Change Readiness

- [ ] All vSAN health tests green before any host maintenance: `Get-VsanClusterHealthSummary`
- [ ] No active resync in progress — wait for resync to complete before starting maintenance
- [ ] Disk group capacity headroom confirmed — at least 30% free per host after planned change
- [ ] No hosts currently in maintenance mode — only one host at a time for vSAN maintenance
- [ ] vSAN license valid and not expired
- [ ] Full data migration option selected when putting host into maintenance mode (not `Ensure Accessibility`)
- [ ] Change window approved; storage admin and compute team notified

| Item | Status | Notes |
|---|---|---|
| All health tests green | | `Get-VsanClusterHealthSummary` |
| No active resync | | vCenter → vSAN → Resyncing Objects |
| Disk group capacity OK | | < 70% per host |
| No other hosts in maintenance | | One host at a time |
| Change window approved | | Ticket reference |

## Incident Triage

- [ ] Run `Get-VsanClusterHealthSummary` — identify which health test(s) are failing and in which category
- [ ] Check disk group health: `Get-VsanDiskGroup` — look for absent, degraded, or evacuating disks
- [ ] Check vSAN network health in vSAN Health → Network — confirm VMkernel adapter connectivity between hosts
- [ ] Check vSAN object accessibility: vCenter → vSAN → Monitor → Virtual Objects — identify VMs with inaccessible objects
- [ ] Review ESXi vmkernel log on affected host for vSAN-related errors: `grep -i vsan /var/log/vmkernel.log`
- [ ] Check witness appliance health (2-node/stretched): confirm witness host is connected and its vSAN component is healthy
- [ ] Review resync status — degraded objects after a disk or host failure will show here
- [ ] If objects are permanently inaccessible and resync cannot start, escalate to VMware Support immediately

| Question | Answer |
|---|---|
| Which health tests are failing? | `Get-VsanClusterHealthSummary` — test name and status |
| Are disk groups healthy? | `Get-VsanDiskGroup` — absent or evacuating disks |
| Is the vSAN network healthy? | vSAN Health → Network category |
| Are any VM objects inaccessible? | vCenter → vSAN → Virtual Objects |
| What does vmkernel.log show? | `grep -i vsan /var/log/vmkernel.log` on affected host |

## Maintenance Window

1. Confirm all vSAN health tests are green and no resync is in progress before starting
2. Check disk group capacity — ensure remaining hosts have sufficient capacity after data migration
3. Put host into maintenance mode with **Full Data Migration** selected (not `Ensure Accessibility`)
4. Monitor resync progress: vCenter → vSAN → Monitor → Resyncing Objects — wait for resync to complete before proceeding to next host
5. Perform the required maintenance work on the evacuated host
6. Exit maintenance mode and wait for the host to rejoin the vSAN cluster
7. Confirm `Get-VsanClusterHealthSummary` returns all green and no resync is queued before touching the next host
8. Repeat for each host — never put more than one host into maintenance mode simultaneously

## Post-Change Validation

- [ ] All vSAN health tests green: `Get-VsanClusterHealthSummary`
- [ ] No resync in progress: vCenter → vSAN → Monitor → Resyncing Objects shows empty
- [ ] All disk groups healthy and online: `Get-VsanDiskGroup`
- [ ] All VM objects accessible: vCenter → vSAN → Monitor → Virtual Objects — no degraded or inaccessible state
- [ ] Disk group capacity within acceptable range per host
- [ ] vSAN network health confirmed green
- [ ] No new vmkernel errors on any vSAN host since change completed
- [ ] Close change ticket with health summary screenshot and resync status confirmation
