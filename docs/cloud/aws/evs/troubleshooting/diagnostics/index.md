# Amazon EVS — Diagnostics

<div class="kb-summary">
EVS diagnostic data collection: AWS CloudTrail, VPC Flow Logs, NSX-T support bundle, vSAN HCL check, HCX log bundle, and per-component log locations.
</div>

```text
┌──────────────────────────────── Amazon EVS — Diagnostics ─────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   AWS: CloudTrail (API actions) + VPC Flow Logs (network) are always-on diagnostic sources    │   │
│   │   VMware: vSAN support bundle + NSX-T support bundle + vCenter log bundle for platform issues  │  │
│   │   HCX: built-in log bundle download from HCX Manager UI for migration/connectivity issues     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## AWS CloudTrail

```bash
# Query EVS API actions in CloudTrail (last 1 hour)
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventSource,AttributeValue=evs.amazonaws.com \
  --start-time $(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ) \
  --query 'Events[*].[EventTime,EventName,Username,ErrorCode]' \
  --output table

# Filter for only failed events
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventSource,AttributeValue=evs.amazonaws.com \
  --start-time $(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ) | \
  python3 -c "
import sys, json
events = json.load(sys.stdin).get('Events', [])
for e in events:
    ct = json.loads(e.get('CloudTrailEvent','{}'))
    if ct.get('errorCode'):
        print(f\"{e['EventTime']} {e['EventName']}: {ct['errorCode']} - {ct.get('errorMessage','')}\")
"
```

## VPC Flow Logs

```bash
# Query flow logs in CloudWatch Logs Insights
# Go to: CloudWatch → Logs Insights → select evs-flow-logs log group

# Query: top rejected connections last 1 hour
# fields @timestamp, srcAddr, dstAddr, dstPort, action
# | filter action = "REJECT"
# | stats count(*) as rejectCount by srcAddr, dstAddr, dstPort
# | sort rejectCount desc
# | limit 20

# Via CLI (query last 5 min of rejects from EVS subnet)
aws logs start-query \
  --log-group-name evs-flow-logs \
  --start-time $(($(date +%s) - 300)) \
  --end-time $(date +%s) \
  --query-string 'fields @timestamp, srcAddr, dstAddr, dstPort, action | filter action = "REJECT" | limit 50'
```

## NSX-T Support Bundle

```bash
# Generate NSX-T support bundle (includes all Manager, Controller, and Edge logs)
TASK_ID=$(curl -sk -u "admin:$NSX_PASSWORD" \
  -X POST "$NSX_URL/api/v1/support-bundles?action=collect" \
  -H "Content-Type: application/json" \
  -d '{"log_age": 1440}' | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# Monitor collection progress
curl -sk -u "admin:$NSX_PASSWORD" \
  "$NSX_URL/api/v1/tasks/$TASK_ID" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Status: {d['status']}\")"

# Download when complete (status = success)
curl -sk -u "admin:$NSX_PASSWORD" \
  "$NSX_URL/api/v1/support-bundles?action=collect&$TASK_ID" -o nsxt-support-bundle.tar.gz
```

## vSAN Support Bundle

```powershell
# Generate vSAN support bundle via PowerCLI
$cluster = Get-Cluster -Name "EVS-Management-Cluster"
$perfSvc = Get-VsanView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system"

# Collect vSAN support bundle
$bundle = $perfSvc.CreateVsanSystemSupportBundle($cluster.Id, "/tmp/vsan-bundle.zip")
Write-Host "vSAN bundle saved to: $bundle"

# vSAN HCL compatibility check
$hclSvc = Get-VsanView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system"
$hclResult = $hclSvc.QueryVsanClusterHealthSummary($cluster.Id, $null, @("vsanHclDbUpToDate","vSanHclHostBadState"), $true, $null, $null, "defaultView")
$hclResult.Groups | ForEach-Object { Write-Host "$($_.GroupName): $($_.GroupHealth)" }
```

## Log Locations

| Component | Log Location | Access Method |
|---|---|---|
| ESXi syslog | `/var/log/vmkernel.log`, `/var/log/hostd.log` | SSH or vCenter → Host → Monitor → Logs |
| vCenter | `/var/log/vmware/vpxd/vpxd.log` | vCenter appliance SSH |
| NSX-T Manager | `/var/log/vmware/nsx-manager/` | NSX Manager SSH |
| SDDC Manager | `/var/log/vmware/sddc-manager/` | SDDC Manager SSH |
| HCX Manager | HCX UI → Support → Download Logs | HCX Manager UI |
| AWS EVS | CloudTrail + CloudWatch | AWS console or CLI |
