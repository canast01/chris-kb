---
tags:
  - netapp
  - troubleshooting
search:
  boost: 1.5
---
# SnapMirror — Common Issues


<div class="kb-summary">
SnapMirror troubleshooting: `snapmirror show -fields status,health` for broken relationships, transfer failures, missing common snapshots, and NetApp support escalation.

*Applies to: SnapMirror*
</div>
![SnapMirror — Common Issues](../../../../assets/storage-netapp-snapmirror-troubleshooting-common-issues.svg)




---

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> A[Relationship in broken-off state]
    S --> B[Lag time exceeding RPO]
    S --> C[Transfer stuck in progress]
    S --> D[Destination volume full]
    S --> E[SnapMirror Sync out of sync]
    A --> A1{Was a failover or DR test run?}
    A1 -->|Yes| A2[Resync after confirming data direction — see Common Issues Reference]
    A1 -->|No| A3[Check for manual quiesce and break commands in audit log]
    B --> B1{Network or schedule issue?}
    B1 -->|Network| B2[Check intercluster LIF and WAN bandwidth — see Common Issues Reference]
    B1 -->|Schedule| B3[Increase transfer frequency or adjust throttle]
    C --> C1{Source snapshot still present?}
    C1 -->|No| C2[Abort and restart transfer — see Common Issues Reference]
    C1 -->|Yes| C3[Check network interruption and resume transfer]
    D --> D1{Retention policy correct?}
    D1 -->|No| D2[Update SnapVault retention and delete excess snapshots]
    D1 -->|Yes| D3[Expand destination volume size — see Common Issues Reference]
    E --> E1[Check intercluster latency; relationship auto-resyncs on restore — see Common Issues Reference]
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

## Common Issues Reference

| Symptom | Likely Cause | Action |
|---|---|---|
| Relationship in `broken-off` state | `snapmirror quiesce` + `snapmirror break` was run manually for a DR test or failover and was never resynced | Resync with `snapmirror resync -destination-path svm_dst:vol_dst`; confirm data direction before running |
| Lag time exceeding RPO | Network congestion, high source change rate, or transfer schedule too infrequent | Check `snapmirror show -fields lag-time,transfer-bytes`; increase schedule frequency or investigate network bandwidth |
| Transfer stuck in progress | Network interruption mid-transfer or source snapshot deleted before transfer completed | Run `snapmirror abort -destination-path svm_dst:vol_dst`; wait for abort to complete; restart with `snapmirror update` |
| Destination volume full | SnapVault/XDP retention policy not pruning old snapshots; autogrow not configured | Check destination volume space with `volume show -fields size,used`; review SnapVault retention rules; delete excess snapshots |
| SMBC mediator unreachable | Network connectivity issue to mediator VM or mediator service not running | Check mediator connectivity from both clusters: `snapmirror mediator show`; verify mediator VM status and network path |
| Initialize failing: destination not DP type | Destination volume created as RW instead of DP | Delete and recreate destination volume with `-type DP`; rerun `snapmirror initialize` |
| SnapMirror Sync showing `Out-of-Sync` | Inter-site latency exceeded threshold or network interruption | Check intercluster LIF connectivity; relationship auto-resyncs when connectivity restores within the resync window |
| SVM-DR update failing | SVM configuration change on source not yet reflected on destination | Run `snapmirror update -destination-path svm_dst:` at the SVM level to force a configuration sync |

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Snapmirror — Diagnostics](diagnostics/)
- [Snapmirror — Escalation](escalation/)
- [Snapmirror — Health Checks](../operations/health-checks/)
