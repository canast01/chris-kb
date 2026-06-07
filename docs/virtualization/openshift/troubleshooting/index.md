# OpenShift — Troubleshooting

<div class="kb-summary">
OpenShift troubleshooting: pod failures, node issues, cluster operator problems, must-gather collection, and Red Hat support escalation.
</div>

```text
┌────────────────────────────────────── OpenShift Troubleshooting ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               OpenShift Troubleshooting Overview                              │   │
│   │       Three sub-sections: Common Issues, Diagnostics (must-gather), Escalation (Red Hat)      │   │
│   │       First step: oc get events -A and oc logs <pod> --previous; resolves 90% of issues       │   │
│   │         Escalation: always attach must-gather; Sev 1 = call Red Hat after opening case        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                 ▼                               ▼                                 ▼                   │
│                                                                                                       │
│   ┌────────────────────────────┐  ┌────────────────────────────┐  ┌───────────────────────────────┐   │
│   │       Common Issues        │  │        Diagnostics         │  │           Escalation          │   │
│   │       CrashLoopBackOff     │  │      must-gather bundle    │  │       Sev 1–4 definitions     │   │
│   │       ImagePullBackOff     │  │        oc adm inspect      │  │       SOS report per node     │   │
│   │        Node NotReady       │  │       etcd diagnostics     │  │       Case data checklist     │   │
│   │          OOMKilled         │  │        Network debug       │  │       TAM escalation path     │   │
│   │      Operator Degraded     │  │     Node crictl/kubelet    │  │        access.redhat.com      │   │
│   └────────────────────────────┘  └────────────────────────────┘  └───────────────────────────────┘   │
│                                                                                                       │
```
<div class="kb-grid">
  <a class="kb-card" href="common-issues/">
    <span class="kb-card-title">Common Issues</span>
    <span class="kb-card-desc">CrashLoopBackOff, ImagePullBackOff, node NotReady, pending pods, OOMKilled</span>
  </a>
  <a class="kb-card" href="diagnostics/">
    <span class="kb-card-title">Diagnostics</span>
    <span class="kb-card-desc">must-gather, oc adm inspect, log collection, and etcd diagnostics</span>
  </a>
  <a class="kb-card" href="escalation/">
    <span class="kb-card-title">Escalation</span>
    <span class="kb-card-desc">Red Hat support case process, SOS report, and severity levels</span>
  </a>
</div>
