# vSAN — Health Checks

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| [ ] Cluster health summary | `Get-VsanClusterHealthSummary` | All tests should return green |
| [ ] Object health | vCenter → vSAN → Monitor → Virtual Objects | Flag any inaccessible or degraded objects |
| [ ] Disk groups | `Get-VsanDiskGroup` | All healthy; no drives evacuating or absent |
| [ ] Resync status | vCenter → vSAN → Monitor → Resyncing Objects | Confirm no unexpected resync in progress |
| [ ] Capacity per host | vCenter → vSAN → Monitor → Capacity | Flag hosts above 70% |
| [ ] Witness appliance (2-node/stretched) | Ping / vCenter | Confirm reachable |
| [ ] Performance dashboard | vCenter → vSAN → Monitor → Performance | Review for latency or throughput anomalies |

## Health Checklist

- [ ] All vSAN health tests green
- [ ] No degraded or inaccessible VM objects
- [ ] All disk groups healthy and no evacuating drives
- [ ] No active resync in progress
- [ ] Disk group capacity below 70% per host
- [ ] Witness appliance reachable (2-node/stretched)
- [ ] No performance anomalies

```powershell
# PowerCLI vSAN health sweep
Get-VsanClusterHealthSummary -Cluster (Get-Cluster) | Select -ExpandProperty Groups | Select GroupName,GroupHealth

Get-VsanDiskGroup | Select VMHost,State,@{N='DiskCount';E={$_.Disks.Count}}
```

## Change Readiness

- [ ] All vSAN health tests green before any host maintenance
- [ ] No active resync in progress — wait for resync to complete first
- [ ] Disk group capacity headroom confirmed — at least 30% free per host
- [ ] No hosts currently in maintenance mode — only one host at a time
- [ ] Full data migration selected when putting host into maintenance (not `Ensure Accessibility`)
- [ ] Change window approved; storage admin and compute team notified

| Item | Status | Notes |
|---|---|---|
| All health tests green | | `Get-VsanClusterHealthSummary` |
| No active resync | | vCenter → vSAN → Resyncing Objects |
| Disk group capacity OK | | < 70% per host |
| No other hosts in maintenance | | One host at a time |
| Change window approved | | Ticket reference |
