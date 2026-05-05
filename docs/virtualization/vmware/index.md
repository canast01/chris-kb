# VMware Platform

The VMware platform is the core virtualization layer used to run, manage, protect, and operate virtual machines across enterprise infrastructure. The main components usually include **vCenter**, **ESXi**, **vSAN**, **NSX**, and sometimes **VMware Cloud Foundation**.

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="vmware-cloud-foundation/">
  <strong>VMware Cloud Foundation</strong>
  <span>VCF architecture, workload domains, lifecycle, and operations.</span>
</a>

<a class="kb-card" href="vcenter/">
  <strong>vCenter</strong>
  <span>Inventory, permissions, alarms, tasks, certificates, backup, and field reference notes.</span>
</a>

<a class="kb-card" href="esxi/">
  <strong>ESXi</strong>
  <span>Host health, networking, storage paths, logs, maintenance, patching, and field reference notes.</span>
</a>

<a class="kb-card" href="vsan/">
  <strong>vSAN</strong>
  <span>Storage policies, disk groups, capacity, resync, health, performance, and field reference notes.</span>
</a>

<a class="kb-card" href="nsx/">
  <strong>NSX</strong>
  <span>Segments, gateways, firewalling, routing, edge nodes, and troubleshooting.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>VMware Operations</strong>
  <span>Day-to-day VMware procedures, checks, and troubleshooting workflows.</span>
</a>

</div>

## Key Components

| Component | Purpose |
|---|---|
| vCenter | Central management for ESXi hosts, clusters, VMs, permissions, templates, and lifecycle tasks |
| ESXi | Hypervisor installed on physical servers to run virtual machines |
| vSAN | Software-defined storage that uses local disks across ESXi hosts |
| NSX | Software-defined networking and security platform |
| VCF | Full-stack private cloud platform combining vSphere, vSAN, NSX, and lifecycle management |
| Lifecycle Manager | Used for patching, firmware alignment, image baselines, and upgrade compliance |

## What to Know

A healthy VMware platform depends on the relationship between compute, storage, networking, DNS, certificates, identity, and hardware health. Most VMware issues are not isolated to one layer — a VM problem may come from a datastore issue, a host issue, a network issue, or a permissions issue.

## Common Operational Areas

- Cluster health
- Host connection state
- Datastore capacity
- vSAN health
- VM performance
- Snapshot cleanup
- vCenter services
- Certificate expiration
- DNS and NTP
- Backup integration
- Access and role validation

## Common Checks

- Confirm all ESXi hosts are connected in vCenter
- Confirm no hosts are in a warning, disconnected, or not responding state
- Check datastore free space
- Check vSAN Skyline Health if vSAN is used
- Review active alarms
- Check recent tasks and events
- Validate backup job status
- Confirm DRS and HA status
- Review host hardware health
- Check NTP sync across vCenter and ESXi hosts

## Common Issues

| Issue | What to Check |
|---|---|
| Host disconnected | Management network, DNS, firewall, vpxa/hostd services |
| VM slow performance | CPU ready, memory ballooning, datastore latency, network drops |
| Datastore full | Snapshots, ISO files, old templates, orphaned VMDKs |
| Login failure | SSO, LDAP/AD connection, locked account, expired password |
| Certificate warning | vCenter certificate expiration, trusted roots, STS certificate |
| vMotion failure | VMkernel network, MTU, licensing, EVC, shared storage |
| HA warning | Management network, admission control, host isolation settings |
| vSAN warning | Disk groups, physical disks, network, object compliance |

## Useful Commands

```bash
# Restart ESXi management agents
/etc/init.d/hostd restart
/etc/init.d/vpxa restart

# Check ESXi services
services.sh status

# Restart all ESXi management agents
services.sh restart

# Check ESXi version
vmware -v

# Check host uptime
uptime

# Check NTP status
ntpq -p
```
