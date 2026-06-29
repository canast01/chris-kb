---
tags:
  - security
---
# Certificates — Authentication

<div class="kb-summary">
Authentication reference covering Root CA Lifecycle — Offline Operation Flow, Root CA Offline Procedure, Certificate Transparency (CT).
</div>

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "User / Service" as USR
participant "Authentication" as SVC
participant "Identity Provider\n(LDAP / OIDC / AD)" as IDP
participant "Token / Session Store" as TOKEN

USR -> SVC: Authentication request
SVC -> IDP: Validate credentials
IDP --> SVC: Identity confirmed
SVC -> TOKEN: Issue session token
TOKEN --> SVC: Token granted
SVC --> USR: Access allowed

note over SVC
  Root CA Lifecycle  Offline Operation Flow
  Root CA Offline Procedure
  Certificate Transparency (CT)
end note

@enduml
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Root CA Lifecycle — Offline Operation Flow

```d2
direction: right

rootNormal: "Root CA — powered off\n(air-gapped — HSM keys secured" {shape: rectangle}
powerOn: "Power on Root CA\nin secure ceremony room\n(2+ witnesses required" {shape: rectangle}
submitCSR: "Receive Subordinate CA CSR\n(from Issuing CA" {shape: rectangle}
signCert: "Sign Subordinate CA certificate\n(certreq -submit SubCA template" {shape: rectangle}
publishAD: "Publish new CA cert to AD\n(certutil -dspublish SubCA" {shape: rectangle}
powerOff: "Power off Root CA immediately\n(Stop-Computer -Force" {shape: rectangle}

rootNormal -> powerOn
powerOn -> submitCSR
submitCSR -> signCert
signCert -> publishAD
publishAD -> powerOff
powerOff -> rootNormal
```

## Root CA Offline Procedure

The Root CA is powered on only for these specific events:
1. Issuing a new Subordinate/Issuing CA certificate
2. Renewing the Root CA certificate itself
3. Updating the CRL (if Root CA issues CRL directly)

```powershell
# On Root CA — issue a subordinate CA certificate from a PKCS#10 CSR
certreq -submit -attrib "CertificateTemplate:SubCA" SubCA-Request.req SubCA-Certificate.cer

# After signing, power down Root CA immediately
Stop-Computer -Force
```

## Certificate Transparency (CT)

All publicly trusted certificates must be submitted to CT logs (required by CA/Browser Forum Baseline Requirements).

```bash
# Verify a certificate has SCT (Signed Certificate Timestamps) embedded
openssl x509 -in cert.pem -noout -text | grep -A 10 "CT Precertificate SCTs"

# Check certificate in public CT logs
# https://crt.sh/?q=<hostname> — search by domain
# curl example:
curl -s "https://crt.sh/?q=corp.example.com&output=json" | jq '.[0:5] | .[] | {id, issuer_name, not_before, not_after}'
```

## See also

- [Certificates — Access Control](../access-control/)
- [Certificates — Encryption](../encryption/)
- [Certificates — Security Hardening](../hardening/)
- [Certificates — Common Issues](../../troubleshooting/common-issues/)
