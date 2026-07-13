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


```text title="Expected output"
Manufacturer: Dell Inc.
Product Name: PowerEdge R750
Serial Number: 1HSTK63
UUID: 4c4c4544-0048-5310-8054-b6c04f4b3633
Version: 2.16.0
Release Date: 12/15/2023
NAME SIZE VENDOR MODEL SERIAL ROTA
sda 1.8T SEAGATE ST1800MM0129 ZL84P5KH 0
sdb 1.8T SEAGATE ST1800MM0129 ZL84P5KG 0
nvme0n1 476.9G Samsung 990 PRO S7GUNG0T900123X 0
eth0:
eth1:
eth2:
lo:
Speed: 10000Mb/s
Duplex: Full
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `dmidecode: permission denied` | Run the command with `sudo` or as root user. |
    | `ethtool: No such device` | Replace `<interface>` with an actual interface name from the `ip link show` output (e.g., `eth0`). |
    | `smartctl: command not found` | Install smartmontools package with `sudo apt install smartmontools` (Debian/Ubuntu) or `sudo yum install smartmontools` (RHEL/CentOS). |
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
