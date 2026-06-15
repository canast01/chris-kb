---
tags:
  - architecture
  - san
---
# Cisco MDS — Architecture

<div class="kb-summary">
Cisco MDS 9000 series FC switches running NX-OS. Core isolation mechanism is the VSAN — multiple logical fabrics share physical hardware with separate name servers, zone databases, and domain IDs per VSAN. Directors support ISSU for zero-downtime maintenance.

*Applies to: Cisco MDS · Nexus*
</div>

```text
┌───────────────────────────── Cisco MDS Architecture — NX-OS FC Switching ─────────────────────────────┐
│                                                                                                       │
│  MDS 9000 NX-OS FC switches; VSANs create logical fabrics on shared hardware;                         │
│  each VSAN has own name server, zone DB, and domain ID; ISSU for zero-downtime.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Platform Types                │  │              VSAN Architecture              │   │
│   │           Fixed: 9132T/9148T/9396T           │  │       VSAN: logical fabric on 1 switch      │   │
│   │           Director: 9706/9710/9718           │  │         Separate NS/zone DB per VSAN        │   │
│   │         ISSU: zero-downtime upgrade          │  │        Port VSAN assignment: per port       │   │
│   │         Dual supervisor (directors)          │  │          Domain ID: per VSAN unique         │   │
│   │        Linecard: modular port density        │  │        VSAN 1: default; avoid in prod       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  VSAN isolation: devices in different VSANs cannot communicate directly.                              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 FC Services                  │  │                  Management                 │   │
│   │           FCNS: fabric name server           │  │           DCNM/NDFC: central mgmt           │   │
│   │          FSPF: fabric shortest path          │  │            CLI: NX-OS SSH access            │   │
│   │         FLOGI: fabric login process          │  │           SNMP: v3 for monitoring           │   │
│   │         FDISC: N-port virtualisation         │  │           NTP: clock sync required          │   │
│   │         TE port: trunked E port ISL          │  │            AAA: TACACS+ or RADIUS           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  FC switches in dedicated SAN racks; A and B fabric physical separation;                              │
│  32G/64G SFP+ optics; separate out-of-band management on mgmt0 port.                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  NX-OS         = Cisco network OS for MDS (and Nexus) switches                                        │
│  VSAN          = Virtual SAN; logical fabric partition; own name server                               │
│  Domain ID     = 1-byte fabric-unique switch ID per VSAN                                              │
│  FCNS          = Fibre Channel Name Server; tracks WWN logins per VSAN                                │
│  FSPF          = Fabric Shortest Path First; FC routing protocol                                      │
│  ISSU          = In-Service Software Upgrade; zero-downtime NX-OS upgrade                             │
│  TE port       = Trunked E port; ISL carrying multiple VSANs                                          │
│  FLOGI         = Fabric Login; HBA logs in to get FC address (FCID)                                   │
│  FCID          = Fabric-assigned 3-byte address; domain.area.port                                     │
│  Zoning        = access control; same concept as Brocade; per VSAN                                    │
│  DCNM/NDFC     = Cisco fabric manager; discover, zone, monitor MDS                                    │
│  Director      = high-end chassis MDS; dual supervisors; ISSU capable                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Cisco MDS Architecture](../../../../assets/cisco-mds-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with DCNM/NDFC, storage arrays, and host connectivity.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Dual-fabric design, VSAN allocation, zoning model, and ISL standards.</span></a>
</div>

## Platform Reference

| Model | Type | Max FC Ports | Notes |
|---|---|---|---|
| MDS 9132T | Fixed | 32× 32G FC | Entry/mid-range |
| MDS 9148T | Fixed | 48× 32G FC | Mid-range |
| MDS 9396T | Fixed | 96× 32G FC | High-density fixed |
| MDS 9706 | Director | Up to 384 FC | Modular director — ISSU |
| MDS 9710 | Director | Up to 576 FC | Large-scale director — ISSU |

## Dual-Fabric Topology

