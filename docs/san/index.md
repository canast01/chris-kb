---
title: SAN
---

# SAN

<div class="kb-summary">
SAN knowledge base covering Cisco MDS switches, DCNM, Nexus Dashboard, Brocade Fabric OS, and SANnav. Includes fabric architecture, zoning standards, ISL and port configuration, host connectivity, CLI references, health checks, and troubleshooting guides for Fibre Channel environments.
</div>

```text
┌───────────────────────────────────────── SAN Fabric Overview ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     SAN Fabric Management                                     │   │
│   │              Cisco: DCNM / Nexus Dashboard · CLI · NX-OS REST API · SNMP · Syslog             │   │
│   │            Brocade: SANnav Portal · Fabric OS CLI · REST API · SNMP trap forwarding           │   │
│   │          Both vendors: fabric-wide zoning, ISL monitoring, and performance dashboards         │   │
│   │             REST APIs enable programmable fabric automation and health integration            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Management platforms provide fabric-wide visibility, zoning, and lifecycle control                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Cisco MDS (SAN-OS / NX-OS)          │  │             Brocade (Fabric OS)             │   │
│   │       MDS 9000: 16/32/64G FC switches        │  │           Gen 7: 64G FC switching           │   │
│   │       VSANs: virtual fabric isolation        │  │         Zone aliases + zone configs         │   │
│   │        Smart Zoning + device aliases         │  │         ISL trunking + Port Channels        │   │
│   │           IVR: inter-VSAN routing            │  │           QoS: priority FC traffic          │   │
│   │         DCNM / Nexus Dashboard mgmt          │  │          SANnav: fabric management          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Both vendors deliver 16/32/64G Fibre Channel with zoning and trunked ISLs                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Cisco Fabric Services             │  │           Brocade Fabric Services           │   │
│   │         FLOGI: host login to fabric          │  │          FLOGI DB: registered ports         │   │
│   │          FSPF: fabric shortest path          │  │           D-Port: diagnostics port          │   │
│   │           CFS: config fabric sync            │  │           MAPS: monitoring alerts           │   │
│   │          FCNS: fabric name service           │  │          Buffer Credits: flow ctrl          │   │
│   │         Port modes: F · E · TE · NP          │  │          E-Port: ISL · F-Port: host         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Fabric protocol services register initiators and targets for SCSI data exchange                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      FLOGI       │      FDISC       │       Zoning      │       FSPF       │   ISL / Trunk    │   │
│   │   N_Port login   │    NPIV port     │   Access control  │   Link routing   │   E-port links   │   │
│   │  WWPN register   │   Virtual WWPN   │    pWWN / alias   │  Shortest path   │  TE/trunk port   │   │
│   │   FC-ID assign   │  HBA multiplex   │    Hard or soft   │   ECMP spread    │   Load balance   │   │
│   │  FCNS register   │  VF_Port serve   │   Zone database   │  Path failover   │    BB credits    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  FC switches · 16G/32G/64G SFPs · OM4 fibre · FC HBAs in hosts · Power & Cooling                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  FC       = Fibre Channel; dedicated high-speed block network using optical or copper links           │
│  WWPN     = World Wide Port Name; globally unique 64-bit identifier for each FC HBA port              │
│  WWNN     = World Wide Node Name; 64-bit identifier for the HBA device (node) itself                  │
│  FLOGI    = Fabric Login; N-Port registers its WWPN with the fabric to get an FC-ID                   │
│  FSPF     = Fabric Shortest Path First; link-state routing protocol for FC fabric paths               │
│  Zoning   = Fabric access control; limits which initiators can communicate with targets               │
│  VSAN     = Virtual SAN (Cisco); logical fabric partition within a shared physical switch             │
│  ISL      = Inter-Switch Link; E-Port or TE-Port carrying aggregated fabric traffic                   │
│  NPIV     = N-Port ID Virtualisation; one HBA presents multiple virtual WWPNs                         │
│  D-Port   = Diagnostic Port; Brocade link mode for BER and latency testing                            │
│  MAPS     = Monitoring and Alerting Policy Suite; Brocade threshold-based SAN alerts                  │
│  IVR      = Inter-VSAN Routing; Cisco controlled traffic flow between VSANs                           │
│  SANnav   = Brocade SAN management portal; replaced BSNA with modern REST-based UI                    │
│  DCNM     = Data Center Network Manager; Cisco fabric management (now Nexus Dashboard)                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-2">
<a class="kb-card" href="cisco/"><strong>Cisco SAN</strong><span>MDS switches — architecture, standards, lifecycle, CLI, scripts, troubleshooting, and security.</span></a>
<a class="kb-card" href="brocade/"><strong>Brocade SAN</strong><span>Fabric OS switches — architecture, standards, lifecycle, CLI, scripts, troubleshooting, and security.</span></a>
</div>
