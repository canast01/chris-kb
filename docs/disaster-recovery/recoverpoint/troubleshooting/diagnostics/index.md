# RecoverPoint — Diagnostics

> Part of the [RecoverPoint](../../index.md) > [Troubleshooting](../index.md) reference.

---

## Log Locations

| Log | Location |
|---|---|
| RPA system logs | Accessible via `boxmgmt` → `Support` → `Collect support bundle` |
| RPMA audit log | RecoverPoint Management Application → Reports → Audit Log |
| Splitter logs (ESXi) | `/var/log/vmkernel.log` on ESXi host |

---

## Support Bundle Collection

```bash
# Via boxmgmt
boxmgmt support collect_bundle
```
┌───────────────────────────────────── RecoverPoint — Diagnostics ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               RecoverPoint — Diagnostic Commands                              │   │
│   │                       Collect these before opening a vendor support case                      │   │
│   │                                   image access enable/disable                                 │   │
│   │                                        failover / reverse                                     │   │
│   │                       Check system logs: /var/log/ or Windows Event Viewer                    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Log Collection                │  │               Live Diagnostics              │   │
│   │            Application log bundle            │  │             Network connectivity            │   │
│   │            OS syslog (journalctl)            │  │              Storage path check             │   │
│   │             Core dump if crashed             │  │              Process list check             │   │
│   │             Config export/backup             │  │              Port reachability              │   │
│   │         image access enable/disable          │  │              failover / reverse             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  RPA virtual appliances on ESXi · Journal volumes on storage array · WAN link between sites           │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPA           = RecoverPoint Appliance — virtual appliance managing journal and replication          │
│  Splitter      = intercepts host I/O at hypervisor or array level; sends copy to RPA                  │
│  Journal       = write-order-consistent storage capturing all writes for point-in-time access         │
│  Consistency Group= set of volumes protected together; writes are applied in order across all         │
│  Bookmark      = named marker in journal; enables deterministic recovery to a known state             │
│  Image Access  = mounting a journal point-in-time image to a host for testing or recovery             │
│  Failover      = activating the replica at the recovery site; breaks replication relationship         │
│  Test Copy     = non-disruptive image access for validation without breaking replication              │
│  RPO           = Recovery Point Objective; how much data loss is acceptable; CDP = near-zero          │
│  RTO           = Recovery Time Objective; time from failover to service restored                      │
│  Reverse       = after failover, replicates from recovery site back to re-sync production             │
│  Splitter Lag  = delay between host write and journal commit; monitor for replication health          │
│  CDP           = Continuous Data Protection; every write journaled, not just scheduled snaps          │
│  Distributed CG= consistency group spanning volumes on multiple storage arrays                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

---

## Splitter Health Check on ESXi (RP4VM)

The RP4VM vSphere splitter is installed as a VIB on ESXi hosts. Use these commands directly on the ESXi host (SSH or ESXi shell).

```bash
# Check RP4VM splitter VIB is installed
esxcli software vib list | grep -i recoverpoint

# Verify the splitter driver is loaded
vmkload_mod -l | grep splitter

# Check vmkernel log for splitter-related events
grep -i "recoverpoint\|rp4vm\|splitter" /var/log/vmkernel.log | tail -50

# List all VMs with RP4VM splitter protection active
esxcli recoverpoint vm list

# Show splitter statistics for a specific VM (replace <vmid> with VM world ID)
esxcli recoverpoint vm stats --vm-id <vmid>

# Verify RPA connectivity from the ESXi splitter perspective
esxcli recoverpoint rpa list

# Check splitter-to-RPA link state
esxcli recoverpoint rpa stats
```

> If `esxcli recoverpoint` commands are not available, the RP4VM VIB is not installed or has been corrupted. Re-deploy from the RecoverPoint Deployment Manager.
