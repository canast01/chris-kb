---
tags:
  - architecture
  - dell
---
# RecoverPoint — How It Works


<div class="kb-summary">
How It Works reference covering Overview, Topology, Journal Sizing, Journal Monitoring Thresholds, High Availability.

*Applies to: RecoverPoint 5.x*
</div>
![RecoverPoint — How It Works](../../../../assets/storage-dell-recoverpoint-architecture-how-it-works.svg)


```d2
direction: right

center: "RecoverPoint" {shape: hexagon}
topology: "Topology" {shape: rectangle}
journal_monitoring_thresholds: "Journal Monitoring Thresholds" {shape: rectangle}
high_availability: "High Availability" {shape: rectangle}

center -> topology
center -> journal_monitoring_thresholds
center -> high_availability
```

## Overview

Dell EMC RecoverPoint provides continuous data protection (CDP) and continuous remote replication (CRR) through journal-based replication. RPA (RecoverPoint Appliance) clusters at each site intercept writes via splitters and maintain a rolling journal enabling point-in-time recovery to any point within the journal window. All volumes that must be recovered together are grouped into a Consistency Group (CG).

## Topology

```mermaid
graph LR
  RPA1["RPA Cluster\nSite A"] --> STG_A[("Storage A\nProduction LUNs")]
  RPA2["RPA Cluster\nSite B"] --> STG_B[("Storage B\nReplica + Journal")]
  RPA1 <-->|"WAN — compressed replication"| RPA2
  STG_A -->|"captured writes"| RPA1
  H_A(["Production Hosts"]) --> STG_A
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class RPA1 ctrl
  class RPA2 dr
  class STG_A,STG_B store
  class H_A host
```


| Environment Write Rate | Minimum Journal Size | Recommended Retention |
|---|---|---|
| < 10 MB/s | 50 GB | 8 hours |
| 10–50 MB/s | 200–750 GB | 4–8 hours |
| 50–200 MB/s | 750 GB – 3 TB | 2–4 hours |

## Journal Monitoring Thresholds

| Threshold | Action |
|---|---|
| > 70% | Warning alert; review write rate and link bandwidth |
| > 80% | Critical alert; plan immediate journal expansion |
| > 90% | Emergency; expand journal before replication halts |
| 100% | Replication halted; full resync required after expansion |

## High Availability

- RPA clusters operate active-active within a site; an RPA failure causes automatic redistribution of CGs to surviving RPAs
- Quorum is maintained within the cluster; loss of majority halts replication to protect data consistency
- Minimum 2 RPAs per cluster for HA; 4+ for large environments

---

## See also

- [Recoverpoint — Design Standards](design-standards/)
- [Recoverpoint — Integrations](integrations/)
- [Recoverpoint — Deploy](../deploy/)
