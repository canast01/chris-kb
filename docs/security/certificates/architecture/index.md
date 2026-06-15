---
tags:
  - architecture
  - security
---
# Certificates — Architecture

<div class="kb-summary">
Three-tier PKI hierarchy with offline Root CA, ADCS-backed Issuing CA, and commercial CA integrations; certificate lifecycle managed via auto-enrollment, OCSP revocation, and Venafi TPP.
</div>

```text
┌────────────────────────── Security Certificates Architecture — Architecture ──────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Certificates architecture overview: Security Certificates Architecture platform        │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │     Key components: Security Certificates Architecture, Management, Monitoring, Automation    │   │
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
│    Physical: Security Certificates Architecture infrastructure · management network · monitoring      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Certificates       = Security Certificates Architecture platform overview and core concepts        │
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


![Certificates Architecture](../../../assets/certificates-architecture-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="how-it-works/">
  <strong>How It Works</strong>
  <span>PKI hierarchy, certificate lifecycle, ADCS roles, CDP/AIA, and revocation flows.</span>
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

## PKI Tiers

| Tier | Role | Connectivity |
|---|---|---|
| Root CA | Trust anchor; signs Issuing CA certificates | Offline / air-gapped |
| Issuing CA (ADCS) | Day-to-day certificate issuance to internal hosts | Online |
| Issuing CA (Commercial) | External and publicly trusted certificates | Online (via API) |
| OCSP Responder | Real-time revocation status for relying parties | Online (HTTP) |
| CRL Distribution Point | Signed revocation list published on schedule | Online (HTTP / LDAP) |

## PKI Hierarchy

```mermaid
graph TB
  ROOT[("Root CA\n(offline — HSM)")] -->|"signs"| INT1["Intermediate CA 1\nInternal Issuing CA"]
  ROOT -->|"signs"| INT2["Intermediate CA 2\nPublic / External CA"]
  INT1 -->|"issues"| CERT1["Server Certificate"]
  INT1 -->|"issues"| CERT2["Client Certificate"]
  INT2 -->|"issues"| CERT3["Publicly Trusted Cert"]
  CERT1 & CERT2 & CERT3 -.->|"OCSP / CRL"| CRL["Revocation\nCRL / OCSP Responder"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  class ROOT store
  class INT1,INT2 ctrl
  class CERT1,CERT2,CERT3 host
  class CRL mgmt
```
