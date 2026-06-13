---
tags:
  - reference
---
# Virtualization — Weak Areas

<div class="kb-summary">
Certification weak areas log — topics that scored below threshold in practice exams, with targeted study notes and reference links.

*Applies to: vSphere 7.x / 8.x*
</div>

```text
┌─────────────────────────────── Certification Weak-Area Analysis Cycle ────────────────────────────────┐
│                                                                                                       │
│   After each practice exam: flag incorrect answers and note the correct principle                     │
│   Group flags by exam section; ≥2 misses in a section on a single run = weak area                     │
│   Re-test the weak area in isolation before returning to full mixed practice runs                     │
│                                                                                                       │
│   Common weak areas — VCP-DCV 8                                                                       │
│   PVLAN types: which port types can communicate with which (Isolated/Community/Promiscuous)           │
│   HA admission control modes: percentage vs slot-based vs dedicated failover hosts                    │
│   vLCM image vs baseline: mutual exclusivity per cluster; one-way migration                           │
│   vSAN FTT rules: FTT=1 needs ≥3 hosts; FTT=2 needs ≥5 hosts; RAID-5 needs ≥4 hosts                   │
│   Memory reclamation order: TPS → balloon driver → memory compression → swap                          │
│   vCLS retreat mode: DRS goes manual; HA Optimal Placement off; HA restarts still work                │
│                                                                                                       │
│   Study action cycle                                                                                  │
│   Step 1: Read the relevant official exam guide section for the weak topic                            │
│   Step 2: Work through a lab example or draw the concept on paper                                     │
│   Step 3: Write a one-paragraph summary in your own words (teach-back method)                         │
│   Step 4: Attempt 5 targeted practice questions on the specific sub-topic only                        │
│   Step 5: Return to full mixed practice exams when sub-topic score reaches ≥80%                       │
│                                                                                                       │
│   Success criteria: score ≥80% on 3 consecutive isolated sub-topic runs before moving on              │
│                                                                                                       │
│   Key terms:                                                                                          │
│   Weak area  = sub-topic with a consistent miss rate across two or more separate practice runs        │
│   Isolation  = practice only the weak sub-topic questions, not mixed full exams                       │
│   Threshold  = target for moving on: ≥75% overall mixed, ≥80% isolated sub-topic                      │
│   Blueprint  = official exam objective guide; section weights drive how many questions appear         │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
