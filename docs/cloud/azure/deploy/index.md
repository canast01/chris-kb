# Azure — Subscription and Landing Zone Setup

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

**Move subscriptions under the correct MG:**

```bash
az account management-group subscription add \
    --name "platform" \
    --subscription <subscription-id>
```

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

Review compliance:

```bash
az policy state summarize \
    --management-group root-mg \
    --query "[].{Policy:policyAssignmentName, Compliant:results.compliantResources, NonCompliant:results.nonCompliantResources}"
```

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

Configure security contacts:

```bash
az security contact create \
    --name default \
    --email security@corp.com \
    --phone "+1-555-000-0000" \
    --alert-notifications On \
    --alerts-to-admins On
```

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

**Enable Microsoft Sentinel on the workspace:**

```bash
az sentinel workspace create \
    --resource-group rg-platform-monitoring \
    --workspace-name law-platform-prod
```

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

Deploy Azure Bastion for secure VM access:

```bash
az network bastion create \
    --resource-group rg-platform-network \
    --name bastion-hub-prod \
    --vnet-name vnet-hub-prod \
    --location eastus
```

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

Enable backup for a VM:

```bash
az backup protection enable-for-vm \
    --resource-group rg-workload-prod \
    --vault-name rsv-platform-prod \
    --vm <vm-name> \
    --policy-name DailyVMPolicy
```

---

## Validate the Deployment

**Defender for Cloud Secure Score:**

```bash
az security secure-score show --name ascScore
```

Target is 70% or higher before onboarding workloads.

**Policy compliance report:**

```bash
az policy state summarize --management-group root-mg
```

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
