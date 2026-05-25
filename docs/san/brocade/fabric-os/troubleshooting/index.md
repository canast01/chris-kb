# FabricOS — Troubleshooting


```
┌───────────────────────────────────── FabricOS — Troubleshooting ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          FabricOS troubleshooting workflow: port → fabric → ISL → trunk → escalation          │   │
│   │    Port-level: portshow, portlogdump, portperfshow, porterrshow for individual port issues    │   │
│   │        Fabric-level: fabricshow, nsshow, topologyshow for namespace and topology issues       │   │
│   │            Escalation: supportshow output + RASlog bundle sent to Broadcom/Dell TAC           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Port-level → fabric-level → ISL/trunk → RASlog analysis → TAC escalation                           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Port Level         │  │         Fabric Level        │  │          Escalation         │   │
│   │           portshow          │  │          fabricshow         │  │         supportshow         │   │
│   │         portlogdump         │  │            nsshow           │  │        RASlog bundle        │   │
│   │         portperfshow        │  │         topologyshow        │  │      Dell/Broadcom TAC      │   │
│   │         porterrshow         │  │           iodshow           │  │         configupload        │   │
│   │           sfpshow           │  │          trunkshow          │  │        Firmware check       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Always run supportshow before any disruptive action; output needed for TAC case                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Symptom      │  First command   │     Key output    │    Resolution    │    Escalation    │   │
│   │   Port offline   │    portshow N    │   State, no_sync  │ Check SFP/cable  │  TAC if persist  │   │
│   │    Segmented     │    fabricshow    │     Domain IDs    │ Domain conflict  │    TAC merge     │   │
│   │     Slow I/O     │   portperfshow   │   MB/s per port   │ BB credit / ISL  │  TAC + storage   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SFP Tx/Rx dBm · LC cable continuity · ISL physical path · HBA driver                     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    portshow N    = Detailed state for port N; shows login state, connected WWN, errors                │
│    portlogdump   = FIFO event log for a port; captures FLOGI/PLOGI events and errors                  │
│    portperfshow  = Real-time port throughput; run during I/O to see bytes/sec                         │
│    porterrshow   = Error counters for all ports: CRC, LOS, LOSync, Bad EOF                            │
│    fabricshow    = All switches in the fabric; shows domain IDs and principal switch                  │
│    nsshow        = Name Server entries (FLOGI database); lists all logged-in devices                  │
│    topologyshow  = ISL topology map including inter-switch distances and port connections             │
│    trunkshow     = ISL trunk member ports and bandwidth utilisation per trunk group                   │
│    iodshow       = In-Order Delivery state; relevant when frames arrive out of order                  │
│    RASlog        = FabricOS Reliability, Availability, Serviceability log; TAC key artifact           │
│    supportshow   = Combined diagnostic output of 50+ show commands; attach to TAC case                │
│    configupload  = Back up switch config before any change or TAC-guided recovery                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="diagnostics/"><strong>Diagnostics</strong><span>Diagnostic procedures and log analysis.</span></a>
<a class="kb-card" href="escalation/"><strong>Escalation</strong><span>Vendor escalation procedures and support contacts.</span></a>
</div>

```
┌───────────────────────────────────── FabricOS — Troubleshooting ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          FabricOS troubleshooting workflow: port → fabric → ISL → trunk → escalation          │   │
│   │    Port-level: portshow, portlogdump, portperfshow, porterrshow for individual port issues    │   │
│   │        Fabric-level: fabricshow, nsshow, topologyshow for namespace and topology issues       │   │
│   │            Escalation: supportshow output + RASlog bundle sent to Broadcom/Dell TAC           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Port-level → fabric-level → ISL/trunk → RASlog analysis → TAC escalation                           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Port Level         │  │         Fabric Level        │  │          Escalation         │   │
│   │           portshow          │  │          fabricshow         │  │         supportshow         │   │
│   │         portlogdump         │  │            nsshow           │  │        RASlog bundle        │   │
│   │         portperfshow        │  │         topologyshow        │  │      Dell/Broadcom TAC      │   │
│   │         porterrshow         │  │           iodshow           │  │         configupload        │   │
│   │           sfpshow           │  │          trunkshow          │  │        Firmware check       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Always run supportshow before any disruptive action; output needed for TAC case                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Symptom      │  First command   │     Key output    │    Resolution    │    Escalation    │   │
│   │   Port offline   │    portshow N    │   State, no_sync  │ Check SFP/cable  │  TAC if persist  │   │
│   │    Segmented     │    fabricshow    │     Domain IDs    │ Domain conflict  │    TAC merge     │   │
│   │     Slow I/O     │   portperfshow   │   MB/s per port   │ BB credit / ISL  │  TAC + storage   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SFP Tx/Rx dBm · LC cable continuity · ISL physical path · HBA driver                     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    portshow N    = Detailed state for port N; shows login state, connected WWN, errors                │
│    portlogdump   = FIFO event log for a port; captures FLOGI/PLOGI events and errors                  │
│    portperfshow  = Real-time port throughput; run during I/O to see bytes/sec                         │
│    porterrshow   = Error counters for all ports: CRC, LOS, LOSync, Bad EOF                            │
│    fabricshow    = All switches in the fabric; shows domain IDs and principal switch                  │
│    nsshow        = Name Server entries (FLOGI database); lists all logged-in devices                  │
│    topologyshow  = ISL topology map including inter-switch distances and port connections             │
│    trunkshow     = ISL trunk member ports and bandwidth utilisation per trunk group                   │
│    iodshow       = In-Order Delivery state; relevant when frames arrive out of order                  │
│    RASlog        = FabricOS Reliability, Availability, Serviceability log; TAC key artifact           │
│    supportshow   = Combined diagnostic output of 50+ show commands; attach to TAC case                │
│    configupload  = Back up switch config before any change or TAC-guided recovery                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [Brocade Fabric OS](../index.md) reference.
