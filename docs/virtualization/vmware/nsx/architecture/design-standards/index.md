# NSX — Design Standards

```text
┌───────────────────────────────── NSX Architecture — Design Standards ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       NSX design standards: transport zones, T0/T1 gateway tiers, Edge sizing, IP pools       │   │
│   │       Two transport zones: VLAN TZ (N-S Edge uplinks) + Overlay TZ (E-W tenant segments)      │   │
│   │          T0 per environment (provider); T1 per tenant or application group (consumer)         │   │
│   │        Edge clusters: min 2 Edge Nodes for HA; bare-metal for high-throughput workloads       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Transport Zone design → Gateway tier → Edge cluster → IP pool → segment naming                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Transport Zones       │  │        Gateway Design       │  │         Edge Sizing         │   │
│   │          Overlay TZ         │  │         T0: provider        │  │         Small: 2vCPU        │   │
│   │           VLAN TZ           │  │        T1: per tenant       │  │        Medium: 4vCPU        │   │
│   │         No cross-TZ         │  │         T0 BGP ECMP         │  │         Large: 8vCPU        │   │
│   │        Host TZ attach       │  │        T1 static/OSPF       │  │        Bare-metal max       │   │
│   │        Multi-TZ Edge        │  │         NAT on T1 SR        │  │        Min 2 per site       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    TEP pool: /24 minimum; no overlap with VM or management networks; MTU 1600+ on pNIC                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Design area    │     Standard     │        Why        │      Verify      │      Notes       │   │
│   │     TEP pool     │ /24 non-overlap  │     No routing    │    Ping TEPs     │     MTU 1600     │   │
│   │     Edge HA      │   2 nodes min    │    SR failover    │    BFD state     │    A/S or A/A    │   │
│   │    T0 uplinks    │    2 per Edge    │     ECMP / HA     │    BGP peers     │     VLAN TZ      │   │
│   │    Seg naming    │   <env>-<app>    │    Readability    │      Audit       │    No spaces     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: pNIC MTU ≥ 1600 for Geneve · dedicated TEP VLAN · ToR BGP peer config                    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Overlay TZ    = Transport Zone spanning all hosts; carries Geneve-encapsulated E-W traffic         │
│    VLAN TZ       = Transport Zone for Edge uplinks; carries native VLAN traffic to physical           │
│    TEP pool      = IP pool assigned to hosts for Geneve src/dst; one IP per host TEP vmknic           │
│    T0 gateway    = Provider Logical Router; BGP to physical; ECMP over multiple Edge uplinks          │
│    T1 gateway    = Tenant Logical Router; connects segments upstream to T0                            │
│    Edge cluster  = Group of Edge Nodes hosting Service Routers; provides N-S HA                       │
│    BFD           = Bidirectional Forwarding Detection; fast failover between Edge uplinks             │
│    ECMP          = Equal-Cost Multi-Path; distributes N-S traffic across multiple Edge uplinks        │
│    Active/Standby = SR runs on one Edge; fails to standby if primary fails                            │
│    Active/Active  = Two SRs active; stateless traffic only; requires external LB for SPI              │
│    MTU 1600      = Minimum pNIC MTU for Geneve (50-byte overhead) + standard 1500 payload             │
│    Seg naming    = Consistent segment naming prevents confusion in large environments                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

The three-node NSX Manager cluster uses sequential numbering. Site codes should match vCenter and ESXi naming (`lon` for London, `ams` for Amsterdam, etc.).

### Segments (Logical Switches)

```text
Format: seg-<environment>-<function>-<vlan_or_subnet>
Example: seg-prod-web-10.0.1.0
         seg-dev-db-10.1.3.0
         seg-mgmt-vmotion-10.100.2.0
```

VLAN-backed segments (for management or underlay traffic) should include the VLAN ID:

```text
Format: seg-vlan-<vlan_id>-<function>
Example: seg-vlan-100-management
         seg-vlan-200-tep
         seg-vlan-300-edge-uplink
```

### Transport Zones

```text
Format: tz-<type>-<scope>
Example: tz-overlay-compute
         tz-vlan-edge
         tz-overlay-edge
```

| Transport Zone | Type | Purpose |
|---|---|---|
| tz-overlay-compute | OVERLAY | All ESXi compute hosts — VM workload segments |
| tz-overlay-edge | OVERLAY | Edge nodes — carries T0/T1 overlay traffic |
| tz-vlan-edge | VLAN | Edge uplinks to physical routers |

### Tier-0 Gateways

```text
Format: t0-<site>-<function>
Example: t0-lon-prod
         t0-lon-dmz
         t0-ams-prod
```

Separate T0 gateways for production and DMZ allow independent routing table management and security policy.

### Tier-1 Gateways

```text
Format: t1-<environment>-<tenant_or_application>
Example: t1-prod-frontend
         t1-prod-database
         t1-dev-platform
```

Each T1 maps to a logical application boundary. A single T1 can connect multiple segments that share the same routing domain.

### Edge Nodes and Edge Clusters

```text
Format: edge-<site>-<nn>
         edge-cluster-<site>-<purpose>
Example: edge-lon-01, edge-lon-02
         edge-cluster-lon-prod
```

Edge nodes must be deployed in pairs for HA. The edge cluster contains the pair.

### DFW Policies and Rules

```text
DFW Category order (NSX-T built-in, top to bottom):
  Ethernet      — L2 rules
  Emergency     — Break-glass block rules
  Infrastructure — Management/monitoring allow rules
  Environment   — Inter-zone rules
  Application   — Application-specific micro-segmentation

Policy name format: <category>-<application>-<purpose>
Example: Application-Web-Tier
         Environment-PCI-Isolation
         Infrastructure-Monitoring-Allow

Rule name format: <action>-<source>-to-<dest>-<service>
Example: Allow-Web-to-App-HTTPS
         Deny-Dev-to-Prod-Any
         Allow-Monitoring-to-Any-SNMP
```

---

## Design Rules

### Overlay Network Design

1. **Dedicated TEP VLAN**: All ESXi hosts and Edge nodes must use a dedicated VLAN for TEP traffic. Never share the TEP VLAN with management or VM traffic.

2. **MTU**: TEP VLAN must carry MTU 9000 (jumbo frames) end-to-end. Verify from host to physical switch upstream. Minimum viable MTU is 1600 for Geneve overhead, but 9000 is required for vSAN on the same hosts.

3. **BFD**: Enable BFD on T0 uplinks to detect physical path failures within seconds. BFD minimum timers: 500ms interval, 3 multiplier.

4. **Route advertisement**: T1 gateways advertise `TIER1_CONNECTED` and `TIER1_STATIC` routes upward to T0. T0 redistributes these into BGP as type-2 EVPN or connected routes depending on underlay design.

5. **IP pools**: Use separate IP pools for ESXi host TEPs and Edge TEPs. Edge TEPs may need to be in a different subnet if on separate physical switches.

### Firewall Design

1. **Default deny**: Every DFW policy ends with a default-deny rule. The NSX built-in default rule (rule 65535) is `any-any-drop` — verify it has not been changed to `allow`.

2. **Use groups, not IPs**: All DFW rules must reference NSX security groups or segments — not raw IP addresses. IP-based rules break when VMs move to different hosts or subnets.

3. **Policy priority order**: Emergency rules at the top, Infrastructure (monitoring, backup, management) before Application rules. Application policies are the most numerous and most specific.

4. **Log critical rules**: Enable logging on deny rules in Application and Environment categories. DFW logs are forwarded via ESXi syslog.

5. **Scope rules to segments or groups**: Apply rules to the smallest possible scope. Rules scoped to `Applied To: DFW` affect all VMs — use only for truly global rules.

### Gateway Design

1. **Active/Standby for T0**: For simplicity and predictable failover, use `ACTIVE_STANDBY` HA mode on T0 gateways unless ECMP is required. ECMP requires `ACTIVE_ACTIVE` mode and equal-cost BGP paths.

2. **Edge cluster sizing**: Each Edge cluster needs a minimum of two nodes. Size based on throughput — a Large Edge VM supports ~100 Gbps; a Bare Metal Edge supports line-rate on 25/100G NICs.

3. **Separate Edge clusters for workloads**: Do not run production T0 and DMZ T0 on the same Edge cluster. Separate Edge clusters prevent a single failure from affecting multiple routing domains.

4. **T1 locality**: T1 gateways perform distributed routing on ESXi hosts — they do not require Edge nodes unless services (load balancing, NAT, VPN) are attached.

---

## Configuration Baselines

### NSX Manager Cluster

| Parameter | Recommended Value |
|---|---|
| Nodes | 3 (for production) |
| vCPU | 6 (medium) or 12 (large) |
| Memory | 24 GB (medium) or 48 GB (large) |
| Disk | 300 GB thin-provisioned |
| NTP sources | At least 2, matching vCenter NTP |
| Backup schedule | Daily at off-peak time; retain 14 copies |
| Syslog | Configured to SIEM on TLS 6514 |

### Edge Node VM Sizing

| Workload | Form Factor | vCPU | Memory | Storage |
|---|---|---|---|---|
| L4 load balancing, NAT, VPN | Large VM | 8 | 32 GB | 200 GB |
| High-throughput north-south | Bare Metal | Physical | 256 GB | 400 GB |
| Lab / dev | Small VM | 2 | 8 GB | 200 GB |

Edge VMs must be on hosts that are **not** in the compute cluster — deploy on a dedicated management/edge cluster or on separate physical hosts.

### Transport Zone Scope

| Zone | Hosts Included | Segments Hosted |
|---|---|---|
| tz-overlay-compute | All vSphere cluster hosts | All VM workload segments |
| tz-overlay-edge | Edge nodes + compute hosts (same overlay) | Same as above |
| tz-vlan-edge | Edge nodes only | Uplink portgroups (physical router-facing) |

### IP Pool Assignments

| Pool | Subnet | Allocation |
|---|---|---|
| pool-tep-compute | 192.168.200.0/24 | ESXi host TEPs (one IP per host) |
| pool-tep-edge | 192.168.201.0/24 | Edge node TEPs (two IPs per Edge: internal + external) |
| pool-lb-vip | 10.0.50.0/24 | NSX load balancer VIPs |

---

## Version Compatibility Matrix

Always verify with the [VMware Product Interoperability Matrix](https://interopmatrix.broadcom.com) before upgrades.

| NSX Version | ESXi Minimum | vCenter Minimum | VCF Version |
|---|---|---|---|
| NSX 4.2.x | ESXi 7.0 U3 | vCenter 7.0 U3 | VCF 5.1 |
| NSX 4.1.x | ESXi 7.0 U2 | vCenter 7.0 U2 | VCF 5.0 |
| NSX 3.2.x | ESXi 7.0 U1 | vCenter 7.0 | VCF 4.4 |

**Key rule**: NSX Manager version must be equal to or greater than the ESXi host version. NSX cannot manage a higher ESXi version than itself.

### vDS Compatibility

| NSX Version | Minimum vDS Version |
|---|---|
| NSX 4.x | vDS 7.0 |
| NSX 3.x | vDS 6.6 |

N-VDS (NSX Virtual Distributed Switch) is deprecated from NSX 4.0 onward. Migrate N-VDS hosts to vDS before upgrading to NSX 4.x.

---

## Change Control Standards

| Change Type | Pre-Checks Required | Rollback Method |
|---|---|---|
| DFW rule add/modify | Backup NSX config; peer review rule; test in lower environment | Delete or revert rule in DFW policy |
| Segment add | Verify transport zone scope; IP pool availability | Delete segment (only if no ports attached) |
| T0 BGP neighbor add | Verify BGP ASN and password with network team; check underlay connectivity | Remove neighbor from T0 locale-service |
| Edge cluster modification | Confirm active service dependencies; no active VPN/LB sessions | Restore prior Edge cluster membership |
| Transport node upgrade | NSX backup current; all TN healthy; maintenance window confirmed | Not supported in-place; must restore from backup |
| NSX Manager upgrade | Full backup to SFTP; vCenter and ESXi compatibility verified | Restore from backup (NSX does not support downgrade) |

All NSX configuration changes must be captured in the backup immediately after completion:

```bash
# Trigger immediate backup via API
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{}' \
  "https://<nsx-manager>/api/v1/node/backups/create"
```
