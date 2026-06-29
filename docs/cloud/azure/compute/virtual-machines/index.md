---
tags:
  - azure
---
# Virtual Machines

<div class="kb-summary">
Reference for creating, managing, sizing, and operating Azure Virtual Machines using the `az vm` CLI commands.

*Applies to: Azure*
</div>

---

## Azure VM Architecture

```mermaid
flowchart TD
    subgraph vmComponents["VM Components"]
        compute["Compute\nvCPU · RAM (SKU)"]
        osDisk["OS Disk\nManaged Disk (P/E/S)"]
        dataDisks["Data Disks\nup to 64 per VM"]
        nic["NIC\nIP · NSG · Accelerated Networking"]
    end
    subgraph platform["Platform Services"]
        avail["Availability Zone / Set"]
        ext["Extensions\nMonitor Agent · Defender · Custom Script"]
        diagBoot["Boot Diagnostics\nserial console · screenshot"]
    end
    rg["Resource Group"]
    vnet["Virtual Network / Subnet"]

    rg --> vmComponents
    rg --> platform
    nic --> vnet
    avail --> compute
```

## Azure VM Deployment Flow

```mermaid
flowchart TD
    request["Deployment Request\nPortal · CLI · Terraform · ARM"]
    rbacCheck["RBAC Check\nMicrosoft.Compute/virtualMachines/write"]
    policyCheck["Azure Policy Evaluation\nallowed SKUs · location · tags"]
    policyDeny["Deployment DENIED\npolicy non-compliant"]
    armValidate["ARM Template Validation\nresource provider checks"]
    resourceGroup["Resource Group\ncontainer for resources"]
    subgraph provision["Provisioning"]
        osDisk["OS Disk\nManaged Disk provisioned"]
        nic["NIC\nIP allocated from subnet"]
        compute["Compute\nVM SKU allocated in AZ"]
    end
    extensions["Extensions Applied\nMonitor Agent · Defender · Custom Script"]
    running["VM Running\nProvisioning state: Succeeded"]

    request --> rbacCheck --> policyCheck
    policyCheck -- Non-compliant --> policyDeny
    policyCheck -- Compliant --> armValidate --> resourceGroup --> provision
    provision --> extensions --> running
```

## Creating VMs

```bash
# Create a Linux VM with defaults
az vm create \
  --resource-group <rg> \
  --name <vm-name> \
  --image Ubuntu2204 \
  --size Standard_D2s_v3 \
  --admin-username azureuser \
  --generate-ssh-keys

# Create a Windows VM
az vm create \
  --resource-group <rg> \
  --name <win-vm-name> \
  --image Win2022Datacenter \
  --size Standard_D2s_v3 \
  --admin-username azureuser \
  --admin-password <password>

# Create a VM in a specific zone with a static private IP
az vm create \
  --resource-group <rg> \
  --name <vm-name> \
  --image Ubuntu2204 \
  --size Standard_D4s_v3 \
  --zone 1 \
  --vnet-name <vnet-name> \
  --subnet <subnet-name> \
  --private-ip-address 10.0.1.10 \
  --public-ip-sku Standard \
  --admin-username azureuser \
  --generate-ssh-keys \
  --tags env=prod role=webserver
```


```text title="Expected output"
{
  "fqdns": "vm-prod-01.eastus.cloudapp.azure.com",
  "id": "/subscriptions/12a34b5c-6789-0d1e-2f3g-4h5i6j7k8l9m/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/vm-prod-01",
  "location": "eastus",
  "macAddress": "00:0D:3A:2F:5C:8E",
  "powerState": "VM running",
  "privateIpAddress": "10.0.1.4",
  "publicIpAddress": "20.45.123.67",
  "resourceGroup": "prod-rg",
  "zones": ""
}
{
  "fqdns": "win-vm-prod-01.eastus.cloudapp.azure.com",
  "id": "/subscriptions/12a34b5c-6789-0d1e-2f3g-4h5i6j7k8l9m/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/win-vm-prod-01",
  "location": "eastus",
  "powerState": "VM running",
  "privateIpAddress": "10.0.1.5",
  "publicIpAddress": "20.45.124.89",
  "resourceGroup": "prod-rg"
}
{
  "fqdns": "vm-zoned-01.eastus.cloudapp.azure.com",
  "id": "/subscriptions/12a34b5c-6789-0d1e-2f3g-4h5i6j7k8l9m/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/vm-zoned-01",
  "location": "eastus",
  "powerState": "VM running",
  "privateIpAddress": "10.0.1.10",
  "publicIpAddress": "20.45.125.42",
  "resourceGroup": "prod-rg",
  "zones": [
    "1"
  ]
}
```

!!! warning "Common errors"
    **`ResourceGroupNotFound`** — Verify the resource group exists in your subscription with `az group list` and use the correct `--resource-group` name.
    **`InvalidImageName`** — Use `az vm image list --output table` to find valid image names for your region, as image availability varies by location.
    **`PrivateIPAddressNotAvailable`** — Ensure the static IP address 10.0.1.10 is within the subnet range and not already assigned to another resource.
---

## VM Sizing

```bash
# List available VM sizes in a region
az vm list-sizes \
  --location eastus \
  --output table

# List sizes available for a VM (before resize)
az vm list-vm-resize-options \
  --resource-group <rg> \
  --name <vm-name> \
  --output table

# Resize an existing VM
az vm resize \
  --resource-group <rg> \
  --name <vm-name> \
  --size Standard_D4s_v3
```


```text title="Expected output"
Name                   NumberOfCores    MemoryInMB    ResourceDiskSizeInMB
---------------------  ---------------  -----------  ----------------------
Standard_B1s           1                 1024         4096
Standard_B2s           2                 4096         8192
Standard_D2s_v3        2                 8192         16384
Standard_D4s_v3        4                 16384        32768
Standard_D8s_v3        8                 32768        65536
...

Name                   NumberOfCores    MemoryInMB    ResourceDiskSizeInMB
---------------------  ---------------  -----------  ----------------------
Standard_D2s_v3        2                 8192         16384
Standard_D4s_v3        4                 16384        32768
Standard_D8s_v3        8                 32768        65536
Standard_E4s_v3        4                 32768        65536

(no output — command completes silently)
```

!!! warning "Common errors"
    **`The resource group '<rg>' could not be found.`** — Verify the resource group name with `az group list` and ensure you're using the correct subscription with `az account set --subscription <id>`.
    **`The virtual machine '<vm-name>' does not exist in the resource group '<rg>'.`** — Confirm the VM name with `az vm list --resource-group <rg>` and check that the VM is in the correct resource group.
    **`Operation failed with status: 'Conflict'. Details: The VM '<vm-name>' is currently in a running state. Please deallocate the VM before resizing.`** — Stop the VM first with `az vm deallocate --resource-group <rg> --name <vm-name>`, then retry the resize command.
Common VM size families:

| Family | Use Case | Example SKUs |
|---|---|---|
| Dsv5 / Dsv4 | General purpose (balanced) | Standard_D2s_v5, D4s_v5 |
| Esv5 / Esv4 | Memory-optimised | Standard_E4s_v5, E8s_v5 |
| Fsv2 | Compute-optimised | Standard_F4s_v2, F8s_v2 |
| Lsv3 | Storage-optimised (NVMe) | Standard_L8s_v3 |
| Msv3 | Large memory (SAP) | Standard_M8ms |
| NCasT4_v3 | GPU (inference) | Standard_NC4as_T4_v3 |

---

## Power State Operations

```bash
# Start a deallocated VM
az vm start --resource-group <rg> --name <vm-name>

# Stop (OS shutdown) — billing continues
az vm stop --resource-group <rg> --name <vm-name>

# Deallocate — stop billing for compute
az vm deallocate --resource-group <rg> --name <vm-name>

# Restart
az vm restart --resource-group <rg> --name <vm-name>

# Force delete (skip shutdown)
az vm delete --resource-group <rg> --name <vm-name> --force-deletion yes --yes

# Batch start all VMs in a resource group
az vm list --resource-group <rg> --query "[].name" --output tsv | \
  xargs -I {} az vm start --resource-group <rg> --name {}
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1cde/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01",
  "name": "web-vm-01",
  "powerState": "VM running",
  "provisioningState": "Succeeded",
  "resourceGroup": "prod-rg"
}
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1cde/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01",
  "name": "web-vm-01",
  "powerState": "VM stopped",
  "provisioningState": "Succeeded",
  "resourceGroup": "prod-rg"
}
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1cde/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01",
  "name": "web-vm-01",
  "powerState": "VM deallocated",
  "provisioningState": "Succeeded",
  "resourceGroup": "prod-rg"
}
web-vm-01
web-vm-02
web-vm-03
{
  "powerState": "VM running",
  "provisioningState": "Succeeded"
}
{
  "powerState": "VM running",
  "provisioningState": "Succeeded"
}
```

!!! warning "Common errors"
    **`ResourceGroupNotFound : Resource group '<rg>' could not be found.`** — Verify the resource group name with `az group list` and use the correct spelling and subscription context.
    **`ResourceNotFound : The Resource 'Microsoft.Compute/virtualMachines/<vm-name>' under resource group '<rg>' was not found.`** — Confirm the VM name exists in the resource group using `az vm list --resource-group <rg>`.
    **`AuthorizationFailed : The client '<user-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Compute/virtualMachines/start/action' over scope '<resource-id>'.`** — Ensure your Azure account has Contributor or Virtual Machine Contributor role on the resource group.
---

## Disk Operations

```bash
# Add a new managed data disk to a running VM
az vm disk attach \
  --resource-group <rg> \
  --vm-name <vm-name> \
  --name <new-disk-name> \
  --new \
  --size-gb 256 \
  --sku Premium_LRS

# Attach an existing managed disk
az vm disk attach \
  --resource-group <rg> \
  --vm-name <vm-name> \
  --name <existing-disk-name>

# Detach a data disk
az vm disk detach \
  --resource-group <rg> \
  --vm-name <vm-name> \
  --name <disk-name>

# List disks attached to a VM
az vm show \
  --resource-group <rg> \
  --name <vm-name> \
  --query "storageProfile.dataDisks[].{Name:name, Lun:lun, SizeGB:diskSizeGb, Sku:managedDisk.storageAccountType}" \
  --output table
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890ab1234/resourceGroups/prod-rg/providers/Microsoft.Compute/disks/datadisk-prod-256gb",
  "location": "eastus",
  "name": "datadisk-prod-256gb",
  "resourceGroup": "prod-rg",
  "sku": {
    "name": "Premium_LRS"
  },
  "timeCreated": "2024-01-15T10:23:45.123456+00:00"
}
(no output — command completes silently)
(no output — command completes silently)
Name                  Lun    SizeGB    Sku
--------------------  -----  --------  ---------------
datadisk-prod-256gb   0      256       Premium_LRS
datadisk-app-128gb    1      128       Standard_LRS
datadisk-backup-512   2      512       Premium_LRS
```

!!! warning "Common errors"
    **`ResourceNotFound: The Resource 'Microsoft.Compute/virtualMachines/<vm-name>' under resource group '<rg>' was not found.`** — Verify the resource group name and VM name are correct with `az vm list --resource-group <rg>`.
    **`The disk '<disk-name>' cannot be attached because it is already managed by another virtual machine.`** — Detach the disk from its current VM first using `az vm disk detach` before attaching it to a different VM.
---

## Networking

```bash
# List NICs attached to a VM
az vm show \
  --resource-group <rg> \
  --name <vm-name> \
  --query "networkProfile.networkInterfaces[].id" \
  --output tsv

# Add a public IP to an existing NIC
az network nic ip-config update \
  --resource-group <rg> \
  --nic-name <nic-name> \
  --name ipconfig1 \
  --public-ip-address <pip-name>

# Open a port in the NSG (quick rule for testing)
az vm open-port \
  --resource-group <rg> \
  --name <vm-name> \
  --port 443

# Get the public IP of a VM
az vm list-ip-addresses \
  --resource-group <rg> \
  --name <vm-name> \
  --output table
```

---

## Running Commands on a VM

```bash
# Run a shell command on a Linux VM without SSH
az vm run-command invoke \
  --resource-group <rg> \
  --name <vm-name> \
  --command-id RunShellScript \
  --scripts "df -h && free -m && uptime"

# Run a PowerShell command on a Windows VM
az vm run-command invoke \
  --resource-group <rg> \
  --name <win-vm-name> \
  --command-id RunPowerShellScript \
  --scripts "Get-Process | Sort-Object CPU -Descending | Select-Object -First 10"
```

---

## Monitoring and Health

```bash
# Show VM power state and provisioning state
az vm show \
  --resource-group <rg> \
  --name <vm-name> \
  --show-details \
  --query "{PowerState:powerState, ProvisioningState:provisioningState}" \
  --output table

# Get instance view (agent status, extension status, disk statuses)
az vm get-instance-view \
  --resource-group <rg> \
  --name <vm-name> \
  --query "instanceView.{Agent:vmAgent.statuses[0].displayStatus, Disks:disks[].statuses[0].displayStatus}" \
  --output json

# List all VMs across all resource groups in a subscription
az vm list --show-details \
  --query "[].{Name:name, RG:resourceGroup, Size:hardwareProfile.vmSize, State:powerState, Location:location}" \
  --output table
```
