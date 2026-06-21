---
tags:
  - netapp
  - troubleshooting
search:
  boost: 1.5
---
# Superna Eyeglass — Common Issues


<div class="kb-summary">
Common Superna Eyeglass issues — sync failures, DR test errors, configuration drift, and SyncIQ job problems.

*Applies to: Superna Eyeglass*
</div>
![Superna Eyeglass — Common Issues](../../../../assets/storage-netapp-superna-eyeglass-troubleshooting-common-issue.svg)



Common Eyeglass issues include SyncIQ policies not being detected, low DR readiness scores, DNS cutover failures, and failover jobs that stall or complete with errors. Most issues trace back to API connectivity between Eyeglass and the PowerScale clusters, configuration drift between the primary and DR cluster, or DNS delegation misconfiguration.

| Issue | Likely Cause | Resolution |
|---|---|---|
| SyncIQ policy not detected | Eyeglass-to-OneFS API connectivity failure | Check Eyeglass cluster credentials and OneFS API reachability; re-register cluster in Eyeglass |
| DR readiness score low | Quota or share mismatch between clusters | Review Eyeglass sync log; re-run share/quota sync; check for manually created shares not in Eyeglass |
| DNS cutover failure | DNS delegation not configured or DNS plugin issue | Verify DNS delegation zone configuration; check Eyeglass DNS plugin logs; test manual DNS cutover |
| Failover stuck / not completing | API timeout, share conflict, or quota error | Review Eyeglass admin UI task log; check OneFS audit log for errors; use manual intervention steps in Eyeglass UI |
| RPO breach alerts | SyncIQ replication lag exceeding threshold | Check SyncIQ job status on source cluster (`isi sync jobs list`); check network bandwidth between sites |
| Eyeglass appliance unreachable | VM or network issue | Verify VM is powered on in vCenter; check management network connectivity; check Eyeglass service status via console |

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> A[Configuration replication lag]
    S --> B[SVM DR failover test failed]
    S --> C[Audit event not captured]
    S --> D[Eyeglass appliance unreachable]
    S --> E[License expiry warning]
    A --> A1{API connectivity OK?}
    A1 -->|No| A2[Re-register cluster credentials in Eyeglass — see Common Issues Reference]
    A1 -->|Yes| A3[Check SyncIQ job status and network bandwidth between sites]
    B --> B1{Pre-check passed?}
    B1 -->|No| B2[Fix pre-check error; re-run DR runbook — see Common Issues Reference]
    B1 -->|Yes| B3[Review Eyeglass task log and OneFS audit log for step-level error]
    C --> C1{RAPA service running?}
    C1 -->|No| C2[Restart RAPA service on Eyeglass appliance]
    C1 -->|Yes| C3[Verify audit log connector configuration and OneFS audit settings]
    D --> D1{VM powered on?}
    D1 -->|No| D2[Power on Eyeglass VM in vCenter — see Common Issues Reference]
    D1 -->|Yes| D3[Check management network and Eyeglass service status via console]
    E --> E1[Log in to Superna portal and renew license; apply key in Eyeglass UI]
    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class A,B,C,D,E,A2,A3,B2,B3,C2,C3,D2,D3,E1 section
    class A1,B1,C1,D1 decision
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

- [Superna Eyeglass — Diagnostics](diagnostics/)
- [Superna Eyeglass — Escalation](escalation/)
- [Superna Eyeglass — Health Checks](../operations/health-checks/)
