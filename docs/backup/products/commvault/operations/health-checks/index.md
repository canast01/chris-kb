---
tags:
  - commvault
  - operations
description: "Health Checks reference covering Daily Checklist, Weekly Checks."
---
# Commvault — Health Checks

<div class="kb-summary">
Health Checks reference covering Daily Checklist, Weekly Checks.

*Applies to: Commvault 2024.x*
</div>

```d2
direction: right

begin_checks: "Begin Checks" {shape: oval}
run_this_routine: "Run This Routine" {shape: rectangle}
daily_checklist: "Daily Checklist" {shape: rectangle}
weekly_checks: "Weekly Checks" {shape: rectangle}
verify: "Verify" {shape: rectangle}
generate_report: "Generate Report" {shape: oval}

begin_checks -> run_this_routine
run_this_routine -> daily_checklist
daily_checklist -> weekly_checks
weekly_checks -> verify
verify -> generate_report
```

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

Run these steps each morning for a complete CommVault CommServe health snapshot.

1. **CommServe services** — confirm core services are running:
   - Linux: `commvault list`
   - Windows: `net start | findstr /i "commvault"`
2. **Job activity summary** — CommCell Console → Job Controller → count Active / Waiting / Pending jobs; investigate any unexpected Pending or Waiting queue build-up.
3. **Alert console** — CommCell Console → Alerts → review all open Critical and High alerts; acknowledge resolved ones and action any new ones.
4. **MediaAgent connectivity** — verify all MAs show Ready status:
   ```bash
   qoperation execscript -sn GetMediaAgentStatus.sql
   ```
   Or check MA status directly in CommCell Console → MediaAgents.
5. **Library and drive status** — CommCell Console → Storage Resources → Libraries → confirm all drives show Online; investigate any Offline or Error state.
6. **Storage policy RPO compliance** — CommCell Console → Storage Policies → review last backup completion time per policy; flag any policy that has not completed within its RPO window.
7. **Failed jobs (last 24 h)** — CommCell Console → Reports → Backup Job Summary → filter Last 24 h + Failed; document each failure with error code and next action.
8. **CommServe disk space** — check host disk usage on the CommServe server:
   - Windows: `C:\Program Files\CommVault\ContentStore` — alert if >80 % used
   - Linux: `/opt/commvault/` — alert if >80 % used
9. **Client connectivity** — count offline clients:
   ```bash
   qinfo -info clientlist
   ```
   Or CommCell Console → Clients → filter for Offline; investigate any unexpected offline client.
10. **License usage** — CommCell Console → Control Panel → License Administration → confirm licence capacity is not exceeded and no component licences are expired.

Daily CommVault operations begin in the Job Controller (Command Center or Java GUI) to review all jobs from the previous 24 hours. Failed jobs display a status code — hovering reveals a description, and the job detail view shows phase-level failure logs. MediaAgent connectivity status and library health (if tape is in use) must be checked each morning, as a downed MediaAgent silently prevents any job targeting its storage pools from running. DDB space must be monitored closely; a full DDB causes all deduplication-enabled jobs to fail.

## Daily Checklist

- [ ] Job Controller — review all Failed and Pending jobs from last 24 hours
- [ ] Alert Console — clear or acknowledge resolved alerts; investigate new ones
- [ ] MediaAgent status — all MediaAgents online and communicating with CommServe
- [ ] Library status (if tape) — all drives online; no media errors
- [ ] DDB space — `qlist ddb` or Command Center Storage > Deduplication; alert if <20% free
- [ ] CommServe DB backup — confirm it completed last night

## Weekly Checks

- Verify auxiliary copy jobs ran successfully for all secondary copy pools
- Review SLA reports in Command Center — identify any clients below SLA threshold
- Run DDB verification on any DDB that has not been verified in the last 7 days

---

## Verify

- **Job status:** confirm backup job completed with status Success (not Warning)
- **Recovery test:** restore a single file or VM from the new backup to confirm restorability
- **Retention:** verify old recovery points are expiring per the configured retention policy

---

## See also

- [Commvault — Procedures](../procedures/)
- [Commvault — CLI Reference](../cli-reference/)
- [Commvault — Common Issues](../../troubleshooting/common-issues/)
