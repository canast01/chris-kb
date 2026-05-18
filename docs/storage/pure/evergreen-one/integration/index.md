# Pure Storage Evergreen//One Integration

```
  Evergreen//One Integration Landscape

  ┌───────────────┐   phonehome    ┌────────────────────┐
  │  FlashArray / │──HTTPS 443────►│  Pure1 Portal      │
  │  FlashBlade   │◄───────────────│  SLA / Capacity /  │
  │  (Pure-owned) │  telemetry     │  Health / Alerts   │
  └───────┬───────┘                └────────┬───────────┘
          │                                 │ REST API
          │ FC/iSCSI/NVMe/NFS               ▼
          ▼                        ┌────────────────────┐
  ┌───────────────┐                │  FinOps / CMDB /   │
  │  vSphere /    │◄── VASA/VAAI   │  Billing systems   │
  │  ESXi hosts   │                └────────────────────┘
  └───────┬───────┘
          │ SRM / vVols
          ▼
  ┌───────────────┐                ┌────────────────────┐
  │  VMware SRM   │                │  Backup tools      │
  │  (DR orchestr)│                │  Veeam / Commvault │
  └───────────────┘                │  Rubrik / NetBackup│
                                   └────────────────────┘
  Snapshot capacity counts toward monthly consumption total
```

## Pure1 Integration

Pure1 (https://pure1.purestorage.com) is the central management and reporting platform for all Evergreen//One deployments. Unlike standard Evergreen where Pure1 is a monitoring complement to local array management, for Evergreen//One Pure1 is the primary operational interface for the customer. All capacity reporting, SLA compliance tracking, billing data, and lifecycle management flow through Pure1.

Key Pure1 capabilities for Evergreen//One:

- **Consumption dashboard** — real-time view of consumed vs. committed reserve vs. burst capacity; daily and monthly trend graphs
- **SLA compliance reports** — availability and performance SLA event history; breach events, credit status, and resolution notes
- **Capacity forecasting** — AIOps-driven capacity growth projection to support committed reserve adjustment ahead of growth
- **Health monitoring** — array health score, open alerts, and hardware status for all arrays in the service
- **Lifecycle tracking** — controller generation, Purity version (Pure-managed), and scheduled upgrade notifications

Phonehome telemetry from each array to Pure1 runs over outbound HTTPS port 443. This must remain active at all times — Pure's SLA monitoring, proactive maintenance, and automatic case creation all depend on continuous phonehome connectivity. If a proxy is required, configure it in the array management GUI and test connectivity after any network change.

## Capacity True-Up Integration with Finance

For monthly billing reconciliation:

1. Export the Pure1 monthly consumption report (Pure1 > Evergreen//One > Consumption > Export)
2. Compare consumed TiB against the committed reserve and identify burst usage days
3. Reconcile against the Pure invoice — burst charges should match daily burst readings in the report
4. Share the report with the finance team before invoice approval

Automate consumption report retrieval using the Pure1 REST API to integrate with internal billing or FinOps platforms:

- Pure1 API base: `https://api.pure1.purestorage.com/api/1.x/`
- Authentication: API key generated in Pure1 portal > Account > API Registration
- Relevant endpoints: `/arrays`, `/metrics`, `/subscriptions`

## VMware Integration

Evergreen//One deployments support the same VMware integrations as standard FlashArray and FlashBlade:

| Integration | Description |
|---|---|
| vSphere Plugin for Pure Storage | Volume and datastore management from vCenter GUI |
| VASA Provider | vVols support with per-VM storage policy management via SPBM |
| VAAI | Hardware offload for VMFS clone, zeroing, and ATS operations |
| VMware Site Recovery Manager (SRM) | SRA for DR orchestration using FlashArray async replication |

Install from the VMware Marketplace. Pure Support can assist with initial installation and configuration as part of the service onboarding.

## Backup Integration

Backup tool integration for Evergreen//One is identical to standard FlashArray and FlashBlade deployments. The backup tool's service account requires `storage_admin` role in Purity.

| Tool | Integration Method |
|---|---|
| Veeam Backup & Replication | Veeam Storage Integration API (VDAP) — snapshot-based backup and instant recovery |
| Commvault | IntelliSnap snapshot integration |
| Veritas NetBackup | FlexSnapshot integration |
| Rubrik / Cohesity | Native REST API snapshot integration |

For Evergreen//One, snapshot capacity consumed by backup integration counts toward the monthly consumption total — ensure backup snapshot retention policies are calibrated to avoid unexpected burst usage.

## REST API

Array-level REST API access for Evergreen//One follows the same Purity API as standard FlashArray and FlashBlade:

- **Base URL**: `https://<array-management-ip>/api/<version>/`
- **Authentication**: Bearer token via POST to `/api/<version>/auth/session`, or long-lived API token from the Purity GUI

Confirm with the service agreement whether direct API access to the array management interface is included or requires Pure Support involvement.

The **Pure1 REST API** is the preferred integration point for service-level data (capacity, SLA, billing) and does not require access to the individual array management interface:

```bash
# Example: retrieve array metrics via Pure1 API
curl -s -H "Authorization: Bearer <pure1-api-key>" \
  "https://api.pure1.purestorage.com/api/1.x/metrics?names=array_total_load" | jq .
```

Use the Pure1 API for integration with FinOps platforms, CMDB automation, and capacity planning tools to avoid dependency on per-array management access.
