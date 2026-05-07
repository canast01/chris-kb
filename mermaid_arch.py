#!/usr/bin/env python3
"""Replace ASCII architecture diagrams with Mermaid in all architecture pages."""
import re, os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

def m(content):
    return "```mermaid\n" + content.strip() + "\n```"

DIAGRAMS = {}

# ── Storage: Pure ──────────────────────────────────────────────────────────

DIAGRAMS["storage/pure/flasharray/architecture/index.md"] = m("""
graph LR
  H1(["ESXi-01"]) & H2(["ESXi-02"]) --> FabA["FC Fabric A"] & FabB["FC Fabric B"]
  H3(["ESXi-03"]) & H4(["ESXi-04"]) --> FabA & FabB
  FabA & FabB --> FA_A["FlashArray Site A\\nCT0 · CT1"]
  FabA & FabB --> FA_B["FlashArray Site B\\nCT0 · CT1"]
  FA_A <-->|"ActiveCluster\\nsync replication"| FA_B
  FA_A & FA_B -.->|"heartbeat"| MED(["Purity Mediator"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef med fill:#b45309,stroke:#92400e,color:#fff
  class FA_A,FA_B ctrl
  class FabA,FabB net
  class H1,H2,H3,H4 host
  class MED med
""")

DIAGRAMS["storage/pure/flashblade/architecture/index.md"] = m("""
graph TB
  FMM["Fabric Management Module\\n(NVMe-oF internal fabric)"]
  B1["Blade 1"] & B2["Blade 2"] & B3["Blade 3"] & BN["Blade N…"] --> FMM
  FMM --> ETH["10 / 25 / 100 GbE\\nData Ports"]
  ETH --> NFS(["NFS v3/v4.1 Clients"])
  ETH --> S3(["S3 / Object Clients"])
  ETH --> SMB(["SMB Clients"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class FMM,B1,B2,B3,BN ctrl
  class ETH net
  class NFS,S3,SMB host
""")

DIAGRAMS["storage/pure/evergreen/architecture/index.md"] = m("""
graph LR
  A["FlashArray Gen N\\n(current)"] -->|"Non-disruptive\\nhardware swap"| B["FlashArray Gen N+1\\n(upgraded blades/controllers)"]
  B -->|"Evergreen//Forever"| C["FlashArray Gen N+2"]
  A & B & C --> DATA[("Data — always online\\nno migration required")]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  class A,B,C ctrl
  class DATA store
""")

DIAGRAMS["storage/pure/evergreen-one/architecture/index.md"] = m("""
graph TB
  FA["FlashArray / FlashBlade\\n(on-premises)"] -->|"telemetry"| PURE1["Pure1 Cloud\\n(subscription management)"]
  PURE1 -->|"capacity orders · firmware · support"| FA
  ADMIN(["Storage Admin"]) -->|"portal"| PURE1
  PURE1 -->|"alerts · forecasting · health score"| ADMIN
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class FA ctrl
  class PURE1 cloud
  class ADMIN host
""")

# ── Storage: Dell ──────────────────────────────────────────────────────────

DIAGRAMS["storage/dell/powermax/architecture/index.md"] = m("""
graph TB
  FA1["FA Director A\\nFC / NVMe-oF"] & FA2["FA Director B\\nFC / NVMe-oF"] --> XB["Crossbar Interconnect"]
  SR1["SRDF Director A"] & SR2["SRDF Director B"] --> XB
  XB --> FLASH[("NVMe Flash\\nNVMe-SCM / eTLC")]
  FA1 & FA2 --> FAB["SAN Fabric\\n(Brocade / Cisco)"]
  FAB --> H(["Hosts — Oracle / SQL / SAP"])
  SR1 & SR2 -->|"SRDF/S or SRDF/A"| REMOTE["Remote PowerMax"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef net fill:#1d4ed8,stroke:#1e40af,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  class FA1,FA2,SR1,SR2 ctrl
  class XB,FAB net
  class FLASH store
  class H host
  class REMOTE dr
""")

DIAGRAMS["storage/dell/unity/architecture/index.md"] = m("""
graph TB
  SPA["Storage Processor A\\n(active for pool set A)"] <-->|"HA heartbeat"| SPB["Storage Processor B\\n(standby / active)"]
  SPA & SPB --> POOL[("Drive Pool\\nSSD / NL-SAS / SAS")]
  SPA --> NAS["NFS · SMB · FTP\\nData Mover"]
  SPA --> SAN["iSCSI · FC\\nBlock LUNs"]
  SPB --> NAS & SAN
  NAS --> NH(["NAS Clients"])
  SAN --> SH(["SAN Hosts"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class SPA,SPB ctrl
  class POOL store
  class NH,SH host
""")

DIAGRAMS["storage/dell/powerscale/architecture/index.md"] = m("""
graph TB
  N1["Node 1"] & N2["Node 2"] & N3["Node 3"] & NN["Node N…"] --> INT["InfiniBand / 100GbE\\nInternal Cluster Network"]
  INT --> SC["SmartConnect\\n(DNS-based load balancing)"]
  SC --> NFS(["NFS v3/v4 Clients"])
  SC --> SMB(["SMB / CIFS Clients"])
  SC --> HDFS(["HDFS / S3 Clients"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class N1,N2,N3,NN ctrl
  class INT,SC net
  class NFS,SMB,HDFS host
""")

DIAGRAMS["storage/dell/vplex/architecture/index.md"] = m("""
graph LR
  H1(["Hosts Site A"]) --> DIR1["VPLEX Director Pair\\nCluster 1 — Site A"]
  H2(["Hosts Site B"]) --> DIR2["VPLEX Director Pair\\nCluster 2 — Site B"]
  DIR1 <-->|"WAN link\\nGeoSynchrony"| DIR2
  DIR1 --> STG1[("Local Storage A")]
  DIR2 --> STG2[("Local Storage B")]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class DIR1,DIR2 ctrl
  class STG1,STG2 store
  class H1,H2 host
""")

DIAGRAMS["storage/dell/data-domain/architecture/index.md"] = m("""
graph TB
  BU(["Backup Servers\\nNetBackup / Commvault / Veeam"]) -->|"DDBoost / NFS / CIFS / VTL"| DD["Dell Data Domain\\n(dedup + compression)"]
  DD -->|"DD Replicator"| DDDR["Remote Data Domain\\n(DR copy)"]
  DD --> CLOUD["Cloud Tier\\nS3 / Azure Blob — long-term"]
  DD --> VTL["Virtual Tape Library\\n(optional)"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  class DD ctrl
  class BU host
  class CLOUD cloud
  class DDDR dr
""")

DIAGRAMS["storage/dell/ecs/architecture/index.md"] = m("""
graph TB
  CLT(["S3 / Swift / Atmos Clients"]) --> GW["Load Balancer\\n(optional)"]
  GW --> N1["ECS Node 1"] & N2["ECS Node 2"] & N3["ECS Node 3"] & NN["Node N…"]
  N1 & N2 & N3 & NN --> RING[("Object Ring\\ndistributed erasure coding")]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class N1,N2,N3,NN ctrl
  class GW,RING net
  class CLT host
""")

DIAGRAMS["storage/dell/cloudiq/architecture/index.md"] = m("""
graph TB
  ARRAYS["Dell Arrays\\nPowerMax · Unity · PowerScale · PowerStore"] -->|"secure telemetry HTTPS"| CLOUDIQ["Dell CloudIQ\\n(SaaS analytics)"]
  CLOUDIQ --> HEALTH["Health Score & Alerts"]
  CLOUDIQ --> CAP["Capacity Forecasting"]
  CLOUDIQ --> REC["AI Recommendations"]
  ADMIN(["IT Admin"]) -->|"web portal"| CLOUDIQ
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class ARRAYS ctrl
  class CLOUDIQ,HEALTH,CAP,REC cloud
  class ADMIN host
""")

DIAGRAMS["storage/dell/cod/architecture/index.md"] = m("""
graph LR
  ARRAY["Dell Array\\nPowerStore / PowerMax\\n(on-premises)"] <-->|"Dell APEX portal\\ncapacity-on-demand"| APEX["Dell APEX\\nCloud Console"]
  ADMIN(["Storage Admin"]) -->|"portal"| APEX
  APEX --> BILL["Usage-based Billing\\n& Reporting"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class ARRAY ctrl
  class APEX,BILL cloud
  class ADMIN host
""")

DIAGRAMS["storage/dell/powerpath/architecture/index.md"] = m("""
graph LR
  HOST(["Host — Linux / Windows / VMware"]) --> PP["PowerPath\\n(MPIO driver)"]
  PP --> P1["HBA0 → Fabric A → SP-A"]
  PP --> P2["HBA0 → Fabric A → SP-B"]
  PP --> P3["HBA1 → Fabric B → SP-A"]
  PP --> P4["HBA1 → Fabric B → SP-B"]
  P1 & P2 & P3 & P4 --> ARRAY["Storage Array\\nPowerMax / Unity"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class PP net
  class P1,P2,P3,P4 net
  class HOST host
  class ARRAY ctrl
""")

# ── Storage: NetApp ────────────────────────────────────────────────────────

DIAGRAMS["storage/netapp/ontap/architecture/index.md"] = m("""
graph TB
  N1["Node 1 (Controller)\\nSVM-1 · SVM-2"] <-->|"HA interconnect\\n100GbE cluster net"| N2["Node 2 (Controller)\\n(takeover on failover)"]
  N1 & N2 --> SHELVES[("Disk Shelves\\nNVMe SSD / SAS HDD")]
  N1 --> NAS["NFS · SMB/CIFS"]
  N1 --> SAN["iSCSI · FC · NVMe-oF"]
  N2 --> NAS & SAN
  NAS --> NC(["NAS Clients"])
  SAN --> SC(["SAN Hosts"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class N1,N2 ctrl
  class SHELVES store
  class NC,SC host
""")

DIAGRAMS["storage/netapp/snapmirror/architecture/index.md"] = m("""
graph LR
  SRC["Source Volume\\nSVM / Cluster A"] -->|"SnapMirror replication\\n(incremental block diff)"| DST["Destination Volume\\nSVM / Cluster B — read-only"]
  SRC --> SNAP[("Local Snapshots")]
  DST -->|"break to activate for DR"| DRACT["DR Active Volume\\n(after SnapMirror break)"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  class SRC,DST ctrl
  class SNAP store
  class DRACT dr
""")

DIAGRAMS["storage/netapp/snapcenter/architecture/index.md"] = m("""
graph TB
  SCW["SnapCenter Server\\n(Windows / Linux VM)"]
  SCW --> PL1["Plug-in for SQL Server"]
  SCW --> PL2["Plug-in for Oracle"]
  SCW --> PL3["Plug-in for VMware"]
  PL1 & PL2 & PL3 --> ONTAP["NetApp ONTAP\\nSnapshot · SnapMirror · SnapVault"]
  ADMIN(["DBA / Storage Admin"]) -->|"web UI / REST API"| SCW
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class SCW,PL1,PL2,PL3 ctrl
  class ONTAP store
  class ADMIN host
""")

DIAGRAMS["storage/netapp/keystone/architecture/index.md"] = m("""
graph TB
  ONTAP["NetApp ONTAP\\n(on-premises / colocation)"] -->|"telemetry"| KS["NetApp Keystone\\n(STaaS portal)"]
  KS --> COMMIT["Committed Capacity Tier"]
  KS --> BURST["Burst Capacity\\n(on-demand)"]
  KS --> BILL["Monthly Billing"]
  ADMIN(["Customer Admin"]) -->|"portal"| KS
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class ONTAP ctrl
  class KS,COMMIT,BURST,BILL cloud
  class ADMIN host
""")

# ── SAN ────────────────────────────────────────────────────────────────────

DIAGRAMS["san/brocade/fabric-os/architecture/index.md"] = m("""
graph TB
  H1(["ESXi-01\\nHBA0 · HBA1"]) & H2(["ESXi-02\\nHBA0 · HBA1"]) --> DIRA["Brocade Director A\\n(Fabric A)"]
  H1 & H2 --> DIRB["Brocade Director B\\n(Fabric B)"]
  DIRA <-->|"ISL — 10/40 Gbps"| DIRC["Brocade Director C\\n(Fabric A — DR)"]
  DIRB <-->|"ISL — 10/40 Gbps"| DIRD["Brocade Director D\\n(Fabric B — DR)"]
  DIRA & DIRB --> FA[("FlashArray")]
  DIRC & DIRD --> PM[("PowerMax")]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class DIRA,DIRB,DIRC,DIRD ctrl
  class FA,PM store
  class H1,H2 host
""")

# ── Security ───────────────────────────────────────────────────────────────

DIAGRAMS["security/active-directory/architecture/index.md"] = m("""
graph TB
  FOREST["AD Forest\\n(security boundary)"] --> ROOT["Forest Root Domain\\ncorp.example.com"]
  ROOT --> DC1["DC-01 Site A\\nPDC · RID · Infra Master"]
  ROOT --> DC2["DC-02 Site A\\nGlobal Catalog"]
  ROOT -->|"AD replication"| DC3["DC-03 · DC-04\\nSite B — replica DCs"]
  ROOT --> CHILD["Child Domain\\ndivision.corp.example.com"]
  CHILD --> CDC["Child DC"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  class DC1,DC2,DC3,CDC ctrl
  class FOREST,ROOT,CHILD mgmt
""")

DIAGRAMS["security/certificates/architecture/index.md"] = m("""
graph TB
  ROOT[("Root CA\\n(offline — HSM)")] -->|"signs"| INT1["Intermediate CA 1\\nInternal Issuing CA"]
  ROOT -->|"signs"| INT2["Intermediate CA 2\\nPublic / External CA"]
  INT1 -->|"issues"| CERT1["Server Certificate"]
  INT1 -->|"issues"| CERT2["Client Certificate"]
  INT2 -->|"issues"| CERT3["Publicly Trusted Cert"]
  CERT1 & CERT2 & CERT3 -.->|"OCSP / CRL"| CRL["Revocation\\nCRL / OCSP Responder"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  class ROOT store
  class INT1,INT2 ctrl
  class CERT1,CERT2,CERT3 host
  class CRL mgmt
""")

DIAGRAMS["security/cyberark/architecture/index.md"] = m("""
graph TB
  PVWA["PVWA\\n(web interface)"] & PSM["PSM\\n(session proxy)"] & CPM["CPM\\n(rotation engine)"] --> VAULT["CyberArk Vault\\n(encrypted credential store)"]
  USER(["Privileged User"]) -->|"browser"| PVWA
  PSM -->|"RDP / SSH proxy\\nsession recording"| TARGET(["Target Servers"])
  CPM -->|"password rotation"| TARGET
  VAULT -.->|"audit stream"| SIEM(["SIEM"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class VAULT store
  class PVWA,PSM,CPM ctrl
  class USER,TARGET,SIEM host
""")

DIAGRAMS["security/venafi/architecture/index.md"] = m("""
graph TB
  TPP["Venafi Trust Protection Platform"]
  TPP --> DISC["Discovery Engine\\n(network scan / agent)"]
  TPP --> CA1["CA Connector — ADCS"]
  TPP --> CA2["CA Connector — DigiCert / Entrust"]
  TPP --> AUTO["Automation\\n(renewal / provisioning)"]
  DISC -->|"found certs"| TPP
  ADMIN(["Security Admin"]) -->|"portal"| TPP
  TPP -->|"SIEM / SNMP"| SIEM(["SIEM / Monitoring"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class TPP,DISC ctrl
  class CA1,CA2,AUTO mgmt
  class ADMIN,SIEM host
""")

# ── Virtualization ─────────────────────────────────────────────────────────

DIAGRAMS["virtualization/vmware/vcenter/architecture/index.md"] = m("""
graph TB
  VCSA["vCenter Server Appliance\\n(VCSA)"] --> CL["vSphere Cluster\\nDRS · HA enabled"]
  VCSA --> LCM["Lifecycle Manager\\n(patching)"]
  VCSA --> NSX["NSX Manager\\n(optional)"]
  CL --> ESX1["ESXi-01"] & ESX2["ESXi-02"] & ESX3["ESXi-03"] & ESX4["ESXi-04"]
  ESX1 & ESX2 & ESX3 & ESX4 --> VDS["vSphere Distributed Switch\\nVM Net · vMotion · Storage · Mgmt"]
  VDS --> STORE["Shared Storage\\nFlashArray · vSAN · NFS"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef store fill:#1d4ed8,stroke:#1e40af,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  class VCSA,LCM,NSX mgmt
  class CL,VDS net
  class ESX1,ESX2,ESX3,ESX4 ctrl
  class STORE store
""")

DIAGRAMS["virtualization/vmware/vsan/architecture/index.md"] = m("""
graph TB
  H1["ESXi-01\\nCache NVMe + Capacity SSD"] & H2["ESXi-02\\nCache NVMe + Capacity SSD"] & H3["ESXi-03\\nCache NVMe + Capacity SSD"] --> VSANNET["vSAN VMkernel Network\\n25 / 10 GbE dedicated"]
  VSANNET --> DS[("vSAN Datastore\\nFTT policy — RAID-1 / RAID-5 / RAID-6")]
  DS --> VM(["VM Workloads"])
  VCSA["vCenter\\n(vSAN management)"] --> VSANNET
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef store fill:#1d4ed8,stroke:#1e40af,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  class H1,H2,H3 ctrl
  class VSANNET net
  class DS store
  class VM host
  class VCSA mgmt
""")

DIAGRAMS["virtualization/vmware/esxi/architecture/index.md"] = m("""
graph TB
  ESXI["ESXi Hypervisor\\n(VMkernel)"]
  ESXI --> VMK0["vmk0 — Management"]
  ESXI --> VMK1["vmk1 — vMotion"]
  ESXI --> VMK2["vmk2 — Storage iSCSI/NFS"]
  ESXI --> VMS(["Virtual Machines"])
  ESXI --> VSWITCH["vSwitch / VDS\\n(port groups)"]
  VSWITCH --> VMNIC["Physical NICs\\nvmnic0 · vmnic1 · vmnic2 · vmnic3"]
  ESXI --> HBA["FC HBAs\\n(SAN connectivity)"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class ESXI ctrl
  class VMK0,VMK1,VMK2,VSWITCH,VMNIC,HBA net
  class VMS host
""")

DIAGRAMS["virtualization/vmware/vmware-cloud-foundation/architecture/index.md"] = m("""
graph TB
  SDDC["SDDC Manager\\n(VCF orchestration)"] --> MGMT["Management Domain\\nvCenter · NSX · vSAN"]
  SDDC --> WL1["Workload Domain I\\n(VI workloads)"]
  SDDC --> WL2["Workload Domain II\\n(VVF cloud workloads)"]
  MGMT --> EMH["ESXi Mgmt Hosts\\n(4 minimum)"]
  WL1 --> EWH["ESXi Workload Hosts"]
  SDDC --> CLOUD["VMware Cloud\\n(optional hybrid)"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  class SDDC mgmt
  class MGMT,WL1,WL2 ctrl
  class EMH,EWH host
  class CLOUD cloud
""")

DIAGRAMS["virtualization/vxrail/architecture/index.md"] = m("""
graph TB
  VXM["VxRail Manager\\n(lifecycle management)"] --> VCSA["vCenter Server"]
  VXM --> NODES["VxRail Cluster\\n3 – 64 nodes"]
  NODES --> N1["VxRail Node 1\\nvSAN cache + capacity"]
  NODES --> N2["Node 2"]
  NODES --> N3["Node N…"]
  N1 & N2 & N3 --> DS[("vSAN Datastore")]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class VXM,VCSA mgmt
  class NODES ctrl
  class N1,N2,N3 host
  class DS store
""")

DIAGRAMS["virtualization/vmware/aria-operations/architecture/index.md"] = m("""
graph TB
  ADP1["vCenter Adapter"] & ADP2["NSX Adapter"] & ADP3["Storage Adapter"] --> COL["Remote Collector\\n(cloud proxy)"]
  COL --> ANAL["Aria Operations\\nAnalytics Cluster"]
  ANAL --> DATA[("Metrics Store")]
  ANAL --> ALERTS["Alerts · Capacity · Rightsizing"]
  ADMIN(["vSphere Admin"]) -->|"browser"| ANAL
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  class ANAL,COL ctrl
  class DATA store
  class ADP1,ADP2,ADP3,ALERTS mgmt
  class ADMIN host
""")

DIAGRAMS["virtualization/vmware/aria-operations-for-logs/architecture/index.md"] = m("""
graph TB
  SRC1(["ESXi / vCenter syslog"]) & SRC2(["NSX / VMs syslog"]) & SRC3(["Linux / Windows agent"]) --> VRLI["Aria Operations for Logs\\n(Log Intelligence cluster)"]
  VRLI --> IDX[("Log Index\\nhot + warm retention")]
  VRLI --> ALERTS["Alert Rules & Notifications"]
  ADMIN(["Operator"]) -->|"browser"| VRLI
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class VRLI ctrl
  class IDX store
  class SRC1,SRC2,SRC3,ADMIN host
""")

DIAGRAMS["virtualization/vmware/aria-suite-lifecycle/architecture/index.md"] = m("""
graph TB
  LCM["Aria Suite Lifecycle\\n(LCM appliance)"]
  LCM --> VROPS["Aria Operations"]
  LCM --> VRLI["Aria Ops for Logs"]
  LCM --> VRA["Aria Automation"]
  LCM --> VRNI["Aria Ops for Networks"]
  LCM --> REPO["Product Binaries Repo"]
  ADMIN(["vSphere Admin"]) -->|"web UI"| LCM
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class LCM mgmt
  class VROPS,VRLI,VRA,VRNI ctrl
  class ADMIN host
""")

DIAGRAMS["virtualization/vmware/aria-automation/architecture/index.md"] = m("""
graph TB
  CAT["Service Catalog\\n(consumer portal)"] --> ORCH["Aria Automation Orchestrator\\n(workflow engine)"]
  ORCH --> IAAS["IaaS Service\\n(compute engine)"]
  IAAS --> VCTR["vCenter\\n(VM provisioning)"]
  IAAS --> NSX_T["NSX\\n(network provisioning)"]
  IAAS --> CLOUDS["Public Cloud\\nAWS · Azure · GCP"]
  ADMIN(["Cloud Admin"]) -->|"UI / API"| CAT
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  class CAT,ORCH,IAAS ctrl
  class VCTR,NSX_T mgmt
  class ADMIN host
  class CLOUDS cloud
""")

# ── Disaster Recovery ──────────────────────────────────────────────────────

DIAGRAMS["disaster-recovery/srm/architecture/index.md"] = m("""
graph LR
  VC_A["vCenter A\\n+ SRM Server A + SRA"] --> STG_A[("Storage A")]
  VC_B["vCenter B\\n+ SRM Server B + SRA"] --> STG_B[("Storage B")]
  VC_A <-->|"SRM pairing"| VC_B
  STG_A -->|"replication\\nvSphere Rep / array"| STG_B
  H_A(["Production VMs\\nSite A"]) --> VC_A
  H_B(["DR VMs\\nSite B"]) -.-> VC_B
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class VC_A ctrl
  class VC_B dr
  class STG_A,STG_B store
  class H_A host
  class H_B dr
""")

DIAGRAMS["disaster-recovery/srdf-s/architecture/index.md"] = m("""
graph LR
  PM_A["PowerMax Primary\\nSite A — R1"] -->|"SRDF/S synchronous\\n(≤10ms RTT)"| PM_B["PowerMax Secondary\\nSite B — R2"]
  PM_A --> HA(["Production Hosts\\nSite A"])
  PM_B -.->|"read-only\\n(Synchronized state)"| HB(["Standby Hosts\\nSite B"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class PM_A ctrl
  class PM_B dr
  class HA host
  class HB dr
""")

DIAGRAMS["disaster-recovery/srdf-a/architecture/index.md"] = m("""
graph LR
  PM_A["PowerMax Primary\\nSite A — R1"] -->|"writes buffered"| CYCLE["Delta Set Extension\\n(DSE — WAN buffer)"]
  CYCLE -->|"cycle flush\\n~30s"| PM_B["PowerMax Secondary\\nSite B — R2"]
  PM_B -.->|"RPO / lag monitor"| LAG["SRDF/A Cycle State"]
  PM_A --> HA(["Production Hosts"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class PM_A ctrl
  class PM_B dr
  class CYCLE,LAG mgmt
  class HA host
""")

DIAGRAMS["disaster-recovery/recoverpoint/architecture/index.md"] = m("""
graph LR
  RPA1["RPA Cluster\\nSite A"] --> STG_A[("Storage A\\nProduction LUNs")]
  RPA2["RPA Cluster\\nSite B"] --> STG_B[("Storage B\\nReplica + Journal")]
  RPA1 <-->|"WAN — compressed replication"| RPA2
  STG_A -->|"captured writes"| RPA1
  H_A(["Production Hosts"]) --> STG_A
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class RPA1 ctrl
  class RPA2 dr
  class STG_A,STG_B store
  class H_A host
""")

DIAGRAMS["disaster-recovery/superna-eyeglass/architecture/index.md"] = m("""
graph LR
  PS_A["PowerScale Cluster A\\n(production)"] -->|"SyncIQ policy"| PS_B["PowerScale Cluster B\\n(DR)"]
  EG["Superna Eyeglass\\nDR Assistant"] -->|"monitors SyncIQ"| PS_A
  EG -->|"orchestrates failover\\naccess zone migration"| PS_B
  ADMIN(["Admin"]) -->|"Eyeglass UI"| EG
  DNS(["DNS / AD\\naccess zone cutover"]) <--> EG
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class PS_A ctrl
  class PS_B dr
  class EG mgmt
  class ADMIN,DNS host
""")

DIAGRAMS["disaster-recovery/veeam/architecture/index.md"] = m("""
graph TB
  VBR["Veeam Backup & Replication Server"] --> PROXY["Backup Proxy\\n(data mover)"]
  PROXY --> REPO[("Backup Repository\\nSOBR / immutable")]
  VCTR(["VMware vCenter\\nsource VMs"]) --> PROXY
  REPO -->|"capacity tier"| OBJ[("Object Storage\\nS3 / Azure Blob")]
  REPO -->|"tape offload"| TAPE[("Tape Library")]
  ADMIN(["Backup Admin"]) -->|"console"| VBR
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  class VBR,PROXY ctrl
  class REPO,TAPE store
  class VCTR,ADMIN host
  class OBJ cloud
""")

DIAGRAMS["disaster-recovery/commvault/architecture/index.md"] = m("""
graph TB
  CS["CommServe\\n(command & control)"] --> WEBCON["Web Console\\n& Command Center"]
  MA1["Media Agent 1\\n(data mover)"] & MA2["Media Agent 2"] --> CS
  SRC(["Source — VMs / DBs / Files"]) --> MA1 & MA2
  MA1 & MA2 --> DISK[("Disk Library\\nDDB dedup")]
  DISK -->|"aux copy"| TAPE[("Tape / Object\\nlong-term retention")]
  ADMIN(["Backup Admin"]) --> WEBCON
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  class CS,MA1,MA2 ctrl
  class DISK,TAPE store
  class SRC,ADMIN host
  class WEBCON mgmt
""")

# ── Monitoring ─────────────────────────────────────────────────────────────

DIAGRAMS["monitoring/aria-operations/architecture/index.md"] = m("""
graph TB
  ADP1["vCenter Adapter"] & ADP2["NSX Adapter"] & ADP3["Third-party Adapters"] --> COL["Remote Collector\\n(cloud proxy)"]
  COL --> ANAL["Aria Operations\\nAnalytics Cluster"]
  ANAL --> DATA[("Metrics Store")]
  ANAL --> ALERTS["Alert Engine\\nCapacity · Compliance"]
  ADMIN(["Admin"]) -->|"browser"| ANAL
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  class ANAL,COL ctrl
  class DATA store
  class ADP1,ADP2,ADP3,ALERTS mgmt
  class ADMIN host
""")

DIAGRAMS["monitoring/cloudiq/architecture/index.md"] = m("""
graph TB
  ARRAYS["Dell Arrays\\nPowerMax · Unity · PowerScale"] -->|"secure telemetry HTTPS"| CLOUDIQ["Dell CloudIQ\\n(SaaS analytics)"]
  CLOUDIQ --> HEALTH["Health Score & Alerts"]
  CLOUDIQ --> CAP["Capacity Forecasting"]
  CLOUDIQ --> REC["AI Recommendations"]
  ADMIN(["IT Admin"]) -->|"web portal"| CLOUDIQ
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class ARRAYS ctrl
  class CLOUDIQ,HEALTH,CAP,REC cloud
  class ADMIN host
""")

DIAGRAMS["monitoring/dell-aiops/architecture/index.md"] = m("""
graph TB
  ARRAYS["Dell Storage Arrays\\n(telemetry streams)"] --> AIOPS["Dell AIOps\\n(AI analytics engine)"]
  AIOPS --> ANOM["Anomaly Detection"]
  AIOPS --> PRED["Predictive Insights"]
  AIOPS --> RECS["Actionable Recommendations"]
  AIOPS --> CIQ["CloudIQ Integration"]
  ADMIN(["Storage Team"]) -->|"dashboard"| AIOPS
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class ARRAYS ctrl
  class AIOPS,ANOM,PRED,RECS,CIQ cloud
  class ADMIN host
""")

DIAGRAMS["monitoring/insightiq/architecture/index.md"] = m("""
graph TB
  PS["PowerScale Cluster\\n(OneFS API)"] -->|"performance telemetry"| IIQ["InsightIQ Server\\n(analytics VM)"]
  IIQ --> PERF["Performance Dashboards\\nIOPS · Throughput · Latency"]
  IIQ --> CAP["Capacity Trending\\n& Protocol Breakdown"]
  IIQ --> REP["Scheduled Reports\\nPDF / CSV export"]
  ADMIN(["Storage Admin"]) -->|"browser"| IIQ
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class PS ctrl
  class IIQ,PERF,CAP,REP cloud
  class ADMIN host
""")

DIAGRAMS["monitoring/nexus-dashboard/architecture/index.md"] = m("""
graph TB
  ND["Cisco Nexus Dashboard\\n(3-node cluster)"] --> NDFC["NDFC — Fabric Controller"]
  ND --> NDI["ND Insights\\ntelemetry · flow analysis"]
  ND --> NDO["ND Orchestrator\\nmulti-site ACI"]
  NDFC & NDI & NDO --> FABRICS["Managed Fabrics\\nNexus · ACI · MDS"]
  ADMIN(["Network Admin"]) -->|"browser"| ND
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class ND ctrl
  class NDFC,NDI,NDO mgmt
  class ADMIN,FABRICS host
""")

DIAGRAMS["monitoring/pure1/architecture/index.md"] = m("""
graph TB
  FA["FlashArray / FlashBlade\\n(on-premises)"] -->|"telemetry HTTPS"| PURE1["Pure1 Cloud\\n(SaaS analytics)"]
  PURE1 --> HEALTH["Health Score & Alerts"]
  PURE1 --> CAP["Capacity Forecasting\\n(Evergreen model)"]
  PURE1 --> PERF["Performance Analytics"]
  PURE1 --> SUP["Support Integration\\n(log collection · auto-case)"]
  ADMIN(["Storage Admin"]) -->|"browser / mobile"| PURE1
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class FA ctrl
  class PURE1,HEALTH,CAP,PERF,SUP cloud
  class ADMIN host
""")

# ── Compute ────────────────────────────────────────────────────────────────

DIAGRAMS["compute/linux/architecture/index.md"] = m("""
graph TB
  KERNEL["Linux Kernel\\nRHEL / Ubuntu / SLES"]
  KERNEL --> STORAGE["Storage Stack\\nlvm2 · dm-multipath · xfs/ext4"]
  KERNEL --> NET["Network Stack\\nnm · bonding · firewalld"]
  KERNEL --> SVCS["systemd Services\\nsshd · rsyslog · cron"]
  KERNEL --> SEC["Security\\nSELinux / AppArmor · auditd · PAM"]
  STORAGE --> DISK[("Block Devices\\n/dev/sd* / /dev/mapper/*")]
  NET --> NIC["Physical NICs\\neth0 / bond0 / enp*"]
  ADMIN(["Sysadmin"]) -->|"SSH / console"| KERNEL
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef net fill:#1d4ed8,stroke:#1e40af,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class KERNEL ctrl
  class STORAGE,SVCS,SEC net
  class DISK store
  class NIC,NET net
  class ADMIN host
""")

DIAGRAMS["compute/windows-server/architecture/index.md"] = m("""
graph TB
  WS["Windows Server 2019 / 2022"]
  WS --> AD["Active Directory DS\\n(DC role)"]
  WS --> DNS_R["DNS Server"]
  WS --> FS["File Server\\nSMB · DFS"]
  WS --> IIS["IIS / App Roles"]
  WS --> WSUS["Windows Update\\nWSUS / Azure Update Manager"]
  WS --> SEC["Windows Defender\\nFirewall · Audit Policy"]
  ADMIN(["Windows Admin"]) -->|"RDP / PowerShell"| WS
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class WS ctrl
  class AD,DNS_R,FS,IIS,WSUS,SEC mgmt
  class ADMIN host
""")

# ── Cloud ──────────────────────────────────────────────────────────────────

DIAGRAMS["cloud/aws/architecture/index.md"] = m("""
graph TB
  ORG["AWS Organization\\n(management account)"] --> LOG["Log Archive Account"]
  ORG --> AUDIT["Audit / Security Account"]
  ORG --> PROD["Production Account\\n(workload VPC)"]
  PROD --> VPC["VPC — 10.0.0.0/16"]
  VPC --> PUB["Public Subnets\\nALB · NAT GW"]
  VPC --> PRIV["Private Subnets\\nEC2 · RDS · EKS"]
  PUB --> IGW["Internet Gateway"]
  PRIV --> TGW["Transit Gateway\\nhub-and-spoke"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  class ORG,LOG,AUDIT,PROD ctrl
  class VPC,PUB,PRIV net
  class IGW,TGW cloud
""")

DIAGRAMS["cloud/azure/architecture/index.md"] = m("""
graph TB
  TENANT["Azure Tenant\\n(Entra ID)"] --> MG["Management Groups\\nCorp > Prod > Non-Prod"]
  MG --> SUBP["Production Subscription"]
  MG --> SUBD["Dev/Test Subscription"]
  SUBP --> HUB["Hub VNet\\nFirewall · Bastion · VPN GW"]
  SUBP --> SP1["Spoke VNet 1\\n(Workload A)"]
  SUBP --> SP2["Spoke VNet 2\\n(Workload B)"]
  HUB <-->|"VNet peering"| SP1 & SP2
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  class TENANT,MG ctrl
  class SUBP,SUBD cloud
  class HUB,SP1,SP2 net
""")

# ── Main architecture overview ─────────────────────────────────────────────

DIAGRAMS["architecture/index.md"] = m("""
graph TB
  COMP["Compute\\nESXi · Linux · Windows"] --> FABRIC["SAN Fabric\\nBrocade · Cisco MDS"]
  COMP --> NET["Network\\nVDS · NSX · VLANs"]
  FABRIC --> STORE["Storage\\nFlashArray · PowerMax · ONTAP"]
  NET --> STORE
  STORE -->|"replication"| DR["Disaster Recovery\\nSRM · SRDF · RecoverPoint"]
  COMP --> MON["Monitoring\\nAria Ops · CloudIQ · Pure1"]
  STORE --> MON
  COMP --> SEC["Security\\nAD · CyberArk · PKI"]
  NET --> SEC
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef net fill:#1d4ed8,stroke:#1e40af,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  classDef mon fill:#b45309,stroke:#92400e,color:#fff
  classDef sec fill:#15803d,stroke:#166534,color:#fff
  class COMP,FABRIC ctrl
  class STORE store
  class NET net
  class DR dr
  class MON mon
  class SEC sec
""")

# ── Run ────────────────────────────────────────────────────────────────────

ASCII_BLOCK = re.compile(
    r'```\n(?:[^\n]*\n)*?(?:[^\n]*[┌└│►◄▼▲┐┘─]{1}[^\n]*\n)(?:[^\n]*\n)*?```',
    re.MULTILINE
)

updated = skipped = no_match = 0

for rel, mermaid_block in sorted(DIAGRAMS.items()):
    path = os.path.join(BASE, rel)
    if not os.path.exists(path):
        print(f"NOT FOUND:  {rel}"); skipped += 1; continue
    content = open(path).read()
    if '```mermaid' in content:
        print(f"SKIP (has mermaid): {rel}"); skipped += 1; continue
    match = ASCII_BLOCK.search(content)
    if not match:
        print(f"NO ASCII:   {rel}"); no_match += 1; continue
    new = content[:match.start()] + mermaid_block + content[match.end():]
    open(path, 'w').write(new)
    print(f"CONVERTED:  {rel}"); updated += 1

print(f"\nDone — converted: {updated}  skipped: {skipped}  no-ascii-found: {no_match}")
