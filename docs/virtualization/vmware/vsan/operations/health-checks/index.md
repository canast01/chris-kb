# vSAN — Health Checks


<div class="kb-summary">
Health Checks reference covering Weekly Checks, Performance Baseline, Network Health, Stretched Cluster Checks, Change Readiness.
</div>

```text
vSAN HEALTH CHECK SCOPE

  ┌───────────────────────────────────────────────────────┐
  │                   vSAN Cluster                        │
  │                                                       │
  │  ┌─────────────────────────────────────────────────┐  │
  │  │  Cluster-Level Checks                           │  │
  │  │  ├── vSAN partition / membership (CMMDS)        │  │
  │  │  ├── Software version alignment (all hosts)     │  │
  │  │  ├── Time drift (< 500 ms required)             │  │
  │  │  └── Capacity (< 70% alert, < 80% escalate)     │  │
  │  └─────────────────────────────────────────────────┘  │
  │                                                       │
  │  ┌─────────────────────────────────────────────────┐  │
  │  │  Host-Level Checks (per ESXi host)              │  │
  │  │  ├── vSAN vmkernel tagged and reachable         │  │
  │  │  ├── MTU 9000 end-to-end (vmkping -d -s 8972)  │  │
  │  │  ├── Disk group state (healthy / degraded)      │  │
  │  │  └── NIC errors / link speed                    │  │
  │  └─────────────────────────────────────────────────┘  │
  │                                                       │
  │  ┌─────────────────────────────────────────────────┐  │
  │  │  Object-Level Checks                            │  │
  │  │  ├── All objects healthy (no absent components) │  │
  │  │  ├── Storage policy compliance                  │  │
  │  │  └── Resync queue: 0 bytes remaining (idle)     │  │
  │  └─────────────────────────────────────────────────┘  │
  └───────────────────────────────────────────────────────┘
           │
           ▼
  Skyline Health (vCenter UI) + esxcli vsan health cluster list
```
```
┌──────────────────────────────────────── vSAN — Health Checks ─────────────────────────────────────────┐
│                                                                                                       │
│  vSAN health checks verify cluster, network, disk, and object health; run daily                       │
│  via the vSAN Health UI or Test-VsanClusterHealth PowerCLI cmdlet.                                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Cluster Health                │  │                Network Health               │   │
│   │         All hosts: member of cluster         │  │             vSAN MTU test: 9000             │   │
│   │             No host disconnected             │  │          Latency <1ms host to host          │   │
│   │        Witness reachable (stretched)         │  │            No multicast required            │   │
│   │         No decommission in progress          │  │            Unicast agent running            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Cluster and network health are prerequisites; disk and object health depend on them.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Disk & Object Health             │  │               Capacity Health               │   │
│   │            All disks: healthy/OK             │  │            Free space >30% total            │   │
│   │            No degraded components            │  │               Resync ETA <24h               │   │
│   │           Policy compliance: 100%            │  │           No dedup overhead alarm           │   │
│   │           Resync: 0 bytes pending            │  │          Capacity per host balanced         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Physical disk health reported via SMART; failed disk shows degraded component;                       │
│  replace disk within 60 minutes to avoid data loss window.                                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Degraded      = component lost; vSAN has no redundancy until rebuilt                                 │
│  Absent        = component temporarily missing; wait 60min before rebuild                             │
│  Resync        = rebuilding missing components after host/disk failure                                │
│  Policy compliance= all VMs must meet FTT policy; red = risk                                          │
│  MTU test      = vSAN sends 8972-byte pings to test jumbo frames end-to-end                           │
│  Unicast agent = replaced multicast in vSAN 6.6+; always check running                                │
│  SMART         = disk self-monitoring; pre-failure indicator                                          │
│  Decommission  = remove host from vSAN while migrating data; slow                                     │
│  60-min timer  = vSAN waits 60 min before marking absent as degraded                                  │
│  Witness (stretched)= third-site VM; heartbeat must be <200ms RTT                                     │
│  Free 30%      = vSAN needs headroom for resync; alert at <25%                                        │
│  Resync ETA    = estimate shown in vSAN performance health panel                                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash

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
