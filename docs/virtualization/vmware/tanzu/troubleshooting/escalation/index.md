# Tanzu — Escalation

```
┌─────────────────── Tanzu Escalation Path ──────────────────────────────────────┐
│                                                                                 │
│  Issue identified                                                               │
│      │                                                                          │
│      ▼                                                                          │
│  Collect diagnostics before escalating                                          │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  tanzu diagnostics collect │ kubectl cluster-info dump                  │   │
│  │  vCenter logs │ NSX/AVI support bundle │ Harbor logs                    │   │
│  │  tanzu version │ kubectl version │ vSphere version                      │   │
│  └───────────────────────────────────────┬──────────────────────────────────┘  │
│                                          │                                      │
│  Severity triage                         ▼                                      │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  Sev 1: Supervisor down ──► create case + call support immediately       │  │
│  │  Sev 2: Cluster degraded / storage failing ──► case within 1 hour       │   │
│  │  Sev 3: Specific NS or Harbor failing ──► case next business day         │  │
│  └───────────────────────────────────────┬──────────────────────────────────┘  │
│                                          │                                      │
│  Open case                               ▼                                      │
│  support.broadcom.com ► Tanzu KG / vSphere with Tanzu                          │
│  Attach diagnostics ► component owner routes to correct team                   │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before Opening a Support Case

| Item | How to Collect |
|---|---|
| tanzu diagnostics bundle | `tanzu diagnostics collect --management-cluster` |
| kubectl cluster dump | `kubectl cluster-info dump --output-directory=/tmp/dump --all-namespaces` |
| vCenter logs | vCenter → Administration → Export System Logs |
| NSX-T logs (if networking involved) | NSX-T → System → Fabric → Support Bundle |
| AVI logs (if AVI is load balancer) | AVI Controller → Administration → Tech Support |
| Harbor logs | `docker-compose logs` or `kubectl logs -n harbor` |
| tanzu CLI version | `tanzu version` |
| vSphere version | vCenter → About |
| Kubernetes version | `kubectl version` |
| Symptom description | What was attempted, what failed, exact error messages, timestamps |

---

## Severity Definitions

| Severity | Condition |
|---|---|
| Sev 1 | Supervisor down — no cluster creation, all workloads inaccessible |
| Sev 2 | Workload cluster(s) degraded — pods not scheduling, storage not provisioning |
| Sev 3 | Individual application issue, Harbor down, specific namespace failing |
| Sev 4 | General how-to question, feature request |

For Sev 1: create case online AND call VMware Support.

---

## Escalation Steps

```bash
# Enable maximum verbosity before contacting support
TANZU_LOG_LEVEL=debug tanzu cluster get my-cluster 2>&1 > tanzu-verbose.log

# Collect full cluster dump
kubectl cluster-info dump --output-directory=/tmp/cluster-dump --all-namespaces
tar czf cluster-dump.tar.gz /tmp/cluster-dump/

# Collect vSphere events for the affected cluster VMs
# vCenter → Monitor → Events → filter by cluster VM names → export
```

---

## VMware Support Portal

1. **Portal:** support.broadcom.com → Log Case
   - Product: VMware Tanzu Kubernetes Grid (or vSphere with Tanzu)
   - Version: [TKG version]
   - Component: Management Cluster / Workload Cluster / Supervisor / Harbor
   - Attach: diagnostics bundle, cluster dump, symptom description

2. **For Sev 1:** after creating case, call support and reference case number

---

## Component-Specific Support

| Component | Owner |
|---|---|
| Supervisor / vSphere with Tanzu | VMware Support — vSphere team |
| TKG management/workload cluster | VMware Support — Tanzu team |
| Harbor Registry | VMware Support — Harbor team |
| NSX-T (load balancer) | VMware Support — NSX team |
| AVI (load balancer) | VMware Support — AVI team |
| Pinniped authentication | VMware Support — Tanzu team |

---

## Community Resources

- Tanzu Community Slack: #tanzu-platform, #tkg-users on vmware-code.slack.com
- Tanzu Documentation: docs.vmware.com/tanzu-kubernetes-grid
- Tanzu GitHub: github.com/vmware-tanzu
- Harbor Documentation: goharbor.io/docs
- Pinniped Documentation: pinniped.dev/docs
- Velero Documentation: velero.io/docs
