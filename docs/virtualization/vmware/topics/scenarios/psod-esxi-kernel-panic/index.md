# PSOD — ESXi Kernel Panic (Purple Screen of Death)

<div class="kb-summary">
A PSOD is ESXi's kernel panic — the host halts immediately and displays a purple screen with a backtrace.
All VMs on the host are terminated instantly. This scenario covers confirming HA restart status, capturing
the PSOD screen for diagnosis, correlating hardware events from iDRAC/iLO, retrieving post-reboot logs,
and identifying driver/firmware mismatch as the most common production cause.
</div>

```text
┌───────────────────────────── ESXi PSOD — Response and Diagnosis Flow ───────────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│   │  START: Host goes offline; vCenter shows "Not Responding"; VMs show "Disconnected"              │ │
│   └──────────────────────────────────────────┬──────────────────────────────────────────────────────┘ │
│                                              │                                                        │
│              ┌───────────────────────────────┼───────────────────────────────┐                        │
│              ▼                               ▼                               ▼                        │
│   ┌─────────────────────┐        ┌─────────────────────┐        ┌─────────────────────┐               │
│   │ vCenter HA Monitor  │        │ iDRAC / iLO console │        │ Photograph / capture│               │
│   │ VM Restarts tab →   │        │ confirm purple screen│        │ PSOD backtrace text │              │
│   │ are VMs coming back │        │ vs other crash state │        │ before host reboots │              │
│   └────────┬────────────┘        └────────┬────────────┘        └─────────┬───────────┘               │
│            │                              │                               │                           │
│            ▼                              ▼                               ▼                           │
│   ┌─────────────────────┐        ┌─────────────────────┐        ┌─────────────────────┐               │
│   │ HA restarting VMs   │        │ iDRAC SEL → hardware│        │ Note: panic module  │               │
│   │ on other hosts      │        │ events (DIMM/NIC/HBA│        │ name (#PF/#GP/vmw_*) │              │
│   └─────────────────────┘        └─────────────────────┘        └─────────┬───────────┘               │
│                                                                            │                          │
│   ┌────────────────────────────────────────────────────────────────────────▼────────────────────────┐ │
│   │  Host reboots → SSH in → retrieve vmkernel.log, vmksummary.log → generate vm-support bundle    │  │
│   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────┐ │
│   │  Match module name to VMware KB → check HCL for driver+firmware combination → LCM if VxRail    │  │
│   └─────────────────────────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

The first 60 seconds after a PSOD are for confirming VM restart — not diagnosing the cause. VMs on
the affected host are gone and cannot be recovered without a reboot. Verify HA is working:

In vCenter navigate to **Cluster → Monitor → vSphere HA → VM Restarts**. You should see the affected
VMs listed with a restart timestamp and the target host where they are restarting.

If VMs are not restarting, check:

- HA is enabled on the cluster (**Cluster → Configure → vSphere HA → Turn On**)
- Cluster has sufficient failover capacity (sufficient CPU and memory on remaining hosts)
- HA admission control policy is not blocking restarts

---

## 2. Capture the PSOD Screen

The purple screen contains the crash module name, error code, and backtrace — the primary diagnostic
data. It is visible for only a few minutes before the host auto-reboots (if configured).

Capture it immediately using:

- iDRAC/iLO **Virtual Console → Screenshot** function
- IPMI remote console screenshot
- Physical photograph of the screen if necessary

The critical elements to record:

```text
#PF Exception 14 in world XXXX:vmm0:<vmname>  → page fault in VMM world (driver or VM issue)
#GP Exception 13 in world XXXX:helper          → general protection fault in helper world
@BlueScreen: ASSERT bora/vmkernel/...          → assertion failure with source file and line
Backtrace: 0x...  vmw_pvscsi.o                 → module name = vmw_pvscsi (PVSCSI driver issue)
Backtrace: 0x...  nmlx5_core.o                 → module name = nmlx5_core (Mellanox NIC driver)
```

The module name in the backtrace is the most actionable piece of data. Note it exactly.

---

## 3. Check iDRAC / iLO Hardware Event Log

A PSOD often follows a hardware event by seconds or minutes. Correlating the hardware event timeline
with the PSOD timestamp narrows the root cause significantly.

Access iDRAC (Dell) or iLO (HPE) for the affected host and navigate to:

- **iDRAC → System Event Log (SEL)**
- Look for events timestamped within 5 minutes before the PSOD

Critical hardware events to look for:

| Hardware Event | Significance |
|---|---|
| Uncorrectable memory error (DIMM slot X) | Memory fault caused kernel to halt |
| Correctable memory error count exceeded | Memory degradation in progress |
| NIC link down / NIC CRC errors | Network hardware fault preceding driver panic |
| HBA / PCIe error | Storage controller fault |
| CPU machine check exception (MCE) | CPU or system bus fault |

A hardware event immediately before the PSOD strongly suggests hardware replacement is required
alongside any driver/firmware fix.

---

## 4. Retrieve Logs After Host Reboots

After the host reboots and SSH is accessible, collect the key log files:

```bash
cat /var/log/vmkernel.log | grep -iE "PSOD|panic|backtrace|oops" | tail -50
```

```bash
cat /var/log/vmksummary.log | tail -20
```

The vmksummary.log contains a concise summary of the last crash including timestamp, panic type,
and the initiating world. The vmkernel.log contains the full backtrace.

Check hostd for any events in the seconds before the crash:

```bash
cat /var/log/hostd.log | grep -E "ERROR|WARNING" | tail -50
```

Look for recurring errors in the minutes before the crash timestamp — these are often the
precursor events that indicate a driver entering a bad state before the final panic.

---

## 5. Generate a vm-support Bundle

Attach a vm-support bundle to any VMware GSS case or keep it for internal diagnosis. Generate it
after the host reboots:

```bash
vm-support -w /tmp/
```

This creates a compressed archive in `/tmp/` containing all logs, configuration, and system state.
Transfer it off the host with SCP before any further reboots (subsequent boots may overwrite logs).

Alternatively, generate from vCenter: right-click the host → **Export System Logs**. This is
equivalent but generates the bundle remotely and saves it to your local machine.

---

## 6. Match Module Name to VMware KB

The module name from the PSOD backtrace almost always maps to a known VMware KB article or community
post. Search the VMware Knowledge Base at `kb.vmware.com` using:

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

The majority of PSODs in production environments are caused by a mismatch between the NIC or HBA
driver version installed on ESXi and the firmware version on the hardware. The VMware HCL lists the
exact validated combinations.

Navigate to `www.vmware.com/resources/compatibility` and search for your hardware model and ESXi
version. The HCL entry shows:

- Supported firmware versions for the device
- Supported driver versions for that firmware
- Any known issues with specific combinations

If the host is running a driver/firmware combination not in the HCL, update to a validated pair.
For standalone ESXi hosts, update using VUM (vSphere Lifecycle Manager). For VxRail, see Step 8.

---

## 8. VxRail Hosts — Only Update Through VxRail LCM

VxRail validates ESXi, driver, and firmware versions together as a bundle. Any out-of-band driver
update on a VxRail node — installing a driver directly via esxcli or vendor tools without going
through VxRail LCM — results in a combination that is outside VxRail's validated matrix.

A PSOD on a VxRail host after a manually applied driver update is a strong indicator that the update
bypassed VxRail LCM. To resolve:

1. Verify the manually installed driver version: `esxcli software vib list | grep <module>`
2. Remove the non-LCM VIB: `esxcli software vib remove --vibname <vib-name>`
3. Use VxRail Manager → LCM to apply the correct validated driver as part of a bundle upgrade.

For the full VxRail LCM upgrade procedure, see the
[VxRail LCM Upgrade Failure](../vxrail-lcm-upgrade-failure/index.md) scenario.

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

- [ESXi Host Disconnected from vCenter](../esxi-host-disconnected/index.md) — if the host is
  unreachable after the crash with no console access, confirm PSOD vs other unresponsive states.
- [VxRail LCM Upgrade Failure](../vxrail-lcm-upgrade-failure/index.md) — the correct path for
  applying driver and firmware fixes on VxRail nodes after a PSOD.
- [VM Inaccessible / HA Failover](../vm-inaccessible-ha-failover/index.md) — when HA fails to restart
  VMs after a PSOD, the VM inaccessibility scenario covers the next steps.
