---
tags:
  - operations
  - vmware
  - vxrail
---
# VxRail — CLI Reference

<div class="kb-summary">
Complete command reference for VxRail operations: VxRail Manager REST API, esxcli vSAN and network commands, iDRAC RACADM, and PowerCLI vSAN cmdlets. Use this page as the go-to lookup for day-to-day VxRail CLI and API work.
</div>

```text
┌─────────────────────────────────────── VxRail — CLI Reference ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   VxRail Manager REST API  ·  base URL: https://<vxm-ip>/rest/vxm/v1/  ·  Basic auth (mystic) │   │
│   │   esxcli vSAN commands run over SSH to any ESXi host in the cluster                           │   │
│   │   iDRAC RACADM commands run over SSH to each node's dedicated iDRAC IP                        │   │
│   │   PowerCLI cmdlets run from a Windows or Linux host with VMware.PowerCLI module installed     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      VxRail Manager API     │  │        esxcli vSAN          │  │       iDRAC RACADM          │   │
│   │   GET /cluster              │  │   vsan health cluster get   │  │   getsysinfo                │   │
│   │   GET /hosts                │  │   vsan storage list         │  │   getsel                    │   │
│   │   GET /lcm/upgrade          │  │   vsan debug resync list    │  │   getversion -f bios/idrac  │   │
│   │   POST /lcm/bundle          │  │   vsan debug network test   │  │   nicstatistics             │   │
│   │   GET /support/bundle       │  │   vsan cluster get          │  │   serveraction powercycle   │   │
│   │   GET /system               │  │   hardware sensor list      │  │   storagecontroller get     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                                          ▼                                                            │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               PowerCLI vSAN Cmdlets                                           │   │
│   │   Get-VsanClusterHealthSummary  ·  Get-SpbmStoragePolicy  ·  Get-VM | Get-SpbmEntityConfig    │   │
│   │   Get-Datastore (vSAN capacity)  ·  Get-VMHostFirmware  ·  Get-VMHost (version/build)         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Dell PowerEdge servers · iDRAC OOB port per node · 25GbE NICs · ToR switches                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│  VxRail Manager API  = REST API on VxRail Manager VM; base path /rest/vxm/v1/                         │
│  mystic              = VxRail Manager local admin account; used for API and SSH login                 │
│  esxcli              = ESXi shell CLI; run over SSH to any cluster node                               │
│  RACADM              = iDRAC command-line interface; available over SSH to <idrac-ip>                 │
│  PowerCLI            = VMware PowerShell module; connects to vCenter for cluster automation           │
│  LCM bundle          = Dell upgrade package; uploaded via API POST /lcm/bundle                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## VxRail Manager — Login and Access

VxRail Manager is a Linux appliance VM. Access it via SSH or the web UI.

```bash
# SSH login to VxRail Manager
ssh mystic@<vxm-ip>

# Web UI
https://<vxm-ip>/ui

# REST API base URL
https://<vxm-ip>/rest/vxm/v1/
```

**Authentication:** HTTP Basic auth. Use the `mystic` account (or a dedicated service account created in VxRail Manager). Base64-encode credentials for `curl`:

```bash
# Encode credentials for curl
AUTH=$(echo -n 'mystic:YourPassword' | base64)

# Use in every API call
curl -sk -H "Authorization: Basic $AUTH" "https://<vxm-ip>/rest/vxm/v1/cluster"
```

---

## VxRail Manager REST API

### Common Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/rest/vxm/v1/cluster` | GET | Cluster summary: version, health, node count |
| `/rest/vxm/v1/hosts` | GET | All nodes: IDs, health, ESXi version, serial |
| `/rest/vxm/v1/lcm/upgrade` | GET | Current LCM upgrade job status |
| `/rest/vxm/v1/lcm/bundle` | POST | Upload a new LCM bundle (multipart/form-data) |
| `/rest/vxm/v1/lcm/precheck/status` | GET | Pre-upgrade check results |
| `/rest/vxm/v1/support/bundle` | POST | Trigger a support bundle collection |
| `/rest/vxm/v1/system` | GET | VxRail Manager version and build number |

### Cluster Info

```bash
# Get cluster summary
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxm-ip>/rest/vxm/v1/cluster" | python3 -m json.tool

# List all hosts with health status
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxm-ip>/rest/vxm/v1/hosts" | python3 -m json.tool

# Get VxRail Manager version and build
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxm-ip>/rest/vxm/v1/system" | python3 -m json.tool
```

### LCM Endpoints

```bash
# Upload an LCM bundle (multipart POST)
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  -F "file=@/tmp/VxRail-7.0.401-bundle.bin" \
  "https://<vxm-ip>/rest/vxm/v1/lcm/bundle"

# Check pre-upgrade status
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxm-ip>/rest/vxm/v1/lcm/precheck/status" | python3 -m json.tool

# Poll LCM upgrade job status
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxm-ip>/rest/vxm/v1/lcm/upgrade" | python3 -m json.tool

# Trigger node expansion
curl -sk \
  -X POST \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "hosts": [{
      "idrac": {
        "ip": "10.0.100.25",
        "username": "root",
        "password": "CalvinIdrac1!"
      }
    }]
  }' \
  "https://<vxm-ip>/rest/vxm/v1/cluster/expansion"
```

### Support Bundle

```bash
# Trigger support bundle collection and download
curl -sk \
  -X POST \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxm-ip>/rest/vxm/v1/support/bundle"

# Check collection status
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://<vxm-ip>/rest/vxm/v1/support/bundle/status"
```

---

## esxcli — vSAN Commands

Run these commands by SSH-ing to any VxRail node (`ssh root@<esxi-host-ip>`).

### vSAN Health

```bash
# Cluster-level health summary
esxcli vsan health cluster get

# Detailed health summary (all checks)
esxcli vsan health summary get

# Cluster configuration
esxcli vsan cluster get
```

### vSAN Storage

```bash
# List disk groups and disk status on this node
esxcli vsan storage list

# Filter for key fields
esxcli vsan storage list | grep -E "Disk Group UUID|Display Name|Is SSD|Device:"
```

### vSAN Resync and Rebuild

```bash
# Check object resync status — look for Remaining Bytes = 0
esxcli vsan debug resync list

# Watch resync in a loop (exit when done)
watch -n 10 'esxcli vsan debug resync list | grep -E "Total|Remaining"'
```

### vSAN Network Test

```bash
# Run vSAN network connectivity test across all nodes
esxcli vsan debug network test

# List vSAN VMkernel ports
esxcli vsan network list
```

---

## esxcli — Network Commands

```bash
# List all VMkernel interfaces (IPs, MTU, tags)
esxcli network ip interface list

# Show IPv4 addresses
esxcli network ip interface ipv4 get

# Show VMkernel tags (management, vSAN, vMotion)
esxcli network ip interface tag get -i vmk0
esxcli network ip interface tag get -i vmk1
esxcli network ip interface tag get -i vmk2

# List vSwitches (standard)
esxcli network vswitch standard list

# List VDS uplink info
esxcli network vswitch dvs vmware list

# Check physical NIC link status
esxcli network nic list
esxcli network nic get -n vmnic0
```

---

## esxcli — Hardware Sensors

```bash
# Temperature sensors
esxcli hardware sensor list --type Temperature

# Fan speed sensors
esxcli hardware sensor list --type Fan

# Power sensors
esxcli hardware sensor list --type Power

# Platform info (model, serial, BIOS version)
esxcli hardware platform get

# IPMI system event log (hardware faults)
esxcli hardware ipmi sel list | tail -20
```

---

## iDRAC RACADM Commands

Each VxRail node has a dedicated iDRAC IP on the OOB management network. SSH to it as `root` (factory default password `Calvin` — change immediately on new nodes).

```bash
# SSH to iDRAC
ssh root@<idrac-ip>
```

### System Information

```bash
# Full system info: model, serial, iDRAC version, BIOS version
racadm getsysinfo

# Get BIOS firmware version
racadm getversion -f bios

# Get iDRAC firmware version
racadm getversion -f idrac

# Get NIC firmware version
racadm getversion -f nic
```

### Event Log

```bash
# System event log (hardware faults, power events)
racadm getsel

# Last 20 events
racadm getsel | tail -20

# Clear the event log (after resolving hardware issues)
racadm clrsel
```

### NIC Statistics

```bash
# NIC interface statistics
racadm nicstatistics -n NIC.Integrated.1-1
racadm nicstatistics -n NIC.Integrated.1-2

# List all network interfaces
racadm getnic -c
```

### Storage Controller

```bash
# List storage controllers
racadm storagecontroller get

# List physical disks
racadm storage get pdisks

# List virtual disks (RAID)
racadm storage get vdisks
```

### Power Actions

```bash
# Power cycle a node (graceful — use with caution)
racadm serveraction gracereboot

# Hard power cycle (use only if node is unresponsive)
racadm serveraction powercycle

# Power off
racadm serveraction powerdown

# Power on
racadm serveraction powerup
```

---

## PowerCLI — vSAN Commands

Connect to vCenter before running any PowerCLI commands:

```powershell
# Connect to vCenter
Connect-VIServer -Server vcenter.example.local -Credential (Get-Credential)
```

### vSAN Health

```powershell
# Cluster health summary
Get-VsanClusterHealthSummary -Cluster "VxRail-Cluster" |
  Select-Object OverallHealth, OverallHealthDescription

# Detailed health groups
Get-VsanClusterHealthSummary -Cluster "VxRail-Cluster" |
  Select-Object -ExpandProperty Groups |
  Select-Object GroupName, GroupHealth |
  Sort-Object GroupName
```

### Storage Policies

```powershell
# List all vSAN storage policies
Get-SpbmStoragePolicy | Where-Object {$_.Name -like "vSAN*"} |
  Select-Object Name, Description

# Check policy compliance for all VMs
Get-VM | Get-SpbmEntityConfiguration |
  Select-Object Entity, StoragePolicy, ComplianceStatus |
  Where-Object {$_.ComplianceStatus -ne "compliant"}
```

### Capacity

```powershell
# vSAN datastore capacity and used percentage
Get-Datastore "vsanDatastore" | Select-Object Name,
    @{N="TotalGB"; E={[Math]::Round($_.CapacityGB)}},
    @{N="FreeGB"; E={[Math]::Round($_.FreeSpaceGB)}},
    @{N="UsedPct"; E={[Math]::Round((1 - $_.FreeSpaceGB/$_.CapacityGB)*100,1)}}
```

### Host Firmware and Version

```powershell
# ESXi version and build per host
Get-VMHost | Select-Object Name,
    @{N="Version"; E={$_.Version}},
    @{N="Build"; E={$_.Build}} |
  Sort-Object Name

# Export ESXi host configuration bundle
Get-VMHostFirmware -VMHost "vxrail-node-01.example.local" \
  -BackupConfiguration -DestinationPath C:\backups\vxrail\
```
