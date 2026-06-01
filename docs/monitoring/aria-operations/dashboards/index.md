# Aria Operations: Dashboards — Creating, Editing, and Sharing


<div class="kb-summary">
Creating, Editing, and Sharing reference covering Dashboard Interactions, Sharing and Cloning Dashboards, Importing Community Dashboards, Common Dashboard Issues.
</div>

```text
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
