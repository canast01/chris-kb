# RecoverPoint — How It Works

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
```

## Consistency Group Commands

```bash
# SSH to RPA cluster management IP
ssh admin@<rpa-cluster-ip>

# All CGs and their current replication state
groups status

# Detailed CG state including RPO, lag, and journal utilization
groups status detail

# Create a manual bookmark before a patching window
group create_bookmark --gname <cg_name> --name "pre-patch-$(date +%Y%m%d)"

# Enable image access at a specific bookmark (DR test)
group enable-image-access --gname <cg_name> --copy DR --image <bookmark_name>

# Disable image access (return to replication)
group disable-image-access --gname <cg_name>

# Suspend / resume replication
group disable-replication --gname <cg_name>
group enable-replication --gname <cg_name>
```

## Journal Sizing

```text
Journal size (GB) = Write rate (MB/s) × 3600 × Retention hours / 1024

Example: 50 MB/s write rate, 4-hour retention
  50 × 3600 × 4 / 1024 = ~703 GB

Minimum recommended: 10× hourly write rate
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
