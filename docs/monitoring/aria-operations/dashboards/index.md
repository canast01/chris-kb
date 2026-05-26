# Aria Operations: Dashboards — Creating, Editing, and Sharing

```
┌──────────────────────────────────── Aria Operations — Dashboards ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Aria Operations Dashboards — Built-in, Custom, and Shared Dashboard Management        │   │
│   │         Built-in: Executive Overview · Capacity Overview · vSphere Health · NSX Health        │   │
│   │     Widget types: scoreboard · time-series · heatmap · topology · alert list · object list    │   │
│   │       Interaction: drill-down from widget to object · filter by tag · time-range picker       │   │
│   │          Sharing: publish to group · export JSON · import · embed in external portal          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Import community dashboards from VMware {code} exchange to accelerate deployment                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │     Built-in Dashboards     │  │        Custom Widgets       │  │       Sharing & Export      │   │
│   │      Executive Overview     │  │          Scoreboard         │  │       Publish to group      │   │
│   │      Capacity Overview      │  │      Time-series chart      │  │         Export JSON         │   │
│   │        vSphere Health       │  │        Heatmap widget       │  │         Import JSON         │   │
│   │          NSX Health         │  │         Topology map        │  │         Embed iframe        │   │
│   │        Alert Overview       │  │      Alert list widget      │  │       Clone/customise       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Dashboards stored in Aria Ops vPostgres DB · UI served on HTTPS/443 from master node                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Built-in dashboard = Pre-configured dashboard shipped with Aria Operations                           │
│  Scoreboard widget  = Tile displaying current metric value with colour-coded threshold                │
│  Time-series widget = Line chart of metric over configurable time window                              │
│  Heatmap widget     = Grid with colour-coded cells per object; fast outlier detection                 │
│  Topology widget    = Visual map of object relationships (VM → host → cluster)                        │
│  Alert list widget  = Live count and list of active alerts for filtered object set                    │
│  Drill-down         = Clicking widget navigates to the individual object detail page                  │
│  Tag filter         = Filtering dashboard widgets by vSphere tag or Aria Ops group tag                │
│  Export JSON        = Serialising dashboard definition for sharing or backup                          │
│  VMware {code}      = VMware community code exchange hosting dashboard JSON templates                 │
│  Super metric       = Custom calculated metric combining multiple raw metrics in a formula            │
│  Clone dashboard    = Copying an existing dashboard as starting point for customisation               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
