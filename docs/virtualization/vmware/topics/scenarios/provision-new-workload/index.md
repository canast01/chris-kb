# Provision a New Workload

<div class="kb-summary">
Provisioning a new production VM correctly means more than clicking "New Virtual Machine" and
accepting defaults. Default settings give the VM no storage policy (zero redundancy on vSAN), no
security group membership (DFW rules don't apply), and no tagging (invisible to Aria Operations).
This scenario covers the full provisioning workflow: right-sizing, storage policy selection, NSX
segment assignment, tagging, and post-provision compliance verification.
</div>

```text
┌──────────────────────────────── Provision New Workload — Full Workflow ─────────────────────────────────────────┐
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
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

Get workload requirements from the application team before creating the VM. The goal is to match
allocated resources to the application's actual working requirements — not to be generous.
Over-allocation wastes cluster capacity and degrades NUMA locality on large VMs.

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

Every VM disk stored on a vSAN datastore must have an explicit Storage Policy-Based Management
(SPBM) policy assigned. A VM with no policy assigned gets the default policy — which in most
environments has no redundancy (FTT=0). A single disk failure destroys that VM's data.

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

Before creating the VM, confirm the correct NSX logical segment for the workload tier. NSX
segments are the network equivalent of VLANs, but enforced in software with DFW rules attached.

```bash
# Verify the target segment exists in NSX Manager before VM creation
# NSX Manager → Networking → Segments → confirm segment name, VLAN binding, and connected T1 gateway
```

Each tier of a multi-tier application should use a separate segment:

| Tier | Example segment name |
|---|---|
| Management / jumpbox | mgmt-segment |
| Web / presentation | web-segment |
| Application logic | app-segment |
| Database | db-segment |

---

## 4. Create the VM

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

Applying the storage policy at creation time through the wizard is preferred, but when creating
via PowerCLI or when adjusting after creation, use:

```powershell
$vm = Get-VM "vm-name"
$policy = Get-SpbmStoragePolicy "Production-Standard"

# Apply policy to all hard disks on the VM
Get-HardDisk -VM $vm | Set-SpbmEntityConfiguration -StoragePolicy $policy

# Verify policy is applied and compliant
Get-HardDisk -VM $vm | Get-SpbmEntityConfiguration |
  Select Entity, StoragePolicy, ComplianceStatus
```

The `ComplianceStatus` field must show `Compliant`. A status of `NonCompliant` means vSAN cannot
currently satisfy the policy requirements — commonly caused by insufficient hosts or disk capacity.

---

## 6. Tag the VM in vCenter for Aria Operations

Aria Operations reads vCenter tags to group VMs into application objects for dashboards, alert
routing, and capacity tracking. Tags must be applied at VM creation time.

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

NSX Distributed Firewall rules apply to security groups, not to individual VMs. A new VM that is
not a member of the correct group has no DFW rules applied — it is effectively unrestricted on
east-west traffic.

NSX Manager → **Inventory** → **Groups** → select the appropriate group → **Members** → add the VM.

Security group membership can also be dynamic (automatic) based on VM tags or name patterns:

- If the group uses a tag-based membership criterion (e.g., all VMs tagged `Environment=Production`
  and `Application=WebApp-01`), applying the correct vCenter tags in step 6 adds the VM to the
  group automatically.
- If the group uses static membership, add the VM manually.

---

## 8. Post-Provision Validation

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

## Common Mistakes

- **Accepting the default storage policy.** In most environments the default policy is FTT=0 — no
  redundancy. A single disk failure on the vSAN host destroys the VM's data.
- **Not adding the VM to the NSX security group.** The VM has more network access than intended
  because no DFW rules apply. This is a security misconfiguration, not just a monitoring gap.
- **Oversizing vCPU.** A VM with more vCPUs than the host has physical CPUs per NUMA node forces
  cross-NUMA scheduling, adding latency to every memory access. Start conservatively and scale up
  if monitoring shows CPU saturation.
- **Skipping tagging.** An untagged VM is invisible to Aria Operations application-level dashboards
  and alert routing. Capacity is consumed but not tracked against any application owner.

---

## Related Scenarios

- Capacity Planning
- Host Maintenance and Patching
- Certificate Expiry and Rotation
