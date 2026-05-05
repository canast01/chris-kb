# VMware Network Inventory

| Field | Example |
|---|---|
| vSwitch or DVS Name | vDS-prod-01 |
| Port Group Name | pg-prod-app-vlan100 |
| VLAN ID | 100 |
| MTU | 1500 or 9000 |
| Uplink Mapping | vmnic0, vmnic1 |
| VMkernel Adapters | vmk0 (mgmt), vmk1 (vMotion), vmk2 (vSAN) |
| vMotion Network | VLAN 200, vmk1 |
| Management Network | VLAN 10, vmk0 |
| vSAN Network | VLAN 300, vmk2 |
| NSX Segment Mapping | seg-prod-app-01 maps to VLAN 100 |
| NIC Teaming Policy | Load-based or Active/Standby |
| Notes | Any exceptions or non-standard config |
