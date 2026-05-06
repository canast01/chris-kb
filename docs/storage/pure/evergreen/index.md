# Pure Storage Evergreen

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>HA topology, components, connectivity, and sizing.</span>
</a>

<a class="kb-card" href="standards/">
  <strong>Standards</strong>
  <span>Naming conventions, build baseline, and configuration checklist.</span>
</a>

<a class="kb-card" href="lifecycle/">
  <strong>Lifecycle</strong>
  <span>Version matrix, upgrade paths, EOL tracking, and refresh planning.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Daily checks, health monitoring, maintenance tasks, and runbooks.</span>
</a>

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>Command reference by category with syntax and examples.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts for daily checks, health, incident triage, and validation.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostic commands, log locations, and error codes.</span>
</a>

<a class="kb-card" href="integration/">
  <strong>Integration</strong>
  <span>VMware, backup tools, monitoring, authentication, and API integration.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Hardening checklist, RBAC, encryption, audit logging, and compliance.</span>
</a>

<a class="kb-card" href="vendor-support/">
  <strong>Vendor Support</strong>
  <span>Opening a case, information to collect, support portal, and SLA tiers.</span>
</a>

</div>

## Overview

Pure Storage Evergreen is a hardware subscription model for FlashArray and FlashBlade that bundles hardware, Purity software, support, and controller upgrades into a single ongoing subscription. The core design principle is non-disruptive controller refresh every three years — data stays in place, hosts remain connected, and there is no forklift replacement or data migration. The model spans three tiers: Evergreen//Forever (base hardware subscription with Every Modern controller upgrades), Evergreen//Flex (adds non-disruptive blade and capacity swap flexibility), and Evergreen//One (consumption-based STaaS, covered separately).

## Where It Fits

- Primary block and file storage for production VM and application workloads
- Environments requiring long-term platform continuity without data migration cycles
- Organisations replacing traditional CapEx storage refresh cycles with subscription-based OpEx
- Sites running ActiveCluster or replication that cannot tolerate disruptive upgrades
- Capacity expansion without downtime using Evergreen//Flex blade additions
- Colocation or remote sites where physical refresh logistics are a constraint

## Daily Checks

- Confirm no open hardware alerts in Pure1 or the FlashArray/FlashBlade GUI
- Review array capacity: used, provisioned, and data reduction ratio
- Validate replication pod and ActiveCluster status are healthy
- Check host connectivity — confirm no offline or degraded paths via `purehost list` or GUI
- Review Purity software version against Pure support-recommended range
- Confirm Pure1 phone-home connectivity (support tunnel active)
- Check snapshot schedule completion and retention policy compliance

## Health Commands

~~~bash
# List array hardware status and component health
purearray list --hardware

# Review active alerts on the array
purealert list

# Check capacity usage and data reduction
purearray list --space

# Verify host and host group path status
purehost list
purehostgroup list

# Review replication pod and ActiveCluster status
purepod list
purepod list --failover-preference

# Check Purity software version
purearray list

# Confirm Pure1 phone-home support tunnel status
# (Portal: Pure1 > Arrays > select array > Support > Phone Home)
~~~

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| Controller upgrade window missed | Subscription renewal not scheduled ahead of expiry | Contact Pure account team to schedule Ever Modern controller upgrade before subscription end date |
| Host path goes offline during controller upgrade | Multipath failover not validated pre-upgrade | Pre-validate host multipathing with `purehostconnection list`; confirm all hosts have redundant paths before upgrade starts |
| ActiveCluster mediator unreachable during upgrade | Network change or mediator misconfigured | Verify mediator IP connectivity and quorum before entering upgrade window |
| Replication pod sync lag after upgrade | Workload spike during upgrade window | Monitor pod sync status with `purepod list`; verify replication network bandwidth |
| Pure1 phone-home offline | Proxy change, firewall rule, or network reconfiguration | Confirm outbound access to Pure1 endpoints on port 443; check proxy settings in array GUI |
| Capacity alert at upgrade time | Snapshot growth or volume provisioning without cleanup | Review snapshot usage with `puresnapshot list --space`; expire or eradicate stale snapshots before upgrade |

## Operational Tasks

- Schedule Ever Modern controller upgrade with Pure support at least 30 days before subscription renewal date
- Plan and validate host multipathing before entering any controller upgrade window
- Validate ActiveCluster mediator and pod status before upgrade
- Confirm Purity software is within the upgrade-supported range (check Pure compatibility matrix)
- Review and clean up stale snapshots and destroyed volumes before capacity review
- Validate replication pod resume after upgrade completion
- Confirm all host paths are restored post-upgrade using `purehostconnection list`
- Update subscription documentation with new controller generation and renewal date

## Upgrade Notes

1. Confirm Purity software version is within the supported range for the target controller generation using Pure's compatibility matrix
2. Validate all host paths are redundant and multipathing is active on every connected host
3. Confirm ActiveCluster mediator is reachable and pods are in sync before upgrade window
4. Pause or validate replication schedules so lag does not trigger alerts during the upgrade
5. Engage Pure Support to schedule and lead the non-disruptive controller upgrade (Pure performs the swap)
6. Monitor host I/O during the upgrade using `purearray monitor` to confirm no latency impact
7. After upgrade, verify all hardware components are healthy, all host paths are restored, and replication pods have resumed

## Best Practices

- Schedule Ever Modern controller upgrades well before the subscription renewal date — do not let the window lapse
- Always upgrade Purity software to the recommended release before entering a controller upgrade window
- Validate host multipathing and fabric zoning before every upgrade; never proceed with single-path hosts
- Run controller upgrades during approved maintenance windows even though they are non-disruptive, to reduce risk
- Keep Pure1 phone-home active at all times so Pure Support has visibility and can provide proactive health alerts
- Document the current controller generation, subscription tier, and renewal date in your CMDB
- Review snapshot retention policies quarterly to prevent capacity bloat that can affect upgrade planning
- Engage your Pure account team quarterly to review subscription status, capacity trends, and upcoming upgrade eligibility
