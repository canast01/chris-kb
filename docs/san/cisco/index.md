---
tags:
  - san
---
# Cisco SAN

<div class="kb-summary">
Cisco SAN knowledge base covering MDS switches, DCNM, and Nexus Dashboard. Includes fabric architecture, zoning, CLI references, health checks, and troubleshooting guides for Cisco Fibre Channel environments.

*Applies to: Cisco MDS · Nexus*
</div>

```text
┌─────────────────────────────────────────── Cisco SAN Stack ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                      Cisco SAN Management                                     │   │
│   │         DCNM / Nexus Dashboard: GUI fabric management, zoning workflows, and telemetry        │   │
│   │             NX-OS / SAN-OS CLI: config t · show flogi database · show zone status             │   │
│   │           SNMP v3 · Syslog: event collection and forwarding to monitoring platforms           │   │
│   │            REST API: programmable fabric config, metrics, and zoning via HTTPS/JSON           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Management tools span hardware switches, legacy DCNM, and modern Nexus Dashboard                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Cisco MDS 9000       │  │             DCNM            │  │     Nexus Dashboard (ND)    │   │
│   │    9132T: 32-port 32G FC    │  │     Data Center Ntwk Mgr    │  │      Successor to DCNM      │   │
│   │    9396T: 96-port 32G FC    │  │    Fabric discovery+sync    │  │   Fabric Controller (NDF)   │   │
│   │    9700: modular director   │  │    Zoning: templates+push   │  │    Fabric Insights (NDI)    │   │
│   │    Line cards: 16/32/64G    │  │    Performance monitoring   │  │    Multi-site management    │   │
│   │    SAN-OS → NX-OS upgrade   │  │    Health: port + fabric    │  │    Flow telemetry + VXLAN   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    MDS hardware, DCNM (legacy), and Nexus Dashboard (current) form the Cisco SAN stack                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            VSANs            │  │            Zoning           │  │        ISL & Trunking       │   │
│   │   Virtual fabric partition  │  │    Device aliases: names    │  │     E-Port: standard ISL    │   │
│   │    VSAN membership: port    │  │    pWWN or FC ID members    │  │     TE-Port: trunked ISL    │   │
│   │      Domain IDs: 1–239      │  │   Smart Zoning: auto-bind   │  │     Port channels: LACP     │   │
│   │    IVR: inter-VSAN route    │  │   Enhanced zoning: atomic   │  │     FSPF: load balancing    │   │
│   │     VSAN DB sync via CFS    │  │   Zone sets: named policy   │  │     F-Port channels: NPV    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    VSANs isolate traffic · Zoning controls access · ISL trunks carry aggregated load                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      FLOGI       │      FDISC       │       FC-NS       │       RSCN       │       CFS        │   │
│   │   N_Port login   │    NPIV port     │    Name service   │  Change notice   │   Fabric sync    │   │
│   │   WWPN + WWNN    │  Virtual ports   │   FCid database   │   Topology chg   │   Atomic apply   │   │
│   │  FC-ID: 24-bit   │  HBA multiplex   │   PLOGI follows   │   Zone trigger   │     CFS lock     │   │
│   │  FCNS register   │  VF_Port serve   │   show flogi db   │   RSCN payload   │   Full fabric    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  MDS 9000 switches · 16G/32G/64G FC SFPs · OM4 fibre · FC HBAs · Power & Cooling                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  MDS     = Cisco Multilayer Director Switch; purpose-built FC SAN switches                            │
│  NX-OS   = Network OS used on Cisco MDS after SAN-OS; shared CLI with Nexus                           │
│  SAN-OS  = Original Cisco MDS OS; succeeded by NX-OS for unified CLI                                  │
│  VSAN    = Virtual SAN; Cisco method of partitioning one fabric into isolated SANs                    │
│  IVR     = Inter-VSAN Routing; allows controlled traffic exchange between VSANs                       │
│  DCNM    = Data Center Network Manager; Cisco GUI for MDS zoning and monitoring                       │
│  ND      = Nexus Dashboard; successor to DCNM; unified multi-fabric management                        │
│  Smart Zoning= Inserts exact FC IDs into zone members; reduces unnecessary RSCN storms                │
│  Device Alias= Fabric-wide friendly name for a WWN; simplifies zone configuration                     │
│  CFS     = Cisco Fabric Services; distributes and synchronises config across MDS peers                │
│  RSCN    = Registered State Change Notification; alerts hosts of topology changes                     │
│  TE-Port = Trunked E-Port; carries multiple VSANs over one physical ISL link                          │
│  NPV     = N-Port Virtualiser; MDS edge mode that proxies logins to a core switch                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


```text
┌──────────────────────────────── Cisco MDS SAN — Fabric Build Sequence ────────────────────────────────┐
│                                                                                                       │
│  Step 1 · Physical Readiness                                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Rack MDS 9000 directors or fabric switches  ·  dual power feeds to separate PDUs                     │
│  ISL cables between directors  ·  SFP type must match (SWL/LWL/ELWL per distance)                     │
│  Management: OOB GigE port  ·  assign IP via console (serial cable, 9600 baud)                        │
│  Upgrade NX-OS to target version  ·  verify supervisor and line card firmware                         │
│  DNS A-records for all switch management FQDNs  ·  NTP reachable from management VRF                  │
│                                                                                                       │
│                                        │  complete NX-OS initial configuration                        │
│                                        ▼                                                              │
│  Step 2 · NX-OS Initialisation                                                                        │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Initial setup script on first boot  ·  hostname, admin password, management IP                       │
│  Configure management VRF: ip route 0.0.0.0/0 vrf management <gateway>                                │
│  Enable SSH  ·  disable Telnet  ·  configure AAA to RADIUS/TACACS+ for production                     │
│  Set NTP server  ·  set timezone  ·  verify with show clock and show ntp status                       │
│  Install and activate Feature Set: feature fport-channel-trunk  ·  feature npv if needed              │
│                                                                                                       │
│                                        │  configure VSANs and port channels                           │
│                                        ▼                                                              │
│  Step 3 · VSANs & Port Channels                                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create VSANs: vsan database  ·  vsan <id> name <name>  ·  assign to interfaces                       │
│  Create port channels for ISLs: interface port-channel <n>  ·  channel-group <id> force               │
│  Assign F-ports (host) and E-ports (ISL) per VSAN  ·  no switchport on FC interfaces                  │
│  Verify VSAN membership with show vsan membership  ·  check ISL state with show topology              │
│  Enable FSPF load balancing on port channels for multi-path ISL traffic distribution                  │
│                                                                                                       │
│                                        │  build device-alias database and zones                       │
│                                        ▼                                                              │
│  Step 4 · Device Aliases + Zoning                                                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create device-alias database: device-alias name <alias> pwwn <wwn>  ·  commit                        │
│  Create zones using device-alias names (not raw WWNs) for maintainability                             │
│  zone name <zone>  ·  member device-alias <alias>  ·  one initiator per zone                          │
│  Create zoneset  ·  add all zones  ·  zoneset activate name <set> vsan <id>                           │
│  Verify: show zoneset active  ·  show fcns database  ·  no stale entries                              │
│                                                                                                       │
│                                        │  validate host and array logins                              │
│                                        ▼                                                              │
│  Step 5 · Host + Array Login                                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Connect host HBAs  ·  confirm FLOGI in show flogi database  ·  per-VSAN scope                        │
│  Confirm device-alias auto-learnt or manually bound to PWWN                                           │
│  Connect array front-end ports  ·  verify target FLOGI and PLOGI exchange                             │
│  Run show fcns database vsan <id> to confirm full N-port visibility                                   │
│  Validate LUN masking scope matches zone  ·  run I/O test from host                                   │
│                                                                                                       │
│                                        │  deploy Nexus Dashboard Fabric Controller                    │
│                                        ▼                                                              │
│  Step 6 · Nexus Dashboard & NDFC                                                                      │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Deploy Nexus Dashboard OVA (3 master nodes or 1 for lab)  ·  assign management IP                    │
│  Install NDFC (formerly DCNM) service on Nexus Dashboard  ·  enable SAN controller                    │
│  Add MDS fabrics via Discover  ·  SSH credentials required  ·  topology auto-builds                   │
│  Configure SNMP trap and syslog forwarding from all switches to NDFC                                  │
│  Enable performance monitoring  ·  configure fabric health and zoning drift alerts                    │
│  Export zone config backups to NDFC  ·  document port inventory for CMDB                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="mds/"><strong>Cisco MDS</strong><span>MDS 9000 series switches — zoning, fabric configuration, CLI, health checks, and troubleshooting.</span></a>
<a class="kb-card" href="cisco-dcnm/"><strong>DCNM</strong><span>Data Center Network Manager — SAN management, discovery, and monitoring.</span></a>
<a class="kb-card" href="nexus-dashboard/"><strong>Nexus Dashboard</strong><span>Fabric health, flow telemetry, policy compliance, and multi-site management.</span></a>
</div>
