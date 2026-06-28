---
tags:
  - aws
  - operations
---
# Amazon EVS — Health Checks

<div class="kb-summary">
EVS health check routine: cluster and host status via AWS CLI, vSAN and vCenter via PowerCLI, NSX-T component health, HCX service mesh status, and capacity review.

*Applies to: Amazon EVS*
</div>



```d2
direction: right

hub: "AWS EVS\nOperations" {shape: hexagon}
run_this_routine: "Run This Routine" {shape: rectangle}
manual_checks: "Manual Checks" {shape: rectangle}
verify: "Verify" {shape: rectangle}

hub -> run_this_routine
hub -> manual_checks
hub -> verify
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

```bash
#!/bin/bash
# EVS Daily Health Check

ENV_ID="${EVS_ENV_ID:?Set EVS_ENV_ID}"
VCENTER="${VCENTER_HOST:?Set VCENTER_HOST}"
VCENTER_USER="${VCENTER_USER:-administrator@vsphere.local}"

echo "=== [1] AWS EVS Cluster State ==="
aws evs get-environment --environment-id "$ENV_ID" \
  --query '[environment.state, environment.environmentName]' --output text

echo "=== [2] Host States ==="
aws evs list-environment-hosts --environment-id "$ENV_ID" \
  --query 'hostSummaries[*].[hostId,instanceType,state]' --output table

echo "=== [3] vCenter Host Health (PowerCLI) ==="
pwsh -Command "
  Connect-VIServer -Server $VCENTER -User $VCENTER_USER -Password \$env:VCENTER_PASSWORD -WarningAction SilentlyContinue | Out-Null
  Get-VMHost | Select-Object Name, ConnectionState, PowerState | Format-Table -AutoSize
  Disconnect-VIServer -Confirm:\$false | Out-Null
"

echo "=== [4] vSAN Health Summary ==="
pwsh -Command "
  Connect-VIServer -Server $VCENTER -User $VCENTER_USER -Password \$env:VCENTER_PASSWORD -WarningAction SilentlyContinue | Out-Null
  \$cluster = Get-Cluster | Select-Object -First 1
  \$hs = Get-VsanView -Id 'VsanVcClusterHealthSystem-vsan-cluster-health-system'
  \$summary = \$hs.QueryVsanClusterHealthSummary(\$cluster.Id, \$null, \$null, \$true, \$null, \$null, 'defaultView')
  \$summary.Groups | ForEach-Object { Write-Host \"\$(\$_.GroupName): \$(\$_.GroupHealth)\" }
  Disconnect-VIServer -Confirm:\$false | Out-Null
"

echo "=== [5] NSX-T Manager Health ==="
NSX_URL="${NSX_MANAGER_URL:?Set NSX_MANAGER_URL}"
curl -sk -u "admin:${NSX_PASSWORD}" "$NSX_URL/api/v1/cluster/status" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Control cluster: {d['control_cluster_status']['status']}\")"

echo "=== [6] HCX Service Mesh Status ==="
# Check HCX UI: Interconnect → Service Mesh → all appliances should show Running
# Or via HCX API:
curl -sk -u "admin:${HCX_PASSWORD}" \
  "https://${HCX_MANAGER_IP}/hybridity/api/interconnect/links" | \
  python3 -c "import sys,json; [print(f\"{l['label']}: {l['status']}\") for l in json.load(sys.stdin).get('items',[])]"

echo "=== [7] vSAN Capacity ==="
pwsh -Command "
  Connect-VIServer -Server $VCENTER -User $VCENTER_USER -Password \$env:VCENTER_PASSWORD -WarningAction SilentlyContinue | Out-Null
  Get-Datastore -Name *vsan* | Select-Object Name, CapacityGB, FreeSpaceGB,
    @{N='UsedPct';E={[math]::Round((1-\$_.FreeSpaceGB/\$_.CapacityGB)*100,1)}} | Format-Table -AutoSize
  Disconnect-VIServer -Confirm:\$false | Out-Null
"
```

## Manual Checks

![Manual Checks](../../../../assets/cloud-aws-evs-hc-manual-checks.svg)

```bash
# Check for vSAN resync activity (should be 0 outside of maintenance)
# PowerCLI:
# Get-VsanResyncDashboard -Cluster (Get-Cluster) | Select BytesToSync, ActiveTasks

# Check NSX Manager cluster nodes
curl -sk -u "admin:$NSX_PASSWORD" \
  "https://$NSX_MANAGER_URL/api/v1/cluster/nodes" | \
  python3 -c "import sys,json; [print(f\"{n['display_name']}: {n['manager_role']['mgmt_cluster_listen_addr']['ip_address']}\") for n in json.load(sys.stdin)['results']]"

# Check NSX Edge nodes
curl -sk -u "admin:$NSX_PASSWORD" \
  "https://$NSX_MANAGER_URL/api/v1/transport-nodes?node_types=EdgeNode" | \
  python3 -c "import sys,json; [print(f\"{n['display_name']}: {n.get('node_deployment_state',{}).get('state','unknown')}\") for n in json.load(sys.stdin)['results']]"
```

---

## See also

- [Amazon EVS — Common Issues](../troubleshooting/common-issues/)
- [Amazon EVS — Procedures](procedures/)
- [Amazon EVS — CLI Reference](cli-reference/)

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
