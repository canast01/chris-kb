# Dell VPLEX — Integrations

> Integration with other platforms and external systems.

## Backend Storage Arrays

VPLEX virtualises storage volumes from heterogeneous backend arrays. Supported backend arrays include:

- Dell PowerMax / VMAX
- Dell Unity XT
- Dell PowerStore
- Third-party arrays (verify compatibility with the Dell VPLEX Compatibility Matrix)

VPLEX back-end FC ports zone to backend array ports. VPLEX discovers unclaimed storage volumes and presents them as VPLEX storage volumes for use in virtual volume provisioning.

## VMware vSphere

VPLEX integrates with VMware vSphere environments:

- Virtual volumes are presented to ESXi hosts via VPLEX front-end FC ports
- VPLEX Metro enables vSphere HA and vMotion across Metro sites using the same distributed virtual volume
- VMware VASA provider is available for vVols support on compatible VPLEX configurations
- Verify ESXi host multipath driver compatibility with the Dell VPLEX Compatibility Matrix before upgrades

## RecoverPoint (VPLEX Geo)

VPLEX Geo uses Dell RecoverPoint for asynchronous replication between sites beyond Metro RTT limits:

- RecoverPoint splitters are integrated with VPLEX directors
- Asynchronous replication provides DR capability with configurable RPO
- Not active-active; volumes are active on one site at a time in Geo mode
- Failover requires an orchestrated RecoverPoint failover procedure

## Unisphere for VPLEX

Unisphere for VPLEX provides a web-based management interface as an alternative to `vplexcli`:

- Dashboard view of cluster health, director status, and distributed device state
- Storage view and consistency group management
- Alert monitoring and notification configuration
- Access via browser: `https://<VMS_IP>/`

## CloudIQ / Dell APEX AIOps

VPLEX can be integrated with Dell CloudIQ / APEX AIOps for proactive health monitoring and predictive analytics. Configure under VMS settings to enable telemetry upload to the Dell cloud.
