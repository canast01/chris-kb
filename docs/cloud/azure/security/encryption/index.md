---
tags:
  - azure
  - security
---
# Azure — Encryption


<div class="kb-summary">
Azure encrypts all data at rest by default using platform-managed keys (PMK). Customer-managed keys (CMK) in Azure Key Vault give you control over the encryption key lifecycle. Data in transit is protected by TLS 1.2+ for all Azure service endpoints.

*Applies to: Azure*
</div>
```text
┌────────────────────────────────── Cloud Azure Security — Encryption ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Azure encryption: data at rest and in transit encryption for all stored data         │   │
│   │          At rest: AES-256 encryption using controller-managed or external key manager         │   │
│   │          In transit: TLS 1.2+ for management; protocol encryption for data in flight          │   │
│   │         Key management: external KMIP-compatible KMS or built-in key lifecycle manager        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Enable encryption → configure KMS → verify → audit → rotate keys                                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │     Standard     │     Key source    │       KMS        │      Notes       │   │
│   │     At rest      │     AES-256      │     Controller    │  Internal/KMIP   │    Always on     │   │
│   │    In transit    │     TLS 1.2+     │      PKI cert     │   Internal CA    │   Mgmt + data    │   │
│   │   Key rotation   │      Annual      │     KMS policy    │   External KMS   │    Automated     │   │
│   │    Key escrow    │     Required     │     KMS vault     │   External KMS   │    DR access     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Cloud Azure Security infrastructure · management network · monitoring                    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Cloud Azure Security platform overview and core concepts                      │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Encryption Coverage by Service

| Service | At Rest | In Transit | CMK Support |
|---|---|---|---|
| Azure Storage (blobs, files, queues, tables) | AES-256, PMK default | TLS 1.2+ | Yes — Key Vault |
| Managed Disks | AES-256, PMK default | N/A (internal) | Yes — Disk Encryption Set |
| Azure SQL / SQL MI | TDE, PMK default | TLS 1.2+ | Yes — Key Vault |
| Azure Key Vault | AES-256, PMK | TLS 1.2+ | Yes — HSM-backed |
| Azure Backup | AES-256 | TLS 1.2+ | Yes — Key Vault |
| AKS (etcd) | AES-256, PMK | TLS 1.2+ | Yes — Key Vault |
| Azure Kubernetes node disks | PMK default | N/A | Yes — Disk Encryption Set |

---

## Azure Key Vault

Key Vault stores and controls access to keys, secrets, and certificates. All access is logged to Azure Monitor.

```bash
# Create a Key Vault (soft-delete and purge protection required for CMK)
az keyvault create \
  --name <kv-name> \
  --resource-group <rg-name> \
  --location <region> \
  --sku standard \
  --enable-soft-delete true \
  --enable-purge-protection true \
  --retention-days 90

# Set access policy (legacy model — prefer RBAC)
az keyvault set-policy \
  --name <kv-name> \
  --object-id <principal-object-id> \
  --key-permissions get list create delete unwrapKey wrapKey \
  --secret-permissions get list set delete

# Enable RBAC authorization (preferred over access policies)
az keyvault update \
  --name <kv-name> \
  --resource-group <rg-name> \
  --enable-rbac-authorization true

# Assign Key Vault Crypto Officer to an identity
az role assignment create \
  --role "Key Vault Crypto Officer" \
  --assignee <principal-object-id> \
  --scope <key-vault-resource-id>

# Check Key Vault firewall — restrict to known subnets and private endpoint
az keyvault network-rule list --name <kv-name>
```

### Key Vault Operations

```bash
# Create a key
az keyvault key create \
  --vault-name <kv-name> \
  --name <key-name> \
  --kty RSA \
  --size 4096 \
  --ops wrapKey unwrapKey

# List keys
az keyvault key list --vault-name <kv-name> --output table

# List secrets
az keyvault secret list --vault-name <kv-name> --output table

# Show a secret value
az keyvault secret show --vault-name <kv-name> --name <secret-name> --query value -o tsv

# Set a secret
az keyvault secret set \
  --vault-name <kv-name> \
  --name <secret-name> \
  --value "<secret-value>"

# Rotate a key (creates a new version; old version retained until explicitly deleted)
az keyvault key rotate --vault-name <kv-name> --name <key-name>
```

---

## Customer-Managed Keys for Storage

```bash
# Create a key for storage encryption
az keyvault key create \
  --vault-name <kv-name> \
  --name storage-cmk \
  --kty RSA \
  --size 4096

# Enable CMK on a storage account
az storage account update \
  --name <storage-account> \
  --resource-group <rg-name> \
  --encryption-key-source Microsoft.Keyvault \
  --encryption-key-vault "https://<kv-name>.vault.azure.net" \
  --encryption-key-name storage-cmk \
  --encryption-key-version <key-version>

# Verify CMK is active
az storage account show \
  --name <storage-account> \
  --query "encryption" \
  --output json
```

---

## Customer-Managed Keys for Managed Disks

Disk Encryption Sets (DES) link a Key Vault key to managed disk encryption.

```bash
# Create a Disk Encryption Set
az disk-encryption-set create \
  --name <des-name> \
  --resource-group <rg-name> \
  --location <region> \
  --key-url "https://<kv-name>.vault.azure.net/keys/<key-name>/<key-version>" \
  --source-vault <kv-resource-id>

# Grant the DES access to the Key Vault key
DES_IDENTITY=$(az disk-encryption-set show \
  --name <des-name> \
  --resource-group <rg-name> \
  --query "identity.principalId" -o tsv)

az role assignment create \
  --role "Key Vault Crypto Service Encryption User" \
  --assignee $DES_IDENTITY \
  --scope <kv-resource-id>

# Create a managed disk using the DES
az disk create \
  --name <disk-name> \
  --resource-group <rg-name> \
  --size-gb 128 \
  --disk-encryption-set <des-resource-id>

# Apply DES to an existing VM's OS disk
az vm update \
  --name <vm-name> \
  --resource-group <rg-name> \
  --disk-encryption-set <des-resource-id>
```

---

## Azure Disk Encryption (ADE)

ADE encrypts VM disks at the OS level using BitLocker (Windows) or DM-Crypt (Linux). Keys are stored in Key Vault.

```bash
# Enable ADE on a Windows VM
az vm encryption enable \
  --name <vm-name> \
  --resource-group <rg-name> \
  --disk-encryption-keyvault <kv-resource-id>

# Enable ADE on a Linux VM
az vm encryption enable \
  --name <vm-name> \
  --resource-group <rg-name> \
  --disk-encryption-keyvault <kv-resource-id> \
  --volume-type All

# Check ADE status
az vm encryption show \
  --name <vm-name> \
  --resource-group <rg-name>
```

> **ADE vs Server-Side Encryption (SSE):** SSE with CMK (Disk Encryption Set) encrypts at the storage layer — simpler to manage and works for all disk types. ADE encrypts at the OS layer — required for some compliance standards (FIPS 140-2). Do not apply both; pick one per workload.

---

## TLS Enforcement

### Storage Account

```bash
# Require TLS 1.2 minimum on storage accounts
az storage account update \
  --name <storage-account> \
  --resource-group <rg-name> \
  --min-tls-version TLS1_2

# Verify minimum TLS version
az storage account show \
  --name <storage-account> \
  --query "minimumTlsVersion"

# Require HTTPS-only (disable HTTP)
az storage account update \
  --name <storage-account> \
  --resource-group <rg-name> \
  --https-only true
```

### App Service / API Management

```bash
# Set minimum TLS on App Service
az webapp config set \
  --name <app-name> \
  --resource-group <rg-name> \
  --min-tls-version 1.2

# Enforce HTTPS redirect
az webapp update \
  --name <app-name> \
  --resource-group <rg-name> \
  --https-only true
```

---

## Private Endpoints for Key Vault

Key Vault should only be accessible from private endpoints — no public network access.

```bash
# Disable public network access on Key Vault
az keyvault update \
  --name <kv-name> \
  --resource-group <rg-name> \
  --public-network-access Disabled

# Create a private endpoint
az network private-endpoint create \
  --name pe-keyvault \
  --resource-group <rg-name> \
  --vnet-name <vnet-name> \
  --subnet <subnet-name> \
  --private-connection-resource-id <kv-resource-id> \
  --group-id vault \
  --connection-name pec-keyvault

# Create DNS record for private endpoint resolution
az network private-dns zone create \
  --resource-group <rg-name> \
  --name "privatelink.vaultcore.azure.net"

az network private-endpoint dns-zone-group create \
  --resource-group <rg-name> \
  --endpoint-name pe-keyvault \
  --name keyvault-dns-group \
  --private-dns-zone "privatelink.vaultcore.azure.net" \
  --zone-name keyvault
```

---

## Key Vault Diagnostics

```bash
# Enable audit logging to Log Analytics
az monitor diagnostic-settings create \
  --name kv-diagnostics \
  --resource <kv-resource-id> \
  --workspace <log-analytics-workspace-id> \
  --logs '[{"category": "AuditEvent", "enabled": true}]'

# Query Key Vault access logs in Log Analytics
# AzureDiagnostics
# | where ResourceType == "VAULTS"
# | where OperationName in ("SecretGet", "KeyUnwrap", "KeyWrap")
# | project TimeGenerated, CallerIPAddress, identity_claim_oid_g, OperationName, ResultType
# | order by TimeGenerated desc

# Alert on Key Vault secret access by unexpected principals
# Create a scheduled query rule in Azure Monitor targeting the above query
```
