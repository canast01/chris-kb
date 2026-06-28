---
tags:
  - architecture
  - nsx
  - nsx-4
  - vmware
---
# NSX — Integrations


<div class="kb-summary">
Integrations reference covering Host Transport Node Profiles, VMware Cloud Foundation (VCF) Integration, Physical Underlay Requirements, BGP Integration with Physical Network, Active Directory / LDAP Integration and 2 more sections.

*Applies to: NSX-T 3.x · NSX 4.x*
</div>
![NSX — Integrations](../../../../assets/virtualization-vmware-nsx-architecture-integrations.svg)




```d2
direction: right

center: "NSX-T" {shape: hexagon}
physical_network_integration: "Physical Network Integration" {shape: rectangle}
bgp_integration_with_physical_networ: "BGP Integration with Physical Network" {shape: rectangle}
active_directory_ldap_integration: "Active Directory / LDAP Integration" {shape: rectangle}
vsphere_distributed_switch_vds_integ: "vSphere Distributed Switch (vDS) Integration" {shape: rectangle}
log_forwarding_to_siem: "Log Forwarding to SIEM" {shape: rectangle}

center -> physical_network_integration
center -> bgp_integration_with_physical_networ
center -> active_directory_ldap_integration
center -> vsphere_distributed_switch_vds_integ
center -> log_forwarding_to_siem
```

## Physical Network Integration

### VLAN Requirements

| Traffic Type | VLAN | MTU Requirement |
|---|---|---|
| TEP (overlay encap) | Dedicated VLAN | 1600 minimum, 9000 preferred |
| NSX Manager management | Management VLAN | 1500 standard |
| Edge uplinks (BGP) | Transit VLAN(s) | 1500 minimum |
| Edge TEP | Edge TEP VLAN | 1600 minimum |

### Routing Requirements

Physical routers must be reachable from Edge node uplink interfaces for BGP peering. The Edge VM's uplink interfaces (fp-eth0, fp-eth1) connect directly to the physical VDS portgroup in the transit VLAN.

---

## BGP Integration with Physical Network

Tier-0 gateways peer with physical routers via eBGP (typically) or iBGP. The Edge nodes host the BGP sessions and exchange routes with the physical fabric.

### Standard BGP Design

```text
Physical Router (AS 65000)
    |  eBGP
Edge Node Active (T0 Uplink)
Edge Node Standby (T0 Uplink)
```

**Route advertisement**: The Tier-0 gateway advertises connected routes (NSX overlay prefixes) to the physical router. The physical router announces a default route or specific external prefixes back to NSX.

### BGP Configuration via Policy API

```bash
# Create BGP neighbor on a Tier-0 gateway
curl -sk -u 'admin:password' \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
    "resource_type": "BgpNeighborConfig",
    "display_name": "ToR-Switch-01",
    "neighbor_address": "10.0.0.1",
    "remote_as_num": "65000",
    "password": "bgp-auth-key"
  }' \
  "https://<nsx-manager>/policy/api/v1/infra/tier-0s/<t0-id>/locale-services/default/bgp/neighbors/tor-switch-01"
```

Verify BGP state from Edge CLI:

```bash
# SSH to Edge node
vrf <tier0-vrf-id>
get bgp neighbor summary
# Expected: all peers in Established state

get bgp neighbor 10.0.0.1 routes
get bgp neighbor 10.0.0.1 advertised-routes
```

---

## Active Directory / LDAP Integration

NSX-T supports LDAP (Active Directory or OpenLDAP) for user authentication. LDAP users can be assigned NSX roles, eliminating the need for local admin accounts.

### Configure LDAP Identity Source

**System → Users and Roles → LDAP → Add**

| Field | Example |
|---|---|
| Name | corp-ad |
| LDAP Protocol | LDAPS (port 636) — recommended |
| Hostname | ldap.example.local |
| Base DN | DC=corp,DC=local |
| Bind DN | CN=nsxbind,OU=ServiceAccounts,DC=corp,DC=local |
| Bind Password | (service account password) |

Test connectivity before saving. NSX will validate the bind DN and base DN.

### Verify LDAP Integration via API

```bash
# List configured identity sources
curl -sk -u 'admin:password' \
  https://<nsx-manager>/api/v1/aaa/vidm/status

# Test LDAP search
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"search_query": "nsxadmin", "cursor": "0"}' \
  "https://<nsx-manager>/api/v1/aaa/ldap/search"
```

### Assign Roles to AD Groups

**System → Users and Roles → Role Assignments → Add**

| Setting | Value |
|---|---|
| Name | CN=NSX-Admins,OU=Groups,DC=corp,DC=local |
| Identity Source | corp-ad |
| Role | Enterprise Admin |

| NSX Role | Permissions |
|---|---|
| Enterprise Admin | Full read/write; equivalent to admin |
| Operator | Read-only with some operational actions (reset stats, force failover) |
| Security Admin | DFW policy read/write; no infrastructure access |
| Auditor | Read-only |
| Network Engineer | Networking read/write; no security policy access |

---

## vSphere Distributed Switch (vDS) Integration

NSX overlays ESXi host networking by attaching TEP traffic to a vDS uplink. The VDS must be created in vCenter before NSX fabric preparation.

### Requirements

- vDS version 6.6+ for NSX 3.x; vDS 7.0+ for NSX 4.x
- At least one dedicated VLAN-backed portgroup for TEP traffic
- N-VDS (NSX Virtual Distributed Switch) is deprecated in NSX 4.x; vDS is the standard

### Verify vDS Port Binding on ESXi Host

```bash
# On ESXi host (SSH or shell)
# List all VDS attached to the host
esxcli network vswitch dvs vmware list

# List uplinks and their VDS mappings
esxcli network vswitch dvs vmware list | grep -A5 "Uplinks"

# Verify TEP vmkernel adapter is on vDS
esxcli network ip interface list | grep vmk

# Check TEP IP is assigned
esxcli network ip interface ipv4 get
```

---

## Log Forwarding to SIEM

NSX components forward syslog via the NSX Manager CLI or API:

```bash
# Add syslog target on NSX Manager
nsxcli
set service syslog exporter siem-01 level info protocol TLS server 10.0.0.100 port 6514

# Verify
get service syslog exporters

# Add syslog on Edge node (SSH to Edge)
set service syslog exporter siem-01 level info protocol UDP server 10.0.0.100 port 514
```

Key log sources to forward:

| Source | Path / Method | Content |
|---|---|---|
| NSX Manager | `set service syslog exporter` | API audit, policy changes, alarms |
| Edge Node | Same CLI command on each Edge | BGP events, NAT, LB pool changes |
| ESXi DFW | ESXi host syslog with DFW tag | Firewall rule hits, drops |
| NSX Manager audit | `/var/log/vmware/nsx-manager/audit.log` | Admin actions, role changes |

## See also

- [NSX — How It Works](how-it-works/)
- [NSX — Deploy](../deploy/)
