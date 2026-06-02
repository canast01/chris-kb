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

## Run This Routine

Paste this block into an ESXi host shell to get a full cluster health snapshot in under 2 minutes. Run from any host in the cluster.

```bash
echo "=== 1. Cluster membership ==="
esxcli vsan cluster get | grep -E "Member|Master|Sub-Cluster UUID|Health"

echo "=== 2. Overall health tests ==="
esxcli vsan health cluster get | grep -E "TestName|Health:" | grep -v "PASS"

echo "=== 3. Disk group state ==="
esxcli vsan storage list | grep -E "Disk Group UUID|Is SSD|Health|State|Tier"

echo "=== 4. Object health summary ==="
esxcli vsan debug object list | grep -v healthy | wc -l
echo "unhealthy objects (0 = all good)"

echo "=== 5. Resync queue ==="
esxcli vsan debug resync summary get

echo "=== 6. Capacity ==="
esxcli vsan storage list | grep -E "Used Capacity|Total Capacity|Free Capacity"

echo "=== 7. Non-compliant policy check ==="
esxcli vsan debug object list | grep -i "non-compliant"

echo "=== 8. Network MTU test (update IPs) ==="
vmkping -I vmk2 -d -s 8972 <host2-vsan-ip> -c 3 | grep -E "loss|received"
vmkping -I vmk2 -d -s 8972 <host3-vsan-ip> -c 3 | grep -E "loss|received"

echo "=== 9. NIC error check ==="
esxcli network nic stats get -n vmnic2 | grep -E "Errors|Dropped"

echo "=== Done ==="
```

**What to look for:**

| Section | Green | Investigate |
|---|---|---|
| Cluster membership | All hosts listed, one master | Any host missing |
| Health tests | All PASS | Any FAIL or WARN |
| Disk group state | All Healthy | Degraded or Error |
| Unhealthy objects | 0 | > 0 |
| Resync queue | 0 bytes remaining | > 0 — note ETA |
| Capacity | Used < 70% | > 70% — plan expansion |
| Non-compliant | No output | Any — see Procedures → Remediate |
| MTU test | 0% loss | Any loss — check switch MTU |
| NIC errors | 0 errors, 0 drops | Non-zero — check cabling |

---

## Disk Group Health

```bash
# List all disk groups — cache and capacity disks per host
esxcli vsan storage list | grep -E "Is SSD|Disk Group UUID|naa\.|Display Name|Tier|Health"

# Check SMART data on a specific disk (replace naa with actual device ID)
esxcli storage core device smart get -d naa.xxxxxxxxxxxxxxxx
# Reallocated Sectors, Pending Sectors, Uncorrectable Errors — any non-zero = failing disk

# Check for LSOM disk errors in kernel log
grep -i "lsom\|diskgroup" /var/log/vmkernel.log | grep -i "err\|fail" | tail -20

# Disk group congestion (should be 0 per group)
esxcli vsan debug disk list | grep -i "congestion\|Disk Group"
```

**Disk states to know:**

| State | Meaning | Action |
|---|---|---|
| Healthy | Normal operation | None |
| Degraded | Disk group has a failed component | Replace disk within 60 min window |
| Absent | Component temporarily missing (host rebooted etc.) | Wait 60 min; if no recovery, replace |
| Error | LSOM-level I/O error on disk | Immediate — check SMART data, replace |

---

## Object Health

```bash
# Count of objects by health state
esxcli vsan debug object list | awk '{print $NF}' | sort | uniq -c | sort -rn

# List all non-healthy objects with UUIDs
esxcli vsan debug object list | grep -v "Healthy"

# Show detail for a specific object (get UUID from above)
esxcli vsan debug object get -u <object-uuid>

# List all absent components (quick degradation indicator)
esxcli vsan debug component list | grep -i "absent"

# Resync detail — which objects are currently rebuilding
esxcli vsan debug resync list
```

**Object states:**

| State | Meaning | Action |
|---|---|---|
| Healthy | Policy met, all components accessible | None |
| Degraded | One component lost; no redundancy | Monitor — rebuild should start within 60 min |
| Absent | Component host is offline temporarily | Wait for host to return; set repair timer appropriately |
| Non-compliant | Policy cannot be met (capacity/host count) | See Procedures → Remediate Non-Compliant Objects |
| Inaccessible | All copies unavailable — VMs offline | P1 — escalate immediately |

---

## Skyline Health Categories

Skyline Health in vCenter groups all checks into categories. The most important ones:

**From vCenter UI:** Cluster → Monitor → vSAN → Skyline Health

| Category | Key checks | Common failures |
|---|---|---|
| Cluster | Cluster membership, software version, time config | Host disconnected, version mismatch, NTP drift |
| Network | MTU, multicast/unicast, host connectivity | MTU mismatch on switch, vmk tag missing |
| Physical disk | Capacity remaining, disk health, HCL status | Disk not on HCL, capacity > 75%, SMART warn |
| Data | Object health, policy compliance, resync | Non-compliant VMs, high resync queue |
| Performance | Latency, IOPS, throughput baseline | Cache pressure, congestion > 0 |
| vSAN build recommendation | Known issues for current version | Apply recommended patches |
| Limits | Hosts, disk groups, VMs per cluster | Approaching vSAN cluster maximums |
| Encryption | KMS connectivity, key status | KMS unreachable, key rotation needed |

Run `Get-VsanClusterHealthSummary -Cluster (Get-Cluster "VSAN-LON-01") -FetchFromCache:$false` in PowerCLI for a full programmatic health report.

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
