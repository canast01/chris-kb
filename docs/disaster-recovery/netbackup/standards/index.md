# NetBackup Standards

Policy names follow the convention `app-os-frequency` (e.g., `oracle-linux-daily`, `mssql-win-weekly`) to make workload, platform, and schedule immediately identifiable. Schedule names append the retention level (e.g., `daily-14d`, `weekly-8w`) so retention intent is visible without opening the policy. Client-side or media-server-side encryption is mandatory for policies covering PII or regulated data. Catalog backups must run daily to a dedicated storage unit separate from standard backup targets.

| Retention Level | Schedule Type | Retention Period |
|---|---|---|
| Daily | Full or Incremental | 14 days |
| Weekly | Full | 8 weeks |
| Monthly | Full | 12 months |
| Yearly | Full | 7 years |

- Multiplexing limit: maximum 8 jobs per drive to avoid excessive fragmentation during restores.
- All policies require an explicitly named client list — wildcard client lists are not permitted in production.
