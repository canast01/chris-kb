# VMware Internals

<div class="kb-summary">
Deep-dive articles on how core vSphere components work internally — cluster services, compute scheduling, networking, storage, security, lifecycle, and cross-product mechanisms. Use these pages to build the mental model before working on procedures or troubleshooting.
</div>

```text
┌─────────────────────────────────── VMware Internals — Reference Map ──────────────────────────────────┐
│                                                                                                       │
│   Internals pages explain how things work: scoring, state machines, math, limits, and edge cases.     │
│   Use them to build mental models before working on procedures or troubleshooting.                    │
│   Each page targets one vSphere sub-system with cross-references to related product pages.            │
│                                                                                                       │
│   Compute & Availability                                                                              │
│   Cluster Services: HA (restart VMs after host failure), DRS (load balance), FT (continuous)          │
│   DRS scoring: imbalance ratio, migration cost, predictive DRS, initial placement decisions           │
│   HA admission control: percentage, slot-based, dedicated failover hosts; vCLS agent VMs              │
│   Resource management: shares, reservations, limits, expandable reservations, resource pools          │
│   vCenter HA: 3-node active/passive/witness, DB replication, ~4 min RTO, split-brain guard            │
│                                                                                                       │
│   Networking                                                                                          │
│   vSphere networking: VSS vs VDS, NIOC traffic pools, LBT/LACP teaming, PVLAN, CDP/LLDP               │
│   NSX data plane: N-VDS, TEP, Geneve (UDP 6081), BFD, distributed router, DFW fast path               │
│   vSphere Networking Internals: DVS port groups, PVLAN isolated/community/promiscuous modes           │
│                                                                                                       │
│   Storage                                                                                             │
│   vSphere storage: VMFS, NFS, vVols, SPBM, VASA, VAAI offload, datastore cluster concepts             │
│   vSAN cluster health: component state machine, resync throttle, disk-group failure domains           │
│   Certificate chain: VMCA hierarchy, STS signing cert, custom CA, VECS stores, renewal order          │
│                                                                                                       │
│   Lifecycle, Security & Monitoring                                                                    │
│   vLCM: image vs baseline (mutually exclusive per cluster), depot, rolling remediation                │
│   vSphere lifecycle, monitoring, permissions, security — platform-level architecture                  │
│                                                                                                       │
│   Key terms: HA = High Availability  DRS = Distributed Resource Scheduler                             │
│   vLCM = Lifecycle Manager  SPBM = Storage Policy-Based Management  N-VDS = NSX vDS                   │
│   NIOC = Network I/O Control  TEP = Tunnel Endpoint  VCHA = vCenter High Availability                 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cluster-services/">
  <strong>Cluster Services</strong>
  <span>DRS, HA, FT, and vCLS — how vSphere cluster services interact and when each applies.</span>
</a>

<a class="kb-card" href="vsphere-lifecycle/">
  <strong>vSphere Lifecycle</strong>
  <span>vLCM, patch baselines, firmware management, and the ESXi host upgrade flow.</span>
</a>

<a class="kb-card" href="vsphere-monitoring/">
  <strong>vSphere Monitoring</strong>
  <span>Performance charts, alarms, events, and integration with Aria Operations.</span>
</a>

<a class="kb-card" href="vsphere-networking/">
  <strong>vSphere Networking</strong>
  <span>vSS vs vDS, portgroups, uplinks, MTU, and network I/O control concepts.</span>
</a>

<a class="kb-card" href="vsphere-permissions/">
  <strong>vSphere Permissions</strong>
  <span>RBAC model, roles, privileges, permission propagation, and SSO identity sources.</span>
</a>

<a class="kb-card" href="vsphere-resource-management/">
  <strong>Resource Management</strong>
  <span>CPU/memory reservations, limits, shares, resource pools, and admission control.</span>
</a>

<a class="kb-card" href="vsphere-security/">
  <strong>vSphere Security</strong>
  <span>ESXi lockdown mode, encrypted VMs, TLS policy, and certificate management concepts.</span>
</a>

<a class="kb-card" href="vsphere-storage/">
  <strong>vSphere Storage</strong>
  <span>VMFS, NFS, vVols, storage policies, SPBM, and datastore cluster concepts.</span>
</a>

<a class="kb-card" href="vcha-internals/">
  <strong>vCenter HA Internals</strong>
  <span>3-node topology, DB replication, failover triggers, split-brain prevention, RTO tuning.</span>
</a>

<a class="kb-card" href="drs-mechanics/">
  <strong>DRS Mechanics</strong>
  <span>Imbalance scoring, migration priority bands, predictive DRS, initial placement, EVC edge cases.</span>
</a>

<a class="kb-card" href="ha-deep-dive/">
  <strong>HA Deep Dive</strong>
  <span>Slot calculation math, admission control policies, restart priority, APD vs PDL, isolation response.</span>
</a>

<a class="kb-card" href="vsphere-networking-internals/">
  <strong>Networking Internals</strong>
  <span>DVS architecture, PVLAN, NIOC traffic pools, LBT/LACP teaming, VMkernel adapters, CDP/LLDP.</span>
</a>

<a class="kb-card" href="vsan-cluster-health/">
  <strong>vSAN Cluster Health</strong>
  <span>Component state machine, rebuild triggers, resync throttle, disk group failure domains, proactive rebalance.</span>
</a>

<a class="kb-card" href="certificate-chain/">
  <strong>Certificate Chain</strong>
  <span>VMCA hierarchy, STS signing cert, custom CA / hybrid mode, VECS stores, renewal order, STS recovery.</span>
</a>

<a class="kb-card" href="nsx-data-plane/">
  <strong>NSX Data Plane</strong>
  <span>N-VDS, TEP, Geneve encapsulation, BFD, Distributed Router fast path, DFW, Edge N-S topology.</span>
</a>

<a class="kb-card" href="vlcm-mechanics/">
  <strong>vLCM Mechanics</strong>
  <span>Image vs baseline, cluster image drift, depot types, rolling remediation, vendor add-ons, staging.</span>
</a>

</div>
