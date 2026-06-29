---
tags:
  - aws
  - operations
---
# Amazon EVS — CLI Reference

<div class="kb-summary">
AWS CLI commands for EVS cluster and host management, PowerCLI for vSphere operations, NSX-T REST API for network queries, and HCX API for migration management on EVS bare-metal hosts.

*Applies to: Amazon EVS*
</div>
![Amazon EVS — CLI Reference](../../../../assets/cloud-aws-evs-operations-cli-reference.svg)

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## EVS CLI Quick Reference

| Action | Command |
|---|---|
| List all environments | `aws evs list-environments --output table` |
| Get environment details | `aws evs get-environment --environment-id env-xxx` |
| List hosts in environment | `aws evs list-environment-hosts --environment-id env-xxx --output table` |
| Get a specific host | `aws evs get-environment-host --environment-id env-xxx --host-id host-xxx` |
| Add a host | `aws evs create-environment-host --environment-id env-xxx --host '{...}'` |
| Remove a host | `aws evs delete-environment-host --environment-id env-xxx --host-id host-xxx` |
| List environment VLANs | `aws evs list-environment-vlans --environment-id env-xxx` |
| Create new environment | `aws evs create-environment --cli-input-json file://evs-env.json` |
| Check environment tags | `aws evs list-tags-for-resource --resource-arn arn:aws:evs:...` |
| Update environment tags | `aws evs tag-resource --resource-arn arn:aws:evs:... --tags Key=Env,Value=prod` |

## AWS EVS CLI

### list-environments

```bash
aws evs list-environments \
  --query 'environmentSummaries[*].[environmentId,environmentName,state,createdAt]' \
  --output table
```


```text title="Expected output"
---------------------------------------------------------------------------------------------------------
|                                    environmentSummaries                                              |
+----------+---------------------------+---------------+---------------------------+
|  env-a7f2b9c1d4e5  |  production-us-east-1   |  ACTIVE       |  2024-01-15T09:23:47Z    |
|  env-c3k8m2n9p1q6  |  staging-us-west-2      |  ACTIVE       |  2024-01-10T14:52:31Z    |
|  env-e9r5s7t2u4v8  |  development-eu-west-1  |  INACTIVE     |  2023-12-28T11:18:09Z    |
|  env-f1w3x6y8z2a4  |  qa-ap-southeast-1      |  ACTIVE       |  2024-01-12T16:45:22Z    |
|  env-h5b7c9d1e3f6  |  legacy-us-east-1       |  TERMINATING  |  2023-11-05T08:31:15Z    |
---------------------------------------------------------------------------------------------------------
```

!!! warning "Common errors"
    **`An error occurred (UnauthorizedOperation) exception has occurred: User: arn:aws:iam::123456789012:user/admin is not authorized to perform: evs:ListEnvironments on resource: *`** — Ensure the IAM user or role has the `evs:ListEnvironments` permission attached in their policy.
    **`Unable to locate credentials. You can configure credentials by running "aws configure".`** — Configure AWS credentials using `aws configure` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables.
Expected output structure:

```text
----------------------------------------------------------
|               ListEnvironments                         |
+----------------+-------------------+---------+---------+
|  env-0a1b2c3d  |  evs-prod-cluster |  ACTIVE | 2024-01 |
|  env-9z8y7x6w  |  evs-dev-cluster  |  ACTIVE | 2024-03 |
+----------------+-------------------+---------+---------+
```

### get-environment

```bash
aws evs get-environment --environment-id env-0a1b2c3d
```


```text title="Expected output"
{
    "environment": {
        "environmentId": "env-0a1b2c3d",
        "name": "production-web-cluster",
        "status": "ACTIVE",
        "createdAt": "2024-01-15T09:32:47Z",
        "region": "us-east-1",
        "vpcId": "vpc-8f4a9e2b",
        "subnetIds": [
            "subnet-12345678",
            "subnet-87654321"
        ],
        "securityGroupIds": [
            "sg-0a1b2c3d"
        ],
        "instanceType": "t3.large",
        "desiredCapacity": 3,
        "currentCapacity": 3,
        "tags": {
            "Environment": "production",
            "Team": "platform"
        }
    }
}
```

!!! warning "Common errors"
    **`An error occurred (ResourceNotFoundException) when calling the GetEnvironment operation: Environment env-0a1b2c3d not found`** — Verify the environment ID is correct and exists in the current region using `aws evs list-environments`.
    **`An error occurred (AccessDeniedException) when calling the GetEnvironment operation: User is not authorized to perform: evs:GetEnvironment`** — Add the `evs:GetEnvironment` permission to your IAM user or role policy.
    **`Unable to locate credentials`** — Configure AWS credentials using `aws configure` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables.
Extract key fields with `--query`:

```bash
aws evs get-environment --environment-id env-0a1b2c3d \
  --query 'environment.{ID:environmentId,Name:environmentName,State:state,VcfVersion:vcfVersion,VPCID:vpcId}' \
  --output table
```


```text title="Expected output"
-------------------------------------------
|                    Environment Details   |
+-------------------------------------------+
|  ID          | env-0a1b2c3d              |
|  Name        | prod-vcf-cluster-01       |
|  State       | ACTIVE                    |
|  VcfVersion  | 5.2.1                     |
|  VPCID       | vpc-0f8e9d7c5b2a1e4f      |
-------------------------------------------
```

!!! warning "Common errors"
    **`An error occurred (InvalidEnvironmentId.NotFound) when calling the GetEnvironment operation: Environment env-0a1b2c3d not found`** — Verify the environment ID exists in your region using `aws evs list-environments`.
    **`An error occurred (AccessDenied) when calling the GetEnvironment operation: User is not authorized to perform: evs:GetEnvironment`** — Add the `evs:GetEnvironment` permission to your IAM user or role policy.
    **`Unable to locate credentials`** — Configure AWS credentials using `aws configure` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables.
### create-environment

```bash
aws evs create-environment \
  --environment-name evs-prod-cluster \
  --kms-key-id arn:aws:kms:us-east-1:123456789012:key/mrk-xxx \
  --vcf-version VCF-5.1 \
  --connectivity-info '{"privateRouteServerPeerings":[{"routeServerId":"rts-xxx"}]}' \
  --vcf-host-names '["evs-host-01","evs-host-02","evs-host-03","evs-host-04"]' \
  --vcenter-configuration '{"datastoreName":"vsanDatastore","rootPassword":"P@ssw0rd!","vmFolderName":"management-vms"}' \
  --nsx-configuration '{"nsxManagerRootPassword":"P@ssw0rd!","overlaySubnetwork":"192.168.100.0/26"}' \
  --initial-vlans '[{"cidr":"10.0.10.0/24","mtu":9000,"vlanId":10,"vlanType":"vmotionVlan"}]'
```


```text title="Expected output"
{
    "environmentId": "env-0a1b2c3d4e5f6g7h",
    "environmentName": "evs-prod-cluster",
    "vcfVersion": "VCF-5.1",
    "status": "CREATING",
    "creationTime": "2024-01-15T14:32:18.456Z",
    "kmsKeyId": "arn:aws:kms:us-east-1:123456789012:key/mrk-xxx",
    "hostCount": 4,
    "connectivityStatus": "PENDING",
    "operationId": "op-8f9g0h1i2j3k4l5m"
}
```

!!! warning "Common errors"
    **`An error occurred (InvalidParameterException) when calling the CreateEnvironment operation: Invalid KMS key ARN format or key does not exist`** — Verify the KMS key ARN exists in the specified region and your IAM principal has kms:DescribeKey permissions.
    **`An error occurred (ValidationException) when calling the CreateEnvironment operation: VCF version VCF-5.1 is not supported in this region`** — Check the AWS documentation for supported VCF versions in us-east-1 or switch to a supported version.
    **`An error occurred (InvalidParameterException) when calling the CreateEnvironment operation: Invalid VLAN configuration: MTU 9000 exceeds maximum allowed value`** — Reduce the MTU value to 1500 or verify your network infrastructure supports jumbo frames before retrying.
### create-environment-host

```bash
aws evs create-environment-host \
  --environment-id env-0a1b2c3d \
  --host '{
    "instanceType": "i4i.metal",
    "keyName": "evs-cluster-key",
    "hostName": "evs-host-05",
    "placementGroupId": "pg-xxx"
  }'
```


```text title="Expected output"
{
    "environmentHostId": "eh-f7a9e2c1b4d6",
    "environmentId": "env-0a1b2c3d",
    "hostName": "evs-host-05",
    "instanceType": "i4i.metal",
    "instanceId": "i-0d7f2a9c1e5b3f8a",
    "keyName": "evs-cluster-key",
    "placementGroupId": "pg-xxx",
    "state": "PROVISIONING",
    "launchTime": "2024-01-15T14:32:47.000Z",
    "publicIpAddress": "54.192.47.183",
    "privateIpAddress": "10.18.5.42",
    "tags": []
}
```

!!! warning "Common errors"
    **`An error occurred (InvalidParameterValue) when calling the CreateEnvironmentHost operation: Invalid environment ID: env-0a1b2c3d`** — Verify the environment exists with `aws evs describe-environments` and use a valid environment ID.
    **`An error occurred (InvalidKeyPair.NotFound) when calling the CreateEnvironmentHost operation: The key pair 'evs-cluster-key' does not exist`** — Create the key pair first with `aws ec2 create-key-pair --key-name evs-cluster-key` or use an existing key name.
    **`An error occurred (InvalidParameterValue) when calling the CreateEnvironmentHost operation: Placement group pg-xxx does not exist or is not available`** — Create the placement group with `aws ec2 create-placement-group --group-name pg-xxx --strategy cluster` before launching the host.
Expected output:

```json
{
    "host": {
        "hostId": "host-05abcdef",
        "environmentId": "env-0a1b2c3d",
        "instanceType": "i4i.metal",
        "state": "CREATING",
        "createdAt": "2024-06-11T10:00:00Z"
    }
}
```

### list-environment-hosts

```bash
aws evs list-environment-hosts --environment-id env-0a1b2c3d \
  --query 'hostSummaries[*].[hostId,hostName,instanceType,state,createdAt]' \
  --output table
```


```text title="Expected output"
---------------------------------------------------------------------------------------------------------
|                                    listEnvironmentHosts                                              |
+------------------+------------------------+---------------+----------+---------------------------+
| hostId           | hostName               | instanceType  | state    | createdAt                 |
+------------------+------------------------+---------------+----------+---------------------------+
| host-f4e8a9b2c1  | evs-worker-prod-01     | t3.xlarge     | RUNNING  | 2024-01-15T09:23:47.000Z  |
| host-d7c2e5f1a9  | evs-worker-prod-02     | t3.xlarge     | RUNNING  | 2024-01-15T09:24:12.000Z  |
| host-b3a6c8e2f5  | evs-worker-prod-03     | t3.xlarge     | STOPPED  | 2024-01-15T09:24:38.000Z  |
| host-e1f9a4c6d2  | evs-bastion-prod       | t3.large      | RUNNING  | 2024-01-14T14:51:22.000Z  |
| host-c5b2d7e9a1  | evs-monitor-prod       | t3.medium     | RUNNING  | 2024-01-14T14:52:05.000Z  |
+------------------+------------------------+---------------+----------+---------------------------+
```

!!! warning "Common errors"
    **`An error occurred (ResourceNotFoundException) when calling the ListEnvironmentHosts operation: Environment env-0a1b2c3d not found`** — Verify the environment ID is correct using `aws evs list-environments`.
    **`An error occurred (AccessDeniedException) when calling the ListEnvironmentHosts operation: User is not authorized to perform: evs:ListEnvironmentHosts`** — Add the `evs:ListEnvironmentHosts` permission to your IAM policy.
    **`Unable to locate credentials`** — Configure AWS credentials using `aws configure` or set `AWS_PROFILE`, `AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY` environment variables.
Filter only ACTIVE hosts:

```bash
aws evs list-environment-hosts --environment-id env-0a1b2c3d \
  --query 'hostSummaries[?state==`ACTIVE`].[hostId,hostName,instanceType]' \
  --output table
```


```text title="Expected output"
-----------------------------------------
|                 hostId                  |      hostName      | instanceType |
|-----------------------------------------|--------------------|--------------| 
| host-0f8e9d7c6b5a4321                  | evs-prod-web-01    | m5.xlarge    |
| host-1a2b3c4d5e6f7g8h                  | evs-prod-web-02    | m5.xlarge    |
| host-2x9y8z7w6v5u4t3s                  | evs-prod-db-01     | r5.2xlarge   |
| host-3p2o1n0m9l8k7j6i                  | evs-prod-cache-01  | c5.large     |
| host-4q3r2s1t0u9v8w7x                  | evs-prod-api-01    | m5.2xlarge   |
-----------------------------------------
```

!!! warning "Common errors"
    **`An error occurred (InvalidParameterException) when calling the ListEnvironmentHosts operation: Invalid environment ID format`** — Verify the environment ID matches the format `env-` followed by alphanumeric characters using `aws evs describe-environments`.
    **`An error occurred (AccessDeniedException) when calling the ListEnvironmentHosts operation: User is not authorized to perform: evs:ListEnvironmentHosts`** — Add the `evs:ListEnvironmentHosts` permission to your IAM policy or assume a role with EVS read access.
### delete-environment-host

Always put the ESXi host in vSphere maintenance mode and verify vSAN BytesToSync is 0 before running this command.

```bash
aws evs delete-environment-host \
  --environment-id env-0a1b2c3d \
  --host-id host-01abcdef
```


```text title="Expected output"
{
    "environmentId": "env-0a1b2c3d",
    "hostId": "host-01abcdef",
    "status": "DELETION_IN_PROGRESS",
    "requestId": "req-f7e2d9c4-8b1a-4f6e-9d2e-1c3b5a7f9e2d",
    "timestamp": "2024-01-15T14:32:18.456Z"
}
```

!!! warning "Common errors"
    **`An error occurred (ResourceNotFoundException) when calling the DeleteEnvironmentHost operation: Environment env-0a1b2c3d not found`** — Verify the environment ID exists with `aws evs describe-environments` and use the correct ID.
    **`An error occurred (InvalidParameterException) when calling the DeleteEnvironmentHost operation: Host host-01abcdef is not part of environment env-0a1b2c3d`** — Confirm the host belongs to the specified environment using `aws evs describe-environment-hosts --environment-id env-0a1b2c3d`.
    **`An error occurred (ConflictException) when calling the DeleteEnvironmentHost operation: Cannot delete host in DELETION_IN_PROGRESS state`** — Wait for the previous deletion to complete before attempting another delete operation.
Poll until the host is removed:

```bash
watch -n 30 "aws evs list-environment-hosts --environment-id env-0a1b2c3d \
  --query 'hostSummaries[*].[hostId,hostName,state]' --output table"
```


```text title="Expected output"
Every 30.0s: aws evs list-environment-hosts --environment-id env-0a1b2c3d --query 'hostSummaries[*].[hostId,hostName,state]' --output table

|  hostId  |      hostName      |  state   |
|----------|--------------------|----------|
| host-001 | evs-worker-01.prod | RUNNING  |
| host-002 | evs-worker-02.prod | RUNNING  |
| host-003 | evs-worker-03.prod | RUNNING  |
| host-004 | evs-control-01.prod| HEALTHY  |
| host-005 | evs-control-02.prod| HEALTHY  |
```

!!! warning "Common errors"
    **`An error occurred (InvalidParameterException) when calling the ListEnvironmentHosts operation: Invalid environment ID format`** — Verify the environment ID matches the pattern `env-` followed by alphanumeric characters using `aws evs describe-environments --query 'environments[*].environmentId'`.
    **`Unable to locate credentials`** — Configure AWS credentials using `aws configure` or ensure the `AWS_PROFILE`, `AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY` environment variables are set.
    **`An error occurred (AccessDeniedException) when calling the ListEnvironmentHosts operation: User is not authorized to perform: evs:ListEnvironmentHosts`** — Add the `evs:ListEnvironmentHosts` permission to your IAM user or role policy.
## vSphere PowerCLI

Connect to vCenter before running any PowerCLI commands:

```powershell
Connect-VIServer -Server vcenter.vcf.internal \
  -User administrator@vsphere.local \
  -Password 'P@ssw0rd'
```

### Cluster and Host Queries

```powershell
# All clusters with HA and DRS status
Get-Cluster | Select Name, HAEnabled, DRSEnabled, @{N="Hosts";E={($_ | Get-VMHost).Count}}

# Hosts in a specific cluster
Get-Cluster -Name "EVS-Management-Cluster" | Get-VMHost | `
  Select Name, ConnectionState, PowerState, NumCpu, MemoryTotalGB, MemoryUsageGB

# Hosts filtered by connection state
Get-VMHost | Where-Object { $_.ConnectionState -eq "Connected" } | `
  Select Name, NumCpu, MemoryTotalGB

# Hosts with low free memory (flag those with <10% free)
Get-VMHost | Select Name, MemoryTotalGB, MemoryUsageGB, `
  @{N="MemFreePct";E={[math]::Round((1-($_.MemoryUsageGB/$_.MemoryTotalGB))*100,1)}} | `
  Where-Object { $_.MemFreePct -lt 10 }
```

### VM Queries

```powershell
# All VMs with host and power state
Get-VM | Select Name, PowerState, NumCpu, MemoryGB, @{N="Host";E={$_.VMHost.Name}} | Sort Name

# VMs on a specific datastore
Get-Datastore -Name "vsanDatastore" | Get-VM | Select Name, PowerState, VMHost

# Powered-off VMs only
Get-VM | Where-Object { $_.PowerState -eq "PoweredOff" } | Select Name, VMHost

# VMs by CPU usage (descending)
Get-VM | Where-Object { $_.PowerState -eq "PoweredOn" } | `
  Select Name, @{N="CPUUsageMHz";E={$_.ExtensionData.Summary.QuickStats.OverallCpuUsage}} | `
  Sort CPUUsageMHz -Descending | Select -First 10
```

### Datastore Queries

```powershell
# All datastores with capacity
Get-Datastore | Select Name, Type, CapacityGB, FreeSpaceGB, `
  @{N="UsedGB";E={[math]::Round($_.CapacityGB - $_.FreeSpaceGB,1)}}, `
  @{N="UsedPct";E={[math]::Round((1-($_.FreeSpaceGB/$_.CapacityGB))*100,1)}}

# vSAN datastore free space alert (flag if <20% free)
Get-Datastore -Name "vsanDatastore" | `
  Select Name, CapacityGB, FreeSpaceGB, `
  @{N="FreePct";E={[math]::Round(($_.FreeSpaceGB/$_.CapacityGB)*100,1)}}
```

### vSAN Health and Resync

```powershell
# vSAN cluster health summary
$cluster = Get-Cluster -Name "EVS-Management-Cluster"
$vsanHealth = Get-VsanView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system"
$result = $vsanHealth.QueryVsanClusterHealthSummary($cluster.Id,$null,$null,$true,$null,$null,"defaultView")
$result.Groups | Select GroupName, GroupHealth

# vSAN disk groups per host
Get-VsanDiskGroup | Select VMHost, `
  @{N="CacheDisks";E={($_.ExtensionData.SSD).Count}}, `
  @{N="CapacityDisks";E={($_.ExtensionData.NonSSD).Count}}

# vSAN resync status (BytesToSync must be 0 before removing a host)
Get-VsanResyncDashboard -Cluster (Get-Cluster "EVS-Management-Cluster") | `
  Select BytesToSync, RecoveryETA
```

### vMotion and Maintenance Mode

```powershell
# Move VM to a specific host (vMotion)
Move-VM -VM "myvm" -Destination (Get-VMHost "evs-host-02.vcf.internal")

# Move all VMs from a host to the cluster (DRS-based placement)
$src = Get-VMHost "evs-host-01.vcf.internal"
Get-VM -Location $src | Move-VM -Destination (Get-Cluster "EVS-Management-Cluster")

# Put host in maintenance mode with vSAN full data evacuation
Set-VMHost -VMHost "evs-host-01.vcf.internal" -State Maintenance -Evacuate $true

# Exit maintenance mode
Set-VMHost -VMHost "evs-host-01.vcf.internal" -State Connected
```

## NSX-T API

Set variables before running curl commands:

```bash
NSX_MANAGER="https://nsx-manager.vcf.internal"
NSX_USER="admin"
NSX_PASS="VMware1!VMware1!"
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`bash: NSX_MANAGER: command not found`** — Ensure you are using `export` before the variable name if you intend to set it as an environment variable, or remove the leading space if copy-pasted incorrectly.
    **`bash: syntax error near unexpected token '!'`** — Escape the exclamation mark in the password with a backslash (`VMware1\!VMware1\!`) or wrap the entire password in single quotes instead of double quotes.
### Cluster Status

```bash
curl -sk -u "${NSX_USER}:${NSX_PASS}" \
  "${NSX_MANAGER}/api/v1/cluster/status" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); \
  [print(f'{k}: {v}') for k,v in d.items() if k in ['control_cluster_status','mgmt_cluster_status']]"
```


```text title="Expected output"
control_cluster_status: STABLE
mgmt_cluster_status: STABLE
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip certificate verification, or import the NSX Manager's CA certificate into your system trust store.
    **`jq: command not found`** — Use `python3 -c` with json module (as shown) instead of piping to jq, or install jq with `apt-get install jq` / `yum install jq`.
    **`curl: (7) Failed to connect to <NSX_MANAGER>: Name or service not known`** — Verify the `NSX_MANAGER` environment variable is set correctly with `echo $NSX_MANAGER` and that the hostname/IP is resolvable from your network.
### Transport Nodes

```bash
# List all transport nodes
curl -sk -u "${NSX_USER}:${NSX_PASS}" \
  "${NSX_MANAGER}/api/v1/transport-nodes" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for n in d.get('results', []):
    print(n['display_name'], n.get('resource_type',''), n.get('state',''))
"

# Filter Edge Nodes only
curl -sk -u "${NSX_USER}:${NSX_PASS}" \
  "${NSX_MANAGER}/api/v1/transport-nodes?node_types=EdgeNode" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for n in d.get('results', []):
    print(n['display_name'], n.get('state',''))
"

# Filter Host Nodes only
curl -sk -u "${NSX_USER}:${NSX_PASS}" \
  "${NSX_MANAGER}/api/v1/transport-nodes?node_types=HostNode" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for n in d.get('results', []):
    print(n['display_name'], n.get('state',''))
"
```


```text title="Expected output"
edge-node-01 EdgeNode UP
edge-node-02 EdgeNode UP
host-node-esx01.lab.local HostNode UP
host-node-esx02.lab.local HostNode UP
host-node-esx03.lab.local HostNode UP
edge-node-01 UP
edge-node-02 UP
host-node-esx01.lab.local UP
host-node-esx02.lab.local UP
host-node-esx03.lab.local UP
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to 192.168.1.50 port 443: Connection refused`** — Verify NSX_MANAGER variable is set correctly and the NSX appliance is reachable on the network.
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`** — Confirm NSX_USER and NSX_PASS credentials are correct; invalid credentials return HTML error pages instead of JSON.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Remove the `-k` flag only if using a trusted certificate, or ensure your CA bundle includes the NSX manager's certificate.
### Logical Routers

```bash
curl -sk -u "${NSX_USER}:${NSX_PASS}" \
  "${NSX_MANAGER}/api/v1/logical-routers" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for r in d.get('results', []):
    print(r['display_name'], r['router_type'], r.get('high_availability_mode',''))
"
```


```text title="Expected output"
tier0-prod-router TIER0 ACTIVE-ACTIVE
tier1-web-router TIER1 ACTIVE-STANDBY
tier1-db-router TIER1 ACTIVE-STANDBY
tier1-mgmt-router TIER1 
edge-cluster-router TIER0 ACTIVE-ACTIVE
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip SSL verification (already present in the example, but ensure it's not removed).
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`** — Verify NSX_MANAGER, NSX_USER, and NSX_PASS environment variables are set correctly and the API endpoint is reachable.
    **`curl: (7) Failed to connect to <hostname> port 443: Connection refused`** — Confirm the NSX Manager hostname/IP is correct and the management cluster is running and accessible from your network.
### Firewall Sections

```bash
curl -sk -u "${NSX_USER}:${NSX_PASS}" \
  "${NSX_MANAGER}/api/v1/firewall/sections" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for s in d.get('results', []):
    rule_count = s.get('rule_count', 0)
    print(f\"{s['display_name']:<40} rules={rule_count:<5} type={s.get('section_type','')}\")
"
```


```text title="Expected output"
Infrastructure                           rules=12   type=LAYER3
DMZ-Ingress                              rules=8    type=LAYER3
Database-Protection                      rules=15   type=LAYER3
Kubernetes-Egress                        rules=6    type=LAYER3
Legacy-Systems                           rules=23   type=LAYER3
Default-Drop                             rules=1    type=LAYER3
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to 192.168.1.50 port 443: Connection refused`** — Verify NSX Manager is running and accessible at the hostname/IP specified in `$NSX_MANAGER`, and check network connectivity.
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`** — Confirm `$NSX_USER` and `$NSX_PASS` credentials are correct; invalid credentials return HTML error pages instead of JSON.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Remove the `-k` flag only if using a trusted certificate, or ensure your environment accepts self-signed certificates for NSX Manager.
## HCX API

Set variables before running HCX commands:

```bash
HCX_MANAGER="https://hcx-cloud.vcf.internal"
HCX_USER="administrator@vsphere.local"
HCX_PASS="P@ssw0rd"
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`bash: HCX_MANAGER: command not found`** — Ensure you are using `=` without spaces around the equals sign for variable assignment.
    **`bash: administrator@vsphere.local: command not found`** — Verify the entire variable assignment is on one line and properly quoted if the value contains special characters.
Authenticate and get a session token:

```bash
HCX_TOKEN=$(curl -sk -X POST \
  "${HCX_MANAGER}/hybridity/api/sessions" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"${HCX_USER}\",\"password\":\"${HCX_PASS}\"}" | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('data',{}).get('token',''))")
```


```text title="Expected output"
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTcwOTMxNjgwMCwiaWF0IjoxNzA5MzAwNDAwLCJqdGkiOiI0ZjU4YTJjYy1lYzQyLTQ0ZDItOWY0Yi1hYzNmNWI2ZDc4OTAifQ.kX9mZ2pL8qR5vN3jW7sT4uY6bA9cD2eF1gH0jK4mN5o
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to port 443: Connection refused`** — Verify the HCX_MANAGER variable is set correctly and the HCX appliance is reachable on the network.
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`** — Check that HCX_USER and HCX_PASS credentials are correct; the API returned an error response instead of valid JSON.
    **`KeyError: 'data'`** — Confirm the HCX API version matches your documentation; the response structure may differ if the token is at a different path in the JSON hierarchy.
### Service Mesh Status

```bash
curl -sk -H "x-hm-authorization: ${HCX_TOKEN}" \
  "${HCX_MANAGER}/hybridity/api/interconnect/links" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for link in d.get('data', []):
    print(link.get('displayName',''), link.get('status',''), link.get('endpointType',''))
"
```


```text title="Expected output"
HCX-Link-01 UP CLOUD
HCX-Link-02 UP ON_PREMISES
HCX-Link-03 DOWN ON_PREMISES
HCX-Link-04 UP CLOUD
HCX-Link-05 DEGRADED ON_PREMISES
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip SSL verification (already present in the example, but ensure it's not removed).
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`** — Verify the HCX_TOKEN and HCX_MANAGER environment variables are set correctly with `echo $HCX_TOKEN` and `echo $HCX_MANAGER`.
    **`curl: (7) Failed to connect to <manager-ip> port 443: Connection refused`** — Confirm the HCX Manager is running and accessible at the specified endpoint with `curl -sk https://${HCX_MANAGER}/hybridity/api/health`.
### Migration Job Status

```bash
curl -sk -H "x-hm-authorization: ${HCX_TOKEN}" \
  "${HCX_MANAGER}/hybridity/api/vmotion/jobs" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for job in d.get('data', []):
    print(job.get('displayName',''), job.get('state',''), job.get('progressPercent',''), '%')
"
```


```text title="Expected output"
vMotion-VM-prod-01 COMPLETED 100 %
vMotion-VM-prod-02 COMPLETED 100 %
vMotion-VM-staging-03 IN_PROGRESS 67 %
vMotion-VM-dev-04 QUEUED 0 %
vMotion-VM-prod-05 FAILED 45 %
vMotion-VM-prod-06 COMPLETED 100 %
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present; if still failing, verify HCX_MANAGER URL is correct).
    **`curl: (7) Failed to connect to <ip>: Connection refused`** — Ensure HCX Manager is running and accessible; verify HCX_MANAGER environment variable is set to the correct IP/hostname and port (e.g., `export HCX_MANAGER="https://192.168.1.100:443"`).
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1`** — Verify the HCX_TOKEN is valid and not expired; check that the API endpoint returns valid JSON by testing `curl -sk -H "x-hm-authorization: ${HCX_TOKEN}" "${HCX_MANAGER}/hybridity/api/vmotion/jobs"` directly.
### Start a vMotion Migration

```bash
curl -sk -X POST \
  -H "x-hm-authorization: ${HCX_TOKEN}" \
  -H "Content-Type: application/json" \
  "${HCX_MANAGER}/hybridity/api/vmotion" \
  -d '{
    "migrationType": "vMotion",
    "migrations": [
      {
        "srcVM": {
          "objectType": "VirtualMachine",
          "id": "vm-123",
          "name": "myvm"
        },
        "destNetworkMapping": [
          {
            "srcNetwork": { "name": "on-prem-pg" },
            "destNetwork": { "name": "evs-segment-prod" }
          }
        ],
        "destDatastore": { "name": "vsanDatastore" },
        "destFolder": { "name": "Migrated-VMs" },
        "destCluster": { "name": "EVS-Management-Cluster" }
      }
    ]
  }'
```


```text title="Expected output"
{
  "id": "migration-task-8f4a2c91-7e3d-4b9a-a1c2-5d8e9f2b3a4c",
  "status": "QUEUED",
  "migrationType": "vMotion",
  "startTime": "2024-01-15T14:32:18.456Z",
  "migrations": [
    {
      "id": "mig-001",
      "srcVM": {
        "id": "vm-123",
        "name": "myvm"
      },
      "destCluster": "EVS-Management-Cluster",
      "destDatastore": "vsanDatastore",
      "status": "PENDING",
      "progress": 0
    }
  ]
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to hcx-manager.corp.local port 443: Connection refused`** — Verify HCX_MANAGER environment variable is set correctly and the HCX Manager appliance is running and network-accessible.
    **`{"error": "Invalid token", "code": 401}`** — Ensure HCX_TOKEN is valid and not expired; regenerate the token from the HCX Manager UI if necessary.
    **`{"error": "Network 'on-prem-pg' not found", "code": 404}`** — Confirm the source network name matches exactly in the on-premises vCenter and that network mappings are configured in HCX before initiating migration.
## esxcli — ESXi Host Diagnostics

SSH to an ESXi host (enable SSH via vCenter or DCUI first):

```bash
ssh root@evs-host-01.vcf.internal
```


```text title="Expected output"
The authenticity of host 'evs-host-01.vcf.internal (10.42.18.15)' can't be established.
ECDSA key fingerprint is SHA256:aBcD1EfGhIjKlMnOpQrStUvWxYz2A3B4C5D6E7F8G.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'evs-host-01.vcf.internal,10.42.18.15' (ECDSA) to the list of known hosts.
Last login: Wed Jan 15 14:32:18 2025 from 10.42.10.8
[root@evs-host-01 ~]#
```

!!! warning "Common errors"
    **`ssh: Could not resolve hostname evs-host-01.vcf.internal: Name or service not known`** — Verify DNS resolution with `nslookup evs-host-01.vcf.internal` or update `/etc/hosts` with the correct IP address.
    **`Permission denied (publickey,gssapi-keyex,gssapi-with-mic)`** — Ensure your SSH key is added to the remote host's `~/.ssh/authorized_keys` or configure password authentication in `/etc/ssh/sshd_config`.
    **`ssh: connect to host evs-host-01.vcf.internal port 22: Connection timed out`** — Check network connectivity and firewall rules; verify the host is reachable with `ping evs-host-01.vcf.internal` or `nc -zv evs-host-01.vcf.internal 22`.
```bash
# Storage adapter list
esxcli storage core adapter list

# vSAN disk list on this host
esxcli vsan storage list

# NVMe device list (EVS hosts use NVMe for vSAN cache and capacity)
esxcli nvme device list

# VMkernel interface list
esxcli network ip interface list

# VMkernel routing table
esxcli network ip route list

# vSAN health check from host level
esxcli vsan health cluster list

# Test VMkernel reachability (MTU-aware)
vmkping -I vmk0 <target-ip>
vmkping -I vmk1 <vtep-gateway-ip>   # NSX-T VTEP VMkernel

# Check NVMe device health
esxcli nvme device get -A vmhba1

# List running VMs on this host
vim-cmd vmsvc/getallvms
```


```text title="Expected output"
Name    Driver      Link  Speed  Duplex  MTU  Description
vmhba0  ahci        Up    Unknown Unknown 1500 AHCI Controller
vmhba1  nvme        Up    Unknown Unknown 1500 NVMe Controller
vmhba2  nvme        Up    Unknown Unknown 1500 NVMe Controller

Host UUID: 5a3c8e2f-b1d4-4e9a-8c2b-7f9d1a4e6b3c
Disk UUID: 6b4d9f3g-c2e5-5f0b-9d3c-8g0e2b5f7c4d
Disk Group UUID: 7c5e0g4h-d3f6-6g1c-0e4d-9h1f3c6g8d5e
Disk Group Health: Healthy
Disk Group Status: Healthy

Device: nvme0n1
Model: Samsung PM1735 3.2TB
Serial: S6GXNF0R900001
Firmware: GXS7502Q
Health Status: OK

Device: nvme1n1
Model: Samsung PM1735 3.2TB
Serial: S6GXNF0R900002
Firmware: GXS7502Q
Health Status: OK

Name  Portset  IP Address      Netmask         Broadcast       MTU  MAC Address
vmk0  0        10.50.12.45     255.255.255.0   10.50.12.255    1500 00:0c:29:a4:5e:2f
vmk1  0        172.16.100.50   255.255.255.0   172.16.100.255  1500 00:0c:29:a4:5e:30

Destination     Netmask         Gateway         VMknic  MTU  Metric
0.0.0.0         0.0.0.0         10.50.12.1      vmk0    1500 0
172.16.100.0    255.255.255.0   0.0.0.0         vmk1    1500 0

Cluster Status: Healthy
Node UUID: 5a3c8e2f-b1d4-4e9a-8c2b-7f9d1a4e6b3c
Node Health: Healthy
Disk Group Count: 2
Disk Count: 4

PING 10.50.12.1 (10.50.12.1): 56 data bytes
64 bytes from 10.50.12.1: icmp_seq=0 time=0.456 ms
64 bytes from 10.50.12.1: icmp_seq=1 time=0.412 ms
64 bytes from 10.50.12.1: icmp_seq=2 time=0.389 ms
--- 10.50.12.1 statistics ---
3 packets transmitted, 3 packets received, 0% packet loss

Device: vmhba1
Model: Samsung PM1735 3.2TB
Serial: S6GXNF0R900001
Firmware: GXS7502Q
Health Status: OK
Temperature: 42C

Vmid  Name
```
---

## See also

- [Amazon EVS — Procedures](../procedures/)
- [Amazon EVS — Scripts](../scripts/)
- [Amazon EVS — Health Checks](../health-checks/)

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
