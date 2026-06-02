# ESXi — Integrations


<div class="kb-summary">
Integrations reference covering Network Integration, Backup Integration, Monitoring Integration.
</div>

```text
ESXi Integration Map
                    ┌─────────────────────┐
                    │  vCenter Server      │
                    │  ├── Cluster / HA    │
                    │  ├── DRS / vMotion   │
                    │  └── Host Profiles   │
                    └──────────┬──────────┘
                               │ vpxa / hostd (TCP 443/902)
          ┌────────────────────▼──────────────────────┐
          │            ESXi Host (VMkernel)            │
          │                                            │
   ┌──────┤  Storage           Network                 │
   │ NSX  │  ├── FC / iSCSI    ├── vDS (vSphere port  │
   │ VIBs │  ├── NFS 3 / 4.1  │   groups, LACP, LLDP)│
   │ DFW  │  ├── NVMe/FC       ├── NIOC bandwidth ctrl │
   │ TEPs │  └── vSAN (HCI)    └── CDP / LLDP discovery│
   └──────┤                                            │
          │  Backup (VADP)     Monitoring              │
          │  ├── Veeam proxy   ├── Aria Ops (vROps)    │
          │  ├── CBT tracking  ├── Log Insight syslog  │
          │  └── Hot-add /     └── SNMP traps          │
          │      NBD / SAN                             │
          └────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────────── ESXi — Integrations ─────────────────────────────────────────┐
│                                                                                                       │
│  ESXi integrates with vCenter, storage arrays, AD, backup agents, monitoring.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             vCenter Integration              │  │             Storage Integration             │   │
│   │        vCenter manages host lifecycle        │  │            VMFS on iSCSI/FC/FCoE            │   │
│   │          vLCM patches ESXi firmware          │  │            NFS v3/v4.1 datastores           │   │
│   │          HA/DRS cluster membership           │  │            vSAN local disk pools            │   │
│   │         vMotion/svMotion operations          │  │            NVMe-oF fabric support           │   │
│   │           dvSwitch port group mgmt           │  │            VAAI offload to array            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  vCenter API → ESXi agent; backup uses VADP/CBT snapshot transport.                                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Identity / AD Integration           │  │             Backup / Monitoring             │   │
│   │            AD join for host auth             │  │           Veeam VADP proxy on ESXi          │   │
│   │            Smart card / CAC login            │  │            Commvault / Avamar CBT           │   │
│   │          LDAP for SSO identity src           │  │           Aria Ops agent per host           │   │
│   │          Local host users fallback           │  │              SNMP traps to NMS              │   │
│   │          vSphere Roles on AD groups          │  │            Syslog to Log Insight            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 hosts, SAN/NAS arrays, 10/25 GbE NICs, mgmt network for vCenter reach                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VADP     = vStorage APIs for Data Protection; snapshot-based backup API                              │
│  CBT      = Changed Block Tracking; tracks dirty disk blocks since backup                             │
│  VAAI     = vStorage APIs for Array Integration; offloads clone/zero to array                         │
│  vLCM     = vSphere Lifecycle Mgr; manages ESXi image + firmware baseline                             │
│  dvSwitch = Distributed vSwitch; centrally managed by vCenter across hosts                            │
│  VMFS     = VMware File System; clustered FS shared across ESXi hosts                                 │
│  NFS      = Network File System; supported as ESXi datastore v3 and v4.1                              │
│  NVMe-oF  = NVMe over Fabrics; high-perf block storage protocol on ESXi                               │
│  Aria Ops = VMware monitoring; collects ESXi metrics via agent/API                                    │
│  SNMP     = Simple Network Mgmt Protocol; ESXi sends traps on events                                  │
│  SSO      = Single Sign-On; vCenter auth; integrates AD for ESXi login                                │
│  svMotion = Storage vMotion; migrates VMDK between datastores live                                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Ensure the NFS vmkernel adapter is on the correct VLAN and the NFS server export allows the ESXi management/NFS IP.

**NVMe/FC:** NVMe over Fabrics adapters appear as `vmhba` devices; configure via `esxcli nvme` subcommands. Requires NVMe-capable HBA and array.

**VAAI (vStorage APIs for Array Integration):** Offloads clone, zero, and lock primitives to compatible arrays (Pure Storage, Dell PowerStore, NetApp ONTAP). Verify VAAI is active:

```bash
esxcli storage core plugin list | grep NMP
vmkfstools -P /vmfs/volumes/<datastore>
```

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

## Backup Integration

**Veeam Backup & Replication** uses the VMware VADP (vStorage APIs for Data Protection) framework. A Backup Proxy VM (Windows-based) connects to ESXi hosts and the vCenter API to read VM data.

Changed Block Tracking (CBT) must be enabled on VMs for incremental backups:

```bash
# Check CBT status via PowerCLI
Get-VM <VMname> | Get-View | Select -ExpandProperty Config | Select ChangeTrackingEnabled
```

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

The Aria Operations for Logs VMware vSphere content pack parses ESXi syslog fields automatically.

**SNMP:** Configure SNMP traps for alerting to a monitoring platform:

```bash
esxcli system snmp set --communities=public --targets=monitor.example.com@162/public
esxcli system snmp set --enable=true
esxcli system snmp get
```

**Aria Operations (vROps):** The ESXi adapter connects through vCenter. Add vCenter as an account in Aria Operations and the ESXi adapter automatically discovers all managed hosts. Metrics include CPU ready, memory balloon, storage latency, and network utilisation per host.
