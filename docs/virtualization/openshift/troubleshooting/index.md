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

![OpenShift — Troubleshooting — Diagram](../../../assets/virtualization-openshift-troubleshooting-diagram.svg)

```d2
direction: right

B: "B" {shape: rectangle}
C: "Review CO conditions\noc get co" {shape: rectangle}
D: "D" {shape: rectangle}
E: "Review operator pod logs\noc describe co and oc logs" {shape: rectangle}
F: "F" {shape: rectangle}
G: "kubelet / CRI-O / disk\noc debug node" {shape: rectangle}
H: "H" {shape: rectangle}
I: "oc logs --previous\noc describe pod" {shape: rectangle}
J: "J" {shape: rectangle}
K: "Check openshift-dns pods\nnslookup from debug pod" {shape: rectangle}
L: "OVN-K status\nNetworkPolicy review" {shape: rectangle}
M: "Open support case\nwith must-gather" {shape: rectangle}
A: "Start: Issue Reported" {shape: rectangle}

B -> C
D -> E
F -> G
H -> I
J -> K
J -> L
E -> M
G -> M
I -> M
K -> M
L -> M
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
