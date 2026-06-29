---
tags:
  - azure
---
# Boot Diagnostics

<div class="kb-summary">
Azure Boot Diagnostics captures the serial console output and a screenshot of the VM's screen at boot time. It is essential for diagnosing VMs that fail to start or are unreachable via SSH/RDP.

*Applies to: Azure*
</div>

---

## Boot Diagnostics Flow

```d2
direction: right

vmStart: "VM Start / Restart" {shape: rectangle}
firmware: "UEFI / BIOS\nfirmware init" {shape: rectangle}
bootloader: "Bootloader\nGRUB2 / Windows Boot Mgr" {shape: rectangle}
osInit: "OS Initialisation\nkernel · systemd / WinInit" {shape: rectangle}
serialLog: "Serial Console Output\ncaptured to storage" {shape: rectangle}
screenshot: "Boot Screenshot\nPNG of screen state" {shape: rectangle}
diagnosticsAPI: "Boot Diagnostics API\nazure portal · serial console access" {shape: rectangle}

vmStart -> firmware
firmware -> bootloader
bootloader -> osInit
osInit -> serialLog
serialLog -> screenshot
screenshot -> diagnosticsAPI
```

## Overview

| Feature | Description |
|---|---|
| Serial log | Text output from the OS boot process (kernel messages, systemd, etc.) |
| Boot screenshot | A PNG snapshot of what the monitor would show (OS login screen, panic, etc.) |
| Managed storage | Azure stores diagnostics data automatically — no storage account needed |
| Custom storage | You can specify your own storage account for compliance or retention reasons |

---

## Enabling Boot Diagnostics

```bash
# Enable boot diagnostics with managed storage (recommended)
az vm boot-diagnostics enable \
  --resource-group <rg> \
  --name <vm-name>

# Enable boot diagnostics with a custom storage account
az vm boot-diagnostics enable \
  --resource-group <rg> \
  --name <vm-name> \
  --storage <storage-account-uri>

# Verify boot diagnostics is enabled
az vm show \
  --resource-group <rg> \
  --name <vm-name> \
  --query "diagnosticsProfile.bootDiagnostics" \
  --output json
```


```text title="Expected output"
{
  "enabled": true,
  "storageUri": "https://diagstg12345.blob.core.windows.net/"
}
```

!!! warning "Common errors"
    **`ResourceNotFound : The Resource 'Microsoft.Compute/virtualMachines/<vm-name>' under resource group '<rg>' was not found.`** — Verify the resource group name and VM name are correct with `az vm list --resource-group <rg>`.
    
    **`StorageAccountNotFound : The storage account '<storage-account-uri>' does not exist or you do not have permission to access it.`** — Ensure the storage account URI is valid and your account has Storage Blob Data Contributor role on that storage account.
    
    **`InvalidParameter : Boot diagnostics storage account must be in the same region as the virtual machine.`** — Create or specify a storage account in the same Azure region as your VM.
---

## Enabling at VM Creation

```bash
# Create VM with boot diagnostics enabled (managed storage)
az vm create \
  --resource-group <rg> \
  --name <vm-name> \
  --image Ubuntu2204 \
  --size Standard_D2s_v3 \
  --boot-diagnostics-storage "" \
  --admin-username azureuser \
  --generate-ssh-keys

# Create VM with boot diagnostics using a specific storage account
az vm create \
  --resource-group <rg> \
  --name <vm-name> \
  --image Ubuntu2204 \
  --size Standard_D2s_v3 \
  --boot-diagnostics-storage https://<storage-account>.blob.core.windows.net/ \
  --admin-username azureuser \
  --generate-ssh-keys
```


```text title="Expected output"
{
  "fqdns": "",
  "id": "/subscriptions/a1b2c3d4-e5f6-4789-a012-b3c4d5e6f7a8/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-01",
  "location": "eastus",
  "macAddress": "00:0D:3A:2E:5F:8C",
  "powerState": "VM running",
  "privateIpAddress": "10.0.1.42",
  "publicIpAddress": "52.170.45.123",
  "resourceGroup": "prod-rg",
  "zones": ""
}
{
  "fqdns": "",
  "id": "/subscriptions/a1b2c3d4-e5f6-4789-a012-b3c4d5e6f7a8/resourceGroups/prod-rg/providers/Microsoft.Compute/virtualMachines/web-vm-02",
  "location": "eastus",
  "macAddress": "00:0D:3A:2E:5F:8D",
  "powerState": "VM running",
  "privateIpAddress": "10.0.1.43",
  "publicIpAddress": "52.170.45.124",
  "resourceGroup": "prod-rg",
  "zones": ""
}
```

!!! warning "Common errors"
    **`ResourceGroupNotFound`** — Verify the resource group exists in the target subscription with `az group list` and use the correct `--resource-group` name.
    **`InvalidStorageAccountUri`** — Ensure the storage account URI follows the format `https://<storage-account>.blob.core.windows.net/` and the storage account exists in the same region and subscription.
    **`InsufficientQuotaAvailable`** — Request a quota increase for the Standard_D2s_v3 VM size in your subscription via the Azure portal or contact support.
---

## Reading Boot Logs

```bash
# Get the serial console log (text output from OS boot)
az vm boot-diagnostics get-boot-log \
  --resource-group <rg> \
  --name <vm-name>

# Save the boot log to a file for analysis
az vm boot-diagnostics get-boot-log \
  --resource-group <rg> \
  --name <vm-name> > boot-log.txt

# Get a SAS URL to download the boot screenshot
az vm boot-diagnostics get-boot-log-uris \
  --resource-group <rg> \
  --name <vm-name> \
  --output json
```


```text title="Expected output"
Booting [=========================] 100%
[    0.000000] Linux version 5.10.0-28-generic (buildd@lgw02-amd64-060) (gcc-10 (Debian 10.2.1-6) 10.2.1 20210110, GNU ld (GNU Binutils for Debian) 2.35.2) #30-Ubuntu SMP Tue Mar 7 12:46:06 UTC 2023 (Ubuntu 5.10.0-28.29-generic 5.10.209)
[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-5.10.0-28-generic root=UUID=a1b2c3d4-e5f6-7890-abcd-ef1234567890 ro quiet splash
[    0.000000] KERNEL supported cpus:
[    0.000000]   Intel GenuineIntel
[    0.000000]   AMD AuthenticAMD
[    0.000000]   Hygon HygonGenuine
[    0.000000]   Centaur CentaurHauls
[    0.000000]   zhaoxin   Shanghai
[    0.123456] Memory: 7891234K/8388608K available (14339K kernel code, 2741K rwdata, 4640K rodata, 2788K init, 7234K pages, 5432K reserved, 0K cma)
[    1.234567] systemd[1]: Started User Manager for UID 0.
[    2.345678] cloud-init[1234]: Cloud-init v. 23.1.1 running 'init' stage (PID 1234 TIME 2.34s)
[    3.456789] systemd[1]: Started Session c1 of user root.
{
  "consoleScreenshotBlobUri": "https://diagstg1a2b3c4d5e6f.blob.core.windows.net/bootdiagnostics-vmname-a1b2c3d4-e5f6-7890-abcd-ef1234567890/vmname.screenshot.bmp?sv=2021-06-08&ss=b&srt=sco&sp=rwdlac&se=2024-01-15T12:34:56Z&st=2024-01-14T12:34:56Z&spr=https&sig=AbCdEfGhIjKlMnOpQrStUvWxYz1234567890ABCDEFGH%3D",
  "serialConsoleLogBlobUri": "https://diagstg1a2b3c4d5e6f.blob.core.windows.net/bootdiagnostics-vmname-a1b2c3d4-e5f6-7890-abcd-ef1234567890/vmname.serialconsole.log?sv=2021-06-08&ss=b&srt=sco&sp=rwdlac&se=2024-01-15T12:34:56Z&st=2024-01-14T12:34:56Z&spr=https&sig=XyZ9876543210FeDcB
```
---

## Serial Console Access

Azure Serial Console provides interactive access to the VM's serial port, even when the VM has no network connectivity. It requires boot diagnostics to be enabled.

```bash
# Serial Console is accessed via the Azure portal:
# Virtual Machines > <vm-name> > Help > Serial Console

# Confirm prerequisites are met
az vm show \
  --resource-group <rg> \
  --name <vm-name> \
  --query "{BootDiagnostics:diagnosticsProfile.bootDiagnostics.enabled, PowerState:powerState}" \
  --output json

# Ensure the VM agent is running (required for some serial console features)
az vm get-instance-view \
  --resource-group <rg> \
  --name <vm-name> \
  --query "instanceView.vmAgent.statuses[?code=='ProvisioningState/succeeded']" \
  --output table
```


```text title="Expected output"
{
  "BootDiagnostics": true,
  "PowerState": "VM running"
}

Code    DisplayStatus    Message
------  ---------------  -----------------------------------------
ProvisioningState/succeeded  Provisioning succeeded  Guest Agent has reported success.
```

!!! warning "Common errors"
    **`ResourceNotFoundError: The Resource 'Microsoft.Compute/virtualMachines/<vm-name>' under resource group '<rg>' was not found.`** — Verify the resource group name and VM name are correct with `az vm list --resource-group <rg>`.
    
    **`AuthorizationFailed: The client '<user-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Compute/virtualMachines/read' over scope '/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Compute/virtualMachines/<vm-name>'.`** — Ensure your Azure account has at least Reader role on the resource group or VM.
| Serial Console Feature | Linux | Windows |
|---|---|---|
| GRUB menu access | Yes | N/A |
| Single-user / rescue mode | Yes | Via SAC |
| Special Admin Console (SAC) | N/A | Yes |
| CMD/PowerShell via SAC | N/A | Yes |
| Reset password via console | No (use `az vm user reset-ssh`) | Via SAC |

---

## Windows — Special Admin Console (SAC)

On Windows VMs, the Serial Console connects to the Special Administration Console.

```bash
# In SAC, type the following to open a command prompt channel:
cmd

# List active channels
ch -?

# Switch to cmd channel
ch -si <channel-number>
```


```text title="Expected output"
SAC>cmd
The Command Prompt session was successfully created.
SAC>ch -?
Channel List

Cmd                                      Cmd(1)
EMS                                      Cmd(2)
SAC                                      SAC(3)

SAC>ch -si 1
Name                : Cmd
Description         : Command Prompt
Type                : VT100/ANSI
Channel GUID        : 60908076-a466-11d1-b053-00c04fc2d4cd
Application Type    : Cmd
Command Line        : Cmd.exe
Transport           : Serial
Flags               : 
Access Level        : *
```

!!! warning "Common errors"
    **`ch -si: No such channel`** — Verify the channel number exists by running `ch -?` first and use the correct number in parentheses.
    **`SAC>: command not found`** — Ensure you are in the Serial Admin Console (SAC) session; if disconnected, reconnect via `sasutil.exe` or the Azure portal's Serial Console blade.
---

## Common Boot Issues and Diagnostics

| Symptom | What to Check | Resolution |
|---|---|---|
| VM stuck at "Waiting for FSCK" | Serial log for disk errors | Run `fsck` from rescue mode |
| Black screen / no login prompt | Boot screenshot shows blank | Check GPU driver or custom image issues |
| Kernel panic in serial log | Log shows `Kernel panic - not syncing` | Boot from recovery image, check disk |
| Windows BSOD (stop code) | Boot screenshot shows blue screen | Check stop code, review Windows Event Log |
| `fstab` error (Linux) | Log shows mount failure | Boot rescue mode, fix `/etc/fstab` |

```bash
# Disable boot diagnostics if no longer needed
az vm boot-diagnostics disable \
  --resource-group <rg> \
  --name <vm-name>
```


```text title="Expected output"
Command group 'vm boot-diagnostics' is deprecated and will be removed in a future release. Use 'vm boot-diagnostics disable' from 'az vm' instead.
(no output — command completes silently)
```

!!! warning "Common errors"
    **`ResourceGroupNotFound : The resource group '<rg>' could not be found.`** — Verify the resource group name with `az group list` and ensure you're using the correct subscription via `az account set --subscription <id>`.
    **`ResourceNotFound : The Resource 'Microsoft.Compute/virtualMachines/<vm-name>' under resource group '<rg>' was not found.`** — Confirm the VM name and resource group are correct by running `az vm list --resource-group <rg> --query "[].name"`.