# SANnav

<div class="kb-summary">
Brocade SANnav management platform knowledge base covering fabric discovery, monitoring, inventory, alerts, reports, and troubleshooting for Brocade Fibre Channel environments.
</div>

```
┌──────────────────────────────── Brocade SANnav — Management Platform ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  SANnav: web-based SAN management for Brocade FC switches — discovery, monitoring, reporting  │   │
│   │         Deployed as a Linux VM; connects to all Brocade switches via SSH and REST API         │   │
│   │        Fabric discovery: topology mapping, zone config pull, port inventory, SFP health       │   │
│   │        Replaces legacy DCFM; supports up to 150 switches and 15,000 ports per instance        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Fabric discovery → health monitoring → inventory and reporting layers                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Discovery          │  │          Monitoring         │  │          Reporting          │   │
│   │       Switch discovery      │  │         Port health         │  │       Switch inventory      │   │
│   │       Topology mapping      │  │        Error counters       │  │        Port inventory       │   │
│   │       Zone config pull      │  │       SFP Tx/Rx power       │  │       Firmware matrix       │   │
│   │       Credential mgmt       │  │       Threshold alerts      │  │         SAN reports         │   │
│   │       SNMP integration      │  │       Performance data      │  │         Audit trail         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    REST API and LDAP integration allow external monitoring and centralised auth                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │     Function     │      Protocol     │      Output      │   Integration    │   │
│   │    Discovery     │  Topology/zones  │      SSH/REST     │    Fabric map    │    SNMP traps    │   │
│   │    Monitoring    │ Port/SFP health  │      Polling      │      Alerts      │   Syslog/email   │   │
│   │    Reporting     │ Inventory/audit  │      REST API     │     PDF/CSV      │    LDAP auth     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SANnav Linux VM · Brocade FC switches (G630/G720/G730) · FC SFP transceivers             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SANnav        = Brocade SAN management platform (replaces legacy DCFM/Network Advisor)             │
│    Fabric        = Set of Brocade FC switches connected via ISLs sharing a single namespace           │
│    Zone config   = Active zone configuration defining which HBAs can communicate with which targets   │
│    SFP           = Small Form-factor Pluggable transceiver; optical FC link on each switch port       │
│    Tx/Rx power   = SFP optical transmit/receive power; out-of-range indicates failing optic           │
│    Port health   = FC port state: online/offline/error; error counters: CRC, Loss of Signal           │
│    SNMP trap     = SANnav sends fault events to NMS via SNMP; configured per severity level           │
│    DCFM          = Data Center Fabric Manager; legacy predecessor to SANnav                           │
│    REST API      = SANnav REST API; used for automation and ITSM integration                          │
│    Topology map  = SANnav graphical view of switch interconnections and ISL links                     │
│    ISL           = Inter-Switch Link; FC trunk connecting two Brocade switches in a fabric            │
│    LDAP auth     = SANnav supports AD/LDAP for centralised user authentication                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
