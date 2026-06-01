# Evergreen — Integrations


<div class="kb-summary">
Integrations reference covering Pure1 Integration, True Forward Capacity Upgrades, VMware Integration, Backup Integration, REST API.
</div>
```
┌──────────────────────────────── Storage Pure Evergreen — Integrations ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Pure integrations: VMware vSphere, Kubernetes CSI, backup software, and monitoring      │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │ API: Storage Pure Evergreen management console REST API enables automation and third-party to │   │
│   │             Plug-ins available for vCenter, OpenShift, Splunk, and SIEM platforms             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Pure → REST API / plug-ins → VMware / K8s / backup / monitoring                                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Storage Pure Evergreen infrastructure · management network · monitoring                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Pure               = Storage Pure Evergreen platform overview and core concepts                    │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


```text
Evergreen Integration Touchpoints
  FlashArray / FlashBlade
          │  phone-home (HTTPS 443, always-on)
          ▼
  Pure1 Cloud
  ├── Subscription entitlement + True Forward tracking
  ├── Ever Modern eligibility + upgrade scheduling
  ├── Fleet health score + anomaly detection
  ├── Capacity forecasting + growth projections
  └── Support case creation + diagnostic integration
          │
          ▼
  Customer interfaces:
  ├── Pure1 portal (pure1.purestorage.com)
  ├── Pure1 REST API (automation, reporting)
  └── Pure Account Team (renewal, refresh planning)
```

> Part of the [Evergreen Architecture](../index.md) reference.

---

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

The REST API supports all array operations available in the GUI and CLI. Use API version 2.x for new integrations — version 1.x is deprecated. Pure1 also provides a fleet-level REST API for subscription and capacity data.
