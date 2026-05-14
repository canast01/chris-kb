# Aria Automation — How It Works

## Overview

Aria Automation (formerly vRealize Automation) is available as a **SaaS offering** or an **on-premises appliance cluster**. The on-premises deployment is a Kubernetes-based microservices platform. All infrastructure provisioning flows through cloud templates (YAML IaC), projects, and cloud zones — Aria Automation resolves placement constraints and orchestrates provisioning without hardcoded infrastructure references.

## Deployment Models

| Model | Description |
|---|---|
| SaaS (Cloud) | VMware-hosted; no infrastructure to manage; connected via cloud extensibility proxy |
| On-Premises | 1 or 3 appliance cluster; self-managed; supports air-gap environments |

## Cluster Topology

```mermaid
graph TB
  CAT["Service Catalog\n(consumer portal)"] --> ORCH["Aria Automation Orchestrator\n(workflow engine)"]
  ORCH --> IAAS["IaaS Service\n(compute engine)"]
  IAAS --> VCTR["vCenter\n(VM provisioning)"]
  IAAS --> NSX_T["NSX\n(network provisioning)"]
  IAAS --> CLOUDS["Public Cloud\nAWS · Azure · GCP"]
  ADMIN(["Cloud Admin"]) -->|"UI / API"| CAT
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  class CAT,ORCH,IAAS ctrl
  class VCTR,NSX_T mgmt
  class ADMIN host
  class CLOUDS cloud
```

## Single Node vs. 3-Node Cluster

| Attribute | Single Node | 3-Node Cluster |
|---|---|---|
| HA | No — single point of failure | Yes — quorum-based HA |
| Use case | Lab / non-prod | Production |
| Load balancer | Not required | Required (L4/L7 VIP in front of 3 nodes) |

## Core Services

| Service | Purpose |
|---|---|
| Automation Assembler | Cloud template (YAML IaC) authoring and resource provisioning |
| Service Broker | Self-service catalog — exposes templates to end users via projects |
| Event Broker | Internal event bus — routes lifecycle events to ABX/Orchestrator subscriptions |
| Orchestrator (embedded vRO) | Workflow engine for Day-2 operations and approval routing |
| Automation Pipelines | CI/CD pipeline engine triggered from Git events |
| PostgreSQL | Deployment state, catalog definitions, event log |
| RabbitMQ | Async messaging between microservices |
| Kubernetes | Container orchestration for all microservices (managed by appliance) |
| Nginx / Envoy | HTTPS ingress and load balancing between microservice endpoints |

## Kubernetes Namespaces (Diagnostics)

| Namespace | Services |
|---|---|
| `prelude` | Core services: assembler, catalog, event-broker |
| `vro` | Embedded vRealize Orchestrator |
| `saltstack` | Automation Config (SaltStack) |
| `pipeline` | Automation Pipelines (Code Stream) |

```bash
kubectl get pods -n prelude
kubectl logs -n prelude -l app=assembler --tail=100
kubectl describe pod -n prelude <pod-name>
```

## Cloud Account Types

| Cloud Account | Managed Resources |
|---|---|
| vCenter (vSphere) | VMs, networks, datastores, clusters |
| NSX-T | Overlay segments, security groups, load balancers |
| AWS | EC2, VPC, S3 |
| Azure | VMs, VNets, storage |
| GCP | Compute Engine, VPC |
| Kubernetes | Pod deployments, services |

## Appliance Sizing

| Size | vCPUs | RAM | Disk | Deployments/day |
|---|---|---|---|---|
| Small (1 node) | 8 | 32 GB | 100 GB | Up to 100 |
| Medium (3 nodes) | 16 per node | 48 GB per node | 100 GB per node | Up to 500 |
| Large (3 nodes) | 24 per node | 64 GB per node | 150 GB per node | 500+ |

## Network Ports

| Port | Protocol | Direction | Purpose |
|---|---|---|---|
| 443 | TCP | Inbound | Web UI and REST API |
| 22 | TCP | Inbound | SSH admin access |
| 5480 | TCP | Inbound | VAMI appliance management |
| 443 | TCP | Outbound | vCenter, NSX, Orchestrator, VIDM APIs |
| 5432 | TCP | Cluster-internal | PostgreSQL replication |
| 5671/5672 | TCP | Cluster-internal | RabbitMQ messaging |

## Event Broker Topics (ABX / Extensibility)

| Event Topic | When It Fires |
|---|---|
| `Deployment.Provision.Post` | After all resources provisioned successfully |
| `Deployment.Provision.Pre` | Before provisioning (use for validation) |
| `Deployment.Destroy.Post` | After deployment deleted |
| `Deployment.Resize.Post` | After a VM resize Day-2 action |
