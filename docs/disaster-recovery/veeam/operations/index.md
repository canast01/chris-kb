# Veeam Operations

Daily operations centre on reviewing the Veeam Backup & Replication console Home view, which summarises job counts by status (Success, Warning, Failed, Running). Failed jobs should be investigated immediately — right-click the job and select "Statistics" to see the task-level error. Warning-state jobs often indicate a VM snapshot commit delay or a VSS quiesce issue and should not be left unresolved as they can escalate to failures. Verify SOBR capacity and confirm no extent is in a sealed or unavailable state.

**Daily Checklist**

- [ ] Console Home view — review Success / Warning / Failed counts
- [ ] Investigate all Failed jobs (Statistics > Error message)
- [ ] Review Warning jobs — identify and document root cause
- [ ] `Get-VBRRepository | Select Name, FreeSpace, TotalSpace` — capacity check
- [ ] SOBR Health: verify no extent is in Sealed or Unavailable state
- [ ] Active sessions — confirm no jobs are stuck (running >2x normal duration)
- [ ] Tape (if applicable) — confirm eject schedule ran and tapes are offsite

**Weekly**

- Run SureBackup verification job for critical VM groups
- Review Backup Copy job status — confirm off-site restore points are current
- Generate Veeam ONE report for job success rate and capacity trend
