# Commvault — Health Checks

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
