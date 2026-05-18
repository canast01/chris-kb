# ESXi — Design Standards

```
ESXi Host Design Checklist — Standard Layout
┌──────────────────────────────────────────────────────────┐
│  Naming & DNS                                            │
│  └── FQDN: esxi-<nn>.<domain>  (A + PTR records)         │
│                                                          │
│  BIOS / UEFI Baseline                                    │
│  ├── Hyperthreading: Enabled                             │
│  ├── Power Policy: High Performance                      │
│  ├── C-States: Disabled (or C1 only)                     │
│  ├── IOMMU / VT-d: Enabled                               │
│  ├── Secure Boot + TPM 2.0: Enabled                      │
│  └── IPMI / iDRAC / iLO: Enabled on OOB NIC              │
│                                                          │
│  NIC Layout (vDS — 4 pNICs minimum)                      │
│  ├── vmnic0 + vmnic1 → vDS uplinks (active/active)       │
│  └── vmnic2 + vmnic3 → vDS uplinks (teamed, LACP)        │
│                                                          │
│  VMkernel Adapters                                       │
│  ├── vmk0  Management    1500 MTU  Mgmt VLAN             │
│  ├── vmk1  vMotion       9000 MTU  vMotion VLAN          │
│  ├── vmk2  vSAN          9000 MTU  vSAN VLAN             │
│  └── vmk3  NFS / iSCSI   9000 MTU  Storage VLAN          │
│                                                          │
│  Boot Device: M.2 NVMe (preferred)                       │
│  HBA Config: FC / NVMe-oF — single-initiator zoning      │
│  NTP: 2+ servers matching vCenter NTP sources            │
└──────────────────────────────────────────────────────────┘
```

## Host Naming

All ESXi hosts use fully qualified domain names (FQDN) and must have matching forward and reverse DNS records:

```
Format: esxi-<nn>.<domain>
Example: esxi-01.corp.example.com
         esxi-02.corp.example.com
```

The hostname set in DCUI must match the DNS A record. DNS mismatch causes certificate errors and SSL thumbprint mismatches when adding hosts to vCenter.

---

## BIOS / UEFI Baseline

Configure the following on all physical hosts before installing ESXi:

| Setting | Required Value | Reason |
|---|---|---|
| Hyperthreading | Enabled | Required for NUMA-aware scheduling |
| Power Policy | High Performance | Prevent CPU throttling under load |
| C-States | Disabled or C1 only | Reduce latency jitter for VMs |
| IOMMU (VT-d / AMD-Vi) | Enabled | Required for DirectPath I/O (SR-IOV, GPU passthrough) |
| Secure Boot | Enabled | Required for TPM 2.0 attestation |
| TPM 2.0 | Enabled | Host attestation; vSphere 7.0+ feature |
| Serial Port | Disabled | Reduce attack surface |
| PXE Boot on management NIC | Disabled (unless Auto Deploy) | Prevent unintended re-provision |
| IPMI / iDRAC / iLO | Enabled, on dedicated OOB NIC | Out-of-band management |

---

## VMkernel Adapter Layout

Standard vmkernel layout for cluster hosts. All adapters are configured on the vDS:

| Adapter | Service | MTU | Subnet |
|---|---|---|---|
| vmk0 | Management | 1500 | Mgmt VLAN /24 |
| vmk1 | vMotion | 9000 | vMotion VLAN /24 |
| vmk2 | vSAN | 9000 | vSAN VLAN /24 |
| vmk3 | NFS / iSCSI | 9000 | Storage VLAN /24 |

Jumbo frames (MTU 9000) require matching configuration on physical switch ports and upstream switches for storage and vMotion traffic.

Verify MTU end-to-end:

```bash
vmkping -I vmk2 -d -s 8972 <target-IP>
# -d = don't fragment, -s = payload size (8972 = 9000 - 28 byte IP+UDP header)
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
