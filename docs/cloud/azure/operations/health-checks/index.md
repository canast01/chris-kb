# Azure — Health Checks


<div class="kb-summary">
Service health, VM status, load balancer health, and monitor alert review. See also: [Operations](../index.md) for the full daily checklist and incident triage procedures.
</div>

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

> To set a budget alert: use `az consumption budget create` or configure in the Azure Portal under **Cost Management + Billing → Budgets**. Set both an actual-spend threshold (e.g., 80%, 100%) and a forecast threshold to catch trends before they breach the limit.

---
```text
┌─────────────────────────────── Cloud Azure Operations — Health Checks ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Azure health checks: routine verification of operational status and performance        │   │
│   │         Checks include: controller status, drive health, replication lag, and capacity        │   │
│   │         Frequency: daily quick checks; weekly detailed review; monthly capacity report        │   │
│   │        Configure threshold-based alerts for proactive incident prevention and awareness       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Check status → review alerts → verify replication → capacity → log                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Check area    │  How to verify   │   Pass criteria   │    Frequency     │       Tool       │   │
│   │   Controllers    │   show status    │    All healthy    │      Daily       │     CLI/GUI      │   │
│   │      Drives      │   show drives    │  No failed/pred.  │      Daily       │     CLI/GUI      │   │
│   │   Replication    │ show replication │  Lag < threshold  │      Daily       │     CLI/GUI      │   │
│   │     Capacity     │  show capacity   │     < 80% used    │      Daily       │     CLI/GUI      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Cloud Azure Operations infrastructure · management network · monitoring                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Cloud Azure Operations platform overview and core concepts                    │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


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
