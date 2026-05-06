# Superna Eyeglass Security

Eyeglass admin access is controlled through built-in roles: admin (full access including failover initiation) and read-only (dashboard and reporting access only). The Eyeglass management console must be accessible only via HTTPS — HTTP access should be disabled or redirected. API tokens used by automation scripts must be stored in a secrets manager and rotated on a defined schedule.

All failover events are recorded in the Eyeglass audit log, which should be forwarded to a SIEM. Network access to the Eyeglass management interface should be restricted to the management VLAN or jump host only. OneFS API credentials stored in Eyeglass for cluster connectivity should use dedicated service accounts with minimum required privileges.

| Control | Detail |
|---|---|
| RBAC | Admin and read-only roles; enforce least privilege |
| Console access | HTTPS only; restrict to management VLAN or jump host |
| API token management | Store in secrets manager; rotate on schedule and on personnel change |
| Audit log | All failover and configuration events logged; forward to SIEM |
| Network access | Restrict Eyeglass UI and API to management network |
| OneFS API credentials | Dedicated service account; minimum required OneFS privileges |
| Appliance hardening | Disable unused services; keep appliance patched to current release |
