# VxRail

VxRail is Dell's hyperconverged infrastructure platform built on VMware vSphere and vSAN. It combines Dell PowerEdge hardware, VMware software, lifecycle automation, firmware management, and support bundle collection through VxRail Manager.

<div class="kb-grid kb-grid-5">

  <div class="kb-card">
    <h3><a href="cluster-health/">Cluster Health</a></h3>
    <p>Cluster Health notes, checks, commands, troubleshooting, and validation.</p>
  </div>

  <div class="kb-card">
    <h3><a href="lifecycle/">Lifecycle</a></h3>
    <p>Lifecycle notes, checks, commands, troubleshooting, and validation.</p>
  </div>

  <div class="kb-card">
    <h3><a href="support-bundles/">Support Bundles</a></h3>
    <p>Support Bundles notes, checks, commands, troubleshooting, and validation.</p>
  </div>

  <div class="kb-card">
    <h3><a href="upgrade-readiness/">Upgrade Readiness</a></h3>
    <p>Upgrade Readiness notes, checks, commands, troubleshooting, and validation.</p>
  </div>

  <div class="kb-card">
    <h3><a href="validation/">Validation</a></h3>
    <p>Validation notes, checks, commands, troubleshooting, and validation.</p>
  </div>

</div>

## Key Components

| Component | Purpose |
|---|---|
| VxRail Manager | Manages VxRail cluster lifecycle, upgrades, validation, and support bundles |
| vCenter | Manages ESXi hosts, clusters, VMs, and VMware services |
| ESXi | Hypervisor running on VxRail nodes |
| vSAN | Storage layer used by VxRail clusters |
| iDRAC | Hardware management interface for each node |
| Dell SupportAssist | Used for Dell support connectivity and log collection |

## What to Know

VxRail upgrades are different from standard VMware upgrades because they include both VMware software and Dell firmware. The VxRail bundle keeps ESXi, vCenter compatibility, drivers, and firmware aligned.

## Common Operational Tasks

- Review VxRail Manager health
- Check cluster status before maintenance
- Generate support bundles
- Validate upgrade readiness
- Review hardware alerts
- Confirm iDRAC access
- Check vSAN health
- Confirm node firmware consistency
- Validate DNS, NTP, and certificate health

## Upgrade Process

1. Review release notes
2. Confirm supported target version
3. Check VxRail Manager health
4. Run pre-checks
5. Confirm backups are healthy
6. Confirm vCenter and VxRail Manager access
7. Validate DNS and NTP
8. Open or review Dell support guidance if required
9. Start upgrade from VxRail Manager
10. Monitor node-by-node upgrade progress
11. Validate cluster health after completion

## Support Bundle Collection

Support bundles are usually collected when Dell or VMware support needs logs for troubleshooting.

Typical bundle sources:

- VxRail Manager
- vCenter
- ESXi hosts
- vSAN logs
- iDRAC / hardware logs

## Common Issues

| Issue | What to Check |
|---|---|
| Upgrade pre-check failure | DNS, NTP, vSAN health, hardware alerts, version compatibility |
| Node hardware alert | iDRAC, Lifecycle Controller, PSU, memory, disk, NIC |
| VxRail Manager unreachable | VM status, IP, DNS, services, certificates |
| vSAN warning | Disk group health, physical disks, network, resync status |
| Support bundle failure | Disk space, permissions, VxRail Manager services |

## Useful Commands

```bash
# Check ESXi version
vmware -v

# Check host management agents
services.sh status

# Check vSAN resync status from ESXi
esxcli vsan debug resync summary get

# Check network interfaces
esxcli network nic list

# Check storage adapters
esxcli storage core adapter list
```
