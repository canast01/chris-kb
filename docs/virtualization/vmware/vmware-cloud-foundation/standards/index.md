# VMware Cloud Foundation Standards

VCF deployments must adhere to strict naming and sizing standards to ensure SDDC Manager can successfully validate and manage all components throughout the lifecycle. Management domain hosts must meet vSAN Ready Node specifications with a minimum of 4 hosts, 10 GbE networking with separate management, vMotion, vSAN, and NSX overlay VMkernel adapters. Network pool naming follows `<datacenter>-<env>-pool-<purpose>` (e.g. `dc1-prod-pool-workload`), and all VCF component passwords must be 15+ characters with complexity meeting SDDC Manager's built-in policy.

**Management domain sizing minimums:**
| Component | Minimum | Recommended |
|---|---|---|
| ESXi hosts (management) | 4 | 6 |
| vSAN disk groups per host | 1 | 2 |
| Management VM NIC speed | 10 GbE | 25 GbE |
| SDDC Manager vCPU | 4 | 8 |
| SDDC Manager RAM | 16 GB | 24 GB |

**Naming convention:**
- SDDC Manager: `sddc-mgr-<env>.<domain>`
- vCenter: `vc-<domain-name>-<env>.<domain>`
- NSX Manager: `nsx-<env>-<node#>.<domain>`
- ESXi hosts: `esxi-<rack>-<unit>.<domain>`
