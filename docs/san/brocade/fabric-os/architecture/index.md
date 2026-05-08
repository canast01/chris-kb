# Brocade Fabric OS — Architecture

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="overview/">
  <strong>Overview</strong>
  <span>Architecture overview, topology, and how it fits in the stack.</span>
</a>

<a class="kb-card" href="components/">
  <strong>Components</strong>
  <span>Core services, ports, dependencies, and internals.</span>
</a>

<a class="kb-card" href="integrations/">
  <strong>Integrations</strong>
  <span>Integration with other platforms and services.</span>
</a>

<a class="kb-card" href="standards/">
  <strong>Standards</strong>
  <span>Naming conventions, design rules, and configuration baselines.</span>
</a>

</div>

> Part of the [Brocade Fabric OS](../) reference.

---
## SAN Fabric Topology

```mermaid
graph TB
  H1(["ESXi-01\nHBA0 · HBA1"]) & H2(["ESXi-02\nHBA0 · HBA1"]) --> DIRA["Brocade Director A\n(Fabric A)"]
  H1 & H2 --> DIRB["Brocade Director B\n(Fabric B)"]
  DIRA <-->|"ISL — 10/40 Gbps"| DIRC["Brocade Director C\n(Fabric A — DR)"]
  DIRB <-->|"ISL — 10/40 Gbps"| DIRD["Brocade Director D\n(Fabric B — DR)"]
  DIRA & DIRB --> FA[("FlashArray")]
  DIRC & DIRD --> PM[("PowerMax")]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class DIRA,DIRB,DIRC,DIRD ctrl
  class FA,PM store
  class H1,H2 host
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="fabric-os/">
  <strong>Fabric OS</strong>
  <span>Switch CLI, zoning, ports, ISLs, firmware, and diagnostics.</span>
</a>

<a class="kb-card" href="sannav/">
  <strong>SANnav</strong>
  <span>Fabric management, alerts, inventory, monitoring, and reporting.</span>
</a>

</div>

## Overview

Fabric OS (FOS) runs on Brocade/Broadcom SAN switches. Fabrics are deployed in a core-edge topology with ISLs (trunked) connecting edge switches to core directors. One switch per fabric is elected as the **principal switch**, which owns the fabric name server and manages domain ID assignments.

---

## Platform Reference

| Platform | Type | Max Ports | Notes |
|---|---|---|---|
| G620 | Fixed | 64x 32G FC | Mid-range |
| G720 | Fixed | 64x 64G FC | High-performance fixed |
| X7-4 | Director | Up to 192 FC | 4-slot director |
| X7-8 | Director | Up to 384 FC | 8-slot director |
| 6510 | Fixed | 48x 16G FC | End-of-sale — plan migration |

Directors (X7-4 / X7-8) support non-disruptive firmware upgrades (HA chassis with dual CPs).

---

## Fabric Design

Standard dual-fabric design:

```
Fabric A:  Host HBA Port 0 → G620-SW01 → Storage Target (Fabric A ports)
Fabric B:  Host HBA Port 1 → G620-SW02 → Storage Target (Fabric B ports)
```

Each fabric is independent. ISLs form trunk groups between switches within a fabric — not between Fabric A and Fabric B.

**Trunk groups:** Brocade ISL trunks group multiple physical ISL links into a single logical ISL for bandwidth aggregation and resilience. All links in a trunk must be same speed and between the same pair of switches.

---

## Port Types

| Port Type | Role |
|---|---|
| E_Port | ISL — connects to another switch |
| F_Port | Fabric port — connects to host HBA or storage target |
| N_Port | Node port — on the host or storage device |
| D_Port | Diagnostic port — used for link health tests |
| EX_Port | Extended E_Port — used for FC Routing between fabrics |

```bash
# Check port type and state
portshow <port-number>

# Check all ports
switchshow

# Show detailed port statistics
portstatsshow <port-number>
```

---

## Principal Switch and Domain ID

One switch per fabric is the principal switch, elected by lowest WWN (by default) or by priority setting.

```bash
# Show current principal switch
fabricshow
# The principal switch has a ">" marker

# Show domain ID assignment
switchshow | grep Domain

# Show all switches in the fabric with domain IDs
fabricshow
```

Domain IDs are unique per switch within a fabric (1–239). They are assigned dynamically unless statically configured. Static domain IDs are strongly recommended for production fabrics to prevent reconfiguration after a fabric partition and rejoin.

```bash
# Set a static domain ID (requires fabric re-segmentation momentarily)
configure
# At "Domain:" prompt, enter the desired domain ID
# At "Fabric parameters" prompt, set "insistDomainId" to 1
```

---

## Zoning

Zoning controls initiator-to-target access. Best practice: **single-initiator / single-target** zones.

```bash
# Show active zone configuration
cfgshow      # Full zone database (all zones, zone sets)
zoneshow     # Active zone configuration only

# Check if a specific WWPN is zoned
zoneshow | grep <wwpn>

# Show all aliases
alishow

# Show zone database size (relevant for large fabrics)
cfgsave      # Saves zone database to persistent storage
cfgsize      # Shows current zone database size vs limit
```

Activating a zone set replaces the currently active zone set on the fabric — always verify before activating to avoid removing existing zones.

---

## Fabric Health Checks

```bash
# Overall fabric health
fabricshow

# Port error summary (check for CRC, loss of sync, etc.)
porterrshow

# Show fabric routing table
topologyshow

# Show name server (all logged-in devices)
nsshow

# Check switch temperature and hardware health
sensorshow
tempshow
psshow   # Power supply status
fanshow  # Fan status
```
