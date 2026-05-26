# NetBackup — Install & Upgrade

## Release Cadence

Veritas releases NetBackup on a major.minor cadence, with Long-Term Support (LTS) releases receiving maintenance updates for three years post-GA.

| Version | Type | EOS (check Veritas SORT) |
|---|---|---|
| 10.x | LTS | Check SORT tool |
| 9.1.x | Standard | Check SORT tool |
| 8.3.x | LTS (older) | Likely at or near EOL — review |

Check lifecycle dates at: [sort.veritas.com](https://sort.veritas.com) → EOL dates.

## Upgrade Order

### Upgrade Dependency Chain

```mermaid
flowchart TD
    start(["Start upgrade window"])
    start --> catBackup["Force catalog backup\nbpbackup -i -h <master> -p NBU_Catalog_Backup\nVerify completion"]
    catBackup --> catOK{"Catalog backup\ncomplete?"}
    catOK -->|No| halt["STOP — catalog must be\nbacked up before proceeding"]
    catOK -->|Yes| eebReview["Review EEB register\nNote which EEBs\nsuperseded by this upgrade"]
    eebReview --> masterUpgrade["Upgrade Primary Server\nAll media servers can still backup\nduring master upgrade (N-1 supported)"]
    masterUpgrade --> masterVerify["bpclntcmd -self\nVerify master server version"]
    masterVerify --> mediaUpgrade["Upgrade Media Servers\none at a time\nbpclntcmd -hn <ms> -chk after each"]
    mediaUpgrade --> clientUpgrade["Upgrade Clients\npush from Admin Console\nor manual per client"]
    clientUpgrade --> postValid["Post-upgrade validation:\nbpdbm -consistency_check\nbpbackup test run"]
    postValid --> done(["Upgrade complete"])

    classDef action fill:#2563eb,stroke:#1d4ed8,color:#fff
    classDef decision fill:#b45309,stroke:#92400e,color:#fff
    classDef warn fill:#be123c,stroke:#9f1239,color:#fff
    classDef terminal fill:#15803d,stroke:#166534,color:#fff
    class catBackup,eebReview,masterUpgrade,masterVerify,mediaUpgrade,clientUpgrade,postValid action
    class catOK decision
    class halt warn
    class start,done terminal
```
```

## Migration: Physical Master to Appliance

Migrating from physical NetBackup installation to a NetBackup appliance requires catalog migration — do NOT upgrade and migrate in the same maintenance window:

1. Deploy appliance with matching NetBackup version
2. Migrate catalog: run `nbcatutil` to export and import catalog
3. Redirect media servers to new master
4. Decommission old master only after 24-48 hours validation

## License Lifecycle

Track license types:
- **APTARE/IT Analytics licenses**: annual subscription
- **Capacity-based licensing**: TB under management; audit monthly
- **Veritas support contract**: align renewal with SORT lifecycle dates
