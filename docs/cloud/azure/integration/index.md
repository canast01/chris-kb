# Azure Integration

## ExpressRoute + VPN Gateway

```bash
# Check ExpressRoute circuit status
az network express-route show --name <circuit-name> -g <rg> \
    --query '{CircuitProvisioningState:circuitProvisioningState,ServiceProviderProvisioningState:serviceProviderProvisioningState}'

# Check ExpressRoute peering state
az network express-route peering show --circuit-name <circuit-name> -g <rg> --name AzurePrivatePeering \
    --query 'state'

# VPN Gateway status (backup path)
az network vnet-gateway show -n <vpn-gw-name> -g <rg> --query 'provisioningState'
```

BGP routes from on-premises should appear in all spoke VNet effective routes:
```bash
az network nic show-effective-route-table -n <nic-name> -g <rg> | jq '.value[] | select(.source=="VpnGateway")'
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
