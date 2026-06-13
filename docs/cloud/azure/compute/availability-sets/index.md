---
tags:
  - azure
---
# Availability Sets


<div class="kb-summary">
Availability Sets provide high availability for Azure VMs by distributing them across fault domains (separate physical hardware) and update domains (staggered maintenance windows). They protect against both hardware failures and planned maintenance events.

*Applies to: Azure*
</div>
```text
┌───────────────────────────────────────── Cloud Azure Compute ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Azure: Cloud Azure Compute platform                              │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                       Management: Cloud Azure Compute management console                      │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
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
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Cloud Azure Compute infrastructure · management network · monitoring                     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Cloud Azure Compute platform overview and core concepts                       │
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
