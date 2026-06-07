# Amazon EVS — Health Checks

<div class="kb-summary">
EVS health check routine: cluster and host status via AWS CLI, vSAN and vCenter via PowerCLI, NSX-T component health, HCX service mesh status, and capacity review.
</div>

```text
┌──────────────────────────────── Amazon EVS — Health Checks ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Check sequence: AWS cluster → vCenter hosts → vSAN health → NSX-T → HCX → capacity          │   │
│   │   vSAN: all checks Green before any host maintenance; Orange = investigate before proceeding   │  │
│   │   NSX-T: Manager + Controller + Edge nodes all must show green before changes                  │  │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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
