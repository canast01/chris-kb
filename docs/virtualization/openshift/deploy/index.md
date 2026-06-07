# OpenShift — Deploy

<div class="kb-summary">
IPI vs UPI installation methods, install-config.yaml structure, RHCOS bootstrap, air-gap mirror setup, and post-install validation checklist.
</div>

```text
┌──────────────────────────────────────── OpenShift Deployment ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 OpenShift Installation Methods                                │   │
│   │       IPI: installer manages infrastructure (vSphere, AWS, bare-metal); fully automated       │   │
│   │      UPI: admin provisions infra manually; installer only bootstraps the cluster software     │   │
│   │     Air-gap: all images mirrored to internal registry; no internet required during install    │   │
│   │        install-config.yaml: single source of truth for cluster topology and parameters        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           IPI Install (Automated)            │  │             UPI Install (Manual)            │   │
│   │        openshift-install create cluster      │  │            Provision nodes manually         │   │
│   │        Installer creates VMs (vSphere)       │  │           Generate ignition configs         │   │
│   │          Manages load balancers, DNS         │  │            Bootstrap node → masters         │   │
│   │         MachineAPI for worker scaling        │  │           Manual worker CSR approval        │   │
│   │         Recommended for vSphere/cloud        │  │         Required for bare-metal/custom      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│    Bootstrap  = Temporary node that initializes first master; removed after install                   │
│    Ignition   = CoreOS provisioning system; configures RHCOS nodes on first boot                      │
│    CSR        = Certificate Signing Request; workers submit CSRs; admin approves                      │
│                                                                                                       │
```

## Prerequisites Checklist

```bash
# DNS requirements (MUST exist before install)
# api.<cluster>.<base-domain>        → load balancer / VIP for masters port 6443
# api-int.<cluster>.<base-domain>    → same (internal)
# *.apps.<cluster>.<base-domain>     → wildcard for router (port 80/443)

# Validate DNS
nslookup api.ocp.example.com
nslookup test.apps.ocp.example.com
dig +short api.ocp.example.com

# NTP (etcd requires <1s drift between masters)
chronyc tracking        # or timedatectl status

# Port requirements on load balancer
# Master API:  6443 (from workers + clients)
# Machine config: 22623 (from nodes, bootstrap phase only)
# Router HTTP:  80 → infra/worker nodes
# Router HTTPS: 443 → infra/worker nodes
```

## install-config.yaml

```yaml
apiVersion: v1
baseDomain: example.com
metadata:
  name: ocp                # cluster name; combined: ocp.example.com
compute:
- architecture: amd64
  hyperthreading: Enabled
  name: worker
  replicas: 3
controlPlane:
  architecture: amd64
  hyperthreading: Enabled
  name: master
  replicas: 3              # Always 3 for production
platform:
  vsphere:
    vcenter: vcenter.example.com
    username: ocp-install@vsphere.local
    password: "VMware1!"
    datacenter: Datacenter
    defaultDatastore: vsanDatastore
    folder: /Datacenter/vm/ocp
    network: "VM Network"
    diskType: thin
pullSecret: '{"auths":{"cloud.redhat.com":{"auth":"..."}}}'
sshKey: 'ssh-rsa AAAA... admin@example.com'
```

## IPI Installation

```bash
# Download installer from Red Hat Console or mirror
wget https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/openshift-install-linux.tar.gz

# Create install dir (preserves install state)
mkdir ocp-install && cp install-config.yaml ocp-install/

# Run full install
./openshift-install create cluster --dir ocp-install --log-level=info

# Monitor progress
./openshift-install wait-for bootstrap-complete --dir ocp-install
./openshift-install wait-for install-complete --dir ocp-install

# Credentials written to:
cat ocp-install/auth/kubeconfig
cat ocp-install/auth/kubeadmin-password
```

## UPI Installation (vSphere)

```bash
# 1. Generate manifests and ignition configs
./openshift-install create manifests --dir ocp-install
./openshift-install create ignition-configs --dir ocp-install

# 2. Host ignition files via HTTP (nodes fetch on first boot)
# bootstrap.ign, master.ign, worker.ign

# 3. Create VMs from RHCOS OVA; pass ignition via guestinfo:
#    guestinfo.ignition.config.data = base64(ignition file)
#    guestinfo.ignition.config.data.encoding = base64

# 4. Monitor bootstrap
./openshift-install wait-for bootstrap-complete

# 5. Approve worker CSRs
oc get csr | grep Pending
oc adm certificate approve <csr-name>
# Or approve all:
oc get csr -o name | xargs oc adm certificate approve

# 6. Confirm install
./openshift-install wait-for install-complete
```

## Air-Gap Mirror Setup

```bash
# 1. Create mirror registry (Quay mirror or oc-mirror)
oc-mirror --config imageset-config.yaml docker://quay.local:8443/ocp

# 2. Add ImageContentSourcePolicy to install-config.yaml
imageContentSources:
- mirrors:
  - quay.local:8443/ocp/openshift/release-images
  source: quay.io/openshift-release-dev/ocp-release
- mirrors:
  - quay.local:8443/ocp/openshift/release
  source: quay.io/openshift-release-dev/ocp-v4.0-art-dev

# 3. Add CA cert to additionalTrustBundle in install-config.yaml
additionalTrustBundle: |
  -----BEGIN CERTIFICATE-----
  <mirror registry CA>
  -----END CERTIFICATE-----
```

## Post-Install Validation

```bash
export KUBECONFIG=ocp-install/auth/kubeconfig

# 1. All nodes Ready
oc get nodes

# 2. All cluster operators Available, none Degraded
oc get co | grep -v "True.*False.*False"

# 3. All pods running
oc get pods --all-namespaces | grep -v "Running\|Completed"

# 4. Default StorageClass exists
oc get sc | grep default

# 5. Router accessible
curl -k https://console-openshift-console.apps.ocp.example.com

# 6. Image registry functional
oc get configs.imageregistry.operator.openshift.io cluster -o jsonpath='{.spec.managementState}'

# 7. etcd healthy
oc rsh -n openshift-etcd etcd-<master-node> etcdctl endpoint health --cluster
```
