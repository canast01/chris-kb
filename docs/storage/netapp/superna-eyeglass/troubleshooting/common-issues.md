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

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```d2
direction: right

S: "What is the symptom?" {shape: rectangle}
A: "Configuration replication lag" {shape: rectangle}
B: "SVM DR failover test failed" {shape: rectangle}
C: "Audit event not captured" {shape: rectangle}
D: "Eyeglass appliance unreachable" {shape: rectangle}
E: "License expiry warning" {shape: rectangle}
A1: "A1" {shape: rectangle}
A2: "Re-register cluster credentials in Eyeglass — see\nCommon Issues Reference" {shape: rectangle}
A3: "Check SyncIQ job status and network bandwidth\nbetween sites" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "Fix pre-check error; re-run DR runbook — see\nCommon Issues Reference" {shape: rectangle}
B3: "Review Eyeglass task log and OneFS audit log for\nstep-level error" {shape: rectangle}
C1: "C1" {shape: rectangle}
C2: "Restart RAPA service on Eyeglass appliance" {shape: rectangle}
C3: "Verify audit log connector configuration and OneFS\naudit settings" {shape: rectangle}
D1: "D1" {shape: rectangle}
D2: "Power on Eyeglass VM in vCenter — see Common\nIssues Reference" {shape: rectangle}
D3: "Check management network and Eyeglass service\nstatus via console" {shape: rectangle}
E1: "Log in to Superna portal and renew license; apply\nkey in Eyeglass UI" {shape: rectangle}

S -> A
S -> B
S -> C
S -> D
S -> E
A1 -> A2
A1 -> A3
B1 -> B2
B1 -> B3
C1 -> C2
C1 -> C3
D1 -> D2
D1 -> D3
E -> E1
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

- [Superna Eyeglass — Diagnostics](../diagnostics/)
- [Superna Eyeglass — Escalation](../escalation/)
- [Superna Eyeglass — Health Checks](../../operations/health-checks/)
