# Aria Suite Lifecycle — Product Lifecycle

LCM must always be upgraded first before upgrading any managed Aria product; attempting to upgrade a product with an older LCM version is unsupported and will be blocked. Workspace ONE Access (Identity Manager) must be upgraded immediately after LCM and before any Aria Operations, Aria Automation, or Aria Log Insight upgrades. VMware publishes a product interoperability matrix that must be consulted before every upgrade cycle to confirm supported version combinations across the Aria portfolio.

| Product | Current GA | End of General Support | Upgrade Sequence Priority |
|---|---|---|---|
| Aria Suite Lifecycle | 8.x | Check Broadcom lifecycle page | 1 — always first |
| Workspace ONE Access | 3.3.x / 23.x | Check Broadcom lifecycle page | 2 — before all products |
| Aria Operations | 8.x | Check Broadcom lifecycle page | 3 |
| Aria Automation | 8.x | Check Broadcom lifecycle page | 4 |
| Aria Log Insight | 8.x | Check Broadcom lifecycle page | 5 |
| Aria Operations for Networks | 6.x | Check Broadcom lifecycle page | 6 |

**EOL tracking:** Subscribe to Broadcom lifecycle notifications and review the [VMware Product Lifecycle Matrix](https://lifecycle.vmware.com) quarterly.
