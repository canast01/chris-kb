---
tags:
  - pure
---
# Pure Storage Evergreen Integration

<div class="kb-summary">
Pure Storage Evergreen Integration reference covering Pure1 Integration, True Forward Capacity Upgrades, VMware Integration, Backup Integration, REST API.

*Applies to: Evergreen*
</div>

![Pure Storage Evergreen Integration — Diagram](../../../../../assets/storage-pure-evergreen-integration-diagram.svg)

## Pure1 Integration

All Evergreen subscriptions are managed through the Pure1 cloud management platform (https://pure1.purestorage.com). Pure1 provides:

- **Capacity management** — used vs. entitled capacity across all arrays in the subscription; capacity trend forecasting and anomaly detection
- **Health monitoring** — real-time array health score, hardware status, and alert history for every array in the fleet
- **Lifecycle tracking** — controller generation, subscription renewal dates, Ever Modern eligibility, and upgrade readiness reports
- **Phonehome telemetry** — continuous encrypted telemetry from each array to Pure1 over port 443; used by Pure Support for proactive health monitoring and automatic case creation on hardware faults

Ensure port 443 outbound is permitted from each array's management interface to Pure1 endpoints. If a proxy is required, configure the proxy in the array management settings. Phonehome must remain active at all times for the subscription SLA and Ever Modern guarantee to apply.

## True Forward Capacity Upgrades

Evergreen includes a **True Forward** capacity model: if actual consumed capacity exceeds the contracted entitlement at the annual review, Pure upgrades the subscription to match actual usage at the current subscription price — customers are never charged retroactively for overages.

To request a capacity increase:

1. Log into Pure1 and review the current consumed vs. entitled capacity
2. Submit a capacity expansion request through the Pure1 portal or via the Pure account team
3. Pure provisions additional capacity without hardware change (for in-range additions) or schedules a drive shelf addition

True Forward reviews are conducted annually; engage the Pure account team at least 60 days before the review date to prepare consumption data and budget alignment.

## VMware Integration

| Integration | Description |
|---|---|
| vSphere Plugin for Pure Storage | GUI integration for volume management directly from vCenter; browse, create, and resize datastores without leaving vSphere |
| VASA Provider | Enables vVols (Virtual Volumes) on FlashArray; per-VM storage policy management via vSphere Storage Policy Based Management (SPBM) |
| vSphere API for Array Integration (VAAI) | Offloads VMFS clone, zeroing, and locking operations to FlashArray hardware; reduces ESXi host CPU load |
| VMware Site Recovery Manager (SRM) | FlashArray Storage Replication Adapter (SRA) enables SRM-orchestrated DR failover using FlashArray async replication |

Install the Pure Storage vSphere Plugin from the VMware Marketplace. VASA Provider is included in the plugin.

## Backup Integration

| Tool | Integration Method |
|---|---|
| Veeam Backup & Replication | Veeam Storage Integration API (VDAP) — Veeam orchestrates FlashArray snapshots for application-consistent backup; supports instant VM recovery from FlashArray snapshots |
| Commvault | IntelliSnap snapshot integration; array-level snapshots taken by Commvault before streaming to media |
| Veritas NetBackup | FlexSnapshot integration for array-level snapshots coordinated with NetBackup job schedules |
| Rubrik / Cohesity | Native FlashArray REST API integration for snapshot-based protection and cataloguing |

For all backup integrations, ensure the backup tool's service account is assigned the `storage_admin` role in Purity — it requires snapshot creation and deletion permissions but does not need `array_admin`.

## REST API

FlashArray exposes a versioned REST API for automation and integration:

- **Base URL**: `https://<array-management-ip>/api/<version>/`
- **Current API version**: check `https://<array>/api/api_version` for supported versions
- **Authentication**: Bearer token — obtain a token with a POST to `/api/<version>/auth/session` using array credentials, or generate a long-lived API token in the Purity GUI under **Settings > Users > API Tokens**

```bash
# Get an API token via CLI
pureuser apitoken create <username>

# List existing API tokens
pureuser apitoken list

# Example: list volumes via REST API (curl)
curl -s -H "Authorization: Bearer <token>" \
  https://<array>/api/2.x/volumes | jq .
```


```text title="Expected output"
# Get an API token via CLI
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcwOTMxMjAwMH0.abc123def456

# List existing API tokens
Name                          Created                  Expires                  
admin-token-prod              2024-02-15T10:22:33Z     2025-02-15T10:22:33Z     
backup-service-token         2024-01-20T14:55:12Z     2025-01-20T14:55:12Z     
monitoring-api-token         2024-02-01T09:18:45Z     2025-02-01T09:18:45Z     

# Example: list volumes via REST API (curl)
{
  "items": [
    {
      "name": "prod-db-vol-01",
      "size": 1099511627776,
      "provisioned": 1099511627776,
      "serial": "ABC123DEF456GHI789"
    },
    {
      "name": "backup-vol-02",
      "size": 2199023255552,
      "provisioned": 2199023255552,
      "serial": "XYZ789ABC123DEF456"
    }
  ],
  "continuation_token": null
}
```

!!! warning "Common errors"
    **`error: invalid credentials for user '<username>'`** — Verify the username exists and you have sufficient permissions to create API tokens.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command or configure proper certificate validation for your array's HTTPS endpoint.
The REST API supports all array operations available in the GUI and CLI. Use API version 2.x for new integrations — version 1.x is deprecated. Pure1 also provides a fleet-level REST API for subscription and capacity data.
