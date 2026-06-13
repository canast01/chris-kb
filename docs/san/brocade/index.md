---
tags:
  - san
---
# Brocade SAN

<div class="kb-summary">
Brocade SAN knowledge base covering Fabric OS switches and SANnav management. Includes fabric architecture, zoning, CLI references, health checks, and troubleshooting guides for Brocade Fibre Channel environments.

*Applies to: Brocade FOS 9.x*
</div>

```text
┌────────────────────────────────────────── Brocade SAN Stack ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     Brocade SAN Management                                    │   │
│   │         SANnav Management Portal: web UI for fabric discovery, zoning, and performance        │   │
│   │           Fabric OS CLI: switchshow · cfgshow · zoneshow · supportshow · portcfgshow          │   │
│   │                 REST API: HTTPS-based access to FOS config and monitoring data                │   │
│   │           SNMP v3 · Syslog: polling and trap forwarding to SIEM and monitoring tools          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    SANnav and the FOS CLI are the two primary management surfaces for Brocade fabrics                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Fabric OS (FOS)                │  │           SANnav Management Portal          │   │
│   │       Distributed OS across all ports        │  │         Fabric discovery + inventory        │   │
│   │       Zone management: cfgshow/cfgsave       │  │          Health dashboard + alerts          │   │
│   │          ISL trunking: trunk groups          │  │           Zoning: drag-and-drop UI          │   │
│   │        Port types: E / F / G / D / L         │  │         Performance analytics: IOPS         │   │
│   │         MAPS: threshold-based alerts         │  │          Replaces older BSNA / DCFM         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Fabric OS runs on the switch; SANnav is the management application layer                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Zoning & Security               │  │              ISL & Performance              │   │
│   │           Zone aliases: pWWN names           │  │          Trunk groups: 8 ports max          │   │
│   │           Zone configs: named sets           │  │          Buffer credits: flow ctrl          │   │
│   │        Open / enforce / strict modes         │  │          QoS: high/medium/low lanes         │   │
│   │         DCC: device connection ctrl          │  │           D-Port: link diagnostics          │   │
│   │         SCC: switch connection ctrl          │  │          Access Gateway: edge mode          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Zoning enforces access control · ISL trunks aggregate bandwidth between switches                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     FLOGI DB     │      Zoning      │     ISL Trunk     │       MAPS       │      D-Port      │   │
│   │  Login register  │    Zone alias    │    Trunk groups   │   Alert policy   │    Link test     │   │
│   │   WWN + FC-ID    │   cfgshow/save   │     trunkshow     │     mapsshow     │     portdiag     │   │
│   │    nsshow cmd    │    cfgenable     │    Port Channel   │ Threshold rules  │   BER testing    │   │
│   │    fabricshow    │    zonecreate    │    Load balance   │  Health scoring  │   Eye margins    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Brocade FC switches · 16G/32G/64G SFPs · OM4 fibre · FC HBAs · Power & Cooling                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  FOS       = Fabric OS; Brocade switch OS distributed across all ports in the switch                  │
│  SANnav    = Brocade SAN management portal; replaced BSNA/DCFM with modern REST UI                    │
│  MAPS      = Monitoring and Alerting Policy Suite; threshold engine for SAN health                    │
│  D-Port    = Diagnostic Port; Brocade link mode for BER and optical latency testing                   │
│  Trunk Group= Bundle of ISL ports acting as one logical link for load balancing                       │
│  Buffer Credits= FC flow control; limits in-flight frames per port to prevent overflow                │
│  Zone Alias= Named reference to a pWWN; simplifies zone member configuration                          │
│  Zone Config= Named collection of zones saved and activated as a policy on the fabric                 │
│  cfgshow   = FOS command to display zone config; cfgsave persists to flash                            │
│  DCC       = Device Connection Control; restricts ports a WWN may connect to                          │
│  SCC       = Switch Connection Control; restricts which switches may join via ISL                     │
│  Access Gateway= Brocade edge mode; connects to core switch as an N-Port proxy                        │
│  supportshow= FOS diagnostic command; captures full switch state for support cases                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


```text
┌───────────────────────────────── Brocade SAN — Fabric Build Sequence ─────────────────────────────────┐
│                                                                                                       │
│  Step 1 · Physical Readiness                                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Rack directors and edge switches  ·  connect power feeds to separate PDUs                            │
│  ISL cables between directors  ·  use OM4/OS2 per port type (SWL/LWL)                                 │
│  Management: 1 GbE OOB port per switch  ·  assign IP via front panel serial console                   │
│  Confirm serial console access  ·  upgrade Fabric OS to target version (RFI approved)                 │
│  DNS A-records for all switch management hostnames  ·  NTP server reachable                           │
│                                                                                                       │
│                                        │  configure switch parameters                                 │
│                                        ▼                                                              │
│  Step 2 · Switch Initialisation                                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Set switch name, domain ID (unique per fabric)  ·  disable port range not in use                     │
│  Set BB credit per port type  ·  fabric-wide BB credit buffer tuning on ISLs                          │
│  Enable Enhanced Transmission Selection (ETS) for FCoE if applicable                                  │
│  Set in-band management to disabled  ·  restrict Telnet  ·  enable SSH only                           │
│  Set insistent domain ID  ·  configure fabric parameters (E_D_TOV, R_A_TOV) consistently              │
│                                                                                                       │
│                                        │  form fabric with ISL trunking                               │
│                                        ▼                                                              │
│  Step 3 · Fabric Formation                                                                            │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Enable ISL trunking (brocade Trunking licence)  ·  group ISL ports into trunk groups                 │
│  Verify fabric topology with fabricshow  ·  all principal switches visible                            │
│  FCID assignment: verify no domain ID conflicts  ·  check fabricShow principal election               │
│  Enable DLS (dynamic load sharing) on all switches  ·  verify with dlsShow                            │
│  Run fabricShow  ·  nsShow  ·  trunkShow to confirm clean fabric state                                │
│                                                                                                       │
│                                        │  create aliases and zones                                    │
│                                        ▼                                                              │
│  Step 4 · Zoning                                                                                      │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create PWWN-based aliases for every initiator and target: alicreate  ·  aliadd                       │
│  Create peer zones: one initiator per zone  ·  all reachable targets in same zone                     │
│  Never use domain,index (D,I) zoning in production — breaks on switch replacement                     │
│  Create zone configuration (cfgcreate)  ·  add all zones  ·  cfgenable to activate                    │
│  Verify active zone config with cfgShow  ·  test that hosts can see storage targets                   │
│                                                                                                       │
│                                        │  present ports to hosts and arrays                           │
│                                        ▼                                                              │
│  Step 5 · Host + Array Login                                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Connect host HBAs to fabric  ·  confirm FLOGI in nsShow output per port                              │
│  Confirm PLOGI and PRLI exchange  ·  verify SCSI LUN discovery on host                                │
│  Connect array front-end ports  ·  confirm target FLOGI and visibility in nsShow                      │
│  Run nsAllShow to confirm all N-ports visible to fabric  ·  cross-check with array                    │
│  Verify LUN masking on array matches zone scope  ·  test I/O from host to LUN                         │
│                                                                                                       │
│                                        │  deploy SANnav management                                    │
│                                        ▼                                                              │
│  Step 6 · SANnav Management                                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Deploy SANnav OVA on vSphere or install on RHEL  ·  assign management IP                             │
│  Add all fabric switches via Discover Switches  ·  SSH credential required                            │
│  Configure SNMP trap target = SANnav IP on all switches  ·  verify trap receipt                       │
│  Set up syslog forwarding from switches to SANnav and to SIEM                                         │
│  Enable performance collection  ·  configure SANnav alerts for port errors and congestion             │
│  Baseline: export zone config backup  ·  document port-to-server mapping inventory                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="fabric-os/"><strong>Fabric OS</strong><span>Brocade switch OS — zoning, fabric configuration, CLI, health checks, and troubleshooting.</span></a>
<a class="kb-card" href="sannav/"><strong>SANnav</strong><span>Brocade SAN management — fabric discovery, monitoring, and zoning management.</span></a>
</div>
