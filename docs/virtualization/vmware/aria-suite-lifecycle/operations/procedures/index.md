# Aria Suite Lifecycle — Procedures

## Deploy a New Aria Product

1. LCM → Lifecycle Operations → Environments → select or create environment
2. Click "Add Product"
3. Select product, version, and deployment size (Medium/Large)
4. Provide vCenter target: cluster, datastore, network, IP addresses, hostnames, admin password (stored in LCM Locker)
5. LCM runs pre-checks (DNS, NTP, vCenter connectivity) — all must pass
6. Click Deploy — monitor via the workflow progress screen
7. Post-deployment: validate product UI is accessible and health shows green in LCM

## Trigger a Product Upgrade

1. LCM → Lifecycle Operations → Environments → click the product
2. Click "Upgrade" — LCM presents compatible target versions
3. Review pre-checks: all must pass before proceeding
4. Click "Start Upgrade" — LCM takes snapshots, performs upgrade, validates post-state
5. Monitor: Lifecycle Operations → Requests

If upgrade fails mid-way, LCM provides a "Rollback" option that reverts from snapshots.
