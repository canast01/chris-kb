# Maintenance Window Planning

## Overview

Good maintenance windows are won in the planning phase. The execution itself is often the easy part when planning has been thorough — the runbook is clear, dependencies are mapped, risks are understood, and stakeholders are prepared. This page covers the planning checklist and key decisions that must be made before a window is scheduled.

---

## Planning Checklist

Start planning at least 10 business days before the target window for Major changes, and at least 5 for Normal changes.

- [ ] Define the scope: what specific work will be done?
- [ ] Identify all affected services and CIs (use CMDB relationships)
- [ ] Identify all dependencies: upstream and downstream services
- [ ] Write or review the implementation plan (step-by-step)
- [ ] Write or review the backout plan (step-by-step, with decision triggers)
- [ ] Identify required team members and confirm their availability
- [ ] Identify required vendor support and pre-engage if needed
- [ ] Select the maintenance window time (see scheduling guidance below)
- [ ] Confirm no conflict with business freeze periods or other changes
- [ ] Draft the stakeholder communication (advance notice)
- [ ] Submit change request and obtain approval before sending comms

---

## Window Scheduling Guidance

| Consideration           | Guidance                                                      |
|-------------------------|---------------------------------------------------------------|
| Day of week             | Avoid Monday (post-weekend issues) and Friday (no week buffer)|
| Time of day             | Use lowest-traffic period for the service (check analytics)   |
| Duration                | Add 30–50% buffer to estimated task time                      |
| Rollback time           | Rollback must fit within the window; if not, extend the window|
| Business events         | Avoid month-end, quarter-end, product launches, peak seasons  |
| Downstream dependencies | Check if dependencies have their own freeze or change windows |

Schedule the rollback decision deadline explicitly — not just the window end time.

---

## Dependency Mapping

Map dependencies before finalising scope. A change to one service can cascade.

- [ ] List all services that the target system depends on (upstream)
- [ ] List all services that depend on the target system (downstream)
- [ ] Confirm each dependency owner is aware of the maintenance window
- [ ] Identify whether any dependency needs its own maintenance window first
- [ ] Check for any shared infrastructure (load balancers, databases, auth services)

Use the CMDB CI relationship view to generate the dependency list. Supplement with application architecture diagrams for complex services.

---

## Risk Review

| Risk Category          | Questions to Ask                                             |
|------------------------|--------------------------------------------------------------|
| Technical risk         | What is the most likely failure mode? Is it recoverable?     |
| Time risk              | What if the main task takes 2x as long as estimated?         |
| Dependency risk        | What if an upstream service degrades during the window?      |
| Data risk              | Is any data transformation or migration involved?            |
| People risk            | What if the lead engineer is unavailable 30 min in?          |
| Vendor risk            | Is any vendor support required? Is it confirmed?             |

Rate overall risk (Low/Medium/High/Critical) and document it in the change request.

---

## Pre-Window Communication Schedule

Agree on the communication schedule as part of planning — not the morning of the window.

- [ ] Advance notice date and recipient list agreed
- [ ] 48-hour reminder date and recipient list agreed
- [ ] Day-of confirmation message owner assigned
- [ ] Bridge/war room link created (for Medium risk and above)
- [ ] Escalation contacts confirmed and added to the bridge invite
- [ ] Status page event created with correct maintenance window times
