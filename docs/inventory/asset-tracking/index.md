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
