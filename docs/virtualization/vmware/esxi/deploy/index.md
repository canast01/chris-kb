---
tags:
  - deployment
  - esxi
  - vmware
  - vsphere-8
search:
  boost: 2
---
# ESXi Host Deployment

<div class="kb-summary">
Step-by-step guide to deploying a new ESXi host: hardware readiness, installation, network and storage configuration, vCenter join, and baseline hardening.

*Applies to: vSphere 7.x / 8.x*
</div>

```text
┌────────────────────────────────────── ESXi Host Deployment Flow ──────────────────────────────────────┐
│                                                                                                       │
│  Phase 1: Physical Readiness                                                                          │
│  BIOS/firmware at vendor minimum  ·  VT-x on  ·  DNS A+PTR records created  ·  NTP reachable          │
│                                        │                                                              │
│                                        ▼                                                              │
│  Phase 2: ESXi Installation                                                                           │
│  Boot ISO or PXE  ·  Select disk  ·  Set root password  ·  DCUI: IP/hostname/DNS/NTP                  │
│                                        │                                                              │
│                                        ▼                                                              │
│  Phase 3: Network Configuration                                                                       │
│  vmk0 management  ·  vMotion VMkernel  ·  vSAN VMkernel MTU 9000  ·  Verify ping                      │
│                                        │                                                              │
│                                        ▼                                                              │
│  Phase 4: Storage Configuration                                                                       │
│  iSCSI targets / FC zoning  ·  Multipath PSP  ·  VAAI plugin  ·  Datastores visible                   │
│                                        │                                                              │
│                                        ▼                                                              │
│  Phase 5: Add to vCenter                                                                              │
│  Add Host wizard  ·  Assign licence  ·  Host profile remediate  ·  HA agent installs                  │
│                                        │                                                              │
│                                        ▼                                                              │
│  Phase 6: Hardening & Baseline                                                                        │
│  Lockdown mode normal  ·  SSH disabled  ·  NTP confirmed  ·  Syslog  ·  LCM baseline                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** vCenter Administrator role and SSH access to VCSA/ESXi hosts
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## Phase 1: Physical Host Readiness

Before installing ESXi, validate the hardware platform.

**Firmware**

Update server BIOS, HBA, and NIC firmware to vendor-recommended minimums before ESXi install. Mismatched firmware causes unreliable driver binding and PSOD.

**BIOS settings to verify**

| Setting | Required Value |
|---|---|
| VT-x / AMD-V | Enabled |
| VT-d / IOMMU | Enabled (for DirectPath I/O) |
| Hyperthreading | Enabled |
| C-States / Power management | OS Control or Performance |
| Secure Boot | Disabled during install; re-enable after |
| Boot order | ISO first, then local disk |

**DNS pre-creation**

Create A and PTR records for the host FQDN before installing ESXi. ESXi registers its hostname at first boot — missing DNS causes vCenter join failures and HA agent errors.

```bash
# Verify DNS resolves in both directions after record creation
nslookup esxi-host-01.domain.local
nslookup 10.0.0.10
```

**NTP reachability**

```bash
# From a jump host on the management VLAN
ntpdate -q ntp1.domain.local
```

**Cabling**

- Dedicated NICs for management, vMotion, vSAN, and VM traffic (or LACP bond)
- IPMI/iDRAC configured with its own management IP for out-of-band access

---

## Phase 2: ESXi Installation

**Boot media options**

| Method | Command / Notes |
|---|---|
| USB ISO | Write ISO to USB with Rufus or `dd`; boot from USB in BIOS |
| iDRAC/iLO virtual media | Mount ISO via BMC web UI; set virtual CD first in boot order |
| PXE (TFTP/HTTP) | Requires PXE server with `mboot.c32` and ESXi boot.cfg |
| Auto Deploy | Requires vCenter + Auto Deploy service; rule-based iPXE |

**Interactive installation sequence**

1. Boot from media — `VMware ESXi <version> Installer` screen appears
2. Press **Enter** to continue, **F11** to accept EULA
3. Select install disk (local SSD/HDD — not shared storage)
4. Select keyboard layout, set root password
5. Confirm install — data on disk will be overwritten
6. Reboot — remove boot media

**DCUI initial configuration (F2 → Configure Management Network)**

```text
Network Adapters:    vmnic0 (select management NIC)
VLAN (optional):     <management VLAN ID>
IPv4 Configuration:  Static — IP, Subnet, Gateway
DNS Configuration:   Primary + Secondary DNS, Hostname (FQDN)
Custom DNS Suffixes: domain.local
```

After saving, test connectivity:

```text
F12 → Test Management Network → ping gateway, DNS, hostname
```

**Enable SSH temporarily for configuration**

```text
F2 → Troubleshooting Options → Enable SSH
```

---

## Phase 3: Network Configuration

**VMkernel ports required per host**

| VMkernel | Traffic | VLAN | MTU | Required Service Tag |
|---|---|---|---|---|
| vmk0 | Management | MGMT VLAN | 1500 | Management |
| vmk1 | vMotion | vMotion VLAN | 9000 | vMotion |
| vmk2 | vSAN | vSAN VLAN | 9000 | vSAN |
| vmk3 | NFS/iSCSI | Storage VLAN | 9000 | — |

**Create vMotion VMkernel via esxcli**

```bash
# Add VMkernel port for vMotion
esxcli network ip interface add --interface-name vmk1 --portgroup-name "vMotion"
esxcli network ip interface ipv4 set --interface-name vmk1 --type static \
  --ipv4 10.10.1.10 --netmask 255.255.255.0

# Tag for vMotion traffic
esxcli vsan network list   # verify vSAN VMk
esxcli network ip interface tag add --interface-name vmk1 --tagname VMotion
```

**Create vSAN VMkernel**

```bash
esxcli network ip interface add --interface-name vmk2 --portgroup-name "vSAN"
esxcli network ip interface ipv4 set --interface-name vmk2 --type static \
  --ipv4 10.20.1.10 --netmask 255.255.255.0
esxcli network ip interface tag add --interface-name vmk2 --tagname VSAN

# Set MTU to 9000 on vSwitch (or on dvSwitch from vCenter)
esxcli network vswitch standard set --vswitch-name vSwitch1 --mtu 9000
```

**Verify connectivity from each VMkernel**

```bash
# Ping gateway from specific VMkernel
vmkping -I vmk1 10.10.1.1
vmkping -I vmk2 10.20.1.1 -d -s 8972   # 9000 MTU test (8972 = 9000 - 28 byte header)
```

**List all VMkernel interfaces**

```bash
esxcli network ip interface list
```

---

## Phase 4: Storage Configuration

**iSCSI software initiator**

```bash
# Enable software iSCSI initiator
esxcli iscsi software set --enabled=true

# Get initiator name (provide to storage team for IQN-based access)
esxcli iscsi adapter list

# Add dynamic discovery target
esxcli iscsi adapter discovery sendtarget add \
  --address 10.30.1.10:3260 --adapter vmhba65

# Rescan to discover LUNs
esxcli storage core adapter rescan --adapter vmhba65

# Verify targets
esxcli iscsi adapter target list
```

**Fibre Channel**

```bash
# List HBA WWPNs (provide to storage team for zoning)
esxcli storage core adapter list | grep -i fc

# After zoning is confirmed, rescan
esxcli storage core adapter rescan --all

# Verify LUN visibility
esxcli storage core device list | grep naa
```

**Multipathing (PSP)**

```bash
# Set Round Robin for active-active arrays
esxcli storage nmp device set --device naa.<id> --psp VMW_PSP_RR

# Set IOPS threshold for Round Robin (default 1000; lower for better spread)
esxcli storage nmp psp roundrobin deviceconfig set --device naa.<id> \
  --type iops --iops 1

# Verify paths
esxcli storage nmp path list --device naa.<id>
```

**VAAI plugin**

Install the array vendor's VAAI plugin via VUM/LCM if the array supports hardware acceleration (XCOPY, ATS, WriteSame). Verify:

```bash
esxcli storage core device vaai status get
```

**Confirm datastores**

```bash
esxcli storage filesystem list
```

---

## Phase 5: Add Host to vCenter

**Via vCenter UI**

1. Navigate to the target **Datacenter** or **Cluster**
2. Right-click → **Add Host**
3. Enter the host FQDN (not IP address)
4. Accept the SSL thumbprint
5. Enter root credentials
6. Assign the ESXi licence
7. Select **Datacenter/Cluster placement**
8. Host Profile: apply if a baseline profile exists → **Remediate**
9. Confirm — vCenter installs HA agent automatically

**Verify host state**

```bash
# In vCenter PowerCLI
Connect-VIServer vcenter.domain.local
Get-VMHost esxi-host-01.domain.local | Select-Object Name, ConnectionState, PowerState
```

Expected output:

```text
Name                          ConnectionState  PowerState
----                          ---------------  ----------
esxi-host-01.domain.local     Connected        PoweredOn
```

**HA agent and DRS**

Once the host is in a cluster with HA and DRS enabled, vCenter automatically:
- Installs `vmware-fdm` HA agent
- Adds host to DRS resource pool
- Assigns cluster-level vSAN disk claim (if vSAN cluster)

**Verify HA agent**

```bash
# From ESXi SSH
/etc/init.d/vmware-fdm status
```

---

## Phase 6: Hardening & Baseline

**Lockdown mode**

```bash
# Enable normal lockdown mode (via vCenter — disables direct root login)
# vCenter → Host → Configure → Security Profile → Lockdown Mode → Edit → Normal

# Via PowerCLI
$host = Get-VMHost "esxi-host-01.domain.local"
$hostView = Get-View $host
$hostView.EnterLockdownMode()
```

**Disable SSH and ESXi Shell post-configuration**

```bash
# vCenter → Host → Configure → Security Profile → Services → SSH → Stop + Policy: Start/stop manually
# Via esxcli from local console or one final SSH session:
esxcli system maintenanceMode set --enable false   # if in maintenance
vim-cmd hostsvc/disable_ssh
vim-cmd hostsvc/disable_esx_shell
```

**NTP service**

```bash
esxcli system ntp set --server ntp1.domain.local --server ntp2.domain.local
esxcli system ntp set --enabled true

# Confirm sync
esxcli system ntp get
ntpq -p
```

**Syslog forwarding**

```bash
# Forward to Aria Operations for Logs or a syslog server
esxcli system syslog config set --loghost=udp://arialogs.domain.local:514
esxcli system syslog config get   # verify
esxcli system syslog reload

# Open firewall for syslog
esxcli network firewall ruleset set --ruleset-id syslog --enabled true
esxcli network firewall refresh
```

**LCM baseline remediation**

1. vCenter → **Menu → Lifecycle Manager**
2. Attach the cluster baseline to the host
3. **Check Compliance** — note missing patches
4. **Stage** patches during business hours; **Remediate** in maintenance window
5. Host reboots automatically if kernel patches are included

---

## Post-Deployment Checklist

| Check | Command / Location | Expected |
|---|---|---|
| Host connected | vCenter inventory | Connected |
| HA agent running | `/etc/init.d/vmware-fdm status` | Running |
| NTP synced | `esxcli system ntp get` | NTP enabled, peers shown |
| Syslog forwarding | `esxcli system syslog config get` | loghost set |
| SSH disabled | vCenter → Security Profile | Stopped |
| Lockdown mode | vCenter → Security Profile | Normal |
| Datastores visible | `esxcli storage filesystem list` | All expected datastores |
| VMkernel pings | `vmkping -I vmk1 <gateway>` | 0% packet loss |
| LCM compliant | vCenter → Lifecycle Manager | Compliant / no critical patches |
| Host profile | vCenter → Host Profiles | Compliant |

---

## Verify

- **Host connected:** vSphere Client → host status shows Connected (green)
- **NTP sync:** `esxcli system time get` — time within 5 seconds of authoritative source
- **Network:** `esxcli network ip interface list` — vmk0 (management) shows Up
- **SSH disabled:** `esxcli system ssh get` — Policy: off (re-enable only when needed)
