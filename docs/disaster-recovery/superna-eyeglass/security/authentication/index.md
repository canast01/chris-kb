# Superna Eyeglass — Authentication

Eyeglass admin access is controlled through built-in roles: **admin** (full access including failover initiation) and **read-only** (dashboard and reporting access only).

| Role | Access Level |
|---|---|
| admin | Full access including failover initiation and configuration changes |
| read-only | Dashboard and reporting access only |

Enforce least privilege — assign read-only to personnel who only require visibility into DR state without the ability to trigger failover actions.

OneFS API credentials stored in Eyeglass for cluster connectivity should use dedicated service accounts with the minimum required OneFS privileges. See the [Integrations](../../architecture/integrations/) page for the required PowerScale role configuration.
