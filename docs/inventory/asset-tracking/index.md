# Asset Tracking

Track hardware and cloud resources from procurement through decommission to maintain accurate inventory and prevent orphaned costs.

```text
┌──────────┐  ┌──────────┐  ┌──────────────┐  ┌──────────────────┐  ┌──────────────┐
│ Discover │  │   Tag    │  │   Classify   │  │ Track Lifecycle  │  │ Decommission │
│          │  │          │  │              │  │                  │  │              │
│ Physical │  │ Name /   │  │ Prod/Dev/DR  │  │ In service →     │  │ Wipe → cert  │
│ scan or  │─►│ Owner /  │─►│ Tier / Role  │─►│ Maintenance →    │─►│ disposal /   │
│ cloud API│  │ Env / CC │  │ Criticality  │  │ Decom pending    │  │ return       │
└──────────┘  └──────────┘  └──────────────┘  └──────────────────┘  └──────────────┘
      │                                                 │
      │                                        ┌────────┘
      ▼                                        ▼
┌──────────────────┐                  ┌──────────────────┐
│  Asset Register  │                  │  CMDB CI Record                            │
│  (CMDB / ITSM)   │◄─────────────────│  linked to asset                           │
└──────────────────┘                  └──────────────────┘
```

## Asset Register — Key Attributes

| Attribute | Physical | Virtual / Cloud |
|---|---|---|
| Asset ID | Barcode / serial | Instance ID / resource ID |
| Asset type | Server / storage / switch | EC2 / VM / RDS / disk |
| Make / model | Dell PowerEdge R750 | t3.large / Standard_D4s_v5 |
| Location | Rack, row, DC | Region, AZ, resource group |
| Owner / team | Assigned team | Tag: Owner |
| Environment | Prod / Dev / DR | Tag: Environment |
| Purchase date | PO date | Created date |
| Warranty / support expiry | From vendor portal | Subscription / reserved instance expiry |
| Status | In service / decommissioned / spares | Running / stopped / terminated |
| CMDB CI link | CMDB record | CMDB record |

## Physical Asset Inventory

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

```powershell
# Windows — hardware inventory
Get-WmiObject Win32_ComputerSystem | Select-Object Manufacturer, Model, TotalPhysicalMemory
Get-WmiObject Win32_BIOS | Select-Object SerialNumber, Version
Get-WmiObject Win32_PhysicalMemory | Select-Object Capacity, Speed
Get-Disk | Select-Object Number, FriendlyName, SerialNumber, Size
```

## Cloud Asset Inventory

### AWS

```bash
# All EC2 instances
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].{ID:InstanceId,Type:InstanceType,State:State.Name,Name:Tags[?Key==`Name`].Value|[0],Launched:LaunchTime}' \
  --output table

# Untagged resources (no Owner tag — orphan risk)
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*] | [?!Tags[?Key==`Owner`]] | [*].{ID:InstanceId,State:State.Name}' \
  --output table

# Stopped instances older than 30 days
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=stopped" \
  --query 'Reservations[*].Instances[*].{ID:InstanceId,Name:Tags[?Key==`Name`].Value|[0],Launched:LaunchTime}' \
  --output table

# EBS volumes not attached
aws ec2 describe-volumes \
  --filters "Name=status,Values=available" \
  --query 'Volumes[*].{ID:VolumeId,Size:Size,Created:CreateTime,Type:VolumeType}' \
  --output table
```

### Azure

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

## Asset Lifecycle States

```text
Ordered → Received → Configured → In Service → Decommission Pending → Wiped → Disposed / Returned
                                                                     ↓
                                                            Spares Pool (if reusable)
```

## Tagging Standards

All cloud resources must have:

| Tag | Format | Example |
|---|---|---|
| `Name` | descriptive-name | `web-prod-01` |
| `Environment` | Production / Staging / Dev / DR | `Production` |
| `Owner` | team email | `platform-team@example.com` |
| `CostCenter` | finance code | `CC-1042` |
| `Project` | project name | `customer-portal` |

```bash
# Apply tags to all EC2 instances in a group (AWS)
aws ec2 create-tags \
  --resources <instance-id-1> <instance-id-2> \
  --tags Key=Environment,Value=Production Key=Owner,Value=platform-team@example.com

# Azure — tag a resource group (applies to contained resources)
az group update -n <rg-name> --tags Environment=Production Owner="platform-team@example.com"
```

## Asset Tracking Checklist

- [ ] All production servers have CI records in CMDB
- [ ] No untagged cloud resources (ownership unknown)
- [ ] Stopped/deallocated VMs reviewed — decommission or document reason for retention
- [ ] Unattached EBS volumes / managed disks reviewed and disposed of if orphaned
- [ ] Hardware warranty checked — no in-service hardware with expired warranty
- [ ] Decommissioned assets removed from monitoring and firewall rules
- [ ] Asset disposal completed with data-wipe certificate for decommissioned hardware
