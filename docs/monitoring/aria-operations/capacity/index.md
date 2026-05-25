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
┌───────────────────────────────────── Aria Operations — Capacity ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Aria Operations Capacity Management — Forecasting, Right-Sizing, and What-If         │   │
│   │      Capacity models: Demand model (usage trend) · Allocation model (provisioned CPU/mem)     │   │
│   │                Forecast horizon: 30 / 60 / 90 days configurable per object type               │   │
│   │           Right-sizing: oversized VMs flagged; reclaim CPU/mem/disk recommendations           │   │
│   │                What-if: add N VMs and see projected impact on cluster headroom                │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Run what-if analysis before any major workload migration to validate headroom                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Capacity Models       │  │         Forecasting         │  │         Right-Sizing        │   │
│   │         Demand model        │  │        30-day horizon       │  │        Oversized VMs        │   │
│   │       Allocation model      │  │        60-day horizon       │  │        Undersized VMs       │   │
│   │        Custom buffers       │  │        90-day horizon       │  │       Reclaim CPU/mem       │   │
│   │       Policy overrides      │  │       What-if: add VMs      │  │         Reclaim disk        │   │
│   │      Per-cluster scope      │  │       Trend visualise       │  │         Batch action        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Capacity analytics on Aria Ops master · data feeds: vCenter/vSAN/storage adapters                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Demand model      = Capacity model tracking actual usage trend over time                             │
│  Allocation model  = Capacity model tracking provisioned (allocated) CPU and memory                   │
│  Buffer            = Reserved headroom percentage excluded from usable capacity calc                  │
│  Forecast horizon  = Number of days projected; longer = less accurate but more strategic              │
│  What-if analysis  = Simulation adding/removing workloads to predict capacity impact                  │
│  Right-sizing      = Recommendation to adjust vCPU/vMem to match actual usage patterns                │
│  Reclaim           = Action recovering idle CPU, memory, or disk from oversized VMs                   │
│  Oversized VM      = VM provisioned significantly above its measured peak utilisation                 │
│  Undersized VM     = VM hitting its provisioned limits; causes performance degradation                │
│  Batch action      = Applying right-size recommendations to multiple VMs simultaneously               │
│  Policy override   = Cluster-specific capacity policy overriding global default settings              │
│  Headroom          = Remaining available capacity before the configured utilisation limit             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
