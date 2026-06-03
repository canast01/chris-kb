# Azure Integration

<div class="kb-summary">
Azure Integration reference covering Azure VM Deployment Flow, Azure AD Connect (Hybrid Identity), Azure Monitor → SIEM, GitHub Actions + OIDC Federation, Terraform Remote State and 2 more sections.
</div>

## Azure VM Deployment Flow

```mermaid
flowchart LR
    request["Deployment Request\nPortal / CLI / Terraform"]
    rbacCheck["RBAC Check\nMicrosoft.Compute/virtualMachines/write"]
    policyCheck["Azure Policy Evaluation\nallowed SKUs · allowed regions"]
    resourceGroup["Resource Group\nrg-prod-euw-app"]
    vnetPlace["VNet / Subnet Placement\nsnet-prod-euw-app"]
    nsgApply["NSG Applied\ndefault rules + custom"]
    diskAttach["Managed Disk\nOS + data disks attached"]
    extensions["Extensions Applied\nMonitor Agent · Defender · Custom Script"]
    running["VM Running\nProvisioning State: Succeeded"]

    request --> rbacCheck --> policyCheck --> resourceGroup --> vnetPlace --> nsgApply --> diskAttach --> extensions --> running
```text
┌────────────────────────────────── Azure Architecture — Integrations ──────────────────────────────────┐
│                                                                                                       │
│  Azure integrates with on-premises via ExpressRoute/VPN, AD sync, and hybrid networking.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Identity Integration             │  │             Network Integration             │   │
│   │          Entra ID Connect: AD sync           │  │       ExpressRoute: private 1/10 Gbps       │   │
│   │          SAML/OIDC: federate to IdP          │  │        Site-to-Site VPN: IPSec tunnel       │   │
│   │      Password hash sync or passthrough       │  │       VNet Peering: cross-region VNets      │   │
│   │        Seamless SSO: transparent auth        │  │          Virtual WAN: hub-and-spoke         │   │
│   │       B2B: external partner identities       │  │        Private Endpoint: no internet        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  ExpressRoute bypasses internet; Private Endpoints restrict service access to VNet only.              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Data & App Integration            │  │            Monitoring Integration           │   │
│   │      Azure Arc: manage on-prem in Azure      │  │       Azure Monitor: unified telemetry      │   │
│   │       Logic Apps: workflow automation        │  │       Log Analytics: central log sink       │   │
│   │       API Management: gateway + portal       │  │       Defender for Cloud: posture mgmt      │   │
│   │      Event Grid: event routing service       │  │         Sentinel: cloud-native SIEM         │   │
│   │      Service Bus: enterprise messaging       │  │        Cost Management: billing view        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Azure global backbone · ExpressRoute partner peering locations · Regional POPs                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Entra ID Connect= Tool syncing on-premises AD users and groups to Entra ID                           │
│  Password hash sync= Syncs hashed passwords; allows cloud auth without on-prem dependency             │
│  PassthroughAuth = Validates passwords against on-prem AD; requires agent online                      │
│  ExpressRoute    = Dedicated private circuit to Azure bypassing public internet                       │
│  S2S VPN         = IPSec/IKEv2 encrypted tunnel over internet to Azure VPN Gateway                    │
│  Virtual WAN     = Azure managed hub-and-spoke network for global connectivity                        │
│  Azure Arc       = Extends Azure management plane to on-prem and multi-cloud resources                │
│  Private Endpoint= NIC in VNet with private IP for a PaaS service; no public exposure                 │
│  B2B federation  = Allows external Azure AD/Entra tenants to access your resources                    │
│  Seamless SSO    = Kerberos-based SSO for domain-joined machines accessing Azure apps                 │
│  Event Grid      = Publish-subscribe event routing service; connects Azure services                   │
│  Azure Sentinel  = Cloud-native SIEM/SOAR; ingests logs and generates security alerts                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Azure AD Connect (Hybrid Identity)

```powershell
# Check AD Connect sync status
Import-Module ADSync
Get-ADSyncScheduler           # Verify SyncCycleEnabled = True
Get-ADSyncConnectorRunStatus  # Last sync status
```

Verify sync health in Entra ID admin center: Identity → Hybrid management → Azure AD Connect.

If sync fails:
```powershell
Start-ADSyncSyncCycle -PolicyType Delta   # Force delta sync
Start-ADSyncSyncCycle -PolicyType Initial # Full sync (slow — only if required)
```

## Azure Monitor → SIEM

Configure diagnostic settings to send to Log Analytics and Event Hub:

```bash
# Enable diagnostic settings on a resource (example: NSG)
az monitor diagnostic-settings create --name "to-log-analytics" \
    --resource <nsg-resource-id> \
    --workspace <log-analytics-workspace-id> \
    --logs '[{"category": "NetworkSecurityGroupEvent", "enabled": true}]'

# Stream to Splunk/Elastic via Event Hub
az eventhubs eventhub create --name azure-logs --namespace-name <ns> -g <rg>
# Configure Splunk Add-on for Microsoft Cloud Services to pull from Event Hub
```

## GitHub Actions + OIDC Federation

No client secrets — use OIDC:

```bash
# Create federated credential on service principal
az ad app federated-credential create --id <app-id> --parameters '{
  "name": "github-actions-main",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:org/repo:ref:refs/heads/main",
  "audiences": ["api://AzureADTokenExchange"]
}'
```

```yaml
# .github/workflows/deploy.yml
- uses: azure/login@v2
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

## Terraform Remote State

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "corpterraformstateprod"
    container_name       = "tfstate"
    key                  = "prod/vnet/terraform.tfstate"
  }
}
```

State storage account standards:
- Versioning enabled
- Soft delete enabled (30-day retention)
- Network access restricted to Terraform runner IPs

## Azure Backup

```bash
# List recovery vaults
az backup vault list --output table

# List protected items in vault
az backup item list --vault-name <vault> -g <rg> --output table

# Trigger ad-hoc backup
az backup protection backup-now --vault-name <vault> -g <rg> \
    --item-name <vm-name> --container-name <container> \
    --backup-management-type AzureIaasVM --retain-until 2026-12-31
```

## Key Vault Integration

```bash
# Verify Key Vault is accessible
az keyvault show --name <kv-name> --query 'properties.provisioningState'

# Grant access to a managed identity
az keyvault set-policy --name <kv-name> \
    --object-id <managed-identity-object-id> \
    --secret-permissions get list

# Test secret retrieval
az keyvault secret show --vault-name <kv-name> --name <secret-name>
```
