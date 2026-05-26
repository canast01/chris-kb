# NSX — Integrations

```
┌─────────────────────────────────── NSX Architecture — Integrations ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      NSX integrations: vCenter, Aria suite, Active Directory IDFW, and third-party tools      │   │
│   │           vCenter: registers NSX Manager as plugin; VM tag sync via Compute Manager           │   │
│   │         IDFW: AD group membership drives DFW rules per user; key for VDI environments         │   │
│   │         Aria Network Insight: flow-level visibility; Aria Operations: health and alert        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    vCenter sync → VM tagging → dynamic groups → DFW auto-update → policy enforcement                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         VMware Stack        │  │        Identity / AD        │  │         Third-Party         │   │
│   │       vCenter plug-in       │  │         LDAP/AD join        │  │          Partner LB         │   │
│   │         VM tag sync         │  │          IDFW rules         │  │         IDS/IPS feed        │   │
│   │       Aria Operations       │  │        User → VM map        │  │          ServiceNow         │   │
│   │       Aria Net.Insight      │  │         Group member        │  │      Ansible/Terraform      │   │
│   │         Tanzu / TKG         │  │         Policy auto         │  │         Panorama/FMC        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Compute Manager (vCenter) registration is prerequisite for VM-tag dynamic group policy             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Integration    │     Protocol     │    NSX feature    │     Benefit      │      Notes       │   │
│   │     vCenter      │     REST API     │      Tag sync     │   Dyn. groups    │    Comp. Mgr     │   │
│   │    AD / LDAP     │      LDAPS       │     IDFW rules    │  User-based FW   │     VDI use      │   │
│   │     Aria NI      │   Flow export    │     Visibility    │     Flow map     │   IPFIX parse    │   │
│   │    Terraform     │   NSX provider   │     IaC deploy    │  Repeatability   │   VCS pipeline   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: vCenter API access from NSX Manager · AD reachable via management network                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Compute Manager = vCenter registered in NSX Manager; source of VM inventory and tags               │
│    VM tag          = vSphere tag applied to VM; synced to NSX for dynamic group membership            │
│    Dynamic group   = NSX group whose membership auto-updates based on tag, OS, or name                │
│    IDFW            = Identity Firewall; maps AD user to VM for user-based DFW policy                  │
│    LDAP            = AD integration; NSX reads group membership to build IDFW mappings                │
│    Aria Net.Insight = VMware flow analytics; parses NSX IPFIX/sFlow; builds flow map                  │
│    Aria Operations = VMware monitoring; NSX plugin shows gateway health and DFW stats                 │
│    Tanzu / TKG     = Kubernetes integration; NSX provides pod networking via NCP plugin               │
│    NCP             = NSX Container Plugin; syncs K8s namespace/pod state to NSX segments              │
│    Terraform NSX   = VMware NSX Terraform provider; declare segments, rules, gateways as HCL          │
│    Partner LB      = Third-party LB (F5, Citrix) inserted into NSX via service chain                  │
│    Panorama/FMC    = Palo Alto/Cisco FMC; integrates with NSX for micro-seg enforcement               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```

Once registered, vCenter clusters appear under **System → Fabric → Hosts**. Use them to apply transport node profiles at cluster scope.

### Host Transport Node Profiles

A Transport Node Profile (TNP) captures the NSX configuration applied to every ESXi host in a cluster: which VDS/vSS uplinks carry TEP traffic, which Transport Zones are included, and which IP pool allocates TEP addresses.

```bash
# Apply a TNP to a cluster (prepares all hosts in the cluster as transport nodes)
# Via API — Policy endpoint
curl -sk -u 'admin:password' \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "host_profile_binding": {
      "transport_node_profile_id": "<tnp-id>"
    }
  }' \
  "https://<nsx-manager>/policy/api/v1/infra/sites/default/enforcement-points/default/clusters/<cluster-id>"
```

Monitor preparation progress: **System → Fabric → Hosts → Configuration** — each host shows `Success` when preparation is complete.

---

## VMware Cloud Foundation (VCF) Integration

In VCF deployments, NSX is deployed and lifecycle-managed by SDDC Manager. NSX is not configured directly — changes go through the SDDC Manager UI or API.

Key differences in VCF-managed NSX:

| Capability | Standalone NSX | VCF-Managed NSX |
|---|---|---|
| Upgrade orchestration | NSX LCM | SDDC Manager Bundle |
| Certificate management | NSX Manager CLI/API | SDDC Manager |
| Transport node profiles | Manual | SDDC Manager workflow |
| NSX Manager cluster sizing | Any | VCF-prescribed sizing |

Check SDDC Manager for pending NSX upgrades before performing direct NSX operations. VCF enforces version alignment between vCenter, NSX, and ESXi.

---

## Physical Underlay Requirements

NSX overlay traffic runs over the physical network. The underlay must meet specific requirements for Geneve encapsulation to function correctly.

### MTU Requirements

Geneve adds a 54-byte overhead to each packet. The underlay must support an MTU of at least **1600** on all paths between TEPs. Jumbo frames (MTU 9000) are recommended.

```bash
# Test MTU from an ESXi host TEP vmkernel — don't-fragment ping
vmkping -I vmk1 -d -s 1572 <remote-tep-ip>
# -s 1572 = 1600 (Geneve MTU) - 28 (IP+UDP headers)
# If this fails, the underlay MTU is insufficient
```

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
