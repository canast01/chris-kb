---
tags:
  - operations
---
# OpenShift — CLI Reference

<div class="kb-summary">
oc command reference: resource management, log collection, exec, adm commands, debugging, and context management. oc extends kubectl with OpenShift-specific resources and shortcuts.

*Applies to: OpenShift 4.x*
</div>

```d2
direction: right

OC: "oc" {shape: rectangle}
RES: "Resource Ops · get / apply / patch · delete / label / annotate" {shape: rectangle}
ADM: "Admin Ops · adm drain / cordon · adm policy / inspect" {shape: rectangle}
DBG: "Debug Ops · debug node/ · rsh / exec · must-gather" {shape: rectangle}
IMG: "Image Ops · image mirror · tag / import-image · registry login" {shape: rectangle}

OC -> RES
OC -> ADM
OC -> DBG
OC -> IMG
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Authentication & Context

```bash
# Login
oc login https://api.ocp.example.com:6443 -u admin -p password
oc login --token=<token> --server=https://api.ocp.example.com:6443

# Who am I / current context
oc whoami
oc whoami --show-token
oc config current-context

# Switch project (namespace)
oc project openshift-monitoring
oc new-project my-app
oc projects          # list all accessible projects
```


```text title="Expected output"
Login successful.

You have access to the following projects and can switch between them with 'oc project <projectname>':

  * default
  * kube-system
  * openshift-monitoring
  * openshift-ingress
  * my-app

Using project "admin" on server "https://api.ocp.example.com:6443".

admin
sha256~ABC123DEF456GHI789JKL012MNO345PQR678STU901VWX234YZ567ABC890
admin

Now using project "openshift-monitoring" on server "https://api.ocp.example.com:6443".

Now using project "my-app" on server "https://api.ocp.example.com:6443".

openshift-monitoring
default
kube-system
openshift-ingress
my-app
```

!!! warning "Common errors"
    **`error: invalid credentials provided`** — Verify the username, password, and API server URL are correct, then retry the login command.
    **`error: the server has asked for the client to provide credentials`** — Ensure your token is valid and not expired; generate a new token from the OpenShift web console if needed.
    **`error: You don't have permission to switch to project "my-app"`** — Confirm the project exists and your user account has access; contact your cluster administrator if access is required.
## Resource Management

```bash
# Get resources
oc get nodes -o wide
oc get pods -n openshift-etcd
oc get pods --all-namespaces | grep -v "Running\|Completed"
oc get co            # cluster operators
oc get csr           # certificate signing requests

# Get all resources in a namespace
oc get all -n my-app

# Describe and inspect
oc describe node <node-name>
oc describe pod <pod> -n <ns>
oc get events -n <ns> --sort-by='.lastTimestamp'

# Apply / delete
oc apply -f manifest.yaml
oc delete pod <pod> -n <ns>
oc delete pod <pod> -n <ns> --grace-period=0 --force
```


```text title="Expected output"
NAME                                         STATUS   ROLES                  AGE   VERSION        INTERNAL-IP      EXTERNAL-IP   OS-IMAGE
master-0.ocp.example.com                     Ready    control-plane,master   45d   v1.27.8+4fab27b 192.168.1.10     <none>        Red Hat Enterprise Linux CoreOS 4.13.13
master-1.ocp.example.com                     Ready    control-plane,master   45d   v1.27.8+4fab27b 192.168.1.11     <none>        Red Hat Enterprise Linux CoreOS 4.13.13
worker-0.ocp.example.com                     Ready    worker                 44d   v1.27.8+4fab27b 192.168.1.20     <none>        Red Hat Enterprise Linux CoreOS 4.13.13
worker-1.ocp.example.com                     Ready    worker                 44d   v1.27.8+4fab27b 192.168.1.21     <none>        Red Hat Enterprise Linux CoreOS 4.13.13

NAMESPACE            NAME                                             READY   STATUS    RESTARTS   AGE
openshift-etcd       etcd-master-0.ocp.example.com                    1/1     Running   2          45d
openshift-etcd       etcd-master-1.ocp.example.com                    1/1     Running   1          45d
openshift-etcd       etcd-master-2.ocp.example.com                    1/1     Running   3          45d
openshift-etcd       etcd-peering-master-0.ocp.example.com            1/1     Running   0          45d

NAMESPACE                  NAME                                                    READY   STATUS             RESTARTS   AGE
openshift-apiserver       apiserver-7d4f8c2b9                                     0/1     CrashLoopBackOff   12         2h
openshift-monitoring      prometheus-operator-6f7b8d9c5                           0/1     ImagePullBackOff   0          1h

NAME                                                                 STATUS      ROLES
authentication                                                       Available   
apiserver                                                            Degraded    
etcd                                                                 Available   
ingress                                                              Available   

NAME                                                                 AGE       SIGNERNAME                                    REQUESTOR                                     CONDITION
csr-7k9m2                                                            3d        kubernetes.io/kube-apiserver-client-kubelet   system:serviceaccount:openshift-machine-config-operator:default   Approved,Issued
csr-9x2lp                                                            2d        kubernetes.io/kube-apiserver-client            system:admin                                   Pending

NAME                 READY   STATUS    RESTARTS   AGE
my-app-deploy-abc1   1/1     Running   0          5d
my-app-svc-xyz2      1/1     Running   1          4d

Name:               master-0.ocp.example.com
Roles:              control-plane,master
Status:             Ready
Allocatable:        cpu: 3500m, memory: 6Gi, ephemeral-storage: 50Gi
Conditions:         Ready True, MemoryP
```
## Resource Watching

```bash
# Watch pod state changes in real time
oc get pods -n <ns> -w

# Watch events sorted by time (most useful for troubleshooting)
oc get events -n <ns> --sort-by=.lastTimestamp
oc get events --all-namespaces --sort-by=.lastTimestamp | tail -40

# Watch nodes during a drain or upgrade
oc get nodes -w

# Watch cluster operators settling after an upgrade
oc get co -w
```


```text title="Expected output"
NAME                                    READY   STATUS    RESTARTS   AGE
nginx-deployment-66b6c48dd5-4k8vx       1/1     Running   0          2m
nginx-deployment-66b6c48dd5-7j2p9       1/1     Running   0          1m
redis-cache-0                           1/1     Running   0          5m
postgres-db-5d4f8c9b2-lmqrs             0/1     Pending   0          3s
postgres-db-5d4f8c9b2-lmqrs             0/1     ContainerCreating   0          5s
postgres-db-5d4f8c9b2-lmqrs             1/1     Running             0          12s

LAST SEEN   TYPE      REASON              OBJECT                                MESSAGE
2m15s       Normal    Scheduled           pod/nginx-deployment-66b6c48dd5-4k8vx   Successfully assigned default/nginx-deployment-66b6c48dd5-4k8vx to worker-02.ocp.local
2m10s       Normal    Pulling             pod/nginx-deployment-66b6c48dd5-4k8vx   Pulling image "nginx:1.21"
2m8s        Normal    Pulled              pod/nginx-deployment-66b6c48dd5-4k8vx   Successfully pulled image "nginx:1.21" in 2.5s
2m5s        Normal    Created             pod/nginx-deployment-66b6c48dd5-4k8vx   Created container nginx
2m4s        Normal    Started             pod/nginx-deployment-66b6c48dd5-4k8vx   Started container nginx
45s         Warning   FailedScheduling    pod/postgres-db-5d4f8c9b2-lmqrs        0/3 nodes available: insufficient memory

NAME                STATUS   ROLES           AGE    VERSION
master-01.ocp.local   Ready    control-plane   45d    v1.27.3
master-02.ocp.local   Ready    control-plane   45d    v1.27.3
worker-01.ocp.local   Ready    worker          42d    v1.27.3
worker-02.ocp.local   NotReady SchedulingDisabled 2m    v1.27.3

NAME                       VERSION   AVAILABLE   PROGRESSING   DEGRADED   SINCE
authentication             4.13.5    True        False         False      3d
cloud-credential           4.13.5    True        False         False      3d
cluster-autoscaler         4.13.5    True        False         False      3d
console                    4.13.5    False       True          False      8m
dns                        4.13.5    True        False         False      3d
...
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "co"`** — Use the full name `oc get clusteroperators` or ensure you're on OpenShift 4.x where the `co` shorthand is available.
    **`error: You must be logged in to the server (Unauthorized)`** — Authenticate with `oc login <cluster-url>` or verify your kubeconfig is set correctly.
    **`error: namespace "<ns>" not found
## Patching Resources

```bash
# Strategic merge patch (simple key overwrite)
oc patch deployment/myapp -p '{"spec":{"replicas":3}}'
oc patch node <node> -p '{"spec":{"unschedulable":true}}'

# JSON patch (precise path operations)
oc patch deployment/myapp --type=json \
  -p '[{"op":"replace","path":"/spec/replicas","value":3}]'

# Add a toleration via JSON patch
oc patch deployment/myapp --type=json \
  -p '[{"op":"add","path":"/spec/template/spec/tolerations","value":[{"key":"node-role.kubernetes.io/infra","effect":"NoSchedule"}]}]'

# Remove a field
oc patch deployment/myapp --type=json \
  -p '[{"op":"remove","path":"/spec/template/spec/affinity"}]'
```


```text title="Expected output"
deployment.apps/myapp patched
node/worker-node-01 patched
deployment.apps/myapp patched
deployment.apps/myapp patched
deployment.apps/myapp patched
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "deployment"`** — Verify the resource exists with `oc get deployment` and check you're in the correct namespace with `oc project`.
    **`error: failed to apply strategic merge patch to body`** — Ensure your JSON syntax is valid (matching quotes and brackets) and the field path exists in the resource spec.
    **`error: jsonpatch: test failed`** — Use `oc get deployment/myapp -o yaml` to verify the exact current path structure before applying a JSON patch operation.
## Output Formats

```bash
# JSON / YAML for full spec
oc get pod <pod> -n <ns> -o json
oc get pod <pod> -n <ns> -o yaml

# jsonpath — extract a single field
oc get pod <pod> -n <ns> -o jsonpath='{.status.phase}'
oc get node <node> -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'

# custom-columns — tabular output
oc get pods -n <ns> \
  -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName

# Get all pod images across namespaces
oc get pods --all-namespaces \
  -o custom-columns=NS:.metadata.namespace,NAME:.metadata.name,IMAGE:.spec.containers[0].image

# Output names only (for piping)
oc get pods -n <ns> -o name
oc get csr -o name | xargs oc adm certificate approve
```


```text title="Expected output"
{
  "apiVersion": "v1",
  "kind": "Pod",
  "metadata": {
    "name": "nginx-deployment-66b6c48dd5-k9x2m",
    "namespace": "default",
    "uid": "a7f3e2c1-9b4d-4e8f-b2d6-1c5a9e7f3d2b"
  },
  "status": {
    "phase": "Running",
    "conditions": [
      {"type": "Ready", "status": "True"}
    ]
  }
}
Running
True
NAME                                    STATUS    NODE
nginx-deployment-66b6c48dd5-k9x2m       Running   worker-node-01
nginx-deployment-66b6c48dd5-p7q2l       Running   worker-node-02
NAMESPACE     NAME                              IMAGE
default       nginx-deployment-66b6c48dd5-k9x2m nginx:1.21.6
kube-system   coredns-558bd4d5db-2xvkm          registry.k8s.io/coredns:v1.8.6
openshift-dns dns-default-8f7xq                 registry.redhat.com/openshift4/ose-dns:v4.12.5
pod/nginx-deployment-66b6c48dd5-k9x2m
pod/nginx-deployment-66b6c48dd5-p7q2l
certificatesigningrequest.certificates.k8s.io/node-csr-abc123def456
certificatesigningrequest.certificates.k8s.io/node-csr-xyz789uvw012
certificatesigningrequest.certificates.k8s.io/node-csr-abc123def456 approved
certificatesigningrequest.certificates.k8s.io/node-csr-xyz789uvw012 approved
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "pod" or "pods"`** — Verify the API group and resource name are correct; use `oc api-resources` to list available resources.
    **`Error from server (NotFound): pods "<pod>" not found`** — Confirm the pod name and namespace are correct with `oc get pods -n <ns>`.
    **`error: jsonpath expression is invalid`** — Check bracket syntax and field paths match the actual object structure using `oc get pod <pod> -o yaml` to verify field names.
## Labels & Selectors

```bash
# Filter by label selector
oc get pods -l app=myapp -n <ns>
oc get pods -l app=myapp,tier=frontend -n <ns>
oc get pods -l 'app in (frontend,backend)' -n <ns>

# Label a node
oc label node <node> node-role.kubernetes.io/infra=
oc label node <node> zone=east --overwrite

# Remove a label
oc label node <node> zone-

# Annotate a pod
oc annotate pod <pod> -n <ns> key=value
oc annotate pod <pod> -n <ns> key-       # remove annotation
```


```text title="Expected output"
NAME                                    READY   STATUS    RESTARTS   AGE
myapp-deployment-5d4c7b9f8-2kx9n       1/1     Running   0          3d
myapp-deployment-5d4c7b9f8-7qm2p       1/1     Running   0          2d
myapp-deployment-5d4c7b9f8-9lw3x       1/1     Running   0          1d

NAME                                    READY   STATUS    RESTARTS   AGE
myapp-frontend-8c9d2e1f4-4pq6r         1/1     Running   0          5h
myapp-frontend-8c9d2e1f4-8vx2s         1/1     Running   0          4h

NAME                                    READY   STATUS    RESTARTS   AGE
backend-service-6f3a1b2c9-jk8wl        1/1     Running   0          2d
frontend-app-4e7d9c5a2-m3n7p           1/1     Running   0          1d

node/worker-01.prod.local labeled
node/worker-02.prod.local labeled
node/worker-03.prod.local labeled
pod/myapp-5d4c7b9f8-2kx9n annotated
pod/myapp-5d4c7b9f8-7qm2p annotated
```

!!! warning "Common errors"
    **`error: node "<node>" not found`** — Verify the node name with `oc get nodes` and ensure you're connected to the correct cluster.
    **`error: label must have a value`** — Add a value after the equals sign (e.g., `node-role.kubernetes.io/infra=true`) or use `--overwrite` flag if updating an existing label.
    **`Error from server (NotFound): pods "<pod>" not found`** — Confirm the pod name and namespace with `oc get pods -n <ns>`, and ensure the pod exists before annotating.
## Logs

```bash
# Pod logs
oc logs <pod> -n <ns>
oc logs <pod> -n <ns> -c <container>    # specific container
oc logs <pod> -n <ns> --previous        # previous container instance
oc logs <pod> -n <ns> --follow          # stream (alias: -f)
oc logs <pod> -n <ns> --tail=100        # last 100 lines
oc logs <pod> -n <ns> --since=1h        # last hour only

# Stream logs from a deployment (any pod matching)
oc logs -f deploy/<name> -n <ns>

# Node logs (systemd journal via oc adm)
oc adm node-logs <node> -u crio         # CRI-O container runtime
oc adm node-logs <node> -u kubelet      # kubelet service
oc adm node-logs <node> -u NetworkManager
oc adm node-logs <node> --path=/var/log/messages
oc adm node-logs <node> --path=/var/log/audit/audit.log
```


```text title="Expected output"
2024-01-15T10:23:47.123456Z stdout F [INFO] Application started successfully
2024-01-15T10:23:48.456789Z stdout F [INFO] Listening on port 8080
2024-01-15T10:23:49.789012Z stdout F [DEBUG] Database connection pool initialized
2024-01-15T10:23:50.012345Z stdout F [INFO] Ready to accept requests
2024-01-15T10:23:51.345678Z stderr F [WARN] Deprecated API endpoint used

-- Logs begin at Mon 2024-01-15 09:45:22 UTC, end at Mon 2024-01-15 10:35:18 UTC --
Jan 15 10:15:33 worker-node-02 crio[2847]: time="2024-01-15T10:15:33.456789Z" level=info msg="Container started" id=abc123def456
Jan 15 10:15:34 worker-node-02 crio[2847]: time="2024-01-15T10:15:34.789012Z" level=info msg="Image pulled" image="quay.io/openshift/origin-node:v4.13.2"
Jan 15 10:15:35 worker-node-02 kubelet[1234]: I0115 10:15:35.123456 1234 kubelet.go:1234] Node status updated
Jan 15 10:15:36 worker-node-02 NetworkManager[567]: <info> [1705318536.1234] device (eth0): state change: activated -> unavailable
```

!!! warning "Common errors"
    **`Error from server (NotFound): pods "<pod>" not found`** — Verify the pod name with `oc get pods -n <ns>` and ensure you're querying the correct namespace.
    **`error: the server doesn't have a resource type "adm"`** — Use `oc adm node-logs` only on OpenShift 4.3+; for earlier versions use `oc debug node/<node>` instead.
    **`error: you must be logged in to the server`** — Authenticate with `oc login <cluster-url>` before running log commands.
## Exec and Remote Shell

```bash
# Execute a one-off command in a pod
oc exec <pod> -n <ns> -- ls /var/log
oc exec <pod> -n <ns> -c <container> -- cat /etc/config.yaml

# Interactive shell (exec with TTY)
oc exec -it <pod> -n <ns> -- bash
oc exec -it <pod> -n <ns> -- sh        # if bash not available

# Remote shell shorthand (oc-specific)
oc rsh <pod>
oc rsh -n <ns> <pod>

# Debug node (spawns privileged pod on host network/PID/IPC)
oc debug node/<node-name>
# Inside the debug pod:
chroot /host                          # access node filesystem as root
systemctl status kubelet
crictl ps                             # list running containers
crictl logs <container-id>
journalctl -u crio --since "10 min ago"

# Debug a deployment using its image (runs as root by default in debug)
oc debug deployment/<name> -n <ns> --as-root
# Override the command
oc debug deployment/<name> -n <ns> -- /bin/sh -c "env | grep SECRET"
```


```text title="Expected output"
bin
dev
etc
lost+found
proc
sys
var
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  config.yaml: |
    server:
      port: 8080
      timeout: 30s
bash-4.4# exit
Starting debug pod on node worker-02.example.com ...
Creating debug namespace ... 
Pod IP: 10.128.45.67
If you don't see a command prompt, try pressing enter.
sh-4.4# chroot /host
sh-4.4# systemctl status kubelet
● kubelet.service - Kubernetes Kubelet
   Loaded: loaded (/etc/systemd/system/kubelet.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2h 47min ago
sh-4.4# crictl ps | head -8
CONTAINER ID        IMAGE                                    CREATED             STATE               NAME                      ATTEMPT             POD ID
a7f2e9c1d4b5       quay.io/openshift/crio:v4.13.2          2 hours ago         Running             crio                      0                   8f3a2c1e9d7b
b2c3d4e5f6a7       registry.redhat.io/ose-pod:v4.13        45 minutes ago      Running             POD                       0                   9g4b3d2f0e8c
c3d4e5f6a7b8       docker.io/library/nginx:1.24            12 minutes ago      Running             nginx-app                 1                   0h5c4e3g1f9d
...
sh-4.4# exit
Debugging deployment/web-server ...
Starting debug pod with image registry.redhat.io/ose-cli:v4.13 ...
Pod IP: 10.128.67.89
sh-4.4# SECRET_API_KEY=sk-1a2b3c4d5e6f7g8h
sh-4.4# exit
```

!!! warning "Common errors"
    **`error: pod <pod> not found`** — Verify the pod name with `oc get pods -n <ns>` and ensure you're targeting the correct namespace.
    **`error: container <container> not found`** — List available containers in the pod with `oc get pod <pod> -n <ns> -o jsonpath='{.spec.containers[*].name}'` and use the correct container name.
    **`error: unable to upgrade connection: container not running or does not exist`** — Ensure the pod is in Running state with `oc get pod <pod> -n <ns>` and retry after the pod fully starts.
## Administrative Commands

```bash
# Node management
oc adm cordon <node>                  # mark unschedulable
oc adm uncordon <node>
oc adm drain <node> \
  --ignore-daemonsets \
  --delete-emptydir-data \
  --grace-period=60 \
  --timeout=300s

# Certificate management
oc get csr | grep Pending
oc adm certificate approve <csr-name>
oc get csr -o name | xargs oc adm certificate approve  # approve all pending

# RBAC
oc adm policy add-role-to-user admin <username> -n <project>
oc adm policy add-cluster-role-to-user cluster-admin <username>
oc adm policy remove-cluster-role-from-user cluster-admin <username>
oc adm policy who-can get pods -n <ns>

# Resource usage
oc adm top nodes
oc adm top pods --all-namespaces
oc adm top pods -n <ns> --containers   # per-container breakdown
```


```text title="Expected output"
NAME                          READY   STATUS   ROLES    AGE     VERSION
worker-node-01.prod.local    True    Ready    worker   45d     v1.27.8+4fab27b
worker-node-02.prod.local    True    Ready    worker   45d     v1.27.8+4fab27b
master-node-01.prod.local    True    Ready    master   120d    v1.27.8+4fab27b

NAME                                                   AGE   SIGNERNAME                                    REQUESTOR                                        CONDITION
csr-5k9m2                                              2m    kubernetes.io/kube-apiserver-client-kubelet   system:serviceaccount:openshift-machine-config-operator:default   Pending
csr-7x3pq                                              1m    kubernetes.io/kube-apiserver-client-kubelet   system:serviceaccount:openshift-machine-config-operator:default   Pending

certificatesigningrequest.certificates.k8s.io/csr-5k9m2 approved
certificatesigningrequest.certificates.k8s.io/csr-7x3pq approved

NAME                          CPU(cores)   MEMORY(bytes)
worker-node-01.prod.local    850m         12.4Gi
worker-node-02.prod.local    620m         8.7Gi
master-node-01.prod.local    1200m        16.2Gi

POD                                    NAMESPACE              CPU(cores)   MEMORY(bytes)
etcd-master-node-01.prod.local        openshift-etcd         180m         892Mi
kube-apiserver-master-node-01         openshift-kube-apiserver   320m    1.2Gi
...

NAME                          CPU(cores)   MEMORY(bytes)
nginx-deployment-5d4f7c9b8   default      45m          128Mi
nginx-deployment-5d4f7c9b8   default      42m          125Mi
```

!!! warning "Common errors"
    **`Error from server (NotFound): certificatesigningrequest.certificates.k8s.io "<csr-name>" not found`** — Verify the CSR name with `oc get csr` and ensure it exists before approval.
    **`Error: user "<username>" cannot be found in the cluster`** — Confirm the username exists in your identity provider (LDAP/OAuth) and has logged in at least once.
    **`error: timed out waiting for the condition on nodes/<node>`** — Increase the `--timeout` value or manually evict pods with `oc delete pod <pod> -n <ns>` before draining.
## oc adm inspect

`oc adm inspect` dumps all resources associated with an operator or namespace into a local directory. More targeted than must-gather for a single component.

```bash
# Dump all resources for the etcd operator
oc adm inspect clusteroperator/etcd --dest-dir=/tmp/etcd-inspect

# Dump a namespace (all objects, logs, events)
oc adm inspect namespace/openshift-monitoring --dest-dir=/tmp/mon-inspect

# Dump a specific deployment
oc adm inspect deployment/prometheus-operator -n openshift-monitoring --dest-dir=/tmp/prom-inspect

# The output directory contains:
#   cluster-scoped-resources/  — CRDs, nodes, cluster operators
#   namespaces/<ns>/           — pods, configmaps, secrets (redacted), events, logs
```


```text title="Expected output"
Inspecting clusteroperator/etcd...
Wrote cluster-scoped-resources/apiextensions.k8s.io/customresourcedefinitions.yaml
Wrote cluster-scoped-resources/config.openshift.io/clusteroperators/etcd.yaml
Wrote namespaces/openshift-etcd/pods/etcd-ip-10-0-45-12.ec2.internal/etcd/logs/current.log
Wrote namespaces/openshift-etcd/events.yaml
Wrote namespaces/openshift-etcd/configmaps.yaml
Inspection complete. Resources saved to /tmp/etcd-inspect

Inspecting namespace/openshift-monitoring...
Wrote namespaces/openshift-monitoring/pods/prometheus-operator-7d4f8c9b2-kx9m4/prometheus-operator/logs/current.log
Wrote namespaces/openshift-monitoring/pods/alertmanager-main-0/alertmanager/logs/current.log
Wrote namespaces/openshift-monitoring/configmaps.yaml
Wrote namespaces/openshift-monitoring/secrets.yaml (redacted)
Wrote namespaces/openshift-monitoring/events.yaml
Inspection complete. Resources saved to /tmp/mon-inspect

Inspecting deployment/prometheus-operator in namespace openshift-monitoring...
Wrote namespaces/openshift-monitoring/deployments/prometheus-operator.yaml
Wrote namespaces/openshift-monitoring/pods/prometheus-operator-7d4f8c9b2-kx9m4/logs/current.log
Inspection complete. Resources saved to /tmp/prom-inspect
```

!!! warning "Common errors"
    **`Error: clusteroperator/etcd not found`** — Verify the cluster operator exists with `oc get clusteroperators` and check the exact name.
    **`Error: unable to create directory /tmp/etcd-inspect: permission denied`** — Ensure the destination directory is writable or use a different path like `/var/tmp` with appropriate permissions.
    **`Error: namespace openshift-monitoring not found`** — Confirm the namespace exists with `oc get namespaces` and verify it is not in a terminating state.
## must-gather

```bash
# Collect full cluster state (takes 5-10 minutes)
oc adm must-gather                    # default collection
oc adm must-gather --image=<custom>   # product-specific (ODF, ACM, Logging)
oc adm must-gather --dest-dir=/tmp/mg

# ODF-specific must-gather
oc adm must-gather --image=registry.redhat.io/odf4/odf-must-gather-rhel9:latest

# Networking must-gather
oc adm must-gather --image=registry.redhat.io/openshift4/network-tools-rhel8

# Quick cluster state snapshot
oc adm top nodes
oc adm top pods --all-namespaces
```


```text title="Expected output"
$ oc adm must-gather
gathering data...
Gathering data for cluster...
Compressing must-gather output...
must-gather data collected successfully. Your data is located in ./must-gather.local.5891748503421891234/

$ oc adm must-gather --dest-dir=/tmp/mg
gathering data...
Gathering data for cluster...
Compressing must-gather output...
must-gather data collected successfully. Your data is located in /tmp/mg/must-gather.local.6234891234567891234/

$ oc adm top nodes
NAME                                       CPU(cores)   CPU%   MEMORY(Mi)   MEMORY%
worker-0.ocp.example.com                   892m         22%    7234Mi       45%
worker-1.ocp.example.com                   1156m        29%    8912Mi       56%
master-0.ocp.example.com                   645m         16%    6123Mi       38%
master-1.ocp.example.com                   723m         18%    6891Mi       43%
master-2.ocp.example.com                   698m         17%    6456Mi       40%

$ oc adm top pods --all-namespaces
NAMESPACE                  NAME                                       CPU(m)   MEMORY(Mi)
openshift-apiserver       apiserver-5d8f4c9b2-xk9lm                  234      512
openshift-controller-mgr  controller-manager-7c2b1f8d-qp3nk           156      384
openshift-etcd            etcd-master-0                               423      1024
openshift-kube-apiserver  kube-apiserver-master-1                    312      768
kube-system               coredns-6d4cf4b4c8-2jk8n                   45       128
...
```

!!! warning "Common errors"
    **`error: unable to connect to the server: dial tcp: lookup api.ocp.example.com on 8.8.8.8:53: no such host`** — Verify cluster API endpoint is resolvable and accessible; check your kubeconfig with `oc config view`.
    **`Error: image pull backoff for registry.redhat.io/odf4/odf-must-gather-rhel9:latest`** — Ensure the node has pull credentials for registry.redhat.io configured in the cluster's pull-secret.
    **`error: metrics not available yet`** — Wait 2-3 minutes after cluster startup for metrics-server to initialize, then retry the `oc adm top` command.
## Useful Aliases

```bash
alias k=kubectl
alias oc-all='oc get pods --all-namespaces | grep -v "Running\|Completed"'
alias oc-co='oc get co | grep -E "False|True.*True|True.*False.*True"'
alias oc-events='oc get events --all-namespaces --sort-by=.lastTimestamp | tail -30'
alias oc-notready='oc get nodes --no-headers | grep -v " Ready"'
alias oc-csr='oc get csr | grep Pending'
```


```text title="Expected output"
$ alias k=kubectl
$ alias oc-all='oc get pods --all-namespaces | grep -v "Running\|Completed"'
$ alias oc-co='oc get co | grep -E "False|True.*True|True.*False.*True"'
$ alias oc-events='oc get events --all-namespaces --sort-by=.lastTimestamp | tail -30'
$ alias oc-notready='oc get nodes --no-headers | grep -v " Ready"'
$ alias oc-csr='oc get csr | grep Pending'
$ k get nodes
NAME                           STATUS   ROLES           AGE     VERSION
master-01.ocp.local           Ready    control-plane   45d     v1.27.6+f67aeb3
master-02.ocp.local           Ready    control-plane   45d     v1.27.6+f67aeb3
worker-01.ocp.local           Ready    worker          42d     v1.27.6+f67aeb3
worker-02.ocp.local           Ready    worker          42d     v1.27.6+f67aeb3
$ oc-notready
worker-03.ocp.local           NotReady,SchedulingDisabled   worker   8d      v1.27.6+f67aeb3
$ oc-csr
NAME        AGE     SIGNERNAME                                    REQUESTOR                 REQUESTEDDURATION   CONDITION
csr-4m9kx   2m      kubernetes.io/kube-apiserver-client-kubelet   system:serviceaccount:openshift-machine-config-operator:default   <none>              Pending
csr-7p2lq   1m      kubernetes.io/kube-apiserver-client-kubelet   system:serviceaccount:openshift-machine-config-operator:default   <none>              Pending
```

!!! warning "Common errors"
    **`command not found: oc`** — Ensure the OpenShift CLI is installed and in your PATH with `which oc` or install via `curl -L https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/openshift-client-linux.tar.gz | tar xz -C /usr/local/bin`.
    **`error: the server doesn't have a resource type "co"`** — Update your OpenShift CLI to match the cluster version, as `clusteroperator` (co) requires a compatible client build.
    **`grep: (standard input): No such file or directory`** — Verify the parent command (e.g., `oc get pods`) succeeds independently before using the piped alias.
---

## See also

- [OpenShift — Procedures](../procedures/)
- [OpenShift — Scripts](../scripts/)
- [OpenShift — Health Checks](../health-checks/)

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
