# VMware Cloud Foundation Lifecycle

VCF upgrades are orchestrated entirely through SDDC Manager, which downloads lifecycle bundles from the VMware depot (or an offline bundle depot) and applies them in a strictly enforced sequence: SDDC Manager itself is updated first, followed by vCenter Server, then ESXi hosts (via parallel remediation), then NSX-T, and finally vSAN (in-place upgrade where applicable). Async patches allow individual component updates between full VCF version releases but must be validated against the VCF compatibility matrix before application. Bundle availability is checked automatically by SDDC Manager on a configured schedule, or manually triggered under Lifecycle Management > Bundle Management.

**Upgrade sequence:**
1. SDDC Manager (always first — gates all other upgrades)
2. vCenter Server (management domain, then VI domains)
3. ESXi hosts (host remediation per cluster, one cluster at a time)
4. NSX-T Manager cluster, then NSX Edge clusters
5. vSAN (firmware/driver updates via Hardware Compatibility List check)

| VCF Release | ESXi | vCenter | NSX-T | vSAN | End of General Support |
|---|---|---|---|---|---|
| 5.2 | 8.0 U3 | 8.0 U3 | 4.2 | 8.0 U3 | Check Broadcom lifecycle |
| 5.1 | 8.0 U2 | 8.0 U2 | 4.1 | 8.0 U2 | Check Broadcom lifecycle |
| 4.5 | 7.0 U3 | 7.0 U3 | 3.2 | 7.0 U3 | Check Broadcom lifecycle |
