---
tags:
  - architecture
  - san
---
# Cisco DCNM — Architecture

<div class="kb-summary">
Cisco DCNM 11.x is the last standalone SAN management appliance for Cisco MDS environments. Starting with version 12.0 (2022), it was renamed Nexus Dashboard Fabric Controller (NDFC) and now runs as an application on the Cisco Nexus Dashboard platform.

*Applies to: Cisco MDS · Nexus*
</div>

```text
┌──────────────────────── Cisco DCNM Architecture — Last Standalone SAN Manager ────────────────────────┐
│                                                                                                       │
│  DCNM 11.x is the last standalone SAN management appliance; superseded by NDFC                        │
│  (Nexus Dashboard Fabric Controller) on Nexus Dashboard 12.0+.                                        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            DCNM 11.x Architecture            │  │               Managed Domains               │   │
│   │       Standalone Linux appliance (OVA)       │  │            SAN: Cisco MDS fabrics           │   │
│   │        PostgreSQL: config + topology         │  │         LAN: Nexus switching fabric         │   │
│   │          Elasticsearch: log search           │  │           Media: IP LAN for video           │   │
│   │          REST/SSH: switch discovery          │  │           DCNM licences per device          │   │
│   │            SNMP: event ingestion             │  │          Web UI: central management         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  DCNM 11.x end-of-support: migrate to Nexus Dashboard + NDFC for ongoing support.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Migration Path to NDFC            │  │           DCNM vs NDFC Differences          │   │
│   │        Deploy Nexus Dashboard 3-node         │  │           NDFC: app on ND platform          │   │
│   │          Install NDFC on ND cluster          │  │        NDFC: multi-tenant ND account        │   │
│   │         Re-discover switches in NDFC         │  │         NDFC: REST API v1 compatible        │   │
│   │         Export: templates + configs          │  │         ND: shared identity + scale         │   │
│   │         Cutover: update SNMP targets         │  │         DCNM: deprecated as of 12.0         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  DCNM: Linux OVA VM (16 vCPU, 64 GB RAM, 500 GB disk); management network                             │
│  access to all Cisco MDS and Nexus switches on TCP 22 (SSH) and 443.                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  DCNM          = Data Center Network Manager; Cisco SAN/LAN management v11                            │
│  NDFC          = Nexus Dashboard Fabric Controller; replacement for DCNM                              │
│  Nexus Dashboard= app-hosting platform; runs NDFC, NDI, NDO as apps                                   │
│  OVA           = Open Virtualization Appliance; VMware import format                                  │
│  EOS           = End of Support; DCNM 11.x reached EOS; migrate to NDFC                               │
│  SAN Insights  = DCNM feature; IO latency analytics per initiator-target pair                         │
│  LAN discovery = DCNM autodiscovery via CDP/LLDP from seed switch                                     │
│  SNMP          = trap receiver in DCNM for switch alerts                                              │
│  Template      = DCNM config template; import/export to NDFC                                          │
│  vRF           = virtual routing and forwarding; DCNM overlay construct                               │
│  ND account    = identity in Nexus Dashboard; DCNM → NDFC user migration                              │
│  Seed switch   = first switch discovered; DCNM expands via CDP                                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Cisco DCNM Architecture](../../../../assets/cisco-dcnm-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with MDS switches, LDAP, and SIEM.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Deployment model selection, sizing, and HA configuration standards.</span></a>
</div>

## Deployment Models

| Model | Description | HA |
|---|---|---|
| Standalone | Single DCNM server | None |
| Native HA | Active + standby with shared external DB and VIP | Yes |
| Federation | Multiple instances managing separate fabrics; single login (11.5+) | Per instance |

## Management Topology

