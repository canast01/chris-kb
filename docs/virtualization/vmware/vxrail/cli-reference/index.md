---
tags:
  - vxrail
---
# VxRail CLI Reference

<div class="kb-summary">
VxRail CLI reference: `vxrail-upgrade`, `vxrail-health-check`, `vxrail-lcm-status`, `mystic` health API queries, and `vc-maint-mode` commands.

*Applies to: VxRail 7.x · 8.x*
</div>

---

```d2
direction: down

vxrail_manager_rest_api: "VxRail Manager REST API" {shape: rectangle}
vxrail_manager_ssh_cli: "VxRail Manager SSH CLI" {shape: rectangle}
powercli_vxrail_module: "PowerCLI + VxRail Module" {shape: rectangle}
esxcli_on_vxrail_nodes: "ESXCLI on VxRail Nodes" {shape: rectangle}
idrac_racadm_hardware_health: "iDRAC / RACADM (Hardware Health)" {shape: rectangle}

vxrail_manager_rest_api -> vxrail_manager_ssh_cli: uses
vxrail_manager_ssh_cli -> powercli_vxrail_module: uses
powercli_vxrail_module -> esxcli_on_vxrail_nodes: uses
esxcli_on_vxrail_nodes -> idrac_racadm_hardware_health: uses
```

## Overview

VxRail management interfaces:

| Interface | Access method | Use case |
|---|---|---|
| VxRail Manager REST API | HTTPS to VxRail Manager VM | Cluster, host, alert, LCM queries |
| VxRail Manager SSH CLI | SSH to VxRail Manager appliance | Health checks, diagnostics |
| PowerCLI + VxRail module | PowerShell on management host | Automation, lifecycle management |
| ESXCLI | SSH to individual ESXi host | Node-level host diagnostics |
| iDRAC / RACADM | SSH or HTTPS to iDRAC IP | Hardware health, BMC settings |

---

## VxRail Manager REST API

Base URL: `https://<vxrail-manager-ip>/rest/vxm`  
Authentication: HTTP Basic (local `mystic` or vCenter-joined domain user).

```bash
VXM="https://vxrail-mgr.example.com/rest/vxm"
AUTH="-u mystic:password --insecure"

# Cluster summary
curl -s $AUTH "$VXM/v1/cluster" | python3 -m json.tool

# Host list (all nodes)
curl -s $AUTH "$VXM/v1/hosts" | python3 -c "
import sys, json
hosts = json.load(sys.stdin)
for h in hosts:
    print(f\"{h['id']:40s}  state={h['operational_status']:12s}  health={h['health']}\")
"

# Specific host detail
HOST_SN="XXXXXXX"
curl -s $AUTH "$VXM/v1/hosts/${HOST_SN}" | python3 -m json.tool

# System alerts
curl -s $AUTH "$VXM/v1/system/alerts" | python3 -c "
import sys, json
alerts = json.load(sys.stdin)
for a in alerts:
    print(f\"{a.get('severity','?'):8s}  {a.get('message_id','?'):20s}  {a.get('message','')}\")
"

# Active only
curl -s $AUTH "$VXM/v1/system/alerts?status=active" | python3 -m json.tool

# System version and build info
curl -s $AUTH "$VXM/v1/system/cluster-hosts-info" | python3 -m json.tool

# VxRail software version
curl -s $AUTH "$VXM/v1/system/version" | python3 -m json.tool
```


```text title="Expected output"
{
  "cluster_name": "VXRail-Cluster-01",
  "cluster_id": "cluster-123abc",
  "health": "Healthy",
  "operational_status": "Online",
  "node_count": 4,
  "vcenter_version": "7.0.3"
}
node-01.vxrail.local                      state=Online       health=Healthy
node-02.vxrail.local                      state=Online       health=Healthy
node-03.vxrail.local                      state=Online       health=Healthy
node-04.vxrail.local                      state=Maintenance  health=Healthy
{
  "id": "XXXXXXX",
  "hostname": "node-01.vxrail.local",
  "operational_status": "Online",
  "health": "Healthy",
  "cpu_count": 32,
  "memory_gb": 512,
  "firmware_version": "2.11.0.1"
}
CRITICAL  VXRAIL_ALERT_001      Disk capacity on node-02 at 87%
WARNING   VXRAIL_ALERT_015      vSAN resync in progress
INFO      VXRAIL_ALERT_042      Scheduled maintenance window approaching
[
  {
    "severity": "CRITICAL",
    "message_id": "VXRAIL_ALERT_001",
    "message": "Disk capacity on node-02 at 87%",
    "timestamp": "2024-01-15T09:42:33Z"
  }
]
{
  "cluster_hosts": [
    {
      "hostname": "node-01.vxrail.local",
      "build_number": "24.1.0.1-build.12345",
      "status": "Online"
    },
    {
      "hostname": "node-02.vxrail.local",
      "build_number": "24.1.0.1-build.12345",
      "status": "Online"
    }
  ]
}
{
  "vxrail_version": "8.0.200",
  "vxrail_build": "24.1.0.1-build.12345",
  "release_date": "2024-01-10",
  "api_version": "v1"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Remove `--insecure` flag only if you have a valid CA certificate, or keep it for self-signed lab environments.
    **`jq: command not found`** — Install `python3-json` or use `python3 -m json.tool` as shown in the examples (already included in the script).
    **`curl: (7) Failed to connect to vxrail-mgr.example.com port 443: Connection refused`** — Verify the VXM hostname/IP is correct and the management interface is reachable with `ping vxrail-mgr.example.com` and `telnet vxrail-mgr.example.com 443`.
### LCM (Lifecycle Manager) Upgrades

```bash
# Check available upgrades
curl -s $AUTH "$VXM/v1/lcm/upgrade/selection" | python3 -m json.tool

# Get the current LCM status
curl -s $AUTH "$VXM/v1/lcm/upgrade/status" | python3 -m json.tool

# Initiate an LCM upgrade (replace target_version and vcenter details)
curl -s -X POST $AUTH "$VXM/v1/lcm/upgrade" \
  -H "Content-Type: application/json" \
  -d '{
    "bundle_file_locator": "/tmp/VxRail-7.0.xxx-bundle.zip",
    "target_hosts_to_remediate_in_parallel": 1,
    "vcenter": {
      "ip": "vcenter.example.com",
      "username": "administrator@vsphere.local",
      "password": "vcPassword"
    }
  }' | python3 -m json.tool

# Poll LCM upgrade progress
curl -s $AUTH "$VXM/v1/lcm/upgrade/status" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f\"State: {d.get('state','?')}  Progress: {d.get('progress','?')}%\")
print(f\"Step:  {d.get('step','?')}\")
"
```


```text title="Expected output"
{
  "upgrade_selections": [
    {
      "component": "vxrail",
      "current_version": "7.0.210",
      "available_versions": [
        "7.0.220",
        "7.0.230"
      ]
    },
    {
      "component": "vcenter",
      "current_version": "7.0.2.00000",
      "available_versions": [
        "7.0.3.00000"
      ]
    }
  ]
}
{
  "state": "IDLE",
  "progress": 0,
  "step": "None",
  "last_upgrade_time": "2024-01-15T08:32:15Z"
}
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "state": "RUNNING",
  "progress": 0,
  "step": "PRE_UPGRADE_CHECKS"
}
State: RUNNING  Progress: 35%
Step:  UPGRADING_VXRAIL_MANAGER
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to 192.168.1.100 port 443: Connection refused`** — Verify the VXM hostname/IP in the $VXM variable and ensure the management interface is reachable and the API service is running.
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`** — Confirm the $AUTH variable contains valid credentials (e.g., `-H "Authorization: Bearer $TOKEN"`) and the API endpoint is correct.
    **`"error": "Bundle file not found at /tmp/VxRail-7.0.xxx-bundle.zip"`** — Download the correct VxRail bundle to the specified path or update the bundle_file_locator path to match the actual file location.
---

## VxRail Manager SSH CLI

SSH to the VxRail Manager appliance IP as `mystic`.

```bash
ssh mystic@vxrail-mgr.example.com
```


```text title="Expected output"
The authenticity of host 'vxrail-mgr.example.com (192.168.1.42)' can't be established.
ECDSA key fingerprint is SHA256:aBcD1EfGhIjKlMnOpQrStUvWxYz2A3b4C5d6E7f8G9h.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'vxrail-mgr.example.com,192.168.1.42' (ECDSA) to the known_hosts file.
mystic@vxrail-mgr.example.com's password: 
Last login: Wed Jan 15 14:32:18 2025 from 10.20.30.40
VxRail Manager 7.0.510 (Build 12345)
mystic@vxrail-mgr:~$
```

!!! warning "Common errors"
    **`ssh: Could not resolve hostname vxrail-mgr.example.com: Name or service not known`** — Verify the VxRail Manager hostname or IP address is correct and resolvable from your network.
    **`Permission denied (publickey,password).`** — Confirm the username and password are correct, and that the user account exists on the VxRail Manager.
    **`ssh: connect to host vxrail-mgr.example.com port 22: Connection refused`** — Ensure the VxRail Manager is powered on and SSH service is enabled; check network connectivity to the management interface.
Once logged in, run `vxm-cli` commands:

```bash
# VxRail Manager version and system status
mystic@vxrail-mgr:~$ /opt/vmware/marvin/bin/vxm-cli system version
mystic@vxrail-mgr:~$ /opt/vmware/marvin/bin/vxm-cli cluster health
mystic@vxrail-mgr:~$ /opt/vmware/marvin/bin/vxm-cli node list

# Check all services within VxRail Manager
mystic@vxrail-mgr:~$ systemctl list-units --type=service --state=running | grep -i vx

# View VxRail Manager logs
mystic@vxrail-mgr:~$ journalctl -u marvin -f
mystic@vxrail-mgr:~$ tail -f /var/log/marvin/marvin.log

# Restart VxRail Manager service (if unresponsive)
mystic@vxrail-mgr:~$ sudo systemctl restart marvin
```


```text title="Expected output"
VxRail Manager Version: 7.0.410-28176892
Build Number: 28176892
Release Date: 2024-01-15

Cluster Health Status: HEALTHY
Overall Health: GREEN
vSAN Health: HEALTHY
vCenter Health: HEALTHY

Node List:
  Node 1: vxrail-node1.local (192.168.1.101) - ONLINE
  Node 2: vxrail-node2.local (192.168.1.102) - ONLINE
  Node 3: vxrail-node3.local (192.168.1.103) - ONLINE
  Node 4: vxrail-node4.local (192.168.1.104) - ONLINE

marvin.service                    loaded active running VxRail Manager Service
marvin-api.service                loaded active running VxRail API Service
marvin-db.service                 loaded active running VxRail Database Service
marvin-monitor.service            loaded active running VxRail Monitor Service

Jan 15 14:23:45 vxrail-mgr marvin[2847]: [INFO] Cluster health check completed successfully
Jan 15 14:23:46 vxrail-mgr marvin[2847]: [INFO] All nodes reporting nominal status
Jan 15 14:23:47 vxrail-mgr marvin[2847]: [INFO] vSAN capacity: 89.2% utilized

(no output — command completes silently)
```

!!! warning "Common errors"
    **`/opt/vmware/marvin/bin/vxm-cli: command not found`** — Verify the VxRail Manager package is installed with `rpm -qa | grep marvin` and check the installation path.
    **`Error: Unable to connect to VxRail Manager API (Connection refused)`** — Restart the marvin service with `sudo systemctl restart marvin` and wait 30 seconds for it to fully initialize.
    **`sudo: systemctl: command not found`** — Run the restart command without `sudo` if your user already has systemctl permissions, or check your PATH environment variable.
---

## PowerCLI + VxRail Module

Install the VxRail PowerCLI module from VMware on the management host.

```powershell
# Install modules
Install-Module -Name VMware.PowerCLI -Scope CurrentUser -Force
Install-Module -Name VMware.VxRail.PowerCLI -Scope CurrentUser -Force

# Connect to vCenter (VxRail is managed via vCenter)
Connect-VIServer -Server vcenter.example.com -User administrator@vsphere.local -Password "vcPassword"

# Connect to VxRail Manager
Connect-VxRailManager -Server vxrail-mgr.example.com -Username mystic -Password "password"

# Cluster info
Get-VxRailCluster

# All nodes
Get-VxRailNode

# Specific node
Get-VxRailNode -Id "XXXXXXX"

# System health
Get-VxRailSystemHealth

# Available LCM upgrade packages
Get-VxRailAvailableUpgrade

# Start upgrade
Update-VxRail -TargetVersion "7.0.xxx" -vCenterCredential $vcCred

# Check upgrade progress
Get-VxRailUpgradeStatus
```

---

## ESXCLI on VxRail Nodes

SSH to the individual ESXi node IP using the root or service account. Standard ESXCLI commands apply.

```bash
ssh root@vxrail-node01.example.com

# ESXi version
esxcli system version get

# NIC list and link state
esxcli network nic list

# Storage adapter and device list
esxcli storage core adapter list
esxcli storage core device list

# Check vSAN disk health (on vSAN cluster)
esxcli vsan storage list

# Active VMs on this host
esxcli vm process list

# Host memory and CPU summary
esxcli hardware memory get
esxcli hardware cpu global get

# Running services
esxcli system process list | head -30
```


```text title="Expected output"
Connected to vxrail-node01.example.com
   DCUI has started in FIPS mode

Product: VMware ESXi
Version: 7.0.3
Build: 19482537
Update: 3

Name    Driver      Link State    Speed    Duplex    MAC Address
vmnic0  bnx2x       Up            10000    Full      00:0a:95:9d:2e:f1
vmnic1  bnx2x       Up            10000    Full      00:0a:95:9d:2e:f2
vmnic2  bnx2x       Down          0        Half      00:0a:95:9d:2e:f3
vmnic3  bnx2x       Up            10000    Full      00:0a:95:9d:2e:f4

HBA Name    Driver      Link State    qlnq_fc
vmhba0      lpfc        link up       FC
vmhba1      lpfc        link up       FC
vmhba2      megaraid_sas link up      SAS

Device Name    Display Name                Size        Devfs Path
naa.6001405a1b2c3d4e5f6g7h8i9j0k1l2m3  NETAPP LUN 01  1099511627776  /vmfs/devices/disks/naa.6001405a1b2c3d4e5f6g7h8i9j0k1l2m3
naa.6001405a9z8y7x6w5v4u3t2s1r0q9p8o7n  NETAPP LUN 02  1099511627776  /vmfs/devices/disks/naa.6001405a9z8y7x6w5v4u3t2s1r0q9p8o7n

vSAN Disk Group 1:
  Disk: naa.5001405a1b2c3d4e (SSD, 960GB) - Healthy
  Disk: naa.5001405a9z8y7x6w (HDD, 3.6TB) - Healthy
  Disk: naa.5001405a5t4u3v2w (HDD, 3.6TB) - Healthy

World ID  Process ID  Used CPU  Reservation  Name
1048576   2097152     1200      0            vm-prod-web-01
1048577   2097153     850       0            vm-prod-db-02
1048578   2097154     420       0            vm-dev-test-03

Memory Information
  Physical Memory: 1048576 MB
  System Memory: 1048576 MB
  Free Memory: 524288 MB
  Swap Memory: 2097152 MB

CPU Package Count: 2
CPU Core Count: 32
CPU Thread Count: 64
CPU Speed: 2600 MHz

World ID  Process ID  Used CPU  Mem (MB)  Name
1         1           0         45        init
2         2           0         12        kslowd0
3         3           0         8         kslowd1
4         4           0         120       vmkernel
5         5           0         85        hostd
6         6           0
```
---

## iDRAC / RACADM (Hardware Health)

Accessible via SSH to the iDRAC IP or in-band via `racadm` on the ESXi host.

```bash
# SSH to iDRAC
ssh root@idrac-node01.example.com

# System info (model, service tag, BIOS, OS)
racadm getsysinfo

# Hardware inventory
racadm hwinventory

# Current sensor readings (fans, PSU, temps)
racadm getsensorinfo

# All chassis components
racadm chassisname
racadm getled

# Storage controller and disk status
racadm storage get controllers
racadm storage get pdisks -o

# RAID virtual disk status
racadm storage get vdisks -o

# SEL (System Event Log) — last 20 entries
racadm getsel --count 20

# Firmware versions for all components
racadm getversion -all

# In-band from ESXi host (requires Dell OpenManage)
esxcli system namespace list | grep dell
```


```text title="Expected output"
The system is ready for input.

System Information:
  System Model: PowerEdge R750
  Service Tag: ABC1234
  BIOS Version: 2.14.2
  OS: VMware ESXi 7.0.3

Fan Sensors:
  Fan1: 4200 RPM
  Fan2: 4150 RPM
  Fan3: 4180 RPM
PSU1 Status: OK (850W)
PSU2 Status: OK (850W)
System Board Inlet Temp: 28°C
System Board Exhaust Temp: 32°C

Chassis Name: vxrail-node-01
LED Status: System Health LED: Green

Storage Controllers:
  Controller 0: PERC H745P (Firmware: 50.16.01-3816)
    Status: OK

Physical Disks:
  Disk 0.0.0: 1.92TB SSD (Status: Online)
  Disk 0.0.1: 1.92TB SSD (Status: Online)
  Disk 0.0.2: 1.92TB SSD (Status: Online)

Virtual Disks:
  RAID 5 Volume 0: 5.46TB (Status: Optimal)
  RAID 5 Volume 1: 5.46TB (Status: Optimal)

SEL Records (Last 20):
  2024-01-15 14:32:15 | System Event Log | Log Area Reset | OK
  2024-01-15 10:15:42 | Temperature | Temp Above Threshold | Warning
  2024-01-14 08:22:18 | Power Supply | PSU 2 Recovered | OK

Firmware Versions:
  iDRAC: 5.10.20.00
  BIOS: 2.14.2
  PERC H745P: 50.16.01-3816
  NIC Firmware: 20.5.17

dell_asm
dell_openmanage
```

!!! warning "Common errors"
    **`Error: Unable to connect to iDRAC at idrac-node01.example.com`** — Verify the iDRAC hostname/IP is correct and reachable via `ping idrac-node01.example.com`, and confirm SSH is enabled in iDRAC settings.
    **`racadm: ERROR: DRAC_E_INVALID_PARAMETER`** — Ensure you are running the command with correct syntax; use `racadm help <command>` to verify the exact parameter format for your iDRAC firmware version.
    **`command not found: esxcli`** — Run the in-band command directly from an ESXi host (SSH to the host first), not from iDRAC, and verify Dell OpenManage Agent is installed with `rpm -qa | grep dell`.
## See also

- [VxRail — Overview](../../)
