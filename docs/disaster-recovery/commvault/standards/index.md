# CommVault Standards

Storage policy names follow the convention `app-retention-tier` (e.g., `oracle-7yr-primary`, `vm-90d-secondary`) to make workload type, retention duration, and copy tier immediately identifiable. Subclient names should reflect the application and data scope (e.g., `oracle-prod-db01-full`). Schedule policies should be designed with a primary copy (disk/dedup) and a secondary copy (offsite or tape) in the same policy, so both copies are managed under one SLA. Deduplication databases must reside on SSD-backed storage with at least 20% free space headroom at all times.

| Retention Level | Copy Type | Retention |
|---|---|---|
| Daily | Primary (disk) | 14 days |
| Weekly | Primary (disk) | 8 weeks |
| Monthly | Secondary (offsite) | 12 months |
| Yearly | Secondary (tape/cloud) | 7 years |

- Encryption standard: AES-256 for any subclient covering PII or regulated data; cipher mode set at storage policy level.
- DDB placement: dedicated LUN on SSD; never co-locate DDB with backup data or OS.
- SLA plans in Command Center should be the single source of truth for all retention configurations in new deployments.
