# SANnav — Architecture

<div class="kb-summary">
Brocade SANnav is a SAN management platform in two variants: Management Portal (per-fabric operations) and Global View (multi-portal aggregation). Deployed as Linux virtual appliances; communicates with switches via HTTPS and SNMP v3.
</div>

```text
┌──────────────────────────────────── Brocade SANnav — Architecture ────────────────────────────────────┐
│                                                                                                       │
│  SANnav: centralised SAN management platform for Brocade FC fabrics, zoning, and analytics.           │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         How It Works        │  │         Integrations        │  │       Design Standards      │   │
│   │   SANnav OVA: VM appliance  │  │      DCNM / NDFC import     │  │    HA: primary + standby    │   │
│   │ Discovers via SNMP/REST API │  │    syslog forward to SIEM   │  │      Separate mgmt VLAN     │   │
│   │  Zone management GUI + API  │  │       TACACS+ for auth      │  │      Role-based access      │   │
│   │    MAPS alert aggregation   │  │   REST API for automation   │  │      Backup to NFS/SCP      │   │
│   │     Firmware management     │  │     Email/SNMP alerting     │  │       TLS 1.2/1.3 only      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  SANnav aggregates all Brocade fabric management into one GUI and REST API endpoint.                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Managed Resources      │  │          Data Layer         │  │       Management Layer      │   │
│   │     Brocade FC switches     │  │    PostgreSQL DB: config    │  │        Web GUI: HTTPS       │   │
│   │      Brocade Directors      │  │   Elasticsearch: analytics  │  │     REST API: token auth    │   │
│   │     Virtual Fabrics (VF)    │  │    Time-series perf data    │  │      CLI: sannav-admin      │   │
│   │      FC zone databases      │  │     Configuration backup    │  │      LDAP/TACACS+ auth      │   │
│   │    SFP inventory per port   │  │      Audit trail events     │  │      SNMP trap receiver     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Linux VM (OVA) on vSphere · management Ethernet · Brocade FC switch management ports                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SANnav          = Broadcom SAN Navigator; management platform for Brocade FC fabrics                 │
│  OVA             = Open Virtual Appliance; pre-built VM image for vSphere deployment                  │
│  MAPS            = Monitoring and Alerting Policy Suite; threshold alerts from switches               │
│  Virtual Fabric  = logical switch partitioning on Brocade directors; managed per-VF                   │
│  REST API        = SANnav northbound API; JSON over HTTPS for automation integration                  │
│  Elasticsearch   = search and analytics engine; stores SANnav performance time-series                 │
│  PostgreSQL      = relational database storing SANnav configuration and inventory                     │
│  SFP             = Small Form-factor Pluggable transceiver; FC port optical module                    │
│  Zone database   = set of zones and aliases defining which devices can communicate                    │
│  TACACS+         = Terminal Access Controller Auth; centralised SANnav user auth                      │
│  HA pair         = SANnav primary + standby; standby takes over if primary fails                      │
│  Audit trail     = log of all user actions in SANnav; retained for compliance                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![SANnav Architecture](../../../../assets/sannav-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with Brocade FC switches, vCenter, LDAP, and SIEM.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Sizing guidelines, HA design, and deployment best practices.</span></a>
</div>

## VM Sizing

| Variant | Environment | vCPU | RAM | Storage | Max Switches |
|---|---|---|---|---|---|
| Management Portal | Small | 8 | 32 GB | 300 GB | 50 |
| Management Portal | Medium | 16 | 64 GB | 500 GB | 150 |
| Management Portal | Large | 24 | 96 GB | 1 TB | 300 |
| Global View | Standard | 8 | 32 GB | 500 GB | 10 portals |

## Management Topology


