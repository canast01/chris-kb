---
tags:
  - azure
  - security
---
# Azure — Certificates

<div class="kb-summary">
Azure Key Vault manages X.509 certificates, providing lifecycle management including creation, import, auto-renewal, and expiry alerting. Key Vault integrates with App Gateway, API Management, App Service, and other services for SSL/TLS offloading.

*Applies to: Azure*
</div>

```d2
direction: down

creating_a_key_vault_certificate: "Creating a Key Vault Certificate" {shape: rectangle}
importing_certificates: "Importing Certificates" {shape: rectangle}
certificate_versions_and_rotation: "Certificate Versions and Rotation" {shape: rectangle}
autorotation_with_lifetime_actions: "Auto-Rotation with Lifetime Actions" {shape: rectangle}
app_gateway_integration: "App Gateway Integration" {shape: rectangle}
certificate_expiry_monitoring: "Certificate Expiry Monitoring" {shape: rectangle}

creating_a_key_vault_certificate -> importing_certificates: uses
importing_certificates -> certificate_versions_and_rotation: uses
certificate_versions_and_rotation -> autorotation_with_lifetime_actions: uses
autorotation_with_lifetime_actions -> app_gateway_integration: uses
app_gateway_integration -> certificate_expiry_monitoring: uses
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Creating a Key Vault Certificate

```bash
# Generate a self-signed certificate in Key Vault
az keyvault certificate create \
  --vault-name myKeyVault \
  --name myCert \
  --policy "$(az keyvault certificate get-default-policy)"

# Create with a custom policy (CA-issued, auto-renewal)
cat > cert-policy.json <<'EOF'
{
  "issuerParameters": {"name": "DigiCert"},
  "keyProperties": {"exportable": true, "keySize": 2048, "keyType": "RSA"},
  "lifetimeActions": [{"action": {"actionType": "AutoRenew"}, "trigger": {"daysBeforeExpiry": 30}}],
  "secretProperties": {"contentType": "application/x-pkcs12"},
  "x509CertificateProperties": {
    "subject": "CN=example.com",
    "subjectAlternativeNames": {"dnsNames": ["example.com", "www.example.com"]},
    "validityInMonths": 12
  }
}
EOF

az keyvault certificate create \
  --vault-name myKeyVault \
  --name my-ca-cert \
  --policy @cert-policy.json
```


```text title="Expected output"
{
  "attributes": {
    "created": 1704067200,
    "enabled": true,
    "expires": 1735689600,
    "updated": 1704067200
  },
  "id": "https://mykeyvault.vault.azure.net/certificates/myCert/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "name": "myCert",
  "policy": {
    "issuerParameters": {"name": "Self"},
    "keyProperties": {"keySize": 2048, "keyType": "RSA"},
    "secretProperties": {"contentType": "application/x-pkcs12"},
    "x509CertificateProperties": {"validityInMonths": 12}
  }
}
{
  "attributes": {
    "created": 1704067215,
    "enabled": true,
    "expires": 1735689615,
    "updated": 1704067215
  },
  "id": "https://mykeyvault.vault.azure.net/certificates/my-ca-cert/b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7",
  "name": "my-ca-cert",
  "policy": {
    "issuerParameters": {"name": "DigiCert"},
    "keyProperties": {"exportable": true, "keySize": 2048, "keyType": "RSA"},
    "lifetimeActions": [{"action": {"actionType": "AutoRenew"}, "trigger": {"daysBeforeExpiry": 30}}],
    "secretProperties": {"contentType": "application/x-pkcs12"},
    "x509CertificateProperties": {
      "subject": "CN=example.com",
      "subjectAlternativeNames": {"dnsNames": ["example.com", "www.example.com"]},
      "validityInMonths": 12
    }
  }
}
```

!!! warning "Common errors"
    **`ResourceNotFound: The resource 'myKeyVault' does not exist in the subscription`** — Verify the Key Vault name exists in your subscription with `az keyvault list` and use the correct vault name.
    **`InvalidJsonFile: Invalid JSON in cert-policy.json at line X`** — Validate the JSON syntax using `jq . cert-policy.json` before running the certificate create command.
    **`Forbidden: The user does not have permission to create certificates in this Key Vault`** — Ensure your Azure account has the "Certificate Officer" or equivalent RBAC role assigned on the Key Vault resource.
## Importing Certificates

```bash
# Import a PFX certificate
az keyvault certificate import \
  --vault-name myKeyVault \
  --name imported-cert \
  --file mycert.pfx \
  --password "PfxP@ssword"

# Import a PEM certificate
az keyvault certificate import \
  --vault-name myKeyVault \
  --name imported-pem-cert \
  --file mycert.pem

# List certificates in a vault
az keyvault certificate list \
  --vault-name myKeyVault \
  --output table

# Show certificate details including expiry
az keyvault certificate show \
  --vault-name myKeyVault \
  --name myCert \
  --output json
```


```text title="Expected output"
{
  "attributes": {
    "created": 1704067200,
    "enabled": true,
    "expires": 1735689600,
    "updated": 1704067200
  },
  "id": "https://mykeyvault.vault.azure.net/certificates/imported-cert/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "name": "imported-cert",
  "properties": {
    "contentType": "application/x-pkcs12"
  }
}
{
  "attributes": {
    "created": 1704067201,
    "enabled": true,
    "expires": 1735689601,
    "updated": 1704067201
  },
  "id": "https://mykeyvault.vault.azure.net/certificates/imported-pem-cert/b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7",
  "name": "imported-pem-cert",
  "properties": {
    "contentType": "application/x-pem-file"
  }
}
Name                  Enabled    Expires             Created             Updated
--------------------  ---------  ------------------  ------------------  ------------------
imported-cert         True       2025-01-02 12:00:00 2024-01-01 12:00:00 2024-01-01 12:00:00
imported-pem-cert     True       2025-01-02 12:00:01 2024-01-01 12:00:01 2024-01-01 12:00:01
myCert                True       2025-06-15 08:30:00 2023-06-15 08:30:00 2024-01-01 10:15:00
...
{
  "attributes": {
    "created": 1686830400,
    "enabled": true,
    "expires": 1750291200,
    "updated": 1704067200
  },
  "id": "https://mykeyvault.vault.azure.net/certificates/myCert/c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8",
  "name": "myCert",
  "properties": {
    "contentType": "application/x-pkcs12",
    "subject": "CN=example.com,O=Contoso,C=US",
    "subjectAlternativeNames": ["www.example.com", "api.example.com"]
  }
}
```

!!! warning "Common errors"
    **`KeyVaultErrorException: (BadParameter) The certificate file is invalid or corrupted.`** — Verify the PFX/PEM file is valid and not corrupted by testing it locally with `openssl x509 -in mycert.pem -text -noout`.
    **`ResourceNotFound: The vault 'myKeyVault' does not exist or you do not have permission to access it.`** — Ensure the Key Vault name is correct and your Azure account has the `Microsoft.KeyVault/vaults/certificates/create` permission on that vault.
    **`BadParameter: The password
## Certificate Versions and Rotation

Each update to a certificate creates a new version. The current version is the default unless a specific version is referenced.

```bash
# List all versions of a certificate
az keyvault certificate list-versions \
  --vault-name myKeyVault \
  --name myCert \
  --output table

# Download the certificate as a PEM file
az keyvault certificate download \
  --vault-name myKeyVault \
  --name myCert \
  --file downloaded-cert.pem \
  --encoding PEM

# Get the secret (includes private key) as base64 PFX
az keyvault secret download \
  --vault-name myKeyVault \
  --name myCert \
  --file cert-with-key.pfx \
  --encoding base64
```


```text title="Expected output"
Name    Version                          Created                Updated                Enabled
------  --------------------------------  ---------------------  ---------------------  ---------
myCert  a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5  2024-01-15T10:32:45Z  2024-01-15T10:32:45Z  True
myCert  9z8y7x6w5v4u3t2s1r0q9p8o7n6m5l  2023-12-20T14:18:22Z  2023-12-20T14:18:22Z  True
myCert  5k4j3i2h1g0f9e8d7c6b5a4z3y2x1w  2023-11-05T09:47:11Z  2023-11-05T09:47:11Z  True

(no output — command completes silently)

(no output — command completes silently)
```

!!! warning "Common errors"
    **`The specified vault myKeyVault does not exist or you do not have permission to access it.`** — Verify the vault name is correct and your Azure credentials have Keyvault access permissions via `az account show`.
    **`Certificate myCert not found in vault myKeyVault.`** — Confirm the certificate name exists by running `az keyvault certificate list --vault-name myKeyVault` to list all available certificates.
    **`The file 'downloaded-cert.pem' cannot be created because the directory does not exist.`** — Create the target directory first with `mkdir -p <directory>` or specify a valid existing path for the output file.
## Auto-Rotation with Lifetime Actions

| Action Type     | Trigger                  | Effect                                   |
|-----------------|--------------------------|------------------------------------------|
| AutoRenew       | daysBeforeExpiry / pct   | Requests a new certificate automatically |
| EmailContacts   | daysBeforeExpiry / pct   | Sends email to vault contacts            |

```bash
# Update lifetime actions on an existing certificate policy
az keyvault certificate get-default-policy | \
  jq '.lifetimeActions = [{"action":{"actionType":"AutoRenew"},"trigger":{"daysBeforeExpiry":45}}]' > updated-policy.json

az keyvault certificate set-attributes \
  --vault-name myKeyVault \
  --name myCert \
  --policy @updated-policy.json
```


```text title="Expected output"
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myResourceGroup/providers/Microsoft.KeyVault/vaults/myKeyVault/certificates/myCert/versions/abcd1234efgh5678ijkl9012mnop3456",
  "attributes": {
    "enabled": true,
    "created": 1698765432,
    "updated": 1698765433,
    "recoveryLevel": "Recoverable+Purgeable"
  },
  "policy": {
    "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myResourceGroup/providers/Microsoft.KeyVault/vaults/myKeyVault/certificates/myCert/policy",
    "key_props": {
      "exportable": true,
      "kty": "RSA",
      "key_size": 2048
    },
    "lifetime_actions": [
      {
        "action": {
          "action_type": "AutoRenew"
        },
        "trigger": {
          "days_before_expiry": 45
        }
      }
    ],
    "issuer": {
      "name": "Self"
    },
    "attributes": {
      "enabled": true
    }
  }
}
```

!!! warning "Common errors"
    **`jq: command not found`** — Install jq with `apt-get install jq` (Linux) or `brew install jq` (macOS).
    **`The user, group or application 'appId=...' does not have certificates permissions to perform action 'Microsoft.KeyVault/vaults/certificates/update/action'`** — Grant the service principal certificate management permissions via `az keyvault set-policy --name myKeyVault --object-id <objectId> --certificate-permissions update`.
    **`Keyvault 'myKeyVault' not found`** — Verify the vault name is correct and exists in the current subscription with `az keyvault list`.
## App Gateway Integration

App Gateway can reference Key Vault certificates directly via a managed identity, avoiding manual certificate uploads.

```bash
# Assign managed identity to the App Gateway
az network application-gateway identity assign \
  --resource-group myRG \
  --gateway-name myAppGW \
  --identity /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/myAppGWIdentity

# Grant the identity access to Key Vault secrets (for certificate retrieval)
az keyvault set-policy \
  --name myKeyVault \
  --object-id <identity-object-id> \
  --secret-permissions get list

# Add SSL cert to App Gateway referencing KV secret URI
az network application-gateway ssl-cert create \
  --gateway-name myAppGW \
  --resource-group myRG \
  --name kv-cert \
  --key-vault-secret-id "https://myKeyVault.vault.azure.net/secrets/myCert"
```


```text title="Expected output"
{
  "identity": {
    "principalId": "a7f3c2e1-9b4d-4f8a-b2c5-d1e6f7a8b9c0",
    "tenantId": "72f988bf-86f1-41af-91ab-2d7cd011db47",
    "type": "UserAssigned",
    "userAssignedIdentities": {
      "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.ManagedIdentity/userAssignedIdentities/myAppGWIdentity": {
        "clientId": "c8d4e5f6-7a8b-9c0d-1e2f-3a4b5c6d7e8f",
        "principalId": "a7f3c2e1-9b4d-4f8a-b2c5-d1e6f7a8b9c0"
      }
    }
  }
}
Key vault secret permissions have been updated.
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myRG/providers/Microsoft.Network/applicationGateways/myAppGW/sslCertificates/kv-cert",
  "name": "kv-cert",
  "keyVaultSecretId": "https://myKeyVault.vault.azure.net/secrets/myCert",
  "provisioningState": "Succeeded",
  "type": "Microsoft.Network/applicationGateways/sslCertificates"
}
```

!!! warning "Common errors"
    **`(ResourceNotFound) The Resource 'Microsoft.ManagedIdentity/userAssignedIdentities/myAppGWIdentity' under resource group 'myRG' was not found.`** — Verify the managed identity exists in the same resource group and region, or create it with `az identity create --resource-group myRG --name myAppGWIdentity`.
    **`(InvalidKeyVaultSecretId) The key vault secret ID format is invalid or the secret does not exist.`** — Ensure the secret exists in Key Vault by running `az keyvault secret show --vault-name myKeyVault --name myCert` and verify the URI format matches exactly.
    **`(AuthorizationFailed) The client does not have permission to perform action 'Microsoft.KeyVault/vaults/secrets/get' on resource.`** — Confirm the managed identity's object ID in the set-policy command matches the principalId from the identity assign output.
## Certificate Expiry Monitoring

```bash
# Query Log Analytics for certificates expiring within 30 days
az monitor log-analytics query \
  --workspace /subscriptions/<sub-id>/resourceGroups/myRG/providers/Microsoft.OperationalInsights/workspaces/myWorkspace \
  --analytics-query "AzureDiagnostics | where ResourceType == 'VAULTS' | where OperationName == 'CertificateNearExpiry' | project TimeGenerated, requestUri_s, ResultDescription" \
  --output table

# Set up email contact for expiry alerts
az keyvault certificate set-attributes \
  --vault-name myKeyVault \
  --name myCert \
  --email-addresses ops@example.com
```


```text title="Expected output"
TimeGenerated                    RequestUri_s                                          ResultDescription
2024-01-15T09:23:47.123456Z      https://myvault.vault.azure.net/certificates/web-cert  Certificate expires in 28 days
2024-01-15T10:45:12.654321Z      https://myvault.vault.azure.net/certificates/api-cert  Certificate expires in 12 days
2024-01-15T14:18:33.987654Z      https://myvault.vault.azure.net/certificates/db-cert   Certificate expires in 5 days

Certificate attributes updated successfully.
```

!!! warning "Common errors"
    **`The workspace specified in the --workspace argument is invalid or does not exist.`** — Verify the subscription ID and resource group name match your Key Vault workspace, and confirm the workspace exists in the Azure portal.
    **`The specified certificate 'myCert' does not exist in the vault 'myKeyVault'.`** — List certificates with `az keyvault certificate list --vault-name myKeyVault` to confirm the exact certificate name.
    **`Operation failed with status: 'Unauthorized'. The user, group or application does not have the 'set' permission for certificates on this vault.`** — Grant the user or service principal the "Certificate Officer" or "Key Vault Administrator" role on the Key Vault resource.