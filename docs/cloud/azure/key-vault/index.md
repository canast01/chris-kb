# Key Vault

Azure Key Vault — secrets, keys, and certificate management.

## What Key Vault Stores

| Type | Description |
|---|---|
| Secret | Passwords, connection strings, API keys |
| Key | RSA or EC keys for encryption/signing; HSM-backed option |
| Certificate | X.509 certificates with automatic renewal via DigiCert / Let's Encrypt |

## Common Azure CLI Commands

```bash
# List key vaults
az keyvault list --query '[*].{Name:name,RG:resourceGroup,Location:location}' -o table

# List secrets in a vault
az keyvault secret list --vault-name <vault-name> \
  --query '[*].{Name:name,Enabled:attributes.enabled,Expires:attributes.expires}' -o table

# Get secret value
az keyvault secret show --vault-name <vault-name> --name <secret-name> --query value -o tsv

# Set a secret
az keyvault secret set --vault-name <vault-name> --name <secret-name> --value "<value>"

# Set secret expiry
az keyvault secret set-attributes \
  --vault-name <vault-name> \
  --name <secret-name> \
  --expires 2027-01-01T00:00:00Z

# List keys
az keyvault key list --vault-name <vault-name> -o table

# List certificates and expiry
az keyvault certificate list --vault-name <vault-name> \
  --query '[*].{Name:name,Enabled:attributes.enabled,Expires:attributes.expires}' -o table

# Download a certificate
az keyvault certificate download --vault-name <vault-name> --name <cert-name> --file cert.pem
```

## Access Policies vs RBAC

Key Vault supports two authorization models:
- **Vault access policies** (legacy): grant permissions per principal per vault
- **Azure RBAC** (recommended): use roles like `Key Vault Secrets User`, `Key Vault Administrator`

```bash
# Assign RBAC role to a service principal
az role assignment create \
  --role "Key Vault Secrets User" \
  --assignee <service-principal-object-id> \
  --scope /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.KeyVault/vaults/<vault-name>
```

## Retrieve Secrets in Code

**Python (azure-keyvault-secrets):**
```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://<vault-name>.vault.azure.net", credential=credential)
secret = client.get_secret("<secret-name>")
print(secret.value)
```

**PowerShell:**
```powershell
$secret = Get-AzKeyVaultSecret -VaultName "<vault-name>" -Name "<secret-name>" -AsPlainText
```

## Monitoring

```bash
# Enable diagnostic logging for a vault
az monitor diagnostic-settings create \
  --name kv-logs \
  --resource /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.KeyVault/vaults/<vault-name> \
  --logs '[{"category":"AuditEvent","enabled":true}]' \
  --workspace <log-analytics-workspace-id>
```

**KQL — find secret access events:**
```kql
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.KEYVAULT"
| where OperationName == "SecretGet"
| project TimeGenerated, CallerIPAddress, identity_claim_unique_name_s, resourceId
| sort by TimeGenerated desc
```

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| `Forbidden` on secret access | RBAC or access policy | Verify correct role (`Key Vault Secrets User`) is assigned |
| Secret expiry warning | `attributes.expires` | Update or rotate secret; update expiry date |
| Certificate not auto-renewing | Contact admin email / CA integration | Check renewal action config; verify CA contact in vault |
| Soft-deleted vault | `az keyvault list-deleted` | Recover with `az keyvault recover --name <vault>` |
