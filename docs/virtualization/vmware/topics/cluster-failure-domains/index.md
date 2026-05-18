# Cluster Failure Domains

```
┌──────────────── Failure Domain Layers: Stretched Cluster & Fault Domains ──────┐
│                                                                                 │
│  Availability Zone / Site level                                                 │
│  ┌─────────────────────────────────┐   ┌─────────────────────────────────┐     │
│  │          Site A                 │   │          Site B                 │     │
│  │  ┌──────────────────────────┐   │   │  ┌──────────────────────────┐  │      │
│  │  │ Rack A    │  Rack B      │   │   │  │ Rack C    │  Rack D      │  │      │
│  │  │ esxi-01   │  esxi-04     │   │   │  │ esxi-07   │  esxi-10     │  │      │
│  │  │ esxi-02   │  esxi-05     │   │   │  │ esxi-08   │  esxi-11     │  │      │
│  │  │ esxi-03   │  esxi-06     │   │   │  │ esxi-09   │  esxi-12     │  │      │
│  │  └──────────────────────────┘   │   │  └──────────────────────────┘  │      │
│  └─────────────────────────────────┘   └─────────────────────────────────┘     │
│                     │                                  │   + Witness VM         │
│                     └──────────── vSAN stretched ──────┘                       │
│                                                                                 │
│  vSAN fault domains prevent both copies landing in same rack/site:              │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  FTT=1 RAID-1: 3 fault domains min │ FTT=2 RAID-6: 6 fault domains min │    │
│  │  Objects: component-owner-1 in FD-A │ component-owner-2 in FD-B         │   │
│  └──────────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────┘
```

A failure domain is the blast radius of a single fault: the set of hosts, storage, or network paths that share a common point of failure. Correctly mapping and configuring failure domains is the foundation of vSAN resilience, HA placement, and maintenance safety.

---

## Failure Domain Taxonomy

| Domain Level | What It Covers | Impact of Single Failure | Mitigation |
|---|---|---|---|
| **Host** | One ESXi server (CPU, RAM, local NICs) | All VMs on that host lose compute | HA restart; vSAN FTT ≥ 1 |
| **Rack** | All hosts sharing a physical rack | Multiple hosts lose power/top-of-rack switching | Spread hosts across racks; vSAN rack-aware fault domains |
| **Power feed** | All hosts on one PDU or UPS string | Full PDU failure takes down the rack's feed | Dual-corded hosts; A/B feed distribution across racks |
| **Network switch** | All ports on one ToR or aggregation switch | Management, vSAN, and vMotion paths affected | NIC teaming across separate switches; separate vSAN VMkernel on redundant switch |
| **Storage controller** | One HBA or NVMe controller inside a host | Disk group goes offline for that host | Dual disk groups per host where possible; vSAN deduplication/RAID-5/6 for capacity tier |
| **Availability zone** | An entire datacenter or building | Full site outage | Stretched cluster (2 sites + witness); or cross-site replication via SRM/Zerto |

---

## vSAN FTT and RAID Policy Mapping

Choose a storage policy based on how many simultaneous failure domains you can tolerate.

| Policy | FTT | RAID | Min Hosts Required | Capacity Overhead | Typical Use Case |
|---|---|---|---|---|---|
| RAID-1 mirror | 1 | RAID-1 | 3 | 2× (50% usable) | Small clusters (3–4 nodes), low-latency workloads |
| RAID-5 erasure coding | 1 | RAID-5 | 4 | 1.33× (75% usable) | All-flash 4+ node clusters, capacity-sensitive |
| RAID-1 mirror | 2 | RAID-1 | 5 | 3× (33% usable) | Mission-critical VMs requiring two simultaneous host failures |
| RAID-6 erasure coding | 2 | RAID-6 | 6 | 1.5× (67% usable) | All-flash 6+ node clusters, maximum capacity efficiency at FTT=2 |

> **Note:** Erasure coding (RAID-5/6) requires all-flash disk groups. Mixed (hybrid) configurations must use RAID-1.

Set the policy per VM:

```powershell
# View current storage policies
Get-SpbmStoragePolicy | Select-Object Name, Description

# Assign a policy to a VM
Get-VM "prod-db-01" | Set-SpbmEntityConfiguration -StoragePolicy (Get-SpbmStoragePolicy "vSAN FTT=2 RAID-6")
```

---

## vSAN Fault Domain Configuration

Rack-aware fault domains tell vSAN to treat all hosts in a rack as a single failure boundary, preventing both copies of an object landing in the same rack.

### View current fault domain assignment

```bash
# From ESXi host SSH
esxcli vsan fault domain list
```

```powershell
# PowerCLI
Get-VsanFaultDomainConfiguration -Cluster <ClusterName>
```

### Create or update fault domains

```powershell
# Create fault domains per rack
New-VsanFaultDomain -Cluster "Prod-Cluster" -Name "Rack-A" -VMHost @("esxi-01", "esxi-02", "esxi-03")
New-VsanFaultDomain -Cluster "Prod-Cluster" -Name "Rack-B" -VMHost @("esxi-04", "esxi-05", "esxi-06")
```

After configuration, confirm each host shows its fault domain:

```powershell
Get-VMHost | Select-Object Name, @{N="FaultDomain"; E={ (Get-VsanView -Id $_.ExtensionData.ConfigManager.VsanSystem).GetRuntimeStats().FaultDomainName }}
```

---

## VM-Host Affinity and Anti-Affinity Rules

DRS rules enforce placement across failure domains. Anti-affinity rules are critical for HA pairs (e.g., primary/secondary databases, paired application tiers).

### Why configure affinity rules

- **Anti-affinity (VM-VM):** Prevents two VMs from running on the same host. Use for active/passive pairs.
- **Anti-affinity (VM-Host):** Prevents specific VMs from running on specific hosts (e.g., keep licensing VMs off hosts under maintenance rotation).
- **Affinity (VM-Host):** Pins VMs to a host group — use for NUMA-sensitive or hardware-licensed workloads.

### Create a VM anti-affinity rule (keep VMs apart)

```powershell
# Create VM anti-affinity rule: prod-db-01 and prod-db-02 must not share a host
New-DrsRule -Cluster "Prod-Cluster" -Name "AntiAffinity-DB-Pair" `
    -KeepTogether $false `
    -VM (Get-VM "prod-db-01", "prod-db-02") `
    -Enabled $true
```

### Create a VM-Host affinity rule (pin VMs to a host group)

```powershell
# Step 1: Create host group
New-DrsClusterGroup -Cluster "Prod-Cluster" -Name "Rack-A-Hosts" `
    -VMHost (Get-VMHost "esxi-01", "esxi-02", "esxi-03")

# Step 2: Create VM group
New-DrsClusterGroup -Cluster "Prod-Cluster" -Name "Licensing-VMs" `
    -VM (Get-VM "license-server-01")

# Step 3: Create VM-Host rule
New-DrsVMHostRule -Cluster "Prod-Cluster" -Name "License-Pinned-RackA" `
    -VMGroup "Licensing-VMs" -VMHostGroup "Rack-A-Hosts" `
    -Type MustRunOn -Enabled $true
```

### List and audit all DRS rules

```powershell
# All DRS rules in all clusters
Get-DrsRule | Select-Object Name, Cluster, Enabled, KeepTogether, Type

# VM-Host rules specifically
Get-DrsVMHostRule | Select-Object Name, Cluster, VMGroup, VMHostGroup, Type, Enabled
```

---

## Failure Domain Verification Table

After configuring failure domains, confirm each layer is correctly set up.

| Domain | Verification Method | Command / Check | Pass Criteria |
|---|---|---|---|
| vSAN fault domains | Check all hosts assigned | `esxcli vsan fault domain list` | Each host shows a named fault domain; no host in `None` |
| Fault domain count | Minimum fault domains for policy | `Get-VsanFaultDomainConfiguration` | FTT=1 needs ≥ 3 domains; FTT=2 needs ≥ 5 domains |
| Object placement | Objects span domains | `esxcli vsan debug object list` | Component owners are in different fault domains |
| Network uplink diversity | NIC team split across switches | vSphere → Host → Configure → Virtual Switches | Each VMNIC on a separate physical switch |
| Power feed diversity | Hosts on separate PDUs | Physical audit or DCIM tool | No two hosts in same fault domain share a PDU |
| DRS anti-affinity rules | Critical VM pairs are split | `Get-DrsRule \| Where-Object { $_.KeepTogether -eq $false }` | At least one rule per HA-sensitive VM pair |
| HA host failures to tolerate | HA setting matches FTT | `(Get-Cluster <name>).HAFailoverLevel` | Matches vSAN FTT setting |
