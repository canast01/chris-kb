# Venafi — Architecture

<div class="kb-summary">
Enterprise certificate lifecycle management — TPP enforces policy, integrates with ADCS and commercial CAs, automates renewal via CA connectors, and provides visibility across all managed certificates; SQL Server-backed HA pair behind a load balancer.
</div>
```
┌───────────────────────────── Security Venafi Architecture — Architecture ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              Venafi architecture overview: Security Venafi Architecture platform              │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │        Key components: Security Venafi Architecture, Management, Monitoring, Automation       │   │
│   │          Design principles: HA, scalability, non-disruptive operations, and security          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Design → deploy → configure → validate → monitor → optimise                                        │
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
│    Physical: Security Venafi Architecture infrastructure · management network · monitoring            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Venafi             = Security Venafi Architecture platform overview and core concepts              │
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


![Venafi Architecture](../../../assets/venafi-architecture-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="how-it-works/">
  <strong>How It Works</strong>
  <span>Policy tree, CA connectors, certificate lifecycle, HA topology, and network requirements.</span>
</a>

<a class="kb-card" href="integrations/">
  <strong>Integrations</strong>
  <span>Integration with other platforms and external systems.</span>
</a>

<a class="kb-card" href="design-standards/">
  <strong>Design Standards</strong>
  <span>Sizing guidelines, design standards, and best practices.</span>
</a>

</div>

## Component Overview

| Component | Role | Deployment |
|---|---|---|
| Policy Server | Lifecycle management, CA integration, policy enforcement | On-prem VM (primary + secondary) |
| Edge Proxy | Certificate discovery across segmented networks | Lightweight on-prem agent |
| Log Server | Audit event aggregation and SIEM forwarding | On-prem VM or syslog target |
| VaaS / TLS Protect Cloud | SaaS alternative to TPP | Hosted by Venafi |
| CA Connectors | Integration adapters for ADCS, DigiCert, Entrust | Configured on Policy Server |
| Venafi SDK / REST API | Automation and integration interface | Consumed by CI/CD and scripts |

## Trust Protection Platform Topology

```mermaid
graph TB
  TPP["Venafi Trust Protection Platform"]
  TPP --> DISC["Discovery Engine\n(network scan / agent)"]
  TPP --> CA1["CA Connector — ADCS"]
  TPP --> CA2["CA Connector — DigiCert / Entrust"]
  TPP --> AUTO["Automation\n(renewal / provisioning)"]
  DISC -->|"found certs"| TPP
  ADMIN(["Security Admin"]) -->|"portal"| TPP
  TPP -->|"SIEM / SNMP"| SIEM(["SIEM / Monitoring"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class TPP,DISC ctrl
  class CA1,CA2,AUTO mgmt
  class ADMIN,SIEM host
```
