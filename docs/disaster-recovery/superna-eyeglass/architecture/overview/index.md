# Superna Eyeglass — Architecture Overview

## Overview

Superna Eyeglass is a DR orchestration platform purpose-built for NetApp PowerScale (Isilon). It automates the share, quota, and DNS reconfiguration steps that previously required hours of manual work during a SyncIQ failover.

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

## DR Readiness Dashboard

Eyeglass continuously monitors and scores DR readiness:

```
DR Readiness Score = 100% when:
  ✓ All SyncIQ policies in sync state (not lagging beyond RPO threshold)
  ✓ All SMB shares mirrored on DR cluster
  ✓ All NFS exports mirrored on DR cluster
  ✓ All quotas aligned between primary and DR cluster
  ✓ DNS zones pre-configured for cutover
  ✓ Both Eyeglass appliances healthy and communicating
```

Access readiness dashboard: `https://<eyeglass-ip>` → DR → Readiness.

## Failover Execution Flow

When a failover is triggered:

1. Eyeglass breaks SyncIQ replication (makes DR cluster writable)
2. Reconfigures SMB shares and NFS exports on DR cluster to match primary settings
3. Applies quota policies on DR cluster
4. Executes DNS zone cutover (delegate authority to DR DNS entries)
5. Notifies operations via email/SNMP

RTO: typically 5–15 minutes for file services, depending on share count.

```mermaid
sequenceDiagram
    actor Admin
    participant EG as Eyeglass DR Assistant
    participant ProdPS as Production PowerScale
    participant DRPS as DR PowerScale
    participant DNS as DNS Server

    Admin->>EG: egcli drfailover --policy POL-NAS-PROD --confirm
    EG->>ProdPS: Pause / break SyncIQ replication
    ProdPS-->>EG: SyncIQ stopped
    EG->>DRPS: Activate access zones
    EG->>DRPS: Apply NFS exports + SMB shares
    EG->>DRPS: Apply quota policies
    EG->>DNS: Update SmartConnect zone delegation → DR VIPs
    DNS-->>EG: DNS updated
    EG-->>Admin: Failover complete — notify via SNMP/email
    Note over DRPS: Clients now resolve to DR cluster
```

## Appliance Sizing

| Environment | Eyeglass VM Size |
|---|---|
| < 500 shares | 4 vCPU, 8 GB RAM |
| 500–2,000 shares | 8 vCPU, 16 GB RAM |
| > 2,000 shares | 8 vCPU, 32 GB RAM (or contact Superna for sizing) |

## Networking

| Traffic | Port | Notes |
|---|---|---|
| Eyeglass Admin UI | 443 (HTTPS) | From management network |
| PowerScale OneFS API | 8080 / 443 | From Eyeglass to each cluster |
| Eyeglass appliance sync | 9000 | Between primary and DR Eyeglass appliances |
| DNS management | 53, 445 (Windows DNS WMI) | From Eyeglass to DNS servers |
