# Superna Eyeglass Lifecycle

Eyeglass version compatibility with NetApp PowerScale OneFS versions must be validated before any upgrade — refer to the Superna compatibility matrix. The upgrade procedure involves downloading the new OVA, deploying it alongside the existing appliance, migrating configuration, and registering the new license. In-place upgrades may be supported in later versions — always verify against the release notes.

EOL for Eyeglass appliance versions is published on the Superna support portal. SyncIQ policy configuration changes on PowerScale (e.g., schedule or path changes) must be re-validated in Eyeglass after any OneFS upgrade to confirm policy detection and DR readiness scoring remains accurate.

| Stage | Action |
|---|---|
| Pre-upgrade | Validate Eyeglass–OneFS compatibility matrix; take config backup |
| Upgrade | Deploy new OVA, migrate configuration, register new license |
| Post-upgrade | Validate SyncIQ policy detection, DR readiness score, DNS sync |
| EOL tracking | Check Superna support portal quarterly |
| OneFS upgrade impact | Re-validate all SyncIQ policies in Eyeglass after OneFS upgrade |
