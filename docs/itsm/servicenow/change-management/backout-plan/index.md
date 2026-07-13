---
tags:
  - servicenow
description: "Backout Plan reference covering Overview, Backout Criteria, Backout Steps Template, Backout Checklist, Validation After Backout and 1 more sections."
---
# Backout Plan

<div class="kb-summary">
Backout Plan reference covering Overview, Backout Criteria, Backout Steps Template, Backout Checklist, Validation After Backout and 1 more sections.

*Applies to: ServiceNow*
</div>

```d2
direction: down

backout_criteria: "Backout Criteria" {shape: rectangle}
backout_steps_template: "Backout Steps Template" {shape: rectangle}
backout_checklist: "Backout Checklist" {shape: rectangle}
validation_after_backout: "Validation After Backout" {shape: rectangle}
postbackout_communication: "Post-Backout Communication" {shape: rectangle}

backout_criteria -> backout_steps_template: uses
backout_steps_template -> backout_checklist: uses
backout_checklist -> validation_after_backout: uses
validation_after_backout -> postbackout_communication: uses
```

## Overview

A backout plan defines exactly how to reverse a change if it fails or causes unintended impact. Every change with a risk score above 2 must have a documented backout plan approved before implementation begins. A vague "restore from backup" is not an acceptable backout plan — it must be specific, tested, and actionable in the heat of an incident.

---

## Backout Criteria

Define trigger conditions clearly before the change window opens. The team should not need to debate whether to back out — the criteria decide it.

| Trigger Condition                              | Recommended Action       |
|------------------------------------------------|--------------------------|
| Service fails to come back online within X min | Initiate backout         |
| Error rate exceeds pre-defined threshold       | Initiate backout         |
| Monitoring alerts fire within rollback window  | Assess; likely backout   |
| Dependency service reports degradation         | Assess; notify and pause |
| Go/no-go check fails during implementation     | Stop and backout         |

Set the rollback decision deadline before starting — for example, "if service is not healthy by 02:30, we backout." Do not extend deadlines mid-window without explicit approval.

---

## Backout Steps Template

Document backout steps as a numbered, executable list. Example structure:

1. Stop the deployment or configuration process
2. Revert configuration files from backup taken at step X of the implementation plan
3. Restart affected services in dependency order
4. Validate service health (checks listed in the Validation section)
5. Notify the change bridge / incident bridge of backout status
6. Open an incident ticket if service has not recovered within 15 minutes of backout completion

Each step should include the exact command or GUI action, the expected output, and what to do if the output is not as expected.

---

## Backout Checklist

- [ ] Backout plan written and reviewed by a peer before the change window
- [ ] Snapshot, backup, or config export taken immediately before implementation
- [ ] Rollback decision deadline agreed and documented
- [ ] All team members on the change bridge aware of backout criteria
- [ ] Backout has been tested in a non-production environment where possible
- [ ] Backout duration estimated (does it fit within the change window?)
- [ ] Customer / stakeholder communication drafted for backout scenario

---

## Validation After Backout

After executing a backout, confirm the environment has returned to baseline state.

| Check                            | Expected Result                      |
|----------------------------------|--------------------------------------|
| Service health endpoint          | HTTP 200 / healthy status            |
| Application logs                 | No new errors introduced by change   |
| Monitoring dashboards            | Metrics back to pre-change baseline  |
| Downstream services              | No reported impact or degradation    |
| CMDB / config records            | Reflect pre-change state             |

Document backout completion time and validation results in the change ticket.

---

## Post-Backout Communication

Once backout is confirmed complete and the environment is stable:

- Update the incident or change ticket with backout timestamp and outcome
- Notify all stakeholders on the change distribution list
- Keep the change status as `Backed Out` — do not mark it as `Successful`
- Schedule a post-implementation review (PIR) within 5 business days
- Identify root cause of backout trigger before rescheduling the change
