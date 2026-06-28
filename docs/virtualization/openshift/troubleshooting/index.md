---
tags:
  - troubleshooting
search:
  boost: 1.5
---
# OpenShift — Troubleshooting

<div class="kb-summary">
OpenShift troubleshooting: pod failures, node issues, cluster operator problems, must-gather collection, and Red Hat support escalation.

*Applies to: OpenShift 4.x*
</div>
![OpenShift — Troubleshooting](../../../assets/virtualization-openshift-troubleshooting-index.svg)


![OpenShift — Troubleshooting — Diagram](../../../assets/virtualization-openshift-troubleshooting-diagram.svg)

```mermaid
graph TD
    A([Start: Issue Reported]) --> B{Check CVO\noc get clusterversion}
    B -->|Upgrade stuck| C[Review CO conditions\noc get co]
    B -->|No upgrade issue| D{Check Operators\noc get co}
    D -->|Degraded CO found| E[Review operator pod logs\noc describe co and oc logs]
    D -->|All operators OK| F{Check Nodes\noc get nodes}
    F -->|NotReady node| G[kubelet / CRI-O / disk\noc debug node]
    F -->|All nodes Ready| H{Check Pods\noc get pods -A}
    H -->|CrashLoop / Pending| I[oc logs --previous\noc describe pod]
    H -->|All pods running| J{Check Networking\nDNS / connectivity}
    J -->|DNS failure| K[Check openshift-dns pods\nnslookup from debug pod]
    J -->|Network timeout| L[OVN-K status\nNetworkPolicy review]
    E --> M([Open support case\nwith must-gather])
    G --> M
    I --> M
    K --> M
    L --> M

    classDef dark fill:#1e3a5f,color:#fff
    classDef action fill:#78350f,color:#fff
    classDef escalate fill:#991b1b,color:#fff
    class A,B,D,F,H,J dark
    class C,E,G,I,K,L action
    class M escalate
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
subpage_index: "Sub-Page Index" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> subpage_index: investigate
subpage_index -> resolution
```

## Sub-Page Index

| Symptom | Go To |
|---|---|
| CrashLoopBackOff, ImagePullBackOff, Pending, OOMKilled, node NotReady, operator Degraded | [Common Issues](common-issues/) |
| Collecting must-gather, etcd diagnostics, network traces, node-level logs | [Diagnostics](diagnostics/) |
| Opening a Red Hat support case, SOS report, severity levels, escalation path | [Escalation](escalation/) |

<div class="kb-grid">
  <a class="kb-card" href="common-issues/">
    <span class="kb-card-title">Common Issues</span>
    <span class="kb-card-desc">CrashLoopBackOff, ImagePullBackOff, node NotReady, pending pods, OOMKilled, etcd latency, DNS failures</span>
  </a>
  <a class="kb-card" href="diagnostics/">
    <span class="kb-card-title">Diagnostics</span>
    <span class="kb-card-desc">must-gather, oc adm inspect, Prometheus queries, OVN flow trace, log collection, etcd diagnostics</span>
  </a>
  <a class="kb-card" href="escalation/">
    <span class="kb-card-title">Escalation</span>
    <span class="kb-card-desc">Red Hat support case process, SOS report, severity levels, KCS solutions, escalation path</span>
  </a>
</div>
