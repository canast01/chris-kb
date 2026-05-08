# Superna Eyeglass — Access Control

Network access to the Eyeglass management interface must be restricted to the management VLAN or jump host only. Direct access from user workstations or untrusted networks is not permitted.

| Control | Detail |
|---|---|
| Network access | Restrict Eyeglass UI and API to management network |
| Console access | HTTPS only; restrict to management VLAN or jump host |
| OneFS API credentials | Dedicated service account; minimum required OneFS privileges |
| RBAC | Admin and read-only roles; enforce least privilege |

All failover events are recorded in the Eyeglass audit log. The audit log must be forwarded to a SIEM to ensure a complete record of all failover and configuration events is retained outside the appliance.
