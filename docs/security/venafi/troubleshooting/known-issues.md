---
tags:
  - troubleshooting
  - venafi
  - certificates
  - known-issues
---
# Venafi Trust Protection Platform — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Venafi TPP bugs, error codes, and workarounds covering certificate discovery, ADCS integration, and policy engine issues.

*Applies to: Venafi TPP 22.x / 23.x*
</div>

```text
┌───────────────────────────────────────── Venafi TLS Protect ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Machine identity management — certificate discovery, policy, and automation          │   │
│   │              Protocols: HTTPS (UI/API) · ACME · EST · REST · SSH cert management              │   │
│   │          Management: Venafi web UI · VCert CLI · REST API · ACME · Terraform provider         │   │
│   │          Scan -> discover cert -> policy check -> request from CA -> deploy + monitor         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │          Discovery          │  │       Network scanner       │  │        TLS port sweep       │   │
│   │            Policy           │  │        Policy folder        │  │      CA, key, SAN rules     │   │
│   │           Issuance          │  │         CA connector        │  │    DigiCert/MSCA/Entrust    │   │
│   │           Delivery          │  │      VCert / adaptable      │  │      Deploy to endpoint     │   │
│   │          Monitoring         │  │       Expiry dashboard      │  │     Alert before expiry     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │TPP / TLS Protect │ Central manager  │     HTTPS 443     │   LDAP / SAML    │ On-prem or cloud │   │
│   │   CA connector   │Cert issuance link│    CA-specific    │  CA admin creds  │  Per-CA plugin   │   │
│   │    VCert CLI     │ Cert automation  │    HTTPS (API)    │     API key      │  enroll + renew  │   │
│   │  Policy folder   │ Policy container │      Internal     │    Role-based    │Inheritable rules │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: Venafi server -> CA connectors -> managed endpoints (web, LB, app servers)                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TPP          = Trust Protection Platform; original on-prem Venafi product name                       │
│  TLS Protect  = current Venafi platform name; cloud or on-prem deployment                             │
│  Policy folder = Venafi object defining CA, key length, SAN, and renewal rules                        │
│  CA connector = plugin linking Venafi to a specific certificate authority                             │
│  VCert        = Venafi CLI tool for enroll/renew from pipelines and automation                        │
│  Discovery    = Venafi network scanner finding TLS certs on reachable hosts/ports                     │
│  Adaptable CA = custom Venafi driver for CAs without a built-in connector                             │
│  ACME         = RFC 8555 protocol supported by Venafi for automated cert issuance                     │
│  EST          = Enrollment over Secure Transport; RFC 7030 device enrolment                           │
│  Machine ID   = Venafi term for any TLS/SSH key managed by the platform                               │
│  Expiry alert = Venafi notification sent before a certificate expires (configurable)                  │
│  Terraform    = Venafi Terraform provider for IaC-driven cert lifecycle                               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Venafi errors appear in TPP UI → Monitor → Log.
- Venafi support logs: collected via `VenafiLog.ps1` or TPP Diagnostic → Log Collection.
- DCOM issues (port 135 + dynamic) are the most common ADCS CA integration problem.

## Certificate Issuance

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Certificate request fails: `CA unavailable` | TPP 22.x | TPP cannot reach ADCS CA on port 135 | Verify TCP 135 + dynamic RPC (49152-65535) from TPP to CA server | N/A |
| `Policy violation — key length too short` | TPP 22.x | Certificate template requesting 1024-bit RSA vs policy minimum | Update certificate request to use 2048/4096 RSA or P-256 ECC | N/A |
| `Certificate already exists in CA` | TPP 22.x | Duplicate CN in CA; TPP trying to re-issue without revoke | Revoke existing certificate in CA before re-issuing; or use `Force Reissue` option | N/A |

## Discovery

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Network discovery not finding certificates on hosts | TPP 22.x | Discovery engine cannot connect to target on 443 | Ensure discovery engine has network access to target hosts on 443 | N/A |
| `SSH key scan failed` for Linux hosts | TPP 22.x | TPP discovery account lacks SSH access | Verify TPP discovery account has SSH key configured; test SSH from TPP server | N/A |

## Satellite and Agents

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Venafi Satellite `Offline` in TPP | TPP 22.x | TCP 443 from Satellite to TPP Management UI blocked | Verify TCP 443 from Satellite host to TPP server | N/A |
| `Venafi agent not responding` on Windows host | TPP 22.x | VenafiAgent Windows service stopped | Restart: `Get-Service VenafiAgent | Start-Service` | N/A |

## See also

- [Venafi TPP — Common Issues](common-issues.md)
- [Certificates — Known Issues](../../certificates/troubleshooting/known-issues/)
- [Active Directory — Known Issues](../../../compute/windows-server/active-directory/troubleshooting/known-issues/)
