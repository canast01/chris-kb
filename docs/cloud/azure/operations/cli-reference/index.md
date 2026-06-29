---
tags:
  - azure
  - operations
---
# Azure Operations CLI Reference

<div class="kb-summary">
A practical reference for day-to-day Azure CLI usage: authentication, subscription management, resource group operations, output formatting, and productivity tools.

*Applies to: Azure*
</div>

---

```d2
direction: down

authentication_and_login: "Authentication and Login" {shape: rectangle}
account_and_subscription_management: "Account and Subscription Management" {shape: rectangle}
resource_group_operations: "Resource Group Operations" {shape: rectangle}
output_formats: "Output Formats" {shape: rectangle}
useful_queries_with_query: "Useful Queries with --query" {shape: rectangle}
az_find_command_discovery: "az find — Command Discovery" {shape: rectangle}

authentication_and_login -> account_and_subscription_management: uses
account_and_subscription_management -> resource_group_operations: uses
resource_group_operations -> output_formats: uses
output_formats -> useful_queries_with_query: uses
useful_queries_with_query -> az_find_command_discovery: uses
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Authentication and Login

```bash
# Interactive browser login
az login

# Login with a specific tenant
az login --tenant <tenant-id>

# Login with a service principal (client secret)
az login --service-principal \
  --username <app-id> \
  --password <client-secret> \
  --tenant <tenant-id>

# Login with a service principal (certificate)
az login --service-principal \
  --username <app-id> \
  --certificate /path/to/cert.pem \
  --tenant <tenant-id>

# Check current login status
az account show

# Logout
az logout
```


```text title="Expected output"
To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code ABC123DEF456 to authenticate.
[
  {
    "cloudName": "AzureCloud",
    "homeTenantId": "12345678-1234-1234-1234-123456789012",
    "id": "87654321-4321-4321-4321-210987654321",
    "isDefault": true,
    "name": "Production",
    "state": "Enabled",
    "tenantId": "12345678-1234-1234-1234-123456789012",
    "user": {
      "name": "admin@contoso.onmicrosoft.com",
      "type": "user"
    }
  }
]
{
  "environmentName": "AzureCloud",
  "homeTenantId": "12345678-1234-1234-1234-123456789012",
  "id": "87654321-4321-4321-4321-210987654321",
  "isDefault": true,
  "name": "Production",
  "state": "Enabled",
  "tenantId": "12345678-1234-1234-1234-123456789012",
  "user": {
    "name": "admin@contoso.onmicrosoft.com",
    "type": "servicePrincipal"
  }
}
```

!!! warning "Common errors"
    **`ERROR: AADSTS700016: Application with identifier 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' was not found in the directory`** — Verify the app ID is correct and exists in the target Azure AD tenant.
    **`ERROR: Get Token request returned http error: 401, server response details: "invalid_client"`** — Confirm the client secret or certificate has not expired and matches the registered credential in Azure AD.
    **`ERROR: Please run 'az login' to setup account`** — Run `az login` interactively or with service principal credentials before executing other Azure CLI commands.
---

## Account and Subscription Management

```bash
# List all subscriptions accessible to the logged-in identity
az account list --output table

# Set the active subscription
az account set --subscription <subscription-id-or-name>

# Show current subscription details
az account show --output json

# List subscriptions with specific fields
az account list \
  --query "[].{Name:name, ID:id, State:state}" \
  --output table

# Get the current subscription ID
az account show --query id --output tsv
```


```text title="Expected output"
Name                                 CloudName    SubscriptionId                       State
---------------------------------    -----------  ------------------------------------  -------
Production Environment               AzureCloud   a1b2c3d4-e5f6-7890-abcd-ef1234567890  Enabled
Development Sandbox                  AzureCloud   f9e8d7c6-b5a4-3210-fedc-ba9876543210  Enabled
Staging - Legacy                     AzureCloud   12345678-1234-1234-1234-123456789012  Enabled

{
  "environmentName": "AzureCloud",
  "homeTenantId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "isDefault": true,
  "name": "Production Environment",
  "state": "Enabled",
  "tenantId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "user": {
    "name": "admin@contoso.onmicrosoft.com",
    "type": "user"
  }
}

Name                    ID                                    State
----------------------  ------------------------------------  -------
Production Environment  a1b2c3d4-e5f6-7890-abcd-ef1234567890  Enabled
Development Sandbox     f9e8d7c6-b5a4-3210-fedc-ba9876543210  Enabled
Staging - Legacy        12345678-1234-1234-1234-123456789012  Enabled

a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

!!! warning "Common errors"
    **`ERROR: The subscription of '<subscription-id>' does not have a registered namespace for type 'Microsoft.Compute'.`** — Ensure the subscription has the required resource providers registered using `az provider register --namespace Microsoft.Compute`.
    **`ERROR: Please call 'az login' to setup account.`** — Authenticate with Azure using `az login` or `az login --service-principal` before running account commands.
    **`ERROR: No subscriptions found for '<subscription-name>'.`** — Verify the subscription name or ID is correct by running `az account list` to see all available subscriptions.
| Command | Description |
|---|---|
| `az account list` | List all subscriptions |
| `az account set` | Switch active subscription |
| `az account show` | Show active subscription |
| `az account get-access-token` | Get a bearer token for the current session |

---

## Resource Group Operations

```bash
# Create a resource group
az group create \
  --name <rg-name> \
  --location <region>

# List all resource groups
az group list --output table

# Show details of a specific resource group
az group show --name <rg-name>

# Delete a resource group (non-interactive)
az group delete --name <rg-name> --yes --no-wait

# List all resources inside a resource group
az resource list \
  --resource-group <rg-name> \
  --output table

# Move a resource between resource groups
az resource move \
  --destination-group <target-rg> \
  --ids <resource-id>

# Tag a resource group
az group update \
  --name <rg-name> \
  --tags env=prod owner=platform-team
```


```text title="Expected output"
Creating resource group 'prod-rg' in eastus...
{
  "id": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/prod-rg",
  "location": "eastus",
  "managedBy": null,
  "name": "prod-rg",
  "properties": {
    "provisioningState": "Succeeded"
  },
  "tags": {}
}

Name              Location    Status
-----------------  ----------  ---------
prod-rg            eastus      Succeeded
staging-rg         westus2     Succeeded
dev-rg             eastus      Succeeded

ResourceGroup: prod-rg
Location: eastus
ProvisioningState: Succeeded
Tags: env=prod owner=platform-team

Name                           Type                                    Location
-----------------------------  ------                                  ----------
prod-storage-acct              Microsoft.Storage/storageAccounts       eastus
prod-vnet                      Microsoft.Network/virtualNetworks       eastus
prod-nsg                       Microsoft.Network/networkSecurityGroups eastus
prod-vm-nic                    Microsoft.Network/networkInterfaces     eastus
...

Moving resource /subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/prod-rg/providers/Microsoft.Storage/storageAccounts/prodstorage to target-rg...
{
  "id": "/subscriptions/12a34b56-78cd-90ef-1234-567890abcdef/resourceGroups/target-rg/providers/Microsoft.Storage/storageAccounts/prodstorage",
  "location": "eastus",
  "name": "prodstorage",
  "type": "Microsoft.Storage/storageAccounts"
}

Updated resource group 'prod-rg' with tags: env=prod owner=platform-team
```

!!! warning "Common errors"
    **`ResourceGroupNotFound`** — Verify the resource group name matches exactly and exists in the current subscription using `az group list`.
    **`AuthorizationFailed: The client does not have permission to perform action 'Microsoft.Resources/resourceGroups/delete' on scope`** — Ensure your Azure account has Owner or Contributor role on the subscription using `az role assignment list --assignee <your-email>`.
---

## Output Formats

Azure CLI supports four primary output formats. The default is `json`.

```bash
# JSON (default, machine-readable)
az vm list --output json

# Table (human-readable)
az vm list --output table

# TSV (tab-separated, good for scripts)
az vm list --query "[].{Name:name}" --output tsv

# YAML
az vm list --output yaml

# Set a default output format
az configure --defaults output=table
```


```text title="Expected output"
[
  {
    "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-server-01",
    "location": "eastus",
    "name": "web-server-01",
    "powerState": "VM running",
    "resourceGroup": "prod-rg",
    "vmId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
  },
  {
    "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/db-server-02",
    "location": "westus2",
    "name": "db-server-02",
    "powerState": "VM deallocated",
    "resourceGroup": "prod-rg",
    "vmId": "b2c3d4e5-f6a7-8901-bcde-f12345678901"
  }
]

Name          ResourceGroup    PowerState      PublicIps    PrivateIps
-----------   ---------------  ---------------  -----------  -----------
web-server-01 prod-rg          VM running       40.71.12.45  10.0.1.5
db-server-02  prod-rg          VM deallocated              10.0.2.8

web-server-01
db-server-02

name: web-server-01
id: /subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-server-01
location: eastus
powerState: VM running
resourceGroup: prod-rg
vmId: a1b2c3d4-e5f6-7890-abcd-ef1234567890

(no output — command completes silently)
```

!!! warning "Common errors"
    **`ERROR: The following arguments are required: --resource-group/-g`** — Add `--resource-group <group-name>` or ensure you have a default resource group configured with `az configure --defaults group=<name>`.
    **`ERROR: Not authenticated. Run 'az login' to set up account.`** — Run `az login` to authenticate with your Azure subscription before executing VM commands.
| Format | Flag | Best For |
|---|---|---|
| JSON | `--output json` | Scripting, APIs, full data |
| Table | `--output table` | Human reading, quick review |
| TSV | `--output tsv` | Shell variable assignment, loops |
| YAML | `--output yaml` | Readability with structure |
| None | `--output none` | Suppress output in automation |

---

## Useful Queries with --query

The `--query` flag uses JMESPath syntax to filter and reshape output.

```bash
# Get only VM names and locations
az vm list --query "[].{Name:name, Location:location}" --output table

# Filter VMs by power state
az vm list \
  --resource-group <rg-name> \
  --query "[?powerState=='VM running'].name" \
  --output tsv

# Get the first public IP address
az network public-ip list \
  --query "[0].ipAddress" \
  --output tsv

# Get storage account names starting with 'prod'
az storage account list \
  --query "[?starts_with(name, 'prod')].name" \
  --output tsv

# Count all VMs across all resource groups
az vm list --query "length(@)"

# Get all resource IDs in a resource group
az resource list \
  --resource-group <rg-name> \
  --query "[].id" \
  --output tsv

# Extract a nested value (NIC private IP)
az vm show \
  --resource-group <rg-name> \
  --name <vm-name> \
  --query "networkProfile.networkInterfaces[0].id" \
  --output tsv
```


```text title="Expected output"
Name                Location
------------------  ----------
prod-web-01         eastus
prod-db-02          westus2
dev-app-03          eastus
staging-cache-01    centralus

prod-web-01
prod-db-02
staging-cache-01

203.0.113.45

prod-storage-main
prod-storage-backup
prod-storage-logs

42

/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myResourceGroup/providers/Microsoft.Compute/virtualMachines/prod-web-01
/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myResourceGroup/providers/Microsoft.Network/networkInterfaces/prod-web-01-nic
/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myResourceGroup/providers/Microsoft.Storage/storageAccounts/prodstorage01

/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/myResourceGroup/providers/Microsoft.Network/networkInterfaces/prod-web-01-nic
```

!!! warning "Common errors"
    **`ERROR: argument --resource-group/-g: expected one argument`** — Replace `<rg-name>` with your actual resource group name (e.g., `--resource-group myResourceGroup`).
    **`ERROR: (ResourceNotFound) The Resource 'Microsoft.Compute/virtualMachines/<vm-name>' under resource group '<rg-name>' was not found.`** — Verify the VM name and resource group exist by running `az vm list --resource-group <rg-name>` first.
    **`ERROR: No subscriptions found. Run 'az login' to set up an account.`** — Authenticate to Azure by running `az login` and selecting the correct subscription with `az account set --subscription <subscription-id>`.
---

## az find — Command Discovery

`az find` uses AI-backed search to help locate the right command when the exact syntax is unclear.

```bash
# Find commands related to a topic
az find "backup vault"

# Find examples for a specific command
az find "az vm create"

# Find commands for a service
az find "key vault secret"
```


```text title="Expected output"
# Find commands related to a topic
Found 12 matches for "backup vault"

az backup vault create
  Create a new backup vault.
  az backup vault create --resource-group MyResourceGroup --vault-name MyVault

az backup vault list
  List all backup vaults in a resource group.
  az backup vault list --resource-group MyResourceGroup

az backup vault show
  Show details of a backup vault.
  az backup vault show --resource-group MyResourceGroup --vault-name MyVault

az backup vault delete
  Delete a backup vault.
  az backup vault delete --resource-group MyResourceGroup --vault-name MyVault

# Find examples for a specific command
Found 8 matches for "az vm create"

az vm create
  Create an Azure virtual machine.
  az vm create --resource-group MyResourceGroup --name MyVM --image UbuntuLTS

az vm create (with managed disk)
  Create a VM with a managed disk.
  az vm create --resource-group MyResourceGroup --name MyVM --image Win2019Datacenter --os-disk-size-gb 128

# Find commands for a service
Found 15 matches for "key vault secret"

az keyvault secret set
  Set a secret in a key vault.
  az keyvault secret set --vault-name MyKeyVault --name MySecret --value MySecretValue

az keyvault secret get
  Get a secret from a key vault.
  az keyvault secret get --vault-name MyKeyVault --name MySecret

az keyvault secret list
  List all secrets in a key vault.
  az keyvault secret list --vault-name MyKeyVault
```

!!! warning "Common errors"
    **`ERROR: The following arguments are required: --resource-group`** — Ensure you have authenticated with `az login` and that your default subscription is set with `az account set --subscription <subscription-id>`.
    **`ERROR: 'find' is not in the 'az' command group. Did you mean 'az --help'?`** — Update the Azure CLI to the latest version with `az upgrade` as the `find` command requires Azure CLI 2.0.41 or later.
---

## az interactive — Autocomplete Shell

`az interactive` launches a rich shell with autocomplete, parameter hints, and inline documentation.

```bash
# Install the interactive extension
az extension add --name interactive

# Launch the interactive shell
az interactive
```


```text title="Expected output"
The following extensions will be installed:

Name      Version
--------  -------
interactive 0.4.5

(no output — command completes silently)

az-cli interactive shell
========================

Type "help" for commands. Type "?" for examples.

>>
```

!!! warning "Common errors"
    **`ERROR: The following extensions have dependency conflicts and cannot be installed: interactive [Dependency 'azure-cli-core' version does not match]`** — Upgrade Azure CLI to the latest version with `az upgrade` before installing the extension.
    
    **`ERROR: This command requires the extension 'interactive' to be installed. Try installing it with 'az extension add --name interactive'`** — Run `az extension add --name interactive` to install the required extension.
Inside the interactive shell:

| Key / Action | Effect |
|---|---|
| Tab | Autocomplete command or parameter |
| F1 | Open docs for the current command |
| `%` prefix | Run a native shell command |
| `exit` | Quit the interactive session |

---

## Configuration and Defaults

```bash
# Set default resource group and location
az configure --defaults group=<rg-name> location=eastus

# View current defaults
az configure --list-defaults

# Clear all defaults
az configure --defaults group='' location=''

# Upgrade CLI to the latest version
az upgrade

# Show the installed CLI version
az version
```


```text title="Expected output"
(no output — command completes silently)

The following defaults are set:
group                                  myapp-rg
location                               eastus

(no output — command completes silently)

Azure CLI is up to date (2.57.0).

{
  "azure-cli": "2.57.0",
  "azure-cli-core": "2.57.0",
  "azure-cli-telemetry": "1.1.0",
  "extensions": {}
}
```

!!! warning "Common errors"
    **`ERROR: argument --defaults: expected one argument`** — Ensure you provide key=value pairs with no spaces around the equals sign (e.g., `group=myapp-rg`).
    **`ERROR: This command requires the user to be logged in. Please run 'az login' to set up account.`** — Run `az login` to authenticate before configuring defaults.
    **`ERROR: The resource group '<rg-name>' could not be found.`** — Replace `<rg-name>` with an actual resource group name that exists in your subscription (verify with `az group list`).
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Azure — Procedures](../procedures/)
- [Azure — Scripts](../scripts/)
- [Azure — Health Checks](../health-checks/)
