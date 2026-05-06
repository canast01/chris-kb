# NetApp SnapMirror Vendor Support

## Support Portal

NetApp support portal: [https://mysupport.netapp.com](https://mysupport.netapp.com)

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
