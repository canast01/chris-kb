---
tags:
  - reference
---
# VMware Platform Design Decisions

This page documents key architectural design decisions made for the VMware platform environment. Each entry captures what was chosen, why it was chosen over the alternatives, and what trade-offs were accepted. This serves as institutional memory — a record of intent that should inform future changes and prevent decisions from being revisited without cause.

---

```d2
direction: down

storage_decisions: "Storage Decisions" {shape: rectangle}
decision_vsan_as_primary_vm_storage: "Decision: vSAN as Primary VM Storage" {shape: rectangle}
decision_powermax_pure_storage_for_m: "Decision: PowerMax / Pure Storage for Mission-\nCritical Workl" {shape: rectangle}
networking_decisions: "Networking Decisions" {shape: rectangle}
decision_nsxt_as_the_overlay_network: "Decision: NSX-T as the Overlay Network" {shape: rectangle}
decision_vsphere_distributed_switch_: "Decision: vSphere Distributed Switch (VDS) over\nStandard Swi" {shape: rectangle}

storage_decisions -> decision_vsan_as_primary_vm_storage: uses
decision_vsan_as_primary_vm_storage -> decision_powermax_pure_storage_for_m: uses
decision_powermax_pure_storage_for_m -> networking_decisions: uses
networking_decisions -> decision_nsxt_as_the_overlay_network: uses
decision_nsxt_as_the_overlay_network -> decision_vsphere_distributed_switch_: uses
```

## Storage Decisions

---

## Decision: vSAN as Primary VM Storage

**Decision:** Use vSAN for VM workload storage on HCI nodes rather than presenting external SAN LUNs to ESXi hosts.

**Rationale:** vSAN eliminates the SAN fabric dependency for the VM storage tier entirely. Storage policy-based management (SPBM) allows per-VM data services (mirroring, erasure coding, encryption, compression) without SAN administrator involvement. The hyperconverged model reduces the operational boundary between compute and storage teams, and the management plane is integrated directly into vCenter.

**Alternatives considered:**

- NFS datastore from NetApp ONTAP
- iSCSI LUNs from Dell PowerMax
- Fibre Channel from Brocade fabric connected to existing arrays

**Trade-offs:** Capacity scales with compute nodes — you cannot add storage without also adding compute (and vice versa), which creates overprovisioning risk in unbalanced workloads. vSAN requires dedicated SSD disk groups; those drives cannot be repurposed without removing the host from the cluster. During a host failure, rebuild window is longer than traditional RAID rebuild on an array.

**Review trigger:** When VM density requires more storage capacity than the corresponding compute headroom supports; when latency SLAs tighten below what vSAN ESA NVMe-based architecture can consistently deliver.

---

## Decision: PowerMax / Pure Storage for Mission-Critical Workloads

**Decision:** Retain array-based storage (Dell PowerMax, Pure Storage) for tier-1 databases and applications that require consistent sub-millisecond latency or RDM block access.

**Rationale:** Dedicated arrays provide guaranteed sub-millisecond latency that is independent of hypervisor scheduling, vSAN rebuild activity, or cluster rebalancing. PowerMax SRDF enables near-zero RPO replication natively at the array level without VM-level agents. Proven workload isolation ensures that a noisy-neighbour VM workload on vSAN cannot affect a production database LUN.

**Alternatives considered:** Moving all workloads, including tier-1 databases, onto vSAN and relying on SPBM policies for performance isolation.

**Trade-offs:** Higher cost per TB compared to vSAN capacity. Requires a dedicated SAN team with array-specific expertise. A separate management plane (PowerMax Unisphere, Pure1) must be maintained independently of vCenter.

**Review trigger:** When vSAN ESA NVMe latency profiles are validated to match dedicated array latency for specific database workloads under production load patterns.

---

## Networking Decisions

---

## Decision: NSX-T as the Overlay Network

**Decision:** All VM networking runs over NSX-T logical segments. Physical VLANs are used only for the underlay transport network (TEP, management, uplinks). No VM is placed directly on a physical VLAN segment.

**Rationale:** NSX-T Distributed Firewall (DFW) enforces microsegmentation at the vNIC level without requiring changes to physical ACLs or upstream switch configuration. Workloads are portable across physical racks and even sites without IP address changes because routing is handled at the Tier-0/Tier-1 logical level. Security policy follows the workload identity, not the physical port.

**Alternatives considered:**

- Pure VLAN-based segmentation managed through vSphere Distributed Switch port groups
- Cisco ACI fabric as the overlay and policy enforcement plane

**Trade-offs:** NSX-T introduces significant operational complexity. Staff require NSX-specific expertise beyond vSphere administration. The NSX Manager cluster (three appliances) is an additional infrastructure dependency that must be maintained, patched, and backed up. DFW rule sprawl requires governance to remain manageable.

**Review trigger:** When DFW rule count approaches documented performance thresholds for the platform version in use; when NSX-T transitions to NSX 4.x architectural changes that alter the management or data plane model.

---

## Decision: vSphere Distributed Switch (VDS) over Standard Switch (VSS)

**Decision:** All production ESXi hosts use a vSphere Distributed Switch. VSS is used only on the management physical NIC during initial host bootstrap before the host joins vCenter.

**Rationale:** VDS enables centralised network policy management from vCenter. Features that are exclusively available on VDS and are required in this environment include: Network I/O Control (NIOC) for traffic class bandwidth guarantees, LACP-based NIC teaming, NetFlow export for traffic visibility, and port mirroring for security monitoring.

**Alternatives considered:** Retaining VSS on all hosts with consistent per-host configuration enforced through scripts or host profiles.

**Trade-offs:** VDS configuration changes require vCenter to be operational. If vCenter is unavailable, no VDS port group or uplink changes can be made. Hosts retain their existing VDS configuration and continue to forward traffic, but administrative changes are blocked until vCenter is restored.

**Review trigger:** If ESXi hosts are ever deployed into an environment outside vCenter management (standalone ESXi, edge deployments), VDS is not applicable and VSS design is required for that deployment class.

---

## DR and Replication Decisions

---

## Decision: SRM + vSphere Replication as Primary DR Orchestration

**Decision:** VMware Site Recovery Manager (SRM) is used as the DR orchestration layer for non-tier-1 workloads. vSphere Replication provides the host-based asynchronous replication transport for those VMs.

**Rationale:** SRM provides automated, policy-driven recovery plan execution including VM boot order, IP remapping, and pre/post-recovery scripts. Recovery plan testing can be executed without impacting production or the current replication stream. Protection groups allow workload-level RPO assignment via vSphere Replication policies, with minimum RPO of 5 minutes.

**Alternatives considered:**

- Script-based manual failover procedures
- Veeam replication with manual orchestration
- Extending SRDF/A to all VM tiers (cost-prohibitive at scale)

**Trade-offs:** vSphere Replication agent runs within each replicated VM's host, consuming CPU and memory resources proportional to the change rate. Pre-8.x SRM required a Windows Server VM; while the OVA-based deployment resolves this, it introduces an additional appliance to manage. Recovery plans must be maintained as workloads change.

**Review trigger:** When RPO requirements for a protected workload drop below 5 minutes — at that point, array-based replication (SRDF/A) must be used instead of vSphere Replication.

---

## Decision: SRDF/A for Tier-1 Database Replication

**Decision:** PowerMax SRDF/A (synchronous mode) is used for all databases with an RPO=0 requirement. No data loss is tolerable for this workload class.

**Rationale:** SRDF/A provides zero data loss replication that is completely transparent to the guest OS and application. No in-guest agent is required. Array-level consistency groups ensure that multi-LUN databases (data, log, temp) are replicated and can be recovered to a consistent point. The write acknowledgement is not returned to the host until the write has been confirmed at the DR array.

**Alternatives considered:** Relying on application-level replication (SQL Always On, Oracle Data Guard) in place of array-level replication for the same tier.

**Trade-offs:** Every write I/O incurs the latency of a round-trip to the DR site before the acknowledgement is returned to the application. This makes SRDF/A sensitive to WAN round-trip time. Dedicated dark fibre or a reserved WAN circuit is required to keep latency within the acceptable window. For write-intensive databases, this can reduce throughput.

**Review trigger:** When WAN round-trip latency to the DR site exceeds 10ms. Beyond that threshold, SRDF synchronous mode cannot maintain the required I/O performance and the design must be re-evaluated — either by improving the WAN link or accepting an RPO > 0 with SRDF/S (asynchronous).

---

## Virtualisation Decisions

---

## Decision: VCF for New Platform Deployments

**Decision:** All new data centre buildouts use VMware Cloud Foundation (VCF) as the deployment and lifecycle framework. Standalone vSphere deployments are not created for new workload domains.

**Rationale:** VCF automated bring-up eliminates the manual sequencing of NSX, vSAN, vCenter, and ESXi installation. The SDDC Manager maintains a validated Bill of Materials (BOM) and enforces version alignment across all components. Workload domain provisioning ensures consistent cluster configuration. Unified lifecycle management reduces the risk of component version drift that creates upgrade complications over time.

**Alternatives considered:** Standalone vSphere with independently managed NSX and vSAN deployments, using custom scripts and host profiles to enforce consistency.

**Trade-offs:** VCF carries a licensing cost premium over standalone vSphere licensing. SDDC Manager is an additional management appliance that must be operated, backed up, and patched. Workload domain provisioning introduces additional lead time compared to manually building a cluster. Not all third-party integrations are validated in the VCF BOM.

**Review trigger:** If Broadcom licensing changes materially alter the cost or entitlement structure of VCF relative to standalone vSphere + NSX + vSAN, the economic rationale for VCF should be reassessed.

---

## Decision: Instant Clone for Horizon Desktop Pools

**Decision:** All non-persistent Horizon desktop pools use instant clones. Persistent desktop pools use full clones. Linked clones are not used.

**Rationale:** Instant clone provisioning completes in under 30 seconds by forking a running parent VM's memory and disk state. This eliminates the snapshot chain overhead of linked clones and the storage growth associated with full clones for non-persistent use cases. There is no redirect-on-write penalty after boot because the instant clone is an independent VM from the moment it is forked.

**Alternatives considered:**

- Linked clones (now deprecated in current Horizon versions)
- Full clones for all pool types regardless of persistence requirement

**Trade-offs:** Instant clone requires a parent VM to be running at all times for each pool; that parent VM consumes compute and memory resources continuously. Desktop customisation is performed by ClonePrep (Horizon's customisation mechanism) rather than sysprep, which has compatibility differences with some applications. Parent VM updates require a push operation that causes active sessions to log off.

**Review trigger:** If App Volumes or Dynamic Environment Manager compatibility issues arise that require sysprep-based customisation, full clone pools should be evaluated for the affected application sets.

---

## Decision: Native Key Provider for VM Encryption

**Decision:** vSphere Native Key Provider (NKP) is used for VM encryption and vSAN data-at-rest encryption rather than an external KMS appliance.

**Rationale:** NKP has no external dependency — it does not require a separate KMS appliance to be reachable at host boot time or during vCenter restart. Keys are distributed from vCenter and cached on ESXi hosts, meaning encrypted VMs can power on even if the VCSA is temporarily unavailable. NKP is backed up with the vCenter file-based backup, simplifying key lifecycle. It meets encryption compliance requirements for most regulatory frameworks without additional infrastructure.

**Alternatives considered:**

- Thales CipherTrust (formerly SafeNet) as external KMS
- Entrust nShield as external KMS
- HashiCorp Vault with KMIP interface

**Trade-offs:** NKP key material is ultimately backed by the vCenter backup. If the VCSA is lost without a restorable backup, the encryption keys are lost and encrypted VMs cannot be recovered. External KMS solutions provide an independent key lifecycle and custody chain that is outside vCenter. NKP does not meet FIPS 140-2 Level 3 requirements, which some regulatory audits mandate.

**Review trigger:** If a regulatory audit or compliance framework requires FIPS 140-2 Level 3 hardware security module protection or mandates independent key custody outside the virtualisation management plane.

---

## Lifecycle Decisions

---

## Decision: Image-Based Lifecycle Management (vLCM) for All Clusters

**Decision:** All ESXi clusters are managed using vSphere Lifecycle Manager (vLCM) image-based management. Baseline-based remediation is retired and not used for any cluster that has been migrated to image management.

**Rationale:** vLCM image-based management enforces a desired-state model: a single image manifest defines the exact ESXi build, version, and vendor add-on set for every host in a cluster. This eliminates the per-host configuration drift that baselines allowed. Vendor add-ons (drivers, agents) are included in the image and validated together, reducing the risk of post-upgrade driver incompatibility. Hosts managed by vLCM image are eligible for Quick Boot, which reduces remediation downtime.

**Alternatives considered:** Continuing to use vLCM baseline-based remediation with extension and patch baselines per cluster.

**Trade-offs:** Image-based management and baseline-based management are mutually exclusive for a given cluster — once a cluster is migrated to an image, it cannot be reverted to baselines without destroying and rebuilding the cluster configuration. The migration is therefore a one-way operation. Not all vendor add-ons are available in the VMware or partner depots; missing add-ons block image composition until the vendor publishes a depot-compatible package.

**Review trigger:** If a required vendor add-on or driver is not available in the vLCM depot for image composition and there is no vendor roadmap commitment to publish it, the cluster must remain on baseline management until the gap is resolved.

---

## Compute Decisions

---

## Decision: 4:1 CPU Overcommit Ratio as Default; 8:1 Maximum Permitted

**Decision:** The default CPU overcommit ratio for general workload clusters is 4 vCPUs per physical core (4:1). No cluster is permitted to exceed 8:1 without an explicit architectural exception and documented workload characterisation.

**Rationale:** A 4:1 ratio balances density with scheduling headroom. At this ratio, CPU ready time on typical mixed workloads remains below 5% — the threshold above which application response time degradation becomes measurable. An 8:1 ceiling provides a hard guard against the runaway overcommit that builds silently when VM deployments are not regularly reviewed against actual utilisation.

**Alternatives considered:**

- Fixed 10:1 ratio across all clusters as per some vendor reference architectures
- Unlimited overcommit with reactive remediation based on performance alerts

**Trade-offs:** A conservative overcommit ratio leaves physical CPU capacity underutilised during off-peak periods. The 4:1 default increases per-VM cost compared to a 10:1 reference design. Workload-specific clusters (Horizon VDI, Tanzu Supervisor) require tuned ratios that differ from the general default and must be documented separately.

**Review trigger:** When average cluster-wide CPU utilisation sustained over a 30-day period exceeds 60%, the overcommit ceiling for that cluster should be reviewed against its workload profile. When a new workload class with a validated low vCPU utilisation pattern (e.g., test/dev or batch) is introduced, a higher ratio may be justified.

---

## Decision: NUMA Boundary Crossing Is Prohibited for Production VMs Above 8 vCPUs

**Decision:** VMs with more than 8 vCPUs are sized to fit within a single NUMA node. A VM that would require vNUMA spanning is resized, the host is right-sized to a larger NUMA topology, or the workload is distributed across multiple smaller VMs.

**Rationale:** When a VM's vCPU count exceeds the number of physical cores in a single NUMA node, the hypervisor must schedule vCPUs across two NUMA nodes. Memory accesses from vCPUs on one node to memory allocated on the other incur a NUMA remote access penalty — typically 20–40 ns additional latency per access on current hardware. For memory-intensive workloads (databases, in-memory caches), this penalty has a measurable impact on throughput.

**Alternatives considered:** Allowing unrestricted NUMA spanning and relying on the ESXi NUMA scheduler to minimise cross-node scheduling where possible.

**Trade-offs:** This policy constrains maximum VM size to the per-socket core count of the physical hosts in the cluster. On a dual-socket host with 32 cores per socket, this limits single VMs to 32 vCPUs. Workloads that genuinely require more vCPUs must either be split or hosted on purpose-built large-NUMA hardware.

**Review trigger:** When new host hardware with a different NUMA topology (e.g., 4-socket systems, AMD EPYC with multiple CCX groups, or Intel Sapphire Rapids SNC-4 mode) is introduced, the vCPU boundary thresholds must be recalculated against the new physical NUMA layout.

---

## Decision: EVC Baseline Set to Highest Common Feature Set Across All Cluster Members

**Decision:** Each cluster's Enhanced vMotion Compatibility (EVC) baseline is set to the highest CPU feature set that all current cluster members support. The baseline is not set below the common denominator unnecessarily, and it is not set above what all hosts support.

**Rationale:** Setting EVC to the true common denominator preserves access to the maximum available instruction set for running VMs (including AVX-512, SHA-NI, and other acceleration instructions used by databases and encryption workloads). Setting it lower than necessary to "future-proof" for unknown hardware additions masks CPU features and degrades application performance without benefit.

**Alternatives considered:**

- Setting EVC to a deliberately conservative baseline (e.g., two generations behind) to make future host additions trivially compatible
- Disabling EVC entirely on homogeneous clusters

**Trade-offs:** Setting EVC to the highest common baseline means that adding a host with a lower CPU feature set requires either lowering the baseline (which requires powering off all running VMs before the change takes effect) or rejecting the new host from the cluster. This creates a hardware procurement constraint — new servers must match or exceed the existing EVC baseline.

**Review trigger:** When new ESXi hosts with a different CPU generation are to be added to an existing cluster, the EVC baseline compatibility must be verified before host addition is attempted. If the new hosts cannot meet the existing baseline, an architectural decision is required.

---

## Decision: No CPU or Memory Reservations on General Workload VMs; Hard Limits Prohibited

**Decision:** General workload VMs are deployed without CPU or memory reservations and without CPU or memory hard limits. Reservations are used only for infrastructure VMs (NSX Edge, vCLS, SRM appliances) that require guaranteed resources. Limits are never applied.

**Rationale:** Reservations reduce the effective overcommit headroom of a cluster by locking physical resources to a VM regardless of whether the VM is actively using them. Limits are more dangerous — a VM with a CPU limit below its actual vCPU allocation will suffer artificial CPU ready time even when the host has idle capacity, leading to performance problems that are invisible in standard capacity reports. The operational cost of managing per-VM reservations across a large fleet outweighs the benefit for workloads that are not latency-critical.

**Alternatives considered:** Using memory reservations as a default to prevent balloon driver and swap activity; using CPU limits as a cost-showback mechanism.

**Trade-offs:** Without reservations, infrastructure VMs compete with workload VMs during resource contention events. This is mitigated by placing infrastructure VMs in resource pools with guaranteed shares and by the conservative overcommit policy above. The absence of limits means a runaway VM can consume disproportionate host resources if vCPU hotplug is enabled and is abused.

**Review trigger:** If a regulatory or chargeback requirement mandates per-VM resource accountability, a resource pool structure with shares-based entitlement is the preferred approach over per-VM limits.

---

## Management Decisions

---

## Decision: vCenter Linked Mode with a Single SSO Domain Across All vCenters

**Decision:** All vCenter Server instances in the environment are joined to a single vSphere SSO domain (`vsphere.local`) and configured in Enhanced Linked Mode (ELM). No standalone vCenter deployments exist, and no secondary SSO domains are created.

**Rationale:** Enhanced Linked Mode provides a single-pane-of-glass view across all vCenter instances. A single SSO domain means a single set of identity sources (AD), a single set of vSphere permissions, and a single certificate trust root. Administrators do not need multiple logins or separate browser sessions to manage different vCenters. Global Permissions applied at the SSO domain level propagate to all linked vCenters, simplifying RBAC maintenance.

**Alternatives considered:**

- Multiple independent SSO domains per data centre or per business unit, federated via identity provider
- Standalone vCenter per workload domain with separate AD authentication

**Trade-offs:** ELM creates an operational dependency between vCenter instances via the SSO replication ring. If the primary vCenter in the SSO domain experiences certificate or lookup service issues, it can affect authentication for all linked vCenters. SSO domain topology must be carefully planned — vCenters in different physical sites joined to the same SSO domain require reliable network connectivity between them for replication.

**Review trigger:** If a business unit acquisition introduces a separate Active Directory forest that cannot be federated into the existing SSO domain, a separate SSO domain with cross-domain trust may need to be evaluated.

---

## Decision: VCSA Sized at Large Deployment for All Production vCenters

**Decision:** All production vCenter Server Appliances are deployed at the **Large** deployment size (16 vCPU, 32 GB RAM) regardless of the initial managed object count. The **Small** or **Medium** sizes are used only for isolated lab or development vCenters with no production workloads.

**Rationale:** vCenter appliance sizing based on current VM count is a common mistake that defers pain — as the managed object count grows, vCenter services begin to exhibit latency before the formal threshold for the next size tier is crossed. Deploying at Large from the start eliminates reactive resizing operations, which require a maintenance window and VCSA reconfiguration. Large-size vCenter also provides headroom for the inventory spike that occurs during VCF workload domain provisioning operations.

**Alternatives considered:** Starting with Medium and resizing when vCenter performance degrades; using the VMware sizing tool output directly as the deployment size target.

**Trade-offs:** Over-provisioning VCSA by one size tier consumes approximately 8 additional vCPUs and 16 GB of RAM relative to a Medium deployment. On a dedicated management cluster this resource cost is acceptable; on a stretched resource-constrained cluster it may not be.

**Review trigger:** If the environment grows to more than 2,000 VMs or 200 ESXi hosts under a single vCenter, the X-Large tier must be evaluated. At that scale, the vPostgres database growth rate and task scheduler load can exceed Large-tier capacity.

---

## Decision: vCenter HA Deployed for All Production vCenter Instances

**Decision:** vCenter High Availability (vCenter HA) is configured for every production VCSA. The Active, Passive, and Witness nodes are placed on separate ESXi hosts in the management cluster using VM-to-host anti-affinity rules.

**Rationale:** vCenter HA provides an automatic failover path that reduces vCenter downtime from hours (restore from backup) to under 5 minutes (passive node promotion). The passive node is a continuously updated hot standby that requires no restore operation. In an environment where vCenter manages the DRS and HA behaviour of workload clusters, vCenter downtime is not a benign event — it prevents VM migrations, disables automated HA responses, and blocks all management plane operations.

**Alternatives considered:**

- File-based backup with recovery to a new OVA deployment (no HA)
- vSphere HA restart of a standalone VCSA on host failure

**Trade-offs:** vCenter HA requires three VCSA instances (active, passive, witness) where the passive is a full-resource replica of the active. The resource footprint is approximately 3x a standalone deployment. The vCenter HA network is an additional management network segment that must be provisioned and maintained. Failover is automatic but monitoring is required to confirm the passive node is in sync.

**Review trigger:** If the management cluster does not have sufficient capacity to host all three vCenter HA nodes with anti-affinity rules respected, the vCenter HA topology must be re-evaluated or the management cluster capacity must be expanded.

---

## Security Decisions

---

## Decision: VM Encryption via vSAN Data-at-Rest Encryption; Not Per-VM Encryption

**Decision:** Data-at-rest encryption is enforced at the vSAN datastore level using vSAN Encryption. Per-VM encryption via SPBM VM Encryption policy is not applied to general workload VMs.

**Rationale:** vSAN datastore encryption encrypts all data written to the storage tier at the disk group level, covering all VMs on the datastore with a single policy. It requires no per-VM reconfiguration and has no per-VM CPU overhead beyond the storage I/O path. Per-VM encryption, while more granular, adds encryption overhead to every individual VM's storage I/O and multiplies the key management complexity proportionally with the number of encrypted VMs. For a compliance posture that requires "all data at rest is encrypted," datastore-level encryption is operationally simpler and achieves the requirement.

**Alternatives considered:**

- Per-VM encryption using SPBM VM Encryption storage policy applied selectively
- Combined approach: vSAN Encryption for the datastore plus per-VM encryption for a highest-sensitivity subset

**Trade-offs:** vSAN datastore encryption encrypts every VM on the datastore without distinction — there is no way to decrypt a single VM's data while leaving others encrypted. If a workload specifically requires its encryption keys to be separately managed from all other workloads (e.g., a regulated business unit with independent key custody requirements), per-VM encryption with its own KMS is the only option. vSAN Encryption also requires the full datastore to be decrypted before changing the key provider.

**Review trigger:** If a regulated workload with an independent key custody requirement is onboarded, per-VM encryption must be evaluated for that workload tier. If a compliance audit requires demonstrable separation of encryption keys between workload classes, the shared-key vSAN encryption model must be revisited.

---

## Decision: vSphere Native Key Provider for All Encryption; External KMS Deferred

**Decision:** vSphere Native Key Provider (NKP) is the sole key provider for vSAN encryption and any per-VM encryption in use. External KMS integration (Thales, Entrust, HashiCorp Vault) is not deployed until a regulatory requirement mandates it.

**Rationale:** NKP eliminates the operational dependency on an external KMS appliance at host boot time. Keys are cached on ESXi hosts and distributed from vCenter, meaning encrypted datastores mount and encrypted VMs power on without a network call to an external system. NKP key material is protected by vCenter backup, which is already within the backup and recovery SLA. This satisfies encryption-at-rest requirements for most internal compliance frameworks without additional infrastructure cost or operational complexity.

**Alternatives considered:**

- Thales CipherTrust as external KMS with KMIP interface
- HashiCorp Vault with the VMware KMIP Secrets Engine
- Entrust nShield HSM-backed KMS

**Trade-offs:** NKP key material is tied to the vCenter instance. Loss of vCenter without a restorable backup is a total loss of encryption keys and renders all encrypted VMs irrecoverable. NKP does not provide FIPS 140-2 Level 3 hardware security module protection. Regulatory frameworks that mandate independent key custody, HSM-backed key storage, or key rotation auditing at the HSM level cannot be satisfied by NKP alone.

**Review trigger:** If any regulatory audit, framework, or contractual obligation requires FIPS 140-2 Level 3 HSM protection, independent key custody outside the virtualisation management plane, or integration with an enterprise key management system that has its own audit trail, external KMS must be implemented.

---

## Decision: Audit Log Retention at 90 Days Online; 1 Year Archived to SIEM

**Decision:** vCenter, NSX Manager, and ESXi audit and event logs are retained for 90 days in the local log store and streamed in real time to the enterprise SIEM (Aria Operations for Logs) where they are retained for 12 months.

**Rationale:** A 90-day local retention window covers the investigative window for most operational incidents without exhausting VCSA or NSX Manager disk capacity. SIEM retention to 12 months satisfies the most common regulatory audit requirements (ISO 27001, PCI-DSS, SOC 2) that mandate event log availability for a full year. Streaming to SIEM in real time ensures that log data is preserved even if a vCenter or NSX Manager appliance is lost or must be rebuilt.

**Alternatives considered:**

- Log retention entirely within vCenter and NSX Manager local stores (no SIEM forwarding)
- 30-day local retention with indefinite SIEM archival

**Trade-offs:** Real-time log streaming to the SIEM adds a persistent network flow from every managed appliance and ESXi host to the SIEM collector endpoints. If the SIEM collector is unavailable, events buffer locally and may be dropped if the buffer fills before the collector is restored. SIEM storage costs scale with log volume — high-change-rate environments (large DFW rulesets, frequent VM provisioning) generate significantly more log data than steady-state clusters.

**Review trigger:** If a regulatory framework or contractual obligation requires log retention beyond 12 months, the SIEM archival policy must be extended. If a security incident reveals that 90 days of local log history was insufficient for a forensic investigation, the local retention window should be increased.
