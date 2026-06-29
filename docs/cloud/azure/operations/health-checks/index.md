---
tags:
  - azure
  - operations
---
# Azure — Health Checks

<div class="kb-summary">
Azure daily health checks — runnable CLI routine covering service health incidents, VM power states and provisioning failures, load balancer backend pool health, storage capacity, NSG flow log validation, and Monitor alert review.

*Applies to: Azure*
</div>

```d2
direction: right

begin_checks: "Begin Checks" {shape: oval}
run_this_routine: "Run This Routine" {shape: rectangle}
vm_health: "VM Health" {shape: rectangle}
network_health: "Network Health" {shape: rectangle}
storage_health: "Storage Health" {shape: rectangle}
identity_and_security: "Identity and Security" {shape: rectangle}
cost_optimization: "Cost Optimization" {shape: rectangle}
generate_report: "Generate Report" {shape: oval}

begin_checks -> run_this_routine
run_this_routine -> vm_health
vm_health -> network_health
network_health -> storage_health
storage_health -> identity_and_security
identity_and_security -> cost_optimization
cost_optimization -> generate_report
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

Run these eight commands at the start of every operational shift to verify Azure environment health.

```bash
# 1. Azure Service Health — active incidents and planned maintenance for your subscription
az rest \
  --method GET \
  --url 'https://management.azure.com/subscriptions/<sub>/providers/Microsoft.ResourceHealth/events?api-version=2022-10-01' \
  --query 'value[].{Title:properties.title,Type:properties.eventType,Status:properties.status,Region:properties.impactedRegions[0].id}' \
  -o table

# 2. All VM power states
az vm list -d \
  --query '[].{Name:name,RG:resourceGroup,PowerState:powerState,ProvisioningState:provisioningState}' \
  -o table

# 3. VMs with failed or non-Succeeded provisioning state
az vm list -d \
  --query '[?provisioningState!=`Succeeded`].{Name:name,RG:resourceGroup,State:provisioningState,PowerState:powerState}' \
  -o table

# 4. Load balancer backend address pools (check for empty or misconfigured pools)
az network lb show \
  -g <rg> \
  -n <lb-name> \
  --query 'backendAddressPools[].{Name:name,Addresses:backendIPConfigurations|length(@)}' \
  -o table

# 5. Storage account used capacity
az monitor metrics list \
  --resource <storage-resource-id> \
  --metric UsedCapacity \
  --interval PT1H \
  --query 'value[0].timeseries[0].data[-1].{UsedBytes:average}' \
  -o table

# 6. NSG flow log status by region
az network watcher flow-log list \
  -l <location> \
  --query '[].{Name:name,Enabled:enabled,StorageAccount:storageId,RetentionDays:retentionPolicy.days}' \
  -o table

# 7. Entra ID app registration credential expiry
az ad app list \
  --query '[].{Name:displayName,AppId:appId,Expiry:passwordCredentials[0].endDateTime}' \
  -o table | grep -E "2024|2025|2026"

# 8. Azure Advisor security recommendations
az advisor recommendation list \
  --category Security \
  --query '[].{Title:shortDescription.solution,Impact:impact,Resource:resourceMetadata.resourceId}' \
  -o table
```


```text title="Expected output"
Title                                          Type              Status    Region
─────────────────────────────────────────────  ────────────────  ────────  ──────────────────────
Azure Storage service degradation in eastus2  Incident          Resolved  /subscriptions/abc123/locations/eastus2
Planned maintenance - VM host updates         PlannedMaintenance Active   /subscriptions/abc123/locations/westus

Name              RG              PowerState    ProvisioningState
────────────────  ──────────────  ────────────  ──────────────────
prod-web-01       prod-rg         VM running    Succeeded
prod-web-02       prod-rg         VM running    Succeeded
staging-db-01     staging-rg      VM stopped    Succeeded
dev-test-vm       dev-rg          VM running    Succeeded

Name              RG              State         PowerState
────────────────  ──────────────  ────────────  ──────────────────
legacy-app-vm     legacy-rg       Failed        VM deallocated

Name                    Addresses
──────────────────────  ──────────
backend-pool-primary    8
backend-pool-secondary  0

UsedBytes
──────────────────
847362891776.0

Name                    Enabled    StorageAccount                                    RetentionDays
──────────────────────  ─────────  ──────────────────────────────────────────────────  ───────────────
NetworkWatcher_eastus   true       /subscriptions/abc123/resourceGroups/nw-rg/...     90
NetworkWatcher_westus   true       /subscriptions/abc123/resourceGroups/nw-rg/...     30

Name                              AppId                                 Expiry
────────────────────────────────  ──────────────────────────────────────  ──────────────────────
MyWebApp                          a1b2c3d4-e5f6-7890-abcd-ef1234567890   2025-03-15T10:30:00Z
LegacyIntegrationService          f9e8d7c6-b5a4-3210-fedc-ba9876543210   2024-11-22T14:45:00Z

Title                                                    Impact      Resource
─────────────────────────────────────────────────────────  ──────────  ──────────────────────────────────────────────
Enable MFA on privileged accounts                        High        /subscriptions/abc123/resourceGroups/prod-rg/...
Review and remove unused managed identities              Medium      /subscriptions/abc123/resourceGroups/prod-rg/...
Encrypt data in transit for Application Gateway          High        /subscriptions/abc123/resourceGroups/prod-rg/...
```

!!! warning "Common errors"
    **`ERROR: The following arguments are required: --resource`** — Provide the full resource ID for the storage account using `--resource /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<name>`.
    **`ERROR: (ResourceNotFound) Resource 'Microsoft.Network/networkWatchers' not found`** — Ensure Network Watcher is deployed in the target region with `az network watcher configure --resource-group <rg>
---

## VM Health

Verify compute VM status, availability sets, and extension health.

```bash
# All VMs with detailed state
az vm list -d \
  --query '[].{Name:name,RG:resourceGroup,Size:hardwareProfile.vmSize,OS:storageProfile.osDisk.osType,PowerState:powerState,Provisioning:provisioningState}' \
  -o table

# VMs that are deallocated (stopped but still billed for managed disk)
az vm list -d \
  --query '[?powerState==`VM deallocated`].{Name:name,RG:resourceGroup,Size:hardwareProfile.vmSize}' \
  -o table

# VM availability set member health
az vm availability-set list \
  --query '[*].{Name:name,RG:resourceGroup,FaultDomains:platformFaultDomainCount,UpdateDomains:platformUpdateDomainCount}' \
  -o table

# VM extensions — check for failed provisioning
az vm extension list \
  --resource-group <rg> \
  --vm-name <vm-name> \
  --query '[].{Extension:name,Type:typeHandlerVersion,State:provisioningState}' \
  -o table

# VM instance view — detailed health including guest OS-level status
az vm get-instance-view \
  --resource-group <rg> \
  --name <vm-name> \
  --query 'instanceView.statuses[].{Code:code,Level:level,Display:displayStatus}' \
  -o table

# Recent VM operations from activity log (last 24 hours)
az monitor activity-log list \
  --resource-group <rg> \
  --start-time $(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v-24H +%Y-%m-%dT%H:%M:%SZ) \
  --query '[?category.value==`Administrative`].{Time:eventTimestamp,Operation:operationName.localizedValue,Status:status.localizedValue,Caller:caller}' \
  -o table
```


```text title="Expected output"
Name                          RG              Size           OS      PowerState      Provisioning
------------------------------  ---------------  ---------------  ------  ---------------  ---------------
prod-web-01                    prod-rg          Standard_D2s_v3  Linux   VM running      Succeeded
prod-web-02                    prod-rg          Standard_D2s_v3  Linux   VM running      Succeeded
prod-db-01                     prod-rg          Standard_E4s_v3  Windows VM deallocated  Succeeded
dev-app-03                     dev-rg           Standard_B2s     Linux   VM stopped       Succeeded
staging-api-01                 staging-rg       Standard_D4s_v3  Windows VM running      Succeeded

Name                          RG              Size
------------------------------  ---------------  ---------------
prod-db-01                     prod-rg          Standard_E4s_v3

Name                          RG              FaultDomains  UpdateDomains
------------------------------  ---------------  ---------------  ---------------
prod-web-avset                 prod-rg          3              5
prod-db-avset                  prod-rg          2              5

Extension                     Type              State
------------------------------  ---------------  ---------------
CustomScript                  1.10              Succeeded
DependencyAgent               9.10              Succeeded

Code                                      Level    Display
---------------------------------------------  -------  -----------------------------------------------
ProvisioningState/succeeded                info     Provisioning succeeded
PowerState/running                         info     VM running
HealthState/healthy                        info     VM is healthy

Time                              Operation                           Status      Caller
------------------------------  --------------------------------  -----------  ----------------------
2024-01-15T14:32:18.123456Z     Create Virtual Machine              Succeeded   user@contoso.com
2024-01-15T09:47:52.654321Z     Start Virtual Machine               Succeeded   automation@contoso.com
2024-01-14T22:15:33.987654Z     Deallocate Virtual Machine          Succeeded   user@contoso.com
```

!!! warning "Common errors"
    **`The resource group '<rg>' could not be found.`** — Verify the resource group name with `az group list` and ensure you are querying the correct subscription.
    **`The virtual machine '<vm-name>' does not exist in the resource group '<rg>'.`** — Confirm the VM name is correct and exists in the specified resource group using `az vm list -d --resource-group <rg>`.
    **`date: invalid date 'TZ=UTC0 24 hours ago'`** — Use the macOS-compatible date syntax: `date -u -v-24H +%Y-%m-%dT%H:%M:%SZ` or install GNU coreutils on macOS.
| Status | Meaning | Action |
|---|---|---|
| `VM running` | Normal operating state | No action |
| `VM deallocated` | Stopped — compute released | Review if intentional; start if needed |
| `VM stopped` | Stopped — compute still reserved and billed | Deallocate to release compute |
| `Failed` provisioning | Deployment error | Check activity log; redeploy if needed |

---

## Network Health

Verify load balancers, NSGs, VNet peerings, and VPN gateway status.

```bash
# All load balancers and provisioning state
az network lb list \
  --query '[].{Name:name,RG:resourceGroup,SKU:sku.name,Provisioning:provisioningState}' \
  -o table

# Application gateway health
az network application-gateway list \
  --query '[].{Name:name,RG:resourceGroup,State:operationalState,Provisioning:provisioningState}' \
  -o table

# VNet peering status
az network vnet peering list \
  --resource-group <rg> \
  --vnet-name <vnet-name> \
  --query '[].{Name:name,Remote:remoteVirtualNetwork.id,State:peeringState,AllowForwardedTraffic:allowForwardedTraffic}' \
  -o table

# VPN gateway connections
az network vpn-connection list \
  --resource-group <rg> \
  --query '[].{Name:name,State:connectionStatus,EgressKbps:egressBytesTransferred,IngressKbps:ingressBytesTransferred}' \
  -o table

# ExpressRoute circuit status
az network express-route list \
  --query '[].{Name:name,RG:resourceGroup,Provisioning:provisioningState,CircuitProvisioning:circuitProvisioningState,BandwidthMbps:bandwidthInMbps}' \
  -o table

# NSG rule list for a specific NSG
az network nsg rule list \
  --resource-group <rg> \
  --nsg-name <nsg-name> \
  --query '[].{Name:name,Priority:priority,Dir:direction,Access:access,Protocol:protocol,DestPort:destinationPortRange}' \
  -o table
```


```text title="Expected output"
Name                          RG              SKU      Provisioning
------------------------------  ---------------  -------  ---------------
prod-lb-eastus-01             prod-network     Standard Succeeded
staging-lb-westus-02          staging-network  Basic    Succeeded
internal-lb-centralus         prod-network     Standard Succeeded

Name                          RG              State       Provisioning
------------------------------  ---------------  -----------  ---------------
api-appgw-prod                prod-network     Running      Succeeded
web-appgw-staging             staging-network  Running      Succeeded

Name                          Remote                                                          State      AllowForwardedTraffic
------------------------------  ---------------------------------------------------------------  ---------  ----------------------
peer-to-hub-vnet              /subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/hub-rg/providers/Microsoft.Network/virtualNetworks/hub-vnet  Connected  True
peer-to-spoke-02              /subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/spoke-rg/providers/Microsoft.Network/virtualNetworks/spoke-vnet-02  Connected  False

Name                          State       EgressKbps  IngressKbps
------------------------------  -----------  -----------  -----------
site-to-site-vpn-01           Connected    2048000      1536000
site-to-site-vpn-02           Disconnected 0            0

Name                          RG              Provisioning  CircuitProvisioning  BandwidthMbps
------------------------------  ---------------  ---------------  --------------------  ---------------
expressroute-circuit-prod     prod-network     Succeeded        ServiceProvisioned    1000
expressroute-circuit-dr       dr-network       Succeeded        ServiceProvisioned    500

Name                          Priority  Dir        Access  Protocol  DestPort
------------------------------  --------  ---------  ------  --------  --------
allow-https-inbound           100       Inbound    Allow   Tcp       443
allow-http-inbound            110       Inbound    Allow   Tcp       80
deny-all-inbound              4096      Inbound    Deny    *         *
allow-outbound-dns            200       Outbound   Allow   Udp       53
...
```

!!! warning "Common errors"
    **`The following arguments are required: --resource-group`** — Provide the resource group name by replacing `<rg>` with your actual resource group name.
    **`No NSGs found in resource group '<rg>'`** — Verify the NSG exists in the specified resource group and that you have read permissions on it.
    **`The following arguments are required: --vnet-name`** — Replace `<vnet-name>` with the actual virtual network name in your resource group.
---

## Storage Health

Verify storage accounts, managed disk state, and backup job status.

```bash
# All storage accounts and their replication type
az storage account list \
  --query '[].{Name:name,RG:resourceGroup,SKU:sku.name,Kind:kind,HTTPS:supportsHttpsTrafficOnly,Provisioning:provisioningState}' \
  -o table

# Managed disks in an error or unattached state
az disk list \
  --query '[?diskState==`Unattached` || diskState==`Reserved`].{Name:name,RG:resourceGroup,SizeGB:diskSizeGb,State:diskState,SKU:sku.name}' \
  -o table

# Disks approaching size limits (> 80% of allocated size is a warning)
az disk list \
  --query '[].{Name:name,SizeGB:diskSizeGb,State:diskState,SKU:sku.name}' \
  -o table

# Azure Backup — failed jobs in the last 7 days
az backup job list \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --status Failed \
  --query '[].{VM:properties.entityFriendlyName,Type:properties.jobType,Start:properties.startTime,Error:properties.errorDetails[0].errorMessage}' \
  -o table

# Azure Backup — protection status for all VMs in vault
az backup item list \
  --resource-group <rg> \
  --vault-name <vault-name> \
  --backup-management-type AzureIaasVM \
  --query '[].{VM:properties.friendlyName,Status:properties.protectionStatus,LastBackup:properties.lastBackupTime,Policy:properties.policyName}' \
  -o table

# File share quotas and usage
az storage share list \
  --account-name <storage-account> \
  --query '[].{Name:name,QuotaGB:properties.quota,Tier:accessTier}' \
  -o table
```


```text title="Expected output"
Name                          RG              SKU              Kind       HTTPS    Provisioning
------------------------------  ---------------  ---------------  ---------  -------  ---------------
prodstg001                      prod-rg          Standard_LRS     StorageV2  True     Succeeded
prodstg002                      prod-rg          Premium_LRS      BlockBlobStorage  True     Succeeded
backupstg01                     backup-rg        Standard_GRS     StorageV2  True     Succeeded
devstg001                       dev-rg           Standard_LRS     StorageV2  False    Succeeded

Name                          RG              SizeGB    State        SKU
------------------------------  ---------------  --------  -----------  ---------------
disk-orphan-prod-01             prod-rg          256       Unattached   Premium_LRS
disk-reserved-backup-02         backup-rg        512       Reserved     Standard_LRS

Name                          SizeGB    State        SKU
------------------------------  --------  -----------  ---------------
vm-prod-osdisk                  128       Attached     Premium_LRS
vm-dev-datadisk-01              256       Attached     Standard_LRS
vm-backup-disk-03               512       Attached     Premium_LRS

VM                    Type              Start                          Error
---------------------  ----------------  -----------------------------  -----------------------------------------------
prod-web-01           AzureIaasVMJob    2024-01-15T02:30:45.123456Z    Snapshot creation failed: insufficient quota
prod-db-02            AzureIaasVMJob    2024-01-14T23:15:22.654321Z    Network timeout during backup transfer

VM                    Status            LastBackup                     Policy
---------------------  ----------------  -----------------------------  -----------------------------------------------
prod-web-01           Protected         2024-01-15T03:45:12.123456Z    DailyBackup-7day
prod-db-02            Protected         2024-01-14T04:20:33.987654Z    WeeklyBackup-30day
dev-app-01            ProtectionStopped  2024-01-10T05:10:00.456789Z    DailyBackup-7day

Name                          QuotaGB    Tier
------------------------------  ---------  -------
logs-share                      100        Hot
backups-share                   500        Cool
config-share                    50         Hot
```

!!! warning "Common errors"
    **`ERROR: The following arguments are required: --resource-group, --vault-name`** — Replace `<rg>` and `<vault-name>` with actual resource group and Recovery Services vault names.
    **`ERROR: The following arguments are required: --account-name`** — Replace `<storage-account>` with the actual storage account name.
    **`ResourceNotFound: The Resource 'Microsoft.RecoveryServices/vaults/<vault-name>' under resource group '<rg>' was not found`** — Verify the vault exists in the specified resource group and region using `az backup vault list --resource-group <rg>`.
---

## Identity and Security

Review Entra ID credentials, role assignments, and security centre findings.

```bash
# Entra ID app registrations with expiring credentials (within 60 days)
az ad app list \
  --query '[].{Name:displayName,AppId:appId,SecretExpiry:passwordCredentials[0].endDateTime,CertExpiry:keyCredentials[0].endDateTime}' \
  -o table

# Service principals with expired credentials
az ad sp list \
  --all \
  --query '[?passwordCredentials[0].endDateTime!=null].{SP:displayName,Expiry:passwordCredentials[0].endDateTime}' \
  -o table | grep -E "202[0-6]"

# All role assignments at subscription level
az role assignment list \
  --scope /subscriptions/$(az account show --query id -o tsv) \
  --query '[].{Principal:principalName,Role:roleDefinitionName,Scope:scope,Type:principalType}' \
  -o table

# Microsoft Defender for Cloud — active security recommendations
az security assessment list \
  --query '[?status.code!=`Healthy`].{Name:displayName,Status:status.code,Severity:metadata.severity,Resource:resourceDetails.id}' \
  -o table

# Privileged Identity Management — active role assignments (requires PIM license)
az rest \
  --method GET \
  --url 'https://management.azure.com/subscriptions/<sub>/providers/Microsoft.Authorization/roleAssignments?api-version=2022-04-01' \
  --query 'value[?properties.principalType==`User`].{Principal:properties.principalId,Role:properties.roleDefinitionId,Scope:properties.scope}' \
  -o table

# Key Vault — certificates nearing expiry
az keyvault certificate list \
  --vault-name <vault-name> \
  --query '[].{Name:name,Enabled:attributes.enabled,Expires:attributes.expires}' \
  -o table
```


```text title="Expected output"
Name                                    AppId                                SecretExpiry        CertExpiry
--------------------------------------  ------------------------------------ -------------------- --------------------
GraphAPI-Integration                    a7f2c891-4d3e-4b2a-9e1f-5c8d2a3b4e5f 2025-03-15T10:30:00Z 2025-06-20T14:45:00Z
ServiceBusConnector                     b8e3d9a2-5e4f-5c3b-0f2g-6d9e3b4c5f6g 2025-02-28T08:15:00Z None
WebAppAuth                              c9f4e0b3-6f5g-6d4c-1g3h-7e0f4c5d6g7h None                 2025-08-10T16:20:00Z

SP                                      Expiry
--------------------------------------  --------------------
legacy-batch-processor                  2024-11-30T12:00:00Z
old-automation-account                  2024-09-15T09:30:00Z

Principal                               Role                      Scope                                                     Type
--------------------------------------  ------------------------  --------------------------------------------------------- --------
alice.johnson@contoso.com               Owner                     /subscriptions/12345678-1234-1234-1234-123456789012     User
bob.smith@contoso.com                   Contributor               /subscriptions/12345678-1234-1234-1234-123456789012     User
managed-identity-prod-01                Reader                    /subscriptions/12345678-1234-1234-1234-123456789012     ServicePrincipal
automation-runbook-svc                  Virtual Machine Operator  /subscriptions/12345678-1234-1234-1234-123456789012     ServicePrincipal

Name                                    Status                    Severity      Resource
--------------------------------------  ----------------------- -------------- -----------------------------------------------
MFA should be enabled on accounts with write permissions
Enabled                                 High                      /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg
Unencrypted data in transit detected    Enabled                   Critical      /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01
SQL Server auditing disabled            Enabled                   Medium        /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Sql/servers/sqldb-prod

Principal                               Role                                          Scope
--------------------------------------  ------------------------------------------------ -----------------------------------------------
a1b2c3d4-e5f6-7890-abcd-ef1234567890   /subscriptions/12345678-1234-1234-1234-123456789012/providers/Microsoft.Authorization/roleDefinitions/8e3af657-a8ff-443c-a75c-2fe8c4bcb635
f5e6d7c8-b9a0-1234-5678-9abcdef01234   /subscriptions/12345678-1234-1234-1234-123
```
---

## Cost Optimization

Review spend by resource group, identify idle resources, and check budget thresholds.

```bash
# Current month cost by resource group
az consumption usage list \
  --billing-period-name $(date +%Y%m) \
  --query 'sort_by([].{RG:instanceName,Cost:pretaxCost,Currency:currency}, &Cost)[-10:]' \
  -o table

# Azure Advisor cost recommendations
az advisor recommendation list \
  --category Cost \
  --query '[].{Title:shortDescription.solution,Impact:impact,Savings:extendedProperties.annualSavingsAmount,Resource:resourceMetadata.resourceId}' \
  -o table

# Budget status
az consumption budget list \
  --query '[].{Name:name,Limit:amount,TimeGrain:timeGrain,Current:currentSpend.amount,Forecast:forecastSpend.amount}' \
  -o table

# Deallocated VMs still incurring managed disk costs
az vm list -d \
  --query '[?powerState==`VM deallocated`].{Name:name,RG:resourceGroup,Size:hardwareProfile.vmSize,OSDisk:storageProfile.osDisk.name}' \
  -o table

# Unattached managed disks (orphaned, accruing cost)
az disk list \
  --query '[?diskState==`Unattached`].{Name:name,RG:resourceGroup,SizeGB:diskSizeGb,SKU:sku.name,Created:timeCreated}' \
  -o table

# Unused public IP addresses
az network public-ip list \
  --query '[?ipAddress==null || ipAddress==``].{Name:name,RG:resourceGroup,SKU:sku.name,AllocationMethod:publicIPAllocationMethod}' \
  -o table
```


```text title="Expected output"
Name                          Cost        Currency
myapp-prod-rg                 4521.89     USD
data-analytics-rg             3847.12     USD
legacy-services-rg            2156.43     USD
dev-test-rg                   891.27      USD
backup-vault-rg               654.18      USD
monitoring-rg                 423.56      USD
network-rg                    287.91      USD
storage-archive-rg            156.34      USD
...

Title                                                Impact    Savings              Resource
Resize underutilized Virtual Machines               Medium    $1,247.00/year       /subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/myapp-prod-rg/providers/Microsoft.Compute/virtualMachines/web-server-01
Delete unattached managed disks                     Low       $892.50/year         /subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/data-analytics-rg/providers/Microsoft.Compute/disks/orphaned-disk-042
Release unused public IP addresses                  Low       $456.00/year         /subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/legacy-services-rg/providers/Microsoft.Network/publicIPAddresses/unused-pip-001
Reduce SQL Database compute capacity                High      $2,134.75/year       /subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/dev-test-rg/providers/Microsoft.Sql/servers/analytics-db/databases/warehouse

Name              Limit      TimeGrain    Current    Forecast
Production-Q1     5000.00    Monthly      3847.12    4521.89
Development       1000.00    Monthly      891.27     945.33
Backup-Services   2000.00    Monthly      654.18     712.45

Name                    RG                  Size          OSDisk
legacy-app-vm-02        legacy-services-rg  Standard_D4s  legacy-app-vm-02_OsDisk_1
test-server-04          dev-test-rg         Standard_B2s  test-server-04_OsDisk_1

Name                    RG                  SizeGB    SKU              Created
orphaned-disk-042       data-analytics-rg   256       Premium_LRS      2023-11-15T08:22:14.000000+00:00
unused-backup-disk-018  backup-vault-rg     512       StandardSSD_LRS  2023-10-02T14:45:33.000000+00:00
old-snapshot-disk-007   monitoring-rg       128       Standard_LRS     2023-09-28T11:18:09.000000+00:00

Name                    RG              SKU      AllocationMethod
unused-pip-001          legacy-services-r
```
> To set a budget alert: use `az consumption budget create` or configure in the Azure Portal under **Cost Management + Billing → Budgets**. Set both an actual-spend threshold (e.g., 80%, 100%) and a forecast threshold to catch trends before they breach the limit.

---

> Service health, VM status, load balancer health, and monitor alert review.

See also: [Operations](../index.md) for the full daily checklist and incident triage procedures.

---

## Quick Commands

```bash
# List VMs with power state
az vm list --show-details \
  --query '[*].[name,resourceGroup,powerState,provisioningState]' \
  -o table

# Load balancer status
az network lb show \
  --name <lb-name> \
  --resource-group <rg> \
  --query '{name:name,provisioningState:provisioningState}' \
  -o table

# Activity log — last 50 events
az monitor activity-log list --max-events 50 \
  --query '[*].[eventTimestamp,level,operationName.localizedValue,status.localizedValue]' \
  -o table

# Failed backup jobs
az backup job list \
  --vault-name $VAULT \
  -g $RG \
  --query '[?properties.status==`Failed`].[properties.jobType,properties.startTime,properties.errorDetails]' \
  -o table

# Azure Service Health — active incidents
az rest --method get \
  --url "https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.ResourceHealth/events?api-version=2022-10-01"
```


```text title="Expected output"
Name                ResourceGroup      PowerState    ProvisioningState
------------------  -----------------  -----------   -----------------
prod-web-01         rg-production      VM running    Succeeded
prod-web-02         rg-production      VM running    Succeeded
staging-app-01      rg-staging         VM deallocated Succeeded
dev-db-01           rg-development     VM running    Succeeded

Name              ProvisioningState
----------------  -----------------
lb-prod-eastus    Succeeded

EventTimestamp                    Level    OperationName                        Status
--------------------------------  -------  ------------------------------------  -----------
2024-01-15T14:32:18.456789Z       Info     Create or Update Virtual Machine     Succeeded
2024-01-15T13:47:22.123456Z       Info     Start Virtual Machine                Succeeded
2024-01-15T12:15:09.789012Z       Warning  Restart Virtual Machine              Succeeded
2024-01-15T11:03:44.345678Z       Error    Delete Network Interface             Failed
2024-01-15T10:22:15.901234Z       Info     Update Load Balancer                 Succeeded

JobType           StartTime                     ErrorDetails
----------------  ----------------------------  -----------------------------------------------
AzureIaaSVMJob    2024-01-14T22:30:00.000000Z   Snapshot creation failed: timeout after 3600s
AzureIaaSVMJob    2024-01-13T20:15:00.000000Z   Agent communication error on target VM

{
  "value": [
    {
      "id": "/subscriptions/12345678-1234-1234-1234-123456789012/providers/Microsoft.ResourceHealth/events/incident-2024-0115-001",
      "name": "incident-2024-0115-001",
      "type": "Microsoft.ResourceHealth/events",
      "properties": {
        "eventType": "ServiceIssue",
        "title": "Intermittent connectivity in East US region",
        "description": "Some customers may experience latency",
        "impactStartTime": "2024-01-15T08:00:00Z",
        "status": "Active"
      }
    }
  ]
}
```

!!! warning "Common errors"
    **`ERROR: The following arguments are required: --name, --resource-group`** — Replace `<lb-name>` and `<rg>` with actual load balancer name and resource group name.
    **`ERROR: argument --vault-name: expected one argument`** — Ensure the `$VAULT` and `$RG` environment variables are set before running the command (e.g., `export VAULT=myVault RG=myRG`).
    **`ERROR: Invalid subscription ID in URL`** — Replace `{subscriptionId}` with your actual subscription ID using `az account show --query id -o tsv`.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Azure — Procedures](../procedures/)
- [Azure — CLI Reference](../cli-reference/)
- [Azure — Common Issues](../../troubleshooting/common-issues/)
