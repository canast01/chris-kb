# Scenarios

<div class="kb-summary">
Cross-product VMware scenarios: reactive troubleshooting and planned operational workflows. Each scenario traces an issue or task across multiple products, showing how vCenter, ESXi, vSAN, NSX, Aria, and VxRail interact.
</div>

```text
┌──────────────────────────────────── VMware — Scenarios ───────────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────┐   ┌───────────────────────────────────────────────────┐│
│   │              ISSUES (Reactive)            │   │               TASKS (Planned)                    ││
│   │  Something broke — trace it across layers │   │  Operational workflow — execute across products  ││
│   │                                           │   │                                                   ││
│   │  · VM Performance Degraded                │   │  · Host Maintenance and Patching                 ││
│   │  · VM Inaccessible / HA Failover          │   │  · Capacity Planning                             ││
│   │  · vSAN Disk or Component Failure         │   │  · Provision a New Workload                      ││
│   │  · vMotion Failing                        │   │  · Certificate Expiry and Rotation               ││
│   │  · NSX Connectivity Broken                │   │  · DR Test / Planned Failover                    ││
│   │    ... + 13 more                          │   │    ... + 6 more                                  ││
│   └───────────────────────────────────────────┘   └───────────────────────────────────────────────────┘│
│                                                                                                       │
│                              ▼                                          ▼                             │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │   Products involved across all scenarios                                                         ││
│   │   vCenter · ESXi · vSAN · NSX · Aria Suite (Ops / Logs / Networks) · VxRail · SRM                ││
│   │   Each scenario shows which product you start in and where the chain leads                       ││
│   └───────────────────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Issues

<div class="kb-grid kb-grid-5">

<a class="kb-card" href="vm-performance-degraded/">
  <strong>VM Performance Degraded</strong>
  <span>ESXi esxtop → vSAN latency → NSX DFW → Aria Ops alert chain.</span>
</a>

<a class="kb-card" href="vm-inaccessible-ha-failover/">
  <strong>VM Inaccessible / HA Failover</strong>
  <span>APD/PDL response, HA restart, post-failover validation.</span>
</a>

<a class="kb-card" href="vsan-disk-component-failure/">
  <strong>vSAN Disk or Component Failure</strong>
  <span>Alarm to rebuild, risk window, hardware replacement.</span>
</a>

<a class="kb-card" href="vmotion-failing/">
  <strong>vMotion Failing</strong>
  <span>MTU, EVC mode, licensing, network config diagnosis.</span>
</a>

<a class="kb-card" href="nsx-connectivity-broken/">
  <strong>NSX Connectivity Broken</strong>
  <span>DFW rules, segment config, T0/T1 routing, Aria Networks path trace.</span>
</a>

<a class="kb-card" href="esxi-host-disconnected/">
  <strong>ESXi Host Disconnected</strong>
  <span>HA isolation, management network, DNS/NTP, reconnect procedure.</span>
</a>

<a class="kb-card" href="vcenter-down/">
  <strong>vCenter Down / Unreachable</strong>
  <span>VCSA services, VAMI, PSC, restore from backup.</span>
</a>

<a class="kb-card" href="ntp-drift-sso-certificate/">
  <strong>NTP Drift / SSO and Certificate Errors</strong>
  <span>NTP sync, certificate validity, SSO token expiry chain.</span>
</a>

<a class="kb-card" href="psod-esxi-kernel-panic/">
  <strong>PSOD — ESXi Kernel Panic</strong>
  <span>vmkernel.log, driver/firmware, iDRAC crash dump, GSS escalation.</span>
</a>

<a class="kb-card" href="vxrail-lcm-upgrade-failure/">
  <strong>VxRail LCM Upgrade Failure</strong>
  <span>Pre-check failures, bundle validation, rollback, Dell support.</span>
</a>

<a class="kb-card" href="aria-ops-alert-storm/">
  <strong>Aria Ops Alert Storm</strong>
  <span>Noise filter, alert correlation, Aria Logs, root-cause vs suppress.</span>
</a>

<a class="kb-card" href="nsx-edge-failure-bgp-down/">
  <strong>NSX Edge Failure / BGP Down</strong>
  <span>Edge HA, BGP peer state, T0 failover, upstream switch.</span>
</a>

<a class="kb-card" href="vsan-stretched-cluster-split-brain/">
  <strong>vSAN Stretched Cluster Split-Brain</strong>
  <span>Witness appliance, preferred site, forced recovery.</span>
</a>

<a class="kb-card" href="datastore-full-capacity-alarm/">
  <strong>Datastore Full / Capacity Alarm</strong>
  <span>vSAN inflation, snapshot cleanup, SPBM remediation.</span>
</a>

<a class="kb-card" href="srm-replication-lag-rpo-violation/">
  <strong>SRM Replication Lag / RPO Violation</strong>
  <span>vSR status, bandwidth, RPO breach, failover decision.</span>
</a>

<a class="kb-card" href="storage-apd-datastore-inaccessible/">
  <strong>Storage APD — Datastore Inaccessible</strong>
  <span>All paths down, APD vs PDL, VMCP timeout, fabric recovery, VM restart.</span>
</a>

<a class="kb-card" href="vm-snapshot-consolidation-required/">
  <strong>VM Snapshot Consolidation Required</strong>
  <span>Orphaned delta files, consolidation failure, vmkfstools repair, backup agent fix.</span>
</a>

<a class="kb-card" href="ha-admission-control-breach/">
  <strong>HA Admission Control Breach</strong>
  <span>Multi-host failure, capacity exhausted, restart triage, policy relaxation, N+1 sizing.</span>
</a>

</div>

### Tasks

<div class="kb-grid kb-grid-5">

<a class="kb-card" href="host-maintenance-patching/">
  <strong>Host Maintenance and Patching</strong>
  <span>vMotion evacuation, maintenance mode, LCM patch, return and validate.</span>
</a>

<a class="kb-card" href="capacity-planning/">
  <strong>Capacity Planning</strong>
  <span>vSAN space trending, cluster CPU/RAM headroom, when to add a node.</span>
</a>

<a class="kb-card" href="provision-new-workload/">
  <strong>Provision a New Workload</strong>
  <span>VM sizing, vSAN policy, NSX segment, Aria Ops tagging.</span>
</a>

<a class="kb-card" href="certificate-expiry-rotation/">
  <strong>Certificate Expiry and Rotation</strong>
  <span>Aria SuiteLC cert rotation, vCenter, ESXi thumbprint.</span>
</a>

<a class="kb-card" href="dr-test-planned-failover/">
  <strong>DR Test / Planned Failover</strong>
  <span>SRM/vSR test procedure, validation, failback.</span>
</a>

<a class="kb-card" href="add-esxi-host-to-cluster/">
  <strong>Add ESXi Host to Cluster</strong>
  <span>Hardware readiness, install, network/storage, vCenter join, LCM baseline.</span>
</a>

<a class="kb-card" href="expand-vxrail-cluster/">
  <strong>Expand VxRail Cluster</strong>
  <span>iDRAC readiness, VxRail Manager wizard, vSAN rebalance, validation.</span>
</a>

<a class="kb-card" href="storage-vmotion-datastore-migration/">
  <strong>Storage vMotion / Datastore Migration</strong>
  <span>svMotion, policy reapply, old datastore decom.</span>
</a>

<a class="kb-card" href="nsx-microsegmentation-rollout/">
  <strong>NSX Microsegmentation Rollout</strong>
  <span>Aria Networks flow analysis, DFW group design, monitor mode, enforce.</span>
</a>

<a class="kb-card" href="enable-vsan-encryption/">
  <strong>Enable vSAN Encryption</strong>
  <span>KMS/NKP setup, encryption policy, full data rebuild, key backup.</span>
</a>

<a class="kb-card" href="vcenter-upgrade-failure/">
  <strong>vCenter Upgrade Failure / Rollback</strong>
  <span>Stage 1 vs Stage 2, rollback snapshot, SuiteLC path, pre-upgrade checklist.</span>
</a>

</div>
