# ESXi — Design Standards


<div class="kb-summary">
Design Standards reference covering BIOS / UEFI Baseline, VMkernel Adapter Layout, NTP Configuration, VIB Acceptance Levels, Storage Path Configuration and 3 more sections.
</div>

ESXi Host Design Checklist — Standard Layout
```text
┌─────────────────────────────────────── ESXi — Design Standards ───────────────────────────────────────┐
│                                                                                                       │
│  Hardware sizing, HA cluster design, and build standards for ESXi deployments.                        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Hardware Requirements             │  │                Cluster Design               │   │
│   │           Min 2 sockets / 16 cores           │  │            Min 3 hosts for HA N+1           │   │
│   │           256 GB RAM per prod host           │  │           Max 96 hosts per cluster          │   │
│   │          2x 10/25 GbE NICs mgmt+VM           │  │           EVC mode per CPU family           │   │
│   │          2x 10/25 GbE vMotion/vSAN           │  │           DRS threshold: moderate           │   │
│   │           Boot: SD/USB/M.2 or disk           │  │           HA admission ctrl: slots          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical sizing → cluster policy → HA/DRS tuning → network teaming standard.                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Networking Standards             │  │              Storage Standards              │   │
│   │         dvSwitch for all prod hosts          │  │            VMFS-6 on shared LUNs            │   │
│   │            vmk0 mgmt VLAN tagged             │  │           vSAN disk group: 1 cache          │   │
│   │           vMotion on dedicated vmk           │  │          Datastore naming standard          │   │
│   │          NIC teaming: LACP/failover          │  │           Multipathing: RR for SAN          │   │
│   │            MTU 9000 vSAN/vMotion             │  │            VAAI enabled on arrays           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Rack servers (2U), ToR switches (25 GbE), SAN fabric, power redundancy (2N)                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  EVC     = Enhanced vMotion Compat; masks CPU features for live migration                             │
│  HA      = High Availability; vSphere restarts VMs after host failure                                 │
│  DRS     = Distributed Resource Scheduler; balances CPU/mem load via vMotion                          │
│  LACP    = Link Aggregation Control Protocol; bonds NICs for bandwidth                                │
│  MTU     = Maximum Transmission Unit; jumbo frames (9000) for vSAN/vMotion                            │
│  RR      = Round Robin; PSA path policy across all active storage paths                               │
│  vmk     = VMkernel adapter; carries system traffic (mgmt/vMotion/vSAN)                               │
│  dvSwitch= Distributed vSwitch; enforces consistent port config across hosts                          │
│  VAAI    = vStorage API Array Integration; array offload for clone/zeroing                            │
│  Admission ctrl = HA policy reserving capacity to restart VMs on failure                              │
│  N+1     = cluster design with capacity to lose 1 host without VM impact                              │
│  Slot    = HA resource unit = worst-case VM CPU+mem in cluster                                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
---

## NTP Configuration

All ESXi hosts must synchronise to the same NTP sources as vCenter. Clock skew > 5 minutes causes authentication failures.

```bash
# Check NTP status
esxcli system time get
esxcli network ntp get

# Set NTP servers
esxcli system ntp set --server=ntp1.example.com --server=ntp2.example.com --enabled=true
```

---

## VIB Acceptance Levels

ESXi enforces VIB acceptance levels. Production hosts should accept only:

| Level | Description | Production Use |
|---|---|---|
| VMwareCertified | VMware-signed and certified | Yes |
| VMwareAccepted | Partner-signed, VMware accepted | Yes |
| PartnerSupported | Vendor-signed only | Review case-by-case |
| CommunitySupported | No signing | Not in production |

```bash
# Check acceptance level
esxcli software acceptance get

# Set minimum to VMwareAccepted
esxcli software acceptance set --level=VMwareAccepted
```

---

## Storage Path Configuration

| Array Type | Recommended PSP | Notes |
|---|---|---|
| Pure Storage FlashArray | Round Robin | Set I/O ops limit to 1 (not 1000) for Pure |
| Dell PowerStore | Round Robin | |
| NetApp AFF | Round Robin | Use NetApp DSM for advanced features |
| EMC VMAX / PowerMax | Round Robin | |
| Active/Passive legacy | MRU | Do not use RR on A/P arrays |

```bash
# Configure Round Robin with I/O ops limit of 1
esxcli storage nmp psp roundrobin deviceconfig set -d <device-naa> --type=iops --iops=1
```

---

## Host Profile Baseline

Every cluster host must conform to the Host Profile applied from vCenter. A Host Profile captures:

- VMkernel adapter configuration (IP, services, MTU)
- NTP servers
- DNS settings
- Firewall ruleset
- VIB acceptance level
- SATP/PSP rules for storage
- SSH/ESXi Shell state (disabled in profile)
- Syslog server address

After any host change, run **Check Compliance** in vCenter before marking the change as complete.

---

## ESXi Shell and SSH Policy

| Service | Production State | Maintenance State |
|---|---|---|
| ESXi Shell | Stopped / Disabled | Allowed temporarily |
| SSH | Stopped / Disabled | Allowed temporarily |
| DCUI | Running | Running |

Set shell timeout to limit exposure if left enabled:

```bash
esxcli system settings advanced set -o /UserVars/ESXiShellTimeOut -i 600
esxcli system settings advanced set -o /UserVars/ESXiShellInteractiveTimeOut -i 300
```

---

## Cluster Sizing Reference

| Cluster Type | Min Hosts | Storage | HA Capacity |
|---|---|---|---|
| Standalone | 1 | Any | None |
| Standard (N+1) | 3 | Shared SAN/NAS | Survive 1 host failure |
| Standard (N+2) | 5 | Shared SAN/NAS | Survive 2 host failures |
| vSAN (FTT=1 RAID-1) | 3 | Pooled (vSAN) | Survive 1 host failure |
| vSAN (FTT=1 RAID-5) | 4 | Pooled (vSAN) | Survive 1 host failure |
| vSAN (FTT=2 RAID-6) | 6 | Pooled (vSAN) | Survive 2 host failures |

**CPU overcommit guidance:** 4:1 vCPU:pCPU ratio for general workloads; 2:1 for latency-sensitive (databases, real-time). Monitor CPU Ready — sustained > 5% indicates overcommitment.

**Memory overcommit guidance:** Size physical RAM to cover peak active memory across all VMs. Balloon and swap are performance impacts, not design targets. Include 10–15% overhead for VMkernel and VM metadata.
