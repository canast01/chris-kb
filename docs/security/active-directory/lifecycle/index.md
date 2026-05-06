# Active Directory Lifecycle

Active Directory domain and forest functional levels determine which features are available and which DC OS versions are supported; raising functional levels is a one-way operation and requires all DCs to run at least the corresponding Windows Server version. SYSVOL replication must be migrated from the legacy FRS mechanism to DFSR before the domain functional level can be raised to Windows Server 2008 R2 or higher. The DC retirement procedure involves transferring or seizing FSMO roles, demoting via `dcpromo` or `Uninstall-ADDSDomainController`, and removing metadata with `ntdsutil` for force-demoted DCs.

| Domain Functional Level | Minimum DC OS | Key Feature Unlocked |
|---|---|---|
| Windows Server 2016 | Server 2016 | Privileged Access Management, PAC compression |
| Windows Server 2019 | Server 2019 | n/a (feature parity) |
| Windows Server 2022 | Server 2022 | AES encryption improvements |
| SYSVOL migration | N/A | FRS → DFSR via `dfsrmig` |
| AD Recycle Bin | DFL 2008 R2+ | Object restore without authoritative restore |
