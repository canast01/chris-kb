---
tags:
  - azure
  - security
description: "Key Vault keys are cryptographic keys used for encryption, signing, and wrapping operations. Unlike secrets, keys are never exported as plaintext — all..."
---
# Azure — Key Vault Keys

<div class="kb-summary">
Key Vault keys are cryptographic keys used for encryption, signing, and wrapping operations. Unlike secrets, keys are never exported as plaintext — all cryptographic operations happen within Key Vault (or the HSM).

*Applies to: Azure*
</div>

```d2
direction: down

key_types: "Key Types" {shape: rectangle}
key_operations: "Key Operations" {shape: rectangle}
creating_keys: "Creating Keys" {shape: rectangle}
key_rotation: "Key Rotation" {shape: rectangle}
key_versions: "Key Versions" {shape: rectangle}
byok_bring_your_own_key: "BYOK — Bring Your Own Key" {shape: rectangle}

key_types -> key_operations: uses
key_operations -> creating_keys: uses
creating_keys -> key_rotation: uses
key_rotation -> key_versions: uses
key_versions -> byok_bring_your_own_key: uses
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Key Types

| Type | Algorithm family | Key sizes | Supports HSM backing |
|---|---|---|---|
| **RSA** | RSA | 2048, 3072, 4096 | Yes (Premium/Managed HSM) |
| **EC** | Elliptic Curve | P-256, P-256K, P-384, P-521 | Yes |
| **oct** (symmetric) | AES | 128, 192, 256 | Managed HSM only |

## Key Operations

| Operation | Description |
|---|---|
| `encrypt` / `decrypt` | Encrypt/decrypt data directly with the key |
| `wrapKey` / `unwrapKey` | Wrap/unwrap another key (envelope encryption) |
| `sign` / `verify` | Generate/verify digital signatures |
| `import` | Import external key material |
| `backup` / `restore` | Export encrypted key backup (vault-to-vault within same geography) |

## Creating Keys

```bash
# Create RSA key (software-backed)
az keyvault key create \
  --vault-name <vault-name> \
  --name "my-rsa-key" \
  --kty RSA \
  --size 4096

# Create EC key
az keyvault key create \
  --vault-name <vault-name> \
  --name "my-ec-key" \
  --kty EC \
  --curve P-256

# Create HSM-backed RSA key (Premium vault required)
az keyvault key create \
  --vault-name <vault-name> \
  --name "my-hsm-key" \
  --kty RSA-HSM \
  --size 4096

# Create key with expiry and rotation policy
az keyvault key create \
  --vault-name <vault-name> \
  --name "cmk-storage" \
  --kty RSA \
  --size 4096 \
  --expires "2027-01-01T00:00:00Z"
```


```text title="Expected output"
{
  "attributes": {
    "created": 1704067200,
    "enabled": true,
    "expires": null,
    "notBefore": null,
    "recoveryLevel": "Recoverable+Purgeable",
    "updated": 1704067200
  },
  "key": {
    "crv": null,
    "d": null,
    "dp": null,
    "dq": null,
    "e": "AQAB",
    "k": null,
    "keyOps": [
      "sign",
      "verify",
      "wrapKey",
      "unwrapKey",
      "encrypt",
      "decrypt"
    ],
    "kid": "https://myvault.vault.azure.net/keys/my-rsa-key/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    "kty": "RSA",
    "n": "0vx7agoebGcQSuuPiLJXZptN9nndrQmbXEps2aiAFbWhM78LhWx4cbbfAAtVT86zwu1RK7aPFFxuhDR1L6tSoc_BJECPebWKRXjBZCiFV4n3oknjhMstn64tZ_2W-5JsGY4Hc5n9yBXArwl93lqt7_RN5w6Cf0h4QyQ5v-65YGjQR0_FDW2QvzqY368QQMicAtaSqzs8KJZgnYb9c7d0zgdAZHzu6qMQvRL5hajrn1n91CbOpbISD08qNLyrdkt-bFTWhAI4vMQFh6WeZu0fM4lFd2NcRwr3XPksINHaQ-G_xBniIqbw0Ls1jF44-csFCur-kEgU8awapJzKnqDKgw",
    "p": null,
    "q": null,
    "qi": null,
    "t": null,
    "x": null,
    "y": null
  },
  "name": "my-rsa-key",
  "tags": null,
  "vault_name": "myvault"
}
{
  "attributes": {
    "created": 1704067215,
    "enabled": true,
    "expires": null,
    "notBefore": null,
    "recoveryLevel": "Recoverable+Purgeable",
    "updated": 1704067215
  },
  "key": {
    "crv": "P-256",
    "kty": "EC",
    "kid": "https://myvault.vault.azure.net/keys/my-ec-key/b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7",
    "keyOps": [
      "sign",
      "verify"
    ],
    "x
```
## Key Rotation

```bash
# Manually rotate a key (creates new version; old version retained)
az keyvault key rotate --vault-name <vault-name> --name "my-rsa-key"

# Set automatic rotation policy (rotate every 12 months)
az keyvault key rotation-policy update \
  --vault-name <vault-name> \
  --name "my-rsa-key" \
  --value '{
    "lifetimeActions": [
      {
        "trigger": {"timeAfterCreate": "P12M"},
        "action": {"type": "Rotate"}
      },
      {
        "trigger": {"timeBeforeExpiry": "P30D"},
        "action": {"type": "Notify"}
      }
    ],
    "attributes": {
      "expiryTime": "P18M"
    }
  }'

# Get current rotation policy
az keyvault key rotation-policy show --vault-name <vault-name> --name "my-rsa-key"
```


```text title="Expected output"
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.KeyVault/vaults/my-vault/keys/my-rsa-key",
  "attributes": {
    "created": 1704067200,
    "updated": 1704153600,
    "recoveryLevel": "Recoverable+Purgeable"
  },
  "key": {
    "kty": "RSA",
    "kid": "https://my-vault.vault.azure.net/keys/my-rsa-key/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
    "key_ops": ["sign", "verify", "wrapKey", "unwrapKey"],
    "n": "0vx7agoebGcQSuuPiLJXZptN9nndrQmbXEps2aiAFbWhM78LhWx4cbbfAAtVT86zwu1RK7aPFFxuhDR1L6tSoc_BJECPebWKRXjBZCiFV4n3oknjhMstn64tZ_2W-5JsGY4Hc5n9yBXArwl93lqt7_RN5w6Cf0h4QyQ5v-65YGjQR0_FDW2QvzqY368QQMicAtaSqzs8KJZgnYb9c7d0zgdAZHzu6qMQvRL5hajrn1n91CbOpbISD08qNLyrdkt-bFTWhAI4vMQFh6WeZu0fM4lFd2NcRwr3XPksINHaQ-G_xBniIqbw0Ls1jF44-csFCur-kEgU8awapJzKnqDKgw",
    "e": "AQAB"
  }
}

Rotation policy updated successfully.

{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.KeyVault/vaults/my-vault/keys/my-rsa-key/rotationpolicy/default",
  "lifetimeActions": [
    {
      "trigger": {
        "timeAfterCreate": "P12M"
      },
      "action": {
        "type": "Rotate"
      }
    },
    {
      "trigger": {
        "timeBeforeExpiry": "P30D"
      },
      "action": {
        "type": "Notify"
      }
    }
  ],
  "attributes": {
    "expiryTime": "P18M"
  }
}
```

!!! warning "Common errors"
    **`The user, group or application 'appid=<id>;oid=<oid>;iss=https://sts.windows.net/<tenant>/' does not have permissions to perform action 'Microsoft.KeyVault/vaults/keys/rotate/action' on resource '/
## Key Versions

Each rotation or import creates a new key version. Azure services using a CMK can be configured to auto-update to the latest version or pin to a specific version.

```bash
# List all versions of a key
az keyvault key list-versions --vault-name <vault-name> --name "my-rsa-key" --output table

# Get a specific version
az keyvault key show \
  --vault-name <vault-name> \
  --name "my-rsa-key" \
  --version <version-id>

# Disable an old key version
az keyvault key set-attributes \
  --vault-name <vault-name> \
  --name "my-rsa-key" \
  --version <old-version-id> \
  --enabled false
```


```text title="Expected output"
Name       Version                              Enabled    Expires    Updated
---------  ------------------------------------  ---------  ---------  -----------------------
my-rsa-key 7f8c9a2b1e4d5f6a3c8b9e0d1f2a3b4c5  True       2026-12-31 2024-01-15 10:23:45
my-rsa-key 6e7b8a9c0d3e4f5a2b9c8d1e0f3a4b5c6  True       2025-06-30 2023-11-20 14:47:22
my-rsa-key 5d6a7b8c9e0f1a2b3c4d5e6f7a8b9c0d  False      2024-03-15 2023-08-10 09:12:11

Key ID: https://myvault.vault.azure.net/keys/my-rsa-key/7f8c9a2b1e4d5f6a3c8b9e0d1f2a3b4c5
Key Type: RSA
Key Size: 2048
Enabled: true
Expires: 2026-12-31T00:00:00+00:00
Created: 2024-01-15T10:23:45+00:00
Updated: 2024-01-15T10:23:45+00:00

(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The specified vault <vault-name> does not exist or you do not have permission to access it.` | Verify the vault name is correct and you have `Microsoft.KeyVault/vaults/read` permissions on the Key Vault resource. |
    | `The specified key version <version-id> does not exist.` | Run `az keyvault key list-versions` to confirm the version ID exists before referencing it. |
## BYOK — Bring Your Own Key

Import externally generated key material into Key Vault (HSM-backed vaults only for HSM-protected keys).

```bash
# Download KEK (Key Exchange Key) from the vault
az keyvault key download \
  --vault-name <vault-name> \
  --name "byok-kek" \
  --file kek.pem

# Generate key on-premises with your HSM, wrap with KEK, export as .byok file
# (process is HSM-vendor specific — refer to vendor BYOK guide)

# Import the wrapped key
az keyvault key import \
  --vault-name <vault-name> \
  --name "imported-key" \
  --byok-file wrapped-key.byok \
  --kty RSA-HSM
```


```text title="Expected output"
Downloading key from vault: byok-kek
Key downloaded successfully to kek.pem
Key size: 2048 bits
Key type: RSA
Vault URI: https://prod-vault-001.vault.azure.net/
Key version: 7f3a9c2d1e5b4a8f9c2d1e5b4a8f9c2d

Importing wrapped key to vault: prod-vault-001
Key imported successfully
Key name: imported-key
Key type: RSA-HSM
Key ID: https://prod-vault-001.vault.azure.net/keys/imported-key/7f3a9c2d1e5b4a8f9c2d1e5b4a8f9c2d
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceNotFound: The key 'byok-kek' does not exist in vault 'prod-vault-001'.` | Verify the KEK key name matches exactly and exists in the specified vault using `az keyvault key list --vault-name <vault-name>`. |
    | `InvalidKeyFormat: The BYOK file format is invalid or corrupted.` | Ensure the wrapped-key.byok file was generated correctly by your HSM vendor's BYOK tool and has not been modified or truncated during transfer. |
    | `Forbidden: The user does not have permission to import keys.` | Grant the user the "Key Vault Crypto Officer" or "Key Vault Administrator" role on the vault using `az role assignment create`. |
## Using Keys for Crypto Operations

```bash
# Encrypt a value (base64 plaintext input)
az keyvault key encrypt \
  --vault-name <vault-name> \
  --name "my-rsa-key" \
  --algorithm RSA-OAEP \
  --value "$(echo -n 'secret data' | base64)"

# Decrypt (base64 ciphertext input)
az keyvault key decrypt \
  --vault-name <vault-name> \
  --name "my-rsa-key" \
  --algorithm RSA-OAEP \
  --value "<base64-ciphertext>"

# Sign a digest
az keyvault key sign \
  --vault-name <vault-name> \
  --name "my-rsa-key" \
  --algorithm RS256 \
  --digest "$(echo -n 'data to sign' | sha256sum | awk '{print $1}')"
```


```text title="Expected output"
{
  "kid": "https://myvault.vault.azure.net/keys/my-rsa-key/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "result": "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2x8vK9pL4mN3qR5sT8vW..."
}
{
  "kid": "https://myvault.vault.azure.net/keys/my-rsa-key/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "result": "c2VjcmV0IGRhdGE="
}
{
  "kid": "https://myvault.vault.azure.net/keys/my-rsa-key/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "result": "SIGNEDDATAx9vK9pL4mN3qR5sT8vWaB2cD4eF6gH8iJ0kL2mN4oP6qR8sT0uV2wX4yZ6aB8cD0eF2gH4iJ6kL8mN0oP2qR4sT6uV8wX0yZ2aB4cD2eF4gH6iJ8kL0mN2oP4qR6sT8uV0wX2yZ4aB6cD4eF6gH8iJ0kL2mN4oP6qR8sT0uV2wX4yZ6aB8cD0eF2gH4iJ6kL8mN0oP2qR4sT6uV8wX0yZ2aB4cD2eF4gH6iJ8kL0mN2oP4qR6sT8uV0wX2yZ4aB6cD4eF6gH8iJ0kL2mN4oP6qR8sT0uV2wX4yZ6aB8cD0eF2gH4iJ6kL8mN0oP2qR4sT6uV8wX0yZ2aB4cD2eF4gH6iJ8kL0mN2oP4qR6sT8uV0wX2yZ4aB6cD4eF6gH8iJ0kL2mN4oP6qR8sT0uV2wX4yZ6aB8cD0eF2gH4iJ6kL8mN0oP2qR4sT6uV8wX0yZ2aB4cD2eF4gH6iJ8kL0mN2oP4qR6sT8uV0wX2yZ4aB6cD4eF6gH8iJ0kL2mN
```
## Customer-Managed Keys (CMK)

Azure services (Storage, SQL, Disk Encryption) can use a Key Vault key as a CMK instead of Microsoft-managed keys.

```bash
# Example: Enable CMK for a storage account
az storage account update \
  --name <storage-account> \
  --resource-group <rg> \
  --encryption-key-source Microsoft.Keyvault \
  --encryption-key-vault https://<vault-name>.vault.azure.net \
  --encryption-key-name "cmk-storage" \
  --encryption-key-version ""   # empty = always use latest version
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4789-0abc-def123456789/resourceGroups/prod-rg/providers/Microsoft.Storage/storageAccounts/prodstg2024",
  "name": "prodstg2024",
  "type": "Microsoft.Storage/storageAccounts",
  "location": "eastus",
  "sku": {
    "name": "Standard_GRS",
    "tier": "Standard"
  },
  "kind": "StorageV2",
  "encryption": {
    "services": {
      "blob": {
        "enabled": true,
        "lastEnabledTime": "2024-01-15T09:42:33.521234Z"
      },
      "file": {
        "enabled": true,
        "lastEnabledTime": "2024-01-15T09:42:33.521234Z"
      }
    },
    "keySource": "Microsoft.Keyvault",
    "keyVaultProperties": {
      "keyVaultUri": "https://prod-vault.vault.azure.net/",
      "keyName": "cmk-storage",
      "keyVersion": ""
    }
  },
  "provisioningState": "Succeeded"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `KeyVault key 'cmk-storage' not found in vault 'prod-vault'` | Verify the key exists in the Key Vault using `az keyvault key list --vault-name <vault-name>` and confirm the name matches exactly. |
    | `The user, group or application does not have the 'get', 'wrapKey', 'unwrapKey' permission(s) on the key` | Grant the storage account's managed identity Key Vault permissions using `az keyvault set-policy --name <vault-name> --object-id <storage-mi-object-id> --key-permissions get wrapKey unwrapKey`. |
    | `Storage account '<storage-account>' not found in resource group '<rg>'` | Confirm the storage account name and resource group are correct with `az storage account list --resource-group <rg>`. |
## Common Issues

| Symptom | Cause | Resolution |
|---|---|---|
| `Forbidden` on key operation | Missing Crypto User role or wrong operation type | Assign `Key Vault Crypto User`; verify allowed operations on the key |
| CMK service can't access key | Service identity lacks Key Vault Crypto Service Encryption User role | Assign role to the service's managed identity |
| Key rotation breaks CMK service | Service pinned to old key version and auto-update disabled | Configure CMK to use latest version (empty version ID) |
| Cannot delete key | Soft-delete and purge protection prevent immediate deletion | Wait out soft-delete retention; disable old key version instead |
| HSM-backed key creation fails | Vault SKU is Standard (not Premium) | Upgrade vault to Premium or use Managed HSM |
