# Cisco DCNM — Architecture

<div class="kb-summary">
Cisco DCNM 11.x is the last standalone SAN management appliance for Cisco MDS environments. Starting with version 12.0 (2022), it was renamed Nexus Dashboard Fabric Controller (NDFC) and now runs as an application on the Cisco Nexus Dashboard platform.
</div>

```text
┌────────────────────────────────────── Cisco DCNM — Architecture ──────────────────────────────────────┐
│                                                                                                       │
│  DCNM (Data Center Network Manager): centralised SAN + LAN management for Cisco MDS/Nexus.            │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         How It Works        │  │         Integrations        │  │       Design Standards      │   │
│   │     OVA/ISO VM appliance    │  │    Cisco ISE: AAA policy    │  │    HA: primary + standby    │   │
│   │  Discovers via SNMP/NETCONF │  │     SIEM: syslog + SNMP     │  │     Mgmt VLAN isolation     │   │
│   │   SAN zoning + LAN config   │  │     ServiceNow CMDB sync    │  │    RBAC: read/write/admin   │   │
│   │   Topology: VSAN map view   │  │     REST API northbound     │  │      TLS 1.2/1.3 HTTPS      │   │
│   │   Firmware lifecycle mgmt   │  │     Email/SNMP alerting     │  │      2 TB storage perf      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  DCNM unifies SAN and LAN fabric management into one platform for Cisco data centers.                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Managed Resources      │  │          Data Layer         │  │       Management Layer      │   │
│   │  Cisco MDS 9000 FC switches │  │    PostgreSQL: config DB    │  │        Web GUI: HTTPS       │   │
│   │     Nexus switches (LAN)    │  │   Elastic: perf analytics   │  │      REST/RESTCONF API      │   │
│   │     VSAN zone databases     │  │     Time-series counters    │  │        DCNM CLI admin       │   │
│   │     SFP + HBA inventory     │  │     Config backup store     │  │     TACACS+/RADIUS auth     │   │
│   │    FC zone alias mapping    │  │      Audit event trail      │  │      SNMP trap receiver     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Linux VM on vSphere · management Ethernet · Cisco MDS switch management ports                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  DCNM            = Data Center Network Manager; Cisco SAN+LAN management platform                     │
│  VSAN            = Virtual SAN; logical FC fabric partition on MDS switches                           │
│  OVA             = Open Virtual Appliance; DCNM package for vSphere deployment                        │
│  SNMP            = Simple Network Management Protocol; used for device discovery/polling              │
│  NETCONF         = Network Configuration Protocol; XML-based switch configuration                     │
│  REST API        = DCNM northbound API; JSON/HTTPS for automation integration                         │
│  TACACS+         = centralised CLI and GUI auth; maps roles to DCNM permissions                       │
│  ISE             = Cisco Identity Services Engine; AAA policy and RADIUS/TACACS+                      │
│  PostgreSQL      = relational DB for DCNM configuration and inventory data                            │
│  Elasticsearch   = DCNM analytics DB; stores performance time-series data                             │
│  RBAC            = Role-Based Access Control; network-admin/operator/read-only                        │
│  SFP inventory   = transceiver data from switch; optical power + type + serial                        │
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


