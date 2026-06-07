# OpenShift — Integrations

<div class="kb-summary">
vSphere IPI and UPI installation modes, LDAP/Active Directory identity, Quay image registry, Advanced Cluster Management (ACM), and ODF storage integration.
</div>

```text
┌──────────────────────────────────── OpenShift Integrations ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   vSphere IPI: installer creates VMs via vCenter API; CCM manages node lifecycle              │   │
│   │   Identity: OAuth server front-ends all auth; LDAP/AD provider maps groups to RBAC            │   │
│   │   Quay: enterprise image registry; integrated via ImageContentSourcePolicy for air-gap        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │    Infrastructure (IPI)     │  │       Identity (LDAP)        │  │     Registry (Quay)         │  │
│   │      ─────────────          │  │      ─────────────           │  │      ─────────────          │  │
│   │  vCenter creds in secret    │  │  OAuth → LDAPIdentityProvider│  │  ImageContentSourcePolicy  │   │
│   │  VM folder + datastore      │  │  Group sync via CronJob      │  │  Pull-through cache         │  │
│   │  Cloud Controller Manager   │  │  serviceAccountIssuer TLS   │  │  Robot accounts for CI      │   │
│   │  CSI driver for PVCs        │  │  kubeadmin disabled post-day1│  │  Cosign image signing       │  │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    CCM          = Cloud Controller Manager; integrates OCP with vSphere/AWS/Azure node lifecycle      │
│    ICSP         = ImageContentSourcePolicy; redirects registry pulls (e.g. quay.io → mirror.local)    │
│    OAuth server = OpenShift's built-in OAuth2 server; IdentityProviders add login methods             │
│    ACM          = Advanced Cluster Management; fleet-level policy, placement, and observability       │
│    ODF          = OpenShift Data Foundation (Rook-Ceph); provides RBD and CephFS StorageClasses       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

# CSI driver config post-install
oc get configmap cloud-provider-config -n openshift-config
oc get csidriver csi.vsphere.volume.vmware.com
```

## LDAP / Active Directory Identity Provider

```yaml
# OAuth LDAP identity provider
apiVersion: config.openshift.io/v1
kind: OAuth
metadata:
  name: cluster
spec:
  identityProviders:
  - name: ldap
    type: LDAP
    ldap:
      url: "ldap://ad.example.com/CN=Users,DC=example,DC=com?sAMAccountName"
      bindDN: "CN=svc-ocp,OU=ServiceAccounts,DC=example,DC=com"
      bindPassword:
        name: ldap-bind-password    # Secret in openshift-config namespace
      insecure: false
      ca:
        name: ldap-ca-cert          # ConfigMap with CA cert
      attributes:
        id: ["dn"]
        email: ["mail"]
        name: ["cn"]
        preferredUsername: ["sAMAccountName"]
```

```bash
# Group sync — run periodically via CronJob
oc adm groups sync --sync-config=ldap-sync-config.yaml --confirm

# Bind AD group to OCP cluster-admin
oc adm policy add-cluster-role-to-group cluster-admin "CN=OCP-Admins,OU=Groups,DC=example,DC=com"

# Disable kubeadmin after LDAP confirmed working
oc delete secret kubeadmin -n kube-system
```

## Quay Image Registry

```yaml
# ImageContentSourcePolicy — redirect docker.io to internal mirror
apiVersion: operator.openshift.io/v1alpha1
kind: ImageContentSourcePolicy
metadata:
  name: mirror-registry
spec:
  repositoryDigestMirrors:
  - mirrors:
    - quay.local.example.com/openshift
    source: quay.io/openshift-release-dev/ocp-release
  - mirrors:
    - quay.local.example.com/library
    source: docker.io/library
```

```bash
# Configure internal registry storage (OCP built-in)
oc patch configs.imageregistry.operator.openshift.io cluster \
  --type merge -p '{"spec":{"managementState":"Managed","storage":{"pvc":{"claim":""}}}}'

# Pull secret — add Quay credentials
oc set data secret/pull-secret -n openshift-config --from-file=.dockerconfigjson=pull-secret.json
```

## Advanced Cluster Management (ACM)

```bash
# Install ACM operator from OperatorHub
oc apply -f multiclusterhub.yaml    # Creates MultiClusterHub in open-cluster-management ns

# Import existing cluster
oc apply -f import-cluster.yaml     # Generates klusterlet agent manifests for spoke cluster

# Check hub status
oc get multiclusterhub -n open-cluster-management
oc get managedclusters                        # All registered clusters
oc get policy -n policies                     # Applied governance policies
```

## ODF (OpenShift Data Foundation) Storage

```bash
# ODF operator install via OperatorHub, then:
oc apply -f storagecluster.yaml     # StorageCluster CR — defines OSD disks and replica count

# Verify ODF health
oc get storagecluster -n openshift-storage
oc get cephcluster -n openshift-storage
oc rsh -n openshift-storage $(oc get pod -n openshift-storage -l app=rook-ceph-tools -o name) \
  ceph status
```
