# Brocade Fabric OS — Architecture

<div class="kb-summary">
Fabric OS runs on Brocade/Broadcom FC switches in dual-fabric core-edge topology. Principal switch election, distributed name server, WWN-based zoning, ISL trunks, Virtual Fabrics (FID partitioning), and MAPS health monitoring are the core platform mechanisms.
</div>

```
┌────────────────────────────── FabricOS Architecture — Component Layers ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   FabricOS runs on Brocade ASICs (Condor, Goldeneye, Orca families) + embedded Linux kernel   │   │
│   │      Architecture: hardware forwarding plane + software control plane + management plane      │   │
│   │       Control plane: fabric services (FSPF, NS, Zone Server) run as daemons on main CPU       │   │
│   │           Data plane: FC frames forwarded in hardware by switching ASIC at line rate          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Control Plane                 │  │                  Data Plane                 │   │
│   │             FSPF routing daemon              │  │             ASIC frame switching            │   │
│   │              Zone Server daemon              │  │            Hardware zoning lookup           │   │
│   │              Name Server daemon              │  │             Port buffer credits             │   │
│   │             MAPS monitor daemon              │  │            ISL trunk aggregation            │   │
│   │                SSH / REST API                │  │              SFP DOM monitoring             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Protocol     │     Function     │       CLI        │   │
│   │     Control      │   FSPF daemon    │       SW_ILS      │  Fabric routing  │   topologyshow   │   │
│   │     Control      │   Zone Server    │       SW_ILS      │   Zone enforce   │     cfgshow      │   │
│   │       Mgmt       │     REST API     │       HTTPS       │    Automation    │   curl/Postman   │   │
│   │       Data       │       ASIC       │         FC        │    Frame fwd     │     portshow     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: FC director chassis · blades · SFPs · inter-chassis ICL cables · power supplies          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Control plane   = Software layer: routing, zone enforcement, name resolution decisions             │
│    Data plane      = Hardware layer: ASIC forwards FC frames at full line rate                        │
│    ASIC            = Application-Specific IC; Condor4/Orca on modern Brocade directors                │
│    Buffer credits  = Flow control units; each port has Rx credits; exhaustion = backpressure          │
│    DOM             = Digital Optical Monitoring; SFP reports Tx/Rx power, temp, voltage               │
│    FSPF daemon     = Software process computing shortest-path fabric routes                           │
│    Zone Server     = Daemon storing zone DB; pushes active config to ASIC for enforcement             │
│    ICL             = Inter-Chassis Link; high-density connection between director blades              │
│    topologyshow    = CLI command displaying fabric topology and domain IDs                            │
│    portshow        = CLI command showing per-port statistics and state                                │
│    cfgshow         = CLI command listing all zone configurations in the database                      │
│    SW_ILS          = Switch Internal Link Service; fabric-wide control frames                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Fabric OS Architecture](../../../../assets/fabric-os-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with SANnav, vCenter, and storage arrays.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Dual-fabric design, zoning model, domain ID, and ISL trunking standards.</span></a>
</div>

## Platform Reference

| Platform | Type | Max Ports | Notes |
|---|---|---|---|
| G620 | Fixed | 64× 32G FC | Mid-range |
| G720 | Fixed | 64× 64G FC | High-performance fixed |
| X7-4 | Director | Up to 192 FC | 4-slot director — dual CP, non-disruptive upgrades |
| X7-8 | Director | Up to 384 FC | 8-slot director — dual CP, non-disruptive upgrades |
| 6510 | Fixed | 48× 16G FC | End-of-sale — plan migration |

## Dual-Fabric Topology


