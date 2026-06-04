# VMware Platform Design Decisions

This page documents key architectural design decisions made for the VMware platform environment. Each entry captures what was chosen, why it was chosen over the alternatives, and what trade-offs were accepted. This serves as institutional memory — a record of intent that should inform future changes and prevent decisions from being revisited without cause.

---

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
