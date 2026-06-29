---
tags:
  - azure
  - deployment
search:
  boost: 1.5
---
# Azure — Subscription and Landing Zone Setup

<div class="kb-summary">
Landing Zone deployment guide: Management Group hierarchy, Azure Policy, Defender for Cloud, Log Analytics, Sentinel, Entra ID baseline, Hub VNet, and Azure Backup configuration.

*Applies to: Azure / Entra ID*
</div>

```d2
direction: right

plan: "Plan" {shape: oval}
prerequisites: "Prerequisites" {shape: rectangle}
create_management_group_hierarchy: "Create Management Group Hierarchy" {shape: rectangle}
configure_azure_policy_at_management: "Configure Azure Policy at Management Group Level" {shape: rectangle}
configure_microsoft_defender_for_clo: "Configure Microsoft Defender for Cloud" {shape: rectangle}
set_up_log_analytics_workspace_and_s: "Set Up Log Analytics Workspace and Sentinel" {shape: rectangle}
configure_entra_id_azure_ad_baseline: "Configure Entra ID (Azure AD) Baseline" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> prerequisites
prerequisites -> create_management_group_hierarchy
create_management_group_hierarchy -> configure_azure_policy_at_management
configure_azure_policy_at_management -> configure_microsoft_defender_for_clo
configure_microsoft_defender_for_clo -> set_up_log_analytics_workspace_and_s
set_up_log_analytics_workspace_and_s -> configure_entra_id_azure_ad_baseline
configure_entra_id_azure_ad_baseline -> validate
```

## Before you begin

- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---

This guide covers building an Azure Landing Zone from scratch: Management Group hierarchy, Azure Policy, Defender for Cloud, Log Analytics, Sentinel, Entra ID baseline, Hub VNet, Azure Backup, and deployment validation.

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Azure AD Global Administrator | Required for Management Group and Entra ID configuration |
| Azure subscription (management) | Dedicated to platform operations; no workloads |
| Azure CLI | `az --version` — use 2.50+ |
| Billing account | EA, MCA, or Pay-As-You-Go |
| IdP | Azure AD (Entra ID) as the identity source; connect on-premises AD via AD Connect if hybrid |

Plan your Management Group tree before starting. Changes to MG hierarchy are disruptive once policy assignments exist.

---

## Create Management Group Hierarchy

Management Groups allow you to apply Azure Policy and RBAC across multiple subscriptions.

**Enable Management Groups in the tenant:**

```bash
az account management-group create --name "root-mg" --display-name "Tenant Root"
```


```text title="Expected output"
{
  "id": "/providers/Microsoft.Management/managementGroups/root-mg",
  "name": "root-mg",
  "displayName": "Tenant Root",
  "tenantId": "72f988bf-86f1-41af-91ab-2d7cd011db47",
  "type": "/providers/Microsoft.Management/managementGroups",
  "childrenCount": 0,
  "children": []
}
```

!!! warning "Common errors"
    **`The user 'user@contoso.com' does not have authorization to perform action 'Microsoft.Management/managementGroups/write' over scope '/providers/Microsoft.Management/managementGroups/root-mg'.`** — Assign the user the "Management Group Contributor" role at the tenant root scope.
    **`Management group with name 'root-mg' already exists.`** — Use a different name or delete the existing management group with `az account management-group delete --name "root-mg"`.
**Create the standard hierarchy:**

```bash
# Platform group — subscriptions for shared services
az account management-group create \
    --name "platform" \
    --display-name "Platform" \
    --parent "root-mg"

# Landing Zones group — workload subscriptions
az account management-group create \
    --name "landing-zones" \
    --display-name "Landing Zones" \
    --parent "root-mg"

# Environment sub-groups
az account management-group create \
    --name "lz-production" --display-name "Production" --parent "landing-zones"
az account management-group create \
    --name "lz-dev" --display-name "Development" --parent "landing-zones"

# Sandbox group — unrestricted for experimentation
az account management-group create \
    --name "sandbox" --display-name "Sandbox" --parent "root-mg"
```


```text title="Expected output"
{
  "id": "/providers/Microsoft.Management/managementGroups/platform",
  "name": "platform",
  "displayName": "Platform",
  "tenantId": "12345678-1234-1234-1234-123456789012",
  "type": "/providers/Microsoft.Management/managementGroups",
  "parentId": "/providers/Microsoft.Management/managementGroups/root-mg"
}
{
  "id": "/providers/Microsoft.Management/managementGroups/landing-zones",
  "name": "landing-zones",
  "displayName": "Landing Zones",
  "tenantId": "12345678-1234-1234-1234-123456789012",
  "type": "/providers/Microsoft.Management/managementGroups",
  "parentId": "/providers/Microsoft.Management/managementGroups/root-mg"
}
{
  "id": "/providers/Microsoft.Management/managementGroups/lz-production",
  "name": "lz-production",
  "displayName": "Production",
  "tenantId": "12345678-1234-1234-1234-123456789012",
  "type": "/providers/Microsoft.Management/managementGroups",
  "parentId": "/providers/Microsoft.Management/managementGroups/landing-zones"
}
{
  "id": "/providers/Microsoft.Management/managementGroups/lz-dev",
  "name": "lz-dev",
  "displayName": "Development",
  "tenantId": "12345678-1234-1234-1234-123456789012",
  "type": "/providers/Microsoft.Management/managementGroups",
  "parentId": "/providers/Microsoft.Management/managementGroups/landing-zones"
}
{
  "id": "/providers/Microsoft.Management/managementGroups/sandbox",
  "name": "sandbox",
  "displayName": "Sandbox",
  "tenantId": "12345678-1234-1234-1234-123456789012",
  "type": "/providers/Microsoft.Management/managementGroups",
  "parentId": "/providers/Microsoft.Management/managementGroups/root-mg"
}
```

!!! warning "Common errors"
    **`Management group 'root-mg' not found`** — Ensure the root management group exists or use your tenant root group ID (typically your tenant name) as the parent.
    **`Insufficient privileges to create management groups`** — Verify your account has the Management Group Contributor role assigned at the tenant root scope.
    **`Management group 'platform' already exists`** — Use `az account management-group show --name platform` to verify existing groups, then skip or delete duplicates before recreating.
**Move subscriptions under the correct MG:**

```bash
az account management-group subscription add \
    --name "platform" \
    --subscription <subscription-id>
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`The subscription '<subscription-id>' could not be found.`** — Verify the subscription ID is correct and exists in your Azure tenant by running `az account subscription list`.
    **`You do not have permission to perform action 'Microsoft.Management/managementGroups/subscriptions/write' on scope '/subscriptions/<subscription-id>'.`** — Ensure your Azure account has Owner or Management Group Contributor role on the "platform" management group.
---

## Configure Azure Policy at Management Group Level

Assign security initiatives at the Management Group level so all current and future subscriptions inherit them.

**Assign the Azure Security Benchmark initiative:**

```bash
az policy assignment create \
    --name "asb-baseline" \
    --display-name "Azure Security Benchmark" \
    --policy-set-definition "1f3afdf9-d0c9-4c3d-847f-89da613e70a8" \
    --scope "/providers/Microsoft.Management/managementGroups/root-mg" \
    --enforcement-mode DoNotEnforce
```


```text title="Expected output"
{
  "description": null,
  "displayName": "Azure Security Benchmark",
  "enforcementMode": "DoNotEnforce",
  "id": "/providers/Microsoft.Management/managementGroups/root-mg/providers/Microsoft.Authorization/policyAssignments/asb-baseline",
  "identity": null,
  "location": null,
  "metadata": {
    "createdBy": "12345678-1234-1234-1234-123456789012",
    "createdOn": "2024-01-15T09:42:33.847291+00:00",
    "updatedBy": "12345678-1234-1234-1234-123456789012",
    "updatedOn": "2024-01-15T09:42:33.847291+00:00"
  },
  "name": "asb-baseline",
  "notScopes": null,
  "parameters": null,
  "policyDefinitionId": "/subscriptions/00000000-0000-0000-0000-000000000000/providers/Microsoft.Authorization/policySetDefinitions/1f3afdf9-d0c9-4c3d-847f-89da613e70a8",
  "scope": "/providers/Microsoft.Management/managementGroups/root-mg",
  "type": "Microsoft.Authorization/policyAssignments"
}
```

!!! warning "Common errors"
    **`The policy set definition '1f3afdf9-d0c9-4c3d-847f-89da613e70a8' could not be found.`** — Verify the policy definition ID exists in your tenant using `az policy set-definition list` and copy the correct ID.
    **`The scope '/providers/Microsoft.Management/managementGroups/root-mg' is invalid or does not exist.`** — Confirm the management group exists and use the correct scope format from `az account management-group list`.
Use `DoNotEnforce` (Audit only) initially. Switch to `Default` (Deny) after remediating existing findings.

**Assign the CIS Microsoft Azure Foundations initiative:**

```bash
az policy assignment create \
    --name "cis-azure-foundations" \
    --display-name "CIS Microsoft Azure Foundations Benchmark" \
    --policy-set-definition "612b5213-9160-4969-8578-1518bd2a000c" \
    --scope "/providers/Microsoft.Management/managementGroups/root-mg" \
    --enforcement-mode DoNotEnforce
```


```text title="Expected output"
{
  "description": null,
  "displayName": "CIS Microsoft Azure Foundations Benchmark",
  "enforcementMode": "DoNotEnforce",
  "id": "/providers/Microsoft.Management/managementGroups/root-mg/providers/Microsoft.Authorization/policyAssignments/cis-azure-foundations",
  "identity": null,
  "location": null,
  "metadata": {
    "createdBy": "00000000-0000-0000-0000-000000000000",
    "createdOn": "2024-01-15T14:32:18.123456Z",
    "updatedBy": "00000000-0000-0000-0000-000000000000",
    "updatedOn": "2024-01-15T14:32:18.123456Z"
  },
  "name": "cis-azure-foundations",
  "notScopes": null,
  "policyDefinitionId": "/subscriptions/12345678-1234-1234-1234-123456789012/providers/Microsoft.Authorization/policySetDefinitions/612b5213-9160-4969-8578-1518bd2a000c",
  "scope": "/providers/Microsoft.Management/managementGroups/root-mg",
  "type": "Microsoft.Authorization/policyAssignments"
}
```

!!! warning "Common errors"
    **`The policy set definition '612b5213-9160-4969-8578-1518bd2a000c' could not be found.`** — Verify the policy definition ID exists in your subscription or use `az policy set-definition list` to find the correct ID.
    **`The user does not have permission to perform action 'Microsoft.Authorization/policyAssignments/write' on scope '/providers/Microsoft.Management/managementGroups/root-mg'.`** — Ensure your account has Owner or Policy Contributor role on the management group.
    **`Invalid scope '/providers/Microsoft.Management/managementGroups/root-mg': management group 'root-mg' does not exist.`** — Replace the scope with a valid management group ID from `az account management-group list`.
Review compliance:

```bash
az policy state summarize \
    --management-group root-mg \
    --query "[].{Policy:policyAssignmentName, Compliant:results.compliantResources, NonCompliant:results.nonCompliantResources}"
```


```text title="Expected output"
[
  {
    "Policy": "Enforce-HTTPS-Only",
    "Compliant": 47,
    "NonCompliant": 3
  },
  {
    "Policy": "Require-Tags-Environment",
    "Compliant": 89,
    "NonCompliant": 12
  },
  {
    "Policy": "Deny-Unencrypted-Storage",
    "Compliant": 156,
    "NonCompliant": 8
  },
  {
    "Policy": "Audit-Public-IPs",
    "Compliant": 203,
    "NonCompliant": 19
  }
]
```

!!! warning "Common errors"
    **`ERROR: The client 'user@contoso.com' with object id '12345678-1234-1234-1234-123456789012' does not have authorization to perform action 'Microsoft.Authorization/policyStates/queryResults/action'`** — Assign the "Policy Insights Data Writer" or "Reader" role to your user on the management group.
    **`ERROR: Management group 'root-mg' not found.`** — Verify the management group ID with `az account management-group list` and use the correct name.
    **`ERROR: No policy state data available for the specified scope.`** — Ensure policies are assigned to the management group and resources have been evaluated; wait 15–30 minutes after assignment for initial compliance data.
---

## Configure Microsoft Defender for Cloud

Enable Defender plans across all subscriptions in the Landing Zones MG.

```bash
# Enable Defender for Servers (Plan 2)
az security pricing create \
    --name VirtualMachines \
    --tier Standard \
    --subscription <subscription-id>

# Enable Defender for Storage
az security pricing create --name StorageAccounts --tier Standard --subscription <subscription-id>

# Enable Defender for SQL
az security pricing create --name SqlServers --tier Standard --subscription <subscription-id>

# Enable Defender for App Service
az security pricing create --name AppServices --tier Standard --subscription <subscription-id>
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Security/pricings/VirtualMachines",
  "name": "VirtualMachines",
  "pricingTier": "Standard",
  "freeTrialRemainingDays": 0,
  "type": "Microsoft.Security/pricings"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Security/pricings/StorageAccounts",
  "name": "StorageAccounts",
  "pricingTier": "Standard",
  "freeTrialRemainingDays": 0,
  "type": "Microsoft.Security/pricings"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Security/pricings/SqlServers",
  "name": "SqlServers",
  "pricingTier": "Standard",
  "freeTrialRemainingDays": 0,
  "type": "Microsoft.Security/pricings"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Security/pricings/AppServices",
  "name": "AppServices",
  "pricingTier": "Standard",
  "freeTrialRemainingDays": 0,
  "type": "Microsoft.Security/pricings"
}
```

!!! warning "Common errors"
    **`(AuthorizationFailed) The client 'user@contoso.com' with object id '12345678-1234-1234-1234-123456789012' does not have authorization to perform action 'Microsoft.Security/pricings/write' over scope '/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/providers/Microsoft.Security/pricings/VirtualMachines'.`** — Assign the Security Admin or Owner role to the user on the target subscription.
    **`(InvalidRequest) Pricing tier 'Standard' is not valid for resource type 'VirtualMachines'. Valid values are: 'Free', 'Standard'.`** — Verify the pricing tier name matches the exact case and valid options for the resource type.
    **`(ResourceNotFound) The subscription 'a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d' could not be found.`** — Replace `<subscription-id>` with a valid subscription ID from `az account list`.
Configure security contacts:

```bash
az security contact create \
    --name default \
    --email security@corp.com \
    --phone "+1-555-000-0000" \
    --alert-notifications On \
    --alerts-to-admins On
```


```text title="Expected output"
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/providers/Microsoft.Security/securityContacts/default",
  "name": "default",
  "type": "Microsoft.Security/securityContacts",
  "properties": {
    "email": "security@corp.com",
    "phone": "+1-555-000-0000",
    "alertNotifications": "On",
    "alertsToAdmins": "On"
  }
}
```

!!! warning "Common errors"
    **`ERROR: (ResourceNotFound) The resource of type 'securityContacts' with name 'default' could not be found.`** — Ensure you are authenticated with `az login` and have the correct subscription selected via `az account set --subscription <subscription-id>`.
    **`ERROR: Invalid email address format: security@corp.com`** — Use a valid email format; verify the domain exists and the email parameter is not malformed.
    **`ERROR: (AuthorizationFailed) The client 'user@corp.com' with object id '...' does not have authorization to perform action 'Microsoft.Security/securityContacts/write' over scope '/subscriptions/...'`** — Grant the user the Security Admin or Owner role on the subscription using `az role assignment create`.
---

## Set Up Log Analytics Workspace and Sentinel

All platform and workload logs should flow into a centralised Log Analytics workspace before Sentinel is enabled.

**Create the Log Analytics workspace:**

```bash
az monitor log-analytics workspace create \
    --resource-group rg-platform-monitoring \
    --workspace-name law-platform-prod \
    --location eastus \
    --sku PerGB2018 \
    --retention-time 90
```


```text title="Expected output"
{
  "createdDate": "2024-01-15T14:32:47.123456+00:00",
  "customerId": "d4f8c9e2-7a1b-4d6f-9e3c-2b5a8f1d4c7e",
  "eTag": "\"0x8DBE8F2C4A5B6C7D\"",
  "features": {
    "clusterResourceId": null,
    "disableLocalAuth": false,
    "enableLogAccessUsingOnlyResourcePermissions": false
  },
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourcegroups/rg-platform-monitoring/providers/microsoft.operationalinsights/workspaces/law-platform-prod",
  "location": "eastus",
  "name": "law-platform-prod",
  "provisioningState": "Succeeded",
  "publicNetworkAccessForIngestion": "Enabled",
  "publicNetworkAccessForQuery": "Enabled",
  "resourceGroup": "rg-platform-monitoring",
  "retentionInDays": 90,
  "sku": {
    "capacityReservationLevel": null,
    "lastSkuUpdate": "2024-01-15T14:32:47.123456+00:00",
    "maxCapacityReservationLevel": 3000,
    "name": "PerGB2018"
  },
  "tags": {},
  "type": "Microsoft.OperationalInsights/workspaces"
}
```

!!! warning "Common errors"
    **`ResourceGroupNotFound: Resource group 'rg-platform-monitoring' could not be found.`** — Create the resource group first using `az group create --name rg-platform-monitoring --location eastus`.
    **`InvalidSkuName: The provided SKU 'PerGB2018' is not valid for this subscription.`** — Verify available SKUs with `az monitor log-analytics workspace list-skus` or use a valid SKU like `PerGB2018` or `CapacityReservation`.
**Enable Microsoft Sentinel on the workspace:**

```bash
az sentinel workspace create \
    --resource-group rg-platform-monitoring \
    --workspace-name law-platform-prod
```


```text title="Expected output"
{
  "etag": "W/\"1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-platform-monitoring/providers/Microsoft.OperationalInsights/workspaces/law-platform-prod",
  "location": "eastus",
  "name": "law-platform-prod",
  "provisioningState": "Succeeded",
  "publicNetworkAccessForIngestion": "Enabled",
  "publicNetworkAccessForQuery": "Enabled",
  "resourceGroup": "rg-platform-monitoring",
  "retentionInDays": 30,
  "sku": {
    "name": "PerGB2018"
  },
  "tags": {},
  "type": "Microsoft.OperationalInsights/workspaces"
}
```

!!! warning "Common errors"
    **`ResourceGroupNotFound : The resource group 'rg-platform-monitoring' could not be found.`** — Verify the resource group exists in your subscription using `az group list` and correct the `--resource-group` parameter.
    **`InvalidResourceName : The value of the parameter workspaceName is invalid.`** — Ensure the workspace name contains only alphanumeric characters and hyphens, is 4-63 characters long, and doesn't start with a hyphen.
    **`AuthorizationFailed : The client 'user@example.com' with object id '...' does not have authorization to perform action 'Microsoft.OperationalInsights/workspaces/write'.`** — Assign the "Log Analytics Contributor" role to your user account on the resource group using `az role assignment create`.
**Connect core data connectors via the Sentinel portal:**

Navigate to Sentinel → Data Connectors and enable:

| Connector | Data Source |
|-----------|------------|
| Azure Active Directory | Sign-in logs, audit logs |
| Azure Activity | Subscription-level operations |
| Microsoft Defender for Cloud | Security alerts |
| Microsoft 365 Defender | Endpoint, identity, and cloud app signals |

For each connector, follow the wizard to grant the required permissions and complete the configuration.

---

## Configure Entra ID (Azure AD) Baseline

**Enable MFA for all users:**

```text
Portal → Entra ID → Security → Conditional Access → New Policy
Name: Require MFA for All Users
Assignments → Users: All Users
Access Controls → Grant: Require multi-factor authentication
Enable policy: Report-only first, then On
```

**Enable Identity Protection:**

```bash
az ad identity-protection user-risk-policy update \
    --operator "greaterThan" \
    --risk-level "medium" \
    --mfa-required true
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`ERROR: unrecognized arguments: --operator`** — Use `--risk-level` and `--mfa-required` only; `--operator` is not a valid parameter for this command.
    **`ERROR: argument --risk-level: invalid choice: 'medium' (choose from 'low', 'medium', 'high')`** — Ensure the risk level value matches one of the accepted enum values exactly.
**Configure PIM for privileged roles:**

1. Portal → Entra ID → Privileged Identity Management → Azure AD Roles.
2. Set `Global Administrator` and `Subscription Owner` to require activation with MFA and justification.
3. Set maximum activation duration to 8 hours.
4. Enable alerts for permanent role assignments.

**Create Conditional Access policy — block legacy authentication:**

```text
Name: Block Legacy Authentication
Assignments → Users: All Users
Conditions → Client Apps: Exchange ActiveSync and Other clients (checked)
Access Controls → Block
```

---

## Set Up Hub VNet and Peering

The Hub-and-Spoke network topology centralises security and routing through the Hub VNet.

```bash
# Create Hub VNet
az network vnet create \
    --resource-group rg-platform-network \
    --name vnet-hub-prod \
    --address-prefix 10.0.0.0/16 \
    --location eastus

# Hub subnets
az network vnet subnet create \
    --resource-group rg-platform-network \
    --vnet-name vnet-hub-prod \
    --name AzureFirewallSubnet \
    --address-prefix 10.0.1.0/26

az network vnet subnet create \
    --resource-group rg-platform-network \
    --vnet-name vnet-hub-prod \
    --name AzureBastionSubnet \
    --address-prefix 10.0.2.0/27

# Create a Spoke VNet
az network vnet create \
    --resource-group rg-workload-prod \
    --name vnet-spoke-prod \
    --address-prefix 10.1.0.0/16 \
    --location eastus

# Peer Hub to Spoke
az network vnet peering create \
    --resource-group rg-platform-network \
    --name hub-to-spoke-prod \
    --vnet-name vnet-hub-prod \
    --remote-vnet /subscriptions/<sub-id>/resourceGroups/rg-workload-prod/providers/Microsoft.Network/virtualNetworks/vnet-spoke-prod \
    --allow-forwarded-traffic true \
    --allow-gateway-transit true

# Peer Spoke to Hub
az network vnet peering create \
    --resource-group rg-workload-prod \
    --name spoke-to-hub-prod \
    --vnet-name vnet-spoke-prod \
    --remote-vnet /subscriptions/<sub-id>/resourceGroups/rg-platform-network/providers/Microsoft.Network/virtualNetworks/vnet-hub-prod \
    --use-remote-gateways false
```


```text title="Expected output"
{
  "addressSpace": {
    "addressPrefixes": [
      "10.0.0.0/16"
    ]
  },
  "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/rg-platform-network/providers/Microsoft.Network/virtualNetworks/vnet-hub-prod",
  "location": "eastus",
  "name": "vnet-hub-prod",
  "provisioningState": "Succeeded",
  "resourceGroup": "rg-platform-network"
}
{
  "addressPrefix": "10.0.1.0/26",
  "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/rg-platform-network/providers/Microsoft.Network/virtualNetworks/vnet-hub-prod/subnets/AzureFirewallSubnet",
  "name": "AzureFirewallSubnet",
  "provisioningState": "Succeeded"
}
{
  "addressPrefix": "10.0.2.0/27",
  "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/rg-platform-network/providers/Microsoft.Network/virtualNetworks/vnet-hub-prod/subnets/AzureBastionSubnet",
  "name": "AzureBastionSubnet",
  "provisioningState": "Succeeded"
}
{
  "addressSpace": {
    "addressPrefixes": [
      "10.1.0.0/16"
    ]
  },
  "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/rg-workload-prod/providers/Microsoft.Network/virtualNetworks/vnet-spoke-prod",
  "location": "eastus",
  "name": "vnet-spoke-prod",
  "provisioningState": "Succeeded",
  "resourceGroup": "rg-workload-prod"
}
{
  "allowForwardedTraffic": true,
  "allowGatewayTransit": true,
  "allowVirtualNetworkAccess": true,
  "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/rg-platform-network/providers/Microsoft.Network/virtualNetworks/vnet-hub-prod/peerings/hub-to-spoke-prod",
  "name": "hub-to-spoke-prod",
  "peeringState": "Initiated",
  "provisioningState": "Succeeded"
}
{
  "allowForwardedTraffic": false,
  "allowGatewayTransit": false,
  "allowVirtualNetworkAccess": true,
  "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/rg-workload-prod/providers/Microsoft.
```
Deploy Azure Bastion for secure VM access:

```bash
az network bastion create \
    --resource-group rg-platform-network \
    --name bastion-hub-prod \
    --vnet-name vnet-hub-prod \
    --location eastus
```


```text title="Expected output"
{
  "dnsSettings": null,
  "etag": "W/\"a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p\"",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-platform-network/providers/Microsoft.Network/bastionHosts/bastion-hub-prod",
  "ipConfigurations": [
    {
      "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-platform-network/providers/Microsoft.Network/bastionHosts/bastion-hub-prod/bastionHostIpConfigurations/IpConf",
      "name": "IpConf",
      "privateIpAddress": "10.0.1.4",
      "privateIpAllocationMethod": "Dynamic",
      "publicIpAddress": {
        "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-platform-network/providers/Microsoft.Network/publicIPAddresses/pip-bastion-hub-prod",
        "resourceGroup": "rg-platform-network"
      },
      "subnet": {
        "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-platform-network/providers/Microsoft.Network/virtualNetworks/vnet-hub-prod/subnets/AzureBastionSubnet",
        "resourceGroup": "rg-platform-network"
      }
    }
  ],
  "location": "eastus",
  "name": "bastion-hub-prod",
  "provisioningState": "Succeeded",
  "resourceGroup": "rg-platform-network",
  "sku": {
    "name": "Basic"
  },
  "type": "Microsoft.Network/bastionHosts"
}
```

!!! warning "Common errors"
    **`(ResourceNotFound) Resource 'Microsoft.Network/virtualNetworks/vnet-hub-prod' under resource group 'rg-platform-network' was not found.`** — Verify the virtual network name and resource group exist using `az network vnet list --resource-group rg-platform-network`.
    **`(InvalidResourceReference) The subnet 'AzureBastionSubnet' does not exist in virtual network 'vnet-hub-prod'.`** — Create the required AzureBastionSubnet with address prefix /26 or larger using `az network vnet subnet create --resource-group rg-platform-network --vnet-name vnet-hub-prod --name AzureBastionSubnet --address-prefix 10.0.1.0/26`.
    **`(AuthorizationFailed) The client 'user@contoso.com' with object id 'a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p' does not have permission to perform action 'Microsoft.Network/bastionHosts/write' over scope '/subscriptions/12345678-1234-1234-1234-123456789
---

## Enable Azure Backup Vault

Create a Recovery Services vault for centralised backup management.

```bash
az backup vault create \
    --resource-group rg-platform-backup \
    --name rsv-platform-prod \
    --location eastus

# Create a backup policy (daily, 30-day retention)
az backup policy create \
    --resource-group rg-platform-backup \
    --vault-name rsv-platform-prod \
    --name DailyVMPolicy \
    --policy '{
      "schedulePolicy": {"schedulePolicyType": "SimpleSchedulePolicy", "scheduleRunFrequency": "Daily", "scheduleRunTimes": ["2023-01-01T02:00:00Z"]},
      "retentionPolicy": {"retentionPolicyType": "LongTermRetentionPolicy", "dailySchedule": {"retentionTimes": ["2023-01-01T02:00:00Z"], "retentionDuration": {"count": 30, "durationType": "Days"}}}
    }'
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/rg-platform-backup/providers/Microsoft.RecoveryServices/vaults/rsv-platform-prod",
  "location": "eastus",
  "name": "rsv-platform-prod",
  "properties": {
    "encryption": {
      "keyVaultProperties": null,
      "kmsKeyVaultProperties": null
    },
    "publicNetworkAccess": "Enabled"
  },
  "resourceGroup": "rg-platform-backup",
  "type": "Microsoft.RecoveryServices/vaults"
}
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/rg-platform-backup/providers/Microsoft.RecoveryServices/vaults/rsv-platform-prod/backupPolicies/DailyVMPolicy",
  "name": "DailyVMPolicy",
  "properties": {
    "backupManagementType": "AzureIaaSVM",
    "retentionPolicy": {
      "dailySchedule": {
        "retentionDuration": {
          "count": 30,
          "durationType": "Days"
        },
        "retentionTimes": [
          "2023-01-01T02:00:00Z"
        ]
      },
      "retentionPolicyType": "LongTermRetentionPolicy"
    },
    "schedulePolicy": {
      "scheduleRunFrequency": "Daily",
      "scheduleRunTimes": [
        "2023-01-01T02:00:00Z"
      ],
      "schedulePolicyType": "SimpleSchedulePolicy"
    }
  },
  "resourceGroup": "rg-platform-backup",
  "type": "Microsoft.RecoveryServices/backupPolicies"
}
```

!!! warning "Common errors"
    **`ResourceGroupNotFound`** — Verify the resource group exists with `az group list` and create it if needed using `az group create --name rg-platform-backup --location eastus`.
    **`InvalidJsonInput`** — Escape the JSON policy string properly by using single quotes around the entire JSON block or save the policy to a file and reference it with `@policy.json`.
Enable backup for a VM:

```bash
az backup protection enable-for-vm \
    --resource-group rg-workload-prod \
    --vault-name rsv-platform-prod \
    --vm <vm-name> \
    --policy-name DailyVMPolicy
```


```text title="Expected output"
Command group 'backup protection' is deprecated and will be removed in a future release. Use 'backup protection enable-for-vm' instead.
Request sent to enable backup protection for VM 'vm-web-prod-01'.
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-workload-prod/providers/Microsoft.RecoveryServices/vaults/rsv-platform-prod/backupFabrics/Azure/protectionContainers/IaasVMContainer;iaasvmcontainerv2;rg-workload-prod;vm-web-prod-01/protectedItems/VM;iaasvmcontainerv2;rg-workload-prod;vm-web-prod-01",
  "name": "vm-web-prod-01",
  "properties": {
    "protectionStatus": "Protected",
    "protectionState": "IRPending",
    "policyId": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-workload-prod/providers/Microsoft.RecoveryServices/vaults/rsv-platform-prod/backupPolicies/DailyVMPolicy",
    "lastBackupStatus": "Pending",
    "lastBackupTime": null
  },
  "type": "Microsoft.RecoveryServices/vaults/backupFabrics/protectionContainers/protectedItems"
}
```

!!! warning "Common errors"
    **`ResourceNotFound: The resource 'Microsoft.Compute/virtualMachines/vm-web-prod-01' under resource group 'rg-workload-prod' was not found.`** — Verify the VM name and resource group name are correct using `az vm list --resource-group rg-workload-prod`.
    **`InvalidPolicyId: The policy 'DailyVMPolicy' was not found in vault 'rsv-platform-prod'.`** — List available policies with `az backup policy list --resource-group rg-workload-prod --vault-name rsv-platform-prod` and use an existing policy name.
    **`VaultNotFound: The Recovery Services vault 'rsv-platform-prod' was not found in resource group 'rg-workload-prod'.`** — Confirm the vault exists and the resource group name is spelled correctly using `az backup vault list --resource-group rg-workload-prod`.
---

## Validate the Deployment

**Defender for Cloud Secure Score:**

```bash
az security secure-score show --name ascScore
```


```text title="Expected output"
{
  "displayName": "Secure Score",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/providers/Microsoft.Security/secureScores/ascScore",
  "name": "ascScore",
  "percentage": 42.5,
  "resourceGroup": null,
  "subscriptionId": "12345678-1234-1234-1234-123456789012",
  "type": "Microsoft.Security/secureScores",
  "weight": 0
}
```

!!! warning "Common errors"
    **`ERROR: (ResourceNotFound) The resource 'Microsoft.Security/secureScores/ascScore' under resource group '<subscription>' was not found.`** — Ensure Azure Security Center is enabled on your subscription and the secure score has been calculated at least once.
    **`ERROR: (AuthorizationFailed) The client '<user>' with object id '<id>' does not have authorization to perform action 'Microsoft.Security/secureScores/read' over scope '/subscriptions/<id>'.`** — Grant the user or service principal the "Security Reader" or "Owner" role on the subscription using `az role assignment create`.
Target is 70% or higher before onboarding workloads.

**Policy compliance report:**

```bash
az policy state summarize --management-group root-mg
```


```text title="Expected output"
{
  "results": {
    "nonCompliantResources": 1247,
    "compliantResources": 8934,
    "resourceDetails": [
      {
        "resourceId": "/subscriptions/a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01",
        "complianceState": "NonCompliant",
        "policyAssignmentId": "/providers/Microsoft.Management/managementGroups/root-mg/providers/Microsoft.Authorization/policyAssignments/enforce-encryption",
        "policyDefinitionId": "/providers/Microsoft.Authorization/policyDefinitions/require-disk-encryption"
      },
      {
        "resourceId": "/subscriptions/b2c3d4e5-f6a7-5b6c-9d0e-1f2a3b4c5d6e/resourceGroups/dev-rg/providers/Microsoft.Storage/storageAccounts/devstg2024",
        "complianceState": "NonCompliant",
        "policyAssignmentId": "/providers/Microsoft.Management/managementGroups/root-mg/providers/Microsoft.Authorization/policyAssignments/enforce-https",
        "policyDefinitionId": "/providers/Microsoft.Authorization/policyDefinitions/require-https-storage"
      }
    ],
    "summary": {
      "queryResultsUnitCount": 10181,
      "nonCompliantResourcesCount": 1247,
      "compliantResourcesCount": 8934
    }
  }
}
```

!!! warning "Common errors"
    **`ERROR: The user does not have authorization to perform action 'Microsoft.PolicyInsights/policyStates/summarize/action' over the requested scope.`** — Ensure your Azure account has Reader or Policy Insights Data Writer role assigned at the management group scope.
    **`ERROR: Management group 'root-mg' not found.`** — Verify the management group ID exists and use the correct name with `az account management-group list`.
**Verify Sentinel is receiving logs:**

Run a KQL query in the Sentinel Logs blade:

```kql
AzureActivity
| where TimeGenerated > ago(1h)
| summarize count() by OperationNameValue
| order by count_ desc
| take 20
```

Results confirm Azure Activity logs are flowing.

**Test Bastion access:**

1. Portal → Virtual Machines → select a VM → Connect → Bastion.
2. Enter credentials and confirm the browser-based RDP or SSH session opens.

**Verify MG hierarchy and policy assignments:**

```bash
az account management-group show --name root-mg --expand --recurse
az policy assignment list --scope "/providers/Microsoft.Management/managementGroups/root-mg"
```


```text title="Expected output"
{
  "displayName": "root-mg",
  "id": "/providers/Microsoft.Management/managementGroups/root-mg",
  "name": "root-mg",
  "tenantId": "72f988bf-86f1-41af-91ab-2d7cd011db47",
  "type": "Microsoft.Management/managementGroups",
  "children": [
    {
      "displayName": "Production",
      "id": "/providers/Microsoft.Management/managementGroups/prod-mg",
      "name": "prod-mg",
      "type": "Microsoft.Management/managementGroups"
    },
    {
      "displayName": "Staging",
      "id": "/providers/Microsoft.Management/managementGroups/staging-mg",
      "name": "staging-mg",
      "type": "Microsoft.Management/managementGroups"
    }
  ]
}
[
  {
    "id": "/providers/Microsoft.Management/managementGroups/root-mg/providers/Microsoft.Authorization/policyAssignments/audit-storage-https",
    "name": "audit-storage-https",
    "type": "Microsoft.Authorization/policyAssignments",
    "displayName": "Audit Storage HTTPS Only",
    "policyDefinitionId": "/providers/Microsoft.Authorization/policyDefinitions/404c3081-a854-4457-ae30-26a93ef643f9"
  },
  {
    "id": "/providers/Microsoft.Management/managementGroups/root-mg/providers/Microsoft.Authorization/policyAssignments/enforce-tags",
    "name": "enforce-tags",
    "type": "Microsoft.Authorization/policyAssignments",
    "displayName": "Enforce Required Tags"
  }
]
```

!!! warning "Common errors"
    **`ERROR: Management group 'root-mg' not found.`** — Verify the management group name with `az account management-group list` and use the correct name.
    **`ERROR: The user does not have authorization to perform action 'Microsoft.Authorization/policyAssignments/read' over scope '/providers/Microsoft.Management/managementGroups/root-mg'.`** — Ensure your Azure account has Reader or higher role assigned at the management group scope.
---

## Verify

- Confirm the service or component is running and reachable
- Check management UI for any errors or warnings
- Run a basic functional test (login, read, write) to confirm end-to-end operation

---

## See also

- [Azure — Procedures](../operations/procedures/)
- [Azure — Common Issues](../troubleshooting/common-issues/)
- [Azure — How It Works](../architecture/how-it-works/)
