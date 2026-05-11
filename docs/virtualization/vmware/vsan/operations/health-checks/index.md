# vSAN — Health Checks

## Daily Checks

| Check | Command / Location | Notes |
|---|---|---|
| Cluster health summary | `Get-VsanClusterHealthSummary` | All tests should return green |
| Object health | vCenter → vSAN → Monitor → Virtual Objects | Flag any inaccessible or degraded objects |
| Disk groups | `Get-VsanDiskGroup` | All healthy; no drives evacuating or absent |
| Resync status | vCenter → vSAN → Monitor → Resyncing Objects | Confirm no unexpected resync in progress |
| Capacity per host | vCenter → vSAN → Monitor → Capacity | Flag hosts above 70% |
| Witness appliance (2-node/stretched) | Ping / vCenter | Confirm reachable |
| Performance dashboard | vCenter → vSAN → Monitor → Performance | Review for latency or throughput anomalies |

```powershell
# PowerCLI vSAN health sweep
Get-VsanClusterHealthSummary -Cluster (Get-Cluster) | Select -ExpandProperty Groups | Select GroupName,GroupHealth
Get-VsanDiskGroup | Select VMHost,State,@{N='DiskCount';E={$_.Disks.Count}}
```

---

## Weekly Checks

| Check | Command / Location | Notes |
|---|---|---|
| Storage policy compliance | vCenter → vSAN → Monitor → Virtual Objects → filter Non-Compliant | All objects should be compliant; non-compliant triggers resync |
| Capacity trend | vCenter → vSAN → Monitor → Capacity → Capacity History | Identify growth trends; flag if projected to hit 70% within 30 days |
| Resync history | vCenter → vSAN → Monitor → Resyncing Objects → History | Confirm all resyncs completed; flag any that are stalled or recurring |
| vSAN health test detail | vCenter → vSAN → Monitor → Skyline Health | Expand any yellow/red items; review recommended actions |
| Software version alignment | `esxcli system version get` on each host | All hosts in a cluster must run the same ESXi build |

```powershell
# Check policy compliance across all VMs
Get-VM | Get-SpbmEntityConfiguration | Where-Object {$_.ComplianceStatus -ne "compliant"} | Select Name,ComplianceStatus

# Cluster capacity summary
Get-VsanSpaceUsage -Cluster (Get-Cluster) | Select FreeSpaceGB,TotalCapacityGB,UsedSpaceGB
```

---

## Performance Baseline

Normal operating ranges for a healthy vSAN cluster. Values vary by workload — establish a baseline during steady-state and alert on deviation.

| Metric | Typical Healthy Range | Investigate If |
|---|---|---|
| Read latency (all-flash OSA) | < 1 ms | > 5 ms sustained |
| Write latency (all-flash OSA) | < 2 ms | > 10 ms sustained |
| Read latency (ESA) | < 0.5 ms | > 2 ms sustained |
| Write latency (ESA) | < 1 ms | > 5 ms sustained |
| Cache read hit ratio (OSA) | > 90% (all-flash has no read cache — N/A) | < 70% on hybrid OSA |
| Resync throughput | 0 MB/s during steady state | > 0 sustained without active maintenance |
| Congestion | 0 | Any non-zero value |

```bash
# Per-host latency and IOPS from ESXi shell
esxcli vsan perf query -e host-domclient -st 2024-01-01T00:00:00
```

---

## Network Health

| Check | Command | Expected Result |
|---|---|---|
| MTU end-to-end (9000) | `vmkping -I vmk2 -d -s 8972 <remote-vmk-ip>` | 100% success; any loss = MTU mismatch |
| vSAN vmkernel reachability | `vmkping -I vmk2 <remote-vmk-ip>` | Reachable from all hosts to all hosts |
| NIOC reservation (if shared NICs) | vCenter → vDS → Configure → Network I/O Control | vSAN ≥ 50%, NSX TEP ≥ 25%, vMotion ≥ 25% |
| vSAN network latency | vCenter → vSAN → Monitor → Skyline Health → Network | All inter-host latency < 1 ms |

```bash
# Run from each host — test against all other vSAN vmk IPs
vmkping -I vmk2 -d -s 8972 <host2-vsan-ip>
vmkping -I vmk2 -d -s 8972 <host3-vsan-ip>
```

---

## Stretched Cluster Checks

Run these in addition to standard daily/weekly checks when managing a stretched cluster.

| Check | Command / Location | Notes |
|---|---|---|
| Witness reachability | vCenter → vSAN → Configure → Fault Domains | Witness must show Connected |
| Site balance | vCenter → vSAN → Monitor → Virtual Objects | Objects should have one component per site + witness |
| Inter-site latency | vCenter → vSAN → Monitor → Skyline Health → Network | Must be < 5 ms RTT; < 1 ms for latency-sensitive workloads |
| VM affinity alignment | vCenter → Cluster → Configure → VM/Host Groups | Confirm production VMs pinned to preferred site |
| Preferred site designation | vCenter → vSAN → Configure → Fault Domains | Confirm preferred site is set correctly |

```powershell
# Check witness appliance connectivity
Get-VsanView -Id "VsanVcStretchedClusterSystem-vsan-stretched-cluster-system" | %{$_.GetWitnessHosts($_.MoRef)}
```

---

## Change Readiness

Run before any host maintenance, upgrade, or cluster configuration change.

| Item | Status | Command / Location |
|---|---|---|
| All health tests green | | `Get-VsanClusterHealthSummary` |
| No active resync | | vCenter → vSAN → Resyncing Objects |
| Disk group capacity < 70% per host | | vCenter → vSAN → Monitor → Capacity |
| No other hosts in maintenance mode | | One host at a time only |
| Full data migration selected | | Select "Full Data Migration" — not "Ensure Accessibility" |
| Change window approved | | Ticket reference |

- [ ] All vSAN health tests green before any host maintenance
- [ ] No active resync in progress — wait for resync to complete first
- [ ] Disk group capacity headroom confirmed — at least 30% free per host
- [ ] No hosts currently in maintenance mode
- [ ] Full data migration selected when putting host into maintenance
- [ ] Change window approved; storage admin and compute team notified
