---
tags:
  - aws
  - operations
description: "EVS operational procedures: adding and removing hosts, host replacement, vSAN rebalance, NSX-T segment and edge cluster management, VCF password rotation..."
---
# Amazon EVS — Procedures

<div class="kb-summary">
EVS operational procedures: adding and removing hosts, host replacement, vSAN rebalance, NSX-T segment and edge cluster management, VCF password rotation, vSAN storage policy updates, and HCX migration workflows.

*Applies to: Amazon EVS*
</div>

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Remove a Host

```d2
direction: right

A: "Pre-check: verify ≥4 hosts remain after removal" {shape: rectangle}
B: "vSphere Maintenance Mode\nwith vSAN full data evacuation" {shape: rectangle}
C: "vSAN Evacuate Data\nfrom host disk groups" {shape: rectangle}
E: "AWS: delete-environment-host" {shape: rectangle}
F: "Verify host removed\nfrom EVS host list" {shape: rectangle}
G: "Verify vSAN rebalance\ncompletes on remaining hosts" {shape: rectangle}
H: "Done — cluster healthy" {shape: rectangle}
D: "D" {shape: rectangle}

A -> B
B -> C
E -> F
F -> G
G -> H
```

```bash
# 1. Verify vSAN has enough hosts remaining (minimum 3 after removal; 4 for FTT=1 with full tolerance)
aws evs list-environment-hosts --environment-id $ENV_ID --query 'length(hostSummaries)'

# 2. Put host in maintenance mode with full data evacuation (PowerCLI)
Set-VMHost -VMHost "evs-host-01.vcf.internal" -State Maintenance -Evacuate $true
# Wait for VMs to vMotion off and vSAN to resync — check: Get-VMHost | Select Name, State

# 3. Wait for vSAN resync to complete (BytesToSync = 0)
Get-VsanResyncDashboard -Cluster (Get-Cluster) | Select BytesToSync, ActiveTasks

# 4. Delete host via EVS API
aws evs delete-environment-host --environment-id $ENV_ID --host-id host-xxx

# 5. Verify host is gone from host list
aws evs list-environment-hosts --environment-id $ENV_ID \
  --query 'hostSummaries[*].[hostId,hostName,state]' --output table

# 6. Verify vSAN rebalance on remaining hosts
Get-VsanResyncDashboard -Cluster (Get-Cluster) | Select BytesToSync, RecoveryETA
```


```text title="Expected output"
3

(no output — command completes silently)

BytesToSync ActiveTasks
----------- -----------
          0           0

(no output — command completes silently)

-----------------------------------------
|  hostId      |  hostName           |  state      |
-----------------------------------------
|  host-yyy    |  evs-host-02.vcf... |  ACTIVE     |
|  host-zzz    |  evs-host-03.vcf... |  ACTIVE     |
|  host-www    |  evs-host-04.vcf... |  ACTIVE     |
-----------------------------------------

BytesToSync RecoveryETA
----------- -----------
          0  00:00:00
```

!!! warning "Common errors"
    **`The host has 2 remaining hosts. Minimum 3 required for vSAN cluster.`** — Verify cluster size before removal or adjust FTT policy; use `aws evs describe-environment --environment-id $ENV_ID` to confirm host count.
    **`Set-VMHost : The object 'evs-host-01.vcf.internal' cannot be found.`** — Verify the exact hostname with `Get-VMHost | Select Name` and ensure vCenter connectivity with `Test-VcenterConnection`.
    **`An error occurred (ResourceNotFound) when calling the DeleteEnvironmentHost operation: Host host-xxx not found.`** — Confirm the correct host ID from `aws evs list-environment-hosts` output and ensure the host is in maintenance mode before deletion.
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

# 5. Verify vSAN automatically adds the host disk groups
Get-VsanDiskGroup | Where-Object { $_.VMHost.Name -eq "new-host.vcf.internal" }

# 6. Allow vSAN to rebalance (may take 1-4 hours depending on data volume)
Get-VsanResyncDashboard -Cluster (Get-Cluster) | Select BytesToSync
```


```text title="Expected output"
ACTIVE	ACTIVE	ACTIVE	ACTIVE	ACTIVE
{
    "hostId": "host-evs-0847",
    "state": "PROVISIONING"
}

Every 30.0s: aws evs list-environment-hosts --environment-id env-prod-cluster-01 ...

hostId              state
──────────────────  ──────────────
host-evs-0842       CREATED
host-evs-0843       CREATED
host-evs-0844       CREATED
host-evs-0845       CREATED
host-evs-0847       CREATED

CanonicalName                 : /vmfs/volumes/vsan:52d4a8c1-8f2e-4c2a-91b3-7e3c9a2f1d48
Disks                         : {naa.55cd2e404bd3c4a1, naa.55cd2e404bd3c4a2}
IsSsd                         : True
VMHost                        : new-host.vcf.internal
DiskCount                     : 2

BytesToSync : 847293456384
ResyncRate  : 12582912
TimeRemaining : 67200
```

!!! warning "Common errors"
    **`An error occurred (InvalidEnvironmentId) when calling the ListEnvironmentHosts operation: The environment ID 'env-prod-cluster-01' does not exist or you do not have access.`** — Verify the environment ID with `aws evs list-environments` and ensure your IAM role has `evs:ListEnvironmentHosts` permissions.
    **`error: watch: command not found`** — Install `procps` package with `apt-get install procps` or use `while true; do ... sleep 30; done` as an alternative.
    **`Get-VsanDiskGroup : The term 'Get-VsanDiskGroup' is not recognized`** — Load the vSAN PowerCLI module with `Import-Module VMware.VimAutomation.Vsan` before running PowerShell commands.
## Host Replacement (AWS-Initiated)

AWS performs the physical host replacement when a bare-metal host fails a hardware health check. AWS will notify you when the replacement host is available. Your responsibility is the VMware layer.

**Trigger:** AWS notifies via EVS event or CloudWatch alarm that a host has been replaced.

```bash
# 1. Confirm the new host appears in the EVS host list with state = ACTIVE
aws evs list-environment-hosts --environment-id $ENV_ID \
  --query 'hostSummaries[*].[hostId,hostName,state]' --output table

# 2. Verify the new host appears in vCenter as Connected
# vCenter → Hosts and Clusters → new host should be present and Connected
# If not connected after 15 min, verify VPC network connectivity to the host ENI

# 3. Verify ESXi configuration (NTP, syslog, DNS) was re-applied by VCF
# SDDC Manager automatically pushes host config during add; verify in vCenter

# 4. Verify vSAN disk groups were claimed on the new host
Get-VsanDiskGroup | Where-Object { $_.VMHost.Name -like "*new-host*" } | `
  Select VMHost, @{N="CacheDisks";E={($_.ExtensionData.SSD).Count}}, `
  @{N="CapacityDisks";E={($_.ExtensionData.NonSSD).Count}}

# If vSAN disk groups are missing, claim disks manually:
# vCenter → Cluster → Configure → vSAN → Disk Management → Claim Disks

# 5. Verify vSAN has resynced all objects to the new host (BytesToSync = 0)
Get-VsanResyncDashboard -Cluster (Get-Cluster) | Select BytesToSync, ActiveTasks, RecoveryETA

# 6. Verify NSX-T host transport node state is UP
# NSX Manager → System → Fabric → Nodes → Host Transport Nodes → new host = Success
curl -sk -u "admin:$NSX_PASS" "$NSX_URL/api/v1/transport-nodes" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for n in d.get('results', []):
    print(n['display_name'], n.get('state',''))
"

# 7. Verify VMs have been rebalanced via DRS (if DRS is set to Fully Automated)
Get-VM | Select Name, VMHost | Sort VMHost
```


```text title="Expected output"
---------------------------------------------------------------------------
|                        hostId                        |   hostName    | state  |
|---------------------------------------------------------------------------|
| host-12a4f8c9-7e2b-4d91-a3c2-9f1e8b6c5d3a          | esx-prod-04   | ACTIVE |
| host-98b3e7d2-1c4a-4f6b-8e9d-2a5c7b1f3e6h          | esx-prod-05   | ACTIVE |
---------------------------------------------------------------------------

VMHost                                    CacheDisks CapacityDisks
------                                    ---------- ---------------
esx-prod-04.corp.local                             2             10
esx-prod-05.corp.local                             2             10

BytesToSync ActiveTasks RecoveryETA
----------- ----------- -----------
          0           0 00:00:00

esx-prod-04.corp.local Success
esx-prod-05.corp.local Success

Name                                      VMHost
----                                      ------
prod-web-01                               esx-prod-01.corp.local
prod-web-02                               esx-prod-04.corp.local
prod-app-03                               esx-prod-02.corp.local
prod-app-04                               esx-prod-04.corp.local
prod-db-01                                esx-prod-03.corp.local
prod-db-02                                esx-prod-05.corp.local
```

!!! warning "Common errors"
    **`Get-VsanDiskGroup : The term 'Get-VsanDiskGroup' is not recognized`** — Load the VMware.VimAutomation.Vsan module with `Import-Module VMware.VimAutomation.Vsan` before running vSAN cmdlets.
    **`curl: (7) Failed to connect to nsxmgr.corp.local port 443: Connection timed out`** — Verify NSX Manager IP/hostname in `$NSX_URL` and confirm network connectivity from the jump host to the NSX Manager management interface.
    **`jq: command not found`** — Install `jq` with `apt-get install jq` or `yum install jq`, or use Python's json module as shown in the curl command for JSON parsing.
## VCF Password Rotation

Password rotation is required quarterly for most security policies. SDDC Manager manages all VCF component credentials.

**UI Method:** SDDC Manager → Administration → Credentials → Select all → Rotate

**API Method (for automation):**

```bash
SDDC_MANAGER="https://sddc-manager.vcf.internal"
SDDC_TOKEN=$(curl -sk -X POST \
  "${SDDC_MANAGER}/v1/tokens" \
  -H "Content-Type: application/json" \
  -d '{"username":"administrator@vsphere.local","password":"P@ssw0rd"}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('accessToken',''))")

# List all credentials managed by SDDC Manager
curl -sk -H "Authorization: Bearer ${SDDC_TOKEN}" \
  "${SDDC_MANAGER}/v1/credentials" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for c in d.get('elements', []):
    print(c.get('entityName',''), c.get('credentialType',''), c.get('username',''))
"

# Initiate rotation for all credentials
TASK_ID=$(curl -sk -X PATCH \
  -H "Authorization: Bearer ${SDDC_TOKEN}" \
  -H "Content-Type: application/json" \
  "${SDDC_MANAGER}/v1/credentials" \
  -d '{"operationType":"ROTATE","elements":[{"resourceName":"ALL"}]}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")

echo "Rotation task ID: ${TASK_ID}"

# Poll task status until complete
watch -n 30 "curl -sk -H 'Authorization: Bearer ${SDDC_TOKEN}' \
  ${SDDC_MANAGER}/v1/tasks/${TASK_ID} | \
  python3 -c \"import sys,json; d=json.load(sys.stdin); print(d.get('status',''), d.get('completionTimestamp',''))\""
```


```text title="Expected output"
vcsa-01.vcf.internal APPLIANCE root
vcsa-02.vcf.internal APPLIANCE root
nsx-manager-01.vcf.internal NSX_MANAGER admin
esxi-01.vcf.internal ESXI root
esxi-02.vcf.internal ESXI root
...
Rotation task ID: 550e8400-e29b-41d4-a716-446655440000
Every 30.0s: curl -sk -H 'Authorization: Bearer eyJhbGc...' https://sddc-manager.vcf.internal/v1/tasks/550e8400-e29b-41d4-a716-446655440000 | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status',''), d.get('completionTimestamp',''))"

RUNNING 
RUNNING 
RUNNING 
COMPLETED 2024-01-15T14:32:18.456Z
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to curl to skip SSL verification, or import the SDDC Manager certificate into your system trust store.
    **`jq: error (at <stdin>:1): Cannot index string with string "accessToken"`** — Verify the SDDC Manager credentials are correct and the `/v1/tokens` endpoint returned valid JSON; check the response with `curl -sk -X POST ... | python3 -m json.tool`.
    **`Authorization header missing or invalid`** — Ensure the `${SDDC_TOKEN}` variable is populated by checking `echo ${SDDC_TOKEN}` before running subsequent curl commands; re-authenticate if the token is empty or expired.
After rotation completes, update any external automation or scripts that reference VCF credentials.

## NSX-T Edge Cluster Scale-Out

Add Edge nodes when workloads have high North-South throughput requirements, or when existing Edge nodes are CPU or bandwidth saturated.

**When to scale out:** Edge node CPU sustained above 70%, or when adding gateway services (load balancers, NAT) that require additional capacity.

```bash
# Step 1: Deploy a new Edge VM from SDDC Manager or NSX Manager
# SDDC Manager handles Edge deployment in VCF environments — use SDDC Manager UI
# SDDC Manager → Workload Domains → Cluster → Add Edge Node

# If adding manually via NSX Manager (non-VCF-managed):
# NSX Manager → System → Fabric → Nodes → Edge Transport Nodes → Add Node
# Select form factor: Large (16 vCPU, 64 GB RAM recommended for production)
# Assign uplink profiles and transport zones matching existing Edge nodes

# Step 2: Once Edge node is deployed, verify it appears as a transport node
curl -sk -u "admin:$NSX_PASS" \
  "$NSX_URL/api/v1/transport-nodes?node_types=EdgeNode" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for n in d.get('results', []):
    print(n['display_name'], n.get('state',''))
"

# Step 3: Add the new Edge node to the existing Edge Cluster
# Get existing Edge Cluster ID
EDGE_CLUSTER_ID=$(curl -sk -u "admin:$NSX_PASS" \
  "$NSX_URL/api/v1/edge-clusters" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d['results'][0]['id'])")

# Get new Edge node transport node ID
NEW_EDGE_TN_ID=$(curl -sk -u "admin:$NSX_PASS" \
  "$NSX_URL/api/v1/transport-nodes?node_types=EdgeNode" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); [print(n['id']) for n in d['results'] if 'new-edge' in n['display_name']]")

# Add member to Edge Cluster via PUT (full replacement of member list)
curl -sk -X PUT -u "admin:$NSX_PASS" \
  -H "Content-Type: application/json" \
  "$NSX_URL/api/v1/edge-clusters/${EDGE_CLUSTER_ID}" \
  -d "{
    \"members\": [
      {\"transport_node_id\": \"<existing-edge-tn-id>\"},
      {\"transport_node_id\": \"${NEW_EDGE_TN_ID}\"}
    ]
  }"

# Step 4: Verify Edge Cluster member count and status
curl -sk -u "admin:$NSX_PASS" \
  "$NSX_URL/api/v1/edge-clusters/${EDGE_CLUSTER_ID}/status" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('member_statuses',[]))"
```


```text title="Expected output"
edge-01 UP
edge-02 UP
new-edge-01 UP
edge-cluster-1
tn-edge-02-uuid-a1b2c3d4e5f6
[{'transport_node_id': 'tn-edge-01-uuid-9x8y7z6w5v4u', 'status': 'UP', 'realtime_status': 'REALIZED'}, {'transport_node_id': 'tn-edge-02-uuid-a1b2c3d4e5f6', 'status': 'UP', 'realtime_status': 'REALIZED'}]
```

!!! warning "Common errors"
    **`jq: error (at <stdin>:0): Cannot index array with string "results"`** — Verify NSX_URL is correct and the API endpoint is returning valid JSON; test with `curl -sk -u "admin:$NSX_PASS" "$NSX_URL/api/v1/edge-clusters" | head -20`.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command or configure NSX Manager certificate in your CA bundle; the `-sk` flags should suppress this but verify NSX_URL uses https.
    **`ValueError: No JSON object could be decoded`** — Ensure NSX_PASS is set correctly and the admin user has API permissions; test authentication with `curl -sk -u "admin:$NSX_PASS" "$NSX_URL/api/v1/transport-nodes" -w "\n%{http_code}\n"` to check for 401 responses.
## vSAN Storage Policy Update

Storage policies (SPBM) control the data protection level for VM objects. Update policies when changing FTT, RAID type, or adding encryption requirements.

```bash
# Step 1: Create a new SPBM policy via PowerCLI
$policy = New-SpbmStoragePolicy -Name "EVS-FTT2-RAID1" -Description "FTT=2 RAID-1 mirroring" `
  -AnyOfRuleSets @(
    New-SpbmRuleSet -AllOfRules @(
      New-SpbmRule -Capability (Get-SpbmCapability -Name "VSAN.hostFailuresToTolerate") -Value 2,
      New-SpbmRule -Capability (Get-SpbmCapability -Name "VSAN.replicaPreference") -Value "RAID-1 (Mirroring) - Performance"
    )
  )

# Step 2: Check compliance of existing VMs against the new policy
Get-VM | Get-SpbmEntityConfiguration | `
  Select Entity, StoragePolicy, @{N="Compliant";E={$_.ComplianceStatus}}

# Step 3: Apply the new policy to a specific VM
$vm = Get-VM -Name "myvm"
Set-SpbmEntityConfiguration -Configuration (Get-SpbmEntityConfiguration $vm) `
  -StoragePolicy $policy

# Step 4: Apply policy to all VMDKs of a VM
Get-VM -Name "myvm" | Get-HardDisk | `
  Set-SpbmEntityConfiguration -StoragePolicy $policy

# Step 5: Check compliance status after applying
Get-VM -Name "myvm" | Get-SpbmEntityConfiguration | `
  Select Entity, StoragePolicy, ComplianceStatus

# Step 6: Run a cluster-wide compliance check
Get-Cluster -Name "EVS-Management-Cluster" | Get-VM | Get-SpbmEntityConfiguration | `
  Where-Object { $_.ComplianceStatus -ne "compliant" } | `
  Select Entity, StoragePolicy, ComplianceStatus
```


```text title="Expected output"
Name                          : EVS-FTT2-RAID1
Description                   : FTT=2 RAID-1 mirroring
ResourceType                  : Storage
CreationTime                  : 2024-01-15 14:32:18
ModifiedTime                  : 2024-01-15 14:32:18

Entity                         StoragePolicy              Compliant
------                         ---------------            ---------
myvm                           vSAN Default Policy        compliant
web-app-01                     EVS-FTT2-RAID1             compliant
db-server-02                   vSAN Default Policy        nonCompliant
cache-node-03                  EVS-FTT2-RAID1             compliant
...

Entity                         StoragePolicy              ComplianceStatus
------                         ---------------            -----------------
myvm                           EVS-FTT2-RAID1             compliant

Entity                         StoragePolicy              ComplianceStatus
------                         ---------------            -----------------
db-server-02                   EVS-FTT2-RAID1             nonCompliant
legacy-app-vm                  vSAN Default Policy        nonCompliant
backup-staging-01              EVS-FTT2-RAID1             nonCompliant
```

!!! warning "Common errors"
    **`Get-SpbmCapability : The term 'Get-SpbmCapability' is not recognized`** — Load the VMware.VimAutomation.Storage module with `Import-Module VMware.VimAutomation.Storage` before running SPBM commands.
    **`Set-SpbmEntityConfiguration : Cannot bind argument to parameter 'StoragePolicy' because it is null`** — Ensure the policy variable `$policy` was successfully created in Step 1 by running `$policy | Get-Member` to verify the object exists.
    **`Get-VM : The specified VM 'myvm' was not found`** — Verify the VM name matches exactly (case-sensitive) using `Get-VM | Select Name` to list available VMs in the connected vCenter.
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


```text title="Expected output"
{
  "id": "logical-switch-70001",
  "display_name": "workload-web-01",
  "transport_zone_id": "tz-overlay-prod-01",
  "replication_mode": "MTEP",
  "admin_state": "UP",
  "vni": 70001,
  "resource_type": "LogicalSwitch",
  "_create_time": 1699564823456,
  "_last_modified_time": 1699564823456,
  "_system_owned": false,
  "_protection": "NOT_PROTECTED",
  "revision": 0
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command (already present in example) or import the NSX Manager certificate into your system trust store.
    **`{"error_code":400,"error_message":"Invalid transport_zone_id"}`** — Replace `<overlay-tz-id>` with an actual transport zone UUID from your NSX deployment (retrieve via `curl -sk -u "admin:$NSX_PASSWORD" "$NSX_URL/api/v1/transport-zones"`).
    **`curl: (7) Failed to connect to $NSX_URL port 443: Connection refused`** — Verify `$NSX_URL` environment variable is set correctly (e.g., `export NSX_URL=https://nsx-manager.example.com`) and NSX Manager is reachable on the network.
## vSAN Rebalance

```bash
# Trigger manual vSAN rebalance (PowerCLI)
$cluster = Get-Cluster -Name "EVS-Management-Cluster"

# Check current vSAN disk balance across hosts
$vsanHealth = Get-VsanView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system"
$health = $vsanHealth.QueryVsanClusterHealthSummary($cluster.Id,$null,$null,$true,$null,$null,"defaultView")
$health.Groups | Select GroupName, GroupHealth

# Trigger proactive rebalance via vSAN API
Invoke-VsanCommand -Cluster $cluster -VsanCommand "proactive-rebalance start"

# Monitor rebalance progress
Get-VsanResyncDashboard -Cluster $cluster | Select BytesToSync, ActiveTasks, RecoveryETA
```


```text title="Expected output"
GroupName                          GroupHealth
---------                          -----------
Capacity                           Healthy
Performance                        Healthy
Network                            Healthy
Disk Balance                        Warning
Memory                              Healthy

Proactive rebalance initiated on cluster EVS-Management-Cluster
Rebalance job ID: 4a7c9e2f-b1d3-4e8a-9f2c-5d6e7f8a9b0c
Status: In Progress

BytesToSync                        ActiveTasks    RecoveryETA
-----------                        -----------    -----------
847.3 GB                           12             00:45:23
```

!!! warning "Common errors"
    **`Get-VsanView : The term 'Get-VsanView' is not recognized`** — Import the VMware.VimAutomation.Vsan module with `Import-Module VMware.VimAutomation.Vsan` before running the script.
    **`Invoke-VsanCommand : Cluster 'EVS-Management-Cluster' is not vSAN enabled`** — Verify the cluster name matches exactly and that vSAN is enabled on the cluster with `Get-Cluster | Get-VsanClusterConfiguration`.
## HCX Migration Procedure

```bash
# Pre-migration checks:
# 1. Verify HCX service mesh is Green
# 2. Confirm Direct Connect bandwidth is adequate (1 Gbps for live vMotion)
# 3. Verify L2 network extension (NE) is active for the VM network
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

---

## See also

- [Amazon EVS — Health Checks](../health-checks/)
- [Amazon EVS — Common Issues](../../troubleshooting/common-issues/)
- [Amazon EVS — CLI Reference](../cli-reference/)

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
