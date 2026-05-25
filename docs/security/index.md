# Security

```
┌──────────────────────────────────────────────────────────────────────┐
│                     Security Overview                                │
│                                                                      │
│  ┌─────────────────────┐        ┌──────────────────────────────┐     │
│  │   Identity (PAM)    │        │    Certificate / PKI          │    │
│  │   CyberArk Vault    │        │    Venafi · Internal CA       │    │
│  │   CPM rotation      │        │    Cert lifecycle mgmt        │    │
│  │   PSM session proxy │        └──────────────────────────────┘     │
│  └────────┬────────────┘                                             │
│           │  privileged access                                       │
│  ┌────────▼────────────────────────────────────────────────────┐     │
│  │              Infrastructure (all platforms)                 │     │
│  │       vSphere · NSX · Storage arrays · Network devices       │    │
│  └────────┬────────────────────────────────────────────────────┘     │
│           │                                                          │
│  ┌────────▼────────────┐        ┌──────────────────────────────┐     │
│  │   Vulnerability     │        │    Incident Response         │     │
│  │   Management        │        │    Detect ► Contain          │     │
│  │   Scan ► CVSS ► fix │        │    Eradicate ► Recover       │     │
│  └─────────────────────┘        └──────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────────┘
```

## Shared Reference

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="ldap-integration/"><strong>Standard LDAP Integration</strong><span>Canonical LDAP/AD field reference, service account standards, TLS requirements, connectivity testing, and common issues.</span></a>
<a class="kb-card" href="saml-configuration/"><strong>Standard SAML Configuration</strong><span>SAML 2.0 SSO reference: SP/IdP setup, Azure AD and Okta steps, attribute mapping, security requirements, and troubleshooting.</span></a>
</div>

## Platforms

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="active-directory/"><strong>Active Directory</strong><span>AD architecture, standards, lifecycle, operations, CLI, scripts, troubleshooting, and security.</span></a>
<a class="kb-card" href="cyberark/"><strong>CyberArk</strong><span>PAM platform — vault, safes, CPM rotation, PSM session recording, architecture, and operations.</span></a>
<a class="kb-card" href="venafi/"><strong>Venafi</strong><span>Machine identity management — certificate lifecycle, policy, automation, and CA integration.</span></a>
<a class="kb-card" href="certificates/"><strong>Certificates</strong><span>PKI architecture, certificate standards, lifecycle, renewal, chain management, and troubleshooting.</span></a>
</div>

## Operations

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="access-review/"><strong>Access Review</strong><span>Periodic review of user and service account access rights to enforce least privilege.</span></a>
<a class="kb-card" href="compliance-standards/"><strong>Compliance Standards</strong><span>CIS, NIST, ISO 27001, PCI, and internal compliance frameworks with audit mapping.</span></a>
<a class="kb-card" href="incident-handling/"><strong>Incident Handling</strong><span>Security incident response: detection, containment, eradication, recovery, and lessons learned.</span></a>
<a class="kb-card" href="mfa/"><strong>MFA</strong><span>Multi-factor authentication configuration, enforcement policies, and troubleshooting.</span></a>
<a class="kb-card" href="patch-compliance/"><strong>Patch Compliance</strong><span>Patch status reporting, missing patch identification, and remediation tracking.</span></a>
<a class="kb-card" href="pki/"><strong>PKI</strong><span>CA hierarchy, certificate templates, enrollment, revocation, CRL, and OCSP.</span></a>
<a class="kb-card" href="security-audit/"><strong>Security Audit</strong><span>Security posture audit covering accounts, configurations, patching, and access controls.</span></a>
<a class="kb-card" href="security-monitoring/"><strong>Security Monitoring</strong><span>SIEM, log analysis, threat detection, and alert triage for security events.</span></a>
<a class="kb-card" href="vulnerability-management/"><strong>Vulnerability Management</strong><span>Scan scheduling, CVSS-based prioritization, remediation tracking, and exception handling.</span></a>
</div>
