---
tags:
  - security
---
# OpenShift — Hardening

<div class="kb-summary">
OpenShift hardening: Security Context Constraints (SCC), Pod Security Admission, RHCOS node hardening, Compliance Operator, audit logging, network policies, image security, and CIS benchmark controls.

*Applies to: OpenShift 4.x*
</div>

```d2
direction: right

A: "Cluster Layer" {shape: rectangle}
B: "API endpoint hardening\nAudit logging enabled\netcd encryption on" {shape: rectangle}
C: "Node Layer" {shape: rectangle}
D: "RHCOS immutable OS\nSELinux enforcing\nNo SSH by default" {shape: rectangle}
E: "Workload Layer" {shape: rectangle}
F: "SCC restricted-v2\nNetworkPolicy deny-all\nResource limits required" {shape: rectangle}
G: "Supply Chain Layer" {shape: rectangle}
H: "Image signing cosign\nImageContentSourcePolicy\nNo :latest in production" {shape: rectangle}
I: "Hardened Cluster" {shape: rectangle}

A -> B
C -> D
E -> F
G -> H
B -> I
D -> I
F -> I
H -> I
```

```d2
direction: down

security_context_constraints: "Security Context Constraints" {shape: rectangle}
rhcos_node_hardening: "RHCOS Node Hardening" {shape: rectangle}
compliance_operator: "Compliance Operator" {shape: rectangle}
pod_security_admission_labels: "Pod Security Admission Labels" {shape: rectangle}
networkpolicy_defaults: "NetworkPolicy Defaults" {shape: rectangle}
image_security: "Image Security" {shape: rectangle}

security_context_constraints -> rhcos_node_hardening: hardens
rhcos_node_hardening -> compliance_operator: hardens
compliance_operator -> pod_security_admission_labels: hardens
pod_security_admission_labels -> networkpolicy_defaults: hardens
networkpolicy_defaults -> image_security: hardens
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Security Context Constraints

```bash
# List SCCs (ordered from least to most permissive)
oc get scc | awk '{print $1, $2, $3}'

# Check which SCC a running pod used
oc get pod <pod> -n <ns> \
  -o jsonpath='{.metadata.annotations.openshift\.io/scc}'

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

## RHCOS Node Hardening

RHCOS is a purpose-built immutable OS. Standard package management (yum/dnf) is disabled in the normal runtime. Changes are applied via MachineConfig objects managed by the Machine Config Operator (MCO).

```bash
# Inspect RHCOS node without modifying it
oc debug node/<node-name>
chroot /host
# / is read-only; writes go to /var or temporary paths

# Check SELinux status on node
oc debug node/<node> -- chroot /host sestatus

# Check which MachineConfig a node currently uses
oc get node <node> -o jsonpath='{.metadata.annotations.machineconfiguration\.openshift\.io/currentConfig}'

# Apply kernel sysctl settings via MachineConfig
oc apply -f - <<EOF
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  name: 99-worker-sysctl
  labels:
    machineconfiguration.openshift.io/role: worker
spec:
  config:
    ignition:
      version: 3.4.0
    storage:
      files:
      - path: /etc/sysctl.d/99-custom.conf
        mode: 0644
        contents:
          source: "data:,net.ipv4.ip_forward%3D1%0Akernel.dmesg_restrict%3D1%0Anet.ipv4.conf.all.log_martians%3D1"
EOF

# Monitor MachineConfig rollout (nodes drain and reboot sequentially)
oc get mcp worker -w
oc get nodes -w
```


```text title="Expected output"
Starting debug pod on node worker-1.example.com ...
Pod IP: 10.128.45.23
If you don't see a command prompt, try pressing enter.
sh-4.4# 
sh-4.4# exit
exit

SELinux status:
   SELinux status:                 enabled
   Current mode:                   enforcing
   Mode from config file:          enforcing
   Policy version:                 33
   Policy MLS status:              enabled

rendered-worker-99a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p

machineconfig.machineconfiguration.openshift.io/99-worker-sysctl created

NAME     CONFIG                                           UPDATED   UPDATING   DEGRADED   MACHINECOUNT   READYMACHINECOUNT   UPDATEDMACHINECOUNT   DEGRADEDMACHINECOUNT   AGE
worker   rendered-worker-99a1b2c3d4e5f6g7h8i9j0k1l2m3   False     True       False      3               1                   1                     0                      45d

NAME                STATUS   ROLES    AGE   VERSION
master-0            Ready    master   45d   v1.27.8+4fab27b
worker-0            Ready    worker   45d   v1.27.8+4fab27b
worker-1            NotReady worker   45d   v1.27.8+4fab27b
worker-2            Ready    worker   45d   v1.27.8+4fab27b
```

!!! warning "Common errors"
    **`error: unable to connect to the server: dial tcp: lookup api.example.com on 8.8.8.8:53: no such host`** — Verify your KUBECONFIG is set correctly and the cluster API endpoint is reachable.
    **`Error from server (BadRequest): error when creating "STDIN": MachineConfig.machineconfiguration.openshift.io "99-worker-sysctl" is invalid: spec.config.storage.files[0].contents.source: Invalid value: "data:,net.ipv4.ip_forward%3D1...": must be a valid data URL`** — Ensure the data URL is properly percent-encoded and the ignition version matches your OpenShift release.
    **`error: nodes "worker-1" not found`** — Verify the node name with `oc get nodes` and use the exact name from the output.
## Compliance Operator

The Compliance Operator runs OpenSCAP-based scans against CIS, PCI-DSS, FedRAMP, and STIG profiles.

```bash
# Install via OperatorHub (namespace: openshift-compliance)
# After install, create a scan binding:

oc apply -f - <<EOF
apiVersion: compliance.openshift.io/v1alpha1
kind: ScanSettingBinding
metadata:
  name: cis-compliance
  namespace: openshift-compliance
spec:
  profiles:
  - name: ocp4-cis
    kind: Profile
    apiGroup: compliance.openshift.io/v1alpha1
  - name: ocp4-cis-node
    kind: Profile
    apiGroup: compliance.openshift.io/v1alpha1
  settingsRef:
    name: default
    kind: ScanSetting
    apiGroup: compliance.openshift.io/v1alpha1
EOF

# Monitor scan progress
oc get compliancesuite -n openshift-compliance -w
oc get compliancescan -n openshift-compliance

# View results
oc get compliancecheckresult -n openshift-compliance | grep FAIL

# View available remediations
oc get complianceremediations -n openshift-compliance

# Apply a specific remediation
oc patch complianceremediation <name> -n openshift-compliance \
  --type=merge \
  -p '{"spec":{"apply":true}}'

# Apply all remediations for a scan (bulk apply — test in non-prod first)
oc get complianceremediations -n openshift-compliance -o name | \
  xargs -I{} oc patch {} -n openshift-compliance \
  --type=merge -p '{"spec":{"apply":true}}'
```


```text title="Expected output"
scansettingbinding.compliance.openshift.io/cis-compliance created
NAME                                    PHASE       RESULT
cis-compliance                          RUNNING     NOT-AVAILABLE
cis-compliance                          RUNNING     NOT-AVAILABLE
cis-compliance                          DONE        NON-COMPLIANT

NAME                          PHASE       RESULT
ocp4-cis                       DONE        NON-COMPLIANT
ocp4-cis-node                  DONE        NON-COMPLIANT

NAME                                                          STATUS
ocp4-cis-accounts-restrict-service-account-tokens           FAIL
ocp4-cis-api-server-audit-log-maxage                        FAIL
ocp4-cis-api-server-encryption-provider-cipher              FAIL
ocp4-cis-node-kubelet-anonymous-auth-disabled               FAIL
ocp4-cis-node-kubelet-streaming-connection-idle-timeout     FAIL
...

NAME                                                          CURRENT STATE
ocp4-cis-accounts-restrict-service-account-tokens           available
ocp4-cis-api-server-audit-log-maxage                        available
ocp4-cis-api-server-encryption-provider-cipher              available
ocp4-cis-node-kubelet-anonymous-auth-disabled               available
...

complianceremediation.compliance.openshift.io/ocp4-cis-api-server-audit-log-maxage patched
complianceremediation.compliance.openshift.io/ocp4-cis-api-server-encryption-provider-cipher patched
complianceremediation.compliance.openshift.io/ocp4-cis-node-kubelet-anonymous-auth-disabled patched
complianceremediation.compliance.openshift.io/ocp4-cis-node-kubelet-streaming-connection-idle-timeout patched
```

!!! warning "Common errors"
    **`error: resource mapping not found for name: "cis-compliance" namespace: "openshift-compliance" from "": no matches for kind "ScanSettingBinding" in version "compliance.openshift.io/v1alpha1"`** — Verify the Compliance Operator is installed in openshift-compliance namespace with `oc get deployment -n openshift-compliance`.
    **`Error from server (NotFound): complianceremediations.compliance.openshift.io "<name>" not found`** — Confirm the remediation name matches output from `oc get complianceremediations -n openshift-compliance` and wait for scans to complete.
    **`error: no matches for kind "ScanSetting" in version "compliance.openshift.io/v1alpha1"`** — Create the default ScanSetting resource first with `oc apply -f - <<EOF` using the ScanSetting template from the Compliance Operator documentation.
## Pod Security Admission Labels

```bash
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

# Verify which pods would fail restricted enforcement (dry-run audit)
oc label namespace my-project \
  pod-security.kubernetes.io/audit=restricted --overwrite
# Then check events:
oc get events -n my-project | grep PodSecurity
```


```text title="Expected output"
namespace/my-project labeled
namespace/legacy-app labeled
pod-security.kubernetes.io/enforce: restricted
pod-security.kubernetes.io/enforce-version: latest
pod-security.kubernetes.io/warn: restricted
pod-security.kubernetes.io/warn-version: latest
namespace/my-project labeled
LAST SEEN   TYPE     REASON           OBJECT                    MESSAGE
2m45s       Warning  PodSecurityViolation  pod/nginx-deployment-5d4b8c9f7  violates "restricted": allowPrivilegeEscalation != false
89s         Warning  PodSecurityViolation  pod/app-worker-2k8vx      violates "restricted": runAsNonRoot != true
45s         Warning  PodSecurityViolation  pod/legacy-svc-7j9m2      violates "restricted": capabilities.drop missing ["ALL"]
```

!!! warning "Common errors"
    **`Error from server (NotFound): namespaces "my-project" not found`** — Verify the namespace exists with `oc get namespaces` and use the correct name.
    **`error: unable to recognize "": no matches for kind "PodSecurityPolicy" in version "policy/v1beta1"`** — Pod Security Policies are deprecated; use Pod Security Admission (PSA) labels on namespaces instead.
    **`Warning: pod-security.kubernetes.io/enforce: restricted is not a valid label value`** — Ensure the label value is exactly `restricted`, `baseline`, or `privileged` with no typos or extra whitespace.
## NetworkPolicy Defaults

```yaml
# deny-all-ingress-egress.yaml — apply to every application namespace
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
# allow-same-namespace ingress
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
# allow-from-router — required for Routes/Ingress to reach pods
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
---
# allow DNS egress (required for pods to resolve names)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns-egress
  namespace: my-project
spec:
  podSelector: {}
  egress:
  - ports:
    - port: 53
      protocol: UDP
    - port: 53
      protocol: TCP
```

```bash
# Apply and verify
oc apply -f deny-all-ingress-egress.yaml -n my-project
oc get networkpolicy -n my-project

# Label namespace for router access policy
oc label namespace openshift-ingress network.openshift.io/policy-group=ingress
```


```text title="Expected output"
networkpolicy.networking.k8s.io/deny-all-ingress-egress created
NAME                        POD-SELECTOR   AGE
deny-all-ingress-egress     <none>         0s
namespace/openshift-ingress labeled
```

!!! warning "Common errors"
    **`Error from server (NotFound): namespaces "my-project" not found`** — Verify the project exists with `oc get projects` and create it if needed using `oc new-project my-project`.
    **`Error from server (AlreadyExists): networkpolicies.networking.k8s.io "deny-all-ingress-egress" already exists`** — Delete the existing policy first with `oc delete networkpolicy deny-all-ingress-egress -n my-project` or use `oc apply --force-conflicts=true`.
## Image Security

```bash
# Schedule periodic re-import to pick up patched base images
oc import-image myapp:latest \
  --from=quay.io/myorg/myapp:latest \
  --confirm \
  --scheduled \
  -n my-project

# ImagePruner CR: automatic cleanup of old image layers
oc apply -f - <<EOF
apiVersion: imageregistry.operator.openshift.io/v1
kind: ImagePruner
metadata:
  name: cluster
spec:
  schedule: "0 0 * * *"
  suspend: false
  keepTagRevisions: 3
  keepYoungerThan: 604800   # 7 days in seconds
  resources: {}
EOF

# Pin images by digest to prevent supply chain tampering
# BAD: image: myapp:latest
# GOOD: image: quay.io/myorg/myapp@sha256:abc123...

# Check image streams for untagged/stale images
oc get imagestream -A | grep -v "<none>"
oc adm top images
```


```text title="Expected output"
Importing image 'myapp:latest' from 'quay.io/myorg/myapp:latest'
Scheduled import added to ImageStream 'myapp'
imagestreamimport.image.openshift.io/myapp imported

imagepruner.imageregistry.operator.openshift.io/cluster created

NAMESPACE     NAME                IMAGE REPOSITORY                           TAGS      UPDATED
my-project    myapp               quay.io/myorg/myapp                         latest    2 minutes ago
kube-system   coredns             registry.k8s.io/coredns                     v1.9.3    5 days ago
openshift     oauth-proxy         registry.redhat.com/openshift4/ose-oauth   v4.12.15  3 weeks ago
...

Images by size:
NAME                                                    SIZE
quay.io/myorg/myapp@sha256:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6   487.3 MiB
registry.redhat.com/openshift4/ose-oauth@sha256:9z8y7x6w5v4u3t2s1r0q9p8o7n6m5l4k3j2i1h0g   156.8 MiB
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "imagepruner"`** — Ensure the image-registry operator is installed and running with `oc get operator image-registry -o wide`.
    **`error: unable to connect to quay.io/myorg/myapp:latest: unauthorized`** — Verify the image pull secret exists in the namespace with `oc get secrets -n my-project | grep pull-secret` and that credentials have pull access to the registry.
## Audit Logging

```bash
# Enable API audit logging
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


```text title="Expected output"
apiserver.config.openshift.io/cluster patched
audit:
  profile: WriteRequestBodies
spec:
  servingCerts: {}
  unsupportedConfigOverrides: null

Jumping into namespace "openshift-kube-apiserver"
Starting pod/ip-10-0-45-12-debug ...
To use host binaries, run `chroot /host`

Nov 15 14:32:18 ip-10-0-45-12 kube-apiserver[2847]: audit: level=RequestResponse verb=create user="system:admin" namespace=default resource=pods
Nov 15 14:32:19 ip-10-0-45-12 kube-apiserver[2847]: audit: level=RequestResponse verb=patch user="system:serviceaccount:openshift-kube-apiserver:sa-token" namespace=openshift-kube-apiserver resource=configmaps
Nov 15 14:32:21 ip-10-0-45-12 kube-apiserver[2847]: audit: level=RequestResponse verb=get user="system:kube-controller-manager" namespace="" resource=clusterrolebindings
Nov 15 14:32:22 ip-10-0-45-12 kube-apiserver[2847]: audit: level=RequestResponse verb=watch user="system:node:ip-10-0-45-12" namespace=default resource=pods
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "apiserver"`** — Verify you are connected to an OpenShift cluster (not vanilla Kubernetes) with `oc api-resources | grep apiserver`.
    **`journalctl: command not found`** — Run `chroot /host` first before executing journalctl to access the host filesystem.
    **`No such file or directory: /var/log/kube-apiserver/audit.log`** — Check the actual audit log path with `find /var/log -name "*audit*"` or verify the audit profile has been applied with `oc get apiserver cluster -o yaml`.
## CIS OCP 4 Benchmark — Key Controls

| Category | Control | Command / Action |
|---|---|---|
| API Server | Disable anonymous auth | Enforced by default; verify with `oc get apiserver cluster -o yaml` |
| API Server | Enable audit logging | `oc patch apiserver cluster --type merge -p '{"spec":{"audit":{"profile":"WriteRequestBodies"}}}'` |
| etcd | Encrypt data at rest | `oc patch apiserver cluster --type merge -p '{"spec":{"encryption":{"type":"aesgcm"}}}'` |
| Authentication | Disable kubeadmin | `oc delete secret kubeadmin -n kube-system` (after IDP configured) |
| RBAC | Remove self-provisioner from all | `oc adm policy remove-cluster-role-from-group self-provisioner system:authenticated:oauth` |
| RBAC | Avoid cluster-admin for humans | Use `admin` role in namespace; `cluster-admin` only for break-glass SAs |
| Networking | Default deny NetworkPolicy | Apply deny-all NetworkPolicy to every application namespace |
| Networking | Restrict egress | Add egress NetworkPolicy rules; deny external by default |
| Workloads | Use restricted SCC | Default for new namespaces; audit with `oc get pod -o jsonpath='{.items[*].metadata.annotations.openshift\.io/scc}'` |
| Workloads | Enforce PSA restricted | `oc label namespace <ns> pod-security.kubernetes.io/enforce=restricted` |
| Images | No `:latest` tags in production | Use digest references; configure ImagePruner |
| Images | Require signed images | Deploy `ClusterImagePolicy` with cosign public key |
| Nodes | SELinux enforcing | Enforced by default on RHCOS; verify with `sestatus` via node debug |
| Nodes | No SSH access | Default RHCOS; enable only via MachineConfig for break-glass |

## See also

- [OpenShift — Access Control](../access-control/)
- [OpenShift — Authentication](../authentication/)
- [OpenShift — Health Checks](../../operations/health-checks/)
