# Azure — Managed Identities

Managed identities give Azure resources an identity in Entra ID without requiring credentials in code or config.

```
┌──────────────────────────────────────────────────────────────┐
│               Managed Identity Flow                          │
│                                                              │
│  ┌──────────────────┐   system-assigned  ┌────────────────┐  │
│  │  Azure VM /      │───────────────────►│  Entra ID      │  │
│  │  App Service /   │   user-assigned    │  (identity     │  │
│  │  AKS Pod         │◄───────────────────│   registered)  │  │
│  └────────┬─────────┘                   └────────────────┘   │
│           │                                                  │
│           │ code calls IMDS endpoint                         │
│           ▼  (169.254.169.254)                               │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  MSI Token Endpoint  ──►  access token (OAuth2)      │    │
│  └──────────────────────────┬─────────────────────────┘      │
│                             │ token attached to request      │
│                             ▼                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  Target Resource  (Key Vault / Storage / SQL / ...)  │    │
│  │  RBAC validates: principal has required role ✓       │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
``` Azure manages credential rotation and renewal automatically.

## Identity Types

| Type | Lifecycle | Shared across resources | Use case |
|---|---|---|---|
| **System-assigned** | Tied to the resource; deleted with it | No — 1:1 with the resource | Single-resource workloads; simplest to set up |
| **User-assigned** | Independent; exists until explicitly deleted | Yes — assign to many resources | Shared identity across multiple resources; pre-provision before resource creation |

## Enable on a Resource

### System-Assigned

```bash
# Enable on a VM
az vm identity assign --name <vm-name> --resource-group <rg>

# Enable on App Service
az webapp identity assign --name <app-name> --resource-group <rg>

# Get the principal ID (object ID) — used for RBAC assignments
az vm identity show --name <vm-name> --resource-group <rg> \
  --query principalId --output tsv
```

### User-Assigned

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

## Common Issues

| Symptom | Cause | Resolution |
|---|---|---|
| `ManagedIdentityCredential authentication failed` | Identity not assigned or IMDS not reachable | Confirm: `az vm identity show --name <vm>`; verify IMDS reachable from VM |
| 403 when accessing resource | Role not assigned to the managed identity's principal ID | `az role assignment list --assignee <principal-id> --all` |
| User-assigned identity missing after VM creation | Identity must be assigned at or before VM creation — some SDKs need restart | Restart the application or request a fresh token |
| AKS pod cannot authenticate | OIDC issuer URL mismatch or subject format incorrect | Verify: subject = `system:serviceaccount:<ns>:<sa>` |
