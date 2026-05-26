# Superna Eyeglass — How It Works

## Overview

Superna Eyeglass is a DR orchestration platform purpose-built for NetApp PowerScale (Isilon). It automates the share, quota, and DNS reconfiguration steps that previously required hours of manual work during a SyncIQ failover. Eyeglass continuously monitors DR readiness and scores it at 100% only when all shares, exports, quotas, and DNS zones are aligned between primary and DR clusters.

## Component Topology

```mermaid
graph LR
  PS_A["PowerScale Cluster A\n(production)"] -->|"SyncIQ policy"| PS_B["PowerScale Cluster B\n(DR)"]
  EG["Superna Eyeglass\nDR Assistant"] -->|"monitors SyncIQ"| PS_A
  EG -->|"orchestrates failover\naccess zone migration"| PS_B
  ADMIN(["Admin"]) -->|"Eyeglass UI"| EG
  DNS(["DNS / AD\naccess zone cutover"]) <--> EG
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class PS_A ctrl
  class PS_B dr
  class EG mgmt
  class ADMIN,DNS host
```
```

RTO: typically 5–15 minutes for file services, depending on share count.

## DR Readiness Dashboard

Eyeglass continuously monitors and scores DR readiness at `https://<eyeglass-ip>` → DR → Readiness:

```text
DR Readiness Score = 100% when:
  ✓ All SyncIQ policies in sync state (not lagging beyond RPO threshold)
  ✓ All SMB shares mirrored on DR cluster
  ✓ All NFS exports mirrored on DR cluster
  ✓ All quotas aligned between primary and DR cluster
  ✓ DNS zones pre-configured for cutover
  ✓ Both Eyeglass appliances healthy and communicating
```

## Connectivity

| Traffic | Port | Notes |
|---|---|---|
| Eyeglass Admin UI | 443 (HTTPS) | From management network |
| PowerScale OneFS API | 8080 / 443 | From Eyeglass to each cluster |
| Eyeglass appliance sync | 9000 | Between primary and DR Eyeglass appliances |
| DNS management | 53, 445 | From Eyeglass to DNS servers |

## Key CLI Commands

```bash
# List all DR policies
egcli drpolicy list

# Status of all policies (replication state, lag, last test)
egcli drpolicy status --all

# Trigger a DR failover
egcli drfailover --policy POL-NAS-PROD --confirm

# Manually trigger a SyncIQ sync before planned failover
isi sync jobs start <synciq_policy_name>

# Check SyncIQ lag on production cluster
isi sync policies list | grep -E "Name|Last|Status"
```

## Sizing

| Environment | Eyeglass VM Size |
|---|---|
| < 500 shares | 4 vCPU, 8 GB RAM |
| 500–2,000 shares | 8 vCPU, 16 GB RAM |
| > 2,000 shares | 8 vCPU, 32 GB RAM |

## RPO Tiers

| Data Tier | SyncIQ Schedule | RPO Target | Alert Threshold |
|---|---|---|---|
| Tier 1 (critical file services) | Continuous | < 15 minutes | > 10 minutes lag |
| Tier 2 (departmental shares) | Every 4 hours | < 4 hours | > 3.5 hours lag |
| Tier 3 (archival) | Daily | < 24 hours | > 20 hours lag |
