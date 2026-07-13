---
tags:
  - architecture
  - esxi
  - vmware
  - vsphere-8
description: "Integrations reference covering Network Integration, Backup Integration, Monitoring Integration."
---
# ESXi — Integrations

<div class="kb-summary">
Integrations reference covering Network Integration, Backup Integration, Monitoring Integration.

*Applies to: vSphere 7.x · 8.x*
</div>
![ESXi — Integrations](../../../../../assets/virtualization-vmware-esxi-architecture-integrations.svg)

Ensure the NFS vmkernel adapter is on the correct VLAN and the NFS server export allows the ESXi management/NFS IP.

**NVMe/FC:** NVMe over Fabrics adapters appear as `vmhba` devices; configure via `esxcli nvme` subcommands. Requires NVMe-capable HBA and array.

**VAAI (vStorage APIs for Array Integration):** Offloads clone, zero, and lock primitives to compatible arrays (Pure Storage, Dell PowerStore, NetApp ONTAP). Verify VAAI is active:

```bash
esxcli storage core plugin list | grep NMP
vmkfstools -P /vmfs/volumes/<datastore>
```


```text title="Expected output"
NMP                                    VMware NMP Plugin                       1.0.0.0-0.0.0
NMP                                    VMware NMP Plugin                       1.0.0.0-0.0.0

VMFS-6 extent [0] blockSize 1048576, unmapGranularity 2097152, unmapPriority low
   /vmfs/volumes/datastore1 -> 4014402d-12345678-abcd-ef0123456789
   /vmfs/volumes/datastore1 (VMFS UUID: 4014402d-12345678-abcd-ef0123456789) mounted as VMFS-6
   Extent 0 - SCSI Reservation: Not Supported
   Capacity 2097152 MB, ~2048 GB
   Thin-Provisioned VMFS Extent
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Unknown command or namespace storage core plugin` | Verify esxcli is available and you are running ESXi 5.0 or later; if using vSphere CLI, ensure the vSphere SDK is installed. |
    | `Error: Could not find VMFS volume at /vmfs/volumes/<datastore>` | Replace `<datastore>` with an actual datastore name (e.g., `datastore1`) and verify the datastore is mounted with `esxcli storage filesystem list`. |
VAAI primitives (XCOPY, WRITE_SAME, ATS) significantly reduce ESXi CPU overhead during cloning and provisioning.

## Network Integration

ESXi networking uses either Standard vSwitch (vSS) or Distributed vSwitch (vDS). vDS is managed from vCenter and provides advanced features including LACP, LLDP, NetFlow, and port mirroring.

**vmkernel adapters** are created for each traffic type:

| vmkernel | Traffic Type | Typical IP |
|---|---|---|
| vmk0 | Management | Management subnet |
| vmk1 | vMotion | vMotion subnet |
| vmk2 | vSAN | vSAN subnet |
| vmk3 | NFS/iSCSI | Storage subnet |

**LACP/LAG:** On vDS, configure a Link Aggregation Group for uplink bonding. Requires LACP support on the upstream physical switch. Configure via vCenter > vDS > Configure > LACP.

**CDP/LLDP:** ESXi supports Cisco Discovery Protocol (CDP) and Link Layer Discovery Protocol (LLDP) for upstream switch discovery. View neighbour information:

```bash
esxcli network nic get --nic-name=vmnic0
# CDP/LLDP info visible in vSphere Client > host > Configure > Physical Adapters
```


```text title="Expected output"
Name                                                        Value
----                                                        -----
Driver                                                      ixgbe
Driver Version                                              5.13.5
Firmware Version                                            0x80001234
Speed                                                       10000 Mbps
Duplex                                                      Full
MAC Address                                                 00:50:56:c0:00:08
MTU                                                         1500
Enabled                                                     true
Connector Type                                              SFP+ (optical)
Transceiver Type                                            SFP+ (10GBASE-SR)
Link Status                                                 Up
Wake on LAN Supported                                       false
Wake on LAN Enabled                                         false
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Unknown option or malformed command line.` | Verify the NIC name is correct (use `esxcli network nic list` to confirm valid names like vmnic0, vmnic1, etc.). |
    | `Error: Could not get NIC information.` | Ensure the ESXi host is in a healthy state and the NIC is physically present; check `esxcli hardware pci list` to confirm the adapter is detected. |
## Backup Integration

**Veeam Backup & Replication** uses the VMware VADP (vStorage APIs for Data Protection) framework. A Backup Proxy VM (Windows-based) connects to ESXi hosts and the vCenter API to read VM data.

Changed Block Tracking (CBT) must be enabled on VMs for incremental backups:

```bash
# Check CBT status via PowerCLI
Get-VM <VMname> | Get-View | Select -ExpandProperty Config | Select ChangeTrackingEnabled
```


```text title="Expected output"
ChangeTrackingEnabled
                True
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Get-VM : The term 'Get-VM' is not recognized as the name of a cmdlet, function, script file, or operable program.` | Install VMware PowerCLI module with `Install-Module -Name VMware.PowerCLI -Force`. |
    | `Cannot find a provider with the name 'VimAutomation.Core'.` | Connect to vCenter first using `Connect-VIServer -Server <vcenter_fqdn> -Credential (Get-Credential)` before running Get-VM commands. |
CBT is enabled per VM in the VM's advanced settings (`ctkEnabled = TRUE`). Veeam enables this automatically when the first backup job runs.

**Transport modes:**

- **Hot-add:** Backup proxy VM is on the same ESXi host; VMDKs are attached directly — most efficient.
- **Network (NBD):** VMDKs are read over the network via ESXi NFC port (TCP 902); used when hot-add is unavailable.
- **Direct SAN:** Backup proxy reads VMDKs directly from FC/iSCSI LUNs; requires shared storage access.

## Monitoring Integration

**Aria Operations for Logs (Log Insight):** Forward ESXi syslog to a central log server:

```bash
esxcli system syslog config set --loghost=tcp://loginsight.example.com:514
esxcli system syslog reload
esxcli system syslog config get
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
   Hostname: loginsight.example.com
   Port: 514
   Protocol: tcp
   LogLevel: info
   LogToFile: true
   DefaultRotate: 30
   DefaultSize: 1024
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Unable to resolve hostname loginsight.example.com` | Verify the hostname is resolvable from the ESXi host using `ping loginsight.example.com` or check DNS/hosts configuration. |
    | `Error: Connection refused to loginsight.example.com:514` | Ensure the syslog server is running and listening on port 514, and that firewall rules allow traffic from the ESXi host. |
The Aria Operations for Logs VMware vSphere content pack parses ESXi syslog fields automatically.

**SNMP:** Configure SNMP traps for alerting to a monitoring platform:

```bash
esxcli system snmp set --communities=public --targets=monitor.example.com@162/public
esxcli system snmp set --enable=true
esxcli system snmp get
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
   Enable: true
   Authentication: default
   Communities: public
   Targets: monitor.example.com@162/public
   Trap Level: info
   Log Level: info
   Port: 161
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Unknown option --communities` | Use `--communities` only with `esxcli system snmp set`; verify your ESXi version supports this parameter (6.5+). |
    | `Error: Invalid target format 'monitor.example.com@162/public'` | Use the correct format `<hostname>@<port>/<community>` without quotes, or verify the hostname resolves on the ESXi host. |
    | `Error: SNMP agent is not running` | Enable SNMP with `esxcli system snmp set --enable=true` before querying, or check firewall rules allow UDP 161 outbound. |
**Aria Operations (vROps):** The ESXi adapter connects through vCenter. Add vCenter as an account in Aria Operations and the ESXi adapter automatically discovers all managed hosts. Metrics include CPU ready, memory balloon, storage latency, and network utilisation per host.

## See also

- [ESXi — How It Works](../how-it-works/)
- [ESXi Host Deployment](../../deploy/)
