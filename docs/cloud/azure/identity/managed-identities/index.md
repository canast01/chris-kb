---
tags:
  - azure
description: "Managed identities give Azure resources an identity in Entra ID without requiring credentials in code or config."
---
# Azure — Managed Identities

<div class="kb-summary">
Managed identities give Azure resources an identity in Entra ID without requiring credentials in code or config.

*Applies to: Azure*
</div>

```d2
direction: down

userassigned: "User-Assigned" {shape: rectangle}
grant_access_via_rbac: "Grant Access via RBAC" {shape: rectangle}
using_the_identity_in_code: "Using the Identity in Code" {shape: rectangle}
aks_workload_identity: "AKS Workload Identity" {shape: rectangle}
common_issues: "Common Issues" {shape: rectangle}

userassigned -> grant_access_via_rbac: uses
grant_access_via_rbac -> using_the_identity_in_code: uses
using_the_identity_in_code -> aks_workload_identity: uses
aks_workload_identity -> common_issues: uses
```

## User-Assigned

```bash
# Create
az identity create \
  --name "my-workload-identity" \
  --resource-group <rg> \
  --location <region>

# Get IDs
az identity show \
  --name "my-workload-identity" \
  --resource-group <rg> \
  --query '{resourceId:id, clientId:clientId, principalId:principalId}' \
  --output json

# Assign to a VM
az vm identity assign \
  --name <vm-name> \
  --resource-group <rg> \
  --identities /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/my-workload-identity

# Assign to App Service
az webapp identity assign \
  --name <app-name> \
  --resource-group <rg> \
  --identities /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/my-workload-identity
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1cde/resourceGroups/prod-rg/providers/Microsoft.ManagedIdentity/userAssignedIdentities/my-workload-identity",
  "location": "eastus",
  "name": "my-workload-identity",
  "resourceGroup": "prod-rg",
  "type": "Microsoft.ManagedIdentity/userAssignedIdentities"
}
{
  "resourceId": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1cde/resourceGroups/prod-rg/providers/Microsoft.ManagedIdentity/userAssignedIdentities/my-workload-identity",
  "clientId": "a1b2c3d4-e5f6-47a8-b9c0-d1e2f3a4b5c6",
  "principalId": "f8e7d6c5-b4a3-2109-8765-4321fedcba98"
}
Identity assigned to VM 'web-server-01'.
Identity assigned to App Service 'api-backend-prod'.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceGroupNotFound` | Verify the resource group name with `az group list` and ensure it exists in the correct subscription. |
    | `InvalidResourceId` | Confirm the subscription ID, resource group name, and identity name in the full resource ID path match exactly with `az identity list --resource-group <rg>`. |
    | `AuthorizationFailed: The client does not have permission` | Ensure your Azure account has the Managed Identity Operator or Owner role on the target VM/App Service resource. |
## Grant Access via RBAC

```bash
# Grant the identity access to Key Vault secrets
az role assignment create \
  --assignee <principal-id> \
  --role "Key Vault Secrets User" \
  --scope /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.KeyVault/vaults/<vault-name>

# Grant access to a Storage Account (data plane)
az role assignment create \
  --assignee <principal-id> \
  --role "Storage Blob Data Reader" \
  --scope /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<account>
```


```text title="Expected output"
{
  "canDelegate": false,
  "condition": null,
  "conditionVersion": null,
  "createdBy": "admin@contoso.onmicrosoft.com",
  "createdOn": "2024-01-15T09:42:33.847392+00:00",
  "delegatedManagedIdentityResourceId": null,
  "description": null,
  "id": "/subscriptions/a1b2c3d4-e5f6-47a8-9b0c-1d2e3f4a5b6c/resourceGroups/prod-rg/providers/Microsoft.Authorization/roleAssignments/7f8e9d0c-1b2a-3f4e-5d6c-7b8a9f0e1d2c",
  "principalId": "f1e2d3c4-b5a6-47f8-9e0d-1c2b3a4f5e6d",
  "principalType": "ServicePrincipal",
  "roleDefinitionId": "/subscriptions/a1b2c3d4-e5f6-47a8-9b0c-1d2e3f4a5b6c/providers/Microsoft.Authorization/roleDefinitions/4633458b-17de-408a-b874-0445c86300d2",
  "scope": "/subscriptions/a1b2c3d4-e5f6-47a8-9b0c-1d2e3f4a5b6c/resourceGroups/prod-rg/providers/Microsoft.KeyVault/vaults/prod-kv-001",
  "updatedBy": "admin@contoso.onmicrosoft.com",
  "updatedOn": "2024-01-15T09:42:33.847392+00:00"
}
{
  "canDelegate": false,
  "condition": null,
  "conditionVersion": null,
  "createdBy": "admin@contoso.onmicrosoft.com",
  "createdOn": "2024-01-15T09:42:51.223614+00:00",
  "delegatedManagedIdentityResourceId": null,
  "description": null,
  "id": "/subscriptions/a1b2c3d4-e5f6-47a8-9b0c-1d2e3f4a5b6c/resourceGroups/prod-rg/providers/Microsoft.Authorization/roleAssignments/9a8b7c6d-5e4f-3a2b-1c0d-9e8f7a6b5c4d",
  "principalId": "f1e2d3c4-b5a6-47f8-9e0d-1c2b3a4f5e6d",
  "principalType": "ServicePrincipal",
  "roleDefinitionId": "/subscriptions/a1b2c3d4-e5f6-47a8-9b0c-1d2e3f4a5b6c/providers/Microsoft.Authorization/roleDefinitions/2a2b9908-6ea1-4ae2-8e65-a410df84e7
```
## Using the Identity in Code

### Python (Azure SDK)

```python
from azure.identity import ManagedIdentityCredential, DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# System-assigned
credential = ManagedIdentityCredential()

# User-assigned — specify client ID
credential = ManagedIdentityCredential(client_id="<client-id>")

# DefaultAzureCredential tries managed identity automatically in Azure
credential = DefaultAzureCredential()

client = SecretClient(vault_url="https://<vault>.vault.azure.net", credential=credential)
secret = client.get_secret("my-secret")
print(secret.value)
```

### Bash — raw IMDS token

```bash
# Get access token via Instance Metadata Service (system-assigned)
curl -s -H "Metadata: true" \
  "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])"

# User-assigned — include client_id
curl -s -H "Metadata: true" \
  "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://vault.azure.net&client_id=<client-id>" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('access_token', d))"
```


```text title="Expected output"
eyJhbGciOiJSUzI1NiIsImtpZCI6IjEyMzQ1Njc4OTBhYmNkZWYiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJodHRwczovL21hbmFnZW1lbnQuYXp1cmUuY29tLyIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzEyMzQ1Njc4LWFiY2QtMTIzNC1hYmNkLTEyMzQ1Njc4YWJjZC8iLCJpYXQiOjE2OTk2MzQ4MjAsImV4cCI6MTY5OTYzODQyMCwibmFtZWlkIjoiMTIzNDU2Nzg5MDEyMzQ1Njc4OTAxMjM0NTY3ODkwIiwib2lkIjoiYWJjZGVmMDEtMjM0NS02Nzg5LWFiY2QtZWYwMTIzNDU2Nzg5IiwiYXV0aF90aW1lIjoxNjk5NjM0ODIwLCJzdWIiOiJhYmNkZWYwMS0yMzQ1LTY3ODktYWJjZC1lZjAxMjM0NTY3ODkifQ.SigNature_Base64EncodedHere_1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ

eyJhbGciOiJSUzI1NiIsImtpZCI6IjljZGU4ZjEyMzQ1NjdhYmMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJodHRwczovL3ZhdWx0LmF6dXJlLm5ldCIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzEyMzQ1Njc4LWFiY2QtMTIzNC1hYmNkLTEyMzQ1Njc4YWJjZC8iLCJpYXQiOjE2OTk2MzQ4MjUsImV4cCI6MTY5OTYzODQyNSwibmFtZWlkIjoiMTIzNDU2Nzg5MDEyMzQ1Njc4OTAxMjM0NTY3ODkwIiwib2lkIjoiZWYwMTIzNDUtNjc4OS1hYmNkLWVmMDEt
```
## AKS Workload Identity

For Kubernetes workloads, use Workload Identity (federated credential) instead of pod-level managed identity.

```bash
# Enable OIDC issuer and workload identity on AKS
az aks update \
  --name <cluster> \
  --resource-group <rg> \
  --enable-oidc-issuer \
  --enable-workload-identity

# Get OIDC issuer URL
OIDC_ISSUER=$(az aks show --name <cluster> --resource-group <rg> \
  --query "oidcIssuerProfile.issuerUrl" --output tsv)

# Create federated credential
az identity federated-credential create \
  --name "aks-workload-credential" \
  --identity-name "my-workload-identity" \
  --resource-group <rg> \
  --issuer "$OIDC_ISSUER" \
  --subject "system:serviceaccount:<namespace>:<service-account-name>" \
  --audience "api://AzureADTokenExchange"
```


```text title="Expected output"
Running update on AKS cluster 'prod-cluster' in resource group 'prod-rg'...
{
  "oidcIssuerProfile": {
    "enabled": true,
    "issuerUrl": "https://eastus.oic.prod-cluster.azmk8s.io/00000000-0000-0000-0000-000000000000/"
  },
  "workloadIdentityProfile": {
    "enabled": true
  }
}
Federated credential 'aks-workload-credential' created successfully.
{
  "audiences": [
    "api://AzureADTokenExchange"
  ],
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourcegroups/prod-rg/providers/microsoft.managedidentity/userassignedidentities/my-workload-identity/federatedidentitycredentials/aks-workload-credential",
  "issuer": "https://eastus.oic.prod-cluster.azmk8s.io/00000000-0000-0000-0000-000000000000/",
  "name": "aks-workload-credential",
  "resourceGroup": "prod-rg",
  "subject": "system:serviceaccount:default:my-service-account"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `(ResourceNotFound) The Resource 'Microsoft.ContainerService/managedClusters/<cluster>' under resource group '<rg>' was not found.` | Verify the cluster name and resource group name are correct and the cluster exists in your subscription. |
    | `(InvalidInput) The identity '<identity-name>' does not exist in resource group '<rg>'.` | Create the user-assigned managed identity first using `az identity create --name <identity-name> --resource-group <rg>`. |
    | `(InvalidInput) The subject 'system:serviceaccount:<namespace>:<service-account-name>' is invalid.` | Ensure the namespace and service account name match exactly what exists in your AKS cluster; verify with `kubectl get serviceaccount -n <namespace>`. |
## Common Issues

| Symptom | Cause | Resolution |
|---|---|---|
| `ManagedIdentityCredential authentication failed` | Identity not assigned or IMDS not reachable | Confirm: `az vm identity show --name <vm>`; verify IMDS reachable from VM |
| 403 when accessing resource | Role not assigned to the managed identity's principal ID | `az role assignment list --assignee <principal-id> --all` |
| User-assigned identity missing after VM creation | Identity must be assigned at or before VM creation — some SDKs need restart | Restart the application or request a fresh token |
| AKS pod cannot authenticate | OIDC issuer URL mismatch or subject format incorrect | Verify: subject = `system:serviceaccount:<ns>:<sa>` |
