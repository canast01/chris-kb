# Nexus Dashboard Architecture

Cisco Nexus Dashboard (ND) is a centralised operations platform for Cisco ACI and NX-OS fabrics, providing a unified management plane for fabric visibility, health monitoring, and policy orchestration. A standard ND cluster consists of 3 nodes (physical or virtual) for production deployments; 5 nodes are required for higher availability or scale. Services — including Nexus Dashboard Fabric Controller (NDFC) and Nexus Dashboard Insights (NDI) — run as microservices on top of the ND platform, independently licensed and deployed. Nodes communicate over a dedicated cluster network and present a single virtual IP for management access.

| Component | Role |
|---|---|
| ND Master Node | Cluster management, API gateway, UI |
| ND Worker Nodes | Workload distribution for ND services |
| NDFC (Fabric Controller) | Fabric policy management, provisioning (replaces DCNM) |
| NDI (Insights) | Fabric health, anomaly detection, flow telemetry |
| ACI APIC | Integrated controller for ACI fabric policy |
