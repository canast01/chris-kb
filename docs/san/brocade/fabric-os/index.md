# Brocade Fabric OS

<div class="kb-summary">
Brocade Fabric OS knowledge base covering switch architecture, zoning, ISLs, ports, firmware, CLI references, health checks, scripts, and troubleshooting guides for Fibre Channel SAN environments.
</div>

```text
┌──────────────────────────────────── Brocade Fabric OS — Overview ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Fabric OS (FOS): Brocade switch OS for FC SAN — zoning, routing, management          │   │
│   │           Runs on all Brocade FC switches (G630, G720, G730, X7 director platforms)           │   │
│   │             Core services: FCNS (name server), FCSM, zone management, ISL trunking            │   │
│   │         Management interfaces: CLI (SSH), REST API (FOS 8.2+), SANnav GUI integration         │   │
│   │     Fabric-wide config distribution: zone DB, fabric parameters, principal switch election    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Core OS services -> fabric-level functions -> management and integration layer                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         FC Services         │  │         Fabric Layer        │  │          Management         │   │
│   │       FCNS name server      │  │         Zone DB sync        │  │         CLI via SSH         │   │
│   │      Port login (FLOGI)     │  │         ISL trunking        │  │           REST API          │   │
│   │      FC routing (FSPF)      │  │       Principal switch      │  │          SANnav GUI         │   │
│   │        FCSM security        │  │        Fabric params        │  │         SNMP/syslog         │   │
│   │       RAS/diagnostics       │  │        Domain ID mgmt       │  │          LDAP auth          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Zone changes replicated across fabric; principal switch coordinates domain IDs                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │       Role       │      Protocol     │     Version      │      Notes       │   │
│   │       FCNS       │   Name server    │       FC-GS       │      FOS 6+      │  Per-fabric DB   │   │
│   │       FSPF       │    FC routing    │       FC-SW       │      FOS 6+      │ Least-cost path  │   │
│   │     REST API     │  Mgmt interface  │       HTTPS       │     FOS 8.2+     │     JSON/XML     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Brocade G630/G720/G730 switches · X7-8/X7-4 directors · FC SFP optics · ISL cables       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Fabric OS      = Brocade proprietary OS running on all Brocade FC switch hardware                  │
│    FCNS           = Fibre Channel Name Server; maps WWN to N_Port ID within the fabric                │
│    FSPF           = Fabric Shortest Path First; FC link-state routing protocol                        │
│    FLOGI          = Fabric Login; HBA registers with fabric and obtains FC address (FCID)             │
│    FCSM           = FC Security Manager; enforces DH-CHAP switch authentication                       │
│    Zone DB        = Fabric-wide zone configuration replicated to all switches in fabric               │
│    ISL trunk      = Multiple ISLs bundled for bandwidth aggregation between switches                  │
│    Principal switch = Elected switch managing domain ID assignments for the fabric                    │
│    Domain ID      = Unique numeric identifier for each switch in the fabric (1-239)                   │
│    REST API       = FOS 8.2+ HTTP management interface; JSON/XML payloads over HTTPS                  │
│    MAPS           = Monitoring and Alerting Policy Suite; FOS threshold alert engine                  │
│    portcfg        = FOS CLI command to configure port speed, mode, and behaviour                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-2">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>FC services, fabric layer, zone DB sync, and management interfaces.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Health checks, zone management, firmware download, and maintenance.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>DH-CHAP, FCSM, LDAP auth, SNMPv3, and access control hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Port diagnostics, fabric segmentation, ISL issues, and TAC escalation.</span>
</a>

</div>

---

## Platform Summary

| Platform | Type | Max FC Ports | FC Speed | Notes |
|---|---|---|---|---|
| G610 | Fixed | 24x | 32G | Entry-level fixed switch |
| G620 | Fixed | 64x | 32G | Mid-range workhorse |
| G720 | Fixed | 64x | 64G | High-performance fixed |
| G730 | Fixed | 64x | 64G | High-performance, latest gen |
| X7-4 | Director | Up to 192 | 32G/64G | 4-slot director — dual CP |
| X7-8 | Director | Up to 384 | 32G/64G | 8-slot director — dual CP |
| SAN256B-7 | Director | Up to 256 | 64G | High-density director |

Directors (X7-4, X7-8, SAN256B-7) support non-disruptive firmware upgrades via dual Control Processors (CPs). Fixed-form switches (G-series) require a reboot to apply firmware — always upgrade one fabric while the other carries traffic.
