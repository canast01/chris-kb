# Asset Tracking


<div class="kb-summary">
Track hardware and cloud resources from procurement through decommission to maintain accurate inventory and prevent orphaned costs.
</div>

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
```text
┌───────────────────────────────────── Inventory — Asset Tracking ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Hardware asset register: serial number, rack location, owner, function, lifecycle state    │   │
│   │        Update register at: receipt, rack/decommission, ownership change, support change       │   │
│   │     Audit: reconcile physical assets against register quarterly; investigate discrepancies    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Register Attributes              │  │               Lifecycle States              │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │            Hostname + IP address             │  │              Ordered: PO raised             │   │
│   │            Serial number + model             │  │          In use: active production          │   │
│   │            Rack / rack unit / DC             │  │            Maintenance: in repair           │   │
│   │             Owner + cost centre              │  │            EOL: past support end            │   │
│   │             Support contract ref             │  │           Decommissioned: retired           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   │      Field       │     Example      │  Source of truth  │   Updated when   │      Owner       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │      Serial      │    SVC-12345X    │    Vendor label   │    On receipt    │    Asset team    │   │
│   │     Rack loc     │   DC1-A01-U14    │     DCIM tool     │    On install    │      DC ops      │   │
│   │    Lifecycle     │    Active/EOL    │  CMDB + register  │    On change     │    Asset team    │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    DCIM         = Data Centre Infrastructure Management tool; tracks rack/power/cooling               │
│    Rack unit    = 1U = 44.45 mm height; standard measure for data centre rack space                   │
│    Cost centre  = Finance code; determines which team is billed for the asset                         │
│    Asset audit  = Physical reconciliation of assets against register; finds ghost/missing assets      │
│    Ghost asset  = Asset in register that no longer physically exists; arises from poor process        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
