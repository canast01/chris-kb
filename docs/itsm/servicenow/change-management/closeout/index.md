---
tags:
  - servicenow
description: "Change Closeout reference covering Overview, Closeout Checklist, Change Outcome Classification, PIR (Post-Implementation Review), Lessons Learned and 1..."
---
# Change Closeout

<div class="kb-summary">
Change Closeout reference covering Overview, Closeout Checklist, Change Outcome Classification, PIR (Post-Implementation Review), Lessons Learned and 1 more sections.

*Applies to: ServiceNow*
</div>

```d2
direction: down

closeout_checklist: "Closeout Checklist" {shape: rectangle}
change_outcome_classification: "Change Outcome Classification" {shape: rectangle}
pir_postimplementation_review: "PIR (Post-Implementation Review)" {shape: rectangle}
lessons_learned: "Lessons Learned" {shape: rectangle}
cmdb_update_on_closeout: "CMDB Update on Closeout" {shape: rectangle}

closeout_checklist -> change_outcome_classification: uses
change_outcome_classification -> pir_postimplementation_review: uses
pir_postimplementation_review -> lessons_learned: uses
lessons_learned -> cmdb_update_on_closeout: uses
```

## Overview

Change closeout is the final phase of the change lifecycle. It ensures that the change is formally concluded, documentation is complete, CMDB records are updated, and any lessons learned are captured. Skipping closeout leaves the change process incomplete and can mask problems that should inform future changes.

---

## Closeout Checklist

Complete all items before setting change status to `Closed`.

- [ ] Implementation confirmed complete (or backout confirmed complete)
- [ ] Post-change validation passed and signed off
- [ ] All change window tasks ticked off in the implementation plan
- [ ] Monitoring confirmed stable for the agreed observation period
- [ ] All team members released from the change bridge
- [ ] Incident tickets raised during the change window linked to the change record
- [ ] Change ticket updated with actual start time, end time, and outcome
- [ ] CMDB updated to reflect any CI modifications made during the change
- [ ] PIR scheduled if change was Major, Emergency, or resulted in a backout

---

## Change Outcome Classification

| Outcome               | Description                                             |
|-----------------------|---------------------------------------------------------|
| Successful            | Implemented as planned; no issues; validation passed    |
| Successful with issues| Implemented but minor issues encountered and resolved   |
| Backed out            | Change reversed due to failure or trigger condition met |
| Partially implemented | Some tasks completed; remainder deferred                |
| Cancelled             | Change not started within the approved window           |

Set the outcome field on the ticket accurately. `Successful with issues` changes should have the issues described in the notes field.

---

## PIR (Post-Implementation Review)

A PIR is required for:

- All Major changes
- All Emergency changes
- Any change that was backed out
- Any change where unintended impact occurred

PIR agenda items:

1. What was the change, and did it achieve its objective?
2. What went well?
3. What went wrong or was unexpected?
4. What would we do differently next time?
5. Are there any follow-up actions required?

PIR output is stored in the change ticket and shared with the CAB at the next meeting.

---

## Lessons Learned

Lessons from PIRs feed back into process improvement. Track recurring themes:

| Theme                         | Frequency | Action Taken                          |
|-------------------------------|-----------|---------------------------------------|
| Backout plan inadequate       | (count)   | Update backout plan template          |
| Change window underestimated  | (count)   | Revise estimation guidance            |
| Missing dependency identified | (count)   | Improve pre-change dependency check   |
| Insufficient testing          | (count)   | Strengthen test plan requirements     |

Review lessons learned quarterly with the change management team. Update process documentation and templates as needed.

---

## CMDB Update on Closeout

Every closed change must leave the CMDB in an accurate state.

- [ ] New CIs created during the change added to CMDB
- [ ] Modified CIs updated (IP, OS version, config baseline)
- [ ] Decommissioned CIs marked as Retired
- [ ] CI relationships updated if dependencies changed
- [ ] Change ticket linked to all affected CIs in CMDB
