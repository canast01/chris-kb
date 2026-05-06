# NAT & Load Balancing

> Part of the [NSX-T CLI Reference](../).

## NAT

NAT rules are configured on Tier-0 or Tier-1 gateways. CLI inspection runs on the Edge node.

```bash
# SSH to Edge node, enter the gateway VRF
vrf <lr_id>

# List all NAT rules
get nat rules

# NAT rule hit statistics
get nat rule stats

# SNAT translations active
get nat translations
```

### NAT Rule Output Fields

| Field | Meaning |
|---|---|
| Rule ID | Matches NSX Manager policy NAT rule ID |
| Type | `SNAT`, `DNAT`, `REFLEXIVE`, `NO_NAT` |
| Match Source | Source IP/prefix triggering this rule |
| Match Destination | Destination IP/prefix |
| Translated Address | Address substituted in the packet |
| Action | `SNAT` = rewrite source; `DNAT` = rewrite destination |

## Load Balancer

NSX-T load balancer runs on the Edge node. All commands below run in the Edge CLI (not VRF context).

```bash
# Overall load balancer status
get load-balancer status

# List virtual servers (VIPs)
get load-balancer virtual-servers

# Server pools and member state
get load-balancer pools

# Specific pool detail (member health)
get load-balancer pool <pool_id>

# Active connections per virtual server
get load-balancer virtual-server <vs_id> stats
```

### Load Balancer Status Values

| Status | Meaning |
|---|---|
| `UP` | All pool members healthy |
| `PARTIALLY_UP` | At least one member healthy |
| `DOWN` | No healthy members |
| `DISABLED` | Administratively disabled |
| `DETACHED` | Edge cluster assignment missing |

## Troubleshooting NAT

```bash
# Confirm rule exists for expected source
get nat rules | grep <source_ip>

# Check translation table for active SNAT flows
get nat translations | grep <internal_ip>

# Verify interface has correct uplink for NAT
get interfaces
```

## Troubleshooting Load Balancer

```bash
# Are pool members passing health checks?
get load-balancer pools

# Member is DOWN — check:
# 1. Security group / DFW allows health check port
# 2. Application listening on expected port
# 3. Pool monitor type matches application (HTTP vs TCP)

# Check Edge CPU — LB is Edge-hosted, CPU bound under high load
get service dataplane stats
```
