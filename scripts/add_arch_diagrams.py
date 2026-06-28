#!/usr/bin/env python3
"""
Inject D2, PlantUML, and Vega-Lite diagrams into architecture/how-it-works pages.

Each entry in DIAGRAMS specifies:
  - file: relative path under docs/
  - type: d2 | plantuml | vega-lite
  - position: "after_svg" (before first H2) | "in_section:Section Name" (after that H2 heading line)
  - content: the diagram source

Idempotent: skips injection if the fence type already appears in the file.
"""

import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent / "docs"

# ---------------------------------------------------------------------------
# Diagram registry
# ---------------------------------------------------------------------------

DIAGRAMS = [

    # ── vSAN ────────────────────────────────────────────────────────────────

    {
        "file": "virtualization/vmware/vsan/architecture/how-it-works.md",
        "type": "d2",
        "position": "after_svg",
        "content": """\
```d2
direction: right

cluster: vSAN Cluster {
  host1: ESXi Host 1 {
    dg1: "Cache SSD + 3× Capacity" {shape: cylinder}
  }
  host2: ESXi Host 2 {
    dg2: "Cache SSD + 3× Capacity" {shape: cylinder}
  }
  host3: ESXi Host 3 {
    dg3: "Cache SSD + 3× Capacity" {shape: cylinder}
  }
}

vcenter: vCenter Server {shape: rectangle}
witness: Witness Appliance\\n(stretched only) {shape: diamond}

vcenter -> cluster.host1: ESXi management
vcenter -> cluster.host2: ESXi management
vcenter -> cluster.host3: ESXi management

cluster.host1 -> cluster.host2: vSAN VMkernel (UDP 2233)
cluster.host2 -> cluster.host3: vSAN VMkernel (UDP 2233)
cluster.host1 -> cluster.host3: vSAN VMkernel (UDP 2233)
```
""",
    },

    {
        "file": "virtualization/vmware/vsan/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "in_section:Write Path",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "VM / App" as VM
participant "vSAN Kernel\\n(local host)" as KERNEL
participant "Object Manager\\n(OM)" as OM
participant "CLOM\\n(cluster placement)" as CLOM
participant "DOM\\n(distributed I/O)" as DOM
participant "Cache Tier\\n(SSD)" as CACHE
participant "Capacity Tier\\n(HDD / NVMe)" as CAP

VM -> KERNEL: Write I/O
KERNEL -> OM: Policy-based placement
OM -> CLOM: FTT compliance check
CLOM -> DOM: Distribute components across hosts
DOM -> CACHE: Write to cache (SSD)
CACHE --> DOM: ACK (write acknowledged to VM)
DOM --> VM: Write complete
...async destage...
CACHE -> CAP: Destage to capacity tier
@enduml
```
""",
    },

    # ── SRM ─────────────────────────────────────────────────────────────────

    {
        "file": "virtualization/vmware/srm/architecture/how-it-works.md",
        "type": "d2",
        "position": "in_section:Site Topology",
        "content": """\
```d2
direction: right

protected: Protected Site {
  vc_p: vCenter Server {shape: rectangle}
  srm_p: SRM Server {shape: rectangle}
  vms: Protected VMs {shape: rectangle}
  storage_p: Production Storage {shape: cylinder}
  vc_p -> srm_p
  srm_p -> vms: protect
  vms -> storage_p
}

recovery: Recovery Site {
  vc_r: vCenter Server {shape: rectangle}
  srm_r: SRM Server {shape: rectangle}
  placeholders: Placeholder VMs {shape: rectangle}
  storage_r: Recovery Storage {shape: cylinder}
  vc_r -> srm_r
  srm_r -> placeholders
}

protected.srm_p -> recovery.srm_r: SRM pairing (TCP 443)
protected.storage_p -> recovery.storage_r: Replication (SRA / vSphere Replication)
```
""",
    },

    {
        "file": "virtualization/vmware/srm/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "in_section:Disaster Recovery Failover",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "SRM Admin" as Admin
participant "SRM\\n(Protected Site)" as SRM_P
participant "SRM\\n(Recovery Site)" as SRM_R
participant "Storage SRA" as SRA
participant "vCenter\\n(Recovery)" as VC_R
participant "Recovered VMs" as VMS

Admin -> SRM_R: Execute Recovery Plan
SRM_R -> SRM_P: Notify protected site (if reachable)
SRM_R -> SRA: Invoke failover snapshot
SRA --> SRM_R: Storage volumes ready
SRM_R -> VC_R: Remove placeholder VMs
SRM_R -> VC_R: Register recovered VMs (priority order)
VC_R -> VMS: Power on — highest priority first
VMS --> SRM_R: VM heartbeat OK
SRM_R -> Admin: Recovery report (RPO achieved)
@enduml
```
""",
    },

    # ── ESXi ────────────────────────────────────────────────────────────────

    {
        "file": "virtualization/vmware/esxi/architecture/how-it-works.md",
        "type": "d2",
        "position": "in_section:VMkernel Architecture",
        "content": """\
```d2
direction: down

hardware: Physical Hardware {
  cpu: CPUs {shape: rectangle}
  mem: Memory {shape: rectangle}
  nic: Network (NICs) {shape: rectangle}
  hba: Storage (HBAs / NVMe) {shape: rectangle}
}

vmkernel: VMkernel (Hypervisor) {
  scheduler: CPU Scheduler {shape: rectangle}
  memctl: Memory Manager {shape: rectangle}
  netstack: TCP/IP Network Stack {shape: rectangle}
  psa: Storage Stack (PSA/NMP) {shape: rectangle}
}

userworld: User World (Processes) {
  hostd: hostd (host agent) {shape: rectangle}
  vpxa: vpxa (vCenter agent) {shape: rectangle}
  ntpd: ntpd / syslog {shape: rectangle}
}

vms: Virtual Machines {
  vm1: VM 1 (vCPU / vMEM / vNIC / vDisk) {shape: rectangle}
  vm2: VM 2 {shape: rectangle}
  vmn: VM N {shape: rectangle}
}

hardware -> vmkernel: direct hardware access
vmkernel -> userworld: system calls
vmkernel -> vms: virtualised resources
```
""",
    },

    # ── NetApp ONTAP ────────────────────────────────────────────────────────

    {
        "file": "storage/netapp/ontap/architecture/how-it-works.md",
        "type": "d2",
        "position": "in_section:HA Pair Architecture",
        "content": """\
```d2
direction: right

node_a: Controller A (Active) {shape: rectangle}
node_b: Controller B (HA Partner) {shape: rectangle}
shelves: Disk Shelves {shape: cylinder}
clients: Clients {shape: person}
svms: SVMs (Data LIFs) {shape: rectangle}

node_a -> node_b: HA interconnect\\n(NVRAM mirror, RDMA)
node_a -> shelves: SAS / NVMe (owns aggregates)
node_b -> shelves: SAS / NVMe (takeover path)
clients -> svms: NFS / CIFS / iSCSI / NVMe-oF
svms -> node_a: served via aggregates
node_b -> svms: serves LIFs during takeover
```
""",
    },

    {
        "file": "storage/netapp/ontap/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "in_section:SnapMirror and SnapVault",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Source SVM\\n(Primary)" as SRC
participant "Source Volume" as SVOL
participant "SnapMirror Engine" as SM
participant "Destination SVM\\n(Secondary)" as DST
participant "Destination Volume\\n(DP — read-only)" as DVOL

SRC -> SM: Initialize relationship
SM -> SVOL: Create baseline Snapshot
SM -> DST: Transfer baseline (full copy)
DST -> DVOL: Write baseline
DVOL --> SM: Baseline complete

loop Scheduled update (hourly / daily)
  SM -> SVOL: Create new Snapshot
  SM -> SM: Compute incremental delta from last transfer Snapshot
  SM -> DST: Transfer delta blocks
  DST -> DVOL: Apply delta
  DVOL --> SM: Update complete
  SM -> SVOL: Delete previous transfer Snapshot
end

note over SM,DST: On DR activation — break relationship, promote DVOL to R/W
@enduml
```
""",
    },

    # ── Brocade Fabric OS ───────────────────────────────────────────────────

    {
        "file": "san/brocade/fabric-os/architecture/how-it-works.md",
        "type": "d2",
        "position": "after_svg",
        "content": """\
```d2
direction: right

hosts: Servers {
  h1: Server 1 (dual HBA) {shape: rectangle}
  h2: Server 2 (dual HBA) {shape: rectangle}
  h3: Server 3 (dual HBA) {shape: rectangle}
}

fabric_a: Fabric A (primary) {
  sw1: Switch A1\\n(principal) {shape: rectangle}
  sw2: Switch A2 {shape: rectangle}
  sw1 -> sw2: ISL (E_Port)
}

fabric_b: Fabric B (redundant) {
  sw3: Switch B1\\n(principal) {shape: rectangle}
  sw4: Switch B2 {shape: rectangle}
  sw3 -> sw4: ISL (E_Port)
}

storage: Storage Arrays {
  arr1: Array 1 (target ports) {shape: cylinder}
  arr2: Array 2 (target ports) {shape: cylinder}
}

hosts.h1 -> fabric_a.sw1: F_Port
hosts.h1 -> fabric_b.sw3: F_Port
hosts.h2 -> fabric_a.sw2: F_Port
hosts.h2 -> fabric_b.sw4: F_Port
hosts.h3 -> fabric_a.sw1: F_Port
hosts.h3 -> fabric_b.sw3: F_Port

fabric_a.sw1 -> storage.arr1: F_Port
fabric_a.sw2 -> storage.arr2: F_Port
fabric_b.sw3 -> storage.arr1: F_Port
fabric_b.sw4 -> storage.arr2: F_Port
```
""",
    },

    # ── Pure FlashArray ─────────────────────────────────────────────────────

    {
        "file": "storage/pure/flasharray/architecture/how-it-works.md",
        "type": "d2",
        "position": "after_svg",
        "content": """\
```d2
direction: right

hosts: Hosts {
  host1: Host 1 {shape: rectangle}
  host2: Host 2 {shape: rectangle}
}

fa1: FlashArray //X (site A) {
  ct0: Controller 0 {shape: rectangle}
  ct1: Controller 1 {shape: rectangle}
  nvme: NVMe Flash Modules {shape: cylinder}
  ct0 -> ct1: Active/Active (NVRAM sync)
  ct0 -> nvme
  ct1 -> nvme
}

fa2: FlashArray //X (site B, ActiveCluster) {
  ct0b: Controller 0 {shape: rectangle}
  ct1b: Controller 1 {shape: rectangle}
  nvme2: NVMe Flash Modules {shape: cylinder}
  ct0b -> ct1b: Active/Active (NVRAM sync)
  ct0b -> nvme2
  ct1b -> nvme2
}

mediator: Pure1 Mediator\\n(quorum arbitration) {shape: diamond}

hosts.host1 -> fa1.ct0: FC / iSCSI / NVMe-oF
hosts.host2 -> fa2.ct0b: FC / iSCSI / NVMe-oF

fa1 -> fa2: ActiveCluster sync replication
fa1 -> mediator: heartbeat
fa2 -> mediator: heartbeat
```
""",
    },

    # ── Nutanix ─────────────────────────────────────────────────────────────

    {
        "file": "virtualization/nutanix/architecture/how-it-works.md",
        "type": "d2",
        "position": "after_svg",
        "content": """\
```d2
direction: right

cluster: Nutanix HCI Cluster {
  node1: Node 1 {
    cvm1: CVM 1 {shape: rectangle}
    vm1: Guest VMs {shape: rectangle}
    disk1: Local NVMe/SSD/HDD {shape: cylinder}
    cvm1 -> disk1: manages
  }
  node2: Node 2 {
    cvm2: CVM 2 {shape: rectangle}
    vm2: Guest VMs {shape: rectangle}
    disk2: Local NVMe/SSD/HDD {shape: cylinder}
    cvm2 -> disk2: manages
  }
  node3: Node 3 {
    cvm3: CVM 3 {shape: rectangle}
    vm3: Guest VMs {shape: rectangle}
    disk3: Local NVMe/SSD/HDD {shape: cylinder}
    cvm3 -> disk3: manages
  }
}

prism: Prism Central\\n(management) {shape: rectangle}
ad: Active Directory {shape: rectangle}

prism -> cluster.node1.cvm1: manage
prism -> cluster.node2.cvm2: manage
prism -> cluster.node3.cvm3: manage
prism -> ad: auth

cluster.node1.cvm1 -> cluster.node2.cvm2: DSF replication
cluster.node2.cvm2 -> cluster.node3.cvm3: DSF replication
cluster.node1.cvm1 -> cluster.node3.cvm3: DSF replication
```
""",
    },

    # ── Cisco MDS ───────────────────────────────────────────────────────────

    {
        "file": "san/cisco/mds/architecture/how-it-works.md",
        "type": "d2",
        "position": "after_svg",
        "content": """\
```d2
direction: right

hosts: Servers {
  h1: Host 1 (HBA) {shape: rectangle}
  h2: Host 2 (HBA) {shape: rectangle}
}

director_a: MDS Director A\\n(Fabric A) {
  linecard1: Line Card 1 (32×32G) {shape: rectangle}
  linecard2: Line Card 2 (32×32G) {shape: rectangle}
  sup: Supervisor Module {shape: rectangle}
  linecard1 -> sup: backplane
  linecard2 -> sup: backplane
}

director_b: MDS Director B\\n(Fabric B) {
  linecard3: Line Card 3 (32×32G) {shape: rectangle}
  linecard4: Line Card 4 (32×32G) {shape: rectangle}
  sup2: Supervisor Module {shape: rectangle}
  linecard3 -> sup2: backplane
  linecard4 -> sup2: backplane
}

storage: Storage Arrays {
  arr: Target Ports {shape: cylinder}
}

dcnm: Cisco DCNM\\n(management) {shape: rectangle}

hosts.h1 -> director_a.linecard1: F_Port (32G FC)
hosts.h1 -> director_b.linecard3: F_Port (dual fabric)
hosts.h2 -> director_a.linecard1: F_Port
hosts.h2 -> director_b.linecard3: F_Port

director_a.linecard2 -> storage.arr: F_Port
director_b.linecard4 -> storage.arr: F_Port

dcnm -> director_a.sup: SNMP / SSH
dcnm -> director_b.sup2: SNMP / SSH
```
""",
    },

    # ── Dell PowerMax ───────────────────────────────────────────────────────

    {
        "file": "storage/dell/powermax/architecture/how-it-works.md",
        "type": "d2",
        "position": "after_svg",
        "content": """\
```d2
direction: right

hosts: Hosts {
  h1: Host A {shape: rectangle}
  h2: Host B {shape: rectangle}
}

pm1: PowerMax (Site A) {
  fe_a: Front-End Directors\\n(FC / iSCSI / NVMe) {shape: rectangle}
  be_a: Back-End Directors\\n(NVMe-oF to flash) {shape: rectangle}
  rdf_a: RDF Directors {shape: rectangle}
  flash_a: NVMe Flash Bays {shape: cylinder}
  fe_a -> be_a: internal fabric
  be_a -> flash_a
}

pm2: PowerMax (Site B) {
  fe_b: Front-End Directors {shape: rectangle}
  rdf_b: RDF Directors {shape: rectangle}
  flash_b: NVMe Flash Bays {shape: cylinder}
  fe_b -> flash_b
}

unisphere: Unisphere\\n(management) {shape: rectangle}

hosts.h1 -> pm1.fe_a: FC / NVMe-oF
hosts.h2 -> pm2.fe_b: FC / NVMe-oF

pm1.rdf_a -> pm2.rdf_b: SRDF replication\\n(sync / async / STAR)

unisphere -> pm1.fe_a: manage
unisphere -> pm2.fe_b: manage
```
""",
    },

    # ── NSX-T ───────────────────────────────────────────────────────────────

    {
        "file": "virtualization/vmware/nsx/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "Admin" as ADM
participant "NSX Manager\\n(policy API)" as MGR
participant "NSX Controller\\n(cluster)" as CTL
participant "ESXi Transport Node\\n(TEP + N-VDS)" as ESX
participant "Edge Node\\n(Tier-0 / Tier-1 GW)" as EDGE
participant "Physical Fabric\\n(BGP peer)" as FABRIC

ADM -> MGR: Define segment / DFW policy
MGR -> CTL: Distribute intent
CTL -> ESX: Push TEP config + DFW rules
CTL -> EDGE: Push routing config
EDGE -> FABRIC: BGP advertise prefixes
FABRIC --> EDGE: BGP ack
ESX --> CTL: Config applied
CTL --> MGR: Realisation complete
MGR --> ADM: Policy enforced
@enduml
```
""",
    },

    # ── Horizon ─────────────────────────────────────────────────────────────

    {
        "file": "virtualization/vmware/horizon/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "End User" as USR
participant "Horizon Client" as CLT
participant "Unified Access\\nGateway (UAG)" as UAG
participant "Connection Server" as CS
participant "AD / IdP" as AD
participant "VDI Pool\\n(Instant Clones)" as VDI

USR -> CLT: Launch Horizon Client
CLT -> UAG: HTTPS / Blast Extreme
UAG -> CS: Forward authentication
CS -> AD: LDAP credential check
AD --> CS: Groups + entitlements
CS --> CLT: Desktop list
USR -> CLT: Select desktop
CLT -> UAG: Tunnel session
UAG -> VDI: Blast / PCoIP protocol
VDI --> USR: Desktop stream
@enduml
```
""",
    },

    # ── VMware Cloud Foundation ──────────────────────────────────────────────

    {
        "file": "virtualization/vmware/vmware-cloud-foundation/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "Cloud Admin" as ADM
participant "SDDC Manager" as SDDC
participant "vCenter Server" as VC
participant "NSX Manager" as NSX
participant "vSAN" as VSAN
participant "Aria Suite\\n(Ops / Auto)" as ARIA

ADM -> SDDC: Deploy workload domain
SDDC -> VC: Provision vCenter
SDDC -> NSX: Configure overlay network
SDDC -> VSAN: Create datastore
SDDC -> ARIA: Register management pack
VC --> SDDC: vCenter ready
NSX --> SDDC: Network ready
VSAN --> SDDC: Storage ready
SDDC --> ADM: Workload domain live
@enduml
```
""",
    },

    # ── Aria Automation ─────────────────────────────────────────────────────

    {
        "file": "virtualization/vmware/aria-automation/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "Developer" as DEV
participant "Service Broker\\n(catalog)" as SB
participant "Assembler\\n(blueprint)" as AB
participant "Orchestrator\\n(ABX / vRO)" as ORC
participant "Cloud Account\\n(vSphere / AWS / Azure)" as CA
participant "IPAM / CMDB" as CMDB

DEV -> SB: Request catalog item
SB -> AB: Resolve blueprint version
AB -> ORC: Execute extensibility action
ORC -> CA: Provision infrastructure
ORC -> CMDB: Update CMDB record
CA --> ORC: Resource IDs
ORC --> AB: Provisioning complete
AB --> SB: Deployment created
SB --> DEV: Access details
@enduml
```
""",
    },

    # ── Aria Operations ──────────────────────────────────────────────────────

    {
        "file": "virtualization/vmware/aria-operations/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Managed Object\\n(VM / Host / Datastore)" as OBJ
participant "Collector Node" as COL
participant "Analytics Cluster" as ANA
participant "Aria Ops UI\\n/ API" as UI
actor "Admin" as ADM

OBJ -> COL: Metrics (5-min polling)
COL -> ANA: Ingest + normalise
ANA -> ANA: Capacity model\\n+ anomaly detection
ANA -> UI: Alerts + recommendations
ADM -> UI: View dashboard / set policy
UI -> ANA: Apply action (right-size, reclaim)
ANA -> OBJ: Execute remediation
@enduml
```
""",
    },

    # ── vSphere Replication ──────────────────────────────────────────────────

    {
        "file": "virtualization/vmware/vsphere-replication/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Source VM\\n(protected site)" as SRC
participant "vSphere Replication\\nAgent (VRA)" as VRA_S
participant "Network\\n(TCP 31031)" as NET
participant "vSphere Replication\\nServer (VRS)" as VRS_R
participant "Target Datastore\\n(recovery site)" as TGT

SRC -> VRA_S: Changed blocks (write intercept)
VRA_S -> NET: Compressed + encrypted delta
NET -> VRS_R: Delta transfer
VRS_R -> TGT: Apply to replica VMDK
TGT --> VRS_R: Write confirmed
VRS_R --> VRA_S: RPO checkpoint saved

note over VRA_S,VRS_R
  RPO: 5 min – 24 h
  Quiesce: VMware Tools snapshot
end note
@enduml
```
""",
    },

    # ── Tanzu ────────────────────────────────────────────────────────────────

    {
        "file": "virtualization/vmware/tanzu/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "Platform Operator" as OPS
actor "Developer" as DEV
participant "Supervisor Cluster\\n(vSphere + vSAN)" as SUP
participant "Tanzu Kubernetes\\nGrid (TKG) cluster" as TKG
participant "NSX / AVI\\n(load balancer)" as NET
participant "Harbor Registry" as REG

OPS -> SUP: Enable Workload Management
SUP -> SUP: Create Supervisor namespace
OPS -> SUP: Create TKC (kubectl apply)
SUP -> TKG: Provision worker nodes (VMs)
TKG -> NET: Request LoadBalancer IP
NET --> TKG: VIP assigned
DEV -> REG: Push container image
DEV -> TKG: kubectl apply workload
TKG --> DEV: Pod running
@enduml
```
""",
    },

    # ── VxRail ───────────────────────────────────────────────────────────────

    {
        "file": "virtualization/vmware/vxrail/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "Admin" as ADM
participant "VxRail Manager\\n(vCenter plugin)" as VXM
participant "vCenter Server\\n(embedded)" as VC
participant "vSAN" as VSAN
participant "VxRail Node\\n(ESXi host)" as NODE
participant "Dell Support\\n(SupportAssist)" as DELL

ADM -> VXM: Initiate node expansion
VXM -> NODE: Discover + validate hardware
VXM -> VC: Add host to cluster
VXM -> VSAN: Rebalance data
VSAN --> VXM: Rebalance complete
VXM -> DELL: Upload telemetry (SupportAssist)
DELL --> VXM: Proactive support ticket (if anomaly)
VXM --> ADM: Expansion complete
@enduml
```
""",
    },

    # ── PowerCLI ─────────────────────────────────────────────────────────────

    {
        "file": "virtualization/vmware/powercli/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "Admin" as ADM
participant "PowerCLI\\n(PowerShell module)" as CLI
participant "VMware REST API\\n/ SOAP API" as API
participant "vCenter Server" as VC
participant "ESXi Host" as ESX

ADM -> CLI: Connect-VIServer -Server vc01
CLI -> API: HTTPS REST / SOAP session
API -> VC: Authenticate + return session token
VC --> CLI: Session established

ADM -> CLI: Get-VM | Start-VM
CLI -> API: POST /vcenter/vm/{id}/power/start
API -> VC: Dispatch power-on task
VC -> ESX: Power on VM
ESX --> VC: VM powered on
VC --> CLI: Task complete
CLI --> ADM: Output object
@enduml
```
""",
    },

    # ── Active Directory ─────────────────────────────────────────────────────

    {
        "file": "compute/windows-server/active-directory/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "User" as USR
participant "Workstation\\n(Kerberos client)" as WS
participant "Domain Controller\\n(KDC)" as DC
participant "Global Catalog\\nServer" as GC
participant "Target Service\\n(file share / app)" as SVC

USR -> WS: Login (username + password)
WS -> DC: AS-REQ (pre-auth with password hash)
DC --> WS: AS-REP (TGT + session key)
WS -> DC: TGS-REQ (request service ticket)
DC -> GC: Universal group lookup
GC --> DC: Group membership
DC --> WS: TGS-REP (service ticket)
WS -> SVC: AP-REQ (service ticket)
SVC --> WS: AP-REP (session established)
WS --> USR: Access granted
@enduml
```
""",
    },

    # ── SQL Server ────────────────────────────────────────────────────────────

    {
        "file": "compute/windows-server/sql-server/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Primary Replica\\n(AG primary)" as PRI
participant "Secondary Replica 1\\n(sync commit)" as SEC1
participant "Secondary Replica 2\\n(async commit)" as SEC2
participant "Windows Server\\nFailover Cluster" as WSFC
actor "App / Client" as APP

APP -> PRI: Read / Write (listener VIP)
PRI -> SEC1: Log block (sync — waits for ack)
PRI -> SEC2: Log block (async — no wait)
SEC1 --> PRI: Hardened ACK
SEC2 --> PRI: ACK (best effort)
PRI --> APP: Commit confirmed

note over PRI,WSFC: On failure
WSFC -> SEC1: Failover vote
SEC1 -> WSFC: Become new primary
WSFC --> APP: Listener re-routes to SEC1
@enduml
```
""",
    },

    # ── MySQL ─────────────────────────────────────────────────────────────────

    {
        "file": "compute/linux/mysql/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "MySQL Primary" as PRI
participant "Binary Log\\n(binlog)" as BLOG
participant "MySQL Replica\\n(async)" as REP
participant "Relay Log" as RLOG
participant "SQL Thread" as SQL

PRI -> BLOG: Write DML/DDL event
BLOG --> PRI: Flush to disk
REP -> PRI: COM_REGISTER_SLAVE
PRI --> REP: Binlog stream starts
REP -> RLOG: Write relay log
RLOG -> SQL: SQL thread reads events
SQL -> REP: Apply to replica storage
SQL --> RLOG: Relay log position updated

note over PRI,REP: GTID mode — each transaction has\\nglobal unique ID for safe failover
@enduml
```
""",
    },

    # ── PostgreSQL ───────────────────────────────────────────────────────────

    {
        "file": "compute/linux/postgresql/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Primary\\n(pg_wal writer)" as PRI
participant "WAL Sender\\nProcess" as SND
participant "Network\\n(TCP 5432)" as NET
participant "WAL Receiver\\nProcess" as RCV
participant "Standby\\n(pg_wal apply)" as STB

PRI -> SND: New WAL segment ready
SND -> NET: Stream WAL records (streaming replication)
NET -> RCV: Deliver WAL records
RCV -> STB: Write to pg_wal
STB -> STB: Apply WAL (recovery mode)
STB --> RCV: LSN position feedback
RCV --> SND: Acknowledge LSN
SND --> PRI: Standby confirmed up to LSN

note over PRI,STB: synchronous_commit=on — primary\\nwaits for standby WAL flush before ack
@enduml
```
""",
    },

    # ── Data Domain ──────────────────────────────────────────────────────────

    {
        "file": "storage/dell/data-domain/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Backup Client\\n(Veeam / NetBackup)" as CLT
participant "DD Boost\\nLibrary (client-side)" as DDB
participant "Data Domain\\nOS (DDOS)" as DD
participant "SISL Dedup Engine" as SISL
participant "Local Disks\\n(RAID-6)" as DISK
participant "Remote DD\\n(replication target)" as REMO

CLT -> DDB: Backup stream
DDB -> DD: Segmented + fingerprinted chunks
DD -> SISL: Deduplicate against index
SISL --> DD: Unique chunks only
DD -> DISK: Write unique segments
DD --> CLT: Backup complete (dedup ratio reported)

DD -> REMO: DD Replication (unique chunks delta)
REMO --> DD: Replication confirmed
@enduml
```
""",
    },

    # ── RecoverPoint ─────────────────────────────────────────────────────────

    {
        "file": "storage/dell/recoverpoint/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Production Host" as HOST
participant "Write Splitter\\n(ESXi VAIO / FC splitter)" as SPL
participant "Production Volume\\n(primary)" as PVOL
participant "RPA Cluster\\n(RecoverPoint Appliance)" as RPA
participant "Journal Volume" as JRN
participant "Replica Volume\\n(copy)" as RVOL

HOST -> SPL: Write I/O
SPL -> PVOL: Write to production (continues)
SPL -> RPA: Split copy of write
RPA -> JRN: Journal write (ordered, timestamped)
JRN -> RVOL: Apply to replica (lag = RPO)
RVOL --> RPA: Applied LSN
RPA --> HOST: Asynchronous ack

note over JRN,RVOL: Any journal point-in-time\\ncan be mounted for recovery
@enduml
```
""",
    },

    # ── SRDF/A ───────────────────────────────────────────────────────────────

    {
        "file": "storage/dell/srdf-a/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Host Write" as HOST
participant "R1 Volume\\n(source)" as R1
participant "SRDF/A Cycle\\nBuffer" as BUF
participant "RDF Link\\n(IP / FC)" as RDF
participant "R2 Volume\\n(target)" as R2

HOST -> R1: Write I/O (acked immediately)
R1 -> BUF: Accumulate cycle (default 30s)
BUF -> RDF: Transmit cycle delta (compressed)
RDF -> R2: Apply cycle in order
R2 --> BUF: Cycle confirmed

note over BUF,R2
  Delta sets maintain write-order fidelity.
  RPO = transmission lag + 1 cycle.
end note
@enduml
```
""",
    },

    # ── SRDF/S ───────────────────────────────────────────────────────────────

    {
        "file": "storage/dell/srdf-s/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Host" as HOST
participant "R1 Volume\\n(source)" as R1
participant "RDF Link\\n(FC / IP)" as RDF
participant "R2 Volume\\n(target)" as R2

HOST -> R1: Write I/O
R1 -> RDF: Synchronous mirror write
RDF -> R2: Write to remote
R2 --> RDF: Write hardened ACK
RDF --> R1: Remote confirmed
R1 --> HOST: I/O complete (zero RPO)

note over R1,R2: Both sites must acknowledge\\nbefore host I/O completes.\\nDistance limit: ~200 km (latency).
@enduml
```
""",
    },

    # ── VPLEX ────────────────────────────────────────────────────────────────

    {
        "file": "storage/dell/vplex/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Host A\\n(Site 1)" as HA
participant "VPLEX\\n(Site 1)" as VP1
participant "WAN Interconnect\\n(FC / IP)" as WAN
participant "VPLEX\\n(Site 2)" as VP2
participant "Host B\\n(Site 2)" as HB
participant "Backend Storage\\n(Site 1 + 2)" as STG

HA -> VP1: Write to distributed volume
VP1 -> STG: Write to local backend
VP1 -> WAN: Mirror write to site 2
WAN -> VP2: Deliver write
VP2 -> STG: Write to remote backend
VP2 --> VP1: ACK
VP1 --> HA: Write complete

HB -> VP2: Read from same volume
VP2 -> STG: Serve from local copy
@enduml
```
""",
    },

    # ── SnapCenter ───────────────────────────────────────────────────────────

    {
        "file": "storage/netapp/snapcenter/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "Admin" as ADM
participant "SnapCenter Server\\n(Windows)" as SC
participant "SnapCenter Plugin\\n(host agent)" as PLG
participant "Application\\n(SQL / Oracle / SAP)" as APP
participant "ONTAP\\n(Snapshot engine)" as ONTAP
participant "SnapVault / SnapMirror" as REP

ADM -> SC: Schedule backup policy
SC -> PLG: Trigger pre-backup quiesce
PLG -> APP: Application-consistent quiesce
APP --> PLG: Quiesced
PLG -> ONTAP: Create Snapshot
ONTAP --> PLG: Snapshot created
PLG -> APP: Unquiesce
APP --> PLG: Running
ONTAP -> REP: Vault / mirror Snapshot to secondary
REP --> ONTAP: Replicated
SC --> ADM: Backup complete + catalog entry
@enduml
```
""",
    },

    # ── SnapMirror (standalone) ──────────────────────────────────────────────

    {
        "file": "storage/netapp/snapmirror/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Source Volume\\n(primary SVM)" as SRC
participant "SnapMirror Engine" as SM
participant "Intercluster LIF\\n(TCP 11104 / 11105)" as NET
participant "Destination Volume\\n(DP — read-only)" as DST

SRC -> SM: Initialize relationship
SM -> SRC: Baseline Snapshot
SM -> NET: Transfer baseline (full copy)
NET -> DST: Write baseline
DST --> SM: Baseline complete

loop Scheduled update
  SM -> SRC: New Snapshot
  SM -> SM: Delta vs last transfer Snapshot
  SM -> NET: Transfer delta blocks
  NET -> DST: Apply delta
  DST --> SM: LSN updated
  SM -> SRC: Delete previous transfer Snapshot
end

note over SM,DST: Break + promote DST\\nto R/W for DR activation
@enduml
```
""",
    },

    # ── FlashBlade ────────────────────────────────────────────────────────────

    {
        "file": "storage/pure/flashblade/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "Client\\n(NFS / S3 / SMB)" as CLT
participant "Purity//FB\\n(blade OS)" as PURE
participant "Fabric Module\\n(100GbE switch fabric)" as FAB
participant "Flash Blade\\n(NVMe SSD)" as BLD
participant "Metadata Engine\\n(distributed)" as META

CLT -> PURE: Read / Write request
PURE -> META: Lookup object / file metadata
META --> PURE: Blade address
PURE -> FAB: Route I/O to target blade
FAB -> BLD: NVMe read / write
BLD --> FAB: Data
FAB --> PURE: Response
PURE --> CLT: Data / ack

note over META,BLD: Erasure coding across blades\\n(6+2 or 10+2); no RAID rebuild downtime
@enduml
```
""",
    },

    # ── SANnav ────────────────────────────────────────────────────────────────

    {
        "file": "san/brocade/sannav/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Brocade\\nFabric Switch" as SW
participant "SANnav\\nManagement Portal" as SNV
participant "Analytics\\nEngine" as ANA
participant "Alert\\nService" as ALT
actor "SAN Admin" as ADM

SW -> SNV: SNMP traps + REST telemetry
SNV -> ANA: Ingest metrics (IOPS / latency / errors)
ANA -> ANA: Baseline + anomaly detection
ANA -> ALT: Threshold breach
ALT -> ADM: Email / SNMP alert

ADM -> SNV: View topology map
SNV -> SW: REST config push (zoning / QoS)
SW --> SNV: Config applied
@enduml
```
""",
    },

    # ── Nexus Dashboard ──────────────────────────────────────────────────────

    {
        "file": "san/cisco/nexus-dashboard/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "Network Admin" as ADM
participant "Nexus Dashboard\\n(cluster)" as ND
participant "Fabric Controller\\n(DCNM service)" as FC
participant "Insights\\n(telemetry service)" as INS
participant "Nexus Switch\\n(NX-OS)" as SW

ADM -> ND: Login + select service
ND -> FC: Template-based config deploy
FC -> SW: NX-OS configuration push
SW --> FC: Apply confirmed

SW -> INS: Streaming telemetry (gRPC)
INS -> INS: Anomaly + flow analysis
INS -> ADM: Dashboard alert
@enduml
```
""",
    },

    # ── AWS EVS ──────────────────────────────────────────────────────────────

    {
        "file": "cloud/aws/evs/architecture/how-it-works.md",
        "type": "plantuml",
        "position": "after_svg",
        "content": """\
```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "Admin" as ADM
participant "AWS Console / CLI" as AWS
participant "EVS Control Plane" as EVS
participant "VPC\\n(customer)" as VPC
participant "ESXi Hosts\\n(on Nitro)" as ESX
participant "vCenter Server" as VC

ADM -> AWS: Create EVS environment
AWS -> EVS: Provision Nitro bare-metal
EVS -> VPC: Deploy into customer VPC
EVS -> ESX: Bootstrap ESXi on Nitro
EVS -> VC: Deploy vCenter + vSAN
VC --> EVS: SDDC ready
EVS --> ADM: Management URL

note over VPC,ESX: Traffic stays within AWS region.\\nOn-prem connectivity via Direct Connect / VPN.
@enduml
```
""",
    },

]

# ---------------------------------------------------------------------------
# Injection logic
# ---------------------------------------------------------------------------

FENCE_TYPE_MARKER = {
    "d2":         "```d2",
    "plantuml":   "```plantuml",
    "vega-lite":  "```vega-lite",
}


def already_has(lines: list[str], fence_type: str) -> bool:
    marker = FENCE_TYPE_MARKER[fence_type]
    return any(line.rstrip() == marker for line in lines)


def find_after_svg(lines: list[str]) -> int | None:
    """Return index of the line immediately before the first ## heading,
    after the SVG image line."""
    svg_seen = False
    for i, line in enumerate(lines):
        if not svg_seen and "![" in line and ".svg" in line:
            svg_seen = True
            continue
        if svg_seen and line.startswith("## "):
            return i
    return None


def find_in_section(lines: list[str], section: str) -> int | None:
    """Return index of the line immediately after the ## heading line."""
    target = f"## {section}"
    for i, line in enumerate(lines):
        if line.rstrip() == target:
            return i + 1  # insert right after heading
    return None


def inject(lines: list[str], pos: int, content: str) -> list[str]:
    """Insert content block at pos, preceded by a blank line if needed."""
    block = []
    if pos > 0 and lines[pos - 1].strip():
        block.append("\n")
    block.append(content if content.endswith("\n") else content + "\n")
    if pos < len(lines) and lines[pos].strip():
        block.append("\n")
    return lines[:pos] + block + lines[pos:]


def process(entry: dict, dry_run: bool) -> str:
    path = ROOT / entry["file"]
    if not path.exists():
        return "NOT FOUND"

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    if already_has(lines, entry["type"]):
        return "SKIP (already has diagram)"

    position = entry["position"]
    if position == "after_svg":
        pos = find_after_svg(lines)
    elif position.startswith("in_section:"):
        section = position[len("in_section:"):]
        pos = find_in_section(lines, section)
    else:
        return f"UNKNOWN position: {position}"

    if pos is None:
        return f"SKIP (insertion point not found: {position})"

    if not dry_run:
        new_lines = inject(lines, pos, entry["content"])
        path.write_text("".join(new_lines), encoding="utf-8")

    return "DRY RUN" if dry_run else "UPDATED"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--file", help="Process only entries matching this path substring")
    args = ap.parse_args()

    entries = DIAGRAMS
    if args.file:
        entries = [e for e in entries if args.file in e["file"]]

    updated = skipped = missing = 0
    for e in entries:
        result = process(e, args.dry_run)
        label = "DRY RUN" if args.dry_run and "UPDATED" in result else result.split()[0]
        print(f"[{label:8}] {e['file']}  ({e['type']}  @ {e['position']})")
        if "UPDATED" in result or "DRY RUN" in result:
            updated += 1
        elif "NOT FOUND" in result:
            missing += 1
        else:
            skipped += 1

    print()
    print("=" * 64)
    verb = "would update" if args.dry_run else "updated"
    print(f"{verb.capitalize()}: {updated}  |  Skipped: {skipped}  |  Not found: {missing}")
    print("=" * 64)


if __name__ == "__main__":
    main()
