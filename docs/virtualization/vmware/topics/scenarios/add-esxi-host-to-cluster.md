---
tags:
  - esxi
  - scenarios
  - vmware
  - vsphere-8
description: "Adding a new ESXi host to an existing production cluster spans every major VMware product: hardware firmware, ESXi installation, vCenter onboarding, vSAN..."
---
# Add ESXi Host to Cluster

<div class="kb-summary">
Adding a new ESXi host to an existing production cluster spans every major VMware product: hardware
firmware, ESXi installation, vCenter onboarding, vSAN disk claim, NSX transport node configuration,
LCM patch baseline compliance, and post-join monitoring in Aria Operations. Each step must be
completed in order — skipping or reordering steps causes network, storage, or security gaps that
are difficult to diagnose after the fact.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

products_involved: "Products Involved" {shape: rectangle}
1_hardware_firmware_and_esxi_install: "1. Hardware Firmware and ESXi Installation" {shape: rectangle}
2_dns_precheck: "2. DNS Pre-Check" {shape: rectangle}
3_ntp_configuration: "3. NTP Configuration" {shape: rectangle}
4_vmkernel_port_configuration: "4. VMkernel Port Configuration" {shape: rectangle}
5_add_host_to_vcenter: "5. Add Host to vCenter" {shape: rectangle}

products_involved -> 1_hardware_firmware_and_esxi_install: uses
1_hardware_firmware_and_esxi_install -> 2_dns_precheck: uses
2_dns_precheck -> 3_ntp_configuration: uses
3_ntp_configuration -> 4_vmkernel_port_configuration: uses
4_vmkernel_port_configuration -> 5_add_host_to_vcenter: uses
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

Update BIOS, HBA, and NIC firmware to the vendor-minimum version before installing ESXi, then boot the correct ISO for your environment.

| Environment | ISO to use |
|---|---|
| VxRail cluster | Dell VxRail custom ESXi ISO — includes VxRail-specific drivers and VIBs |
| Standalone Dell host | Dell EMC custom ESXi ISO — includes iDRAC and PERC drivers |
| Generic / other vendor | VMware stock ESXi ISO |

On first boot, press **F2** at the DCUI to configure:

- Management IP, subnet mask, and default gateway
- Hostname — FQDN matching both the DNS A record and PTR record (e.g. `esxi-prod-07.domain.local`)
- DNS server addresses
- Enable SSH temporarily for the configuration steps that follow

---

## 2. DNS Pre-Check

DNS must resolve in both directions before the host is added to vCenter — a missing PTR record causes HA agent registration failures.

```bash
# From a jump host — verify forward resolution
nslookup esxi-new-host.domain.local

# Verify reverse resolution
nslookup <esxi-management-ip>
```


```text title="Expected output"
Server:		10.0.1.53
Address:	10.0.1.53#53

Name:	esxi-new-host.domain.local
Address: 192.168.100.45

Server:		10.0.1.53
Address:	10.0.1.53#53
45.100.168.192.in-addr.arpa	name = esxi-new-host.domain.local.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `** server can't find esxi-new-host.domain.local: NXDOMAIN` | Verify the hostname is correctly registered in DNS and check that the jump host can reach the DNS server (ping 10.0.1.53). |
    | `** server can't find 45.100.168.192.in-addr.arpa: NXDOMAIN` | Confirm the reverse DNS zone is configured on the DNS server and the PTR record exists for the ESXi management IP address. |
Expected: both lookups return the correct name/IP. Fix DNS if either fails — do not use `/etc/hosts` workarounds.

---

## 3. NTP Configuration

Configure NTP before the host joins vCenter — SSO certificate validation fails if the host clock differs from vCenter by more than 5 minutes.

```bash
esxcli system ntp set --server ntp1.domain.local --server ntp2.domain.local
esxcli system ntp set --enabled true
ntpq -p
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
 ntp1.domain.lo  10.0.0.1         2 u   64  128  377   12.543    2.156   1.234
 ntp2.domain.lo  10.0.0.2         2 u   32  128  377   14.821   -1.892   0.987
 LOCAL(0)        .LOCL.          10 l  998 1024    1    0.000    0.000   0.001
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Unknown option --server` | Use `esxcli system ntp set --servers=ntp1.domain.local,ntp2.domain.local` (comma-separated in a single argument) on some ESXi versions instead of repeated `--server` flags. |
    | `Error: Unable to resolve ntp1.domain.local` | Verify DNS resolution is working on the ESXi host and the NTP server hostnames are resolvable via `nslookup ntp1.domain.local`. |
    | `reach   delay   offset  jitter` (no peer entries)` | Wait 2-3 minutes for NTP to synchronize and re-run `ntpq -p`, or check firewall rules allow UDP port 123 outbound to the NTP servers. |
Look for: `*` or `+` next to a server in the `ntpq -p` output, indicating an active sync source.

---

## 4. VMkernel Port Configuration

Configure vMotion and vSAN VMkernel ports before adding the host to vCenter, then test vSAN MTU across the network.

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

# MTU test — -d disables fragmentation, -s 8972 is the vSAN jumbo frame test size
vmkping -I vmk2 -d -s 8972 <existing-host-vSAN-vmk-ip>
```


```text title="Expected output"
vmk1 successfully added.
vmk1 successfully configured.
vmk1 successfully tagged.
vmk2 successfully added.
vmk2 successfully configured.
vmk2 successfully tagged.
PING 10.20.1.42 (10.20.1.42): 8972 data bytes
8980 bytes from 10.20.1.42: icmp_seq=0 time=1.245 ms
8980 bytes from 10.20.1.42: icmp_seq=1 time=1.198 ms
8980 bytes from 10.20.1.42: icmp_seq=2 time=1.267 ms
8980 bytes from 10.20.1.42: icmp_seq=3 time=1.203 ms
--- 10.20.1.42 statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: The object already exists.` | Verify the VMkernel interface does not already exist with `esxcli network ip interface list` before adding. |
    | `Error: The portgroup does not exist.` | Ensure the port group "vMotion" or "vSAN" is created on the vSwitch before running the interface add command. |
    | `100% packet loss` | Confirm the target vSAN host's vmk2 IP is reachable and that jumbo frames (MTU 9000) are enabled on both the physical switch and vSAN port group. |
Expected: vmkping returns 0% packet loss. If it fails, check MTU on the switch port and VDS portgroup — vSAN requires end-to-end MTU 9000.

---

## 5. Add Host to vCenter

Add the host to the cluster via PowerCLI, then immediately assign a licence to avoid evaluation mode expiry.

```powershell
Add-VMHost -Name "esxi-new-host.domain.local" `
           -Location (Get-Cluster "cluster-name") `
           -User root -Password "<password>" `
           -Force
```

Expected: host appears in vCenter as **Connected**. Then assign the licence: vCenter → **Administration** → **Licences** → **Assets** → **Hosts** → select the new host → **Assign Licence Key**.

---

## 6. vSAN Disk Claim

If the cluster uses vSAN, claim disks via vCenter → **vSAN** → **Disk Management** → select the new host, then verify the disk group is healthy.

```bash
esxcli vsan storage list
```


```text title="Expected output"
Name                                    VSANID                                Tier  Allocated  Capacity
------------------------------------    ------------------------------------  ----  ---------  ----------
vsanDatastore                           52d33c41-a8f2-4e12-b1c3-7f9e2a1d5c8b  All   2.3 TB     4.6 TB
vsanDatastore-2                         61e44d52-b9f3-5f23-c2d4-8g0f3b2e6d9c  All   1.8 TB     3.2 TB
vsanDatastore-backup                    7af55e63-ca04-6g34-d3e5-9h1g4c3f7e0d  All   892 GB     2.0 TB
vsanDatastore-prod                      8bg66f74-db15-7h45-e4f6-0i2h5d4g8f1e  All   3.1 TB     5.5 TB
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `esxcli: command not found` | Run this command directly on an ESXi host via SSH or vSphere CLI, not from a local workstation. |
    | `Error: Could not connect to the vSAN cluster` | Verify the host is part of a vSAN cluster and vSAN is enabled on the cluster. |
Expected: all disks shown as claimed and healthy in the disk group. If EZ-Claim is not enabled, manually select disks, click **Claim Disks**, and assign cache and capacity roles.

---

## 7. NSX Transport Node Configuration

Register the host as an NSX transport node so VMs placed on it by DRS can reach NSX overlay segments.

NSX Manager → **System** → **Fabric** → **Hosts** → locate the new host → **Configure NSX**.

NSX Manager pushes VIBs to the host, creates the TEP VMkernel port for overlay traffic, and updates the transport node status — no host reboot required.

Expected: NSX Manager → **Fabric** → **Hosts** → **NSX Configuration** column shows **Success** within 5–10 minutes.

---

## 8. LCM Patch Baseline

Check the new host's patch compliance and remediate if it does not match the cluster baseline.

vCenter → **Lifecycle Manager** → **Hosts** → select the new host → **Check Compliance**.

If **Non-Compliant**, click **Remediate** — LCM places the host into maintenance mode, applies the baseline, and reboots automatically.

Expected: host shows **Compliant** after remediation. Note: for VxRail clusters, run LCM through VxRail Manager only — never vCenter LCM directly.

---

## 9. Disable SSH

Disable SSH once all configuration steps are complete.

```bash
vim-cmd hostsvc/disable_ssh
```


```text title="Expected output"
SSH has been disabled.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Unknown command: disable_ssh` | Verify the correct vSphere API command syntax; use `vim-cmd hostsvc/enable_ssh` or `vim-cmd hostsvc/query_config` to check SSH status instead. |
    | `vim-cmd: command not found` | Ensure you are running this command directly on the ESXi host (not a vCenter server) where vim-cmd is available in the PATH. |
Expected: SSH service stops. Set startup policy to **Start and stop manually** (vCenter → Host → **Configure** → **Services** → **SSH**) to prevent it restarting on reboot.

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

---

## Key Terms

| Term | Definition |
|---|---|
| DCUI | Direct Console User Interface — the local F2 menu on an ESXi host used to set management IP, hostname, and DNS before the host is reachable over the network |
| vmnic | Physical NIC presented to ESXi; the underlying uplink that VMkernel ports and VM portgroups share via the virtual switch |
| VMkernel (vmk) | A virtual network interface on ESXi used for host-originated traffic such as management, vMotion, vSAN, and TEP; not used by VM guest traffic |
| MTU | Maximum Transmission Unit — the largest frame size a network path will carry; vSAN requires end-to-end MTU 9000 (jumbo frames) to avoid silent packet fragmentation loss |
| vmkping | ESXi CLI tool for testing VMkernel-to-VMkernel connectivity; the `-d` flag disables fragmentation so MTU issues cause visible failure rather than silent fragmentation |
| DNS A/PTR record | A record maps hostname to IP; PTR record maps IP back to hostname — both must resolve correctly before vCenter and vSAN can register the host successfully |
| NTP | Network Time Protocol — keeps host clock in sync with vCenter; a drift of more than 5 minutes causes SSO certificate validation failures during cluster join |
| VIB | vSphere Installation Bundle — the package format used to install kernel modules and drivers on ESXi, including NSX kernel modules pushed during transport node configuration |
| LCM baseline | A defined patch level managed by vCenter Lifecycle Manager; hosts are checked for compliance against the baseline and remediated (patched + rebooted) if they do not match |
| NSX transport node | An ESXi host registered with NSX and configured to carry overlay (GENEVE-encapsulated) traffic; required before any VM on the host can connect to NSX logical segments |
| TEP | Tunnel Endpoint — a VMkernel port created by NSX on each transport node; carries GENEVE-encapsulated overlay traffic between hosts over the physical underlay network |
| FDM | Fault Domain Manager — the vSphere HA agent that runs on each ESXi host; coordinates VM restart decisions when a host failure is detected |
| vSAN disk group | A logical grouping of one cache disk and one or more capacity disks on a single ESXi host; the basic storage unit vSAN uses to contribute capacity to the shared datastore |
| iDRAC | Integrated Dell Remote Access Controller — Dell's out-of-band management interface for hardware-level access (power, console, firmware) independent of the ESXi OS state |

## Related Scenarios

- Expand VxRail Cluster (Add Node)
- Host Maintenance and Patching
- VxRail LCM Upgrade Failure
- NSX Microsegmentation Rollout
