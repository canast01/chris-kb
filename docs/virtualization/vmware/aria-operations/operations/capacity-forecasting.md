---
tags:
  - aria-operations
  - operations
  - vmware
---
# Capacity Forecasting

<div class="kb-summary">
Capacity forecasting predicts when a resource will be exhausted based on historical trend data, enabling proactive expansion before impact occurs.

*Applies to: Aria Ops 8.x*
</div>

```d2
direction: right

forecasting_model: "Forecasting Model" {shape: rectangle}
forecasting_by_resource_type: "Forecasting by Resource Type" {shape: rectangle}
forecasting_thresholds: "Forecasting Thresholds" {shape: rectangle}
capacity_report_template: "Capacity Report Template" {shape: rectangle}
automation_monthly_report_script: "Automation — Monthly Report Script" {shape: rectangle}
verify: "Verify" {shape: rectangle}

forecasting_model -> forecasting_by_resource_type
forecasting_by_resource_type -> forecasting_thresholds
forecasting_thresholds -> capacity_report_template
capacity_report_template -> automation_monthly_report_script
automation_monthly_report_script -> verify
```

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Forecasting Model

**Pure FlashArray:**
```bash
purecli volume list --space   # per-volume capacity
purecli array get             # array-wide reduction ratio and used capacity
```


```text title="Expected output"
Name                          Size      Provisioned   Used       Data Reduction
vol-prod-db-01                2.0T      1.8T          892.3G     3.2:1
vol-prod-db-02                2.0T      1.9T          1.1T       2.8:1
vol-staging-app-01            500G      450G          234.5G     2.1:1
vol-dev-backup-01             1.0T      950G          567.8G     1.9:1
vol-archive-02                5.0T      4.2T          3.2T       1.5:1

Name          Model              Capacity      Used          Data Reduction
pure-array-1  FlashArray//X70-2  100.0T        67.4T         4.1:1
```

!!! warning "Common errors"
    **`Error: Connection refused (111)`** — Verify the Pure Storage array is reachable and purecli is configured with correct credentials via `purecli login`.
    **`Error: Invalid volume name or volume does not exist`** — Ensure the volume name is correct and exists on the array; use `purecli volume list` without filters to verify available volumes.
## Forecasting by Resource Type

### Storage

```bash
# Current usage and growth estimate
df -h /data
# Compare with last month's snapshot
# If usage grows 50 GB/month and 200 GB free → 4 months to full

# ONTAP aggregate capacity
storage aggregate show -fields size,used,percent-used,availsize
```


```text title="Expected output"
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       2.0T  1.6T  400G  80% /data

Name            Size       Used       Percent-Used  Availsize
aggr0           10.0TB     8.2TB      82%           1.8TB
aggr1           15.0TB     11.5TB     77%           3.5TB
aggr2           8.0TB      6.1TB      76%           1.9TB
aggr_ssd        5.0TB      4.3TB      86%           700GB
```

!!! warning "Common errors"
    **`df: '/data': No such file or directory`** — Verify the mount point exists and is mounted with `mount | grep /data`.
    **`Error: command not found: storage`** — Ensure you are connected to the ONTAP cluster via SSH or the NetApp CLI is installed and configured.
    **`permission denied`** — Run the commands with appropriate privileges (sudo for df, or ensure your ONTAP user has storage admin role).
### Compute (CPU/Memory)

```bash
# Average CPU over last 30 days from sar
for day in $(seq 1 30); do
  sar -u -f /var/log/sa/sa$(date -d "$day days ago" +%d) 2>/dev/null | \
    awk '/Average/ {print $3}' | tail -1
done | awk '{sum+=$1; count++} END {print "30d avg CPU:", sum/count "%"}'
```


```text title="Expected output"
30d avg CPU: 34.27 %
```

!!! warning "Common errors"
    **`sar: Cannot open /var/log/sa/sa01: No such file or directory`** — Enable sysstat collection with `systemctl enable sysstat && systemctl start sysstat`, then wait 24 hours for sa files to be generated.
    **`awk: syntax error: unexpected newline or EOF`** — Ensure the awk command is on a single line or properly escaped; the pipe chain may have been corrupted during copy-paste.
### Network

```bash
# Interface utilisation trend (sar)
sar -n DEV 1 10 | grep eth0
# Historical: sar -n DEV -f /var/log/sa/saDD
```


```text title="Expected output"
Linux 5.15.0-84-generic (aria-ops-vm01) 	01/15/2025 	_x86_64_	(8 CPU)

12:34:56 PM     IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s   %ifutil
12:34:57 PM      eth0    1247.00   892.00    156.32    124.78      0.00      0.00      0.00      2.14
12:34:58 PM      eth0    1156.00   945.00    142.15    118.64      0.00      0.00      0.00      1.98
12:34:59 PM      eth0    1389.00   1023.00   178.45    156.32      0.00      0.00      0.00      2.41
12:35:00 PM      eth0    1092.00   876.00    134.28    112.45      0.00      0.00      0.00      1.87
12:35:01 PM      eth0    1445.00   1156.00   189.67    167.89      0.00      0.00      0.00      2.63
Average:        eth0    1265.80    978.40    160.17    136.02      0.00      0.00      0.00      2.21
```

!!! warning "Common errors"
    **`Cannot open /var/log/sa/saDD: No such file or directory`** — Replace `DD` with the actual date (e.g., `sa15` for the 15th) or check that sysstat logs are enabled with `systemctl status sysstat`.
    **`command not found: sar`** — Install sysstat package with `apt-get install sysstat` (Debian/Ubuntu) or `yum install sysstat` (RHEL/CentOS).
## Forecasting Thresholds

| Resource | Alert at | Plan expansion at |
|---|---|---|
| Storage (array/volume) | 75% used | 60 days to full |
| CPU (sustained avg) | >70% | >60% sustained trend |
| Memory | >80% | >75% sustained trend |
| Network (sustained) | >60% of link speed | >50% sustained trend |
| Backup window | >90% of allowed window | 75% |

## Capacity Report Template

```markdown
Date:          2026-05-06
System:        prod-storage-01 (ONTAP)
Current Usage: 68% (34 TB / 50 TB)
Growth rate:   ~400 GB/month (3-month avg)
Days to 85%:   ~105 days (est. mid-August)
Days to 100%:  ~180 days (est. November)

Recommendation:
  Order 20 TB additional capacity by July.
  Submit hardware request by 2026-06-01 (6-week lead time).
```

## Automation — Monthly Report Script

```bash
#!/bin/bash
echo "=== Capacity Forecast $(date +%Y-%m-%d) ==="
df -h | awk 'NR>1 && $5+0 > 70 {print "WARNING:", $6, "at", $5}'
echo ""
echo "Storage volumes near capacity:"
# Add ONTAP/Pure/array CLI calls here for production use
```


```text title="Expected output"
=== Capacity Forecast 2024-01-15 ===
WARNING: /var/log at 78%
WARNING: /home at 82%
WARNING: /opt/vmware at 71%

Storage volumes near capacity:
```

!!! warning "Common errors"
    **`awk: syntax error in pattern near line 1`** — Ensure the script uses standard awk syntax; check for non-ASCII characters or shell encoding issues by running `file script.sh`.
    **`df: command not found`** — Verify `df` is available in the PATH by running `which df` or use the full path `/bin/df -h`.
---

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier

## See also

- [Alert Management](alert-management.md)
- [Aria Operations: Alert Definitions and Policies](alerts.md)
- [Aria Operations Backup & Restore](backup-restore.md)
- [Aria Operations — Operations](index.md)
- [Aria Operations — Architecture](../../architecture/)
- [Aria Operations — Deploy](../../deploy/)
- [Aria Operations — Security](../../security/)
- [Aria Operations — Troubleshooting](../../troubleshooting/)
