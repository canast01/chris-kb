---
tags:
  - operations
  - pure
---
# FlashBlade — Known Issues


<div class="kb-summary">
Known Issues reference covering Incident Triage, Common Issues Reference.
</div>

```text
FlashBlade Triage Flow
  Alert / Symptom reported
          │
          ▼
  purefb alert list ──► Identify failure domain
          │
   ┌────────────────────────────────────────────────── ┴ ──────────────────────────────────────────────────┐
   ▼                                     ▼
Blade fault                       Client connectivity loss
purefb blade list                  Check NFS export policy
  │                                or S3 bucket ACL
  ▼                                       │
Open Pure support case             Verify network / IP routing
  │                                from client to FlashBlade
  ▼
Monitor blade replacement

Replication issue:
  purefb replication list ──► lag / status ──► check network BW
```

> Part of the [FlashBlade Operations](../index.md) reference.

---

## Incident Triage

- [ ] Run `purefb alert list` first — active alerts identify the failure domain (blade, hardware, replication, capacity)
- [ ] Run `purefb blade list` — a failed or missing blade is a capacity and performance degradation event; open a Pure support case immediately
- [ ] Run `purefb hardware list` — check for failed PSU, fan, or fabric module; multiple failures on the same chassis indicate a critical event
- [ ] Check filesystem and bucket accessibility: `purefb filesystem list` — a filesystem at its provisioned limit causes client write failures
- [ ] Check replication: `purefb replication list` — an `inactive` or high-lag replication link requires investigation of the network path between sites
- [ ] For NFS `stale file handle` errors: the issue is typically client-side after a FlashBlade event — unmount and remount on affected clients
- [ ] For S3 403 errors: run `purefb objectstoreaccount list` to check access key status and verify bucket policies

| Question | Answer |
|---|---|
| What does `purefb alert list` show? | |
| Are any blades failed or missing? | |
| Is any filesystem at or near its provisioned limit? | |
| Are ActiveDR replication links active and within RPO? | |
| Is this affecting NFS, SMB, S3, or all protocols? | |

## Common Issues Reference

| Symptom | Likely Cause | Action |
|---|---|---|
| Blade in `failed` or `missing` state | Physical blade hardware failure or seating issue | Run `purefb blade list`; open a Pure support case immediately — capacity and throughput are reduced until the blade is replaced; do not attempt to reseat the blade without Pure Support guidance |
| NFS clients showing stale file handle errors | Client-side NFS state not cleaned after a FlashBlade event (blade failover or upgrade) | Unmount and remount the NFS filesystem on affected clients; verify `/etc/fstab` uses `soft` or `intr` NFS mount options to prevent hard-hang on server-side events |
| NFS mounts timing out or hanging | FlashBlade data VIP unreachable due to network issue; NFS export policy blocking the client | Verify the FlashBlade data VIP is reachable from the client (`ping`); run `purefb network interface list` to confirm VIP is `up`; check NFS export policy source IP rules |
| S3 returning 403 Forbidden | S3 access key expired, suspended, or IAM bucket policy denies the operation | Run `purefb objectstoreuser list` to check key status; regenerate the access key; review bucket access policies under `purefb bucket list --access-policy` |
| ActiveDR replication lag exceeding RPO | Replication network bandwidth saturated or replication link down | Run `purefb replication list` to check lag and link state; verify network path between sites; check for bandwidth saturation on replication interfaces |
| SMB share inaccessible after AD credential change | FlashBlade machine account password or AD bind credentials have expired | Rejoin the FlashBlade to Active Directory from the GUI or CLI; update AD bind credentials in the directory service configuration |
| Filesystem approaching its provisioned limit | Organic data growth or backup tool writing more than expected | Expand the filesystem limit non-disruptively: `purefb filesystem update --provisioned <new_size> <fsname>`; review backup retention policies to expire older data |
| Blade in `rebalancing` state after blade add | Normal state during data rebalancing after a new blade is added | This is expected behaviour — monitor progress with `purefb blade list`; do not interrupt the rebalancing process; alert if rebalancing is stuck for more than 24 hours |
| High NFS latency during AI/ML training | Clients not using pNFS parallel access; single VIP bottleneck | Enable pNFS (NFSv4.1 pNFS) on the filesystem and verify client NFS mounts use `nfsvers=4.1` and `proto=tcp`; pNFS allows clients to access multiple blades in parallel |
| Snapshot schedule not creating snapshots | Snapshot policy not associated with the filesystem, or policy is paused | Run `purefb policy list` to verify the snapshot policy; check `purefb snap list` to confirm recent snapshots exist; re-associate the policy with the filesystem if needed |
| NFS mount fails | Export rules | Verify client IP matches export rule |
| SMB share inaccessible | SMB enabled | `purefb fs update --smb-enabled true` |
| File system full | Capacity | Resize with `purefb fs update --size` |
| Snapshot missing | Snapshots enabled? | Enable with `--snapshot-enabled true` |
| S3 access denied | Access key credentials | Verify key matches user/account |
| Bucket not found | Bucket name correct | `purefb bucket list` |
| Replication lag high | Network or capacity | Check inter-array connectivity |
| Cannot delete bucket | Bucket not empty | Delete objects first |
