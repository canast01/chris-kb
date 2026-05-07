# VMware Build Standards

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
