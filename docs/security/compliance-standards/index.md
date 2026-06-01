# Compliance Standards

<div class="kb-summary">
Compliance Standards reference covering Framework Overview, ISO 27001 — Key Control Areas, PCI-DSS — Infra Control Checklist, CIS Controls — Priority Implementation, Evidence Collection for Audits and 1 more sections.
</div>
```text
┌──────────────────────────────────── Security Compliance Standards ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                  Compliance Standards: Security Compliance Standards platform                 │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                  Management: Security Compliance Standards management console                 │   │
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
│    Physical: Security Compliance Standards infrastructure · management network · monitoring           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Compliance Standards = Security Compliance Standards platform overview and core concepts           │
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
