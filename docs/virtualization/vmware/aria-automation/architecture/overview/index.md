# Aria Automation — Architecture Overview

## Overview

Aria Automation (formerly vRealize Automation) is available as a **SaaS offering** or as an **on-premises appliance cluster**. The on-premises deployment is an appliance-based Kubernetes platform running microservices.

## Deployment Models

| Model | Description |
|-------|-------------|
| SaaS (Cloud) | VMware-hosted; no infrastructure to manage; connected via cloud extensibility proxy |
| On-Premises | One or three appliance cluster; self-managed; supports air-gap environments |

## On-Premises Cluster Topology

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

## Single-Node vs. Cluster

| Attribute | Single Node | 3-Node Cluster |
|-----------|-------------|----------------|
| HA | No — single point of failure | Yes — quorum-based HA |
| Use case | Lab / non-prod | Production |
| Load balancer | Not required | Required (VIP in front of 3 nodes) |
