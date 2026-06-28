---
tags:
  - vsphere
  - architecture
  - operations
  - comparison
---
# Decision Trees

<div class="kb-summary">
Flowcharts for common VMware infrastructure design decisions — storage policy, NSX topology, DR tool selection, and Aria product selection.
</div>

<div class="kb-grid">
<a class="kb-card" href="vsan-policy/">
<strong>vSAN Storage Policy</strong><br>
Choose FTT level, RAID type, encryption, and dedup/compression based on cluster size and requirements.
</a>
<a class="kb-card" href="nsx-topology/">
<strong>NSX Topology</strong><br>
Select overlay vs VLAN, T0/T1 placement, Edge sizing, HA model, and north-south routing type.
</a>
<a class="kb-card" href="dr-tool/">
<strong>DR Tool Selection</strong><br>
SRM vs vSphere Replication vs backup-based DR — choose based on RPO, RTO, and licensing.
</a>
<a class="kb-card" href="aria-selection/">
<strong>Aria Product Selection</strong><br>
Which Aria product fits your need — monitoring, logging, automation, network visibility, or lifecycle.
</a>
</div>

---

## Product Comparison Tables

### vSAN vs ONTAP vs PowerStore vs FlashArray

| Feature | vSAN | NetApp ONTAP | Dell PowerStore | Pure Storage FlashArray |
|---|---|---|---|---|
| **Primary use case** | HCI storage for vSphere clusters | Enterprise NAS/SAN, data management | Unified all-flash block + file | All-flash block with NVMe focus |
| **Protocol support** | iSCSI, NFS (via vSAN File Services) | NFS, SMB, iSCSI, FC, NVMe/FC, NVMe/TCP | NFS, SMB, iSCSI, FC, NVMe/FC | iSCSI, FC, NVMe/FC, NVMe/TCP |
| **Max raw capacity** | Scales with cluster nodes (PB-scale with large clusters) | PB-scale (AFF A-series, C-series) | Up to 4PB raw per cluster | Up to 4PB (//X) |
| **Dedup/compression** | Inline dedup + compression (all-flash clusters) | Inline dedup, compression, compaction | Inline dedup + compression, data reduction ratio reporting | Always-on inline dedup + compression (always enabled) |
| **Replication tool** | vSphere Replication / HCX / vSAN Stretched Cluster | SnapMirror (sync/async), MetroCluster | PowerStore replication (sync/async), Dell RecoverPoint | ActiveDR (sync), ActiveCluster (stretch), async replication |
| **Cloud integration** | VMware Cloud on AWS, Azure VMware Solution | Cloud Volumes ONTAP (AWS/Azure/GCP), BlueXP | PowerStore with Dell APEX cloud services | Pure Cloud Block Store (AWS, Azure) |
| **Ideal workload** | vSphere VMs, VDI, Kubernetes (Tanzu) | Mixed NAS/SAN, Oracle, SAP, DevOps | Mixed enterprise block + file, virtualization | High-performance databases, VDI, Kubernetes |
| **Management UI** | vSphere Client (native), vSAN Health UI | ONTAP System Manager, BlueXP | PowerStore Manager (REST-first UI) | Pure1 (cloud-based), Purity//FA GUI |

> **When to choose:** Pick **vSAN** when you want hyper-converged simplicity and everything runs in vSphere. Pick **ONTAP** when you need mature NAS at scale with rich data management (SnapMirror, FlexClone). Pick **PowerStore** when the workload is mixed block/file on Dell hardware. Pick **FlashArray** when latency is the primary constraint and NVMe-first architecture matters.

---

### Veeam vs CommVault vs NetBackup

| Feature | Veeam Backup & Replication | Commvault Complete Backup & Recovery | Veritas NetBackup |
|---|---|---|---|
| **Backup targets** | Disk (repo), tape, object storage (S3/Azure/GCS), immutable object, Veeam Cloud Connect | Disk, tape, object storage, Commvault Metallic (SaaS), cloud-native | Disk, tape, object storage, cloud (AWS/Azure/GCP), NetBackup CloudCatalyst |
| **VMware integration depth** | Native vStorage API (VADP), vSphere plug-in, instant VM recovery, SureBackup auto-testing | VADP-based, IntelliSnap for array snapshots, deep vCenter integration | VADP, VMware snapshot integration, Accelerator for fast full backups |
| **Cloud archive support** | S3-compatible + cloud tier with capacity licensing; native Azure Blob/GCS archive tiers | Commvault Metallic SaaS, direct-to-cloud backups, WORM object lock | S3/Azure Blob/GCS archive tiers, CloudCatalyst dedup to cloud |
| **Ransomware protection** | Immutable repos (Linux hardened, object lock), SureBackup integrity scan, 4-eyes auth for delete | Ransomware detection analytics, immutable storage, honeypot files, threat scan on restore | Anomaly detection, WORM/immutable storage, NetBackup Malware Scanning |
| **RPO/RTO capabilities** | RPO: minutes (continuous CDP option); RTO: seconds with Instant VM Recovery | RPO: minutes; RTO: minutes with IntelliSnap; granular file/app recovery | RPO: minutes; RTO: minutes with Instant Access; ROBO optimised |
| **Licensing model** | Per-VM socket or per-workload (Universal License); perpetual + subscription | Per-capacity TB or per-workload subscription; VaultBridge SaaS option | Per-front-end TB (FETB) subscription; workload-based add-ons |

> **When to choose:** Pick **Veeam** for a VMware-first environment where speed of recovery and simplicity matter most. Pick **Commvault** for heterogeneous enterprise environments requiring broad workload coverage and analytics. Pick **NetBackup** for large enterprise or service provider environments with tape, complex SLA tiers, and multi-site policies.

---

### NSX vs Physical SAN Networking

| Feature | VMware NSX (Software-Defined) | Physical SAN Networking (FC/FCoE) |
|---|---|---|
| **Micro-segmentation approach** | Distributed Firewall (DFW) rules at each vNIC — policy follows the workload regardless of location | VLAN/Zone-based segmentation on physical switches/directors; changes require reconfiguration of fabric |
| **East-west traffic handling** | Stays within the hypervisor kernel (no physical hop); line-rate forwarding via DPDK/SmartNIC offload | All east-west traffic traverses physical fabric switches; latency depends on switch hops and ISL capacity |
| **Operational complexity** | Policy managed centrally in NSX Manager; zero-touch provisioning; infra team owns policy, not per-switch configs | Per-switch zone configuration (WWPN/WWNN zoning); change control required per fabric; separate SAN admin skill set |
| **Hardware requirements** | Commodity 10/25/100 GbE NICs + standard Ethernet switches; SmartNICs optional for offload | Dedicated FC HBAs, FC switches (Brocade/Cisco MDS), SFPs; separate physical fabric from LAN |

> **When to choose:** Choose **NSX** when you want security policy that follows workloads, want to eliminate dedicated SAN fabric costs, or need rapid micro-segmentation at scale. Choose **physical SAN networking** when you have latency-sensitive storage workloads (sub-100us FC), existing Fibre Channel investment, or compliance requirements mandating physical separation of storage traffic.

---

### Ansible vs Terraform vs PowerCLI for VMware Automation

| Feature | Ansible | Terraform | PowerCLI |
|---|---|---|---|
| **Idempotency** | Module-level idempotency; most VMware modules check current state before acting | Full state-driven idempotency via `.tfstate`; plan shows exact drift before apply | Script-level; developer must write idempotency logic explicitly |
| **VMware module ecosystem** | `community.vmware` collection (200+ modules); Ansible Automation Platform adds EE support | `hashicorp/vsphere` provider + `dell/vxrail`, `netapp/netapp-ontap`; growing ecosystem | Full native vSphere/vSAN/NSX/Aria API coverage via VMware-maintained cmdlets |
| **State management** | Stateless — no drift tracking between runs; re-runs tasks if not skipped by conditionals | Stateful — tracks all managed resources in `.tfstate`; detects and reconciles drift | Stateless — no built-in state; script output only |
| **Learning curve** | Low-medium; YAML playbooks readable by ops teams; Python knowledge helps for custom modules | Medium; HCL syntax straightforward; understanding plan/apply/state lifecycle takes time | Low for Windows/PowerShell admins; steep for Linux/non-MS backgrounds |
| **Best for (Day 0/1/2)** | **Day 1-2**: Config management, post-deploy hardening, patching, service config on VMs | **Day 0-1**: Infrastructure provisioning (deploy VMs, networks, clusters, datastores) | **Day 1-2**: Interactive admin, one-off scripting, deep vSphere API tasks, health checks |

> **When to choose:** Use **Terraform** to provision VMware infrastructure (VMs, port groups, datastores) as code with full lifecycle management. Use **Ansible** for configuration management, compliance enforcement, and Day 2 operations on running VMs. Use **PowerCLI** for ad-hoc administration, reporting, and tasks requiring deep vSphere API access beyond what provider modules expose. In practice, all three often coexist: Terraform provisions, Ansible configures, PowerCLI audits.

---

## Use-Case to Product Recommendation Guide

### 1. Choosing a Primary Storage Platform

**Scenario:** "I need to choose storage for a new VMware environment"

| Workload Type | Recommended Platform | Why | Watch out for |
|---|---|---|---|
| All-flash NVMe performance (databases, VDI) | Pure Storage FlashArray | NVMe-first architecture, always-on inline dedup/compression, sub-100µs latency | Higher per-TB cost; block-only (no native NAS without additional products) |
| Mid-range hybrid or mixed block/file | Dell PowerStore | Unified block + file on a single platform, strong REST API, PowerStore Manager simplicity | Less mature NAS than ONTAP; ecosystem smaller than legacy VNX/Unity |
| VMware-native HCI (small-to-medium clusters) | VMware vSAN | Fully integrated with vSphere, no external array needed, scales with compute | Performance tied to cluster size; not ideal when storage and compute scale independently |
| Enterprise multi-protocol NAS/SAN at scale | NetApp ONTAP | Richest data management (SnapMirror, FlexClone, FabricPool), broad protocol support, decades of maturity | Operational complexity; licensing can be expensive; CLI steep for new users |
| Scale-out NAS / analytics / unstructured data | Dell PowerScale or Pure FlashBlade | Massively parallel NFS/SMB at petabyte scale; linear performance scaling | Not suited for block workloads; overkill for small environments |
| Object storage (S3, cloud-native apps) | Dell ECS or Pure FlashBlade S3 | S3-compatible API, geographic distribution, erasure coding for durability | Object semantics only — not a drop-in for file or block; latency higher than block arrays |

---

### 2. Choosing a Backup Strategy

**Scenario:** "I need to protect 500+ VMs with &lt;4h RTO and ransomware protection"

| Requirement | Solution | Notes |
|---|---|---|
| Image-level VM backup with fast RTO | Veeam Backup &amp; Replication | Instant VM Recovery boots directly from backup repo in seconds; SureBackup validates recoverability automatically |
| Enterprise multi-workload (VMs + Oracle + SAP + files) | Commvault Complete Backup &amp; Recovery | IntelliSnap for array-integrated snapshots; broad workload agents; analytics for anomaly detection |
| Large-scale tape/cloud tiering with complex SLA policies | Veritas NetBackup | FETB licensing suits high-volume environments; CloudCatalyst deduplication to cloud; strong ROBO support |
| Hardware snapshot offload + software orchestration | Veeam + FlashArray Storage Snapshots or ONTAP SnapVault | Offloads backup I/O from production; near-zero impact; Veeam orchestrates snapshot catalogue |
| Immutable backups (ransomware-proof) | Pure SafeMode (FlashArray) or NetApp ONTAP SnapLock | SafeMode snapshots cannot be deleted without Pure support involvement; SnapLock enforces WORM retention on volumes |
| Cloud-tier backup (long-term retention to S3) | Veeam + AWS S3 (with Object Lock) | Capacity Tier moves older restore points to object storage; Object Lock provides immutability; cost-effective for cold data |

---

### 3. Choosing a DR Strategy

**Scenario:** "What DR approach fits my RPO/RTO requirements?"

| RPO | RTO | Solution | Notes |
|---|---|---|---|
| 0 (zero data loss) | Seconds (transparent failover) | Pure ActiveDR / SM-BC (SnapMirror Business Continuity) / NetApp MetroCluster | Synchronous replication; both sites active; applications see no outage; requires low-latency inter-site link (&lt;5ms RTT) |
| &lt;15 min | Minutes | NetApp SnapMirror Async + VMware SRM | SRM automates failover runbooks; SnapMirror replicates at configurable intervals; widely deployed for Tier-1 apps |
| &lt;1 h | &lt;1 h | Dell RecoverPoint + VMware SRM | Journal-based replication enables any-point-in-time recovery; particularly strong for Dell/EMC storage estates |
| &lt;4 h | &lt;4 h | Veeam Replication | Replicates VM snapshots to secondary site; SureReplica tests failover health; no additional storage array required |
| &lt;24 h | Hours (manual) | NetApp SnapVault + manual runbook | Daily or hourly SnapVault schedule protects secondary copies; runbook-driven failover; cost-effective for Tier-3 apps |

---

### 4. Choosing a Network Virtualisation Approach

**Scenario:** "I need microsegmentation for a multi-tenant VMware environment"

| Scale | Approach | Tools | Notes |
|---|---|---|---|
| Small (&lt;50 VMs, single site) | VLAN-based segmentation + vDS port-group firewall | vSphere Distributed Switch (vDS), NSX not required | Low complexity; VLAN-per-tenant works at this scale; limited dynamic policy; no workload-following firewall |
| Medium (50–500 VMs, single or dual site) | NSX-T Distributed Firewall (DFW) | NSX-T Manager, DFW policy groups, vCenter tag-based membership | Policy follows workloads via VM tags; enforced at each vNIC in the hypervisor kernel; centrally managed |
| Large (500+ VMs, multi-site, multi-tenant) | NSX-T DFW + Active Directory IDFW + VMware Cloud Foundation | NSX-T, AD IDFW, VCF SDDC Manager, NSX Federation (optional) | IDFW ties firewall policy to AD user identity; VCF standardises lifecycle; NSX Federation spans multiple NSX deployments |
| Cloud-hybrid (on-prem + public cloud) | NSX Federation or Antrea (Kubernetes) | NSX Federation for VM workloads; Antrea CNI for Tanzu/K8s | Extends consistent policy to AVS/VMC; Antrea provides K8s-native NetworkPolicy with optional NSX integration |

---

### 5. Choosing an Automation Approach

**Scenario:** "I want to automate Day 2 VM and storage operations"

| Use Case | Tool | When to Use |
|---|---|---|
| Ad-hoc VM configuration, one-off scripting, deep vSphere API access | PowerCLI | When you need native access to vSphere/vSAN/NSX/Aria APIs beyond what provider modules expose; ideal for interactive admin, health checks, and reporting scripts |
| Idempotent infrastructure provisioning (VMs, port groups, datastores, clusters) | Terraform + vSphere Provider | Day 0–1 infrastructure-as-code; state tracking detects drift; plan/apply workflow enforces review before change; also supports ONTAP, FlashArray, and PowerStore providers |
| Configuration management at scale, compliance enforcement, patching | Ansible + community.vmware collection | Day 1–2 config management; 200+ VMware modules; stateless but idempotent at module level; Ansible Automation Platform adds RBAC and scheduling |
| Full lifecycle automation with self-service portal | VMware Aria Automation | When teams need a self-service catalog, multi-cloud provisioning, approval workflows, and integration with ITSM; higher operational overhead to set up |
| Scripting, reporting, and custom integrations | Python + pyVmomi | When PowerCLI is unavailable (Linux-only pipelines) or when building custom tooling, CI/CD integrations, or REST API clients against vCenter/NSX/ONTAP |

> **Key principle:** No tool wins all scenarios — the best environments use all 5 in their right context. Terraform provisions the infrastructure, Ansible enforces configuration and compliance, PowerCLI handles ad-hoc tasks and audits, Aria Automation provides self-service to application teams, and Python glues it all together in pipelines and custom integrations.
