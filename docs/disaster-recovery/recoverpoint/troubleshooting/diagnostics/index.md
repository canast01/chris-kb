# RecoverPoint — Diagnostics

> Part of the [RecoverPoint](../../) > [Troubleshooting](../) reference.

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

Upload bundle to Dell Support case via https://www.dell.com/support.

---

## `boxmgmt` Command Reference

SSH to the RPA as `admin` (default port 22) and use `boxmgmt` for all diagnostic and management operations.

### System and Hardware Health

| Command | Purpose |
|---|---|
| `boxmgmt system show_system_info` | RPA model, firmware version, serial number |
| `boxmgmt system show_hw_status` | Hardware component health (PSU, fans, NICs) |
| `boxmgmt system show_load` | CPU and memory utilisation on the RPA |
| `boxmgmt network show_interfaces` | NIC status, IP addresses, link state |
| `boxmgmt network ping <ip>` | ICMP connectivity test from RPA to target IP |
| `boxmgmt network traceroute <ip>` | Trace route from RPA for path diagnostics |
| `boxmgmt storage show_volumes` | Storage volumes visible to the RPA |
| `boxmgmt storage show_journal_state` | Journal volume status per consistency group |

### Replication Link Health

| Command | Purpose |
|---|---|
| `boxmgmt links show_link_status` | WAN link state and latency between RPAs |
| `boxmgmt links show_link_stats` | Throughput, packet loss on inter-RPA links |
| `boxmgmt links show_compression_stats` | WAN compression ratio and savings |

### Consistency Group State

| Command | Purpose |
|---|---|
| `boxmgmt cgs show_all_cgs` | List all consistency groups and their states |
| `boxmgmt cgs show_cg_state <cg_name>` | Detailed state for a specific CG (Active, Paused, Initialising) |
| `boxmgmt cgs show_lag <cg_name>` | Replication lag (RPO delta) for a specific CG |
| `boxmgmt cgs show_journal_usage <cg_name>` | Journal capacity consumption and headroom |

---

## CLI Diagnostic Commands via SSH (RPACLI)

When logged into the RPA via SSH, the RPACLI shell is available as an alternative to `boxmgmt` for consistency-group-level diagnostics.

```bash
# Connect to RPA
ssh admin@<rpa-ip>

# Enter RPACLI (if not default shell)
rpacli

# List all clusters in the RecoverPoint deployment
get_all_clusters

# Show system-wide replication status
get_system_status

# Show all consistency groups with state and lag
get_all_groups_state

# Show detailed info for a specific consistency group
get_group_state --group "CG-VM-Prod"

# Show copy set details (source and replica volumes) for a CG
get_copy_sets --group "CG-VM-Prod"

# Show link health between this cluster and a remote cluster
get_link_health --local-cluster "Site-A" --remote-cluster "Site-B"

# Test WAN link connectivity to remote RPA
test_link --remote-rpa <remote-rpa-ip>

# Show journal state for a specific copy
get_journal_state --group "CG-VM-Prod" --copy "DR-Copy"
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
