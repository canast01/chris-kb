# VM Standard

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
> Part of the [Standards](../index.md) reference.

---

## Overview

This standard defines how virtual machines are built, sized, and configured in the vSphere environment. All new VMs deployed from a template or built manually must comply with these requirements.

## Templates

| Setting | Requirement |
|---|---|
| Source | Deploy all VMs from an approved template |
| Template naming | `tmpl-<os>-<version>-<date>` (e.g. `tmpl-win2022-std-20260101`) |
| Template refresh | Templates refreshed quarterly with OS patches and VMware Tools updates |
| Template location | Stored in the designated `Templates` folder and `Templates` content library |

Never deploy from an outdated template. Check the template version date before deploying.

## VMware Tools

| Requirement | Detail |
|---|---|
| VMware Tools installed | Mandatory on all VMs |
| Tools version | Current version shipped with the installed ESXi baseline |
| Update policy | Tools updated automatically with host (Managed) — or updated during application maintenance windows |
| Tools running state | VMware Tools must be running and up to date in vCenter |

A VM with VMware Tools not installed or not running is a compliance failure. Remediate within 7 days of detection.

## Hardware Version

| Setting | Requirement |
|---|---|
| Virtual Hardware Version | Match current vCenter default for new VMs |
| Current approved version | HW Version 21 (vSphere 8.0) |
| Upgrade policy | Upgrade hardware version during scheduled maintenance, not during business hours |
| Legacy VMs | Hardware version upgrades require application owner approval and testing |

## CPU

| Setting | Requirement |
|---|---|
| vCPU sizing | Start small. Match workload profile. |
| CPU Hot Add | Disabled unless explicitly required by the application |
| vCPU count | Do not exceed physical pCPU thread count of a single host (avoid NUMA overhead) |
| CPU limit/reservation | Do not set CPU limits on production VMs. Set reservations for tier-1 workloads only. |

CPU hot add requires VM power-off on some OS types to take effect. Avoid enabling it unless the application requires zero-downtime CPU scaling.

## Memory

| Setting | Requirement |
|---|---|
| Memory sizing | Align to workload requirements + 10% headroom |
| Memory Hot Add | Disabled by default |
| Memory limit | Do not set memory limits on production VMs |
| Memory reservation | Only set for tier-1 workloads requiring guaranteed memory |
| Memory balloon/swap | Keep vSphere memory swap at zero — avoid overcommit in production |

## Disk

| Setting | Requirement |
|---|---|
| Disk Controller | PVSCSI (paravirtual SCSI) for all non-boot disks with I/O workload |
| Boot Disk | LSI Logic or PVSCSI — follow OS vendor guidance |
| Disk Format | Thin or Thick Eager Zeroed. Use Eager Zeroed for databases and high-I/O workloads. |
| Snapshot Policy | No standing snapshots in production. Snapshots older than 72 hours alert. |
| Maximum snapshot age | 7 days hard limit — auto-alerting required |

## Network

| Setting | Requirement |
|---|---|
| NIC Type | VMXNET3 for all VMs |
| NIC count | One NIC unless the application requires NIC separation |
| Port group | Assign to the correct production VM port group for the environment |

Do not use E1000 or E1000e NICs on new VMs. These have higher CPU overhead than VMXNET3.

## Tagging and Documentation

Every VM must have the following tags applied before handover:

| Tag Category | Required? | Example |
|---|---|---|
| Environment | Yes | `prod`, `dev`, `test` |
| Application | Yes | Application or service name |
| Backup Tier | Yes | `backup-gold`, `backup-silver`, `backup-none` |
| Owner | Yes | Team or individual owner |

## VM Build Checklist

- [ ] Deployed from approved template
- [ ] VMware Tools installed and running
- [ ] Hardware version at current approved level
- [ ] CPU hot add disabled (unless required)
- [ ] Memory hot add disabled
- [ ] PVSCSI controller for data disks
- [ ] VMXNET3 NIC
- [ ] OS patched to current approved level
- [ ] VM name follows naming standard
- [ ] Tags applied (environment, application, backup tier, owner)
- [ ] Backup job configured or VM included in tag-based job
- [ ] VM added to monitoring
- [ ] CMDB record created or updated
