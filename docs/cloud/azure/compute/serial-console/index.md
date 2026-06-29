---
tags:
  - azure
---
# Serial Console

<div class="kb-summary">
Azure Serial Console provides out-of-band terminal access to a VM's serial port.

*Applies to: Azure*
</div>

---

```d2
direction: down

accessing_the_serial_console: "Accessing the Serial Console" {shape: rectangle}
linux_serial_console: "Linux Serial Console" {shape: rectangle}
windows_serial_console_sac: "Windows Serial Console — SAC" {shape: rectangle}
enabling_sac_on_windows_if_not_preen: "Enabling SAC on Windows (if not pre-enabled)" {shape: rectangle}
troubleshooting_common_scenarios: "Troubleshooting Common Scenarios" {shape: rectangle}

accessing_the_serial_console -> linux_serial_console: uses
linux_serial_console -> windows_serial_console_sac: uses
windows_serial_console_sac -> enabling_sac_on_windows_if_not_preen: uses
enabling_sac_on_windows_if_not_preen -> troubleshooting_common_scenarios: uses
```

## Accessing the Serial Console

Serial Console is accessed exclusively through the Azure portal:

1. Navigate to **Virtual Machines** > select VM > **Help** > **Serial console**
2. The portal connects to the VM's serial port and displays the current output buffer
3. Press **Enter** to send input if the prompt is idle

There is no `az` CLI command to directly open an interactive serial console session. However, you can verify readiness and collect the serial log programmatically.

```bash
# Get the serial log (non-interactive, last N KB of serial output)
az vm boot-diagnostics get-boot-log \
  --resource-group <rg> \
  --name <vm-name>

# Get URIs for both the log and screenshot
az vm boot-diagnostics get-boot-log-uris \
  --resource-group <rg> \
  --name <vm-name> \
  --output json
```


```text title="Expected output"
{
  "consoleLogBlobUri": "https://bootdiagstg12345.blob.core.windows.net/bootdiagnostics-myvm/myvm.serialconsole.log?sv=2021-06-08&sig=AbCdEfGhIjKlMnOpQrStUvWxYz1234567890%3D&se=2024-01-15T18%3A30%3A00Z&sr=b&sp=r",
  "serialConsoleLogBlobUri": "https://bootdiagstg12345.blob.core.windows.net/bootdiagnostics-myvm/myvm.serialconsole.log?sv=2021-06-08&sig=XyZ9876543210AbCdEfGhIjKlMnOpQrStUvWx%3D&se=2024-01-15T18%3A30%3A00Z&sr=b&sp=r"
}
```

!!! warning "Common errors"
    **`ResourceNotFound: The Resource 'Microsoft.Compute/virtualMachines/<vm-name>' under resource group '<rg>' was not found.`** — Verify the VM name and resource group name are correct and the VM exists in that region.
    **`AuthorizationFailed: The client '<client-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Compute/virtualMachines/read' over scope '/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Compute/virtualMachines/<vm-name>'.`** — Ensure your Azure account has at least Reader role on the VM or resource group.
    **`InvalidParameter: Boot diagnostics is not enabled on this VM.`** — Enable boot diagnostics on the VM by running `az vm boot-diagnostics enable --resource-group <rg> --name <vm-name>`.
---

## Linux Serial Console

On Linux VMs, the serial console presents a login prompt on `ttyS0`. Common use cases:

```bash
# After logging in via the serial console (in-console commands):

# Check filesystem for errors (run from single-user mode)
fsck -y /dev/sda1

# Edit fstab if the VM won't boot due to bad mount entry
mount -o remount,rw /
vi /etc/fstab

# Unlock an SSH user (if locked out)
passwd azureuser

# Check network configuration
ip addr show
cat /etc/netplan/*.yaml

# Restart networking
systemctl restart systemd-networkd
```


```text title="Expected output"
fsck from util-linux 2.37.2
e2fsck 1.46.2 (28-Feb-2021)
/dev/sda1: clean, 45821/524288 files, 892156/2097152 blocks

(no output — command completes silently)

New password: 
Retype new password: 
passwd: password updated successfully

1: lo: <LOOPBACK,UP,RUNNING> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
2: eth0: <BROADCAST,MULTICAST,UP,RUNNING> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 60:45:bd:a2:c1:f8 brd ff:ff:ff:ff:ff:ff
    inet 10.0.1.42/24 brd 10.0.1.255 scope global eth0

network:
  version: 2
  ethernets:
    eth0:
      dhcp4: true

(no output — command completes silently)
```

!!! warning "Common errors"
    **`fsck: /dev/sda1 is mounted`** — Run fsck only in single-user mode or from a recovery environment; reboot into single-user mode with `systemctl rescue`.
    **`E325: ATTENTION: Found a swap file by the name "/etc/fstab.swp"`** — Delete the swap file with `rm /etc/fstab.swp` before editing, or use `vi -r` to recover unsaved changes.
    **`Job for systemd-networkd.service failed because the control process exited with error code`** — Check for syntax errors in `/etc/netplan/*.yaml` with `netplan validate` and correct the YAML formatting.
To access GRUB on Linux via serial console, the VM must have `console=ttyS0` in its kernel command line. Most Azure marketplace images include this by default.

---

## Windows Serial Console — SAC

On Windows VMs, the Serial Console connects to the Special Administration Console (SAC). SAC requires EMS (Emergency Management Services) to be enabled.

```cmd
# From within SAC (entered after connecting via portal Serial Console):

# List running processes
cmd

# After 'cmd', switch to the command prompt channel
ch -si 1

# Inside the SAC cmd channel:

# Check disk
chkdsk C: /f

# View event logs
wevtutil qe System /c:20 /f:text

# Reset admin password
net user Administrator <NewPassword>

# Check network
ipconfig /all
netsh advfirewall show allprofiles
```

| SAC Command | Function |
|---|---|
| `cmd` | Open a new cmd.exe channel |
| `ch` | List active channels |
| `ch -si <n>` | Switch to channel n |
| `d` | Show system info |
| `i` | Show network config |
| `restart` | Reboot the machine |

---

## Enabling SAC on Windows (if not pre-enabled)

```bash
# Run via az vm run-command if the VM is still reachable via RDP/PowerShell
az vm run-command invoke \
  --resource-group <rg> \
  --name <win-vm-name> \
  --command-id RunPowerShellScript \
  --scripts "bcdedit /ems {current} on; bcdedit /emssettings EMSPORT:1 EMSBAUDRATE:115200; bcdedit /bootems {current} on"
```


```text title="Expected output"
{
  "value": [
    {
      "code": "ProvisioningState/succeeded",
      "displayStatus": "Provision succeeded",
      "message": "The operation completed successfully."
    },
    {
      "code": "ComponentStatus/stdout/succeeded",
      "displayStatus": "Stdout succeeded",
      "message": "The operation completed successfully.\nThe boot configuration has been successfully modified.\nEMS settings configured for port 1 at 115200 baud.\nBoot EMS enabled for current boot entry."
    }
  ]
}
```

!!! warning "Common errors"
    **`The client 'user@contoso.com' with object id 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' does not have authorization to perform action 'Microsoft.Compute/virtualMachines/runCommands/action'`** — Ensure your user account has the Contributor or Virtual Machine Contributor role on the resource group or VM.
    **`The resource group '<rg>' could not be found.`** — Verify the resource group name is correct and exists in your current Azure subscription using `az group list`.
    **`The virtual machine '<win-vm-name>' could not be found in resource group '<rg>'.`** — Confirm the VM name is spelled correctly and belongs to the specified resource group using `az vm list --resource-group <rg>`.
---

## Troubleshooting Common Scenarios

| Scenario | Approach |
|---|---|
| VM stuck at GRUB (Linux) | Use serial console to select kernel or enter single-user mode |
| `fstab` error on boot (Linux) | Boot to emergency shell, fix `/etc/fstab`, remount, reboot |
| Windows BSOD loop | SAC cmd channel — run `chkdsk`, check MBR/BCD |
| Password locked (Linux) | Single-user mode, `passwd` command |
| SSH daemon not starting | Serial console, `systemctl status sshd`, check port/config |
| Network misconfiguration | Serial console, fix netplan/ifcfg, restart networking |

```bash
# After fixing the issue remotely, force VM restart
az vm restart \
  --resource-group <rg> \
  --name <vm-name>
```


```text title="Expected output"
Command group 'vm' is in preview and under development. Reference and support levels: https://aka.ms/CLI_refstatus
(no output — command completes silently)
VM restart initiated successfully.
```

!!! warning "Common errors"
    **`ResourceNotFound : The Resource 'Microsoft.Compute/virtualMachines/<vm-name>' under resource group '<rg>' was not found.`** — Verify the resource group name and VM name are correct using `az vm list --resource-group <rg>`.
    **`AuthorizationFailed : The client '<user-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Compute/virtualMachines/restart/action' over scope '/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Compute/virtualMachines/<vm-name>'.`** — Ensure your Azure account has Contributor or Virtual Machine Contributor role on the resource group or VM.