# SRDF/S — Scripts

> Part of the [SRDF/S Operations](../index.md) reference.

Automation scripts for SRDF/S use Solutions Enabler SYMCLI via shell or the Solutions Enabler REST API via Python. All scripts should be run from a dedicated automation host with read-only credentials for health checks and elevated credentials for failover operations. Failover scripts must include pre-flight validation (pair state, site connectivity) and post-failover confirmation (R2 volumes writable, host I/O resuming).

---

## Available Scripts

| Script | Language | Purpose |
|---|---|---|
| `srdf_s_state_check.sh` | Bash | Poll all SRDF/S groups and report non-Synchronized pairs |
| `srdf_s_failover.sh` | Bash | Automated failover with pre/post validation gates |
| `srdf_s_health_report.py` | Python | Daily replication health report via SE REST API |
| `srdf_s_latency_check.sh` | Bash | Check site RTT and alert if ≥4ms (warning) or ≥5ms (critical) |

---

## Script Pattern — State Check

```bash
symrdf query -g ${RDFG} | grep -v "Synchronized" | grep -v "^$" && \
  echo "ALERT: Non-synchronized pairs detected" || echo "OK: All pairs synchronized"
```
