---
tags:
  - architecture
  - security
---
# Certificates — Architecture

<div class="kb-summary">
Three-tier PKI hierarchy with offline Root CA, ADCS-backed Issuing CA, and commercial CA integrations; certificate lifecycle managed via auto-enrollment, OCSP revocation, and Venafi TPP.
</div>

![Certificates — Architecture — Diagram](../../../assets/security-certificates-architecture-diagram.svg)


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
