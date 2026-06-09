---
title: VCP-DCV 8 Exam Reference
---

# VCP-DCV 8 — Exam Reference (2V0-21.23)

<div class="kb-summary">
Maps VCP-DCV 8 exam objectives (exam code 2V0-21.23) to KB content pages. Use this page to navigate from each exam section to the relevant technical reference. Includes a sample question analysis section that explains correct answers and the reasoning behind them.
</div>

```text
┌──────────────────────── VCP-DCV 8 (2V0-21.23) — Exam Blueprint Map ────────────────────────────────────┐
│                                                                                                       │
│   70 questions / 135 min / pass 300 of 500 / Pearson VUE / 2-year recertification required            │
│   Section 1 (Architecture) is the largest — weight study time there first                             │
│   Prerequisite: VMware vSphere Install Configure Manage course or equivalent                          │
│                                                                                                       │
│   Section 1 — Architecture & Technologies (largest section)                                           │
│   ESXi + vCenter architecture; vSAN disk groups and FTT; storage (VAAI/VASA/SPBM/vVOLs)               │
│   Networking: VSS vs VDS, NIOC, PVLAN modes; Security: vTA, vTPM, VM Encryption, VBS                  │
│                                                                                                       │
│   Section 2 — Products & Solutions                                                                    │
│   vSphere in the SDDC context; SRM + vSphere Replication (RTO/RPO); DPU/Distributed Services          │
│   Tanzu: Supervisor cluster, Namespaces, vSphere Pods, TKG integration with vSphere                   │
│                                                                                                       │
│   Section 4 — Installing, Configuring, and Setup                                                      │
│   SSO + identity sources (AD LDAP, ADFS federation); VDS/VSS configuration; HA and DRS config         │
│   vLCM + Host Profiles; VCSA deployment sizing; vCenter HA (VCHA) active/passive/witness              │
│                                                                                                       │
│   Section 5 — Performance & Upgrades                                                                  │
│   Resource pools: shares, reservations, limits; NIOC/SIOC thresholds; snapshot disk impact            │
│   vLCM staged remediation and compliance; Skyline Advisor Pro; Update Planner for vCenter             │
│                                                                                                       │
│   Section 6 — Troubleshooting                                                                         │
│   vCLS retreat mode: DRS goes manual, HA Optimal Placement disabled (HA restarts still work)          │
│   Log files: vmkernel.log, vpxd.log, fdm.log, hostd.log, vpxa.log; vm-support bundle collection       │
│   ESXTOP counters: %RDY (CPU contention), DAVG (storage latency), balloon/swap (memory)               │
│                                                                                                       │
│   Section 7 — Administrative Tasks                                                                    │
│   Snapshot management: create/revert/delete/consolidate; vMotion + Storage vMotion                    │
│   DRS affinity/anti-affinity rules; SPBM storage policy assignment and compliance checks              │
│                                                                                                       │
│   Key terms:                                                                                          │
│   VAAI  = vStorage APIs for Array Integration; offloads full-copy, block-zero, locking to array       │
│   VASA  = vSphere APIs for Storage Awareness; array reports capabilities to vCenter for SPBM          │
│   vTA   = vSphere Trust Authority; hardware-rooted trust chain for encrypted VMs                      │
│   VBS   = Virtualization-Based Security; Windows feature requiring vTPM and UEFI VM firmware          │
│   vCLS  = vSphere Cluster Services; retreat mode stops DRS automation and HA optimal placement        │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Exam Overview

| Item | Detail |
|---|---|
| **Exam Code** | 2V0-21.23 |
| **Certification** | VMware Certified Professional — Data Center Virtualization (VCP-DCV) 8 |
| **Number of Questions** | 70 |
| **Duration** | 135 minutes |
| **Passing Score** | 300 out of 500 |
| **Testing Platform** | Pearson VUE |
| **Language** | English (and other languages) |
| **Prerequisite** | VCP-DCV 2023 course requirement (VMware vSphere: Install, Configure, Manage or equivalent) |
| **Exam Guide** | Available at vmware.com/education-services |

> **VCP-DCV Exam Note:** The score scale of 300/500 does not mean you need 60%. VMware uses a scaled scoring system — the passing threshold is calibrated against question difficulty. Aim to answer approximately 65–70% of questions correctly, though the exact equivalence varies per exam form.

---

## Section 1 — Architecture and Technologies

This section covers the foundational concepts of vSphere architecture, storage, networking, and security. It is typically the largest section on the exam.

### 1.1 — vSphere Prerequisites and ESXi Architecture

**Objectives:** Understand ESXi hardware requirements, supported server hardware, BIOS vs UEFI, memory requirements, and the role of the VMkernel.

| KB Reference | Content |
|---|---|
| [ESXi Architecture and Operations](../../../vmware/esxi/) | Host stack, VMkernel, storage adapters, networking adapters |
| [vCenter Architecture](../../../vmware/vcenter/) | vCenter Server Appliance topology, PSC integration, SSO |

---

### 1.2 — vCenter Architecture

**Objectives:** Describe vCenter Server components (VCSA, PSC, SSO), vCenter HA (VCHA), Enhanced Linked Mode, and the vCenter Appliance Management Interface (VAMI).

| KB Reference | Content |
|---|---|
| [vCenter Architecture](../../../vmware/vcenter/architecture/) | VCSA deployment, PSC, SSO, VCHA active/passive/witness |

---

### 1.3 — Storage Concepts

**Objectives:** Identify and explain NFS, iSCSI, and FC SAN protocols. Understand VAAI, VASA, SPBM, vSAN, vVOLs, RDMs, SIOC, and datastore clusters.

| KB Reference | Content |
|---|---|
| [vSphere Storage Concepts](../concepts/vsphere-storage/) | All storage protocols, SPBM, vVOLs, RDMs, SIOC, datastore clusters |
| [vSAN Architecture](../../../vmware/vsan/architecture/) | vSAN cluster architecture, fault domains, policies |

> **VCP-DCV Exam Note:** **VAAI** offloads storage operations (full copy, block zero, locking) to the array. **VASA** allows arrays to report their capabilities to vCenter for SPBM policy matching. **SPBM** is the policy layer that maps VM storage requirements to datastore capabilities — it is the link between VASA (what the array can do) and VM storage profiles (what the VM needs).

---

### 1.4 — ESXi Cluster Features (DRS, EVC, HA, FT)

**Objectives:** Explain DRS load balancing, EVC mode purpose, HA admission control, FT requirements and limitations.

| KB Reference | Content |
|---|---|
| [Cluster Services — DRS, HA, FT, and EVC](../concepts/cluster-services/) | All cluster services, configuration, requirements |

---

### 1.5 — vSphere Networking (VSS, VDS, VMkernel, NIOC)

**Objectives:** Compare VSS and VDS. Identify VMkernel adapter types. Explain networking policies, NIOC, PVLAN, and multiple TCP/IP stacks.

| KB Reference | Content |
|---|---|
| [vSphere Networking Concepts](../concepts/vsphere-networking/) | VSS/VDS comparison, VMkernel types, NIOC traffic types, PVLAN |

---

### 1.6 — vSphere Lifecycle Manager (vLCM)

**Objectives:** Distinguish image-based from baseline-based management. Explain cluster images, Quick Boot, and the remediation workflow.

| KB Reference | Content |
|---|---|
| [vSphere Lifecycle Management](../concepts/vsphere-lifecycle/) | vLCM, cluster images, Quick Boot, Update Planner |

---

### 1.7 — vSAN Basics

**Objectives:** Explain vSAN cluster architecture, disk groups, fault tolerance (FTT), storage policies, and vSAN datastore.

| KB Reference | Content |
|---|---|
| [vSAN Architecture](../../../vmware/vsan/architecture/) | Disk groups, fault domains, FTT, vSAN policies |

---

### 1.8 — VM Encryption and vSphere Trust Authority (vTA)

**Objectives:** Describe VM encryption (data-at-rest), vTA architecture, key providers (KMS and vTA), and encrypted vMotion.

| KB Reference | Content |
|---|---|
| [vSphere Security Concepts](../concepts/vsphere-security/) | VM encryption, vSphere Trust Authority, KMS integration |

---

### 1.9 — VM Security (vTPM, BIOS/UEFI, VBS)

**Objectives:** Explain virtual TPM (vTPM) requirements and use cases, BIOS vs UEFI VM firmware, and Virtualization-Based Security (VBS) for Windows VMs.

| KB Reference | Content |
|---|---|
| [vSphere Security Concepts](../concepts/vsphere-security/) | vTPM, VBS, VM firmware options |

---

### 1.10 — Identity Federation

**Objectives:** Describe vCenter identity federation with external identity providers (Active Directory Federation Services, Okta), the role of External Identity Provider Federation (ADFS), and vCenter SSO.

| KB Reference | Content |
|---|---|
| [vSphere Security Concepts](../concepts/vsphere-security/) | SSO, identity federation, external IdP configuration |

---

### 1.11 — DPU / Distributed Services Engine

**Objectives:** Explain the role of Data Processing Units (DPUs/SmartNICs) in vSphere, how the Distributed Services Engine offloads network and storage processing.

| KB Reference | No dedicated KB page yet — see VMware documentation |
|---|---|
| Vendor documentation | Pensando/AMD, Nvidia BlueField DPU integration with ESXi 8.0 |

---

### 1.12 — VMware Tools

**Objectives:** Describe VMware Tools components, how they improve VM performance and manageability, and how to manage Tools versions.

| KB Reference | Content |
|---|---|
| [vCenter Operations](../../../vmware/vcenter/operations/) | VMware Tools management, updating, open-vm-tools |

---

### 1.13 — vSphere with Tanzu

**Objectives:** Describe the Supervisor cluster concept, Namespaces, vSphere Pods, and Tanzu Kubernetes Grid integration with vSphere.

| KB Reference | Content |
|---|---|
| [Tanzu on vSphere](../../../vmware/tanzu/) | Supervisor cluster, Namespaces, vSphere Pods, TKG |

---

## Section 2 — Products and Solutions

### 2.1 — vSphere in the SDDC

**Objectives:** Understand how vSphere fits within the VMware Software-Defined Data Center (SDDC) alongside NSX, vSAN, and VMware Cloud Foundation (VCF).

| KB Reference | Content |
|---|---|
| [VMware Cloud Foundation](../../../vmware/vmware-cloud-foundation/) | VCF architecture, BOM, SDDC Manager, bring-up process |

---

### 2.4 — Disaster Recovery Use Cases (SRM, vSphere Replication)

**Objectives:** Explain RTO/RPO concepts, SRM failover workflow, vSphere Replication as a DR transport, and recovery plan configuration.

| KB Reference | Content |
|---|---|
| [Site Recovery Manager (SRM)](../../../vmware/srm/) | SRM architecture, protection groups, recovery plans |
| [vSphere Replication](../../../vmware/vsphere-replication/) | Replication targets, RPO configuration, failover |

> **VCP-DCV Exam Note:** **RTO** (Recovery Time Objective) is how long recovery takes. **RPO** (Recovery Point Objective) is how much data loss is acceptable. vSphere Replication minimum RPO is **5 minutes**. SRM orchestrates the failover — it does not replicate data itself. SRM can use vSphere Replication or array-based replication as the underlying data transport.

---

## Section 4 — Installing, Configuring, and Setup

### 4.1 — SSO Configuration

**Objectives:** Configure vCenter Single Sign-On, add identity sources (AD over LDAP, Integrated Windows Auth), manage SSO users and groups.

| KB Reference | Content |
|---|---|
| [vCenter Security and SSO](../../../vmware/vcenter/architecture/) | SSO domains, identity sources, STS token configuration |

---

### 4.2–4.3 — VDS and VSS Configuration

**Objectives:** Create and configure vSphere Standard Switches and Distributed Switches. Configure uplink teaming, port groups, and VLANs.

| KB Reference | Content |
|---|---|
| [vSphere Networking Concepts](../concepts/vsphere-networking/) | VSS/VDS creation, port group VLAN modes, uplink policies |

---

### 4.5 — VCSA Deployment

**Objectives:** Deploy the vCenter Server Appliance using the installer, understand Stage 1 (OVA deployment) vs Stage 2 (configuration), and configure VCSA sizing.

| KB Reference | Content |
|---|---|
| [vCenter Deployment](../../../vmware/vcenter/deploy/) | VCSA installer, deployment sizing, initial configuration |

---

### 4.6 — HA and DRS Configuration

**Objectives:** Configure vSphere HA admission control policies (percentage, failover hosts, slot-based), configure DRS automation levels, and set VM-Host affinity/anti-affinity rules.

| KB Reference | Content |
|---|---|
| [Cluster Services — DRS, HA, FT](../concepts/cluster-services/) | HA admission control options, DRS automation levels, rules |

---

### 4.7 — vCenter HA (VCHA)

**Objectives:** Explain VCHA active/passive/witness topology, automatic vs manual failover, and VCHA requirements.

| KB Reference | Content |
|---|---|
| [vCenter Architecture — How It Works](../../../vmware/vcenter/architecture/how-it-works/) | VCHA topology, failover triggers, RPO (near-zero) |

---

### 4.8–4.10 — Content Library

**Objectives:** Create and configure Content Libraries (local, published, subscribed). Deploy VMs from library templates and manage template versions.

| KB Reference | Content |
|---|---|
| [vSphere Lifecycle Management](../concepts/vsphere-lifecycle/) | Content Library types, publish/subscribe, template deployment |

---

### 4.12 — vSphere Trust Authority

**Objectives:** Configure vSphere Trust Authority, trusted hosts, key providers, and encrypted VM deployment in a vTA environment.

| KB Reference | Content |
|---|---|
| [vSphere Security Concepts](../concepts/vsphere-security/) | vTA architecture, trusted cluster, key provider config |

---

### 4.13 — Certificate Management

**Objectives:** Understand VMCA (VMware Certificate Authority) and its role in vSphere, replace machine SSL certificates, and configure custom CA certificates.

| KB Reference | Content |
|---|---|
| [PKI and Certificate Management](../../standards/) | VMCA, certificate replacement, VECS, certificate stores |
| [vCenter Security](../../../vmware/vcenter/) | Certificate management from vCenter UI and certmgr |

---

### 4.14 — vLCM Configuration

**Objectives:** Configure vLCM depots, create cluster images, stage and remediate hosts, enable Quick Boot.

| KB Reference | Content |
|---|---|
| [vSphere Lifecycle Management](../concepts/vsphere-lifecycle/) | vLCM setup, depot configuration, image creation, remediation |

---

### 4.16 — Host Profiles

**Objectives:** Create host profiles from a reference host, attach to clusters, run compliance checks, and manage answer files for host-specific settings.

| KB Reference | Content |
|---|---|
| [vSphere Lifecycle Management](../concepts/vsphere-lifecycle/) | Host profiles, answer files, compliance checks, remediation |

---

### 4.17 — ESXi Boot Options (Secure Boot, Quick Boot)

**Objectives:** Configure Secure Boot for ESXi, explain the Secure Boot chain of trust, and identify Quick Boot hardware requirements.

| KB Reference | Content |
|---|---|
| [vSphere Lifecycle Management](../concepts/vsphere-lifecycle/) | Secure Boot chain, Quick Boot requirements (UEFI, no passthrough) |

---

### 4.19 — ESXi Host Configuration and Hardening

**Objectives:** Configure lockdown mode (normal and strict), manage ESXi firewall rules, configure NTP, and harden ESXi host settings.

| KB Reference | Content |
|---|---|
| [ESXi Security](../../../vmware/esxi/) | Lockdown modes, firewall, SSH/Shell management, syslog |

---

### 4.20 — vSphere with Tanzu Deployment

**Objectives:** Enable vSphere with Tanzu on a cluster, configure Supervisor Namespaces, and manage workload management settings.

| KB Reference | Content |
|---|---|
| [Tanzu Deployment](../../../vmware/tanzu/deploy/) | Supervisor cluster enablement, Namespace configuration |

---

## Section 5 — Performance and Upgrades

### 5.1 — Resource Pools

**Objectives:** Configure resource pools with CPU/memory shares, reservations, and limits. Explain expandable reservations and the resource pool tree.

| KB Reference | Content |
|---|---|
| [Cluster Services — Resource Pools](../concepts/cluster-services/) | Shares, reservations, limits, expandable reservations |

---

### 5.3–5.5 — NIOC, SIOC, and Performance Monitoring

**Objectives:** Configure NIOC traffic shares and limits. Explain SIOC thresholds for I/O prioritization. Interpret performance charts for CPU, memory, disk, and network.

| KB Reference | Content |
|---|---|
| [vSphere Networking — NIOC](../concepts/vsphere-networking/) | NIOC traffic types, shares, limits, VDS requirement |
| [vSphere Monitoring](../concepts/vsphere-monitoring/) | Performance charts, key metrics, ESXTOP, thresholds |

---

### 5.7 — Snapshot Performance

**Objectives:** Explain the performance impact of VM snapshots (snapshot chains, delta disks), best practices for snapshot management, and consolidation.

| KB Reference | Content |
|---|---|
| [vCenter Operations — Snapshots](../../../vmware/vcenter/operations/) | Snapshot chains, delta disk types, consolidation, impact |

---

### 5.9 — vLCM Updates and Patching

**Objectives:** Use vLCM to stage and apply updates, use Update Planner for vCenter upgrades, and validate post-update compliance.

| KB Reference | Content |
|---|---|
| [vSphere Lifecycle Management](../concepts/vsphere-lifecycle/) | Update Planner, staged remediation, compliance verification |

---

### 5.11 — Skyline

**Objectives:** Describe Skyline data collection, health checks, advisory recommendations, and how Skyline integrates with VMware support.

| KB Reference | Content |
|---|---|
| [vSphere Monitoring — Skyline](../concepts/vsphere-monitoring/) | Skyline telemetry, Advisor Pro, Aria Operations comparison |

---

## Section 6 — Troubleshooting

### 6.1 — vCLS Retreat Mode

**Objectives:** Explain when to use vCLS retreat mode, its impact on HA Optimal Placement and DRS, and how to enable/disable it.

| KB Reference | Content |
|---|---|
| [vSphere Monitoring — vCLS Retreat Mode](../concepts/vsphere-monitoring/) | Retreat mode trigger, HA impact, DRS impact, re-enabling vCLS |

---

### 6.2 — Log File Locations and Contents

**Objectives:** Identify key ESXi and vCenter log files by name and purpose (vmkernel.log, fdm.log, vpxd.log, hostd.log, vpxa.log).

| KB Reference | Content |
|---|---|
| [vSphere Monitoring — Log Files](../concepts/vsphere-monitoring/) | Full table of log files, locations, contents |

---

### 6.3 — Log Bundle Collection

**Objectives:** Generate an ESXi support bundle using vm-support. Generate a vCenter support bundle from VAMI or the API. Understand what is included in each bundle.

| KB Reference | Content |
|---|---|
| [vSphere Monitoring — Log Bundle](../concepts/vsphere-monitoring/) | vm-support commands, VCSA VAMI bundle, API method |
| ESXi Troubleshooting | Host support bundle collection, log forwarding to syslog |

---

## Section 7 — Administrative Tasks

### 7.1 — Snapshot Management

**Objectives:** Create, revert, and delete VM snapshots. Understand snapshot consolidation and the impact of long-lived snapshots.

| KB Reference | Content |
|---|---|
| [vCenter Operations — Snapshots](../../../vmware/vcenter/operations/) | Snapshot workflow, consolidation, disk growth, best practices |

---

### 7.2–7.3 — VM Management

**Objectives:** Perform cold and hot migrations (vMotion, Storage vMotion). Configure VM hardware (CPU, memory, disks, NICs) and VM options (boot options, VMware Tools settings).

| KB Reference | Content |
|---|---|
| [vCenter Operations](../../../vmware/vcenter/operations/) | vMotion, Storage vMotion, VM hardware configuration |

---

### 7.4 — Storage Management

**Objectives:** Create and manage VMFS and NFS datastores. Expand datastores, manage storage policies (SPBM), and manage multipathing (PSPs, SASPs).

| KB Reference | Content |
|---|---|
| [vSphere Storage Concepts](../concepts/vsphere-storage/) | Datastore types, VMFS expansion, PSPs, SPBM, vVOLs |

---

### 7.5 — DRS Rules

**Objectives:** Configure VM-VM affinity rules (keep together / keep apart) and VM-Host rules (must run on / should run on). Understand the precedence of mandatory vs optional rules.

| KB Reference | Content |
|---|---|
| [Cluster Services — DRS Rules](../concepts/cluster-services/) | Affinity/anti-affinity, VM-Host rules, mandatory vs optional |

---

## Sample Question Analysis

The following questions represent the type of scenario-based questions on the 2V0-21.23 exam. Each answer is explained with the underlying reasoning.

---

### Question 1

**A vSphere administrator notices VMs are experiencing high CPU latency. ESXTOP shows %RDY values of 25 ms per 20-second interval on several VMs. What is the most likely cause?**

A. The host has insufficient physical RAM
B. The VMs are CPU-ready due to more vCPUs than physical cores available
C. The storage array is experiencing high latency
D. The vMotion network is saturated

**Correct Answer: B**

**Explanation:** CPU Ready (%RDY in ESXTOP) measures the time a vCPU was ready to run but could not be scheduled on a physical core. A value of 25 ms per 20-second interval is well above the ~5–10 ms threshold and indicates CPU contention — the host has more active vCPUs than physical cores can service. RAM shortage (A) would show balloon or swap metrics. Storage latency (C) would appear in DAVG/KAVG. vMotion saturation (D) would affect live migration, not general VM CPU performance.

---

### Question 2

**An administrator wants to ensure that traffic from vSAN does not starve vMotion traffic during periods of peak storage I/O. The cluster uses a VDS. What should the administrator configure?**

A. Beacon probing on the VDS uplinks
B. Network I/O Control (NIOC) with shares assigned to each system traffic type
C. A separate VSS for vSAN traffic
D. Route based on IP hash load balancing

**Correct Answer: B**

**Explanation:** NIOC is the correct mechanism to allocate bandwidth between competing traffic types (vSAN, vMotion, management, VM traffic) on shared uplinks. NIOC is a VDS feature that assigns relative shares and optional hard limits per system traffic type — ensuring that a surge in vSAN traffic cannot monopolize uplink capacity to the exclusion of vMotion. Beacon probing (A) is failover detection, not bandwidth management. Creating a separate VSS (C) would not solve the contention if both shares the same physical NICs. IP hash (D) is a load balancing policy that helps distribute traffic across uplinks but does not prioritize one traffic type over another.

---

### Question 3

**An administrator needs to migrate a cluster from baseline-based (VUM) management to image-based management using vLCM. Which statement is correct about this migration?**

A. Baselines and image-based management can coexist on the same cluster after migration
B. The migration removes all baseline associations from the cluster
C. Image-based management is only available for clusters with fewer than 32 hosts
D. Quick Boot is automatically enabled when switching to image-based management

**Correct Answer: B**

**Explanation:** When a cluster is switched to vLCM image-based management, all baseline associations are removed from that cluster — baselines and image-based management cannot coexist on the same cluster (eliminates A). There is no 32-host limit for image-based management (eliminates C). Quick Boot is not automatically enabled — it depends on hardware eligibility and must be verified separately (eliminates D). The key exam point is that image-based and baseline-based are mutually exclusive per cluster.

---

### Question 4

**A vSphere Distributed Switch is configured with two port groups: PG-Web and PG-DB. The administrator enables Private VLANs. VMs in PG-Web must be able to communicate with each other and with the gateway firewall VM, but must NOT communicate with VMs in PG-DB. Which PVLAN types should be assigned?**

A. PG-Web: Isolated; PG-DB: Community; Firewall: Promiscuous
B. PG-Web: Community; PG-DB: Isolated; Firewall: Promiscuous
C. PG-Web: Promiscuous; PG-DB: Community; Firewall: Isolated
D. PG-Web: Community; PG-DB: Community (different community); Firewall: Promiscuous

**Correct Answer: D**

**Explanation:** Community ports can communicate with each other (within the same community) and with promiscuous ports — but not with ports in a different community or isolated ports. By placing PG-Web and PG-DB in separate communities with the firewall VM on a promiscuous port: web VMs can reach each other (same community) and can reach the firewall (promiscuous), but cannot reach DB VMs (different community). Option B would use Isolated for PG-Web — isolated ports cannot reach each other, only promiscuous. Option A reverses Web and DB with the wrong isolation direction. Option C incorrectly places the gateway on an Isolated port, which would prevent it from reaching community ports.

---

### Question 5

**An administrator enables vCLS retreat mode on a cluster. Which immediate impact should they expect?**

A. vSphere HA is completely disabled and VMs will not be restarted if a host fails
B. DRS automation changes to manual mode and HA Optimal Placement is disabled
C. All vCLS agent VMs are migrated to a different cluster
D. The cluster enters lockdown mode and prevents new VM deployments

**Correct Answer: B**

**Explanation:** vCLS retreat mode powers off and removes the vCLS agent VMs. The immediate impacts are: DRS loses its coordination agent VMs and reverts to manual mode (automated load balancing stops), and HA Optimal Placement is disabled (HA can still restart VMs, but without the optimization logic that vCLS provides). HA is NOT completely disabled (eliminates A) — hosts can still detect failures and restart VMs; they just won't have optimized placement. vCLS VMs are removed, not migrated to another cluster (eliminates C). Lockdown mode is unrelated to vCLS (eliminates D). The exam often attempts to confuse candidates by suggesting HA is fully disabled — it is not.

---

## Study Tips

| Area | High-Yield Topics |
|---|---|
| Networking | PVLAN types and their communication rules; NIOC traffic types; IP hash vs originating port ID; beacon probing requirements |
| Storage | SPBM, VAAI vs VASA, SIOC, vVOLs, RDM types (physical vs virtual) |
| Cluster Services | HA admission control types (percentage vs slot vs dedicated failover hosts); DRS automation levels; FT requirements (max vCPUs, no unsupported features) |
| Lifecycle | Quick Boot requirements (UEFI, no passthrough); image-based vs baseline mutual exclusivity; answer files for host profiles |
| Monitoring | CPU Ready threshold; memory reclamation order (TPS → balloon → compress → swap); log file names and their contents; vCLS retreat mode impact |
| Security | PVLAN types; vTPM requirements; VM encryption key providers; vSphere Trust Authority topology |
