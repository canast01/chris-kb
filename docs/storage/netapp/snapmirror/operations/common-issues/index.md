# SnapMirror — Known Issues

> Part of the [SnapMirror Operations](../index.md) reference.

---

## Incident Triage

- [ ] Run `snapmirror show -fields lag-time,healthy,state` — identify which relationships are affected
- [ ] Check the `reason` field on unhealthy relationships: `snapmirror show -destination-path <svm:vol>` for full detail
- [ ] Check network bandwidth between source and destination — large lag increases often point to bandwidth saturation: `network port show` and review inter-cluster LIF stats
- [ ] Check destination volume space: `volume show -vserver <dst-svm> -volume <dst-vol> -fields used-percent` — a full destination volume blocks transfers
- [ ] For `broken-off` state: determine if this was an intentional DR test or an unplanned break; do not resync without confirming data direction first
- [ ] For SnapMirror Synchronous `Out-of-Sync`: check inter-cluster LIF connectivity; relationship will attempt auto-resync once connectivity is restored
- [ ] For SMBC: run `snapmirror mediator show` to verify mediator health; check pod state with the source-cluster `snapmirror show` command

| Question | Answer |
|---|---|
| Which relationships are unhealthy or lagging? | |
| What is the reason field showing? | |
| Is this broken-off intentional (DR test) or unplanned? | |
| Is the destination volume full? | |
| Is the network path between sites healthy? | |

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
