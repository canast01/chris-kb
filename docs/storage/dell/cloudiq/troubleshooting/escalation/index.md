---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# CloudIQ — Escalation


<div class="kb-summary">
Escalation reference covering Support Portal, Opening a Case, Information to Collect, SLA Tiers, Escalation.
</div>

```text
┌─────────────────────────────────────── Dell CloudIQ Escalation ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Escalate CloudIQ issues to Dell Support with SR; attach SCG log bundle and API trace     │   │
│   │        SCG issues: collect scg logs, note SCG version, capture connectivity test output       │   │
│   │         CloudIQ data issues: note system name, time window, expected vs actual values         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Before Escalating               │  │               Escalation Steps              │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │          SCG version (scg version)           │  │         Open SR at support.dell.com         │   │
│   │           Connectivity test output           │  │            Attach SCG log bundle            │   │
│   │           SCG log bundle collected           │  │           Note affected system IDs          │   │
│   │          Affected system name + ID           │  │            CloudIQ org ID from UI           │   │
│   │             Time window of issue             │  │        Request CloudIQ backend check        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SR             = Service Request; Dell support case opened at support.dell.com                     │
│    CloudIQ org ID = Unique identifier for your CloudIQ tenant; visible in Settings > Org              │
│    Backend check  = Dell CloudIQ SRE team investigates ingest pipeline for missing data               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Additional items:

- SCG application logs from `/var/log/dsagw/` (compress and attach to the case).
- CloudIQ API error response body with HTTP status code and timestamp.
- Browser console errors (F12 > Console) if the issue is UI-related — export as a log file.
- CloudIQ audit log export (Admin > Audit Log) for the relevant time window if the issue involves access or configuration.

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## SLA Tiers

CloudIQ support SLA follows the ProSupport Plus contract of the managed storage system. There is no separate CloudIQ SLA.

| Priority | Condition | Response Time | Coverage |
|---|---|---|---|
| P1 | CloudIQ outage causing inability to monitor production systems | 2 hours | 24x7x365 |
| P2 | Degraded CloudIQ functionality (partial data, delayed alerts) | 4 hours | 24x7x365 |
| P3 | Non-critical CloudIQ issue (UI display, API edge case) | Next business day | Business hours |
| P4 | General question or enhancement request | Next business day | Business hours |

## Escalation

For SaaS platform-level issues (CloudIQ dashboard unavailable, systemic reporting failures across all systems):

1. Open a P1 support case and specify that the issue is a **CloudIQ SaaS platform issue** affecting all managed systems.
2. Contact your **Dell account team** and request escalation to the **CloudIQ product team**. The CloudIQ engineering team can investigate SaaS-side infrastructure issues that front-line support cannot resolve.
3. Check [https://www.dell.com/support/incidents-outages](https://www.dell.com/support/incidents-outages) or the Dell support portal for any announced CloudIQ service incidents before escalating — platform maintenance or incidents may already be tracked.
4. For prolonged SaaS outages affecting contractual monitoring obligations, request engagement through **Dell Global Priority Services** via your account team.

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
