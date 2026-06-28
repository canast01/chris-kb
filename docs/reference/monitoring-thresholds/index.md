---
title: "Monitoring & Alert Thresholds Reference"
tags:
  - monitoring
  - operations
  - architecture
  - vmware
  - storage
---

<!-- kb-summary-start -->
Standard alert thresholds for compute, storage, network, and backup infrastructure. Use these as starting baselines — tune for your environment.
<!-- kb-summary-end -->

# Monitoring & Alert Thresholds Reference

---

```d2
direction: down

vmware_vsphere: "VMware vSphere" {shape: rectangle}
ontap: "ONTAP" {shape: rectangle}
pure_flasharray: "Pure FlashArray" {shape: rectangle}
veeam_backup: "Veeam Backup" {shape: rectangle}
network_nsx: "Network / NSX" {shape: rectangle}
fc_san: "FC / SAN" {shape: rectangle}

vmware_vsphere -> ontap: uses
ontap -> pure_flasharray: uses
pure_flasharray -> veeam_backup: uses
veeam_backup -> network_nsx: uses
network_nsx -> fc_san: uses
```

## VMware vSphere

### Host-Level Metrics

| Metric | Warning | Critical | Alert Action | SNMP/API Path |
|---|---|---|---|---|
| CPU Ready (ms/s) | >1000 | >2000 | Check VM density, add CPUs | `cpu.ready.summation` |
| CPU Co-Stop | >500 | >1000 | NUMA-aware scheduling | `cpu.costop.summation` |
| Memory Balloon | >0 | >5% RAM | Add RAM or vMotion VMs | `mem.vmmemctl.average` |
| Memory Swap | >0 | >100 MB/s | Critical: add RAM immediately | `mem.swapout.average` |
| Host CPU % | >70% avg | >90% avg | Add hosts or rebalance | `cpu.usagemhz.average` |
| Host Memory % | >80% | >90% | Add RAM / vMotion VMs | `mem.usage.average` |
| Disk Latency (ms) | >10 | >20 | Storage performance investigation | `disk.totalLatency.average` |

### Datastore Metrics

| Metric | Warning | Critical | Action |
|---|---|---|---|
| Datastore used % | >75% | >85% | Expand or add datastore |
| Datastore IOPS | >80% of array max | >90% | Add storage tier |
| Datastore latency | >15ms | >30ms | Check storage array |

### vSAN Specific

| Metric | Warning | Critical | Action |
|---|---|---|---|
| Slack space | <30% | <20% | Add capacity disk groups |
| Resync objects | >100 | >500 | Pause maintenance ops |
| Health check | Any warning | Any error | Follow vSAN health guide |

---

## ONTAP

| Metric | Warning | Critical | Action |
|---|---|---|---|
| Aggregate used % | >75% | >85% | Add disks or thin-reclaim |
| Volume used % | >80% | >90% | Expand or move |
| Node CPU % | >60% avg | >80% avg | Check workload distribution |
| SnapMirror lag | >2x schedule | >RPO target | Force update |
| Broken drives | Any | Any | Replace immediately |
| NVRAM battery | Any warning | — | Replace (data at risk) |
| Temp sensor | Any warning | — | Check cooling |

---

## Pure FlashArray

| Metric | Warning | Critical | Action |
|---|---|---|---|
| Array used % | >70% | >80% | Add shelves |
| Write IOPS | >80% max | >90% max | Tune workload or add capacity |
| Write latency | >1ms | >2ms | Check host path count |
| Drive state | Not Healthy | Failed | Replace drive |
| Controller failover | Any | — | Engage Pure support |
| SafeMode | Disabled | — | Re-enable immediately |

---

## Veeam Backup

| Metric | Warning | Critical | Action |
|---|---|---|---|
| Backup repo free | <20% | <10% | Extend or archive |
| Backup job success | <95% | <80% | Investigate failures |
| Restore point age | >24h | >48h | Retry failed jobs |
| Backup window | Exceeds window | Misses | Tune job concurrency |
| SureBackup result | Any warning | Any failure | Investigate immediately |

---

## Network / NSX

| Metric | Warning | Critical | Action |
|---|---|---|---|
| Uplink utilisation | >60% | >80% | Add uplinks or LAG |
| Packet loss | >0.1% | >1% | Check physical layer |
| DFW denied connections | Sudden spike | — | Security investigation |
| BGP peer state | Idle | Down | Check underlay routing |
| MTU mismatch | — | Any | Fix VXLAN/NFS MTU |

---

## FC / SAN

| Metric | Warning | Critical | Action |
|---|---|---|---|
| FC port utilisation | >60% | >80% | Add ISLs |
| CRC errors | Any | — | Check cable/SFP |
| FC login failures | Any pattern | — | Zoning investigation |
| FLOGI timeout | Any | — | Check fabric health |

---

## General Principles

- **Alert fatigue**: if >10 alerts/day are "normal", recalibrate thresholds
- **Baseline first**: collect 2-4 weeks of data before setting warning thresholds
- **Trending > snapshot**: use 30-min averages, not instantaneous peaks for compute
- **Escalation matrix**: define who gets paged at Warning vs Critical before an incident

## See Also

- [Capacity Planning](../capacity-planning/index.md)
- [Incident Response](../incident-response/index.md)
