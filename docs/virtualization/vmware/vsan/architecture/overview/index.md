# vSAN — Architecture Overview

## Cluster Topology

```mermaid
graph TB
  H1["ESXi-01\nCache NVMe + Capacity SSD"] & H2["ESXi-02\nCache NVMe + Capacity SSD"] & H3["ESXi-03\nCache NVMe + Capacity SSD"] --> VSANNET["vSAN VMkernel Network\n25 / 10 GbE dedicated"]
  VSANNET --> DS[("vSAN Datastore\nFTT policy — RAID-1 / RAID-5 / RAID-6")]
  DS --> VM(["VM Workloads"])
  VCSA["vCenter\n(vSAN management)"] --> VSANNET
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef store fill:#1d4ed8,stroke:#1e40af,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  class H1,H2,H3 ctrl
  class VSANNET net
  class DS store
  class VM host
  class VCSA mgmt
```

## Overview

vSAN pools local disks across ESXi hosts to create a distributed shared datastore. Compute and storage run on the same ESXi hosts, eliminating the need for an external SAN or NAS. The vSAN datastore is presented as a single shared storage namespace to all hosts in the cluster.

vSAN is policy-driven: each VM's storage characteristics (availability, performance, capacity) are defined by a VM Storage Policy assigned at provisioning time.
