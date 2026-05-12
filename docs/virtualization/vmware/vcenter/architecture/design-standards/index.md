# vCenter — Design Standards

## Naming Conventions

Consistent naming across the vSphere inventory is critical for readability, automation, and audit filtering.

| Object | Format | Example |
|---|---|---|
| Datacenter | `DC-<site>` | `DC-LON`, `DC-AMS` |
| Cluster | `CL-<site>-<function>` | `CL-LON-PROD`, `CL-AMS-DEV` |
| ESXi Host | `esxi-<nn>.<domain>` | `esxi-01.corp.example.com` |
| VMFS Datastore | `DS-VMFS-<array>-<nn>` | `DS-VMFS-PURE01-01` |
| NFS Datastore | `DS-NFS-<array>-<nn>` | `DS-NFS-NETAPP01-01` |
| vSAN Datastore | `DS-VSAN-<cluster>` | `DS-VSAN-CL-LON-PROD` |
| vDS | `VDS-<site>-<nn>` | `VDS-LON-01` |
| Port Group | `PG-<vlan>-<purpose>` | `PG-100-MGMT`, `PG-200-VMOTION` |
| Resource Pool | `RP-<tier>-<team>` | `RP-PROD-APP`, `RP-DEV-TEST` |
| vSphere Tag | `<category>:<value>` | `env:prod`, `tier:gold` |

## Cluster Configuration Baseline

### HA Settings

| Setting | Value | Notes |
|---|---|---|
| HA Enabled | Yes | Mandatory for production clusters |
| Admission Control | Cluster Resource Percentage | Reserve 25% CPU and memory |
| Host Failures to Tolerate | 1 | Increase to 2 for critical clusters |
| VM Monitoring | VM and Application | Requires VMware Tools |
| Datastore Heartbeating | 2 datastores | Select datastores on different arrays |
| VM Restart Priority | Medium (default) | Adjust per VM criticality |

### DRS Settings

| Setting | Value | Notes |
|---|---|---|
| DRS Enabled | Yes | Mandatory for production clusters |
| Automation Level | Fully Automated | Manual only acceptable in DR/test clusters |
| Migration Threshold | 3 (Conservative) | Adjust if vMotion noise is high |
| Predictive DRS | Enabled | Requires Aria Operations integration |
| VM Overrides | Per business requirement | Document in CMDB |

### vSphere HA Advanced Options (production)

```
das.failuredetectiontime = 15000
das.isolationaddress0 = <gateway IP>
das.isolationaddress1 = <secondary IP>
das.usedefaultisolationaddress = false
```

## Resource Pool Naming and Structure

```
Cluster Root
├── RP-PROD-CRITICAL   (Reservation: 40%, Limit: unlimited, Expandable: no)
├── RP-PROD-STANDARD   (Reservation: 20%, Limit: unlimited, Expandable: yes)
├── RP-DEV             (Reservation: 0, Limit: 4 GHz / 16 GB, Expandable: no)
└── RP-TEST            (Reservation: 0, Limit: 2 GHz / 8 GB, Expandable: no)
```

Avoid the **default resource pool** — all production VMs must be in a named pool.

## vSAN Cluster Baseline (where applicable)

| Setting | Value |
|---|---|
| Deduplication and Compression | Enabled (All-Flash only) |
| Encryption | Site-specific (requires KMS) |
| Storage I/O Control | Enabled |
| Default Storage Policy | `VSAN-FTT1-RAID1` (minimum production) |

## vCenter Configuration Checklist

- [ ] NTP configured (at least 2 sources, matching ESXi host NTP)
- [ ] DNS forward/reverse resolution working for all hosts
- [ ] Syslog forwarding configured to log aggregator
- [ ] SMTP relay configured for alarm notifications
- [ ] vCenter backup schedule configured and validated
- [ ] Certificate validity checked (>90 days remaining)
- [ ] SSO lockout policy set (5 failed attempts, 5-minute lockout)
- [ ] Default admin account password rotated per policy
- [ ] Alarm definitions reviewed and recipients set
- [ ] vSphere tags applied to all VMs (env, tier, owner)
- [ ] Resource pools created; default pool empty
- [ ] DRS and HA enabled on all production clusters

## VM Template Standards

| Setting | Standard |
|---|---|
| VMware Tools | Latest available, managed by vCenter |
| VM Hardware Version | Match the cluster's minimum supported version |
| vNIC | VMXNET3 |
| Disk Controller | VMware Paravirtual (PVSCSI) |
| Disk Provisioning | Thin (unless performance tier policy) |
| BIOS/EFI | EFI with Secure Boot for Windows Server 2019+/RHEL 8+ |

---


## VM Naming Convention

VM names in vCenter must match the OS hostname exactly. Names are lowercase, use hyphens as delimiters, and follow the server naming schema `{site}{role}{env}{num}`.

Examples:
- `dc1-wsql-prd-01` — site dc1, Windows SQL, production, instance 01
- `dc2-wapp-dev-03` — site dc2, Windows app, development, instance 03
- `dc1-lmon-prd-01` — site dc1, Linux monitoring, production, instance 01

The VM display name, OS hostname, and DNS A record must all match. Mismatches must be corrected within 48 hours of being flagged by the drift-detection job.

| Field | Value |
|---|---|
| VM display name | Matches OS hostname |
| Guest OS full name | Set correctly (Windows Server 2022, RHEL 9, etc.) |
| VM folder | `/Datacenter/VMs/{env}/{app}` |
| Resource pool | `rp-{env}-{app}` |
| vApp | Not used unless specifically required |

## Hardware Version and VMware Tools

**Hardware version:** All new VMs must use the hardware version matching the vSphere version in use. Check the current minimum with the platform team before building.

Current minimum: hardware version 19 (vSphere 7.0 U2+).

Do not use hardware versions below 13 on any new build. Upgrades on existing VMs require a maintenance window and reboot.

**VMware Tools:** Open VM Tools (`open-vm-tools`) must be installed and running before build sign-off. Do not use legacy VMware Tools ISO-based installations on RHEL 8+ or Ubuntu 20.04+.

```bash
# Linux: verify
systemctl status vmtoolsd

# Windows: verify via PowerShell
Get-Service -Name VMTools | Select-Object Name, Status, StartType
```

Tools must report `running` status in vCenter. A stale or not-running Tools status blocks live migration.

## vNIC Type and Network Configuration

| Setting | Required Value |
|---|---|
| Network adapter type | VMXNET3 |
| E1000/E1000e | Not permitted on new builds |
| NIC count | One per network segment (no bonding in guest) |
| MAC address type | VMware-generated (do not set static MACs) |

Each VM connects to a named port group. Port group names follow the VLAN naming convention. Do not connect VMs directly to a vSwitch uplink.

PCI passthrough and SR-IOV are permitted only for workloads with documented performance requirements and approved by the platform team.

## Disk Provisioning Standards

| Scenario | Provisioning Type | Justification |
|---|---|---|
| Production VMs | Thick eager zeroed | Best performance, no lazy-zero latency |
| Staging/test VMs | Thin provisioned | Space efficiency acceptable |
| Templates | Thin provisioned | Templates are not run directly |
| Linked clones | Not permitted | Not used in standard builds |

All VM disks must reside on a vSphere datastore with sufficient free space. Alert threshold is 80% capacity; hard limit for new provisioning is 85%.

```
# Recommended disk layout
Disk 1: OS        50 GB   thick eager zeroed
Disk 2: Data      varies  thick eager zeroed
Disk 3: Swap/page 8 GB    thick eager zeroed (Windows only)
```

Do not store data on the OS VMDK. Separate OS and data disks from day one.

## Snapshot Policy

Snapshots are a temporary operational tool, not a backup mechanism.

| Rule | Requirement |
|---|---|
| Maximum active snapshots per VM | 1 |
| Maximum snapshot age (production) | 48 hours |
| Maximum snapshot age (non-production) | 7 days |
| Snapshot before patching | Permitted; must be deleted within 48 hours of successful patch |
| Snapshots on SQL/Oracle VMs | Only with application-consistent pre-freeze scripts |

Stale snapshots (older than the limit) are reported daily. After 7 days overdue, snapshots are deleted automatically with prior notification to the VM owner.

Never use snapshots as a substitute for a tested backup and restore process.

## Resource and DRS Configuration

All production VMs must be placed in a DRS-enabled cluster. DRS automation level: fully automated.

vCPU and memory allocations must be sized to the approved tier:

| Tier | vCPU | RAM |
|---|---|---|
| Small | 2 | 4 GB |
| Medium | 4 | 8 GB |
| Large | 8 | 16 GB |
| XL | 16 | 32 GB |
| Custom | Requires platform team sign-off | — |

CPU and memory hot-add must be enabled on all VMs to allow online scaling without a maintenance window. Confirm in VM settings: `Edit Settings > VM Options > Memory/CPU Hot Plug`.
