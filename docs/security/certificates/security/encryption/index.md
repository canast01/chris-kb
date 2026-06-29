---
tags:
  - security
---
# Certificates — Encryption

<div class="kb-summary">
Encryption reference covering CA Key Protection Hierarchy, CA Key Protection, CRL Availability.
</div>

```d2
direction: down

ca_key_protection_hierarchy: "CA Key Protection Hierarchy" {shape: rectangle}
ca_key_protection: "CA Key Protection" {shape: rectangle}
crl_availability: "CRL Availability" {shape: rectangle}

ca_key_protection_hierarchy -> ca_key_protection: hardens
ca_key_protection -> crl_availability: hardens
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## CA Key Protection Hierarchy

```d2
direction: right

rootCA: "Root CA Private Key\nHSM — FIPS 140-2 Level 3\n(offline / air-gapped" {shape: rectangle}
issuingCA: "Issuing CA Private Key\nHSM or TPM-backed\n(online — issues end-entity certs" {shape: rectangle}
endEntity: "End-Entity Private Key\nSoftware key acceptable\n(generated on target host — never exported" {shape: rectangle}

rootCA -> issuingCA
issuingCA -> endEntity
```

## CA Key Protection

Root CA and Issuing CA private keys must be protected by HSMs — software-only key storage is not acceptable for CA keys.

| CA Tier | Key Storage Requirement | Online Status |
|---|---|---|
| Root CA | HSM (FIPS 140-2 Level 3 minimum) | Offline / air-gapped |
| Issuing CA | HSM or TPM-backed key | Online — issues end-entity certs |
| End-entity cert | Software key acceptable | Per-application |

```powershell
# Verify ADCS CA uses HSM-backed key (look for CSP = Microsoft Smart Card or nCipher)
certutil -getreg CA\CSP\Provider
# Desired: hardware CSP listed (e.g., "nFast RSA and DH" or "SafeNet")

# Check CA key protection on the issuing CA
certutil -store My | findstr /i "provider\|key"
```

## CRL Availability

CRL Distribution Points must remain highly available — unavailability can cause soft-fail clients to proceed with revoked certificates.

```bash
# Test CRL download
curl -I http://crl.example.local/IssuingCA.crl
# Verify: HTTP 200, Content-Type: application/pkix-crl

# Check CRL freshness (nextUpdate)
openssl crl -in IssuingCA.crl -inform DER -noout -text | grep "Next Update"
# CRL should be published at least 2x before expiry (overlap period)
```

```powershell
# Monitor CRL validity from ADCS CA
Get-ItemProperty -Path "HKLM:\System\CurrentControlSet\Services\CertSvc\Configuration\IssuingCA" |
    Select-Object CRLPeriodUnits, CRLPeriod, CRLDeltaPeriodUnits, CRLDeltaPeriod
```

## See also

- [Certificates — Access Control](../access-control/)
- [Certificates — Authentication](../authentication/)
- [Certificates — Security Hardening](../hardening/)
- [Certificates — Common Issues](../../troubleshooting/common-issues/)
