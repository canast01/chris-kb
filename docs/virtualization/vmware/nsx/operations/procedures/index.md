```bash
# Via API — create a group by tag
curl -sk -u 'admin:password' \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "sg-web-tier",
    "expression": [{
      "resource_type": "Condition",
      "member_type": "VirtualMachine",
      "key": "Tag",
      "operator": "EQUALS",
      "value": "web-tier"
    }]
  }' \
  "https://<nsx-manager>/policy/api/v1/infra/domains/default/groups/sg-web-tier"
```

```text
┌────────────────────────────────────── NSX — Standard Procedures ──────────────────────────────────────┐
│                                                                                                       │
│  Segment creation, T0/T1 gateway config, DFW rule changes, and change control.                        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Add New Segment                │  │              T1 Gateway Config              │   │
│   │        Policy > Networking > Segments        │  │                Add T1 gateway               │   │
│   │           Set VNI / transport zone           │  │              Link to T0 gateway             │   │
│   │           Set VLAN or overlay mode           │  │             Advertise connected             │   │
│   │            Connect to T1 gateway             │  │               Set edge cluster              │   │
│   │          Attach segment to VM vNIC           │  │            Apply DNS/DHCP profile           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Network change → DFW policy update → change control record → verify.                                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               DFW Rule Changes               │  │              Change Management              │   │
│   │            Add to security policy            │  │            Raise CR before change           │   │
│   │          Define source/dest groups           │  │           Pre-change packet trace           │   │
│   │           Set service (port/proto)           │  │             Change window agreed            │   │
│   │            Publish policy changes            │  │           Post-change connectivity          │   │
│   │             Verify in traceflow              │  │            Close CR with evidence           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  NSX Manager VMs, Edge VMs, ESXi hosts, ToR switches, vCenter, management net                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Segment     = logical L2 overlay network; mapped to a transport zone                                 │
│  VNI         = VXLAN Network ID; unique per segment in overlay                                        │
│  Transport zone = scope of overlay or VLAN segment reachability                                       │
│  T1 gateway  = distributed L3 gateway; service router on edge cluster                                 │
│  T0 gateway  = north-south routing gateway; BGP peers with fabric                                     │
│  DFW         = Distributed Firewall; L4 stateful firewall per vNIC                                    │
│  Security policy = DFW container grouping rules by purpose                                            │
│  Groups      = NSX dynamic member sets (tag, OS, name, IP criteria)                                   │
│  Traceflow   = NSX UI tool; injects synthetic packet to trace path/drops                              │
│  Publish     = NSX action; commits policy changes to dataplane                                        │
│  Packet trace= captures before change; confirms expected traffic flow                                 │
│  CR          = Change Request; ITSM record authorising change                                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
curl -v https://<dest-vm-ip>/
# Or: telnet <dest-vm-ip> 443
```
```bash
curl -sk -u 'admin:password' \
  -X DELETE \
  "https://<nsx-manager>/policy/api/v1/infra/domains/default/security-policies/<policy-id>/rules/<rule-id>"
```
```powershell
# PowerCLI — assign NSX tag to a VM
$vm = Get-VM "app-server-01"
New-TagAssignment -Tag (Get-Tag -Name "app-tier") -Entity $vm
```
```bash
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": "<vm-moref-id>",
    "tags": [{"scope": "tier", "tag": "app"}]
  }' \
  "https://<nsx-manager>/api/v1/fabric/virtual-machines?action=update_tags"
```
```bash
curl -sk -u 'admin:password' \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "seg-prod-app",
    "transport_zone_path": "/infra/sites/default/enforcement-points/default/transport-zones/tz-overlay-compute",
    "connectivity_path": "/infra/tier-1s/t1-prod-frontend",
    "subnets": [{
      "gateway_address": "10.0.2.1/24"
    }],
    "admin_state": "UP"
  }' \
  "https://<nsx-manager>/policy/api/v1/infra/segments/seg-prod-app"
```
```bash
nsxcli
get logical-switches | grep seg-prod-app
get logical-switch <id> status
# Expected: Admin State: UP  Operational Status: UP
```
```bash
get logical-switch <id> | grep VNI
```
```bash
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/logical-ports?logical_switch_id=<segment-id>&attachment_type=VIF"
```
```bash
curl -sk -u 'admin:password' \
  -X DELETE \
  "https://<nsx-manager>/policy/api/v1/infra/segments/seg-prod-app"
```
```bash
# SSH to the currently STANDBY Edge node (check with: get edge-cluster status)
set edge-cluster failover
# The standby becomes active; the previously active Edge becomes standby
# BGP reconverges — typically within 10–30 seconds with BFD

# Verify new state
get edge-cluster status
get bgp neighbor summary
```
```bash
# Via Policy API
curl -sk -u 'admin:password' \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "ToR-02",
    "neighbor_address": "10.0.0.5",
    "remote_as_num": "65000",
    "bfd_config": {
      "enabled": true,
      "interval": 500,
      "multiple": 3
    },
    "password": "bgp-md5-key"
  }' \
  "https://<nsx-manager>/policy/api/v1/infra/tier-0s/<t0-id>/locale-services/default/bgp/neighbors/tor-02"
```
```bash
vrf <tier0-vrf>
get bgp neighbor summary | grep 10.0.0.5
# State should be Established
```
```bash
# Verify existing route advertisement config
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/policy/api/v1/infra/tier-1s/<t1-id>/route-advertisement"

# Enable TIER1_CONNECTED if not already set
curl -sk -u 'admin:password' \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
    "enabled": true,
    "advertise_connected": true
  }' \
  "https://<nsx-manager>/policy/api/v1/infra/tier-1s/<t1-id>/route-advertisement"
```
```bash
# Step 1 — Confirm no VMs remain on the host
vim-cmd vmsvc/getallvms   # run on the host — should show empty or powered-off VMs only

# Step 2 — Put host in maintenance mode in vCenter (DRS migrates VMs)

# Step 3 — Remove transport node via API
curl -sk -u 'admin:password' \
  -X DELETE \
  "https://<nsx-manager>/api/v1/transport-nodes/<tn-id>"

# Step 4 — Verify removal
nsxcli
get transport-nodes | grep <hostname>
# Should no longer appear
```
```bash
# Check state
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/transport-nodes/<tn-id>/state"

# Trigger re-sync
curl -sk -u 'admin:password' \
  -X POST \
  "https://<nsx-manager>/api/v1/transport-nodes/<tn-id>?action=restore_cluster_config"
```
```bash
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "allocation_id": "manual-host-01"
  }' \
  "https://<nsx-manager>/api/v1/pools/ip-pools/<pool-id>/ip-allocations"
```
```bash
curl -sk -u 'admin:password' \
  -X DELETE \
  "https://<nsx-manager>/api/v1/pools/ip-pools/<pool-id>/ip-allocations/<allocation-id>"
```
```bash
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/pools/ip-pools/<pool-id>" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for s in d.get('subnets', []):
    total = s.get('total_ips', 0)
    free = s.get('free_ips', 0)
    used = total - free
    print(f'Subnet: {s[\"cidr\"]}  Total: {total}  Used: {used}  Free: {free}')
"
```
