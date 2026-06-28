---
tags:
  - servicenow
---
# Inventory — Asset Tracking

```bash
# Linux — server hardware info
dmidecode -t system | grep -E "Manufacturer|Product|Serial|UUID"
dmidecode -t bios | grep -E "Version|Release Date"

# Storage
lsblk -d -o NAME,SIZE,VENDOR,MODEL,SERIAL,ROTA
smartctl -a /dev/sda | grep -E "Serial|Model|Capacity|Health"

# Network interfaces
ip link show | awk '/^[0-9]/{print $2}'
ethtool <interface> | grep -E "Speed|Duplex"
```

```bash
# All VMs across subscription
az vm list --query '[*].{Name:name,RG:resourceGroup,Size:hardwareProfile.vmSize,Location:location,OS:storageProfile.osDisk.osType}' -o table

# Untagged resources
az resource list --query '[?tags==null || !tags.Owner] | [*].{Name:name,Type:type,RG:resourceGroup}' -o table

# Deallocated VMs (not deleted, still costing storage)
az vm list --query '[?powerState==`VM deallocated`] | [*].{Name:name,RG:resourceGroup}' -o table

# Unattached disks
az disk list --query '[?diskState==`Unattached`] | [*].{Name:name,Size:diskSizeGb,RG:resourceGroup}' -o table
```
```text
Ordered → Received → Configured → In Service → Decommission Pending → Wiped → Disposed / Returned
                                                                     ↓
                                                            Spares Pool (if reusable)
```
```bash
# Apply tags to all EC2 instances in a group (AWS)
aws ec2 create-tags \
  --resources <instance-id-1> <instance-id-2> \
  --tags Key=Environment,Value=Production Key=Owner,Value=platform-team@example.com

# Azure — tag a resource group (applies to contained resources)
az group update -n <rg-name> --tags Environment=Production Owner="platform-team@example.com"
```

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```
