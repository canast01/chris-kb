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

```d2
direction: right

ROOT: "Root CA\n(offline — HSM" {shape: rectangle}
INT1: "Intermediate CA 1\nInternal Issuing CA" {shape: rectangle}
INT2: "Intermediate CA 2\nPublic / External CA" {shape: rectangle}
CERT1: "Server Certificate" {shape: rectangle}
CERT2: "Client Certificate" {shape: rectangle}
CERT3: "Publicly Trusted Cert" {shape: rectangle}

ROOT -> INT1
ROOT -> INT2
INT1 -> CERT1
INT1 -> CERT2
INT2 -> CERT3
```
