---
tags:
  - troubleshooting
  - security
  - known-issues
---
# Security — Known Issues Reference

<div class="kb-summary">
Index of security product known issues and error codes. This top-level page links to per-product known-issues catalogs.

*Applies to: CyberArk PAM, Venafi TPP, PKI / Certificates*
</div>

```text
┌────────────────────────────────── Security Products — Known Issues ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            Index linking CyberArk, Venafi, and Certificates/PKI known-issues pages            │   │
│   │                 Scope: PAM, certificate lifecycle, PKI — not a deployed system                │   │
│   │                           Management: N/A — documentation index only                          │   │
│   │              Identify product -> Open known-issues page -> Check dependency chain             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Topic            │  │           Resource          │  │            Notes            │   │
│   │         CyberArk PAM        │  │      Vault/PVWA/CPM/PSM     │  │      See cyberark page      │   │
│   │          Venafi TPP         │  │        Cert lifecycle       │  │       See venafi page       │   │
│   │          Certs/PKI          │  │        ADCS, OCSP/CRL       │  │    See certificates page    │   │
│   │          Dependency         │  │         AD/Kerberos         │  │    Often true root cause    │   │
│   │          Dependency         │  │           DNS/TLS           │  │    Cascading failure src    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │  CyberArk page   │ PAM troubleshoot │        N/A        │       N/A        │  cyberark page   │   │
│   │   Venafi page    │ Cert mgmt issues │        N/A        │       N/A        │   venafi page    │   │
│   │Certificates page │    PKI issues    │        N/A        │       N/A        │certs/known-issues│   │
│   │ Dependency chain │Root-cause method │        N/A        │       N/A        │Check AD/DNS/certs│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: N/A — documentation index page, not a deployed system                                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  PAM            = Privileged Access Management; CyberArk product category                             │
│  TPP            = Trust Protection Platform; Venafi cert lifecycle product                            │
│  PKI            = Public Key Infrastructure; certs, CAs, trust chains                                 │
│  ADCS           = Active Directory Certificate Services; MS CA role                                   │
│  OCSP           = Online Certificate Status Protocol; live revocation                                 │
│  CRL            = Certificate Revocation List; periodic publication                                   │
│  Dependency chain= security failures often cascade from AD/DNS/certs                                  │
│  DCOM           = legacy RPC mechanism used by some ADCS integrations                                 │
│  Cert discovery = scanning hosts/network for unmanaged certificates                                   │
│  Reconcile acct = CyberArk mechanism fixing out-of-sync passwords                                     │
│  Key length pol.= minimum RSA/ECC key size enforced by templates                                      │
│  Renewal autom. = ACME or vendor-API driven cert renewal                                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

Security product issues often cascade — a CyberArk CPM failure may stem from an AD authentication issue, which may stem from a certificate expiry. Follow the dependency chain.

## Security Product Known-Issues Pages

| Product | Known Issues |
|---|---|
| CyberArk PAM | [CyberArk — Known Issues](cyberark/troubleshooting/known-issues/) |
| Venafi TPP | [Venafi — Known Issues](venafi/troubleshooting/known-issues/) |
| Certificates / PKI | [Certificates — Known Issues](certificates/troubleshooting/known-issues/) |

## See also

- [Security — Common Issues](index.md)
- [Active Directory — Known Issues](../compute/windows-server/active-directory/troubleshooting/known-issues/)
- [TLS — Known Issues](../networking/protocols/tls/troubleshooting/known-issues/)
