# PKI & Certificates — Learning Path

<div class="kb-summary">
Recommended reading order for PKI and certificate management. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```text
┌──────────────────────────────────── Certificates — Learning Path ─────────────────────────────────────┐
│                                                                                                       │
│    5 stages in order: Architecture → Deploy → Operations → Security → Troubleshoot                    │
│                                                                                                       │
│   ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐  ┌────────────────┐  ┌────────────────┐ │
│   │  Architecture  │  │     Deploy     │  │    Operations   │  │    Security    │  │  Troubleshoot  │ │
│   │                │  │                │  │                 │  │                │  │                │ │
│   │  How It Works  │  │ Initial Setup  │  │  Health Checks  │  │ Access Control │  │ Common Issues  │ │
│   │Design Standards│  │Install/Upgrade │  │  CLI Reference  │  │ Authentication │  │  Diagnostics   │ │
│   │  Integrations  │  │                │  │    Procedures   │  │   Encryption   │  │   Escalation   │ │
│   │                │  │                │  │ Backup & Restore│  │   Hardening    │  │                │ │
│   │                │  │                │  │     Scripts     │  │                │  │                │ │
│   └────────────────┘  └────────────────┘  └─────────────────┘  └────────────────┘  └────────────────┘ │
│                                                                                                       │
│    Stage 1 (Architecture) builds understanding. Stage 3 (Operations) is daily work. Troubleshoot last.│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```
## Stage 1 — Architecture

**Goal**: Understand the PKI trust model, CA hierarchy, certificate anatomy, and how certificates underpin TLS, code signing, and mutual authentication.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — X.509 certificate structure (Subject, Issuer, SAN, validity, key usage extensions), CA hierarchy (root CA offline, intermediate CA online), trust chain validation, certificate revocation (CRL, OCSP)
- [Design Standards](../architecture/design-standards/) — Two-tier vs three-tier CA hierarchy decisions, root CA key length and algorithm (RSA 4096 / ECDSA P-384), intermediate CA offline storage, SAN vs wildcard certificate policy, certificate lifecycle design (issuance, renewal, revocation)
- [Integrations](../architecture/integrations/) — ACME protocol and Let's Encrypt for public certificates, Microsoft ADCS for internal PKI, HashiCorp Vault PKI secrets engine, Venafi TLS Protect integration, certificate stores: JKS (Java), PEM (Linux), PFX/PKCS12 (Windows)

**Why first**: Every operational procedure — CSR generation, signing, deployment, renewal — only makes sense once you understand the trust chain and why certificate fields matter.

---

## Stage 2 — Deployment

**Goal**: Stand up an internal CA, issue first certificates, and configure trust distribution to endpoints.

**Read**:

- [Deploy](../deploy/) — Internal CA deployment (Microsoft ADCS or Vault PKI), root CA ceremony procedure, intermediate CA issuance, trust anchor distribution to OS certificate stores, ACME client configuration for automated renewal
- [PKI Deployment](../deploy/pki-deployment/) — Step-by-step CA hierarchy build, HSM integration for root CA key protection, CRL/OCSP responder deployment

---

## Stage 3 — Operations

**Goal**: Execute the CSR/sign/deploy cycle, manage renewals before expiry, and maintain certificate inventory.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — Run the routine first on every shift; scan for certificates expiring within 30/60/90 days, validate OCSP responder availability, check CRL freshness
- [CLI Reference](../operations/cli-reference/) — `openssl` command reference: `req`, `x509`, `pkcs12`, `verify`, `s_client`; `certutil` on Windows; `keytool` for JKS management; ACME client CLI
- [Procedures](../operations/procedures/) — CSR generation for a new service, CA signing workflow (internal vs external CA), certificate deployment to web server/load balancer/application, emergency revocation procedure
- [Certificate Trust](../operations/certificate-trust/) — Installing CA chains into OS trust stores (Linux `/etc/pki`, Windows certmgr), Java cacerts update, application-specific trust store management
- [Backup & Restore](../operations/backup-restore/) — CA database backup, private key escrow and recovery procedure, certificate store backup before renewal
- [Scripts](../operations/scripts/) — Automated expiry scanning scripts, ACME auto-renewal hooks, certificate deployment automation for Nginx/Apache/F5

---

## Stage 4 — Security

**Goal**: Protect CA private keys, enforce certificate policy, and prevent certificate misuse.

**Read**:

- [Access Control](../security/access-control/) — CA administrator role separation, certificate requestor vs approver workflow, ADCS template permission ACLs
- [Authentication](../security/authentication/) — Client certificate mutual TLS (mTLS) configuration, certificate-based SSH authentication, code signing certificate controls
- [Encryption](../security/encryption/) — CA private key protection (HSM, air-gapped root), TLS 1.2+ enforcement on CA web enrollment, PKCS12 export password requirements
- [Hardening](../security/hardening/) — Root CA kept offline (powered off when not in use), short intermediate CA validity periods, CT log monitoring for rogue certificates, certificate pinning considerations

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose expired certificate errors, trust chain failures, and OCSP/CRL validation issues.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — TLS handshake failure (certificate expired, untrusted CA, SAN mismatch), OCSP stapling not working, CRL too large causing validation timeout, JKS/PFX password mismatch
- [Diagnostics](../troubleshooting/diagnostics/) — `openssl s_client -connect`, `openssl verify`, `openssl x509 -text`, browser certificate chain inspector, `certutil -verify` on Windows, OCSP responder test
- [Escalation](../troubleshooting/escalation/) — CA vendor support for ADCS or Vault issues, escalation for suspected CA compromise (revoke intermediate), public CA misissuance report via CT logs

**Why last**: Certificate errors are almost always caused by misunderstanding the trust chain or expiry model — both established in the Architecture stage before any operational work.
