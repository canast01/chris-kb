# Aria Operations Lifecycle

Aria Operations follows VMware's standard product lifecycle, with upgrades delivered and orchestrated via Aria Suite Lifecycle Manager (LCM) — manual upgrades outside LCM are not supported in multi-node deployments. The default data retention period is 6 months; extending it requires additional data node capacity. Management pack compatibility must be verified against the target Aria Operations version before upgrade. EOL dates are tracked in the Broadcom Product Lifecycle Matrix.

| Activity | Tool / Method |
|---|---|
| Upgrade | Aria Suite Lifecycle Manager (LCM) |
| Node expansion | LCM scale-out wizard |
| Data retention config | Admin > Global Settings > Retention |
| Management pack updates | Admin > Solutions > Upgrade |
| EOL tracking | Broadcom Product Lifecycle Matrix |
| Version compatibility | VMware Interoperability Matrix |
