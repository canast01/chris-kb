# CyberArk — Health Checks


<div class="kb-summary">
Daily operations focus on confirming that the Vault service is running, CPM is successfully rotating passwords, PSM is brokering sessions without errors, and no critical accounts are in a failed rotation state.
</div>

 Check the PVWA dashboard for failed rotation jobs (red accounts), CPM heartbeat status, and DR replication lag each morning. Weekly, review session recording storage capacity to ensure sufficient space for recordings retention.

## Daily Checks

- Vault service health: confirm `PrivateArk Server` service is running on primary and DR
- CPM heartbeat: PVWA → Administration → System Health → CPM status green
- PSM health: PVWA → Administration → System Health → PSM status green
- Failed rotation jobs: PVWA → Accounts → filter by "Rotation failed" status
- DR Vault replication: confirm `replication lag = 0` in Vault DR dashboard
- Safe utilisation: flag safes approaching 10,000 object limit

## Weekly Checks

- Session recording storage capacity (target: >30% free)
- Review new safe creation requests against naming standards
- Confirm CPM platform configurations are up to date
- Audit users with "Vault Admin" role for any additions
