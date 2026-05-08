# Aria Automation — Components

## Core Service Components

Aria Automation (formerly vRealize Automation) runs as a Kubernetes-based microservices platform on a Linux appliance. The key services and their functions:

| Service | Purpose |
|---|---|
| **Automation Assembler** | Cloud template (blueprint) authoring, IaC in YAML, resource provisioning |
| **Service Broker** | Self-service catalog — exposes content to end users via projects |
| **Automation Pipelines** | CI/CD pipeline execution engine (formerly Code Stream) |
| **Automation Config** | GitOps-based configuration management (formerly SaltStack Config) |
| **Orchestrator** | Workflow engine for Day-2 actions and automation logic (embedded vRO) |
| **PostgreSQL** | Backend relational database for deployment state, catalog, and event log |
| **RabbitMQ** | Internal messaging bus between microservices |
| **Kubernetes (K8s)** | Container orchestration for all microservices (managed by the appliance) |
| **Nginx / Envoy** | Ingress proxy for UI and API routing |

---

## Deployment Topology

| Deployment | Nodes | Use Case |
|---|---|---|
| Standalone (small) | 1 appliance | Lab, PoC, development |
| Clustered (HA) | 3 appliances | Production — active/active with shared Postgres |
| Scaled-out | 3+ appliances | Production with high request volume |

For production, a 3-node cluster is the minimum — it provides HA for all services and survives a single node failure.

---

## Network Ports

| Port | Protocol | Direction | Purpose |
|---|---|---|---|
| 443 | TCP | Inbound | Web UI and REST API |
| 22 | TCP | Inbound | SSH admin access |
| 5480 | TCP | Inbound | VAMI (appliance management) |
| 443 | TCP | Outbound | vCenter API (cloud account) |
| 443 | TCP | Outbound | NSX-T Manager API |
| 443 | TCP | Outbound | Aria Orchestrator |
| 443 | TCP | Outbound | VIDM/SSO |
| 5432 | TCP | Cluster-internal | PostgreSQL replication |
| 5671/5672 | TCP | Cluster-internal | RabbitMQ messaging |

---

## Kubernetes Pod Namespaces

Aria Automation microservices run in Kubernetes namespaces on each appliance. Key namespaces for diagnostics:

| Namespace | Services |
|---|---|
| `prelude` | Core Aria Automation services (assembler, catalog, event-broker) |
| `vro` | Embedded vRealize Orchestrator |
| `saltstack` | Automation Config (SaltStack) |
| `pipeline` | Automation Pipelines (Code Stream) |

```bash
# List all namespaces
kubectl get namespaces

# List all pods in the prelude namespace
kubectl get pods -n prelude

# Get logs for a specific service
kubectl logs -n prelude -l app=assembler --tail=100

# Describe a failing pod for events and error messages
kubectl describe pod -n prelude <pod-name>
```

---

## Cloud Account Types

Cloud accounts define the connections to cloud and infrastructure endpoints. Aria Automation uses cloud accounts to discover resources and target deployments.

| Cloud Account Type | Protocol | Managed Resources |
|---|---|---|
| vCenter (vSphere) | vCenter API (443) | VMs, networks, datastores, clusters |
| NSX-T | NSX Manager API (443) | Overlay segments, security groups, load balancers |
| VMware Cloud on AWS | VMware Cloud API | SDDC VMs and networks |
| AWS | AWS API | EC2, VPC, S3 |
| Azure | Azure Resource Manager API | VMs, VNets, storage |
| GCP | GCP API | Compute Engine, VPC |
| Kubernetes | Kubernetes API | Pod deployments, services |

Configure cloud accounts: **Infrastructure → Connections → Cloud Accounts → Add**.

---

## Appliance Resource Requirements

| Size | vCPUs | RAM | Disk | Supported Deployments/day |
|---|---|---|---|---|
| Small (1 node) | 8 | 32 GB | 100 GB | Up to 100 |
| Medium (3 nodes) | 16 per node | 48 GB per node | 100 GB per node | Up to 500 |
| Large (3 nodes) | 24 per node | 64 GB per node | 150 GB per node | 500+ |
