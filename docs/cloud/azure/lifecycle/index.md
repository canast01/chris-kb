# Azure Lifecycle

VM OS images are sourced from Azure Marketplace and patched via Azure Update Manager on a monthly schedule aligned to Microsoft's Patch Tuesday, with production VMs updated in rolling waves. AKS clusters are supported for N-2 minor versions; clusters running an unsupported version must be upgraded within the 30-day deprecation window to remain eligible for support. Azure service retirements are tracked via Azure Updates and the Azure Portal's Retirement Workbook, and affected resources must be migrated before the announced retirement date.

| Component | Lifecycle Event | Cadence / Policy |
|---|---|---|
| VM OS images | Patch via Azure Update Manager | Monthly, Patch Tuesday + 1 week |
| AKS versions | Supported: N-2 minor versions | Upgrade within 30 days of deprecation notice |
| Azure service retirements | Track via Azure Updates | Migrate before retirement date; review monthly |
| Subscription decommissioning | Cancel → move resources → delete | 90-day hold after cancellation before permanent deletion |
| Resource group cleanup | Tag-based expiry for non-production | Reviewed quarterly; expired RGs deleted after 14-day notice |
