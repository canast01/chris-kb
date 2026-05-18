# Cluster Standard

> Part of the [Standards](../) reference.

---

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     Cluster Standard — Config Baseline                   │
├───────────────────────────────┬──────────────────────────────────────────┤
│   vSphere HA                  │   DRS                                    │
│                               │                                          │
│  Enabled: Yes                 │  Enabled: Yes                            │
│  Host Monitoring: On          │  Automation: Fully Automated (prod)      │
│  Admission Control: n+1 (25%) │  Migration Threshold: Priority 3+        │
│  VM Monitoring: On (prod)     │  Predictive DRS: On (if Aria integrated) │
│  Heartbeat DSs: ≥ 2           │                                          │
├───────────────────────────────┴──────────────────────────────────────────┤
│   EVC: Enabled (lowest CPU baseline in cluster)                          │
│   vSAN: RAID-1 FTT=1 min │ Dedup+Compress On (all-flash) │ Health green  │
│   Resource Pools: rp-prod-critical │ rp-prod-standard │ rp-dev           │
│   Min hosts: 3 (prod/mgmt/DR)  │  2 (edge/NSX only)                      │
└──────────────────────────────────────────────────────────────────────────┘
```
## Overview

This standard defines the minimum required configuration for all vSphere clusters in the production environment. Any new cluster must meet these requirements before workloads are placed on it.

## Minimum Host Count

| Cluster Type | Minimum Hosts | Recommended |
|---|---|---|
| Production compute | 3 | 4+ |
| Management cluster | 3 | 3 |
| Edge cluster (NSX) | 2 | 2 |
| DR compute | 3 | 4 |

A minimum of 3 hosts is required for any cluster running vSAN with FTT=1 (RAID-1 mirroring). Two-host clusters are only permitted for edge/NSX clusters with no vSAN.

## vSphere HA

HA must be enabled on all production and DR clusters.

| Setting | Required Value |
|---|---|
| vSphere HA | Enabled |
| Host Monitoring | Enabled |
| Admission Control | Enabled |
| Admission Control Policy | Reserve `n+1` host capacity (percentage-based) |
| VM Monitoring | VM and Application Monitoring enabled (production) |
| Heartbeat Datastores | At least 2 heartbeat datastores configured |

For clusters with 3–4 hosts, configure admission control to reserve 25% of cluster resources (equivalent to 1 host). For clusters with 5+ hosts, 20% is acceptable.

## DRS

| Setting | Required Value |
|---|---|
| DRS | Enabled |
| Automation Level | Fully Automated (production compute) |
| Migration Threshold | Apply priority 3 recommendations and above |
| Predictive DRS | Enabled (if Aria Operations integrated) |

Management and edge clusters may use Partially Automated DRS where workload placement is more controlled.

## EVC (Enhanced vMotion Compatibility)

EVC must be enabled on all clusters containing mixed-generation CPU hardware. Set EVC to the lowest CPU baseline present in the cluster.

| CPU Generation | EVC Mode |
|---|---|
| Intel Skylake / Cascade Lake | Intel "Skylake" Generation |
| Intel Ice Lake / Sapphire Rapids | Intel "Icelake" Generation |
| AMD EPYC Rome | AMD EPYC Rome Generation |

If all hosts are identical hardware generation, EVC should still be enabled to prevent future compatibility issues when adding newer hardware.

## vSAN (for vSAN-enabled clusters)

| Setting | Required Value |
|---|---|
| Deduplication and Compression | Enabled (all-flash only) |
| Default Storage Policy | RAID-1 FTT=1 (minimum) |
| vSAN Health Checks | All enabled |
| Proactive Tests | Performance test run quarterly |
| Skyline Health | Green before workload placement |

## Resource Pools

Do not use a single default resource pool for all VMs. Define resource pools aligned to application tiers or environments:

- `rp-prod-critical` — Reservations for tier-1 workloads
- `rp-prod-standard` — Standard production workloads
- `rp-dev` — Development workloads (shares, no reservations)

## New Cluster Checklist

- [ ] Minimum host count met
- [ ] HA enabled with admission control
- [ ] DRS set to Fully Automated
- [ ] EVC enabled at correct baseline
- [ ] vSAN health green (if applicable)
- [ ] Cluster name follows naming standard
- [ ] Environment and owner tags applied
- [ ] Resource pools created
- [ ] Cluster added to monitoring platform
- [ ] Cluster listed in cluster inventory
- [ ] Change record closed with post-validation evidence
