# Incident Handling — Operations

<div class="kb-summary">
Incident handling operational procedures: incident classification, triage workflows, evidence collection, escalation, and post-incident review.
</div>

```text
┌─────────────────────────────────── Incident Handling — Operations ────────────────────────────────────┐
│                                                                                                       │
│   Lifecycle: detect → classify → triage → contain → investigate → recover → post-incident review      │
│   Severity tiers: P1 (critical / active breach) → P2 (high / significant risk) → P3/P4 (lower)        │
│   Evidence preservation: isolate before wiping; memory dump before reboot; chain of custody log       │
│   Post-incident review within 5 business days; lessons learned fed back to detection rules            │
│                                                                                                       │
│   Classification criteria                                                                             │
│   P1  Active data exfiltration, ransomware, full system compromise, regulatory notification trigger   │
│   P2  Suspected compromise, privileged account misuse, lateral movement detected                      │
│   P3  Policy violation, isolated malware, failed attack with no confirmed compromise                  │
│   P4  False positive confirmed; no further action beyond documentation                                │
│                                                                                                       │
│   Triage steps                                                                                        │
│   1. Validate the alert is genuine; confirm affected asset and scope                                  │
│   2. Classify severity; notify on-call IR lead for P1/P2                                              │
│   3. Isolate affected host (network isolation) before investigation to prevent spread                 │
│   4. Begin evidence collection: memory, disk image, logs, network captures                            │
│                                                                                                       │
│   Post-incident review                                                                                │
│   Timeline reconstruction; root cause analysis; MITRE ATT&CK technique mapping                        │
│   Gap identification: detection missed, containment delayed, or evidence lost                         │
│   Action items: update playbooks, tune detection rules, patch exploited vulnerability                 │
│                                                                                                       │
│   Key terms:                                                                                          │
│   chain of custody = documented record of who collected, handled, and stored each evidence item       │
│   memory dump      = volatile memory capture (Volatility); must be taken before reboot                │
│   MITRE ATT&CK     = adversary tactics and techniques framework; maps incident to known TTPs          │
│   isolation        = network quarantine of a host to prevent lateral movement during investigation    │
│   regulatory notif = mandatory breach notification to regulator (GDPR 72h, HIPAA 60d timelines)       │
│   IR playbook      = documented step-by-step response procedure for a specific incident type          │
│   P1 SLA           = initial response within 15 minutes; incident commander assigned within 30 min    │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-1">

<a class="kb-card" href="procedures/">
  <strong>Standard Procedures</strong>
  <span>Incident handling procedures — first response, classification, escalation matrix, evidence collection, and post-incident review steps.</span>
</a>

</div>
