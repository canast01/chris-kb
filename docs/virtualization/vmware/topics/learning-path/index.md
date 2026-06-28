---
tags:
  - learning-path
  - vmware
---
# VMware Learning Path

<div class="kb-summary">
Recommended reading order for VMware. Start here to build a complete mental model — from the management plane down to hypervisor, storage, networking, and operations tooling.

*Applies to: vSphere 7.x / 8.x*
</div>

## Stage 1: vCenter Server

vCenter is the management plane that everything else plugs into. Learn it first because every other product assumes you already understand it.

**What to learn:**

- Inventory model: Datacenter > Cluster > Host > VM — this hierarchy controls permissions, policies, and features
- DRS: how it scores cluster balance and triggers vMotion automatically
- HA: how it detects host failures and restarts VMs on surviving hosts
- Lifecycle Manager (LCM): firmware and patch baselines for ESXi
- vSphere Client: where 90% of day-to-day operations happen
- Roles and permissions: how vCenter grants access to objects in the hierarchy

**Why first:** NSX segments attach to vCenter objects. vSAN policies are assigned at vCenter. Aria Ops discovers inventory through vCenter. Without the management plane mental model, nothing else makes sense.

---

## Stage 2: ESXi

ESXi is the hypervisor that vCenter manages. You cannot troubleshoot a VM problem without understanding what the host is doing underneath it.

**What to learn:**

- VMkernel OS: a purpose-built kernel, not Linux — understanding this explains why standard Linux tools do not apply
- VMkernel ports (vmk0-vmkN): each port handles a specific traffic type (management, vMotion, vSAN, vSphere Replication)
- vSwitches and vDS: how virtual networking is wired at the host level before NSX overlays it
- Storage adapters: software iSCSI, FC HBA, NVMe — how ESXi sees physical storage
- esxcli: the command-line tool for everything from NIC stats to vSAN configuration
- esxtop: real-time host performance counters — CPU ready, memory balloon, disk latency
- Lockdown mode: restricts direct host access; important for security posture
- Host profiles: templated configuration enforcement across multiple hosts

**Why before vSAN and NSX:** vSAN runs as a module inside ESXi. NSX kernel modules run inside ESXi. Understanding the host gives you the foundation to diagnose both.

---

## Stage 3: vSAN

vSAN is distributed storage built into ESXi — no external storage array required. Storage issues are the most common production incidents in VMware environments.

**What to learn:**

- OSA vs ESA: Original Storage Architecture (disk groups with cache + capacity tiers) vs Express Storage Architecture (single-tier NVMe, vSAN 8+)
- Disk groups: how OSA organises cache and capacity devices per host
- SPBM (Storage Policy-Based Management): policies define FTT, RAID level, and I/O reservation per VM
- FTT (Failures to Tolerate): FTT=1 with RAID-1 requires 3 hosts; FTT=1 with RAID-5 requires 4 hosts
- RAID-5 vs RAID-6: erasure coding; less overhead than mirroring at the cost of rebuild time
- vSAN health checks: the built-in service that validates disk, network, and data integrity
- Rebuild operations: what happens when a disk or host fails and how long rebuilds take
- Stretched clusters: witness appliance placement, preferred site, split-brain recovery

**Why before NSX:** vSAN uses VMkernel ports for its storage traffic — understanding ESXi VMkernel ports first makes vSAN networking configuration legible.

---

## Stage 4: NSX

NSX is software-defined networking overlaid on top of ESXi hosts. The Distributed Firewall runs in the hypervisor kernel, making it invisible to traditional network teams — and capable of silently blocking traffic in ways that look like application problems.

**What to learn:**

- T0 router: the border router — connects NSX overlay to the physical underlay; handles BGP with upstream switches
- T1 router: the tenant router — connects workload segments to T0; handles NAT and load balancer services
- Segments: the overlay networks VMs attach to (replaces VLANs for east-west traffic)
- DFW (Distributed Firewall): stateful firewall rules enforced at the vNIC level on every host — rules follow the VM regardless of host
- NAT: T1 SNAT/DNAT for north-south traffic
- Load balancer: active/standby or active/active; runs on T1 or dedicated Service Router
- Edge nodes: dedicated VMs (or bare metal) that host T0/T1 Service Router components for north-south traffic
- BGP configuration: how T0 peers with physical ToR switches for routing

**Why NSX must come after ESXi and vSAN:** NSX data plane modules are loaded into the ESXi kernel. DFW rules can drop vSAN replication traffic. You must understand the layers underneath to diagnose cross-layer problems.

---

## Stage 5: Aria Suite

Aria Suite is the observability and automation layer. Once you understand the infrastructure, Aria shows you what it is doing in real time. Learn it after you understand what it is measuring.

**What to learn:**

- Aria Operations (formerly vROps): collects metrics from vCenter, ESXi, vSAN, and NSX; generates capacity and alert analysis
- Alerts and symptoms: how Aria Ops builds alert chains from raw metrics through symptom definitions
- Capacity analytics: headroom reports, time-to-exhaustion projections, what-if modelling
- Aria Operations for Logs (formerly vRLI): log ingestion from ESXi syslog, vCenter events, NSX appliances; structured search and dashboards
- Aria Operations for Networks (formerly vRNI): network topology discovery, flow analysis (IPFIX), DFW path trace, BGP adjacency visibility

**Why after everything else:** Aria Ops alerts reference vCenter objects, ESXi metrics, vSAN health states, and NSX flows. You need to understand those objects before the alerts mean anything.

---

## Stage 6: VxRail

VxRail is a Dell HCI appliance that bundles ESXi, vSAN, and vCenter with a unified lifecycle manager. Most Dell enterprise VMware deployments use VxRail, and it changes how you perform upgrades and hardware management compared to a standard VMware deployment.

**What to learn:**

- First Run Wizard: the initial cluster configuration wizard that configures ESXi, vSAN, and vCenter in sequence
- VxRail Manager: the vCenter plugin that provides VxRail-specific cluster health and lifecycle operations
- LCM bundles: composite update packages that upgrade ESXi firmware, drivers, vSAN, and VxRail software together — individual component upgrades are not supported
- iDRAC: Dell's out-of-band management interface; used for hardware health, remote console, and crash dump collection
- OMIVV (OpenManage Integration for VMware vCenter): the Dell plugin for hardware inventory and firmware visibility inside vCenter

**Why last:** VxRail is a packaging of everything in Stages 1-3. Troubleshooting VxRail issues requires you to know whether a problem is at the ESXi layer, the vSAN layer, the vCenter layer, or the Dell hardware layer. You need all three stages first to make that determination.

---

## How the Products Connect in Practice

| Scenario | Product chain |
|---|---|
| **VM is slow** | Aria Ops detects latency alert → ESXi esxtop confirms CPU ready or disk latency → vSAN health checks identify rebuild or capacity issue → NSX DFW path trace rules out firewall drops |
| **Host fails** | ESXi goes offline → vCenter HA agent detects missed heartbeat → HA restarts VMs on surviving hosts → vSAN begins component rebuild → Aria Ops raises host down and vSAN degraded alerts |
| **Patching a cluster** | LCM baseline in vCenter identifies patch → ESXi host enters maintenance mode (DRS evacuates VMs) → patch applies → host exits maintenance mode → VxRail LCM used instead on HCI nodes |
| **Provisioning a workload** | vCenter creates VM, places on cluster → vSAN SPBM policy assigned (FTT, RAID level) → NSX segment attached to VM NIC → Aria Ops discovers VM and applies monitoring policy |

---

Next: work through the Scenarios section to see these products interact under real conditions.
