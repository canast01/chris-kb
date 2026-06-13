---
tags:
  - aria-automation
  - troubleshooting
  - vmware
---
# Aria Automation — Troubleshooting

<div class="kb-summary">
Diagnosing Aria Automation deployment failures, vRO workflow errors, integration issues, and catalog problems.

*Applies to: Aria Automation 8.x*
</div>

```text
┌────────────────────────────────── Aria Automation — Troubleshooting ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Blueprint deploy failures; ABX action errors; cloud account connectivity issues        │   │
│   │           Catalog item errors; pipeline failures; API debug for root cause analysis           │   │
│   │      Event broker subscription troubleshooting; lease expiry and approval stuck scenarios     │   │
│   │       Diagnostics: vRA API debug, ABX function logs, vRO log files, request detail view       │   │
│   │     Escalation: vRA log bundle export; GSS case; TAM for P1; support compatibility matrix     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues define the triage path · diagnostics isolate root cause                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │        Blueprint fail       │  │        vRA API debug        │  │        vRA log bundle       │   │
│   │        ABX action err       │  │       ABX function log      │  │        GSS case open        │   │
│   │       Cloud acct conn       │  │        vRO log files        │  │        ABX debug mode       │   │
│   │       Catalog item err      │  │       Request details       │  │          API trace          │   │
│   │         Lease expiry        │  │       Event broker log      │  │        Support matrix       │   │
│   │        Approval stuck       │  │       ABX FaaS console      │  │          Log export         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics use API and logs · escalation bundles evidence for GSS    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │  Blueprint fail  │  vRA API debug   │    /var/log/vra   │  vRA log bundle  │    Re-deploy     │   │
│   │    ABX error     │  ABX func logs   │    /var/log/abx   │   GSS P1 case    │   Fix + retry    │   │
│   │  Cloud acct err  │     vRO logs     │    /var/log/vro   │   TAM escalate   │   Re-auth acct   │   │
│   │  Approval stuck  │   Event broker   │   /var/log/event  │  Support matrix  │  Clear + retry   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VM (Automation appliance) · RAM DIMMs · Network NICs · Cloud provider APIs                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Blueprint deployment = End-to-end request from Service Broker through Assembler to cloud provider    │
│  ABX action    = FaaS function failure; check ABX console logs and timeout configuration              │
│  Cloud account = vCenter/AWS/Azure connection; re-validate credentials and proxy connectivity         │
│  Catalog item  = Service Broker published item; errors traced via request detail and event log        │
│  Approval policy = Stuck approval due to missing approver; check policy config and user assignment    │
│  Event broker  = Aria Automation event bus; subscription failures visible in event broker log         │
│  Subscription  = Event-to-action mapping; failed subscriptions appear in event broker error log       │
│  Lease expiry  = Deployment TTL reached; check reclaim notification config and project lease policy   │
│  vRO (Orchestrator) = Embedded workflow engine; logs at /var/log/vro for workflow execution debug     │
│  API debug     = Aria REST API with ?debug=true parameter; returns detailed provisioning trace        │
│  Request lifecycle = Created → Pending Approval → In Progress → Successful/Failed states              │
│  Pipeline stage = Aria Automation Pipelines stage failure; review stage log for task error detail     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Frequently seen problems and resolution steps.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Log locations, diagnostic commands, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>When and how to escalate to VMware support.</span>
</a>

</div>
