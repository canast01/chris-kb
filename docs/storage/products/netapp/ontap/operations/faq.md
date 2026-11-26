---
tags:
  - netapp-ontap
  - faq
  - operations
description: "Common questions about NetApp ONTAP operations, configuration, and troubleshooting. For step-by-step procedures, see the Operations section."
---
# NetApp ONTAP — Frequently Asked Questions

*Applies to: NetApp ONTAP 9.18.1–9.20.1*

<div class="kb-summary">
Common questions about NetApp ONTAP operations, configuration, and troubleshooting. For step-by-step procedures, see the <a href="../">Operations</a> section.
</div>
![NetApp ONTAP — Frequently Asked Questions](../../../../../assets/storage-netapp-ontap-operations-faq.svg)

## General

**Q: What ONTAP version is recommended for new deployments?**
A: The current release is ONTAP 9.20.1 (November 2026); 9.19.1 (July 2026) and 9.18.1 (November 2025) are the previous releases ([ONTAP 9 release support](https://docs.netapp.com/us-en/ontap/release-notes/release-support-reference.html)). Choose a release supported on your hardware (NetApp Hardware Universe) and apply its latest patch release; NetApp publishes Minimum Recommended ONTAP releases on the NetApp Support Site. Check with `version` from ONTAP CLI or System Manager → Cluster → Software. Always apply the latest patch release.

**Q: How do I check the current NetApp ONTAP version?**
A: `version`

## Configuration

**Q: What is the default volume guarantee and when should it change?**
A: Default is `volume` guarantee (thick provisioning). Switch to `none` (thin provisioning) to allow overcommitment: `volume modify -volume vol1 -space-guarantee none`. Monitor aggregate space carefully when thin provisioning.

**Q: How do I enable ONTAP inline deduplication and compression?**
A: `volume efficiency on -volume vol1` enables inline dedup and compression. Verify: `volume efficiency show -volume vol1`. For AFF arrays, both are enabled by default. Expected savings: 2-5x for typical workloads.

## Operations

**Q: How do I perform an ONTAP rolling upgrade without downtime?**
A: Use ONTAP automated non-disruptive upgrade (ANDU): download the image with `cluster image package get -url <url>`, then start the update with `cluster image update -version <version>`. ANDU upgrades nodes one at a time, taking over and giving back storage. Monitor with `cluster image show-update-progress` and verify with `cluster image show`.

**Q: What is the correct procedure to create a new SVM and NFS export?**
A: `vserver create -vserver nfs_svm -rootvolume root -rootvolume-security-style unix`. Add data LIF. Create volume. Add export policy. Verify: `vserver show -vserver nfs_svm`. Test mount from a client.

## Troubleshooting

**Q: ONTAP shows 'Aggregate is nearly full'. What does it mean?**
A: Aggregate space usage is above 90%. ONTAP restricts new volume creation and thin-provisioned writes above 98%. Add drives, move volumes to another aggregate, or delete snapshots to reclaim space immediately.

**Q: NFS/iSCSI latency increased — where do I start?**
A: Check `qos statistics performance show` for workload latency breakdown. Review `statistics show -object volume` for per-volume IOPS. Check aggregate disk busy % with `storage aggregate show-space`. Review network with `network interface show`.

## Backup and Recovery

**Q: How often should I back up ONTAP configuration?**
A: ONTAP automatically backs up configuration to all nodes. Manual export: `system configuration backup upload`. For disaster recovery, configure SnapMirror for data and MetroCluster for HA. Test failover quarterly.

**Q: Can I restore a single file from an ONTAP snapshot?**
A: Yes — access the `.snapshot` directory in any NFS mount (`ls /mnt/vol1/.snapshot`). Copy the file directly from the snapshot directory. For block (iSCSI/FC), use SnapRestore: `volume snapshot restore-file -volume vol -snapshot snap -path /file`.

## See Also

- [NetApp ONTAP Operations](index.md)
- [NetApp ONTAP Troubleshooting](../../../../troubleshooting/index.md)
