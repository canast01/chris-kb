---
tags:
  - azure
  - security
---
# Azure — Hardening

<div class="kb-summary">
Azure hardening applies the principle of least privilege, reduces the attack surface, and enforces security configuration standards across subscriptions, resource groups, and individual resources.

*Applies to: Azure*
</div>

---

```d2
direction: down

microsoft_defender_for_cloud: "Microsoft Defender for Cloud" {shape: rectangle}
network_security_groups: "Network Security Groups" {shape: rectangle}
justintime_vm_access: "Just-In-Time VM Access" {shape: rectangle}
azure_policy_for_security: "Azure Policy for Security" {shape: rectangle}
resource_locks: "Resource Locks" {shape: rectangle}
defender_for_servers_hardening: "Defender for Servers — Hardening" {shape: rectangle}

microsoft_defender_for_cloud -> network_security_groups: hardens
network_security_groups -> justintime_vm_access: hardens
justintime_vm_access -> azure_policy_for_security: hardens
azure_policy_for_security -> resource_locks: hardens
resource_locks -> defender_for_servers_hardening: hardens
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Microsoft Defender for Cloud

Defender for Cloud is the primary security posture dashboard. It aggregates recommendations, assigns a Secure Score, and provides threat detection.

```bash
# Enable Defender for Cloud on a subscription (free tier — CSPM only)
az security auto-provisioning-setting update \
  --name mma \
  --auto-provision On

# Enable Defender plans (paid) for specific resource types
az security pricing create --name VirtualMachines --tier Standard
az security pricing create --name StorageAccounts --tier Standard
az security pricing create --name SqlServers --tier Standard
az security pricing create --name AppServices --tier Standard
az security pricing create --name Containers --tier Standard

# List all Defender plan states
az security pricing list --output table

# Get current Secure Score
az security secure-score list --output table
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b5c-6789-0def-1234-567890abcdef/providers/Microsoft.Security/autoProvisioningSettings/mma",
  "name": "mma",
  "autoProvision": "On",
  "type": "Microsoft.Security/autoProvisioningSettings"
}
{
  "id": "/subscriptions/12a34b5c-6789-0def-1234-567890abcdef/providers/Microsoft.Security/pricings/VirtualMachines",
  "name": "VirtualMachines",
  "pricingTier": "Standard"
}
{
  "id": "/subscriptions/12a34b5c-6789-0def-1234-567890abcdef/providers/Microsoft.Security/pricings/StorageAccounts",
  "name": "StorageAccounts",
  "pricingTier": "Standard"
}
{
  "id": "/subscriptions/12a34b5c-6789-0def-1234-567890abcdef/providers/Microsoft.Security/pricings/SqlServers",
  "name": "SqlServers",
  "pricingTier": "Standard"
}
{
  "id": "/subscriptions/12a34b5c-6789-0def-1234-567890abcdef/providers/Microsoft.Security/pricings/AppServices",
  "name": "AppServices",
  "pricingTier": "Standard"
}
{
  "id": "/subscriptions/12a34b5c-6789-0def-1234-567890abcdef/providers/Microsoft.Security/pricings/Containers",
  "name": "Containers",
  "pricingTier": "Standard"
}
Name                  PricingTier    FreeTrialRemainingDays
--------------------  -----------    ----------------------
VirtualMachines       Standard       0
StorageAccounts       Standard       0
SqlServers            Standard       0
AppServices           Standard       0
Containers            Standard       0
KeyVaults             Free           -1
ResourceManager       Free           -1
CurrentSecureScore    MaxScore    Percentage    ControlsStatus
------------------    --------    ----------    ---------------
42                    100         42%           Healthy: 8, Unhealthy: 12, NotApplicable: 5
```

!!! warning "Common errors"
    **`(AuthorizationFailed) The client '12a34b5c-6789-0def-1234-567890abcdef' with object id '98765432-1098-7654-3210-fedcba987654' does not have authorization to perform action 'Microsoft.Security/pricings/write' over scope '/subscriptions/12a34b5c-6789-0def-1234-567890abcdef'.`** — Ensure your user account or service principal has the Security Admin or Owner role on the subscription.
    **`(InvalidResourceType) The resource type 'VirtualMachines' is not valid for the current subscription.`** — Verify the subscription has at least one VM deployed; Defender pricing cannot be enabled for resource types that don't exist in the subscription.
### Unhealthy Recommendations

```bash
# List all unhealthy security recommendations
az security assessment list \
  --query "[?status.code=='Unhealthy']" \
  --output table

# Get details on a specific recommendation
az security assessment show \
  --name <assessment-name> \
  --assessed-resource-id <resource-id>

# Export all recommendations to JSON for remediation tracking
az security assessment list --output json > security-assessments-$(date +%Y%m%d).json
```


```text title="Expected output"
Name                                          Status      ResourceCount    Severity
────────────────────────────────────────────  ──────────  ───────────────  ────────
Ensure that 'Enforce SSL connection' is ON    Unhealthy   3                High
Ensure MFA is enabled for all users           Unhealthy   12               High
Ensure storage accounts use SAS tokens        Unhealthy   5                Medium
Ensure Network Security Groups are hardened   Unhealthy   8                High
Ensure Key Vault logging is enabled           Unhealthy   2                Medium
...

{
  "id": "/subscriptions/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6/providers/Microsoft.Security/assessments/mfa-enabled-assessment",
  "name": "mfa-enabled-assessment",
  "type": "Microsoft.Security/assessments",
  "properties": {
    "displayName": "Ensure MFA is enabled for all users",
    "status": {
      "code": "Unhealthy",
      "cause": "OffByPolicy",
      "firstEvaluationDate": "2024-01-15T08:30:00Z",
      "statusChangeDate": "2024-01-20T14:22:15Z"
    },
    "resourceDetails": {
      "id": "/subscriptions/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01"
    }
  }
}

security-assessments-20240122.json
```

!!! warning "Common errors"
    **`ERROR: The following arguments are required: --name, --assessed-resource-id`** — Provide the exact assessment name and resource ID from the list output, or use `az security assessment list --query "[0].[name,id]"` to retrieve them.
    **`ERROR: No subscriptions found. Run 'az login' to set up account.`** — Authenticate with `az login` and set the correct subscription using `az account set --subscription <subscription-id>`.
    **`ERROR: The client '<client-id>' does not have authorization to perform action 'Microsoft.Security/assessments/read'`** — Ensure your Azure account has the Security Reader or higher role assigned at the subscription scope.
---

## Network Security Groups

NSGs filter traffic at the subnet or NIC level. Apply NSGs to subnets (preferred) rather than individual NICs.

```bash
# Create an NSG
az network nsg create \
  --name nsg-appsubnet \
  --resource-group <rg-name> \
  --location <region>

# Add a rule — allow HTTPS inbound from a specific CIDR
az network nsg rule create \
  --nsg-name nsg-appsubnet \
  --resource-group <rg-name> \
  --name Allow-HTTPS-Inbound \
  --priority 100 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes 10.0.0.0/8 \
  --destination-port-ranges 443

# Deny all other inbound (explicit deny — NSGs have implicit deny but make it explicit for auditing)
az network nsg rule create \
  --nsg-name nsg-appsubnet \
  --resource-group <rg-name> \
  --name Deny-All-Inbound \
  --priority 4000 \
  --direction Inbound \
  --access Deny \
  --protocol '*' \
  --source-address-prefixes '*' \
  --destination-port-ranges '*'

# Associate NSG with a subnet
az network vnet subnet update \
  --vnet-name <vnet-name> \
  --name <subnet-name> \
  --resource-group <rg-name> \
  --network-security-group nsg-appsubnet

# List effective NSG rules on a NIC (what actually applies including inheritance)
az network nic list-effective-nsg \
  --name <nic-name> \
  --resource-group <rg-name>
```


```text title="Expected output"
{
  "etag": "W/\"a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Network/networkSecurityGroups/nsg-appsubnet",
  "location": "eastus",
  "name": "nsg-appsubnet",
  "provisioningState": "Succeeded",
  "resourceGroup": "prod-rg",
  "type": "Microsoft.Network/networkSecurityGroups"
}
{
  "access": "Allow",
  "description": null,
  "destinationAddressPrefix": "*",
  "destinationPortRange": "443",
  "direction": "Inbound",
  "etag": "W/\"b2c3d4e5-f6g7-48h9-i0j1-k2l3m4n5o6p7\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Network/networkSecurityGroups/nsg-appsubnet/securityRules/Allow-HTTPS-Inbound",
  "name": "Allow-HTTPS-Inbound",
  "priority": 100,
  "protocol": "Tcp",
  "provisioningState": "Succeeded",
  "sourceAddressPrefix": "10.0.0.0/8",
  "type": "Microsoft.Network/securityRules"
}
{
  "access": "Deny",
  "description": null,
  "destinationAddressPrefix": "*",
  "destinationPortRange": "*",
  "direction": "Inbound",
  "etag": "W/\"c3d4e5f6-g7h8-49i0-j1k2-l3m4n5o6p7q8\"",
  "name": "Deny-All-Inbound",
  "priority": 4000,
  "protocol": "*",
  "provisioningState": "Succeeded",
  "sourceAddressPrefix": "*",
  "type": "Microsoft.Network/securityRules"
}
{
  "etag": "W/\"d4e5f6g7-h8i9-50j0-k1l2-m3n4o5p6q7r8\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Network/virtualNetworks/prod-vnet/subnets/app-subnet",
  "name": "app-subnet",
  "provisioningState": "Succeeded",
  "type": "Microsoft.Network/virtualNetworks/subnets"
}
[
  {
    "access": "Allow",
    "destinationPortRange": "443",
    "direction": "Inbound",
    "name": "Allow-HTTPS-Inbound",
    "priority": 100,
    "protocol": "Tcp",
```
### NSG Flow Logs

Enable flow logs for all production NSGs. Required for security investigations and network anomaly detection.

```bash
# Create a storage account for NSG flow logs
az storage account create \
  --name <sa-nsgflowlogs> \
  --resource-group <rg-name> \
  --sku Standard_LRS

# Enable NSG flow logs (version 2 includes traffic analytics)
az network watcher flow-log create \
  --name flowlog-nsg-appsubnet \
  --resource-group <rg-name> \
  --nsg <nsg-resource-id> \
  --storage-account <sa-resource-id> \
  --enabled true \
  --format JSON \
  --log-version 2 \
  --retention 90 \
  --traffic-analytics true \
  --workspace <log-analytics-workspace-id>
```


```text title="Expected output"
{
  "accessTier": "Hot",
  "creationTime": "2024-01-15T09:42:33.847391+00:00",
  "customDomain": null,
  "enableHttpsTrafficOnly": true,
  "encryption": {
    "keySource": "Microsoft.Storage",
    "services": {
      "blob": {
        "enabled": true,
        "lastEnabledTime": "2024-01-15T09:42:33.847391+00:00"
      },
      "file": {
        "enabled": true,
        "lastEnabledTime": "2024-01-15T09:42:33.847391+00:00"
      }
    }
  },
  "id": "/subscriptions/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6/resourceGroups/rg-prod-eastus/providers/Microsoft.Storage/storageAccounts/sansgflowlogs2024",
  "kind": "StorageV2",
  "location": "eastus",
  "name": "sansgflowlogs2024",
  "primaryEndpoints": {
    "blob": "https://sansgflowlogs2024.blob.core.windows.net/",
    "file": "https://sansgflowlogs2024.file.core.windows.net/",
    "queue": "https://sansgflowlogs2024.queue.core.windows.net/",
    "table": "https://sansgflowlogs2024.table.core.windows.net/"
  },
  "resourceGroup": "rg-prod-eastus",
  "sku": {
    "name": "Standard_LRS",
    "tier": "Standard"
  },
  "statusOfPrimary": "available"
}
{
  "enabled": true,
  "etag": "W/\"2024-01-15T10:18:22.5634521Z\"",
  "format": "JSON",
  "id": "/subscriptions/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6/resourceGroups/rg-prod-eastus/providers/Microsoft.Network/networkWatchers/NetworkWatcher_eastus/flowLogs/flowlog-nsg-appsubnet",
  "location": "eastus",
  "name": "flowlog-nsg-appsubnet",
  "provisioningState": "Succeeded",
  "retentionPolicy": {
    "days": 90,
    "enabled": true
  },
  "storageId": "/subscriptions/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6/resourceGroups/rg-prod-eastus/providers/Microsoft.Storage/storageAccounts/sansgflowlogs2024",
  "targetResourceId": "/subscriptions/a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6/resourceGroups/rg-
```
---

## Just-In-Time VM Access

JIT VM access blocks management ports (RDP/SSH) by default and opens them only for approved requests with time limits.

```bash
# Enable JIT on a VM
az security jit-policy create \
  --resource-group <rg-name> \
  --location <region> \
  --vm-name <vm-name> \
  --ports '[
    {
      "number": 22,
      "protocol": "TCP",
      "allowedSourceAddressPrefix": "*",
      "maxRequestAccessDuration": "PT3H"
    },
    {
      "number": 3389,
      "protocol": "TCP",
      "allowedSourceAddressPrefix": "*",
      "maxRequestAccessDuration": "PT3H"
    }
  ]'

# Request JIT access (opens port for 2 hours from your IP)
az security jit-policy initiate \
  --resource-group <rg-name> \
  --vm-name <vm-name> \
  --vm-requests '[
    {
      "virtualMachineResourceId": "<vm-resource-id>",
      "ports": [
        {
          "number": 22,
          "allowedSourceAddressPrefix": "<your-ip>/32",
          "endTimeUtc": "2024-01-01T12:00:00.0000000Z",
          "duration": "PT2H"
        }
      ]
    }
  ]'
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Security/locations/eastus/jitNetworkAccessPolicies/default",
  "name": "default",
  "properties": {
    "virtualMachines": [
      {
        "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01",
        "ports": [
          {
            "number": 22,
            "protocol": "TCP",
            "allowedSourceAddressPrefix": "*",
            "maxRequestAccessDuration": "PT3H"
          },
          {
            "number": 3389,
            "protocol": "TCP",
            "allowedSourceAddressPrefix": "*",
            "maxRequestAccessDuration": "PT3H"
          }
        ]
      }
    ],
    "requests": []
  },
  "type": "Microsoft.Security/locations/jitNetworkAccessPolicies"
}
{
  "properties": {
    "virtualMachines": [
      {
        "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01",
        "ports": [
          {
            "number": 22,
            "allowedSourceAddressPrefix": "203.0.113.45/32",
            "endTimeUtc": "2024-01-01T14:00:00.0000000Z",
            "duration": "PT2H",
            "status": "Initiated"
          }
        ]
      }
    ]
  }
}
```

!!! warning "Common errors"
    **`(ResourceNotFound) The resource '/subscriptions/.../jitNetworkAccessPolicies/default' could not be found.`** — Ensure the VM exists in the specified resource group and region, and that Azure Security Center is enabled for the subscription.
    **`(InvalidRequestContent) The request body is invalid.`** — Validate the JSON syntax in the ports array and ensure the endTimeUtc timestamp is in ISO 8601 format and in the future.
    **`(AuthorizationFailed) The client 'user@example.com' with object id 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' does not have authorization to perform action 'Microsoft.Security/locations/jitNetworkAccessPolicies/initiate/action'.`** — Assign the Security Admin or higher role to the user on the subscription or resource group.
---

## Azure Policy for Security

Azure Policy enforces configuration standards automatically and audits for drift.

```bash
# List all built-in security policies
az policy definition list \
  --query "[?policyType=='BuiltIn' && contains(displayName, 'Security')]" \
  --output table

# Assign a built-in policy: require TLS 1.2 on storage accounts
az policy assignment create \
  --name "require-tls12-storage" \
  --display-name "Require TLS 1.2 on Storage Accounts" \
  --policy "fe83a0eb-a853-422d-aac2-1bffd182c5d0" \
  --scope "/subscriptions/<sub-id>" \
  --enforcement-mode Default

# Assign CIS Microsoft Azure Foundations Benchmark initiative
az policy assignment create \
  --name "cis-azure-benchmark" \
  --display-name "CIS Microsoft Azure Foundations Benchmark" \
  --policy-set-definition "612b5213-9160-4969-8578-1518bd2a000c" \
  --scope "/subscriptions/<sub-id>"

# Get policy compliance state
az policy state summarize \
  --subscription <sub-id> \
  --output table

# Get non-compliant resources for a specific assignment
az policy state list \
  --policy-assignment <assignment-id> \
  --filter "complianceState eq 'NonCompliant'" \
  --output table
```


```text title="Expected output"
DisplayName                                          Name                                      PolicyType    Mode
-------------------------------------------------    ------------------------------------       ---------     ------
Require HTTPS in Storage Account                     e7d100dd-e89b-4265-bc78-24b1f824910c     BuiltIn       Indexed
Require TLS version on Linux web apps                 f0e6e85b-9b9f-4a4b-b952-6b6b7d5c8e9a     BuiltIn       Indexed
Secure transfer to storage accounts enabled          7414c4b6-fb4c-46c6-b00f-eb134e3e6e20     BuiltIn       Indexed
...

{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Authorization/policyAssignments/require-tls12-storage",
  "name": "require-tls12-storage",
  "displayName": "Require TLS 1.2 on Storage Accounts",
  "policyDefinitionId": "/providers/Microsoft.Authorization/policyDefinitions/fe83a0eb-a853-422d-aac2-1bffd182c5d0",
  "scope": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
  "enforcementMode": "Default"
}

{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Authorization/policyAssignments/cis-azure-benchmark",
  "name": "cis-azure-benchmark",
  "displayName": "CIS Microsoft Azure Foundations Benchmark",
  "policySetDefinitionId": "/providers/Microsoft.Authorization/policySetDefinitions/612b5213-9160-4969-8578-1518bd2a000c",
  "scope": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d"
}

SubscriptionId                        ComplianceState    TotalResources    CompliantResources    NonCompliantResources
------------------------------------  ----------------   ---------------   --------------------  ----------------------
a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d  NonCompliant       47                 38                    9

ResourceId                                                                                    ComplianceState    PolicyAssignmentId
------------------------------------------------------------------------------------------------------  ----------------   -----------------------------------------------
/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Storage/storageAccounts/prodstg001  NonCompliant  /subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/
```
---

## Resource Locks

Resource locks prevent accidental deletion or modification of critical resources.

```bash
# Apply a delete lock to a resource group
az lock create \
  --name lock-prod-rg \
  --resource-group <rg-name> \
  --lock-type CanNotDelete \
  --notes "Production resource group — cannot delete without removing lock"

# Apply a read-only lock (prevents modification)
az lock create \
  --name lock-prod-vnet-readonly \
  --resource-group <rg-name> \
  --resource-type Microsoft.Network/virtualNetworks \
  --resource-name <vnet-name> \
  --lock-type ReadOnly

# List all locks in a subscription
az lock list --output table

# Remove a lock
az lock delete \
  --name lock-prod-rg \
  --resource-group <rg-name>
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Authorization/locks/lock-prod-rg",
  "level": "CanNotDelete",
  "name": "lock-prod-rg",
  "notes": "Production resource group — cannot delete without removing lock",
  "owner": {
    "applicationId": null
  },
  "resourceGroup": "prod-rg",
  "type": "Microsoft.Authorization/locks"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Network/virtualNetworks/prod-vnet/providers/Microsoft.Authorization/locks/lock-prod-vnet-readonly",
  "level": "ReadOnly",
  "name": "lock-prod-vnet-readonly",
  "resourceGroup": "prod-rg",
  "type": "Microsoft.Authorization/locks"
}
Name                      ResourceGroup    ResourceName    ResourceType                      Level        Notes
------------------------  ---------------  --------------  --------------------------------  -----------  -----------------------------------------------
lock-prod-rg              prod-rg                                                             CanNotDelete  Production resource group — cannot delete...
lock-prod-vnet-readonly   prod-rg          prod-vnet       Microsoft.Network/virtualNetworks ReadOnly

(no output — command completes silently)
```

!!! warning "Common errors"
    **`The resource group '<rg-name>' could not be found.`** — Replace `<rg-name>` with the actual resource group name, or verify it exists with `az group list`.
    **`The resource 'Microsoft.Network/virtualNetworks/<vnet-name>' does not exist in resource group '<rg-name>'.`** — Verify the virtual network name and resource group are correct using `az network vnet list --resource-group <rg-name>`.
Apply `CanNotDelete` locks to all production resource groups, key vaults, virtual networks, and storage accounts that hold critical data.

---

## Defender for Servers — Hardening

When Defender for Servers (Plan 2) is enabled, it provides:
- Microsoft Defender Vulnerability Management (MDVM) for OS and application CVE scanning
- File Integrity Monitoring (FIM) — alerts on changes to critical system files
- Adaptive Application Controls — allowlist for running processes
- OS security baseline assessment (CIS benchmarks)

```bash
# Check vulnerability assessment findings for a VM
az security va sql scans list \
  --server-name <server> \
  --database-name <db> \
  --resource-group <rg-name>

# Get endpoint protection status on VMs
az security assessment list \
  --query "[?contains(displayName, 'endpoint protection')]" \
  --output table
```


```text title="Expected output"
Id                                          DisplayName                                      State
--------------------------------------------  -----------------------------------------------  ---------
/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/prod-rg/providers/Microsoft.Security/assessments/endpoint-protection-001  Endpoint Protection should be installed on your machines  Healthy
/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/prod-rg/providers/Microsoft.Security/assessments/endpoint-protection-002  Endpoint Protection health issues should be resolved  Unhealthy
/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/prod-rg/providers/Microsoft.Security/assessments/endpoint-protection-003  Missing endpoint protection  Unhealthy

ScanId                 Database      Server           Status      StartTime
---------------------  -----------  ---------------  ----------  -------------------------
scan-20240115-001      paymentdb    sql-prod-01      Completed   2024-01-15T09:30:22Z
scan-20240115-002      inventorydb  sql-prod-01      Completed   2024-01-15T10:15:45Z
scan-20240115-003      analyticsdb  sql-prod-02      In Progress 2024-01-15T11:00:10Z
```

!!! warning "Common errors"
    **`The provided resource group <rg-name> does not exist.`** — Verify the resource group name with `az group list` and ensure it matches your subscription.
    **`No assessments found matching the query.`** — Check that Defender for Cloud is enabled on your subscription with `az security auto-provisioning-setting list`.
    **`Server '<server>' not found in resource group '<rg-name>'.`** — Confirm the SQL server name exists in the specified resource group using `az sql server list --resource-group <rg-name>`.
---

## Security Baseline Hardening Checklist

| Control | Azure Implementation | Status Check |
|---|---|---|
| MFA enforced for all users | Conditional Access policy | `az rest --url graph.microsoft.com/v1.0/identity/conditionalAccess/policies` |
| Legacy auth blocked | Conditional Access → block legacy clients | Same as above |
| No standing Owner assignments | PIM eligible assignments only | `az role assignment list --all --query "[?roleDefinitionName=='Owner']"` |
| JIT VM access | Defender for Cloud → JIT | `az security jit-policy list` |
| NSG flow logs | All production NSGs | `az network watcher flow-log list` |
| Key Vault purge protection | Enabled on all vaults | `az keyvault list --query "[?properties.enablePurgeProtection!=true]"` |
| Storage HTTPS only | All storage accounts | `az storage account list --query "[?enableHttpsTrafficOnly!=true]"` |
| Storage TLS 1.2+ | All storage accounts | `az storage account list --query "[?minimumTlsVersion!='TLS1_2']"` |
| Defender for Cloud enabled | All subscriptions | `az security auto-provisioning-setting list` |
| Diagnostic settings | All critical resources | `az monitor diagnostic-settings list` |
| No public storage blobs | All storage accounts | `az storage account list --query "[?allowBlobPublicAccess==true]"` |

```bash
# Quick hardening audit — find storage accounts with HTTP allowed or public access
az storage account list --output json | python3 -c "
import json, sys
accounts = json.load(sys.stdin)
for a in accounts:
    issues = []
    if not a.get('enableHttpsTrafficOnly'): issues.append('HTTP allowed')
    if a.get('allowBlobPublicAccess'): issues.append('public blob access')
    if a.get('minimumTlsVersion','') != 'TLS1_2': issues.append('TLS < 1.2')
    if issues:
        print(f'{a[\"name\"]}: {\", \".join(issues)}')
"
```


```text title="Expected output"
storageacct001: HTTP allowed, TLS < 1.2
proddata-storage: HTTP allowed, public blob access
backupvault-east: TLS < 1.2
```

!!! warning "Common errors"
    **`jq: command not found`** — Install jq with `apt-get install jq` or use the built-in Python JSON parser as shown in the example.
    **`ERROR: The following arguments are required: --resource-group`** — Add `--resource-group <group-name>` or use `--query "[].{name:name, https:enableHttpsTrafficOnly}"` to filter specific subscriptions.
    **`ModuleNotFoundError: No module named 'json'`** — The json module is built-in to Python 3; verify Python 3 is installed with `python3 --version` and that the script syntax is correct.
---

## See also

- [Azure — Authentication](../authentication/)
- [Azure — Access Control](../access-control/)
- [Azure — Encryption](../encryption/)
