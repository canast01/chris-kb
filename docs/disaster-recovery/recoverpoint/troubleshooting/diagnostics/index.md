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
```

---

## Common Log Analysis: What to Look For in a Support Bundle

After collecting a support bundle (`boxmgmt support collect_bundle`), extract and review the following:

| Log File (inside bundle) | What to Look For |
|---|---|
| `system/messages` | Kernel errors, OOM events, hardware faults |
| `rp/rpa_log` | RPA process crashes, journal overflow events, CG state transitions |
| `rp/wcc_log` | WAN connectivity controller errors; look for `LINK_DOWN` or `TIMEOUT` entries |
| `rp/splitter_log` | Splitter-to-RPA communication failures; `SPLIT_ERROR` indicates data not being captured |
| `rp/journal_log` | Journal allocation failures, journal full events — indicates RPO at risk |
| `network/ifconfig` | Verify NIC configuration matches expected topology |
| `storage/disk_info` | Storage path failures, multipath issues |

**Key patterns to grep for:**

```bash
# After extracting the bundle tarball
grep -i "LINK_DOWN\|TIMEOUT\|JOURNAL_FULL\|SPLIT_ERROR\|CG_PAUSED" rp/rpa_log
grep -i "error\|critical\|fatal" system/messages | grep -v "audit"
grep -i "INIT\|PAUSE\|FAILOVER" rp/rpa_log | tail -50
```

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
