# Aria Operations: Dashboards — Creating, Editing, and Sharing

```text
Dashboard Hierarchy — Aria Operations
┌─────────────────────────────────────────┐
│         Executive KPIs (top-level)      │
│  ┌──────────┐  ┌──────────┐  ┌───────┐ │
│  │ Workload │  │ Capacity │  │ Risk  │ │
│  │ summary  │  │ overview │  │ score │ │
│  └──────────┘  └──────────┘  └───────┘ │
└─────────────────────┬───────────────────┘
                      ▼ drill-down
┌─────────────────────────────────────────┐
│      Operational View (per team)        │
│  ┌─────────────┐  ┌────────────────┐   │
│  │ Cluster CPU │  │  Active alerts │   │
│  │ heat map    │  │  by severity   │   │
│  └──────┬──────┘  └────────────────┘   │
└─────────┼───────────────────────────────┘
          ▼ click object to drill-down
┌─────────────────────────────────────────┐
│    Troubleshooting (object detail)      │
│  Metric charts │ Relationship │ Alerts  │
└─────────────────────────────────────────┘
```

Aria Operations dashboards provide real-time visibility into the health, risk, and efficiency of your infrastructure. This page covers building dashboards, configuring widgets, using interactions, and sharing with other users.

## Dashboard Basics

Dashboards are per-user by default but can be shared with roles or all users. Each dashboard is composed of one or more **widgets** arranged in a grid layout.

Navigation: **Home > Dashboards > + Add**

Dashboard scope options:

| Scope | Behaviour |
|---|---|
| Self-owned | Visible only to the creator |
| Shared (read) | Others can view but not edit |
| Shared (edit) | Others can view and modify |
| Default Dashboard | Shown to all users on login |

## Adding and Configuring Widgets

```bash
# List available widget definitions via API
curl -sk -X GET \
  "https://aria-ops.example.com/suite-api/api/widgetdefinitions" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -H "Accept: application/json" | jq '.widgetDefinitions[].name'
```

Common widget types and their use cases:

| Widget | Use Case |
|---|---|
| Metric Chart | Time-series graph of one or more metrics |
| Metric Sparkline | Compact trend indicator for summary dashboards |
| Health Chart | Object health over time |
| Object List | Filtered list of resources with columns |
| Alert List | Active or recent alerts with severity |
| Heat Map | Grid view of objects by metric value |
| Scoreboard | Single metric value with status colouring |
| Relationship Chart | Object topology graph |

When configuring a Metric Chart widget:
1. Select **Edit Widget > Data > Add Metric**.
2. Choose object type (e.g., ClusterComputeResource).
3. Select metric key (e.g., `cpu|usage_average`).
4. Set time range and aggregation (AVG, MAX, MIN).

## Dashboard Interactions

Widgets can be linked so clicking an object in one widget filters the data in connected widgets. This is configured via **Widget Interactions** in the dashboard editor.

```bash
# Export a dashboard definition as JSON (for backup or migration)
curl -sk -X GET \
  "https://aria-ops.example.com/suite-api/api/dashboards/<dashboardId>" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -H "Accept: application/json" > dashboard-backup.json

# Import a dashboard from JSON
curl -sk -X POST \
  "https://aria-ops.example.com/suite-api/api/dashboards" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -H "Content-Type: application/json" \
  -d @dashboard-backup.json
```

## Sharing and Cloning Dashboards

To share a dashboard:
1. Open the dashboard and click **Actions > Share Dashboard**.
2. Set sharing level: read or edit.
3. Optionally set as the **Default Dashboard** for all users.

To clone a dashboard for customisation:
1. **Actions > Clone Dashboard** — creates a private copy.
2. Rename and modify without affecting the original.

## Importing Community Dashboards

VMware/Broadcom Exchange (exchange.vmware.com) hosts community dashboard packs. Download the `.zip`, then:

```bash
# Upload dashboard pack via API
curl -sk -X POST \
  "https://aria-ops.example.com/suite-api/api/dashboards/import" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -F "dashboardPack=@/path/to/dashboardpack.zip"
```

Popular community packs:

| Pack | Coverage |
|---|---|
| vSphere Operations | CPU, memory, storage, network per cluster/host |
| NSX-T Operations | Logical network health and flow telemetry |
| vSAN Operations | Disk group health, capacity, performance |
| Kubernetes | Container resource usage via Telegraf |

## Common Dashboard Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Widget shows "No Data" | Wrong object scope or metric key | Check widget configuration and object filter |
| Dashboard loads slowly | Too many widgets or long time ranges | Reduce widget count or shorten time range |
| Shared dashboard not visible | User lacks required role | Check user role permissions |
| Import fails | Dashboard JSON version mismatch | Re-export from same Aria Ops version |
| Widget interactions not working | Widgets not linked | Enable interactions in dashboard editor |
