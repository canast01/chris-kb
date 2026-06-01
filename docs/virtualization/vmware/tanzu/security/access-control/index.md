# Tanzu — Access Control


<div class="kb-summary">
Access Control reference covering Supervisor / vSphere Namespace RBAC, Kubernetes RBAC (Workload Clusters), Harbor RBAC, Network Policy (Namespace Isolation), Pod Security Admission and 1 more sections.
</div>
```
┌──────────────────────────── Virtualization Vmware Tanzu — Access Control ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Vmware access control: RBAC roles, least-privilege, and access audit logging         │   │
│   │        Roles: admin (full), operator (read/modify), read-only (view); map to AD groups        │   │
│   │       Authentication: local accounts, LDAP/AD integration, and MFA for privileged users       │   │
│   │          Audit: log all admin actions; review access logs monthly; rotate credentials         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify user → assign role → enforce MFA → audit → review quarterly                               │
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
│   │       Role       │   Permissions    │       Scope       │       Auth       │   Review cycle   │   │
│   │      Admin       │    Full CRUD     │       Global      │   MFA required   │     Monthly      │   │
│   │     Operator     │   Read/modify    │      Assigned     │   MFA required   │    Quarterly     │   │
│   │    Read-only     │    View only     │      Assigned     │     Password     │    Quarterly     │   │
│   │   Service acct   │     API only     │    Specific API   │    Token/cert    │      Annual      │   │
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

## Supervisor / vSphere Namespace RBAC

vSphere Namespaces have three access levels, assigned in vCenter:

| Permission | Capabilities |
|---|---|
| Owner | Full control — deploy/delete TKG clusters, manage all resources |
| Edit | Deploy workloads, create PVCs — cannot delete clusters |
| View | Read-only — inspect resources only |

```text
vCenter → Workload Management → Namespaces → [namespace] → Permissions → Add
  User/Group: CORP\team-alpha-owners → Owner
  User/Group: CORP\team-alpha-devs → Edit
```

---

## Kubernetes RBAC (Workload Clusters)

```yaml
# ClusterRole for ops team — full cluster access
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: ops-cluster-admin
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: Group
  name: cluster-ops  # OIDC group name from Pinniped
  apiGroup: rbac.authorization.k8s.io
```

```yaml
# RoleBinding for dev team — namespace-scoped edit
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: dev-edit
  namespace: production
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: edit
subjects:
- kind: Group
  name: team-alpha-devs
  apiGroup: rbac.authorization.k8s.io
```

```yaml
# Read-only ClusterRole for monitoring/audit teams
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: readonly-audit
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: view
subjects:
- kind: Group
  name: audit-team
  apiGroup: rbac.authorization.k8s.io
```

---

## Harbor RBAC

Harbor project roles:

| Role | Capabilities |
|---|---|
| Project Admin | Full project control — delete repos, manage members, edit config |
| Maintainer | Push/pull, manage tags, delete images |
| Developer | Push and pull images |
| Guest | Pull images only |
| Limited Guest | Pull images — no project visibility |

```bash
# Add LDAP group to Harbor project
curl -sk -X POST "https://harbor.example.local/api/v2.0/projects/team-alpha/members" \
  -u admin:<password> \
  -H "Content-Type: application/json" \
  -d '{
    "role_id": 2,
    "member_group": {
      "group_name": "team-alpha-devs",
      "group_type": 1
    }
  }'
# role_id: 1=Project Admin, 2=Developer, 3=Guest, 4=Maintainer
```

---

## Network Policy (Namespace Isolation)

Apply a default-deny policy to every namespace and explicitly allow required traffic:

```yaml
# Default deny all ingress and egress in a namespace
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

```yaml
# Allow ingress from ingress controller only
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-controller
  namespace: production
spec:
  podSelector: {}
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: projectcontour
```

---

## Pod Security Admission

Label namespaces to enforce Pod Security Standards:

```bash
# Enforce restricted mode (no privileged containers, no hostPath, etc.)
kubectl label namespace production \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/warn=restricted \
  pod-security.kubernetes.io/audit=restricted

# Baseline for less-strict namespaces
kubectl label namespace logging \
  pod-security.kubernetes.io/enforce=baseline
```

---

## OPA Gatekeeper Policies

```yaml
# Require resource limits on all containers
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: requiredresourcelimits
spec:
  crd:
    spec:
      names:
        kind: RequiredResourceLimits
  targets:
  - target: admission.k8s.gatekeeper.sh
    rego: |
      package requiredresourcelimits
      violation[{"msg": msg}] {
        container := input.review.object.spec.containers[_]
        not container.resources.limits
        msg := sprintf("Container '%v' must have resource limits", [container.name])
      }
---
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: RequiredResourceLimits
metadata:
  name: require-limits-all-namespaces
spec:
  match:
    kinds:
    - apiGroups: [""]
      kinds: ["Pod"]
```
