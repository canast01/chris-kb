# SRM Standards

Protection groups follow the naming convention `PG-<tier>-<site-pair>` (e.g., `PG-DB-DC1DC2`) and are scoped to a single application tier per group to enable independent failover. Recovery plans are named `RP-<priority>-<tier>-<site-pair>` and tiered by business priority (P1 critical, P2 standard, P3 batch). Test failovers must be executed at minimum quarterly and results documented in the change record system.

| Standard | Value |
|---|---|
| Protection group naming | `PG-<tier>-<site-pair>` |
| Recovery plan naming | `RP-<priority>-<tier>-<site-pair>` |
| Test failover frequency | Quarterly minimum |
| RPO target — Tier 1 | 0 (SRDF/S) |
| RPO target — Tier 2 | ≤30 min (SRDF/A or vSphere Replication) |
| IP customisation | Mandatory; define per-VM network mapping rules |
| Datastore mapping | Pre-validated; source ↔ recovery datastore pairs documented |
