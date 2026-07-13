---
tags:
  - esxi
  - scenarios
  - vmware
  - vsphere-8
description: "A PSOD is ESXi's kernel panic — the host halts immediately and displays a purple screen with a backtrace. All VMs on the host are terminated instantly..."
---
# PSOD — ESXi Kernel Panic (Purple Screen of Death)

<div class="kb-summary">
A PSOD is ESXi's kernel panic — the host halts immediately and displays a purple screen with a backtrace.
All VMs on the host are terminated instantly. This scenario covers confirming HA restart status, capturing
the PSOD screen for diagnosis, correlating hardware events from iDRAC/iLO, retrieving post-reboot logs,
and identifying driver/firmware mismatch as the most common production cause.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

products_involved: "Products Involved" {shape: rectangle}
1_confirm_ha_is_restarting_vms: "1. Confirm HA Is Restarting VMs" {shape: rectangle}
2_capture_the_psod_screen: "2. Capture the PSOD Screen" {shape: rectangle}
3_check_idrac_ilo_hardware_event_log: "3. Check iDRAC / iLO Hardware Event Log" {shape: rectangle}
4_retrieve_logs_after_host_reboots: "4. Retrieve Logs After Host Reboots" {shape: rectangle}
5_generate_a_vmsupport_bundle: "5. Generate a vm-support Bundle" {shape: rectangle}

products_involved -> 1_confirm_ha_is_restarting_vms: uses
1_confirm_ha_is_restarting_vms -> 2_capture_the_psod_screen: uses
2_capture_the_psod_screen -> 3_check_idrac_ilo_hardware_event_log: uses
3_check_idrac_ilo_hardware_event_log -> 4_retrieve_logs_after_host_reboots: uses
4_retrieve_logs_after_host_reboots -> 5_generate_a_vmsupport_bundle: uses
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| ESXi | The failing component; kernel panic terminates all VMs; vmkernel.log holds the post-boot trace |
| vCenter | Detects host failure and triggers HA restart of VMs on surviving hosts |
| iDRAC / iLO | Remote console for capturing the PSOD screen; hardware event log for root cause |
| Aria Operations | Issues host-down alert; shows timeline of metrics leading up to crash |
| VxRail (OMIVV) | Manages driver and firmware bundles; out-of-band updates on VxRail bypass LCM validation |

---

## 1. Confirm HA Is Restarting VMs

The first 60 seconds after a PSOD are for confirming VM restart, not diagnosing the cause — VMs on the affected host are gone and cannot be recovered without a reboot.

In vCenter navigate to **Cluster → Monitor → vSphere HA → VM Restarts** and confirm affected VMs are listed with a restart timestamp and target host.

If VMs are not restarting, check:

- HA is enabled on the cluster (**Cluster → Configure → vSphere HA → Turn On**)
- Cluster has sufficient failover capacity (CPU and memory on remaining hosts)
- HA admission control policy is not blocking restarts

---

## 2. Capture the PSOD Screen

The purple screen contains the crash module name, error code, and backtrace — capture it immediately before the host auto-reboots.

Capture using:

- iDRAC/iLO **Virtual Console → Screenshot** function
- IPMI remote console screenshot
- Physical photograph if necessary

Critical elements to record:

```text
#PF Exception 14 in world XXXX:vmm0:<vmname>  → page fault in VMM world (driver or VM issue)
#GP Exception 13 in world XXXX:helper          → general protection fault in helper world
@BlueScreen: ASSERT bora/vmkernel/...          → assertion failure with source file and line
Backtrace: 0x...  vmw_pvscsi.o                 → module name = vmw_pvscsi (PVSCSI driver issue)
Backtrace: 0x...  nmlx5_core.o                 → module name = nmlx5_core (Mellanox NIC driver)
```

The module name in the backtrace is the most actionable piece of data — note it exactly.

---

## 3. Check iDRAC / iLO Hardware Event Log

A PSOD often follows a hardware event by seconds or minutes — correlating the SEL timeline with the PSOD timestamp narrows root cause significantly.

Access iDRAC (Dell) or iLO (HPE) → **System Event Log (SEL)** and look for events timestamped within 5 minutes before the PSOD:

| Hardware Event | Significance |
|---|---|
| Uncorrectable memory error (DIMM slot X) | Memory fault caused kernel to halt |
| Correctable memory error count exceeded | Memory degradation in progress |
| NIC link down / NIC CRC errors | Network hardware fault preceding driver panic |
| HBA / PCIe error | Storage controller fault |
| CPU machine check exception (MCE) | CPU or system bus fault |

A hardware event immediately before the PSOD indicates hardware replacement is required alongside any driver/firmware fix.

---

## 4. Retrieve Logs After Host Reboots

After the host reboots and SSH is accessible, collect the key log files.

```bash
cat /var/log/vmkernel.log | grep -iE "PSOD|panic|backtrace|oops" | tail -50
```


```text title="Expected output"
2024-01-15T14:32:18.123Z cpu2:65432)PANIC: Exception 14 in world 12345 ip=0x418f2a3c addr=0x7f8c9000
2024-01-15T14:32:18.456Z cpu5:87654)Backtrace for world 12345:
2024-01-15T14:32:18.789Z cpu5:87654) 0x418f2a3c 0x418f1b2c 0x418f0e4a 0x41234567
2024-01-15T14:32:19.012Z cpu2:65432)PSOD: Unrecoverable error in module 'vmkernel' at 0x418f2a3c
2024-01-15T14:32:19.234Z cpu3:45678)Oops: Page fault at 0x7f8c9000, code=0x00000002
2024-01-15T14:32:19.567Z cpu1:23456)Backtrace for world 87654:
2024-01-15T14:32:19.890Z cpu1:23456) 0x41234567 0x41234abc 0x41234def 0x41234999
2024-01-15T14:32:20.123Z cpu4:99999)PANIC: NMI watchdog timeout on CPU 4
2024-01-15T14:32:20.456Z cpu6:11111)Oops: NULL pointer dereference in vmk_HeapFree
2024-01-15T14:32:20.789Z cpu2:65432)PSOD: Dumping core to /vmfs/volumes/datastore1/vmkernel-dump-2024-01-15
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `grep: (standard input): No such file or directory` | Ensure vmkernel.log exists at /var/log/vmkernel.log; check file permissions with `ls -la /var/log/vmkernel.log`. |
    | `tail: cannot open '50' for reading: No such file or directory` | Remove the pipe and use `tail -50 /var/log/vmkernel.log | grep -iE "PSOD|panic|backtrace|oops"` instead (correct command order). |
```bash
cat /var/log/vmksummary.log | tail -20
```


```text title="Expected output"
2024-01-15T08:23:14.567Z: [vmkernel] 2621506 cpu0:65536)ALERT: NFS mount /vmfs/volumes/nfs-datastore-01 is degraded
2024-01-15T08:24:02.891Z: [vmkernel] 2621507 cpu2:65537)WARNING: Memory pressure at 87% on NUMA node 1
2024-01-15T08:25:45.123Z: [vmkernel] 2621508 cpu1:65538)INFO: vMotion migration completed for VM-prod-web-03 (duration: 45s)
2024-01-15T08:26:18.456Z: [vmkernel] 2621509 cpu3:65539)ERROR: iSCSI target 192.168.100.45:3260 unreachable
2024-01-15T08:27:33.789Z: [vmkernel] 2621510 cpu0:65540)WARNING: CPU ready time exceeded threshold on host esx-prod-04.lab.local
2024-01-15T08:28:01.234Z: [vmkernel] 2621511 cpu2:65541)INFO: HA agent heartbeat received from esx-prod-05.lab.local
2024-01-15T08:29:15.567Z: [vmkernel] 2621512 cpu1:65542)ALERT: Datastore /vmfs/volumes/local-ssd-01 free space below 5%
2024-01-15T08:30:44.890Z: [vmkernel] 2621513 cpu3:65543)WARNING: Network latency detected on vSwitch0 (avg 12ms)
2024-01-15T08:31:22.145Z: [vmkernel] 2621514 cpu0:65544)INFO: VM snapshot consolidation started for VM-backup-db-01
2024-01-15T08:32:55.678Z: [vmkernel] 2621515 cpu2:65545)ERROR: PSOD detected - initiating core dump to /vmfs/volumes/coredump
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `cat: /var/log/vmksummary.log: No such file or directory` | Verify the ESXi host is running and the log file path is correct; on some ESXi versions the file may be `/var/log/vmkernel.log` instead. |
    | `tail: cannot open '/var/log/vmksummary.log' for reading: Permission denied` | Run the command with root privileges using `sudo` or SSH directly as root to the ESXi host. |
Look for: the vmksummary.log gives a concise summary of the crash (timestamp, panic type, initiating world). The vmkernel.log contains the full backtrace.

Check hostd for precursor events in the seconds before the crash:

```bash
cat /var/log/hostd.log | grep -E "ERROR|WARNING" | tail -50
```


```text title="Expected output"
2024-01-15T09:23:47.123Z [INFO] hostd[94521] [Originator@6876 sub=Hostd] Hostd started
2024-01-15T09:24:12.456Z [WARNING] hostd[94521] [Originator@6876 sub=Libs] Failed to load module libvmkctl.so: symbol not found
2024-01-15T09:25:03.789Z [ERROR] hostd[94521] [Originator@6876 sub=Config] Unable to read /etc/vmware/config: Permission denied
2024-01-15T09:26:45.234Z [WARNING] hostd[94521] [Originator@6876 sub=Hostd] NTP sync failed, clock skew detected: 2.3 seconds
2024-01-15T09:27:18.567Z [ERROR] hostd[94521] [Originator@6876 sub=Vpx] Connection to vCenter lost: timeout after 30s
2024-01-15T09:28:22.891Z [WARNING] hostd[94521] [Originator@6876 sub=Hostd] Memory pressure: 87% utilization
2024-01-15T09:29:01.345Z [ERROR] hostd[94521] [Originator@6876 sub=Net] vSwitch0 link down on vmnic2
2024-01-15T09:30:15.678Z [WARNING] hostd[94521] [Originator@6876 sub=Storage] Datastore ds-nfs-01 latency high: 145ms
2024-01-15T09:31:42.912Z [ERROR] hostd[94521] [Originator@6876 sub=Hostd] Failed to allocate memory for VM vm-prod-web-03
2024-01-15T09:32:08.234Z [WARNING] hostd[94521] [Originator@6876 sub=Hostd] Swap usage increased to 12%
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `cat: /var/log/hostd.log: No such file or directory` | Verify the ESXi host is running and the hostd service is active with `systemctl status hostd` or check the correct log path for your vSphere version. |
    | `grep: (standard input): Permission denied` | Run the command with elevated privileges using `sudo` or as root, since hostd logs typically require root access. |
---

## 5. Generate a vm-support Bundle

Generate a support bundle after the host reboots — transfer it off the host before any further reboots as subsequent boots may overwrite logs.

```bash
vm-support -w /tmp/
```


```text title="Expected output"
Collecting support information for VM host-esx-prod-01.dc1.internal...
Gathering system logs... [████████████████████] 100%
Collecting diagnostic data... [████████████████████] 100%
Collecting performance metrics... [████████████████████] 100%
Creating support bundle...
Support bundle created: /tmp/esx-support-2024-01-15-14-32-45.tar.gz
Bundle size: 487 MB
Checksum (SHA256): a7f3e2c9d1b4e8f6a2c5d9e1f3a7b4c6d8e0f1a3b5c7d9e1f3a5b7c9d1e3f5
Support information collection completed successfully.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `vm-support: command not found` | Ensure you are running this command on an ESXi host with VMware Tools installed, or load the appropriate VMware module. |
    | `Permission denied: /tmp/` | Run the command with appropriate privileges (sudo or as root) or specify a writable directory where your user has write permissions. |
    | `No space left on device` | Free up disk space on the target filesystem or specify an alternate output directory with sufficient capacity (typically 500 MB+ required). |
This creates a compressed archive in `/tmp/` containing all logs, configuration, and system state. Transfer with SCP.

Alternatively, generate from vCenter: right-click the host → **Export System Logs** — equivalent but saves directly to your local machine.

---

## 6. Match Module Name to VMware KB

The backtrace module name almost always maps to a known VMware KB article — search `kb.vmware.com` using the module name and ESXi version.

```text
<module-name> PSOD <esxi-version>
```

Example searches:

```text
nmlx5_core PSOD 8.0
vmw_ahci PSOD 7.0 U3
lpfc PSOD 8.0 U2
```

Common modules and their hardware components:

| Module Name | Hardware Component |
|---|---|
| `vmw_ahci` | SATA/AHCI storage controller |
| `nmlx5_core` | Mellanox ConnectX NIC |
| `vmw_pvscsi` | Paravirtual SCSI controller |
| `lpfc` / `qlnativefc` | Fibre Channel HBA |
| `i40en` | Intel X710 NIC |

---

## 7. Check the VMware HCL for Driver and Firmware Versions

Most production PSODs are caused by a mismatch between NIC or HBA driver version on ESXi and the firmware on the hardware — the HCL lists validated combinations.

Navigate to `www.vmware.com/resources/compatibility/search.php` and search for your hardware model and ESXi version. The HCL entry shows:

- Supported firmware versions for the device
- Supported driver versions for that firmware
- Any known issues with specific combinations

Look for: the currently installed driver and firmware versions matching an HCL-validated pair. If not, update to a validated combination via vSphere Lifecycle Manager (standalone) or VxRail LCM (VxRail).

---

## 8. VxRail Hosts — Only Update Through VxRail LCM

A PSOD on a VxRail host after a manually applied driver update is a strong indicator that the update bypassed VxRail LCM and is now outside the validated matrix.

To resolve:

```bash
# Verify the manually installed driver version
esxcli software vib list | grep <module>
# Remove the non-LCM VIB
esxcli software vib remove --vibname <vib-name>
```


```text title="Expected output"
Name                           Version                        Vendor  Acceptance Level  Install Date
net-driver-bnx2x               20.2.209.0-1OEM.700.1.0.15160482  Broadcom  PartnerSupported  2024-01-15
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `VIB net-driver-bnx2x not found.` | Verify the exact VIB name with `esxcli software vib list | grep -i <partial-name>` and use the correct name from the output. |
    | `Cannot remove VIB: VIB is part of an Image Profile and cannot be removed independently.` | Use LCM (Lifecycle Manager) or boot into maintenance mode and remove via `esxcli software vib remove --vibname <vib-name> --force` if safe to do so. |
Then use VxRail Manager → LCM to apply the correct validated driver as part of a bundle upgrade. For the full VxRail LCM upgrade procedure, see the
[VxRail LCM Upgrade Failure](vxrail-lcm-upgrade-failure.md) scenario.

---

## Key Terms

| Term | Definition |
|---|---|
| PSOD | Purple Screen of Death — ESXi's kernel panic display; the host halts immediately, showing a purple screen with a backtrace identifying the crashing module and exception type |
| vmkernel.log | The primary ESXi kernel log file; contains the full backtrace from the most recent PSOD and all kernel-level driver and hardware events leading up to the crash |
| vmksummary | A condensed crash summary log written by ESXi on reboot; contains the PSOD timestamp, panic type, and initiating world — faster to read than the full vmkernel.log |
| vm-support | VMware CLI tool that generates a compressed diagnostic bundle containing all logs, configuration, and system state; required by VMware GSS and Dell support for case escalation |
| VIB | vSphere Installation Bundle — the package format used to install drivers and components on ESXi; VIBs installed outside of VxRail LCM break the validated driver/firmware matrix |
| HCL | Hardware Compatibility List — VMware's database of validated hardware models, driver versions, and firmware combinations for each ESXi release; the reference for confirming whether a driver/firmware pair is supported |
| iDRAC | Integrated Dell Remote Access Controller — the out-of-band management interface on Dell servers; used to capture the PSOD screen via Virtual Console and read the System Event Log for hardware faults |
| SEL | System Event Log — the hardware event log stored in iDRAC (Dell) or iLO (HPE); records uncorrectable memory errors, PCIe faults, and CPU machine checks that may trigger a PSOD |
| HA | vSphere High Availability — the cluster feature that monitors ESXi hosts and automatically restarts VMs on surviving hosts when a host fails due to PSOD or other crash |
| DIMM | Dual In-line Memory Module — a physical RAM stick; uncorrectable memory errors on a DIMM are a leading hardware cause of PSOD as the kernel halts rather than continue with corrupted memory |
| Backtrace | The stack trace printed on the PSOD screen showing the sequence of function calls that led to the panic; the module name at the bottom identifies the driver or component responsible |
| Panic frame | The register state and memory dump captured at the moment of the PSOD; used by VMware engineering and GSS to identify the exact code path that caused the kernel halt |

---

## Common Mistakes

- **Rebooting the host immediately without capturing the PSOD screen.** The purple screen is the
  primary diagnostic artifact. Rebooting before photographing it discards the module name, exception
  type, and backtrace — making root cause analysis significantly harder.
- **Not checking iDRAC/iLO hardware logs.** A PSOD triggered by a DIMM uncorrectable error or PCIe
  fault requires hardware replacement, not just a driver update. Hardware logs provide the timeline
  that connects the hardware event to the panic.
- **Updating drivers manually on VxRail.** VxRail's bundled validation makes driver/firmware
  combinations interdependent. Manual updates bypass this validation and are the leading cause of
  PSODs on VxRail nodes.
- **Assuming a one-off PSOD is random.** PSODs are deterministic — the same driver bug or hardware
  fault will panic the host again under the same conditions. Always identify and fix the root cause
  before returning the host to production.

---

## Related Scenarios

- [ESXi Host Disconnected from vCenter](esxi-host-disconnected.md) — if the host is
  unreachable after the crash with no console access, confirm PSOD vs other unresponsive states.
- [VxRail LCM Upgrade Failure](vxrail-lcm-upgrade-failure.md) — the correct path for
  applying driver and firmware fixes on VxRail nodes after a PSOD.
- [VM Inaccessible / HA Failover](vm-inaccessible-ha-failover.md) — when HA fails to restart
  VMs after a PSOD, the VM inaccessibility scenario covers the next steps.
