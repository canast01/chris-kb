---
tags:
  - servicenow
---
# ServiceNow — Incident Templates

<div class="kb-summary">
Incident record templates for common failure types — P1 outage, service degradation, security incident, and infrastructure failure templates.
</div>

```text
┌─────────────────────────────────── ServiceNow — Incident Templates ───────────────────────────────────┐
│                                                                                                       │
│   Four templates: P1 outage, service degradation (P2), security incident, infrastructure failure      │
│   Templates pre-populate: priority, impact, urgency, assignment group, category, and subcategory      │
│   Security incident template pre-populates evidence-preservation steps as initial work notes          │
│   Infra failure template links to CMDB CI; affected services auto-populated via service map           │
│                                                                                                       │
│   P1 outage template                                                                                  │
│   Priority = 1; Impact = 1 (org-wide); Urgency = 1; SLA = 1h response, 4h resolution                  │
│   Assignment: Major Incident team + Service Owner notified automatically                              │
│   Bridge line: major incident bridge details pre-populated in description field                       │
│   Communications: status page update triggered; stakeholder notification every 30 min                 │
│                                                                                                       │
│   Security incident template                                                                          │
│   Category = Security; assignment → SecOps queue automatically                                        │
│   Pre-populated work notes: isolate host, preserve memory/logs, do not reboot before analysis         │
│   Escalation field: links to CISO and Legal for data breach notification decision                     │
│                                                                                                       │
│   Infrastructure failure template                                                                     │
│   CI field mandatory; auto-populated affected services from CMDB service map                          │
│   Category = Infrastructure; assignment routes to infrastructure on-call team                         │
│   Checklist fields: redundancy status, failover tested, monitoring silenced (Y/N)                     │
│                                                                                                       │
│   Key terms:                                                                                          │
│   Major Incident team = dedicated team activated for P1/P2 outages with bridge call coordination      │
│   service map   = CMDB dependency graph; shows downstream services affected by a CI failure           │
│   SLA           = Service Level Agreement; defines response and resolution time targets by priority   │
│   work note     = internal-only note on an incident record; not visible to the caller                 │
│   bridge line   = conference call line pre-established for major incident coordination                │
│   SecOps        = Security Operations team; owns all security incident classification and response    │
│   CISO          = Chief Information Security Officer; notified for all confirmed data breach events   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
