# VMware Concepts

<div class="kb-summary">
Cross-product deep-dive references for VMware vSphere internals: vCenter HA topology, DRS scoring, HA admission control math, distributed switching, vSAN health state machines, certificate chains, NSX data-plane architecture, and vLCM image mechanics.
</div>

```text
┌─────────────────────────── VMware Concepts — Cross-Product Internals ─────────────────────────────────┐
│                                                                                                       │
│   vCenter HA          DRS Mechanics        HA Admission         vSphere Networking                    │
│   3-node: active/     Imbalance score,     Control Math         DVS layers, NIOC,                     │
│   passive/witness     migration bands,     Slot calc, restart   teaming, LACP, PVLAN                  │
│   DB replication,     predictive DRS,      priority, APD/PDL    CDP/LLDP, NSX-T                       │
│   ~4 min RTO          initial placement    net isolation resp   N-VDS migration                       │
│                                                                                                       │
│   vSAN Cluster        Certificate Chain    NSX Data Plane        vLCM Mechanics                       │
│   Health              VMCA hierarchy,      N-VDS, TEP,           Image vs baseline,                   │
│   Component states,   STS, custom CA,      Geneve (UDP 6081),    depot, rolling                       │
│   rebuild triggers,   renewal order,       DR fast path, DFW,    remediation, vendor                  │
│   resync throttle     VECS stores          Edge N-S traffic      add-ons, staging                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid">
  <a class="kb-card" href="vcha-internals/">
    <div class="kb-card-title">vCenter HA Internals</div>
    <div class="kb-card-body">3-node topology, DB replication, failover triggers, split-brain prevention, RTO tuning.</div>
  </a>
  <a class="kb-card" href="drs-mechanics/">
    <div class="kb-card-title">DRS Mechanics</div>
    <div class="kb-card-body">Imbalance scoring, migration priority bands, predictive DRS, initial placement, EVC edge cases.</div>
  </a>
  <a class="kb-card" href="ha-deep-dive/">
    <div class="kb-card-title">HA Deep Dive</div>
    <div class="kb-card-body">Slot calculation math, admission control policies, restart priority, APD vs PDL, isolation response.</div>
  </a>
  <a class="kb-card" href="vsphere-networking-internals/">
    <div class="kb-card-title">vSphere Networking</div>
    <div class="kb-card-body">DVS architecture, PVLAN, NIOC traffic pools, LBT/LACP teaming, VMkernel adapters, CDP/LLDP.</div>
  </a>
  <a class="kb-card" href="vsan-cluster-health/">
    <div class="kb-card-title">vSAN Cluster Health</div>
    <div class="kb-card-body">Component state machine, rebuild triggers, resync throttle, disk group failure domains, proactive rebalance.</div>
  </a>
  <a class="kb-card" href="certificate-chain/">
    <div class="kb-card-title">Certificate Chain</div>
    <div class="kb-card-body">VMCA hierarchy, STS signing cert, custom CA / hybrid mode, VECS stores, renewal order, STS recovery.</div>
  </a>
  <a class="kb-card" href="nsx-data-plane/">
    <div class="kb-card-title">NSX Data Plane</div>
    <div class="kb-card-body">N-VDS, TEP, Geneve encapsulation, BFD, Distributed Router fast path, DFW, Edge N-S topology.</div>
  </a>
  <a class="kb-card" href="vlcm-mechanics/">
    <div class="kb-card-title">vLCM Mechanics</div>
    <div class="kb-card-body">Image vs baseline, cluster image drift, depot types, rolling remediation, vendor add-ons, staging.</div>
  </a>
</div>
