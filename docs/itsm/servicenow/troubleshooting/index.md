---
tags:
  - servicenow
  - troubleshooting
---
# ServiceNow — Troubleshooting



<div class="kb-summary">
Diagnosing ServiceNow outages, workflow errors, integration failures, MID server connectivity, and slow performance.

*Applies to: ServiceNow (Washington / Xanadu)*
</div>

```text
┌───────────────────────────────────── ServiceNow Troubleshooting ──────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐                                                    │
│   │              Performance Issues              │                                                    │
│   │        Slow form load → check scripts        │                                                    │
│   │        Long queries → DB index review        │                                                    │
│   │         High memory → scheduled jobs         │                                                    │
│   │         Stats.do for instance health         │                                                    │
│   └──────────────────────────────────────────────┘                                                    │
│                                                     ┌─────────────────────────────────────────────┐   │
│                                                     │              Integration Issues             │   │
│                                                     │            REST: check ECC queue            │   │
│                                                     │         MID server: connection test         │   │
│                                                     │         LDAP: test connection in UI         │   │
│                                                     │          Email: smtp_test.do check          │   │
│                                                     └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐                                                    │
│   │             User / Login Issues              │                                                    │
│   │            SSO failure → IdP logs            │                                                    │
│   │         Account locked → admin reset         │                                                    │
│   │          Missing role → group check          │                                                    │
│   │           Impersonate to reproduce           │                                                    │
│   └──────────────────────────────────────────────┘                                                    │
│                                                     ┌─────────────────────────────────────────────┐   │
│                                                     │          Workflow / Approval Issues         │   │
│                                                     │             Workflow context log            │   │
│                                                     │          Stuck approvals → reassign         │   │
│                                                     │        SLA breach → calculation check       │   │
│                                                     │        Escalations → schedule review        │   │
│                                                     └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ServiceNow SaaS nodes · MID server VMs on-prem · LDAP/IdP infrastructure                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  stats.do   = ServiceNow diagnostic URL; shows node stats, memory, active threads                     │
│  ECC Queue  = External Communication Channel queue; REST/SOAP message log                             │
│  MID Server = Management Instrumentation Discovery server; on-prem relay agent                        │
│  Impersonate= view instance as another user; useful for reproducing access issues                     │
│  Workflow context= runtime log of workflow execution; shows current activity state                    │
│  SLA        = Service Level Agreement; time-based target tracked per ticket                           │
│  smtp_test.do= diagnostic page to test outbound email configuration                                   │
│  DB index   = database index on table column; missing index causes full table scan                    │
│  Scheduled Job= background task; overloaded jobs cause memory/CPU spikes                              │
│  LDAP test  = connection test in System LDAP; validates bind credentials + query                      │
│  IdP logs   = identity provider audit log; shows SAML assertion errors                                │
│  Script debug= set sys_log level in scripts to trace execution path                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Frequently encountered problems and fixes.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Diagnostic commands and log analysis.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>Escalation paths and vendor support procedures.</span>
</a>

</div>

