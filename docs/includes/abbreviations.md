<!-- Global abbreviations — auto-appended to every page via pymdownx.snippets -->

*[vSAN]: vSphere Storage Area Network — VMware's software-defined HCI storage layer
*[VMFS]: Virtual Machine File System — VMware's clustered filesystem for ESXi datastores
*[VMDK]: Virtual Machine Disk — the disk image format used by VMware VMs
*[OVA]: Open Virtual Appliance — a packaged VM template (single-file .ova archive)
*[OVF]: Open Virtualization Format — the open standard for packaging VM images
*[ESXi]: VMware's type-1 bare-metal hypervisor (Elastic Sky X Integrated)
*[VCSA]: vCenter Server Appliance — the Linux-based vCenter deployment
*[VAMI]: Virtual Appliance Management Interface — VCSA's appliance admin web UI (port 5480)
*[VMCA]: VMware Certificate Authority — vCenter's internal CA for signing host and solution certificates
*[STS]: Security Token Service — vCenter SSO component that issues SAML tokens
*[SSO]: Single Sign-On — vCenter's identity federation layer (vsphere.local domain)
*[VCF]: VMware Cloud Foundation — Broadcom's integrated SDDC stack (vSphere + vSAN + NSX + Aria)
*[SDDC]: Software-Defined Data Center — an abstraction layer for compute, storage, and networking
*[DRS]: Distributed Resource Scheduler — vSphere feature for automated VM load balancing across hosts
*[HA]: High Availability — vSphere feature that restarts VMs on surviving hosts after a host failure
*[FTT]: Failures to Tolerate — vSAN storage policy parameter defining redundancy level
*[vDS]: vSphere Distributed Switch — a centrally managed virtual switch spanning multiple ESXi hosts
*[VDS]: vSphere Distributed Switch — a centrally managed virtual switch spanning multiple ESXi hosts
*[VADP]: vStorage APIs for Data Protection — VMware's agentless backup integration framework
*[VDDK]: Virtual Disk Development Kit — VMware SDK for reading/writing VMDK data (used by VADP proxies)
*[CBT]: Changed Block Tracking — VMware API that tracks which VMDK blocks changed since last backup
*[vMotion]: VMware live VM migration between ESXi hosts without downtime
*[ELM]: Enhanced Linked Mode — vCenter feature linking multiple vCenter instances to a shared SSO domain
*[VECS]: VMware Endpoint Certificate Store — the certificate store on VCSA that holds machine SSL and solution certs
*[NSX]: VMware's software-defined networking and security platform (formerly NSX-T)
*[TEP]: Tunnel Endpoint — NSX overlay network termination point on ESXi hosts (VXLAN/Geneve)
*[N-VDS]: NSX Virtual Distributed Switch — NSX-managed data-plane switch replacing VDS in NSX-T 2.x
*[VTI]: Virtual Tunnel Interface — NSX point-to-point IPsec tunnel interface
*[VTEP]: VXLAN Tunnel Endpoint — the interface that encapsulates/decapsulates VXLAN frames
*[TKG]: Tanzu Kubernetes Grid — VMware's Kubernetes distribution on vSphere Supervisor
*[TKGm]: Tanzu Kubernetes Grid Multicloud — standalone TKG for multi-cloud deployments
*[CAPV]: Cluster API Provider vSphere — the Kubernetes Cluster API driver for vSphere
*[CSI]: Container Storage Interface — Kubernetes standard API for storage drivers
*[CNI]: Container Network Interface — Kubernetes standard API for network plugins

*[IOPS]: Input/Output Operations Per Second — storage throughput metric
*[NVMe]: Non-Volatile Memory Express — high-performance storage protocol over PCIe
*[NFS]: Network File System — network-based file sharing protocol (TCP 2049)
*[SMB]: Server Message Block — Windows network file sharing protocol (TCP 445)
*[iSCSI]: Internet Small Computer System Interface — block storage over TCP/IP (port 3260)
*[FC]: Fibre Channel — high-speed block storage networking protocol
*[FCP]: Fibre Channel Protocol — the SCSI transport layer running over Fibre Channel
*[FCIP]: Fibre Channel over IP — tunneling FC frames over IP/Ethernet networks
*[RAID]: Redundant Array of Independent Disks — data redundancy via disk striping and mirroring
*[HDD]: Hard Disk Drive — traditional spinning magnetic storage disk
*[SSD]: Solid State Drive — flash-based storage with no moving parts
*[ONTAP]: NetApp's operating system for all-flash and hybrid storage arrays
*[WAFL]: Write Anywhere File Layout — NetApp's ONTAP filesystem that enables instant snapshots
*[FlexVol]: NetApp flexible volume — a storage container in ONTAP with independent policies
*[FlexGroup]: NetApp scale-out NAS volume — a single namespace distributed across many nodes
*[SnapMirror]: NetApp async or sync replication from one ONTAP volume to another
*[SnapVault]: NetApp backup-to-secondary ONTAP feature (snapshot-based, disk-to-disk)
*[SRDF]: Symmetrix Remote Data Facility — Dell/EMC PowerMax synchronous/asynchronous replication
*[SOBR]: Scale-Out Backup Repository — Veeam tiered repository combining fast disk + object storage
*[VBK]: Veeam Backup — full backup file format (.vbk)
*[VIB]: Veeam Incremental Backup — incremental backup file format (.vib)
*[GFS]: Grandfather-Father-Son — backup retention scheme with daily/weekly/monthly/yearly tiers
*[CEPH]: A distributed object, block, and file storage platform (open-source)
*[OSD]: Object Storage Daemon — a Ceph process that manages a single storage disk
*[MON]: Ceph Monitor — a Ceph component that maintains cluster state and quorum
*[MGR]: Ceph Manager — a Ceph component that handles metrics, dashboards, and modules
*[RGW]: RADOS Gateway — Ceph's S3/Swift-compatible object storage front-end
*[RBD]: RADOS Block Device — Ceph's block storage interface for VMs and containers
*[PG]: Placement Group — Ceph's internal unit for data distribution across OSDs

*[VLAN]: Virtual Local Area Network — Layer 2 network segmentation using 802.1Q tags
*[VXLAN]: Virtual Extensible LAN — Layer 2 overlay encapsulated in UDP (port 4789) for large-scale networks
*[MTU]: Maximum Transmission Unit — the largest packet size a network interface will transmit
*[BGP]: Border Gateway Protocol — the Internet's path-vector routing protocol (TCP 179)
*[OSPF]: Open Shortest Path First — a link-state interior gateway routing protocol
*[ECMP]: Equal-Cost Multi-Path — routing technique using multiple equal-cost paths simultaneously
*[LAG]: Link Aggregation Group — bonding multiple physical NICs into one logical interface (802.3ad)
*[LACP]: Link Aggregation Control Protocol — 802.3ad protocol for dynamic LAG negotiation
*[HCL]: Hardware Compatibility List — VMware's list of certified hardware for ESXi

*[RPO]: Recovery Point Objective — the maximum acceptable data loss measured in time
*[RTO]: Recovery Time Objective — the maximum acceptable downtime before service must be restored
*[DR]: Disaster Recovery — the strategy and process for restoring IT services after a major outage
*[BC]: Business Continuity — the overall plan to maintain operations during a disruption
*[CMDB]: Configuration Management Database — the authoritative record of IT assets and their relationships
*[CAB]: Change Advisory Board — the governance body that reviews and approves change requests
*[ITSM]: IT Service Management — the set of practices for delivering and managing IT services

*[LDAP]: Lightweight Directory Access Protocol — directory service query protocol (TCP 389)
*[LDAPS]: LDAP over TLS — encrypted directory query protocol (TCP 636)
*[SAML]: Security Assertion Markup Language — XML-based SSO federation standard
*[OIDC]: OpenID Connect — OAuth 2.0-based identity layer for SSO
*[OAuth]: Open Authorization — protocol for delegated access to resources without sharing credentials
*[JWT]: JSON Web Token — compact, URL-safe token format for claims between parties
*[TLS]: Transport Layer Security — cryptographic protocol for secure communications (successor to SSL)
*[PKI]: Public Key Infrastructure — the framework of CAs, certificates, and policies for managing digital identities
*[CA]: Certificate Authority — an entity that signs and issues digital certificates
*[CSR]: Certificate Signing Request — a block of encoded data sent to a CA to obtain a signed certificate
*[CRL]: Certificate Revocation List — a list of certificates that have been revoked before expiry
*[OCSP]: Online Certificate Status Protocol — a real-time alternative to CRL for checking certificate validity
*[MFA]: Multi-Factor Authentication — authentication requiring two or more verification factors
*[PAM]: Privileged Access Management — tools and policies for controlling access to privileged accounts
*[RBAC]: Role-Based Access Control — access model where permissions are assigned to roles, not individuals
*[SSO]: Single Sign-On — authentication that grants access to multiple systems with one login

*[API]: Application Programming Interface — a set of definitions for how software components communicate
*[REST]: Representational State Transfer — an architectural style for stateless HTTP APIs
*[CLI]: Command-Line Interface — a text-based interface for interacting with software
*[GUI]: Graphical User Interface — a visual interface for interacting with software
*[SDK]: Software Development Kit — a collection of tools and libraries for building applications
*[CI/CD]: Continuous Integration / Continuous Delivery — automated software build, test, and deploy pipelines
*[IaC]: Infrastructure as Code — managing infrastructure through version-controlled configuration files
*[HCL]: HashiCorp Configuration Language — the declarative language used by Terraform
*[YAML]: YAML Ain't Markup Language — a human-readable data serialisation format used in configuration files
*[JSON]: JavaScript Object Notation — a lightweight data interchange format
*[VM]: Virtual Machine — an emulated computer running on a hypervisor
*[KVM]: Kernel-based Virtual Machine — Linux's built-in Type-1 hypervisor
*[CPU]: Central Processing Unit — the primary computation component of a computer
*[RAM]: Random Access Memory — fast, volatile memory used for active workloads
*[vCPU]: Virtual CPU — a CPU core assigned to a virtual machine
*[NUMA]: Non-Uniform Memory Access — server architecture where CPU memory access latency varies by proximity
*[BIOS]: Basic Input/Output System — firmware that initialises hardware during boot
*[UEFI]: Unified Extensible Firmware Interface — the modern replacement for BIOS
*[PCI]: Peripheral Component Interconnect — the bus standard for connecting expansion cards
*[PCIe]: PCI Express — the high-speed serial bus standard for GPUs, NVMe SSDs, and NICs
*[NIC]: Network Interface Card — a hardware component providing network connectivity
*[HBA]: Host Bus Adapter — a card connecting a server to a storage network (FC or iSCSI)
*[ILO]: Integrated Lights-Out — HPE's out-of-band server management interface
*[iDRAC]: Integrated Dell Remote Access Controller — Dell's out-of-band server management interface
*[IPMI]: Intelligent Platform Management Interface — a standard for out-of-band server management
