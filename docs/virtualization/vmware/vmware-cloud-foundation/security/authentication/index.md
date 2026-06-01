# VCF Security — Authentication


<div class="kb-summary">
Authentication reference covering Common Issues, Related Reference.
</div>

VCF Authentication Flow
```text
┌─────────────────────────────────────────────────────┐
│  Operator / Admin                                   │
└──────────────────────┬──────────────────────────────┘
```
┌────────────────────────────── VMware Cloud Foundation — Authentication ───────────────────────────────┐
│                                                                                                       │
│  VCF authentication flows through SDDC Manager (API token), vCenter SSO (per domain),                 │
│  and NSX; vIDM provides unified identity across all VCF components.                                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              SDDC Manager Auth               │  │               Per-Domain Auth               │   │
│   │           Local users + AD groups            │  │         Each domain: own vCenter SSO        │   │
│   │             API: POST /v1/tokens             │  │             AD joined per domain            │   │
│   │            Bearer token: 24h TTL             │  │           SSO: local + AD identity          │   │
│   │            MFA: via RADIUS proxy             │  │          vIDM: optional unified SSO         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SDDC Manager token auth is separate from each domain SSO; both may need AD.                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               vIDM Integration               │  │              NSX Authentication             │   │
│   │         Unified identity across VCF          │  │            NSX: local + vIDM/LDAP           │   │
│   │           SAML federation to Aria            │  │            NSX token: 24h expiry            │   │
│   │           AD: one source per vIDM            │  │            NSX API: Bearer token            │   │
│   │             MFA: per vIDM policy             │  │           NSX UI: SSO via vCenter           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AD DCs must be reachable on management network; vIDM requires TCP 443 to AD and                      │
│  all VCF components; RADIUS server required for MFA.                                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vIDM         = VMware Identity Manager; unified SSO across VCF                                       │
│  SDDC Mgr token= bearer JWT; 24h TTL; POST /v1/tokens                                                 │
│  SAML         = Security Assertion Markup Language; federation format                                 │
│  vCenter SSO  = per-domain identity service; issues SAML tokens                                       │
│  RADIUS       = Remote Authentication Dial-In User Service; MFA backend                               │
│  Bearer token = JWT presented in Authorization header for API calls                                   │
│  AD joined    = vCenter SSO configured with AD as identity source                                     │
│  NSX token    = separate API token; 24h TTL; POST to NSX manager                                      │
│  MFA          = Multi-Factor Auth; enforced via vIDM or RADIUS policy                                 │
│  TTL          = Token Time-to-Live; renew before expiry for automation                                │
│  NSX SSO      = NSX UI login via vCenter SSO delegation                                               │
│  SAML to Aria = vIDM provides SAML assertions to Aria Operations/Logs                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
                       │ passes auth context to
          ┌────────────┼────────────┐
          ▼            ▼            ▼
```text
```
┌──────────────┐ ┌──────────────┐ ┌──────────────────┐
│ vCenter SSO  │ │ NSX Manager  │ │ SDDC Manager      │
│              │ │              │ │ Password Manager  │
│ Same AD      │ │ Same AD      │ │                   │
│ identity     │ │ identity     │ │ Rotates all       │
│ source       │ │ source       │ │ component creds   │
│              │ │              │ │ on schedule       │
└──────────────┘ └──────────────┘ └──────────────────┘
```text
┌────────────────────────────── VMware Cloud Foundation — Authentication ───────────────────────────────┐
│                                                                                                       │
│  VCF authentication flows through SDDC Manager (API token), vCenter SSO (per domain),                 │
│  and NSX; vIDM provides unified identity across all VCF components.                                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              SDDC Manager Auth               │  │               Per-Domain Auth               │   │
│   │           Local users + AD groups            │  │         Each domain: own vCenter SSO        │   │
│   │             API: POST /v1/tokens             │  │             AD joined per domain            │   │
│   │            Bearer token: 24h TTL             │  │           SSO: local + AD identity          │   │
│   │            MFA: via RADIUS proxy             │  │          vIDM: optional unified SSO         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SDDC Manager token auth is separate from each domain SSO; both may need AD.                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               vIDM Integration               │  │              NSX Authentication             │   │
│   │         Unified identity across VCF          │  │            NSX: local + vIDM/LDAP           │   │
│   │           SAML federation to Aria            │  │            NSX token: 24h expiry            │   │
│   │           AD: one source per vIDM            │  │            NSX API: Bearer token            │   │
│   │             MFA: per vIDM policy             │  │           NSX UI: SSO via vCenter           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AD DCs must be reachable on management network; vIDM requires TCP 443 to AD and                      │
│  all VCF components; RADIUS server required for MFA.                                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vIDM         = VMware Identity Manager; unified SSO across VCF                                       │
│  SDDC Mgr token= bearer JWT; 24h TTL; POST /v1/tokens                                                 │
│  SAML         = Security Assertion Markup Language; federation format                                 │
│  vCenter SSO  = per-domain identity service; issues SAML tokens                                       │
│  RADIUS       = Remote Authentication Dial-In User Service; MFA backend                               │
│  Bearer token = JWT presented in Authorization header for API calls                                   │
│  AD joined    = vCenter SSO configured with AD as identity source                                     │
│  NSX token    = separate API token; 24h TTL; POST to NSX manager                                      │
│  MFA          = Multi-Factor Auth; enforced via vIDM or RADIUS policy                                 │
│  TTL          = Token Time-to-Live; renew before expiry for automation                                │
│  NSX SSO      = NSX UI login via vCenter SSO delegation                                               │
│  SAML to Aria = vIDM provides SAML assertions to Aria Operations/Logs                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Common Issues

- Failed or stuck tasks.
- Certificate, DNS, or authentication issues.
- Capacity pressure.
- Service health warnings.
- Version mismatch after maintenance.
- Monitoring gaps.

### Operational Tasks

| Task | Command |
|---|---|
| Review alarms and events. |  |
| Confirm ownership and support notes. |  |
| Validate dependencies. |  |
| Document changes. |  |
| Confirm monitoring coverage. |  |

### Upgrade Notes

- Confirm compatibility.
- Review known issues.
- Confirm rollback plan.
- Validate health before and after the change.

### Best Practices

| Recommendation | Detail |
|---|---|
| Keep naming consistent. | Keep naming consistent. |
| Keep versions aligned. | Keep versions aligned. |
| Avoid unsupported version combinations. | Avoid unsupported version combinations. |
| Document exceptions. | Document exceptions. |
| Validate after every change. | Validate after every change. |
---

## Related Reference

- [Standard LDAP Integration](../../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
