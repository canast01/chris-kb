# Topics

Deep-dive reference articles on specific VMware behaviors, edge cases, and troubleshooting scenarios.

```
┌──────────────────── VMware Deep-Dive Topics: Navigation ───────────────────────┐
│                                                                                 │
│  What type of issue?                                                            │
│      │                                                                          │
│      ├── Cluster health / state    ──► Cluster State Validation                │
│      │                                 Cluster Failure Domains                  │
│      │                                                                          │
│      ├── VM placement / migration  ──► DRS and vMotion Behavior                │
│      │                                 HA Admission Control                     │
│      │                                                                          │
│      ├── Host failure / isolation  ──► Host Isolation Response                 │
│      │                                 Recovery Behavior                        │
│      │                                                                          │
│      ├── Pre-maintenance safety    ──► Maintenance Risk Validation             │
│      │                                 Upgrade Sequence Reference               │
│      │                                                                          │
│      ├── Performance / contention  ──► Resource Contention                     │
│      │                                 Storage Latency Troubleshooting          │
│      │                                                                          │
│      ├── Network issues            ──► Network Packet Loss                     │
│      │                                                                          │
│      └── Infrastructure basics    ──► Time and DNS Validation                  │
└────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-5">

<a class="kb-card" href="cluster-failure-domains/">
  <strong>Cluster Failure Domains</strong>
  <span>Failure domain behavior, rules, and impact on vSAN and HA.</span>
</a>

<a class="kb-card" href="cluster-state-validation/">
  <strong>Cluster State Validation</strong>
  <span>Validating cluster health, HA status, DRS balance, and readiness.</span>
</a>

<a class="kb-card" href="drs-vmotion-behavior/">
  <strong>DRS and vMotion Behavior</strong>
  <span>DRS automation levels, vMotion triggers, and placement logic.</span>
</a>

<a class="kb-card" href="ha-admission-control/">
  <strong>HA Admission Control</strong>
  <span>HA admission control policies, slot sizing, and failover capacity.</span>
</a>

<a class="kb-card" href="host-isolation-response/">
  <strong>Host Isolation Response</strong>
  <span>ESXi host isolation behavior, response settings, and impact.</span>
</a>

<a class="kb-card" href="maintenance-risk-validation/">
  <strong>Maintenance Risk Validation</strong>
  <span>Pre-maintenance risk checks for hosts, storage, and network impact.</span>
</a>

<a class="kb-card" href="network-packet-loss/">
  <strong>Network Packet Loss</strong>
  <span>Packet loss troubleshooting on VMkernel, vSwitch, and physical NICs.</span>
</a>

<a class="kb-card" href="recovery-behavior/">
  <strong>Recovery Behavior</strong>
  <span>HA restart behavior, APD/PDL response, and VM recovery options.</span>
</a>

<a class="kb-card" href="resource-contention/">
  <strong>Resource Contention</strong>
  <span>CPU ready, memory pressure, storage latency, and network saturation.</span>
</a>

<a class="kb-card" href="snapshot-impact/">
  <strong>Snapshot Impact</strong>
  <span>Performance and storage impact of snapshots, and cleanup procedures.</span>
</a>

<a class="kb-card" href="storage-latency-troubleshooting/">
  <strong>Storage Latency Troubleshooting</strong>
  <span>Identifying and resolving datastore and vSAN latency issues.</span>
</a>

<a class="kb-card" href="time-dns-validation/">
  <strong>Time and DNS Validation</strong>
  <span>NTP sync, DNS resolution, and time drift troubleshooting.</span>
</a>

<a class="kb-card" href="upgrade-sequence-reference/">
  <strong>Upgrade Sequence Reference</strong>
  <span>Component upgrade order for vCenter, ESXi, vSAN, NSX, and VCF.</span>
</a>

</div>
