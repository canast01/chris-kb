# Pure Storage

<div class="kb-summary">
Pure Storage knowledge base covering FlashArray and FlashBlade — including ActiveDR, ActiveCluster, Evergreen, and Pure1. Includes architecture references, operational procedures, CLI commands, replication, and troubleshooting guides.
</div>

```text
┌───────────────────────────────────────── Pure Storage Stack ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                             Pure1                                             │   │
│   │            SaaS cloud management portal — no on-prem management appliance required            │   │
│   │           Fleet health monitoring · capacity analytics · AI-driven anomaly detection          │   │
│   │            Upgrade orchestration: non-disruptive controller and software refreshes            │   │
│   │             Auto-opens support cases; integrates with Pure Technical Services team            │   │
│   │             REST API · Purity CLI · Pure Service Orchestrator (PSO) for Kubernetes            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Pure1 manages all arrays via HTTPS — no on-prem management server required                         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Pure FlashArray       │  │       Pure FlashBlade       │  │  Evergreen / Evergreen//One │   │
│   │    //X · //C · //E models   │  │  //S: perf · //E: capacity  │  │   Non-disruptive refreshes  │   │
│   │   All-flash block storage   │  │   Scale-out file + object   │  │ Controller swap, no downtime│   │
│   │     FC · iSCSI · NVMe-oF    │  │    NFS · SMB · S3 · HDFS    │  │    Evergreen//One: STaaS    │   │
│   │  Always-on dedup + compress │  │  DirectFlash blade modules  │  │  Pure-owned HW on-premises  │   │
│   │  SafeMode: immutable snaps  │  │ Rapid Restore: backup target│  │  SLA-guaranteed performance │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    FlashArray serves block workloads · FlashBlade serves file and object workloads                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │     ActiveCluster (Sync)    │  │       ActiveDR (Async)      │  │     Purity OS · SafeMode    │   │
│   │Active-active stretch cluster│  │   Asynchronous replication  │  │  Purity//FA: FlashArray OS  │   │
│   │   Sync replication, RPO=0   │  │  RPO configurable (seconds) │  │  Purity//FB: FlashBlade OS  │   │
│   │  Mediator: tie-breaker node │  │Cross-array and cross-site DR│  │  SafeMode: retention-locked │   │
│   │  Transparent host failover  │  │ Non-disruptive failover test│  │ Policy-based snap scheduling│   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Replication and data services protect workloads across sites and against ransomware                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Fibre Channel   │      iSCSI       │      NVMe-oF      │    NFS / SMB     │    S3 / HDFS     │   │
│   │ SAN block access │ IP block access  │ NVMe over Fabrics │  File protocols  │Object / analytics│   │
│   │ 16G · 32G · 64G  │  TCP/IP network  │  Ethernet / RoCE  │NFS v3/v4.1 · SMB │REST · SDK · POSIX│   │
│   │ HBA → SAN switch │ iSCSI initiator  │ NVMe host adapter │ Exports + shares │  Buckets + keys  │   │
│   │ Zoning + masking │ CHAP auth · iSNS │  RDMA low latency │  Perms + quotas  │  IAM + policies  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  DirectFlash NVMe modules · Dual controllers · 10/25/100 GbE · FC 16G/32G · Power & Cooling           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  FlashArray    = Pure all-flash block array; //X (performance), //C (capacity), //E (entry)           │
│  FlashBlade    = Pure scale-out file + object platform built on DirectFlash blade modules             │
│  Pure1         = Pure SaaS cloud management; health, analytics, and upgrade orchestration             │
│  Purity//FA    = FlashArray operating system; manages volumes, snapshots, and replication             │
│  Purity//FB    = FlashBlade operating system; manages NFS, SMB, S3 buckets, and expansion             │
│  ActiveCluster = Sync active-active stretch cluster; RPO=0, transparent host failover                 │
│  ActiveDR      = Async replication with configurable RPO (seconds); used for cross-site DR            │
│  SafeMode      = Immutable retention-locked snapshots; immune to admin or ransomware deletion         │
│  Evergreen     = Pure upgrade programme; controller refresh without downtime or data migration        │
│  Evergreen//One= STaaS model; Pure owns and maintains hardware on-premises, billed by use             │
│  DirectFlash   = Pure proprietary NVMe modules; bypasses SSD firmware for lower latency               │
│  PSO           = Pure Service Orchestrator; Kubernetes operator for dynamic volume provisioning       │
│  Mediator      = Lightweight VM that arbitrates ActiveCluster split-brain scenarios                   │
│  RPO           = Recovery Point Objective; max acceptable data loss (ActiveCluster=0, ActiveDR=secs)  │
│  STaaS         = Storage-as-a-Service; hardware owned by Pure, customer pays by consumption           │
│  NVMe-oF       = NVMe over Fabrics; extends NVMe protocol across Ethernet (RoCE) or FC                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


```text
┌───────────────────────────── Pure Storage — Initial Deployment Sequence ──────────────────────────────┐
│                                                                                                       │
│  Step 1 · Physical Readiness                                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Rack FlashArray//X or //C  ·  dual power cables to redundant PDUs                                    │
│  FC: cable controller ports to SAN fabric  ·  iSCSI/NVMe-oF: cable to storage VLAN                    │
│  Replication: dedicated Ethernet ports for array-to-array replication network                         │
│  Management: eth0 (controller A) and eth0 (controller B) connected to OOB switch                      │
│  Confirm initial IP visible (factory default 192.168.170.2)  ·  set management IP                     │
│                                                                                                       │
│                                        │  complete Purity initial setup                               │
│                                        ▼                                                              │
│  Step 2 · Purity Initial Setup                                                                        │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Connect browser to management IP  ·  login with pureuser / pureuser (change immediately)             │
│  Run initial setup wizard: array name, management IP, gateway, DNS, NTP, time zone                    │
│  Set admin password  ·  set pureuser password  ·  enable two-factor if required                       │
│  Configure alert notification: SMTP relay, recipient address, severity threshold                      │
│  Register with Pure1 cloud: Settings → Support → register with Pure1 API token                        │
│                                                                                                       │
│                                        │  configure network interfaces                                │
│                                        ▼                                                              │
│  Step 3 · Network Interfaces                                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create iSCSI interfaces: array → Network → Interfaces → enable iSCSI on each port                    │
│  Create FC interfaces: ports auto-detected  ·  assign WWPN to SAN zone                                │
│  Create replication interface: dedicated port  ·  assign replication network VLAN                     │
│  NVMe-oF (FlashArray//XL): enable NVMe-oF  ·  assign RDMA or TCP transport per port                   │
│  Verify connectivity: ping test from host management  ·  check port LEDs                              │
│                                                                                                       │
│                                        │  register hosts and connect volumes                          │
│                                        ▼                                                              │
│  Step 4 · Host Connectivity                                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create host object: array → Storage → Hosts → Create  ·  enter IQN or WWNs                           │
│  Create host group for VMware clusters or Oracle RAC  ·  add hosts to group                           │
│  Create volume: Storage → Volumes → Create  ·  set size and name                                      │
│  Connect volume to host group  ·  rescan storage from host  ·  confirm LUN visible                    │
│  Deploy Pure Storage VASA Provider for vSphere  ·  enables vVols and Storage Policy                   │
│                                                                                                       │
│                                        │  configure protection groups                                 │
│                                        ▼                                                              │
│  Step 5 · Protection Groups                                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create protection group: add volumes, hosts, or host groups                                          │
│  Set snapshot schedule: frequency, retention window (local and replicated)                            │
│  Add replication target: create array-to-array connection  ·  enter remote credentials                │
│  Enable asynchronous replication  ·  verify first transfer completes cleanly                          │
│  ActiveCluster (sync): add stretched volume to pod  ·  confirm mediator registered                    │
│                                                                                                       │
│                                        │  connect Pure1 and validate                                  │
│                                        ▼                                                              │
│  Step 6 · Pure1 & ActiveDR                                                                            │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Pure1 registration complete  ·  array telemetry uploading  ·  health visible in portal               │
│  Install Pure Storage Plugin for VMware vCenter  ·  enables datastore management                      │
│  ActiveDR (async DR): configure VM group  ·  test failover to DR array  ·  document RTO               │
│  Enable Evergreen subscription checks  ·  confirm controller and shelf firmware current               │
│  Run Pure1 Workload Planner assessment  ·  document baseline IOPs and latency                         │
│  Capacity alert: set 80% threshold  ·  configure escalation path for storage growth                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="flasharray/"><strong>FlashArray</strong><span>All-flash block storage — ActiveDR, ActiveCluster, snapshots, replication, and Purity.</span></a>
<a class="kb-card" href="flashblade/"><strong>FlashBlade</strong><span>Unified fast file and object storage — scale-out NFS, S3, and analytics workloads.</span></a>
<a class="kb-card" href="evergreen/"><strong>Evergreen</strong><span>Non-disruptive upgrades, controller refreshes, and capacity expansions.</span></a>
<a class="kb-card" href="evergreen-one/"><strong>Evergreen One</strong><span>Storage-as-a-service — consumption-based model, SLA guarantees, and Pure1 management.</span></a>
<a class="kb-card" href="operations/"><strong>Operations</strong><span>Alerts, Pure1 monitoring, and support case management across the Pure fleet.</span></a>
</div>
