# NetBackup Lifecycle

Veritas follows a major.minor release cadence for NetBackup, with Long-Term Support (LTS) releases receiving maintenance updates for three years post-GA. Upgrade order is strictly enforced: Master Server first, then Media Servers, then Clients — clients one version behind the master are supported but should be brought current within one maintenance cycle. Emergency Engineering Binaries (EEBs) must be tracked in a register alongside the version they target, as EEBs are superseded by the next maintenance release and must be re-validated after each upgrade.

| Version | Type | EOS Date |
|---|---|---|
| 10.x | LTS | Check Veritas SORT |
| 9.1.x | Standard | Check Veritas SORT |
| 8.3.x | LTS (older) | Review for EOL |

- NetBackup IT Analytics replaces OpsCenter for telemetry and reporting in newer deployments.
- Client version compatibility: one major version behind master is supported; two versions behind requires immediate upgrade planning.
- Migration from physical master to appliance (or vice versa) requires catalog migration procedure — do not upgrade and migrate simultaneously.
