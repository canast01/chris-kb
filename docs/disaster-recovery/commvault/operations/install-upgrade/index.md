# Commvault — Install & Upgrade

## Release Cadence

CommVault releases Feature Releases (FRs) quarterly, each receiving Maintenance Releases (MRs/SPs) for approximately 12 months post-GA.

| Release Type | Cadence | Support Window |
|---|---|---|
| Feature Release (FR) | Quarterly | ~12 months of maintenance releases |
| Maintenance Release (MR) | As needed | Cumulative for the FR branch |
| Hotfix | On demand | Targeted; requires SR for delivery |

Check current version EOL: [documentation.commvault.com](https://documentation.commvault.com) → Product Lifecycle.

## Upgrade Order

### CommVault Upgrade Dependency Chain

```mermaid
flowchart TD
    start(["Start upgrade window"])
    start --> backup["Back up CommServe SQL DB\nverify backup completes"]
    backup --> dbCheck{"DB backup\ncomplete?"}
    dbCheck -->|No| halt["STOP — do not proceed\nuntil backup confirmed"]
    dbCheck -->|Yes| csUpgrade["Upgrade CommServe\nSQL DB upgraded automatically"]
    csUpgrade --> maUpgrade["Upgrade MediaAgents\nrolling — one pool at a time"]
    maUpgrade --> clientUpgrade["Upgrade Clients\npush via client group or individual"]
    clientUpgrade --> validate["Validate:\n- All services running\n- No jobs queued/failed\n- Test backup on non-critical client"]
    validate --> done(["Upgrade complete"])

    classDef action fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef decision fill:#b45309,stroke:#92400e,color:#fff
    classDef terminal fill:#15803d,stroke:#166534,color:#fff
    classDef warn fill:#be123c,stroke:#9f1239,color:#fff
    class backup,csUpgrade,maUpgrade,clientUpgrade,validate action
    class dbCheck decision
    class start,done terminal
    class halt warn
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
