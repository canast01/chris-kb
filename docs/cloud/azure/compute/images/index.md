---
tags:
  - azure
description: "Azure VM images are the base OS configurations used to create virtual machines. This page covers Marketplace images, custom images, Azure Compute Gallery..."
---
# VM Images

<div class="kb-summary">
Azure VM images are the base OS configurations used to create virtual machines. This page covers Marketplace images, custom images, Azure Compute Gallery (ACG), and image versioning.

*Applies to: Azure*
</div>

---

## Azure Image Lifecycle

```d2
direction: right

marketplace: "Azure Marketplace Image\nPublisher · Offer · SKU" {shape: rectangle}
customise: "Customise VM\ninstall software · harden" {shape: rectangle}
generalise: "Generalise\nsysprep (Windows) · waagent (Linux" {shape: rectangle}
captureImage: "Capture Image\ncustom image" {shape: rectangle}
acg: "Azure Compute Gallery\nimage definition + versions" {shape: rectangle}
deploy: "Deploy VMs\nfrom gallery image version" {shape: rectangle}

marketplace -> customise
customise -> generalise
generalise -> captureImage
captureImage -> acg
acg -> deploy
deploy -> customise
```

## Marketplace Images

```bash
# List all publishers in a region
az vm image list-publishers \
  --location eastus \
  --output table | head -30

# List offers from a specific publisher
az vm image list-offers \
  --location eastus \
  --publisher Canonical \
  --output table

# List SKUs for an offer
az vm image list-skus \
  --location eastus \
  --publisher Canonical \
  --offer 0001-com-ubuntu-server-jammy \
  --output table

# Get the latest version of a specific SKU
az vm image list \
  --location eastus \
  --publisher Canonical \
  --offer 0001-com-ubuntu-server-jammy \
  --sku 22_04-lts-gen2 \
  --all \
  --query "[-1]" \
  --output json

# Use a marketplace image URN to create a VM
az vm create \
  --resource-group <rg> \
  --name <vm-name> \
  --image Ubuntu2204 \
  --size Standard_D2s_v3 \
  --admin-username azureuser \
  --generate-ssh-keys
```


```text title="Expected output"
Publisher                                Location
-----------------------------------------------------
Canonical                                eastus
MicrosoftWindowsServer                   eastus
MicrosoftSQLServer                       eastus
RedHat                                   eastus
OpenLogic                                eastus
Bitnami                                  eastus
...

Offer
-----------------------------------------------------
0001-com-ubuntu-server-focal
0001-com-ubuntu-server-jammy
0001-com-ubuntu-server-noble
WindowsServer
SQLServer2019-WS2019
...

Sku
-----------------------------------------------------
20_04-lts-gen2
22_04-lts-gen2
22_04-lts-arm64
23_10-daily-gen2
...

{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/providers/Microsoft.Compute/locations/eastus/publishers/Canonical/artifacttypes/vmimage/offers/0001-com-ubuntu-server-jammy/skus/22_04-lts-gen2/versions/22.04.202401150",
  "location": "eastus",
  "name": "22.04.202401150",
  "offer": "0001-com-ubuntu-server-jammy",
  "publisher": "Canonical",
  "sku": "22_04-lts-gen2",
  "version": "22.04.202401150"
}

It is recommended to use an image alias instead of a full URN for better maintainability.
{
  "fqdns": "",
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/myResourceGroup/providers/Microsoft.Compute/virtualMachines/myvm01",
  "location": "eastus",
  "macAddress": "00:0D:3A:12:34:56",
  "powerState": "VM running",
  "privateIpAddress": "10.0.0.4",
  "publicIpAddress": "20.45.67.89",
  "resourceGroup": "myResourceGroup"
}
```

!!! warning "Common errors"
    **`ERROR: unrecognized arguments: --all`** — Remove the `--all` flag; use `--query "[0]"` to get the latest version instead.
    **`ERROR: The resource group '<rg>' could not be found.`** — Replace `<rg>` with an actual resource group name or create it first with `az group create --name <rg> --location eastus`.
    **`ERROR: The image 'Ubuntu2204' could not be found.`** — Use the full URN format `Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest` or verify the image alias exists in your region.
Common image aliases:

| Alias | Full URN |
|---|---|
| `Ubuntu2204` | Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest |
| `Ubuntu2404` | Canonical:ubuntu-24_04-lts:server:latest |
| `Win2022Datacenter` | MicrosoftWindowsServer:WindowsServer:2022-datacenter-g2:latest |
| `Win2019Datacenter` | MicrosoftWindowsServer:WindowsServer:2019-datacenter-gensecond:latest |
| `RHEL94` | RedHat:RHEL:9_4:latest |
| `Debian12` | Debian:debian-12:12:latest |

---

## Creating Custom Images

Before creating a custom image, the VM must be generalised (sysprep on Windows, waagent deprovision on Linux).

```bash
# Step 1: Generalise a Linux VM
az vm run-command invoke \
  --resource-group <rg> \
  --name <vm-name> \
  --command-id RunShellScript \
  --scripts "sudo waagent -deprovision+user -force"

# Step 2: Deallocate and generalise
az vm deallocate --resource-group <rg> --name <vm-name>
az vm generalize --resource-group <rg> --name <vm-name>

# Step 3: Create an image from the generalised VM
az image create \
  --resource-group <rg> \
  --name <image-name> \
  --source <vm-name> \
  --location eastus

# List custom images in a resource group
az image list --resource-group <rg> --output table

# Deploy a VM from a custom image
az vm create \
  --resource-group <rg> \
  --name <new-vm-name> \
  --image <image-resource-id> \
  --size Standard_D2s_v3 \
  --admin-username azureuser \
  --generate-ssh-keys
```


```text title="Expected output"
{
  "value": [
    {
      "code": "ProvisioningState/succeeded",
      "displayStatus": "Provision succeeded",
      "message": "Enable succeeded",
      "time": "2024-01-15T10:42:33.521212+00:00"
    }
  ]
}
(no output — command completes silently)
(no output — command completes silently)
{
  "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/prod-rg/providers/Microsoft.Compute/images/ubuntu-base-image-v1",
  "location": "eastus",
  "name": "ubuntu-base-image-v1",
  "provisioningState": "Succeeded",
  "resourceGroup": "prod-rg"
}
ResourceGroup    Name                        Location    ProvisioningState
---------------  --------------------------  ----------  -------------------
prod-rg          ubuntu-base-image-v1       eastus      Succeeded
prod-rg          windows-server-2022-img    eastus      Succeeded
prod-rg          debian-11-custom           eastus      Succeeded
{
  "fqdns": "",
  "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-server-01",
  "location": "eastus",
  "macAddress": "00:0D:3A:2F:5C:8B",
  "powerState": "VM running",
  "privateIpAddress": "10.0.1.25",
  "publicIpAddress": "52.168.94.187",
  "resourceGroup": "prod-rg"
}
```

!!! warning "Common errors"
    **`The source VM must be generalized before creating an image.`** — Run `az vm generalize` on the source VM before executing the image create command.
    **`The image resource ID is invalid or the image does not exist in the specified resource group.`** — Verify the image resource ID with `az image list --resource-group <rg>` and ensure you are using the correct subscription and resource group.
    **`Run command failed with exit code 1. Error: sudo: command not found`** — Ensure the VM has the Azure VM Agent installed and the waagent command is available; use a supported Linux distribution image as the base.
---

## Azure Compute Gallery (ACG)

ACG (formerly Shared Image Gallery) provides enterprise-grade image management with versioning, replication, and RBAC.

```bash
# Create an Azure Compute Gallery
az sig create \
  --resource-group <rg> \
  --gallery-name <gallery-name> \
  --location eastus

# Create an image definition in the gallery
az sig image-definition create \
  --resource-group <rg> \
  --gallery-name <gallery-name> \
  --gallery-image-definition <image-def-name> \
  --publisher MyOrg \
  --offer WebServer \
  --sku Ubuntu2204 \
  --os-type Linux \
  --os-state Generalized \
  --hyper-v-generation V2

# Create an image version from a managed image or VM
az sig image-version create \
  --resource-group <rg> \
  --gallery-name <gallery-name> \
  --gallery-image-definition <image-def-name> \
  --gallery-image-version 1.0.0 \
  --managed-image <image-resource-id> \
  --target-regions eastus=1 westeurope=1 \
  --replica-count 1
```


```text title="Expected output"
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Compute/galleries/mycompgallery",
  "location": "eastus",
  "name": "mycompgallery",
  "provisioningState": "Succeeded",
  "resourceGroup": "prod-rg"
}
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Compute/galleries/mycompgallery/images/ubuntu-webserver-def",
  "location": "eastus",
  "name": "ubuntu-webserver-def",
  "osState": "Generalized",
  "osType": "Linux",
  "provisioningState": "Succeeded",
  "resourceGroup": "prod-rg"
}
{
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/prod-rg/providers/Microsoft.Compute/galleries/mycompgallery/images/ubuntu-webserver-def/versions/1.0.0",
  "location": "eastus",
  "name": "1.0.0",
  "provisioningState": "Succeeded",
  "publishingProfile": {
    "replicaCount": 1,
    "targetRegions": [
      {"name": "eastus", "regionalReplicaCount": 1},
      {"name": "westeurope", "regionalReplicaCount": 1}
    ]
  },
  "resourceGroup": "prod-rg"
}
```

!!! warning "Common errors"
    **`ResourceGroupNotFound`** — Verify the resource group name with `az group list` and ensure it exists in your subscription.
    **`InvalidManagedImageId`** — Confirm the managed image resource ID is correct by running `az image list --resource-group <rg> --query "[].id"`.
    **`GalleryImageVersionAlreadyExists`** — Use a different version number (e.g., 1.0.1) or delete the existing version with `az sig image-version delete`.
---

## Image Versioning and Replication

| Field | Description |
|---|---|
| Gallery Image Version | Semantic version, e.g. `1.0.0`, `2.1.3` |
| Target Regions | Regions where the version is replicated |
| Replica Count | Number of replicas per region (1–10) |
| End-of-Life Date | Date after which the version is hidden from `latest` |

```bash
# List all image versions for a definition
az sig image-version list \
  --resource-group <rg> \
  --gallery-name <gallery-name> \
  --gallery-image-definition <image-def-name> \
  --output table

# Deploy a VM from a gallery image version
az vm create \
  --resource-group <rg> \
  --name <vm-name> \
  --image "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Compute/galleries/<gallery>/images/<image-def>/versions/1.0.0" \
  --size Standard_D2s_v3 \
  --admin-username azureuser \
  --generate-ssh-keys

# Deprecate an old image version
az sig image-version update \
  --resource-group <rg> \
  --gallery-name <gallery-name> \
  --gallery-image-definition <image-def-name> \
  --gallery-image-version 1.0.0 \
  --end-of-life-date 2026-12-31
```


```text title="Expected output"
Name    Publishing State    Replicated Region Count
------  ------------------  -----------------------
1.0.0   Succeeded           3
1.1.0   Succeeded           2
1.2.0   Succeeded           1
2.0.0   InProgress          0

VM creation in progress... (Elapsed Time: 45s)
{
  "fqdns": "vm-prod-01.eastus.cloudapp.azure.com",
  "id": "/subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/vm-prod-01",
  "location": "eastus",
  "powerState": "VM running",
  "publicIpAddress": "40.71.82.145",
  "resourceGroup": "prod-rg"
}

(no output — command completes silently)
```

!!! warning "Common errors"
    **`ResourceNotFound : The resource '/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Compute/galleries/<gallery>/images/<image-def>/versions/1.0.0' could not be found.`** — Verify the subscription ID, resource group, gallery name, image definition, and version number are correct and exist in your subscription.
    **`InvalidParameter : The value of parameter 'image' is invalid.`** — Ensure the image URI follows the exact format `/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Compute/galleries/<gallery>/images/<image-def>/versions/<version>` with no extra spaces or slashes.
    **`AuthorizationFailed : The client '<user-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Compute/galleries/images/versions/read' over scope '/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Compute/galleries/<gallery>'.`** — Add the Contributor or Custom Role with `Microsoft.Compute/galleries/images/versions/*` permissions to your user or service principal.
---

## Sharing Gallery Images

```bash
# Share the gallery with another subscription (RBAC)
az role assignment create \
  --assignee <principal-id> \
  --role "Reader" \
  --scope "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Compute/galleries/<gallery-name>"

# List all galleries accessible in the subscription
az sig list --output table
```


```text title="Expected output"
(no output — command completes silently)

Name                          ResourceGroup        Location
-----------------------------  -------------------  ----------
SharedImageGallery-prod       rg-images-eastus     eastus
corp-gallery-shared           rg-compute-westus2   westus2
legacy-gallery-archive        rg-legacy-images     eastus
dev-gallery-internal          rg-dev-compute       centralus
marketplace-gallery-sync      rg-shared-resources   eastus
```

!!! warning "Common errors"
    **`Principal <principal-id> does not exist in the directory`** — Verify the principal ID is correct and exists in your Azure AD tenant using `az ad sp show --id <principal-id>`.
    **`The scope provided is invalid`** — Ensure the subscription ID, resource group name, and gallery name are correct by running `az sig list --query "[].id"` to get valid scope paths.