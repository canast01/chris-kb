---
tags:
  - certifications
  - san
description: "SAN Fabric Concepts reference covering Fibre Channel Layer Model, Port Types, WWPN vs WWNN, Fabric IDs and Domain IDs, Fabric Login Sequence and 2 more..."
---
# SAN Fabric Concepts

<div class="kb-summary">
SAN Fabric Concepts reference covering Fibre Channel Layer Model, Port Types, WWPN vs WWNN, Fabric IDs and Domain IDs, Fabric Login Sequence and 2 more sections.
</div>

```d2
direction: down

fibre_channel_layer_model: "Fibre Channel Layer Model" {shape: rectangle}
port_types: "Port Types" {shape: rectangle}
wwpn_vs_wwnn: "WWPN vs WWNN" {shape: rectangle}
fabric_ids_and_domain_ids: "Fabric IDs and Domain IDs" {shape: rectangle}
fabric_login_sequence: "Fabric Login Sequence" {shape: rectangle}
fabric_services_wellknown_addresses: "Fabric Services (Well-Known Addresses)" {shape: rectangle}

fibre_channel_layer_model -> port_types: uses
port_types -> wwpn_vs_wwnn: uses
wwpn_vs_wwnn -> fabric_ids_and_domain_ids: uses
fabric_ids_and_domain_ids -> fabric_login_sequence: uses
fabric_login_sequence -> fabric_services_wellknown_addresses: uses
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
