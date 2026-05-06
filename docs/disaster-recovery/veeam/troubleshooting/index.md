# Veeam Troubleshooting

Most Veeam job failures fall into a small set of categories: VMware snapshot issues, repository space problems, proxy connectivity timeouts, and Veeam service instability. The first step for any failure is to open the job statistics view in the console — the task-level error message and reason field usually point to the root cause without needing to open log files. Veeam logs are written to `C:\ProgramData\Veeam\Backup\` on the Backup Server and `C:\ProgramData\Veeam\Backup\` (or Linux equivalent) on proxies.

| Symptom | Likely Cause | Remediation |
|---|---|---|
| Job fails at "Creating snapshot" | VMware snapshot quiesce failure | Check VMware Tools version; disable application-aware processing temporarily to isolate |
| Job fails at "Committing snapshot" | VMware snapshot stuck | Remove stale snapshots via vCenter; check vSphere task log |
| Repository out of space | SOBR capacity tier offload not running | Check capacity tier offload policy; manually trigger offload |
| Proxy timeout | Network congestion or proxy resource exhaustion | Increase proxy task timeout; check proxy CPU/RAM; add proxy |
| VBR service crash | Software bug or corrupt config DB | Check Windows Event Log (Application); review `C:\ProgramData\Veeam\Backup\Svc.VeeamBackup.log` |
| Backup copy job never completes | WAN link saturation or copy target unavailable | Check WAN Accelerator stats; verify target repo reachability |
| SureBackup fails | Lab network misconfiguration | Check virtual lab network mapping; verify test credentials |

**Key log locations**

- VBR service log: `C:\ProgramData\Veeam\Backup\Svc.VeeamBackup.log`
- Job session logs: `C:\ProgramData\Veeam\Backup\Job_<JobName>\`
- Proxy logs: `C:\ProgramData\Veeam\Backup\` on each proxy server
