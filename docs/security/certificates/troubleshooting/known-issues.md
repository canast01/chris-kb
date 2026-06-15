---
tags:
  - troubleshooting
  - certificates
  - pki
  - tls
  - known-issues
---
# Certificates / PKI — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known PKI and certificate bugs, error codes, and workarounds covering ADCS, OCSP, CRL, and ACME / Let's Encrypt.

*Applies to: Microsoft ADCS, Let's Encrypt, general TLS/PKI*
</div>

```text
┌──────────────────────────────── Security Certificates Troubleshooting ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                  Certificates: Security Certificates Troubleshooting platform                 │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │              Management: Security Certificates Troubleshooting management console             │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
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
│    Physical: Security Certificates Troubleshooting infrastructure · management network · monitoring   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Certificates       = Security Certificates Troubleshooting platform overview and core concepts     │
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


## Before you begin

- Certificate errors surface in many forms — browser warnings, application SSL errors, or authentication failures.
- Diagnose with: `openssl s_client -connect <host>:443` to inspect the certificate chain.
- OCSP and CRL responders must be reachable from all client zones — this is the most common silent failure.

## ADCS

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `The RPC server is unavailable` when connecting to CA | ADCS | TCP 135 + dynamic RPC range blocked | Open 135 + 49152-65535 TCP from requestor to CA; or use ADCS Web Enrollment (443) | N/A |
| Certificate template not visible to end users | ADCS | Template not published to AD; enrollment permissions missing | Publish template: CA MMC → Certificate Templates → New → Certificate Template to Issue | N/A |
| `Denied by policy module` during enrollment | ADCS | Certificate template requires manager approval; or SAN not matching policy | Check policy module settings; or use autoenrollment group policy | N/A |
| ADCS Web Enrollment 404 after CA server patch | ADCS | IIS CertSrv role broken by Windows update | Reinstall IIS `CertificateServices` role via Server Manager | N/A |

## OCSP / CRL

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `OCSP responder not responding` — certificate validation fails | All | HTTP port 80 blocked to OCSP URL | Open TCP 80 from client networks to OCSP responder URL (embedded in cert AIA extension) | N/A |
| CRL `This certificate has an invalid digital signature` | All | CRL expired; CA not publishing new CRL | Manually publish CRL: `certutil -crl` on ADCS CA server | N/A |
| Application shows `revocation check failed` despite valid cert | All | CRL Distribution Point URL not reachable | Verify CDP URL in cert with `certutil -dump <cert>` is reachable from client | N/A |

## Let's Encrypt / ACME

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| HTTP-01 challenge fails: `Connection refused on port 80` | Let's Encrypt | Inbound port 80 blocked from LE validation servers to ACME client | Open inbound TCP 80 from internet; or switch to DNS-01 challenge | N/A |
| `Rate limit exceeded` | Let's Encrypt | Too many certificate issuances for the same domain in 7 days | Wait 7 days; use Let's Encrypt staging environment for testing | N/A |
| `Certificate not yet valid` immediately after issuance | Let's Encrypt | Client clock skew; cert validity starts in future relative to client | Sync NTP on client; check clock accuracy | N/A |

## General TLS

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `SSL_ERROR_RX_RECORD_TOO_LONG` in browser | All | Server sending plaintext on HTTPS port; or TLS version mismatch | Verify server is actually serving TLS; check server TLS config | N/A |
| `Certificate name mismatch` warning | All | CN or SAN in cert doesn't match hostname | Reissue cert with correct SAN; modern browsers ignore CN — must use SAN | N/A |

## See also

- [Certificates — Common Issues](common-issues.md)
- [Venafi — Known Issues](../../venafi/troubleshooting/known-issues/)
- [Active Directory — Known Issues](../../../compute/windows-server/active-directory/troubleshooting/known-issues/)
