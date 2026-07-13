---
tags:
  - servicenow
description: "Maintenance Window Execution reference covering Overview, Go / No-Go at Window Open, Execution Checklist, Step-by-Step Discipline, Time Management During..."
---
# Maintenance Window Execution

<div class="kb-summary">
Maintenance Window Execution reference covering Overview, Go / No-Go at Window Open, Execution Checklist, Step-by-Step Discipline, Time Management During Execution and 1 more sections.

*Applies to: ServiceNow*
</div>

```d2
direction: down

go_nogo_at_window_open: "Go / No-Go at Window Open" {shape: rectangle}
execution_checklist: "Execution Checklist" {shape: rectangle}
stepbystep_discipline: "Step-by-Step Discipline" {shape: rectangle}
time_management_during_execution: "Time Management During Execution" {shape: rectangle}
handling_unexpected_issues_during_ex: "Handling Unexpected Issues During Execution" {shape: rectangle}

go_nogo_at_window_open -> execution_checklist: uses
execution_checklist -> stepbystep_discipline: uses
stepbystep_discipline -> time_management_during_execution: uses
time_management_during_execution -> handling_unexpected_issues_during_ex: uses
```

## Overview

Execution is where the planned work happens. The discipline during this phase — following the runbook, checking off steps, calling go/no-go at the right moments — determines whether the window succeeds. Improvisation during execution is a leading cause of extended windows and unplanned outages.

---

## Go / No-Go at Window Open

Before the first task starts, run a final go/no-go check on the bridge.

| Condition                                          | Decision       |
|----------------------------------------------------|----------------|
| All pre-checks passed earlier in the day           | Go             |
| All required team members confirmed on bridge      | Go             |
| No active incidents on affected services           | Go             |
| Monitoring alert firing on affected service        | No-Go          |
| Required access or credentials unavailable         | No-Go          |
| Team member missing with no confirmed backup       | No-Go          |

A no-go must be declared within the first 5 minutes of the window. After that, proceeding with a delay requires documented justification.

---

## Execution Checklist

- [ ] Change window confirmed open; start time recorded in ticket
- [ ] Go/no-go passed and confirmed on the bridge
- [ ] Pre-change baseline snapshot taken (if not done in pre-checks)
- [ ] Step 1 of implementation plan started; time noted
- [ ] Each step signed off before proceeding to the next
- [ ] Progress updates posted to Slack/stakeholders per communications plan
- [ ] Any deviations from the implementation plan noted in the ticket immediately
- [ ] Rollback decision deadline monitored (alarm set if helpful)
- [ ] Validation checks run after each major step, not only at the end

---

## Step-by-Step Discipline

Each step in the implementation plan should follow this pattern:

1. Read the step aloud or confirm it with the second engineer
2. Execute the action
3. Verify the expected output
4. Record completion in the ticket (step number + timestamp)
5. Confirm no unexpected side effects before moving to the next step

If the expected output differs from actual output: **stop, assess, do not proceed** to the next step until the discrepancy is understood.

---

## Time Management During Execution

| Checkpoint                              | Action                                       |
|-----------------------------------------|----------------------------------------------|
| 25% of window elapsed                   | Confirm task progress is on track            |
| 50% of window elapsed                   | If behind schedule, assess remaining scope   |
| 75% of window elapsed                   | Decision point: complete, defer, or extend   |
| Rollback deadline reached               | Initiate backout if success not confirmed    |
| Window end time approached              | Notify stakeholders; request extension or end|

Never silently extend the window. Any extension beyond the approved time must be communicated to stakeholders and recorded.

---

## Handling Unexpected Issues During Execution

When something unexpected occurs:

- [ ] Stop the current step; do not continue blindly
- [ ] Assess whether the unexpected issue is within the rollback decision criteria
- [ ] Escalate to the bridge host if it may affect the window outcome
- [ ] Document what was found in the ticket notes with a timestamp
- [ ] Decide: resolve and continue, defer the affected task, or initiate backout
- [ ] Communicate the status to stakeholders immediately

Do not attempt to fix an unexpected issue silently and then continue — transparency on the bridge protects everyone.
