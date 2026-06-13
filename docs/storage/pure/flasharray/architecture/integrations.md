---
tags:
  - architecture
  - pure
---
# FlashArray — Integrations


<div class="kb-summary">
Integrations reference covering VMware Integration, Backup Integration, Pure1 Monitoring, Authentication, REST API.
</div>

```text
┌──────────────────────────────────── Pure FlashArray Integrations ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        FlashArray Integration Ecosystem — VMware, Kubernetes, Backup, Cloud, Automation       │   │
│   │          VMware: VASA/VAAI plugin · vVols datastore · SPBM policy-driven provisioning         │   │
│   │        Kubernetes: Pure Service Orchestrator (PSO) / Portworx; dynamic PVC provisioning       │   │
│   │           Backup: Veeam, Commvault, Veritas via snapshot-based offload via Pure APIs          │   │
│   │       Automation: Ansible collection, Terraform provider, REST API v2 for all operations      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Pure REST API v2 is the integration backbone — all plugins and tools consume it                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      VMware Integration     │  │   Kubernetes / Containers   │  │     Backup + Automation     │   │
│   │  VASA: storage policy mgmt  │  │  PSO: dynamic PVC on-demand │  │  Veeam: snap-based offload  │   │
│   │   VAAI: HW-accelerated ops  │  │ CSI driver: standard K8s API│  │  Commvault: snap management │   │
│   │    vVols: per-VM volumes    │  │Portworx: data services layer│  │    purestorage.flasharray   │   │
│   │   SPBM: QoS per datastore   │  │ StatefulSet persistent store│  │ Terraform: volume lifecycle │   │
│   │   SRM: site recovery plans  │  │  Multi-attach: RWX volumes  │  │  REST v2: token auth + JSON │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    All integrations leverage REST API · VMware via VASA/VAAI · K8s via CSI/PSO                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   VMware Setup   │    K8s Setup     │   Backup Config   │     REST API     │    Automation    │   │
│   │Install VASA plug │ Deploy PSO helm  │ Register array IP │   GET /arrays    │  ansible-galaxy  │   │
│   │Create vVol store │Set storage class │  API token creds  │  POST /volumes   │  terraform init  │   │
│   │SPBM policy assign│ Test dynamic PVC │ Snapshot schedule │   PATCH /hosts   │ pureuser API add │   │
│   │SRM plugin config │  Verify PV bind  │   Offload verify  │ DELETE /volumes  │ Idempotent runs  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  FlashArray controllers · ESXi hosts · K8s worker nodes · Backup media server · IP/FC SAN fabric      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VASA          = vSphere API for Storage Awareness; allows vSphere to query array capabilities        │
│  VAAI          = vSphere API for Array Integration; offloads clone, zero, lock ops to array HW        │
│  vVols         = Virtual Volumes; per-VM volume objects managed directly by FlashArray                │
│  SPBM          = Storage Policy-Based Management; assigns QoS and protection to VMs by policy         │
│  PSO           = Pure Service Orchestrator; Kubernetes dynamic storage provisioner for Pure arrays    │
│  CSI           = Container Storage Interface; standard Kubernetes block/file storage API              │
│  Portworx      = Pure-owned container data platform; distributed storage layer for K8s workloads      │
│  SRM           = Site Recovery Manager; VMware DR orchestration using Pure replication snapshots      │
│  REST v2       = Pure FlashArray REST API version 2; JSON, token auth, full CRUD for all objects      │
│  Ansible coll  = purestorage.flasharray Galaxy collection; modules for volumes, hosts, PGs            │
│  Terraform     = HashiCorp IaC; purestorage/flasharray provider for declarative volume management     │
│  API token     = Authentication credential for REST and automation; scoped to array user role         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────── Pure FlashArray Integrations ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        FlashArray Integration Ecosystem — VMware, Kubernetes, Backup, Cloud, Automation       │   │
│   │          VMware: VASA/VAAI plugin · vVols datastore · SPBM policy-driven provisioning         │   │
│   │        Kubernetes: Pure Service Orchestrator (PSO) / Portworx; dynamic PVC provisioning       │   │
│   │           Backup: Veeam, Commvault, Veritas via snapshot-based offload via Pure APIs          │   │
│   │       Automation: Ansible collection, Terraform provider, REST API v2 for all operations      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Pure REST API v2 is the integration backbone — all plugins and tools consume it                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      VMware Integration     │  │   Kubernetes / Containers   │  │     Backup + Automation     │   │
│   │  VASA: storage policy mgmt  │  │  PSO: dynamic PVC on-demand │  │  Veeam: snap-based offload  │   │
│   │   VAAI: HW-accelerated ops  │  │ CSI driver: standard K8s API│  │  Commvault: snap management │   │
│   │    vVols: per-VM volumes    │  │Portworx: data services layer│  │    purestorage.flasharray   │   │
│   │   SPBM: QoS per datastore   │  │ StatefulSet persistent store│  │ Terraform: volume lifecycle │   │
│   │   SRM: site recovery plans  │  │  Multi-attach: RWX volumes  │  │  REST v2: token auth + JSON │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    All integrations leverage REST API · VMware via VASA/VAAI · K8s via CSI/PSO                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   VMware Setup   │    K8s Setup     │   Backup Config   │     REST API     │    Automation    │   │
│   │Install VASA plug │ Deploy PSO helm  │ Register array IP │   GET /arrays    │  ansible-galaxy  │   │
│   │Create vVol store │Set storage class │  API token creds  │  POST /volumes   │  terraform init  │   │
│   │SPBM policy assign│ Test dynamic PVC │ Snapshot schedule │   PATCH /hosts   │ pureuser API add │   │
│   │SRM plugin config │  Verify PV bind  │   Offload verify  │ DELETE /volumes  │ Idempotent runs  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  FlashArray controllers · ESXi hosts · K8s worker nodes · Backup media server · IP/FC SAN fabric      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VASA          = vSphere API for Storage Awareness; allows vSphere to query array capabilities        │
│  VAAI          = vSphere API for Array Integration; offloads clone, zero, lock ops to array HW        │
│  vVols         = Virtual Volumes; per-VM volume objects managed directly by FlashArray                │
│  SPBM          = Storage Policy-Based Management; assigns QoS and protection to VMs by policy         │
│  PSO           = Pure Service Orchestrator; Kubernetes dynamic storage provisioner for Pure arrays    │
│  CSI           = Container Storage Interface; standard Kubernetes block/file storage API              │
│  Portworx      = Pure-owned container data platform; distributed storage layer for K8s workloads      │
│  SRM           = Site Recovery Manager; VMware DR orchestration using Pure replication snapshots      │
│  REST v2       = Pure FlashArray REST API version 2; JSON, token auth, full CRUD for all objects      │
│  Ansible coll  = purestorage.flasharray Galaxy collection; modules for volumes, hosts, PGs            │
│  Terraform     = HashiCorp IaC; purestorage/flasharray provider for declarative volume management     │
│  API token     = Authentication credential for REST and automation; scoped to array user role         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Generate an API token for a service account:**

```bash
# On the array CLI
pureadmin create --role array_admin svc-monitoring
pureadmin apitoken create svc-monitoring
# Copy the token and store in a secrets manager
```

**Common API calls:**

```bash
# Get array status
GET /api/2.x/arrays

# List volumes
GET /api/2.x/volumes

# List active alerts
GET /api/2.x/alerts?filter=state%3D%27open%27

# Get array capacity
GET /api/2.x/arrays?space=true
```

Full API reference: [Pure Storage API documentation](https://support.purestorage.com/bundle/m_fa_rest_api)
