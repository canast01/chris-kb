---
tags:
  - certifications
  - san
---
# SAN Fabric Concepts


<div class="kb-summary">
SAN Fabric Concepts reference covering Fibre Channel Layer Model, Port Types, WWPN vs WWNN, Fabric IDs and Domain IDs, Fabric Login Sequence and 2 more sections.
</div>
```text
┌───────────────────────────────── Certifications San Fabric Concepts ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                        San: Certifications San Fabric Concepts platform                       │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │               Management: Certifications San Fabric Concepts management console               │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Certifications San Fabric Concepts infrastructure · management network · monitoring      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    San                = Certifications San Fabric Concepts platform overview and core concepts        │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Fibre Channel Layer Model

| Layer | Name | Function |
|---|---|---|
| FC-0 | Physical | Media, connectors, transceivers (SFP+) |
| FC-1 | Encode/Decode | 8B/10B or 64B/66B encoding, serial transmission |
| FC-2 | Framing and Signaling | Frame format, flow control, sequencing, error detection |
| FC-3 | Common Services | Hunt groups, multicast (rarely used) |
| FC-4 | Upper Layer Protocols | FCP (SCSI over FC), FICON, NVMe-FC |

## Port Types

| Port | Name | Description |
|---|---|---|
| N_Port | Node Port | Host or storage HBA port connecting to the fabric |
| F_Port | Fabric Port | Switch port connecting to an N_Port (end device) |
| E_Port | Expansion Port | Switch-to-switch interswitch link (ISL) |
| TE_Port | Trunked E_Port | ISL carrying multiple VSANs over one physical link (Cisco) |
| NL_Port | Node Loop Port | Node port on arbitrated loop (FC-AL; legacy) |
| G_Port | Generic Port | Auto-negotiates to F_Port or E_Port |
| U_Port | Universal Port | Pre-login, before role is determined |

## WWPN vs WWNN

| Identifier | Full Name | Scope | Used In |
|---|---|---|---|
| WWNN | World Wide Node Name | HBA card (host/storage node) | Identifies the physical HBA; one per HBA |
| WWPN | World Wide Port Name | Each port on the HBA | Zoning, LUN masking; one per port |

Key exam rule: Zoning is done using WWPN, not WWNN. A dual-port HBA has 1 WWNN and 2 WWPNs.

## Fabric IDs and Domain IDs

- **Domain ID**: Unique 8-bit identifier for each switch in a fabric (1–239 valid; 0 and 240–255 reserved)
- **Area ID**: 8-bit identifier for a port group within a switch
- **Port ID (FCID)**: 24-bit address = Domain ID (8) + Area ID (8) + Port ID (8) — assigned during fabric login
- Fabric Principal Switch: elected via FSPF; assigns Domain IDs to other switches during merge
- Domain ID conflicts cause fabric segmentation — critical exam topic

## Fabric Login Sequence

1. **FLOGI (Fabric Login)**: N_Port sends FLOGI to well-known address FF:FF:FE requesting a Fibre Channel address (FCID)
2. **PLOGI (Port Login)**: N_Port logs in to another N_Port or F_Port to establish session
3. **PRLI (Process Login)**: Upper-layer protocol login (e.g., SCSI-3 or NVMe); establishes exchange parameters
4. **LOGO (Logout)**: Terminates session; can be implicit (link down) or explicit

## Fabric Services (Well-Known Addresses)

| Address | Service |
|---|---|
| FF:FF:FE | Fabric Login (FLOGI) |
| FF:FF:FD | Fabric Controller |
| FF:FF:FC | Name Server (FCNS) — registers WWPNs and FCIDs |
| FF:FF:FB | Fabric Configuration Server |
| FF:FF:FA | Management Server |

## Study Checklist

- [ ] Explain each FC layer (FC-0 through FC-4) with one sentence
- [ ] Distinguish F_Port, E_Port, N_Port, and G_Port by connection type
- [ ] Explain WWPN vs WWNN and which is used for zoning
- [ ] Describe the FCID 24-bit structure from memory
- [ ] Walk through the complete fabric login sequence (FLOGI → PLOGI → PRLI)
- [ ] Know the Name Server well-known address and its function
- [ ] Explain what triggers fabric segmentation due to Domain ID conflict
