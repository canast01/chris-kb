# VMware Platform

The VMware platform is the core virtualization layer used to run, manage, protect, and operate virtual machines across enterprise infrastructure. The main components usually include **vCenter**, **ESXi**, **vSAN**, **NSX**, and sometimes **VMware Cloud Foundation**.

<div class="kb-grid kb-grid-11">

<a class="kb-card" href="vmware-cloud-foundation/"><strong>VMware Cloud Foundation</strong><span>Full-stack SDDC — SDDC Manager, workload domains, lifecycle, and operations.</span></a>
<a class="kb-card" href="vcenter/"><strong>vCenter</strong><span>Inventory, permissions, alarms, certificates, backup, and lifecycle.</span></a>
<a class="kb-card" href="esxi/"><strong>ESXi</strong><span>Host health, networking, storage paths, logs, maintenance, and patching.</span></a>
<a class="kb-card" href="vsan/"><strong>vSAN</strong><span>Storage policies, disk groups, capacity, resync, health, and performance.</span></a>
<a class="kb-card" href="nsx/"><strong>NSX</strong><span>Segments, gateways, distributed firewall, routing, and edge nodes.</span></a>
<a class="kb-card" href="aria-operations/"><strong>Aria Operations</strong><span>Performance monitoring, capacity management, and compliance across the vSphere platform.</span></a>
<a class="kb-card" href="aria-automation/"><strong>Aria Automation</strong><span>Infrastructure automation, service catalogue, and IaC pipeline integration.</span></a>
<a class="kb-card" href="aria-suite-lifecycle/"><strong>Aria Suite Lifecycle</strong><span>Deployment, patching, certificate management, and upgrade orchestration for all Aria products.</span></a>
<a class="kb-card" href="aria-operations-for-logs/"><strong>Aria Ops for Logs</strong><span>Log ingestion, querying, alerting, and integration for VMware infrastructure logs.</span></a>


<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Health check procedures and validation steps.</span>
</a>

<a class="kb-card" href="topics/">
  <strong>Topics</strong>
  <span>Topics notes, checks, commands, and references.</span>
</a>
</div>

## vSphere Cluster Topology

```
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                          vSphere Cluster                                    │
  │                                                                             │
  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
  │  │   ESXi-01    │  │   ESXi-02    │  │   ESXi-03    │  │   ESXi-04    │   │
  │  │  vmnic0/1    │  │  vmnic0/1    │  │  vmnic0/1    │  │  vmnic0/1    │   │
  │  │  vmnic2/3    │  │  vmnic2/3    │  │  vmnic2/3    │  │  vmnic2/3    │   │
  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
  │         │  VDS             │                 │                 │           │
  └─────────┼──────────────────┼─────────────────┼─────────────────┼───────────┘
            │                  │                 │                 │
  ┌─────────▼──────────────────▼─────────────────▼─────────────────▼───────────┐
  │                   vSphere Distributed Switch (VDS)                          │
  │   ┌───────────┐  ┌────────────┐  ┌─────────────┐  ┌──────────────────┐    │
  │   │  VM Net   │  │ vMotion    │  │  Storage    │  │  Management      │    │
  │   │  (dvPG)   │  │ VMkernel   │  │  VMkernel   │  │  VMkernel        │    │
  │   └───────────┘  └────────────┘  └─────────────┘  └──────────────────┘    │
  └───────────────────────────────────────────────────────────────────────────┘
            │ Management & API                          │ Storage
  ┌─────────▼──────────────────────────────┐  ┌────────▼──────────────────────┐
  │  vCenter Server                        │  │  Shared Storage               │
  │  ┌────────────┐  ┌────────────────┐   │  │  ┌────────────┐  ┌─────────┐  │
  │  │  vSphere   │  │  Lifecycle Mgr │   │  │  │ FlashArray │  │  vSAN   │  │
  │  │  Client    │  │  (patching)    │   │  │  │ (VMFS/vVol)│  │ (local) │  │
  │  └────────────┘  └────────────────┘   │  │  └────────────┘  └─────────┘  │
  │  ┌────────────┐  ┌────────────────┐   │  └───────────────────────────────┘
  │  │  DRS / HA  │  │  NSX Manager   │   │
  │  └────────────┘  └────────────────┘   │
  └────────────────────────────────────────┘
```

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
