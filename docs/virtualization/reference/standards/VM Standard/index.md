# VM Standards

```
┌──────────────────────────────────────── vSphere — VM Standard ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Baseline VM configuration standard — hardware version, sizing, snapshot, and tools policy   │   │
│   │     Hardware version: vHW 21 minimum (ESXi 8.0); upgrade at OS patching cycle if feasible     │   │
│   │       Sizing tiers: XS/S/M/L/XL — defined by vCPU and RAM; over-sized VMs flagged by DRS      │   │
│   │      Snapshots: max 3 per VM, max 14 days age; monitored and alerted via Aria Operations      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Hardware version → OS template → sizing tier → storage policy → snapshot compliance                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Hardware Config       │  │        Sizing Policy        │  │          Lifecycle          │   │
│   │        vHW 21 minimum       │  │        XS: 1vCPU/2GB        │  │         VMware Tools        │   │
│   │       CPU hot-add: off      │  │         S: 2vCPU/4GB        │  │        Auto-update on       │   │
│   │       RAM hot-add: off      │  │         M: 4vCPU/8GB        │  │       Snapshot: max 3       │   │
│   │         SCSI: PVSCSI        │  │        L: 8vCPU/16GB        │  │       Max age 14 days       │   │
│   │         NIC: VMXNET3        │  │        XL: 16vCPU/32+       │  │          Thin disks         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Templates enforce vHW version and NIC/SCSI controller types at provisioning time                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Setting      │  Standard value  │   Exception path  │   Enforced by    │      Alert       │   │
│   │   vHW version    │       21+        │   Change ticket   │     Template     │     Aria Ops     │   │
│   │   Snapshot age   │    ≤ 14 days     │    CAB approval   │   Aria monitor   │   Alert email    │   │
│   │   VMware Tools   │     Current      │     Frozen OS     │   Tools check    │     Aria Ops     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: VMs on vSAN datastores with SPBM policy; PVSCSI for all non-legacy workloads             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    vHW version   = VMware Virtual Hardware version; controls available VM features and devices        │
│    CPU hot-add   = Add vCPUs without reboot; disabled — causes NUMA imbalance in most OSes            │
│    RAM hot-add   = Add vRAM without reboot; disabled — OS fragmentation risk, keep off                │
│    PVSCSI        = Paravirtual SCSI controller; higher throughput and lower CPU than LSI Logic        │
│    VMXNET3       = Paravirtual NIC; much higher performance than E1000; required standard             │
│    VMware Tools  = Guest agent enabling quiesced snapshots, heartbeat, IP reporting                   │
│    Thin disk     = VM disk uses only written bytes; grows to allocated maximum on demand              │
│    Snapshot      = Point-in-time VM state; delta disk accumulates writes; delete after use            │
│    Sizing tier   = Predefined vCPU/RAM combination; prevents arbitrary VM sizing                      │
│    SPBM policy   = Storage policy assigned at provisioning; defines redundancy and tiering            │
│    Template      = Golden image VM converted to template; enforces vHW and controller type            │
│    DRS oversized = DRS flag when VM has more vCPUs than it uses; triggers right-size alert            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
- Standard VM naming
- VMware Tools installed and current
- Hardware version managed
- Snapshots should be temporary
- CPU and memory sized correctly
- Guest OS matches actual OS
- Backup policy assigned
- Owner documented
- Criticality documented
