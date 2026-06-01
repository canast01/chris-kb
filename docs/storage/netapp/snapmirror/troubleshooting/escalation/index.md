# SnapMirror — Escalation


<div class="kb-summary">
> Part of the [SnapMirror Troubleshooting](../index.md) reference.
</div>
```text
┌─────────────────────────────────── NetApp SnapMirror — Escalation ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     SnapMirror escalation: severity triage, vendor support contact, and required artifacts    │   │
│   │         L1: basic checks, restart services; L2: log analysis, config review, vendor SR        │   │
│   │        Severity: P1 production down → immediate SR + on-call page; P2/P3 business hours       │   │
│   │         Before escalating: collect support bundle, event timeline, and change history         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Detect issue → triage severity → collect artifacts → open SR → update                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Async            │  │        Periodic sync        │  │         RPO: minutes        │   │
│   │             Sync            │  │           Zero RPO          │  │          Sub-ms lag         │   │
│   │            SM-BC            │  │        Active-active        │  │        Transparent FO       │   │
│   │            Vault            │  │        Long retention       │  │         Backup copy         │   │
│   │            Cloud            │  │         ONTAP → CVO         │  │       Cloud DR/backup       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Severity     │     Criteria     │   Response time   │      Owner       │    Vendor SLA    │   │
│   │        P1        │ Production down  │     Immediate     │   On-call + L2   │    1 hr 24x7     │   │
│   │        P2        │  Major degraded  │       1 hour      │   L2 engineer    │   4 hr biz hrs   │   │
│   │        P3        │  Minor degraded  │      4 hours      │   L2 engineer    │   8 hr biz hrs   │   │
│   │        P4        │    No impact     │    Next biz day   │    L1 support    │    2 biz days    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Source ONTAP cluster · destination ONTAP cluster · intercluster LIFs · WAN link          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SnapMirror         = ONTAP replication; transfers only changed blocks after initial baseline sync  │
│    Intercluster LIF   = dedicated logical interface for SnapMirror traffic between clusters           │
│    SnapMirror policy  = defines schedule, retention, and transfer type (async/sync/vault)             │
│    Baseline transfer  = first full snapshot transfer establishing the SnapMirror relationship         │
│    Update             = incremental transfer; only sends new or changed blocks since last successfu...│
│    Snapmirror break   = breaks the DR relationship; activates destination volume for read-write       │
│    Resync             = re-establishes a broken SnapMirror relationship from the last common snapshot │
│    SM-BC              = SnapMirror Business Continuity; synchronous zero-RPO active-active SAN volumes│
│    Mediator           = ONTAP Mediator; quorum service for SM-BC running on Linux VM at third site    │
│    SnapVault          = SnapMirror variant for backup retention; destination has independent schedule │
│    MirrorAndVault     = policy combining SnapMirror DR and SnapVault backup retention copies          │
│    Fanout             = single source volume replicating to multiple destination clusters simultane...│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## Support Portal

NetApp support portal: [https://support.netapp.com](https://support.netapp.com)

SnapMirror issues are handled under the standard ONTAP support contract — there is no separate SnapMirror support entitlement. Ensure both source and destination clusters are covered under active support contracts before opening a case, as NetApp may require access to both clusters to diagnose replication issues.

## Opening a Case

Required information when opening a SnapMirror support case:

- ONTAP version on both source and destination clusters
- SnapMirror relationship name and destination path (`svm_dst:vol_dst`)
- Relationship type (Async XDP, Sync, SMBC, SVM-DR)
- `snapmirror show` output from the destination cluster
- EMS log extract covering the time of the failure
- AutoSupport triggered from both clusters
- Clear description of the symptom and business impact

## Information to Collect

```bash
# Trigger AutoSupport from both clusters before calling
system node autosupport invoke -node * -type all -message "case <number>"

# Full relationship detail
snapmirror show -expanded

# Transfer history
snapmirror show-history -destination-path svm_dst:vol_dst

# EMS error events
event log show -severity error -time-range <start>..<end>

# SnapMirror-specific EMS events
event log show -message-name snapmirror.*

# Intercluster LIF status
network interface show -role intercluster

# SMBC mediator status (if applicable)
snapmirror mediator show
```

## SLA Tiers

| Priority | Response Time | Coverage |
|---|---|---|
| P1 | 1 hour | 24x7 — production down, DR unavailable |
| P2 | 2 hours | 24x7 — degraded protection, RPO at risk |
| P3 | 4 hours | Business hours — non-critical issue |
| P4 | Next business day | Low impact, informational |

SLA tiers apply under the NetApp SupportEdge Expert or Premier contract. Verify your entitlement tier at the support portal.

## Escalation

- For critical DR scenarios where replication is broken and production access is at risk, request a duty manager escalation at case creation
- Engage the NetApp account team for executive escalation when standard P1 response is not meeting the situation
- Request TAM (Technical Account Manager) engagement for SMBC implementations — SMBC is a complex feature where TAM guidance significantly reduces implementation risk
- NetApp can provide remote hands access to both clusters with customer consent to perform live diagnostics during a P1 event
