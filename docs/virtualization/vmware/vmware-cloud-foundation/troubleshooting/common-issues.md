---
tags:
  - troubleshooting
  - vcf
  - vmware
search:
  boost: 1.5
---
# VCF Troubleshooting — Common Issues


<div class="kb-summary">
Common Issues reference covering Common Issues, Technical Deep Dive.

*Applies to: VCF 4.x / 5.x*
</div>
![VCF Troubleshooting — Common Issues](../../../../assets/virtualization-vmware-vmware-cloud-foundation-troubleshootin.svg)


VCF Common Failure Points — Quick Reference


```d2
direction: down

symptom: Identify Symptom {shape: diamond}
general_troubleshooting: "General Troubleshooting" {shape: rectangle}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> general_troubleshooting: investigate
symptom -> diagnostic_flow: investigate
symptom -> verify_resolution: investigate
general_troubleshooting -> resolution
diagnostic_flow -> resolution
verify_resolution -> resolution
```

## General Troubleshooting

### Common Failure Points

- Lifecycle bundle issue
- Compatibility mismatch
- Password drift
- Certificate drift
- Workload domain health issue
- SDDC Manager service issue
- NSX/vCenter dependency failure
- DNS/NTP issue

### Troubleshooting Workflow

1. Confirm the impact and scope.
2. Check recent changes.
3. Review alerts, tasks, and events.
4. Validate DNS, NTP, authentication, and certificates.
5. Check service status.
6. Check storage and network dependencies.
7. Review logs.
8. Capture screenshots, timestamps, errors, and task IDs.
9. Escalate with clean evidence if needed.

### Upgrade and Compatibility Notes

- Check product interoperability before upgrades.
- Confirm supported version path.
- Confirm backup or rollback method.
- Confirm maintenance window.
- Run pre-checks before change work.
- Validate health after the change.
- Document version before and after.

### Best Practices

| Recommendation | Detail |
|---|---|
| Keep versions aligned. | Keep versions aligned. |
| Keep certificates tracked. | Keep certificates tracked. |
| Keep DNS and NTP clean. | Keep DNS and NTP clean. |
| Keep alerting actionable. | Keep alerting actionable. |
| Document support ownership. | Document support ownership. |
| Avoid undocumented changes. | Avoid undocumented changes. |

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> B1[Upgrade task failed or stuck]
    S --> B2[SOS pre-check failure]
    S --> B3[Workload domain deploy error]
    S --> B4[Certificate sync failure]
    S --> B5[LCM task stuck]
    S --> B6[SDDC Manager unreachable]

    B1 --> D1{Pre-checks\npassed?}
    D1 -->|No| R1[Resolve Pre-check Failures\n→ Upgrade and Compatibility Notes]
    D1 -->|Yes| R2[Retry Failed Step in SDDC Mgr\n→ Troubleshooting Workflow]

    B2 --> R3[Check DNS · NTP · Credentials\n→ Common Failure Points]

    B3 --> D2{DNS and HCL\nvalid?}
    D2 -->|No| R4[Fix DNS A+PTR · Check HCL\n→ Common Failure Points]
    D2 -->|Yes| R5[Review SDDC Mgr Tasks\n→ Troubleshooting Workflow]

    B4 --> R6[Renew Cert via SDDC Mgr UI\n→ Best Practices]

    B5 --> R7[Check Task View · Restart Services\n→ Troubleshooting Workflow]

    B6 --> R8[Check Postgres · Disk Space · Logs\n→ Troubleshooting Workflow]

    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class R1,R2,R3,R4,R5,R6,R7,R8 section
    class D1,D2 decision
    class S start
```

---

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## See also

- [VCF Troubleshooting — Diagnostics](diagnostics/)
- [VCF Troubleshooting — Escalation](escalation/)
- [VCF — Health Checks](../operations/health-checks/)

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
