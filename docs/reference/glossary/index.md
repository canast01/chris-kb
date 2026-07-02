---
tags:
  - vsphere
  - nsx
  - vsan
  - vcf
  - operations
  - kubernetes
  - networking
  - storage
  - security
---
# VMware Infrastructure Glossary

<div class="kb-summary">
155+ terms covering VMware products, virtualization, networking, storage, security, Kubernetes, and observability. Use browser search (Ctrl+F) or site search to find any term quickly.
</div>

Jump: [A](#a) [B](#b) [C](#c) [D](#d) [E](#e) [F](#f) [G](#g) [H](#h) [I](#i) [J](#j) [K](#k) [L](#l) [M](#m) [N](#n) [O](#o) [P](#p) [Q](#q) [R](#r) [S](#s) [T](#t) [U](#u) [V](#v) [W](#w)

---

```d2
direction: down

a: "A" {shape: rectangle}
b: "B" {shape: rectangle}
c: "C" {shape: rectangle}
d: "D" {shape: rectangle}
e: "E" {shape: rectangle}
f: "F" {shape: rectangle}

a -> b: uses
b -> c: uses
c -> d: uses
d -> e: uses
e -> f: uses
```

## A

**Admission Control**{: #admission-control } — vSphere HA mechanism reserving cluster capacity to guarantee VM restart after a host failure. Configured as a percentage of cluster resources or as a fixed number of host failures to tolerate.

**Affinity Rule**{: #affinity-rule } — DRS rule keeping specified VMs on the same ESXi host. Used for performance (shared memory, low latency) or licensing requirements. See also: [Anti-Affinity Rule](#anti-affinity-rule).

**Alarm** — vSphere monitoring trigger fired when a metric crosses a threshold or an event occurs. Alarms can trigger actions such as email, SNMP trap, or running a script.

**Anti-Affinity Rule**{: #anti-affinity-rule } — DRS rule separating specified VMs onto different ESXi hosts for HA purposes. Commonly applied to primary/secondary database nodes. See also: [Affinity Rule](#affinity-rule).

**Antrea** — VMware open-source CNI plugin for Kubernetes providing pod networking and NetworkPolicy enforcement using OVS (Open vSwitch). Native CNI for Tanzu clusters.

**API (vSphere REST)** — vCenter Server REST API (available since vSphere 7.0) for automating VM, cluster, datastore, and policy operations. Endpoint base: `https://vcenter/api`. Replaces the older SOAP-based vSphere API for new automation.

**Aria Automation** — VMware self-service IaaS catalog and infrastructure automation product (formerly vRealize Automation / vRA). Provides blueprints, cloud accounts, and approval workflows. API path: `/deployment/api`.

**Aria Logs** — VMware log aggregation, search, and alerting product (formerly vRealize Log Insight). Collects via syslog UDP/514, liagent, and REST API. API path: `/api/v1`.

**Aria Networks** — VMware network visibility and path analysis product (formerly vRealize Network Insight / vRNI). Ingests flow data from NSX, vCenter, and physical switches. API path: `/api/ni`.

**Aria Operations** — VMware performance monitoring, alerting, and capacity management product (formerly vRealize Operations / vROps). Extensible via adapters. API path: `suite-api/api`.

**Aria Suite Lifecycle** — VMware product deploying and upgrading Aria Suite components (formerly vRealize Suite Lifecycle Manager / LCM). Manages certificates, passwords, and version upgrades centrally.

---

## B

**Backup Proxy** — server or VM running the backup agent that handles data movement between source VMs and backup storage. In Veeam, the proxy offloads the backup server; multiple proxies parallelise jobs.

**Bare-Metal Edge**{: #bare-metal-edge } — NSX Edge deployed on a physical server using DPDK and SR-IOV NICs. Required for throughput above 25 Gbps. Cannot share the host with ESXi hypervisor workloads. See also: [DPDK](#dpdk-data-plane-development-kit).

**BFD (Bidirectional Forwarding Detection)** — lightweight protocol detecting link or path failures in milliseconds. Used by NSX T0/T1 gateways alongside BGP for fast failover without waiting for BGP hold-down timers.

**BGP (Border Gateway Protocol)**{: #bgp-border-gateway-protocol } — dynamic exterior routing protocol. NSX T0 gateways use eBGP to peer with physical ToR switches. Required for ECMP Active/Active HA. See also: [ECMP](#ecmp-equal-cost-multi-path).

---

## C

**CA (Certificate Authority)** — entity issuing and signing X.509 digital certificates. vSphere uses VMCA (VMware Certificate Authority) embedded in vCenter. Enterprise environments chain VMCA to an external root CA for full PKI integration.

**Capacity Pool** — Tanzu/vSphere with Tanzu resource quota applied to a Namespace limiting CPU, memory, and storage consumption for workloads running in that namespace.

**CBT (Changed Block Tracking)** — vSphere API tracking which disk sectors have changed since the last snapshot. Used by backup tools (Veeam, Commvault, NetBackup) for incremental backups, dramatically reducing backup window time.

**Cloud Account** — Aria Automation connection to a cloud or virtualization endpoint (vCenter, AWS, Azure, GCP). Defines which infrastructure Aria Automation can discover and provision resources on.

**Cluster** — vSphere grouping of ESXi hosts sharing HA, DRS, and vSAN configuration. All hosts in a cluster must have access to the same shared storage (vSAN, NFS, or FC/iSCSI).

**Cluster API** — Kubernetes sub-project providing a declarative API for provisioning and managing Kubernetes clusters. TKG uses Cluster API under the hood; clusters are defined as CRDs and reconciled by controllers.

**CNI (Container Network Interface)** — Kubernetes plugin standard for pod networking. Implementations include Antrea, Calico, and Flannel. NSX-T integrates via the NCP plugin, mapping Kubernetes constructs to NSX Segments and DFW rules.

**Compression** — vSAN space efficiency feature reducing stored data size. Enabled at the disk group level on OSA or cluster-wide on ESA. Compatible with D@RE encryption on both architectures.

**Content Library** — vCenter shared repository for VM templates, OVA/OVF files, ISO images, and scripts. Supports subscribed sync between vCenter instances for consistent template distribution across sites.

**CPA (Cloud Pod Architecture)** — Horizon federation feature linking multiple Horizon pods across sites into a single global namespace, enabling cross-pod session brokering and global entitlements.

**CRD (Custom Resource Definition)** — Kubernetes mechanism extending the API server with custom object types. Tanzu and NSX use CRDs (e.g., `TanzuKubernetesCluster`, `NSXLBService`) to expose infrastructure primitives to Kubernetes.

---

## D

**D@RE (Data-at-Rest Encryption)** — vSAN encryption at the datastore layer using a KMIP-compliant KMS. On vSAN OSA, D@RE is incompatible with deduplication. On vSAN ESA, it is compatible with compression. See also: [KMIP](#kmip-key-management-interoperability-protocol).

**Datastore** — vSphere storage abstraction presenting a VMFS volume, NFS share, or vSAN namespace to ESXi hosts. VMs store VMDKs and configuration files in datastores.

**DCUI (Direct Console User Interface)** — ESXi text-mode management console accessible on the physical server console or via IPMI/iDRAC. Used for initial configuration, password reset, and emergency network recovery.

**Deduplication** — vSAN space efficiency feature removing duplicate data blocks cluster-wide. Available on all-flash disk groups using OSA. Incompatible with D@RE on OSA. Not available on vSAN ESA.

**DFW (Distributed Firewall)** — NSX stateful firewall kernel module running on every transport node. Enforces policy at the vNIC level, enabling micro-segmentation without traffic hairpinning through a physical firewall.

**Disk Group** — vSAN OSA storage unit consisting of one cache device (SSD or NVMe) and one to five capacity devices. Each ESXi host in a vSAN OSA cluster contributes one to five disk groups.

**DLR (Distributed Logical Router)** — legacy NSX-V component providing east-west routing in the ESXi kernel. Replaced by T1 Gateways in NSX-T. See also: [T1 Gateway](#t1-gateway).

**DPDK (Data Plane Development Kit)**{: #dpdk-data-plane-development-kit } — user-space networking framework bypassing the OS kernel for packet processing. Used by NSX bare-metal Edge nodes to achieve line-rate throughput exceeding 25 Gbps. See also: [Bare-Metal Edge](#bare-metal-edge).

**DPU (Data Processing Unit)** — SmartNIC with an embedded processor that can offload NSX DFW and data plane operations from the ESXi host CPU. Supported on select VMware versions.

**DRS (Distributed Resource Scheduler)** — vSphere cluster feature automatically migrating VMs via vMotion to balance CPU and memory load across hosts. Modes: Fully Automated, Partially Automated, and Manual.

---

## E

**ECMP (Equal-Cost Multi-Path)**{: #ecmp-equal-cost-multi-path } — routing technique distributing traffic across multiple equal-cost paths. NSX T0 gateways use ECMP in Active/Active HA mode with BGP, providing higher aggregate throughput. Requires stateless data plane. See also: [BGP](#bgp-border-gateway-protocol).

**Edge Cluster** — NSX grouping of two to eight Edge nodes providing redundant north-south routing. All T0 gateways are placed on an Edge cluster. Minimum two nodes for production HA.

**Edge Node** — NSX gateway appliance (VM or bare-metal) running T0/T1 gateways and providing north-south routing, NAT, load balancing, DNS forwarder, and VPN services.

**ELM (Enhanced Linked Mode)**{: #elm-enhanced-linked-mode } — vCenter federation connecting multiple vCenter instances to share a common inventory view, roles, tags, permissions, and policies. Requires vCenter 7.0+; no separate PSC needed.

**Erasure Coding**{: #erasure-coding } — vSAN space-efficient redundancy method using parity striping. RAID-5 (FTT=1, minimum 4 hosts, 1.33× overhead) and RAID-6 (FTT=2, minimum 6 hosts, 1.5× overhead). See also: [FTT](#ftt-failures-to-tolerate).

**ESA (Express Storage Architecture)**{: #esa-express-storage-architecture } — vSAN 8.x architecture requiring NVMe-only devices. Eliminates disk groups in favour of a single-tier storage pool. Supports per-object compression (no dedup). See also: [OSA](#osa-original-storage-architecture).

**ESXi** — VMware type-1 bare-metal hypervisor. Runs the VMkernel directly on hardware, managing VMs, vNICs, VMkernel ports, and datastores. Configurable via DCUI, SSH, PowerCLI, or the vCenter REST API.

**EVC (Enhanced vMotion Compatibility)** — cluster feature masking newer CPU capabilities to a common baseline, enabling live vMotion migration of VMs between ESXi hosts with different CPU generations.

**Event** — vSphere or Aria Logs record of a discrete system action (VM power-on, host disconnect, certificate expiry). Distinct from an Alarm (threshold breach) and a raw syslog log entry.

---

## F

**Fault Domain** — vSAN stretched cluster unit mapping to a physical site or rack. vSAN distributes RAID object components across fault domains to survive a site failure (stretched cluster) or rack failure (rack awareness).

**FC (Fibre Channel)** — high-speed block storage networking protocol over a dedicated SAN fabric. Requires HBAs in ESXi hosts and FC switches. Supports multipathing via MPIO (Most Recently Used, Fixed, Round Robin).

**FCD (First Class Disk)** — vSphere managed disk object not tied to a VM life cycle. Used by the vSphere CSI driver as a Persistent Volume backing for Kubernetes workloads. Managed via the vCenter API independently of any VM.

**FIPS (Federal Information Processing Standard)** — US government cryptographic standard (FIPS 140-2). ESXi and vCenter support FIPS mode, restricting cipher suites to approved algorithms and requiring validated cryptographic modules.

**FT (Fault Tolerance)** — vSphere feature maintaining a live shadow VM on a second host using continuous, synchronous replication. Provides zero RPO and near-zero RTO. Limited to 4 vCPUs and restricted workload types.

**FTT (Failures to Tolerate)**{: #ftt-failures-to-tolerate } — vSAN storage policy parameter defining how many component failures (host, disk, or network partition) a VM object can survive. FTT=1 is the production minimum; FTT=2 is recommended for Tier-1 workloads.

---

## G

**Geneve (Generic Network Virtualization Encapsulation)** — UDP-based overlay encapsulation protocol used by NSX-T for the data plane. Carries extensible TLV metadata headers. Replaces VXLAN (used in NSX-V). See also: [VXLAN](#vxlan-virtual-extensible-lan).

**Guest Customization** — vSphere feature applying hostname, IP address, domain join, and run-once scripts to a cloned or deployed VM. Uses VMware Tools-integrated sysprep on Windows and cloud-init on Linux.

---

## H

**HA (vSphere High Availability)** — vSphere cluster feature restarting VMs on surviving hosts after an ESXi host failure. Requires shared storage. Uses Admission Control to reserve restart capacity. See also: [Admission Control](#admission-control).

**HBA (Host Bus Adapter)** — PCIe card connecting an ESXi host to a Fibre Channel or iSCSI SAN fabric. FC HBAs use WWN addressing; software iSCSI uses the standard NIC with iSCSI initiator.

**HCI (Hyper-Converged Infrastructure)** — architecture co-locating compute and storage on the same physical nodes. vSAN is VMware's HCI storage layer; VxRail is Dell's validated HCI appliance built on vSAN.

**HCX (VMware HCX)** — VMware workload mobility and network extension product. Provides live vMotion-style migration and bulk migration between on-premises and cloud sites with WAN optimisation and traffic engineering.

**Horizon** — VMware VDI and published application platform. Delivers virtual desktops and RDS-published apps. Key components: Connection Server (broker), Unified Access Gateway (UAG), Replica/Security Server, Composer.

**Host Isolation Response** — vSphere HA action taken when an ESXi host loses its management network but VMs remain running. Options: Leave Powered On, Power Off, or Shut Down. Configured per cluster.

**Host Profile** — vSphere policy capturing a reference ESXi host's configuration (networking, storage, security). Applied to detect and remediate configuration drift across cluster hosts.

---

## I

**Image (vLCM)** — vSphere Lifecycle Manager desired-state object combining a base ESXi version, vendor add-ons, and firmware specifications into a single cluster image. Remediation brings hosts to the image state.

**IP Pool** — NSX block of IP addresses assigned to Edge uplinks, Geneve Tunnel Endpoints (TEPs), or load balancer VIPs. Defined per transport zone or Edge cluster.

**iSCSI** — IP-based block storage protocol carrying SCSI commands over TCP/IP. Software iSCSI uses a standard NIC with VMkernel initiator; hardware iSCSI uses a dedicated HBA. Cost-effective alternative to FC on 25 GbE networks.

---

## J

**Jumbo Frames** — Ethernet frames with MTU larger than the standard 1500 bytes, typically 9000 bytes. Required for vSAN and vMotion VMkernel traffic to avoid fragmentation. Must be configured end-to-end on all physical switches and vDS uplinks.

---

## K

**KMIP (Key Management Interoperability Protocol)**{: #kmip-key-management-interoperability-protocol } — OASIS standard for communication between a KMS and a storage or compute client. vSAN and vCenter use KMIP to retrieve and return data encryption keys for D@RE and VM encryption.

**KMS (Key Management Server)** — external appliance storing and managing encryption keys. vCenter registers KMS clusters for vSAN D@RE and VM encryption. Common providers: HyTrust, Thales, HashiCorp Vault, and AWS KMS.

**kubeconfig** — Kubernetes client configuration file defining clusters, users, and contexts. `kubectl` reads `~/.kube/config` by default. Tanzu generates per-cluster kubeconfigs via `tanzu cluster kubeconfig get`.

**Kubernetes** — open-source container orchestration platform. In VMware environments, Tanzu provides Kubernetes on vSphere. NSX-T provides pod networking via the NCP plugin and Antrea as an alternative CNI.

---

## L

**LDAP** — Lightweight Directory Access Protocol for querying directory services (Active Directory, OpenLDAP). vCenter, NSX Manager, Aria products, and Horizon all support LDAP/LDAPS for user authentication and group membership.

**LCM (Lifecycle Manager)** — general abbreviation covering vSphere Lifecycle Manager (vLCM, ESXi patching) and Aria Suite LCM (deploying and upgrading Aria products). Context determines which is meant.

**Linked Mode** — see [ELM (Enhanced Linked Mode)](#elm-enhanced-linked-mode).

**Load Balancer (NSX)** — NSX service distributing traffic across backend server pools. Deployed on T1 gateways. Supports L4 (TCP/UDP) and L7 (HTTP/HTTPS) with health monitors, SSL offload, and session persistence.

---

## M

**Management Domain** — VCF initial domain containing vCenter, NSX Manager, SDDC Manager, and optionally Aria Suite components. Must be deployed before any workload domains can be provisioned.

**Micro-Segmentation** — security architecture enforcing DFW policies at the individual workload level (per vNIC). Prevents east-west lateral movement without requiring traffic to hairpin through a physical firewall. NSX DFW is the VMware implementation.

**Mirror (vSAN RAID-1)** — vSAN redundancy method storing identical copies of data on separate hosts. FTT=1 mirror requires a minimum of 3 hosts with 2× storage overhead. Simpler than erasure coding; works on any cluster size.

**MTU (Maximum Transmission Unit)** — maximum packet size in bytes on a network segment. Standard Ethernet: 1500. Jumbo frames: 9000. Must match end-to-end for VMkernel traffic (vSAN, vMotion, NFS, iSCSI) to avoid fragmentation.

---

## N

**Namespace (vSphere with Tanzu)** — vSphere abstraction mapping to a Kubernetes namespace. Enforces resource quotas (CPU, memory, storage) and controls which Tanzu clusters or VMs can be provisioned inside it.

**NAT (Network Address Translation)** — NSX service on T0/T1 gateways translating private VM IPs to public or routable addresses. Types: SNAT (source), DNAT (destination), Reflexive (stateful bidirectional).

**NCP (NSX Container Plugin)** — NSX-T component running in Kubernetes as a daemon set. Translates Kubernetes NetworkPolicy, Ingress, and LoadBalancer objects into NSX DFW rules, Segments, and LB virtual servers.

**Network Policy** — Kubernetes object controlling ingress and egress traffic between pods based on labels, namespaces, and ports. Enforced by the CNI (Antrea, NCP) in the kernel, not in user space.

**NFS (Network File System)** — file-based shared storage protocol. vSphere supports NFS v3 and v4.1. NFS datastores do not require HBAs; locking and access control are managed by the NFS server.

**NSX** — VMware network virtualization and security platform providing software-defined networking, micro-segmentation, and load balancing. NSX-T (current, kernel module based) supersedes NSX-V (deprecated, vSphere-embedded).

**NSX Manager** — NSX control and management plane appliance. Deployed as a 3-node cluster for production HA. Hosts the NSX UI, REST API, and policy configuration store.

**NSX-V** — legacy, vSphere-integrated version of NSX using VIBs embedded in vSphere. Officially end-of-life in 2022; migration to NSX-T required. Uses VXLAN encapsulation and DLR/ESG for routing.

**NUMA (Non-Uniform Memory Access)** — multi-socket server memory topology where a CPU socket accesses its local DIMM faster than a remote socket's DIMM. vSphere NUMA scheduling tries to keep VM vCPUs and vRAM within the same NUMA node.

**NVMe (Non-Volatile Memory Express)** — PCIe/CXL storage interface optimised for SSDs. Required for vSAN ESA. Delivers lower latency and higher IOPS than SAS/SATA SSDs. Supported as NVMe-oF over networks.

**NVMe-oF (NVMe over Fabrics)** — extends the NVMe protocol over networks using RDMA (RoCE, iWARP) or TCP. Provides near-local NVMe latency for shared storage. vSphere 7.0+ supports NVMe/TCP datastores.

---

## O

**OSA (Original Storage Architecture)**{: #osa-original-storage-architecture } — vSAN disk group model used in versions prior to 8.0. Each disk group contains one cache tier (SSD) and one or more capacity tiers. Supports dedup+compression on all-flash configurations. See also: [ESA](#esa-express-storage-architecture).

**OSPF (Open Shortest Path First)** — link-state IGP routing protocol. Not used by NSX gateways for external ToR peering (BGP is the standard), but commonly deployed in the underlay physical network.

**OVA/OVF (Open Virtualization Appliance/Format)** — portable VM package format. OVF is a directory structure; OVA is a single-file tar archive. Used to distribute vCenter, NSX Manager, Aria appliances, and vendor VMs.

**Overlay Network** — logical network encapsulated within a physical underlay using Geneve (NSX-T) or VXLAN (NSX-V). Decouples VM logical topology from physical switch topology, enabling cross-host Layer 2 segments.

---

## P

**PKI (Public Key Infrastructure)** — framework for issuing, managing, and revoking X.509 certificates. vSphere uses VMCA as an intermediate CA. Enterprise environments chain VMCA to an external root CA for full trust chain integration.

**Pod (Kubernetes)** — smallest deployable unit in Kubernetes, containing one or more containers sharing a network namespace and storage volumes. Each pod receives a unique cluster IP from the CNI plugin.

**PowerCLI** — VMware PowerShell module for automating vSphere, NSX, Horizon, SRM, vSAN, and Aria via API. Install: `Install-Module VMware.PowerCLI`. See the [PowerCLI cheat sheet](../cheat-sheets/powercli/).

**Principal Storage** — VCF concept defining the primary storage type for a workload domain (vSAN, NFS, FC). The principal storage type determines which storage policy capabilities are available in that domain.

**PSC (Platform Services Controller)** — deprecated vSphere component hosting SSO, certificate services, and licensing. Fully embedded into vCenter 7.0+. No longer deployed as a separate VM or appliance.

**PV/PVC (Persistent Volume / Persistent Volume Claim)** — Kubernetes storage abstraction. A PV is a provisioned storage resource; a PVC is a user request for storage. The vSphere CSI driver provisions PVs backed by FCDs on vSAN.

---

## Q

**Queue Depth** — number of I/O operations a storage adapter can process simultaneously. Insufficient queue depth on FC or iSCSI HBAs causes I/O queuing and latency spikes. Tuned via ESXi advanced settings per HBA and device.

---

## R

**RAID-5 / RAID-6** — see [Erasure Coding](#erasure-coding).

**RBAC (Role-Based Access Control)** — permission model assigning predefined or custom roles to users or groups on vCenter inventory objects. NSX, Aria, and Horizon each have their own independent RBAC systems.

**RDM (Raw Device Mapping)** — vSphere feature presenting a physical SAN LUN directly to a VM as a virtual disk. Used for shared disk clustering (MSCS) or applications requiring direct SCSI command access to the LUN.

**Recovery Plan**{: #recovery-plan } — SRM object defining the ordered sequence for failing over a set of VMs: power-on order, IP customization, network mapping, and pre/post recovery scripts. Tested non-disruptively via planned migration.

**RPO (Recovery Point Objective)** — maximum acceptable data loss in a DR event, expressed as time (e.g., 15 minutes). RPO drives replication frequency and technology choice: array replication gives near-zero; backup gives hours to days.

**RTO (Recovery Time Objective)** — maximum acceptable downtime in a DR event, expressed as time (e.g., 1 hour). RTO drives automation level: SRM Recovery Plan targets 15–30 min; manual backup restore targets 1–4 h.

---

## S

**SAML (Security Assertion Markup Language)** — XML-based SSO federation standard. vCenter, NSX, Aria products, and Horizon support SAML 2.0 for integration with enterprise IdPs such as ADFS, Okta, and Ping Identity.

**SAN (Storage Area Network)** — dedicated high-speed block storage network using Fibre Channel or iSCSI. Separated from IP management networks; accessed via HBAs with MPIO for redundancy.

**SDDC (Software-Defined Data Center)** — VMware concept of fully abstracting compute, storage, and networking via software. Implemented as full-stack VCF or as independent vSphere + vSAN + NSX deployments.

**SDDC Manager** — VCF management component orchestrating workload domain lifecycle: deployment, expansion, patching, and decommission. Provides a single API and UI for the entire VCF estate.

**Segment (NSX)** — NSX logical Layer 2 network. VMs connect to segments; segments connect upstream to T1 gateways. Can be overlay-backed (Geneve encapsulation) or VLAN-backed (direct physical VLAN access).

**Snapshot** — vSphere point-in-time capture of a VM's disk state using a delta VMDK. Not a backup replacement. Multiple chained snapshots degrade I/O performance. Used transiently during backup CBT scans and testing.

**SPBM (Storage Policy Based Management)** — vSphere framework defining storage capabilities (FTT, IOPS limit, encryption, compression) as named policies assigned per VMDK. vSAN enforces SPBM policies at the object level.

**SR-IOV (Single Root I/O Virtualization)** — PCIe feature exposing physical NIC virtual functions (VFs) directly to VMs, bypassing the hypervisor vSwitch. Used for latency-sensitive workloads and NSX bare-metal Edges.

**SRA (Storage Replication Adapter)** — SRM plugin supplied by a storage vendor (Pure Storage, NetApp, Dell) enabling SRM to discover replicated LUNs and orchestrate array-level replication during failover.

**SRM (Site Recovery Manager)** — VMware DR orchestration product managing Recovery Plans, network mapping, and IP customization for automated failover between two vCenter sites. See also: [Recovery Plan](#recovery-plan).

**SSO (Single Sign-On)** — vSphere identity service providing token-based authentication across vCenter, NSX, and Aria products. Backed by vCenter's embedded identity provider or an external LDAP/SAML IdP.

**Storage I/O Control (SIOC)** — vSphere feature throttling VM disk I/O shares on shared datastores during congestion. Prevents a single VM from monopolising VMFS or NFS datastore bandwidth.

**Stretched Cluster (vSAN)** — vSAN configuration spanning two sites with a witness VM at a third neutral site. Requires ≤5 ms synchronous round-trip latency between sites. Provides RPO=0 for site failure scenarios.

**Supervisor Cluster** — vSphere with Tanzu control-plane cluster enabling workload namespaces and the TKG service. Requires NSX-T or VDS-based networking and compatible storage (vSAN or NFS/FC with CNS support).

---

## T

**T0 Gateway** — NSX Tier-0 logical router handling north-south routing between the overlay network and the physical underlay. Peers with ToR switches via eBGP. Supports Active/Standby or ECMP Active/Active HA modes.

**T1 Gateway**{: #t1-gateway } — NSX Tier-1 logical router providing east-west routing and services (NAT, load balancing, DNS forwarder) for tenant workloads. Connected to the T0 via a transit segment. Typically one T1 per tenant or application tier.

**Tag (vSphere)** — metadata label applied to vSphere inventory objects (VMs, hosts, datastores, networks). Used to drive DRS affinity rules, SPBM storage policies, backup tool policies, and Aria Operations dashboards.

**Tanzu** — VMware Kubernetes portfolio including TKG (standalone), TKGS (vSphere-embedded), TAS (PaaS), and TMC (multi-cluster management). All editions use NSX-T or Antrea for pod networking.

**TAS (Tanzu Application Service)** — VMware PaaS platform (formerly Pivotal Cloud Foundry) for running 12-factor applications. Abstracts Kubernetes for developers and uses buildpacks to produce OCI container images.

**TKG (Tanzu Kubernetes Grid)** — standalone Kubernetes distribution deployable on vSphere, AWS, or Azure. Uses Cluster API for lifecycle management. Does not require a Supervisor Cluster (vSphere with Tanzu).

**TKGS (Tanzu Kubernetes Grid Service)** — Kubernetes embedded in vSphere via the Supervisor Cluster. Provisioned via vCenter UI or Kubernetes API using the `TanzuKubernetesCluster` CRD.

**TLS (Transport Layer Security)** — cryptographic protocol securing network connections. vSphere, NSX, Aria, and Horizon use TLS 1.2+ with certificate verification. FIPS mode restricts to approved cipher suites only.

**TMC (Tanzu Mission Control)** — SaaS platform managing multiple Kubernetes clusters (TKG, TKGS, EKS, AKS) from a single pane. Provides policy enforcement, cluster inspection, backup, and data protection.

**TPM (Trusted Platform Module)** — hardware security chip providing measured boot, attestation, and sealed key storage. ESXi 7.0+ supports TPM 2.0 for secure boot and integration with vSphere Trust Authority.

**Transport Node** — ESXi host or Edge node configured for the NSX data plane. Transport nodes have TEP (Tunnel Endpoint) VMkernel interfaces carrying Geneve-encapsulated overlay traffic. See also: [Transport Zone](#transport-zone).

**Transport Zone**{: #transport-zone } — NSX logical boundary defining which transport nodes share an overlay (Geneve) or VLAN-backed network. Segments created in a transport zone are reachable only by hosts registered to that zone.

**Thick / Thin Provisioning** — vSphere disk allocation strategies. Thick Eager Zeroed pre-allocates and zeros all blocks at creation for best performance. Thin allocates blocks on first write, conserving datastore space at the cost of potential performance variance.

---

## U

**Update Manager** — deprecated vSphere patching component replaced by vSphere Lifecycle Manager (vLCM) in vSphere 7.0. vLCM supports both baseline (legacy patch) and image-based (desired-state) remediation models.

**Uplink Profile (NSX)** — NSX configuration object defining teaming policy (active/standby, LACP), MTU, and transport VLAN for transport node physical NICs. Applied when preparing an ESXi host or Edge as a transport node.

---

## V

**vCHA (vCenter High Availability)** — vCenter 3-node cluster with active, passive, and witness VMs. Active/passive failover completes in approximately 3 minutes. Requires shared storage accessible to both the active and passive nodes.

**VCF (VMware Cloud Foundation)** — full SDDC stack bundling ESXi, vSAN, NSX, and SDDC Manager. Deployed as a management domain plus one or more workload domains. Supported on VxRail hardware or validated third-party servers.

**vDS (vSphere Distributed Switch)** — centrally managed virtual switch configured at the cluster level in vCenter. Provides consistent port groups, LACP, LLDP, IPFIX (NetFlow), and traffic shaping across all cluster hosts. Requires Enterprise Plus licensing.

**VIB (vSphere Installation Bundle)** — ESXi software package format for drivers, agents, and monitoring tools. Used for custom driver installation on baseline-managed clusters. Superseded by components in vLCM image-based management.

**VLAN (Virtual LAN)** — Layer 2 network segmentation via 802.1Q tagging. NSX VLAN-backed segments expose physical VLANs to VMs without overlay encapsulation. Used for management, storage, and vMotion VMkernel traffic.

**vLCM (vSphere Lifecycle Manager)** — vSphere image-based lifecycle management replacing Update Manager. Manages ESXi versions, vendor add-ons, and firmware as a single desired-state image applied to a cluster.

**VMDK (Virtual Machine Disk)** — vSphere virtual disk file format. The flat VMDK stores actual data; the descriptor VMDK stores metadata. Backed by VMFS, vSAN, or NFS datastores. Used as PV backing via the vSphere CSI driver.

**VMFS (VM File System)** — VMware clustered filesystem on block storage (FC or iSCSI). Multiple ESXi hosts concurrently mount the same VMFS volume. VMFS 6 supports automatic space reclamation via UNMAP.

**vMotion** — vSphere live migration of a running VM between ESXi hosts with no downtime. Requires shared storage (or Storage vMotion for concurrent disk migration). Uses a dedicated VMkernel port; recommended 10 GbE or higher.

**vNIC (Virtual NIC)** — virtual network adapter presented to a VM. Recommended type: VMXNET3 (paravirtual). SR-IOV VFs bypass the vSwitch entirely for maximum throughput at the cost of vMotion compatibility.

**vSAN** — VMware hyper-converged storage using local disks across ESXi cluster nodes to present a shared datastore. Available as OSA (disk groups) or ESA (NVMe pool). Storage policies enforced per VMDK via SPBM.

**vSAN ESA** — see [ESA (Express Storage Architecture)](#esa-express-storage-architecture).

**vSAN File Service** — vSAN feature exposing NFS v4.1 and SMB file shares directly from the vSAN datastore. Enables file-based workloads (CNS ReadWriteMany volumes, shared app data) without a separate NAS appliance.

**vSAN OSA** — see [OSA (Original Storage Architecture)](#osa-original-storage-architecture).

**vSphere with Tanzu** — vSphere feature enabling Kubernetes workloads alongside VMs on the same ESXi cluster via a Supervisor Cluster. Requires NSX-T or VDS networking and compatible storage.

**vSwitch (vSphere Standard Switch)** — per-host virtual switch in ESXi providing basic port groups and uplink teaming. Configuration is host-local and not centrally managed; replaced by vDS for cluster-wide consistency.

**VXLAN (Virtual Extensible LAN)**{: #vxlan-virtual-extensible-lan } — UDP-based Layer 2 overlay encapsulation (RFC 7348) used by NSX-V. Replaced by Geneve in NSX-T. Still appears in third-party SDN solutions and legacy NSX-V environments.

**VxRail** — Dell Technologies HCI appliance built on VMware vSAN. Shipped as a pre-validated node running ESXi + vSAN, with optional NSX and VCF integration. Managed via the VxRail Manager plugin in vCenter.

---

## W

**Witness Appliance** — lightweight VM hosted at a third neutral site (or management cluster) providing tie-breaking quorum for a vSAN 2-node or stretched cluster. Stores metadata only — no VM data.

**Workload Domain** — VCF logical grouping of ESXi hosts, vSAN storage, and NSX network segments managed as a unit by SDDC Manager. Separate from the management domain; provisioned on demand for tenant workloads.

**Workspace ONE Access** — VMware identity manager providing SAML-based SSO for Aria Suite products (formerly VMware Identity Manager / vIDM). Must be deployed before other Aria Suite components when using LCM for a full-stack install.

---

*155+ terms · Last updated: 2026-06-18*
