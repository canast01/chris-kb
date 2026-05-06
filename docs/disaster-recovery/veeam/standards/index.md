# Veeam Standards

Job names follow the convention `env-workload-type` (e.g., `prod-vm-daily`, `dr-fileserver-weekly`, `dev-vm-backup`) to make environment, workload class, and job type immediately clear in the console. Backup windows are scheduled during off-peak hours (22:00–06:00 by default) with a hard stop configured to prevent overlap with the next window. Encryption is mandatory for all jobs writing to cloud repositories or off-site backup copy targets; AES-256 with keys stored in the Veeam configuration database (backed up separately) is the standard. Instant VM Recovery RTO targets must be agreed per application tier and documented in the DR plan.

| Retention Level | Type | Retention |
|---|---|---|
| Daily | Incremental | 14 restore points |
| Weekly | Full (synthetic) | 8 restore points |
| Monthly | Full (active) | 12 restore points |
| Yearly | Full (active) | 7 restore points |

- Repository target: primary repo on fast disk (performance tier); capacity tier offload to object storage after 14 days.
- Encryption key management: keys must be exported and stored in a secure vault (CyberArk or offline safe) — loss of key means loss of backup data.
