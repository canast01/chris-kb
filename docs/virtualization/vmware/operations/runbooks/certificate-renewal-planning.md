---
tags:
  - operations
---
# VMware Certificate Renewal Runbook


<div class="kb-summary">
VMware Certificate Renewal Runbook reference covering Identify the Expiring Certificate, Confirm Affected Products, Capture Current Certificate Details, Confirm Backup Exists, Schedule Maintenance Window and 4 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>

```text
┌───────────────────────────────── VMware Certificate Renewal Runbook ──────────────────────────────────┐
│                                                                                                       │
│    Plan certificate renewals early; capture pre/post evidence; test all integrations                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                   Planning                   │  │                  Execution                  │   │
│   │        ──────────────────────────────        │  │        ─────────────────────────────        │   │
│   │        Identify expiring certificate         │  │         Schedule maintenance window         │   │
│   │         Confirm type: SSL / STS / SU         │  │             Notify stakeholders             │   │
│   │          List all affected products          │  │          Run cert renewal procedure         │   │
│   │          Note integrations at risk           │  │           Post-change: login test           │   │
│   │        Capture: subject, SAN, expiry         │  │          Verify all integrations OK         │   │
│   │          Screenshot as pre-evidence          │  │         Capture post-change evidence        │   │
│   │        Confirm vCenter backup exists         │  │             Close change record             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Machine SSL = vCenter/ESXi HTTPS cert; presented to browsers and API clients                       │
│    STS cert    = Security Token Service cert; used for SAML token signing in SSO                      │
│    SU cert     = Solution User cert; used by vCenter services to authenticate to SSO                  │
│    SAN         = Subject Alternative Name; list of FQDNs the cert is valid for                        │
│    VMCA        = VMware Certificate Authority; built-in CA; issues certs to ESXi hosts                │
│    Expiry buffer = Renew at 60 days remaining; 30 days = urgent; 0 days = service outage              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Only restart services after confirming the new certificate is applied.

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Validate Integrations

- vCenter browser access — no certificate warning
- SSO login for local and AD accounts
- Aria, NSX, backup, and monitoring integrations confirmed

## Document Final Expiration Date

- Update the certificate inventory with the new expiration date
- Set a review reminder 60 days before the new expiration

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
