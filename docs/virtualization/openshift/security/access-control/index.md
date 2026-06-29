---
tags:
  - security
---
# OpenShift — Access Control

<div class="kb-summary">
Kubernetes RBAC in OpenShift: roles, cluster roles, role bindings, service accounts, SCCs, namespace isolation, project request templates, and API audit logging.

*Applies to: OpenShift 4.x*
</div>

```d2
direction: right

B: "B" {shape: rectangle}
C: "403 Forbidden" {shape: rectangle}
D: "D" {shape: rectangle}
E: "403 Forbidden" {shape: rectangle}
F: "F" {shape: rectangle}
G: "Admission Denied" {shape: rectangle}
H: "Persist / Execute" {shape: rectangle}
A: "API Request" {shape: rectangle}

B -> C
D -> E
F -> G
F -> H
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Built-in ClusterRoles

| ClusterRole | Scope | Typical Use Case |
|---|---|---|
| `cluster-admin` | Cluster | Break-glass admin; never use for day-to-day ops |
| `admin` | Namespace | Full namespace control; can grant up to admin rights |
| `edit` | Namespace | Developer access; create/update/delete workloads; no RBAC changes |
| `view` | Namespace | Read-only; for monitoring accounts or CI inspection |
| `cluster-reader` | Cluster | Read-only across all namespaces; for audit tooling |
| `self-provisioner` | Cluster | Allows users to create new projects; remove from `system:authenticated:oauth` in hardened environments |
| `system:node` | Cluster | Assigned to kubelets; grants node-specific API permissions |
| `system:image-puller` | Namespace | Allows service accounts in other namespaces to pull images from this namespace's registry |

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


```text title="Expected output"
clusterrole.rbac.authorization.k8s.io/admin added: "alice"
clusterrole.rbac.authorization.k8s.io/cluster-admin added: "alice"
clusterrole.rbac.authorization.k8s.io/edit added: "dev-team"
clusterrole.rbac.authorization.k8s.io/view added: "monitoring-team"
clusterrole.rbac.authorization.k8s.io/admin removed: "alice"
Verb	Non-Resource URLs	Resource Names	API Groups	Kinds
*	[]	[]	[]	[]
Users	Groups	Service Accounts
alice	dev-team	my-project/default
Verb	Non-Resource URLs	Resource Names	API Groups	Kinds
create	[]	[]	[]	[pods]
Users	Groups	Service Accounts
system:serviceaccount:kube-system:admin	system:masters	default/deployer
```

!!! warning "Common errors"
    **`Error from server (NotFound): users.user.openshift.io "alice" not found`** — Create the user first with `oc create user alice` or ensure the user exists in your identity provider.
    **`Error from server (Forbidden): clusterroles.rbac.authorization.k8s.io is forbidden: User "system:anonymous" cannot create resource`** — Ensure you are logged in with sufficient permissions using `oc login` with a cluster-admin account.
    **`Error from server (NotFound): rolebindings.rbac.authorization.k8s.io "admin" not found`** — Verify the role exists in the namespace with `oc get roles -n my-project` before attempting to remove it.
## Custom Role Creation

```bash
# Imperative: create role with specific verbs and resources
oc create role pod-reader \
  --verb=get,list,watch \
  --resource=pods,pods/log \
  -n my-project

# Bind to a user
oc create rolebinding read-pods \
  --role=pod-reader \
  --user=alice \
  -n my-project

# Bind to a group
oc create rolebinding read-pods-group \
  --role=pod-reader \
  --group=dev-team \
  -n my-project
```


```text title="Expected output"
role.rbac.authorization.k8s.io/pod-reader created
rolebinding.rbac.authorization.k8s.io/read-pods created
rolebinding.rbac.authorization.k8s.io/read-pods-group created
```

!!! warning "Common errors"
    **`error: unable to connect to the server: dial tcp: lookup api.openshift.local on 127.0.0.11:53: no such host`** — Verify the cluster is running and your kubeconfig points to the correct API endpoint with `oc cluster-info`.
    **`Error from server (AlreadyExists): roles.rbac.authorization.k8s.io "pod-reader" already exists`** — Delete the existing role with `oc delete role pod-reader -n my-project` before recreating it, or use `oc apply` with a YAML manifest instead.
    **`Error from server (NotFound): namespaces "my-project" not found`** — Create the namespace first with `oc create namespace my-project` or change `-n my-project` to an existing namespace.
## Security Context Constraints (SCC)

SCCs are an OpenShift-specific admission controller that enforces pod security configuration before a pod is created. Every pod must match at least one SCC granted to its service account.

| SCC | Allows Root | Privileged | Use Case |
|---|---|---|---|
| `restricted-v2` | No | No | Default for new workloads; drop all capabilities, read-only root FS |
| `restricted` | No | No | Legacy default (OCP < 4.11); prefer restricted-v2 |
| `nonroot` | No | No | Runs as any UID ≥ 1 but not 0 |
| `anyuid` | Yes | No | Legacy images that hardcode UID 0; avoid where possible |
| `privileged` | Yes | Yes | Node-level daemons (CNI, CSI drivers); never for application workloads |
| `hostnetwork` | No | No | Pods needing host network namespace (e.g. node exporters) |
| `hostmount-anyuid` | Yes | No | NFS client provisioners needing host mounts |

```bash
# List all SCCs (ordered from least to most permissive)
oc get scc

# Which SCC did a running pod receive?
oc get pod <pod> -n <ns> \
  -o jsonpath='{.metadata.annotations.openshift\.io/scc}'

# Which SCC would a pod YAML use (dry-run check)?
oc adm policy scc-subject-review -f pod.yaml

# Grant SCC to service account (always prefer -z over user)
oc adm policy add-scc-to-serviceaccount anyuid -z myapp-sa -n my-project

# Remove SCC from service account
oc adm policy remove-scc-from-user anyuid -z myapp-sa -n my-project

# List who has permission to use a specific SCC
oc adm policy who-can use scc/anyuid
```


```text title="Expected output"
NAME                                                    PRIORITY     READMISSIONCONTROLLER
anyuid                                                  10           false
hostaccess                                             9            false
hostmount-anyuid                                       8            false
hostnetwork                                            7            false
nonroot                                                4            false
restricted-v2                                          75           true
restricted                                             1            true

restricted

apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  serviceAccountName: myapp-sa
  allowHostDirVolumePlugin: false
  runAsUser:
    type: MustRunAsRange
  seLinuxContext:
    type: MustRunAs
  fsGroup:
    type: MustRunAsRange
  readOnlyRootFilesystem: false
  allowPrivilegedContainer: false
  capabilities:
    drop:
    - ALL

scc "anyuid" added to serviceaccount "myapp-sa" in namespace "my-project"

Error from server (NotFound): serviceaccounts "myapp-sa" not found
Removing SCC from user...
scc "anyuid" removed from user "system:serviceaccount:my-project:myapp-sa"

Verb                Resource                     Resource Name   API Group   Nonresource URL   *   Allow   Deny
*                   scc                          anyuid          security.openshift.io              true
use                 scc                          anyuid          security.openshift.io              true
```

!!! warning "Common errors"
    **`Error from server (NotFound): serviceaccounts "myapp-sa" not found`** — Verify the service account exists in the target namespace with `oc get sa -n my-project` before granting SCC permissions.
    **`error: the server doesn't have a resource type "scc"`** — Use the full resource path `scc/anyuid` or run `oc adm policy who-can use scc/anyuid` instead of `oc get scc/anyuid`.
    **`Error: pod.yaml: error validating the pod: spec.serviceAccountName: Invalid value: "": serviceAccountName is required`** — Ensure the pod YAML includes a valid `serviceAccountName` field under `spec` before running the scc-subject-review command.
## Service Accounts

```bash
# Create service account
oc create serviceaccount myapp-sa -n my-project

# Bind role to service account
oc adm policy add-role-to-user view -z myapp-sa -n my-project

# Grant SCC to service account (if pod needs elevated permissions)
oc adm policy add-scc-to-user anyuid -z myapp-sa -n my-project

# Create short-lived bound token (OCP 4.11+ preferred over legacy token secrets)
oc create token myapp-sa -n my-project --expiration=3600

# List service account tokens (shows legacy secret-based tokens)
oc get serviceaccount myapp-sa -n my-project -o yaml

# Reference in pod spec
# spec.serviceAccountName: myapp-sa
```


```text title="Expected output"
serviceaccount/myapp-sa created
clusterrole.rbac.authorization.k8s.io/view added: "myapp-sa"
securitycontextconstraints.security.openshift.io/anyuid added to: ["myapp-sa"]
eyJhbGciOiJSUzI1NiIsImtpZCI6IkR4M0ZfVEhBQkNERUZHSElKS0xNTk9QUVJTVFV2V1hZWlpBQkNERUYifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjIl0sImV4cCI6MTcwNDY3MTIwMCwiaWF0IjoxNzA0NjY3NjAwLCJpc3MiOiJodHRwczovL2t1YmVybmV0ZXMuZGVmYXVsdC5zdmMiLCJrdWJlcm5ldGVzLmlvIjp7Im5hbWVzcGFjZSI6Im15LXByb2plY3QiLCJzZXJ2aWNlYWNjb3VudCI6eyJuYW1lIjoibXlhcHAtc2EiLCJ1aWQiOiI4YzQyYTk5Ny1mZjU4LTQyZDItODc3Ny1hYmNkZWYwMTIzNDUifX0sIm5iZiI6MTcwNDY2NzYwMCwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Om15LXByb2plY3Q6bXlhcHAtc2EifQ.signature_data_here
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: my-project
secrets:
- name: myapp-sa-token-abc12
```

!!! warning "Common errors"
    **`Error from server (NotFound): serviceaccounts "myapp-sa" not found`** — Verify the namespace exists with `oc get ns my-project` and ensure you're connected to the correct cluster.
    **`error: the server doesn't have a resource type "token"`** — Update to OpenShift 4.11+ or use legacy token secrets with `oc create secret generic myapp-sa-token --from-literal=token=<value>`.
    **`Error: user "myapp-sa" cannot create tokens in namespace "my-project"`** — Ensure your user has `create` permissions on `serviceaccounts/token` resource with `oc auth can-i create serviceaccounts/token -n my-project`.
## Namespace Isolation with NetworkPolicy

```bash
# Label namespaces for network policy targeting
oc label namespace my-project network.openshift.io/policy-group=ingress

# Apply deny-all + allow-from-router pattern
oc apply -f - <<EOF
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
EOF
```


```text title="Expected output"
namespace/my-project labeled
networkpolicy.networking.k8s.io/deny-all created
networkpolicy.networking.k8s.io/allow-same-namespace created
networkpolicy.networking.k8s.io/allow-from-router created
```

!!! warning "Common errors"
    **`Error from server (NotFound): namespaces "my-project" not found`** — Create the namespace first with `oc create namespace my-project` or ensure you are logged into the correct cluster.
    **`error: unable to recognize "STDIN": no matches for kind "NetworkPolicy" in version "networking.k8s.io/v1"`** — Verify the cluster supports NetworkPolicy resources by running `oc api-resources | grep networkpolicies` and confirm your OpenShift version is 3.11+.
    **`The NetworkPolicy "deny-all" is invalid: spec.egress: Invalid value: []`** — Remove the `Egress` policyType or add explicit egress rules, as deny-all egress without allow rules will block all outbound traffic including DNS.
## Project Request Template

A project request template auto-applies NetworkPolicies, LimitRanges, and ResourceQuotas to every new project created in the cluster.

```yaml
# project-request.yaml — applied once, referenced in OAuth/cluster config
apiVersion: template.openshift.io/v1
kind: Template
metadata:
  name: project-request
  namespace: openshift-config
objects:
- apiVersion: project.openshift.io/v1
  kind: Project
  metadata:
    name: ${PROJECT_NAME}
    annotations:
      openshift.io/description: ${PROJECT_DESCRIPTION}
      openshift.io/requester: ${PROJECT_REQUESTING_USER}
- apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata:
    name: deny-all
    namespace: ${PROJECT_NAME}
  spec:
    podSelector: {}
    policyTypes: [Ingress, Egress]
- apiVersion: v1
  kind: LimitRange
  metadata:
    name: default-limits
    namespace: ${PROJECT_NAME}
  spec:
    limits:
    - type: Container
      default:
        cpu: 500m
        memory: 256Mi
      defaultRequest:
        cpu: 100m
        memory: 64Mi
- apiVersion: v1
  kind: ResourceQuota
  metadata:
    name: default-quota
    namespace: ${PROJECT_NAME}
  spec:
    hard:
      pods: "50"
      requests.cpu: "4"
      requests.memory: 8Gi
      limits.cpu: "8"
      limits.memory: 16Gi
parameters:
- name: PROJECT_NAME
- name: PROJECT_DISPLAYNAME
- name: PROJECT_DESCRIPTION
- name: PROJECT_ADMIN_USER
- name: PROJECT_REQUESTING_USER
```

```bash
# Create the template
oc create -f project-request.yaml -n openshift-config

# Configure cluster to use this template for new projects
oc patch project.config.openshift.io/cluster --type=merge \
  -p '{"spec":{"projectRequestTemplate":{"name":"project-request"}}}'
```


```text title="Expected output"
template.template.openshift.io/project-request created
project.config.openshift.io/cluster patched
```

!!! warning "Common errors"
    **`error: unable to recognize "project-request.yaml": no matches for kind "Template" in version "template.openshift.io/v1"`** — Ensure the YAML file contains `kind: Template` and `apiVersion: template.openshift.io/v1` at the top.
    **`Error from server (NotFound): project.config.openshift.io "cluster" not found`** — Verify the cluster configuration object exists by running `oc get project.config.openshift.io` first.
## Audit Logging

API server audit logs record every request with user identity, verb, resource, and response code.

```bash
# Set audit policy profile on APIServer CR
# Profiles: Default (metadata), WriteRequestBodies, AllRequestBodies, None
oc patch apiserver cluster --type=merge \
  -p '{"spec":{"audit":{"profile":"WriteRequestBodies"}}}'

# Verify config is applied
oc get apiserver cluster -o jsonpath='{.spec.audit}'

# View audit logs on master node (rotate daily)
oc debug node/<master-node>
chroot /host
ls /var/log/kube-apiserver/
tail -f /var/log/kube-apiserver/audit.log | python3 -m json.tool

# Filter for a specific user
grep '"user":{"username":"alice"' /var/log/kube-apiserver/audit.log | jq .

# Filter for secrets access
grep '"resource":"secrets"' /var/log/kube-apiserver/audit.log | \
  jq '{user: .user.username, verb: .verb, ns: .objectRef.namespace, name: .objectRef.name}'
```


```text title="Expected output"
apiserver.config.openshift.io/cluster patched
{"profile":"WriteRequestBodies"}
audit.log audit.log.2024-01-15.gz audit.log.2024-01-14.gz audit.log.2024-01-13.gz
{
  "level": "RequestResponse",
  "auditID": "a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6",
  "stage": "ResponseComplete",
  "requestObject": {...},
  "responseObject": {...},
  "user": {
    "username": "alice",
    "uid": "system:serviceaccount:openshift-monitoring:prometheus-k8s"
  },
  "verb": "get",
  "objectRef": {
    "resource": "secrets",
    "namespace": "default",
    "name": "db-credentials"
  }
}
{
  "user": "alice",
  "verb": "get",
  "ns": "default",
  "name": "db-credentials"
}
{
  "user": "alice",
  "verb": "create",
  "ns": "kube-system",
  "name": "etcd-backup-token"
}
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "apiserver"`** — Ensure you are connected to an OpenShift 4.x cluster with `oc login` and the APIServer CRD is available.
    **`chroot: cannot change root directory to /host: No such file or directory`** — Run `oc debug node/<master-node>` first and wait for the debug pod to fully initialize before executing chroot.
    **`jq: parse error: Invalid numeric literal at line 1, column 10`** — Pipe only valid JSON lines to jq by using `grep` to filter complete audit entries before processing.
| Audit Level | What Is Logged | Use Case |
|---|---|---|
| `None` | Nothing | Disable auditing (not recommended in production) |
| `Metadata` | Request metadata only (user, verb, resource) — no body | Low-overhead baseline |
| `Request` | Metadata + request body | Capture what was submitted |
| `RequestResponse` | Metadata + request + response bodies | Full audit; highest storage cost |

## Audit: Who Has Access

```bash
# List all RoleBindings in a namespace
oc get rolebindings -n my-project -o wide

# List ClusterRoleBindings for cluster-admin
oc get clusterrolebindings | grep cluster-admin

# Check a user's permissions
oc auth can-i --list --as=alice -n my-project
oc auth can-i delete pods --as=alice -n my-project

# Check service account permissions
oc auth can-i --list \
  --as=system:serviceaccount:my-project:myapp-sa \
  -n my-project

# List all users with cluster-admin
oc get clusterrolebindings -o json | \
  jq '.items[] | select(.roleRef.name=="cluster-admin") | .subjects[].name'

# Find all RoleBindings that reference a specific user across all namespaces
oc get rolebindings -A -o json | \
  jq '.items[] | select(.subjects[]?.name=="alice") | {ns: .metadata.namespace, role: .roleRef.name}'
```


```text title="Expected output"
NAME                    ROLE                       AGE     USERS   GROUPS   SERVICEACCOUNTS
system:deployers        system:deployer            45d     -       -        deployer
system:image-builders   system:image-builder       45d     -       -        builder
myapp-admin             myapp-admin-role           12d     -       -        myapp-sa
edit                    edit                       8d      alice   -        -

cluster-admin                                                 0s
system:cluster-admin-aggregated-rules                        2d
system:masters                                               45d

Resources                                   Non-Resource URLs   Resource Names   Verbs
pods                                        []                  []               [create delete get list watch]
deployments.apps                            []                  []               [get list watch]
services                                    []                  []               [get list]
                                            [/api]              []               [get]

yes
yes

Resources                                   Non-Resource URLs   Resource Names   Verbs
pods                                        []                  []               [create delete get list watch]
secrets                                     []                  []               [get list]
configmaps                                  []                  []               [get list]

system:masters
cluster-admin-user
admin-sa

{
  "ns": "my-project",
  "role": "edit"
}
{
  "ns": "kube-system",
  "role": "cluster-admin"
}
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "rolebindings"`** — Use the correct plural form `oc get rolebindings` or check that your OpenShift API server is running and accessible.
    **`error: User "alice" cannot get rolebindings in namespace "my-project"`** — Ensure your current user has sufficient permissions; try running as a cluster-admin or grant the necessary role to your user.
    **`command not found: jq`** — Install jq on your system using your package manager (e.g., `apt-get install jq` or `brew install jq`) before running JSON filtering commands.
## See also

- [OpenShift — Authentication](../authentication/)
- [OpenShift — Hardening](../hardening/)
