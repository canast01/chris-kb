---
tags:
  - architecture
description: "vSphere IPI and UPI installation modes, LDAP/Active Directory identity, Quay image registry, Advanced Cluster Management (ACM), and ODF storage..."
---
# OpenShift — Integrations

<div class="kb-summary">
vSphere IPI and UPI installation modes, LDAP/Active Directory identity, Quay image registry, Advanced Cluster Management (ACM), and ODF storage integration.

*Applies to: OpenShift 4.x*
</div>

```d2
direction: right

OCP: "OCP Cluster" {shape: rectangle}
VS: "vSphere\ncloud provider" {shape: rectangle}
ID: "LDAP / AD\nidentity" {shape: rectangle}
REG: "Harbor / Quay\nregistry" {shape: rectangle}
SEC: "Vault / cert-manager\nsecrets + certs" {shape: rectangle}
LOG: "Elasticsearch / Splunk\nlogging" {shape: rectangle}
MON: "Prometheus / Grafana\nmonitoring" {shape: rectangle}
CD: "GitLab / ArgoCD\nCI/CD" {shape: rectangle}
VS1: "CCM node lifecycle" {shape: rectangle}
VS2: "vSphere CSI PVCs" {shape: rectangle}
ID1: "OAuth CR\nLDAP provider" {shape: rectangle}
ID2: "oc adm groups sync" {shape: rectangle}
REG1: "ICSP mirror rules" {shape: rectangle}
REG2: "oc mirror air-gap" {shape: rectangle}
SEC1: "ClusterIssuer" {shape: rectangle}
SEC2: "Certificate CR" {shape: rectangle}
CD1: "OpenShift GitOps\nArgoCD operator" {shape: rectangle}
CD2: "AppProject + Application" {shape: rectangle}

OCP -> VS
OCP -> ID
OCP -> REG
OCP -> SEC
OCP -> LOG
OCP -> MON
OCP -> CD
VS -> VS1
VS -> VS2
ID -> ID1
ID -> ID2
REG -> REG1
REG -> REG2
SEC -> SEC1
SEC -> SEC2
CD -> CD1
CD -> CD2
```

## vSphere IPI Integration

```yaml
# install-config.yaml — vSphere platform section
platform:
  vsphere:
    vcenter: vcenter.example.com
    username: ocp-install@vsphere.local
    password: "<password>"
    datacenter: DC1
    defaultDatastore: vsanDatastore
    folder: /DC1/vm/openshift
    network: VM Network
    diskType: thin
    resourcePool: /DC1/host/Cluster/Resources/openshift
```

```bash
# Required vCenter permissions for IPI installer
# Minimum: create/delete VMs, manage networks/datastores in target folder
# Service account: ocp-install@vsphere.local with custom role

# Verify CSI driver post-install
oc get csidriver csi.vsphere.volume.vmware.com
oc get configmap cloud-provider-config -n openshift-config
```


```text title="Expected output"
NAME                                    PROVISIONER                             AGE
csi.vsphere.volume.vmware.com           csi.vsphere.volume.vmware.com           3d12h

NAME                    DATA   AGE
cloud-provider-config   1      3d12h
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: the server doesn't have a resource type "csidriver"` | Verify the cluster is fully initialized by running `oc get nodes` and waiting for all nodes to reach Ready status. |
    | `Error from server (NotFound): configmaps "cloud-provider-config" not found` | Confirm vSphere integration was enabled during IPI installation; re-run the installer with the correct vCenter credentials if the ConfigMap is missing. |
### vSphere Cloud Controller Manager (CCM)

The CCM (`openshift-cloud-controller-manager` namespace) manages the node lifecycle: it provisions node objects when VMs come up, updates node addresses, and removes node objects when VMs are deleted. It also adds topology labels used by the scheduler.

**Node labels added by CCM:**

| Label | Example value | Source |
|---|---|---|
| `topology.kubernetes.io/zone` | `DC1-Cluster1` | vSphere cluster or host group |
| `topology.kubernetes.io/region` | `DC1` | vSphere datacenter |
| `node.kubernetes.io/instance-type` | `vsphere-vm` | Set by CCM |

```bash
# Check CCM pods
oc get pods -n openshift-cloud-controller-manager

# Verify topology labels on a node
oc get node <node> -o jsonpath='{.metadata.labels}' | jq 'with_entries(select(.key | startswith("topology")))'

# StorageClass using topology (zone-aware volume placement)
cat <<'EOF'
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: thin-csi-zonal
provisioner: csi.vsphere.volume.vmware.com
parameters:
  storagePolicyName: "vSAN Default Storage Policy"
  datastoreURL: "ds:///vmfs/volumes/<uuid>/"
volumeBindingMode: WaitForFirstConsumer   # Waits for pod scheduling to pick zone
allowVolumeExpansion: true
EOF
```


```text title="Expected output"
NAME                                             READY   STATUS    RESTARTS   AGE
vsphere-cloud-controller-manager-8x4kp           1/1     Running   0          12d
vsphere-cloud-controller-manager-j2m9l           1/1     Running   0          12d
vsphere-cloud-controller-manager-qr5xn           1/1     Running   0          12d

{"topology.kubernetes.io/region":"us-east-1","topology.kubernetes.io/zone":"us-east-1a","topology.vmware.com/failure-domain":"fd-1","topology.vmware.com/rack":"rack-02"}

apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: thin-csi-zonal
provisioner: csi.vsphere.volume.vmware.com
parameters:
  storagePolicyName: "vSAN Default Storage Policy"
  datastoreURL: "ds:///vmfs/volumes/5a3e8c2f-7b1d-4e9a-b6c3-2f8e1a9d7c4b/"
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: the server doesn't have a resource type "node" or you've misspelled it` | Replace `<node>` with an actual node name from `oc get nodes`. |
    | `jq: command not found` | Install jq on the bastion host with `sudo yum install -y jq` or use `grep` to filter labels instead. |
    | `error: resource name may not be empty` | Ensure the CCM namespace `openshift-cloud-controller-manager` exists; verify with `oc get ns | grep cloud-controller`. |
## LDAP / Active Directory Identity Provider

```yaml
# OAuth CR — LDAP identity provider configuration
apiVersion: config.openshift.io/v1
kind: OAuth
metadata:
  name: cluster
spec:
  identityProviders:
  - name: ldap
    type: LDAP
    mappingMethod: claim
    ldap:
      url: "ldap://ad.example.com/CN=Users,DC=example,DC=com?sAMAccountName"
      bindDN: "CN=svc-ocp,OU=ServiceAccounts,DC=example,DC=com"
      bindPassword:
        name: ldap-bind-password    # Secret in openshift-config namespace
      insecure: false
      ca:
        name: ldap-ca-cert          # ConfigMap with CA bundle in openshift-config
      attributes:
        id: ["dn"]
        email: ["mail"]
        name: ["cn"]
        preferredUsername: ["sAMAccountName"]
```

```bash
# Create bindPassword secret
oc create secret generic ldap-bind-password \
  --from-literal=bindPassword='<password>' \
  -n openshift-config

# Create CA ConfigMap (if LDAPS / AD certificate)
oc create configmap ldap-ca-cert \
  --from-file=ca.crt=/path/to/ad-ca.crt \
  -n openshift-config

# Manual group sync — run interactively or via CronJob
oc adm groups sync --sync-config=ldap-sync.yaml --confirm

# Bind synced group to cluster-admin
oc adm policy add-cluster-role-to-group cluster-admin ocp-admins

# Disable kubeadmin after LDAP is confirmed working
oc delete secret kubeadmin -n kube-system
```


```text title="Expected output"
secret/ldap-bind-password created
configmap/ldap-ca-cert created
group.user.openshift.io/ocp-admins created
group.user.openshift.io/ocp-developers created
group.user.openshift.io/ocp-viewers created
clusterrolebinding.rbac.authorization.k8s.io/cluster-admin-ocp-admins created
secret "kubeadmin" deleted
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: unable to read /path/to/ad-ca.crt: no such file or directory` | Verify the CA certificate path exists and is readable with `ls -la /path/to/ad-ca.crt` before running the configmap command. |
    | `error: groups sync failed: LDAP server unreachable or invalid credentials` | Confirm LDAP connectivity and bindPassword secret are correct by testing with `ldapsearch -x -H ldap://ad-server:389 -D "cn=bind-user,dc=example,dc=com" -W`. |
    | `Error from server (NotFound): secrets "kubeadmin" not found` | Only delete kubeadmin after LDAP authentication is fully tested; if it's already deleted, skip this step or restore from backup if needed. |
**Recommended:** Use the Red Hat `Group Sync Operator` from OperatorHub for scheduled automatic group synchronization. Install in `group-sync-operator` namespace; create a `GroupSync` CR pointing at your LDAP/AD server to run on a cron schedule (e.g. `*/30 * * * *`).

## Image Registry Integration

### Built-in OpenShift Registry

```bash
# Enable managed image registry with PVC backend
oc patch configs.imageregistry.operator.openshift.io cluster \
  --type merge -p '{"spec":{"managementState":"Managed","storage":{"pvc":{"claim":""}}}}'

# Enable with S3 backend (air-gap / on-prem MinIO)
oc patch configs.imageregistry.operator.openshift.io cluster \
  --type merge -p '{
    "spec":{
      "managementState":"Managed",
      "storage":{
        "s3":{
          "bucket":"openshift-registry",
          "region":"us-east-1",
          "regionEndpoint":"https://minio.example.com",
          "encrypt":false
        }
      }
    }
  }'

# Check registry operator status
oc get configs.imageregistry.operator.openshift.io cluster -o yaml | grep -A10 status
```


```text title="Expected output"
config.imageregistry.operator.openshift.io/cluster patched
config.imageregistry.operator.openshift.io/cluster patched
  status:
    conditions:
    - lastTransitionTime: "2024-01-15T09:42:31Z"
      message: The registry is ready
      reason: Ready
      status: "True"
      type: Available
    - lastTransitionTime: "2024-01-15T09:42:28Z"
      message: ""
      reason: ConfigurationValid
      status: "True"
      type: Progressing
    observedGeneration: 3
    readyReplicas: 2
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: the server doesn't have a resource type "configs" in group "imageregistry.operator.openshift.io"` | Verify the Image Registry Operator is installed with `oc get operators | grep image-registry` and install it from OperatorHub if missing. |
    | `The registry is not available` | Ensure the storage backend (PVC or S3) is accessible and has sufficient capacity by checking `oc describe pvc` or S3 bucket permissions. |
    | `invalid JSON in patch` | Validate JSON syntax using a linter before patching; common issues are unescaped quotes or missing commas in the spec object. |
### Air-Gap Mirror with oc mirror

```bash
# Mirror OCP release images to internal registry (OCP 4.10+ oc-mirror plugin)
oc mirror --config=imageset-config.yaml docker://quay.local.example.com/ocp-mirror

# Apply generated ImageContentSourcePolicy
oc apply -f oc-mirror-workspace/results-*/imageContentSourcePolicy.yaml
oc get imagecontentsourcepolicy
```


```text title="Expected output"
Sending expected image layers to image registry...
Mirroring completed successfully
wrote mirroring manifests to oc-mirror-workspace/

imagecontentsourcepolicy.config.openshift.io/mirror-openshift-container-errata created
imagecontentsourcepolicy.config.openshift.io/mirror-openshift-release-images created

NAME                                    AGE
mirror-openshift-container-errata       2s
mirror-openshift-release-images         5s
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: unable to read imageset-config.yaml: no such file or directory` | Verify the imageset-config.yaml file exists in the current directory and contains valid YAML syntax. |
    | `error: failed to push image to quay.local.example.com: x509: certificate signed by unknown authority` | Configure the registry as insecure in the imageset-config.yaml or add the registry's CA certificate to the system trust store. |
    | `error: imagecontentsourcepolicy.config.openshift.io "mirror-openshift-release-images" already exists` | Delete the existing policy with `oc delete imagecontentsourcepolicy mirror-openshift-release-images` before reapplying. |
## cert-manager Integration

cert-manager automates TLS certificate lifecycle. Install via OperatorHub (`cert-manager` operator in `cert-manager` namespace).

```yaml
# ClusterIssuer for internal CA (ACME/Let's Encrypt alternative)
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: internal-ca
spec:
  ca:
    secretName: internal-ca-key-pair   # Secret containing tls.crt + tls.key

---
# Certificate CR — creates TLS Secret automatically
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: apps-wildcard
  namespace: openshift-ingress
spec:
  secretName: apps-wildcard-tls
  issuerRef:
    name: internal-ca
    kind: ClusterIssuer
  dnsNames:
  - "*.apps.cluster.example.com"
  duration: 8760h    # 1 year
  renewBefore: 720h  # Renew 30 days before expiry
```

```bash
# Patch ingress controller to use custom wildcard cert
oc patch ingresscontroller default -n openshift-ingress-operator \
  --type=merge -p '{
    "spec":{
      "defaultCertificate":{
        "name":"apps-wildcard-tls"
      }
    }
  }'

# Check cert-manager certificate status
oc get certificate -A
```


```text title="Expected output"
ingresscontroller.operator.openshift.io/default patched
NAMESPACE              NAME                           READY   SECRET                AGE
openshift-ingress     apps-wildcard-tls              True    apps-wildcard-tls    45d
cert-manager          letsencrypt-prod               True    letsencrypt-secret    32d
openshift-ingress     api-cert-internal             True    api-cert-secret       89d
cert-manager          wildcard-staging               False   wildcard-staging-tls  2d
kube-system           kubelet-serving-cert           True    kubelet-certs         156d
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: the server doesn't have a resource type "ingresscontroller" in group "operator.openshift.io"` | Verify you are connected to an OpenShift cluster (not vanilla Kubernetes) with `oc api-resources | grep ingress`. |
    | `Error from server (NotFound): secrets "apps-wildcard-tls" not found` | Create the TLS secret first using `oc create secret tls apps-wildcard-tls --cert=cert.crt --key=key.key -n openshift-ingress`. |
    | `certificate.cert-manager.io "apps-wildcard-tls" not found` | Confirm the secret exists in the correct namespace with `oc get secret apps-wildcard-tls -n openshift-ingress` before patching. |
## ArgoCD / OpenShift GitOps

OpenShift GitOps operator installs ArgoCD. Install from OperatorHub; the operator creates an `ArgoCD` CR in `openshift-gitops` namespace automatically.

```yaml
# AppProject — restricts what an ArgoCD project can deploy
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: platform-infra
  namespace: openshift-gitops
spec:
  sourceRepos:
  - https://gitlab.example.com/platform/*
  destinations:
  - namespace: "*"
    server: https://kubernetes.default.svc
  clusterResourceWhitelist:
  - group: "*"
    kind: "*"

---
# Application CR — syncs a Git repo path to a namespace
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: cluster-config
  namespace: openshift-gitops
spec:
  project: platform-infra
  source:
    repoURL: https://gitlab.example.com/platform/cluster-config
    targetRevision: main
    path: overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: openshift-config
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

```bash
# Check ArgoCD application sync status
oc get application -n openshift-gitops
oc get application cluster-config -n openshift-gitops -o yaml | grep -A10 status

# Sync an application manually
oc -n openshift-gitops exec deploy/openshift-gitops-server -- \
  argocd app sync cluster-config --auth-token <token>

# Get ArgoCD admin password
oc -n openshift-gitops get secret openshift-gitops-cluster -o jsonpath='{.data.admin\.password}' | base64 -d
```


```text title="Expected output"
NAME            SYNC STATUS   HEALTH STATUS   REPO                                    PATH
cluster-config  Synced        Healthy         https://github.com/acme/gitops-repo     clusters/prod
ingress-config  OutOfSync     Progressing     https://github.com/acme/gitops-repo     clusters/ingress
status:
  conditions:
  - lastTransitionTime: "2024-01-15T09:42:33Z"
    message: "successfully synced (revision: abc123def456)"
    reason: "SyncOperationSucceeded"
    status: "True"
    type: "Synced"
  health:
    status: Healthy
  syncResult:
    resources: 47
    revision: abc123def456
    syncPhase: Succeeded
    syncTimestamp: "2024-01-15T09:42:33Z"
Application 'cluster-config' synced and healthy
admin@argocd.example.com:p@ssw0rd_2024
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: the server doesn't have a resource type "application"` | Ensure ArgoCD is installed in the cluster with `oc get ns openshift-gitops` and verify the CRD exists via `oc get crd applications.argoproj.io`. |
    | `error: unable to connect to the server: dial tcp: lookup argocd-server on 127.0.0.1:53: no such host` | Port-forward to the ArgoCD server first with `oc port-forward -n openshift-gitops svc/openshift-gitops-server 8080:443` or use the route hostname instead. |
    | `error: invalid token` | Replace `<token>` with a valid ArgoCD API token obtained from `oc -n openshift-gitops exec deploy/openshift-gitops-server -- argocd account generate-token --account <username>`. |
## Advanced Cluster Management (ACM)

```bash
# Install ACM operator from OperatorHub, then create hub
oc apply -f multiclusterhub.yaml    # Creates MultiClusterHub in open-cluster-management ns

# Import existing cluster (generates klusterlet agent manifests for spoke)
oc apply -f import-cluster.yaml

# Check hub and managed cluster status
oc get multiclusterhub -n open-cluster-management
oc get managedclusters
oc get policy -n policies           # Governance policies applied to fleet
```


```text title="Expected output"
multiclusterhub.yaml created
import-cluster.yaml created
NAME            HUB ID                                   STATUS   AGGREGATED STATUS
local-cluster   12a4f8c9-3e2b-11ed-b878-0242ac110002   Running  Healthy
NAME                    HUB ACCEPTED   MANAGED CLUSTER URLS        STATUS
local-cluster           true           https://api.hub.local:6443  Ready
spoke-cluster-prod      true           https://api.spoke1.local    Ready
spoke-cluster-staging   true           https://api.spoke2.local    Ready
NAME                                    REMEDIATION ACTION   COMPLIANCE STATE   AGE
policy-pod-security-standards           inform               Compliant          8d
policy-network-isolation                enforce              Compliant          5d
policy-rbac-enforcement                 audit                NonCompliant       2d
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: resource mapping not found for name: "multiclusterhub" namespace: "open-cluster-management"` | Ensure the ACM operator is fully installed and the CRD is available with `oc get crd | grep multiclusterhub`. |
    | `The MultiClusterHub "multiclusterhub" is invalid: spec.imagePullSecret: Invalid value: "": imagePullSecret cannot be empty` | Add a valid imagePullSecret to multiclusterhub.yaml or use `spec.imagePullSecret: null` if using default registry credentials. |
## ODF (OpenShift Data Foundation) Storage

```bash
# ODF operator install via OperatorHub, then deploy StorageCluster
oc apply -f storagecluster.yaml     # Defines OSD disks and replica count

# Verify ODF health
oc get storagecluster -n openshift-storage
oc get cephcluster -n openshift-storage
oc rsh -n openshift-storage $(oc get pod -n openshift-storage -l app=rook-ceph-tools -o name) \
  ceph status
```


```text title="Expected output"
storagecluster.yaml created
NAME                 AGE   PHASE       EXTERNAL   CREATED AT
ocs-storagecluster   2m    Ready       false      2024-01-15T09:23:14Z

NAME           DATAPOOL   MONCOUNT   AGE   PHASE   MESSAGE
ceph-cluster   3          3          2m    Ready   Cluster created successfully

  cluster:
    id:     a1b2c3d4-e5f6-7890-abcd-ef1234567890
    health: HEALTH_OK
    monmap epoch: 3
    osdmap epoch: 12
    pgmap v45: 128 pgs: 128 active+clean
    mon: 3 daemons, quorum a,b,c (age 2m)
    osd: 3 osds: 3 up (since 2m), 3 in (since 2m)
    pools: 3 pools, 9 pgs
    objects: 0 objects, 0 B
    usage: 0 B used, 300 GiB avail, 0 B total
    pgs: 128 active+clean
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: the server doesn't have a resource type "storagecluster"` | Ensure the ODF operator is installed first via OperatorHub or `oc apply -f odf-operator.yaml`. |
    | `pod not found with selector: app=rook-ceph-tools` | Wait for the rook-ceph-tools pod to be ready with `oc wait --for=condition=Ready pod -l app=rook-ceph-tools -n openshift-storage --timeout=300s`. |
    | `CephCluster is in a degraded state: insufficient OSDs` | Verify that all OSD disks are properly attached and available by checking `oc describe storagecluster -n openshift-storage` for device discovery errors. |
## See also

- [OpenShift — How It Works](../how-it-works/)
- [OpenShift — Deploy](../../deploy/)
