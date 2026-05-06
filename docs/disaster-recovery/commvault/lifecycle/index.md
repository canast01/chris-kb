# CommVault Lifecycle

CommVault releases Feature Releases (FRs) on a quarterly cadence, each receiving maintenance releases (Service Packs) for approximately 12 months post-GA. The CommServe must always be upgraded before MediaAgents and Clients, and the CommServe database (SQL Server) is upgraded automatically as part of the CommServe installer — a pre-upgrade CommServe DB backup is mandatory. One FR behind is supported for MediaAgents and Clients; two FRs behind is not supported and will generate console warnings.

| Release Type | Cadence | Support Window |
|---|---|---|
| Feature Release (FR) | Quarterly | ~12 months of maintenance releases |
| Maintenance Release (MR) | As needed | Cumulative for the FR branch |
| Hotfix | On demand | Targeted; requires SR for delivery |

- CommServe DB upgrade is automatic during CommServe upgrade; ensure SQL Server SA credentials are available.
- Metallic SaaS migration: CommVault provides migration tooling from on-premises CommServe to Metallic; plan for client agent re-registration.
- EOL tracking: check CommVault End-of-Life information at documentation.commvault.com; alert when any FR in use is within 60 days of EOL.
- Upgrade window: schedule CommServe upgrade during a low-backup window; MediaAgent upgrades can be rolling if redundant MediaAgents exist for each storage pool.
