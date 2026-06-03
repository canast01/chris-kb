# Add ESXi Host to Cluster

<div class="kb-summary">
Adding a new ESXi host to an existing production cluster spans every major VMware product: hardware
firmware, ESXi installation, vCenter onboarding, vSAN disk claim, NSX transport node configuration,
LCM patch baseline compliance, and post-join monitoring in Aria Operations. Each step must be
completed in order — skipping or reordering steps causes network, storage, or security gaps that
are difficult to diagnose after the fact.
</div>

```text
┌──────────────────────────────── Add ESXi Host to Cluster — Procedure Flow ────────────────────────────────────────┐
│                                                                                                       │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  START: Rack and cable new host — update BIOS, HBA, and NIC firmware to vendor-minimum before install     ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                                                      ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Step 1 — Install ESXi via vendor ISO; configure management IP, FQDN hostname, DNS via DCUI (F2)         ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                                                      ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Step 2 — DNS pre-check: verify A record and PTR record resolve correctly from jump host                  ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                                                      ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Step 3 — SSH to host: configure NTP, configure vMotion and vSAN VMkernel ports, test vSAN MTU           ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                                                      ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Step 4 — Add host to vCenter cluster via PowerCLI; assign ESXi licence                                   ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                          ┌───────────────────────────┼───────────────────────────┐                    │
│                          ▼                           ▼                           ▼                    │
│          ┌───────────────────────┐   ┌───────────────────────────┐  ┌───────────────────────────┐     │
│          │  vSAN: claim disks,   │   │  NSX: configure transport │  │  LCM: remediate patch     │     │
│          │  verify disk group    │   │  node, install VIBs, TEP  │  │  baseline on new host     │     │
│          └──────────┬────────────┘   └──────────────┬────────────┘  └──────────────┬────────────┘     │
│                     └──────────────────────────────┬─┘─────────────────────────────┘                  │
│                                                    ▼                                                  │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Step 5 — Disable SSH; validate in Aria Operations; confirm HA agent, NTP, vSAN, NSX all green            ││
│  └────────────────────────────────────────────────────────────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| ESXi | The host being installed and onboarded; receives VMkernel, NTP, and SSH configuration |
| vCenter Server | Cluster join, HA agent deployment, licence assignment, inventory management |
| vSAN | Automatic disk claim on join; disk group health validation post-join |
| NSX | Transport node configuration; VIB installation; TEP VMkernel assignment |
| Lifecycle Manager (LCM) | Patch baseline compliance — ensures new host matches the cluster patch level |
| Aria Operations | Post-join health monitoring; validates no new alerts after host joins cluster |

---

## 1. Hardware Firmware and ESXi Installation

Before installing ESXi, update BIOS, HBA, and NIC firmware to the vendor-minimum supported version
for your ESXi build. Installing ESXi on out-of-date firmware causes driver compatibility issues that
are difficult to trace post-install.

Use the correct ISO for your environment:

| Environment | ISO to use |
|---|---|
| VxRail cluster | Dell VxRail custom ESXi ISO — includes VxRail-specific drivers and VIBs |
| Standalone Dell host | Dell EMC custom ESXi ISO — includes iDRAC and PERC drivers |
| Generic / other vendor | VMware stock ESXi ISO |

Boot from the ISO, accept the EULA, select the target disk, and complete the install. On first boot,
press **F2** at the DCUI to configure:

- Management IP, subnet mask, and default gateway
- Hostname — must be a fully qualified domain name (FQDN) matching both the DNS A record and PTR
  record. Example: `esxi-prod-07.domain.local`
- DNS server addresses
- Enable SSH temporarily for the configuration steps that follow

---

## 2. DNS Pre-Check

DNS must resolve in both directions before the host is added to vCenter. vCenter and vSAN use the
FQDN internally for inter-host communication. A missing PTR record causes HA agent registration
failures.

```bash
# From a jump host — verify forward resolution
nslookup esxi-new-host.domain.local

# Verify reverse resolution
nslookup <esxi-management-ip>
```

Both lookups must return the correct result before proceeding. Fix DNS if either fails — do not
proceed and rely on `/etc/hosts` workarounds.

---

## 3. NTP Configuration

```bash
# SSH to the new host
esxcli system ntp set --server ntp1.domain.local --server ntp2.domain.local
esxcli system ntp set --enabled true

# Verify NTP is syncing — look for * or + next to a server indicating a good source
ntpq -p
```

NTP must be synchronised before the host joins vCenter. SSO certificate validation fails if the
host clock differs from vCenter by more than 5 minutes.

---

## 4. VMkernel Port Configuration

Configure vMotion and vSAN VMkernel ports before adding the host to vCenter. If the host joins
vCenter first and the VMkernel ports are added later, vSAN disk claim may target the wrong VMkernel
and vMotion will silently fail for VMs placed on this host.

```bash
# vMotion VMkernel (vmk1)
esxcli network ip interface add --interface-name vmk1 --portgroup-name "vMotion"
esxcli network ip interface ipv4 set --interface-name vmk1 --type static \
  --ipv4 10.10.1.X --netmask 255.255.255.0
esxcli network ip interface tag add --interface-name vmk1 --tagname VMotion

# vSAN VMkernel (vmk2)
esxcli network ip interface add --interface-name vmk2 --portgroup-name "vSAN"
esxcli network ip interface ipv4 set --interface-name vmk2 --type static \
  --ipv4 10.20.1.X --netmask 255.255.255.0
esxcli network ip interface tag add --interface-name vmk2 --tagname VSAN
```

Test vSAN MTU before joining the cluster. Silent packet loss on the vSAN VMkernel causes IO errors
that only surface under load, not during basic connectivity checks.

```bash
# MTU test — -d disables fragmentation, -s 8972 is the vSAN jumbo frame test size
vmkping -I vmk2 -d -s 8972 <existing-host-vSAN-vmk-ip>
```

The ping must succeed. If it fails: check MTU settings on the switch port and VDS port group.
vSAN requires end-to-end MTU 9000 on the vSAN VMkernel path.

---

## 5. Add Host to vCenter

```powershell
# PowerCLI — add host to the target cluster
Add-VMHost -Name "esxi-new-host.domain.local" `
           -Location (Get-Cluster "cluster-name") `
           -User root -Password "<password>" `
           -Force
```

After the host appears in vCenter as **Connected**: assign an ESXi licence. Without a licence, the
host will enter evaluation mode and after 60 days all features become unavailable.

vCenter → **Administration** → **Licences** → **Assets** → **Hosts** → select the new host →
**Assign Licence Key**.

---

## 6. vSAN Disk Claim

If the cluster uses vSAN, vCenter automatically presents eligible disks on the new host for
claiming. Eligible disks: any disk not containing a system partition and not already part of a
disk group on another host.

vCenter → **vSAN** → **Disk Management** → select the new host.

Expected state: the host's cache and capacity disks appear and are claimed into a new disk group
automatically (if vSAN EZ-Claim is enabled on the cluster). If manual claiming is required:
select the disks, click **Claim Disks**, and assign cache and capacity roles.

```bash
# Verify disk group is healthy from ESXi CLI
esxcli vsan storage list
```

The disk group must show all disks in a healthy state before the next step.

---

## 7. NSX Transport Node Configuration

If the cluster uses NSX, the new host must be registered as a transport node before any VMs on it
can use NSX segments. Without this step, VMs placed on the new host by DRS will lose NSX network
connectivity.

NSX Manager → **System** → **Fabric** → **Hosts** → locate the new host → **Configure NSX**.

The configuration process:

1. NSX Manager pushes NSX VIBs to the host (installs NSX kernel modules)
2. vCenter and the host reboot the NSX services (no host reboot required)
3. NSX creates the Tunnel Endpoint (TEP) VMkernel port for overlay traffic
4. The transport node status changes to **Success**

Monitor: NSX Manager → **Fabric** → **Hosts** → watch **NSX Configuration** column. Configuration
typically completes within 5-10 minutes.

---

## 8. LCM Patch Baseline

After the host is joined and configured, ensure it matches the cluster's current patch level.
vCenter → **Lifecycle Manager** → **Hosts** → select the new host → **Check Compliance**.

If the host shows **Non-Compliant**: click **Remediate**. LCM places the host into maintenance mode,
applies the baseline, and reboots. The host must be in maintenance mode for remediation — LCM will
do this automatically.

For VxRail clusters: do not use vCenter LCM directly. Run LCM through VxRail Manager to maintain
the validated hardware-software bundle.

---

## 9. Disable SSH

Once all configuration is complete, disable SSH on the new host.

```bash
vim-cmd hostsvc/disable_ssh
```

Or from the vCenter UI: select the host → **Configure** → **Services** → **SSH** → **Stop**.
Set SSH startup policy to **Start and stop manually** to prevent it restarting on reboot.

---

## Post-Task Validation

| Check | Command / Location | Expected Result |
|---|---|---|
| Host connected to vCenter | vCenter inventory | Connected, no warnings |
| vSAN disk group healthy | `esxcli vsan storage list` | All disks claimed and healthy |
| NSX transport node | NSX Manager → Fabric → Hosts | Configured / Success |
| HA agent running | `/etc/init.d/vmware-fdm status` | Running |
| LCM compliant | vCenter → Lifecycle Manager | Compliant |
| NTP synced | `ntpq -p` | Active sync source shown |
| Aria Ops host visible | Aria Operations → Hosts | Host appears, no critical alerts |
| SSH disabled | vCenter → Host → Configure → Services | SSH stopped |

---

## Common Mistakes

- **Adding the host to vCenter before configuring VMkernel ports.** vSAN disk claim may target the
  wrong VMkernel and vMotion will silently fail for VMs that DRS places on this host.
- **Not checking MTU on the vSAN VMkernel.** A misconfigured switch port silently drops jumbo
  frames. The host appears healthy but vSAN IO fails under load.
- **Forgetting to configure the NSX transport node.** VMs that DRS places on the new host lose
  NSX overlay network connectivity. The symptom appears as a VM network issue, not a host issue,
  making it hard to trace.
- **Using vCenter LCM on a VxRail node.** VxRail nodes must be patched via VxRail Manager to
  maintain the validated firmware-driver-ESXi bundle.

---

## Related Scenarios

- Expand VxRail Cluster (Add Node)
- Host Maintenance and Patching
- VxRail LCM Upgrade Failure
- NSX Microsegmentation Rollout
