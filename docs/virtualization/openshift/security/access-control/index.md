# OpenShift — Access Control

<div class="kb-summary">
Kubernetes RBAC in OpenShift: roles, cluster roles, role bindings, service accounts, project isolation, and group-based access management.
</div>

```text
┌──────────────────────────────────────── OpenShift RBAC Model ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Role (namespace) + RoleBinding → namespace-scoped permissions                               │   │
│   │   ClusterRole + ClusterRoleBinding → cluster-wide permissions                                 │   │
│   │   ClusterRole + RoleBinding → cluster role applied to specific namespace                      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Built-in Roles         │  │      Service Accounts        │  │      Group Sync             │  │
│   │      ─────────────          │  │      ─────────────           │  │      ─────────────          │  │
│   │  cluster-admin: full access │  │  Per-namespace identity       │  │  oc adm groups sync         │ │
│   │  admin: namespace admin     │  │  Token auto-mounted in pod   │  │  LDAP groups → OCP groups   │  │
│   │  edit: create/edit objects  │  │  Bind to roles for API calls │  │  CronJob for periodic sync  │  │
│   │  view: read-only namespace  │  │  IRSA on AWS (OIDC)          │  │  group → ClusterRoleBinding │  │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Subject      = User, group, or service account being granted permissions                           │
│    Verb          = API action: get, list, create, update, patch, delete, watch                        │
│    Resource     = API object type: pods, services, deployments, secrets, etc.                         │
│    Aggregated role= ClusterRole that auto-aggregates rules from labelled ClusterRoles                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Built-in Roles

| Role | Scope | Permissions |
|---|---|---|
| `cluster-admin` | Cluster | Full access to all resources |
| `admin` | Namespace | Full access within namespace; can grant up to admin |
| `edit` | Namespace | Create/update/delete most resources; no RBAC changes |
| `view` | Namespace | Read-only access |
| `cluster-reader` | Cluster | Read-only access to all resources |
| `self-provisioner` | Cluster | Can create new projects |

## Role Bindings

```bash
# Grant namespace-level admin to a user
oc adm policy add-role-to-user admin alice -n my-project

# Grant cluster-admin to a user
oc adm policy add-cluster-role-to-user cluster-admin alice

# Grant role to a group
oc adm policy add-role-to-group edit dev-team -n my-project

# Grant cluster role to a group
oc adm policy add-cluster-role-to-group view monitoring-team

# Remove role
oc adm policy remove-role-from-user admin alice -n my-project

# Who can perform an action?
oc adm policy who-can get secrets -n my-project
oc adm policy who-can create pods --all-namespaces
```

## Custom Roles

```yaml
# Namespace-scoped role example
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: my-project
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-reader-binding
  namespace: my-project
subjects:
- kind: User
  name: bob
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

## Service Accounts

```bash
# Create service account
oc create serviceaccount myapp-sa -n my-project

# Bind role to service account
oc adm policy add-role-to-user view -z myapp-sa -n my-project

# Grant SCC to service account (if pod needs elevated permissions)
oc adm policy add-scc-to-user anyuid -z myapp-sa -n my-project

# List service account tokens
oc get serviceaccount myapp-sa -o yaml

# Reference in pod spec
# spec.serviceAccountName: myapp-sa
```

## Audit: Who Has Access

```bash
# List all RoleBindings in a namespace
oc get rolebindings -n my-project -o wide

# List ClusterRoleBindings for cluster-admin
oc get clusterrolebindings | grep cluster-admin

# Check a user's permissions
oc auth can-i --list --as=alice -n my-project
oc auth can-i delete pods --as=alice -n my-project

# List all users with cluster-admin
oc get clusterrolebindings -o json | \
  jq '.items[] | select(.roleRef.name=="cluster-admin") | .subjects[].name'
```
