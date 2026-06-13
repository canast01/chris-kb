---
tags:
  - aws
  - troubleshooting
---
# Amazon EVS — Diagnostics

<div class="kb-summary">
EVS diagnostic data collection: AWS CloudTrail, VPC Flow Logs, NSX-T support bundle, vSAN HCL check, HCX log bundle, and per-component log locations.
</div>

```text
┌────────────────────────────────────── Amazon EVS — Diagnostics ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   AWS: CloudTrail (API actions) + VPC Flow Logs (network) are always-on diagnostic sources    │   │
│   │   VMware: vSAN support bundle + NSX-T support bundle + vCenter log bundle for platform issues  │  │
│   │   HCX: built-in log bundle download from HCX Manager UI for migration/connectivity issues     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CloudTrail   = AWS API audit log; download from S3 or query via Athena for evs:* events              │
│  VPC Flow Logs = ENI-level traffic metadata; check for dropped packets or unexpected flows            │
│  vm-support bundle = ESXi diagnostic archive; collect with: vm-support -w /tmp; SCP off host          │
│  vCenter log bundle = VCSA diagnostic archive; VAMI → Monitor → Log Bundle; ~2-5 GB                   │
│  NSX-T support bundle = Collected from NSX Manager UI; Troubleshoot → Support Bundle                  │
│  SDDC Manager log = VCF audit log covering bringup, lifecycle, and compliance history                 │
│  HCX log bundle = HCX Manager → Support → Download Log Bundle; includes service mesh logs             │
│  CloudWatch   = AWS metrics for EVS host CPU, memory, and network via AWS integration                 │
│  AWS Health Dashboard = Personal Health Dashboard; shows AWS events affecting EVS resources           │
│  vSAN HCL check = vSAN Health → Hardware Compatibility; flags unsupported disk configurations         │
│  Athena       = AWS serverless query engine; analyze CloudTrail logs at scale using SQL               │
│  tcpdump      = Packet capture on ESXi vmnic; use for network-level diagnostic data collection        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Log Locations Reference

| Component | Log Location | How to Access |
|---|---|---|
| SDDC Manager | `/var/log/vmware/vcf/` | SSH to SDDC Manager appliance (`sddc-manager.vcf.internal`) |
| vCenter | `/var/log/vmware/vpxd/vpxd.log` | SSH to VCSA appliance, or VAMI → Monitoring → Logs |
| NSX-T Manager | `/var/log/vmware/nsx/` | SSH to NSX Manager node |
| ESXi host | `/var/log/vmware/` (hostd.log, vmkernel.log, auth.log) | SSH to host, or vCenter → Host → Monitor → Logs |
| HCX Manager | `/opt/vmware/log/` | SSH to HCX Manager VM, or HCX UI → Support → Download Log Bundle |
| AWS CloudTrail | S3 bucket (configured) or CloudTrail console | `aws cloudtrail lookup-events` or Athena SQL query |
| AWS CloudWatch | EVS namespace metrics | `aws cloudwatch get-metric-statistics` |
| VPC Flow Logs | CloudWatch Logs group or S3 bucket | CloudWatch Logs Insights or S3 + Athena |

Key log files per component:

| Component | File | Content |
|---|---|---|
| vCenter | `vpxd.log` | vCenter API requests, task failures, authentication events |
| vCenter | `sps.log` | Storage Policy (SPBM) operations; VM encryption policy errors |
| ESXi | `hostd.log` | Host daemon; VM power operations, vSphere API calls to host |
| ESXi | `vmkernel.log` | Kernel-level events; NIC errors, storage errors, PSOD precursors |
| ESXi | `auth.log` | SSH logins, DCUI sessions, lockdown mode events |
| NSX-T | `nsx-manager.log` | NSX Manager control plane operations |
| NSX-T | `nsx-controller.log` | Data plane programming; DFW rule push events |
| SDDC Manager | `lcm.log` | Lifecycle management; upgrade and patch workflow events |
| SDDC Manager | `domainmanager.log` | Workload domain operations; cluster expansion events |

## AWS Diagnostic Commands

```bash
# CloudTrail: look up all EVS API calls in the last 24 hours
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventSource,AttributeValue=evs.amazonaws.com \
  --start-time $(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ) \
  --query 'Events[*].[EventTime,EventName,Username,ErrorCode]' \
  --output table

# CloudTrail: filter for failed EVS API calls only
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

```bash
# CloudWatch: get EVS host metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/EVS \
  --metric-name HostState \
  --dimensions Name=EnvironmentId,Value=$ENV_ID \
  --start-time $(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 300 --statistics Average

# EC2: describe all ENIs in EVS subnet — useful to see ENI attachment status
aws ec2 describe-network-interfaces \
  --filters Name=subnet-id,Values=$EVS_MGMT_SUBNET_ID \
  --query 'NetworkInterfaces[*].[NetworkInterfaceId,Status,Attachment.Status,Description]' \
  --output table

# EC2: check for ENIs not attached (may indicate a host that lost its ENI)
aws ec2 describe-network-interfaces \
  --filters Name=subnet-id,Values=$EVS_MGMT_SUBNET_ID \
             Name=status,Values=available \
  --query 'NetworkInterfaces[*].[NetworkInterfaceId,Description]' \
  --output table
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

## vSphere Diagnostic Bundle

The vSphere support bundle collects all component logs, configuration exports, and system state snapshots into a single archive. When opening a case with VMware/Broadcom support, this is the primary artifact they will request.

```bash
# Generate vCenter support bundle via VAMI (vCenter Appliance Management Interface)
# Browser: https://<vcenter-ip>:5480 → Monitoring → Create Support Bundle
# The bundle is stored on the VCSA appliance and available for SFTP download

# Via SSH on the VCSA appliance:
# /usr/lib/vmware-vmafd/bin/vdcrepadmin -f showpartners -h localhost -u administrator
# vc-support.sh -L /tmp/vc-support
# SCP the generated .zip from /var/tmp/vc-support-*.zip

# Alternative: vm-support command on ESXi host
# SSH to ESXi host:
# vm-support -w /tmp
# SCP: /tmp/esx-<hostname>-<timestamp>.tgz
```

The vCenter support bundle contains:
- `vpxd.log` and all vCenter service logs
- vSAN health export (XML)
- vCenter configuration backup
- Task and event history export
- SSO and certificate state

Share the bundle by uploading to the VMware SFTP site provided in the support request. For large bundles (2-5 GB is normal), use the SFTP method rather than portal upload.

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

When opening an NSX-T case, always include:
- NSX-T version (`GET /api/v1/node/version`)
- Upgrade history (NSX Manager → Lifecycle Management → Upgrade History)
- The support bundle
- A description of which DFW policies, T0/T1 gateways, or segments are affected

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

## Systematic Triage Order

Diagnose EVS issues in this order to avoid chasing symptoms at the wrong layer:

**Layer 1: AWS infrastructure**
```bash
# Check host state
aws evs list-environment-hosts --environment-id $ENV_ID \
  --query 'hostSummaries[*].[hostId,state]' --output table

# Check EC2 instance status for EVS hosts
aws ec2 describe-instance-status \
  --filters Name=instance-state-name,Values=running \
  --query 'InstanceStatuses[?SystemStatus.Status!=`ok` || InstanceStatus.Status!=`ok`]'

# Check VPC route tables — missing routes cause NSX-T BGP failure
aws ec2 describe-route-tables \
  --filters Name=vpc-id,Values=$EVS_VPC_ID \
  --query 'RouteTables[*].Routes[*].[DestinationCidrBlock,State,GatewayId,NetworkInterfaceId]' \
  --output table

# Check ENI attachment status for EVS hosts
aws ec2 describe-network-interfaces \
  --filters Name=subnet-id,Values=$EVS_MGMT_SUBNET_ID \
  --query 'NetworkInterfaces[*].[NetworkInterfaceId,Status,Attachment.Status]' --output table
```

**Layer 2: VMware platform**
```powershell
# Check vCenter connectivity and vSAN health
Connect-VIServer -Server $VCENTER -User administrator@vsphere.local -Password $PASS

# vSAN cluster health summary
$vsanHealth = Get-VsanView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system"
$summary = $vsanHealth.QueryVsanClusterHealthSummary(
    (Get-Cluster).Id, $null, $null, $true, $null, $null, "defaultView")
$summary.OverallHealth

# Host connectivity
Get-VMHost | Select Name, ConnectionState, PowerState
```

**Layer 3: NSX-T**
```bash
# Check NSX Manager cluster health
curl -sk -u "admin:$NSX_PASSWORD" "$NSX_URL/api/v1/cluster/status" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Cluster: {d['mgmt_cluster_status']['status']}\")"

# Check T0 BGP neighbor state
curl -sk -u "admin:$NSX_PASSWORD" \
  "$NSX_URL/policy/api/v1/infra/tier-0s/<t0-id>/locale-services/<svc-id>/bgp/neighbors/status" | \
  python3 -c "
import sys,json
for n in json.load(sys.stdin).get('results',[]):
    print(f\"{n['neighbor_address']}: {n['connection_state']}\")"
```

**Layer 4: Application**

After confirming layers 1-3 are healthy, investigate application-layer connectivity using standard tools: ping, traceroute, telnet to port, curl. Capture VPC Flow Logs to confirm whether traffic is reaching the ENI. Check NSX-T DFW logs for deny hits on the relevant workload.

## Log Locations

| Component | Log Location | Access Method |
|---|---|---|
| ESXi syslog | `/var/log/vmkernel.log`, `/var/log/hostd.log` | SSH or vCenter → Host → Monitor → Logs |
| vCenter | `/var/log/vmware/vpxd/vpxd.log` | vCenter appliance SSH |
| NSX-T Manager | `/var/log/vmware/nsx-manager/` | NSX Manager SSH |
| SDDC Manager | `/var/log/vmware/sddc-manager/` | SDDC Manager SSH |
| HCX Manager | HCX UI → Support → Download Logs | HCX Manager UI |
| AWS EVS | CloudTrail + CloudWatch | AWS console or CLI |

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
