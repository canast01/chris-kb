# VxRail CLI Reference


<div class="kb-summary">
> Part of the [VxRail](../index.md) reference.
</div>
```text
┌───────────────────────── Virtualization Vxrail Cli Reference — CLI Reference ─────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Vxrail CLI: command-line interface for all management and operational tasks          │   │
│   │            Access: SSH or REST client to management IP; authenticate as admin role            │   │
│   │        Commands: status, list, create, modify, delete, show, and diagnostic operations        │   │
│   │          Scripting: use REST API or CLI in automation for provisioning and reporting          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    SSH → authenticate → show status → configure → verify → log output                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Category     │     Command      │      Purpose      │      Output      │      Notes       │   │
│   │      Status      │   show status    │    Health check   │   State/alerts   │    Daily run     │   │
│   │       List       │     list all     │     Inventory     │   Name/ID/size   │    Read-only     │   │
│   │      Create      │  create volume   │     Provision     │    New object    │    Change req    │   │
│   │      Delete      │ delete resource  │    Decommission   │   Confirmation   │   Irreversible   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Virtualization Vxrail Cli Reference infrastructure · management network · monitoring     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vxrail             = Virtualization Vxrail Cli Reference platform overview and core concepts       │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

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

---

## VxRail Manager SSH CLI

SSH to the VxRail Manager appliance IP as `mystic`.

```bash
ssh mystic@vxrail-mgr.example.com
```

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
