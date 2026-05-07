# CommVault Lifecycle
## Release Cadence

CommVault releases Feature Releases (FRs) quarterly, each receiving Maintenance Releases (MRs/SPs) for approximately 12 months post-GA.

| Release Type | Cadence | Support Window |
|---|---|---|
| Feature Release (FR) | Quarterly | ~12 months of maintenance releases |
| Maintenance Release (MR) | As needed | Cumulative for the FR branch |
| Hotfix | On demand | Targeted; requires SR for delivery |

Check current version EOL: [documentation.commvault.com](https://documentation.commvault.com) → Product Lifecycle.

## Upgrade Order

**Critical: always upgrade CommServe first.**

1. **Pre-upgrade**: Back up CommServe SQL database manually
   ```powershell
   # CommVault console: Storage → System Backup → Run Now
   # Verify backup completes before proceeding
   ```

2. **Upgrade CommServe** — run installer on CommServe host; SQL DB upgraded automatically

3. **Upgrade MediaAgents** — via CommVault console: Infrastructure → MediaAgents → right-click → Update
   - MediaAgents can be upgraded rolling if multiple MediaAgents serve each storage pool

4. **Upgrade Clients** — deploy via client group push or individually
   - Clients one FR behind CommServe: supported
   - Clients two FRs behind CommServe: not supported — schedule urgent upgrade

## Pre-Upgrade Checklist

- [ ] All jobs complete or suspended (no active jobs on the CommServe)
- [ ] CommServe SQL database backup completed and verified
- [ ] Command Center configuration exported: Main Menu → Export Configuration
- [ ] Compatibility verified for all integrated systems (VMware, storage arrays)
- [ ] Windows Server and SQL Server patched to CommVault minimum requirements

## Post-Upgrade Validation

```powershell
# Check CommServe service status
Get-Service GxCVD, GxEvMgrS, GxShmServer | Select Name, Status

# Verify MediaAgent connectivity
qoperation execute -af UpdateMediaAgent.xml   # or use console check

# Run a test backup after upgrade
# Select a non-critical VM → right-click → Back Up Now
```

Verify in Command Center: Jobs → Active Jobs — confirm no jobs stuck in queued state.

## CommVault to Metallic SaaS Migration

For cloud migration of on-premises CommVault to Metallic (SaaS):
1. Deploy Metallic Gateway appliance or Cloud Connector
2. Re-register existing clients to Metallic CommCell
3. Initial full backup to Metallic; daily incrementals going forward
4. Decommission on-premises CommServe after retention requirements satisfied

## EOL Tracking

| Item | Action |
|---|---|
| FR version | Alert when within 60 days of EOL; upgrade planning starts 90 days before |
| Windows Server OS (CommServe host) | Align CommServe OS lifecycle with CommVault support matrix |
| SQL Server (CommServe DB) | Track SQL Server EOL; upgrade requires CommVault testing |
| Hyperscale X firmware | Annual review against CommVault recommended firmware versions |
