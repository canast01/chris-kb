---
tags:
  - operations
  - servicenow
---
# ServiceNow — Operations



<div class="kb-summary">
ServiceNow day-to-day operations — incident routing, CMDB hygiene, report scheduling, upgrade health checks, and platform monitoring.

*Applies to: ServiceNow (Washington / Xanadu)*
</div>

```text
┌────────────────────────────────── ServiceNow — Operations Overview ───────────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Daily Checks        │  │         Weekly Tasks        │  │        Monthly Tasks        │   │
│   │      MID Server status      │  │        SLA compliance       │  │       Instance health       │   │
│   │       Incident backlog      │  │          User audit         │  │        CMDB accuracy        │   │
│   │      Failed jobs check      │  │      Flow error review      │  │      Update Set review      │   │
│   │         Alert triage        │  │       CMDB drift check      │  │       Security review       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ServiceNow SaaS cloud · MID Server VMs on-prem · monitoring for MID health                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  MID Server status = check via Admin > MID Servers; state should be Up                                │
│  Incident backlog = open incidents exceeding SLA; review daily for P1/P2                              │
│  Failed jobs = System > Scheduled Jobs; check for last-run errors                                     │
│  SLA compliance = reports showing on-time resolution vs SLA targets                                   │
│  Flow error = Flow Designer > Executions; check failed flow instances                                 │
│  CMDB drift = CIs that were discovered but not matched; orphan records                                │
│  CMDB accuracy = percentage of CIs with complete and correct attribute data                           │
│  Update Set review = monthly review of pending Update Sets across instances                           │
│  Instance health = ServiceNow HI (Hi.service-now.com) for instance stats                              │
│  User audit = review inactive users and over-privileged role assignments                              │
│  Security review = monthly review of ACLs and admin role membership                                   │
│  Alert triage = ServiceNow ITOM events; confirm actionable vs noise                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>REST API commands and CLI tooling.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Instance health monitoring and validation.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Incidents, changes, requests, and work notes.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install & Upgrade</strong>
  <span>Installation and upgrade procedures.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup & Restore</strong>
  <span>Backup strategies and restore procedures.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts and utilities.</span>
</a>

</div>
