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

---

## Deleting an Availability Set

```bash
# An availability set must be empty before deletion
az vm availability-set delete \
  --resource-group <rg> \
  --name <avset-name>
```
