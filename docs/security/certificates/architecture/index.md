# Certificates Architecture

Certificate infrastructure follows a three-tier PKI hierarchy: an offline, air-gapped Root CA at the trust anchor, an online Issuing CA for day-to-day certificate issuance, and optionally a Registration Authority (RA) to separate enrolment approval from issuance. The hierarchy flows Root → Intermediate → End-Entity, ensuring the Root CA private key is never exposed during normal operations.

Internal PKI is typically implemented with Microsoft ADCS or a standalone CA. External and public-facing services use commercial CAs (DigiCert, Entrust) or Let's Encrypt via ACME for automated issuance.

| Tier | Role | Online? |
|---|---|---|
| Root CA | Trust anchor; signs Intermediate CA certificates | Offline / air-gapped |
| Issuing / Intermediate CA | Issues end-entity certificates | Online |
| Registration Authority (RA) | Enrolment approval, identity verification | Online (optional) |
| Internal PKI | ADCS or standalone CA for internal services | Online |
| External PKI | DigiCert, Entrust, Let's Encrypt for public services | Cloud / SaaS |
