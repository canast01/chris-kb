---
tags:
  - security
description: "Compliance Standards reference covering Framework Overview, ISO 27001 — Key Control Areas, PCI-DSS — Infra Control Checklist, CIS Controls — Priority..."
---
# Compliance Standards

<div class="kb-summary">
Compliance Standards reference covering Framework Overview, ISO 27001 — Key Control Areas, PCI-DSS — Infra Control Checklist, CIS Controls — Priority Implementation, Evidence Collection for Audits and 1 more sections.
</div>

<div class="kb-grid">
  <a class="kb-card" href="operations/">
    <div class="kb-card-icon">⚙️</div>
    <div class="kb-card-title">Operations</div>
    <div class="kb-card-desc">Framework controls, evidence collection, gap assessments, audit preparation</div>
  </a>
</div>

## Framework Overview

| Framework | Focus | Typical Audience |
|---|---|---|
| ISO 27001 | Information security management system (ISMS) | All industries |
| SOC 2 Type II | Controls relevant to security, availability, processing integrity, confidentiality, privacy | SaaS / service providers |
| PCI-DSS | Payment card data security | Any entity processing card payments |
| NIST CSF | Cybersecurity framework (Identify, Protect, Detect, Respond, Recover) | US federal and broader |
| GDPR | Data privacy and protection | Any entity processing EU personal data |
| CIS Controls | Prioritised security controls | Practical baseline for most orgs |

## ISO 27001 — Key Control Areas

| Annex A Area | What Infra Teams Own |
|---|---|
| A.8 — Asset management | Asset inventory, classification, ownership |
| A.9 — Access control | RBAC, privileged access, account reviews |
| A.10 — Cryptography | Encryption at rest/in transit, key management |
| A.12 — Operations security | Change management, capacity, malware controls |
| A.13 — Communications security | Network segmentation, monitoring |
| A.17 — Business continuity | DR plans, backup, recovery testing |
| A.18 — Compliance | Legal, audit logging, license management |

## PCI-DSS — Infra Control Checklist

| Requirement | Control |
|---|---|
| 1 — Firewall | Network segmentation; cardholder data environment (CDE) isolated |
| 2 — Defaults | No vendor default passwords; hardened configs |
| 6 — Patching | Critical patches within 1 month; all patches within 3 months |
| 7 — Access | Least-privilege; need-to-know for CDE access |
| 8 — Auth | MFA for all CDE admin access; no shared accounts |
| 10 — Audit log | Log all CDE access; retain 1 year (3 months immediately accessible) |
| 11 — Testing | Internal/external vulnerability scans quarterly; pen test annually |

## CIS Controls — Priority Implementation

**Basic (implement first):**
1. Inventory of authorised/unauthorised devices
2. Inventory of authorised/unauthorised software
3. Continuous vulnerability management
4. Controlled use of administrative privileges
5. Secure configuration for hardware and software
6. Maintenance, monitoring, and analysis of audit logs

**Foundational:**
7–16: Email/browser protection, malware defences, data recovery, network config, boundary defence, data protection, access control, wireless control, account monitoring, security skills

## Evidence Collection for Audits

| Control Area | Evidence Type | Where to Get It |
|---|---|---|
| Patch compliance | Patch scan report | Vulnerability scanner (Tenable, Qualys) |
| Access reviews | Signed review records | HR system / ITSM |
| MFA enforcement | AD/Entra ID sign-in report | Azure AD → Sign-in logs |
| Encryption at rest | Storage config export | Array vendor; BitLocker/LUKS reports |
| Audit logging | SIEM index retention config | Splunk / Graylog |
| Backup testing | Recovery test records | Veeam / CommVault job logs |
| Change management | Change tickets | ServiceNow / Jira |

## Gap Assessment Template

```markdown
Control:          [control name or ID]
Requirement:      [what the framework requires]
Current state:    [what is actually in place]
Gap:              [what is missing or insufficient]
Risk level:       [High / Medium / Low]
Owner:            [person/team responsible]
Remediation:      [what needs to be done]
Due date:         [target date]
```
