---
tags:
  - reference
---
# Virtualization — Practice Notes

<div class="kb-summary">
VMware certification practice exam notes — question patterns, topic areas, and worked examples from VCP-DCV and VCAP study sessions.
</div>

```text
┌────────────────────────────────── Practice Exam Approach — VCP-DCV ───────────────────────────────────┐
│                                                                                                       │
│   Scenario questions test "why X not Y?" — identify the principle then apply elimination              │
│   Most wrong answers are valid in a different context; read the full scenario carefully               │
│   High-yield areas: PVLAN types, HA admission control, vLCM image vs baseline, vSAN FTT               │
│                                                                                                       │
│   Question types                                                                                      │
│   Single-answer: most common format; one correct answer from 4–6 choices                              │
│   Multiple-answer: explicitly states how many to select (e.g. "choose two"); all must be correct      │
│   Scenario (long stem): background paragraph followed by the question; read all before answering      │
│   Drag and order: rare; sequence steps or match items; trust the most logical operational order       │
│                                                                                                       │
│   Elimination strategy                                                                                │
│   Step 1: remove answers that belong to the wrong product, feature, or scope                          │
│   Step 2: remove answers that reverse cause and effect                                                │
│   Step 3: of the remaining two, pick the answer that names the specific mechanism asked about         │
│   Never leave blank — flag uncertain questions and return; an educated guess beats no answer          │
│                                                                                                       │
│   Timing: 135 min / 70 questions = ~2 min per question; reserve 10 min for flagged review             │
│   Pass threshold: 300 of 500 (scaled score; approximately 65–70% correct answers required)            │
│                                                                                                       │
│   Key terms:                                                                                          │
│   %RDY    = CPU Ready; >5–10 ms per 20-second interval indicates CPU contention on the host           │
│   NIOC    = Network I/O Control; bandwidth shares and limits per traffic type on VDS uplinks          │
│   PVLAN   = Private VLAN; Isolated/Community/Promiscuous; communication rules tested heavily          │
│   FTT     = Failures to Tolerate; vSAN storage policy; FTT=1 requires minimum 3 hosts                 │
│   vCLS    = vSphere Cluster Services; retreat mode disables DRS automation and HA placement           │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
