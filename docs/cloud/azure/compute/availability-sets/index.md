---
tags:
  - azure
---
# Availability Sets

<div class="kb-summary">
Availability Sets provide high availability for Azure VMs by distributing them across fault domains (separate physical hardware) and update domains (staggered maintenance windows). They protect against both hardware failures and planned maintenance events.

*Applies to: Azure*
</div>

---

```d2
direction: down

core_concepts: "Core Concepts" {shape: rectangle}
creating_an_availability_set: "Creating an Availability Set" {shape: rectangle}
deploying_vms_into_an_availability_s: "Deploying VMs into an Availability Set" {shape: rectangle}
fault_domain_and_update_domain_distr: "Fault Domain and Update Domain Distribution" {shape: rectangle}
availability_sets_vs_availability_zo: "Availability Sets vs Availability Zones vs VMSS" {shape: rectangle}
limitations: "Limitations" {shape: rectangle}

core_concepts -> creating_an_availability_set: uses
creating_an_availability_set -> deploying_vms_into_an_availability_s: uses
deploying_vms_into_an_availability_s -> fault_domain_and_update_domain_distr: uses
fault_domain_and_update_domain_distr -> availability_sets_vs_availability_zo: uses
availability_sets_vs_availability_zo -> limitations: uses
```

## Core Concepts

| Concept | Description |
|---|---|
| Fault Domain (FD) | Group of VMs sharing the same power source and network switch — max 3 FDs |
| Update Domain (UD) | Group of VMs rebooted together during planned maintenance — max 20 UDs |
| Managed Availability Set | Uses managed disks; Azure aligns disks with fault domains automatically |
| Aligned | Managed disk fault domain alignment — always use for new deployments |

**SLA:** 99.95% uptime when 2+ VMs are deployed across an Availability Set.

---

## Creating an Availability Set

```bash
# Create a managed Availability Set with 3 fault domains and 5 update domains
az vm availability-set create \
  --resource-group <rg> \
  --name <avset-name> \
  --location eastus \
  --platform-fault-domain-count 3 \
  --platform-update-domain-count 5

# Create with tags
az vm availability-set create \
  --resource-group <rg> \
  --name <avset-name> \
  --location eastus \
  --platform-fault-domain-count 2 \
  --platform-update-domain-count 5 \
  --tags env=prod tier=web

# List all availability sets in a resource group
az vm availability-set list \
  --resource-group <rg> \
  --output table

# Show availability set details including fault/update domain counts
az vm availability-set show \
  --resource-group <rg> \
  --name <avset-name>
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/prod-rg/providers/Microsoft.Compute/availabilitySets/web-avset-01",
  "location": "eastus",
  "name": "web-avset-01",
  "platformFaultDomainCount": 3,
  "platformUpdateDomainCount": 5,
  "resourceGroup": "prod-rg",
  "sku": "Aligned",
  "tags": null,
  "type": "Microsoft.Compute/availabilitySets",
  "virtualMachines": []
}
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890123456/resourceGroups/prod-rg/providers/Microsoft.Compute/availabilitySets/web-avset-02",
  "location": "eastus",
  "name": "web-avset-02",
  "platformFaultDomainCount": 2,
  "platformUpdateDomainCount": 5,
  "resourceGroup": "prod-rg",
  "tags": {
    "env": "prod",
    "tier": "web"
  },
  "type": "Microsoft.Compute/availabilitySets"
}
Name           ResourceGroup    Location    PlatformFaultDomainCount    PlatformUpdateDomainCount
-------------  ---------------  ----------  -------------------------  --------------------------
web-avset-01   prod-rg          eastus      3                            5
web-avset-02   prod-rg          eastus      2                            5
app-avset-03   prod-rg          eastus      2                            5
...
```

!!! warning "Common errors"
    **`ResourceGroupNotFound`** — Verify the resource group name with `az group list` and ensure you have access to the subscription.
    **`AvailabilitySetAlreadyExists`** — Use a unique name for the availability set or delete the existing one with `az vm availability-set delete --resource-group <rg> --name <avset-name>`.
    **`InvalidParameterValue: platformFaultDomainCount must be between 1 and 3`** — Reduce the `--platform-fault-domain-count` value to a maximum of 3 for your region.
---

## Deploying VMs into an Availability Set

VMs must be assigned to an Availability Set at creation time. You cannot move an existing VM into a set.

```bash
# Create VM 1 in the availability set
az vm create \
  --resource-group <rg> \
  --name <vm-name-1> \
  --image Ubuntu2204 \
  --size Standard_D2s_v3 \
  --availability-set <avset-name> \
  --admin-username azureuser \
  --generate-ssh-keys

# Create VM 2 in the same availability set
az vm create \
  --resource-group <rg> \
  --name <vm-name-2> \
  --image Ubuntu2204 \
  --size Standard_D2s_v3 \
  --availability-set <avset-name> \
  --admin-username azureuser \
  --generate-ssh-keys

# List VMs and their fault/update domain assignments
az vm availability-set show \
  --resource-group <rg> \
  --name <avset-name> \
  --query "virtualMachines[].id" --output tsv
```


```text title="Expected output"
It is recommended to use parameter "--public-ip-sku Standard" to create new public IP with Standard SKU. Please note that the default public IP used for VM creation will be changed from Basic to Standard in the future.
{
  "fqdns": "",
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01",
  "location": "eastus",
  "macAddress": "00:0D:3A:4F:2B:1C",
  "powerState": "VM running",
  "privateIpAddress": "10.0.1.4",
  "publicIpAddress": "52.168.45.123",
  "resourceGroup": "prod-rg",
  "zones": []
}
{
  "fqdns": "",
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-02",
  "location": "eastus",
  "macAddress": "00:0D:3A:4F:2B:2D",
  "powerState": "VM running",
  "privateIpAddress": "10.0.1.5",
  "publicIpAddress": "52.168.45.124",
  "resourceGroup": "prod-rg",
  "zones": []
}
/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01
/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-02
```

!!! warning "Common errors"
    **`The availability set '<avset-name>' does not exist in resource group '<rg>'`** — Create the availability set first using `az vm availability-set create --resource-group <rg> --name <avset-name>`.
    **`The image 'Ubuntu2204' could not be found`** — Use a valid image URN like `UbuntuLTS` or `Ubuntu2204` (verify with `az vm image list --output table`).
    **`Insufficient compute capacity in the region`** — Retry the command, use a different VM size, or deploy to an alternative availability zone/region.
---

## Fault Domain and Update Domain Distribution

```bash
# View the fault and update domain placement for each VM in the set
az vm show \
  --resource-group <rg> \
  --name <vm-name> \
  --query "{Name:name, FaultDomain:instanceView.platformFaultDomain, UpdateDomain:instanceView.platformUpdateDomain}" \
  --output table

# Check all VMs in a set with their domains
az vm list \
  --resource-group <rg> \
  --show-details \
  --query "[?availabilitySet.id!=null].{Name:name, FD:instanceView.platformFaultDomain, UD:instanceView.platformUpdateDomain}" \
  --output table
```


```text title="Expected output"
Name                FaultDomain    UpdateDomain
------------------  --------------  --------------
prod-web-vm-01      1               2
prod-web-vm-02      0               1
prod-web-vm-03      2               0

Name                FD    UD
------------------  ----  ----
prod-web-vm-01      1     2
prod-web-vm-02      0     1
prod-web-vm-03      2     0
prod-db-vm-01       1     0
prod-cache-vm-01    0     2
```

!!! warning "Common errors"
    **`ResourceNotFound : The Resource 'Microsoft.Compute/virtualMachines/<vm-name>' under resource group '<rg>' was not found.`** — Verify the VM name and resource group name are correct and the VM exists in that region.
    **`The client '<subscription-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Compute/virtualMachines/read' over scope '<resource-id>'.`** — Ensure your Azure CLI account has at least Reader role on the resource group or subscription.
---

## Availability Sets vs Availability Zones vs VMSS

| Feature | Availability Sets | Availability Zones | VM Scale Sets |
|---|---|---|---|
| Scope | Single datacenter | Zone-level (AZ1/AZ2/AZ3) | Single zone or multi-zone |
| Fault isolation | Rack-level | Datacenter-level | Depends on mode |
| SLA | 99.95% | 99.99% | 99.95% or 99.99% |
| Managed disk alignment | Yes (aligned) | Automatic | Automatic |
| Supports autoscale | No | No | Yes |
| Best for | Lift-and-shift HA | Greenfield zonal HA | Scalable workloads |

---

## Limitations

- VMs cannot be moved between Availability Sets after creation.
- Maximum 3 fault domains (2 in some regions — verify with `az vm list-skus`).
- Availability Sets do not protect against region-level outages — use ASR for cross-region DR.
- Availability Sets and Availability Zones are mutually exclusive for a given VM.

```bash
# Check supported fault domain counts for a region and VM size
az vm list-skus \
  --location eastus \
  --resource-type availabilitySets \
  --query "[].{Name:name, MaxFaultDomains:capabilities[?name=='MaximumPlatformFaultDomainCount'].value | [0]}" \
  --output table
```


```text title="Expected output"
Name                                    MaxFaultDomains
--------------------------------------  -----------------
Standard_A0                             2
Standard_A1                             2
Standard_A2                             2
Standard_D2s_v3                         3
Standard_D4s_v3                         3
Standard_E2s_v3                         3
Standard_F2s_v2                         3
...
```

!!! warning "Common errors"
    **`ERROR: unrecognized arguments: --resource-type availabilitySets`** — Use `--resource-type virtualMachines` instead, as availability set SKU data is queried through VM SKU listings.
    **`No subscription found. Run 'az login' to set up account.`** — Authenticate with `az login` and set the correct subscription using `az account set --subscription <subscription-id>`.
---

## Deleting an Availability Set

```bash
# An availability set must be empty before deletion
az vm availability-set delete \
  --resource-group <rg> \
  --name <avset-name>
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`The resource 'Microsoft.Compute/availabilitySets/<avset-name>' under resource group '<rg>' was not found.`** — Verify the availability set name and resource group name are correct using `az vm availability-set list --resource-group <rg>`.
    **`The Availability Set '<avset-name>' cannot be deleted because it still contains VM(s).`** — Delete or deallocate all VMs in the availability set before attempting deletion with `az vm delete --resource-group <rg> --name <vm-name>`.