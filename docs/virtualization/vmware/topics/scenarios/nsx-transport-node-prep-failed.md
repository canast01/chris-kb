---
tags:
  - nsx
  - nsx-4
  - scenarios
  - vmware
---
# NSX Transport Node Preparation Failed

<div class="kb-summary">
During NSX host preparation, the transport node transitions to Failed state and the host does not join
the NSX fabric. This scenario covers reading the exact error from NSX Manager, removing conflicting
NSX-V VIBs or stale NSX-T state, validating port reachability between the host and NSX Manager, and
retrying preparation cleanly. A staged rollout process prevents cascading failures across an entire
host cluster.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: right

MGR: "MGR" {shape: rectangle}
VC: "VC" {shape: rectangle}
ESX: "ESX" {shape: rectangle}
CONFLICT: "CONFLICT" {shape: rectangle}
VIBFAIL: "VIB installation fails · status: Not Configured" {shape: rectangle}
PORTFAIL: "Messaging bus unreachable · status: Failure" {shape: rectangle}
SUCCESS: "VIBs installed · Geneve tunnel up · status: Success" {shape: rectangle}
CLEANUP: "Remove conflicting VIBs · esxcli software vib remove" {shape: rectangle}
FIREWALL: "Open port 443 and 1235 · host → NSX Manager VIPs" {shape: rectangle}
RETRY: "Force Sync in NSX Manager" {shape: rectangle}

MGR -> VC
VC -> ESX
CONFLICT -> VIBFAIL
CONFLICT -> PORTFAIL
CONFLICT -> SUCCESS
VIBFAIL -> CLEANUP
PORTFAIL -> FIREWALL
CLEANUP -> RETRY
FIREWALL -> RETRY
RETRY -> SUCCESS
```

## Symptoms

| Indicator | Detail |
|---|---|
| NSX Manager UI | `System → Fabric → Hosts → <host>` shows Configuration Status = `Failed` or `Not Configured` |
| NSX Manager UI | Error banner visible on transport node detail page with error code and message |
| Missing VIBs | `esxcli software vib list` on host does not show `nsx-aggservice`, `nsx-context-mux`, etc. |
| ESXi log | `/var/log/esxupdate.log` contains VIB installation error messages |
| NSX syslog | `/var/log/nsx/nsx-syslog.log` shows connection refused or timeout to NSX Manager |

---

## 1. Read the Exact Error from NSX Manager

Navigate to: **NSX Manager → System → Fabric → Hosts → `<host-name>`**

Expand the **Errors** accordion. Note:

- Error code (e.g., `10020`, `10044`)
- Full message text — do not dismiss until you have copied it
- Timestamp — cross-reference with `/var/log/esxupdate.log` on the host

Common error patterns:

```text
Error 10020: VIB install failed: incompatible VIBs present
Error 10044: Unable to establish message bus connection to NSX Manager
Error 10012: Host acceptance level too restrictive for partner VIBs
```

---

## 2. Check for Conflicting VIBs

SSH to the affected ESXi host:

```bash
# Check for stale NSX-V VIBs (block NSX-T installation)
esxcli software vib list | grep -iE "esx-vsip|esx-vxlan|vmware-nsx"

# Check for partial NSX-T VIBs (failed mid-install)
esxcli software vib list | grep -i nsx
```


```text title="Expected output"
Name                                 Version                Install Date
esx-vsip                             6.7.0-20191015        2024-01-15
esx-vxlan                            6.7.0-20191015        2024-01-15
vmware-nsx-esx                       6.8.1-15842123        2024-03-22
vmware-nsx-esx-vib                   6.8.1-15842123        2024-03-22
vmware-nsx-manager-proxy             6.8.1-15842123        2024-03-22
esx-vxlan-mc                         6.7.0-20191015        2024-01-15
```

!!! warning "Common errors"
    **`grep: (standard input): No such file or directory`** — Verify esxcli is installed and the host has network connectivity to the vCenter server.
    **`Error: Unknown command or namespace`** — Ensure you are running this command directly on an ESXi host with root privileges, not from a remote vCenter client.
    **`VIB esx-vsip is present but vmware-nsx-esx is missing`** — Uninstall all NSX-V VIBs completely before attempting NSX-T installation using `esxcli software vib remove -n esx-vsip esx-vxlan`.
NSX-V VIBs (`esx-vsip`, `esx-vxlan`) are incompatible with NSX-T and must be removed before retrying.

---

## 3. Verify Host Acceptance Level

```bash
esxcli software acceptance get
```


```text title="Expected output"
Current Acceptance Level: CommunitySupported
```

!!! warning "Common errors"
    **`Could not connect to the host. Verify the host name, port, and credentials.`** — Ensure you are connected to the ESXi host via `esxcli` or vSphere CLI, or use the `-s <hostname>` flag with valid credentials.
    **`Unknown command or namespace software acceptance get.`** — Verify you are running this command on ESXi 5.0 or later; older versions do not support the acceptance level feature.
NSX-T VIBs are `PartnerSupported` — the host acceptance level must be `PartnerSupported` or lower
(i.e., `CommunitySupported`). If the host is set to `VMwareCertified` or `VMwareAccepted`, NSX VIBs
will be rejected:

```bash
esxcli software acceptance set --level PartnerSupported
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: Unknown option or parameter: --level`** — Verify the ESXi version supports this parameter; older versions use `--set-level` instead.
    **`Error: Permission denied`** — Run the command as root or with appropriate vSphere privileges; use `sudo` or execute from an account with Administrator role.
---

## 4. Verify Port Reachability

From the ESXi host, confirm both required ports reach NSX Manager:

```bash
# Port 443 — NSX Manager API and VIB download
nc -z <nsx-manager-vip> 443
esxcli network diag ping -H <nsx-manager-vip> -I vmk0 -c 4

# Port 1235 — NSX messaging bus (host to NSX Manager)
nc -z <nsx-manager-vip> 1235
```


```text title="Expected output"
Connection to 192.168.1.50 443 port [tcp/https] succeeded!
PING 192.168.1.50 from 192.168.1.100 via vmk0
Sent: 4 Received: 4 Lost: 0%
round-trip min/avg/max/stddev = 2.145/2.341/2.687/0.201 ms
Connection to 192.168.1.50 1235 port [tcp/*] succeeded!
```

!!! warning "Common errors"
    **`Connection to 192.168.1.50 443 port [tcp/https] failed: Connection refused`** — Verify NSX Manager is running and listening on port 443, or check firewall rules between the ESXi host and NSX Manager VIP.
    **`PING 192.168.1.50 from 192.168.1.100 via vmk0 ... Sent: 4 Received: 0 Lost: 100%`** — Confirm vmk0 management network connectivity and that the NSX Manager VIP is reachable from the ESXi host's management network.
    **`Connection to 192.168.1.50 1235 port [tcp/*] failed: Connection refused`** — Ensure NSX Manager messaging service is active and the host has not been disconnected from the NSX cluster; check NSX Manager logs for service errors.
If `nc` is unavailable on the ESXi host, check from a jump host on the same management network. Any
failure here points to a firewall or routing issue rather than a VIB conflict.

---

## 5. Check esxupdate.log for VIB Install Errors

```bash
grep -iE "error|fail|conflict|reject" /var/log/esxupdate.log | tail -40
```


```text title="Expected output"
2024-01-15T09:23:45.123Z [ERROR] VIB installation failed for esx-base: Dependency conflict detected
2024-01-15T09:24:12.456Z [WARN] Staging area validation: 2 packages marked for removal
2024-01-15T09:25:03.789Z [ERROR] Rollback initiated: Previous state restore in progress
2024-01-15T09:25:45.012Z [INFO] Conflict resolution: esx-ui version mismatch (7.0.1 vs 7.0.2)
2024-01-15T09:26:22.345Z [ERROR] VIB signature validation failed for net-driver-bnx2: Certificate expired
2024-01-15T09:27:01.678Z [WARN] Installation rejected: Insufficient disk space in /boot (412MB required, 389MB available)
2024-01-15T09:27:58.901Z [ERROR] Metadata conflict: Duplicate VIB entries detected in staging
2024-01-15T09:28:34.234Z [INFO] Retry attempt 1 of 3: Redownloading failed component
2024-01-15T09:29:15.567Z [ERROR] Installation failed: Incompatible hardware detected (CPU microcode update required)
2024-01-15T09:30:02.890Z [WARN] Rejection reason: Maintenance mode not enabled before update
```

!!! warning "Common errors"
    **`grep: /var/log/esxupdate.log: No such file or directory`** — Run this command on an ESXi host directly (via SSH or DCUI console), not from vCenter; the log only exists on ESXi systems.
    **`Permission denied`** — Execute the command as root or with sudo; standard users cannot read ESXi system logs.
Representative failure entries:

```text
2026-06-11T03:10:05Z esxupdate: ERROR: VIB esx-vsip conflicts with nsx-aggservice
2026-06-11T03:10:06Z esxupdate: ERROR: Installation aborted; rollback initiated
2026-06-11T03:15:22Z esxupdate: ERROR: Package download from <nsx-mgr>:443 timed out after 30s
```

---

## 6. Resolution

### Remove Conflicting NSX-V VIBs

Put the host into maintenance mode first if VMs are running:

```bash
# Via PowerCLI
Set-VMHost -VMHost <host-fqdn> -State Maintenance

# Via ESXi CLI (if vCenter unreachable)
esxcli system maintenanceMode set --enable true
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Connect-VIServer : Cannot find a valid certificate.`** — Ensure vCenter SSL certificate is valid or use `-SkipCertificateCheck` parameter in PowerCLI connection.
    **`Error: Unable to parse arguments from inputs: Unknown option --enable`** — Verify ESXi version supports the flag syntax; some older versions use `esxcli system maintenanceMode set -e true` instead.
Remove NSX-V VIBs:

```bash
esxcli software vib remove -n esx-vsip -n esx-vxlan --maintenance-mode
```


```text title="Expected output"
Removal Result
   Message: The following VIBs were successfully removed:
   esx-vsip-7.0.3-20.16.15939701
   esx-vxlan-7.0.3-20.16.15939701
   Reboot Required: true
```

!!! warning "Common errors"
    **`Error: Unknown option: --maintenance-mode`** — Use `--force` instead, or ensure the host is already in maintenance mode before running the command.
    **`Error: VIB esx-vsip not found`** — Verify the exact VIB name with `esxcli software vib list` and use the correct identifier.
### Remove Stale NSX-T VIBs (Partial Install)

If a previous preparation attempt left partial NSX-T VIBs:

```bash
esxcli software vib remove \
  -n nsx-aggservice \
  -n nsx-context-mux \
  -n nsx-exporter \
  -n nsx-sfhc \
  --maintenance-mode
```


```text title="Expected output"
Removal Result
   Message: The following VIBs were successfully removed:
   nsx-aggservice 6.4.10.1-28045389
   nsx-context-mux 6.4.10.1-28045389
   nsx-exporter 6.4.10.1-28045389
   nsx-sfhc 6.4.10.1-28045389

   Reboot Required: true
```

!!! warning "Common errors"
    **`Error: The host is not in maintenance mode. Please enter maintenance mode before removing VIBs.`** — Run `esxcli system maintenanceMode set --enable true` before executing the removal command.
    
    **`Error: VIB nsx-aggservice could not be removed. VIB is in use by running processes.`** — Stop all NSX services with `systemctl stop nsxd` and ensure no VMs are actively using NSX networking before retrying.
    
    **`Error: Insufficient space in /scratch partition. Required: 512MB, Available: 128MB.`** — Free up space on the ESXi host's /scratch partition or use `esxcli software vib remove --dry-run` to verify requirements before removal.
After removal, reboot the host to clear any loaded kernel modules:

```bash
reboot
```

### Return Host to Normal Mode and Retry Preparation

```bash
esxcli system maintenanceMode set --enable false
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: Unknown option or parameter: --enable`** — Use `--enable=false` (with equals sign) instead of `--enable false` (with space).
    **`Error: The object or item could not be found on the specified datastore.`** — Ensure the ESXi host is not in a critical state; try reconnecting the host in vCenter before disabling maintenance mode.
In NSX Manager: **System → Fabric → Hosts → `<host>` → Actions → Force Sync**

Monitor the preparation task in NSX Manager — it typically completes within 5–10 minutes.

### Address VIB Version Mismatch

If the error indicates a version mismatch between the VIB bundle and NSX Manager:

1. Confirm NSX Manager version: **System → Appliances → `<manager>` → Version**
2. Check the [VMware NSX Compatibility Matrix](https://interopmatrix.vmware.com) for the correct ESXi
   host version.
3. Either upgrade NSX Manager to a version compatible with the host ESXi version, or patch the host to
   match the NSX compatibility requirement before retrying.

### Open Firewall Port 1235

If port 1235 is blocked between hosts and NSX Manager VIPs, add a firewall rule:

```text
Source: ESXi management VMkernel subnet
Destination: NSX Manager VIP (all three nodes if cluster)
Port: TCP 1235
Direction: Outbound from hosts
```

---

## 7. Verification

```bash
# Confirm NSX VIBs are installed on host
esxcli software vib list | grep -i nsx
```


```text title="Expected output"
nsx-common                                1.0.0-20.5.1.1                    VMware    VisorModuleForCertification
nsx-esg                                   1.0.0-20.5.1.1                    VMware    VisorModuleForCertification
nsx-vxlan                                 1.0.0-20.5.1.1                    VMware    VisorModuleForCertification
nsx-vsip                                  1.0.0-20.5.1.1                    VMware    VisorModuleForCertification
nsx-netcpa                                1.0.0-20.5.1.1                    VMware    VisorModuleForCertification
```

!!! warning "Common errors"
    **`esxcli: command not found`** — Run the command directly on an ESXi host via SSH or vSphere Client console, not from a remote management station.
    **`(empty output / no NSX VIBs listed)`** — NSX VIBs are not installed on this host; use `esxcli software vib install` with the NSX bundle to install them.
Expected VIBs (version strings vary by NSX release):

```text
nsx-aggservice     <version>   Partner   PartnerSupported
nsx-context-mux   <version>   Partner   PartnerSupported
nsx-exporter       <version>   Partner   PartnerSupported
nsx-sfhc           <version>   Partner   PartnerSupported
nsx-ids            <version>   Partner   PartnerSupported
```

In NSX Manager, confirm:

- Transport node status = `Success` (green check icon)
- **Transport Nodes → `<host>` → BFD Status** = `Up` (Geneve tunnel established)

```bash
# Confirm TEP VMkernel adapter is present and has an IP
esxcli network ip interface list | grep -i tep
vmkping -I <tep-vmkernel> <peer-tep-ip> -c 4
```


```text title="Expected output"
Name                           PortBinding            DhcpEnabled   IPv4Address      IPv6Address
vmk10                          vxlan                  false         172.16.50.11     ::1
Reply from 172.16.50.12: bytes=60 time=2.45ms TTL=64
Reply from 172.16.50.12: bytes=60 time=2.31ms TTL=64
Reply from 172.16.50.12: bytes=60 time=2.48ms TTL=64
Reply from 172.16.50.12: bytes=60 time=2.39ms TTL=64

--- PING Statistics ---
Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
```

!!! warning "Common errors"
    **`vmkping: Unknown host <peer-tep-ip>`** — Replace `<peer-tep-ip>` with the actual IP address of the peer TEP VMkernel adapter (e.g., 172.16.50.12).
    **`Name                           PortBinding            DhcpEnabled   IPv4Address      IPv6Address` (no TEP adapter listed)** — Create the TEP VMkernel adapter on the vxlan port binding using `esxcli network ip interface add -i vmk10 -p vxlan -I 172.16.50.11 -N 255.255.255.0`.
---

## 8. Prevention

| Control | Implementation |
|---|---|
| Pre-check: VIB audit | Before NSX preparation, run `esxcli software vib list grep -i nsx` on all target hosts; confirm no NSX-V VIBs present |
| Compatibility matrix | Validate ESXi version against NSX compatibility matrix before beginning host preparation; pin ESXi baseline if needed |
| Staged rollout | Prepare one host, validate BFD tunnel and application connectivity, then proceed to remaining hosts in the cluster |
| Port validation | Include TCP 443 and 1235 reachability in the pre-work checklist for any NSX deployment or upgrade |
| Acceptance level | Set host acceptance level to `PartnerSupported` as a pre-requisite step in the runbook before triggering NSX preparation |

---

## Related Scenarios

- [NSX Connectivity Broken](nsx-connectivity-broken/index.md) — once hosts are prepared, this covers
  data-plane connectivity failures in the overlay network.
- [NSX DFW Blocking Application Traffic](nsx-dfw-blocking-application-traffic/index.md) — after
  successful preparation, DFW policy misconfigurations are a common next issue.
- [NSX Edge Failure / BGP Down](nsx-edge-failure-bgp-down/index.md) — edge node failures often
  surface after transport node preparation when edge nodes share host clusters.
