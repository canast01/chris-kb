# vSAN

Technical and operational KBs for vSAN.

## vSAN Cluster Topology

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                         vSAN Cluster (3-host minimum)                   │
  │                                                                          │
  │  ┌───────────────────────┐  ┌───────────────────────┐  ┌─────────────── │
  │  │       ESXi-01         │  │       ESXi-02         │  │  ESXi-03       │
  │  │  ┌─────┐  ┌────────┐  │  │  ┌─────┐  ┌────────┐  │  │  ┌─────┐  ┌── │
  │  │  │Cache│  │Capacity│  │  │  │Cache│  │Capacity│  │  │  │Cache│  │Ca │
  │  │  │NVMe │  │SSD/NL  │  │  │  │NVMe │  │SSD/NL  │  │  │  │NVMe │  │SS │
  │  │  └──┬──┘  └───┬────┘  │  │  └──┬──┘  └───┬────┘  │  │  └──┬──┘  └── │
  │  │     └────┬────┘       │  │     └────┬────┘       │  │     └────┬──── │
  │  │    Disk Group 1       │  │    Disk Group 1       │  │    Disk Group 1 │
  │  │  vmnic0  vmnic1       │  │  vmnic0  vmnic1       │  │  vmnic0  vmnic1 │
  │  └────┬────────┬─────────┘  └────┬────────┬─────────┘  └────┬────────┬─ │
  └───────┼────────┼─────────────────┼────────┼─────────────────┼────────┼──┘
          │        │                 │        │                 │        │
  ┌───────▼────────▼─────────────────▼────────▼─────────────────▼────────▼──┐
  │             vSAN VMkernel Network (dedicated 10/25 GbE VLAN)            │
  │              [object components distributed across all hosts]           │
  └──────────────────────────────────────────────────────────────────────────┘

  FTT=1 (RAID-1): object has 2 data replicas + 1 witness — survives 1 host loss
  FTT=1 (RAID-5): 4+ hosts required — more space-efficient than RAID-1
  FTT=2 (RAID-6): 6+ hosts required — survives 2 concurrent host failures
```

<div class="kb-grid kb-grid-15">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>esxcli vsan, disk groups, object health, resync, PowerCLI, and RVC commands.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Skyline health, cluster checks, object health, capacity, and policy compliance.</span>
</a>

<a class="kb-card" href="resync-rebuild/">
  <strong>Resync and Rebuild</strong>
  <span>Resync review, rebuild behavior, impact checks, and operational handling.</span>
</a>

<a class="kb-card" href="field-reference/">
  <strong>Field Reference</strong>
  <span>Architecture, dependencies, ports, daily checks, recovery notes, and RCA examples.</span>
</a>

<a class="kb-card" href="technical-deep-dive/">
  <strong>Technical Deep Dive</strong>
  <span>Components, logs, commands, failure points, resync, and upgrade notes.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>PowerCLI vSAN health check, disk group report, RVC diagnostics, and Ansible vSAN playbook.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Daily checks, health check, change readiness, incident triage, maintenance window, and post-change validation.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Resync review, object health, disk group failures, and vSAN recovery procedures.</span>
</a>


<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>Architecture overview, components, and design patterns.</span>
</a>

<a class="kb-card" href="disk-groups/">
  <strong>Disk Groups</strong>
  <span>Disk Groups notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="integration/">
  <strong>Integration</strong>
  <span>Integration with other systems and platforms.</span>
</a>

<a class="kb-card" href="lifecycle/">
  <strong>Lifecycle</strong>
  <span>Installation, upgrades, patching, and decommission.</span>
</a>

<a class="kb-card" href="performance/">
  <strong>Performance</strong>
  <span>Performance monitoring, tuning, and baselining.</span>
</a>

<a class="kb-card" href="standards/">
  <strong>Standards</strong>
  <span>Configuration standards, naming conventions, and baselines.</span>
</a>

<a class="kb-card" href="storage-policies/">
  <strong>Storage Policies</strong>
  <span>Storage Policies notes, checks, commands, and references.</span>
</a>
</div>
