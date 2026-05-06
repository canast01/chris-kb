# SyncIQ — Replication

> Part of the Dell PowerScale (Isilon) CLI Reference.

---

```bash
# List policies
isi sync policies list
isi sync policies view <policy_name>

# Create policy
isi sync policies create --name <policy_name> --action sync --source-root-path /ifs/<src> --target-host <ip> --target-path /ifs/<dst>

# Run / pause / cancel
isi sync jobs list
isi sync jobs start <policy_name>
isi sync jobs pause <policy_name>
isi sync jobs cancel <policy_name>

# View job progress
isi sync jobs view <job_id>

# Reports
isi sync reports list
isi sync reports view <report_id>

# Performance rules
isi sync rules list
isi sync rules create bandwidth --limit <kbps> --schedule always

# Failover / failback
isi sync policies disable <policy_name>
isi sync recover policies list
```
