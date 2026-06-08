# Provision a New Workload

<div class="kb-summary">
Provisioning a new production VM correctly means more than clicking "New Virtual Machine" and
accepting defaults. Default settings give the VM no storage policy (zero redundancy on vSAN), no
security group membership (DFW rules don't apply), and no tagging (invisible to Aria Operations).
This scenario covers the full provisioning workflow: right-sizing, storage policy selection, NSX
segment assignment, tagging, and post-provision compliance verification.
</div>

```text
┌──────────────────────────────── Provision New Workload — Full Workflow ───────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  START: Application team requests new VM — gather requirements (CPU, RAM, disk, SLA tier, network tier) ││
│   └────────────────────────────────────┬─────────────────────────────────────────────────────────────────────┘│
│                                        │                                                              │
│                   ┌────────────────────┼────────────────────┐                                         │
│                   ▼                    ▼                    ▼                                         │
│   ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐                        │
│   │  Right-size VM       │  │  Choose vSAN storage │  │  Identify NSX        │                        │
│   │  CPU, RAM, disk      │  │  policy (FTT, RAID)  │  │  segment for VM NIC  │                        │
│   └──────────┬───────────┘  └──────────┬───────────┘  └──────────┬───────────┘                        │
│              └─────────────────────────┼──────────────────────────┘                                   │
│                                        ▼                                                              │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  Create VM in vCenter — attach to vSAN datastore with correct storage policy                             ││
│   └────────────────────────────────────┬─────────────────────────────────────────────────────────────────────┘│
│                                        │                                                              │
│                   ┌────────────────────┼────────────────────┐                                         │
│                   ▼                    ▼                    ▼                                         │
│   ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐                        │
│   │  Apply SPBM storage  │  │  Tag VM in vCenter   │  │  Add VM to NSX       │                        │
│   │  policy to all disks │  │  for Aria Ops groups │  │  security group      │                        │
│   └──────────┬───────────┘  └──────────┬───────────┘  └──────────┬───────────┘                        │
│              └─────────────────────────┼──────────────────────────┘                                   │
│                                        ▼                                                              │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  Post-provision: verify storage policy compliance, NSX segment, DFW group membership, Aria Ops tags      ││
│   └──────────────────────────────────────────────────────────────────────────────────────────────────────────┘│
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| vCenter Server | VM creation, resource pool placement, tag management |
| vSAN | Storage backend; every VM disk must have an explicit SPBM storage policy |
| NSX | Network segment assignment; Distributed Firewall security group membership |
| Aria Operations | Tag-based VM grouping for dashboards, alert routing, and capacity tracking |

---

## 1. Right-Size the VM

Match allocated resources to the application's actual working requirements — not to be generous.

| Resource | Sizing guideline |
|---|---|
| vCPU | Application peak CPU requirement, not average. Do not exceed 8 vCPU without testing NUMA impact on the target host |
| RAM | Application working set plus 20% headroom. Set reservation only if the workload requires guaranteed memory |
| Disk (OS) | Standard OS + swap — typically 60–80 GB |
| Disk (data) | Application data requirement plus 3 months growth estimate |
| NIC count | 1 vNIC per network segment — management, app tier, DB tier |

Never set vCPU count to match the number of physical CPUs on the host. A VM with 32 vCPUs on a
28-core host forces vCPU scheduling across NUMA domains, adding latency on every CPU-intensive
operation.

---

## 2. Choose the vSAN Storage Policy

Every VM disk on vSAN must have an explicit SPBM policy — a VM with no policy gets the default, which is typically FTT=0 (no redundancy).

Standard production policies:

| Policy name | FTT | Method | Use case |
|---|---|---|---|
| Production-Critical | 1 | RAID-1 (mirroring) | Databases, AD domain controllers, vCenter itself |
| Production-Standard | 1 | RAID-5 (erasure coding) | General application VMs, web tier |
| Development | 0 | None (no redundancy) | Dev and test environments only |

RAID-5 requires a minimum of 4 hosts in the cluster. RAID-1 requires 3. If the cluster has fewer
than the minimum host count for a policy tier, vSAN will not be able to satisfy it.

---

## 3. Assign the NSX Network Segment

Confirm the correct NSX logical segment for the workload tier before creating the VM.

```bash
# Verify the target segment exists in NSX Manager before VM creation
# NSX Manager → Networking → Segments → confirm segment name, VLAN binding, and connected T1 gateway
```

Expected: segment appears in NSX Manager with correct VLAN binding and T1 gateway attachment.

Each tier of a multi-tier application should use a separate segment:

| Tier | Example segment name |
|---|---|
| Management / jumpbox | mgmt-segment |
| Web / presentation | web-segment |
| Application logic | app-segment |
| Database | db-segment |

---

## 4. Create the VM

Create the VM on the target host and vSAN datastore with the right-sized resources.

```powershell
# PowerCLI — create VM on target host and vSAN datastore
New-VM -Name "vm-name" `
  -VMHost (Get-VMHost "esxi-host.domain.local") `
  -Datastore (Get-Datastore "vsanDatastore") `
  -MemoryGB 16 `
  -NumCpu 4 `
  -NetworkName "app-segment" `
  -DiskGB 100 `
  -DiskStorageFormat Thin

# If using a resource pool, add the -ResourcePool parameter
New-VM -Name "vm-name" -ResourcePool (Get-ResourcePool "Production") `
  -VMHost (Get-VMHost "esxi-host.domain.local") `
  -Datastore (Get-Datastore "vsanDatastore") `
  -MemoryGB 16 -NumCpu 4 -DiskGB 100 -DiskStorageFormat Thin
```

---

## 5. Apply SPBM Storage Policy to All Disks

Apply the correct storage policy to every hard disk on the VM and verify compliance status.

```powershell
$vm = Get-VM "vm-name"
$policy = Get-SpbmStoragePolicy "Production-Standard"

# Apply policy to all hard disks on the VM
Get-HardDisk -VM $vm | Set-SpbmEntityConfiguration -StoragePolicy $policy

# Verify policy is applied and compliant
Get-HardDisk -VM $vm | Get-SpbmEntityConfiguration |
  Select Entity, StoragePolicy, ComplianceStatus
```

Expected: `ComplianceStatus` shows `Compliant` for every disk. `NonCompliant` means vSAN cannot
currently satisfy the policy — commonly caused by insufficient hosts or disk capacity.

---

## 6. Tag the VM in vCenter for Aria Operations

Apply tags at VM creation time so the VM is immediately visible in Aria Operations dashboards and alert routing.

Assign the following tag categories at minimum:

| Tag category | Example value | Purpose |
|---|---|---|
| Environment | Production | Separates prod vs dev in all dashboards |
| Application | WebApp-01 | Groups VMs by application for capacity views |
| Owner | platform-team | Alert routing to the correct team |

From the vCenter UI: VM → **Tags & Custom Attributes** → **Assign Tag**.

Aria Operations picks up tag changes within the next collection cycle (typically 5 minutes).

---

## 7. Add the VM to the NSX Security Group

A new VM not in the correct security group has no DFW rules applied — east-west traffic is unrestricted.

NSX Manager → **Inventory** → **Groups** → select the appropriate group → **Members** → add the VM.

Security group membership can also be dynamic (automatic) based on VM tags or name patterns:

- If the group uses a tag-based membership criterion (e.g., all VMs tagged `Environment=Production`
  and `Application=WebApp-01`), applying the correct vCenter tags in step 6 adds the VM to the
  group automatically.
- If the group uses static membership, add the VM manually.

---

## 8. Post-Provision Validation

Verify storage policy compliance, NSX segment assignment, and tag application in one pass.

```powershell
# Verify storage policy compliance
Get-VM "vm-name" | Get-HardDisk |
  Get-SpbmEntityConfiguration |
  Select Entity, StoragePolicy, ComplianceStatus

# Verify NSX segment assignment
Get-VM "vm-name" | Get-NetworkAdapter |
  Select Name, NetworkName, Type

# Verify vCenter tags are applied
Get-VM "vm-name" | Get-TagAssignment |
  Select @{N="Category";E={$_.Tag.Category.Name}}, @{N="Tag";E={$_.Tag.Name}}
```

Expected: ComplianceStatus=Compliant, NetworkName matches target segment, all three tag categories present.

Confirm in NSX Manager that the VM appears as a member of the expected security groups under
**Inventory → Groups** before handing off to the application team.

---

## Post-Task Validation

| Check | Command / Location | Expected Result |
|---|---|---|
| Storage policy compliant | PowerCLI `Get-SpbmEntityConfiguration` | Compliant |
| NSX segment assigned | PowerCLI `Get-NetworkAdapter` | Correct segment name |
| NSX security group member | NSX Manager → Inventory → Groups | VM listed as member |
| vCenter tags applied | PowerCLI `Get-TagAssignment` | Environment, Application, Owner all set |
| VM visible in Aria Ops | Aria Ops → Inventory → VMs | VM appears, tags populated |

---

## Key Terms

| Term | Definition |
|---|---|
| SPBM | Storage Policy-Based Management — the vSAN framework that lets you define storage requirements (FTT, RAID level, encryption) as named policies and enforce them per VM disk, rather than configuring storage per-datastore |
| FTT | Failures to Tolerate — the SPBM policy parameter that sets how many simultaneous host or disk failures vSAN can absorb while keeping the VM's data accessible; FTT=1 tolerates one failure |
| RAID-1 | vSAN data protection method that mirrors each data component to N+1 hosts; requires 3 hosts minimum for FTT=1; uses more raw capacity than RAID-5 but has lower write latency |
| RAID-5 | vSAN erasure coding method that stripes data with parity across hosts; requires 4 hosts minimum for FTT=1; more storage-efficient than RAID-1 but higher CPU overhead on writes |
| NSX segment | A logical Layer-2 network boundary enforced in software by NSX; replaces VLANs for VM networking and serves as the attachment point for Distributed Firewall rules |
| DFW security group | An NSX Distributed Firewall construct that groups VMs by criteria (tags, names, IP ranges); firewall rules are applied to groups, not individual VMs — a VM outside the group receives no DFW rules |
| vCenter tag | A label applied to a vCenter object (VM, host, datastore) used to control group membership in NSX and Aria Operations; tag categories (Environment, Application, Owner) drive automated grouping |
| Aria Operations tagging | The mechanism by which Aria Operations discovers and groups VMs into application objects using vCenter tag assignments; tags must exist before the next collection cycle for dashboards to populate |
| thin provisioning | Disk format that allocates datastore space only as data is written rather than at creation time; inflates apparent free capacity — actual usage grows over time as the guest OS writes data |
| NUMA | Non-Uniform Memory Access — the physical topology of multi-socket servers where each CPU socket has its own local memory; VM vCPU counts that exceed one NUMA node's core count force cross-socket memory access and add latency |
| VMDK | Virtual Machine Disk — the file format for a VM's hard disk stored on a vSAN or VMFS datastore; each VMDK must have an SPBM policy assigned on vSAN |
| vNIC | Virtual Network Interface Card — the software-emulated NIC inside a VM; each vNIC connects to one NSX segment or portgroup and should map to a single network tier |
| dynamic group membership | NSX security group configuration where VMs are added or removed automatically based on matching criteria such as vCenter tags, VM names, or IP addresses — eliminating the need for manual group updates after provisioning |
