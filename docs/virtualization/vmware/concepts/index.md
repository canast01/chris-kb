# VMware Concepts

<div class="kb-summary">
Deep-dive reference articles on core vSphere concepts: cluster services, lifecycle management, monitoring, networking, permissions, resource management, security, and storage internals.
</div>

```text
┌─────────────────────────────────── VMware Concepts — Reference Map ───────────────────────────────────┐
│                                                                                                       │
│   Concepts pages explain internals: how features work, why limits exist, what terms mean              │
│   Use these pages to build the mental model before working on procedures or troubleshooting           │
│   Each page targets one vSphere sub-system with cross-references to related product pages             │
│                                                                                                       │
│   Compute & Availability                                                                              │
│   Cluster Services: HA (host failure restart), DRS (load balancing), FT (continuous availability)     │
│   HA admission control: percentage, slot-based, dedicated failover hosts; vCLS coordination VMs       │
│   Resource pools: shares, reservations, limits, expandable reservations                               │
│                                                                                                       │
│   Networking                                                                                          │
│   VSS vs VDS: distributed switch required for NIOC, LACP, Host Profiles, port mirroring               │
│   NIOC traffic types: vSAN, vMotion, management, VM traffic — bandwidth shares and limits             │
│   PVLAN modes: Isolated (no lateral traffic), Community (within-group only), Promiscuous (all)        │
│                                                                                                       │
│   Storage                                                                                             │
│   VMFS / NFS internals; VAAI offload operations; VASA array capability reporting                      │
│   SPBM: maps VM storage requirements to datastore capabilities via storage policies                   │
│   vVOLs: per-VM logical storage objects on the array; VASA 3.0 required                               │
│                                                                                                       │
│   Lifecycle, Security & Monitoring                                                                    │
│   vLCM: image-based vs baseline-based (mutually exclusive per cluster); Quick Boot                    │
│   Lockdown mode: Normal (DCUI only) vs Strict (no local access); VM encryption + vTA                  │
│   ESXTOP: %RDY (CPU contention), DAVG (storage latency), balloon/swap (memory pressure)               │
│                                                                                                       │
│   Key terms:                                                                                          │
│   HA     = High Availability; restarts VMs on a surviving host after host failure                     │
│   DRS    = Distributed Resource Scheduler; balances vCPU/RAM load across cluster hosts                │
│   vLCM  = vSphere Lifecycle Manager; cluster-image-based patching, replacing VUM baselines            │
│   SPBM  = Storage Policy-Based Management; maps VM requirements to datastore capabilities             │
│   vCLS  = vSphere Cluster Services; agent VMs that coordinate DRS and HA placement decisions          │
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

</div>
