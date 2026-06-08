# Tanzu — Troubleshooting

<div class="kb-summary">
Diagnosing Tanzu cluster failures, pod scheduling issues, ingress errors, and control plane health problems.
</div>

```text
┌─────────────────────────────────── VMware Tanzu — Troubleshooting ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Cluster creation stuck: check Supervisor status in vCenter; validate NSX-T and storage config │   │
│   │  Nodes NotReady: check kubelet status on node; verify vSAN/network connectivity from node VM  │   │
│   │  Workload Management degraded: validate vCenter health, vSphere namespace quota, and NTP sync │   │
│   │   Image pull failures: check Harbor availability; verify imagePullSecret and network policy   │   │
│   │ kubectl logs and describe events are first diagnostic step; tanzu diagnostics collects bundles│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics use kubectl and events · escalation bundles for VMware GSS│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │        Cluster stuck        │  │       kubectl describe      │  │      tanzu diagnostics      │   │
│   │        Node NotReady        │  │         kubectl logs        │  │           GSS case          │   │
│   │         WCP degraded        │  │        kubectl events       │  │        Skyline Health       │   │
│   │       Image pull fail       │  │        vCenter events       │  │        TAM escalation       │   │
│   │         Pod pending         │  │          NSX-T logs         │  │          Log bundle         │   │
│   │        Quota exceeded       │  │        Harbor health        │  │        Version compat       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues triage cluster and node faults · diagnostics use kubectl and vCenter                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │  Cluster stuck   │  kubectl descr   │   vCenter tasks   │  tanzu diagnos   │   Re-provision   │   │
│   │  Node NotReady   │   kubectl logs   │  kubelet journal  │   GSS P1 case    │  Drain+replace   │   │
│   │   WCP degraded   │  kubectl events  │   NSX-T manager   │   TAM escalate   │   Restart WCP    │   │
│   │ Image pull fail  │  Harbor health   │    Harbor logs    │  Skyline health  │  Update secret   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ESXi hosts · RAM DIMMs · Network NICs · vSAN/NFS storage · NSX-T fabric · vCenter appliance          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Supervisor status  = Workload Management health shown in vCenter UI; Running/Degraded/Error states   │
│  Node NotReady      = Kubernetes node condition when kubelet cannot communicate with API server       │
│  kubelet            = Node agent managing pod lifecycle; check journalctl -u kubelet for errors       │
│  WCP                = Workload Control Plane; VMware internal name for the Supervisor Cluster         │
│  kubectl describe   = Shows detailed state and events for any Kubernetes resource                     │
│  kubectl events     = Lists recent events in a namespace; critical for cluster and pod triage         │
│  imagePullSecret    = Kubernetes secret holding registry credentials for pulling private images       │
│  tanzu diagnostics  = CLI command collecting cluster diagnostic bundle for GSS escalation             │
│  Pod Pending        = Pod scheduled but not running; check events for resource or image pull errors   │
│  Quota exceeded     = vSphere namespace CPU/memory/storage limit reached; expand or reclaim resources │
│  Skyline Health     = VMware proactive support tool validating Tanzu configuration against best       │
│  Cluster API events = Events on TanzuKubernetesCluster CR showing provisioning error details          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Frequently seen problems and resolution steps.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Log locations, diagnostic commands, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>When and how to escalate to VMware support.</span>
</a>

</div>
