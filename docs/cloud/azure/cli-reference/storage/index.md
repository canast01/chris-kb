# Storage Accounts & Blobs


<div class="kb-summary">
Storage Accounts & Blobs reference.
</div>

> Part of the Azure CLI Reference.

---

```bash
# Storage accounts
az storage account list --output table
az storage account show --resource-group <rg> --name <account>
az storage account create --resource-group <rg> --name <account> --sku Standard_LRS --kind StorageV2
az storage account delete --resource-group <rg> --name <account> --yes

# Containers
az storage container list --account-name <account>
az storage container create --account-name <account> --name <container>

# Blobs
az storage blob list --account-name <account> --container-name <container>
az storage blob upload --account-name <account> --container-name <container> --file <local_file> --name <blob_name>
az storage blob download --account-name <account> --container-name <container> --name <blob_name> --file <local_file>
az storage blob delete --account-name <account> --container-name <container> --name <blob_name>

# SAS token
az storage container generate-sas --account-name <account> --name <container> \
  --permissions rwdl --expiry 2025-12-31
```
