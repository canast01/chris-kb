---
tags:
  - tanzu
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# Tanzu — Escalation


<div class="kb-summary">
Escalation reference covering Before Opening a Support Case, Severity Definitions, Escalation Steps, VMware Support Portal, Component-Specific Support and 1 more sections.

*Applies to: Tanzu 3.x*
</div>
```text
┌────────────────────────────── Virtualization Vmware Tanzu — Escalation ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Vmware escalation: severity triage, vendor support contact, and required artifacts      │   │
│   │         L1: basic checks, restart services; L2: log analysis, config review, vendor SR        │   │
│   │        Severity: P1 production down → immediate SR + on-call page; P2/P3 business hours       │   │
│   │         Before escalating: collect support bundle, event timeline, and change history         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Detect issue → triage severity → collect artifacts → open SR → update                              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Severity     │     Criteria     │   Response time   │      Owner       │    Vendor SLA    │   │
│   │        P1        │ Production down  │     Immediate     │   On-call + L2   │    1 hr 24x7     │   │
│   │        P2        │  Major degraded  │       1 hour      │   L2 engineer    │   4 hr biz hrs   │   │
│   │        P3        │  Minor degraded  │      4 hours      │   L2 engineer    │   8 hr biz hrs   │   │
│   │        P4        │    No impact     │    Next biz day   │    L1 support    │    2 biz days    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Virtualization Vmware Tanzu infrastructure · management network · monitoring             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vmware             = Virtualization Vmware Tanzu platform overview and core concepts               │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

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

---

## See also

- [Tanzu — Diagnostics](diagnostics/)
- [Virtualization Vmware Tanzu — Common Issues](common-issues/)

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
