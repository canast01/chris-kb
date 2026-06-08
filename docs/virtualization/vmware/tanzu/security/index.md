# Tanzu — Security

<div class="kb-summary">
Tanzu hardening — RBAC, network policies, pod security admission, OPA Gatekeeper, and container image scanning.
</div>

```text
┌─────────────────────────────────────── VMware Tanzu — Security ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    vSphere SSO and LDAP/AD integration for Kubernetes RBAC; namespace-scoped role bindings    │   │
│   │     Pod Security Admission: enforce Restricted/Baseline/Privileged policies per namespace     │   │
│   │           Network policies via NSX-T: micro-segmentation between pods and namespaces          │   │
│   │  Harbor image scanning: Trivy/Clair CVE scanning; admission webhook rejects vulnerable images │   │
│   │       mTLS between services via Tanzu Service Mesh (TSM); certificate rotation automated      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Authentication gates cluster access · RBAC scopes namespace permissions                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │      Workload Security      │   │
│   │         vSphere SSO         │  │        RBAC bindings        │  │       Pod Security Adm      │   │
│   │        LDAP/AD groups       │  │        Namespace RBAC       │  │        Network policy       │   │
│   │        OIDC provider        │  │       Service accounts      │  │        Image scanning       │   │
│   │       kubeconfig auth       │  │        Cluster roles        │  │          mTLS (TSM)         │   │
│   │        Cert rotation        │  │        OPA/Gatekeeper       │  │      Admission webhook      │   │
│   │        Audit logging        │  │         TMC policies        │  │       vSAN encryption       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Auth controls cluster access · RBAC scopes roles                                                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Auth       │   Access Ctrl    │    Workload Sec   │    Hardening     │      Audit       │   │
│   │   vSphere SSO    │    RBAC roles    │    Pod Sec Adm    │  CIS k8s bench   │  API audit log   │   │
│   │   LDAP groups    │  Namespace RBAC  │   Network policy  │  PSA Restricted  │   RBAC changes   │   │
│   │  OIDC provider   │  Cluster roles   │   Image scanning  │  Cert rotation   │ Harbor scan log  │   │
│   │ Service accounts │   OPA policies   │      mTLS TSM     │   Min-priv SA    │  Admission log   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ESXi hosts · RAM DIMMs · Network NICs · NSX-T fabric · vSAN encryption · CA infrastructure           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vSphere SSO        = vCenter Single Sign-On; identity source for Kubernetes RBAC in Tanzu            │
│  RBAC               = Kubernetes Role-Based Access Control; ClusterRole/Role bound to users or groups │
│  Pod Security Adm   = Kubernetes built-in policy enforcing Restricted/Baseline/Privileged per         │
│  Network policy     = Kubernetes resource restricting pod-to-pod traffic; enforced by NSX-T CNI       │
│  OPA/Gatekeeper     = Open Policy Agent admission controller; enforces custom policy constraints      │
│  Admission webhook  = Kubernetes API hook that validates or mutates resources before admission        │
│  Image scanning     = Harbor Trivy/Clair CVE scan; blocks deployment of images above severity         │
│  mTLS               = Mutual TLS between services; provided by Tanzu Service Mesh (Istio-based)       │
│  OIDC               = OpenID Connect; used by Pinniped to federate identity to Kubernetes API server  │
│  Service account    = Kubernetes identity for pods; scoped to namespace; used for API server auth     │
│  vSAN encryption    = Data-at-rest encryption for node disks; uses vCenter Key Provider (KMS)         │
│  Kubernetes audit   = API server audit log capturing all API calls; forwarded to Aria Logs for SIEM   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>SSO, LDAP, local accounts, and identity sources.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Roles, permissions, and least privilege access.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Data encryption and certificate management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines and compliance configuration.</span>
</a>

</div>
