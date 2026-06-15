---
tags:
  - troubleshooting
  - openshift
  - kubernetes
  - known-issues
---
# Red Hat OpenShift — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known OpenShift bugs, error codes, and workarounds covering cluster operators, OVN-Kubernetes networking, image registry, and upgrade issues.

*Applies to: OpenShift Container Platform 4.12–4.16*
</div>

```text
┌────────────────────────────── Virtualization Openshift Troubleshooting ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                  Openshift: Virtualization Openshift Troubleshooting platform                 │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │            Management: Virtualization Openshift Troubleshooting management console            │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
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
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Virtualization Openshift Troubleshooting infrastructure · management network · monitori  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Openshift          = Virtualization Openshift Troubleshooting platform overview and core concepts  │
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


## Before you begin

- Check all cluster operator status: `oc get co` — any `Degraded=True` blocks upgrades.
- `oc adm must-gather` collects all diagnostic data for Red Hat support.
- Cluster upgrade fails are almost always due to a degraded operator or certificate issue.

## Cluster Operators

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `authentication` operator degraded after certificate rotation | OCP 4.12+ | OAuth server certificate not trusted after rotation | Re-approve CSRs: `oc get csr | grep Pending | oc certificate approve` | N/A |
| `kube-apiserver` operator degraded: `revision stuck` | OCP 4.12+ | API server rollout blocked by unhealthy etcd pod | Check etcd pod health: `oc get pods -n openshift-etcd`; restart failed etcd pod | N/A |
| `machine-config` operator degraded after node change | OCP 4.x | MachineConfig pool not rendered cleanly | Check MCO: `oc describe mcp worker`; look for config render errors | N/A |

## Networking (OVN-Kubernetes)

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Pod-to-pod traffic fails across nodes | OCP 4.12+ | OVN-Kubernetes Geneve (UDP 6081) blocked between nodes | Verify UDP 6081 open on all node NICs and any intermediate firewalls | N/A |
| Service ClusterIP unreachable from pods | OCP 4.x | OVN flow tables out of sync | Restart `ovnkube-node` DaemonSet on affected node: `oc delete pod -n openshift-ovn-kubernetes -l app=ovnkube-node --field-selector=spec.nodeName=<node>` | N/A |

## Image Registry and Builds

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `image-registry` operator degraded — storage not available | OCP 4.x | No persistent storage configured for internal registry | Configure PVC or S3 storage for registry: `oc patch configs.imageregistry.operator.openshift.io/cluster --patch '{"spec":{"storage":{"pvc":{"claim":""}}}}' --type=merge` | N/A |
| Build fails: `ImagePullBackOff` from internal registry | OCP 4.x | Registry service cert not trusted by node | Approve pending node CSRs; verify cluster CA trust bundle | N/A |

## Upgrades

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Upgrade stuck at 10% — `machine-config` not applied | OCP 4.x | Worker node reboot loop during MCO config application | Check node: `oc debug node/<node>`; inspect `/var/log/messages` for boot failure | N/A |
| `oc adm upgrade` blocked: `Upgradeable=False` | OCP 4.x | Cluster operator reporting blocker condition | `oc get co`; investigate the Degraded operator; resolve before proceeding | N/A |

## See also

- [OpenShift — Common Issues](common-issues.md)
- [Kubernetes — Networking Reference](../../networking/protocols/)
