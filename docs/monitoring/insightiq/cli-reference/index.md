# InsightIQ CLI Reference

InsightIQ provides a CLI on the appliance for cluster management and data export. OneFS CLI commands are used on the PowerScale cluster itself for correlated performance data when deeper investigation is needed.

**InsightIQ Appliance CLI**

```bash
# List all monitored clusters
iiq cluster list

# Add a new cluster connection
iiq cluster add --host <cluster-mgmt-ip> --user svc-insightiq

# Export performance data to CSV
iiq export --cluster <cluster-name> --start 2024-01-01 --end 2024-01-07 --output /tmp/export.csv
```

**OneFS CLI — Correlated Performance Commands**

```bash
# Real-time statistics summary
isi statistics summary

# Protocol-level performance breakdown
isi statistics protocol --nodes all

# Active client connections
isi statistics client list

# Job engine status (check for background load)
isi job list

# Drive and node performance
isi performance
```
