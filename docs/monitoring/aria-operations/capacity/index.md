# Aria Operations: Capacity Analytics and Rightsizing

```text
Capacity Model — Aria Operations
┌──────────────────────────────────────────┐
│         Capacity Analytics Engine        │
│                                          │
│  Observed usage (demand model)           │
│  ┌──────────────────────────────────┐    │
│  │ Cluster A  ████████░░░░░  68%   │    │
│  │ Cluster B  ██████████████ 92% ! │    │
│  │ Datastore  ████████████░░ 83%   │    │
│  └──────────────────────────────────┘    │
│                   │                      │
│       ┌───────────┼──────────────┐       │
│       ▼           ▼              ▼       │
│  Rightsize    Demand         Reclaim     │
│  recommend.   forecast       idle VMs   │
│  (vCPU/vRAM)  (days left)  (snapshots)  │
└──────────────────────────────────────────┘
```

Aria Operations provides capacity analytics across vSphere clusters, datastores, and virtual machines. This page covers capacity models, time-remaining projections, rightsizing recommendations, and reclaim workflows.

## Capacity Overview and Models

Capacity analytics are driven by the **capacity model** assigned to each object. The model determines how Aria Operations calculates used, available, and total capacity.

Navigation: **Capacity > Overview**

Key capacity model types:

| Model | Description |
|---|---|
| Allocation Model | Based on configured/allocated resources (vCPU, memory reservation) |
| Demand Model | Based on peak observed usage over rolling window |
| Custom Model | User-defined weighting between allocation and demand |

The **Time Remaining** metric projects when a cluster or datastore will be full based on the current growth trend. Default look-back is 30 days; adjust in **Administration > Global Settings > Capacity**.

## Cluster and Datastore Capacity

```bash
# Get capacity for all clusters via API
curl -sk -X POST \
  "https://aria-ops.example.com/suite-api/api/resources/query" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "adapterKind": ["VMWARE"],
    "resourceKind": ["ClusterComputeResource"],
    "resourceStatus": ["DATA_RECEIVING"]
  }' | jq '.resourceList[] | {name: .resourceKey.name, id}'

# Query time-remaining metric for a specific cluster
curl -sk -X GET \
  "https://aria-ops.example.com/suite-api/api/resources/<resourceId>/stats?statKey=summary|capacityRemainingPercentage&rollUpType=AVG&intervalType=HOURS&intervalQuantifier=1" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -H "Accept: application/json"
```

Key capacity metrics to monitor:

| Metric Key | Description |
|---|---|
| `summary|workload` | Current workload percentage |
| `summary|remainingCapacityPercentage` | Remaining headroom |
| `summary|timeRemaining` | Days until capacity exhausted |
| `summary|totalCapacity` | Total configured capacity |

## Rightsizing Recommendations

Aria Operations identifies over-provisioned VMs through the **Reclaim** and **Rightsize** views.

Navigation: **Optimization > Reclaim** or **Optimization > Rightsizing**

Categories of rightsizing actions:

| Category | Action | Typical Trigger |
|---|---|---|
| Oversized CPU | Reduce vCPU count | CPU demand < 20% over 30 days |
| Oversized Memory | Reduce vRAM | Memory demand < 30% with no ballooning |
| Idle VM | Power off or delete | No I/O, CPU, or network for 30+ days |
| Snapshot Cleanup | Remove old snapshots | Snapshot age > 7 days |

```bash
# Export rightsizing recommendations via API
curl -sk -X GET \
  "https://aria-ops.example.com/suite-api/api/recommendations?recommendationType=RIGHTSIZE" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -H "Accept: application/json" | jq '.recommendations[] | {resourceName, description, impact}'
```

## Reclaim Workflow

1. Navigate to **Optimization > Reclaim > Powered Off VMs**.
2. Filter by last powered-on date and cost.
3. Use **Actions > Powered Off VMs Report** to export the list.
4. Validate with VM owners before any deletion.
5. Archive or snapshot before reclaiming storage.

```bash
# List powered-off VMs via API with last-modified filter
curl -sk -X POST \
  "https://aria-ops.example.com/suite-api/api/resources/query" \
  -H "Authorization: vRealizeOpsToken <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "adapterKind": ["VMWARE"],
    "resourceKind": ["VirtualMachine"],
    "propertyConditions": {
      "conditions": [{"key": "summary|runtime|powerState", "operator": "EQ", "stringValue": "powered_off"}]
    }
  }' | jq '.resourceList[].resourceKey.name'
```

## Capacity Planning Reports

Run capacity planning reports to project future needs by cluster or datacenter.

Navigation: **Reports > Report Templates > Capacity Report**

| Report Type | Use Case |
|---|---|
| Capacity Overview | Single-page cluster summary for management |
| VM Rightsizing | List of VMs with recommended changes |
| What-If Analysis | Model impact of adding/removing workloads |
| Time Remaining | Which clusters will be full within N days |

## Common Capacity Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Time remaining shows 0 days | Demand spike or wrong model | Switch to demand model, check for runaway VM |
| Rightsizing not appearing | Insufficient data history | Wait for 30-day baseline window |
| Capacity analytics stale | Collection adapter failing | Check adapter status, restart if needed |
| What-If results not saving | Session timeout | Re-authenticate and rerun analysis |
