---
title: MFA
---

# Multi-Factor Authentication (MFA)


<div class="kb-summary">
Multi-Factor Authentication (MFA) reference covering Overview, MFA Authentication Flow, TOTP vs Push Comparison, Daily Checks, Health Commands and 1 more sections.
</div>
```
┌──────────────────────────────────────────── Security Mfa ─────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   Mfa: Security Mfa platform                                  │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                          Management: Security Mfa management console                          │   │
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
│    Physical: Security Mfa infrastructure · management network · monitoring                            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Mfa                = Security Mfa platform overview and core concepts                              │
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


## Overview

MFA adds an additional authentication factor beyond passwords to protect accounts and systems from unauthorized access.

## MFA Authentication Flow

```text
  User                  Identity Provider (IdP)          MFA Service           Application
    │                            │                            │                     │
    │── Username + Password ────►│                            │                     │
    │                            │── Validate credentials ───►│                     │
    │                            │◄── Primary auth OK ────────│                     │
    │                            │                            │                     │
    │                            │── Trigger MFA challenge ──►│                     │
    │◄── MFA challenge sent ─────│   (push / OTP / hardware)  │                     │
    │                            │                            │                     │
    │── OTP / Approve push ─────────────────────────────────►│                     │
    │                            │◄── Factor confirmed ───────│                     │
    │                            │                            │                     │
    │◄── Auth token (SAML/OIDC) ─│                            │                     │
    │                            │                            │                     │
    │── Present token ────────────────────────────────────────────────────────────►│
    │◄── Access granted ──────────────────────────────────────────────────────────│
    │                            │                            │                     │
    │                    [Session established — token TTL enforced]                │
```

## TOTP vs Push Comparison

```text
  TOTP (Time-based OTP)                Push Notification
  ──────────────────────────────────   ─────────────────────────────────────────
  User generates 6-digit code          IdP sends push to registered device
  Code derived from shared secret      User taps Approve / Deny
  Valid for 30-second window           Out-of-band — does not traverse browser
  Works offline (no network needed)    Requires network on mobile device
  Phishing-resistant if typed once     Vulnerable to MFA fatigue (auto-accept)
  Hardware token: highest assurance    Number-matching mitigates fatigue attacks
```

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| Review authentication failures |  |  |
| Validate MFA service availability |  |  |
| Confirm token synchronization |  |  |
| Review access logs |  |  |

## Health Commands

```bash
Get-MsolUser
Get-MsolCompanyInformation
```

## Upgrade Workflow

1. Backup configuration
2. Validate identity provider connectivity
3. Apply updates
4. Test user authentication flows
