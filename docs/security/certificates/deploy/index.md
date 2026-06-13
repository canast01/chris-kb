---
tags:
  - deployment
  - security
search:
  boost: 1.5
---
# Certificates — Deploy

<div class="kb-summary">
Certificate infrastructure deployment — CA hierarchy build-out, ADCS configuration, and initial trust distribution.
</div>

```text
┌───────────────────────────────── Security Certificates — Deployment ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       PKI deployment sequence: Root CA → Issuing CA → CRL/OCSP → Templates → Enrolment       │    │
│   │            Root CA is offline/air-gapped; Issuing CA is domain-joined and always-on           │   │
│   │         CDP/AIA URLs must be planned before install — they are baked into every cert          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Plan → Root CA → Issuing CA → CRL/OCSP → Templates → Auto-enrolment → Validate                     │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Root CA             │  │         Issuing CA          │  │      CRL / OCSP             │   │
│   │   StandaloneRootCA          │  │   EnterpriseSubordinateCA   │  │   CDP: http://pki/CRL/      │   │
│   │   RSA-4096 · SHA-256        │  │   RSA-2048 · SHA-256        │  │   Online Responder port 80  │   │
│   │   20-year validity          │  │   5-year validity           │  │   CRL freshness alerting    │   │
│   │   Offline after config      │  │   Domain-joined, always-on  │  │   Publish after revocation  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│  CDP  = CRL Distribution Point; HTTP URL baked into every certificate; must remain reachable          │
│  AIA  = Authority Information Access; points to issuing CA cert and OCSP responder URLs               │
│  CSR  = Certificate Signing Request; generated on Issuing CA; signed by offline Root CA               │
│  NTAuth = AD store for enterprise CA certificates; all domain machines trust via GPO                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-1">

<a class="kb-card" href="pki-deployment/">
  <strong>PKI Hierarchy Deployment</strong>
  <span>Step-by-step guide for deploying an offline Root CA and domain-joined Issuing CA with CDP/AIA, certificate templates, and auto-enrollment.</span>
</a>

</div>

