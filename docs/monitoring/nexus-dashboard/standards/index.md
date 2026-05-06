# Nexus Dashboard Standards

The standard ND cluster size is 3 nodes for production environments; 5-node clusters are required when hosting multiple services (e.g., NDFC + NDI) at scale. Node hostnames follow the convention `nd-<site>-<number>` (e.g., `nd-dc1-01`). Fabrics onboarded to ND use the naming format `<site>-<fabric-type>-<number>` (e.g., `dc1-aci-01`). Alert policy priority tiers align with the operational severity model: P1 (Critical), P2 (Major), P3 (Minor), P4 (Warning). RBAC roles are scoped by function: Fabric Operators have write access to assigned fabrics; ReadOnly users have view-only access across all fabrics.

- Cluster size: 3 nodes standard, 5 nodes for HA/scale
- Node naming: `nd-<site>-<number>`
- Fabric naming: `<site>-<fabric-type>-<number>`
- Alert priority tiers: P1 Critical / P2 Major / P3 Minor / P4 Warning
- RBAC: Fabric Operator (scoped write), ReadOnly (global view)
