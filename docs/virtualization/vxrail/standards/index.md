# VxRail Standards

Node naming follows the convention `site-vxr-NN` (e.g., `lon-vxr-01`) to ensure consistent identification across sites and CMDB records. Cluster sizing requires a minimum of 3 nodes to satisfy the FTT=1 vSAN storage policy, with 4 nodes recommended for maintenance window resilience. All firmware versions must align with the VxRail Hardware Compatibility List (HCL) before any lifecycle operation.

| Standard | Value |
|---|---|
| Node naming | `site-vxr-NN` |
| Minimum cluster size | 3 nodes (FTT=1) |
| Recommended minimum | 4 nodes (maintenance safety) |
| vSAN policy — production | FTT=1 RAID-5 (capacity) or RAID-1 (performance) |
| vSAN policy — critical | FTT=2 RAID-6 |
| Network VLANs | Management, vMotion, vSAN, VM traffic (separate per VLAN design) |
| Firmware baseline | Must match VxRail HCL for current cluster version |
