---
tags:
  - azure
description: "Azure Blob Storage reference covering Overview, Blob Lifecycle Management Flow, Access Tiers, Lifecycle Rules, SAS Tokens and 2 more sections."
---
# Azure Blob Storage

<div class="kb-summary">
Azure Blob Storage reference covering Overview, Blob Lifecycle Management Flow, Access Tiers, Lifecycle Rules, SAS Tokens and 2 more sections.

*Applies to: Azure*
</div>

## Overview

Azure Blob Storage is Microsoft's object store for unstructured data. Blobs are organised into containers within Storage Accounts. Three access tiers (Hot, Cool, Archive) control cost versus retrieval latency. Blob versioning, soft delete, and lifecycle management provide data protection and cost control.

## Blob Lifecycle Management Flow

```d2
direction: right

upload: "Blob Upload\nHot Tier" {shape: rectangle}
cool: "Cool Tier\nafter 30 days" {shape: rectangle}
cold: "Cold Tier\nafter 90 days" {shape: rectangle}
archive: "Archive Tier\nafter 180 days" {shape: rectangle}
rehydrate: "Rehydrate\nhours latency" {shape: rectangle}
delete: "Delete\nafter retention period" {shape: rectangle}

upload -> cool
cool -> cold
cold -> archive
archive -> rehydrate
rehydrate -> cool
archive -> delete
```

## Access Tiers

| Tier | Access Latency | Storage Cost | Access Cost | Best For |
|---|---|---|---|---|
| Hot | Milliseconds | Highest | Lowest | Frequently accessed data |
| Cool | Milliseconds | Lower | Higher | Infrequently accessed (>30 days) |
| Cold | Milliseconds | Lower still | Higher | Rarely accessed (>90 days) |
| Archive | Hours (rehydrate first) | Lowest | Highest | Long-term retention (>180 days) |

```bash
# Set the default access tier on a storage account
az storage account update \
  --resource-group rg-storage-prod \
  --name stprodblobs01 \
  --access-tier Cool

# Change access tier on a specific blob
az storage blob set-tier \
  --account-name stprodblobs01 \
  --container-name backups \
  --name "db-backup-2026-01-01.bak" \
  --tier Archive

# Rehydrate an archived blob to Hot tier
az storage blob set-tier \
  --account-name stprodblobs01 \
  --container-name backups \
  --name "db-backup-2026-01-01.bak" \
  --tier Hot \
  --rehydrate-priority High
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`ResourceNotFound: The specified resource group 'rg-storage-prod' could not be found.`** — Verify the resource group name with `az group list` and correct the `--resource-group` parameter.
    **`ResourceNotFound: The specified container 'backups' does not exist.`** — Confirm the container exists with `az storage container list --account-name stprodblobs01` and create it if needed.
    **`InvalidBlobTier: The blob 'db-backup-2026-01-01.bak' does not support the tier 'Archive'.`** — Ensure the storage account kind supports Archive tier (use `--kind BlobStorage` or `--kind StorageV2`) and the blob is not already in an incompatible state.
## Lifecycle Rules

Lifecycle management policies automate tier transitions and deletion based on blob age:

```bash
# View existing lifecycle policy
az storage account management-policy show \
  --resource-group rg-storage-prod \
  --account-name stprodblobs01

# Apply a lifecycle policy from a JSON file
az storage account management-policy create \
  --resource-group rg-storage-prod \
  --account-name stprodblobs01 \
  --policy @lifecycle-policy.json
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-storage-prod/providers/Microsoft.Storage/storageAccounts/stprodblobs01/managementPolicies/default",
  "name": "default",
  "properties": {
    "policy": {
      "rules": [
        {
          "name": "archive-old-blobs",
          "enabled": true,
          "type": "Lifecycle",
          "definition": {
            "filters": {
              "blobTypes": ["blockBlob"],
              "prefixMatch": ["logs/"]
            },
            "actions": {
              "baseBlob": {
                "tierToArchive": {
                  "daysAfterModificationGreaterThan": 90
                }
              }
            }
          }
        }
      ]
    }
  },
  "resourceGroup": "rg-storage-prod",
  "type": "Microsoft.Storage/storageAccounts/managementPolicies"
}
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/rg-storage-prod/providers/Microsoft.Storage/storageAccounts/stprodblobs01/managementPolicies/default",
  "name": "default",
  "properties": {
    "policy": {
      "rules": [...]
    }
  },
  "resourceGroup": "rg-storage-prod",
  "type": "Microsoft.Storage/storageAccounts/managementPolicies"
}
```

!!! warning "Common errors"
    **`ResourceNotFound: The Resource 'Microsoft.Storage/storageAccounts/stprodblobs01' under resource group 'rg-storage-prod' was not found.`** — Verify the storage account name and resource group name are correct with `az storage account list --resource-group rg-storage-prod`.
    **`InvalidJsonInput: Invalid JSON in file 'lifecycle-policy.json': Unexpected token at line 5 column 12.`** — Validate the JSON syntax in your policy file using `jq . < lifecycle-policy.json` or an online JSON validator.
    **`AuthorizationFailed: The client 'user@example.com' with object id 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' does not have authorization to perform action 'Microsoft.Storage/storageAccounts/managementPolicies/write' over scope '/subscriptions/...'.`** — Ensure your Azure account has Storage Account Contributor or Owner role on the storage account or resource group.
Example `lifecycle-policy.json`:

```json
{
  "rules": [
    {
      "name": "tiering-and-expiry",
      "enabled": true,
      "type": "Lifecycle",
      "definition": {
        "filters": {
          "blobTypes": ["blockBlob"],
          "prefixMatch": ["backups/"]
        },
        "actions": {
          "baseBlob": {
            "tierToCool": {"daysAfterModificationGreaterThan": 30},
            "tierToArchive": {"daysAfterModificationGreaterThan": 90},
            "delete": {"daysAfterModificationGreaterThan": 365}
          }
        }
      }
    }
  ]
}
```

## SAS Tokens

Shared Access Signatures (SAS) delegate limited access to storage resources without exposing account keys.

```bash
# Generate a SAS token for a container (read-only, 24 hours)
az storage container generate-sas \
  --account-name stprodblobs01 \
  --name uploads \
  --permissions r \
  --expiry "$(date -u -d '1 day' '+%Y-%m-%dT%H:%MZ')" \
  --output tsv

# Generate a SAS token for a single blob
az storage blob generate-sas \
  --account-name stprodblobs01 \
  --container-name reports \
  --name "monthly-report-2026-04.pdf" \
  --permissions r \
  --expiry "2026-05-14T00:00Z" \
  --output tsv

# Generate an account-level SAS (broader scope)
az storage account generate-sas \
  --account-name stprodblobs01 \
  --services b \
  --resource-types co \
  --permissions rwdlacupx \
  --expiry "2026-05-08T00:00Z" \
  --output tsv
```


```text title="Expected output"
sv=2021-06-08&ss=c&srt=c&sp=r&se=2026-04-15T14:32Z&st=2026-04-14T14:32Z&spr=https&sig=AbCdEfGhIjKlMnOpQrStUvWxYz1234567890abcdefg%3D

sv=2021-06-08&ss=b&srt=o&sp=r&se=2026-05-14T00:00Z&st=2026-04-14T00:00Z&spr=https&sig=XyZ9876543210fedcbaZyXwVuTsRqPoNmLkJiHgFeDcBa%3D

sv=2021-06-08&ss=b&srt=co&sp=rwdlacupx&se=2026-05-08T00:00Z&st=2026-04-14T00:00Z&spr=https&sig=1a2b3c4d5e6f7g8h9i0jKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYz%3D
```

!!! warning "Common errors"
    **`ERROR: (AuthorizationPermissionMismatch) This request is not authorized to perform this operation using this permission.`** — Ensure your Azure CLI session has Storage Blob Data Contributor or higher role on the storage account.
    **`ERROR: (InvalidResourceName) The specified resource name contains invalid characters.`** — Remove special characters from the blob name or URL-encode it properly; use only alphanumeric characters, hyphens, and underscores.
    **`ERROR: (InvalidInput) Argument --expiry: invalid datetime value`** — Use UTC datetime format `YYYY-MM-DDTHH:MMZ` and ensure the date is in the future.
## Blob Versioning

```bash
# Enable versioning on a storage account
az storage account blob-service-properties update \
  --account-name stprodblobs01 \
  --resource-group rg-storage-prod \
  --enable-versioning true

# List versions of a specific blob
az storage blob list \
  --account-name stprodblobs01 \
  --container-name documents \
  --include v \
  --query "[?name=='report.docx']" \
  --output table

# Restore a previous version
az storage blob copy start \
  --account-name stprodblobs01 \
  --destination-container documents \
  --destination-blob "report.docx" \
  --source-uri "https://stprodblobs01.blob.core.windows.net/documents/report.docx?versionId=<version-id>"
```


```text title="Expected output"
(no output — command completes silently)

Name          Snapshot    Version ID                       Last Modified
------------  ----------  --------------------------------  -------------------------
report.docx               2024-01-15T09:32:47.000000+00:00  2024-01-15T09:32:47Z
report.docx               2024-01-14T16:18:22.000000+00:00  2024-01-14T16:18:22Z
report.docx               2024-01-12T11:05:13.000000+00:00  2024-01-12T11:05:13Z

Operation ID: 550e8400-e29b-41d4-a716-446655440000
Status: Pending
```

!!! warning "Common errors"
    **`ResourceNotFound: The specified blob does not exist.`** — Verify the blob name matches exactly and the container exists using `az storage container list --account-name stprodblobs01`.
    **`AuthorizationPermissionMismatch: This request is not authorized to perform this operation.`** — Ensure your Azure CLI account has Storage Blob Data Contributor role on the storage account using `az role assignment list --assignee <your-principal-id>`.
    **`InvalidUri: The URI is invalid.`** — Replace `<version-id>` with an actual version ID from the list output and ensure the URI is properly URL-encoded.
## Soft Delete and Recovery

```bash
# Enable soft delete for blobs (retain for 14 days)
az storage account blob-service-properties update \
  --account-name stprodblobs01 \
  --resource-group rg-storage-prod \
  --enable-delete-retention true \
  --delete-retention-days 14

# List soft-deleted blobs
az storage blob list \
  --account-name stprodblobs01 \
  --container-name documents \
  --include d \
  --query "[?deleted==\`true\`]" \
  --output table

# Undelete a soft-deleted blob
az storage blob undelete \
  --account-name stprodblobs01 \
  --container-name documents \
  --name "deleted-file.txt"
```


```text title="Expected output"
(no output — command completes silently)

Name                          Deleted    Snapshot    Content Length    Last Modified
------------------------------  ---------  ----------  ----------------  -------------------------
deleted-file.txt              true                    2048              2024-01-15T09:32:14+00:00
archive-2023-q4.pdf           true                    5242880           2024-01-14T16:45:22+00:00
temp-report.xlsx              true                    1536              2024-01-13T11:20:08+00:00

Blob 'deleted-file.txt' has been successfully undeleted.
```

!!! warning "Common errors"
    **`ResourceNotFound: The specified blob does not exist.`** — Verify the blob name matches exactly and check that soft delete is enabled on the storage account.
    **`AuthorizationPermissionMismatch: This request is not authorized to perform this operation.`** — Ensure your Azure CLI credentials have the Storage Blob Data Contributor role on the storage account.
    **`InvalidQueryFilter: The query filter is invalid.`** — Remove backticks around `true` in the query and use proper JSON syntax: `--query "[?deleted==true]"`.