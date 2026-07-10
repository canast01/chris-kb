---
tags:
  - azure
  - certifications
---
# Azure Exam Tracking

<div class="kb-summary">
Azure Exam Tracking reference covering Certification Path Overview, Exam Structure — AZ-900 (Fundamentals), Exam Structure — AZ-104 (Administrator), Exam Structure — AZ-305 (Architect), Scheduling and Retake Policy and 2 more sections.
</div>

```d2
direction: down

certification_path_overview: "Certification Path Overview" {shape: rectangle}
exam_structure_az900_fundamentals: "Exam Structure — AZ-900 (Fundamentals)" {shape: rectangle}
exam_structure_az104_administrator: "Exam Structure — AZ-104 (Administrator)" {shape: rectangle}
exam_structure_az305_architect: "Exam Structure — AZ-305 (Architect)" {shape: rectangle}
scheduling_and_retake_policy: "Scheduling and Retake Policy" {shape: rectangle}
attempt_log: "Attempt Log" {shape: rectangle}

certification_path_overview -> exam_structure_az900_fundamentals: uses
exam_structure_az900_fundamentals -> exam_structure_az104_administrator: uses
exam_structure_az104_administrator -> exam_structure_az305_architect: uses
exam_structure_az305_architect -> scheduling_and_retake_policy: uses
scheduling_and_retake_policy -> attempt_log: uses
```

## Certification Path Overview

| Exam | Code | Level | Fee (USD) | Duration | Questions |
|---|---|---|---|---|---|
| Azure Fundamentals | AZ-900 | Foundational | $165 | 85 min | 40–60 |
| Azure Administrator | AZ-104 | Associate | $165 | 100 min | 40–60 |
| Azure Solutions Architect Expert | AZ-305 | Expert | $165 | 100 min | 40–60 |
| Azure AI Engineer Associate | AI-102 | Associate | $165 | 100 min | 40–60 |
| Azure Security Engineer | AZ-500 | Associate | $165 | 100 min | 40–60 |
| Azure DevOps Engineer Expert | AZ-400 | Expert | $165 | 150 min | 40–60 |

## Exam Structure — AZ-900 (Fundamentals)

| Domain | Weight |
|---|---|
| Cloud concepts | 25–30% |
| Azure architecture and services | 35–40% |
| Azure management and governance | 30–35% |

## Exam Structure — AZ-104 (Administrator)

| Domain | Weight |
|---|---|
| Manage Azure identities and governance | 20–25% |
| Implement and manage storage | 15–20% |
| Deploy and manage Azure compute resources | 20–25% |
| Implement and manage virtual networking | 15–20% |
| Monitor and maintain Azure resources | 10–15% |

## Exam Structure — AZ-305 (Architect)

| Domain | Weight |
|---|---|
| Design identity, governance, and monitoring solutions | 25–30% |
| Design data storage solutions | 20–25% |
| Design business continuity solutions | 15–20% |
| Design infrastructure solutions | 30–35% |

## Scheduling and Retake Policy

- Schedule via Pearson VUE or Microsoft Certification Dashboard (learn.microsoft.com/certifications)
- Cancel/reschedule with no penalty if >24 hours before exam
- Retake policy: wait 24 hours after first failure; 14 days after second; 14 days after third; max 5 attempts per year
- Certifications valid for 1 year; renew via free online assessment on Microsoft Learn (no exam fee)
- Annual renewal assessment: opens 6 months before expiry; can be taken multiple times

## Attempt Log

| Date | Exam Code | Score | Result | Notes |
|---|---|---|---|---|
| — | — | — | — | Add attempts here |

## Study Checklist

- [ ] Register target exam and note expiry on calendar
- [ ] Download official Microsoft study guide PDF for the exam code
- [ ] Run diagnostic using Microsoft Learn assessment
- [ ] Track domain-level scores on each practice attempt
- [ ] Schedule renewal reminder 6 months after passing
