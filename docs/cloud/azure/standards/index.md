# Azure Standards

## Naming Convention

Pattern: `<type>-<env>-<region>-<name>[-<seq>]` using CAF abbreviations:

| Resource | Example |
|---|---|
| Resource Group | `rg-prod-euw-network` |
| Virtual Network | `vnet-prod-euw-hub` |
| Subnet | `snet-prod-euw-app` |
| VM | `vm-prod-euw-appserver-01` |
| NSG | `nsg-prod-euw-app` |
| Key Vault | `kv-prod-euw-secrets` |
| Storage Account | `stcorpprodeuwa01` (no hyphens — SA naming is strict) |
| App Service | `app-prod-euw-apimain` |
| AKS Cluster | `aks-prod-euw-platform` |

Region abbreviations: `euw` = West Europe, `eun` = North Europe, `use` = East US.

Full CAF naming reference: [aka.ms/caf/naming](https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming).

## Tagging Policy

Mandatory tags enforced via Azure Policy deny assignments at Management Group level:

| Tag Key | Example | Enforcement |
|---|---|---|
| `Environment` | `prod`, `staging`, `dev` | Required on all resources |
| `Owner` | `infra-team` | Required on all resources |
| `CostCentre` | `CC-1234` | Required on all resource groups |
| `Application` | `erp-frontend` | Required on all resources |

```bash
# Verify tag compliance
az policy state list --resource-group <rg> \
    --filter "policyDefinitionId eq '/providers/Microsoft.Authorization/policyDefinitions/<required-tags-id>'" \
    --query "[?complianceState=='NonCompliant']"
```

## RBAC Standards

| Principle | Standard |
|---|---|
| Least privilege | Use built-in roles where possible; custom roles when built-in too broad |
| No Owner at subscription level for individuals | Use PIM-activated Owner for break-glass only |
| Service principals | Use managed identities where supported; service principal OIDC for CI/CD |
| Access reviews | Quarterly review of Contributor+ role assignments in production |
| PIM | All privileged roles require PIM justification and approval |

```bash
# List role assignments in subscription
az role assignment list --scope /subscriptions/<sub-id> --output table

# Identify stale role assignments (users not in Entra ID)
az role assignment list --scope /subscriptions/<sub-id> \
    --query "[?principalType=='User'].[principalId,roleDefinitionName]"
```

## Security Standards

| Control | Standard |
|---|---|
| Defender for Cloud | Enabled on all subscriptions; recommendations remediated to < 10% unhealthy |
| Azure Policy | CIS Azure Benchmark conformance pack assigned at root Management Group |
| Diagnostic settings | All resources → Log Analytics; Key Vault, NSG, Firewall also to Event Hub |
| VNet flow logs | Enabled on all VNets; 90-day retention |
| Key Vault | Soft delete + purge protection enabled; private endpoint required for production |
| Encryption | All disks CMK or PMK (minimum); storage SSE with Microsoft-managed keys minimum |
| NSG rules | Description field mandatory; inbound ANY:ANY from internet denied by default |

## Resource Lock Standards

Apply locks to prevent accidental deletion of production infrastructure:

```bash
# Add delete lock to production resource group
az lock create --name "prod-rg-lock" --resource-group <rg> --lock-type CanNotDelete

# List locks
az lock list --resource-group <rg>
```

## Approved Regions

Azure resources may only be deployed in:
- `westeurope` — primary
- `northeurope` — secondary / DR

Enforced via Azure Policy: `Allowed locations` assignment at root Management Group.
