# Amazon EVS — Procedures

<div class="kb-summary">
EVS operational procedures: adding and removing hosts, host maintenance mode, vSAN rebalance, NSX-T segment and policy management, and HCX migration workflows.
</div>

```text
┌─────────────────────────────────────── Amazon EVS — Procedures ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Adding a host: vSAN resyncs data automatically; allow 2-4 hours before another change       │   │
│   │   Removing a host: maintenance mode + vSAN evacuation first; then AWS delete-host             │   │
│   │   HCX vMotion: verify bandwidth and HCX service mesh green before migrating production VMs    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Add a Host

```bash
# 1. Verify current cluster capacity before adding
aws evs list-environment-hosts --environment-id $ENV_ID \
  --query 'hostSummaries[*].state' --output text

# 2. Request new host via AWS EVS API
aws evs create-environment-host \
  --environment-id $ENV_ID \
  --host '{"instanceType":"i4i.metal","keyName":"evs-cluster-key"}'

# 3. Monitor host provisioning (takes ~30-60 min)
watch -n 30 'aws evs list-environment-hosts --environment-id $ENV_ID \
  --query "hostSummaries[*].[hostId,state]" --output table'

# 4. Once host state = CREATED, verify it appears in vCenter
# vCenter → Cluster → Hosts → new host should be Connected

# 5. Verify vSAN automatically adds the host's disks
# PowerCLI: Get-VsanDiskGroup | Where { $_.VMHost.Name -eq "new-host" }

# 6. Allow vSAN to rebalance (may take 1-4 hours depending on data volume)
# PowerCLI: Get-VsanResyncDashboard -Cluster (Get-Cluster) | Select BytesToSync
```

## Remove a Host

```bash
# 1. Verify vSAN has enough hosts remaining (minimum 3 after removal)
aws evs list-environment-hosts --environment-id $ENV_ID --query 'length(hostSummaries)'

# 2. Put host in maintenance mode with full data evacuation (PowerCLI)
Set-VMHost -VMHost "evs-host-01.vcf.internal" -State Maintenance -Evacuate $true
# Wait for VMs to vMotion off and vSAN to resync — check: Get-VMHost | Select Name, State

# 3. Wait for vSAN resync to complete (BytesToSync = 0)
# Get-VsanResyncDashboard -Cluster (Get-Cluster) | Select BytesToSync, ActiveTasks

# 4. Delete host via EVS API
aws evs delete-environment-host --environment-id $ENV_ID --host-id host-xxx
```

## NSX-T Segment Management

```bash
# Create a new logical segment (workload network)
curl -sk -u "admin:$NSX_PASSWORD" \
  -X POST "$NSX_URL/api/v1/logical-switches" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "workload-web-01",
    "transport_zone_id": "<overlay-tz-id>",
    "replication_mode": "MTEP",
    "admin_state": "UP",
    "vni": 70001
  }' | python3 -m json.tool

# Attach segment to T1 router (via router port)
# Recommended: do this via NSX-T UI for first-time config; use API for automation

# Update distributed firewall policy to allow new segment
# NSX-T → Security → Distributed Firewall → Add rule targeting new segment group
```

## vSAN Rebalance

```bash
# Trigger manual vSAN rebalance (PowerCLI)
$cluster = Get-Cluster -Name "EVS-Management-Cluster"
$vsanSystem = Get-VsanView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system"

# Check if rebalance is recommended
$cluster.ExtensionData.GetResourceUsage()

# Trigger rebalance
Invoke-VsanCommand -Cluster $cluster -VsanCommand "proactive-rebalance start"
```

## HCX Migration Procedure

```bash
# Pre-migration checks:
# 1. Verify HCX service mesh is Green
# 2. Confirm Direct Connect bandwidth is adequate (1 Gbps for live vMotion)
# 3. Verify L2 network extension (NE) is active for the VM's network
# 4. Check that destination vSAN has sufficient free capacity

# Migrate a VM via HCX vMotion (zero-downtime)
# HCX UI → Migration → Migrate VMs
#   Source site: on-premises
#   Destination site: EVS
#   Migration type: vMotion
#   Target datastore: vsanDatastore
#   Target network: same as source (via NE) or new segment

# Post-migration:
# 1. Verify VM is reachable at same IP (if NE used)
# 2. Check vSAN policy applied to migrated VM
# 3. Remove NE for migrated networks once all VMs are moved
```
