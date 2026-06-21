---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# FOD — Common Issues


<div class="kb-summary">
Common FOD activation errors, feature entitlement failures, and troubleshooting unlicensed features.

*Applies to: Dell FOD*
</div>
![FOD — Common Issues](../../../../assets/storage-dell-fod-troubleshooting-common-issues.svg)




> Part of the [Flex on Demand](../index.md) reference.

---

| Symptom | Likely Cause | Action |
|---|---|---|
| Unexpected burst charges on FOD bill | Workload spike or snapshot/backup growth pushed usage above committed baseline | Review CloudIQ capacity trend for the billing period; identify the growth driver; adjust committed baseline if sustained |
| CloudIQ reports no telemetry for a FOD-enrolled system | Secure Connect Gateway offline or CloudIQ agent not running | Check SCG appliance health; verify outbound HTTPS connectivity to Dell CloudIQ endpoints |
| FOD capacity ceiling reached (no more burst available) | All pre-installed burst capacity is consumed | Contact Dell account team to install additional physical capacity under the FOD agreement |
| Committed baseline appears incorrect in APEX Console | Baseline was set at contract time and workload changed | Submit a baseline adjustment request through APEX Console or Dell account team |

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?])
    S --> B1{Feature activation\nkey not accepted?}
    S --> B2{Feature not visible\nafter license?}
    S --> B3{Support contract\nmismatch?}

    B1 -->|Verify array SN from GUI| D1{SN in key\nmatches array SN?}
    D1 -->|No - SN mismatch| R1[See Issue Reference —\nKey rejected: verify SN then re-download]
    D1 -->|Already applied| R2[See Issue Reference —\nKey duplicate: harmless; check event log]

    B2 -->|Check firmware version| D2{Firmware meets\nminimum requirement?}
    D2 -->|No| R3[See Issue Reference —\nFW too old: upgrade firmware first]
    D2 -->|Feature hidden| R4[See Issue Reference —\nFeature hidden: check Settings > Features]

    B3 -->|Check SN linked to support account| D3{SN linked to\nDell account?}
    D3 -->|No| R5[See Issue Reference —\nAccount link: link SN to support account]
    D3 -->|Wrong feature| R6[See Issue Reference —\nWrong feature: verify key description before buy]

    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class R1,R2,R3,R4,R5,R6 section
    class B1,B2,B3,D1,D2,D3 decision
    class S start
```

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Fod — Diagnostics](diagnostics/)
- [Fod — Escalation](escalation/)
- [Fod — Health Checks](../operations/health-checks/)
