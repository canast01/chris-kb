# Amazon EVS — Common Issues

<div class="kb-summary">
Troubleshooting guide for EVS failures: host stuck in non-CREATED state, vSAN degraded health, HCX service mesh down, NSX-T routing failures, and API errors.
</div>

```text
┌───────────────────────────────────── Amazon EVS — Common Issues ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Host FAILED state: AWS-side issue — contact AWS support; don't delete manually first        │   │
│   │   vSAN degraded: check host connectivity before anything; resync before removing components   │   │
│   │   HCX disconnected: verify DX connectivity and service mesh appliance health                  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Host Stuck or FAILED State

```bash
# Check host state
aws evs list-environment-hosts --environment-id $ENV_ID \
  --query 'hostSummaries[*].[hostId,state]' --output table

# If state is FAILED or CREATE_FAILED:
# 1. DO NOT delete the host immediately — preserve for AWS diagnostics
# 2. Check CloudTrail for EVS API error events
aws logs filter-log-events \
  --log-group-name CloudTrail \
  --filter-pattern "{ $.eventSource = \"evs.amazonaws.com\" && $.errorCode EXISTS }" \
  --start-time $(($(date +%s) - 86400))000

# 3. Check if corresponding EC2 instance is impaired
aws ec2 describe-instance-status \
  --filters Name=instance-state-name,Values=running \
  --query 'InstanceStatuses[?SystemStatus.Status!=`ok`]'

# 4. Open AWS support case with host-id and environment-id
# Provide: environment ID, host ID, approximate failure timestamp, CloudTrail export
```

## vSAN Degraded Health

```powershell
# Get vSAN health status
$cluster = Get-Cluster -Name "EVS-Management-Cluster"
$vsanHealth = Get-VsanView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system"
$summary = $vsanHealth.QueryVsanClusterHealthSummary($cluster.Id, $null, $null, $true, $null, $null, "defaultView")
$summary.Groups | Where-Object { $_.GroupHealth -ne "green" } | ForEach-Object {
    Write-Host "DEGRADED: $($_.GroupName) - $($_.GroupHealth)"
    $_.Tests | Where-Object { $_.TestHealth -ne "green" } | ForEach-Object {
        Write-Host "  Test: $($_.TestName) - $($_.TestHealth)"
    }
}

# Common vSAN issues:
# "Performance Service" degraded → enable vSAN Performance Service
#   Set-VsanClusterConfiguration -VsanClusterConfiguration $vsanConfig -PerformanceServiceEnabled $true

# "vSAN HCL DB up-to-date" → update HCL database in vCenter
#   vCenter → Cluster → vSAN → Skyline Health → Download HCL DB

# "Network misconfiguration" → check VTEP VMkernel on all hosts
#   Get-VMHostNetworkAdapter -VMHost * | Where { $_.VsanTrafficEnabled }
```

## HCX Service Mesh Down

```bash
# Verify HCX interconnect status
curl -sk -u "admin:$HCX_PASSWORD" \
  "https://$HCX_MANAGER_IP/hybridity/api/interconnect/links" | \
  python3 -c "
import sys, json
for link in json.load(sys.stdin).get('items', []):
    print(f\"{link['label']}: {link['status']}\")
"

# Common causes:
# a) Direct Connect down → check DX connection in AWS console
aws directconnect describe-connections --query 'connections[*].[connectionName,connectionState]'

# b) HCX appliance IP unreachable → verify SG rules on VTEP subnet allow UDP 4500, UDP 500
aws ec2 describe-security-groups --group-ids sg-hcx \
  --query 'SecurityGroups[*].IpPermissions'

# c) Certificate expired → regenerate service mesh certificates
#    HCX Manager UI → Interconnect → Service Mesh → Actions → Redeploy
```

## NSX-T Routing Failure (VM Connectivity)

```bash
# Symptoms: VMs on NSX-T segments can't communicate with VPC resources or on-premises

# 1. Check T0 router BGP status (should be Established for DX/TGW)
curl -sk -u "admin:$NSX_PASSWORD" \
  "$NSX_URL/api/v1/logical-routers?router_type=TIER0" | \
  python3 -c "import sys,json; [print(f\"{r['display_name']}: {r['id']}\") for r in json.load(sys.stdin)['results']]"

# Get T0 BGP neighbors
curl -sk -u "admin:$NSX_PASSWORD" \
  "$NSX_URL/api/v1/logical-routers/<t0-id>/routing/bgp/neighbors/status" | \
  python3 -c "
import sys,json
for n in json.load(sys.stdin).get('results',[]):
    print(f\"{n['neighbor_address']}: {n['connection_state']}\")
"

# 2. Verify ENI routing in VPC route table
aws ec2 describe-route-tables \
  --filters Name=vpc-id,Values=$EVS_VPC_ID \
  --query 'RouteTables[*].Routes[?DestinationCidrBlock!=`local`]'

# 3. Ping from NSX-T Edge node to VPC gateway
# NSX-T UI → Networking → Tier-0 Gateways → Edge node → Test Connectivity
```

## AWS EVS API Errors

```bash
# Common API error: AccessDeniedException
# Fix: verify IAM role has elasticvmwareservice:* on the specific environment ARN

# Common API error: ResourceInUseException when deleting host
# Cause: host still in maintenance mode with vSAN evacuation incomplete
# Fix: wait for vSAN BytesToSync = 0, then retry delete

# Common API error: LimitExceededException
# Check current quota
aws service-quotas get-service-quota \
  --service-code elasticvmwareservice \
  --quota-code L-XXXXXXXX   # check quota name in console

# Request quota increase
aws service-quotas request-service-quota-increase \
  --service-code elasticvmwareservice \
  --quota-code L-XXXXXXXX \
  --desired-value 10
```
