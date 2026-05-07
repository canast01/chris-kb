# Subnetting
## CIDR Notation Reference

| CIDR | Subnet Mask | Hosts | Use Case |
|---|---|---|---|
| /30 | 255.255.255.252 | 2 | Point-to-point links |
| /29 | 255.255.255.248 | 6 | Small management segments |
| /28 | 255.255.255.240 | 14 | DMZ / small service zones |
| /27 | 255.255.255.224 | 30 | Medium service segments |
| /26 | 255.255.255.192 | 62 | Storage or server subnets |
| /25 | 255.255.255.128 | 126 | Mid-size server segments |
| /24 | 255.255.255.0 | 254 | Standard server / VLAN |
| /23 | 255.255.254.0 | 510 | Larger server segments |
| /22 | 255.255.252.0 | 1022 | Campus / large server zones |

## Calculate a Subnet

```bash
# Linux — ipcalc
ipcalc 10.10.10.0/24

# Python one-liner
python3 -c "import ipaddress; n = ipaddress.ip_network('10.10.10.0/24'); print(n.network_address, n.broadcast_address, n.num_addresses)"
```

## Find Subnet of a Given IP

```bash
ipcalc 10.10.10.45/24
# Returns: network, broadcast, first/last usable host
```

## Check if Two IPs Are in the Same Subnet

```bash
python3 -c "
import ipaddress
a = ipaddress.ip_address('10.10.10.45')
b = ipaddress.ip_address('10.10.10.200')
net = ipaddress.ip_network('10.10.10.0/24')
print(a in net, b in net)
"
```

## Reserved Addresses in Each Subnet

- **Network address** — first IP (e.g., 10.10.10.0)
- **Broadcast address** — last IP (e.g., 10.10.10.255)
- **Gateway** — typically .1 or .254 (convention, not mandatory)

## Common Infrastructure Subnets

| Network | Purpose | Notes |
|---|---|---|
| 10.x.x.0/24 | Server / production | Standard for most enterprise server VLANs |
| 10.x.x.0/24 | Storage (iSCSI/NFS) | Often on dedicated VLAN with jumbo frames |
| 10.x.x.0/24 | vMotion | Dedicated VLAN, high bandwidth |
| 10.x.x.0/24 | Backup | Often large subnet for media server access |
| 10.x.x.0/30 | Replication uplinks | Point-to-point between sites |

## Overlap Check

Before assigning a new subnet, verify it doesn't overlap with existing routes:

```bash
# Linux — show all routes
ip route show

# Check for overlap manually or with ipcalc
ipcalc <new_network>/<prefix>
```
