---
title: vSphere Networking
tags:
  - internals
  - vmware
---

# vSphere Networking — VSS, VDS, VMkernel, and NIOC

<div class="kb-summary">
Comprehensive reference for vSphere networking. Covers the architecture differences between Standard Switches and Distributed Switches, VMkernel adapter types and purposes, networking policies, Network I/O Control (NIOC), VLAN configuration including Private VLANs, multiple TCP/IP stacks, and topology best practices for production environments.

*Applies to: vSphere 7.x / 8.x*
</div>

---

```d2
direction: down

standard_switch_vss_vs_distributed_s: "Standard Switch (VSS) vs Distributed Switch (VDS)" {shape: rectangle}
vmkernel_adapters: "VMkernel Adapters" {shape: rectangle}
networking_policies: "Networking Policies" {shape: rectangle}
network_io_control_nioc: "Network I/O Control (NIOC)" {shape: rectangle}
port_groups_and_vlans: "Port Groups and VLANs" {shape: rectangle}
multiple_tcpip_stacks: "Multiple TCP/IP Stacks" {shape: rectangle}

standard_switch_vss_vs_distributed_s -> vmkernel_adapters: uses
vmkernel_adapters -> networking_policies: uses
networking_policies -> network_io_control_nioc: uses
network_io_control_nioc -> port_groups_and_vlans: uses
port_groups_and_vlans -> multiple_tcpip_stacks: uses
```

## Standard Switch (VSS) vs Distributed Switch (VDS)

A **vSphere Standard Switch (VSS)** is configured per ESXi host. Each host maintains its own switch configuration independently. A **vSphere Distributed Switch (VDS)** is managed centrally from vCenter and spans multiple hosts — the configuration is consistent across all member hosts.

| Feature | VSS | VDS |
|---|---|---|
| Configuration scope | Per-host | Per-vCenter (cluster-wide) |
| Port group consistency | Manual — must configure on each host | Automatic — defined once, applied everywhere |
| Requires vCenter | No — functions without vCenter | Yes — requires vCenter for config changes |
| Traffic monitoring (RSPAN/ERSPAN) | No | Yes — NetFlow and port mirroring |
| Network I/O Control (NIOC) | No | Yes |
| Private VLANs (PVLAN) | No | Yes |
| Port binding types | Ephemeral only | Static, Dynamic, Ephemeral |
| Link Aggregation (LACP) | No | Yes (Enhanced LACP) |
| Health check for uplinks | No | Yes (VLAN/MTU health check) |
| Licensing requirement | Included with all vSphere | Requires vSphere Enterprise Plus (or VCF) |
| Network Rollback | No | Yes |
| Uplink ports max | 32 | 32 |

**When to use VSS:** Small environments with no vCenter redundancy requirements, edge sites, standalone ESXi hosts that need minimal networking, or as a fallback management switch when vCenter is unavailable.

**When to use VDS:** Any production cluster where operational consistency matters. VDS eliminates configuration drift between hosts and enables advanced capabilities (NIOC, port mirroring, LACP, PVLAN) that VSS cannot provide.

### Migrating VSS to VDS

Migration moves hosts from a VSS to an existing VDS without dropping connectivity. The general workflow:

```bash
# From vCenter UI: Networking → Right-click VDS → Add and Manage Hosts
# CLI equivalent using esxcli to verify port group associations before migration
esxcli network vswitch standard list
esxcli network vswitch dvs vmware list

# Verify vmkernel assignments before migrating
esxcli network ip interface list

# After migration, confirm vmk interfaces are on VDS portgroups
esxcli network ip interface list | grep -E "Name|Portset"
```


```text title="Expected output"
Name: vSwitch0
Num Ports: 128
Used Ports: 6
Configured Ports: 128
MTU: 1500
CDP Status: listen
Beacon Enabled: false

Name: vSwitch1
Num Ports: 256
Used Ports: 12
Configured Ports: 256
MTU: 1500
CDP Status: unlisten
Beacon Enabled: false

DVS Name: VDS-Prod-01
DVS UUID: 50 2e 5f 5b 8c 4a 9f 2e-d1 3e 7c 9a 4b 6f 2d 8e
Num Hosts: 4
Num Ports: 512
Used Ports: 287

Name: vmk0
MAC Address: 00:50:56:a1:2f:4c
IPv4 Address: 192.168.1.50/24
IPv6 Address: fe80::250:56ff:fea1:2f4c/64
Enabled: true
Portset: vSwitch0

Name: vmk1
MAC Address: 00:50:56:a1:2f:4d
IPv4 Address: 10.20.30.100/24
IPv6 Address: fe80::250:56ff:fea1:2f4d/64
Enabled: true
Portset: vSwitch1

Name: vmk0
Portset: DPG-Management
Name: vmk1
Portset: DPG-vMotion
Name: vmk2
Portset: DPG-Storage
```

!!! warning "Common errors"
    **`Error: Unknown command or namespace network vswitch dvs vmware list`** — Use `esxcli network vswitch dvs list` instead (the `vmware` subcommand does not exist in standard esxcli).
    **`Error: Unable to connect to the ESX Server`** — Ensure SSH is enabled on the ESXi host and you have network connectivity; verify with `ping <esxi-hostname>` first.
    **`Error: The object has already been deleted or has not been completely created`** — Wait 30–60 seconds after VDS creation before running these commands, as the distributed switch may still be initializing.
Key consideration: always migrate the management VMkernel port (vmk0) last and ensure physical uplinks are available to the VDS before detaching them from the VSS.

> **VCP-DCV Exam Note:** VDS requires **vSphere Enterprise Plus** licensing. VSS is included with all vSphere editions. A VDS can be used even if vCenter becomes unavailable — hosts retain their last-known configuration, but you cannot make configuration changes until vCenter is restored.

---

## VMkernel Adapters

VMkernel (vmk) adapters are the host's own network interfaces — they are used for host-level traffic, not VM traffic. Each vmk adapter has an IP address and is bound to a specific port group or distributed port group.

| VMkernel Service | Purpose | Typical VLAN |
|---|---|---|
| **Management** | Host management, vCenter communication, SSH/DCUI | Dedicated MGMT VLAN |
| **vMotion** | Live migration traffic between hosts | Dedicated vMotion VLAN |
| **vSAN** | vSAN cluster storage traffic | Dedicated vSAN VLAN |
| **iSCSI** | iSCSI storage traffic (software iSCSI) | Dedicated iSCSI VLAN |
| **NFS** | NAS/NFS datastore traffic | Storage VLAN |
| **vSphere Replication** | Incoming replication data from source sites | Replication VLAN |
| **vSphere Replication NFC** | Outgoing replication data to target site | Replication VLAN |
| **Fault Tolerance (FT) Logging** | FT logging traffic between primary and secondary VMs | Dedicated FT VLAN |
| **Provisioning** | Cold migration, cloning, snapshot traffic | Can share vMotion VLAN |

### Adding a VMkernel Adapter

```bash
# Add a VMkernel port using esxcli
esxcli network ip interface add \
  --interface-name vmk1 \
  --portgroup-name "vMotion-PG"

# Set IP address on the new vmk
esxcli network ip interface ipv4 set \
  --interface-name vmk1 \
  --ipv4 192.168.10.11 \
  --netmask 255.255.255.0 \
  --type static

# Enable vMotion service on vmk1
esxcli vmotion network ip set --interface-name vmk1

# Verify the interface is up
esxcli network ip interface list
```


```text title="Expected output"
VMkernel interface vmk1 added successfully.
(no output — command completes silently)
(no output — command completes silently)
Name    Enabled  Connected  Netstack        IPV4 Address      IPV4 Netmask      IPV6 Address  MTU  MAC Address
------  -------  ---------  ---------------  ----------------  ----------------  -----------  ----  ------------------
vmk0    true     true       defaultTcpipStack 192.168.1.100     255.255.255.0              1500  00:50:56:c0:00:01
vmk1    true     true       defaultTcpipStack 192.168.10.11     255.255.255.0              1500  00:50:56:c0:00:02
vmk2    true     true       vmotion          192.168.20.50      255.255.255.0              1500  00:50:56:c0:00:03
```

!!! warning "Common errors"
    **`Error: The object or name is not valid.`** — Verify the portgroup "vMotion-PG" exists on the vSwitch using `esxcli network vswitch standard portgroup list`.
    **`Error: Could not set ipv4 config for vmk1`** — Ensure the VMkernel interface was successfully created and the IP address is not already in use on the network.
From the vCenter UI: **Host → Configure → Networking → VMkernel adapters → Add networking**.

> **VCP-DCV Exam Note:** A single VMkernel adapter can serve multiple services (e.g., management + vSphere Replication), but this is not recommended for production. vSAN and vMotion should always have dedicated vmk adapters on dedicated VLANs. FT Logging requires very low latency — it must be on its own vmk and ideally a dedicated NIC.

---

## Networking Policies

Networking policies are applied at the port group level (VSS) or distributed port group level (VDS) and define how traffic flows across uplinks.

### Load Balancing Algorithms

| Policy | Description | Requirement |
|---|---|---|
| **Route based on originating virtual port ID** | Default. Each VM is assigned to an uplink at connection time. Simple and low-overhead. | None — works with standard switch ports |
| **Route based on IP hash** | Uses source+destination IP to select uplink. Enables active-active use of all uplinks simultaneously. | Physical switch must have LACP or static EtherChannel configured |
| **Route based on source MAC hash** | Uses the VM's MAC address to select uplink. Slightly more balanced than port ID. | None |
| **Use explicit failover order** | Traffic always uses the first active uplink in the defined list. No true load balancing. | None |
| **Route based on physical NIC load** | VDS only. Dynamically reassigns VMs to less-loaded uplinks when utilization exceeds threshold. | VDS required |

> **VCP-DCV Exam Note:** **IP hash requires EtherChannel (LACP or static)** on the physical switch. If you enable IP hash without EtherChannel, you get unpredictable behavior or duplicate traffic. The **Route based on originating virtual port ID** policy is the default and works without any physical switch configuration. Exam questions often test whether you know that IP hash is the only policy that truly uses all uplinks simultaneously — but only when the physical switch cooperates.

### Failover Detection

| Method | How It Works | When to Use |
|---|---|---|
| **Link State Only** | Detects uplink failure only when the physical link goes down (layer 1 failure). | Simple environments, direct-attach scenarios |
| **Beacon Probing** | ESXi sends beacon frames out all uplinks and expects to receive them on other uplinks. Detects failures that link state cannot (e.g., upstream switch failure with port still "up"). | Any environment where layer 2 failures can occur without link drop |

> **VCP-DCV Exam Note:** **Beacon probing** is the more comprehensive detection method — it can detect upstream switch or cable failures that do not cause a physical link drop. However, beacon probing requires **at least three uplinks** to work correctly (to avoid false positives). Link state only is simpler but misses "silent failure" scenarios.

### Other Policy Settings

- **Notify switches:** When a VM is powered on or vMotioned, ESXi sends a gratuitous ARP to notify upstream switches to update their MAC tables. Should be **enabled** for all environments.
- **Rolling failback policy:** When a failed uplink recovers, ESXi waits before moving traffic back. This prevents flapping. **Failback: Yes** is the default (immediately failback); set to **No** to use rolling behavior.

---

## Network I/O Control (NIOC)

Network I/O Control (NIOC) is a VDS-only feature that allocates bandwidth across different traffic types sharing the same physical uplinks. Without NIOC, a sudden burst of VM traffic could saturate an uplink and starve vSAN or vMotion traffic.

NIOC works by assigning **shares** and optional **limits** to each system traffic type. Shares are relative — they only matter when the uplink is congested.

### System Traffic Types

| Traffic Type | Default Shares | Notes |
|---|---|---|
| Virtual machine traffic | 100 | User VMs — typically the highest volume |
| vMotion | 50 | Live migration traffic |
| vSAN | 50 | Storage cluster traffic — critical for vSAN health |
| Management | 50 | Host management plane |
| iSCSI | 50 | Software iSCSI |
| NFS | 50 | NAS storage |
| vSphere Data Protection | 50 | Backup traffic |
| Fault Tolerance | 50 | FT logging — very latency-sensitive |
| vSphere Replication | 50 | Site Replication Manager traffic |

> **VCP-DCV Exam Note:** NIOC traffic types that appear on exams: **vMotion, vSAN, FT Logging, Management, and VM Traffic**. Know that NIOC is a **VDS-only** feature — VSS has no equivalent. Shares are weighted allocations during contention, not hard reservations. A **bandwidth limit** (Mbps) hard-caps a traffic type regardless of available capacity.

### Configuring NIOC

```bash
# NIOC is configured from vCenter UI:
# VDS → Configure → Resource Allocation → System Traffic

# PowerCLI — set vMotion shares to High (100)
Get-VDSwitch "VDS-Production" | Get-VDTrafficShapingPolicy -Direction Ingress
# Use Set-VDUplinkTeamingPolicy or Set-VDPortgroup for policy updates

# Check current NIOC version on VDS
Get-VDSwitch "VDS-Production" | Select Name, Version, NumUplinkPorts
```


```text title="Expected output"
Name              Direction AverageBandwidth PeakBandwidth BurstSize Enabled
----              --------- ---------------- ------------- --------- -------
System Traffic    Ingress   Unlimited        Unlimited     Unlimited    True
vMotion           Ingress   Unlimited        Unlimited     Unlimited    True
Fault Tolerance   Ingress   Unlimited        Unlimited     Unlimited    True
Management        Ingress   Unlimited        Unlimited     Unlimited    True

Name                Version NumUplinkPorts
----                ------- --------------
VDS-Production      7.0.0   4
```

!!! warning "Common errors"
    **`Get-VDSwitch : The object 'VDS-Production' could not be found on the specified Folder, Datacenter or ResourcePool.`** — Verify the VDS name matches exactly and you are connected to the correct vCenter server with `Connect-VIServer`.
    **`You do not have permission to perform this operation.`** — Ensure your vCenter account has Administrator role or equivalent Network Administrator privileges on the VDS object.
---

## Port Groups and VLANs

### VLAN Configuration Modes

| Mode | VLAN ID Setting | Behavior |
|---|---|---|
| **No VLAN (External)** | 0 | No VLAN tagging. The physical switch port must be an access port. |
| **VLAN** | 1–4094 | ESXi tags frames with the specified VLAN ID (802.1Q). Physical switch port must be a trunk. |
| **VLAN Trunking (VGT)** | 4095 | Guest OS handles VLAN tagging. Used for VMs that need direct VLAN control. Physical switch must be a trunk. |

### Private VLANs (PVLAN)

PVLANs allow layer-2 isolation within the same VLAN. Only available on VDS. Three port types:

| PVLAN Type | Can Communicate With |
|---|---|
| **Promiscuous** | All PVLAN ports (isolated and community). Used for gateway/firewall VMs. |
| **Isolated** | Promiscuous only. Cannot communicate with any other isolated or community port — maximum isolation. |
| **Community** | Other ports in the same community, plus promiscuous. Cannot reach isolated ports or other communities. |

**Use case:** A multi-tenant DMZ where VMs in the same VLAN must not reach each other. Promiscuous port = firewall VM. Isolated ports = individual tenant VMs. Community ports = a group of VMs that can talk to each other but not to other groups.

> **VCP-DCV Exam Note:** Know all three PVLAN types and their communication rules. **Isolated ports can only reach promiscuous ports** — they cannot reach each other even within the same PVLAN. Community ports can reach each other AND promiscuous. PVLAN requires VDS — VSS does not support it. The exam may present a scenario and ask which PVLAN type provides the required isolation.

---

## Multiple TCP/IP Stacks

By default, all VMkernel traffic shares a single TCP/IP stack with a single default gateway and routing table. Multiple TCP/IP stacks allow certain traffic types to use a **separate routing table and default gateway**.

| Stack | Traffic | Use Case |
|---|---|---|
| **Default** | Management, storage (iSCSI/NFS), FT logging | Standard host traffic |
| **vMotion** | vMotion only | Separate gateway for vMotion network |
| **Provisioning** | Cold migration, cloning, snapshots | Isolate provisioning traffic routing |
| **Custom** | User-defined | Advanced routing scenarios |

```bash
# List TCP/IP stacks on a host
esxcli network ip netstack list

# Add a VMkernel to the vMotion TCP/IP stack
esxcli network ip interface add \
  --interface-name vmk2 \
  --portgroup-name "vMotion-PG" \
  --netstack vmotion

# Set the default gateway for the vMotion stack
esxcli network ip route ipv4 add \
  --netstack vmotion \
  --network default \
  --gateway 192.168.20.1
```


```text title="Expected output"
Name            State    Default Route
defaultTcpipStack  active  true
vmotion         active  false
vxlan           active  false

(no output — command completes silently)

(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: The object or item referenced could not be found.`** — Verify the portgroup name exists with `esxcli network vswitch standard portgroup list` and use the exact name.
    **`Error: The specified virtual NIC is already bound to a netstack.`** — Remove the interface from its current stack first using `esxcli network ip interface remove --interface-name vmk2`.
**Why they exist:** Without separate stacks, vMotion and the management interface share the same routing table. If management is on 192.168.1.0/24 and vMotion is on 10.10.10.0/24, you need a route for both — but only one default gateway. Separate stacks eliminate this routing conflict by giving vMotion its own gateway.

---

## Network Topology Best Practices

| Recommendation | Rationale |
|---|---|
| Dedicate NICs for vMotion | Prevents vMotion from competing with VM or storage traffic |
| Set vSAN MTU to 9000 (jumbo frames) | Reduces CPU overhead for large vSAN I/O — requires end-to-end switch support |
| Isolate management on its own VLAN | Prevents VM traffic from reaching host management plane |
| Use at least 2 uplinks per host | Provides redundancy — single NIC failure does not isolate the host |
| Use VDS for production clusters | Ensures consistent port group configuration across all hosts |
| Separate vMotion and storage VLANs | Prevents storage latency spikes during large vMotion events |
| Use beacon probing with ≥3 uplinks | Detects upstream failures that link state alone misses |
| Enable NIOC on VDS | Prevents VM traffic bursts from starving vSAN or vMotion traffic |
| Use dedicated iSCSI NICs per path | Software iSCSI multipathing requires one vmk per physical NIC |

```bash
# Verify MTU on vmkernel interfaces
esxcli network ip interface list | grep -A5 vmk

# Check vSAN network health (MTU, latency, packet loss)
esxcli vsan network list
esxcli vsan health cluster list

# Verify uplink status on all vSwitches
esxcli network vswitch standard uplink list
esxcli network vswitch dvs vmware uplink list
```


```text title="Expected output"
Name  IPv4 Address      IPv6 Address  MTU   Enabled
----  ---------------  -----------   ----  -------
vmk0  192.168.1.100     ::1           1500  true
vmk1  172.16.50.10      ::1           9000  true
vmk2  172.16.51.10      ::1           9000  true
vmk3  172.16.52.10      ::1           1500  true

Cluster Member  Preferred Fault Domain  MTU    Latency  Packet Loss
---------------  ----------------------  -----  -------  -----------
esx-01.lab.local  esx-01.lab.local       9000   0.45ms   0%
esx-02.lab.local  esx-02.lab.local       9000   0.52ms   0%
esx-03.lab.local  esx-03.lab.local       9000   0.48ms   0%

Health Status: Healthy
Last Check: 2024-01-15 14:32:18

vSwitch  Uplink  Status  Speed  Duplex
-------  ------  ------  -----  ------
vSwitch0  vmnic0  Up      10Gbps  Full
vSwitch0  vmnic1  Up      10Gbps  Full
vSwitch1  vmnic2  Up      10Gbps  Full

DVS Name              Uplink  Status  Speed  Duplex
-------------------  ------  ------  -----  ------
DSwitch-Prod-01      vmnic3  Up      10Gbps  Full
DSwitch-Prod-01      vmnic4  Up      10Gbps  Full
DSwitch-Prod-02      vmnic5  Up      10Gbps  Full
```

!!! warning "Common errors"
    **`Error: Unknown command or namespace vsan`** — Verify vSAN is licensed and enabled on the cluster; if not, skip vSAN-specific commands.
    **`Error: Could not get property for object of type HostVirtualNic`** — Ensure the ESXi host is in a healthy state and the vSphere API is responding; try reconnecting the host to vCenter.
---

## Related Pages

- [Cluster Services — DRS, HA, and vSAN](../cluster-services/)
- [vSphere Storage Concepts](../vsphere-storage/)
- [vSphere Lifecycle Management](../vsphere-lifecycle/)
- [ESXi Host Operations](../../esxi/)
