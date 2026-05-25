# RecoverPoint — Escalation

> Part of the [RecoverPoint](../../index.md) > [Troubleshooting](../index.md) reference.

---

Dell support for RecoverPoint is accessed via support.dell.com, with service requests opened against the RPA cluster serial number or site license. Before opening an SR, collect the RecoverPoint support bundle from the CLI using `get support_bundle` on each RPA, as well as the full cluster state from the management console. Provide RPA software versions for both Site A and Site B, the total consistency group count, per-CG journal sizes, and the replication link state at the time of the issue.

- **Support portal:** [support.dell.com](https://support.dell.com) — select RecoverPoint product line
- **SR creation:** Use RPA cluster serial number; specify site A and site B versions
- **Log collection:**
  ```
  get support_bundle
  ```
  Run on each RPA; bundle includes system logs, CG state, journal metadata, and link statistics
- **Required information for SR:**
  - RPA software version (Site A and Site B)
  - Number of consistency groups and volumes
  - Journal volume sizes and current utilization
  - Replication link state and lag at time of incident
  - Management console screenshot of affected CGs
- **Compatibility matrix:** RecoverPoint compatibility matrix available on Dell's support site under RecoverPoint documentation
- **Escalation:** Request Engineering Escalation in the SR for production-down or data-loss risk scenarios
