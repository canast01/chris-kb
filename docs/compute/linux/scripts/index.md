# Linux Scripts

Automation scripts provide consistent, repeatable execution of common operational tasks. All scripts are stored in the team's Ansible/scripts repository and are reviewed before deployment. Scripts are designed to be idempotent and safe to run on production systems. Output is logged to `/var/log/ops/` on each host and forwarded to the central logging platform.

| Script | Purpose |
|---|---|
| `system-health-check.sh` | Checks disk usage, memory, load, and failed services; outputs a summary report |
| `log-archival.sh` | Compresses and archives rotated logs older than 30 days to NFS archive path |
| `patch-status-report.sh` | Lists available updates and last patch date via `dnf`/`apt` |
| `user-audit.sh` | Reports all local users, sudo group members, and last login dates |
| `disk-alert.sh` | Sends alert if any filesystem exceeds configured threshold (default 80%) |
