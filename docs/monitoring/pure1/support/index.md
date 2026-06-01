# Pure1 — Support


<div class="kb-summary">
Support reference covering Diagnostic Bundle Collection, Severity Definitions, Evergreen Support — What's Covered, Proactive Support Features, Escalation Path and 1 more sections.
</div>

```text
┌───────────────────────────────────── Pure1 — Support Integration ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               Pure1 Support: proactive TAC case creation and remote diagnostics               │   │
│   │               Auto-case: Pure1 ML opens TAC case before customer notices failure              │   │
│   │          Case includes: diagnostic bundle, array serial, failure signature, priority          │   │
│   │           Remote assist: Pure engineer connects to array via encrypted Pure1 tunnel           │   │
│   │               Proactive swap: replacement hardware staged before failure occurs               │   │
│   │                      View cases: pure1.purestorage.com > Support > Cases                      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Cases opened in Pure cloud · engineer accesses array via Pure1 secure tunnel                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Auto-case = Pure1 opening TAC case automatically on pre-failure detection                            │
│  Diagnostic bundle = Phonehome data + Purity log snapshot attached to case                            │
│  Remote assist = Pure engineer SSH-ing to array through Pure1 encrypted tunnel                        │
│  Proactive swap = Pure dispatching replacement drive/module before failure                            │
│  Case priority = Sev-1 for pre-failure; Sev-2 for degraded; Sev-3 for advisory                        │
│  Encrypted tunnel = Pure1 remote access over customer-approved secure channel                         │
│  Customer approval = Remote access requires explicit opt-in per session                               │
│  TAC = Pure Storage Technical Assistance Centre; 24x7 for Sev-1                                       │
│  Case view = All open and historical cases visible in Pure1 Support portal                            │
│  Manual case = Open at support.purestorage.com if auto-case not triggered                             │
│  Evergreen = All-inclusive support model; no per-incident charges                                     │
│  Phonehome = Required for auto-case and remote assist; must be enabled and connected                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Bundles include: system logs, configuration, performance data, hardware status, and event history. No customer data is included.

## Severity Definitions

| Severity | Definition | Response target |
|---|---|---|
| **1 — Critical** | Complete loss of access to data or production outage | 15-minute initial response (24×7) |
| **2 — High** | Significant degradation — redundancy lost, DR at risk | 1-hour initial response (24×7) |
| **3 — Medium** | Non-critical degradation, workaround available | 4-hour business hours |
| **4 — Low** | Information request, general question | Next business day |

Always call for Severity 1 — do not rely on portal-only submission for critical issues.

## Evergreen Support — What's Covered

| Included | Not included |
|---|---|
| Drive replacement (any failure) | Data recovery from user-initiated deletions |
| Controller replacement | Professional services for design changes |
| Non-disruptive Purity upgrades | Connectivity troubleshooting beyond the array |
| Capacity expansion credits | Third-party integration issues |
| Pure1 cloud monitoring | |

## Proactive Support Features

### CloudIQ / AI-Assisted Analysis

Pure1 includes anomaly detection that flags performance deviations before they become incidents. Review the **Analytics → Wellness** view weekly.

### Upgrade Recommendations

Pure1 → **Arrays → select array → Settings → Software** shows available Purity upgrades with release notes. Pure Support proactively recommends upgrades when critical fixes apply.

### Log Forwarding to Pure

```bash
# Enable automatic log collection (supports proactive case creation)
puresupport set --log-forwarding enabled
puresupport list | grep log_forwarding
```

## Escalation Path

```text
L1 Support Case (portal / phone)
  ↓ if unresolved after agreed time
L2 Senior Support Engineer (request via case notes)
  ↓ if design or architecture question
Solutions Architect / Systems Engineer (account team)
  ↓ if software defect confirmed
Engineering (TAC escalation — handled by Pure internally)
```

## Common Support Scenarios

| Scenario | Action |
|---|---|
| Drive failed | Pure1 auto-detects; auto-ships replacement (Evergreen). Confirm shipping address in Pure1 → Profile |
| Controller fault | Open Sev 1 by phone immediately |
| Unexpected performance degradation | Collect `puresupport create` bundle; open Sev 2 case |
| Purity upgrade failed / stuck | Open Sev 1 — do not power off array |
| Need to extend snapshot retention | Adjust snapshot policy in array UI; no case needed |
| Volume restore from snapshot | Perform self-service via CLI/UI; open case only if data appears missing |
