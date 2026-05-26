# Brocade Fabric OS — How It Works

## Overview

Fabric OS (FOS) runs on Brocade/Broadcom SAN switches. Fabrics are deployed in a core-edge topology with ISLs (trunked) connecting edge switches to core directors. One switch per fabric is elected as the **principal switch**, which owns the fabric name server and manages domain ID assignments.

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
┌─────────────────────────── FabricOS — How It Works: Login, Zoning, Routing ───────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Device login: HBA sends FLOGI to switch, switch assigns FCID, NS registers WWN+FCID      │   │
│   │       Zone lookup: switch checks active zone config in ASIC; denies frames outside zone       │   │
│   │       FSPF: each switch builds topology from Link State Records; computes shortest path       │   │
│   │       MAPS: monitors counters every polling interval; fires alert if threshold breached       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Three parallel operational flows on every FabricOS switch:                                         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Login Flow         │  │         Zone Enforce        │  │         FSPF Routing        │   │
│   │       HBA sends FLOGI       │  │        Frame arrives        │  │         LSR exchange        │   │
│   │        FCID assigned        │  │       ASIC zone check       │  │         SPF computed        │   │
│   │       NS registration       │  │        Allow or deny        │  │       Route table set       │   │
│   │       PLOGI to target       │  │       Port quarantine       │  │       Frame forwarded       │   │
│   │         PRLI (SCSI)         │  │        Counter logged       │  │         ISL selected        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    MAPS polls error counters every 60 s by default; alerts via SNMP trap or email                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Flow       │     Trigger      │      Key step     │      Result      │    CLI verify    │   │
│   │      Login       │   HBA power-on   │   FLOGI to FCID   │  Device online   │      nsshow      │   │
│   │       Zone       │    Frame sent    │    ASIC lookup    │    Allow/Deny    │     cfgshow      │   │
│   │       FSPF       │   Topology chg   │     LSR flood     │  SPF recompute   │   topologyshow   │   │
│   │       MAPS       │   Counter poll   │   Threshold chk   │   Alert fired    │     mapsshow     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: HBA ports · SFP transceivers · fibre patch panels · FC switch line cards                 │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    FLOGI           = Fabric Login; HBA registers itself with the fabric                               │
│    FCID            = Fibre Channel ID (24-bit address: domain.area.port)                              │
│    PLOGI           = Port Login; initiator opens session with target after FLOGI                      │
│    PRLI            = Process Login; SCSI upper-layer protocol negotiation                             │
│    LSR             = Link State Record; contains port and neighbour information                       │
│    SPF             = Shortest Path First; algorithm computing optimal fabric routes                   │
│    ASIC zone check = Hardware-enforced zone lookup on every FC frame at line rate                     │
│    Port quarantine = Switch isolates offending port; traffic blocked at hardware level                │
│    nsshow          = Displays Name Server entries: WWN, FCID, port type                               │
│    mapsshow        = Shows MAPS policy rules, thresholds, and recent alert history                    │
│    topologyshow    = Displays fabric topology: domains, ISLs, path costs                              │
│    cfgshow         = Lists zone database: zone sets, zones, members                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Fabric A and Fabric B are completely independent — no cross-fabric cables. ISLs form trunk groups between switches within a fabric only.

## Principal Switch and Domain ID

One switch per fabric is the principal switch, elected by lowest WWN (default) or by priority. Domain IDs are unique per switch within a fabric (1–239). Static domain IDs are strongly recommended for production fabrics.

```bash
fabricshow                         # show all switches and domain IDs in fabric
switchshow | grep Domain           # show local domain ID
configure                          # set insistDomainId=1 for static domain ID
```

## Name Server and Fabric Services

When a device logs into the fabric, it registers its WWPN, WWNN, and FC4 type with the name server. Other devices query the name server to discover targets.

```bash
nsshow        # devices registered in local name server
nsallshow     # name server across entire fabric (all domains)
nslookup <wwpn>
portloginshow # FLOGI database — all logged-in devices
```

## Zoning

| Zone Type | Definition | Use Case |
|---|---|---|
| Soft zoning (WWN) | Zone membership by WWPN | Preferred for production — portable across port moves |
| Hard zoning (port-based) | Zone membership by domain ID + port | Use only when WWN flexibility not required |
| Peer zone | Multiple initiators share targets without seeing each other | Multi-host shared-target environments |

**Single-initiator zone model (required):**
```yaml
Zone: esxi01_hba0__pure_ct0_p0
  Member: esxi01_hba0   (WWPN: 10:00:00:00:c9:12:34:56)   ← one initiator only
  Member: pure_ct0_p0   (WWPN: 52:4a:93:7c:00:00:00:01)   ← one or more targets
```

Never place two initiator WWPNs in the same zone. This creates a blast radius risk.

## ISL Trunking

Multiple physical ISL ports between the same pair of switches are grouped into a trunk (single logical high-bandwidth link). All links in a trunk must be same speed and between the same switch pair.

```bash
islshow                    # show ISL status
trunkshow                  # show trunk group membership and master port
portperfshow               # show ISL throughput
porttrunkarea --enable <slot/port>
```

## Virtual Fabrics

Virtual Fabrics (VF) partition a single physical chassis into multiple independent logical switches, each with its own Fabric ID (FID). Ports are assigned to exactly one logical switch at a time.

```bash
lscfg --show               # list logical switches and their FIDs
setContext <fid>           # switch CLI context to a specific FID
lscfg --config <fid> -port <slot/port>   # assign port to logical switch
```

## MAPS — Monitoring and Alerting Policy Suite

MAPS provides threshold-based automated health monitoring. It monitors port error counters, ISL utilization, C3 discard rates, BB credit zero (slow drain), switch environment, fabric events, and security events.

```bash
mapsdashboard --show    # current MAPS health dashboard
mapsdb --show           # all triggered MAPS alerts
mapspolicy --show       # active MAPS policy
```

## FCIP — Fibre Channel over IP

FCIP extends a Fibre Channel fabric over an IP WAN connection for long-distance replication (SRDF, RecoverPoint). Brocade 7810/7840 extension platforms provide FCIP gateway functionality. Target IP network latency: <5 ms one-way for synchronous replication.

```bash
fciptunnel --show       # FCIP tunnel status
fcipcircuit --show      # FCIP circuit status
fcipcircuit --show -perf
```
