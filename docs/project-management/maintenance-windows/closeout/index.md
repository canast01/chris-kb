# Maintenance Window Closeout


<div class="kb-summary">
Maintenance Window Closeout reference covering Overview, Closeout Sequence, Closeout Checklist, Deferred Task Handling, Debrief and Lessons Learned and 1 more sections.
</div>

## Overview

Closeout formally ends the maintenance window, ensures all tasks are accounted for, and hands the environment back to normal operations. A rushed or skipped closeout leaves ambiguity about what was completed, creates gaps in the audit trail, and can leave monitoring in a suppressed state.

---

## Closeout Sequence

Follow this order after the last task in the implementation plan is complete.

| Step | Action                                           | Owner            |
|------|--------------------------------------------------|------------------|
| 1    | Run post-maintenance validation checks           | Lead Engineer    |
| 2    | Confirm all planned tasks completed or deferred  | Lead Engineer    |
| 3    | Re-enable any suppressed monitoring alerts       | Lead Engineer    |
| 4    | Notify stakeholders that maintenance is complete | Comms lead       |
| 5    | Update the maintenance window ticket             | Lead Engineer    |
| 6    | Update CMDB for any CI changes made              | Asset Manager    |
| 7    | Release the maintenance bridge / war room        | Incident Cmdr    |
| 8    ] Schedule debrief if required               | Change Manager   |

Do not suppress monitoring alerts beyond the agreed maintenance window. Re-enable alerts as the first act of closeout, before validation is complete, so that real issues are caught.

---

## Closeout Checklist

- [ ] All implementation plan steps marked complete or deferred (with reason)
- [ ] Post-maintenance health check passed for all affected services
- [ ] Monitoring alerts re-enabled (confirm in alerting tool, not just by assumption)
- [ ] Maintenance window status page / notification updated to "Complete"
- [ ] Stakeholder close-out notification sent
- [ ] Deferred tasks ticketed and assigned with due dates
- [ ] Any issues encountered documented in the ticket notes
- [ ] CMDB updated for all CI changes made during the window
- [ ] Maintenance ticket closed with actual start and end time recorded

---

## Deferred Task Handling

Not all tasks planned for a window will complete. Handle deferrals explicitly.

| Scenario                         | Action                                           |
|----------------------------------|--------------------------------------------------|
| Task ran out of time             | Ticket the remaining work; schedule next window  |
| Task blocked by unexpected issue | Ticket the blocker; notify relevant owner        |
| Task found to be unnecessary     | Document why; close the task with explanation    |
| Task partially complete          | Document completed portion; ticket remainder     |

A task is not "done" until it is either fully completed and validated, or explicitly deferred with a follow-up ticket.

---

## Debrief and Lessons Learned

A brief debrief is recommended after every Major maintenance window and mandatory after any window that encountered significant issues.

Debrief agenda (30 minutes maximum):

1. Did the window run to plan? What deviated?
2. Were there any surprises — technical or logistical?
3. What went well that we should repeat?
4. What would we change for next time?
5. Are there any follow-up actions not already ticketed?

Debrief notes are stored in the maintenance ticket and shared with the change management team.

---

## Monitoring Reinstatement

| Alert Type              | When to Re-enable          | Confirmed By         |
|-------------------------|----------------------------|----------------------|
| Service availability    | Immediately after closeout | Monitoring dashboard |
| Performance thresholds  | After baseline stabilises  | Lead engineer        |
| Capacity alerts         | Immediately after closeout | Monitoring dashboard |
| Custom change-related   | After observation period   | Change owner         |
