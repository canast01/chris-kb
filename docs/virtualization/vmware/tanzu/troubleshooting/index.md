# Tanzu — Troubleshooting

```
┌────────── Tanzu Troubleshooting Decision Tree ─────────────────────────────────┐
│                                                                                 │
│  Symptom                                                                        │
│      │                                                                          │
│      ├── Supervisor unavailable ──► check vCenter WM status ► control plane VMs│
│      │                                                                          │
│      ├── Cluster stuck creating  ──► kubectl describe Machine ► image/creds    │
│      │                                                                          │
│      ├── Node NotReady           ──► kubectl describe node ► Conditions        │
│      │                              kubelet logs on node                        │
│      │                                                                          │
│      ├── Pod Pending             ──► describe pod ► Events (resource/PVC/taint)│
│      │                                                                          │
│      ├── Pod CrashLoopBackOff    ──► kubectl logs --previous ► app errors      │
│      │                                                                          │
│      ├── Storage not provisioning──► CSI driver pods ► StorageClass ► vSAN    │
│      │                                                                          │
│      └── Auth failure            ──► Pinniped supervisor logs ► OIDC/LDAP     │
│                                       token expiry ► re-login                  │
└────────────────────────────────────────────────────────────────────────────────┘
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
