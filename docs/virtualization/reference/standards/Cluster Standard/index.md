# Cluster Standards

```
┌───────────────────────────────────── vSphere — Cluster Standard ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Standard configuration for all vSphere clusters — HA, DRS, EVC, and naming enforcement    │   │
│   │   HA admission control: percentage-based; reserve capacity for N host failures (default N=1)  │   │
│   │  DRS: Fully Automated for compute clusters; Partially Automated for edge/management clusters  │   │
│   │    Naming: cl-{env}-{function}-{nn}; consistent naming enables automated policy application   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    HA protects availability · DRS optimises performance · EVC enables live migration                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         HA Settings         │  │         DRS Settings        │  │         EVC & Sizing        │   │
│   │       Enabled: always       │  │       Fully Automated       │  │         EVC: enabled        │   │
│   │      Admission: % based     │  │        Threshold: 65%       │  │       CPU baseline set      │   │
│   │       Heartbeat: 5 min      │  │        Predictive DRS       │  │         Min 3 hosts         │   │
│   │       Restart priority      │  │        Affinity rules       │  │         Max 64 hosts        │   │
│   │      Failure condition      │  │        Resource pools       │  │        Homogeneous HW       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Settings applied via host profiles and cluster configuration; reviewed quarterly                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Setting      │    Production    │      Dev/Test     │       Edge       │    Management    │   │
│   │        HA        │     Enabled      │      Enabled      │     Enabled      │     Enabled      │   │
│   │       DRS        │    Fully Auto    │     Fully Auto    │     Partial      │     Partial      │   │
│   │       EVC        │     Required     │      Required     │     Optional     │     Required     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: consistent hardware generation per cluster required for EVC baseline stability           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    HA            = High Availability; monitors hosts and restarts VMs on failure detection            │
│    Admission ctrl = HA reserves CPU/RAM capacity for N host failure scenarios                         │
│    DRS           = Distributed Resource Scheduler; migrates VMs to balance cluster load               │
│    Fully Auto    = DRS applies vMotion migrations without operator approval                           │
│    Partial Auto  = DRS recommends but operator must approve each migration                            │
│    EVC           = Enhanced vMotion Compatibility; masks newer CPU features for migration             │
│    Affinity rule = DRS rule keeping or separating specific VMs across hosts                           │
│    Resource pool = vSphere container applying CPU/RAM shares and limits to VM groups                  │
│    Predictive DRS = DRS integration with Aria Operations for workload-aware pre-migration             │
│    Heartbeat     = HA heartbeat network; secondary check when management network lost                 │
│    Homogeneous   = Same CPU generation across cluster hosts; required for stable EVC                  │
│    Restart prio  = HA restart order for VMs; high priority VMs restarted before medium                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
- Use consistent HA and DRS settings
- Enable DRS where appropriate
- Configure admission control based on business requirements
- Use EVC where needed for CPU compatibility
- Keep cluster hardware consistent when possible
- Document stretched cluster or vSAN-specific settings
- Monitor cluster capacity and failover headroom
