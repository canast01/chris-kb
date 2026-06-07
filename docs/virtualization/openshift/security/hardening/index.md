# OpenShift — Hardening

<div class="kb-summary">
OpenShift hardening: Security Context Constraints (SCC), Pod Security Admission, audit logging, network policies, and CIS benchmark controls for production clusters.
</div>

```text
┌──────────────────────────────────── OpenShift Hardening Controls ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   SCCs: OpenShift's admission controller for pod security (superset of K8s PSA)               │   │
│   │   PSA: Kubernetes Pod Security Admission (warn/audit/enforce); use restricted profile         │   │
│   │   NetworkPolicy: default deny + explicit allow; isolate namespaces by default                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       SCCs                  │  │    Pod Security Admission     │  │    Audit & Network          │ │
│   │      ─────────────          │  │      ─────────────           │  │      ─────────────          │  │
│   │  restricted-v2 (default)    │  │  Labels on namespace         │  │  Audit log via APIServer    │  │
│   │  anyuid: run as any UID     │  │  privileged/baseline/restrict│  │  Default network isolation  │  │
│   │  privileged: full access    │  │  enforce/warn/audit modes    │  │  Egress firewall (NP)       │  │
│   │  Grant per SA not user      │  │  OCP 4.12+: PSA enforced     │  │  No default deny in OCP    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SCC         = Security Context Constraint; OCP admission controller for pod security configuration │
│    PSA         = Pod Security Admission; Kubernetes built-in; enforces profiles at namespace level    │
│    restricted-v2= Least-privilege SCC; no root, read-only root FS, drop all capabilities              │
│    anyuid      = Allows pod to run as any UID; needed for legacy images; avoid where possible         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Security Context Constraints

```bash
# List SCCs (ordered from least to most permissive)
oc get scc | awk '{print $1, $2, $3}'

# Check which SCC a running pod used
oc get pod <pod> -o yaml | grep scc

# Which SCC will a pod use (dry run)?
oc adm policy scc-subject-review -f pod.yaml

# Grant SCC to service account (prefer this over granting to user)
oc adm policy add-scc-to-user anyuid -z myapp-sa -n my-project

# Remove SCC
oc adm policy remove-scc-from-user anyuid -z myapp-sa -n my-project

# List who uses a specific SCC
oc adm policy who-can use scc/anyuid
```

```yaml
# Pod spec that works with restricted-v2
spec:
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: app
    image: myapp:latest
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
      runAsNonRoot: true
```

## Pod Security Admission Labels

```bash
# Apply PSA labels to namespace
# Levels: privileged | baseline | restricted
# Modes: enforce (reject) | audit (log) | warn (user warning)

# Production: enforce restricted
oc label namespace my-project \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/enforce-version=latest \
  pod-security.kubernetes.io/warn=restricted \
  pod-security.kubernetes.io/warn-version=latest

# Legacy app namespace (needs anyuid): use baseline enforce
oc label namespace legacy-app \
  pod-security.kubernetes.io/enforce=baseline

# Check namespace PSA labels
oc get namespace my-project -o yaml | grep pod-security
```

## Audit Logging

```bash
# Enable API audit logging (default profile: metadata)
oc patch apiserver cluster --type merge \
  -p '{"spec":{"audit":{"profile":"WriteRequestBodies"}}}'

# Available profiles:
#   Default (metadata only): minimal logging
#   WriteRequestBodies: logs request bodies for write ops
#   AllRequestBodies: logs all request and response bodies
#   None: disable audit

# View audit logs on master node
oc debug node/<master> -- chroot /host
journalctl -u kube-apiserver | grep audit
# Or: /var/log/kube-apiserver/audit.log
```

## Network Policy (Default Deny)

```yaml
# Default deny all ingress in namespace
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: my-project
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
---
# Allow ingress from same namespace
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-same-namespace
  namespace: my-project
spec:
  podSelector: {}
  ingress:
  - from:
    - podSelector: {}
---
# Allow ingress from router (for Routes to work)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-router
  namespace: my-project
spec:
  podSelector: {}
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          network.openshift.io/policy-group: ingress
```

```bash
# Apply and verify
oc apply -f networkpolicies.yaml -n my-project
oc get networkpolicy -n my-project
```

## CIS Benchmark Checklist

| Control | Action |
|---|---|
| Disable kubeadmin | `oc delete secret kubeadmin -n kube-system` |
| Enable etcd encryption | `oc patch apiserver cluster --type merge -p '{"spec":{"encryption":{"type":"aesgcm"}}}'` |
| Enable audit logging | Set audit profile to WriteRequestBodies |
| Remove self-provisioner from all | `oc adm policy remove-cluster-role-from-group self-provisioner system:authenticated:oauth` |
| Restrict project creation | Remove self-provisioner from authenticated users |
| Default namespace deny | Apply NetworkPolicy deny-all per namespace |
| Use restricted SCC | Default for new workloads; avoid anyuid |
| Disable unused OAuth providers | Remove lab/test identity providers |
| Enable PSA restricted | Label production namespaces with restricted enforce |
